# Readiness Is Not Evidence: Fail-Closed Epistemic Boundaries for Governed AI Services

**Stephen P. Lutar Jr.**  
**Affiliation:** SZL Holdings LLC  
**ORCID:** [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)  
**License:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)  
Correspondence: Stephen P. Lutar Jr., SZL Holdings LLC

**Preprint status:** version 0.1.0 unreleased preprint prepared from the local A11oy Wave 17-18 engineering evidence set. This manuscript is externally distributable with its checksummed package, but it has not been submitted, accepted, peer reviewed, independently reproduced, assigned a DOI, pushed, merged, released, or deployed.

**Preprint date:** 13 July 2026

## Abstract

AI-enabled services increasingly combine retrieval, mathematical artifacts, numerical engines, model providers, quantum-development interfaces, and telemetry exporters. In such systems, a healthy process is easily mistaken for a supported answer; a configured endpoint for a reachable service; a deterministic digest for a signature; numerical agreement for proof; a simulated quantum result for hardware evidence; and an export attempt for collector delivery. These category errors are operationally consequential because they allow infrastructure facts to silently promote epistemic claims.

We present a fail-closed state model and four implemented service boundaries for preventing this promotion. The model treats service readiness, query evaluation, source availability, proof status, numerical comparison, telemetry delivery, execution authorization, and deployment as orthogonal dimensions. State transitions are monotone only when the required evidence is present. Unknown, unavailable, conflict, and not-evaluated states are preserved rather than coerced into success, and all non-proved mathematical or numerical outcomes contribute zero proof or trust uplift. The implementation is examined through four cases in an A11oy local candidate at commit f3e2c7c: (1) separation of Brain service readiness from query-level trust; (2) a proposal-only quantum utility whose rupture gate cannot authorize advantage, publication, or execution; (3) bounded external MATLAB/Octave adapters that do not bundle engines and return unavailable when isolation or engines are absent; and (4) private-by-default OpenTelemetry export with strict Trace Context parsing and an explicit distinction between propagation, exporter configuration, and collector acknowledgement. We also analyze a self-hosted model-provider boundary that avoids falsely reporting an unreachable local endpoint as live, while identifying its remaining endpoint-admission limitations.

The combined local software suite reported 400 passing tests and 6 skips. No MATLAB or Octave engine, quantum processing unit, or telemetry collector was available; therefore no engine agreement, quantum advantage, hardware measurement, or collector-delivery claim is made. The contribution is not an efficacy result. It is a reproducible architecture for making absence of evidence visible and non-promotional in governed AI services.

## Keywords

AI governance; fail-closed systems; epistemic state; evidence provenance; service readiness; selective prediction; numerical adapters; quantum benchmarking; OpenTelemetry; Trace Context; zero trust; reproducibility

## 1. Introduction

Production AI is rarely one model behind one endpoint. A contemporary service may retrieve from a graph, consult a theorem registry, call an external numerical engine, propose a quantum experiment, route requests to a local or hosted model, emit traces, and assemble a human-readable result. Each layer has its own notion of success. The graph process can be ready while its sources are stale. A query can be syntactically valid while its signal is insufficient. A theorem record can exist while its proof receipt is missing. Two solvers can return similar floating-point vectors without either result constituting a formal proof. A trace can carry a valid parent context even when no exporter is configured. An exporter can be configured even when no collector acknowledges the batch. A quantum workflow can be internally consistent while never touching quantum hardware.

The central problem is therefore not merely component failure. It is **semantic promotion across boundaries**: a lower-level operational fact is represented as a stronger epistemic or operational claim. These promotions are attractive because they make dashboards green and narratives simple. They are dangerous because the claims have different verification requirements.

Consider six common promotions:

1. process responds \(\Rightarrow\) answer is trustworthy;
2. source name is present \(\Rightarrow\) source bytes were verified;
3. digest is deterministic \(\Rightarrow\) receipt is cryptographically signed;
4. two numerical outputs match \(\Rightarrow\) formula is proved;
5. quantum circuit was simulated \(\Rightarrow\) quantum utility or advantage was measured;
6. OTLP endpoint is configured \(\Rightarrow\) telemetry reached a collector.

None of these implications is valid in general. A governed service must encode the missing premises rather than assume them.

This paper develops and evaluates a practical architecture for doing so. The architecture emerged from an operational hardening pass across the A11oy Brain, formula corpus, quantum-utility boundary, external numerical adapters, telemetry middleware, and local model-provider selection. The work is deliberately scoped. It does not establish AI accuracy, quantum advantage, formal proof of a large formula catalog, hardware deployment, or production security. It establishes that selected local code paths represent their own evidence conservatively under tested conditions.

The title “Readiness Is Not Evidence” names the most frequent category mistake. Readiness is a service property: can the service accept and process a request within its stated dependencies? Evidence is a claim property: what observations, artifacts, proofs, or acknowledgements support this particular result? The two can correlate, but neither entails the other.

Our contributions are:

- a multidimensional state model that prevents readiness, trust, proof, numerical agreement, delivery, and deployment from collapsing into one health value;
- a non-promotion invariant that assigns zero proof or trust uplift to unknown, unavailable, open, refuted, experimental, simulated, configured-only, and conflict states;
- four concrete boundary implementations for query evaluation, proposal-only quantum work, bounded external numerics, and private telemetry;
- an evidence matrix and negative-results protocol that records what was not available and what therefore was not tested;
- a local reproducibility package tied to a specific candidate commit and content hashes.

The architecture follows fail-safe defaults as articulated by Saltzer and Schroeder [1], but applies that principle to claim semantics as well as access control. It also relates to selective prediction, calibrated uncertainty, software-supply-chain provenance, zero-trust networking, and scientific reproducibility. Its distinctive focus is the interface between those areas: how a service prevents one kind of evidence from being silently reinterpreted as another.

## 2. Problem formulation

### 2.1 Claims, observations, and promotion

Let \(c\) be a claim emitted by a service and \(E(c)\) the evidence required by a declared policy. Let \(O\) be the set of observations available during a request. A claim is **admissible** only if:

\[
E(c) \subseteq O
\]

and every element of \(E(c)\) is bound to the request, artifact, and implementation version for which the claim is made. Merely observing a weaker event \(o_w\) does not permit a stronger claim \(c_s\) unless policy declares and validates an implication \(o_w \models E(c_s)\).

We call the unauthorized mapping

\[
o_w \longmapsto c_s
\]

an epistemic promotion. Promotion may be explicit, as when a response says “verified,” or implicit, as when a dashboard presents a configured exporter under a green “telemetry healthy” badge. The latter is especially difficult to detect because the underlying field may be technically true while the visual or narrative interpretation is stronger.

### 2.2 Orthogonal dimensions

A single scalar health score is insufficient for the systems studied here. We represent a request or artifact by a state vector:

\[
\mathbf{s} =
(r,q,a,p,n,t,x,d)
\]

where:

- \(r\): service readiness;
- \(q\): query assessment;
- \(a\): source or engine availability;
- \(p\): proof status;
- \(n\): numerical comparison status;
- \(t\): telemetry state;
- \(x\): execution or publication authorization;
- \(d\): deployment state.

Each coordinate has its own transition rules and evidence. Readiness can become READY while query assessment remains NOT-EVALUATED. Numerical comparison can become MATCH while proof remains UNKNOWN. Telemetry propagation can be READY while delivery remains UNKNOWN. A local test candidate can be validated while deployment remains NOT-CLAIMED.

The architecture refuses to project \(\mathbf{s}\) into a stronger scalar such as “verified” without an explicit, reviewable mapping. User interfaces may summarize, but they must retain the coordinates and the blocking evidence.

### 2.3 Fail-closed does not mean always reject

Fail-closed is sometimes interpreted as refusing all work when any dependency is absent. That is too coarse for AI services. The desired behavior is:

- continue operations that remain valid under the available evidence;
- identify the unavailable boundary;
- reduce the claim strength to the highest supported state;
- deny effects whose authorization requires missing evidence;
- preserve an auditable reason.

For example, the Brain can remain service-ready and return a structured NOT-EVALUATED response to a blank query. The quantum utility can prepare a deterministic proposal without authorizing execution. The numerical adapter can validate a request and return UNAVAILABLE without launching a subprocess. Telemetry middleware can propagate a valid trace context without claiming export delivery. These are useful outcomes, not failures disguised as success.

