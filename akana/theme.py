"""Akana Qt — semantic theme layer (light / dark).

Dark mode rebinds ONLY semantic tokens; primitives stay fixed.
No accent color. State = weight + border (monochrome invariant).
"""

from __future__ import annotations

from akana.tokens import GRAY_PRIMITIVES as G

# ---------------------------------------------------------------------------
# Layer 2: SEMANTIC — resolved hex (Qt QSS cannot follow CSS var chains)
# ---------------------------------------------------------------------------

THEMES: dict[str, dict[str, str]] = {
    "light": {
        "bg": G["gray-0"],
        "surface": G["gray-50"],
        "surface_2": G["gray-100"],
        "border": G["gray-200"],
        "border_strong": G["gray-300"],
        "ink": G["gray-950"],
        "text": G["gray-850"],
        "text_secondary": G["gray-600"],
        "text_muted": G["gray-500"],
        "inverse_bg": G["gray-950"],
        "inverse_text": G["gray-0"],
        # soft shadows as QSS-friendly rgba
        "shadow_sm": "rgba(10, 10, 10, 0.06)",
        "shadow_md": "rgba(10, 10, 10, 0.08)",
    },
    "dark": {
        "bg": G["gray-950"],
        "surface": G["gray-900"],  # #141414
        "surface_2": G["gray-800"],
        "border": G["gray-700"],
        "border_strong": G["gray-700"],
        "ink": G["gray-0"],
        "text": "#ededed",
        "text_secondary": G["gray-400"],
        "text_muted": "#6b6b6b",
        "inverse_bg": G["gray-0"],
        "inverse_text": G["gray-950"],
        "shadow_sm": "rgba(0, 0, 0, 0.4)",
        "shadow_md": "rgba(0, 0, 0, 0.5)",
    },
}

_current = "light"


def set_theme(name: str) -> None:
    global _current
    if name not in THEMES:
        raise ValueError(f"unknown theme: {name!r} (expected light|dark)")
    _current = name


def get_theme() -> dict[str, str]:
    """Return a copy of the active semantic token map."""
    return dict(THEMES[_current])


def current_name() -> str:
    return _current


def token(key: str) -> str:
    """Lookup a single semantic token for the active theme."""
    t = THEMES[_current]
    if key not in t:
        raise KeyError(f"unknown semantic token: {key!r}")
    return t[key]
