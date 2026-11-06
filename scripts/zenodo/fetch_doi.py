#!/usr/bin/env python3
"""Poll the Zenodo public API for the record minted from a GitHub release and
record its version DOI + concept DOI. No token required for public records.

    python scripts/zenodo/fetch_doi.py --tag typesafe-triage-v1.0.0 --timeout 900

Root deposits resolve their title from metadata/zenodo/releases/<tag>.json.
Preprint tags resolve from metadata/zenodo/preprint_release_tags.json, which
points at that paper's own .zenodo.json. A preprint tag never accepts the
shared Ouroboros concept DOI: GitHub–Zenodo deposits the repository-root
metadata, and that deposit is a different work.
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
RELEASES = ROOT / "metadata" / "zenodo" / "releases"
PREPRINT_TAGS = ROOT / "metadata" / "zenodo" / "preprint_release_tags.json"
API = "https://zenodo.org/api/records"
# Concept shared by the Thesis v8 record and later root-metadata deposits.
# Preprint sync must not record it as a paper DOI.
UMBRELLA_CONCEPT_DOI = "10.5281/zenodo.20567256"


def search(title: str, version: str, reject_concept_dois: frozenset[str] | None = None) -> dict | None:
    q = f'title:"{title}"'
    url = API + "?" + urllib.parse.urlencode({"q": q, "size": 10, "sort": "mostrecent"})
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "szl-papers-doi-sync"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.loads(r.read().decode("utf-8"))
    return pick(payload, version, title=title, reject_concept_dois=reject_concept_dois)


def pick(payload: dict, version: str, title: str = "", reject_concept_dois: frozenset[str] | None = None) -> dict | None:
    hits = (payload.get("hits") or {}).get("hits") or []
    rejected = reject_concept_dois or frozenset()
    for h in hits:
        md = h.get("metadata") or {}
        if version and str(md.get("version", "")) != version:
            continue
        found_title = md.get("title")
        if title and found_title != title:
            continue
        doi = h.get("doi") or md.get("doi")
        concept = h.get("conceptdoi") or md.get("conceptdoi")
        if doi in rejected or concept in rejected:
            continue
        if doi:
            return {"record_id": h.get("id"), "doi": doi, "concept_doi": concept,
                    "title": found_title, "version": md.get("version"),
                    "published": md.get("publication_date"), "url": h.get("links", {}).get("self_html")}
    return None


def _read_json(path: pathlib.Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return doc


def resolve_query(tag: str, title: str = "", version: str = "") -> dict:
    """Return title, version, and source: root-release, preprint, cli, or missing."""
    source = "cli" if title else "missing"
    if not title or not version:
        override = RELEASES / f"{tag}.json"
        if override.exists():
            doc = _read_json(override)
            title = title or str(doc.get("title") or "")
            version = version or str(doc.get("version") or "")
            source = "root-release"
        elif PREPRINT_TAGS.exists():
            spec = (_read_json(PREPRINT_TAGS).get("tags") or {}).get(tag)
            if isinstance(spec, dict):
                rel = str(spec.get("zenodo_metadata") or "")
                path = ROOT / rel
                doc = _read_json(path) if rel and path.exists() else {}
                title = title or str(doc.get("title") or "")
                version = version or str(spec.get("version") or doc.get("version") or "")
                source = "preprint"
    if not title:
        source = "missing"
    return {"title": title, "version": version, "source": source}


def self_test() -> None:
    p3 = resolve_query("p3-v1.0.0")
    p4 = resolve_query("p4-v1.0.0")
    assert p3["source"] == "preprint" and p3["version"] == "1.0.0"
    assert p4["source"] == "preprint" and p4["version"] == "1.0.0"
    assert p3["title"] == (
        "Receipt-Attached Reliability: Whole-Chain Measurement for Governed MCP Tool Servers"
    )
    assert p4["title"] == (
        "Honest Abstention Transfer in Small-Corpus Supervised Fine-Tuning: "
        "Measured Refusals and Confabulations in a 4B Estate-Tuned Model"
    )
    assert p3["title"] != p4["title"]

    triage = resolve_query("typesafe-triage-v1.0.1")
    assert triage["source"] == "root-release"
    assert triage["version"] == "1.0.1"
    assert triage["title"].startswith("Governed Type-Safe Triage")

    missing = resolve_query("not-a-real-tag")
    assert missing == {"title": "", "version": "", "source": "missing"}

    cli = resolve_query("typesafe-triage-v1.0.1", title="Custom")
    assert cli["title"] == "Custom" and cli["version"] == "1.0.1" and cli["source"] == "root-release"

    umbrella_hit = {
        "id": 23991485,
        "doi": "10.5281/zenodo.23991485",
        "conceptdoi": UMBRELLA_CONCEPT_DOI,
        "metadata": {
            "title": p3["title"],
            "version": "1.0.0",
            "doi": "10.5281/zenodo.23991485",
            "conceptdoi": UMBRELLA_CONCEPT_DOI,
        },
        "links": {"self_html": "https://zenodo.org/records/23991485"},
    }
    payload = {"hits": {"hits": [umbrella_hit]}}
    assert pick(
        payload, "1.0.0", title=p3["title"], reject_concept_dois=frozenset({UMBRELLA_CONCEPT_DOI})
    ) is None
    kept = pick(payload, "1.0.0", title=p3["title"])
    assert kept is not None and kept["concept_doi"] == UMBRELLA_CONCEPT_DOI

    other = {"hits": {"hits": [{
        "id": 2,
        "doi": "10.5281/zenodo.1",
        "conceptdoi": "10.5281/zenodo.2",
        "metadata": {"title": "Other paper", "version": "1.0.0"},
    }]}}
    assert pick(other, "1.0.0", title=p3["title"]) is None

    good = {"hits": {"hits": [{
        "id": 300,
        "doi": "10.5281/zenodo.300",
        "conceptdoi": "10.5281/zenodo.301",
        "metadata": {"title": p3["title"], "version": "1.0.0", "publication_date": "2026-11-06"},
        "links": {"self_html": "https://zenodo.org/records/300"},
    }]}}
    found = pick(good, "1.0.0", title=p3["title"], reject_concept_dois=frozenset({UMBRELLA_CONCEPT_DOI}))
    assert found is not None
    assert found["doi"] == "10.5281/zenodo.300"
    assert found["concept_doi"] == "10.5281/zenodo.301"
    assert found["title"] == p3["title"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--version", default="")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--interval", type=int, default=60)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        self_test()
        print("zenodo doi resolver self-test OK")
        return
    if not a.tag:
        sys.exit("--tag is required unless --self-test is set")

    resolved = resolve_query(a.tag, a.title, a.version)
    title = resolved["title"]
    version = resolved["version"]
    if not title:
        sys.exit("no title available for the search")

    reject = frozenset({UMBRELLA_CONCEPT_DOI}) if resolved["source"] == "preprint" else frozenset()
    deadline = time.time() + a.timeout
    found = None
    while time.time() < deadline and not found:
        try:
            found = search(title, version, reject)
        except Exception as exc:  # network hiccup should not fail the job immediately
            print(f"query failed: {exc}", file=sys.stderr)
        if not found:
            print(f"no Zenodo record yet for {a.tag}; retrying in {a.interval}s", flush=True)
            time.sleep(a.interval)

    if not found:
        print(f"::warning::no Zenodo record found for {a.tag} within {a.timeout}s "
              f"(ingest may be slow, or the repository switch was off when the tag was cut)")
        if resolved["source"] == "preprint":
            print(
                "::warning::This tag resolves to per-preprint metadata. "
                "GitHub–Zenodo reads only the repository-root .zenodo.json, which is "
                "reference-only. That deposit was not written to the DOI ledger as this preprint."
            )
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