### 2.4 Research questions

We ask:

**RQ1.** Can a shared state model prevent operational readiness from being promoted into query trust, proof, measurement, delivery, or deployment?

**RQ2.** Can boundary implementations preserve useful proposal, validation, and propagation behavior while returning explicit negative or unavailable states?

**RQ3.** Can deterministic receipts support replay and tamper detection without being mislabeled as signatures, proofs, hardware measurements, or deployment attestations?

**RQ4.** What remains untested when external engines, QPUs, and collectors are absent, and can the system surface those absences without inflating claims?

## 3. Evidence-state model

### 3.1 State domains

The implemented model uses small, explicit vocabularies rather than free-form confidence labels.

**Service readiness**

\[
R = \{\text{READY},\text{DEGRADED}\}
\]

Readiness reports whether required local modules and indexes for the endpoint are usable. It does not report freshness, grounding, proof, or query quality.

**Query assessment**

\[
Q = \{\text{EVALUATED},\text{NOT-EVALUATED}\}
\]

An empty or semantically insufficient request is not assigned a synthetic low trust score. It remains NOT-EVALUATED with verdict INSUFFICIENT-SIGNAL and modeled trust equal to null.

**Availability**

\[
A = \{\text{AVAILABLE},\text{SOURCE-UNAVAILABLE},\text{ENGINE-UNAVAILABLE},\text{UNKNOWN}\}
\]

Availability is attached to a named source, executable, license configuration, collector, or provider. One available source cannot stand in for another. A snapshot is not the canonical service unless policy explicitly establishes equivalence.

**Proof status**

\[
P = \{\text{PROVED},\text{OPEN},\text{REFUTED},\text{EXPERIMENTAL},\text{UNKNOWN}\}
\]

PROVED is evidence-intensive. It requires verified artifact bytes, an exact artifact digest, no sorry or admit placeholders, a verified kernel receipt, and receipts pinned to exact Lean and mathlib commits. The other four states confer zero proof credit.

**Numerical comparison**

\[
N = \{\text{MATCH},\text{CONFLICT},\text{UNAVAILABLE},\text{NOT-RUN},\text{UNKNOWN}\}
\]

MATCH means that declared numerical results agree under a declared tolerance for a declared operation and request. It does not imply formal proof, mathematical truth outside the tested input, or superiority of either engine.

**Telemetry**

\[
T = T_p \times T_e \times T_c
\]

where \(T_p\) is propagation validity, \(T_e\) is exporter configuration or attempt, and \(T_c\) is collector acknowledgement. A valid W3C traceparent establishes only \(T_p\). A configured private endpoint may establish an export attempt state in \(T_e\). Delivery requires evidence in \(T_c\), which was not available in this evaluation.

**Authorization**

\[
X = \{\text{DENIED},\text{HUMAN-REVIEW-ELIGIBLE},\text{AUTHORIZED}\}
\]

The quantum boundary can mark a proposal eligible for human review but cannot independently authorize execution, publication, or an advantage claim.

**Deployment**

\[
D = \{\text{LOCAL-CANDIDATE},\text{PUSHED},\text{MERGED},\text{DEPLOYED},\text{UNKNOWN}\}
\]

This study reports LOCAL-CANDIDATE only. Pushed, merged, and deployed require separate external observations.

### 3.2 The non-promotion invariant

For every response, let \(u_p\) denote proof uplift and \(u_t\) trust uplift. The core invariant is:

\[
p \neq \text{PROVED} \Rightarrow u_p = 0
\]

\[
a \in
\{\text{SOURCE-UNAVAILABLE},\text{ENGINE-UNAVAILABLE},\text{UNKNOWN}\}
\Rightarrow u_p = u_t = 0
\]

\[
n \in
\{\text{MATCH},\text{CONFLICT},\text{UNAVAILABLE},\text{NOT-RUN},\text{UNKNOWN}\}
\Rightarrow u_p = 0
\]

Numerical MATCH may inform an engineering comparison, but it never raises proof status. CONFLICT is preserved and cannot be averaged away. A configured-only telemetry state never raises delivery. A simulated quantum observation never raises a hardware-measurement coordinate.

The invariant is enforced both structurally and narratively. Responses contain explicit booleans such as quantum_advantage_verified=false and claim_authorized=false. Receipts identify themselves as unsigned deterministic digests. The manuscript adopts the same rule: it reports only claims for which the evaluation contains the required evidence.

### 3.3 Evidence binding

Evidence that is not bound to its subject is weak. The system binds receipts to:

- canonicalized request content;
- artifact bytes or an exact SHA-256 digest;
- operation name and declared tolerance;
- implementation and dependency commits when relevant;
- timestamp or local sequencing metadata;
- status vocabulary and policy version.

For formal proof, the binding additionally includes exact Lean and mathlib commits and a kernel-verification result. For traces, the accepted parent context determines the server span relationship. For external numerics, the response is checked against a strict schema and the request digest. For quantum proposals, the receipt binds the baseline search parameters and planning output but contains no hardware measurement.

Binding is necessary but not sufficient. A SHA-256 digest can detect content change when recomputed; it cannot authenticate an author without a signing key and verification procedure. A deterministic receipt is therefore labeled UNSIGNED_DETERMINISTIC_DIGEST_ONLY. This distinction follows the motivation for signed supply-chain envelopes such as DSSE and in-toto [2,3], while declining to claim those stronger properties where they were not implemented.

### 3.4 State transitions

Transitions occur only through named evidence gates.

For Brain queries:

\[
\text{NOT-EVALUATED}
\xrightarrow{\text{nonblank admissible query}}
\text{EVALUATED}
\]

and only an evaluated query may receive modeled trust. Service readiness does not participate in this transition.

For formula artifacts:

\[
\text{UNKNOWN or OPEN}
\xrightarrow{\substack{\text{exact bytes and digest}\\
\text{zero sorry/admit}\\
\text{verified kernel receipt}\\
\text{pinned commits}}}
\text{PROVED}
\]

If evidence conflicts, the artifact is quarantined or downgraded to UNKNOWN rather than promoted.

For numerics:

\[
\text{NOT-RUN}
\xrightarrow{\text{engine available and isolation established}}
\text{engine result}
\]

\[
\text{two valid bound results}
\xrightarrow{\|y_1-y_2\|\leq\tau}
\text{MATCH}
\]

or otherwise CONFLICT. Neither branch changes \(P\).

For telemetry:

\[
\text{valid traceparent}
\Rightarrow \text{PROPAGATION-READY}
\]

\[
\text{admitted private endpoint}
\Rightarrow \text{EXPORT-CONFIGURED}
\]

\[
\text{collector acknowledgement}
\Rightarrow \text{DELIVERY-OBSERVED}
\]

The third transition did not occur in this study.

### 3.5 Why a lattice rather than a ladder

These states form a product lattice, not a maturity ladder. “Ready” is not below “proved,” and “match” is not below “deployed.” They refer to different propositions. A total order would invite promotion because every event would appear to move the artifact upward. In the product representation, a system can improve one coordinate while another remains unchanged or becomes less certain.

This approach resembles multi-valued logics that preserve inconsistency and unknown information rather than forcing binary truth. We do not claim a new logic. We use the practical lesson: UNKNOWN and CONFLICT are meaningful values that must survive serialization, aggregation, and user-interface rendering.

## 4. System architecture

### 4.1 Boundary-oriented design

The candidate organizes governance around boundaries at which claim types change:

1. **request to assessment:** a query becomes eligible for evaluation;
2. **artifact to proof:** files and receipts become eligible for PROVED;
3. **proposal to execution:** a modeled plan becomes eligible for human review but not action;
4. **request to external process:** a strict numerical operation becomes eligible for an isolated adapter;
5. **context to telemetry:** a parent trace becomes eligible for propagation and possibly export;
6. **configured provider to serving path:** an endpoint becomes eligible to be reported as the selected provider only if the actual routing path uses it.

Each boundary has an admission function, an output vocabulary, and a forbidden promotion.

