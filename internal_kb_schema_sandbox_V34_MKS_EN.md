# Schema Sandbox V34-KB: A Modular Knowledge System and Trusted Microkernel Architecture for Goal-Preserving Professional AI Capability Machines

## Policy Algebra, Event-Sourced Knowledge State, Profile-Driven Semantics, Recipe-Based Delivery, and Signed Capability Supply Chains

> [!CAUTION]
> **INTERNAL KNOWLEDGE BASE & DETAILED SPECIFICATION (CONFIDENTIAL — V34-KB)**
>
> This document is for internal research, product architecture, implementation, and commercialization planning at psi.run. It contains proprietary design choices, control-plane semantics, packaging strategy, and reference implementation requirements. It is not a public conformance claim and MUST NOT be represented as proof that the current implementation provides a security boundary, scientific authority, industrial certification, or regulatory compliance.

**Author:** Tengjiao Liu  
**Organization:** psi.run  
**Document Version:** V34-KB  
**Evidence/Design Snapshot:** 2026-07-29  
**Status:** Internal normative architecture specification with illustrative implementation schemas  

---

## 0. Document Status, Version Layers, and Normative Language

This knowledge base uses RFC 2119 terms:

- **MUST / SHALL / REQUIRED**: necessary for a system to claim the stated V34 implementation property.
- **SHOULD / RECOMMENDED**: preferred design unless an explicit, evidence-backed exception is recorded.
- **MAY / OPTIONAL**: permitted variation that does not change the stated assurance boundary.

V34 separates the following version layers:

| Layer | Identifier | Meaning |
|---|---|---|
| Knowledge-base document | `V34-KB` | This architecture and method specification |
| Interoperability protocol | `SIP v1.2` | Existing wire/manifest protocol baseline; unchanged by this document |
| Modular extension | `MKS Extension v0.1-draft` | Module, Profile, Recipe, Pack, and composition semantics proposed here |
| Trusted kernel implementation | `schemabox-kernel-v0.1.0-alpha` | Reference implementation target, not yet a security boundary |
| Conformance suite | `schemabox-conformance-v0.1-spec` | Fixtures, algebra properties, threat tests, and replay tests |
| Package versions | SemVer | Individual modules, adapters, profiles, recipes, and packs |

V34 does **not** replace the S1–S10 reference architecture from V33. It defines how that reference architecture can be implemented as a modular, composable, testable, and commercially distributable knowledge system.

---

## 1. Abstract

Schema Sandbox V33 defined a ten-layer, goal-preserving architecture for assembling professional AI capability machines from heterogeneous models, tools, memories, verifiers, experts, and controlled action channels. Its breadth created an adoption problem: a developer who only needed evidence-aware outputs or a research dossier should not have to deploy the entire architecture. An initial “twelve LEGO blocks” proposal addressed adoption but treated modules too much like ordinary middleware: arbitrary hook order, ambiguous state ownership, and insufficient separation between declarations and enforceable guarantees.

V34 introduces the **Schema Sandbox Modular Knowledge System (MKS)**. MKS is not a vector database, a RAG wrapper, or a plugin collection. It is a governed, event-sourced system in which goals, assertions, evidence, artifacts, trajectories, obligations, reviews, configurations, and releases are versioned first-class objects. A non-bypassable **K0 Trusted Microkernel** owns external-effect authorization, canonical event commitment, artifact identity, action receipts, lifecycle scheduling, and replay. Modules may propose constraints, transformations, evidence obligations, routes, and state transitions; they may not directly commit external side effects or mutate canonical state.

V34 separates five concerns: S1–S10 as the conceptual reference model; capability modules as deployable mechanisms; domain Profiles as semantic interpreters; Recipes as tested outcome-oriented compositions; and signed Packs plus a Registry as the distribution and trust layer. Modules compose under an explicit policy algebra rather than arbitrary declaration order. Effective capabilities are the intersection of host authority, Recipe requests, and module restrictions; risk is merged as a profile-defined vector join; evidence obligations are a normalized union; and assertion ceilings are combined through a profile-defined lattice meet. Every transformation creates a new immutable artifact version and a transformation receipt. Every externally consequential action requires an authorization ticket, intent record, execution receipt, and committed outcome event.

The document defines a fixed P0–P10 lifecycle, multi-dimensional governance decisions, module and Pack manifests, event and artifact schemas, effect classes, failure/degradation semantics, conformance levels, supply-chain controls, property-based tests, and reference Recipes for SchemaDocs Evidence Room, GEO Audit, Decision Research Dossier, and AI-assisted mathematical research. V34 is a specification and implementation target. No security, scientific, or industrial assurance is claimed until runtime confinement, durable journals, immutable artifact storage, signing, replay, Profile compilation, and independent conformance tests are operational.

---

## 2. Executive Definition

> **Schema Sandbox is layered as a reference architecture, modular as an implementation system, Profile-driven in domain semantics, Recipe-based in product delivery, Pack-based in distribution, and Registry-governed in trust and exchange. Modules compose under an explicit policy algebra rather than arbitrary middleware order.**

The V34 stack is:

```text
S1–S10 Reference Architecture
    what a complete professional AI system must govern
                         ↓
K0 Trusted Microkernel
    identity, authority, lifecycle, journal, artifacts, effects, replay
                         ↓
Capability Modules
    contract, evidence, telos, assertion, trajectory, assurance, orchestration
                         ↓
Domain Profiles
    GEO, research, legal, mathematical, industrial, bio-evidence, etc.
                         ↓
Tested Recipes
    outcome-oriented compositions such as GEO Audit or Decision Dossier
                         ↓
Signed Packs
    modules + adapters + profile + recipes + fixtures + license + signature
                         ↓
SchemaDocs Registry
    discovery, versions, hashes, revocation, compatibility, licensing, exchange
```

The system has one central commercial and technical promise:

> **Any model, tool, module, human expert, or external service entering the system operates under one replayable framework for goals, permissions, evidence, assertions, artifacts, repairs, and release.**

---

## 3. Why “Modular Knowledge System” Is the Correct Category

A modular knowledge system is more than an agent SDK and more than a knowledge base.

### 3.1 It is not merely a knowledge graph

A knowledge graph stores relationships. MKS also governs:

- who or what may create or change a relationship;
- which evidence supports it;
- which configuration and artifact version it refers to;
- which review scope applies;
- when the support becomes invalid;
- what actions may follow from it;
- how a correction propagates;
- which failed route remains reusable.

### 3.2 It is not merely RAG

RAG retrieves text. MKS distinguishes:

- retrieved source;
- candidate interpretation;
- assertion;
- support set;
- contradiction;
- verifier or review result;
- release ceiling;
- temporal status;
- downstream consequence.

### 3.3 It is not merely an agent runtime

An agent runtime may execute tool calls and preserve state. MKS additionally asks:

- whether the active work still serves the original objective;
- whether a result is candidate, checked, independently reviewed, or publishable;
- whether a formalizer repaired or replaced an argument;
- whether a failed route should be archived, revived, or certified closed;
- whether a new module silently changed the effective guarantee.

### 3.4 It is not merely governance documentation

V34 requires executable schemas, deterministic composition rules, replayable events, artifact hashes, action receipts, conformance fixtures, and threat tests. A policy document without enforcement and evidence does not constitute MKS conformance.

---

## 4. Relationship to V33 and SIP

### 4.1 V33 remains the conceptual reference architecture

S1–S10 continue to answer:

> What dimensions must a complete professional AI capability machine govern?

V34 answers:

> How can those dimensions be deployed incrementally without losing goal, evidence, authority, and assertion semantics when modules are recombined?

There is no required one-to-one mapping from layers to packages.

```text
Reference Architecture ≠ Package Layout
```

A module may implement mechanisms from several S-layers. One S-layer may be supported by several modules, kernel services, and Profiles.

### 4.2 SIP remains the interoperability protocol

SIP governs discovery, manifest exchange, mounting, invocation, integrity, and cross-runtime interoperability. V34 defines a modular implementation architecture and a proposed `MKS Extension v0.1-draft` for:

- `ModuleManifest`;
- `ProfileManifest`;
- `RecipeManifest`;
- `PackManifest`;
- `CompositionAssuranceManifest`;
- capability-interface dependencies;
- lifecycle subscriptions;
- failure semantics;
- conformance evidence.

