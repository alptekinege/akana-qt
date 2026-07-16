"""Akana Qt — monochrome, text-first, offline Qt design system.

Port of web Akana (https://github.com/alptekinege/Akana) v0.5:
3-layer tokens, no accent color, bundled IBM Plex TTF.
"""

from akana import fonts, icons, styles, theme, tokens, util, winchrome
from akana.util import AkFlowLabel, configure_flow_label

__version__ = "0.5.4"

__all__ = [
    "tokens",
    "theme",
    "styles",
    "fonts",
    "icons",
    "util",
    "winchrome",
    "AkFlowLabel",
    "configure_flow_label",
    "__version__",
]
