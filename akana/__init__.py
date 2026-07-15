"""Akana Qt — monochrome, text-first, offline Qt design system.

Port of web Akana (https://github.com/alptekinege/Akana):
3-layer tokens, no accent color, bundled IBM Plex TTF.
"""

from akana import fonts, styles, theme, tokens

__version__ = "0.3.0"

__all__ = [
    "tokens",
    "theme",
    "styles",
    "fonts",
    "__version__",
]