A future SIP revision may standardize these objects. Until then, V34 MUST NOT describe the MKS extension as part of the ratified SIP v1.2 wire contract.

### 4.3 Protocol names and implementation names MUST be separate

Recommended naming:

```text
SIP                     open interoperability specification
@schemabox/kernel       psi.run reference implementation
@schemabox/evidence     psi.run module implementation
SchemaDocs              registry, artifact exchange, trust and publishing layer
```

The `@sip/*` namespace SHOULD NOT be used for proprietary implementation packages if SIP is intended to become an open standard.

---

## 5. Twelve V34 Architectural Invariants

### Invariant 1 — Layers are conceptual; modules are deployable

S1–S10 MUST remain a reference model and MUST NOT be frozen into a package directory.

### Invariant 2 — Module count is not a protocol invariant

“Twelve modules” is a useful product surface, not a permanent ontology. Modules MAY be split or merged when state ownership, failure semantics, adoption value, or testability justify it.

### Invariant 3 — K0 is the sole external-effect committer

Modules MAY propose actions. Only K0 MAY prepare, authorize, execute, and record externally consequential effects.

### Invariant 4 — Modules have no ambient authority

A module MUST NOT obtain filesystem, network, environment, subprocess, database, publication, or device authority merely by being loaded. Such access MUST be provided through capability-scoped K0 handles or approved adapters.

### Invariant 5 — Adding an unprivileged module cannot expand consequences

Without a new signed host authorization, adding a module MUST NOT:

- widen filesystem, network, database, tool, or device scope;
- raise the assertion-release ceiling;
- remove evidence obligations;
- lower any risk coordinate.

### Invariant 6 — Governance decisions are vectors, not one boolean

Authorization, evidence sufficiency, goal disposition, capacity, release, risk, and assertion ceiling MUST remain distinct coordinates.

### Invariant 7 — Canonical state has one source

Canonical state MUST be derivable from a durable, append-only event journal. Module dashboards, graphs, caches, and indexes are rebuildable projections.

### Invariant 8 — Transformations create immutable artifact versions

A module MUST NOT overwrite an existing artifact version. Every material transformation MUST produce a new content hash and a `TransformationReceipt` linking inputs, outputs, module identity, configuration, and evidence.

### Invariant 9 — Failure behavior is declared before execution

Every module MUST declare timeout, unavailability, invalid-state, and dependency-failure behavior. Runtime improvisation that weakens hard boundaries is forbidden.

### Invariant 10 — Domain semantics belong to Profiles

“What counts as verified, safe, qualified, relevant, novel, or publishable” MUST be defined by a domain Profile, not embedded permanently in generic modules.

### Invariant 11 — Products are delivered as tested Recipes

Customers buy outcomes. A Recipe MUST define the Profile, required capabilities, module versions, adapters, fixtures, threat tests, performance envelope, guarantees, and non-guarantees.

### Invariant 12 — Trajectory is an organizational asset

Typed records of failed routes, repairs, representation changes, test anomalies, configuration changes, and revival conditions MUST be retainable and reusable without requiring private chain-of-thought.

---

## 6. Formal Composition Model

A V34 composition is:

\[
\mathcal{C}=\langle K_0, H, R, P, M, A, E \rangle
\]

where:

- \(K_0\) is the trusted microkernel;
- \(H\) is host authority;
- \(R\) is the selected Recipe;
- \(P\) is the active domain Profile;
- \(M\) is the resolved module set;
- \(A\) is the adapter set;
- \(E\) is the execution environment and trust store.

### 6.1 Effective capability scope

\[
C_{effective}
=
C_{host-authorized}
\cap C_{recipe-requested}
\cap \bigcap_{m \in M} C_{module-restricted}(m)
\]

Capability comparison MUST operate on canonicalized semantic scopes, not raw strings. Path normalization, symlink resolution, domain and port normalization, redirects, tool aliases, database operations, and device actions MUST be evaluated before the intersection is accepted.

### 6.2 Governance decision vector

A module returns a partial decision vector:

\[
D=\langle A_u,E_v,G_t,C_p,R_l,\rho,\kappa\rangle
\]

where:

- \(A_u\): authorization;
- \(E_v\): evidence sufficiency and obligations;
- \(G_t\): goal/telos disposition;
- \(C_p\): capacity disposition;
- \(R_l\): release disposition;
- \(\rho\): risk vector;
- \(\kappa\): assertion ceiling.

The kernel merges coordinates independently. A capacity hold MUST NOT be rewritten as an authorization denial. An evidence requirement MUST NOT be treated as human approval. Permission to execute MUST NOT imply permission to release.

### 6.3 Risk vector

The default cross-domain risk vector is:

```yaml
RiskVector:
  confidentiality: LOW | MEDIUM | HIGH | CRITICAL
  integrity: LOW | MEDIUM | HIGH | CRITICAL
  irreversibility: LOW | MEDIUM | HIGH | CRITICAL
  financial: LOW | MEDIUM | HIGH | CRITICAL
  physicalSafety: LOW | MEDIUM | HIGH | CRITICAL
  claimCriticality: LOW | MEDIUM | HIGH | CRITICAL
  regulatory: LOW | MEDIUM | HIGH | CRITICAL
```

Profiles MAY add dimensions. Risk is merged by coordinate-wise join, not by one scalar `maxRisk()` unless the Profile explicitly defines a total order.

### 6.4 Assertion lattice

Assertion maturity and release ceilings are Profile-defined partially ordered sets. The compiler MUST use a Profile-provided `meet` operation:

```typescript
interface AssertionLattice<T> {
  meet(a: T, b: T): T;
  join(a: T, b: T): T;
  isAtLeast(a: T, b: T): boolean;
  validate(value: T): void;
}
```

The generic kernel MUST NOT assume that a proof-kernel status, expert review, production qualification, and regulatory approval lie on one universal linear scale.

### 6.5 Evidence obligations

Evidence obligations merge as a normalized set union. Two obligations are equivalent only if their claim scope, artifact identity, verifier class, independence group, temporal validity, and environment requirements are equivalent under the active Profile.

### 6.6 Informal monotonic consequence-safety property

If:

1. modules have no ambient authority;
2. every effect passes through K0;
3. host authority is fixed;
4. capability normalization is correct;
5. assertion meet and risk join are monotone;

then adding an unprivileged module \(m\) should satisfy:

\[
C_{effective}(\mathcal{C}\oplus m) \subseteq C_{effective}(\mathcal{C})
\]

\[
\kappa(\mathcal{C}\oplus m) \preceq \kappa(\mathcal{C})
\]

\[
Req_E(\mathcal{C}\oplus m) \supseteq Req_E(\mathcal{C})
\]

This is a design invariant, not a machine-checked theorem. The conformance suite MUST test its operational consequences.

---

## 7. Four-Plane Architecture

### 7.1 K0 Trusted Kernel Plane

```text
Module and Pack Identity
Publisher Trust and Revocation
Capability Authority
Fixed Lifecycle Scheduler
Policy Algebra
Canonical Event Journal
Artifact Registry
Action Transaction Executor
State Projection and Replay
Schema Migration and Rollback
```

K0 is not a business feature module. It is the minimum trusted computing base for V34 claims.

### 7.2 Knowledge and Governance Plane

```text
Contract
Evidence
Artifact
Telos
Assertion
Trajectory
Assurance
```

This plane answers:

- What is the objective?
- What is asserted?
- What supports it?
- Which artifact and version are involved?
- What failed or changed?
- What is the strongest allowed release state?

### 7.3 Orchestration and Resource Plane

```text
Workspace
Federation
Capacity
Portfolio
Accommodation
```

This plane answers:

- Where may work run?
- Which model, tool, or expert receives it?
- How much budget is allocated?
- Which routes remain active?
- When may the active frame be challenged?

### 7.4 Domain and Product Plane

```text
Profiles
Adapters
Recipes
Signed Packs
Registry
```

This plane turns generic governance into customer outcomes.

---

## 8. K0 Trusted Microkernel

### 8.1 Minimum trusted computing base

