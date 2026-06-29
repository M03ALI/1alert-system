#!/usr/bin/env python3
"""
Entry point used when packaging the Stock Inventory app into a STANDALONE program
(with PyInstaller). The built program bundles Python + all libraries, so the
computer it runs on does NOT need Python installed — just like Excel.

How it works when running:
  • Your data is kept in a folder in your home directory (StockInventory/inventory.db),
    which is writable and persists between runs.
  • It starts the local Streamlit server in a separate process (so there are no
    background-thread/signal problems when frozen).
  • It opens the app in its OWN WINDOW via pywebview if available, otherwise in your
    default browser. Closing the window shuts everything down.

This same file also works when run directly with Python (python app_entry.py),
which is handy for testing before you build.
"""

import os
import sys
import time
import socket
import threading
import subprocess
import webbrowser

FROZEN = bool(getattr(sys, "frozen", False))


def resource_path(rel):
    """Path to a bundled file, whether running frozen or from source."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


# Persistent, writable data location (the bundle folder is read-only/temporary).
DATA_DIR = os.path.join(os.path.expanduser("~"), "StockInventory")
os.makedirs(DATA_DIR, exist_ok=True)
os.environ.setdefault("INVENTORY_DB_PATH", os.path.join(DATA_DIR, "inventory.db"))


def _free_port(preferred=8501):
    for port in (preferred, 0):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", port))
            chosen = s.getsockname()[1]
            s.close()
            return chosen
        except OSError:
            continue
    return preferred


def _wait_until_up(host, port, timeout=90):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def _run_server(port):
    """Run Streamlit in THIS process (main thread) — the reliable way when frozen."""
    from streamlit.web import cli as stcli
    app = resource_path("inventoryapp.py")
    sys.argv = [
        "streamlit", "run", app,
        "--server.address=127.0.0.1",
        f"--server.port={port}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false",
        # Theme is also injected via CSS, but set the base palette here too so the
        # frozen app looks identical even without a bundled config.toml.
        "--theme.base=light",
        "--theme.primaryColor=#006868",
        "--theme.backgroundColor=#FFFFFF",
        "--theme.secondaryBackgroundColor=#F0FAFA",
        "--theme.textColor=#06343A",
    ]
    sys.exit(stcli.main())


def main():
    # Child process branch: actually run the Streamlit server.
    if os.environ.get("INV_RUN_SERVER") == "1":
        _run_server(int(os.environ.get("INV_PORT", "8501")))
        return

    host = "127.0.0.1"
    port = _free_port(int(os.environ.get("INV_PORT", "8501")))
    url = f"http://{host}:{port}"

    # Re-launch ourselves as the server. Frozen -> the exe; source -> python + this file.
    cmd = [sys.executable] if FROZEN else [sys.executable, os.path.abspath(__file__)]
    env = dict(os.environ, INV_RUN_SERVER="1", INV_PORT=str(port))
    server = subprocess.Popen(cmd, env=env)

    def _shutdown():
        try:
            server.terminate()
        except Exception:
            pass

    try:
        if not _wait_until_up(host, port, timeout=120):
            _shutdown()
            print("The app did not start in time.")
            return
        try:
            import webview  # pywebview, for a real desktop window
            win = webview.create_window("Stock Inventory", url,
                                        width=1180, height=820, min_size=(360, 600))
            try:
                win.events.closed += _shutdown
            except Exception:
                pass
            webview.start()
            _shutdown()
        except Exception:
            threading.Timer(0.4, lambda: webbrowser.open(url)).start()
            print(f"\nStock Inventory is running at {url}")
            print("Close this window to quit.\n")
            server.wait()
    except KeyboardInterrupt:
        pass
    finally:
        _shutdown()


if __name__ == "__main__":
    main()
