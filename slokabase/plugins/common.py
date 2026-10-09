"""Shared infrastructure for SlokaBase importer plugins.

Site-specific plugins (``greenmesg``, ``kksongs``, ...) keep only their own
page parsing, URL enumeration and metadata mapping here; everything generic
-- text helpers, HTTP fetch with disk cache, DB dedupe matching, song
insertion and the import loop -- lives in this module so behaviour stays
identical across importers.
"""

from __future__ import annotations

import os
import re
import sqlite3
import time
import unicodedata

import requests
from bs4 import BeautifulSoup
from IastFramework import IAST

# common.py sits at <repo>/slokabase/plugins/common.py
ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
DB_PATH = os.environ.get(
    "SLOKABASE_DB", os.path.join(ROOT, "database", "slokabase.db")
)

IAST_CONV = IAST()

DEFAULT_STOP_WORDS = frozenset({
    "sri", "shri", "om", "sacred", "stotram", "stotra", "stuti", "stothram",
    "sthothram", "mantra", "ashtakam", "ashtaka", "ashtakam", "stavam", "stava",
    "suktam", "suprabhatam", "dhyanam", "pancharatnam", "panchakam",
    "sahasranama", "sahasranamam", "karavalambam", "vandana", "prarthana",
    "japa", "mala", "the", "of",
})


class ParseError(Exception):
    pass


# --------------------------------------------------------------------------- #
# text helpers
# --------------------------------------------------------------------------- #
def collapse(text: str) -> str:
    return " ".join((text or "").split())


def clean_html(fragment: str) -> str:
    return collapse(BeautifulSoup(fragment or "", "html.parser").get_text(" ", strip=True))


def ascii_fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    return text.lower()


def norm(text: str) -> str:
    s = ascii_fold(text)
    s = re.sub(r"[^a-z0-9]", "", s)
    for a, b in (("sh", "s"), ("ee", "i"), ("oo", "u")):
        s = s.replace(a, b)
    return s


def tokens(text: str, stop_words=DEFAULT_STOP_WORDS) -> set:
    out = set()
    for raw in re.split(r"[^A-Za-z0-9]+", ascii_fold(text)):
        if not raw or raw in stop_words:
            continue
        t = raw.replace("sh", "s").replace("ee", "i").replace("oo", "u")
        if len(t) >= 2:
            out.add(t)
    return out


def to_iast(text: str) -> str:
    text = (text or "").replace("_", "")
    try:
        out = IAST_CONV.to_iast(text)
    except Exception:
        return text
    return out.replace("\u02bc", "\u2019")  # modifier apostrophe -> right single quote


# --------------------------------------------------------------------------- #
# http fetch with disk cache
# --------------------------------------------------------------------------- #
def cache_path(url: str, base: str, cache_dir: str) -> str:
    key = re.sub(r"[^A-Za-z0-9]+", "_", url.replace(base, "")).strip("_")
    return os.path.join(cache_dir, key + ".html")


