# ProofFlow Schema Sandbox — Architecture & Module Specifications

> Implementation status: Alpha.5 adds the revisioned command/event boundary,
> four-plane transition records, typed continuation/handoff contracts and
> evidence/verification projections. Legacy Alpha.4 routes and event lines stay
> readable; direct legacy service commands remain compatibility surfaces while
> new Alpha.5 records use schema `0.6`. See the normative
> [v0.14 requirements](V0_14_THEORY_REQUIREMENTS_CN.md),
> [software audit](V0_14_SOFTWARE_AUDIT_CN.md), and
> [Alpha.5 plan](ALPHA_5_UPGRADE_PLAN_CN.md).

## 1. High-Level Architecture Overview

ProofFlow is structured around a **K0 Trust Kernel** and **12 Lego-like Composable Modules** (`@sip/*`).

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ProofFlow Architecture                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  K0 Trust Kernel:  Identity, Grants, P0-P10 Lifecycle, Decision Algebra,    │
│                    Transaction Executor, Replay Engine                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Foundation (🧱):  F1: @sip/contract    F2: @sip/evidence                   │
│                    F3: @sip/permission  F4: @sip/partition                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Governance (🏗️):  G1: @sip/telos       G2: @sip/claim                      │
│                    G3: @sip/trajectory  G4: @sip/verifier                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Orchestration(🌐):O1: @sip/federation  O2: @sip/capacity                   │
│                    O3: @sip/campaign    O4: @sip/schema-tournament          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. K0 Trust Kernel Invariants and Current Boundary

1. **Fixed Lifecycle (P0–P10)**:
   - P0 `LOAD_ATTEST` → P1 `INPUT_NORMALIZATION` → P2 `GOAL_BINDING` → P3 `PLAN_PROPOSAL` → P4 `ACTION_AUTH` → P5 `EXECUTION` → P6 `ARTIFACT_RECORDING` → P7 `ASSERTION_EVALUATION` → P8 `RELEASE_AUTH` → P9 `ATOMIC_COMMIT` → P10 `TEARDOWN_COMPACT`.

2. **Decision Algebra**:
   - `DENY > REQUIRE_HUMAN > DEFER > REQUIRE_EVIDENCE > ALLOW`
   - Capability Range = $\text{Cap}_1 \cap \text{Cap}_2$
   - Risk Level = $\max(\text{Risk}_i)$
   - Evidence Required = $\bigcup \text{Req}_i$

3. **Target Atomic Transactions & Sourcing**:
   - Canonical append-only SHA-256 chained JSONL event log (`events.jsonl`).
   - SQLite projection databases are 100% rebuildable CQRS projections.

The hash chain and rebuildable projection are implemented in Alpha.4. Alpha.5
adds a single filesystem-replacement boundary for EventStore batches, including
full pre-validation, optimistic revision checks and idempotent retries. The K0
executor now uses that boundary for canonical events. Arbitrary legacy
`state_mutations` callbacks remain derived/in-memory hooks and are not treated as
durable transactional state; canonical replay remains the recovery source.

---

## 3. Composable Module Matrix

| Module | Level | Purpose | Phase Hook |
|:---|:---|:---|:---|
| `@sip/contract` | Foundation (F1) | JSON Schema Input/Output validation & fallback | P1, P8 |
| `@sip/evidence` | Foundation (F2) | Audit log retention & Markdown report export | P6, P9 |
| `@sip/permission` | Foundation (F3) | Scope & whitelist fences (`fs`, `net`, `tools`) | P4 |
| `@sip/partition` | Foundation (F4) | Process & Container workspace isolation | P5, P10 |
| `@sip/telos` | Governance (G1) | Goal anchoring, drift detection & stagnation alerts | P2 |
| `@sip/claim` | Governance (G2) | Claim envelope maturity & human-confirmation invariants | P7 |
| `@sip/trajectory` | Governance (G3) | Trajectory logging & failure assetization | P3, P6 |
| `@sip/verifier` | Governance (G4) | Verifier adapters & mutation hardening checks | P7 |
| `@sip/federation` | Orchestration (O1) | Peer identity, correlation and scoped delegation | P3, P4 |
| `@sip/capacity` | Orchestration (O2) | Token/tool quota and verification-debt limits | P3, P8 |
| `@sip/campaign` | Orchestration (O3) | Attempt portfolio, target denominator and campaign lineage | P2, P9 |
| `@sip/schema-tournament` | Orchestration (O4) | Competing schema/proposal comparison without automatic release | P3, P7 |

In Alpha.4 these modules form a library/SDK design surface and are mostly
in-memory. The table describes their intended lifecycle responsibilities; it
does not imply that every REST endpoint is already governed by those hooks.

---

## 4. v0.14 Target: Four Research-State Planes

The next architecture must not represent research maturity with one global
status. It separates four coordinates whose transitions can occur independently.

