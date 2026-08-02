# ProofFlow Schema Sandbox — Architecture & Module Specifications

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

## 2. K0 Trust Kernel Invariants

1. **Fixed Lifecycle (P0–P10)**:
   - P0 `LOAD_ATTEST` → P1 `INPUT_NORMALIZATION` → P2 `GOAL_BINDING` → P3 `PLAN_PROPOSAL` → P4 `ACTION_AUTH` → P5 `EXECUTION` → P6 `ARTIFACT_RECORDING` → P7 `ASSERTION_EVALUATION` → P8 `RELEASE_AUTH` → P9 `ATOMIC_COMMIT` → P10 `TEARDOWN_COMPACT`.

2. **Decision Algebra**:
   - `DENY > REQUIRE_HUMAN > DEFER > REQUIRE_EVIDENCE > ALLOW`
   - Capability Range = $\text{Cap}_1 \cap \text{Cap}_2$
   - Risk Level = $\max(\text{Risk}_i)$
   - Evidence Required = $\bigcup \text{Req}_i$

3. **Atomic Transactions & Sourcing**:
   - Canonical append-only SHA-256 chained JSONL event log (`events.jsonl`).
   - SQLite projection databases are 100% rebuildable CQRS projections.

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
