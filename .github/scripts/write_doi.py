#!/usr/bin/env python3
"""Write a minted Zenodo DOI into CITATION.cff (doi:) and a README DOI badge.

Usage: python3 write_doi.py <DOI>
Idempotent: re-running with the same DOI is a no-op.
"""
import sys
import re
import pathlib

doi = sys.argv[1].strip()
if not doi:
    print("no DOI passed; nothing to do")
    sys.exit(0)

# CITATION.cff — set or replace top-level doi:, clear any "DOI pending" note.
cff = pathlib.Path("CITATION.cff")
if cff.exists():
    t = cff.read_text()
    if re.search(r"(?m)^doi:\s*.*$", t):
        t = re.sub(r"(?m)^doi:\s*.*$", f'doi: "{doi}"', t, count=1)
    else:
        t = re.sub(r"(?m)^(cff-version:.*$)", r"\1" + f'\ndoi: "{doi}"', t, count=1)
    t = t.replace("DOI pending Zenodo mint", f"DOI {doi}")
    cff.write_text(t)
    print("CITATION.cff updated with", doi)

# README DOI badge (idempotent).
badge = f"[![DOI](https://zenodo.org/badge/DOI/{doi}.svg)](https://doi.org/{doi})"
for name in ("README.md", "Readme.md", "readme.md"):
    rp = pathlib.Path(name)
    if rp.exists():
        r = rp.read_text()
        if "zenodo.org/badge/DOI" in r:
            r = re.sub(
                r"\[!\[DOI\]\(https://zenodo\.org/badge/DOI/[^)]*\)\]\(https://doi\.org/[^)]*\)",
                badge, r, count=1)
        else:
            r = badge + "\n\n" + r
        rp.write_text(r)
        print(name, "badge set to", doi)
        break
