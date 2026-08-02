# ProofFlow Schema Sandbox

**Version:** `0.1.0-alpha.4`  
**Short name:** ProofFlow  
**Status:** local-first experimental mathematics research sandbox

ProofFlow preserves observable mathematical research trajectories. It is not a
guaranteed solver, does not claim access to hidden model reasoning, and never
automatically marks a project solved. `UNRESOLVED` is a first-class outcome;
objections remain easy while certified route closure intentionally requires
strong evidence and a human actor.

## Active development root

This directory is the single active ProofFlow codebase. Make all future
changes, tests, manifests, checksums, and releases here. The adjacent
versioned Alpha.2/Alpha.3/Alpha.4 folders and theory materials are retained as
read-only historical or design references; the release builder excludes them.

## Alpha.4

- Added a read-only `.smath.zip` import preflight that reports archive safety,
  schema compatibility, event-chain integrity and missing artifact blobs before
  a project is copied into a workspace.
- Added registered SQLite projection migrations and an observable projection
  schema version.
- A broken canonical JSONL chain now locks further appends, preserving a
  recoverable read-only state instead of extending corrupt history.

## Alpha.3 foundation

- Append-only, SHA-256-chained JSONL events remain canonical; SQLite remains a
  rebuildable projection.
- Generalized, project-scoped plugin host with explicit install, health, enable,
  disable and uninstall lifecycle. No silent network installation.
- Bundled `python.local` process runner and optional `graphviz.local` command
  adapter. Raw inputs, logs, failures and outputs are retained as artifacts.
- `ModelSession`, `HandoffArtifact` and preview-only `ArenaRecipe` contracts.
  Same-family model reviews are warned as correlated, not counted as independent
  verification.
- Typed epistemic deltas and historical retrieval across routes, objections,
  bridges, dead ends and handoffs, including route-similarity hints.
- Production React Flow and Excalidraw dual canvas at `/app/`. Excalidraw scenes
  are immutable content-addressed artifacts; machine interpretations are stored
  separately and only humans can confirm mappings into the research graph.
- Alpha.2 `.smath.zip` import compatibility and replay are covered by regression
  tests. Historical events are never rewritten.

## Run locally

Python 3.12+ and Node.js 20+ are recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
npm ci --prefix apps/web
npm run build --prefix apps/web
.\.venv\Scripts\python.exe -m uvicorn schemamath_api.main:app --app-dir apps/api --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/app/`. API docs are at `/docs`; the Alpha.2
dependency-free prototype remains available at `/prototype/`.

ProofFlow-prefixed environment variables are preferred:
`PROOFFLOW_WORKSPACE`, `PROOFFLOW_PLUGIN_ROOT`,
`PROOFFLOW_MAX_UPLOAD_BYTES`, `PROOFFLOW_MAX_CHAT_IMPORT_CHARS`,
`PROOFFLOW_MAX_PLUGIN_OUTPUT_BYTES`, and
`PROOFFLOW_MAX_PLUGIN_OUTPUT_FILES`. Their `SCHEMAMATH_*` Alpha.2 aliases remain
supported for compatibility.

## Validate

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
.\.venv\Scripts\ruff.exe check apps/api tests scripts
.\.venv\Scripts\python.exe scripts/validate_schemas.py
npm run build --prefix apps/web
npm audit --prefix apps/web --audit-level=high
```

See [Alpha.4 release notes](docs/ALPHA_4_RELEASE_NOTES_CN.md),
[migration notes](docs/MIGRATION_ALPHA3_TO_ALPHA4_CN.md), and
[validation report](VALIDATION_REPORT.txt).

## Security boundary

The local process runners are not an OS security sandbox and inherit the local
user's authority. Run only trusted code and keep the API bound to localhost.
OCI manifests must use digest-pinned images, but container availability and
security configuration remain an operator responsibility. Tools are installed
only when needed; an unavailable optional tool is reported honestly.

License: Apache-2.0.
