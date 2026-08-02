#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/apps/api${PYTHONPATH:+:$PYTHONPATH}"
PYTHON_CMD="$("$ROOT/scripts/_python.sh")"
if [[ "$PYTHON_CMD" == "uv" ]]; then
  exec uv run python scripts/bootstrap_demo.py
else
  exec "$PYTHON_CMD" scripts/bootstrap_demo.py
fi
