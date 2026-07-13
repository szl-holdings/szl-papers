# A11oy formula and proof frontier audit

Date: 2026-07-12  
Scope: local A11oy formula registry, Lutar-Lean/Mathlib evidence, Ouroboros fixed-point artifacts, the Lutar invariant, the name "Alabada", and the existing wave-14 proof queue.  
Mutation boundary: research artifacts only; no production code, repository, model, deployment, or external system was changed.

## Executive verdict

The estate contains real executable formulas and real kernel-checked Lean work, but its inventories are non-additive and cannot honestly be summarized as "180 proved" or "200 proved."

- **8 locked formula families are PROVED** in the dedicated Lean receipt: `F1`, `F4`, `F7`, `F11`, `F12`, `F18`, `F19`, `F22`.
- Those eight families contain **19 audited declarations**, with zero non-comment `sorry`; their recorded axiom surface is limited to `propext` and `Quot.sound`.
- A fresh full build receipt for Lutar-Lean commit `85dee499b72cc71f49907c70e62018ab85dba01c` records Lean `4.18.0`, Mathlib `aa936c36e8484abd300577139faf8e945850831a`, **13,308/13,308 targets**, exit 0, and 21/21 guard tests.
- The A11oy served formula index has **15 entries: 7 declaration-backed, 8 experimental, 0 unbacked**. "Declaration-backed" is not the same as kernel-proved: the current guard proves name/corpus presence, not absence of `sorry` or an allowed `#print axioms` result.
- The canonical Python formula registry has **21 executable functions**, all TESTED. Runtime tests do not turn them into Lean proofs.
- The evidence ledger has **30 items: 19 TESTED, 4 SUPPORTED, 1 REFUTED, 6 OPEN**.
- The staged advisory index has **80 entries: 17 SUPPORTED, 63 OPEN**.
- The versioned manuscript CSV has **179 formal blocks: 46 SUPPORTED, 2 REFUTED, 131 OPEN**; these are manuscript constructs, not proofs.
- The existing proof queue has **203 records: 200 OPEN, 3 REFUTED**. By task: 131 formalize-and-prove, 63 exact-binding repairs, 7 discharge-or-measure, 2 preserve-counterexample.
- No exact 180-formula proof artifact exists in the audited workspace. The exact count **180 remains rejected as unsourced**.

## Evidence reconciliation

| Scope | Exact count | Current honest state | What it proves |
|---|---:|---|---|
| Locked formula families | 8 | PROVED | The 19 declarations in the pinned `ProvedFormulas.lean` receipt compile with the disclosed allowed axioms. |
| Locked declarations | 19 | PROVED within receipt scope | Encoded list, arithmetic, conservation, budget, queue, and monotonicity statements only; not every real-world interpretation suggested by the family names. |
| Served A11oy index | 15 | 7 declaration-backed / 8 experimental | Corpus/name integrity, not per-declaration kernel closure. |
| Python runtime functions | 21 | TESTED | Reproducible executable behavior under tests, not formal proof. |
| SymPy/units/evidence ledger | 30 | 19 TESTED / 4 SUPPORTED / 1 REFUTED / 6 OPEN | Symbolic, dimensional, definitional, or empirical evidence at the stated tier. |
| Staged theorem index | 80 | 17 SUPPORTED / 63 OPEN | Old advisory bindings; not an 80-proof corpus. |
| Manuscript formal blocks | 179 | 46 SUPPORTED / 2 REFUTED / 131 OPEN | Versioned prose/math blocks; no automatic Lean binding. |
| Proof obligations | 203 | 200 OPEN / 3 REFUTED | A bounded work queue, not training trajectories and not proofs. |

The locked-v11 source counters are **749 declarations / 14 unique named axioms / 149 non-comment sorries**. The audited current-main counters are **1,401 declarations / 25 unique named axioms / 270 non-comment sorries**. These are source counters, not theorem counts. A complete build can succeed while admitted axioms and `sorry` remain, so the full-build receipt must not be used to promote those counters to proofs.

There is also a lineage mismatch that must stay visible: the eight-family receipt was produced from working-tree base `85dee499...` and file SHA-256 `acce5d75...`; older doctrine pin metadata `c7c0ba17...` does not contain that module or `PROVEN_FORMULAS.md`. The receipt must never be represented as evidence from the old `c7` pin.

## Served registry audit

The current A11oy guard reports `7 verified`, but its status means *the named declaration exists somewhere in the local corpus*. The replacement schema should split four independent facts: declaration presence, source closure, kernel acceptance, and axiom policy.

