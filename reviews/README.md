# Reviews (non-normative)

This directory holds **non-normative review sidecars**: documents that compare what a
manuscript or doctrine surface in this repository says with the pinned sources it cites,
and that propose wording for the owner to accept or reject.

Rules for everything in `reviews/`:

- **Non-normative.** A review is an opinion for the owner. It is not doctrine, not a
  manuscript erratum and not a claim registry. Where a review and a manuscript differ, the
  manuscript stays as written until the owner decides.
- **Never modifies manuscripts or doctrine.** A review PR touches only `reviews/` and, at
  most, a read-only checker under `scripts/`. Corrections to manuscripts, `thesis/arxiv/`,
  `PAPERS_INDEX.md`, `bounty/`, lutar-lean or szl-forge are separate PRs that need an
  explicit owner decision.
- **Pinned sources.** Every quote cites a repository, a full 40-hex commit and a file:line,
  and the commit must be the ledger's pin for that repository. Manuscript quotes are checked
  verbatim against the current checkout, so drift fails the checker instead of going unnoticed.
- **Evidence vocabulary.** Results are labelled `MEASURED`, `NOT_RUN` or `UNKNOWN`.
  `UNKNOWN` is never treated as a pass.

## Index

| Review | Subject | Pins | Status |
|---|---|---|---|
| [`v26-locked-eight-claim-ledger.md`](v26-locked-eight-claim-ledger.md) ([JSON copy](v26-locked-eight-claim-ledger.json)) | v26 manuscript wording for the locked eight {F1, F4, F7, F11, F12, F18, F19, F22}, compared with the Lean carriers, plus five cross-cutting rows (count and pin, axiom ledger, Conjecture 1 wording, forge TH10, affected surfaces) | Historical review pins remain szl-papers `5f2f75f`, lutar-lean `04f904e`, and szl-forge `bd0419b`. The separate [locked-claim contract](../metadata/locked-claim-contract.json) binds all 24 ledger carriers to the exact `lutar-lean` `c4c42baf` kernel-evidence artifact. | Draft for owner review (2026-10-06, revised 2026-11-02); CI wiring decision D9 taken without accepting or promoting manuscript wording |

## Checking a ledger

```bash
python3 scripts/check_review_ledger.py --self-test
python3 scripts/check_review_ledger.py
python3 scripts/check_locked_claim_contract.py --self-test
python3 scripts/check_locked_claim_contract.py
# optional, with a lutar-lean checkout at the pinned commit:
python3 scripts/check_review_ledger.py --lean-root <lutar-lean>
```

The checker is stdlib-only, offline and read-only. It checks structure, types, pins, enums,
verbatim quotes and the org overclaim guard's line rules. The Markdown ledger must be exactly the
checker's rendering of the JSON copy (`--render` prints it), so a Markdown line with no JSON
counterpart fails as well as a JSON item missing from the Markdown. A default run
compares the manuscript anchors and szl-papers quotes with the current checkout. lutar-lean
quotes are compared only with `--lean-root`, which also checks the sha256 of the two kernel
input files and the `LockedGuard.lean` carrier list; szl-forge quotes are not checked by the
script. It does not re-run the Lean kernel.

`check_locked_claim_contract.py` additionally verifies the vendored member from
[`lutar-lean` Lake-build run 41392659869](https://github.com/szl-holdings/lutar-lean/actions/runs/41392659869).
It recomputes the evidence manifest's canonical digest, checks the artifact-member
SHA-256 and receipt, requires the exact eight formula IDs and 24 allowed carriers,
and matches every carrier declaration and axiom set to this ledger. It also binds
the v26 repository-source manuscript bytes while preserving that v21 is the latest
published DOI version. Both checks run through `claim-registry.yml`; this is a
consistency gate, not a manuscript correction, proof replay, publication, runtime
receipt, or claim-promotion authority.

## Subsequent operational disposition

The P-X4 finding and its quotes retain the original historical pin. Forge PR #594
(`97980acf54f408e6abe5ec0dac34ad1761a3e822`) subsequently corrected TH10 to TRACKED
with its unproven limitation and preserved the historical run manifest. Its Space
publication was independently read back at `f1dea80259a659ead2882c5e384effe56ec0a923`.
This is delivery evidence for the index correction, not a new theorem or an owner
decision to alter the manuscript. D5 now records that remaining wording decision.
