# Formula-ID crosswalk

This crosswalk binds the eight formula-family identifiers in the locked receipt namespace to its 19 audited Lean declarations. It is not a global alias registry. The same short `F*` labels have conflicting semantics in other inventories, so every row remains `NAMESPACE_SCOPED_ONLY` and every external alias remains `COLLISION_QUARANTINED`.

The `PROVED` label is receipt-scoped: it refers only to the exact encoded declaration, source identity, command, target-module placeholder scan, and disclosed axiom surface recorded by the copied receipt. This bundle does not establish full dependency closure, reconcile the older doctrine pin, or transfer proof credit to served, runtime, manuscript, or queue records.

| Namespaced family | Lean declaration | Axioms | Exact semantic boundary |
|---|---|---|---|
| `doctrine_v11_locked_formulas:F1` | `f1_replay_fold_deterministic` | `none` | pure transition/fold determinism and trace binding; not cryptographic hash security |
| `doctrine_v11_locked_formulas:F1` | `f1_replay_fold_eq_trace_last` | `propext` | pure transition/fold determinism and trace binding; not cryptographic hash security |
| `doctrine_v11_locked_formulas:F4` | `f4_khipu_dag_acyclic_preserved` | `propext` | acyclicity for the encoded Nat edge-list model under the explicit backward-edge invariant |
| `doctrine_v11_locked_formulas:F7` | `f7_chaski_drain_eq` | `propext` | FIFO order for the encoded list queue |
| `doctrine_v11_locked_formulas:F7` | `f7_chaski_fifo_order` | `propext` | FIFO order for the encoded list queue |
| `doctrine_v11_locked_formulas:F7` | `f7_chaski_fifo_positional` | `propext` | FIFO order for the encoded list queue |
| `doctrine_v11_locked_formulas:F11` | `f11_ayni_reciprocity_conservation` | `propext` | integer credit/debit conservation and mirrored-delta parity; not a game-theoretic equilibrium theorem |
| `doctrine_v11_locked_formulas:F11` | `f11_tit_for_tat_parity` | `propext` | integer credit/debit conservation and mirrored-delta parity; not a game-theoretic equilibrium theorem |
| `doctrine_v11_locked_formulas:F12` | `f12_kuramoto_additive` | `none` | linear/additive superposition only; not nonlinear Kuramoto synchronization |
| `doctrine_v11_locked_formulas:F12` | `f12_kuramoto_superposition` | `propext` | linear/additive superposition only; not nonlinear Kuramoto synchronization |
| `doctrine_v11_locked_formulas:F18` | `f18_erasure_tolerance` | `propext;Quot.sound` | RS(10,6) parity arithmetic and erasure-count inequality; not a full Reed-Solomon decoder correctness proof |
| `doctrine_v11_locked_formulas:F18` | `f18_reed_solomon_parity_count` | `none` | RS(10,6) parity arithmetic and erasure-count inequality; not a full Reed-Solomon decoder correctness proof |
| `doctrine_v11_locked_formulas:F19` | `f19_bekenstein_additive` | `none` | additive/monotone budget scaffold only; not the physical Bekenstein bound |
| `doctrine_v11_locked_formulas:F19` | `f19_budget_monotone` | `none` | additive/monotone budget scaffold only; not the physical Bekenstein bound |
| `doctrine_v11_locked_formulas:F19` | `f19_budget_total_cons` | `propext` | additive/monotone budget scaffold only; not the physical Bekenstein bound |
| `doctrine_v11_locked_formulas:F19` | `f19_region_le_total` | `propext` | additive/monotone budget scaffold only; not the physical Bekenstein bound |
| `doctrine_v11_locked_formulas:F22` | `f22_emit_appends_length` | `propext` | monotonicity for the encoded List.range sequence log |
| `doctrine_v11_locked_formulas:F22` | `f22_emit_strictly_greater` | `propext;Quot.sound` | monotonicity for the encoded List.range sequence log |
| `doctrine_v11_locked_formulas:F22` | `f22_khipu_emit_monotone` | `propext;Quot.sound` | monotonicity for the encoded List.range sequence log |

## Non-promotion rules

- Do not join a row to another inventory on the short `F*` token alone.
- Do not describe a family count as a declaration count.
- Do not transfer `PROVED` from these declarations to Python functions, served endpoints, manuscript blocks, or queue items.
- Do not treat a successful whole-project build as a theorem total.
- Do not remove the receipt's pin-reconciliation warning or claim full dependency closure from this bundle.