| Boundary | Admission evidence | Permitted output | Forbidden promotion |
|---|---|---|---|
| Brain query | nonblank admissible query, local index | evaluated verdict or not-evaluated state | readiness to trust |
| Formula corpus | exact bytes, digest, kernel receipt, pinned commits | PROVED or preserved weaker class | record presence to proof |
| Quantum utility | bounded validated request | proposal and review eligibility | simulation to QPU/advantage |
| Numerics adapter | strict operation, bounded data, isolation, engine | result, match, conflict, unavailable | agreement to proof |
| OTel | valid traceparent and admitted endpoint | propagation/export state | configuration to delivery |
| Model provider | actual selected reachable base or credentialed fallback | provider label matching route | configured URL to live local service |

### 4.2 Local candidate and repository context

The evaluated code is the combined local candidate f3e2c7c in branch codex/a11oy-frontier-wave18. Its immediate history incorporates Brain/query separation, bounded quantum request handling, proposal-only quantum utility, formula-corpus admission, external numerical adapters, private telemetry hardening, and runtime-state quarantine. The head commit itself primarily quarantines sandbox test state; it is used as the combined evidence anchor rather than as a claim that every feature originated in that commit.

No remote push, pull request merge, release, deployment, or external service rollout was performed as part of this study. The distinction is important: a clean local candidate and passing suite are not deployment observations.

### 4.3 Receipt philosophy

Receipts are designed to answer “what content and state did this local operation produce?” They include deterministic hashes to support replay and change detection. They do not answer “who signed this?”, “which hardware ran it?”, “did a remote party receive it?”, or “is the underlying scientific claim true?” unless those facts have their own evidence fields and validators.

This narrow philosophy avoids the common use of “attestation” as an all-purpose prestige word. Some project files retain the term in filenames, but the receipt payload and this paper distinguish:

- deterministic digest;
- cryptographic signature;
- formal proof receipt;
- hardware measurement;
- collector acknowledgement;
- deployment attestation.

Only the first and, for specifically admitted Lean artifacts, a constrained form of the third are represented in the present evidence set.

## 5. Case study I: Brain readiness and query trust

### 5.1 Failure mode

An AI command center often exposes a health endpoint and a query endpoint. If both use a single “trust” field, a reachable index can make a blank or unsupported query appear weakly trustworthy rather than unevaluated. Conversely, an insufficient query can make the entire service appear unhealthy. Both are category errors.

The Brain hardening separates:

- whether modules and indexes needed by the service are available;
- whether this request contains enough signal to evaluate;
- whether available sources support the returned content;
- whether contradictions and uncertainty remain.

### 5.2 Readiness state

Service readiness is READY or DEGRADED. Probes inspect local module and index availability. They do not infer epistemic quality from process liveness. Readiness can therefore be READY while a query response is NOT-EVALUATED or UNTRUSTWORTHY.

This is analogous to the distinction between a web server’s readiness probe and the truth of a document it serves. Operational orchestration needs the former. Users and governance need the latter. Combining them makes both less useful.

### 5.3 Query assessment

The query path first tests whether the request is admissible for evaluation. A blank query returns:

- assessment: NOT-EVALUATED;
- verdict: INSUFFICIENT-SIGNAL;
- modeled_trust: null.

The null value is intentional. Assigning zero would imply that an evaluation occurred and found the answer maximally untrustworthy. Assigning a default midpoint would be worse because it would fabricate information. NOT-EVALUATED is a different proposition.

For evaluated queries, modeled trust composes grounding, freshness, provenance, contradiction, and uncertainty signals. It is capped below certainty at 0.97. The cap is not a calibrated probability claim. It prevents the presentation layer from equating a modeled score with absolute certainty. Calibration of model confidence is a separate empirical problem, as demonstrated in neural-network calibration work [4].

### 5.4 Corpus admission

The corpus bridge uses schema szl.brain.corpus-evidence.v1 and recognizes PROVED, OPEN, REFUTED, EXPERIMENTAL, and UNKNOWN. A formula does not become PROVED because it appears in a repository or registry. Admission requires:

1. verified artifact bytes;
2. an exact artifact SHA;
3. no sorry or admit placeholders;
4. a valid proof receipt;
5. a verified kernel result;
6. exact Lean and mathlib commit pins;
7. a receipt digest bound to those facts.

Weak or conflicting evidence produces UNKNOWN or quarantine. Non-PROVED artifacts contribute zero proof and trust uplift. The evaluated local inventory contained 35 OPEN, 13 EXPERIMENTAL, 1 UNKNOWN, and 0 artifacts eligible for PROVED. The canonical Lake source was unavailable; a Hugging Face snapshot was not treated as the canonical Lake service. This is a negative result and a design success: the system did not manufacture proof credit from local naming or partial mirrors.

### 5.5 Refresh and receipt behavior

The local refresh route is loopback-only, nonconcurrent, cooldown-bounded, network-free, and restricted to committed local sources. It does not alter source freshness and does not mint a receipt for a failed reindex. GET endpoints mint no receipts. POST operations that produce a receipt use an unsigned content digest.

This reduces two risks. First, read-only inspection does not create audit artifacts that look like executed work. Second, a failed mutation does not leave behind a success-shaped receipt. The design is consistent with fail-safe defaults [1] and with the broader principle that provenance should describe the actual transformation [3].

### 5.6 Interpretation

The Brain result is not that the graph is trustworthy. It is that service readiness and query evidence are represented separately, blank queries remain not evaluated, missing canonical sources remain unavailable, and unsupported proof claims receive zero uplift. These properties are necessary for trustworthy use, but they do not establish factual accuracy across arbitrary queries.

## 6. Case study II: proposal-only quantum utility

### 6.1 Why quantum boundaries need unusually strict language

Quantum-development interfaces are vulnerable to semantic promotion because the same vocabulary is used for simulation, circuit preparation, hardware execution, benchmarking, and advantage claims. A circuit can be valid without being executable on a particular device. A simulator result can be reproducible without being a hardware measurement. A hardware measurement can be real without showing an advantage over the best classical method.

Primary literature treats benchmarking as a defined experimental procedure, not a decorative metric. Quantum volume, for example, connects performance to randomized model-circuit success under specified conditions [5]. Variational approaches also face trainability hazards such as barren plateaus [6]. These results support a conservative boundary: proposal tooling should not authorize scientific or performance claims.

### 6.2 Implemented scope

The quantum utility is proposal-only. It contains:

- zero effectors;
- zero provider calls;
- zero QPU calls;
- a bounded exact QUBO baseline for at most 16 variables and 65,536 states;
- declared Hamiltonian shot planning;
- strict request validation;
- deterministic unsigned receipts;
- a rupture gate that may mark material eligible for human review but cannot authorize execution or publication.

The exact baseline is deliberately small. An exhaustive \(2^n\) search grows exponentially, so the service binds \(n\leq16\) and a maximum state count. This is a software-safety limit, not a claim that the baseline is competitive for larger scientific problems.

### 6.3 Request admission and resource bounds

Requests are schema-validated, hidden fields are rejected, and request bodies are capped at 256 KiB both by declared length and streaming enforcement. Oversized bodies receive HTTP 413. Bounds cover variables, states, time, and structured values. This prevents a proposal endpoint from becoming an unbounded compute or parsing surface.

The body limit is important even for local services. A Content-Length check alone is insufficient when clients stream without an accurate header. Streaming enforcement binds the consumed body rather than trusting the declaration.

### 6.4 Rupture gate

The rupture gate evaluates whether the proposal contains the declared observations and structure needed for human review. Even when it returns SUPPORTED or review-eligible, the following remain false:

- quantum_advantage_verified;
- claim_authorized;
- publication_authorized;
- execution_authorized.

This is not an arbitrary downgrade. Each stronger claim requires evidence that the utility does not possess. Quantum advantage requires an appropriate comparison against strong classical methods under a defensible benchmark, not merely a favorable internal score. Hardware execution requires a provider call and returned job evidence. Publication authorization is an organizational decision. The utility has none of these authorities.

### 6.5 VQC and Hamiltonian outputs

Variational quantum circuit outputs remain MODELED or SIMULATED. Hamiltonian shot plans are DECLARED planning values, not empirically optimal shot allocations. The service may record repeated modeled observations, but repeated simulation does not cross the hardware-measurement boundary.

This aligns with the caution implied by quantum trainability research [6,7]. A neat optimization trace does not establish scalable trainability, and a local objective improvement does not establish practical quantum utility. The architecture therefore records the computational substrate explicitly.

### 6.6 Interpretation