K0 MUST remain small enough to audit. Its required responsibilities are:

1. identity and trust;
2. capability authority;
3. lifecycle scheduling;
4. decision merging;
5. canonical event commitment;
6. artifact registration;
7. action preparation and execution;
8. receipts and idempotency;
9. state projection and replay;
10. migration, recovery, and rollback.

K0 SHOULD NOT contain domain prompts, GEO rules, legal reasoning, mathematical tactics, or industry-specific scoring.

### 8.2 Module identity and attestation

Before loading a module, K0 MUST verify:

- content digest;
- publisher identity;
- signature;
- revocation state;
- compatible kernel range;
- SBOM reference;
- requested privileges;
- lifecycle subscriptions;
- state schemas and migrations;
- fixture and threat-test digests;
- license and distribution rights.

### 8.3 Capability authority

K0 owns the final grant. Modules MAY:

- restrict a grant;
- request a new grant proposal;
- require approval;
- deny a proposal.

Modules MUST NOT grant themselves or another module new authority.

### 8.4 Runtime confinement

TypeScript interfaces are not a security boundary. A conforming secure runtime MUST prevent modules from directly using ambient `fetch`, filesystem, environment, subprocess, database, or device APIs.

Recommended execution classes:

| Class | Execution | Intended modules | Assurance |
|---|---|---|---|
| `M0-PURE` | In-process, pure functions over immutable inputs | Algebra helpers, schema validators | No external authority |
| `M1-WORKER` | Worker/thread with restricted message interface | Observers, transformers | Process-language isolation only |
| `M2-WASI` | WASI/Wasmtime with explicit preopens and network proxy | Third-party modules | Capability-oriented runtime confinement |
| `M3-REMOTE` | Signed remote service behind K0 proxy | Enterprise policy engines, heavy verifiers | Network and service trust required |
| `K0-NATIVE` | Audited kernel code | capability authority, journal commit, executor | Highest trust; smallest codebase |

### 8.5 Immutable context

Handlers receive immutable snapshots:

```typescript
interface ModuleContext {
  readonly runId: string;
  readonly phase: LifecyclePhase;
  readonly stateSnapshotHash: string;
  readonly artifactSnapshotHash: string;
  readonly policySnapshotHash: string;
  readonly state: Readonly<StateView>;
  readonly artifacts: ReadonlyArtifactView;
  readonly emitProposal: (proposal: ModuleProposal) => void;
}
```

A handler MUST NOT mutate canonical state. It returns decisions, proposed events, and proposed artifacts for K0 adjudication and commit.

---

## 9. Fixed P0–P10 Lifecycle

V34 replaces arbitrary middleware order with a compiled lifecycle.

```text
P0  MODULE_LOAD_AND_ATTEST
P1  INPUT_NORMALIZATION
P2  GOAL_PROFILE_CONTEXT_BINDING
P3  PLAN_AND_ROUTE_PROPOSAL
P4  ACTION_GOVERNANCE
P5  ACTION_PREPARE_AND_INTENT_COMMIT
P6  KERNEL_ACTION_EXECUTION
P7  RESULT_ARTIFACT_EVIDENCE_REGISTRATION
P8  ASSERTION_AND_SUPPORT_EVALUATION
P9  RELEASE_GOVERNANCE_AND_STATE_COMMIT
P10 MERGE_COMPACT_STAGNATION_TEARDOWN
```

### 9.1 Phase ownership

| Phase | Module participation | K0 authority |
|---|---|---|
| P0 | Manifests only | Verify, resolve, reject, load |
| P1 | Contract transformers/gates | Freeze normalized input |
| P2 | Telos, Profile, Contract | Seal objective and active semantics |
| P3 | Portfolio, Federation, Telos | Freeze plan proposal snapshot |
| P4 | Gates, Assurance requirements, Capacity | Merge decision vector |
| P5 | No ordinary module execution | Record intent, idempotency key, authorization ticket |
| P6 | No module handler | Execute through approved adapter/capability proxy |
| P7 | Evidence, Artifact, Assurance observers | Register receipt, artifacts, evidence |
| P8 | Assertion, Trajectory, Assurance, Telos | Evaluate support sets and ceilings |
| P9 | Release gates | Execute release as governed effect and atomically commit state |
| P10 | Merge, compaction, stagnation, teardown | Persist/rebuild/checkpoint/revoke temporary grants |

### 9.2 Deterministic phase behavior

Gate results MUST be independent of completion order. The same snapshot, module versions, Profile, and configuration MUST produce the same merged result, excluding explicitly declared nondeterministic observations whose raw evidence is recorded.

### 9.3 Timeouts

Default timeout semantics:

| Criticality | Timeout behavior |
|---|---|
| `SECURITY_CRITICAL` | deny or fail closed |
| `CLAIM_CRITICAL` | block release and retain candidate |
| `OPERATION_CRITICAL` | defer or require human |
| `ADVISORY` | degrade, record missing signal, continue if Profile permits |

### 9.4 Nested release action

Publishing or persisting an assertion is itself an external effect. P9 MUST invoke the same authorization-ticket and action-receipt semantics used for other external actions.

---

## 10. Multi-Dimensional Policy Algebra

### 10.1 Authorization coordinate

```typescript
type AuthorizationDecision =
  | { status: 'ALLOW' }
  | { status: 'DENY'; reasons: Reason[] }
  | { status: 'REQUIRE_HUMAN'; approvalClass: string; reasons: Reason[] };
```

Authorization merges by restrictive meet.

### 10.2 Evidence coordinate

```typescript
type EvidenceDecision =
  | { status: 'SUFFICIENT' }
  | { status: 'REQUIRE_EVIDENCE'; requirements: EvidenceRequirement[] };
```

Requirements merge by normalized union.

### 10.3 Goal coordinate

```typescript
type GoalDecision =
  | { status: 'CONTINUE' }
  | { status: 'EXPLORE'; ticketClass: string }
  | { status: 'VERIFY' }
  | { status: 'REFRAME'; proposalRef: string }
  | { status: 'STOP'; outcomeClass: string }
  | { status: 'ASK'; questionRef: string };
```

Goal decisions follow explicit Telos conflict rules; they are not mixed into permission decisions.

### 10.4 Capacity coordinate

```typescript
type CapacityDecision =
  | { status: 'ADMIT' }
  | { status: 'HOLD' }
  | { status: 'SCALE_UP'; leaseRequestRef: string }
  | { status: 'SCALE_DOWN'; targetRef: string }
  | { status: 'OVERFLOW'; routeId: string }
  | { status: 'REQUEST_BUDGET'; requestRef: string };
```

Capacity changes MUST preserve the current capability grant and assertion policy.

### 10.5 Release coordinate

```typescript
type ReleaseDecision =
  | { status: 'ALLOW_RELEASE'; scopeRef: string }
  | { status: 'BLOCK_RELEASE'; reasons: Reason[] }
  | { status: 'RELEASE_PARTIAL'; claimAtomRefs: string[]; exclusions: string[] };
```

### 10.6 Governance decision

```typescript
interface GovernanceDecision<TAssertion> {
  authorization: AuthorizationDecision;
  evidence: EvidenceDecision;
  goal: GoalDecision;
  capacity: CapacityDecision;
  release: ReleaseDecision;
  risk: RiskVector;
  assertionCeiling: TAssertion;
  proposedEvents: ProposedEvent[];
  proposedArtifacts: ProposedArtifact[];
}
```

### 10.7 Algebra properties required by conformance

For every Profile-defined merge operation, the suite MUST test where applicable:

- commutativity;
- associativity;
- idempotence;
- monotonicity;
- deterministic serialization;
- stable canonicalization.

---

## 11. Canonical Event Journal and State Projection

### 11.1 Event journal requirements

The canonical journal MUST provide:

- append-only API;
- monotonic sequence numbers;
- previous-event hash;
- event hash;
- schema version;
- actor and module identity;
- durable commit acknowledgment;
- idempotency key;
- transaction boundary;
- corruption detection;
- snapshot and replay;
- schema migration history.

```typescript
interface KernelEvent<T = unknown> {
  eventId: string;
  sequence: string;
  eventType: string;
  schemaVersion: string;
  payload: T;
  runId: string;
  actorRef: string;
  moduleRef?: string;
  previousEventHash: string;
  eventHash: string;
  timestamp: string;
  idempotencyKey?: string;
}
```

