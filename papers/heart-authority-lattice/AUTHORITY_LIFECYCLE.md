# Authority lifecycle contract

**Purpose:** CTO-facing control lifecycle derived from the A11oy Council source contract and aligned with the proposed flagship authority receipt schema.

**Read on:** 2026-09-22

## Core finding

Authority is represented as a bounded grant, not as a property of a model, score, receipt, or successful test.

The Council `CapabilityGrant` implementation includes:

```text
subject
capabilities
actions
exact_targets
budget_microunits
expires_at
revoked
```

The delegation serialization preserves `actions`, `exact_targets`, `budget_microunits`, `expires_at`, and `revoked`. A non-negative budget is enforced by the grant contract.

## Control lifecycle

| Stage | Required control object | Fail-closed question | Evidence retained |
|---|---|---|---|
| 1. Propose | Model/adviser assessment | What is being proposed, by whom, and for what target? | Proposal digest; model/runtime identity if available |
| 2. Bind | Commitment | Is the action description immutable enough to evaluate? | Commitment digest; exact target; action class |
| 3. Scope | Capability grant | Does the named subject hold this capability, for this action and exact target? | Grant ID; subject; capability; actions; exact targets |
| 4. Budget | Capability grant | Is the action within a precommitted budget? | Budget unit; requested cost; remaining budget |
| 5. Deliberate | Council evaluations | Are required roles present and are vetoes clear? | Role assessments; commitment/reveal material; minority record |
| 6. Admit | SENTRA / input controls | Is the request structurally admissible? | Admission result; rejection reason if any |
| 7. Halt check | HUKLLA | Is a tripwire active, including egress, ledger, bypass, deadman, or evidence-gap conditions? | Tripwire evidence; deadman state; chain status |
| 8. Authorize | Explicit verdict | Is the result still in scope, unexpired, and unrevoked immediately before effect? | Verdict; evaluated-at time; grant status |
| 9. Effect | Source-system adapter | Which real identity executed which bounded effect? | Effector identity; source-system receipt; rollback handle |
| 10. Record | YAWAR/Khipu ledger | Is the decision/effect evidence append-only and integrity-checkable? | Receipt payload; hashes; signature state; parent link |
| 11. Revoke / rollback | Revocation and remediation | Can the grant be revoked and can the effect be reversed or contained? | Revocation event; rollback outcome; incident record |

## Lifecycle invariants

```text
I1. Proposal is not authority.
I2. A grant for one target does not authorize a different target.
I3. A grant with an expired timestamp is not valid authority.
I4. A revoked grant is not valid authority.
I5. Budget exhaustion denies the next effect.
I6. A Sentinel or Verifier veto blocks authorization.
I7. A HUKLLA deadman state refuses writes.
I8. Receipt integrity/origin does not prove the decision was correct.
I9. Authorization is checked before the effect, not inferred afterward.
I10. A runtime test does not establish a production effector binding.
```

## CTO interpretation

The paper will frame this as a reference architecture for **bounded delegated authority**:

> An AI may formulate and assess a proposal, but it cannot obtain standing permission by producing a plausible answer. A bounded effect requires a named subject, an allowed capability and action, an exact target, a precommitted budget, a live unrevoked grant, required-role/veto checks, admission and halt checks, and a traceable real effector.

## What source currently establishes

- The Council contract defines scoped grant fields for capabilities, actions, targets, budgets, expiry, and revocation.
- The Council package records tests around capability denial, exact targets, budgets, risk classes, required roles, vetoes, ledger verification, and tamper detection.
- IMMUNE source provides a separate admission/receipt/tripwire path, including deadman refusal of writes.

## What remains unproven

- That every live source-system adapter rechecks grants immediately before effect.
- That all effects have rollback handles.
- That a complete revocation propagation mechanism is deployed across every service.
- That the proposed canonical authority-receipt schema exactly matches every runtime record.
- That independent operators can reproduce the complete end-to-end lifecycle.

## Required manuscript language

```text
Use: “scoped authority contract”, “bounded grant”, “exact target”,
“precommitted budget”, “expiry”, “revocation”, “required-role check”,
“veto”, and “controlled egress”.

Avoid: “the AI is authorized”, “the model decided”, “the receipt grants
permission”, “safe autonomous action”, or “fully deployed control plane”
unless the exact source-system binding is separately demonstrated.
```
