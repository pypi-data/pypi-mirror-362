"""
Main module for VEPmcp.
"""

import sys
from .cli import main as cli_main

__version__ = "0.1.0"


def main() -> int:
    """Main entry point for CLI."""
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())
