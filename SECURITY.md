# Security Policy

ProofFlow Schema Sandbox `0.1.0-alpha.6` is a local research prototype and has not undergone a third-party security audit.

- Bind the FastAPI service to `127.0.0.1`; do not expose it to an untrusted network.
- Production mode (`PROOFFLOW_ENV=production`) fails closed unless
  `PROOFFLOW_SECRET_KEY` and `PROOFFLOW_API_KEYS` are configured. API clients must
  send `X-API-Key` or a short-lived `Authorization: Bearer` token.
- Production mode disables process-local plugins by default. Re-enable them only on
  a host where the operating-system account is already an accepted trust boundary.
- Do not import untrusted `.smath.zip` archives without reviewing their origin. Path traversal is checked, but the archive may still contain large or misleading research artifacts.
- Local process plugins, including `python.local` and `graphviz.local`, are **not**
  a security boundary. They execute with the privileges of the local
  operating-system account.
- The Python runner scrubs most environment variables, uses a dedicated venv and per-run directory, applies best-effort resource limits, and caps outputs. These controls reduce accidental interference; they do not contain malicious code.
- API keys and secrets must not be stored in `.smath` project packages or source artifacts.
- Chat imports are treated as untrusted content and require human confirmation before candidate fragments enter the research graph.
- Plugins are installed and enabled explicitly. No plugin may silently install
  through the network; OCI manifests require digest-pinned images.
- Mathematical validity is outside the software security boundary. A successful process or plugin run is not a proof unless the relevant mathematical evidence supports that claim.

Please report security issues privately to `psi@psi.run` before public disclosure.
