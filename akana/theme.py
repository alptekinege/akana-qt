"""Akana Qt — semantic theme layer (light / dark).

Dark mode rebinds ONLY semantic tokens; primitives stay fixed.
No accent color. State = weight + border (monochrome invariant).

Theme preference is persisted via QSettings under organization
"Akana" / application "AkanaQt" (key: theme), mirroring web
localStorage['akana-theme'].
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
        # soft shadows as QSS-friendly rgba (reserved for hover/modal)
        "shadow_sm": "rgba(10, 10, 10, 0.06)",
        "shadow_md": "rgba(10, 10, 10, 0.08)",
        # hover ink (primary press affordance without hue)
        "ink_hover": G["gray-800"],
        "ink_active": G["gray-700"],
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
        "ink_hover": G["gray-200"],
        "ink_active": G["gray-300"],
    },
}

_current = "light"
_SETTINGS_ORG = "Akana"
_SETTINGS_APP = "AkanaQt"
_SETTINGS_KEY = "theme"


def set_theme(name: str, *, persist: bool = True) -> None:
    """Activate light|dark. Optionally persist for the next session."""
    global _current
    if name not in THEMES:
        raise ValueError(f"unknown theme: {name!r} (expected light|dark)")
    _current = name
    if persist:
        _save_theme(name)


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


def load_saved_theme() -> str:
    """Load theme from QSettings (default light). Does not raise."""
    name = _read_theme()
    if name in THEMES:
        set_theme(name, persist=False)
    return _current


def _save_theme(name: str) -> None:
    try:
        from PyQt6.QtCore import QSettings

        s = QSettings(_SETTINGS_ORG, _SETTINGS_APP)
        s.setValue(_SETTINGS_KEY, name)
    except Exception:
        pass


def _read_theme() -> str | None:
    try:
        from PyQt6.QtCore import QSettings

        s = QSettings(_SETTINGS_ORG, _SETTINGS_APP)
        val = s.value(_SETTINGS_KEY, None)
        return str(val) if val is not None else None
    except Exception:
        return None
