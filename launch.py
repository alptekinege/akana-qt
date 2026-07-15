"""Akana Qt — launch script + optional venv auto-setup."""

from __future__ import annotations

import os
import runpy
import subprocess
import sys

REQUIRED_PACKAGE = "PyQt6"
OPTIONAL_PACKAGE = "PyQt6-WebEngine"

HERE = os.path.dirname(os.path.abspath(__file__))


def ensure_venv() -> str:
    """Create .venv if missing and return the python executable path."""
    venv_dir = os.path.join(HERE, ".venv")
    py = os.path.join(venv_dir, "Scripts", "python.exe")

    if os.path.exists(py):
        return py

    print(f"[akana] no venv found — creating at {venv_dir}")
    subprocess.run(
        [sys.executable, "-m", "venv", venv_dir],
        check=True,
    )

    pip = os.path.join(venv_dir, "Scripts", "pip.exe")
    if not os.path.exists(pip):
        raise RuntimeError("venv created but pip not found")

    print(f"[akana] installing {REQUIRED_PACKAGE}…")
    subprocess.run([pip, "install", "--quiet", REQUIRED_PACKAGE], check=True)

    try:
        print(f"[akana] installing {OPTIONAL_PACKAGE} (optional)…")
        subprocess.run(
            [pip, "install", "--quiet", OPTIONAL_PACKAGE],
            check=False,
        )
    except Exception:
        pass

    return py


def launch() -> None:
    py = ensure_venv()
    env = os.environ.copy()
    env.pop("PYTHONHOME", None)
    env["PYTHONPATH"] = HERE
    subprocess.run([py, "-m", "demo.app"], cwd=HERE, env=env, check=False)


if __name__ == "__main__":
    launch()
