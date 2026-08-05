# Changelog

## 0.1.0-alpha.5

- Added atomic event batches with revision checks, idempotency keys, batch IDs and command metadata.
- Added accepted/rejected research-state transitions across operational, epistemic, claim and artifact planes.
- Added typed continuation contracts, V2 handoff packets and acceptance/rejection receipts.
- Added ClaimAtom proposals, six independent evidence dimensions, review lineage and explicit claim relations.
- Added execution manifests, formal coverage bindings, repository snapshots and repair lineage records.
- Added typed hierarchy nodes, attempt outcomes, cost vectors, micro-falsification plans, benchmark bindings and 27-field dossier V2 records.
- Added the Alpha.5 REST routes, runtime schemas, SQLite projections and control-plane UI summary.
- Comparator results now fail closed when no real primary-kernel execution is available.
- Schema `0.6` accepts Alpha.1–Alpha.5 reads; legacy event lines remain append-only and are projected without rewriting.

## Unreleased — v0.14 theory-alignment documentation

- Added a SHA-256-pinned v0.14 requirements baseline with 16 traceable
  `PF-014` requirement groups.
- Added the current-code software audit, Alpha.5 upgrade plan and acceptance
  matrix while preserving Alpha.4 as the current runtime boundary.
- The implementation work described by this plan is now recorded in the Alpha.5
  release section above; the original audit baseline remains historical.
- Updated the repository map and README links. No runtime behavior, API,
  Schema version or historical release record was changed by this
  documentation-only alignment pass.

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
