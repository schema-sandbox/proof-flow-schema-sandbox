from pathlib import Path
import json
import os

values = [{"n": n, "parity": n % 2} for n in range(12)]
print(f"generated {len(values)} rows")
output = Path(os.environ["SCHEMAMATH_OUTPUT_DIR"]) / "parity.json"
output.write_text(json.dumps(values, indent=2), encoding="utf-8")
