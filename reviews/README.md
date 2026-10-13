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
| [`v26-locked-eight-claim-ledger.md`](v26-locked-eight-claim-ledger.md) ([JSON copy](v26-locked-eight-claim-ledger.json)) | v26 manuscript wording for the locked eight {F1, F4, F7, F11, F12, F18, F19, F22}, compared with the Lean carriers, plus five cross-cutting rows (count and pin, axiom ledger, Conjecture 1 wording, forge TH10, affected surfaces) | szl-papers `5f2f75f`, lutar-lean `04f904e`, szl-forge `bd0419b`. Cited files re-checked on 2026-10-13 at szl-papers `05bc280`, lutar-lean `f73bdba` and szl-forge `cd66836`: all have the same git blob except lutar-lean `.github/workflows/lake-build.yml`, which changed outside the cited lines 240-260 | Draft for owner review (2026-10-06, revised 2026-10-13); owner decisions D1 and D3-D9 open |

## Checking a ledger

```bash
python3 scripts/check_review_ledger.py --self-test
python3 scripts/check_review_ledger.py
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
script. It does not re-run the Lean kernel. It is not wired into CI; wiring it through
`claim-registry.yml` is owner decision D9.
