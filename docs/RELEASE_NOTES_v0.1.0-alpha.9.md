# ProofFlow Schema Sandbox `v0.1.0-alpha.9` Release Notes

**Release:** ProofFlow Schema Sandbox `v0.1.0-alpha.9`

**Release tag:** `v0.1.0-alpha.9`

**License:** MIT

**Package:** `proof-flow-schema-sandbox`

## Release summary

Alpha.9 repairs the release-engineering defects found after Alpha.8. It does not
weaken ProofFlow's experimental status: this remains a local research prototype
without a third-party security audit.

### Clean-checkout validation

- The Alpha.2 `.smath.zip` compatibility fixture is now version-controlled.
- CI builds and stages the production Web UI before running API/UI integration
  tests, eliminating the previous dependence on ignored local build output.
- Python dependencies are installed from an exact Python 3.12 release lock and
  frontend dependencies remain locked by `package-lock.json`.

### Enforced release gate

- `v*` tag pushes now trigger CI as well as the strict release gate.
- The gate rebuilds all release assets, verifies checksums, validates the packaged
  SBOM, installs the wheel in an isolated environment, and discovers both bundled
  plugins.
- GitHub prerelease publication occurs only after the gate succeeds and uses the
  existing, verified tag.

### Standards-compliant SBOM

- `sbom.cyclonedx.json` conforms to CycloneDX 1.5 and is checked against the
  official schema.
- npm Subresource Integrity hashes are converted to the hexadecimal form required
  by CycloneDX.
- SPDX compound expressions use the CycloneDX `expression` field; simple SPDX
  identifiers use `license.id`.
- Python component versions come from `requirements-release.lock`, and npm
  component versions come from `package-lock.json`.

### Accurate, reproducible provenance

- `package_manifest.json` and `SHA256SUMS.txt` are detached release assets rather
  than tracked, self-referential source files.
- The manifest records the exact source commit and release tag.
- The source archive uses fixed timestamps, normalized paths and modes, and embeds
  its own source-file checksum inventory plus the exact manifest.
- Version, product name, MIT license, repository URL, OpenAPI metadata, Python
  package metadata, frontend metadata, documentation, and filenames are aligned.

## Release assets

| Asset | Description |
|---|---|
| `proof_flow_schema_sandbox-0.1.0a9-py3-none-any.whl` | Python wheel with production Web UI and built-in plugins |
| `ProofFlow_Schema_Sandbox_v0.1.0-alpha.9.zip` | Deterministic source release archive |
| `package_manifest.json` | Exact tag, commit, source inventory and asset metadata |
| `sbom.cyclonedx.json` | CycloneDX 1.5 software bill of materials |
| `SHA256SUMS.txt` | SHA-256 checksums for all other release assets |

No detached signature is claimed for this prerelease. Verify downloads with
`SHA256SUMS.txt` and confirm the tag and commit recorded in
`package_manifest.json`.

## Quick start

### Install the wheel

```bash
pip install proof_flow_schema_sandbox-0.1.0a9-py3-none-any.whl
proofflow serve --port 8000
```

### Run from source

```bash
git clone https://github.com/schema-sandbox/proof-flow-schema-sandbox.git
cd proof-flow-schema-sandbox
git checkout v0.1.0-alpha.9
python -m venv .venv
pip install -e .
python start.py
```

Open `http://127.0.0.1:8000/app/`. Keep local process plugins on a trusted
machine and do not expose the development service to an untrusted network.

## Verification commands

```bash
python -m pytest -q -p no:cacheprovider
ruff check apps/api tests scripts
python scripts/validate_release_metadata.py
python scripts/validate_sbom.py --official
npm run build --prefix apps/web
npm audit --prefix apps/web --audit-level=high
python scripts/build_release.py --strict --dist
python scripts/verify_wheel.py
```