def fetch(session: requests.Session, url: str, *, base: str, cache_dir: str,
          headers: dict, delay: float = 0.8, optional: bool = False):
    path = cache_path(url, base, cache_dir)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    # Optional resources (e.g. per-song dictionaries, absent as HTTP 500):
    # single attempt, no retry sleeps -- a miss just means "no data".
    attempts = 1 if optional else 3
    last = None
    for attempt in range(attempts):
        try:
            resp = session.get(url, headers=headers, timeout=45)
            if resp.status_code == 200:
                os.makedirs(cache_dir, exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(resp.text)
                time.sleep(delay)
                return resp.text
            last = ParseError(f"HTTP {resp.status_code} for {url}")
        except Exception as exc:  # noqa: BLE001
            last = exc
        if not optional:
            time.sleep(1.5 * (attempt + 1))
    if optional:
        return None
    raise last if last else ParseError(f"failed: {url}")


# --------------------------------------------------------------------------- #
# existing-song matching ("check DB first, download only if missing")
# --------------------------------------------------------------------------- #
def load_existing(db: sqlite3.Connection, slug_pattern: str) -> dict:
    """Scan SongIndex once; return known URL slugs + matchable name entries.

    ``slug_pattern`` extracts the site path from an ``other_links`` URL, e.g.
    ``r"greenmesg\\.org(/stotras/[^\\s\\\"']+?\\.php)"``.
    """
    rows = db.execute("SELECT song_name, describtion, other_links FROM SongIndex").fetchall()
    url_slugs = set()
    entries = []  # (display_name, norm_name, token_set)
    for name, desc, links in rows:
        for m in re.findall(slug_pattern, links or ""):
            url_slugs.add(m)
        candidates = [("name", name)]
        dm = re.search(r"O[fn]{2}icial Name:\s*(.+)", desc or "")
        if dm:
            candidates.append(("official", collapse(dm.group(1))))
        for _, cand in candidates:
            if cand:
                entries.append((cand, norm(cand), tokens(cand)))
    return {"urls": url_slugs, "entries": entries}


def match_existing(name: str, existing: dict, stop_words=DEFAULT_STOP_WORDS):
    nn, nt = norm(name), tokens(name, stop_words)
    for display, dn, dt in existing["entries"]:
        if nn and nn == dn:
            return display
        if nt and nt == dt and max((len(t) for t in nt), default=0) >= 5:
            return display
        inter = nt & dt
        if len(inter) >= 2 and len(inter) >= 0.7 * len(nt | dt):
            return display
    return None


# --------------------------------------------------------------------------- #
# db insertion
# --------------------------------------------------------------------------- #
def insert_song(db, *, name: str, deity, author, describtion, other_links,
                verses: list, category: str = "", log=None) -> int:
    """Insert one SongIndex row + per-verse Songs rows.

    ``verses``: list of dicts with ``no, sloka_hindi, sloka_eng, synonyms,
    translation``.  Duplicate titles/short names are auto-disambiguated.
    """
    def _log(msg):
        if log is not None:
            log(msg)

    idx = db.execute("SELECT COALESCE(MAX(song_idx),0)+1 FROM SongIndex").fetchone()[0]
    if db.execute(
        "SELECT 1 FROM SongIndex WHERE song_name=?", (name,)
    ).fetchone():
        # Same title, different text -> qualify it.
        name = f"{name} ({category.replace('_', ' ').title()})" if category else f"{name} ({idx})"
        if db.execute(
            "SELECT 1 FROM SongIndex WHERE song_name=?", (name,)
        ).fetchone():
            name = f"{name} ({idx})"
        _log(f"    (title taken, using {name!r})")
    short = re.sub(r"[()]", "", "".join(name.split()))
    if db.execute(
        "SELECT 1 FROM SongIndex WHERE song_short_name=?", (short,)
    ).fetchone():
        dcore = "".join(re.sub(r"^(Lord|Goddess)\s+", "", deity or "").split())
        for cand in (
            short + dcore,
            short + category.capitalize().replace("_", "") if category else short,
            f"{short}{idx}",
        ):
            if cand != short and not db.execute(
                "SELECT 1 FROM SongIndex WHERE song_short_name=?", (cand,)
            ).fetchone():
                _log(f"    (short name taken, using {cand})")
                short = cand
                break
    db.execute(
        "INSERT INTO SongIndex (song_idx, song_name, song_short_name, sloka_statues,"
        " division, division_no, total_slokas, groups, devotion_god, author,"
        " describtion, other_links) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            idx, name, short, 1,
            None, 0, len(verses), None, deity, author,
            describtion, other_links,
        ),
    )
    for verse in verses:
        db.execute(
            "INSERT INTO Songs (song_idx, slokas_no, sloka_hindi, sloka_eng,"
            " synonyms, translation, purpot) VALUES (?,?,?,?,?,?,?)",
            (
                idx, verse["no"], verse["sloka_hindi"], verse["sloka_eng"],
                verse["synonyms"], verse["translation"], None,
            ),
        )
    db.commit()
    return idx


# --------------------------------------------------------------------------- #
# logging + import loop
# --------------------------------------------------------------------------- #
def make_log(log_path: str | None):
    def log(message):
        print(message, flush=True)
        if not log_path:
            return
        try:
            with open(log_path, "a", encoding="utf-8") as fh:
                fh.write(message + "\n")
        except OSError:
            pass
    return log


def run_import(urls: list, process_fn, *, limit: int = 0, progress_every: int = 25,
               log=None) -> dict:
    """Drive ``process_fn(url) -> 'insert'|'skip'|'dry'`` over URLs with a limit."""
    inserted = skipped = failed = 0
    for i, url in enumerate(urls, 1):
        try:
            result = process_fn(url)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            if log is not None:
                log(f"  ! FAILED {url}: {type(exc).__name__}: {exc}")
            continue
        if result == "insert":
            inserted += 1
        elif result == "skip":
            skipped += 1
        if limit and inserted >= limit:
            if log is not None:
                log(f"reached --limit {limit}")
            break
        if i % progress_every == 0 and log is not None:
            log(f"  ... progress {i}/{len(urls)}")
    summary = {"inserted": inserted, "skipped": skipped, "failed": failed}
    if log is not None:
        log(f"done: inserted={inserted} skipped={skipped} failed={failed}")
    return summary
