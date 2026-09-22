#!/usr/bin/env python3
"""Render and verify the root .zenodo.json from base + per-release override.

Zenodo reads ONLY the repository-root .zenodo.json from the tagged tree, so the
root file must be correct BEFORE the tag exists. This script makes that file a
build artifact instead of a hand-edit, and --check turns drift into a CI failure.

    python scripts/zenodo/render_zenodo.py --tag typesafe-triage-v1.0.0 --write
    python scripts/zenodo/render_zenodo.py --check          # uses metadata/zenodo/next.txt
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
META = ROOT / "metadata" / "zenodo"
BASE = META / "base.json"
NEXT = META / "next.txt"
TARGET = ROOT / ".zenodo.json"

REQUIRED = ("title", "upload_type", "creators", "license", "version", "description")
ALLOWED_UPLOAD = {"publication", "software", "dataset", "poster", "presentation", "other"}
MERGE_LISTS = ("keywords", "related_identifiers", "communities", "subjects")


def deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        if k in MERGE_LISTS and isinstance(v, list) and isinstance(out.get(k), list):
            seen, merged = set(), []
            for item in out[k] + v:
                key = json.dumps(item, sort_keys=True)
                if key not in seen:
                    seen.add(key)
                    merged.append(item)
            out[k] = merged
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def validate(doc: dict, tag: str) -> list[str]:
    errs = []
    for f in REQUIRED:
        if not doc.get(f):
            errs.append(f"missing required field: {f}")
    if doc.get("upload_type") not in ALLOWED_UPLOAD:
        errs.append(f"upload_type {doc.get('upload_type')!r} not in {sorted(ALLOWED_UPLOAD)}")
    if doc.get("upload_type") == "publication" and not doc.get("publication_type"):
        errs.append("upload_type=publication requires publication_type")
    creators = doc.get("creators") or []
    if not isinstance(creators, list) or not creators:
        errs.append("creators must be a non-empty list")
    for c in creators:
        if not c.get("name"):
            errs.append("each creator needs a name")
        if not c.get("orcid"):
            errs.append(f"creator {c.get('name','?')} is missing an orcid")
    if doc.get("access_right") not in (None, "open", "embargoed", "restricted", "closed"):
        errs.append("invalid access_right")
    if doc.get("license") and not isinstance(doc["license"], str):
        errs.append("license must be an SPDX-ish id string, e.g. cc-by-4.0")
    ver = str(doc.get("version", ""))
    if ver and ver not in tag:
        errs.append(f"version {ver!r} does not appear in tag {tag!r}")
    if "doi" in doc:
        errs.append("remove 'doi': Zenodo assigns it; a pre-set doi is ignored or conflicts")
    return errs


def render(tag: str) -> dict:
    if not BASE.exists():
        sys.exit(f"missing {BASE.relative_to(ROOT)}")
    base = json.loads(BASE.read_text(encoding="utf-8"))
    over_path = META / "releases" / f"{tag}.json"
    if not over_path.exists():
        sys.exit(f"no override for tag {tag}: create {over_path.relative_to(ROOT)}")
    over = json.loads(over_path.read_text(encoding="utf-8"))
    doc = deep_merge(base, over)
    errs = validate(doc, tag)
    if errs:
        for e in errs:
            print(f"INVALID: {e}", file=sys.stderr)
        sys.exit(2)
    return doc


def canonical(doc: dict) -> str:
    return json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    tag = a.tag or (NEXT.read_text(encoding="utf-8").strip() if NEXT.exists() else "")
    if not tag:
        sys.exit("no tag given and metadata/zenodo/next.txt is missing")
    doc = canonical(render(tag))
    if a.write:
        TARGET.write_text(doc, encoding="utf-8")
        print(f"wrote .zenodo.json for {tag} ({len(doc)} bytes)")
        return
    if a.check:
        if not (META / "ENABLED").exists():
            print("metadata/zenodo/ENABLED is absent: gate is in report-only mode.")
            print("Bootstrap once you have reconciled base.json with the curated root file:")
            print("  python scripts/zenodo/render_zenodo.py --tag <tag> > /tmp/rendered.json")
            print("  diff -u .zenodo.json /tmp/rendered.json")
            print("  python scripts/zenodo/render_zenodo.py --write && touch metadata/zenodo/ENABLED")
            return
        if not TARGET.exists():
            sys.exit("root .zenodo.json is missing")
        current = TARGET.read_text(encoding="utf-8")
        if current != doc:
            print("DRIFT: root .zenodo.json does not match the rendered metadata for tag " + tag, file=sys.stderr)
            print("run: python scripts/zenodo/render_zenodo.py --write", file=sys.stderr)
            sys.exit(1)
        print(f"root .zenodo.json matches rendered metadata for {tag}")
        return
    print(doc)


if __name__ == "__main__":
    main()
