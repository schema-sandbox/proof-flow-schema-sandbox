import json
import os
from pathlib import Path

values = [{"n": n, "parity": n % 2} for n in range(12)]
output_dir = Path(os.environ["SCHEMAMATH_OUTPUT_DIR"])
(output_dir / "parity-table.json").write_text(
    json.dumps(values, indent=2), encoding="utf-8"
)
print(f"wrote {len(values)} rows")
