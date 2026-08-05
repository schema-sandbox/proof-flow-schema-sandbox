# Repository Map — ProofFlow `0.1.0-alpha.5`

Snapshot: Alpha.5 working tree appended to `e77d79d6f5f009b7f5c601a0b37918e4a040c2d3`, audited 2026-08-03.

```text
.
├── apps/
│   ├── api/schemamath_api/
│   │   ├── api.py              # backward-compatible FastAPI plus Alpha.5 control-plane endpoints
│   │   ├── domain.py           # versioned Pydantic contracts
│   │   ├── event_store.py      # canonical append-only JSONL, hash chain, atomic batches and idempotency
│   │   ├── k0/                 # lifecycle, decision, manifest, replay, transaction SDK
│   │   ├── sip/                # 12 composable foundation/governance/orchestration modules
│   │   ├── plugin_host.py      # generalized plugin discovery and execution host
│   │   ├── plugin_runner.py    # compatible python.local process runner
│   │   ├── projection.py       # migrations and rebuildable Alpha.5 evidence/state views
│   │   ├── service.py          # current production domain policy and orchestration
│   │   └── main.py             # serves optional generated _ui assets or text fallback
│   └── web/
│       ├── src/                # React Flow + Excalidraw application
│       ├── dist/               # generated, locally validated production build
│       └── package-lock.json   # reproducible frontend dependency lock
├── prototype/                  # retained Alpha.2 dependency-free UI
├── plugins/builtin/
│   ├── python.local/
│   └── graphviz.local/
├── schemas/                    # 72 JSON Schema documents (67 exported runtime models)
├── api/                        # generated OpenAPI JSON/YAML, 72 paths at the snapshot
├── scripts/                    # validation, export, demo and release tools
├── tests/                      # regression suite plus Alpha.5 negative/vertical-slice tests
├── docs/                       # history plus v0.14 requirements/audit/plan/matrix
├── examples/                   # design examples and Alpha.2 .smath regression package
├── package_manifest.json
└── SHA256SUMS.txt
```

## Canonical versus derived state

- `events/events.jsonl`: canonical observable research history;
- `project.json`: project identity, source problem and current summary;
- `blobs/sha256/`: immutable canonical artifact bytes addressed by SHA-256;
- `database/projections.sqlite3`: derived query projection, safe to rebuild;
- `runs/`: plugin working directories and observable metadata;
- `plugins/plugins.lock.json`: project plugin version/lifecycle lock;
- `exports/`: generated Research Packets and `.smath.zip` bundles.

Alpha.5 adds diagnostics, atomic transition records and recovery safeguards; it does not rewrite historical events.

## Current execution surfaces

Alpha.5 has two related but different execution surfaces:

- the shipped FastAPI service calls `EventStore` and `ProjectionStore` directly;
- K0/SIP is a composable SDK/CLI/test surface and is not yet the mandatory path for every REST write.

Consequently, a SIP module being present does not yet prove that its gate governs every legacy REST
write. New transition/evidence commands use the Alpha.5 revisioned event boundary; legacy commands
remain compatible surfaces until a future major tightening.

## v0.14 / Alpha.5 documents

- [Theory requirements](V0_14_THEORY_REQUIREMENTS_CN.md)
- [Target architecture](ARCHITECTURE.md)
- [Software audit](V0_14_SOFTWARE_AUDIT_CN.md)
- [Alpha.5 upgrade plan](ALPHA_5_UPGRADE_PLAN_CN.md)
- [Alpha.5 acceptance matrix](ALPHA_5_ACCEPTANCE_MATRIX_CN.md)
- [Alpha.5 implementation report](ALPHA_5_IMPLEMENTATION_REPORT_CN.md)

Historical Alpha.1–Alpha.4 release and migration documents remain unchanged records of their original
scope; the v0.14 documents do not retroactively claim those capabilities.
