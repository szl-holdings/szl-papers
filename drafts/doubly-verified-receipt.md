<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- SZL Holdings — Draft short paper · target CAV / ITP (arXiv cs.LO cross-list cs.CR) -->

# Doubly-Verified Receipts: A Lean Theorem that Consumes an α,β-CROWN Robustness Certificate and Binds Model-Verification SOTA to a Governance Kernel

**Draft short paper — target: CAV / ITP (arXiv `cs.LO`, cross-list `cs.CR`, `cs.LG`).**

**Author.** Stephen P. Lutar Jr. — SZL Holdings.
ORCID: [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173).

**Concept DOI (always-latest):** [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926).

**Artifacts.** Lean 4 kernel: [`szl-holdings/lutar-lean`](https://github.com/szl-holdings/lutar-lean),
locked at commit `c7c0ba17` (749 declarations / 14 unique axioms / 163 sorries; locked-8
{F1, F4, F7, F11, F12, F18, F19, F22}, certified by `locked_count_eight`).

> **Honesty banner (binding).** This is a **proposal** with a *stated* Lean theorem schema and a
> worked proof sketch; it is **not** a claim that the doubly-verified theorem is already merged and
> kernel-clean in `lutar-lean` at `c7c0ba17`. The theorem *consumes an external robustness certificate
> as an explicit hypothesis* — it does **not** re-prove the neural-network verifier, and it inherits
> that verifier's soundness caveats (§6). The governance-kernel side (receipt structure, the Λ gate)
> is grounded in the existing locked-8; Λ-uniqueness remains **Conjecture 1** and is not used here.

---

## Abstract

State-of-the-art neural-network robustness verifiers (α,β-CROWN and peers) produce machine-generated
certificates that a network is robust on a specified input region, and are evaluated annually at
VNN-COMP. Separately, an AI-governance kernel can machine-check *governance* properties (append-only
receipts, weakest-link trust gating) in an interactive theorem prover. These two verification cultures
have never been *composed*: a governance receipt today asserts "this decision was governed" but says
nothing checkable about the *model's* robustness, and a robustness certificate says nothing about
*governance*. We propose the missing bridge: a Lean 4 theorem that **consumes an α,β-CROWN robustness
certificate as an explicit hypothesis** and **discharges a governance property**, emitting a
**doubly-verified receipt** that binds the model-verification result to the governance kernel. The
receipt is designed to be independently checkable with standard supply-chain tooling — the certificate
and the Lean proof term are packaged as an **in-toto / SLSA attestation** and logged to a transparency
log (Sigstore/Rekor), so "verify the receipt" is a `cosign`/`slsa-verifier` operation, not an
SZL-only trust-me. We give the theorem schema, the attestation binding, an honest account of the
trusted base (the verifier's soundness is an *assumption*, disclosed as a hypothesis), and the known
soundness pitfalls of NN verifiers (SoundnessBench, floating-point nondeterminism). The contribution
is a *composition pattern* — "doubly-verified" (model verifier ∘ governance kernel) receipts — not a
new verifier.

**Keywords.** neural-network verification, α,β-CROWN, robustness certificate, Lean 4, interactive
theorem proving, proof-carrying attestation, in-toto, SLSA, Sigstore, supply-chain integrity, AI
governance.

---

## 1. Introduction

Two mature but disjoint verification cultures bear on trustworthy AI:

1. **Model verification.** Complete/incomplete NN robustness verifiers such as α,β-CROWN prove that a
   network's output stays within a safe set for all inputs in an \(\ell_p\)-ball around a point. β-CROWN
   introduced per-neuron split constraints via optimizable bound propagation
   ([Wang et al., NeurIPS 2021](https://arxiv.org/abs/2103.06624)), building on the "fast and complete"
   GPU-parallel branch-and-bound of α-CROWN ([Xu et al., 2020](https://arxiv.org/abs/2011.13824)); the
   combined α,β-CROWN tool has been a repeated VNN-COMP winner
   ([Brix et al., VNN-COMP 2024](https://arxiv.org/abs/2412.19985)).
2. **Governance verification.** An interactive theorem prover (Lean 4 + Mathlib) machine-checks
   *governance* properties of a decision loop: that receipts form an append-only hash-chain, that a
   weakest-link trust gate behaves as specified, that ordering is FIFO. In `lutar-lean` these are the
   **locked-8** {F1, F4, F7, F11, F12, F18, F19, F22}, sorry-free at `c7c0ba17`.

Nothing today *composes* them. A governance receipt asserts "governed," but is silent on the model's
robustness; a robustness certificate is silent on governance. We propose to close the gap with a Lean
theorem that takes a robustness certificate as a *hypothesis* and produces a governance conclusion —
so a single receipt witnesses **both** facts, and can be verified by a third party using open
supply-chain tooling.

**Contribution.** (i) A Lean 4 theorem *schema* `doubly_verified_receipt` that consumes an
α,β-CROWN-style certificate as an explicit hypothesis and discharges a governance property (§3–§4).
(ii) An attestation binding that packages the certificate + Lean proof term as an in-toto/SLSA
predicate logged to Sigstore/Rekor, making the receipt `cosign`/`slsa-verifier`-checkable (§5). (iii)
An honest trusted-base and soundness analysis (§6). This is a *composition pattern*, not a new
verifier and not a new soundness proof of α,β-CROWN.

---

## 2. Background and threat model

**Robustness certificate (informal).** For a network \(N\), an input \(x_0\), a radius \(\epsilon\),
and a property \(P\) on outputs, an α,β-CROWN run either (a) *certifies* \(\forall x.\ \lVert x - x_0
\rVert_p \le \epsilon \Rightarrow P(N(x))\), or (b) returns a counterexample, or (c) times out. A
successful run emits a certificate object \(C\) (bounds, split tree, and the verified property) that,
if the verifier is sound, entails the \(\forall\)-statement.

**Governance property (informal).** A predicate \(G(\text{receipt})\) on a governed decision record —
e.g., "the decision's trust vector cleared the Λ weakest-link gate *and* the record is a well-formed
append-only receipt whose emit is monotone." The kernel already proves the structural half
(append-only / FIFO / emit-monotone) as locked-8 formulas F4/F7/F22.

**Threat model.** We defend against (i) *governance forgery* — claiming a decision was governed when
it was not — addressed by the kernel-checked receipt; and (ii) *robustness overclaim* — attaching a
"robust" label with no checkable basis — addressed by requiring the certificate as a hypothesis and
by disclosing verifier soundness as an assumption. We do **not** defend against a *buggy verifier*
producing an unsound certificate; instead we make that dependency *explicit and disclosed* (§6),
which is precisely the honesty the pattern is designed to deliver.

---

## 3. The doubly-verified receipt: theorem schema

We model the certificate as an opaque structure carrying a *verified property* and a *soundness
witness type*. The theorem consumes the certificate's guarantee as a hypothesis and concludes the
governance property, returning a receipt value.

```lean
/-- Abstract robustness certificate produced by an external verifier (α,β-CROWN). -/
structure RobustnessCert where
  net      : Network                     -- the audited network (by content hash)
  center   : Input                       -- x₀
  radius   : ℝ≥0                          -- ε
  prop     : Output → Prop               -- the output-space property P
  /-- The verifier's *claim*: robustness on the ε-ball. Consumed as a hypothesis;
      its truth is the verifier's responsibility, disclosed in `#print axioms`. -/
  certified : ∀ x, dist x center ≤ radius → prop (eval net x)

/-- A governance receipt binding a robustness fact to the governed decision. -/
structure DoublyVerifiedReceipt where
  cert        : RobustnessCert
  decision    : GovernedDecision
  trustVec    : Fin k → NNReal
  gatePassed  : Λ k trustVec = 1            -- weakest-link Λ gate cleared
  chainOk     : AppendOnly decision.log     -- F4/F7/F22 structural guarantee
  bound       : robustnessAxis trustVec = encodeCert cert  -- cert bound to a trust axis

/-- **Theorem schema (proposed).** Given a robustness certificate whose guarantee holds,
    a governed decision whose trust vector clears the Λ gate, and an append-only log,
    there exists a doubly-verified receipt that simultaneously witnesses
    (i) model robustness on the ε-ball and (ii) the governance property. -/
theorem doubly_verified_receipt {k : ℕ} (hk : 0 < k)
    (cert : RobustnessCert)
    (decision : GovernedDecision)
    (trustVec : Fin k → NNReal)
    (hGate  : Λ k trustVec = 1)
    (hChain : AppendOnly decision.log)
    (hBind  : robustnessAxis trustVec = encodeCert cert) :
    ∃ r : DoublyVerifiedReceipt,
      r.cert = cert ∧ r.decision = decision ∧
      (∀ x, dist x cert.center ≤ cert.radius → cert.prop (eval cert.net x)) ∧
      GovernanceOK r := by
  refine ⟨⟨cert, decision, trustVec, hGate, hChain, hBind⟩, rfl, rfl, ?_, ?_⟩
  · exact cert.certified                    -- robustness: *inherited* from the hypothesis
  · exact governanceOK_of_gate_chain hGate hChain hBind   -- governance: kernel-checked
```

The point is the **type of `certified`**: the robustness fact enters as data the theorem *cannot*
manufacture, only *consume*. The kernel proves the governance conclusion `GovernanceOK` from the Λ
gate and the append-only structure (grounded in the locked-8 F4/F7/F22 and the Λ gate), and *carries*
the robustness fact forward verbatim. The receipt therefore *binds* the two without conflating them.

---

## 4. Method: producing and checking the receipt

1. **Run the verifier.** Execute α,β-CROWN on \((N, x_0, \epsilon, P)\). On success it emits a
   certificate \(C\) (bounds + split tree + verified property), pinned by the content hash of \(N\)
   and \(x_0\).
2. **Encode the certificate as a Lean hypothesis.** Serialize \(C\) into a `RobustnessCert` whose
   `certified` field is *asserted from the verifier's output*. This assertion is the honest boundary:
   the Lean proof does not re-derive it; it *records* it and *tracks* it (§6). A stronger variant
   re-checks the certificate's bound-propagation arithmetic inside Lean over rationals; we mark that as
   future work (§7).
3. **Discharge governance.** Apply `doubly_verified_receipt` with the decision's trust vector (which
   must clear the Λ weakest-link gate, \(\Lambda_k = 1\)) and the append-only log obligation
   (F4/F7/F22). The result is a `DoublyVerifiedReceipt` value.
4. **Attest and log** (§5). Emit the receipt, the certificate, and the Lean proof term as an
   in-toto/SLSA attestation, sign it, and record it in a transparency log.
5. **Third-party verification.** A relying party checks: (a) the Lean proof term type-checks against
   the pinned kernel; (b) the attestation signature and provenance verify with `cosign`/
   `slsa-verifier`; (c) the transparency-log inclusion proof. All three are open-tooling operations.

---

## 5. Binding to supply-chain SOTA (in-toto / SLSA / Sigstore)

To make "verify the receipt" a *standard* operation rather than an SZL-only ritual, the receipt is
wrapped as an **in-toto attestation** whose predicate carries: the certificate digest, the audited
network digest, the Lean toolchain + Mathlib pins, the kernel commit (`c7c0ba17`), and the proof-term
digest. in-toto attestations are the recommended vehicle for expressing supply-chain claims within
SLSA ([in-toto and SLSA, 2023](https://slsa.dev/blog/2023/05/in-toto-and-slsa);
[SLSA specification](https://slsa.dev/spec/v1.0/)). The attestation is signed and its inclusion
recorded in a transparency log via Sigstore, so signatures are keyless/ephemeral and publicly
auditable ([Newman, Meyers, Torres-Arias, CCS 2022](https://doi.org/10.1145/3548606.3560596)). A
relying party then runs:

```bash
# verify the attestation's provenance / signature
slsa-verifier verify-artifact receipt.bundle \
  --provenance-path receipt.intoto.jsonl --source-uri github.com/szl-holdings/lutar-lean
# verify signature + transparency-log inclusion
cosign verify-blob --bundle receipt.sigstore receipt.json
```

**Honest posture.** The kernel repos are **SLSA L1 honest with L2 where `attest-build-provenance`
runs**; **L3 is a roadmap** (isolated builders + hermetic builds). We do not claim L3, FedRAMP, Iron
Bank, or CMMC. The attestation *format* is standards-based; the *level* is disclosed as above.

---

## 6. Honest trusted base and soundness caveats

The doubly-verified receipt's guarantee is only as strong as its weakest disclosed dependency. We
enumerate them.

- **Verifier soundness is an assumption, not a theorem.** `RobustnessCert.certified` is *consumed*,
  not proven. If α,β-CROWN is unsound on an instance, the receipt's robustness half is vacuously
  wrong. This is not hypothetical: SoundnessBench demonstrates that state-of-the-art verifiers can
  make *false* verification claims on instances with hidden counterexamples
  ([Zhou et al., 2024](https://arxiv.org/abs/2412.03154)). The pattern's honesty contribution is to
  make this dependency *explicit and disclosed in the `#print axioms` ledger* (as a `verifierSound`
  assumption), rather than silently folding it into a "verified" label.
- **Floating-point / hardware nondeterminism.** NN-verification results can differ across hardware and
  seeds because bound propagation runs in floating point; VNN-COMP evaluates on equal-cost hardware
  precisely to control this ([Brix et al., 2024](https://arxiv.org/abs/2412.19985)). Our kernel
  already carries a floating-point summation forward-error bound (CF-17,
  `Lutar/Khipu/NumericStability.lean`, following
  [Higham, 2002](https://doi.org/10.1137/1.9780898718027)); we surface the fp caveat wherever the
  receipt claims reproducibility, rather than claiming bit-exact determinism.
- **The theorem is a proposal, not a merged locked formula.** `doubly_verified_receipt` is a *schema*
  with a worked sketch; it is **not** part of the locked-8 at `c7c0ba17` and is not claimed
  kernel-clean-in-tree. The governance half rests on existing locked formulas (F4/F7/F22 append-only /
  FIFO / emit-monotone) and the Λ gate; the robustness half is inherited from the hypothesis.
- **Λ is Conjecture 1.** The Λ gate is used only as a *value check* (\(\Lambda_k = 1\) iff every axis
  clears), not via any uniqueness claim. Λ's *unconditional uniqueness* remains **Conjecture 1**
  (machine-checked false as stated); only conditional Theorem U is proven, and this paper does not
  depend on it.
- **Binding integrity.** `encodeCert` must be collision-resistant for the `hBind` equation to bind the
  *right* certificate to the trust axis; this reduces to the disclosed `sha256_collision_resistant`
  idealization already in the kernel's `#print axioms` ledger — an *assumption*, not a hardness proof.

---

## 7. Limitations and future work

- **Re-checking the certificate in-kernel.** The strongest form would re-verify α,β-CROWN's
  bound-propagation arithmetic *inside* Lean over exact rationals (a proof-producing checker), turning
  `certified` from an assumption into a theorem. This is substantial engineering and is out of scope
  here; it is the natural next step and would remove the largest disclosed assumption.
- **Property language.** We treat `prop : Output → Prop` abstractly; a production system needs a fixed,
  audited property DSL (e.g., VNN-LIB-style specifications) with a Lean semantics.
- **Batching and revocation.** Receipts should compose into a batch with a single Merkle root and
  support revocation of a superseded certificate; not modeled here.
- **No empirical evaluation yet.** This draft states the schema and the binding; it does not report
  end-to-end runtimes or a case study. Those belong in a full CAV/ITP submission with an artifact.

---

## 8. Related work

α,β-CROWN and the VNN-COMP series define the model-verification SOTA
([Xu et al., 2020](https://arxiv.org/abs/2011.13824);
[Wang et al., 2021](https://arxiv.org/abs/2103.06624);
[Brix et al., 2024](https://arxiv.org/abs/2412.19985)); SoundnessBench audits their soundness
([Zhou et al., 2024](https://arxiv.org/abs/2412.03154)). Supply-chain integrity SOTA is defined by
SLSA, in-toto, and Sigstore ([in-toto and SLSA, 2023](https://slsa.dev/blog/2023/05/in-toto-and-slsa);
[Newman et al., CCS 2022](https://doi.org/10.1145/3548606.3560596)). Proof-carrying and attested
inference (e.g., inference cards / attested ML artifacts) motivate binding ML claims to verifiable
records ([Duddu et al., "Laminator," 2024/25](https://arxiv.org/abs/2406.17548)). Our contribution is the
*composition*: a theorem-prover-checked receipt that consumes the robustness certificate as a
hypothesis and binds it, via standard attestation, to a governance kernel.

---

## References

1. K. Xu, H. Zhang, S. Wang, Y. Wang, S. Jana, X. Lin, C.-J. Hsieh. *Fast and Complete: Enabling
   Complete Neural Network Verification with Rapid and Massively Parallel Incomplete Verifiers.* 2020.
   [arXiv:2011.13824](https://arxiv.org/abs/2011.13824).
2. S. Wang, H. Zhang, K. Xu, X. Lin, S. Jana, C.-J. Hsieh, J. Z. Kolter. *Beta-CROWN: Efficient Bound
   Propagation with Per-neuron Split Constraints for Neural Network Robustness Verification.* NeurIPS
   2021. [arXiv:2103.06624](https://arxiv.org/abs/2103.06624).
3. C. Brix, S. Bak, T. T. Johnson, H. Wu. *The Fifth International Verification of Neural Networks
   Competition (VNN-COMP 2024): Summary and Results.* 2024.
   [arXiv:2412.19985](https://arxiv.org/abs/2412.19985).
4. X. Zhou, K. Shen, A. Xu, H. Xu, C.-J. Hsieh, H. Zhang, Z. Shi. *SoundnessBench: A Soundness
   Benchmark for Neural Network Verifiers.* 2024. [arXiv:2412.03154](https://arxiv.org/abs/2412.03154).
5. A. Sirish, T. Hennen (in-toto Community). *in-toto and SLSA.* SLSA blog, 2023.
   [slsa.dev/blog/2023/05/in-toto-and-slsa](https://slsa.dev/blog/2023/05/in-toto-and-slsa).
6. *SLSA: Supply-chain Levels for Software Artifacts, v1.0 specification.*
   [slsa.dev/spec/v1.0](https://slsa.dev/spec/v1.0/).
7. Z. Newman, J. S. Meyers, S. Torres-Arias. *Sigstore: Software Signing for Everybody.* ACM CCS 2022.
   [doi:10.1145/3548606.3560596](https://doi.org/10.1145/3548606.3560596).
8. N. J. Higham. *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM, 2002.
   [doi:10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027).
9. V. Duddu, O. Järvinen, L. J. Gunn, N. Asokan. *Laminator: Verifiable ML Property Cards using
   Hardware-assisted Attestations.* 2024. [arXiv:2406.17548](https://arxiv.org/abs/2406.17548).
10. The mathlib Community. *The Lean mathematical library.* CPP 2020.
    [doi:10.1145/3372885.3373824](https://doi.org/10.1145/3372885.3373824).
11. SZL Holdings. *lutar-lean* (locked `c7c0ba17`, 749/14/163, locked-8).
    [github.com/szl-holdings/lutar-lean](https://github.com/szl-holdings/lutar-lean). Concept DOI
    [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926).

---

*Signed-off-by: Stephen P. Lutar Jr. <stephenlutar2@gmail.com>*
*Co-Authored-By: Perplexity Computer Agent <agent@perplexity.ai>*
