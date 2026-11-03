# Source-only readiness disclosure — NON-NORMATIVE

This is a reader-facing qualification of historical summaries, not a new claim
ledger, mathematical correction, release decision, or publication authorization.
It describes the source state at `2c5ece7fb3ee8b29ebf739f401d1e4f552354c0a`.
The canonical evidence, verdicts, and owner decisions remain in the linked records;
this note does not supersede them.

## v26/P3 remains held

The [papers index](../PAPERS_INDEX.md#arxiv-submission-line-preprint-packages-not-yet-posted)
preserves P3/v26 outside the current two-paper arXiv wave pending overlap review.
The [claim contract](../metadata/locked-claim-contract.json) identifies v26 as
repository source, not a separately DOI-published version. A source version, a
registry count, and a citable published work are different objects. This disclosure
does not clear the hold, authorize submission, or resolve the review ledger's open
owner decisions, including D1, D3, D4, and D7.

## Exact comparison scope, not a blanket verdict on the mathematics

The non-normative contract binds the exact v26 manuscript bytes and draft
[review ledger](v26-locked-eight-claim-ledger.md) to 24 Lean carrier declarations,
kernel-emitted axiom sets, and recorded artifact provenance at `lutar-lean` revision
`c4c42baf107f2cd5ec11ac3958fbd8fd06a875c8`.
Its paper-claim review verdicts are:

| Verdict | Claims |
|---|---|
| EXCEEDS | F1, F7, F11, F18 |
| PARTIAL | F4, F22 |
| MARGINAL | F12, F19 |

These verdicts compare the reviewed paper wording with the statements and
hypotheses evidenced at the pin. They do not say the checked declarations are
false, or settle all possible formulations of the underlying claims. For example,
the ledger distinguishes F1's function/map identities from recorded-root replay
and termination, and F18's parity arithmetic from codec correctness. The locked
registry count alone cannot establish those broader interpretations. Read the
per-claim evidence and limitations rather than treating this table as a replacement
for the ledger. The historical locked formulas and manuscripts are unchanged.

## What an offline guard pass does and does not establish

The existing claim-backing, review-ledger, and locked-contract checks test their
specified schema, classifications, quoted source anchors, pinned bytes, and
cross-record consistency. The contract binds recorded kernel evidence; its local
validator does not re-run the Lean kernel or independently authenticate a provider
artifact. Passing these checks is not runtime implementation/refinement evidence,
an empirical replication, or deployment, training, or research-publication
clearance. In particular, hashes establish byte agreement, not scientific validity.
The contract's paper-claim-promotion, publication, deployment, and runtime authority
fields remain explicitly false.

The [claims harvest note](../thesis/ouroboros/corpus-v18/claims_v18_extracted.json.HARVEST_NOTE.txt)
documents a partial historical harvest. The extracted JSON is a truncated prefix;
the claim-backing checker recovers complete leading objects. Its passing result
therefore covers the recovered subset under that check's classification rules,
including reference-only citations, not a complete corpus or kernel verification
of every claim. This disclosure neither repairs the harvest nor upgrades those
citations to proof evidence.

## Zenodo check and lifecycle decisions are separate

At this source state, `metadata/zenodo/ENABLED` is absent. The
[metadata renderer](../scripts/zenodo/render_zenodo.py) consequently returns success
with `REPORT_ONLY` for `--check`; that exit status is not an assertion that root
metadata agrees with rendered release metadata, or that a release is promotable.
This note does not enable the gate or alter metadata.

The [deposit policy](../ZENODO_DEPOSIT_POLICY.md) requires deliberate record
identity and version/supplement decisions, duplicate checks, and exact reviewed
artifact hashes. Its manual-deposit policy and the separate release/dispatch
DOI-sync path in the [metadata workflow](../.github/workflows/zenodo-metadata-gate.yml)
still require owner reconciliation; the
[disabled DOI-writeback workflow](../.github/workflows/doi-writeback.yml) does not
by itself settle that separate path. The existing local DOI ledger's title, tag,
and concept associations likewise require owner intent and provider readback
before any lifecycle or DOI-identity change. This is distinct from the
paper-wording comparisons above, and no fresh Zenodo provider verification is
claimed here. No DOI records, metadata, workflows, HF cards, formulas, manuscripts,
or authority fields are changed by this disclosure; it mints nothing and grants
no publication authority.
