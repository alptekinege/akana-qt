"""Akana Qt — register bundled IBM Plex fonts (offline).

Call `load_fonts()` once after QApplication is created.
Falls back silently if files are missing (system-ui still works).
"""

from __future__ import annotations

import os
from pathlib import Path

from PyQt6.QtGui import QFontDatabase

_FONTS_DIR = Path(__file__).resolve().parent / "assets" / "fonts"

# Weight order for documentation / debugging.
_FONT_FILES = (
    "IBMPlexSans-Regular.ttf",
    "IBMPlexSans-Medium.ttf",
    "IBMPlexSans-SemiBold.ttf",
    "IBMPlexSans-Bold.ttf",
    "IBMPlexMono-Regular.ttf",
    "IBMPlexMono-Medium.ttf",
)

_loaded: list[str] = []
_families: set[str] = set()


def fonts_dir() -> Path:
    return _FONTS_DIR


def load_fonts() -> list[str]:
    """Load bundled TTF into the process. Returns registered family names."""
    global _loaded, _families
    if _loaded:
        return list(_families)

    found: list[str] = []
    families: set[str] = set()

    for name in _FONT_FILES:
        path = _FONTS_DIR / name
        if not path.is_file():
            continue
        fid = QFontDatabase.addApplicationFont(str(path))
        if fid < 0:
            continue
        found.append(name)
        for fam in QFontDatabase.applicationFontFamilies(fid):
            families.add(fam)

    _loaded = found
    _families = families
    return list(families)


def loaded_files() -> list[str]:
    return list(_loaded)


def has_plex() -> bool:
    return any("Plex" in f for f in _families)


def ensure_fonts() -> None:
    """Idempotent load — safe to call from styles.apply / main."""
    load_fonts()