No QPU was available in the evaluated environment. No provider was called. No hardware samples were collected. The result is not a quantum-performance experiment. It is evidence that the proposal boundary is bounded and that its strongest success-shaped path still cannot authorize a quantum-advantage, execution, or publication claim.

## 7. Case study III: external MATLAB/Octave numerical adapter

### 7.1 Boundary objective

Scientific and engineering systems often need independent numerical checks. Calling MATLAB or GNU Octave can be useful, but embedding arbitrary user expressions or shell commands would create a powerful execution surface. Bundling a proprietary engine may violate licensing assumptions, while incorporating a GPL program into the service process can create avoidable distribution and coupling questions. The architecture therefore treats both engines as external processes behind a fixed contract.

The adapter does not copy or bundle either engine. It installs no packages, downloads no models, performs no network calls, and accepts no arbitrary code.

### 7.2 Fixed operation set

The contract exposes three operations:

- MATRIX_SOLVE;
- SYMMETRIC_EIGENVALUES;
- VALIDATE_REFERENCE_VECTOR.

The JSON schema rejects additional properties. Matrices and vectors are limited to dimension 64, numeric magnitude is bounded by \(10^{12}\), and tolerance is constrained to \([0,1]\). Fields commonly used to smuggle execution—code, expression, function, command, path, package, and URL—are prohibited.

This design follows the principle of least common mechanism and economy of mechanism [1]. The external process receives data for a known operation, not a language fragment.

### 7.3 Process isolation

A subprocess is eligible only when the host can establish the declared POSIX network namespace isolation and resource limits. The launch uses shell=false, a temporary directory, timeouts, CPU and memory limits, output caps, and a fixed adapter program. Package installation and network use are disabled. If isolation is unavailable, the adapter returns UNAVAILABLE rather than launching with weaker controls.

The Octave path uses a fixed octave_adapter.m file. The MATLAB path similarly relies on fixed operation dispatch. Engine output is parsed through a strict response schema and bound to the request.

This is defense in depth, not a sandbox proof. Kernel vulnerabilities, interpreter vulnerabilities, filesystem behavior, and platform differences remain possible. The implementation’s claim is narrower: under its policy, absence of required isolation closes the execution path.

### 7.4 Numerical meaning

For a linear system \(Ax=b\), a small residual

\[
\|b-A\hat{x}\|
\]

does not alone establish that \(\hat{x}\) is accurate when \(A\) is ill-conditioned. MATLAB’s official mldivide documentation explicitly warns that nearly singular or badly scaled systems can produce unreliable solutions even with small residuals [8]. Numerical analysis distinguishes forward error, backward error, and conditioning [9]. Therefore, a cross-engine match is an engineering observation under a tolerance, not a proof of the mathematical proposition or a universal accuracy guarantee.

The comparison function returns MATCH when both valid, request-bound outputs differ within the declared tolerance; otherwise it returns CONFLICT. Both contribute zero proof uplift. CONFLICT is not resolved by selecting the output closer to an expected narrative.

### 7.5 Availability result

Local preflight found:

- Octave executable: SOURCE_UNAVAILABLE;
- MATLAB executable: SOURCE_UNAVAILABLE;
- MATLAB license configuration: SOURCE_UNAVAILABLE.

Consequently, no engine computation occurred and no MATLAB/Octave agreement was measured. This is a central negative result. The adapter tests validate contract, rejection, and unavailable behavior; they do not validate real engine integration or numerical agreement.

### 7.6 Licensing and process separation

MATLAB is proprietary and licensed by MathWorks. GNU Octave is distributed under the GNU GPL. This paper does not provide a legal conclusion about every deployment model. Process separation and non-bundling are engineering choices that reduce coupling and make operator responsibilities explicit. Deployers remain responsible for licenses, distribution, platform policy, and legal review.

### 7.7 Interpretation

The numerical boundary demonstrates that a system can be operationally useful even when engines are absent: it can validate requests, reject unsafe fields, explain unavailable prerequisites, and preserve zero uplift. It does not demonstrate real MATLAB or Octave execution.

## 8. Case study IV: private OpenTelemetry boundary

### 8.1 Three different telemetry claims

Telemetry is a frequent source of accidental promotion because libraries compress several events into one “enabled” flag. This study separates:

1. **propagation readiness:** the service can parse or create valid trace context;
2. **export configuration:** an admitted OTLP endpoint is configured and an exporter may attempt transmission;
3. **delivery evidence:** a collector or durable downstream system acknowledges a particular batch or span.

A trace ID printed in a response does not prove export. An initialized exporter does not prove the collector accepted data. Even a successful socket write may not prove durable ingestion. The OpenTelemetry Protocol defines transport and retry behavior, but delivery semantics still depend on the receiving system and available acknowledgement [10,11].

### 8.2 Trace Context validation

The middleware implements strict lowercase W3C Trace Context version 00 parsing [12]. It accepts only the declared structure, requires nonzero trace and parent identifiers, and permits trace flags 00 or 01. Malformed, all-zero, unsupported, or incorrectly cased inputs do not govern the exported server span.

When a valid parent context is accepted, it governs the server span relationship. When no valid parent exists, the service may create a new local context. This is a propagation statement, not an authentication statement: Trace Context identifiers correlate work but do not establish the caller’s identity or the truth of attached metadata.

GET status requests mint no receipt. This avoids a read operation creating success-shaped provenance. The status response distinguishes propagation readiness from exporter state.

### 8.3 Endpoint admission

The OTLP endpoint policy admits:

- loopback IP addresses;
- private IP addresses;
- exact operator-allowlisted DNS names.

It rejects:

- credentials embedded in a URL;
- public, unspecified, multicast, reserved, or link-local IP addresses;
- unsafe schemes;
- non-root paths;
- query components;
- fragments.

The policy is intentionally stricter than generic URI validity. RFC 3986 defines syntax [13]; it does not make a destination safe. NIST Zero Trust Architecture also cautions against implicit trust based solely on network location [14]. Our private-address rule reduces accidental public egress but is not identity-based authorization and is not claimed as full zero trust.

Allowlisted DNS is matched exactly. Endpoint status is redacted and represented by a 16-hex-character SHA-256 fingerprint rather than echoing a potentially sensitive URL. The fingerprint supports stable comparison but is neither a secret nor a signature.

### 8.4 No collector evidence

No collector was available during the bounded evaluation. Accordingly:

- propagation parsing was tested;
- endpoint admission and rejection were tested;
- configuration state was represented;
- no collector delivery was observed;
- no end-to-end telemetry durability claim is made.

The evaluation’s four focused telemetry security and honesty checks passed. Those checks are software assertions over parsing, admission, redaction, and status semantics. They cannot stand in for collector acknowledgement, packet capture, or durable backend query.

### 8.5 Residual network risks

Private-by-default admission is not a complete server-side request forgery defense. DNS rebinding, resolver differences, proxy configuration, IPv4/IPv6 translation, container network topology, and an allowlisted but compromised collector can alter the effective destination. A production design should resolve and pin addresses under policy, authenticate the collector, protect transport, constrain egress at the operating-system or network layer, and verify delivery independently.

The present implementation’s value is representational honesty: the response cannot equate propagation or configuration with delivery. It is not evidence that all possible egress paths are safe.

## 9. Self-hosted provider fail-closed routing

### 9.1 Configuration intent is not serving evidence

The model orchestrator accepts local-provider configuration through A11OY_BRAIN_URL or A11OY_MODEL_BASE_URL. Earlier service patterns often labeled any configured local URL as “local provider,” even when the process was absent. That makes observability contradict reality.

The current selection path probes a candidate local endpoint with a short timeout, using the models route or root. A local label is selected only when the actual serving base is non-Hugging-Face-router and reachable. If a configured local service is unreachable, the orchestrator can use the hosted router only when appropriate credentials are present. Without credentials, it returns a clearly labeled deterministic stub rather than fabricating a model answer or claiming a live provider.

Provider reporting is derived from the selected serving base, not from the mere presence of an environment variable. This eliminates one narrow false-live state:

\[
\text{configured local URL} \land \neg\text{reachable}
\not\Rightarrow \text{local provider live}
\]

### 9.2 What reachability does not prove

A successful HTTP probe does not prove:

- model identity or version;
- model weights or license;
- GPU use;
- response quality;
- endpoint authorization;
- absence of an SSRF path;
- that a later inference request will succeed.

