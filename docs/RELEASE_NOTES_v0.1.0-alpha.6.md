# ProofFlow Schema Sandbox `v0.1.0-alpha.6` Release Notes

**Release Tag:** `v0.1.0-alpha.6`  
**Git Commit:** `28ad6e802d8d93c434501cd2595d2fa760fe840b`  
**License:** Apache-2.0  
**Package:** `proof-flow-schema-sandbox`  

---

## 🌟 What's New in Alpha.6

ProofFlow Schema Sandbox `v0.1.0-alpha.6` is a hardened, production-grade milestone focusing on security isolation, end-to-end cryptographic integrity verification, complete packaging of built-in plugins, and third-party license disclosures.

### 1. 🛡️ Network Security & Fail-Closed Guard
- **Host Security Validation**: The CLI, API runner, and `start.py` launcher enforce a strict security policy. Binding to `0.0.0.0` or non-loopback network interfaces requires explicit authentication (`PROOFFLOW_SECRET_KEY` / `PROOFFLOW_API_KEYS`) and disallows arbitrary local process plugins unless production flags are met.
- **Fail-Closed Default**: Remote unauthenticated execution is blocked unconditionally before socket binding.

### 2. 🔐 Full Artifact Integrity & Blob Tamper Protection
- **Disk Verification in Integrity Reports**: `service.integrity_report(project_id)` actively traverses all project artifacts, verifying their presence, strict content-addressed path (`blobs/sha256/{sha[:2]}/{sha}`), byte size, and SHA-256 checksums. Any missing or modified blob flags the project as invalid.
- **Stream Verification on Reads**: `service.artifact_bytes(project_id, artifact_id)` computes SHA-256 over read bytes and raises `ConflictError` upon tampering.
- **Zip Import Preflight**: `.smath.zip` imports strictly check canonical relative blob paths and reject archives with hash mismatches or non-canonical paths.

### 3. 📦 Complete Wheel & Docker Packaging
- **Built-in Plugins Bundled**: Wheel distribution (`.whl`) and container images package all built-in plugins (`graphviz.local`, `python.local`) and Vite/Prototype UI bundles as package data under `schemamath_api/_plugins/` and `schemamath_api/_ui/`.
- **Zero-Config Standalone Execution**: Installing the wheel provides immediate access to both UI workspaces and local calculation plugins.

### 4. 🌐 Native English & Chinese UI
- **True Bilingual Interface**: Clear language toggle between English and Chinese with consistent schema terminology across the canvas, sidebars, control plane, and inspector.
- **Dossier V2 & Epistemic Deltas**: Fully visualizable from both `/prototype/` (Workbench) and `/app/` (Explorer).

### 5. 📜 Compliance & SBOM
- Complete third-party license notices and software bill of materials in [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

---

## 📦 Release Assets & Checksums

| Asset | Size | SHA-256 Checksum |
|---|---|---|
| `proof_flow_schema_sandbox-0.1.0a6-py3-none-any.whl` | 5.28 MB | `0a22f53a5a1f8b98399dc28d13b89034b16a4bdae0f34f47fe4d8c898fc3d074` |
| `ProofFlow_Schema_Sandbox_v0.1.0-alpha.6.zip` | 864 KB | `a187dfadefdfd510dd7a60095e054f745185ebfa2c59d7de5ae5189621739b4a` |

---

## 🚀 Quick Start Instructions

### Option 1: One-Click Run (Windows)
1. Download `ProofFlow_Schema_Sandbox_v0.1.0-alpha.6.zip` and extract.
2. Double-click `start.bat` (or `启动ProofFlow.bat`).
3. Your browser will open the Workbench at `http://127.0.0.1:8000/prototype/`.

### Option 2: Install via Wheel
```bash
pip install proof_flow_schema_sandbox-0.1.0a6-py3-none-any.whl
proofflow serve --port 8000
```

### Option 3: From Source
```bash
git clone https://github.com/psi-run/ProofFlow.git
cd ProofFlow
python -m venv .venv
# Activate environment and install
pip install -e .
python start.py
```

### Option 4: Docker
```bash
docker build -t proofflow:v0.1.0-alpha.6 .
docker run -p 8000:8000 -e PROOFFLOW_SECRET_KEY=your-secret -e PROOFFLOW_API_KEYS=key1 proofflow:v0.1.0-alpha.6
```

---

## 🧪 Verification Matrix

- **Unit & Integration Tests**: 420/420 passed (`pytest`)
- **Linter**: 0 errors (`ruff check .`)
- **NPM Security Audit**: 0 vulnerabilities (`npm audit --omit=dev`)
- **Release Manifest**: 388 files tracked & verified