### 11.2 Two journals, one canonical transaction boundary

V34 distinguishes:

- **Operational evidence**: actions, arguments, receipts, resources, permissions;
- **Epistemic evidence**: goals, assertions, defects, repairs, reviews, maturity transitions.

They MAY be stored separately for scale, but a consequential transition MUST reference both sides through one committed transaction envelope.

### 11.3 Projections

Examples of rebuildable projections:

- goal state;
- assertion graph;
- alternative support sets;
- route and branch graph;
- proof or assurance obligations;
- reviewer coverage matrix;
- artifact lineage;
- capacity and verification debt;
- public claim cards;
- industrial configuration baseline.

### 11.4 Replay determinism

Given the same event sequence and projection version, replay MUST produce the same projection hash. Migration changes MUST create a new projection version and preserve the ability to reproduce prior states.

---

## 12. Artifact Registry and Transformation Receipts

### 12.1 Artifact identity

```typescript
interface ArtifactRecord {
  artifactId: string;          // logical identity
  versionId: string;           // immutable content-addressed version
  artifactType:
    | 'DOCUMENT' | 'DATASET' | 'CODE' | 'MODEL' | 'PROOF'
    | 'CHECKER' | 'REPORT' | 'CONFIG' | 'TEST_RESULT'
    | 'SIMULATION' | 'CAD' | 'MEDIA' | 'OTHER';
  contentHash: string;
  mediaType: string;
  producerRef: string;
  createdAt: string;
  sourceRefs: string[];
  derivedFrom: string[];
  supersedes: string[];
  contradictedBy: string[];
  transformationReceiptRef?: string;
  accessPolicyRef: string;
  retentionPolicyRef: string;
  integrityStatus: 'UNVERIFIED' | 'HASHED' | 'SIGNED' | 'REVOKED';
}
```

### 12.2 Transformation receipt

```typescript
interface TransformationReceipt {
  transformationId: string;
  moduleId: string;
  moduleVersion: string;
  inputArtifactVersions: string[];
  outputArtifactVersions: string[];
  configurationHash: string;
  evidenceRefs: string[];
  deterministic: boolean;
  executedAt: string;
}
```

### 12.3 No in-place mutation

The registry MUST reject attempts to change the bytes associated with an existing `versionId`. A logical artifact may acquire a new version, but history remains addressable.

### 12.4 Transformation conflicts

If two transformers produce incompatible successors for the same logical artifact and no merge rule is declared, the compiler or runtime MUST emit `TRANSFORMATION_CONFLICT`; load order MUST NOT decide the winner.

### 12.5 SchemaDocs role

SchemaDocs is the natural public/private implementation for:

- artifact identity and passports;
- content-addressed versions;
- publisher identity;
- assertion-to-source binding;
- Recipe and Pack pages;
- trust and revocation notices;
- API/MCP access;
- licensing and exchange.

---

## 13. Action Transaction and Effect Classes

### 13.1 Effect classes

```typescript
type EffectClass =
  | 'PURE'
  | 'LOCAL_REVERSIBLE'
  | 'EXTERNALLY_IDEMPOTENT'
  | 'EXTERNAL_COMPENSATABLE'
  | 'IRREVERSIBLE';
```

Examples:

| Effect class | Example | Required control |
|---|---|---|
| `PURE` | local calculation | deterministic evidence if claim-critical |
| `LOCAL_REVERSIBLE` | write to private worktree | snapshot/rollback |
| `EXTERNALLY_IDEMPOTENT` | API request with idempotency key | deduplication and receipt |
| `EXTERNAL_COMPENSATABLE` | create cloud resource | compensating action plan |
| `IRREVERSIBLE` | send public message, payment, physical actuation | explicit approval and precommit evidence |

### 13.2 Transaction sequence

```text
ActionProposal
    → merged GovernanceDecision
    → AuthorizationTicket
    → Intent Event committed
    → K0 execution through approved Adapter
    → ActionReceipt captured
    → Artifact/Evidence registration
    → Outcome Event committed
    → compensation if supported and required
```

### 13.3 Action receipt

```typescript
interface ActionReceipt {
  actionId: string;
  idempotencyKey: string;
  effectClass: EffectClass;
  requestHash: string;
  responseHash?: string;
  externalReceiptRef?: string;
  status: 'PREPARED' | 'COMMITTED' | 'FAILED' | 'COMPENSATED';
  preparedAt: string;
  completedAt?: string;
}
```

V34 MUST NOT promise universal rollback for irreversible effects.

---

## 14. Module Model

### 14.1 Module kinds

```text
OBSERVER
GATE
STATE_MACHINE
TRANSFORMER
ASSURANCE_PROVIDER
ROUTER
SCHEDULER
ADAPTER
META_CONTROLLER
```

`EXECUTOR` is reserved for K0-native effect execution and is not available to ordinary modules.

### 14.2 Module contract

```typescript
interface SchemaBoxModule {
  readonly manifest: ModuleManifest;
  readonly handlers?: Partial<Record<LifecyclePhase, ModuleHandler>>;
}
```

### 14.3 Capability-interface dependencies

Dependencies MUST target capabilities, not package names:

```yaml
requires:
  - capability: kernel.event_journal
    version: ^1.0
  - capability: artifact.identity
    version: ^1.0
optional:
  - capability: evidence.epistemic
    version: ^1.0
provides:
  - capability: telos.routing
    version: 1.0.0
```

This permits third-party compatible implementations.

### 14.4 Module failure semantics

```yaml
failureSemantics:
  onUnavailable: REQUIRE_HUMAN
  onTimeout: DEFER
  onInvalidState: FAIL_CLOSED
  onDependencyFailure: DEGRADE
```

Allowed actions:

```text
FAIL_CLOSED
DEFER
DEGRADE
REQUIRE_HUMAN
FALLBACK_TO_SIGNED_ROUTE
```

### 14.5 Module guarantees

Guarantees MUST reference preconditions and evidence:

```yaml
guarantees:
  - guaranteeId: goal.lineage_preserved
    onlyIf:
      - kernel.event_journal.available
      - goal.anchor.sealed
    evidenceRefs:
      - fixture:goal-lineage-v1
nonGuarantees:
  - mathematical_correctness
  - scientific_novelty
```

A manifest field is a declaration, not proof of the guarantee.

---

## 15. Standard Capability Surface

The following twelve names are the recommended developer surface. They are not permanent protocol axioms.

### 15.1 Foundation modules

#### 1. Contract

Provides:

- input and output schema validation;
- semantic field constraints;
- goal/requirement normalization;
- source and target binding hooks.

Default failure:

- external output: fail closed;
- internal candidate: retain with violation record.

#### 2. Evidence

Provides:

- operational and epistemic evidence records;
- source snapshots;
- audit tiers;
- export to OpenTelemetry and evidence ledgers.

Default failure:

- A2/A3 consequential action or release: fail closed;
- A0 exploration: degrade only if Profile permits.

#### 3. Artifact

Provides:

- artifact identity;
- immutable versions;
- lineage;
- transformation receipts;
- access and retention policies.

Default failure:

- unknown identity or hash mismatch blocks replacement and release.

#### 4. Workspace

Provides:

- context/worktree/WASI/container/remote isolation adapters;
- snapshots;
- read/write boundaries;
- teardown and cleanup evidence.

Default failure:

- high-risk execution: fail closed;
- R0 reasoning: may continue without external tools.

### 15.2 Governance modules

#### 5. Telos

Provides:

- sealed objective anchor;
- goal deltas;
- progress and stagnation signals;
- outcome-neutral disposition;
- reframe proposals.

#### 6. Assertion

Provides:

- assertion registry;
- claim atoms;
- alternative assurance support sets;
- profile-defined maturity and release ceilings;
- downgrade and retraction propagation.

#### 7. Trajectory

Provides:

- route and branch lifecycle;
- productive veto;
- reopened obligations;
- repair and replacement lineage;
- negative-knowledge and representation-shift assets.

#### 8. Assurance

Provides:

