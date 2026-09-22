# Primary evidence map

**Purpose:** admissible, source-level anchors for the flagship CTO paper and its proof pack.

**Read on:** 2026-09-22

## Evidence classes

| Class | Meaning | May support |
|---|---|---|
| `SOURCE_BACKED` | Directly stated by a versioned source artifact | Architecture, doctrine, schema, and limitation claims |
| `REPRODUCIBLE` | A source provides executable steps and bounded expected behavior | Reproduction procedure claims |
| `STRUCTURE_ONLY` | Artifact proves schema/fixture contract but not cryptographic validity, model quality, or production readiness | Narrow evaluator claims only |
| `NOT_AUTHORITY` | A score, receipt, model card, or formula may constrain/evidence a decision but cannot authorize an effect alone | Prohibited-substitution controls |

## 1. Signed receipt provenance

**Source:** `https://huggingface.co/datasets/SZLHOLDINGS/szl-lake`

- The public lake describes a hash-linked Khipu receipt corpus with ECDSA P-256 DSSE signature material, a public-key manifest, and a documented cosign verification procedure.
- It identifies 14 real DSSE-signed Amaru tick receipts and 2 real Sentra verdict receipts.
- A11oy, Rosie, and Killinchu chains are explicitly represented as empty or unavailable rather than padded.
- Receipts pin the locked kernel anchor `c7c0ba17` and carry the 749 declarations / 14 unique axioms / 163 tracked-sorries baseline.

**Admissible paper claim:** integrity/origin and chain-linkage evidence can be verified where signature material and public keys are present.

**Prohibited claim:** a valid receipt proves the correctness, safety, value, or authority of the action it records.

## 2. Formal status and locked baseline

**Source:** `https://huggingface.co/datasets/SZLHOLDINGS/lean-proofs-v1`

- Canonical locked numbers: 749 declarations, 14 unique axioms, and 163 sorries; dataset tag `0086521`.
- Status labels are explicit: `PROVEN`, `SORRY`, `AXIOM`, and `CONJECTURE`.
- `A2 IsHomogeneous` is an axiom; `A4 IsBounded` is recorded as proven.
- Lambda uniqueness is Conjecture 1, with a `sorry` at `Lutar/Uniqueness.lean:120`.
- The reproducible build boundary is `lake build`, using the pinned Lean toolchain and Mathlib v4.13.0.

**Admissible paper claim:** formal artifacts are status-labeled and version-bounded; not all declarations are theorem-proved.

**Prohibited claim:** zero-sorry formal verification, unconditional Lambda uniqueness, or formal proof of general system trust.

## 3. Formula registry and hard stops

**Source:** `https://huggingface.co/datasets/SZLHOLDINGS/canonical-formulas-v1`

- Registry scope: 21 pure, typed, no-IO Python formulas, corresponding Lean obligations, and the Codex-Kernel governed-loop composer.
- The canonical Lambda runtime form is a weighted geometric mean; alternative definitions are versioned as a uniform-weight special case or a deprecated quantum-tilted sub-gate.
- The documented composer smoke run has five steps, Lambda aggregate approximately 0.99729, `halted=False`, and `replay_ok=True`.
- Four stated hard-stop validators are `state_transition`, `drift_bounds`, `human_gate`, and `axis_floor`; validator failure halts the loop.
- The registry labels DSSE signatures as placeholder where Sigstore is not wired into CI.

**Admissible paper claim:** the estate specifies a typed formula and bounded-loop control design.

**Prohibited claim:** Lambda is authority; smoke output is production validation; placeholder signing is cryptographic CI evidence.

## 4. Governability benchmark boundary

**Source:** `https://huggingface.co/datasets/SZLHOLDINGS/governed-agent-bench`

- The immutable mirror pins its reference source to `szl-holdings/a11oy@1b40fcbe0f65c1ad1e07776f83aa01abb067e864`.
- It covers fail-closed behavior, non-increasing delegated authority, false-success rejection, receipt completeness, and rollback discipline.
- Its own labels are `SAMPLE` corpus, `COMPUTED` scores, `STRUCTURE_ONLY` receipt verification, and cryptographic verification `false`.
- The reference fixture proves the evaluator's deterministic contract; it is explicitly not a model-quality or production claim.

**Admissible paper claim:** a reproducible evaluator exercises five governability dimensions at the documented reference-fixture boundary.

**Prohibited claim:** production readiness, cryptographically verified benchmark results, or a public-model leaderboard result.

## 5. Model identity and publication gate

**Source:** `https://huggingface.co/datasets/SZLHOLDINGS/model-bom`

- The registry records CycloneDX 1.5 BOMs for 44 public models as of its stated audit snapshot.
- Each BOM records file-level components, declared model metadata, dependency closure, and audit properties including `szl:heldout_eval` and `szl:publication_eligible`.
- `publication_eligible=false` is explicitly a gate: a held-out evaluation receipt must be attached and verified before the flag can become true.
- The registry notes that per-repository BOM copies remained pending a write-scoped credential; the dataset itself is the registry of record.

**Admissible paper claim:** model identity and publication eligibility are represented as auditable metadata with an explicit held-out-evaluation gate.

**Prohibited claim:** all models are evaluated, all models are publishable, or a BOM alone certifies runtime behavior.

## Global rule

```text
Evidence constrains authority.
Authority remains a separately scoped, time-bounded, revocable decision.
A model proposes; it does not self-authorize.
A formula measures; it does not self-authorize.
A receipt records; it does not self-authorize.
A benchmark evaluates a bounded contract; it does not self-authorize.
```
