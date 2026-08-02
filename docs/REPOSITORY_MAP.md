# Repository Map — ProofFlow `0.1.0-alpha.4`

```text
.
├── apps/
│   ├── api/schemamath_api/
│   │   ├── api.py              # backward-compatible FastAPI plus Alpha.4 endpoints
│   │   ├── domain.py           # versioned Pydantic contracts
│   │   ├── event_store.py      # canonical append-only JSONL and hash chain
│   │   ├── plugin_host.py      # generalized plugin discovery and execution host
│   │   ├── plugin_runner.py    # compatible python.local process runner
│   │   ├── projection.py       # migrations and rebuildable SQLite views
│   │   └── service.py          # domain policy and orchestration
│   └── web/
│       ├── src/                # React Flow + Excalidraw application
│       ├── dist/               # validated production build
│       └── package-lock.json   # reproducible frontend dependency lock
├── prototype/                  # retained Alpha.2 dependency-free UI
├── plugins/builtin/
│   ├── python.local/
│   └── graphviz.local/
├── schemas/                    # 24 runtime and 4 baseline JSON Schemas
├── api/                        # generated OpenAPI JSON/YAML
├── scripts/                    # validation, export, demo and release tools
├── tests/                      # 28 service/API/regression tests
├── docs/                       # plans, release, migration and acceptance notes
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

Alpha.4 adds diagnostics and recovery safeguards; it does not rewrite historical events.
