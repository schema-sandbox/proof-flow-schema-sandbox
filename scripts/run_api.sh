#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/apps/api${PYTHONPATH:+:$PYTHONPATH}"
PYTHON_CMD="$("$ROOT/scripts/_python.sh")"
if [[ "$PYTHON_CMD" == "uv" ]]; then
  exec uv run uvicorn schemamath_api.main:app --host 127.0.0.1 --port "${SCHEMAMATH_PORT:-8000}" --reload
else
  exec "$PYTHON_CMD" -m uvicorn schemamath_api.main:app --host 127.0.0.1 --port "${SCHEMAMATH_PORT:-8000}" --reload
fi
