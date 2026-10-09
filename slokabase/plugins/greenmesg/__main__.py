"""CLI entry point: ``python -m slokabase.plugins.greenmesg [options]``."""

import sys

from .scraper import main

if __name__ == "__main__":
    sys.exit(main())
