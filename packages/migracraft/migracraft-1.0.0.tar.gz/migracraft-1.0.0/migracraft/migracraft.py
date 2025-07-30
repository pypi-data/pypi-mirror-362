#!/usr/bin/env python3
"""
MigraCraft - Craft perfect PostgreSQL migrations with precision and artistry

This is the main entry point for MigraCraft when installed as a package.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import migrate
sys.path.insert(0, str(Path(__file__).parent.parent))

from migrate import main

if __name__ == "__main__":
    main()
