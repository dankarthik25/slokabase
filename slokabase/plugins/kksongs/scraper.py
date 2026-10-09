#!/usr/bin/env python3
"""Scrape songs from kksongs.org into slokabase.

Adds every kksongs song that is not yet present in
``database/slokabase.db``.  For each song it writes:

* ``SongIndex`` -- name, short name, tag-style ``devotion_god``
  (``krishna, vaishnava, <language>[, <lineage>]``), author, description
  (``Official Name: ...``) and ``other_links`` (lyrics + synonym URLs),
* ``Songs``     -- one row per verse: Devanagari from the ``_deva`` page
  (``sloka_hindi``, NULL when the song has no deva page), IAST lyrics
  (``sloka_eng``), word-to-word meanings from the synonym page
  (``synonyms``) and the English translation (``translation``).

DB-check-first: candidates are enumerated from the index pages (URL + title
only) and matched against ``SongIndex`` *before* any song page is
downloaded; only missing songs are fetched.

Usage::

    python3 -m slokabase.plugins.kksongs --plan          # list skip/missing
    python3 -m slokabase.plugins.kksongs --dry-run --limit 5
    python3 -m slokabase.plugins.kksongs                 # insert everything
    python3 -m slokabase.plugins.kksongs --url http://kksongs.org/songs/a/adharammadhuram.html

The same engine is also exposed through the ``/admin/kksongs`` blueprint
(see :mod:`slokabase.plugins.kksongs.views`).
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
import time

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

BASE = "http://kksongs.org"
# scraper.py sits at <repo>/slokabase/plugins/kksongs/scraper.py
ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.insert(0, ROOT)
from slokabase.plugins import common as C  # noqa: E402  (shared importer infra)

DB_PATH = os.environ.get(
    "SLOKABASE_DB", os.path.join(ROOT, "database", "slokabase.db")
)
CACHE = os.environ.get("SLOKABASE_KK_CACHE", "/tmp/opencode/kk_cache")
LOG_PATH = os.environ.get(
    "SLOKABASE_KK_LOG", "/tmp/opencode/scrape_kksongs.log"
)
SCRIPT_REF = "slokabase/plugins/kksongs"
HEADERS = {"User-Agent": "SlokaBase-scraper/1.0 (kksongs song import)"}
DELAY = 1.0

collapse = C.collapse
norm = C.norm
ParseError = C.ParseError

DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\x80-\x9f]")
VERSE_MARK_RE = re.compile(r"^\(\s*([0-9\u0966-\u096f]+)\s*\)$")
TEXT_MARK_RE = re.compile(r"^\(\s*([A-Za-z][A-Za-z ]*)\s*\)$")
REFRAIN_MARKS = frozenset({"refrain", "chorus", "interlude", "intro", "outro"})
TRANS_NUM_RE = re.compile(r"^([0-9\u0966-\u096f]+)\)\s*(.*)$")
LEAD_DASH_RE = re.compile(r"^[\s:;\u2013\u2014\u2012\-]+")

# Author lineage -> extra devotion_god tags (norm()ed substrings).
AUTHOR_TAGS = [
    (("prabhupada",), ["iskcon"]),
    (("bhaktisiddhanta",), ["iskcon", "gaudiya"]),
    (("bhaktivinoda",), ["iskcon", "gaudiya"]),
    (("narottama", "locana", "govinda"), ["gaudiya"]),
    (("rupagoswami", "sanatana", "jivagoswami", "raghunatha",
      "gopalabhatta", "krsnadasa", "vrndavana"), ["gaudiya"]),
    (("caitanya", "nitai", "nityananda", "advaita", "gadadhara",
      "srivasa"), ["gaudiya", "pancatattva"]),
    (("vallabhacarya", "vitthala"), ["pushti", "vallabha"]),
    (("suradasa", "mirabai", "tulasidasa", "tulsidas"), ["bhakti"]),
    (("jayadeva",), ["gitagovinda"]),
]


def clean(text: str) -> str:
    return collapse(CTRL_RE.sub("", text or ""))


def deva_int(num: str) -> int:
    return int(num.translate(DEV_DIGITS))


# --------------------------------------------------------------------------- #
# http (kksongs serves windows-1252; decode bytes explicitly)
# --------------------------------------------------------------------------- #
def fetch(session: requests.Session, url: str, optional: bool = False):
    path = C.cache_path(url, BASE, CACHE)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    attempts = 1 if optional else 3
    last = None
    for attempt in range(attempts):
        try:
            resp = session.get(url, headers=HEADERS, timeout=45)
            if resp.status_code == 200:
                text = resp.content.decode("windows-1252", errors="replace")
                os.makedirs(CACHE, exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
                time.sleep(DELAY)
                return text
            last = ParseError(f"HTTP {resp.status_code} for {url}")
        except Exception as exc:  # noqa: BLE001
            last = exc
        if not optional:
            time.sleep(1.5 * (attempt + 1))
    if optional:
        return None
    raise last if last else ParseError(f"failed: {url}")


# --------------------------------------------------------------------------- #
# enumeration (index pages only -- no song downloads yet)
# --------------------------------------------------------------------------- #
def enumerate_candidates(session: requests.Session) -> list:
    """Return [(song_url, index_title)] for the whole site, index pages only."""
    try:
        lyrics_html = fetch(session, BASE + "/lyrics.html")
    except ParseError as exc:
        log(f"  ! lyrics index: {exc}")
        lyrics_html = ""
    letters = sorted(set(
        re.findall(r"songs/(song_([a-z])\.html)", lyrics_html or "")
    ))
    index_urls = [BASE + "/songs/" + fn for fn, _ in letters] or [
        BASE + f"/songs/song_{c}.html" for c in "abcdefghijklmnopqrstuvwxyz"
    ]
    candidates = {}
    for index_url in index_urls:
        try:
            html = fetch(session, index_url)
        except ParseError as exc:
            log(f"  ! index {index_url}: {exc}")
            continue
        for a in BeautifulSoup(html, "html.parser").find_all("a", href=True):
            m = re.match(r"^(?:http://kksongs\.org)?(/songs/[a-z]/[a-z0-9_]+\.html)$",
                         a["href"])
            if not m:
                continue
            title = clean(a.get_text(" ", strip=True))
            candidates.setdefault(BASE + m.group(1), title or None)
    # Loose synonym pages at /synonym/ top level point at extra songs.
    try:
        syn_index = fetch(session, BASE + "/synonym/")
    except ParseError:
        syn_index = ""
    for m in re.findall(r'href="(/synonym/[a-z0-9_]+\.html)"', syn_index or ""):
        try:
            html = fetch(session, BASE + m)
        except ParseError:
            continue
        sm = re.search(
            r'href="(?:http://kksongs\.org)?(/songs/[a-z]/[a-z0-9_]+\.html)"', html)
        if sm:
            url = BASE + sm.group(1)
            if url not in candidates:
                pm = re.search(r"Song\s*Name:\s*<a[^>]*>(.*?)</a>", html, re.S | re.I)
                title = clean(pm.group(1)) if pm else None
                candidates[url] = title
    return sorted(candidates.items())


# --------------------------------------------------------------------------- #
# page parsing
# --------------------------------------------------------------------------- #
def _paras(soup: BeautifulSoup) -> list:
    return soup.find_all("p")


def parse_header(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    texts = [clean(p.get_text(" ", strip=True)) for p in _paras(soup)]
    out = {"name": None, "official": None, "author": None,
           "book": None, "language": None}

    def grab(label):
        pat = re.compile(r"^" + label + r"\s*:\s*(.+)$", re.I)
        for t in texts:
            m = pat.match(re.sub(r"\s+", " ", t))
            if m:
                val = collapse(m.group(1))
                return val if val.lower() != "none" else None
        return None

    # Some pages render the header's first letter as a drop-cap image,
    # leaving e.g. "ong Name:" in the text.
    out["name"] = grab(r"Song\s*Name") or grab(r"ong\s*Name")
    out["official"] = grab(r"Official\s*Name")
    out["author"] = grab(r"Author")
    out["book"] = grab(r"Book\s*Name")
    out["language"] = grab(r"Language")
    deva_url = syn_url = None
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/unicode/" in href and href.endswith("_deva.html"):
            deva_url = href if href.startswith("http") else BASE + href
        elif "/synonym/" in href and href.endswith(".html"):
            syn_url = href if href.startswith("http") else BASE + href
    out["deva_url"] = deva_url
    out["syn_url"] = syn_url
    return out


def _numbered_block(paras: list, start_label: str, end_labels: tuple,
                    numbered: bool):
    """Collect [(number, [raw_line, ...])] between header and end labels."""
    texts = [(p, clean(p.get_text("\n", strip=True))) for p in paras]
    start, lead = None, ""
    for i, (_, t) in enumerate(texts):
        s = t.strip()
        if s.rstrip(":").upper() == start_label:
            start = i
            break
        # Header may share its paragraph with the first content
        # ("TRANSLATION 1) ...", "LYRICS: (1)").
        lm = re.match(r"^([A-Za-z /]+?)\s*:\s*(.*)$", s)
        if lm and lm.group(1).strip().upper() == start_label:
            start, lead = i, lm.group(2).strip()
            break
        if s.upper().startswith(start_label + " ") or s.upper().startswith(start_label + "\u00a0"):
            start, lead = i, s[len(start_label):].lstrip(" :\u00a0")
            break
    if start is None:
        return []
    chunks = ([lead] if lead else []) + [t for _, t in texts[start + 1:]]
    verses, cur, seen_marker = [], None, False
    for t in chunks:
        if not t or t == "\xa0":
            continue
        up = t.strip().rstrip(":").upper()
        if any(up.startswith(e) for e in end_labels):
            break
        m = VERSE_MARK_RE.match(t.strip())
        if m:
            seen_marker = True
            cur = (deva_int(m.group(1)), [])
            verses.append(cur)
            continue
        tm2 = TEXT_MARK_RE.match(t.strip())
        if tm2 and tm2.group(1).strip().lower() in REFRAIN_MARKS:
            # "( refrain )" / "( chorus )" start an unnumbered verse.
            seen_marker = True
            cur = (f"R{len(verses)}", [])
            verses.append(cur)
            continue
        if numbered:
            tm = TRANS_NUM_RE.match(t.strip())
            if tm:
                seen_marker = True
                cur = (deva_int(tm.group(1)), [tm.group(2)])
                verses.append(cur)
                continue
        if cur is None:
            if numbered:
                cur = (1, [])
                verses.append(cur)
            else:
                continue
        for line in t.split("\n"):
            line = clean(line)
            if line:
                cur[1].append(line)
    got = [(n, [ln for ln in lines if ln]) for n, lines in verses if lines]
    if got or seen_marker:
        return got
    # Unnumbered single-stanza pages (e.g. translation-only songs): verse 1.
    lines = []
    for t in chunks:
        up = t.strip().rstrip(":").upper()
        if any(up.startswith(e) for e in end_labels):
            break
        for line in t.split("\n"):
            line = clean(line)
            if line:
                lines.append(line)
    return [(1, lines)] if lines else []


LYRICS_ENDS = ("WORD FOR WORD", "TRANSLATION", "REMARKS", "UPDATED")


def parse_lyrics(html: str) -> list:
    got = _numbered_block(
        _paras(BeautifulSoup(html, "html.parser")),
        "LYRICS", LYRICS_ENDS, numbered=False)
    if got:
        return got
    # No LYRICS header: verses run from the first marker to TRANSLATION.
    verses, cur = [], None
    for p in _paras(BeautifulSoup(html, "html.parser")):
        t = clean(p.get_text("\n", strip=True))
        if not t:
            continue
        up = t.strip().rstrip(":").upper()
        if cur is None:
            m = VERSE_MARK_RE.match(t.strip())
            tm2 = TEXT_MARK_RE.match(t.strip())
            if m:
                cur = (deva_int(m.group(1)), [])
                verses.append(cur)
            elif tm2 and tm2.group(1).strip().lower() in REFRAIN_MARKS:
                cur = (f"R{len(verses)}", [])
                verses.append(cur)
            continue
        if any(up.startswith(e) for e in LYRICS_ENDS):
            break
        m = VERSE_MARK_RE.match(t.strip())
        if m:
            cur = (deva_int(m.group(1)), [])
            verses.append(cur)
            continue
        tm2 = TEXT_MARK_RE.match(t.strip())
        if tm2 and tm2.group(1).strip().lower() in REFRAIN_MARKS:
            cur = (f"R{len(verses)}", [])
            verses.append(cur)
            continue
        for line in t.split("\n"):
            line = clean(line)
            if line:
                cur[1].append(line)
    return [(n, [ln for ln in lines if ln]) for n, lines in verses if lines]


def parse_deva(html: str) -> list:
    paras = [p for p in _paras(BeautifulSoup(html, "html.parser"))]
    got = _numbered_block(paras, "LYRICS",
                          ("WORD FOR WORD", "TRANSLATION", "REMARKS", "UPDATED"),
                          numbered=False)
    if got:
        return got
    # Fallback: some deva pages lack the LYRICS header; take all markers.
    verses, cur = [], None
    for p in paras:
        t = clean(p.get_text("\n", strip=True))
        if not t:
            continue
        up = t.strip().rstrip(":").upper()
        if up.startswith(("TRANSLATION", "REMARKS", "UPDATED", "SONG", "OFFICIAL",
                          "AUTHOR", "BOOK", "LANGUAGE", "HOME")):
            if cur is not None:
                break
            continue
        m = VERSE_MARK_RE.match(t.strip())
        if m:
            cur = (deva_int(m.group(1)), [])
            verses.append(cur)
            continue
        if cur is None:
            continue
        for line in t.split("\n"):
            line = clean(line)
            if line:
                cur[1].append(line)
    return [(n, [ln for ln in lines if ln]) for n, lines in verses if lines]


def parse_translation(html: str) -> list:
    raw = _numbered_block(
        _paras(BeautifulSoup(html, "html.parser")),
        "TRANSLATION", ("REMARKS", "UPDATED"), numbered=True)
    return [(n, collapse(" ".join(lines))) for n, lines in raw]


def parse_synonym(html: str) -> list:
    """Return [(verse_no, [(word, meaning), ...])] from a synonym page."""
    paras = _paras(BeautifulSoup(html, "html.parser"))
    texts = [clean(p.get_text(" ", strip=True)) for p in paras]
    start = next((i for i, t in enumerate(texts)
                  if t.strip().rstrip(":").upper() == "LYRICS"), None)
    if start is None:
        return []
    verses, cur = [], None
    for p in paras[start + 1:]:
        t = clean(p.get_text(" ", strip=True))
        if not t:
            continue
        up = t.strip().rstrip(":").upper()
        if up.startswith(("UPDATED", "REMARKS", "TRANSLATION")):
            break
        m = VERSE_MARK_RE.match(t.strip())
        if m:
            cur = (deva_int(m.group(1)), [])
            verses.append(cur)
            continue
        if cur is None:
            continue
        cur[1].extend(_syn_pairs(p))
    return [(n, pairs) for n, pairs in verses if pairs]


def _in_b(element) -> bool:
    return any(getattr(a, "name", None) == "b" for a in element.parents)


def _syn_pairs(p: Tag) -> list:
    # <b>word</b> markers nest at any depth (often inside font <span>s),
    # so walk all descendants: each outermost <b> starts a pair, and the
    # meaning is the text up to the next <b> (first ;-segment wins).
    pairs = []
    word, buf = None, []

    def flush():
        nonlocal word, buf
        if word:
            chunk = collapse("".join(buf)).split(";")[0]
            meaning = LEAD_DASH_RE.sub("", chunk).strip()
            if meaning:
                pairs.append((word, meaning))
        word, buf = None, []

    for el in p.descendants:
        if isinstance(el, Tag):
            if el.name == "b" and not _in_b(el):
                flush()
                word = clean(el.get_text(" ", strip=True))
                buf = []
        elif isinstance(el, NavigableString):
            if word is not None and not _in_b(el):
                buf.append(str(el))
    flush()
    return pairs


# --------------------------------------------------------------------------- #
# metadata mapping
# --------------------------------------------------------------------------- #
def make_tags(author, language) -> str:
    tags = ["krishna", "vaishnava"]
    na = norm(author or "")
    for keys, extra in AUTHOR_TAGS:
        if any(k in na for k in keys):
            tags.extend(extra)
    if language:
        lang = collapse(language).lower()
        if lang and lang not in tags:
            tags.append(lang)
    seen, out = set(), []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return ", ".join(out)


def build_rows(parsed: dict, deva: list, synonym: list) -> dict:
    # Positional alignment: lyrics/deva/translation/synonym blocks each run
    # in verse order (refrain first where present).  Lyrics drive the rows.
    lyrics = [lines for _, lines in parsed["lyrics"]]
    devas = [lines for _, lines in deva or []]
    trans = [text for _, text in parsed["translation"]]
    syns = [pairs for _, pairs in synonym or []]
    rows = []
    for i, lines in enumerate(lyrics):
        hindi = "\n".join(devas[i]) if i < len(devas) else None
        syn = None
        if i < len(syns) and syns[i]:
            s = "; ".join(f"{w} = {m}" for w, m in syns[i])
            syn = s + ";" if s else None
        rows.append({
            "no": i + 1,
            "sloka_hindi": hindi,
            "sloka_eng": "\n".join(lines),
            "synonyms": syn,
            "translation": f"{i + 1}) {trans[i]}" if i < len(trans) else None,
        })
    links = [f"lyrics link:  {parsed['page_url']} "]
    if parsed.get("syn_url"):
        links.append(f"  sysnonym link:  {parsed['syn_url']}")
    return {
        "verses": rows,
        "other_links": "\n".join(links),
        "total_slokas": len(rows),
    }


# --------------------------------------------------------------------------- #
# db-check-first pipeline
# --------------------------------------------------------------------------- #
log = C.make_log(LOG_PATH)


def load_existing(db: sqlite3.Connection) -> dict:
    return C.load_existing(db, r"kksongs\.org(/songs/[^\s\"']+?\.html)")


def match_existing(name: str, existing: dict):
    return C.match_existing(name, existing)


def process(session, db, url, existing, dry_run, force, title=None):
    path = url.replace(BASE, "")
    if not force:
        if path in existing["urls"]:
            log(f"  = skip (URL already in DB): {path}")
            return "skip"
        if title and match_existing(title, existing):
            log(f"  = skip (matches DB '{match_existing(title, existing)}'): {path}")
            return "skip"

    html = fetch(session, url)
    head = parse_header(html)
    if not head["name"]:
        raise ParseError("no Song Name header")
    if not force and not title:
        hit = match_existing(head["name"], existing)
        if hit:
            log(f"  = skip (matches DB '{hit}'): {path}")
            return "skip"

    lyrics = parse_lyrics(html)
    if not lyrics:
        if parse_translation(html):
            log(f"  = skip (translation-only page, no lyrics): {path}")
            return "skip"
        raise ParseError("no LYRICS verses")
    deva = []
    if head["deva_url"]:
        dhtml = fetch(session, head["deva_url"], optional=True)
        if dhtml:
            deva = parse_deva(dhtml)
    synonym = []
    syn_url = head["syn_url"]
    if syn_url:
        shtml = fetch(session, syn_url, optional=True)
        if shtml:
            synonym = parse_synonym(shtml)
    parsed = {"page_url": url, "syn_url": syn_url if synonym else None,
              "lyrics": lyrics,
              "translation": parse_translation(html)}
    data = build_rows(parsed, deva, synonym)
    if not data["verses"]:
        raise ParseError("no verses aligned")

    official = head["official"]
    tags = make_tags(head["author"], head["language"])
    describtion = f"Official Name: {official}" if official else None
    flags = (f"deva={'yes' if any(v['sloka_hindi'] for v in data['verses']) else 'no'}"
             f"  syn={'yes' if synonym else 'no'}"
             f"  trans={'yes' if any(v['translation'] for v in data['verses']) else 'no'}")
    log(f"  + {head['name']}  | verses={len(data['verses'])}  tags={tags}"
        f"  author={head['author']}  {flags}")
    if dry_run:
        return "dry"
    song = {"name": head["name"], "deity": tags, "author": head["author"],
            "category": ""}
    idx = C.insert_song(
        db, name=song["name"], deity=song["deity"], author=song["author"],
        describtion=describtion, other_links=data["other_links"],
        verses=data["verses"], category="", log=log,
    )
    # insert_song may qualify a duplicate title; keep describtion format.
    log(f"    -> inserted Songs#{idx}")
    return "insert"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DB_PATH)
    parser.add_argument("--urls-file", help="newline separated song URLs")
    parser.add_argument("--url", help="scrape a single song URL")
    parser.add_argument("--limit", type=int, default=0, help="stop after N inserts (0=all)")
    parser.add_argument("--dry-run", action="store_true", help="parse but do not write")
    parser.add_argument("--plan", action="store_true", help="only list skip/missing")
    parser.add_argument("--force", action="store_true", help="do not skip existing")
    args = parser.parse_args(argv)

    session = requests.Session()
    if args.url:
        candidates = [(args.url, None)]
    elif args.urls_file:
        with open(args.urls_file, encoding="utf-8") as fh:
            raw = [ln.strip() for ln in fh if ln.strip()]
        candidates = [(u if u.startswith("http") else BASE + u, None)
                      for u in sorted(set(raw))]
    else:
        log("enumerating kksongs index pages (no song downloads yet) ...")
        candidates = enumerate_candidates(session)
    log(f"kksongs song URLs: {len(candidates)}")

    db = sqlite3.connect(args.db)
    existing = load_existing(db)

    if args.plan:
        matched = 0
        for url, title in candidates:
            path = url.replace(BASE, "")
            hit = path in existing["urls"] or (title and match_existing(title, existing))
            if hit:
                matched += 1
                log(f"  = HAVE  {url}   ({hit if isinstance(hit, str) else title})")
        log(f"missing to scrape: {len(candidates) - matched}")
        db.close()
        return 0

    titles = dict(candidates)
    C.run_import(
        [u for u, _ in candidates],
        lambda url: process(session, db, url, existing, args.dry_run,
                            args.force, titles.get(url)),
        limit=args.limit,
        log=log,
    )
    db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
