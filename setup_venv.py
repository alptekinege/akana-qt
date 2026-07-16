"""Akana Qt — create .venv and install PyQt6 if missing.

Used by agents/docs; `launch.py` also auto-creates a venv on first run.
"""

from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIRED = "PyQt6"
OPTIONAL = "PyQt6-WebEngine"


def main() -> int:
    venv_dir = os.path.join(HERE, ".venv")
    if sys.platform == "win32":
        py = os.path.join(venv_dir, "Scripts", "python.exe")
        pip = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        py = os.path.join(venv_dir, "bin", "python")
        pip = os.path.join(venv_dir, "bin", "pip")

    if not os.path.exists(py):
        print(f"[akana] creating venv at {venv_dir}")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

    print(f"[akana] installing {REQUIRED}…")
    subprocess.run([pip, "install", "--upgrade", "pip"], check=False)
    subprocess.run([pip, "install", REQUIRED], check=True)

    print(f"[akana] installing {OPTIONAL} (optional)…")
    subprocess.run([pip, "install", OPTIONAL], check=False)

    print(f"[akana] ready: {py}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
