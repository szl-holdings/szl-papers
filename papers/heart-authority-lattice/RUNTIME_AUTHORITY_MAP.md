# Runtime authority map

**Purpose:** source-grounded map of what the current runtime code and documentation support, and what they do not establish.

**Read on:** 2026-09-22

## Core separation

```text
Model / adviser: proposes assessments.
Council: evaluates a bounded commitment under explicit contracts.
SENTRA: admits or rejects input.
YAWAR: records receipt material.
HUKLLA: detects defined tripwires and can freeze/refuse writes.
Human / source-system control: remains necessary for externally effective action.
```

No one layer substitutes for another.

## A11oy Council kernel

**Primary source:** `szl-holdings/a11oy`, `packages/council-kernel/`

The kernel source describes itself as a deterministic authority kernel for governed adviser councils. Advisers may propose assessments; execution authority is retained in explicit capability, role, veto, diversity, risk, and receipt contracts.

### Source-backed roles

| Role | Source-backed function | Does not establish |
|---|---|---|
| Authority | Checks mandate, capability, target, and budget | Automatic external execution |
| Sentinel | Evaluates safety and may issue categorical veto | General safety proof |
| Verifier | Participates in required-role and evidence checks | Decision-quality proof |
| Value | Participates in governed evaluation | Authority to override scope |

### Source-backed control properties

- Contract tests cover capability denial, exact targets, budgets, risk classes, required roles, blinded commitment/reveal, Sentinel and Verifier vetoes, Authority denial, correlation discounting, minority retention, append-only ledger verification, tamper detection, and honest signature state.
- The CLI documents fail-closed handling for invalid documents and ledgers, and explicitly says its commands do not execute the proposed action, retrieve credentials, or grant ambient authority.
- Post-merge local-source qualification explicitly does not establish hosted checks, independent review, protected promotion, deployment, managed signing authority, or production autonomy.

## IMMUNE admission, receipt, and halt path

**Primary source:** `szl-holdings/immune`, `python/immune/`

The Python runtime initializes in `SENTRA_REJECT` mode. Its documented operational chain is:

```text
SENTRA admission -> YUYAY axes -> Lambda -> YAWAR accept receipt -> HUKLLA -> frontier silhouette
```

This is an implementation/source claim, not a claim that every public endpoint or system-of-record path is deployed and governed by the chain.

### HUKLLA v11 tripwire boundary

The canonical IMMUNE registry exposes T01-T10. Relevant source-indexed conditions include:

| Tripwire | Meaning | Runtime consequence represented by source |
|---|---|---|
| T05 `egress.unauthorized` | Outbound egress to a non-allowlisted host | Critical tripwire condition |
| T06 `ledger.divergence` | Recomputed ledger chain disagrees | Critical tripwire condition |
| T07 `deadman.engaged` | DEADMAN freeze active | Refuse all writes |
| T08 `sentra.bypass` | Receipt produced without SENTRA acceptance | Critical tripwire condition |
| T10 `evidence.gap` | HUKLLA chain gap against cycle counter | High-severity tripwire condition |

A11oy sources also describe the frozen 10-tripwire baseline as: tripwire fire -> `allegiance_pass = False` -> state frozen -> deadman halts cycle, with no partial halt, override, or suppression. The flagship paper will treat that as a version-pinned source statement; direct runtime reproduction remains a separate gate.

## Receipt boundary

The Council receipt verifier says a valid signed receipt demonstrates that a scoped envelope was signed by the pinned runtime key and was unaltered; it expressly says this is not proof of decision quality or authority.

## CTO-facing operational interpretation

The source supports a narrow architecture claim:

> A proposed action can be subjected to explicit scope and budget checks, required roles and vetoes, admission control, append-only receipt recording, and defined halt/freeze tripwires before an external effect is considered.

The source does **not** yet support any broader claim that the system autonomously executes, that all production effects are governed, that signatures prove correctness, or that a local validation result certifies a hosted deployment.

## Paper rules

```text
Do not write “the Council executes.”
Do not write “a receipt authorizes.”
Do not write “HUKLLA makes a deployment safe.”
Do not write “tests prove production autonomy.”
Do write exact scope, target, capability, budget, required roles, vetoes,
receipt state, expiry/revocation state, and the identity of the real effector.
```

## Remaining proof-pack work

- [ ] Read exact Council capability-grant and decision-record schemas.
- [ ] Read runtime state-transition implementation and tests, not only indexed excerpts.
- [ ] Identify which actual egress adapters exist and whether they are bound to source-system authorization.
- [ ] Reproduce a denied-capability, veto, deadman, ledger-divergence, and unauthorized-egress path.
- [ ] Bind the results to commit SHA, command, inputs, outputs, and hashes.
