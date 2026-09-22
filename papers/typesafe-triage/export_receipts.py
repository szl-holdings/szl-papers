#!/usr/bin/env python3
"""Map a triage repo's receipt-like JSON into data/receipts.json.

Never invents values. Fields it cannot find stay absent, so the matching figure
skips and the matching number renders as ?? in the PDF. Inspect the output before
building.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

CAND = re.compile(r"receipt|eval|metric|gate|result", re.I)


def load(p):
    try:
        return json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", default="data/receipts.json")
    a = ap.parse_args()
    root = pathlib.Path(a.repo)
    if not root.exists():
        sys.exit(f"repo not found: {root}")
    docs = []
    for p in root.rglob("*.json"):
        s = str(p)
        if any(x in s for x in (".git", ".venv", "__pycache__", "node_modules")):
            continue
        if not CAND.search(p.name) and not CAND.search(p.parent.name):
            continue
        d = load(p)
        if isinstance(d, dict):
            docs.append((p, d))
    print(f"scanned {root}: {len(docs)} candidate documents")
    out = {"run_id": None, "base_model": None, "seeds": [], "gates": [], "eval": {},
           "promotion_status": None, "contamination_verdict": None,
           "_provenance": [str(p.relative_to(root)) for p, _ in docs]}
    for p, d in docs:
        for k in ("run_id", "base_model", "promotion_status"):
            if out[k] is None and isinstance(d.get(k), str):
                out[k] = d[k]
        cv = (d.get("contamination") or {}).get("verdict") or d.get("contamination_verdict")
        if out["contamination_verdict"] is None and isinstance(cv, str):
            out["contamination_verdict"] = cv.upper()
        if isinstance(d.get("gates"), list) and not out["gates"]:
            out["gates"] = d["gates"]
        if isinstance(d.get("eval"), dict) and ("seed" in d or "adapter" in d):
            seed = d.get("seed") or (d.get("adapter") or {}).get("seed")
            if seed is not None:
                out["seeds"].append({"seed": int(seed), "train_loss": d.get("train_loss") or [],
                                     "eval": d["eval"]})
        for k in ("n_test", "n_families", "ngram_overlap", "family_overlap_jaccard"):
            v = ((d.get("split") or {}).get(k) or (d.get("eval") or {}).get(k)
                 or (d.get("contamination") or {}).get(k))
            if v is not None and k not in out["eval"]:
                out["eval"][k] = v
    out["seeds"].sort(key=lambda s: s["seed"])
    outp = pathlib.Path(a.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {outp}")
    miss = [k for k, v in (("seeds", out["seeds"]), ("gates", out["gates"]),
                           ("eval.n_test", out["eval"].get("n_test"))) if not v]
    if miss:
        print("STILL MISSING (figures will skip): " + ", ".join(miss))
    print('add by hand: "base_reference": {"eval": {"refusal_rate": <frozen base value>}}')


if __name__ == "__main__":
    main()
