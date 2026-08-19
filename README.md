# ProofFlow Schema Sandbox

**Version:** `0.1.0-alpha.8`  
**Short name:** ProofFlow  
**Status:** local-first experimental mathematics research sandbox

ProofFlow is a local-first, human-guided sandbox for experimental mathematics
research. It tracks a project the way it actually unfolds — routes, dead ends,
objections, and bridges — as an append-only, SHA-256-chained event stream that
can be replayed and audited.

ProofFlow does not promise to solve problems. It does not claim access to hidden
model reasoning, and it never automatically marks a project "solved."
`UNRESOLVED` is a first-class outcome. Objections are cheap to raise; a certified
route closure deliberately requires strong evidence and a human actor.

## Why ProofFlow

- **Observable**: research is captured as an event stream you can replay and
  audit, not a black-box answer.
- **Honest**: `UNRESOLVED` is a first-class outcome. Objections stay cheap;
  certified closure is deliberately expensive and requires a human.
- **Human in the loop**: models can propose, but only a human confirms mappings
  and state transitions.

## Who it is for

- Mathematicians who want LLM assistance without losing the decision trail.
- Formal-verification and Lean-adjacent researchers.
- Anyone studying how AI reasoning on hard problems actually unfolds.

## Alpha.6

- Fail-closed security guard on non-loopback network interfaces preventing unauthenticated remote execution.
- Strict content-addressed blob verification across all artifact reads, archive imports, and project integrity reports.
- Zero npm vulnerabilities in frontend production bundle with upgraded DOMPurify and Mermaid.
- Built-in plugins (`graphviz.local`, `python.local`) packaged in wheel distribution and container images.
- Complete third-party SBOM notices in `THIRD_PARTY_NOTICES.md`.

## Alpha.5

- Atomic revisioned/idempotent event batches and accepted/rejected four-plane research-state transitions.
- Typed continuation contracts, V2 handoff receipts, ClaimAtom proposals, six-dimensional evidence cards and review lineage.
- Verification execution manifests, coverage bindings, repository snapshots, repair lineage, typed attempts/costs and 27-field dossier V2.
- `/app/` now summarizes the four research planes, transition proposals, claims and evidence inventory.

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

## Paper v0.14 and the Alpha.5 boundary

`From_Prompt_to_Proof_v0.14.md` introduces four independent research-state
planes, accepted state transitions, typed continuation decisions,
evidence-backed handoffs, claim-to-certificate coverage and repository snapshot
lineage. These are the Alpha.5 control-plane requirements; Alpha.4 behavior
remains readable and is not rewritten.

See the [v0.14 alignment requirements](docs/V0_14_THEORY_REQUIREMENTS_CN.md)
and [target architecture](docs/ARCHITECTURE.md). Alpha.4 remains strongest at
trajectory retention; Alpha.5 adds the transition acceptance, continuation
control, vector-valued claim evidence and formal-release coverage control plane.
External Lean, dependency and clean-release evidence remains a separate
release gate and is never inferred from local static checks.

See the [v0.14 software audit](docs/V0_14_SOFTWARE_AUDIT_CN.md),
[Alpha.5 upgrade plan](docs/ALPHA_5_UPGRADE_PLAN_CN.md), and
[Alpha.5 acceptance matrix](docs/ALPHA_5_ACCEPTANCE_MATRIX_CN.md) for the audit
trail and release gates. Legacy Alpha.1–Alpha.4 events remain readable; new
writes use schema `0.6` and are append-only.
The [Alpha.5 implementation report](docs/ALPHA_5_IMPLEMENTATION_REPORT_CN.md)
records local verification and the external evidence boundary.

## Run locally

Python 3.12+ and Node.js 20+ are recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
npm ci --prefix apps/web
npm run build --prefix apps/web
.\.venv\Scripts\python.exe -m uvicorn schemamath_api.main:app --app-dir apps/api --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/app/` (explore desk). API docs are at `/docs`.

### Two HTTP UIs

| URL | Role |
|-----|------|
| `/app/` (default) | Explore desk: dual canvas, search, deltas, create project, export, integrity |
| `/prototype/` | Full workbench: route state changes, challenges, bridges, dead ends, plugins, chat import |

They share the same API and optional `sessionStorage` API key (`proofflow_api_key`).
Use **打开工作台** on a project to deep-link `/prototype/?project=<id>`.
Exports use authenticated `fetch` + blob download so production API keys are sent.

The API resolves the frontend from both a source checkout and a bundled wheel
(`schemamath_api/_ui`). If no frontend bundle is present the root route serves a
plain-text note pointing here rather than redirecting to a missing page.

For the hardened container profile, copy `.env.production.example` to a protected
`.env.production` file, replace both placeholders, and run:

```powershell
docker compose --env-file .env.production -f docker-compose.prod.yml up --build
```

The production profile persists `/data`, requires API authentication, binds the
published port to loopback, and disables local process plugins. The `/app/` UI
prompts for an API key after a 401 and keeps it only in the current browser session.

ProofFlow-prefixed environment variables are preferred:
`PROOFFLOW_ENV`, `PROOFFLOW_WORKSPACE`, `PROOFFLOW_PLUGIN_ROOT`,
`PROOFFLOW_MAX_UPLOAD_BYTES`, `PROOFFLOW_MAX_CHAT_IMPORT_CHARS`,
`PROOFFLOW_MAX_PLUGIN_OUTPUT_BYTES`, and
`PROOFFLOW_MAX_PLUGIN_OUTPUT_FILES`. `PROOFFLOW_ENV=production` switches to
fail-closed behavior. Production additionally requires
`PROOFFLOW_SECRET_KEY` and `PROOFFLOW_API_KEYS`, and accepts
`PROOFFLOW_AUTH_ENABLED`, `PROOFFLOW_ALLOW_LOCAL_PLUGINS`, and
`PROOFFLOW_MAX_IMPORT_BYTES`. Their `SCHEMAMATH_*` Alpha.2 aliases remain
supported for compatibility.

## Validate

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
.\.venv\Scripts\ruff.exe check apps/api tests scripts
.\.venv\Scripts\python.exe scripts/validate_schemas.py
.\.venv\Scripts\python.exe scripts/export_runtime_schemas.py
.\.venv\Scripts\python.exe scripts/export_k0_schemas.py
.\.venv\Scripts\python.exe scripts/export_openapi.py
npm run build --prefix apps/web
npm audit --prefix apps/web --audit-level=high
python scripts/stage_wheel_ui.py
python -m pip wheel . --no-deps --no-build-isolation -w /tmp/proofflow-wheel
```

See [Alpha.4 release notes](docs/ALPHA_4_RELEASE_NOTES_CN.md),
[migration notes](docs/MIGRATION_ALPHA3_TO_ALPHA4_CN.md), and
[validation report](VALIDATION_REPORT.txt). Next-version requirements are
defined in the [v0.14 alignment specification](docs/V0_14_THEORY_REQUIREMENTS_CN.md).

## Security boundary

The local process runners are not an OS security sandbox and inherit the local
user's authority. Run only trusted code and keep the API bound to localhost.
Production mode fails closed without explicit authentication secrets and disables
local process plugins by default.
OCI manifests must use digest-pinned images, but container availability and
security configuration remain an operator responsibility. Tools are installed
only when needed; an unavailable optional tool is reported honestly.

License: Apache-2.0.