| Plane | Stored question | Examples of accepted evidence |
|:---|:---|:---|
| Operational | Who owns the next bounded action, what is blocked, and may work continue? | gates, todos, leases, human instructions, continuation decisions |
| Epistemic | What is known, excluded, retained, uncertain, or reformulated? | counterexamples, dead-end constraints, bridge results, prior-art updates |
| Claim | What exact proposition is supported, refuted, reviewed, or still open? | claim atoms, source binding, check results, reviews, corrections |
| Artifact | Is an artifact draft, broken, repaired, superseded, released, or withdrawn? | hashes, build logs, repair lineage, repository snapshots |

An event that changes one plane must leave the other planes unchanged unless
their deltas are separately proposed and accepted. A successful build is an
artifact/verification observation; it is not by itself a natural-language claim
transition.

## 5. v0.14 Target: Accepted-Transition Pipeline

```text
provider/tool/model/human observation
    → typed transition proposal
    → evidence and authority validation
    → optimistic-revision and idempotency checks
    → accepted or rejected delta
    → atomic event append
    → read-only projection update
    → typed continuation decision
```

The canonical unit is an accepted delta, not private chain of thought. Proposed
changes must carry trigger evidence, proposer identity, acceptance basis,
rejected components, new obligations and visibility. A rejected proposal stays
auditable without changing durable state.

The fixed P0–P10 lifecycle remains in force. v0.14 refines its boundaries:

- P3 may create proposals, routes and handoff candidates, but cannot commit them;
- P6 records raw observations and immutable artifacts;
- P7 evaluates exact evidence and state-transition predicates;
- P8 decides release and continuation authority separately;
- P9 atomically commits only accepted deltas against an expected revision;
- P10 emits a handoff/continuation receipt and records `NO_CHANGE` when needed.

## 6. v0.14 Target: Core Records

The next schema family adds or strengthens the following records:

| Record | Purpose |
|:---|:---|
| `ClaimAtom` | Exact source/version/scope plus vector-valued evidence maturity |
| `ResearchStateTransition` | Four-plane proposal, acceptance basis and accepted delta |
| `ContinuationContract` | `RUN_NEXT`, `WAIT`, `REDIRECT`, `ASK_HUMAN`, `STOP`, or `NO_CHANGE` |
| `HandoffPacket` | Scope, reachable artifacts, facts, failed routes, obligations and next predicate |
| `EvidenceCard` | Six orthogonal evidence dimensions without one aggregate score |
| `VerificationExecutionManifest` | Exact command, environment, checks executed and negative mutations |
| `FormalCoverageBinding` | Headline/claim-to-module/configuration/theorem/definition coverage |
| `RepositorySnapshot` | URL/ref/commit/observation time/parent and succession relation |
| `RepairLineage` | Transcription, completion, repair, replacement or retargeting relation |
| `AttemptRecord` and `CostVector` | Full denominator, no-change turns and lifecycle cost coordinates |
| `ResearchEpisodeDossier` | Source-attributed publication projection over canonical records |

Existing Alpha.4 records remain readable. Legacy free text is not promoted to
accepted state automatically; it is projected as unclassified or
author-reported until a human or deterministic mechanism accepts a scoped delta.

## 7. v0.14 Target: Claim and Evidence Boundary

ProofFlow uses a six-dimensional evidence card:

1. process provenance;
2. artifact availability;
3. deterministic verification;
4. independent review;
5. novelty and prior art;
6. autonomy and attribution.

The dimensions are not collapsed into one score. Review lineage and artifact
correlation must remain visible: a manuscript, reconstructed process narrative,
checker and formal proof produced by the same model or institution are
complementary but not independent by count.

## 8. v0.14 Target: Formal Verification Boundary

A formal release is modeled as a coverage graph:

```text
public headline
  → manuscript claim atom
  → solution module
  → declared main result
  → trusted challenge / Comparator configuration
  → named theorem and definition bindings
  → axiom policy, kernel result and second-kernel execution
```

Repository existence, a top-level build, main-result registration and named
Comparator coverage are different evidence claims. Challenge placeholders are
separate from solution placeholders. “Configured” is separate from “executed”
and from “independently reproduced”. Every executable checker must fail closed,
record the checks that actually ran and include negative mutations that must
fail.

## 9. v0.14 Target: Repository and Projection Provenance

Repository evidence stores URL, branch/tag, resolved commit, observation time,
parent count, prior audited commit and the relation between snapshots. A new
root or branch pointer is first an Artifact State transition; it does not imply
a mathematical correction.

Every dashboard, dossier, paper export or status summary is a projection with:

- the canonical event revision it represents;
- source event and artifact references;
- derivation class (raw, derived, rewritten, retrospective or final-only);
- a drift check against the current canonical revision.

## 10. Compatibility and Release Invariants

1. Alpha.1–Alpha.4 events are never rewritten to manufacture v0.14 fields.
2. `UNRESOLVED`, failed and no-change outcomes remain valid.
3. Missing control-plane or verification evidence is `unknown`, not inferred.
4. Release packages are built from a clean, declared source set and bind schema,
   OpenAPI, UI, manifest, checksums and repository commit.
5. A release dossier must disclose uncovered claims, missing attempts, correlated
   review and unexecuted verification configurations.