- proof-kernel, exact-checker, test, simulation, and review adapters;
- target binding;
- verifier/checker hardening;
- reviewer qualification, independence, coverage, and exposure;
- evidence ceilings.

### 15.3 Orchestration modules

#### 9. Federation

Provides:

- model/tool/expert role routing;
- typed handoffs;
- provider/data policy;
- correlation-aware review;
- signed fallback routes.

#### 10. Capacity

Provides:

- capacity envelopes and leases;
- verification reserves;
- epistemic backpressure;
- verification debt;
- overflow and budget requests.

Capacity MUST NOT widen capability scope or lower release standards.

#### 11. Portfolio

Provides:

- program and target portfolios;
- global target deduplication;
- route diversity signatures;
- certificate-economy planning;
- campaign/subepisode accounting;
- minority route retention.

#### 12. Accommodation

Provides:

- competing frame/schema proposals;
- equal-budget tournaments;
- migration and rollback plans;
- compatibility and revalidation requirements.

Accommodation MAY propose change. It MUST NOT self-authorize changes to capability grants, confidentiality, audit duties, or assertion ceilings.

---

## 16. ModuleManifest Normative Shape

```yaml
ModuleManifest:
  moduleId: psi.schemabox.telos
  version: 1.0.0
  implementationRef: "@schemabox/telos"
  kernelCompatibility: ">=0.1.0 <0.2.0"

  moduleKinds:
    - STATE_MACHINE
    - ROUTER

  provides:
    - capability: goal.state
      version: 1.0.0
    - capability: telos.routing
      version: 1.0.0

  requires:
    - capability: kernel.event_journal
      version: ^1.0
    - capability: artifact.identity
      version: ^1.0

  optional:
    - capability: evidence.epistemic
      version: ^1.0

  conflicts: []

  lifecyclePhases:
    - P2_GOAL_PROFILE_CONTEXT_BINDING
    - P3_PLAN_AND_ROUTE_PROPOSAL
    - P8_ASSERTION_AND_SUPPORT_EVALUATION
    - P10_MERGE_COMPACT_STAGNATION_TEARDOWN

  privileges:
    fsRead: []
    fsWrite: []
    network: []
    tools: []
    environment: []

  criticality: CLAIM_CRITICAL

  failureSemantics:
    onUnavailable: REQUIRE_HUMAN
    onTimeout: DEFER
    onInvalidState: FAIL_CLOSED
    onDependencyFailure: DEGRADE

  state:
    schemaRef: schemas/telos_state_v1.json
    migrationRefs: []
    rebuildableFromJournal: true

  events:
    consumes:
      - plan.proposed
      - assertion.proposed
      - progress.window.closed
    emits:
      - telos.signal
      - goal.delta.proposed

  integrity:
    packageDigest: sha256:...
    signatureRef: sigstore:...
    sbomRef: spdx:...
    publisherRef: did:psi:...
    revocationRef: https://registry.example/revocations/...

  guarantees:
    - guaranteeId: goal.lineage_preserved
      onlyIf:
        - kernel.event_journal.available
        - goal.anchor.sealed
      evidenceRefs:
        - fixture:goal-lineage-v1

  nonGuarantees:
    - mathematical_correctness
    - scientific_novelty

  conformance:
    fixtureRefs: []
    threatTestRefs: []
    independentAuditRefs: []
```

The accompanying JSON Schema is included in the V34 package.

---

## 17. Transformer DAG

A transformer MUST declare:

```typescript
interface TransformerSpec {
  moduleId: string;
  consumes: string[];
  produces: string[];
  after: string[];
  before: string[];
  readStatePaths: string[];
  deterministic: boolean;
  idempotent: boolean;
  cacheKeyFields: string[];
  mergeStrategy?: string;
}
```

The compiler MUST reject:

- cycles;
- unresolved input types;
- undeclared artifact writes;
- conflicting successors without a merge strategy;
- transformers that request P6 execution rights;
- mutable access to canonical snapshots.

Sequential execution by user declaration order is non-conformant.

---

## 18. Profiles

A Profile defines domain semantics rather than generic runtime mechanics.

### 18.1 Required Profile fields

```yaml
ProfileManifest:
  profileId: psi.profile.geo-audit
  version: 1.0.0
  domain: GEO
  goalTypes: [...]
  assertionTypes: [...]
  evidenceClasses: [...]
  riskDimensions: [...]
  assertionLatticeRef: ...
  supportSetPolicies: ...
  approvalPoints: [...]
  releaseForms: [...]
  temporalValidityRules: ...
  reviewerQualificationRules: ...
  requiredFixtures: [...]
  nonGuarantees: [...]
```

### 18.2 Research Profile

Defines:

- hypothesis, candidate, tested, corroborated, formally checked, independently reviewed, published, corrected, retracted;
- claim atoms and alternative support sets;
- prior-art state;
- research episode dossier;
- productive veto and route closure;
- formalizer/checker delta.

### 18.3 GEO Profile

Defines:

- monitored query set;
- platform and locale;
- brand/product/entity assertion;
- source citation and retrieval state;
- observation versus causal attribution;
- false or outdated answer correction;
- before/after measurement window;
- public evidence and publisher authority;
- non-guarantee of ranking or recommendation.

### 18.4 Decision Research Profile

Defines:

- decision question and non-goals;
- source classes and temporal cutoffs;
- claim-evidence matrix;
- counterevidence and uncertainty;
- scenario assumptions;
- human review points;
- update and withdrawal semantics;
- action recommendation boundaries.

### 18.5 SchemaDocs Evidence Profile

Defines:

- document passport;
- publisher identity;
- source and license;
- claim atoms;
- version, supersession, contradiction, and withdrawal;
- machine access policy;
- signature and archive state.

### 18.6 Industrial Realization Profile

Defines:

- requirements and operating envelope;
- architecture and interface budgets;
- model credibility and extrapolation;
- test-system qualification;
- configuration baseline;
- manufacturability and supply;
- hazard and reliability case;
- field feedback.

It MUST NOT infer industrial certification from mathematical or software conformance.

---

## 19. Recipe, Adapter, Pack, and Registry

### 19.1 Adapter

An Adapter connects K0 to an external capability:

- model/API;
- browser/search;
- MCP server;
- database;
- document system;
- proof assistant;
- exact checker;
- simulator;
- container/WASI runtime;
- human review queue.

Adapters execute only through K0 authority and MUST declare data egress, credentials, effect classes, retry/idempotency behavior, and receipts.

### 19.2 Recipe

A Recipe is a tested outcome composition. It MUST contain:

- Profile reference;
- required capabilities;
- resolved or resolvable modules;
- adapters;
- configuration;
- fixtures;
- threat tests;
- performance envelope;
- degradation modes;
- guarantees and non-guarantees;
- upgrade and rollback plan.

### 19.3 Pack

A Pack is the commercial/distribution unit:

```text
Modules
+ Adapters
+ Profile
+ Recipes
+ Schemas
+ Fixtures
+ Documentation
+ SBOM
+ Signature
+ License
+ Revocation metadata
```

### 19.4 Registry

A Registry provides:

- discovery;
- publisher identity;
- versions and compatibility;
- signatures and hashes;
- revocation;
- vulnerability status;
- licenses and entitlements;
- conformance reports;
- billing and commercial exchange.

SchemaDocs is the preferred psi.run Registry and Artifact Exchange implementation.

---

## 20. Composition Compiler

### 20.1 Inputs

```typescript
const compilation = await compileComposition({
  recipe,
  profile,
  modules,
  adapters,
  hostAuthority,
  environment,
  trustStore,
});
```

### 20.2 Compilation stages

1. canonicalize manifests;
2. verify signatures and revocations;
3. resolve capability dependencies and versions;
4. detect conflicts;
5. validate Profile requirements;
6. compute effective capability scope;
7. compute risk vector;
8. merge evidence obligations;
9. meet assertion ceilings;
10. compile lifecycle subscriptions;
11. compile transformer DAG;
12. validate event schemas and migrations;
13. derive degradation plan;
14. bind fixtures and threat tests;
15. produce resolved composition and assurance manifest.

### 20.3 Resolved composition

