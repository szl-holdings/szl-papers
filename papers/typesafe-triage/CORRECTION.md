# Correction record — private triage note

## Superseded claim

An earlier private draft stated that the Qwen3.5-0.8B triage LoRA failed refusal preservation and passed 11 of 12 promotion checks.

## Controlling public evidence

The public artifact is:

- Model card: `SZLHOLDINGS/szl-triage-qwen3.5-0.8b-lora`
- Behavioural report: `gate_report.json` in that same repository

The behavioural report records:

```text
rows:                    66
malformed:                0
label_ok:                66
state_ok:                66
gold_refusals:           23
false_label_on_refusal:   0
ungrounded_spans:         0
behavioural verdict:      PROMOTABLE
```

The public model card records:

```text
Release state: NOT PROMOTABLE
Reason: contamination / corpus-leakage review did not clear
```

## Corrected statement

The behavioural contract passed on the published gate rows. Release remained blocked because the contamination/corpus-leakage predicate did not clear. The adapter is a reference artifact for inspection and reproducibility, not a cleared or deployable model.

## Removed material

The following unsupported synthetic material is removed from the corrected private note:

- synthetic loss curves
- invented seed aggregates
- invented random-vs-family split numbers
- invented calibration values
- invented latency/token measurements
- invented 11-of-12 gate ledger

## Publication boundary

This corrected note is private and has **no DOI**. It is not an archival empirical publication.
