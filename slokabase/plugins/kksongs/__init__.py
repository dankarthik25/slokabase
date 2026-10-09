"""Kksongs song importer plugin.

Web UI + JSON API over the :mod:`slokabase.plugins.kksongs.scraper`
engine, mounted at ``/admin/kksongs``.  Importing this package has no
side effects; call :func:`register` or register :data:`blueprint`
explicitly.

Disable from the shell with ``SLOKABASE_KKSONGS=0`` (see ``app.py``).
"""

from .views import blueprint

PLUGIN_INFO = {
    "name": "kksongs",
    "description": "Import songs from kksongs.org into slokabase.db",
    "url_prefix": "/admin/kksongs",
    "env_flag": "SLOKABASE_KKSONGS",
}


def register(app):
    """Register the blueprint on a Flask app (idempotent)."""
    if "kksongs" not in app.blueprints:
        app.register_blueprint(blueprint)
    return app


__all__ = ["blueprint", "register", "PLUGIN_INFO"]