The current local-provider admission is older and less restrictive than the OTLP endpoint policy. It does not yet provide a dedicated allowlist, IP-class validation, DNS-resolution pinning, or model-identity attestation. The local-reachable path was not exercised without a live server in this bounded evaluation. These are material limitations, not implementation footnotes.

The fail-closed achievement is therefore limited to labeling and fallback: an unreachable local configuration is not reported as the active live path, and absence of both local service and hosted credentials produces an explicit stub. A future version should reuse a common endpoint-admission policy and bind model identity to a signed or independently verifiable manifest.

## 10. Evaluation method

### 10.1 Study design

We conducted a local software-evidence study of the combined Wave 17–18 candidate. The unit of evaluation was not model accuracy or scientific performance; it was whether boundary code and response schemas preserve declared evidence states under positive, negative, malformed, and unavailable conditions.

The authoritative combined result at f3e2c7c is:

- 400 tests passed;
- 6 tests skipped.

Skipped tests are not counted as evidence of passing behavior. Component receipts also report focused subsets and earlier regression totals. Those counts overlap and are not summed. The combined 400/6 result is the only aggregate test count used in conclusions.

A later, separate validation at `29c5d763506937a7ceb8c2938327365f8e0ff924` added the Formal Conjecture Lab and reported 410 passed, 6 skipped, and 0 failed across 25 selected files. That run postdates the implementation and evidence anchor studied here. It is included as non-promoting follow-up evidence and does not replace, enlarge, or retroactively re-anchor the Paper 2 result of 400 passed and 6 skipped at `f3e2c7c9fdd32d95bfe7b990e2ba35700f8af935`.

### 10.2 Candidate history

The combined candidate incorporates the following local history:

| Commit | Purpose |
|---|---|
| f3e2c7c | quarantine sandbox test state; combined evidence anchor |
| 6429cb8 | harden private trace export |
| 552c7b5 | add fail-closed external numerics adapters |
| 2af3fff | add bounded Brain corpus-admission bridge |
| 33161eb | quarantine local runtime state |
| 6e76c3d | separate Brain readiness from query trust |
| 760c289 | bind quantum execution claims to evidence |
| 2fc3526 | enforce quantum streaming request bound |
| 1f5e985 | add proposal-only quantum utility |
| 0e3e394 | make Brain graph command center dominant |

This history describes local commits. It does not establish that they were pushed, reviewed, merged, released, or deployed.

### 10.3 Test classes

The suite covers five classes.

**Contract tests** check strict schemas, allowed operations, forbidden fields, dimensions, magnitude limits, tolerance, and response vocabularies.

**Negative-path tests** send blank queries, malformed traceparents, oversized quantum requests, unsafe endpoints, missing engines, missing canonical sources, and conflicting or incomplete proof evidence.

**Non-promotion tests** assert that weaker states cannot raise stronger coordinates. Examples include modeled quantum outputs leaving advantage false, numerical MATCH leaving proof uplift zero, and exporter configuration leaving collector delivery unknown.

**Determinism tests** verify stable receipt content and digests for equivalent inputs. They do not test signatures because no signatures are present.

**Regression tests** ensure boundary hardening does not break selected existing local behavior. They do not establish absence of all regressions outside the selected suite.

### 10.4 Environment absences

Three external substrates were absent:

- no MATLAB or GNU Octave engine and no MATLAB license configuration;
- no quantum processing unit or provider call;
- no OpenTelemetry collector.

The canonical Lake service was also unavailable, and the local Hugging Face snapshot was not substituted as canonical. These absences determine the maximum claim strength of the evaluation.

### 10.5 Measures

We report:

- test result counts;
- state-transition outcomes;
- whether prohibited promotions occurred in tested paths;
- content hashes for evidence artifacts;
- available and unavailable external substrates;
- negative results and unresolved limitations.

We do not report latency, throughput, predictive accuracy, calibration error, numerical accuracy on real engines, quantum benchmark performance, or telemetry delivery rate because those experiments were not conducted.

## 11. Results

### 11.1 Aggregate software result

The selected local suite completed with 400 passes and 6 skips. Within the tested paths, the combined candidate represented the following boundaries as intended:

- blank Brain queries remained NOT-EVALUATED with null modeled trust;
- service readiness remained independent from query verdict;
- unavailable canonical corpus sources remained SOURCE_UNAVAILABLE;
- OPEN, REFUTED, EXPERIMENTAL, and UNKNOWN mathematical classes provided zero proof uplift;
- quantum proposal output never authorized advantage, execution, or publication;
- oversized streamed quantum bodies produced HTTP 413;
- unsafe or unavailable numerical execution paths returned unavailable rather than launching with weakened isolation;
- numerical comparison status provided zero proof uplift;
- malformed trace context and unsafe OTLP endpoints were rejected;
- propagation and exporter configuration remained distinct from collector delivery;
- an unreachable local model endpoint was not labeled as the active local serving path.

### 11.2 Evidence matrix

| Property | Local evidence | Result | Stronger claim not made |
|---|---|---|---|
| Brain process readiness | module/index probes | represented independently | answer factuality |
| Blank query handling | response-state test | NOT-EVALUATED, null trust | low-confidence evaluation |
| Formula proof admission | strict receipt and commit checks | 0 eligible PROVED | 49 formulas proved |
| Quantum utility | bounded proposal tests | proposal-only behavior | QPU run or advantage |
| Numerics contract | schema/isolation/unavailable tests | fail-closed boundary | MATLAB/Octave result |
| Numerical comparison | policy tests | MATCH/CONFLICT zero uplift | formal proof |
| Trace propagation | W3C parser tests | valid parent handling | caller authentication |
| OTLP endpoint policy | admission/redaction tests | private/allowlisted only | collector delivery |
| Local provider selection | unreachable/fallback self-test | honest route label | model identity |
| Combined candidate | selected local suite | 400 pass, 6 skip | deployment readiness |

### 11.3 Receipt results

The corpus bridge receipt's internal digest is:

70208a7464e54d1f794ae4fa572c68580fd1df4d2bd89a18e769538b3677fba8

The numerical adapter receipt hash is:

56d962cc2af9735544cfe22790b83e6241fccac497b7cc7922a3bfa8b33fc31b

The telemetry receipt hash is:

8ef6701924caf2f04885d56445dc0b9b2e27336dd2a1fc5e9a8cf03dd700ff0e

The Lake/mathlib/Octave contract hash is:

589a466436558ad3ca5f58d9a6abd9c2f7f0d522da6df7e7753cd3ba4e806583

These are content digests reported by local evidence artifacts. They are not signatures and do not authenticate an author or machine.

## 12. Negative results

Negative results are first-class outputs in this study because the architecture is specifically intended to preserve them.

### 12.1 No proved formula catalog

The local formula classification contained 35 OPEN, 13 EXPERIMENTAL, 1 UNKNOWN, and 0 eligible PROVED. Claims that all formulas, 180 formulas, 200 formulas, or a similarly large catalog were proved are unsupported by this evidence set. A repository count, theorem-name count, or generated document count cannot replace the kernel-bound receipt requirements.

### 12.2 No canonical Lake evidence

The canonical Lake source was unavailable. A Hugging Face snapshot existed but was not treated as equivalent. The result is SOURCE_UNAVAILABLE, not “available by mirror.” This means query support and corpus completeness relying on canonical Lake evidence remain unresolved.

### 12.3 No numerical engine result

No MATLAB or Octave executable was found, and MATLAB license configuration was unavailable. No matrix solve or eigenvalue request reached a real engine. No cross-engine agreement or disagreement was observed. Contract tests cannot be promoted into scientific validation.

### 12.4 No quantum hardware or advantage

No provider was called and no QPU was available. All VQC and Hamiltonian material remained modeled, simulated, or declared. The candidate provides no evidence of hardware execution, error mitigation, quantum utility, or advantage over classical methods.

### 12.5 No telemetry delivery

No collector participated. Valid trace propagation and endpoint configuration do not demonstrate receipt, indexing, durability, or queryability in a backend.

### 12.6 No deployment

The candidate was local. No remote push, merge, deployment, domain update, or production observation is included in the study. “Operational” in this manuscript refers only to tested local code paths and must not be read as production deployment.

### 12.7 Unavailable build checks

The numerical evidence receipt records that a Docker build was unavailable because the sandbox denied the required operation. Copy-synchronization analysis identified 44 pre-existing baseline violations and zero violations introduced by the numerical scope. The inability to perform the Docker build is a limitation; zero newly introduced copy violations does not establish a globally clean repository.

