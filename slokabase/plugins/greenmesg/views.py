"""Web UI + JSON API for the GreenMesg stotra importer.

Routes (all under ``/admin/greenmesg``):

* ``GET  /``        -- status page: DB stats, run form, recent log tail.
* ``GET/POST /run`` -- run the importer (dry-run by default).  For the full
  200+ page import prefer the CLI (``python -m slokabase.plugins.greenmesg``)
  since web requests time out on long runs.
* ``GET  /api/plan`` -- JSON ``{total, have, missing}`` for the URL list.
"""

from __future__ import annotations

import io
import os
import re
import sqlite3
from contextlib import redirect_stdout

import requests
from flask import Blueprint, jsonify, render_template, request

from . import scraper as engine

blueprint = Blueprint(
    "greenmesg",
    __name__,
    url_prefix="/admin/greenmesg",
    template_folder="templates",
)

# Upper bound for web-triggered runs; the full import belongs on the CLI.
WEB_LIMIT_CAP = 50


def _db_path() -> str:
    return os.environ.get(
        "SLOKABASE_DB", os.path.join(os.getcwd(), "database", "slokabase.db")
    )


def _db_stats() -> dict:
    db = sqlite3.connect(_db_path())
    try:
        total = db.execute("SELECT COUNT(*) FROM SongIndex").fetchone()[0]
        gm = db.execute(
            "SELECT COUNT(*) FROM SongIndex WHERE other_links LIKE '%greenmesg.org%'"
        ).fetchone()[0]
        verses = db.execute("SELECT COUNT(*) FROM Songs").fetchone()[0]
    finally:
        db.close()
    return {"songs": total, "greenmesg_songs": gm, "verses": verses}


def _log_tail(n: int = 30) -> str:
    try:
        with open(engine.LOG_PATH, encoding="utf-8", errors="replace") as fh:
            return "".join(fh.readlines()[-n:])
    except OSError:
        return "(no log yet)"


@blueprint.route("/", methods=["GET"])
def status():
    return render_template(
        "greenmesg/status.html",
        stats=_db_stats(),
        log_tail=_log_tail(),
        output=None,
        title="GreenMesg importer",
    )


@blueprint.route("/run", methods=["GET", "POST"])
def run():
    form = request.values
    url = (form.get("url") or "").strip()
    try:
        limit = int(form.get("limit") or 5)
    except ValueError:
        limit = 5
    limit = max(0, min(limit, WEB_LIMIT_CAP))
    dry_run = (form.get("dry_run", "on") == "on")
    force = (form.get("force", "off") == "on")

    argv = ["--db", _db_path(), "--limit", str(limit)]
    if url:
        argv += ["--url", url]
    if dry_run:
        argv.append("--dry-run")
    if force:
        argv.append("--force")

    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            engine.main(argv)
        ok = True
    except SystemExit as exc:  # engine.main never raises; defensive only
        ok = exc.code in (0, None)
        buf.write(f"\nexit={exc.code}\n")
    except Exception as exc:  # noqa: BLE001
        ok = False
        buf.write(f"\nERROR {type(exc).__name__}: {exc}\n")

    return render_template(
        "greenmesg/status.html",
        stats=_db_stats(),
        log_tail=_log_tail(),
        output={"ok": ok, "argv": argv, "text": buf.getvalue()[-20000:]},
        title="GreenMesg importer",
    )


@blueprint.route("/api/plan", methods=["GET"])
def api_plan():
    session = requests.Session()
    urls = engine.load_urls(session, request.args.get("urls_file") or None)
    db = sqlite3.connect(_db_path())
    try:
        existing = engine.load_existing(db)
    finally:
        db.close()
    have, missing = [], []
    for url in urls:
        path = url.replace(engine.BASE, "")
        display = " ".join(
            re.split(r"[_/]", url.rsplit("/", 1)[-1][:-4])
        ).title()
        if path in existing["urls"] or engine.match_existing(display, existing):
            have.append(url)
        else:
            missing.append(url)
    return jsonify({"total": len(urls), "have": have, "missing": missing})
