# msamdd/cli_aff.py
import sys
from msamdd import msa_aff

def main() -> None:
    """Command-line entry point for msa_aff."""
    rc = msa_aff(sys.argv[1:])
    sys.exit(rc)