## 13. Security and threat model

### 13.1 Assets

The protected assets include:

- correctness of claim labels and status coordinates;
- local source and proof artifact integrity;
- model-provider credentials;
- filesystem and process isolation;
- network egress policy;
- trace context integrity as correlation metadata;
- operator review authority;
- availability of bounded service resources.

### 13.2 Adversary capabilities

We consider an external client able to submit crafted JSON, streamed bodies, malformed headers, large numeric values, hidden fields, unsafe URLs, and queries designed to trigger ambiguous states. We also consider a misconfigured operator who provides an unreachable endpoint, a stale snapshot, or incomplete proof metadata.

We do not assume protection against a fully compromised host kernel, malicious repository administrator, compromised dependency, stolen signing key, or hostile external engine binary. No signing key is used here. Those threats require controls beyond the evaluated boundary.

### 13.3 Claim-confusion attacks

A claim-confusion attack tries to make one state serialize or render as another. Examples include:

- omitting assessment so NOT-EVALUATED appears as evaluated;
- using “verified” for a deterministic digest;
- using “connected” for a configured endpoint;
- using “measured” for simulator output;
- using “proved” for numerical agreement;
- using “local provider” for an environment variable whose target is down.

The defense is typed state, required fields, negative assertions, and presentation-layer fidelity. If a frontend discards the coordinates and renders one green icon, the backend protection is weakened. Boundary correctness must therefore extend through the user interface.

### 13.4 Resource-exhaustion threats

The quantum route enforces a 256 KiB streaming body cap and bounded exact search. The numerics contract limits matrix dimension, value magnitude, output, CPU, memory, and time. Brain refresh is nonconcurrent and cooldown-bounded. These controls reduce denial-of-service exposure but do not constitute a full capacity plan or distributed rate-limiting system.

### 13.5 External-process threats

An external numerical interpreter is a high-risk dependency. The fixed operation contract, shell=false, temporary directories, resource limits, no package installation, and required network isolation reduce the input surface. Returning UNAVAILABLE when isolation is absent is the fail-closed decision.

The residual risk includes interpreter vulnerabilities, kernel escape, inherited descriptors, filesystem races, environment leakage, and platform-specific behavior. Stronger isolation could use a dedicated container or microVM with a minimal filesystem, read-only input mount, seccomp profile, separate user, explicit environment allowlist, and egress-deny network policy. Such isolation must itself be measured rather than inferred from configuration.

### 13.6 Endpoint and SSRF threats

The OTLP policy restricts scheme, address class, URL structure, and allowlisted DNS. It rejects credentials and public or special-use addresses. The self-hosted model path does not yet apply the same controls. A future unification should:

1. parse and canonicalize with one policy module;
2. resolve DNS under policy;
3. reject address-class changes;
4. pin the resolved destination for the connection;
5. prohibit proxy inheritance unless explicitly configured;
6. authenticate the peer;
7. enforce host-level egress policy.

NIST Zero Trust guidance emphasizes that network location alone must not confer trust [14]. Private IP admission is thus only an egress constraint, not a trust grant.

### 13.7 Provenance threats

Unsigned digests are vulnerable to substitution by an attacker who can replace both artifact and receipt. They support change detection only when the expected digest arrives through a trusted channel. Stronger provenance should use DSSE or an equivalent signing envelope, protected keys, identity policy, transparency logging where appropriate, and verification integrated into admission [2,3,15].

Even signed provenance would not prove a scientific claim. It would authenticate who asserted what about which bytes. Formal proof still requires kernel verification; hardware measurement still requires device-bound evidence; delivery still requires collector evidence.

### 13.8 Human review

Human-in-the-loop is not automatically safe. Reviewers can be rushed, misled by green status, or lack domain expertise. The quantum utility’s HUMAN-REVIEW-ELIGIBLE state is therefore not an authorization. Review workflows should display negative evidence, substrate, artifact hashes, conflicts, and missing observations; require role-based approval; and record the decision separately from the proposal receipt.

## 14. Limitations

This study has substantial limitations.

First, it is a single-system engineering case study. The state model is generalizable in concept, but its implementation has not been compared across organizations or independently evaluated.

Second, the test suite is selected and local. Four hundred passing tests do not demonstrate correctness for all inputs, absence of vulnerabilities, or production reliability. The six skipped tests remain unresolved for the evaluated run.

Third, external substrates were absent. Real MATLAB and Octave behavior, numerical stability across engines, QPU execution, collector delivery, and reachable self-hosted model identity were not tested.

Fourth, modeled trust is not shown to be statistically calibrated. The 0.97 cap is a presentation safeguard, not a probability guarantee. Selective-classification and calibration literature show that confidence behavior needs empirical evaluation on representative distributions [4,16].

Fifth, endpoint restrictions are incomplete across the system. OTel admission is stricter than local model-provider admission, and private addressing is not authentication.

Sixth, deterministic receipts are unsigned. No key management, transparency log, or third-party verification was exercised.

Seventh, no usability study tested whether operators correctly interpret UNKNOWN, UNAVAILABLE, CONFLICT, NOT-EVALUATED, and zero-uplift fields. A technically accurate schema can still be misread.

Finally, the work does not validate the scientific content of the formula corpus, prove convergence of named conceptual loops, establish unique solutions for any broad thesis, or substantiate counts such as 180 or 200 proved formulas. Those would require separate mathematical manuscripts and independently checkable formal artifacts.

## 15. Related work

### 15.1 Fail-safe defaults and zero trust

Saltzer and Schroeder’s classic protection principles include fail-safe defaults, complete mediation, economy of mechanism, and least privilege [1]. Our design extends fail-safe defaults to claim semantics: absence of claim-specific evidence yields a weaker explicit state, not a success default.

NIST SP 800-207 defines Zero Trust Architecture around removing implicit trust based on network location and protecting resources through explicit policy [14]. The OTel endpoint boundary borrows the spirit of explicit admission but does not claim full ZTA. In particular, private addressing is not identity, and the present evaluation lacks authenticated collector delivery.

### 15.2 AI risk and abstention

The NIST AI Risk Management Framework emphasizes governing, mapping, measuring, and managing AI risk across the lifecycle [17]. The state-vector approach supplies an implementable representation for several measurement and governance questions: what is ready, what was evaluated, which evidence is available, and what action is authorized.

Selective classification studies models that abstain when confidence is inadequate [16]. Our NOT-EVALUATED and INSUFFICIENT-SIGNAL states share the abstention principle but operate at a system boundary, before a trust score is assigned. Calibration research shows that neural confidence can be miscalibrated even when accuracy is strong [4]. We therefore avoid interpreting modeled trust as a calibrated probability.

### 15.3 Provenance and supply-chain attestations

in-toto models the software supply chain as steps whose products and metadata can be verified against a layout [3]. SLSA defines provenance expectations for build artifacts [18]. DSSE provides a signing envelope that binds payload type and bytes while avoiding fragile canonicalization assumptions [2]. Sigstore and Rekor provide identity-linked signing and transparency mechanisms [15].

Our deterministic receipts are intentionally weaker. They borrow content binding and typed payload ideas but omit signatures, identities, and transparency. This makes them useful for local replay while prohibiting the word “signed.”

### 15.4 Trace propagation and telemetry export

W3C Trace Context standardizes traceparent and tracestate propagation [12]. OpenTelemetry specifies OTLP and exporter behavior [10,11]. These standards do not collapse propagation, configuration, and durable collector storage into one event. Our boundary makes that separation visible to the service response.

### 15.5 Numerical validation

Higham’s treatment of numerical accuracy and stability distinguishes forward error, backward error, conditioning, and algorithmic stability [9]. MATLAB and GNU Octave document matrix left division as solver dispatch rather than naïve inverse multiplication [8,19]. A small residual or cross-engine match may still coexist with ill-conditioning or shared algorithmic assumptions. That is why MATCH is not PROVED.

### 15.6 Quantum benchmarking and trainability

Quantum volume uses randomized model circuits and specified success criteria to characterize a system [5]. Preskill’s discussion of the noisy intermediate-scale quantum era emphasizes hardware constraints and the challenge of demonstrating practical value [20]. McClean et al. show that variational circuits can encounter barren plateaus with exponentially vanishing gradients [6], while later work identifies additional optimization traps [7]. These findings support explicit substrate and benchmark boundaries. A proposal generator should not infer hardware utility from a modeled objective.