| Entry | Current guard | Proof-frontier disposition | Required next evidence |
|---|---|---|---|
| `pacbayes` | declaration-backed | SUPPORTED | Isolated compile and `#print axioms pacBayes_inequality_form`; do not inherit the two `sorry` obligations in the probabilistic wrapper. |
| `welford` | declaration-backed | SUPPORTED | Isolated compile, zero-placeholder scan, `#print axioms welford_mean_exact`. |
| `quorum` | declaration-backed | **OPEN_CONJECTURE** | `khipu_consensus_safety` contains `sorry` and is explicitly Conjecture 2; downgrade the served proof label while retaining the source binding. |
| `bloom` | declaration-backed | SUPPORTED | Isolated compile and axiom receipt for `query_after_insert`. |
| `kalman` | declaration-backed | SUPPORTED | Isolated compile and axiom receipt for `posterior_le_prior`. |
| `bls` | declaration-backed | SUPPORTED_MODEL | Compile and axiom receipt; preserve that this is an abstract additive-module model, not production BLS cryptography. |
| `hnsw` | declaration-backed | SUPPORTED_MODEL | Compile and axiom receipt; preserve that the theorem follows the encoded strictly-decreasing-distance model, not arbitrary deployed HNSW performance. |
| `holevo`, `reidemeister`, `kl`, `pinsker`, `aftershock`, `allodial`, `entanglement`, `sovereign` | experimental | EXPERIMENTAL/MEASURED-AS-APPLICABLE | Keep out of proof totals until an exact artifact, commit, compilation receipt, and axiom report exist; empirical `aftershock` must never be promoted by Lean alone. |

## Lutar invariant boundary

The local source defines the equal-weight geometric mean

`Lambda_k(x) = (product_i x_i)^(1/k)`

and includes concrete proofs for the definition/normalization and several properties. It does **not** establish unconditional uniqueness from A1-A5. The repository already contains the machine-checkable counterexample `Round13.maxAgg_ne_Lambda`, and the old `Uniqueness.lean` still contains two tracked `sorry` obligations. The correct state is therefore:

- the Lambda function and individually closed properties: eligible for isolated receipts;
- unconditional Lambda uniqueness under A1-A5: **REFUTED; preserve the counterexample**;
- uniqueness under added multiplicativity/block-consistency assumptions: **CONDITIONAL/AXIOM-GATED** until each bridge axiom is disclosed and each theorem has a pinned `#print axioms` receipt;
- Lambda as a runtime trust aggregate: usable as a declared policy function, never as a uniquely compelled oracle.

Trying to "finish" the old unconditional uniqueness proof would be proving a false statement. The frontier is to formalize the maximal true conditional theorem and preserve `maxAgg_ne_Lambda` as a permanent regression test.

## Ouroboros proof boundary

Two relevant Lean source artifacts exist outside the locked eight-family kernel:

1. `ouroboros_banach_loop_convergence`: a direct specialization of Mathlib's contraction fixed-point theorem. It proves a unique fixed point **only** when the state space is complete and the transition is supplied with an explicit contraction factor `0 <= k < 1` and distance inequality.
2. `ouroboros_kleene_least_fixed_point`: a complete-lattice/order-homomorphism least-fixed-point statement. It proves a least fixed point in the encoded order model, not operational termination, wall-clock convergence, or safe self-modification.

Their bodies contain no `sorry` by local inspection and the full library build is green, but neither is in the locked eight-family count and the available artifacts do not contain dedicated per-declaration `#print axioms` receipts. Proposed state: `SUPPORTED_SOURCE_PRESENT`, promotable only after isolated build receipts at the exact full-build commit.

The machine-checkable Ouroboros frontier is not a mystical infinite loop. It is a bounded state transition system with three separately proved obligations:

- **progress/termination**: a well-founded natural-number measure strictly decreases, or a hard fuel bound is consumed;
- **safety invariant**: every admitted transition preserves policy, receipt-chain, and effect-boundary invariants;
- **convergence**: only for transitions that actually satisfy a proved contraction/order hypothesis.

## "Alabada" and historical provenance

No exact `Alabada`/`Alabadda` named formula, Lean declaration, registry entry, or manuscript-bound artifact was found in the audited proof/formula scopes. It cannot enter the registry as a proof claim until the owner supplies a canonical spelling, equation, domain/codomain, hypotheses, source location, and intended operational interpretation. The delta proposal creates a quarantined alias request, not a theorem.

Ancient, Newtonian, and other historical material is valuable provenance and a source of candidate structures. The local tree contains Babylonian/Heron iteration, Egyptian unit fractions, Liu Hui polygon doubling, Madhava remainder bounds, sexagesimal arithmetic, Maya LCM, and a Kepler/Newton scaling reference. Their age or attribution is never proof evidence. Each modern formal statement still requires an exact Lean theorem, pinned toolchain, zero `sorry`/`admit`, and an axiom allowlist; physical constants or performance claims additionally require measurement and uncertainty evidence.

## Bounded machine-check plan

### Gate 0 — freeze identity

For every candidate record: stable ID, exact natural-language statement, exact Lean declaration name, source commit/path/SHA-256, Lean version, Mathlib SHA, allowed axioms, maturity, and any empirical dependency. Reject ambiguous names and manuscript-only claims before generation.