```typescript
interface ResolvedComposition<TAssertion> {
  modules: ResolvedModule[];
  adapters: ResolvedAdapter[];
  phaseGraph: PhaseGraph;
  capabilityScope: CapabilityGrant;
  risk: RiskVector;
  requiredEvidence: EvidenceRequirement[];
  assertionCeiling: TAssertion;
  degradationPlan: DegradationPlan;
  configurationHash: string;
}
```

### 20.4 Composition Assurance Manifest

```typescript
interface CompositionAssuranceManifest {
  recipeId: string;
  profileId: string;
  resolvedModules: string[];
  resolvedAdapters: string[];
  dependencyGraphHash: string;
  lifecyclePlanHash: string;
  configurationHash: string;

  effectiveCapabilityScope: CapabilityGrant;
  finalRisk: RiskVector;
  assertionCeiling: unknown;
  requiredEvidence: EvidenceRequirement[];

  declaredGuarantees: GuaranteeClaim[];
  verifiedGuarantees: VerifiedGuarantee[];
  unverifiedGuarantees: GuaranteeClaim[];
  nonGuarantees: string[];

  fixtureResults: TestResult[];
  threatTestResults: TestResult[];
  degradedModes: DegradedMode[];
  unresolvedConflicts: Conflict[];

  conformanceLevel:
    | 'UNVALIDATED'
    | 'TYPE_CHECKED'
    | 'FIXTURE_TESTED'
    | 'THREAT_TESTED'
    | 'INDEPENDENTLY_REPRODUCED'
    | 'EXTERNALLY_AUDITED';
}
```

The manifest MUST distinguish declared from verified guarantees.

---

## 21. Standalone, Degraded, and Profile-Conformant Use

A module is not simply “independent” or “dependent.”

### 21.1 Standalone

It provides local value without claiming a larger system guarantee.

### 21.2 Degraded

It runs without an optional capability but exposes a lower ceiling or explicit missing guarantee.

### 21.3 Profile-Conformant

The complete Recipe satisfies all mandatory capabilities, evidence obligations, fixtures, and non-bypass conditions required by the Profile.

| Missing capability | Still permitted | Forbidden claim |
|---|---|---|
| Evidence | ephemeral internal processing | auditable or replayable |
| K0 capability authority | R0 pure reasoning | protected external action |
| Telos | bounded transaction | long-horizon goal preservation |
| Assertion | text generation | evidence-layered claim governance |
| Assurance | candidate output | verified result |
| Trajectory | current attempt | reusable route replacement or negative knowledge |
| Artifact registry | temporary bytes | versioned, lineage-bound artifact |
| Durable journal | local prototype | canonical replay and crash recovery |

---

## 22. Failure and Degradation Semantics

| Capability | Default behavior on failure |
|---|---|
| Contract | block external output; preserve internal candidate with violations |
| Evidence | block A2/A3 consequence; allow A0 only if Profile explicitly permits |
| Artifact | block release/replacement when identity or hash is unresolved |
| Workspace | block high-risk execution |
| Telos | pause long-horizon work or ask human; bounded transaction may continue |
| Assertion | block assertion promotion and release |
| Trajectory | block route replacement, closure, and maturity claims lacking lineage |
| Assurance | retain candidate status; do not raise ceiling |
| Federation | use signed fallback path or stop |
| Capacity | hold or reduce; never widen authority |
| Portfolio | stop opening new targets; preserve active verified work |
| Accommodation | retain current frame; do not self-replace |

A failure MUST emit a typed event and declare whether the result is unavailable, degraded, deferred, or denied.

---

## 23. Supply-Chain and Registry Security

A governance module can be more dangerous than an ordinary tool because it influences permission, evidence, or release. Every third-party module or Pack MUST provide:

- publisher identity;
- cryptographic signature;
- content digest;
- SBOM;
- requested privileges;
- network and data-egress declaration;
- lifecycle phases;
- state paths and migrations;
- compatible kernel range;
- fixtures and threat tests;
- license;
- vulnerability and revocation channel;
- rollback version.

### 23.1 Required threat controls

| Threat | Control |
|---|---|
| Load-time side effect | confined loader; no ambient authority |
| Manifest spoofing | canonicalization and signature verification |
| Capability widening | three-way intersection and host approval |
| Hook-order capture | fixed lifecycle and compiled DAG |
| Event tampering | hash-linked durable journal |
| Artifact overwrite | immutable content-addressed versions |
| Guarantee laundering | evidence-linked guarantee maturity |
| Profile confusion | signed Profile identity and compatibility checks |
| Recipe downgrade | explicit degradation manifest and release ceilings |
| Adapter exfiltration | egress policy, DLP, receipts, data minimization |
| Replay divergence | projection hash and migration tests |
| Duplicate external action | idempotency keys and action receipts |
| Module starvation/DoS | timeouts, quotas, criticality-aware failure semantics |
| Correlated assurance | reviewer/model independence graph |

---

## 24. Observability and OpenTelemetry

V34 SHOULD integrate rather than replace generic observability.

```text
OpenTelemetry
    records runtime behavior, latency, errors, resource usage

Schema Sandbox Evidence
    records goal, assertion, evidence, artifact, repair, review, and release meaning
```

Recommended semantic attributes:

```text
sip.goal.id
sip.formulation.id
sip.route.id
sip.branch.id
sip.assertion.id
sip.support_set.id
sip.artifact.version_id
sip.evidence.class
sip.assertion.ceiling
sip.actor.class
sip.model.run_id
sip.human.intervention
sip.assurance.class
sip.repair.relation
sip.capacity.lease_id
sip.action.effect_class
sip.action.receipt_id
sip.recipe.id
sip.profile.id
```

Telemetry MUST NOT be treated as the canonical epistemic state.

---

## 25. Conformance and Maturity

### 25.1 Implementation maturity

| Level | Meaning |
|---|---|
| `M0 EXPERIMENTAL` | interfaces may change; no guarantee |
| `M1 PACKAGED` | manifest, version, schemas, basic unit tests |
| `M2 COMPOSITION_TESTED` | lifecycle, algebra, replay, failure fixtures pass |
| `M3 SIGNED_PROFILE_CONFORMANT` | signatures, SBOM, Profile requirements, durable replay |
| `M4 INDEPENDENTLY_AUDITED` | independent threat review and reproduction |

### 25.2 Reference implementation status at V34 release

| Area | Status | Claim permitted |
|---|---|---|
| Core types | `PROTOTYPED` | architecture-aligned type surface |
| Fixed lifecycle skeleton | `PROTOTYPED` | phase ordering in local prototype |
| Scalar algebra helpers | `PROTOTYPED` | not sufficient for domain assurance |
| Multi-dimensional decision algebra | `SPECIFIED` | no runtime claim yet |
| Runtime capability confinement | `SPECIFIED` | no security-boundary claim |
| Durable event journal | `SPECIFIED` | no replay or crash-recovery claim |
| Immutable artifact registry | `SPECIFIED` | no provenance guarantee yet |
| Module signing and revocation | `SPECIFIED` | no trusted supply-chain claim |
| Profile/Recipe compiler | `SPECIFIED` | no Profile-conformance claim |
| Independent conformance tests | `PLANNED` | no independent assurance claim |

The implementation MUST be described as an **architecture-aligned skeleton prototype** until the P0 requirements in Section 29 are complete.

---

## 26. Conformance Test Suite

### 26.1 Algebra properties

The suite MUST test:

- capability intersection commutativity, associativity, idempotence;
- risk-vector join commutativity, associativity, idempotence;
- evidence-union normalization and idempotence;
- assertion-lattice meet laws;
- adding an unprivileged module cannot widen capability;
- adding a module cannot raise the assertion ceiling;
- removing evidence cannot increase maturity;
- handler completion order does not change gate result.

### 26.2 Journal and artifact properties

- replay of the same event sequence yields the same projection hash;
- corrupted previous-event hash is detected;
- duplicate idempotency key does not duplicate an effect;
- an artifact version cannot be overwritten;
- every transformation has a receipt;
- every released assertion references exact artifact versions;
- migration preserves prior projection reproducibility.

### 26.3 Failure properties

- security-critical timeout fails closed;
- claim-critical timeout blocks release;
- missing evidence journal blocks A2/A3;
- missing Assurance prevents verified status;
- unavailable Accommodation does not alter the active frame;
- Capacity failure cannot widen scope;
- Profile mismatch blocks composition.

