#!/usr/bin/env python3
"""Scrape stotras from greenmesg.org into slokabase.

Adds every greenmesg stotram that is not yet present in
``database/slokabase.db``.  For each stotram it writes:

* ``SongIndex`` -- name, short name, deity, author, description and
  ``other_links`` (page URL + dictionary URL + a reference to this script),
* ``Songs``     -- one row per verse: Devanagari (``sloka_hindi``), IAST
  (``sloka_eng``), word-to-word meanings (``synonyms``) and the English
  translation (``translation``).

Word-to-word meanings come from the per-stotram dictionary text file that
greenmesg serves for its "click a word" helper; the entry keys match the
page's ``showTT('key')`` word tokens exactly.  Devanagari is converted to
IAST with the ``IastFramework`` package, matching the existing rows.

This module lives in the ``slokabase.plugins.greenmesg`` Flask-blueprint
plugin.  It is a self-contained copy of the original standalone script, so
the original file under ``TODO_Addons/`` is left untouched.

Usage::

    python3 -m slokabase.plugins.greenmesg --plan          # list skip/missing
    python3 -m slokabase.plugins.greenmesg --dry-run --limit 5
    python3 -m slokabase.plugins.greenmesg                 # insert everything
    python3 -m slokabase.plugins.greenmesg --url https://greenmesg.org/stotras/shiva/shivashtakam.php

The same engine is also exposed through the ``/admin/greenmesg`` blueprint
(see :mod:`slokabase.plugins.greenmesg.views`).
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

BASE = "https://greenmesg.org"
# scraper.py sits at <repo>/slokabase/plugins/greenmesg/scraper.py
ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.insert(0, ROOT)
from slokabase.plugins import common as C  # noqa: E402  (shared importer infra)
DB_PATH = os.environ.get(
    "SLOKABASE_DB", os.path.join(ROOT, "database", "slokabase.db")
)
CACHE = os.environ.get("SLOKABASE_GM_CACHE", "/tmp/opencode/gm_cache")
LOG_PATH = os.environ.get(
    "SLOKABASE_GM_LOG", "/tmp/opencode/scrape_greenmesg.log"
)
SCRIPT_REF = "slokabase/plugins/greenmesg"
HEADERS = {"User-Agent": "SlokaBase-scraper/1.0 (greenmesg stotra import)"}
DELAY = 0.8

DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")

# Shared text helpers (single implementation in slokabase.plugins.common).
collapse = C.collapse
clean_html = C.clean_html
ascii_fold = C.ascii_fold
norm = C.norm
to_iast = C.to_iast
ParseError = C.ParseError

FEMALE_WORDS = {
    "durga", "lakshmi", "laxmi", "saraswati", "sarasvati", "sarawati", "parvati",
    "gauri", "bhuvaneshwari", "bhuvaneswari", "bhuvaneshvari", "kali", "kalika",
    "mahakali", "lalita", "tripurasundari", "sundari", "tara", "matangi",
    "dhumavati", "bagalamukhi", "bagala", "chinnamasta", "bhairavi", "kamala",
    "kamalatmika", "radha", "radhika", "sita", "sati", "shakti", "devi",
    "annapurna", "annapoorna", "mangala", "mangalye", "ganga", "gange", "yamuna",
    "gayatri", "narmada", "godavari", "kaveri", "tulasi", "tulsi", "meenakshi",
    "minakshi", "kamakshi", "sharada", "sarada", "chandika", "chandi", "ambika",
    "ambica", "bhavani", "shailaputri", "brahmacharini", "chandraghanta",
    "kushmanda", "skandamata", "katyayani", "kalaratri", "mahagauri",
    "siddhidatri", "shodashi", "rajarajeshwari", "mahalakshmi", "varahi",
    "vaishnavi", "brahmani", "maheshwari", "kaumari", "narasimhi", "aindri",
    "chamunda", "shakambhari", "banashankari", "pratyangira", "matrika",
    "shanti", "vidya", "medha", "dakshayani", "kanyakumari", "renuka",
    "bhoomi", "bhumi", "prithvi", "prthvi", "mohini",
}

STOP_WORDS = {
    "sri", "shri", "om", "sacred", "stotram", "stotra", "stuti", "stothram",
    "sthothram", "mantra", "ashtakam", "ashtaka", "ashtakam", "stavam", "stava",
    "suktam", "suprabhatam", "dhyanam", "pancharatnam", "panchakam",
    "sahasranama", "sahasranamam", "karavalambam", "vandana", "prarthana",
    "japa", "mala", "the", "of",
}

GENERIC_CATEGORIES = {
    "vedas", "upanishads", "gita", "gita_misc", "stotras",
    "others", "pilgrimages", "yajna",
}


class ParseError(Exception):
    pass


# --------------------------------------------------------------------------- #
# text helpers (shared impl in common; site stop-words stay local)
# --------------------------------------------------------------------------- #
def tokens(text: str) -> set:
    return C.tokens(text, STOP_WORDS)


def marker_number(text: str):
    m = re.search(r"॥\s*([०-९]{1,3})\s*॥", text or "")
    if not m:
        return None
    try:
        return int(m.group(1).translate(DEV_DIGITS))
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# http (shared impl in common, bound to this site's base/cache/headers)
# --------------------------------------------------------------------------- #
def cache_path(url: str) -> str:
    return C.cache_path(url, BASE, CACHE)


def fetch(session: requests.Session, url: str, optional: bool = False):
    return C.fetch(
        session, url, base=BASE, cache_dir=CACHE, headers=HEADERS,
        delay=DELAY, optional=optional,
    )


# --------------------------------------------------------------------------- #
# enumeration + existing-song matching
# --------------------------------------------------------------------------- #
def enumerate_urls(session: requests.Session) -> list:
    index = fetch(session, BASE + "/stotras/")
    soup = BeautifulSoup(index, "html.parser")
    urls = set()
    cats = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        direct = re.match(r"^/stotras/[a-z0-9_]+/[a-z0-9_]+\.php$", href)
        if direct:
            urls.add(BASE + href)
        cat = re.match(r"^/stotras/([a-z0-9_]+)/?$", href)
        if cat:
            cats.add(cat.group(1))
    for cat in sorted(cats):
        try:
            html = fetch(session, f"{BASE}/stotras/{cat}/")
        except ParseError as exc:
            log(f"  ! category {cat}: {exc}")
            continue
        for a in BeautifulSoup(html, "html.parser").find_all("a", href=True):
            m = re.match(r"^/stotras/[a-z0-9_]+/[a-z0-9_]+\.php$", a["href"])
            if m:
                urls.add(BASE + a["href"])
    return sorted(urls)


def load_existing(db: sqlite3.Connection) -> dict:
    return C.load_existing(db, r"greenmesg\.org(/stotras/[^\s\"']+?\.php)")


def match_existing(name: str, existing: dict):
    return C.match_existing(name, existing, STOP_WORDS)


# --------------------------------------------------------------------------- #
# page parsing
# --------------------------------------------------------------------------- #
def walk_body(body: Tag):
    """Yield simplified events in document order (see parse_page)."""
    def rec(node):
        for ch in node.children:
            if isinstance(ch, NavigableString):
                s = str(ch)
                if s.strip():
                    if s.strip().startswith("Meaning"):
                        yield ("meaning_start", None)
                    else:
                        yield ("text", s)
                continue
            if not isinstance(ch, Tag):
                continue
            cls = ch.get("class") or []
            if ch.name == "br":
                yield ("br", None)
            elif ch.name == "img":
                continue
            elif ch.name == "span" and "Sanskrit" in cls:
                yield ("sanc", ch)
            elif ch.name == "span" and "lnum" in cls:
                yield ("lnum", ch.get_text(strip=True))
            elif ch.name == "span" and "kword" in cls:
                yield ("kword", ch.get_text(" ", strip=True))
            elif ch.name == "span" and ("sword" in cls or "TooltipBox" in cls):
                continue
            elif ch.name == "b" and ch.get_text(strip=True).startswith("Meaning"):
                yield ("meaning_start", None)
            else:
                yield from rec(ch)
    yield from rec(body)


def fresh_line():
    return {"text": "", "words": []}


def snapshot(lines):
    out = []
    for line in lines:
        text = collapse(line["text"])
        if text or line["words"]:
            out.append({"text": text, "words": list(line["words"])})
    return out


def new_line(lines):
    if lines[-1]["text"].strip() or lines[-1]["words"]:
        lines.append(fresh_line())


def token_key(span: Tag):
    m = re.search(r"showTT\('([^']*)'\)", span.get("onclick", "") or "")
    return m.group(1) if m else None


def add_sanskrit(span: Tag, lines):
    for ch in span.children:
        if isinstance(ch, NavigableString):
            lines[-1]["text"] += str(ch)
            continue
        if not isinstance(ch, Tag):
            continue
        cls = ch.get("class") or []
        if ch.name == "br":
            new_line(lines)
        elif "Tooltip" in cls:
            text = ch.get_text("", strip=True)
            lines[-1]["text"] += text
            lines[-1]["words"].append((text, token_key(ch)))
        else:
            lines[-1]["text"] += ch.get_text()


def parse_label(label: str):
    m = re.match(r"\s*(\d+)(?:\.(\d+))?", label or "")
    if not m:
        return None, None
    return int(m.group(1)), int(m.group(2)) if m.group(2) else None


def parse_verse_markers(lines):
    groups, cur, any_marker = [], [], False
    for line in lines:
        cur.append(line)
        n = marker_number(line["text"])
        if n is not None:
            any_marker = True
            groups.append((cur, n))
            cur = []
    if not any_marker:
        return None
    if cur:
        if groups:
            groups[-1][0].extend(cur)
        else:
            groups.append((cur, None))
    return groups


def build_groups(block):
    """Return list of (verse_number, hindi_lines, meaning_texts)."""
    hindi, units = block["hindi"], block["units"]
    if not units:
        grouped = parse_verse_markers(hindi) or [(hindi, None)]
        return [(n, lines, []) for lines, n in grouped]

    labeled = OrderedDict()
    for u in units:
        labeled.setdefault(u["N"], []).append(u)

    if len(labeled) == 1:
        n, us = next(iter(labeled.items()))
        return [(n, hindi, [u["text"] for u in us])]

    if len(hindi) == len(labeled):
        return [
            (n, [hindi[i]], [u["text"] for u in us])
            for i, (n, us) in enumerate(labeled.items())
        ]

    grouped = parse_verse_markers(hindi)
    if grouped and len(grouped) == len(labeled):
        return [
            (n, lines, [u["text"] for u in us])
            for (lines, _), (n, us) in zip(grouped, labeled.items())
        ]

    n, us = next(iter(labeled.items()))
    return [(n, hindi, [u["text"] for u in units])]


def parse_page(html: str, url: str):
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", id="Container") or soup.find("div", id="ContentPane")
    if not container:
        raise ParseError("no #Container")
    h1 = container.find("h1")
    if not h1:
        raise ParseError("no <h1>")
    content = h1.parent
    h1_text = collapse(h1.get_text(" ", strip=True))
    name = re.sub(
        r"\s*-\s*(Sanskrit Text.*|In hindi with meaning.*|with English.*)$",
        "", h1_text, flags=re.I,
    ).strip() or h1_text
    # Multi-segment titles look like "<Deity> - <Stotra> - <incipit> - <suffix>".
    # The stotra name is usually the longest segment (ties -> earliest one).
    segments = [s for s in (collapse(s) for s in re.split(r"\s+-\s+", name)) if s]
    if len(segments) > 1:
        name = segments[max(
            range(len(segments)), key=lambda i: (len(segments[i]), -i)
        )]
    else:
        name = collapse(name) or h1_text

    body = None
    for div in content.find_all("div", recursive=False):
        if div.find("span", class_="Sanskrit"):
            body = div
            break
    if body is None:
        raise ParseError("no verse container")

    author_match = re.search(r"composed by[:\s\-]*([^\n]+)", content.get_text("\n"), re.I)
    author = collapse(author_match.group(1)) if author_match else None

    # The deity is the nearest preceding <strong> that is not the page title,
    # a "Xyz:" label, or site boilerplate.  Keep scanning past rejected ones
    # instead of stopping at the first <strong>.
    name_norm = norm(name)
    deity_raw = None
    scanned = 0
    for sib in body.previous_siblings:
        if not isinstance(sib, Tag):
            continue
        scanned += 1
        if scanned > 25:
            break
        if sib.name != "strong":
            continue
        txt = collapse(sib.get_text(" ", strip=True))
        if not txt or norm(txt) == name_norm or txt.endswith(":"):
            continue
        if "greenmesg" in ascii_fold(txt) or "." in txt:
            continue
        deity_raw = txt
        break

    pending = [fresh_line()]
    blocks = []
    mode = "hindi"          # hindi | meaning | end
    cur_unit = None

    for kind, value in walk_body(body):
        if kind == "sanc":
            if mode in ("meaning", "end"):
                mode = "hindi"
            add_sanskrit(value, pending)
        elif kind == "br":
            if mode == "hindi":
                new_line(pending)
        elif kind == "meaning_start":
            if mode == "hindi":
                blocks.append({"hindi": snapshot(pending), "units": []})
                pending = [fresh_line()]
            mode = "meaning"
            cur_unit = None
        elif kind == "text":
            text = value
            if mode == "hindi":
                if re.search(r"[A-Za-z]", text):
                    continue  # page's own roman transliteration
                pending[-1]["text"] += text
            elif mode == "meaning":
                if text.startswith("Note:") or "Translated by" in text or text.strip().startswith("Click"):
                    mode = "end"
                    continue
                if cur_unit is None:
                    cur_unit = {"N": None, "M": None, "text": ""}
                    blocks[-1]["units"].append(cur_unit)
                cur_unit["text"] += text
        elif kind == "lnum":
            if mode == "end":
                continue
            if mode != "meaning":
                if mode == "hindi":
                    blocks.append({"hindi": snapshot(pending), "units": []})
                    pending = [fresh_line()]
                mode = "meaning"
            n, m = parse_label(value)
            cur_unit = {"N": n, "M": m, "text": ""}
            blocks[-1]["units"].append(cur_unit)
        elif kind == "kword":
            if mode == "meaning":
                if cur_unit is None:
                    cur_unit = {"N": None, "M": None, "text": ""}
                    blocks[-1]["units"].append(cur_unit)
                sep = "" if not cur_unit["text"] or cur_unit["text"].endswith(" ") else " "
                cur_unit["text"] += sep + value

    trailing = snapshot(pending)
    if not blocks:
        grouped = parse_verse_markers(trailing) or [(trailing, None)]
        blocks = [{"hindi": lines, "units": []} for lines, _ in grouped]
    elif trailing:
        blocks.append({"hindi": trailing, "units": []})

    verses = []
    seq = 0
    for block in blocks:
        for n, hindi, meanings in build_groups(block):
            hindi = [ln for ln in hindi if ln["text"] or ln["words"]]
            if not hindi:
                continue
            seq += 1
            verses.append({
                "no": seq,
                "lines": hindi,
                "meanings": [collapse(m) for m in meanings if collapse(m)],
            })
    if not verses:
        raise ParseError("no verses parsed")

    category = url.split("/stotras/", 1)[1].split("/", 1)[0] if "/stotras/" in url else ""
    return {
        "name": name,
        "author": author,
        "deity": map_deity(deity_raw, category),
        "category": category,
        "verses": verses,
    }


def map_deity(raw, category):
    def category_fallback():
        return "" if category in GENERIC_CATEGORIES else category.replace("_", " ")

    if not raw:
        raw = category_fallback()
    raw = collapse(re.sub(r"\s*\(.*?\)", "", raw))
    if not raw:
        return None
    low = ascii_fold(raw)
    # "X Bhakta Y" (Y devotee of X) -> the deity is Y, e.g. Hanuman.
    m = re.search(r"\bbhakta\s+([A-Za-z]+)\s*$", raw, flags=re.I)
    if m:
        raw = m.group(1)
        low = ascii_fold(raw)
    # Word-boundary match so "Nandakumara" is not read as goddess "Nanda".
    female = low.startswith(("devi", "goddess")) or any(
        re.search(r"\b" + re.escape(w) + r"\b", low) for w in FEMALE_WORDS
    )
    core = re.sub(
        r"^(sri|shri|sriman|srimati|shrimati|lord|goddess|devi|bhagavan"
        r"|bhagwan|bhakta|param|para|mother|mata)\b\s*",
        "", raw, flags=re.I,
    ).strip()
    if not core:
        # raw was a bare honorific ("Devi") -> fall back to the category.
        core = category_fallback().replace("_", " ")
        if not core:
            return None
        low = ascii_fold(core)
        female = female or any(
            re.search(r"\b" + re.escape(w) + r"\b", low) for w in FEMALE_WORDS
        )
    # "Krishna & Vrindavana", "Rama And Ayodhya" -> first name wins.
    core = re.split(r"\s*(?:&|,|\band\b|\bor\b)\s*", core, flags=re.I)[0].strip() or core
    # "Suryadeva" -> "Surya" (only for known Vedic deva stems; "Vasudeva"
    # and friends must stay intact).
    if " " not in core:
        m = re.match(r"^([A-Za-z]+?)(deva|devi|dev)$", core, flags=re.I)
        if m and m.group(1).lower() in {
            "surya", "aditya", "savita", "savitr", "agni", "vayu",
            "indra", "varuna", "mitra", "soma", "rudra", "yama",
        }:
            core = m.group(1).capitalize()
    core = " ".join(
        "-".join(part.capitalize() for part in w.split("-"))
        for w in core.split()
    )
    return ("Goddess " if female else "Lord ") + core


# --------------------------------------------------------------------------- #
# dictionary (word-to-word) parsing
# --------------------------------------------------------------------------- #
def parse_dictionary(text: str) -> dict:
    out = {}
    for line in text.split("\n"):
        m = re.match(r"^(.*?)__(<span class=['\"]mword['\"].*)$", line)
        if not m:
            continue
        key, body = m.group(1), m.group(2)
        mw = re.search(r"<span class=['\"]mword['\"]>(.*?)</span>", body, re.S)
        mm = re.search(r"</span>\)\s*:\s*(.*?)(?:<br\s*/?>|$)", body, re.S)
        if not mm:
            mm = re.search(r"\):\s*(.*?)(?:<br\s*/?>|$)", body, re.S)
        subs = []
        for sm in re.finditer(
            r"<span class=['\"]mng['\"]>(.*?)</span>(.*?)(?:<br\s*/?>|$)", body, re.S
        ):
            sub_hindi = clean_html(sm.group(1))
            chunk = sm.group(2)
            tw = re.search(r"<span class=['\"]trans2['\"]>(.*?)</span>", chunk)
            mw2 = re.search(r"</span>\s*\)\s*=\s*(.*?)(?:<br\s*/?>|$)", chunk, re.S)
            if not mw2:
                mw2 = re.search(r"\)\s*=\s*(.*?)(?:<br\s*/?>|$)", chunk, re.S)
            if sub_hindi:
                subs.append({
                    "hindi": sub_hindi,
                    "word": clean_html(tw.group(1)) if tw else "",
                    "meaning": clean_html(mw2.group(1)) if mw2 else "",
                })
        out[key] = {
            "hindi": clean_html(mw.group(1)) if mw else "",
            "meaning": clean_html(mm.group(1)) if mm else "",
            "subs": subs,
        }
    return out


def build_synonym_line(line, dictionary):
    pairs = []
    for text, key in line["words"]:
        entry = dictionary.get(key)
        if not entry:
            continue
        for sub in entry["subs"]:
            if sub["meaning"]:
                word = to_iast(sub["hindi"])
                if word:
                    pairs.append(f"{word}={sub['meaning']}")
        main_iast = to_iast(text)
        if main_iast and entry["meaning"]:
            pairs.append(f"{main_iast}={entry['meaning']}")
    return "; ".join(pairs) + ";" if pairs else ""


# --------------------------------------------------------------------------- #
# db
# --------------------------------------------------------------------------- #
def build_rows(parsed, dictionary, page_url, dict_url):
    rows = []
    for verse in parsed["verses"]:
        hindi = "\n".join(ln["text"] for ln in verse["lines"])
        eng = "\n".join(to_iast(ln["text"]) for ln in verse["lines"])
        if dictionary:
            syn = [build_synonym_line(ln, dictionary) for ln in verse["lines"]]
            synonyms = "\n".join(syn) if any(syn) else None
        else:
            synonyms = None
        rows.append({
            "no": verse["no"],
            "sloka_hindi": hindi,
            "sloka_eng": eng,
            "synonyms": synonyms,
            "translation": "\n".join(verse["meanings"]) if verse["meanings"] else None,
        })

    links = [page_url]
    if dict_url and dictionary:
        links.append(dict_url)
    links.append(f"Scraped by {SCRIPT_REF}")

    return {
        "verses": rows,
        "other_links": "\n".join(links),
        "total_slokas": len(rows),
    }


def insert_song(db, parsed, data):
    return C.insert_song(
        db,
        name=parsed["name"],
        deity=parsed["deity"],
        author=parsed["author"],
        describtion="Translated by greenmesg.org",
        other_links=data["other_links"],
        verses=data["verses"],
        category=parsed["category"],
        log=log,
    )


# --------------------------------------------------------------------------- #
# logging + main
# --------------------------------------------------------------------------- #
log = C.make_log(LOG_PATH)


def dict_url_for(page_url: str) -> str:
    return page_url.replace("/stotras/", "/dictionary/stotras/").replace(".php", ".txt")


def load_urls(session, urls_file):
    if urls_file:
        with open(urls_file, encoding="utf-8") as fh:
            raw = [ln.strip() for ln in fh if ln.strip()]
        return sorted({u if u.startswith("http") else BASE + u for u in raw})
    return enumerate_urls(session)


# Pages that are interactive tools rather than stotra texts (no verses).
SKIP_PATTERN = re.compile(r"_japa\d*\.php$")
# One-off pages with no Sanskrit verse content (e.g. audio-only songs).
SKIP_PATHS = {
    "/stotras/kali/ekbar_birajo_go_maa.php",  # Bengali audio song
}


def process(session, db, url, existing, dry_run, force):
    path = url.replace(BASE, "")
    if SKIP_PATTERN.search(path) or path in SKIP_PATHS:
        log(f"  = skip (no verse content): {path}")
        return "skip"
    if not force:
        if path in existing["urls"]:
            log(f"  = skip (URL already in DB): {path}")
            return "skip"
        display = " ".join(re.split(r"[_/]", url.rsplit("/", 1)[-1][:-4])).title()
        hit = match_existing(display, existing)
        if hit:
            log(f"  = skip (matches DB '{hit}'): {path}")
            return "skip"

    html = fetch(session, url)
    parsed = parse_page(html, url)
    durl = dict_url_for(url)
    dictionary = None
    dtext = fetch(session, durl, optional=True)
    if dtext:
        dictionary = parse_dictionary(dtext)
        if not dictionary:
            dictionary = None
    data = build_rows(parsed, dictionary, url, durl)

    syn = "yes" if dictionary else "no"
    trans = "yes" if any(v["translation"] for v in data["verses"]) else "no"
    log(
        f"  + {parsed['name']}  | verses={len(parsed['verses'])}  deity={parsed['deity']}"
        f"  author={parsed['author']}  dict={syn}  translation={trans}"
    )
    if dry_run:
        return "dry"
    idx = insert_song(db, parsed, data)
    log(f"    -> inserted Songs#{idx}")
    return "insert"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DB_PATH)
    parser.add_argument("--urls-file", help="newline separated stotram URLs")
    parser.add_argument("--url", help="scrape a single stotram URL")
    parser.add_argument("--limit", type=int, default=0, help="stop after N inserts (0=all)")
    parser.add_argument("--dry-run", action="store_true", help="parse but do not write")
    parser.add_argument("--plan", action="store_true", help="only list skip/missing")
    parser.add_argument("--force", action="store_true", help="do not skip existing")
    args = parser.parse_args(argv)

    session = requests.Session()
    if args.url:
        urls = [args.url]
    else:
        urls = load_urls(session, args.urls_file)
    log(f"greenmesg stotra URLs: {len(urls)}")

    db = sqlite3.connect(args.db)
    existing = load_existing(db)

    if args.plan:
        matched = 0
        for url in urls:
            path = url.replace(BASE, "")
            display = " ".join(re.split(r"[_/]", url.rsplit("/", 1)[-1][:-4])).title()
            hit = path in existing["urls"] or match_existing(display, existing)
            if hit:
                matched += 1
                log(f"  = HAVE  {url}   ({hit})")
        log(f"missing to scrape: {len(urls) - matched}")
        db.close()
        return 0

    C.run_import(
        urls,
        lambda url: process(session, db, url, existing, args.dry_run, args.force),
        limit=args.limit,
        log=log,
    )
    db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
