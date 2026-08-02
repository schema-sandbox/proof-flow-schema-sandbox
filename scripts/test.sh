#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/apps/api${PYTHONPATH:+:$PYTHONPATH}"
PYTHON_CMD="$("$ROOT/scripts/_python.sh")"

run_python() {
  if [[ "$PYTHON_CMD" == "uv" ]]; then
    uv run --extra dev python "$@"
  else
    "$PYTHON_CMD" "$@"
  fi
}

if [[ "$PYTHON_CMD" == "uv" ]]; then
  uv run --extra dev pytest -q
else
  "$PYTHON_CMD" -m pytest -q
fi
run_python scripts/export_runtime_schemas.py
run_python scripts/validate_schemas.py
run_python scripts/export_openapi.py
node --check prototype/app.js
