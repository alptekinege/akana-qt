---
version: 0.5.2
name: Akana Qt
description: Monochrome, text-first design system for PyQt6 (Ak + Ana). Ink-on-paper, no accent color, bundled IBM Plex TTF (SIL OFL 1.1). Port of web Akana.
colors:
  gray-0: "#FFFFFF"
  gray-50: "#FAFAFA"
  gray-100: "#F2F2F2"
  gray-200: "#E4E4E4"
  gray-300: "#CFCFCF"
  gray-400: "#A3A3A3"
  gray-500: "#8A8A8A"
  gray-600: "#525252"
  gray-700: "#3D3D3D"
  gray-800: "#1C1C1C"
  gray-850: "#171717"
  gray-900: "#141414"
  gray-950: "#0A0A0A"
  bg: "{colors.gray-0}"
  surface: "{colors.gray-50}"
  surface-2: "{colors.gray-100}"
  border: "{colors.gray-200}"
  border-strong: "{colors.gray-300}"
  ink: "{colors.gray-950}"
  text: "{colors.gray-850}"
  text-secondary: "{colors.gray-600}"
  text-muted: "{colors.gray-500}"
  inverse-bg: "{colors.gray-950}"
  inverse-text: "{colors.gray-0}"
typography:
  h1:
    fontFamily: "IBM Plex Sans"
    fontSize: 36px
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.02em"
  h2:
    fontFamily: "IBM Plex Sans"
    fontSize: 28px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  body-md:
    fontFamily: "IBM Plex Sans"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "IBM Plex Mono"
    fontSize: 11px
    fontWeight: 500
    letterSpacing: "0.06em"
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  pill: 999px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.inverse-text}"
    rounded: "{rounded.md}"
  button-secondary:
    backgroundColor: transparent
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
  card:
    backgroundColor: "{colors.bg}"
    rounded: "{rounded.lg}"
  input:
    backgroundColor: "{colors.bg}"
    rounded: "{rounded.md}"
---

## Overview

**Akana Qt** is the desktop (PyQt6) implementation of **Akana** — monochrome,
text-first, offline. Same product language as web
[Akana](https://github.com/alptekinege/Akana): *ak* (clarity) + *ana* (source).

No accent hue. State = weight + border. Fonts: IBM Plex Sans + Mono as local
TTF (Qt cannot load woff2). Tokens: Python dicts + generated QSS.

## Invariants

1. **Monochrome only.** No accent, gradient, or tinted surface.
2. **Text-first.** Type + spacing + optional text glyphs (never decorative images).
3. **Offline.** Bundled TTF under `akana/assets/fonts/`. No CDN.
4. **Token-driven.** Components use semantic keys; never hardcode colors.
5. **3-layer tokens.** Primitive → semantic → component. Dark rebinds **only** semantic.

## Tokens

| Layer | Source | Rule |
|-------|--------|------|
| Primitive | `akana/tokens.py` `GRAY_PRIMITIVES` | Theme-agnostic. Never in components. |
| Semantic | `akana/theme.py` `THEMES[light\|dark]` | Intent. Components read these. |
| Component | QSS in `akana/styles.py` | Prefer local property selectors. |

Layout tokens: `SPACE`, `FS`, `RADIUS`, `CONTROL_H` (44), `MAX_W` (1080).

## Theme

```python
from akana.theme import set_theme, load_saved_theme
from akana import styles

load_saved_theme()          # QSettings org=Akana app=AkanaQt
set_theme("dark")           # persists by default
styles.apply(window)
```

## Components

One class per file under `akana/components/`, `Ak*` prefix:

| Group | Modules |
|-------|---------|
| Core | button, card, input, badge, nav/rail/strip, modal, titlebar, link-card |
| Form | field, checkbox*, radio*, select, textarea, toggle* |
| Feedback / nav | alert, tabs, accordion, breadcrumb, pagination |
| Data / content | table, empty-state |
| Gallery | showcase (panel, style board, section) |

\* Custom-painted indicators (not native QSS-only) for reliable monochrome state.

## Accessibility

- Body/secondary text contrast targets WCAG AA (≥4.5:1) via the gray ramp.
- Focus = 2px solid ink border (QSS cannot do CSS outline-offset reliably).
- Decorative glyphs are visual only; icon-only controls need accessible names.
- Prefer muted disabled colors over pure opacity for Qt contrast.

## Gallery

`demo/app.py` — frameless shell, sidebar nav, pages: Overview · Buttons ·
Forms · Feedback · Data · Patterns (web `patterns.html` parity).
