# Formal claim resolution: Lambda uniqueness

**Resolution date:** 2026-09-22

## Decision

The flagship paper shall not state or imply that unconditional Lambda uniqueness follows from the bare A1-A5 axiom set.

The formal source resolves the apparent ambiguity in the v24 thesis introduction:

```text
Unconditional Lambda uniqueness under A1-A5:
FALSE AS STATED / Conjecture 1 remains open as a proof obligation.

Conditional Lambda uniqueness:
REAL, but only under explicitly stated additional structure.
```

## Primary formal source

Repository: `szl-holdings/lutar-lean`

### Unconditional boundary

`Lutar/Round13/Lambda_Uniqueness.lean` documents that bare A1-A5 are insufficient: `maxAgg` and `min` are counterexamples. It labels the unconditional `lambda_unique` obligation open/false as stated.

`Lutar/Uniqueness.lean` retains the same honesty boundary: no sorry-free unconditional proof is re-exported.

### Conditional results

| Result | Exact boundary | Paper wording |
|---|---|---|
| `lambda_unique_of_factors` | `LutarAxioms Phi` plus `Factors Phi alpha` | Proven conditional factorization result |
| `lambda_unique_of_separable` | A1-A5 plus separable, monotone, multiplicative per-axis slices | Axiom-free conditional result, still structural-hypothesis bounded |
| `TheoremU_LambdaUnique` | Identifiability Assumptions; equality modulo `approximatelyLambda`, with strict equality only under anchoring/normalization conditions | Real conditional theorem; do not shorten to “Lambda is unique” |
| `lambda_unique_under_block` | Declared block-consistency A6-prime route | Conditional theorem with a named project assumption |
| `lambda_unique_under_A6` | Declared bisymmetry A6 route | Conditional theorem with a named project assumption |

## Source anchors read

- `Lutar/Round13/Lambda_Uniqueness.lean`: terminal factorization theorem; explicit A1-A5 counterexample boundary.
- `Lutar/Round13/LambdaSeparable.lean`: conditional separable/multiplicative route.
- `Lutar/Uniqueness/TheoremU.lean`: Theorem U by reduction to Round13 conditional theorems; no new axiom token or placeholder in that module.
- `STATUS.md`, `README.md`, `VERIFIED_THEOREMS.md`, and `docs/FRONTIER.md`: repeated status language that unconditional uniqueness remains Conjecture 1 while conditional results are separately labeled.

## Manuscript rule

Every occurrence of “unique,” “uniqueness,” “Theorem U,” “Lambda theorem,” or “proved” must include:

1. the exact result name;
2. the source repository and revision used by the paper;
3. all structural premises or declared assumptions;
4. whether the conclusion is equality or equivalence modulo `approximatelyLambda`;
5. its relation to the locked Doctrine v11 epoch.

## Approved summary sentence

> The formal program contains axiom-free **conditional** Lambda-uniqueness theorems under stated structural premises; it does not establish unconditional uniqueness from the bare A1-A5 axioms, for which published counterexamples remain decisive.

## Forbidden summary sentences

```text
“Lambda uniqueness is proved.”
“The system has a theorem of trust.”
“A Lambda score establishes authority.”
“A later formal result silently upgrades the locked Doctrine v11 baseline.”
```
