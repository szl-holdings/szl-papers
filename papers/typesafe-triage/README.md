# Governed Type-Safe Triage — preprint kit

This folder contains the complete reproducible build for the preprint:
**"Governed Type-Safe Triage: LoRA Distillation Under a Refusal-Preserving Promotion Gate"**.

---

## Quick start (demo mode, no receipts needed)
```powershell
cd papers/typesafe-triage
python figures.py --demo --out figures
python inject_numbers.py          # writes results/*.tex with ?? placeholders
latexmk -pdf main.tex
```
Produces `main.pdf` with every figure watermarked **SYNTHETIC** and every
measured value rendered as `??`. The figure manifest is written to
`figures/figure_manifest.json` listing what was written and what was skipped.

---

## Real build (your data)
```powershell
# 1. Export receipts from your triage repo into the paper schema
python export_receipts.py --repo C:\Users\steph\szl-typesafe-triage --out data/receipts.json

# 2. Inspect data/receipts.json — add the one field the script can't find:
#    "base_reference": {"eval": {"refusal_rate": <frozen base value>}}

# 3. Build
python figures.py --receipts data/receipts.json --out figures
python inject_numbers.py
latexmk -pdf main.tex
```
`main.pdf` now contains your actual numbers and figures with no watermarks.

---

## What each script does

| Script | Role | Strictness |
|---|---|---|
| `figures.py` | Renders 8 panels (loss, gate ledger, refusal delta, split gap, calibration, contamination, per-class, serving). | **Strict** — a panel whose inputs are absent is SKIPPED with a reason logged; nothing is invented. `--demo` uses synthetic data and watermarks every panel. |
| `inject_numbers.py` | Reads `data/receipts.json`, computes means/SD, gate pass count, split gap, refusal delta, 13-gram overlap. Writes `results/generated_numbers.tex` (17 `\renewcommand`s) and `results/per_seed_table.tex`. | Absent values emit `??` in the PDF — missing data is visible, not hidden. |
| `export_receipts.py` | Walks a triage repo for receipt/eval/metric/gate JSON, maps what it finds into the paper schema, prints **STILL MISSING** for anything the paper needs, reminds you to add `base_reference.eval.refusal_rate` by hand. | Never invents values. |
| `build.ps1` | Convenience wrapper: falls back to `--demo` when `data/receipts.json` is missing, otherwise runs the real pipeline, then `latexmk`. | — |

---

## Paper schema (what the figures need)
`data/receipts.schema.json` — JSON Schema with the exact keys the figures read:
- `run_id`, `base_model`, `adapter_bytes`
- `seeds[]` each with `seed`, `train_loss[]` (`step`, `loss`), `eval` block containing:
  `accuracy_family_split`, `accuracy_random_split`, `macro_f1`, `refusal_rate`,
  `review_routing_rate`, `ece`, `confidence_bins[]` (`p_mid`, `acc`, `n`),
  `per_class[]` (`label`, `precision`, `recall`, `support`),
  `latency_ms_p50`, `latency_ms_p95`, `tokens_in`, `tokens_out`
- `base_reference.eval.refusal_rate` (the frozen base; **must add by hand**)
- `gates[]` each with `id`, `name`, `status` (PASS/FAIL/SKIP), optional `per_seed`
- `eval.n_test`, `eval.n_families`, `eval.ngram_overlap[]`, `eval.family_overlap_jaccard[]`
- `contamination_verdict`, `promotion_status`

---

## Figure manifest
After every run `figures/figure_manifest.json` records:
```json
{
  "written": ["fig1_loss", "fig2_gate_ledger", ...],
  "skipped": ["fig3_refusal: missing seeds[].eval.refusal_rate", ...],
  "demo": false,
  "run_id": "...",
  "promotion_status": "NOTPROMOTABLE"
}
```
If a panel is missing in the PDF, the manifest tells you why.

---

## LaTeX dependencies
- `graphicx`, `booktabs`, `pgfplots` (compat=1.18), `siunitx`
- `hyperref`, `cleveref`, `amsmath`, `amssymb`, `authblk`
- `latexmk` (MiKTeX or TeX Live)

---

## License
Code: Apache-2.0  •  Text & figures: CC-BY-4.0

---

## Citation (when the archived version exists)
```bibtex
@article{lutar2026governed,
  title={Governed Type-Safe Triage: LoRA Distillation Under a Refusal-Preserving Promotion Gate},
  author={Lutar, Stephen P.},
  journal={arXiv preprint},
  year={2026}
}
```

---

## Where the other artefacts live
- Preprint PDF (this build) → `main.pdf`
- Archival bundle (receipts + gate ledger + manifest) → concept DOI via Zenodo (not in this repo)
- Source code for the triage pipeline → `szl-typesafe-triage` repo
- The promotion gate specification → Appendix A of this paper

---

**TL;DR for friends:** `git clone`, open `papers/typesafe-triage`, run the three lines under "Quick start". If the PDF looks right, swap `--demo` for your real `data/receipts.json` and rebuild. The numbers in the PDF *are* the receipts — nothing is typed by hand.