### 15.7 Multi-valued evidence

Database nulls, paraconsistent logics, and multi-valued systems all address situations in which binary truth is inadequate. Our model is not a contribution to formal logic. It uses a product of small operational vocabularies to preserve distinctions that binary success/failure erases. The engineering novelty lies in applying the same non-promotion rule across AI query trust, theorem admission, numerical comparison, quantum proposals, telemetry, provider routing, and deployment.

## 16. Reproducibility

### 16.1 Evidence anchor

The manuscript is anchored to local commit:

f3e2c7c9fdd3

Short form:

f3e2c7c

The accompanying archive contains the exact selected source snapshot used for this paper under `sources/a11oy-f3e2c7c/`, the `f3e2c7c` release ledger, and the path-safe supporting receipts. It is not a complete repository clone or dependency cache. Because no remote release or deposit is claimed, readers cannot fetch these bytes from a public release URL; the ZIP checksum is the local package identity.

### 16.2 Required reproduction sequence

A reproduction should:

1. check out the exact full commit;
2. verify a clean working tree except declared local evidence outputs;
3. record operating system, Python and Node versions, dependency lock digests, Lean and mathlib pins, and environment-variable names without secret values;
4. run the selected combined test suite;
5. confirm 400 pass and 6 skip or document the difference;
6. run the Brain blank-query case;
7. run corpus admission with missing canonical Lake and incomplete proof receipts;
8. run quantum oversized-body and proposal-only cases;
9. run numerical unavailable and forbidden-field cases;
10. run OTel malformed-context and unsafe-endpoint cases;
11. run local-provider unreachable and no-credential cases;
12. recompute all evidence-file hashes.

If external engines, a QPU, or a collector are introduced, those runs constitute new experiments. They should not overwrite the unavailable results reported here.

### 16.3 Reproduction expected states

| Experiment | Expected state in this evidence set |
|---|---|
| Blank Brain query | NOT-EVALUATED / INSUFFICIENT-SIGNAL / null trust |
| Missing canonical Lake | SOURCE_UNAVAILABLE |
| Incomplete formula proof evidence | UNKNOWN or non-PROVED / zero uplift |
| Quantum proposal | execution, publication, advantage all false |
| Quantum body over 256 KiB | HTTP 413 |
| Missing MATLAB/Octave | UNAVAILABLE |
| Numerical MATCH policy test | proof uplift zero |
| Unsafe OTLP URL | rejected |
| No collector | delivery unknown/not observed |
| Bogus local model URL, no key | deterministic labeled stub |
| Deployment | LOCAL-CANDIDATE only |

## 17. Ethics and AI-use disclosure

The primary ethical concern is overclaiming. AI and quantum systems attract language that can outrun evidence. This manuscript deliberately records unavailable substrates, zero proved formulas in the admitted local inventory, skipped tests, unsigned receipts, and absent deployment evidence. Those statements should remain intact in derivative decks, dashboards, and summaries.

The system’s human-review gates must not be used to transfer accountability to an unspecified operator. Organizations remain responsible for authorization policy, domain expertise, licensing, privacy, security review, and the consequences of execution.

Generative AI tools assisted with manuscript organization, language editing, code-oriented evidence synthesis, and literature discovery. The named author is responsible for checking every claim, citation, hash, and interpretation before submission. No AI-generated statement should be treated as an independent source. Primary sources and local artifacts, not model output, are the cited evidence.

No human-subject data, patient data, biometric data, or protected demographic inference was used in the reported software tests. This statement does not establish a privacy assessment for future deployments.

## 18. Conclusion

Governed AI services need more than audit logs. They need boundaries that prevent one kind of success from masquerading as another. The implemented state model keeps readiness, query evaluation, source availability, proof, numerical agreement, telemetry delivery, authorization, and deployment separate. Within the selected local suite, 400 tests passed and 6 were skipped, and tested negative paths preserved explicit unavailable, unknown, conflict, and not-evaluated states.

The strongest evidence is architectural: blank queries did not receive fabricated trust; missing proof prerequisites produced zero uplift; quantum proposals could not authorize advantage or execution; absent numerical engines returned unavailable; and telemetry configuration did not become collector delivery. No engine, QPU, or collector was available, so no claim about their behavior is made.

The next research step is not to erase these negative states. It is to add substrate-specific experiments, signed provenance, authenticated endpoint admission, independent reproduction, calibration studies, and usability evaluation while preserving the same non-promotion invariant. Readiness can enable evidence collection. It is never evidence by itself.

## References

[1] J. H. Saltzer and M. D. Schroeder, “The Protection of Information in Computer Systems,” *Proceedings of the IEEE*, vol. 63, no. 9, pp. 1278–1308, 1975. https://doi.org/10.1109/PROC.1975.9939

[2] Secure Systems Lab, “DSSE: Dead Simple Signing Envelope,” specification and reference repository. https://github.com/secure-systems-lab/dsse

[3] S. Torres-Arias, H. Afzali, T. K. Kuppusamy, R. Curtmola, and J. Cappos, “in-toto: Providing Farm-to-Table Guarantees for Bits and Bytes,” *28th USENIX Security Symposium*, 2019. https://www.usenix.org/system/files/sec19-torres-arias.pdf

[4] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, “On Calibration of Modern Neural Networks,” *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70, 2017. https://proceedings.mlr.press/v70/guo17a.html

[5] A. W. Cross, L. S. Bishop, S. Sheldon, P. D. Nation, and J. M. Gambetta, “Validating Quantum Computers Using Randomized Model Circuits,” *Physical Review A*, vol. 100, 032328, 2019. https://doi.org/10.1103/PhysRevA.100.032328

[6] J. R. McClean, S. Boixo, V. N. Smelyanskiy, R. Babbush, and H. Neven, “Barren Plateaus in Quantum Neural Network Training Landscapes,” *Nature Communications*, vol. 9, 4812, 2018. https://doi.org/10.1038/s41467-018-07090-4

[7] E. R. Anschuetz and B. T. Kiani, “Quantum Variational Algorithms Are Swamped with Traps,” *Nature Communications*, vol. 13, 7760, 2022. https://doi.org/10.1038/s41467-022-35364-5

[8] MathWorks, “mldivide: Solve Systems of Linear Equations Ax = B for x,” MATLAB documentation. https://www.mathworks.com/help/matlab/ref/double.mldivide.html

[9] N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002. https://doi.org/10.1137/1.9780898718027

[10] OpenTelemetry, “OpenTelemetry Protocol Specification.” https://opentelemetry.io/docs/specs/otlp/

[11] OpenTelemetry, “OTLP Exporter Specification.” https://opentelemetry.io/docs/specs/otel/protocol/exporter/

[12] World Wide Web Consortium, “Trace Context, W3C Recommendation.” https://www.w3.org/TR/trace-context/

[13] T. Berners-Lee, R. Fielding, and L. Masinter, “Uniform Resource Identifier (URI): Generic Syntax,” RFC 3986, IETF, 2005. https://datatracker.ietf.org/doc/html/rfc3986

[14] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, “Zero Trust Architecture,” NIST Special Publication 800-207, 2020. https://doi.org/10.6028/NIST.SP.800-207

[15] Sigstore, “Rekor Transparency Log,” official project documentation. https://docs.sigstore.dev/logging/overview/

[16] Y. Geifman and R. El-Yaniv, “Selective Classification for Deep Neural Networks,” *Advances in Neural Information Processing Systems 30*, 2017. https://papers.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html

[17] E. Tabassi, “Artificial Intelligence Risk Management Framework (AI RMF 1.0),” NIST AI 100-1, 2023. https://doi.org/10.6028/NIST.AI.100-1

[18] SLSA Project, “SLSA Provenance,” official specification. https://slsa.dev/spec/v1.0/provenance

[19] GNU Octave Project, “Arithmetic Operators and Matrix Left Division,” GNU Octave documentation. https://docs.octave.org/latest/Arithmetic-Ops.html

[20] J. Preskill, “Quantum Computing in the NISQ Era and Beyond,” *Quantum*, vol. 2, 79, 2018. https://doi.org/10.22331/q-2018-08-06-79

## Appendix A. State-transition specification

