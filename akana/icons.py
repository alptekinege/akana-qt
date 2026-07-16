"""Akana Qt — monochrome text glyphs (no image assets).

Web uses 1px-stroke SVG via icons.js. Qt ships no SVG runtime dependency;
we use a small, consistent Unicode set that reads as UI chrome, not decoration.
Glyphs always inherit ink/muted via QSS `color`.
"""

from __future__ import annotations

# Semantic names mirror common web icon ids where possible.
GLYPH: dict[str, str] = {
    "check": "✓",
    "chevron-down": "▾",
    "chevron-up": "▴",
    "chevron-right": "›",
    "chevron-left": "‹",
    "close": "×",
    "minus": "–",
    "plus": "+",
    "maximize": "□",
    "restore": "❐",
    "alert": "!",
    "empty": "∅",
    "mark": "◆",
    "grid": "▦",
    "dot": "·",
    "slash": "/",
    "arrow-right": "→",
    "moon": "☾",
    "sun": "☼",
}


def glyph(name: str, fallback: str = "·") -> str:
    return GLYPH.get(name, fallback)