### Gate 1 — classify before proving

- `FORMAL`: arithmetic, algebraic, structural, finite combinatorial, state-machine, schema, conservation, or invariant claim.
- `CONDITIONAL`: theorem is valid only under explicit model/bridge assumptions.
- `EMPIRICAL`: requires measurements, calibration, dataset, baseline, and uncertainty; Lean may prove the analysis pipeline but not the observation.
- `REFUTED`: retain a compiling counterexample; never regenerate the false target.
- `UNSPECIFIED`: quarantine pending a formal statement (`Alabada` is here).

### Gate 2 — repair the 63 bindings first

Resolve each advisory ID to a current declaration using exact module/name matching. A repaired binding is only `SUPPORTED` until the target module compiles and `#print axioms` passes policy. This is deterministic metadata work and should precede model generation.

### Gate 3 — prove eligible open statements in four cohorts

1. **Finite/decidable**: `by decide`, `native_decide`, `simp`, finite enumeration; require counterexample search first.
2. **Algebra/order**: `ring`, `linarith`, `nlinarith`, `positivity`, Mathlib inequalities; explicitly state domain and nonzero/positivity assumptions.
3. **State/invariant**: induction over traces/lists/transitions; prove base, step preservation, bounded progress, and replay determinism separately.
4. **Analysis/probability/physics**: reuse Mathlib theorems with explicit measurability/integrability/completeness assumptions; physical interpretations remain MODELED until measured.

Every one of the 203 queue records already has a stable ID and a task. The cohort rule in the JSON delta supplies the path for every eligible record: repair binding; attempt counterexample; formalize exact theorem; compile; scan placeholders; print axioms; store receipt. Ineligible empirical or unspecified records stop at measurement/specification, rather than receiving synthetic proofs.

### Gate 4 — compiler-in-the-loop generation

Retrieve premises from pinned Mathlib/Lutar-Lean; generate multiple candidates; compile every candidate; reject nonzero exit, `sorry`, `admit`, unexpected axioms, source drift, and duplicate proof bodies. Parallel candidates increase search only; they do not vote a theorem true. The existing evaluation contract remains `NOT_RUN` because there are zero accepted local proof trajectories.

### Gate 5 — promotion receipt

Promotion to PROVED requires:

- exact source and dependency digests;
- Lean exit 0 on the target declaration/module;
- zero `sorry` and `admit` in the admitted dependency closure;
- `#print axioms` subset of the declared policy;
- counterexample search result retained;
- independent review;
- signed receipt or explicit `UNSIGNED_LOCAL_RECEIPT`.

## Quantum cross-reference

The wave-16 quantum design report already states the right boundary: Lean can prove encoded arithmetic, schema invariants, admissibility, conservation, and transformations, but cannot prove a device's fidelity or quantum advantage without measurements. Apply the same proof gate to QAOA/VQE/resource-estimate claims from `primary-sources.md`: preserve the exact backend, circuit/IR, shots, calibration age, classical baseline, uncertainty, and raw observations. QED-C/MQT/Metriq-style benchmark artifacts may support measurement; they do not alter the formal proof count.

## Release recommendation

Do not train a new foundation model from the 179 manuscript blocks. First publish a review-only `szl-proof-obligations-v1` queue, repair the 63 bindings, preserve the three refutations, and accumulate kernel-accepted trajectories under the frozen evaluation contract. The next numerical milestone should be **accepted receipts**, not a marketing total: `8 locked families / 19 admitted declarations` remains the only locked proof headline until the admission gate produces new receipts.

## Audited local evidence

- `data/formula_readiness_ledger.json`
- `data/proof_obligations_v1.jsonl`
- `evidence/paper1/lean-proved-formulas-receipt.json`
- `evidence/paper1/lutar-lean-full-build-receipt.json`
- `${WORKSPACE_ROOT}/work/a11oy-wave15-release/a11oy_formula_endpoints.py`
- `${WORKSPACE_ROOT}/work/a11oy-wave15-release/a11oy_formula_registry_guard.py`
- `${WORKSPACE_ROOT}/work/a11oy-wave15-release/proofs/lutar-lean/Lutar/Invariant.lean`
- `${WORKSPACE_ROOT}/work/a11oy-wave15-release/proofs/lutar-lean/Lutar/Round13/Lambda_Uniqueness.lean`
- `${WORKSPACE_ROOT}/work/a11oy-wave15-release/proofs/lutar-lean/Lutar/Innovations/round5/OuroborosBanachLoop.lean`
- `${WORKSPACE_ROOT}/work/a11oy-wave15-release/proofs/lutar-lean/Lutar/Innovations/round5/OuroborosKleeneHalt.lean`
- `${WORKSPACE_ROOT}/outputs/quantum-wave16/primary-sources.md`
- `${WORKSPACE_ROOT}/outputs/quantum-wave16/northwestern-quantum-ecosystem-szl-design-report.md`

