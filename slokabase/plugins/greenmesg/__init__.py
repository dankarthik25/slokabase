"""GreenMesg stotra importer plugin.

Web UI + JSON API over the :mod:`slokabase.plugins.greenmesg.scraper`
engine, mounted at ``/admin/greenmesg``.  Importing this package has no
side effects; call :func:`register` or register :data:`blueprint`
explicitly.

Disable from the shell with ``SLOKABASE_GREENMESG=0`` (see ``app.py``).
"""

from .views import blueprint

PLUGIN_INFO = {
    "name": "greenmesg",
    "description": "Import stotras from greenmesg.org into slokabase.db",
    "url_prefix": "/admin/greenmesg",
    "env_flag": "SLOKABASE_GREENMESG",
}


def register(app):
    """Register the blueprint on a Flask app (idempotent)."""
    if "greenmesg" not in app.blueprints:
        app.register_blueprint(blueprint)
    return app


__all__ = ["blueprint", "register", "PLUGIN_INFO"]
