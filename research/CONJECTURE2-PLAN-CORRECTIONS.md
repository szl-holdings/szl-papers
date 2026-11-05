# Conjecture 2 Plan — Review Findings and Corrected Statements

**Epistemic status: [PROPOSED]** — companion to
[`CONJECTURE2-FORMALIZATION-PLAN.md`](./CONJECTURE2-FORMALIZATION-PLAN.md),
recording three defects found in source review of that plan, the counterexample
shapes that expose them, and the corrected statements that Wave 27+ must
target instead. Nothing here is machine-checked. No theorem is promoted.

---

## Defect 1 — The no-equivocation assumption is aimed at the wrong party

**Plan text (defective):** the no-equivocation assumption is stated over
*corrupt authors* — a byzantine validator does not sign two conflicting
blocks. That is an assumption about adversary behavior, which a safety proof
cannot demand: equivocation is precisely what byzantine actors do.

**Counterexample shape:** let validator `v` be corrupt and sign both
`B_r^x` (round `r`, slot `x`) and `B_r^y` (round `r`, slot `y ≠ x`). Under the
plan's assumption this is excluded by fiat, so the safety proof is vacuous for
the byzantine case it exists to cover. No quorum-intersection argument can
recover, because the intersection guarantee ("at least one honest witness")
only constrains *honest* voters.

**Corrected statement:** the equivocation constraint must be a property of
*honest* voters plus the signature scheme, of the form:

```lean
-- honest voters never vote for two distinct proposals in the same round
-- (voter-state model, not author-behavior model)
honest_voter_no_equivocation :
  ∀ (v : Validator) (r : ℕ) (b₁ b₂ : CertifiedBlock V),
    Honest v → v ∈ b₁.qc.votes → v ∈ b₂.qc.votes →
    b₁.round = r → b₂.round = r → b₁ = b₂
```

Corrupt voters may equivocate freely; safety must then follow from
quorum intersection (`|Q₁ ∩ Q₂| ≥ f+1` guarantees an *honest* voter in the
intersection, and that voter's no-equivocation property forces the two
certified blocks to be identical). This is the standard byzantine-quorum
shape and matches the Wave23 lemma's actual content.

## Defect 2 — `conditional_liveness` over-promises

**Plan text (defective):** `conditional_liveness` promises commitment for
*every* certified block, with no `valid`/`proposed`/`in-execution` scope.

**Counterexample shape:** a certified block exists whose payload was never
broadcast to any honest validator (a corrupt author certified it with f+1
corrupt votes plus the quorum's honest votes obtained out of context). The
plan's statement would demand eventual commitment of a block no honest
validator has in its DAG — unprovable under partial synchrony, and false in
the execution where the block is never delivered.

**Corrected statement:** liveness must be scoped to blocks that are (a)
authored by an honest validator or delivered, (b) valid, and (c) in the causal
past of a later certified block, e.g.:

```lean
-- scoped progress: delivered, valid blocks that anchor a later certified
-- round eventually commit, under eventual synchrony
scoped_liveness :
  ∀ (b : CertifiedBlock V),
    Delivered b → Valid b → AnchorsLaterCertifiedRound b →
    Eventually (Committed b)
```

This mirrors lean-dag's liveness-from-eventual-DAG-synchrony shape and stays
inside what the Mysticeti-lineage results actually prove.

## Defect 3 — `delivery_post_GST` lacks a sent-event premise

**Plan text (defective):** `delivery_post_GST` permits delivery assumptions
for messages that were never sent.

**Counterexample shape:** take any message `m` that no process ever
broadcast. `delivery_post_GST` as written still admits "after GST, `m` is
delivered" — the network model becomes unsound because it manufactures
deliveries with no causal origin, and any liveness conclusion can be
"proved" for phantom messages.

**Corrected statement:** the delivery premise must be guarded by a sent-event
premise, as in the standard partially-synchronous model:

```lean
-- only sent messages are eventually delivered, after GST
delivery_post_GST :
  ∀ (m : Message), Sent m →
    EventuallyAfterGST (Delivered m)
```

---

## What is NOT changed

- The locked-8 kernel: untouched, as before.
- The Wave23 quorum-intersection lemma: unchanged; it is the correct
  combinatorial core and defect 1's fix relies on exactly its honest-witness
  guarantee.
- No claim in either document is promoted to [VERIFIED]. Wave 27 must
  formalize the corrected statements above, not the defective originals.

## Attribution

The three defects and their locations in the plan were identified in source
review (recorded in the operational handoff of 2026-11-05); the counterexample
shapes and corrected statements here are drafted with AI assistance and
follow the standard byzantine-quorum / partial-synchrony models (Dwork,
Lynch, Stockmeyer 1988; Malkhi–Reiter quorum systems; the Mysticeti-lineage
mechanized results cited in the parent plan).
