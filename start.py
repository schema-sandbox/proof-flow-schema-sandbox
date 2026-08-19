"""
ProofFlow Local Launcher

Starts the ProofFlow service and opens the Web UI in your default browser.
Automatically detects port conflicts and finds an available port if 8000 is in use.
"""

from __future__ import annotations

import os
import socket
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
API_DIR = ROOT_DIR / "apps" / "api"


def is_port_available(host: str, port: int) -> bool:
    """Check if a specific host:port is free to bind."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return True
        except OSError:
            return False


def find_available_port(host: str, preferred_port: int, max_attempts: int = 50) -> int:
    """Find a free port starting from preferred_port."""
    for port in range(preferred_port, preferred_port + max_attempts):
        if is_port_available(host, port):
            return port
    raise RuntimeError(f"在 {host} 找不到可用端口 (尝试范围: {preferred_port} - {preferred_port + max_attempts})")


def wait_for_server(url: str, timeout: float = 8.0) -> bool:
    """Wait until the server starts responding."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ProofFlow-Launcher"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status in (200, 302, 307):
                    return True
        except Exception:
            time.sleep(0.3)
    return False


def main() -> None:
    # Ensure apps/api is in Python path
    if str(API_DIR) not in sys.path:
        sys.path.insert(0, str(API_DIR))

    pythonpath = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = str(API_DIR) + (os.pathsep + pythonpath if pythonpath else "")

    host = os.environ.get("SCHEMAMATH_HOST", "127.0.0.1")
    requested_port = int(os.environ.get("SCHEMAMATH_PORT", "8000"))

    # Validate host security to prevent unauthenticated non-loopback exposure
    from schemamath_api.config import Settings
    settings = Settings.from_environment()
    try:
        settings.validate_host_security(host)
    except ValueError as exc:
        print(f"\n❌ 安全拦截: {exc}\n")
        sys.exit(1)

    # Auto detect port conflict
    port = find_available_port(host, requested_port)
    port_switched = (port != requested_port)

    url = f"http://{host}:{port}/prototype/"
    demo_url = f"http://{host}:{port}/app/"
    health_url = f"http://{host}:{port}/health"

    print("=" * 64)
    print(" 🚀 ProofFlow Schema Sandbox 启动中...")
    print("=" * 64)
    if port_switched:
        print(f" ⚠️  [端口占用提示] 默认端口 {requested_port} 已被占用，已自动切换到空闲端口 -> {port}")
    print(f" 🌐 服务器地址     : http://{host}:{port}")
    print(f" 🧪 主工作台 UI (主窗口) : {url}")
    print(f" 📱 探索台 UI (案例演示) : {demo_url}")
    print(f" 📚 API 接口       : http://{host}:{port}/docs")
    print("=" * 64)
    print(" 💡 正在启动服务并在浏览器中自动打开...")
    print(" 💡 随时按 Ctrl + C 可安全停止服务。\n")

    # Automatically open browser once server is responsive
    def launch_browser() -> None:
        if wait_for_server(health_url, timeout=10.0):
            print(f"\n[浏览器已启动] 正在访问: {url}")
            webbrowser.open(url)
        else:
            print(f"\n[提示] 服务已启动，可手动在浏览器打开: {url}")

    threading.Thread(target=launch_browser, daemon=True).start()

    try:
        import uvicorn
        uvicorn.run(
            "schemamath_api.main:app",
            host=host,
            port=port,
            reload=False,
            app_dir=str(API_DIR),
        )
    except KeyboardInterrupt:
        print("\n\n👋 ProofFlow 服务已正常停止。")
    except Exception as exc:
        print(f"\n❌ 服务启动失败: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
