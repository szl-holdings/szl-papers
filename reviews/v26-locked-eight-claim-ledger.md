# v26 locked-eight claim ledger

> **Non-normative review.** This ledger compares what the v26 manuscript says about the locked
> eight with the Lean declarations that carry them at a pinned lutar-lean commit. It changes no
> manuscript, doctrine, Lean, forge or arXiv file. Verdicts and proposed wording are review
> opinions for the owner; nothing here takes effect until the owner decides (see
> [Owner decisions](#owner-decisions)).
>
> Status: `DRAFT_FOR_OWNER_REVIEW` · Date: 2026-10-06 · Machine-readable copy:
> [`v26-locked-eight-claim-ledger.json`](v26-locked-eight-claim-ledger.json) · Consistency check:
> `python3 scripts/check_review_ledger.py --self-test && python3 scripts/check_review_ledger.py`

## Pinned sources

| Source | Repository | Commit | Notes |
|---|---|---|---|
| Manuscript `thesis/ouroboros/papers/v26/unified-gpd-thesis-v26.md` (504 lines) | `szl-holdings/szl-papers` | `5f2f75f109bfdadfc167c00bab5808a7a76ac3e2` | git blob `ea9d5e7162bf5d3f400367401cb792e1bbf1c545` |
| Lean locked surface | `szl-holdings/lutar-lean` | `04f904ecd5683753a481ab2b1ded69ac01a7a661` | `ProvedFormulas.lean` last changed in `5cfaf9a3`; `claims/locked-formulas.v1.json` in `3b0b589e`; F22 first added in `e6de491d` |
| Doctrine-v11 count baseline | `szl-holdings/lutar-lean` | `c7c0ba17c2eaec60ad38ea9172b4a0d9ca0b582f` | Doctrine-v11 canonical-count baseline (749/14/163), dated 2026-05-31. It predates every locked carrier declaration. |
| Forge lab index (P-X4 only) | `szl-holdings/szl-forge` | `bd0419b6e96c84608e38c3bce3f4360df265ac95` | spaces/szl-forge-lab/thesis_formula_index.json is byte-identical at db0c709d917b2b7027eb5e4e5729b29236996eb2 (szl-forge main on 2026-10-06). |

Every Lean declaration, file:line reference and statement below was read with
`git show 04f904ec:<path>` on 2026-10-06. Manuscript line numbers are 1-based lines of the
file at the szl-papers pin; the checker fails if a quote is no longer on its cited line. On
2026-10-06 all lutar-lean quotes and statements in this ledger were also compared with a
`git show` export of the pinned files (`check_review_ledger.py --lean-root`, MEASURED).

## Kernel axiom evidence (MEASURED, not CI)

- **Status:** `MEASURED` on 2026-10-06. **CI replay:** `NOT_RUN`.
- **Method:** Bare-core replica of the lake-build.yml 'Locked-8 axiom guard' step: lean -o <olean dir>/Lutar/Puriq/Formulas/ProvedFormulas.olean Lutar/Puriq/Formulas/ProvedFormulas.lean, then LEAN_PATH=<olean dir> lean tools/lean/LockedGuard.lean. Both files were exported unchanged from lutar-lean at the pin.
- **Environment:** Lean 4.18.0 (x86_64-w64-windows-gnu, commit 11ccbced7964), no Mathlib, no lake, Windows 11. Not CI.
- **Result:** 24/24 carriers allowed, 0 refused. 11 use no axiom, 10 use `propext` only, 3 use `propext` + `Quot.sound`; 0 use `Classical.choice`.
- **Trust base** (`tools/lean/LockedGuard.lean:28`): `{propext, Classical.choice, Quot.sound}`.
- **Input hashes (sha256):** `Lutar/Puriq/Formulas/ProvedFormulas.lean` `d9a7dacb6e27c8e229f97dd2d033e3545926a7704c4de4b19c39179f5308bfb9`; `tools/lean/LockedGuard.lean` `0b1d7c65409bc5b445c19d7e122a66dee4d0330f640ea42e1a39a5548a279468`.
- **Agrees with:** The LockedGuard.lean header cross-check of 2026-09-30 (11 / 10 / 3) and the recon run earlier on 2026-10-06.
- **Re-run when:** lutar-lean PR #313 (monthly Lean + Mathlib drift bump, OPEN on 2026-10-06) or any change to ProvedFormulas.lean or LockedGuard.lean.
- Axiom lists below are shown as emitted by LockedGuard (deduplicated, sorted by name string), so Quot.sound sorts before propext.

## Verdict scale

- **EXCEEDS**: The manuscript wording claims materially more than the cited Lean statements carry.
- **PARTIAL**: Some anchors match the Lean statements; others overreach, mis-cite a name or mis-state an axiom set.
- **MARGINAL**: The manuscript already disclaims the main gap; a word-level mislabel remains.
- **MATCHES**: No discrepancy found between the anchors and the Lean statements.

## Summary

| Row | Locked id | Primary Lean declaration | Kernel axioms (primary) | Verdict | Severity |
|---|---|---|---|---|---|
| P-F1 | F1 | `Puriq.Formula.Proved.f1_replay_hash_determinism` | none | **EXCEEDS** | major |
| P-F4 | F4 | `Puriq.Formula.Proved.f4_khipu_dag_acyclic_preserved` | propext | **PARTIAL** | moderate |
| P-F7 | F7 | `Puriq.Formula.Proved.f7_chaski_fifo_order` | propext | **EXCEEDS** | moderate |
| P-F11 | F11 | `Puriq.Formula.Proved.f11_ayni_reciprocity_conservation` | propext | **EXCEEDS** | minor |
| P-F12 | F12 | `Puriq.Formula.Proved.f12_kuramoto_additive` | none | **MARGINAL** | minor |
| P-F18 | F18 | `Puriq.Formula.Proved.f18_reed_solomon_parity_count` | none | **EXCEEDS** | major |
| P-F19 | F19 | `Puriq.Formula.Proved.f19_bekenstein_additive` | none | **MARGINAL** | minor |
| P-F22 | F22 | `Puriq.Formula.Proved.f22_khipu_emit_monotone` | Quot.sound, propext | **PARTIAL** | moderate |

| Row | Cross-cutting topic | Verdict | Severity |
|---|---|---|---|
| P-X1 | Locked-count theorem, the c7c0ba17 pin and A.2 identifiers | **EXCEEDS** | major |
| P-X2 | Axiom ledger compared with kernel-emitted axiom sets | **PARTIAL** | moderate |
| P-X3 | Conjecture 1 and the Λ boundary wording | **PARTIAL** | moderate |
| P-X4 | szl-forge TH10 index entry | **EXCEEDS** | moderate |
| P-X5 | Affected surfaces outside the v26 manuscript | **inventory** | - |

## Per-formula rows

### P-F1 · EXCEEDS · F1 replay determinism

Verdict **EXCEEDS** · severity major · locked id F1

**Lean declarations** (lutar-lean `04f904ec`):

- `Puriq.Formula.Proved.f1_replay_hash_determinism` (primary) · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:53-54` · kernel axioms: none

  ```lean
  theorem f1_replay_hash_determinism {α β : Type} (f : α → β) (x : α) : f x = f x := rfl
  ```

- `Puriq.Formula.Proved.f1_replay_trace_stable` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:57-58` · kernel axioms: none

  ```lean
  theorem f1_replay_trace_stable {α β : Type} (f : α → β) (xs : List α) : xs.map f = xs.map f := rfl
  ```

**What the Lean states.** Reflexive equality of a pure function application (f x = f x) and of List.map (xs.map f = xs.map f), both closed by rfl.

**Manuscript anchors** (verbatim):

- §6.1, L256: `Re-executing the recorded inputs reproduces the recorded root.`
- Abstract, L21: `anchored by **F1 replay determinism** (locked, kernel-verified)`
- §3.2, L130: `P1 governs *that the loop terminates* (well-founded recursion + F1 replay)`
- §7.3, L294: `` replay determinism (`f1_replay_hash_determinism`; P1/P2 anchor) ``
- §8.1, L315: `the loop terminates / record re-derives | F1 replay determinism`

**Manuscript claim.** Re-executing recorded inputs reproduces the recorded Merkle root of the receipt chain, and F1 anchors loop termination (P1) and re-derivation of the record (P1/P2).

**Gap.** Both theorems are instances of rfl. They mention no hash, root, log, recorded input, I/O or termination measure, so the replay-root, termination and re-derivation readings are not carried by them. lutar-lean already narrowed its own wording in 3b0b589 (claims JSON F1 refinement_gap and public_wording; PROVEN_FORMULAS.md:25); the manuscript was not updated.

**Proposed wording** (for the owner; not applied):

> F1 [locked]: reflexive equality of a pure function application and of List.map (f x = f x; xs.map f = xs.map f). It does not establish replay-hash stability of a recorded log, reproduction of a recorded root, or loop termination.

**Owner decisions:** D1, D7 · **Runtime symbol named in claims JSON** (not inspected here; R01 scope): none

**Cross-references** (lutar-lean already narrowed its own wording):

- `claims/locked-formulas.v1.json:73` @ `04f904ec`: `Locked F1 is reflexive equality of a pure application and of List.map. It is not a production replay-hash proof.`
- `PROVEN_FORMULAS.md:25` @ `04f904ec`: `Compiled locked F1 is reflexive equality`

### P-F4 · PARTIAL · F4 Khipu DAG acyclicity preservation

Verdict **PARTIAL** · severity moderate · locked id F4

**Lean declarations** (lutar-lean `04f904ec`):

- `Puriq.Formula.Proved.f4_khipu_dag_acyclic_preserved` (primary) · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:165-169` · kernel axioms: `propext`

  ```lean
  theorem f4_khipu_dag_acyclic_preserved (es : KhipuEdges) (inv : KhipuBackwardInvariant es) (k : Nat) (newEdges : KhipuEdges) (hk : ∀ e ∈ newEdges, e.1 = k ∧ e.2 < k) : ∀ a, ¬ KhipuReach (es ++ newEdges) a a :=
  ```

- `Puriq.Formula.Proved.f4_khipu_reach_decreases` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:132-134` · kernel axioms: none

  ```lean
  theorem f4_khipu_reach_decreases (es : KhipuEdges) (inv : KhipuBackwardInvariant es) {a b : Nat} (r : KhipuReach es a b) : b < a := by
  ```

- `Puriq.Formula.Proved.f4_khipu_no_cycle` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:141-143` · kernel axioms: none

  ```lean
  theorem f4_khipu_no_cycle (es : KhipuEdges) (inv : KhipuBackwardInvariant es) (a : Nat) : ¬ KhipuReach es a a := by
  ```

- `Puriq.Formula.Proved.f4_khipu_append_preserves_invariant` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:150-154` · kernel axioms: `propext`

  ```lean
  theorem f4_khipu_append_preserves_invariant (es : KhipuEdges) (inv : KhipuBackwardInvariant es) (k : Nat) (newEdges : KhipuEdges) (hk : ∀ e ∈ newEdges, e.1 = k ∧ e.2 < k) : KhipuBackwardInvariant (es ++ newEdges) := by
  ```

- `Puriq.Formula.Proved.f4_khipu_no_self_loop` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:117` · kernel axioms: none

  ```lean
  theorem f4_khipu_no_self_loop (src dst : Nat) (h : dst < src) : src ≠ dst := by
  ```

- `Puriq.Formula.Proved.f4_khipu_acyclic_irrefl` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:121` · kernel axioms: none

  ```lean
  theorem f4_khipu_acyclic_irrefl (n : Nat) : ¬ (n < n) := Nat.lt_irrefl n
  ```

- `Puriq.Formula.Proved.f4_khipu_reach_strictly_smaller` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:125-127` · kernel axioms: none

  ```lean
  theorem f4_khipu_reach_strictly_smaller (src mid dst : Nat) (e1 : mid < src) (e2 : dst < mid) : dst < src := Nat.lt_trans e2 e1
  ```

- `Puriq.Formula.Proved.KhipuEdges` · abbrev · `Lutar/Puriq/Formulas/ProvedFormulas.lean:98` · definition (no axiom check)

  ```lean
  abbrev KhipuEdges := List (Nat × Nat)
  ```

- `Puriq.Formula.Proved.KhipuBackwardInvariant` · def · `Lutar/Puriq/Formulas/ProvedFormulas.lean:102-103` · definition (no axiom check)

  ```lean
  def KhipuBackwardInvariant (es : KhipuEdges) : Prop := ∀ e ∈ es, e.2 < e.1
  ```

- `Puriq.Formula.Proved.KhipuReach` · inductive · `Lutar/Puriq/Formulas/ProvedFormulas.lean:111-113` · definition (no axiom check)

  ```lean
  inductive KhipuReach (es : KhipuEdges) : Nat → Nat → Prop | base {a b : Nat} : KhipuStep es a b → KhipuReach es a b | trans {a b c : Nat} : KhipuStep es a b → KhipuReach es b c → KhipuReach es a c
  ```

**What the Lean states.** For a finite Nat×Nat edge list in which every edge (src, dst) has dst < src, every KhipuReach path strictly decreases the node index, so no node reaches itself; appending edges (k, d) with d < k keeps the invariant and therefore acyclicity.

**Manuscript anchors** (verbatim):

- Abstract, L21: `**F4** (the Khipu receipt DAG is acyclic and stays acyclic under append)`
- §7.3, L295: `` appending a backward edge `dst < src` preserves acyclicity of the receipt DAG ``
- §7.3, L295: `now a genuine theorem over a transitive-closure reachability model`
- A.2, L450: `#print axioms Lutar.f4_khipu_dag_acyclic_preserved`

**Manuscript claim.** The Khipu receipt DAG is acyclic and stays acyclic under append (Abstract); appending a backward edge dst < src preserves acyclicity (§7.3); A.2 cites Lutar.f4_khipu_dag_acyclic_preserved with axioms {propext, funext, Classical.choice, Quot.sound}.

**Gap.** §7.3 (L295) matches the Lean model. The Abstract (L21) presents the Nat-indexed edge-list model as the deployed receipt DAG; a deployed store is covered only if it enforces dst < src on every append, which is outside the theorem. A.2 (L450) uses a name that does not resolve at the pin (the declaration is Puriq.Formula.Proved.f4_khipu_dag_acyclic_preserved) and an axiom set that differs from the kernel-emitted [propext] (see P-X2). Minor: hk constrains new edges to source k and targets below k; it does not require k to be fresh, which acyclicity does not need, so the docstring's 'fresh max node' is not a hypothesis.

**Proposed wording** (for the owner; not applied):

> F4 [locked]: for a finite Nat×Nat edge list in which every edge points to a strictly smaller node (dst < src), every path strictly decreases the node index, so no node reaches itself; appending edges (k, d) with d < k preserves this. A deployed receipt store inherits acyclicity only if it enforces dst < src on every append. Byzantine agreement is not addressed (Conjecture 2 stays open).

**Owner decisions:** D1, D7 · **Runtime symbol named in claims JSON** (not inspected here; R01 scope): `tools.locked_formula_runtime.khipu_backward_acyclic`

**Cross-references** (lutar-lean already narrowed its own wording):

- `claims/locked-formulas.v1.json:91` @ `04f904ec`: `Does not prove acyclicity of a store that admits forward edges, concurrent writers, or Byzantine voters. Does not prove Khipu BFT.`

### P-F7 · EXCEEDS · F7 Chaski FIFO reception order

Verdict **EXCEEDS** · severity moderate · locked id F7

**Lean declarations** (lutar-lean `04f904ec`):

- `Puriq.Formula.Proved.f7_chaski_fifo_order` (primary) · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:230-232` · kernel axioms: `propext`

  ```lean
  theorem f7_chaski_fifo_order (msgs : List Nat) : chaskiDrain (chaskiEnqueueAll [] msgs) = msgs := by rw [f7_chaski_enqueueAll_nil, f7_chaski_drain_eq]
  ```

- `Puriq.Formula.Proved.f7_chaski_fifo_positional` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:237-239` · kernel axioms: `propext`

  ```lean
  theorem f7_chaski_fifo_positional (msgs : List Nat) (i : Nat) : (chaskiDrain (chaskiEnqueueAll [] msgs))[i]? = msgs[i]? := by rw [f7_chaski_fifo_order]
  ```

- `Puriq.Formula.Proved.f7_chaski_drain_eq` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:209` · kernel axioms: `propext`

  ```lean
  theorem f7_chaski_drain_eq (q : ChaskiQueue) : chaskiDrain q = q := by
  ```

- `Puriq.Formula.Proved.f7_chaski_enqueueAll_nil` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:203-205` · kernel axioms: `propext`

  ```lean
  theorem f7_chaski_enqueueAll_nil (xs : List Nat) : chaskiEnqueueAll [] xs = xs := by simp [chaskiEnqueueAll]
  ```

- `Puriq.Formula.Proved.f7_chaski_enqueue_preserves_prefix` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:216-218` · kernel axioms: `propext`

  ```lean
  theorem f7_chaski_enqueue_preserves_prefix (q : List Nat) (m : Nat) : (chaskiEnqueue q m).take q.length = q := by simp [chaskiEnqueue]
  ```

- `Puriq.Formula.Proved.f7_chaski_head_is_oldest` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:222-224` · kernel axioms: `propext`

  ```lean
  theorem f7_chaski_head_is_oldest (a m : Nat) (q : List Nat) : (chaskiEnqueue (a :: q) m).head? = some a := by simp [chaskiEnqueue]
  ```

- `Puriq.Formula.Proved.ChaskiQueue` · abbrev · `Lutar/Puriq/Formulas/ProvedFormulas.lean:182` · definition (no axiom check)

  ```lean
  abbrev ChaskiQueue := List Nat
  ```

- `Puriq.Formula.Proved.chaskiEnqueueAll` · def · `Lutar/Puriq/Formulas/ProvedFormulas.lean:188` · definition (no axiom check)

  ```lean
  def chaskiEnqueueAll (q : ChaskiQueue) (xs : List Nat) : ChaskiQueue := q ++ xs
  ```

- `Puriq.Formula.Proved.chaskiDrain` · def · `Lutar/Puriq/Formulas/ProvedFormulas.lean:198-200` · definition (no axiom check)

  ```lean
  def chaskiDrain : ChaskiQueue → List Nat | [] => [] | m :: ms => m :: chaskiDrain ms
  ```

**What the Lean states.** In an in-memory list model, chaskiEnqueueAll q xs := q ++ xs and chaskiDrain is provably the identity on lists (f7_chaski_drain_eq, by structural induction). The main theorem states chaskiDrain (chaskiEnqueueAll [] msgs) = msgs; the positional form states the same with [i]? indexing.

**Manuscript anchors** (verbatim):

- Abstract, L21: `**F7** (the Chaski channel delivers in FIFO order — reception order equals send order, positionally)`
- §2, L98: `` replaced two previously-*vacuous* statements (F4 repackaged its hypothesis; F7 was `msgs = msgs`) with genuine, non-vacuous proofs ``
- §7.3, L296: `` previously the vacuous `msgs = msgs`, now a genuine positional-ordering theorem ``
- §8.3, L335: `retired the previously vacuous F4 and F7 and replaced them with genuine theorems`
- A.2, L451: `genuine FIFO ordering, no longer msgs = msgs`

**Manuscript claim.** The Chaski channel delivers in FIFO order, with reception order equal to send order positionally (Abstract); the 2026-06-10 statement is a genuine, non-vacuous positional-ordering theorem that replaced the vacuous msgs = msgs (§2 rule 3, §7.3, §8.3, A.2).

**Gap.** chaskiDrain is provably the identity and chaskiEnqueueAll [] is the identity, so the main statement reduces to msgs = msgs after two rewrites; its proof is exactly rw [f7_chaski_enqueueAll_nil, f7_chaski_drain_eq]. The model has no interleaving of sends and receives and no concurrency, retries, deduplication or persistence. The manuscript's 'non-vacuous' framing is therefore stronger than the statement supports. claims JSON F7 refinement_gap already says drain is 'definitionally the list itself'; strictly it is provably (by induction), not definitionally, the identity.

**Proposed wording** (for the owner; not applied):

> F7 [locked]: in the in-memory list model, draining the queue obtained by appending msgs to the empty queue returns msgs, and the i-th elements agree. Because drain is provably the identity on lists, this records that the model's definitions compose as intended; FIFO under interleaving, retries, deduplication, persistence or recovery is not established.

**Owner decisions:** D1, D6, D7 · **Runtime symbol named in claims JSON** (not inspected here; R01 scope): `tools.locked_formula_runtime.chaski_fifo_drain`

**Cross-references** (lutar-lean already narrowed its own wording):

- `claims/locked-formulas.v1.json:115` @ `04f904ec`: `drain is definitionally the list itself.`

### P-F11 · EXCEEDS · F11 Ayni reciprocity

Verdict **EXCEEDS** · severity minor · locked id F11

**Lean declarations** (lutar-lean `04f904ec`):

- `Puriq.Formula.Proved.f11_ayni_reciprocity_conservation` (primary) · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:62-64` · kernel axioms: `propext`

  ```lean
  theorem f11_ayni_reciprocity_conservation (b c : Int) : (b + c) - c = b := by simp [Int.add_sub_cancel]
  ```

**What the Lean states.** Integer add-then-subtract cancellation, (b + c) − c = b.

**Manuscript anchors** (verbatim):

- §7.3, L297: `trust-ledger reciprocity-balance invariant`

**Manuscript claim.** F11 is a trust-ledger reciprocity-balance invariant.

**Gap.** An integer identity is not an invariant of any ledger, event log or fold. The Lean docstring at ProvedFormulas.lean:60-61 ('fold-replay of an append-only event log conserves balance') has the same reach; it sits in the locked file and is out of scope here (P-X5).

**Proposed wording** (for the owner; not applied):

> F11 [locked]: the integer identity (b + c) − c = b. It does not establish conservation of a deployed trust ledger or event log.

**Owner decisions:** D1 · **Runtime symbol named in claims JSON** (not inspected here; R01 scope): none

**Cross-references** (lutar-lean already narrowed its own wording):

- `claims/locked-formulas.v1.json:139` @ `04f904ec`: `Locked F11 is the integer identity (b + c) - c = b.`

### P-F12 · MARGINAL · F12 Kuramoto additive fragment

Verdict **MARGINAL** · severity minor · locked id F12

**Lean declarations** (lutar-lean `04f904ec`):

- `Puriq.Formula.Proved.f12_kuramoto_additive` (primary) · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:67-69` · kernel axioms: none

  ```lean
  theorem f12_kuramoto_additive (p1 p2 k : Nat) : k * (p1 + p2) = k * p1 + k * p2 := Nat.left_distrib k p1 p2
  ```

**What the Lean states.** Left distributivity on natural numbers, k·(p1 + p2) = k·p1 + k·p2.

**Manuscript anchors** (verbatim):

- §7.3, L298: `additive coupling *scaffolding only*, not the synchronization theorem`

**Manuscript claim.** F12 is additive coupling scaffolding only, not the Kuramoto synchronization theorem.

**Gap.** The disclaimer is present. Only the word 'coupling' remains attached to Nat left distributivity; no oscillator, phase or coupling term appears in the statement.

**Proposed wording** (for the owner; not applied):

> F12 [locked]: left distributivity on natural numbers, k·(p1+p2) = k·p1 + k·p2. No Kuramoto coupling, dynamics or synchronization result is claimed.

**Owner decisions:** D1 · **Runtime symbol named in claims JSON** (not inspected here; R01 scope): none

**Cross-references** (lutar-lean already narrowed its own wording):

- `claims/locked-formulas.v1.json:156` @ `04f904ec`: `Locked F12 is Nat left distributivity, an additive fragment only.`

### P-F18 · EXCEEDS · F18 Reed–Solomon RS(10,6) shard arithmetic

Verdict **EXCEEDS** · severity major · locked id F18

**Lean declarations** (lutar-lean `04f904ec`):

- `Puriq.Formula.Proved.f18_reed_solomon_parity_count` (primary) · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:72` · kernel axioms: none

  ```lean
  theorem f18_reed_solomon_parity_count : (10 - 6 : Nat) = 4 := by decide
  ```

- `Puriq.Formula.Proved.f18_erasure_tolerance` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:75` · kernel axioms: `Quot.sound`, `propext`

  ```lean
  theorem f18_erasure_tolerance (e : Nat) (h : e ≤ 4) : 6 ≤ 10 - e := by omega
  ```

**What the Lean states.** Shard-count arithmetic for RS(10,6): (10 − 6 : Nat) = 4, and e ≤ 4 implies 6 ≤ 10 − e.

**Manuscript anchors** (verbatim):

- §7.3, L299: `` Reed–Solomon encode/decode correctness (`f18_reed_solomon_parity_count`; P2 receipt coding) ``
- §6.1, L257: `The encoding/decoding correctness used by the receipt layer.`
- Abstract, L21: `with **F18** (Reed–Solomon coding) governing erasure tolerance — all four kernel-verified`
- §8.1, L316: `F18 RS coding; receipt binding; DSSE/cosign SLSA L1+L2`

**Manuscript claim.** F18 is Reed–Solomon encode/decode correctness used by the receipt layer and governs erasure tolerance as one of four locked receipt-layer facts.

**Gap.** The locked statements are natural-number arithmetic. No encoder, decoder, field, polynomial, MDS property or erasure-recovery statement is in the locked set. The experimental rs_distance_lower_bound (Wave14/ReedSolomonDistance.lean:103) is outside the locked eight, and the manuscript itself records (L257) that the full MDS equality is still a tracked sorry. lutar-lean narrowed its own wording in 3b0b589 (claims JSON F18 refinement_gap and public_wording; PROVEN_FORMULAS.md:28).

**Proposed wording** (for the owner; not applied):

> F18 [locked]: shard-count arithmetic for RS(10,6): 10 − 6 = 4, and if e ≤ 4 shards are erased, 6 ≤ 10 − e remain. No encoder, decoder, MDS property or erasure-recovery correctness is established in the locked set.

**Owner decisions:** D1, D7 · **Runtime symbol named in claims JSON** (not inspected here; R01 scope): `tools.locked_formula_runtime.rs10_6_parity`

**Cross-references** (lutar-lean already narrowed its own wording):

- `claims/locked-formulas.v1.json:169` @ `04f904ec`: `Parity-count arithmetic. Not an encoder, decoder, MDS proof, or erasure-recovery implementation.`
- `PROVEN_FORMULAS.md:28` @ `04f904ec`: `Parity-count arithmetic only — **not** an encoder, decoder, or erasure-recovery implementation.`
- `Lutar/Wave14/ReedSolomonDistance.lean:103` @ `04f904ec`: `theorem rs_distance_lower_bound`

### P-F19 · MARGINAL · F19 Bekenstein additive scaffolding

Verdict **MARGINAL** · severity minor · locked id F19

**Lean declarations** (lutar-lean `04f904ec`):

- `Puriq.Formula.Proved.f19_bekenstein_additive` (primary) · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:78-79` · kernel axioms: none

  ```lean
  theorem f19_bekenstein_additive (s1 s2 : Nat) : s1 ≤ s1 + s2 := Nat.le_add_right s1 s2
  ```

- `Puriq.Formula.Proved.f19_budget_monotone` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:82` · kernel axioms: none

  ```lean
  theorem f19_budget_monotone (s d : Nat) : s ≤ s + d := Nat.le_add_right s d
  ```

**What the Lean states.** Add-right monotonicity on natural numbers, s1 ≤ s1 + s2 (and s ≤ s + d).

**Manuscript anchors** (verbatim):

- §7.3, L300: `additive bookkeeping *scaffolding only*, **NOT** the Bekenstein bound`

**Manuscript claim.** F19 is additive bookkeeping scaffolding only, not the Bekenstein bound.

**Gap.** The physical bound is disclaimed. 'Additive' mislabels a monotonicity statement: s1 ≤ s1 + s2 does not express that budgets add. The docstring at ProvedFormulas.lean:77 ('Disjoint-region budgets add') has the same reach; it is in the locked file (P-X5).

**Proposed wording** (for the owner; not applied):

> F19 [locked]: s1 ≤ s1 + s2 on natural numbers (add-right monotonicity). It is neither additivity of entropy budgets nor the Bekenstein bound.

**Owner decisions:** D1 · **Runtime symbol named in claims JSON** (not inspected here; R01 scope): none

**Cross-references** (lutar-lean already narrowed its own wording):

- `claims/locked-formulas.v1.json:194` @ `04f904ec`: `Locked F19 is Nat add-right monotonicity, an additive fragment only.`

### P-F22 · PARTIAL · F22 Khipu emit sequence monotonicity

Verdict **PARTIAL** · severity moderate · locked id F22

**Lean declarations** (lutar-lean `04f904ec`):

- `Puriq.Formula.Proved.f22_khipu_emit_monotone` (primary) · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:254-256` · kernel axioms: `Quot.sound`, `propext`

  ```lean
  theorem f22_khipu_emit_monotone (n i j : Nat) (hij : i < j) (hj : j < n) : (f22_seqLog n)[i]'(by simp [f22_seqLog]; omega) < (f22_seqLog n)[j]'(by simp [f22_seqLog]; exact hj) := by
  ```

- `Puriq.Formula.Proved.f22_emit_appends_length` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:246-247` · kernel axioms: `propext`

  ```lean
  theorem f22_emit_appends_length (n : Nat) : f22_seqLog (n + 1) = f22_seqLog n ++ [n] := by
  ```

- `Puriq.Formula.Proved.f22_emit_strictly_greater` · theorem · `Lutar/Puriq/Formulas/ProvedFormulas.lean:250` · kernel axioms: `Quot.sound`, `propext`

  ```lean
  theorem f22_emit_strictly_greater (n s : Nat) (h : s ∈ f22_seqLog n) : s < n := by
  ```

- `Puriq.Formula.Proved.f22_seqLog` · def · `Lutar/Puriq/Formulas/ProvedFormulas.lean:244` · definition (no axiom check)

  ```lean
  def f22_seqLog (n : Nat) : List Nat := List.range n
  ```

**What the Lean states.** For f22_seqLog n := List.range n: f22_seqLog (n+1) = f22_seqLog n ++ [n]; every member is below n; and for i < j < n the i-th entry is strictly below the j-th.

**Manuscript anchors** (verbatim):

- Abstract, L21: `**F22** (the emit log is append-only and strictly monotone in sequence number)`
- §7.3, L301: `` `seqLog n = List.range n`, each emit appends and the sequence length is monotone non-decreasing ``
- §7.3, L301: `*Newly proven 2026-06-10.*`
- A.2, L452: `#print axioms Lutar.f22_khipu_emit_monotone`

**Manuscript claim.** The emit log is append-only and strictly monotone in sequence number (Abstract); seqLog n = List.range n, each emit appends and the sequence length is monotone non-decreasing, newly proven 2026-06-10 (§7.3).

**Gap.** The statements concern List.range, not a deployed emit path, clock or database sequence. 'Sequence length is monotone non-decreasing' is not one of the three stated theorems; strict increase by position is (f22_khipu_emit_monotone). The manuscript writes seqLog; the Lean name is f22_seqLog. Date: the F22 declarations first appear in e6de491 (2026-06-04) and are unchanged by 5cfaf9a (2026-06-10, which moved the locked count to eight), so 'locked 2026-06-10, proved 2026-06-04' is the more precise reading of 'Newly proven 2026-06-10'.

**Proposed wording** (for the owner; not applied):

> F22 [locked]: for f22_seqLog n := List.range n, f22_seqLog (n+1) = f22_seqLog n ++ [n], every member is below n, and entries strictly increase with position. Monotonicity of a deployed emit path, clock or database sequence is not established.

**Owner decisions:** D1, D7 · **Runtime symbol named in claims JSON** (not inspected here; R01 scope): `tools.locked_formula_runtime.seq_log_range`

**Cross-references** (lutar-lean already narrowed its own wording):

- `claims/locked-formulas.v1.json:208` @ `04f904ec`: `Proves monotonicity of List.range indices. Does not prove monotonicity of a deployed emit path.`

## Cross-cutting rows

### P-X1 · EXCEEDS · Locked-count theorem, the c7c0ba17 pin and A.2 identifiers

Verdict **EXCEEDS** · severity major · surface: manuscript

**Finding.** (a) locked_count_eight states that a hand-written list literal has length 8 (Wave8/AxiomDisclosure.lean:77-94); four more copies state the same over lockedNames (Wave9:81, Wave10:90, Wave11:100, Uniqueness/AxiomCheck.lean:96). None of them states that eight theorems exist or are kernel-checked. What binds the 24 carriers is the CI step at lake-build.yml:240-260, which requires EXPECTED=24 allowed:true lines from tools/lean/LockedGuard.lean. (b) c7c0ba17 (2026-05-31) lists 135 paths and neither Lutar/Puriq/Formulas/ProvedFormulas.lean nor Lutar/Wave8/AxiomDisclosure.lean, so the A.2 command at c7c0ba17 cannot reproduce the locked eight. ProvedFormulas.lean first appears in e6de491 (2026-06-04) and the current F4/F7 statements in 5cfaf9a (2026-06-10); ProvedFormulas.lean:6-7 itself says it is not folded into the v11 count. PAPERS_INDEX.md:79 already separates proof snapshot 5cfaf9a3 from count baseline c7c0ba17. (c) The A.2 names Lutar.lockedDisclosed, Lutar.locked_count_eight and Lutar.f4_/f7_/f22_* do not resolve at the pin; the declarations are Lutar.Wave8.AxiomDisclosure.* and Puriq.Formula.Proved.*.

**Manuscript anchors** (verbatim):

- Front matter, L13: `` the count itself is now a theorem (`locked_count_eight`, by `decide`) ``
- Front matter, L13: `` Pinned commits: locked kernel @ `c7c0ba17` ``
- §2, L98: `` the locked count is kernel-certified (`locked_count_eight`, by `decide`) ``
- §7.3, L292: `` machine-confirmed by `locked_count_eight : lockedDisclosed.length = 8 := by decide` ``
- A.1, L432: `` locks {F1,F4,F7,F11,F12,F18,F19,F22} (`locked_count_eight`) ``
- A.2, L443: `git checkout c7c0ba17 && lake build`
- A.2, L446: `#eval Lutar.lockedDisclosed.length`
- A.2, L447: `#check (Lutar.locked_count_eight : Lutar.lockedDisclosed.length = 8)`

**Evidence:**

- lutar-lean `Lutar/Wave8/AxiomDisclosure.lean:94` @ `04f904ec`: `theorem locked_count_eight : lockedDisclosed.length = 8 := by decide`
- lutar-lean `Lutar/Wave8/AxiomDisclosure.lean:77` @ `04f904ec`: `def lockedDisclosed : List (String × List String) :=`
- lutar-lean `Lutar/Uniqueness/AxiomCheck.lean:96` @ `04f904ec`: `theorem locked_count_eight : lockedNames.length = 8 := by decide`
- lutar-lean `Lutar/Wave9/AxiomDisclosure.lean:81` @ `04f904ec`: `theorem locked_count_eight : lockedNames.length = 8 := by decide`
- lutar-lean `Lutar/Wave10/AxiomDisclosure.lean:90` @ `04f904ec`: `theorem locked_count_eight : lockedNames.length = 8 := by decide`
- lutar-lean `Lutar/Wave11/AxiomDisclosure.lean:100` @ `04f904ec`: `theorem locked_count_eight : lockedNames.length = 8 := by decide`
- lutar-lean `.github/workflows/lake-build.yml:250` @ `04f904ec`: `EXPECTED=24`
- lutar-lean `.github/workflows/lake-build.yml:240` @ `04f904ec`: `- name: Locked-8 axiom guard (kernel-emitted, fail-closed)`
- lutar-lean `Lutar/Puriq/Formulas/ProvedFormulas.lean:6-7` @ `04f904ec`: `(this file is staged in the PURIQ experimental scope and is NOT folded into the v11 count).`
- lutar-lean `Lutar/Puriq/Formulas/ProvedFormulas.lean:48` @ `04f904ec`: `namespace Puriq.Formula.Proved`
- lutar-lean `Lutar/Wave8/AxiomDisclosure.lean:46` @ `04f904ec`: `namespace Lutar.Wave8.AxiomDisclosure`
- lutar-lean @ `c7c0ba17`: git ls-tree -r c7c0ba17 lists 135 paths, none of them ProvedFormulas.lean or Wave8/AxiomDisclosure.lean (read 2026-10-06).
- szl-papers `PAPERS_INDEX.md:79` @ `5f2f75f1`: `` at proof snapshot `5cfaf9a3b55fd75e8a2a1197502a93dd8ca68be3` ``
- szl-papers `PAPERS_INDEX.md:79` @ `5f2f75f1`: `` the distinct frozen Doctrine-v11 canonical-count baseline is `c7c0ba17` (749/14/163) ``

**Proposed wording** (for the owner; not applied):

> The locked set is the 24 carrier theorems in Lutar/Puriq/Formulas/ProvedFormulas.lean. CI's Locked-8 guard step emits kernel axiom sets for all 24 and fails unless each lies inside {propext, Classical.choice, Quot.sound}; locked_count_eight records the length of the disclosed list. Proof snapshot: 5cfaf9a3 (compiled surface on current main). Doctrine-v11 count baseline: c7c0ba17 (749/14/163), which predates the carrier declarations. Reproduce with Puriq.Formula.Proved.* and Lutar.Wave8.AxiomDisclosure.locked_count_eight.

**Owner decisions:** D1, D4, D7

### P-X2 · PARTIAL · Axiom ledger compared with kernel-emitted axiom sets

Verdict **PARTIAL** · severity moderate · surface: manuscript

**Finding.** The manuscript defines the locked tier over {propext, funext, Classical.choice, Quot.sound} (L86, L303) and gives F4 that set (A.2 L450). The bare-core LockedGuard replica (MEASURED; Lean 4.18.0, Windows, not CI) reports all 24 carriers inside {propext, Classical.choice, Quot.sound}: 11 with no axiom, 10 with [propext], 3 with [Quot.sound, propext]; none uses Classical.choice, and F4's main theorem is [propext]. funext is a theorem in Lean 4 core: #print axioms funext reports [Quot.sound] on the same toolchain (MEASURED). The Wave8 lockedDisclosed lists (AxiomDisclosure.lean:77-85) are hand-written and include funext and Classical.choice; claims JSON line 18 already marks them as not collectAxioms ground truth. A.3 (L472) lists the core axioms correctly. L259 names no declaration; if it means the F22 carriers, two of the three report [Quot.sound, propext], so which declarations L259 covers is UNKNOWN.

**Manuscript anchors** (verbatim):

- §2, L86: `` {`propext`, `funext`, `Classical.choice`, `Quot.sound`} ``
- §7.3, L303: `` the `{propext, funext, Classical.choice, Quot.sound}` axiom basis in lockstep ``
- A.2, L450: `{propext, funext, Classical.choice, Quot.sound}`
- §6.1, L259: `` (`#print axioms = {propext}` over the log) ``
- A.3, L472: `` core axioms {`propext`, `Classical.choice`, `Quot.sound`} ``

**Evidence:**

- lutar-lean `tools/lean/LockedGuard.lean:28` @ `04f904ec`: ``` def allowedAxioms : List Name := [``propext, ``Classical.choice, ``Quot.sound] ```
- lutar-lean `Lutar/Wave8/AxiomDisclosure.lean:50-51` @ `04f904ec`: `def leanKernelAxioms : List String := ["propext", "funext", "Classical.choice", "Quot.sound"]`
- lutar-lean `Lutar/Wave8/AxiomDisclosure.lean:79` @ `04f904ec`: `("F4", ["propext", "funext", "Classical.choice", "Quot.sound"]),`
- lutar-lean `claims/locked-formulas.v1.json:18` @ `04f904ec`: `"wave8_lockedDisclosed": "Hand-written axiom-name lists; not collectAxioms ground truth."`

**Proposed wording** (for the owner; not applied):

> Locked-tier trust base: {propext, Classical.choice, Quot.sound} (tools/lean/LockedGuard.lean:28). Kernel-emitted sets for the 24 carriers at lutar-lean 04f904e: 11 use no axiom, 10 use propext only, 3 use propext and Quot.sound; none uses Classical.choice. funext is a Lean 4 theorem (from Quot.sound), not an axiom. F4's main theorem (Puriq.Formula.Proved.f4_khipu_dag_acyclic_preserved) depends on propext only.

**Owner decisions:** D1, D7, D8

### P-X3 · PARTIAL · Conjecture 1 and the Λ boundary wording

Verdict **PARTIAL** · severity moderate · surface: manuscript

**Finding.** The manuscript calls Conjecture 1 machine-checked FALSE (L21, L96, L156, L486, L501) and says the separation at (4,1) is by decide (L162). At the pin, maxAgg_A2, maxAgg_A3, maxAgg_A5 and maxAgg_ne_Lambda are mechanized (Round13/Lambda_Uniqueness.lean:154-212), and maxAgg_ne_Lambda closes with simp and norm_num, not decide. The A1 and A4 membership of maxAgg is argued in a docstring (:145-146) that points to a SORRY_AUDIT document not present at the pin. A text search of the pinned tree found no declaration stating LutarAxioms maxAgg or the negation of Conjecture1_LambdaUnique, which Identifiability.lean:159-161 ships as a statement only. The 'minimum aggregator' witness (L160) has no declaration against LutarAxioms; the nearest minAgg (Wave6/SetAlphaUniqueness.lean:684, on Fin 2 → ℝ) is used to show that it fails A5′ multiplicativity. Three different axiom lists carry the A1–A4 or A1–A5 labels: manuscript A4 is min ≤ Φ ≤ max (L151), Lean IsBounded is the upper bound only (Axioms.lean:111-113), and bounty/README.md:28-31 uses idempotence, monotonicity, symmetry and zero-absorption, under which maxAgg is not a witness (zero-absorption fails). The szl-papers boundary text (bounty/README.md:9, PAPERS_INDEX.md:79, ARXIV_SUBMISSION_GUIDE.md:83) says disproved as stated, with the weaker-condition question open. The kernel axiom sets of the Λ declarations were not re-measured here (NOT_RUN; they need Mathlib).

**Manuscript anchors** (verbatim):

- Abstract, L21: `is **Conjecture 1 — machine-checked FALSE**`
- §2, L96: `machine-checked **FALSE** under A1–A5`
- §4.1, L151: `` `min_i x_i ≤ Φ(x) ≤ max_i x_i` ``
- §4.2, L156: `Conjecture 1 is machine-checked FALSE`
- §4.2, L160: `` There exists `Φ ≠ Λ_k` satisfying A1–A5. ``
- §4.2, L160: `The minimum aggregator is a second witness.`
- §4.2, L162: `` separation at `(4,1)` by `decide` ``
- Appendix B, L486: `unconditional Λ uniqueness — machine-checked FALSE; never a theorem`
- Doctrine footer, L501: `Λ = **Conjecture 1** (machine-checked FALSE; never a theorem)`

**Evidence:**

- lutar-lean `Lutar/Round13/Lambda_Uniqueness.lean:145-146` @ `04f904ec`: `` (A1/A4 hold by `sup'` monotonicity and `A4 = ≤ max` reflexivity — see SORRY_AUDIT §4) ``
- lutar-lean `Lutar/Round13/Lambda_Uniqueness.lean:154` @ `04f904ec`: `theorem maxAgg_A5 : IsPermutationInvariant maxAgg := by`
- lutar-lean `Lutar/Round13/Lambda_Uniqueness.lean:174` @ `04f904ec`: `theorem maxAgg_A3 : ∀ c : NNReal, maxAgg (fun _ => c) = c := by`
- lutar-lean `Lutar/Round13/Lambda_Uniqueness.lean:179-180` @ `04f904ec`: `theorem maxAgg_A2 : ∀ (c : NNReal) (x : Axes 2), maxAgg (fun i => c * x i) = c * maxAgg x := by`
- lutar-lean `Lutar/Round13/Lambda_Uniqueness.lean:188` @ `04f904ec`: `theorem maxAgg_ne_Lambda : maxAgg ≠ Λ 2 := by`
- lutar-lean `Lutar/Round13/Lambda_Uniqueness.lean:212` @ `04f904ec`: `exact absurd hx (by norm_num)`
- lutar-lean `Lutar/Uniqueness/Identifiability.lean:159-161` @ `04f904ec`: `def Conjecture1_LambdaUnique : Prop := ∀ {k : ℕ} (_hk : 0 < k) (Φ Ψ : Aggregator k), LutarAxioms Φ → LutarAxioms Ψ → Φ = Ψ`
- lutar-lean `Lutar/Axioms.lean:111-113` @ `04f904ec`: `def IsBounded {k : ℕ} (hk : 0 < k) (Λ : Aggregator k) : Prop := ∀ x : Axes k, Λ x ≤ Finset.univ.sup' ⟨⟨0, hk⟩, Finset.mem_univ _⟩ x`
- lutar-lean `Lutar/Round13/LambdaSeparable.lean:93-100` @ `04f904ec`: `theorem lambda_unique_of_separable {k : ℕ} (hk : 0 < k) (Φ : Aggregator k) (hL : LutarAxioms Φ) (f : Fin k → (NNReal → NNReal)) (hsep : ∀ x, Φ x = ∏ i, f i (x i)) (hmul : ∀ i s t, f i (s * t) = f i s * f i t) (hone : ∀ i, f i 1 = 1) (hmono : ∀ i, Monotone (f i)) : Φ = Λ k := by`
- lutar-lean `Lutar/Wave6/SetAlphaUniqueness.lean:684` @ `04f904ec`: `noncomputable def minAgg (x : Fin 2 → ℝ) : ℝ := x 0 ⊓ x 1`
- lutar-lean `Lutar/Wave6/SetAlphaUniqueness.lean:686-687` @ `04f904ec`: `theorem minAgg_not_A5prime : ¬ A5_Multiplicativity (n := 2) minAgg := by`
- lutar-lean `claims/locked-formulas.v1.json:31` @ `04f904ec`: `"status": "CONJECTURE_1_OPEN_FALSE_AS_STATED",`
- szl-papers `bounty/README.md:9` @ `5f2f75f1`: `**Conjecture 1 is disproved as stated.** Conditional Theorem U is proven on its declared hypotheses; the weaker-condition uniqueness question remains open.`
- szl-papers `bounty/README.md:31` @ `5f2f75f1`: `**A4** | Zero-absorption`
- szl-papers `PAPERS_INDEX.md:79` @ `5f2f75f1`: `Λ **Conjecture 1 is disproved as stated**; conditional **Theorem U** is axiom-free, and only the weaker-condition question remains open.`
- szl-papers `ARXIV_SUBMISSION_GUIDE.md:83` @ `5f2f75f1`: `**Conjecture 1 is disproved as stated**; conditional **Theorem U** is proven and only the weaker-condition uniqueness question remains open.`

**Proposed wording** (for the owner; not applied):

> Conjecture 1 (unconditional uniqueness under A1–A5) is disproved as stated; the weaker-condition uniqueness question remains open. maxAgg is machine-checked to satisfy A2, A3 and A5 (maxAgg_A2/A3/A5) and to differ from Λ₂ at (4,1) (maxAgg_ne_Lambda); its A1 and A4 membership is argued in prose. Conditional uniqueness (Theorem U, lambda_unique_of_separable) is reported in the experimental tier, outside the locked eight.

**Owner decisions:** D1, D3, D7

### P-X4 · EXCEEDS · szl-forge TH10 index entry

Verdict **EXCEEDS** · severity moderate · surface: szl-forge spaces/szl-forge-lab/thesis_formula_index.json

**Finding.** thesis_formula_index.json:113-126 at szl-forge bd0419b (unchanged at db0c709) lists TH10 with lean_theorem Lutar.uniqueness and status GREEN, and describes it as uniqueness under A1–A4 via Cauchy 1821 and Aczél 1966. No declaration named Lutar.uniqueness exists at the lutar-lean pin. The nearest, Lutar.lutar_unique (Uniqueness.lean:218-224), rests on lutar_is_geomean, which ends in sorry (:215) next to an in-file note that the statement is false under A1–A5. The index meta block (:5-12) pins lutar-lean c4d13795 (2026-05-29) and calls itself STAGED-ADVISORY; 73 of its 80 entries are GREEN and were not re-read here. run_manifest.json:31-37 records a sha256 for the file, and a merge under spaces/szl-forge-lab/** triggers publish-forge-lab.yml. Whether a forge test re-hashes the index against the manifest was not established here (UNKNOWN).

**Evidence:**

- szl-forge `spaces/szl-forge-lab/thesis_formula_index.json:119` @ `bd0419b6`: `"lean_theorem": "Lutar.uniqueness",`
- szl-forge `spaces/szl-forge-lab/thesis_formula_index.json:121` @ `bd0419b6`: `"status": "GREEN",`
- szl-forge `spaces/szl-forge-lab/thesis_formula_index.json:12` @ `bd0419b6`: `STAGED-ADVISORY`
- szl-forge `spaces/szl-forge-lab/run_manifest.json:32` @ `bd0419b6`: `"path": "thesis_formula_index.json",`
- lutar-lean `Lutar/Uniqueness.lean:215` @ `04f904ec`: `sorry`
- lutar-lean `Lutar/Uniqueness.lean:218-222` @ `04f904ec`: `theorem lutar_unique {k : Nat} (hk : 0 < k) (Lambda_fn Lambda_fn' : Aggregator k) (hL : LutarAxioms Lambda_fn) (hL' : LutarAxioms Lambda_fn') : Lambda_fn = Lambda_fn' :=`

**Proposed wording** (for the owner; not applied):

> TH10 should not read GREEN while lean_theorem Lutar.uniqueness does not exist and the nearest declaration rests on a sorry over a statement documented as false. A status such as TRACKED or REFUTED_AS_STATED, pointing to maxAgg_ne_Lambda and Theorem U, would match the pinned source. This needs its own szl-forge PR (regenerate the run_manifest sha256; merging publishes the HF Space).

**Owner decisions:** D5

### P-X5 · inventory · Affected surfaces outside the v26 manuscript

Verdict **inventory (no verdict)** · severity - · surface: inventory

**Finding.** The same wording appears in the arXiv packages: append-only-governance (P1, submission pending) main.tex:34, :66, :135, :627; gpd-v26 main.tex:31, :236, :621, :625; gpd-unified-v26 main.tex:69, :222, :471. In lutar-lean: the ProvedFormulas.lean docstrings for F11 (:60-61) and F19 (:77), and PROVEN_FORMULAS.md:81. Dangling references: team/LEAN_AUDIT_F4F7F22.md (ProvedFormulas.lean:30), team/LEAN_F4F7_PROOFS_REPORT.md (Wave8/AxiomDisclosure.lean:29; PROVEN_FORMULAS.md:10) and team/lambda-closure/SORRY_AUDIT.md (Round13/Lambda_Uniqueness.lean:24). None of these paths exists at the pin, and team/ holds only PROVE_WAVE3_REPORT.md, so the manuscript's 2026-06-10 non-vacuity audit (L335) has no document at the pin to cite. This review edits none of these files.

**Manuscript anchors** (verbatim):

- §8.3, L335: `The non-vacuity audit of 2026-06-10`

**Evidence:**

- szl-papers `thesis/arxiv/append-only-governance/main.tex:34` @ `5f2f75f1`: `texttt{funext}`
- szl-papers `thesis/arxiv/append-only-governance/main.tex:66` @ `5f2f75f1`: `kernel-verified and non-vacuous as of 2026-06-10`
- szl-papers `thesis/arxiv/append-only-governance/main.tex:135` @ `5f2f75f1`: `(iii) a kernel-certified`
- szl-papers `thesis/arxiv/append-only-governance/main.tex:627` @ `5f2f75f1`: `["propext","funext","Classical.choice","Quot.sound"]`
- szl-papers `thesis/arxiv/gpd-v26/main.tex:31` @ `5f2f75f1`: `texttt{funext}`
- szl-papers `thesis/arxiv/gpd-v26/main.tex:236` @ `5f2f75f1`: `the count is kernel-certified`
- szl-papers `thesis/arxiv/gpd-v26/main.tex:621` @ `5f2f75f1`: `#eval Lutar.lockedDisclosed.length`
- szl-papers `thesis/arxiv/gpd-v26/main.tex:625` @ `5f2f75f1`: `#print axioms Lutar.f4_khipu_dag_acyclic_preserved`
- szl-papers `thesis/arxiv/gpd-unified-v26/main.tex:69` @ `5f2f75f1`: `texttt{funext}`
- szl-papers `thesis/arxiv/gpd-unified-v26/main.tex:222` @ `5f2f75f1`: `kernel-certified theorem`
- szl-papers `thesis/arxiv/gpd-unified-v26/main.tex:471` @ `5f2f75f1`: `Lutar.lockedDisclosed.length = 8 := by decide`
- lutar-lean `Lutar/Puriq/Formulas/ProvedFormulas.lean:60-61` @ `04f904ec`: `fold-replay of an append-only event log conserves balance.`
- lutar-lean `Lutar/Puriq/Formulas/ProvedFormulas.lean:77` @ `04f904ec`: `Disjoint-region budgets add.`
- lutar-lean `PROVEN_FORMULAS.md:81` @ `04f904ec`: `the locked set cannot silently grow`
- lutar-lean `Lutar/Puriq/Formulas/ProvedFormulas.lean:30` @ `04f904ec`: `` `team/LEAN_AUDIT_F4F7F22.md` ``
- lutar-lean `Lutar/Wave8/AxiomDisclosure.lean:29` @ `04f904ec`: `` See `team/LEAN_F4F7_PROOFS_REPORT.md`. ``
- lutar-lean `PROVEN_FORMULAS.md:10` @ `04f904ec`: `` see `team/LEAN_F4F7_PROOFS_REPORT.md` ``
- lutar-lean `Lutar/Round13/Lambda_Uniqueness.lean:24` @ `04f904ec`: `` `team/lambda-closure/SORRY_AUDIT.md` ``

**Proposed wording** (for the owner; not applied):

> List these surfaces in any correction plan. Edits to the arXiv packages and to lutar-lean are owner decisions (D7, D8).

**Owner decisions:** D7, D8

## Owner decisions

- **D1** (OPEN): How should v26 be corrected: edit in place, issue an erratum or v26.1, or keep v26 as history with only this review sidecar? The lineage heading at L47 calls prior thesis versions immutable; v26 is not Zenodo-deposited and PAPERS_INDEX.md:63 lists it as a P3 hold.
- **D2** (TAKEN): Should szl-papers gain a non-normative reviews/ directory? Taken for this change (2026-10-06 lane brief): create reviews/. CONTRIBUTING's directory table does not list it yet. Fallback if reversed: a sidecar next to the manuscript, thesis/ouroboros/papers/v26/REVIEW-claim-ledger.md.
- **D3** (OPEN): Should Conjecture 1 be described as machine-checked FALSE, or as disproved as stated with the separation mechanized and A1/A4 membership argued in prose? Should a lutar-lean work item add LutarAxioms maxAgg and the negation of Conjecture1_LambdaUnique?
- **D4** (OPEN): Pin semantics: should doctrine footers stop saying locked-8 @ c7c0ba17 and adopt the proof-snapshot (5cfaf9a3, or the compiled surface on main) versus count-baseline (c7c0ba17) split already used in PAPERS_INDEX.md:79?
- **D5** (OPEN): Should forge TH10 GREEN be corrected now (a szl-forge PR that regenerates the run_manifest sha256 and auto-publishes the HF Space), or only recorded here?
- **D6** (OPEN): F7: drop the genuine / non-vacuous framing (drain is provably the identity), or strengthen the Lean model with interleaved enqueue/dequeue traces?
- **D7** (OPEN): Should the arXiv tex packages, especially P1 append-only-governance (submission pending), be corrected before submission?
- **D8** (OPEN): Should the Wave8 hand-written lockedDisclosed lists and the funext trust-base wording in lutar-lean be aligned with kernel collectAxioms output? That is a protected lockstep change needing a signed-commit PR with lake build.
- **D9** (OPEN): Should scripts/check_review_ledger.py be wired into CI through claim-registry.yml? That workflow is a protected path.

## What this ledger does not claim

- It does not re-run the Lean kernel in CI. The axiom sets are one MEASURED bare-core replica on
  Windows; the Λ / Theorem U axiom sets were not re-measured (NOT_RUN, they need Mathlib).
- It does not decide whether the manuscript, the Lean code or the doctrine is right. Verdicts are
  review opinions; the proposed wording is a draft for the owner.
- It does not inspect `tools/locked_formula_runtime.py` or any deployed receipt path; runtime
  refinement is item R01 of the frontier work queue.
- It covers the eight locked ids and five cross-cutting rows only. The other 79 forge index entries,
  the experimental tier and szl-doctrine were not reviewed.
- `scripts/check_review_ledger.py` checks structure, pins and quotes. A passing run says the ledger
  still matches its pinned sources, nothing more.

## Reproduce

```bash
# From this repository
python3 scripts/check_review_ledger.py --self-test
python3 scripts/check_review_ledger.py
# Optional: compare every Lean quote with a lutar-lean checkout at 04f904ec
git -C <lutar-lean> checkout 04f904ecd5683753a481ab2b1ded69ac01a7a661
python3 scripts/check_review_ledger.py --lean-root <lutar-lean>
# Kernel axiom replica (bare core, no Mathlib), inside the lutar-lean checkout
lean -o _olean/Lutar/Puriq/Formulas/ProvedFormulas.olean Lutar/Puriq/Formulas/ProvedFormulas.lean
LEAN_PATH=_olean lean tools/lean/LockedGuard.lean 2>&1 | grep -c '"allowed":true'   # 24
```