### 26.4 Adversarial module tests

- module calls `fetch` directly;
- module writes outside capability scope;
- module mutates context object;
- module forges sequence number or another module ID;
- module submits duplicate action;
- module blocks indefinitely;
- module emits oversized payload;
- module produces a load-time side effect;
- module requests undeclared privilege;
- module claims a guarantee without evidence;
- revoked module is mounted;
- transformer creates an undeclared successor.

---

## 27. Reference Recipes

### 27.1 SchemaDocs Evidence Room Recipe

Required capabilities:

```text
Contract
Evidence
Artifact
Assertion
Trajectory
Publisher Trust / Signing Adapter
```

Primary outcomes:

- document passports;
- publisher and ownership identity;
- claim-to-source binding;
- immutable versions;
- supersession, contradiction, withdrawal;
- API/MCP access;
- licensing and exchange.

Non-guarantees:

- source truth merely because a publisher signed it;
- universal novelty;
- regulatory approval.

### 27.2 GEO Audit Recipe

Required capabilities:

```text
Contract
Evidence
Artifact
Telos
Assertion
Trajectory
Assurance
Portfolio
Search/Browser Adapters
```

Primary outcomes:

- monitored question portfolio;
- platform/locale snapshots;
- brand and product assertion observations;
- cited-source graph;
- error and omission register;
- repair proposals;
- before/after evidence comparison;
- evidence pack publication.

Non-guarantees:

- ranking;
- recommendation;
- causality from one page change;
- permanence across model updates.

### 27.3 Decision Research Dossier Recipe

Required capabilities:

```text
Contract
Evidence
Artifact
Telos
Assertion
Trajectory
Assurance
Federation
Capacity
Portfolio
```

Primary outcomes:

- sealed decision question;
- multi-route research;
- claim-evidence matrix;
- counterevidence and uncertainty;
- expert intervention record;
- decision-ready report;
- update, downgrade, and withdrawal path.

### 27.4 AI Mathematics Research Recipe

Required capabilities:

```text
Contract
Evidence
Artifact
Telos
Assertion
Trajectory
Assurance
Portfolio
Workspace
optional Federation and Capacity
```

Profile-specific controls:

- source/quantifier binding;
- proof versus counterexample certificate class;
- formalizer delta;
- exact-checker hardening;
- reviewer independence and coverage;
- prior-art state;
- campaign/subepisode accounting;
- post-resolution maturation.

The public mathematics case corpus motivates these controls but does not validate V34 as a whole.

---

## 28. Lessons Incorporated from the Mathematics Case Corpus

The mathematics corpus provides high-observability evidence for the following design choices:

| Observed pattern | V34 mechanism |
|---|---|
| One campaign with ten tasks can be overcounted | Portfolio and global target registry |
| Compact counterexamples have lower audit cost than universal proofs | Certificate-economy planning |
| Same-model critique finds defects but is correlated | Federation independence and Assurance coverage |
| A formalizer can replace a proof step | Artifact lineage, TransformationReceipt, Assurance delta |
| A checker can “succeed” while assertions are disabled | exact-checker hardening and action environment capture |
| A route may fail while a downstream kernel survives | Trajectory assets and Accommodation migration |
| Later human proof may support the theorem but not every original step | alternative support sets and result maturation |
| Very large formalization becomes repository engineering | Workspace, Capacity, Artifact, and workload evidence |
| A new representation can unlock progress | Representation-shift trajectory assets |
| Transparent candidate work can remain mathematically unverified | assertion ceiling separate from process provenance |

These mappings are methodological hypotheses and implementation requirements, not evidence that the architecture increases theorem-solving success.

---

## 29. Implementation Roadmap

### P0 — Make the word “trusted” defensible

1. multi-dimensional decision algebra;
2. K0 as the only effect path;
3. runtime removal of ambient authority;
4. durable hash-linked append-only journal;
5. immutable artifact registry and transformation receipts;
6. host × Recipe × module capability intersection;
7. module signature, digest, privilege, and revocation verification;
8. property-based tests for algebra and monotonic consequence safety.

### P1 — Make compositions replayable and explainable

1. state projections and deterministic replay;
2. transformer DAG compiler;
3. implemented failure/degradation semantics;
4. evidence-backed Composition Assurance Manifest;
5. Profile and Recipe compiler;
6. schema migration and rollback;
7. crash recovery;
8. idempotency and external receipts.

### P2 — Connect real products

1. filesystem and object-store adapters;
2. HTTP/API adapter;
3. database adapter;
4. OpenAI, MCP, and LangGraph adapters;
5. OpenTelemetry export;
6. SchemaDocs registry integration;
7. GEO Audit Recipe pilot;
8. Decision Research Dossier pilot.

### P3 — Scale

1. Federation;
2. Capacity leases and verification debt;
3. multi-tenant isolation;
4. enterprise policy adapters;
5. private Registry and Pack distribution.

### P4 — High-risk meta-control

1. Accommodation proposals;
2. equal-budget frame tournaments;
3. migration and revalidation automation;
4. independent red-team and industrial pilots.

---

## 30. Migration from V33 and the Initial Modular Proposal

| Previous construct | V34 treatment |
|---|---|
| S1–S10 | retained as conceptual reference architecture |
| arbitrary `compose()` hook order | replaced by compiled P0–P10 lifecycle |
| `@sip/permission` | policy provider may remain; enforcement moves into K0 |
| `@sip/partition` | becomes Workspace capability plus runtime adapters |
| `@sip/claim` | normative name `Assertion` |
| `@sip/verifier` | normative name `Assurance` |
| `@sip/campaign` | normative name `Portfolio` |
| `@sip/schema-tournament` | normative name `Accommodation`, proposal-only |
| package-name dependencies | capability-interface dependencies |
| “module works independently” | Standalone / Degraded / Profile-Conformant |
| module self-declared guarantee | declared/verified/unverified guarantee separation |
| in-memory journal | non-conformant prototype only |
| `supersedes` field alone | immutable artifact + transformation receipt |
| scalar `maxRisk` | Profile-defined risk vector join |
| scalar `minCeiling` | Profile-defined assertion-lattice meet |
| one decision enum | multi-dimensional governance decision |
| document website | SchemaDocs as Artifact/Pack/Trust Registry |

---

## 31. Commercial and Open Strategy

### 31.1 Open components

Recommended open or standardizable elements:

- SIP core and modular extension schemas;
- lifecycle phases;
- capability-interface vocabulary;
- policy algebra interfaces;
- Module/Profile/Recipe/Pack schemas;
- basic SDK;
- conformance fixtures;
- example Profiles and Recipes;
- signature verification logic.

### 31.2 Proprietary components

Recommended commercial IP:

- hosted K0 control plane;
- enterprise evidence/artifact storage;
- private industry Profiles;
- high-value Recipes and Packs;
- GEO diagnosis rules and query portfolios;
- decision-research quality policies;
- method and failure-pattern libraries;
- industry ontologies;
- customer-specific adapters;
- private deployment, audit, support, and monitoring;
- marketplace trust and commercial services.

### 31.3 Product ladder

```text
Open source: schemas, SDK, local prototype, example Recipes
Professional: hosted Evidence / Artifact / Assertion / Telos services
Enterprise: private K0, SSO, policy, audit, data connectors, support
Industry: GEO, research, legal, industrial, bio-evidence Packs
Ecosystem: SchemaDocs Registry, publisher trust, licensing, marketplace
```

### 31.4 Near-term product priority

The first implementation should serve existing products:

1. SchemaDocs Evidence Room;
2. GEO Audit and Evidence Pack;
3. Decision Research Dossier.

They generate real customers, artifacts, failure data, and regression fixtures before a general-purpose platform is marketed.

---

## 32. Non-Goals and Explicit Limitations

V34 does not claim:

- a complete secure microkernel implementation;
- proof that modules cannot escape without runtime confinement;
- formal verification of the policy algebra;
- scientific discovery superiority;
- industrial certification;
- universal rollback of external effects;
- automatic novelty determination;
- independence merely from multiple model calls;
- that a signed Pack is safe or correct merely because it is signed;
- that a Profile is valid outside its declared scope;
- that a large number of modules implies a stronger system.

