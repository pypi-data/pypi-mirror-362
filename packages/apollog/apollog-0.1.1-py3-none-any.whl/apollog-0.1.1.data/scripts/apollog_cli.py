#!python
"""
Apollog CLI Wrapper

This script provides a simple way to run the Apollog CLI commands
without relying on entry points.
"""

import sys
from apollog.cli import main

if __name__ == "__main__":
    sys.exit(main())
