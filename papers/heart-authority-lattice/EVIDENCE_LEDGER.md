# Evidence ledger

Every factual statement in the flagship manuscript requires a row here before it is published.

| Claim | Claim class | Source | Revision / date | Limitation | Paper status |
|---|---|---|---|---|---|
| Λ is advisory and not proven trust | SOURCE_BACKED | `SZLHOLDINGS/szl-lambda-gate` kernel source/card | current public card read 2026-09-22 | Unconditional uniqueness remains open/false as stated | admissible |
| Locked baseline is 749 / 14 / 163 | SOURCE_BACKED | doctrine/Lean cards | `c7c0ba17` epoch | Not interchangeable with later Lean epochs | admissible if pinned |
| Theorem U is REAL-conditional | RECEIPT_BACKED | later `lutar_lean_receipts.ndjson` anchor | `e736decd...` | Not in locked baseline | admissible if epoch named |
| Amaru receipt signatures verify | REPRODUCED | SZL Lake + org-cosign public key | public rows read 2026-09-22 | Verifies digest signature, not decision correctness | admissible |
| Sentra receipt material is incomplete | REPRODUCED | SZL Lake sentra NDJSON | public rows read 2026-09-22 | signed flag lacks public sig/PAE fields | admissible as gap |
| Triage behavioral report passes | SOURCE_BACKED | `gate_report.json` | public Hub artifact | finite 66-row report only | admissible |
| Triage release is blocked | SOURCE_BACKED | model card | public Hub artifact | contamination details not fully public | admissible |
| Council / IMMUNE authority lattice | SOURCE_PRESENT_PARTIAL_READ | GitHub code search and runtime docs | current indexed source | full source census pending | scaffold only |

## Forbidden substitutions

```text
PUBLISHED does not substitute for PROMOTABLE.
PROMOTABLE does not substitute for AUTHORIZED.
A receipt does not substitute for correctness.
A formula does not substitute for authority.
An HTTP response does not substitute for deployment certification.
A card does not substitute for source or runtime evidence.
```