V34 deliberately postpones:

- self-authorized schema evolution;
- broad industrial autonomy;
- open marketplace launch before trusted supply exists;
- universal scoring across validity, safety, novelty, and business value.

---

## 33. Release Criteria for a “Trusted Microkernel” Claim

The reference implementation MUST NOT be called a trusted microkernel until all of the following are demonstrated:

1. ordinary modules cannot perform external effects outside K0;
2. capability scopes are canonicalized and enforced at runtime;
3. consequential actions require authorization tickets and receipts;
4. the journal is durable, append-only, hash-linked, and replayable;
5. artifact versions are immutable and transformations have receipts;
6. algebra property tests pass;
7. crash recovery and duplicate-action prevention are demonstrated;
8. signatures, revocation, and privilege declarations are enforced;
9. at least one Profile/Recipe passes fixture and threat tests;
10. an independent reviewer reproduces the stated guarantees.

Until then, the correct designation is:

> **V34 architecture-aligned modular knowledge-system prototype.**

---

## 34. Conclusion

V33 established the breadth of the Schema Sandbox methodology. The initial modular proposal made it adoptable. V34 makes modularity compatible with trust.

The decisive change is not the number of packages. It is the introduction of:

```text
small trusted kernel
+ fixed lifecycle
+ multi-dimensional policy algebra
+ event-sourced canonical knowledge state
+ immutable artifact lineage
+ governed external-effect transactions
+ Profile-defined semantics
+ tested Recipe delivery
+ signed Pack supply chain
+ Registry-based trust and exchange
```

The resulting system can be understood at three levels:

1. **Methodology:** preserve goals, separate candidates from released claims, retain negative knowledge, and track evidence maturity.
2. **Architecture:** ensure modules cannot bypass authority, overwrite history, or manufacture guarantees through composition order.
3. **Business system:** turn reusable professional capability into testable Recipes, distributable Packs, and trusted artifacts exchanged through SchemaDocs.

The long-term category is therefore not merely “an agent framework.” It is:

> **a modular knowledge system and professional AI capability operating layer in which goals, assertions, evidence, artifacts, repairs, reviews, and consequences remain governed across heterogeneous models and tools.**

---

# Appendix A. Reference TypeScript Interfaces

```typescript
export type LifecyclePhase =
  | 'P0_MODULE_LOAD_AND_ATTEST'
  | 'P1_INPUT_NORMALIZATION'
  | 'P2_GOAL_PROFILE_CONTEXT_BINDING'
  | 'P3_PLAN_AND_ROUTE_PROPOSAL'
  | 'P4_ACTION_GOVERNANCE'
  | 'P5_ACTION_PREPARE_AND_INTENT_COMMIT'
  | 'P6_KERNEL_ACTION_EXECUTION'
  | 'P7_RESULT_ARTIFACT_EVIDENCE_REGISTRATION'
  | 'P8_ASSERTION_AND_SUPPORT_EVALUATION'
  | 'P9_RELEASE_GOVERNANCE_AND_STATE_COMMIT'
  | 'P10_MERGE_COMPACT_STAGNATION_TEARDOWN';

export type ModuleKind =
  | 'OBSERVER'
  | 'GATE'
  | 'STATE_MACHINE'
  | 'TRANSFORMER'
  | 'ASSURANCE_PROVIDER'
  | 'ROUTER'
  | 'SCHEDULER'
  | 'ADAPTER'
  | 'META_CONTROLLER';

export type FailureAction =
  | 'FAIL_CLOSED'
  | 'DEFER'
  | 'DEGRADE'
  | 'REQUIRE_HUMAN'
  | 'FALLBACK_TO_SIGNED_ROUTE';

export type Criticality =
  | 'ADVISORY'
  | 'OPERATION_CRITICAL'
  | 'CLAIM_CRITICAL'
  | 'SECURITY_CRITICAL';

export interface CapabilityRef {
  capability: string;
  version: string;
}

export interface PrivilegeRequest {
  fsRead: string[];
  fsWrite: string[];
  network: string[];
  tools: string[];
  environment: string[];
}

export interface ModuleManifest {
  moduleId: string;
  version: string;
  implementationRef: string;
  kernelCompatibility: string;
  moduleKinds: ModuleKind[];
  provides: CapabilityRef[];
  requires: CapabilityRef[];
  optional: CapabilityRef[];
  conflicts: CapabilityRef[];
  lifecyclePhases: LifecyclePhase[];
  privileges: PrivilegeRequest;
  criticality: Criticality;
  failureSemantics: Record<string, FailureAction>;
  integrity: {
    packageDigest: string;
    signatureRef: string;
    sbomRef: string;
    publisherRef: string;
    revocationRef: string;
  };
  guarantees: GuaranteeClaim[];
  nonGuarantees: string[];
}

export interface GuaranteeClaim {
  guaranteeId: string;
  onlyIf: string[];
  evidenceRefs: string[];
}

export interface ModuleProposal {
  decisions?: Partial<GovernanceDecision<unknown>>;
  proposedEvents?: ProposedEvent[];
  proposedArtifacts?: ProposedArtifact[];
  proposedActions?: ActionProposal[];
}

export interface SchemaBoxModule {
  readonly manifest: ModuleManifest;
  readonly handlers?: Partial<Record<LifecyclePhase, ModuleHandler>>;
}

export type ModuleHandler = (
  context: ModuleContext
) => Promise<ModuleProposal> | ModuleProposal;
```

# Appendix B. Example Composition Assurance Manifest

```yaml
recipeId: psi.recipe.geo-audit
profileId: psi.profile.geo-audit
resolvedModules:
  - psi.schemabox.contract@1.0.0
  - psi.schemabox.evidence@1.0.0
  - psi.schemabox.artifact@1.0.0
  - psi.schemabox.telos@1.0.0
  - psi.schemabox.assertion@1.0.0
  - psi.schemabox.trajectory@1.0.0
  - psi.schemabox.assurance@1.0.0
  - psi.schemabox.portfolio@1.0.0
resolvedAdapters:
  - psi.adapter.browser@0.2.0
  - psi.adapter.search@0.2.0
dependencyGraphHash: sha256:...
lifecyclePlanHash: sha256:...
configurationHash: sha256:...

effectiveCapabilityScope:
  fsRead: []
  fsWrite: ["artifact://geo-workspace/*"]
  network: ["https://approved-search.example/*"]
  tools: ["browser.observe", "search.query"]

finalRisk:
  confidentiality: MEDIUM
  integrity: HIGH
  irreversibility: LOW
  financial: LOW
  physicalSafety: LOW
  claimCriticality: HIGH
  regulatory: MEDIUM

assertionCeiling: OBSERVATIONAL_AUDIT
requiredEvidence:
  - platform_snapshot
  - query_definition
  - response_capture
  - citation_capture
  - source_version

declaredGuarantees:
  - guaranteeId: observations_are_traceable_to_captured_responses
verifiedGuarantees: []
unverifiedGuarantees:
  - guaranteeId: observations_are_traceable_to_captured_responses
nonGuarantees:
  - ranking_improvement
  - causal_attribution
  - permanent_model_behavior
conformanceLevel: TYPE_CHECKED
```

# Appendix C. Package Contents

The V34 release package SHOULD contain:

```text
docs/
  internal_kb_schema_sandbox_V34_MKS_EN.md
  internal_kb_schema_sandbox_V34_MKS_CN.md
  V34_RELEASE_NOTES_CN.md
  V33_TO_V34_MIGRATION_CN.md
schemas/
  module_manifest.schema.json
  profile_manifest.schema.json
  recipe_manifest.schema.json
  pack_manifest.schema.json
  kernel_event.schema.json
  artifact_record.schema.json
  action_receipt.schema.json
  composition_assurance_manifest.schema.json
examples/
  evidence_module_manifest.json
  geo_profile.json
  geo_audit_recipe.json
  geo_composition_assurance.json
  kernel_event.json
  artifact_record.json
  action_receipt.json
  geo_pack_manifest.json
tests/
  VALIDATION_REPORT.txt
  SHA256SUMS.txt
```
