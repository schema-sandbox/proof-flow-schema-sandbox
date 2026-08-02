#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${SCHEMAMATH_PYTHON:-}" ]]; then
  printf '%s\n' "$SCHEMAMATH_PYTHON"
  exit 0
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -x "$ROOT/.venv/bin/python" ]] && "$ROOT/.venv/bin/python" -c 'import fastapi, pydantic' >/dev/null 2>&1; then
  printf '%s\n' "$ROOT/.venv/bin/python"
  exit 0
fi

if python -c 'import fastapi, pydantic' >/dev/null 2>&1; then
  command -v python
  exit 0
fi

if command -v uv >/dev/null 2>&1; then
  echo "uv"
  exit 0
fi

cat >&2 <<'MSG'
No usable Python environment was found.
Install dependencies with `uv sync --extra dev` or set SCHEMAMATH_PYTHON.
MSG
exit 1
