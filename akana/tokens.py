"""Akana Qt — primitive design tokens (theme-agnostic).

Mirrors web Akana `assets/tokens.css` Layer 1 (v0.5).
Components must never use GRAY_PRIMITIVES directly; use theme semantics.

Desktop control geometry is intentionally slightly larger than web CSS
hit targets so Qt chrome stays comfortable on mouse + touch.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Layer 1: PRIMITIVE (raw, theme-agnostic) — same ramp as web tokens.css
# ---------------------------------------------------------------------------

GRAY_PRIMITIVES: dict[str, str] = {
    "gray-0": "#ffffff",
    "gray-50": "#fafafa",
    "gray-100": "#f2f2f2",
    "gray-200": "#e4e4e4",
    "gray-300": "#cfcfcf",
    "gray-400": "#a3a3a3",
    "gray-500": "#8a8a8a",
    "gray-600": "#525252",
    "gray-700": "#3d3d3d",
    "gray-800": "#1c1c1c",
    "gray-850": "#171717",
    "gray-900": "#141414",
    "gray-950": "#0a0a0a",
}


@dataclass(frozen=True)
class TypographyTokens:
    """Desktop (px) targets from web type scale maxima, stepped up one notch
    for Qt legibility at the smaller end of the scale.
    """

    family_display: str = '"IBM Plex Sans", system-ui, sans-serif'
    family_ui: str = '"IBM Plex Sans", system-ui, sans-serif'
    family_mono: str = '"IBM Plex Mono", ui-monospace, monospace'
    # 2xs, xs, sm, md, lg, xl, 2xl, 3xl, 4xl — mirrors FS values
    scale: tuple[int, ...] = field(
        default_factory=lambda: (12, 13, 15, 16, 18, 22, 28, 36, 48)
    )
    lh_tight: float = 1.12
    lh_snug: float = 1.3
    lh_normal: float = 1.55
    tracking_tight: str = "-0.02em"
    tracking_label: str = "0.06em"
    tracking_none: str = "0em"


@dataclass(frozen=True)
class SpacingTokens:
    """4px base scale (web --space-*)."""

    unit: int = 4
    # 1,2,3,4,5,6,8,10,12,16,20
    scale: tuple[int, ...] = field(
        default_factory=lambda: (4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80)
    )


@dataclass(frozen=True)
class RadiusTokens:
    """Web: sm=4, md=8, lg=12, pill=999."""

    sm: int = 4
    md: int = 8
    lg: int = 12
    pill: int = 999


@dataclass(frozen=True)
class MotionTokens:
    """Web --dur-fast / --dur-base (ms)."""

    dur_fast_ms: int = 120
    dur_base_ms: int = 200


TYPOGRAPHY = TypographyTokens()
SPACING = SpacingTokens()
RADIUS = RadiusTokens()
MOTION = MotionTokens()

# Named spacing helpers (px) — keys match web --space-N
SPACE = {
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
    6: 24,
    8: 32,
    10: 40,
    12: 48,
    16: 64,
    20: 80,
}

# Named type sizes (desktop px) — keys match web --fs-*
# Desktop Qt reads slightly smaller than browser CSS at the same px;
# UI control type steps up one notch vs web for comfort.
FS = {
    "2xs": 12,   # mono meta / badges (web 11)
    "xs": 13,    # compact UI (web 12)
    "sm": 15,    # controls / buttons (web 14)
    "md": 16,    # body
    "lg": 18,    # lead / card title
    "xl": 22,
    "2xl": 28,
    "3xl": 36,
    "4xl": 48,
}

BORDER_W = 1
FOCUS_W = 2  # fixed focus ring width — never jumps layout
MAX_W = 1080
LEAD_W = 560  # ~60ch at lead size; gallery / section lead measure
EMPTY_BODY_W = 360

# ---- Control geometry (desktop hit targets; ≥ web where noted) ----
CONTROL_H = 48          # input / select resting height (web 44)
CONTROL_H_SM = 36       # compact controls
BUTTON_H = 44           # primary/secondary default min height
BUTTON_H_SM = 36
BUTTON_H_LG = 52
PAGE_BTN = 40           # pagination square (web 36)
NAV_ITEM_H = 44
NAV_STRIP_H = 40        # segmented strip items (slightly tighter than rail)
TAB_H = 44
TITLEBAR_H = 48
TITLE_BTN_W = 44
TITLE_BTN_H = 36
CHECK_BOX = 20          # checkbox side (web 18)
RADIO_BOX = 18          # radio outer (web 16)
TOGGLE_W = 44
TOGGLE_H = 24
TOGGLE_THUMB = 18
BADGE_H = 28
EMPTY_ICON = 52
CARD_ICON = 40
MODAL_W = 480
TEXTAREA_MIN_H = 140    # web ~120; roomier desktop multiline
SCROLL_W = 10
SIZE_GRIP = 16
