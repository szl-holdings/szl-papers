# Math-to-Runtime Execution Matrix

**Status:** design and test-routing contract  
**Scope:** maps the published proof corpus to executable tests and governance receipts.  
**Honesty boundary:** this file does not prove a theorem, qualify a model, authorize a deployment, or convert a CI pass into mathematical proof.

## Source authorities

- **Proof authority:** [szl-holdings/lutar-lean](https://github.com/szl-holdings/lutar-lean), at the exact proof revision named by the release evidence.
- **Formula/runtime authority:** [szl-holdings/szl-formulas](https://github.com/szl-holdings/szl-formulas), [szl-holdings/szl-forge](https://github.com/szl-holdings/szl-forge), and [szl-holdings/szl-invariants](https://github.com/szl-holdings/szl-invariants).
- **Receipt authority:** [governed-receipt-spec](https://github.com/szl-holdings/governed-receipt-spec) and [szl-receipt](https://github.com/szl-holdings/szl-receipt).
- **Observability binding:** [vsp-otel](https://github.com/szl-holdings/vsp-otel).
- **Publication authority:** this repository's source revision plus the separate Hugging Face publication and verification receipt. A GitHub test pass is not a Hugging Face publication witness.

## Proof-status tiers

| Tier | Meaning | Allowed runtime language |
|---|---|---|
| Locked-proven | The declaration is in the exact locked registry at the cited Lean revision and its proof evidence is independently read back. | "locked proof" |
| Experimental | Machine-checked or CI-green, but outside the locked registry. | "experimental machine-checked" |
| Conjecture/open | Not proven; may have a counterexample or only conditional results. | "conjecture/open" |
| Advisory | A runtime policy or score gate, not a theorem. | "advisory gate" |

The current published doctrine names exactly eight locked entries: **F1, F4, F7, F11, F12, F18, F19, F22**. The Λ uniqueness claim is not an unconditional theorem: Conjecture 1 is disproved as stated, while conditional Theorem U is the supported result. Khipu BFT safety remains open/conditional. Counts and status must be read from the pinned source evidence rather than inferred from a dashboard.

## Executable mapping

| Formula | Runtime property to test | Primary implementation target | Required receipt evidence |
|---|---|---|---|
| F1 | Receipt replay and content/hash binding | `governed-receipt-spec/verify.py`, `szl-receipt` | source revision, fixture digest, verifier revision, PASS/FAIL |
| F4 | DAG acyclicity | `szl-forge/inference/validate_control_plane.py`, A11oy graph validators | graph input digest, cycle result, policy decision |
| F7 | FIFO/sequence ordering | `szl-receipt` chain verifier, `vsp-otel` span ordering | seq, prev, digest, trace/span IDs |
| F11 | Ledger conservation | `szl-quant`, `szl-quant-witness`, Forge ledger tests | input/output totals, invariant result, witness digest |
| F12 | Bounded coupling | `szl-formulas`, `szl-quant-witness` | bound parameters, observed value, threshold result |
| F18 | Reed–Solomon/recovery behavior | `szl-invariants` recovery fixtures and Forge recovery lane | shard set digest, recovery result, missing/corrupt shard IDs |
| F19 | Entropy-budget accounting | `szl-invariants`, `szl-energy-attest`, Forge cost/energy lane | measured value or explicit `UNAVAILABLE`, budget and result |
| F22 | Append-only monotonicity | `szl-receipt` chain, source/version admission checks | prior/current revision, monotonicity result, rollback pointer |

Every test must state whether it is a **property test**, **fixture replay**, **machine-checked declaration**, or **runtime observation**. A runtime observation cannot be labeled as a theorem.

## Cross-repository control path

The intended bounded path is:

1. `szl-papers` records the paper, version, DOI, proof-status tier, and source revision.
2. `lutar-lean` supplies the exact formal declaration and proof snapshot.
3. `szl-formulas`/ `szl-invariants` expose executable formula or invariant interfaces.
4. `szl-forge` binds formula identity and maturity into `control_plane.v1`, then runs pre/post witnesses.
5. `szl-receipt` emits a deterministic receipt; unsigned results remain `UNSIGNED-honest` and cannot authorize consequential action.
6. `vsp-otel` attaches trace/span identity without changing the mathematical status.
7. A11oy performs admission and postcondition verification; human approval and a signed receipt remain required at the consequential boundary.
8. Hugging Face publication is a separate writer and must produce a source, publication, and served-byte verification receipt.
9. `a-11-oy.com` and `a11oy.net` may display the evidence, but a reachable page is not proof of runtime readiness.

## Minimum receipt fields

A formula/test receipt should contain:

- `formula_id` and `status_tier`;
- exact source/proof revision and test-vector digest;
- test kind and verifier revision;
- input/output or graph/ledger digests;
- observed result and expected result;
- policy decision (`allow`, `deny`, `review`, or `abstain`);
- OpenTelemetry trace/span link when available;
- signer identity, signature status, and freshness;
- rollback/reference pointer.

For energy, use a real meter reading or `UNAVAILABLE`; never synthesize joules. For Λ, report an advisory gate only and never use it as the sole basis for `ALLOW`.

## Merge and publication gates

A change is not admitted merely because it is mergeable or CI-green. Before merge/publication:

- exact head and current base are captured;
- required checks complete without hidden/skipped qualification gates;
- the effect/control-plane decision is not `DENY` or unresolved `REVIEW_REQUIRED`;
- the source revision, formula registry, and receipt schema agree;
- any Hugging Face publication has an independent served-byte readback;
- public pages disclose the proof tier and known limits.

This matrix is intentionally conservative: it makes the math executable and auditable without claiming that executable tests prove the remaining conjectures.
