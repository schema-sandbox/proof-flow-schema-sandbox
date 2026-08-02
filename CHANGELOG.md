# Changelog

## 0.1.0-alpha.4

- Added fail-closed production API-key/HMAC authentication and disabled local
  process plugins in the production profile by default.
- Bound development and production Compose ports to loopback, added a minimal
  non-root Docker image, persistent `/data`, and secret-file examples.
- Streamed archive uploads with size limits, staged imports before atomic
  replacement, and added cross-process event-store locking.
- Changed unavailable Lean/Z3/WASI/GUDHI and placeholder proof/economic paths to
  report unverified or unavailable outcomes instead of false success.
- Regenerated the release manifest and SHA-256 checksums after the remediation.
- Added read-only `.smath.zip` preflight diagnostics before import.
- Added archive path, duplicate-member, symlink, compressed-size, chain and
  content-addressed artifact checks.
- Added registered SQLite projection migrations and migration version reporting.
- Refused new event appends after a canonical JSONL hash-chain failure.
- Preserved Alpha.2/Alpha.3 import compatibility and all previous product
  constitution constraints.

## 0.1.0-alpha.3

- Renamed the product to ProofFlow Schema Sandbox while preserving Alpha.2 API,
  package and environment compatibility surfaces.
- Added a generalized plugin host and a truthful Graphviz local adapter.
- Added `ModelSession`, `HandoffArtifact`, and preview-only `ArenaRecipe`.
- Added typed epistemic deltas, historical retrieval and route-similarity hints.
- Added immutable Excalidraw snapshots and human-confirmed visual mappings.
- Delivered and build-validated the React Flow + Excalidraw application at `/app/`.
- Added schema migrations, 24 runtime schemas, 46 OpenAPI paths and Alpha.2
  `.smath.zip` regression coverage.

## 0.1.0-alpha.2

- Added `Branch`, `Challenge`, `BridgeResult`, `DeadEndConstraint`, and `ResearchCheckpoint` domain objects.
- Added route split and route merge while preserving source lineage.
- Added conservative branch transitions and certified dead-end safeguards.
- Added ChatGPT companion imports for Markdown, HTML, JSON, and plain text.
- Preserved every imported conversation as a raw content-addressed artifact.
- Added human-confirmed dispositions: model note, checkpoint, challenge, bridge result, new branch, or ignore.
- Added an optional project-scoped `python.local` experiment plugin.
- Recorded Python source, command, environment fingerprint, stdout, stderr, exit status, timeout, and produced artifacts for successful and failed runs.
- Expanded Research Packets with branches, challenges, dead ends, checkpoints, and recent experiment state.
- Expanded the dependency-free browser prototype for Alpha.2 workflows.
- Added runtime JSON Schema export and validation.
- Expanded tests for route lineage, import confirmation, tool failures, portability, and high-threshold closure.

## 0.1.0-alpha.1

- Created a local FastAPI service and `.smath` project format.
- Added append-only, hash-chained observable research events.
- Added rebuildable SQLite projections for routes and artifacts.
- Added conservative route transitions with human-confirmed closure.
- Added human notes, content-addressed artifacts, integrity checks, and export/import.
- Added a Research Packet generator for manual ChatGPT companion workflows.
- Added a dependency-free interactive prototype and a React/Vite scaffold.
