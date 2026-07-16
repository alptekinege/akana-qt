# Akana Qt — Token Reference

Monochrome by design. **No accent color.** State is weight and border.

## Layer model

| Layer | Module | Role |
|-------|--------|------|
| Primitive | `akana/tokens.py` | Gray ramp, type, space, radius |
| Semantic | `akana/theme.py` | Light/dark intent map |
| Component | `akana/styles.py` | QSS selectors |

Components use **semantic** keys only (`bg`, `ink`, `text`, …).

## Gray ramp (primitive)

| Key | Hex |
|-----|-----|
| gray-0 | `#ffffff` |
| gray-50 | `#fafafa` |
| gray-100 | `#f2f2f2` |
| gray-200 | `#e4e4e4` |
| gray-300 | `#cfcfcf` |
| gray-400 | `#a3a3a3` |
| gray-500 | `#8a8a8a` |
| gray-600 | `#525252` |
| gray-700 | `#3d3d3d` |
| gray-800 | `#1c1c1c` |
| gray-850 | `#171717` |
| gray-900 | `#141414` |
| gray-950 | `#0a0a0a` |

## Semantic tokens

| Key | Light | Dark | Use |
|-----|-------|------|-----|
| bg | gray-0 | gray-950 | Page |
| surface | gray-50 | gray-900 | Rails, panels |
| surface_2 | gray-100 | gray-800 | Hover fill |
| border | gray-200 | gray-700 | Quiet edge |
| border_strong | gray-300 | gray-700 | Controls |
| ink | gray-950 | gray-0 | Primary mark |
| ink_hover | gray-800 | gray-200 | Primary hover |
| ink_active | gray-700 | gray-300 | Primary press |
| text | gray-850 | #ededed | Body |
| text_secondary | gray-600 | gray-400 | Secondary |
| text_muted | gray-500 | #6b6b6b | Meta / placeholder |
| inverse_bg | gray-950 | gray-0 | Solid fill |
| inverse_text | gray-0 | gray-950 | On solid |

## Type (desktop px)

Qt UI is nudged up one step vs browser CSS so controls stay legible.
`TypographyTokens.scale` mirrors `FS`.

| Key | px | Role |
|-----|----|------|
| 2xs | 12 | Mono labels / badges |
| xs | 13 | Compact UI / sm buttons |
| sm | 15 | Controls / buttons |
| md | 16 | Body |
| lg | 18 | Lead / card title |
| xl | 22 | Modal title |
| 2xl | 28 | Section |
| 3xl | 36 | Page title |
| 4xl | 48 | Display (optional) |

Families: IBM Plex Sans (display/UI), IBM Plex Mono (labels).  
Tracking: tight `-0.02em`, label `0.06em`.

## Spacing · Radius · Controls

- `SPACE`: 1→4, 2→8, … 20→80 (4px base)
- Radius: sm 4 · md 8 · lg 12 · pill 999
- `BORDER_W` = 1 · `FOCUS_W` = 2 (fixed focus ring; no layout jump)
- `CONTROL_H` = 48 (input / select; web 44)
- `BUTTON_H` / `_SM` / `_LG` = 44 / 36 / 52
- `NAV_ITEM_H` = 44 · `NAV_STRIP_H` = 40 · `TAB_H` = 44 · `PAGE_BTN` = 40
- `TITLEBAR_H` = 48 · `TITLE_BTN_W×H` = 44×36
- `TOGGLE_W×H` = 44×24 · `CHECK_BOX` = 20 · `RADIO_BOX` = 18 · `BADGE_H` = 28
- `TEXTAREA_MIN_H` = 140 · `EMPTY_ICON` = 52 · `CARD_ICON` = 40
- `MAX_W` = 1080 · `LEAD_W` = 560 · `EMPTY_BODY_W` = 360 · `MODAL_W` = 480
- `SCROLL_W` = 10 · `SIZE_GRIP` = 16
- Motion: 120ms fast · 200ms base (reference only; QSS transitions limited)

## Contrast targets

Aligned with web Akana WCAG notes:

- text on bg ≥ 4.5:1
- border-strong / focus ≥ 3:1 (non-text)
- Never put body text on pure ink without inverse tokens
