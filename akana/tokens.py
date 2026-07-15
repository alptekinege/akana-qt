"""Akana Qt — primitive design tokens (theme-agnostic).

Mirrors web Akana `assets/tokens.css` Layer 1.
Components must never use GRAY_PRIMITIVES directly; use theme semantics.
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
    """Desktop (px) targets from web type scale maxima."""

    family_display: str = '"IBM Plex Sans", system-ui, sans-serif'
    family_ui: str = '"IBM Plex Sans", system-ui, sans-serif'
    family_mono: str = '"IBM Plex Mono", ui-monospace, monospace'
    # 2xs, xs, sm, md, lg, xl, 2xl, 3xl  (desktop px)
    scale: tuple[int, ...] = field(
        default_factory=lambda: (11, 12, 14, 16, 18, 22, 28, 36)
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
    dur_fast_ms: int = 120
    dur_base_ms: int = 200


TYPOGRAPHY = TypographyTokens()
SPACING = SpacingTokens()
RADIUS = RadiusTokens()
MOTION = MotionTokens()

# Named spacing helpers (px)
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

# Named type sizes (desktop px)
FS = {
    "2xs": 11,
    "xs": 12,
    "sm": 14,
    "md": 16,
    "lg": 18,
    "xl": 22,
    "2xl": 28,
    "3xl": 36,
}

BORDER_W = 1
MAX_W = 1080
