"""
VEPmcp - Model Context Protocol server for interacting with the Variant Effect Prediction (VEP) API from Ensembl.
"""

__version__ = "0.1.0"
__author__ = "Jules Kreuer"
__email__ = "jules.kreuer@uni-tuebingen.de"

from .bridge import Bridge, Config, VEPValidator
from .cli import main as cli_main

__all__ = ["Bridge", "Config", "VEPValidator", "cli_main"]
