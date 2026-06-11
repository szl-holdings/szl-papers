#!/usr/bin/env python3
"""Read a Zenodo record JSON from stdin, print its DOI (empty string if absent)."""
import sys
import json

try:
    print(json.load(sys.stdin).get("doi", ""))
except Exception:
    print("")
