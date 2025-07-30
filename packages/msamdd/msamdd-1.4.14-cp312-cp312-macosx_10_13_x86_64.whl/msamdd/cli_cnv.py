# msamdd/cli_cnv.py
import sys
from msamdd import msa_cnv   # imported from __init__.py

def main() -> None:
    """Command-line entry point for msa_cnv."""
    # sys.argv[1:] is everything after the command name
    rc = msa_cnv(sys.argv[1:])
    sys.exit(rc)
