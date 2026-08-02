# ProofFlow Schema Sandbox — Quick Start Guide

Welcome to **ProofFlow Schema Sandbox**, a local-first, human-guided experimental research sandbox.

---

## 🚀 5-Minute Quick Start

### 1. Installation

Install via `pip`:

```bash
pip install proof-flow-schema-sandbox
```

Or install from source:

```bash
git clone https://github.com/proofflow/ProofFlow.git
cd ProofFlow
pip install -e .[dev]
```

### 2. Initialize a Project

Use the `proofflow` CLI tool to initialize your first research workspace:

```bash
proofflow init "Collatz Conjecture Exploration" --problem "For any positive integer n, if n is even, divide by 2; if n is odd, 3n+1."
```

### 3. Start the Local API Server & Web UI

Start the local server:

```bash
proofflow serve --port 8000
```

Open your browser to:
- Dual-Canvas Web App: [http://localhost:8000/app/](http://localhost:8000/app/)
- Prototype UI: [http://localhost:8000/prototype/](http://localhost:8000/prototype/)
- Interactive API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧱 30-Second @sip/contract Example

Use `@sip/contract` to enforce JSON Schema output constraints on any LLM or Agent in ~30 lines:

```python
from schemamath_api.sip import compose, createGate

# Define a gate that validates input & output
sandbox = compose(
    createGate(
        input={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
        output={"type": "object", "properties": {"answer": {"type": "string"}, "confidence": {"type": "number"}}, "required": ["answer", "confidence"]},
        fallback={"answer": "Validation failed, returning fallback.", "confidence": 0.0},
    )
)

# Run an operation
result = sandbox.run("my_llm_task", input_data={"query": "Calculate prime factors"})

print(f"Success: {result.success}")
print(f"Approval: {result.final_decision.approval}")
```

---

## 🛠️ CLI Cheat Sheet

| Command | Description |
|:---|:---|
| `proofflow init <title>` | Initialize a new research project workspace |
| `proofflow serve [--port 8000]` | Start local API & Web UI server |
| `proofflow status --project-id <UUID>` | Show project status & metadata |
| `proofflow integrity --project-id <UUID>` | Verify SHA-256 event log chain integrity |
| `proofflow rebuild --project-id <UUID>` | Rebuild SQLite projections from event log |
| `proofflow export --project-id <UUID>` | Export workspace as `.smath.zip` package |
| `proofflow import <path.zip>` | Preflight check & import `.smath.zip` package |
| `proofflow plugin list` | List available execution plugins |
| `proofflow replay --project-id <UUID>` | Replay event stream with progress tracking |
| `proofflow research-packet --project-id <UUID>` | Generate LLM research packet markdown |
