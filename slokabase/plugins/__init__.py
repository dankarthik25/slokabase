"""Optional SlokaBase app plugins (Flask blueprints).

Each subpackage is self-contained and must never break the main app on
import: ``app.py`` imports plugins inside a ``try/except`` guarded by the
``SLOKABASE_<NAME>`` environment flag.
"""
