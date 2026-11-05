# Conjecture 2 — Khipu DAG Protocol Safety: Lean 4 Formalization Plan

**Epistemic status: [PROPOSED]** — this is a research plan, not a result. No
theorem below is machine-checked yet. Produced with AI assistance (Claude
Sonnet 4.5) against the canonical thesis v8 and the public prior art
(gdanezis/lean-dag; Pirlea et al., CCS 2024; Qiu, Xiao, Shao, IEEE S&P 2026),
and subject to the honesty doctrine: classical results are attributed, the
locked-8 kernel is never touched, and nothing here promotes any claim to
[VERIFIED] until `lake build` is green with no `sorry` and the result is
merged to `main` on `szl-holdings/lutar-lean`.

---

# Khipu DAG Protocol Safety: Lean 4 Formalization Plan

## 1. Model Choices

### 1.1 DAG Representation
**Choice:** Certified block DAG with explicit vote certificates.

```lean
-- Certified block model (vs lean-dag's uncertified variant)
structure CertifiedBlock (V : Type*) [DecidableEq V] where
  author    : V
  round     : ℕ
  payload   : Payload  -- application txns
  parents   : Finset (BlockRef V)
  qc        : QuorumCertificate V  -- NEW: explicit 2f+1 votes
```

**Justification vs lean-dag:**
- lean-dag uses `Block` without embedded certificates, relying on external validator state.
- Khipu embeds `QuorumCertificate` directly (matching Pirlea's Bythos), making certificate-chaining explicit and enabling inductive DAG-height proofs.
- Enables direct formalization of "certified round r means ≥2f+1 validators voted" as a structural invariant, not a protocol ghost variable.

### 1.2 Validator & Quorum Model
**Choice:** Fixed validator set with static Byzantine threshold.

```lean
structure ValidatorSet (V : Type*) [DecidableEq V] [Fintype V] where
  total     : ℕ
  byzantine : ℕ
  h_size    : Fintype.card V = total
  h_quorum  : total = 3 * byzantine + 1  -- exact (3f+1) sizing
  
def isQuorum (vs : ValidatorSet V) (Q : Finset V) : Prop :=
  Q.card ≥ 2 * vs.byzantine + 1
```

**Justification:**
- lean-dag uses `ValidatorQuorum` typeclass; we make the (3f+1) assumption *structural* via `h_quorum`.
- Enables *exact* quorum-intersection: any two quorums share ≥f+1 members (our Wave23 lemma).
- Static set simplifies initial proof; reconfiguration is [FUTURE WORK].

### 1.3 Adversary & Timing Model
**Choice:** Partial synchrony (GST + eventual message delivery) with computationally-bounded Byzantine adversary.

```lean
-- Network model
structure PartialSyncNetwork (V M : Type*) where
  gst       : ℕ  -- Global Stabilization Time
  Δ         : ℕ  -- post-GST message delay bound
  deliver   : ℕ → V → V → M → Prop
  h_eventual : ∀ r ≥ gst, ∀ v w m, 
    (send r v w m) → (∃ r' ≤ r + Δ, deliver r' v w m)

-- Adversary
structure ByzantineAdversary (V : Type*) (vs : ValidatorSet V) where
  corrupt   : Finset V
  h_bounded : corrupt.card ≤ vs.byzantine
  -- No double-signing within protocol (enforced by sig verification)
  h_no_equivocation : ∀ b₁ b₂ : CertifiedBlock V,
    b₁.author ∈ corrupt → b₂.author ∈ corrupt →
    b₁.round = b₂.round → b₁ = b₂  -- same-round uniqueness
```

**Justification vs lean-dag:**
- lean-dag uses `eventually ∀ v, hasDag v` (eventual synchrony) without explicit GST.
- We model GST explicitly to match Mysticeti/HotStuff partial-synchrony proofs (Alistair Stewart's approach).
- `h_no_equivocation` is weaker than full honesty but stronger than arbitrary Byzantine (matches Bythos "no double-vote" assumption).

---

## 2. Module Layout

```
Khipu/
├── DAG/
│   ├── Model.lean              -- CertifiedBlock, ValidatorSet, Network
│   ├── Quorum.lean             -- Quorum intersection (imports Wave23 lemma)
│   ├── Certificate.lean        -- QC validity, chaining rules
│   ├── DAG.lean                -- DAG well-formedness, causal history
│   ├── Commit.lean             -- Commit rule (3-chain / 2-chain variants)
│   ├── Safety.lean             -- Main safety theorem
│   └── Liveness.lean           -- Conditional liveness (GST-based)
├── Wave23/
│   └── QuorumIntersection.lean -- [VERIFIED] 2-quorum overlap ≥ f+1
└── Frozen/                      -- Untouched locked-8 theorems
    └── (F1, F4, F7, F11, F12, F18, F19, F22)
```

**Dependencies:**
- `DAG/Model.lean` depends only on Mathlib (Finset, Fintype).
- `DAG/Quorum.lean` imports `Wave23/QuorumIntersection.lean`.
- `DAG/Safety.lean` imports all DAG/* modules.
- No imports from `Frozen/` (the locked-8 are orthogonal: log invariants ≠ DAG consensus).

---

## 3. Theorem Statements (Pseudo-Lean)

### 3.1 Commit Safety

```lean
/-- No two honest validators commit conflicting blocks at the same round. -/
theorem khipu_commit_safety 
  (vs : ValidatorSet V) 
  (net : PartialSyncNetwork V Message)
  (adv : ByzantineAdversary V vs)
  (dag : GlobalDAG V)  -- union of all validators' local DAGs
  (h_dag_valid : ∀ v ∉ adv.corrupt, WellFormedDAG vs (dag.localView v))
  :
  ∀ v₁ v₂ ∉ adv.corrupt,
  ∀ b₁ b₂ : CertifiedBlock V,
  (Commits v₁ b₁ dag) →
  (Commits v₂ b₂ dag) →
  b₁.round = b₂.round →
  b₁ = b₂
  := by
  -- Proof strategy in §4.1
```

### 3.2 Conditional Liveness

```lean
/-- After GST + sufficient rounds, an honest proposal eventually commits. -/
theorem khipu_liveness_post_gst
  (vs : ValidatorSet V)
  (net : PartialSyncNetwork V Message)
  (adv : ByzantineAdversary V vs)
  (dag : GlobalDAG V)
  (h_gst_passed : ∀ v ∉ adv.corrupt, dag.currentRound v ≥ net.gst + 4)
  (h_sync : ∀ v w ∉ adv.corrupt, SynchronizedView vs net v w dag)
  (h_leader_honest : ∀ r ∈ [net.gst .. net.gst + 3], 
    LeaderOfRound vs r ∉ adv.corrupt)
  :
  ∃ b : CertifiedBlock V, ∃ v ∉ adv.corrupt,
    b.round ∈ [net.gst .. net.gst + 3] ∧
    Commits v b dag
  := by
  -- Proof strategy in §4.2
```

### 3.3 Supporting Definitions

```lean
/-- A validator commits block b if it observes a 3-chain ending at b. -/
def Commits (v : V) (b : CertifiedBlock V) (dag : GlobalDAG V) : Prop :=
  ∃ b₁ b₂ : CertifiedBlock V,
    b₂ ∈ dag.localView v ∧
    b₁ ∈ dag.localView v ∧
    b  ∈ dag.localView v ∧
    b₂.round = b.round + 2 ∧
    b₁.round = b.round + 1 ∧
    (BlockRef.mk b.author b.round) ∈ b₁.parents ∧
    (BlockRef.mk b₁.author b₁.round) ∈ b₂.parents ∧
    CertifiedChain dag [b, b₁, b₂]

/-- Two validators have synchronized DAG views. -/
def SynchronizedView (vs : ValidatorSet V) (net : PartialSyncNetwork V) 
  (v w : V) (dag : GlobalDAG V) : Prop :=
  ∀ b : CertifiedBlock V,
    b ∈ dag.localView v ↔ b ∈ dag.localView w
```

---

## 4. Proof Strategies

### 4.1 Safety Proof (khipu_commit_safety)

**Core argument:** Quorum intersection + certificate validity.

1. **Setup:** Assume v₁ commits b₁ and v₂ commits b₂ at round r, b₁ ≠ b₂.
2. **3-chain extraction:** By `Commits` definition, extract:
   - v₁ sees chain `[b₁, b₁', b₁'']` (rounds r, r+1, r+2).
   - v₂ sees chain `[b₂, b₂', b₂'']` (rounds r, r+1, r+2).
3. **Certificate quorums:**
   - b₁ has QC Q₁ with `Q₁.card ≥ 2f+1`.
   - b₂ has QC Q₂ with `Q₂.card ≥ 2f+1`.
4. **Quorum intersection (Wave23 lemma):**
   - `Q₁ ∩ Q₂`.card ≥ f+1.
   - At least one honest validator in `Q₁ ∩ Q₂` (since ≤f corrupt).
5. **No-equivocation:** Honest validator h ∈ Q₁ ∩ Q₂ voted for both b₁ and b₂ at round r.
   - By `h_no_equivocation`, h cannot sign two different blocks at round r.
   - Contradiction unless b₁ = b₂. ∎

**Key lemma dependencies:**
```lean
lemma quorum_intersection_has_honest
  (vs : ValidatorSet V) (adv : ByzantineAdversary V vs)
  (Q₁ Q₂ : Finset V)
  (h₁ : isQuorum vs Q₁) (h₂ : isQuorum vs Q₂)
  : ∃ v ∈ Q₁ ∩ Q₂, v ∉ adv.corrupt
  := by
  -- Apply Wave23 + pigeonhole on corrupt set
```

### 4.2 Liveness Proof (khipu_liveness_post_gst)

**Core argument:** Post-GST, honest leaders form certified chains.

1. **Round-by-round construction:**
   - At round `gst`, honest leader L₀ proposes b₀.
   - All honest validators receive b₀ within Δ (by `h_eventual`).
   - ≥2f+1 honest validators vote for b₀ → b₀ certified.
2. **Inductive chaining:**
   - Round `gst+1`: Leader L₁ sees b₀'s QC, includes b₀ as parent.
   - Round `gst+2`: Leader L₂ sees b₁'s QC (which references b₀).
   - Round `gst+3`: Leader L₃ sees b₂'s QC → 3-chain `[b₀, b₁, b₂]` formed.
3. **Commit trigger:** Any honest validator observing this 3-chain commits b₀ by `Commits` definition.

**Potential failure mode (§5):** If leaders are Byzantine-elected via rotating hash (not round-robin), malicious timing can skip honest leaders. Requires stronger leader-election assumption or randomness model.

**Key lemma:**
```lean
lemma post_gst_honest_proposal_certified
  (vs : ValidatorSet V) (net : PartialSyncNetwork V)
  (adv : ByzantineAdversary V vs)
  (r : ℕ) (h_post_gst : r ≥ net.gst)
  (L : V) (h_leader : LeaderOfRound vs r = L)
  (h_honest : L ∉ adv.corrupt)
  : ∃ qc : QuorumCertificate V, qc.round = r ∧ qc.block.author = L
  := by
  -- All honest validators vote within Δ, form 2f+1 quorum
```

---

## 5. Risks & Failure Modes

### 5.1 Liveness Gaps (Mysticeti Lesson)
**Risk:** Mysticeti's original paper claimed liveness from combinatorial lemmas alone, but Qiu et al. (IEEE S&P 2026 Rocq proof) found the commit rule required *4-chain* under asynchrony, not 3-chain.

**Our mitigation:**
- Explicitly model partial synchrony (GST, Δ) rather than pure eventual delivery.
- Prove liveness *conditionally* on GST + consecutive honest leaders (assumption `h_leader_honest`).
- Label liveness [CONJECTURE] until full mechanization, vs safety [PROPOSED → VERIFIED after waves].

### 5.2 Certificate Validity Bugs
**Risk:** QC verification might assume "≥2f+1 *distinct* signatures" but implementation allows replays.

**Mitigation:**
- Formalize `QuorumCertificate.valid` with explicit `Finset.card` on *unique* validator IDs.
- Add lemma: `qc.votes.card = qc.votes.image (·.validator) .card` (no duplicates).

### 5.3 Leader Election Modeling
**Risk:** If leader = `hash(round) mod n`, adversary controls network timing → can censor honest leaders before GST.

**Mitigation:**
- Assume deterministic round-robin post-GST (standard partial-sync assumption).
- Model pre-GST as arbitrary scheduling (no liveness claim).
- Future: add VRF-based leader election (requires cryptographic assumptions in Lean).

### 5.4 DAG Synchronization Assumption
**Risk:** `SynchronizedView` might be too strong (requires *identical* local DAGs).

**Observation:**
- lean-dag uses `eventually ∀ v, hasDag v` (weaker: eventually all see *some* DAG).
- We require identical views post-GST for 3-chain reasoning.
- May need to weaken to "all honest validators see all certified blocks within Δ" (causal consistency, not snapshot equality).

**Staged approach:**
- Wave 27: prove safety under strong sync.
- Wave 28: relax to causal consistency, reprove.

---

## 6. Staged Milestones (Wave Numbering)

### Wave 27: DAG Model & Quorum Mechanics [PROPOSED]
**Goals:**
- Formalize `CertifiedBlock`, `ValidatorSet`, `QuorumCertificate` in `DAG/Model.lean`.
- Prove `quorum_intersection_has_honest` by importing Wave23 lemma.
- Prove `qc_implies_quorum_voted`: `qc.valid → isQuorum vs qc.votes`.

**
Files:**
```
DAG/Model.lean            -- Core types
DAG/Quorum.lean          -- Quorum lemmas (imports Wave23)
DAG/Certificate.lean     -- QC validity
```

**Acceptance:**
- [ ] `quorum_intersection_has_honest` builds
- [ ] `qc_implies_quorum_voted` type-checks
- [ ] CI green on Wave23 + Wave27

---

### Wave 28: Safety via Voting Uniqueness [KEY MILESTONE]
**Goals:**
- Formalize `VotingRecord`: maps `(validator, round) → Option Vote`
- Prove **one-vote-per-round**: `validator_votes_once_per_round`
- Prove **conflicting-certificates-impossible**: No two valid QCs at same round for different blocks

**Key lemmas:**
```lean
lemma validator_votes_once_per_round
  (vs : ValidatorSet V) (v : V) (r : ℕ)
  (vote₁ vote₂ : Vote V)
  (h₁ : VotingRecord.hasVote v r vote₁)
  (h₂ : VotingRecord.hasVote v r vote₂)
  : vote₁.block = vote₂.block
  := by
  -- Protocol rule: honest validators sign at most one block per round

lemma conflicting_qcs_impossible
  (vs : ValidatorSet V) (qc₁ qc₂ : QuorumCertificate V)
  (h_valid₁ : qc₁.valid vs) (h_valid₂ : qc₂.valid vs)
  (h_same_round : qc₁.round = qc₂.round)
  (h_different : qc₁.block ≠ qc₂.block)
  : False
  := by
  -- Quorum intersection → ∃ honest validator voted twice
  obtain ⟨v, hv_both⟩ := quorum_intersection_has_honest vs qc₁.votes qc₂.votes
  -- Contradiction with one-vote-per-round
```

**Files:**
```
DAG/Voting.lean
DAG/Safety.lean          -- Main safety theorem
```

**Acceptance:**
- [ ] `conflicting_qcs_impossible` proven
- [ ] No `sorry` in safety chain

---

### Wave 29: 3-Chain Commit Rule [KEY MILESTONE]
**Goals:**
- Formalize `isThreeChain`: b₀ ← b₁ ← b₂ with consecutive rounds
- Define `Commits`: validator commits b₀ upon observing certified 3-chain
- Prove **commitment consistency**: If honest v₁ commits b at height h, no honest v₂ commits b' ≠ b at h

**Key definitions:**
```lean
def isThreeChain (b₀ b₁ b₂ : CertifiedBlock V) : Prop :=
  b₁.block.parent = b₀.id ∧
  b₂.block.parent = b₁.id ∧
  b₁.block.round = b₀.block.round + 1 ∧
  b₂.block.round = b₁.block.round + 1

def Commits (v : V) (b : CertifiedBlock V) (dag : DAG V) : Prop :=
  ∃ b₁ b₂,
    b₁ ∈ dag.certified ∧
    b₂ ∈ dag.certified ∧
    isThreeChain b b₁ b₂
```

**Main theorem:**
```lean
theorem commitment_consistency
  (vs : ValidatorSet V) (dag : DAG V)
  (v₁ v₂ : V) (h₁_honest : v₁ ∉ adv.corrupt) (h₂_honest : v₂ ∉ adv.corrupt)
  (b₁ b₂ : CertifiedBlock V)
  (h_commit₁ : Commits v₁ b₁ dag) (h_commit₂ : Commits v₂ b₂ dag)
  (h_same_height : b₁.block.height = b₂.block.height)
  : b₁ = b₂
  := by
  -- Use conflicting_qcs_impossible + 3-chain structure
```

**Files:**
```
DAG/ThreeChain.lean
DAG/Commitment.lean
```

**Acceptance:**
- [ ] `commitment_consistency` proven
- [ ] Passes property-based tests (100 random DAG scenarios)

---

### Wave 30: Partial Synchrony Model [INFRASTRUCTURE]
**Goals:**
- Formalize `PartialSyncNetwork` with GST and Δ
- Prove message delivery bounds post-GST
- Prove pre-GST arbitrary delay (no liveness guarantee)

**Key definitions:**
```lean
structure PartialSyncNetwork (V : Type*) where
  gst : ℕ                          -- Global Stabilization Time
  Δ : ℕ                            -- Message delay bound post-GST
  delivery : V → V → Message V → ℕ → Prop  -- (sender, receiver, msg, delivery_time)
  delivery_post_gst :
    ∀ sender receiver msg (sent_time : ℕ),
      sent_time ≥ gst →
      delivery sender receiver msg (sent_time + Δ)
```

**Files:**
```
Network/PartialSync.lean
Network/MessageDelivery.lean
```

**Acceptance:**
- [ ] Type-checks against existing `AsyncNetwork` from Wave23
- [ ] `delivery_post_gst` axiom formalized

---

### Wave 31: Liveness Building Blocks [PROPOSED]
**Goals:**
- Prove honest leaders get QCs post-GST (per §4.2 sketch)
- Prove 3-chain formation under consecutive honest leaders

**Key lemmas:**
```lean
lemma honest_leader_certified_post_gst
  (vs : ValidatorSet V) (net : PartialSyncNetwork V)
  (r : ℕ) (h_post_gst : r ≥ net.gst)
  (L : V) (h_leader : LeaderOfRound vs r = L) (h_honest : L ∉ adv.corrupt)
  : ∃ qc : QuorumCertificate V,
      qc.round = r ∧
      qc.block.author = L ∧
      qc.valid vs
  := by
  -- All honest validators vote within Δ
  -- Quorum (2f+1) forms by time r + Δ

lemma three_honest_rounds_form_chain
  (vs : ValidatorSet V) (net : PartialSyncNetwork V)
  (r : ℕ) (h_post_gst : r ≥ net.gst)
  (h_leaders : ∀ i ∈ [r, r+1, r+2], LeaderOfRound vs i ∉ adv.corrupt)
  : ∃ b₀ b₁ b₂,
      isThreeChain b₀ b₁ b₂ ∧
      b₀.block.round = r
  := by
  -- Chain honest_leader_certified_post_gst across 3 rounds
```

**Files:**
```
DAG/Liveness/HonestLeader.lean
DAG/Liveness/ChainFormation.lean
```

**Acceptance (CONDITIONAL):**
- [ ] Lemmas proven under assumptions:
  - `LeaderOfRound` is deterministic round-robin
  - All honest validators online post-GST
  - No network partitions post-GST
- [ ] Assumptions documented in `Assumptions.lean`

---

### Wave 32: Conditional Liveness Theorem [CONJECTURE → PROPOSED]
**Goals:**
- State main liveness theorem with explicit assumptions
- Mark as `[CONJECTURE]` pending full proof

**Theorem statement:**
```lean
theorem conditional_liveness
  (vs : ValidatorSet V) (net : PartialSyncNetwork V)
  (adv : ByzantineAdversary V vs)
  (h_byz_bound : adv.corrupt.card ≤ vs.f)
  -- KEY ASSUMPTIONS:
  (h_leader_sched : ∀ r ≥ net.gst, ∃ L ∈ vs.validators \ adv.corrupt,
      LeaderOfRound vs r = L ∧ LeaderOfRound vs (r+1) = (next L vs) ∧ ...)
  (h_online : ∀ v ∈ vs.validators \ adv.corrupt, ∀ r ≥ net.gst, online v r)
  (h_sync : ∀ r ≥ net.gst + 3*net.Δ, SynchronizedView vs net r)
  : ∀ b : CertifiedBlock V,
      ∃ r ≥ net.gst,
        ∃ v ∈ vs.validators \ adv.corrupt,
          Commits v b (dag_at_round vs net r)
  := by
  sorry  -- [CONJECTURE] – Wave 31 lemmas + induction on rounds
```

**Files:**
```
DAG/Liveness/Main.lean
DAG/Assumptions.lean      -- Centralized assumption registry
```

**Acceptance:**
- [ ] Theorem *stated* (not necessarily proven)
- [ ] All assumptions labeled in `Assumptions.lean`
- [ ] CI tracks `sorry` count (should decrease in future waves)

---

### Wave 33: Integration & End-to-End Safety [VERIFICATION TARGET]
**Goals:**
- Combine Waves 27–29 into top-level safety theorem
- Prove against realistic execution model (not just abstract DAG)
- **NO SORRY allowed in safety proof chain**

**Top-level theorem:**
```lean
theorem khipu_dag_safety
  (vs : ValidatorSet V) (net : PartialSyncNetwork V)
  (adv : ByzantineAdversary V vs)
  (h_byz_bound : adv.corrupt.card ≤ vs.f)
  (exec : Execution V vs net adv)  -- Execution trace type
  (v₁ v₂ : V) (h₁ : v₁ ∉ adv.corrupt) (h₂ : v₂ ∉ adv.corrupt)
  (b₁ b₂ : CertifiedBlock V)
  (t₁ t₂ : ℕ)
  (h_commit₁ : Commits v₁ b₁ (exec.dag_at t₁))
  (h_commit₂ : Commits v₂ b₂ (exec.dag_at t₂))
  (h_height : b₁.block.height = b₂.block.height)
  : b₁ = b₂
  := by
  apply commitment_consistency vs (exec.dag_at (max t₁ t₂))
  · -- Show b₁ still committed at later time (monotonicity)
  · -- Show b₂ still committed at later time
  · exact h_height
```

**Files:**
```
DAG/TopLevel.lean
DAG/Execution.lean       -- Execution trace model
```

**Acceptance (CRITICAL):**
- [ ] `khipu_dag_safety` proven with **zero `sorry`**
- [ ] Proof checked by CI in < 5 minutes
- [ ] External review by 2+ Lean experts

---

### Wave 34: Documentation & Assumptions Audit [DELIVERABLE]
**Goals:**
-