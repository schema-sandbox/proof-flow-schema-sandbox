"""
ProofFlow Local Launcher

Starts the ProofFlow service and opens the Web UI in your default browser.
"""

from __future__ import annotations

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
API_DIR = ROOT_DIR / "apps" / "api"

def main() -> None:
    # Ensure apps/api is in Python path
    if str(API_DIR) not in sys.path:
        sys.path.insert(0, str(API_DIR))
    
    pythonpath = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = str(API_DIR) + (os.pathsep + pythonpath if pythonpath else "")

    host = os.environ.get("SCHEMAMATH_HOST", "127.0.0.1")
    port = int(os.environ.get("SCHEMAMATH_PORT", "8000"))
    url = f"http://{host}:{port}/app/"

    print("=" * 60)
    print(" 🚀 ProofFlow Schema Sandbox")
    print("=" * 60)
    print(f" 🌐 Server URL : http://{host}:{port}")
    print(f" 📱 Web UI    : {url}")
    print(f" 📚 API Docs  : http://{host}:{port}/docs")
    print(f" 🧪 Prototype : http://{host}:{port}/prototype/")
    print("=" * 60)
    print(" Press Ctrl+C to stop the server.\n")

    # Automatically open browser after 1.5 seconds
    def launch_browser() -> None:
        time.sleep(1.5)
        webbrowser.open(url)

    threading.Thread(target=launch_browser, daemon=True).start()

    try:
        import uvicorn
        uvicorn.run(
            "schemamath_api.main:app",
            host=host,
            port=port,
            reload=True,
            app_dir=str(API_DIR),
        )
    except KeyboardInterrupt:
        print("\n👋 ProofFlow server stopped.")

if __name__ == "__main__":
    main()
