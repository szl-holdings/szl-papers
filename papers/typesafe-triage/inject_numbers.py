#!/usr/bin/env python3
"""Inject measured numbers from receipts into results/generated_numbers.tex.

Absent quantities stay as the visible placeholder ?? in the PDF. Missing data is
meant to be obvious.
"""
from __future__ import annotations
import json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)


def fmt(v, nd=3):
    return "??" if v is None else f"{v:.{nd}f}"


def main():
    p = ROOT / "data" / "receipts.json"
    if not p.exists():
        sys.exit(f"no receipts at {p}; numbers stay ?? in the PDF (by design)")
    d = json.loads(p.read_text(encoding="utf-8"))
    seeds = d.get("seeds") or []
    grab = lambda k: [s["eval"][k] for s in seeds if (s.get("eval") or {}).get(k) is not None]
    fam, rnd, ref, ece = grab("accuracy_family_split"), grab("accuracy_random_split"), grab("refusal_rate"), grab("ece")
    base = ((d.get("base_reference") or {}).get("eval") or {}).get("refusal_rate")
    gates = d.get("gates") or []
    npass = sum(1 for x in gates if x.get("status") == "PASS")
    ng13 = next((x["train_test_overlap_frac"] for x in ((d.get("eval") or {}).get("ngram_overlap") or [])
                 if x.get("n") == 13), None)
    nt = (d.get("eval") or {}).get("n_test")
    lines = [
      r"\renewcommand{\runId}{%s}" % d.get("run_id", "??"),
      r"\renewcommand{\baseModel}{%s}" % d.get("base_model", "??"),
      r"\renewcommand{\nSeeds}{%d}" % len(seeds),
      r"\renewcommand{\nTest}{%s}" % (f"{nt:,}" if isinstance(nt, int) else "??"),
      r"\renewcommand{\nFamilies}{%s}" % ((d.get("eval") or {}).get("n_families", "??")),
      r"\renewcommand{\gatesTotal}{%d}" % len(gates),
      r"\renewcommand{\gatesPassed}{%d}" % npass,
      r"\renewcommand{\promotionStatus}{\%s}" % ("PR" if d.get("promotion_status") == "PROMOTABLE" else "NP"),
      r"\renewcommand{\accFamilyMean}{%s}" % fmt(statistics.fmean(fam) if fam else None),
      r"\renewcommand{\accFamilySd}{%s}" % fmt(statistics.pstdev(fam) if len(fam) > 1 else None),
      r"\renewcommand{\accRandomMean}{%s}" % fmt(statistics.fmean(rnd) if rnd else None),
      r"\renewcommand{\splitGap}{%s}" % fmt((statistics.fmean(rnd) - statistics.fmean(fam)) if (fam and rnd) else None),
      r"\renewcommand{\refusalBase}{%s}" % fmt(base),
      r"\renewcommand{\refusalMean}{%s}" % fmt(statistics.fmean(ref) if ref else None),
      r"\renewcommand{\refusalDelta}{%s}" % (fmt(statistics.fmean(ref) - base) if (ref and base is not None) else "??"),
      r"\renewcommand{\eceMean}{%s}" % fmt(statistics.fmean(ece) if ece else None),
      r"\renewcommand{\overlapThirteen}{%s}" % fmt(ng13, 5)]
    (OUT / "generated_numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    rows = []
    for s in seeds:
        e = s.get("eval") or {}
        rows.append(" & ".join([str(s["seed"]), fmt(e.get("accuracy_family_split")),
            fmt(e.get("accuracy_random_split")), fmt(e.get("macro_f1")), fmt(e.get("refusal_rate")),
            fmt(e.get("ece")), fmt(e.get("latency_ms_p95"), 1)]) + r" \\")
    (OUT / "per_seed_table.tex").write_text(
        r"\begin{table}[h]\centering\small" + "\n"
        + r"\caption{Per-seed measurements, generated from receipts.}" + "\n"
        + r"\begin{tabular}{@{}rrrrrrr@{}}\toprule" + "\n"
        + r"seed & acc (family) & acc (random) & macro $F_1$ & refusal & ECE & p95 (ms) \\ \midrule" + "\n"
        + "\n".join(rows) + "\n" + r"\bottomrule\end{tabular}\end{table}" + "\n", encoding="utf-8")
    print(f"wrote results/generated_numbers.tex ({len(lines)} macros), per_seed_table.tex ({len(rows)} rows)")


if __name__ == "__main__":
    main()
