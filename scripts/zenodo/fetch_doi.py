#!/usr/bin/env python3
"""Poll the Zenodo public API for the record minted from a GitHub release and
record its version DOI + concept DOI. No token required for public records.

    python scripts/zenodo/fetch_doi.py --tag typesafe-triage-v1.0.0 --timeout 900
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEDGER = ROOT / "metadata" / "zenodo" / "doi_records.json"
API = "https://zenodo.org/api/records"


def search(title: str, version: str) -> dict | None:
    q = f'title:"{title}"'
    url = API + "?" + urllib.parse.urlencode({"q": q, "size": 10, "sort": "mostrecent"})
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "szl-papers-doi-sync"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.loads(r.read().decode("utf-8"))
    return pick(payload, version)


def pick(payload: dict, version: str) -> dict | None:
    hits = (payload.get("hits") or {}).get("hits") or []
    for h in hits:
        md = h.get("metadata") or {}
        if version and str(md.get("version", "")) != version:
            continue
        doi = h.get("doi") or md.get("doi")
        concept = h.get("conceptdoi") or md.get("conceptdoi")
        if doi:
            return {"record_id": h.get("id"), "doi": doi, "concept_doi": concept,
                    "title": md.get("title"), "version": md.get("version"),
                    "published": md.get("publication_date"), "url": h.get("links", {}).get("self_html")}
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--version", default="")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--interval", type=int, default=60)
    a = ap.parse_args()

    title = a.title
    version = a.version
    if not title or not version:
        over = ROOT / "metadata" / "zenodo" / "releases" / f"{a.tag}.json"
        if over.exists():
            doc = json.loads(over.read_text(encoding="utf-8"))
            title = title or doc.get("title", "")
            version = version or str(doc.get("version", ""))
    if not title:
        sys.exit("no title available for the search")

    deadline = time.time() + a.timeout
    found = None
    while time.time() < deadline and not found:
        try:
            found = search(title, version)
        except Exception as exc:  # network hiccup should not fail the job immediately
            print(f"query failed: {exc}", file=sys.stderr)
        if not found:
            print(f"no Zenodo record yet for {a.tag}; retrying in {a.interval}s", flush=True)
            time.sleep(a.interval)

    if not found:
        print(f"::warning::no Zenodo record found for {a.tag} within {a.timeout}s "
              f"(ingest may be slow, or the repository switch was off when the tag was cut)")
        sys.exit(0)

    ledger = {"records": []}
    if LEDGER.exists():
        try:
            ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        except Exception:
            pass
    ledger.setdefault("records", [])
    ledger["records"] = [r for r in ledger["records"] if r.get("tag") != a.tag]
    entry = dict(found); entry["tag"] = a.tag
    ledger["records"].append(entry)
    ledger["records"].sort(key=lambda r: str(r.get("tag")))
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    badge = (f"[![DOI](https://zenodo.org/badge/DOI/{found['concept_doi'] or found['doi']}.svg)]"
             f"(https://doi.org/{found['concept_doi'] or found['doi']})")
    print(f"version DOI : {found['doi']}")
    print(f"concept DOI : {found['concept_doi']}")
    print(f"badge       : {badge}")


if __name__ == "__main__":
    main()