### A.1 Brain

| Prior state | Event | Gate | Next state | Uplift |
|---|---|---|---|---|
| service unknown | readiness probe succeeds | modules/index present | READY | none |
| any readiness | blank query | none | NOT-EVALUATED / INSUFFICIENT-SIGNAL | zero |
| any readiness | admissible query | query evidence functions execute | EVALUATED | modeled only |
| source expected | canonical source absent | no substitution policy | SOURCE_UNAVAILABLE | zero |
| refresh idle | valid loopback POST | cooldown and local-source gates | local reindex attempt | none |
| refresh failed | error | success receipt absent | failed/no receipt | zero |

### A.2 Formula corpus

| Input class | Missing or conflicting evidence | Output class | Proof uplift |
|---|---|---|---|
| claimed PROVED | bytes/digest absent | UNKNOWN/quarantine | 0 |
| claimed PROVED | sorry/admit present | non-PROVED | 0 |
| claimed PROVED | kernel receipt invalid | UNKNOWN/quarantine | 0 |
| claimed PROVED | Lean/mathlib commit mismatch | UNKNOWN/quarantine | 0 |
| OPEN | any numerical observation | OPEN | 0 |
| EXPERIMENTAL | matching solver output | EXPERIMENTAL | 0 |
| REFUTED | registry presence | REFUTED | 0 |

### A.3 Quantum utility

| Event | Output | Advantage verified | Execution authorized |
|---|---|---:|---:|
| valid bounded proposal | proposal receipt | false | false |
| review gate supported | HUMAN-REVIEW-ELIGIBLE | false | false |
| VQC simulation | MODELED/SIMULATED | false | false |
| body exceeds 256 KiB | HTTP 413 | false | false |
| hidden field | validation rejection | false | false |

### A.4 Numerics

| Condition | Response | Proof uplift |
|---|---|---:|
| prohibited field | rejected | 0 |
| isolation unavailable | UNAVAILABLE | 0 |
| engine unavailable | UNAVAILABLE | 0 |
| one invalid result | UNKNOWN/CONFLICT | 0 |
| two results within tolerance | MATCH | 0 |
| two results outside tolerance | CONFLICT | 0 |

### A.5 Telemetry

| Observation | Propagation | Export | Delivery |
|---|---|---|---|
| valid traceparent | READY | unchanged | UNKNOWN |
| invalid traceparent | rejected/new local context | unchanged | UNKNOWN |
| admitted endpoint | unchanged | CONFIGURED | UNKNOWN |
| exporter attempt | unchanged | ATTEMPTED | UNKNOWN |
| collector acknowledgement | unchanged | attempted | OBSERVED |

The last row was not observed in this study.

## Appendix B. Test and evidence inventory

The component reports provide useful detail but overlap:

- Wave 17 candidate: 373 passed, 6 skipped, 5 warnings;
- quantum focused and regression selections: 67 tests;
- numerical adapter: 15 focused tests and 48 regression tests;
- telemetry: 4 focused security and honesty checks;
- corpus bridge: 9 pure contract tests.

These numbers must not be added. The combined candidate's authoritative selected-suite result is 400 passed and 6 skipped at `f3e2c7c`. The later `29c5d` Formal Conjecture Lab ledger reports 410 passed, 6 skipped, and 0 failed in a changed candidate and is preserved separately at `evidence/later-validation/formal-conjecture-lab-release-ledger.json`; it is not part of the Paper 2 aggregate.

The numerical receipt additionally records:

- bundled/copied engines: 0;
- network calls: 0;
- package installs: 0;
- arbitrary user code paths: 0;
- proof/trust uplift: 0;
- copy-completeness check: 287 modules;
- secret/state scans: passed;
- Docker build: unavailable due sandbox denial;
- pre-existing copy-sync violations: 44;
- numerical-scope violations introduced: 0.

The corpus bridge bounded subrun recorded:

- network calls: 0;
- GPU calls: 0;
- writes outside worktree: 0;
- trust-threshold changes: 0;
- Lake source: SOURCE_UNAVAILABLE;
- proof credit: 0.

## Appendix C. Evidence hashes and archive paths

| Archive-relative file | Artifact identity | Source SHA-256 |
|---|---|---|
| `evidence/paper2/brain-corpus-wave18-receipt.json` | Brain corpus bridge receipt internal digest | 70208a7464e54d1f794ae4fa572c68580fd1df4d2bd89a18e769538b3677fba8 |
| `evidence/paper2/numerics-adapter-wave18-receipt.sanitized.json` | Numerical adapter Wave 18 receipt | 56d962cc2af9735544cfe22790b83e6241fccac497b7cc7922a3bfa8b33fc31b |
| `evidence/paper2/otel-provenance-frontier-receipt.json` | OTel provenance frontier receipt | 8ef6701924caf2f04885d56445dc0b9b2e27336dd2a1fc5e9a8cf03dd700ff0e |
| `evidence/shared/lake-mathlib-octave-operational-contract.sanitized.json` | Lake/mathlib/Octave operational contract | 589a466436558ad3ca5f58d9a6abd9c2f7f0d522da6df7e7753cd3ba4e806583 |
| `evidence/paper2/a11oy-frontier-wave18-release-ledger.json` | Primary combined run anchor | see release manifest |
| `evidence/later-validation/formal-conjecture-lab-release-ledger.json` | Later non-promoting validation at `29c5d` | see release manifest |

The two files labeled `sanitized` differ only by documented path normalization; `SOURCE_TRANSFORMATIONS.json` records their original and packaged digests. The hash of this manuscript is intentionally omitted from the body because adding it would change the file. It is reported in the release manifest.

## Appendix D. Claim boundary checklist

Before any derivative publication or presentation, verify:

- [ ] “ready” is not used as a synonym for “trustworthy”;
- [ ] NOT-EVALUATED is not plotted as zero confidence;
- [ ] a snapshot is not called the canonical Lake source;
- [ ] OPEN, EXPERIMENTAL, REFUTED, and UNKNOWN are not called PROVED;
- [ ] deterministic digests are labeled unsigned;
- [ ] numerical MATCH is not described as proof;
- [ ] no MATLAB/Octave agreement is claimed without engine receipts;
- [ ] no QPU, hardware, utility, or advantage claim is made from simulation;
- [ ] review eligibility is not called authorization;
- [ ] trace propagation is not called export delivery;
- [ ] exporter configuration is not called collector receipt;
- [ ] a configured local URL is not called a live provider without route evidence;
- [ ] passing local tests are not called deployment;
- [ ] skipped tests and unavailable substrates remain disclosed;
- [ ] formula-count and theorem-count claims are derived from admitted, independently verifiable artifacts.

## Appendix E. Future experiments

The following experiments would extend, but not retroactively alter, this evidence set.

**E1. Independent reproduction.** A second operator checks out the exact candidate from a content-addressed archive, runs the same suite, recomputes hashes, and records deviations.

**E2. Real numerical engines.** Licensed MATLAB and a separately installed GNU Octave run fixed public test matrices, including well-conditioned, ill-conditioned, singular, and repeated-eigenvalue cases. Results include versions, BLAS/LAPACK providers, condition estimates, forward and backward error, resource limits, and raw bound receipts. Agreement remains non-proof.

**E3. Collector acknowledgement.** A private authenticated collector receives OTLP spans. The experiment binds client export attempt, collector acknowledgement, and backend query to one trace ID while measuring loss and retry behavior.

**E4. Self-hosted provider identity.** A local serving process exposes a signed model manifest and health evidence. Admission uses the same endpoint policy as OTel, peer authentication, DNS/IP pinning, and an inference challenge bound to model version.

**E5. Quantum hardware protocol.** A named benchmark is preregistered with classical baselines, provider and device identity, calibration context, shot count, raw results, statistical analysis, and failure criteria. Proposal software cannot authorize the resulting claim.

**E6. Operator comprehension.** A usability study tests whether participants distinguish READY, NOT-EVALUATED, UNKNOWN, UNAVAILABLE, CONFLICT, MATCH, CONFIGURED, DELIVERED, and DEPLOYED. Misinterpretation becomes a measured frontend defect rather than an assumed training issue.

**E7. Signed provenance.** Local deterministic receipts are wrapped in DSSE, signed with a protected identity, optionally logged transparently, and verified before admission. The study separately evaluates signature validity and subject-matter truth.
