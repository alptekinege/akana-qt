# Changelog

All notable changes to **Akana Qt** are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning follows
[SemVer](https://semver.org/). Aligned with web Akana tags where practical.

## [0.5.4] - 2026-07-16

### Fixed
- **Gallery layout width:** `Page` / `AkPanel` / `AkShowcaseSection` no longer
  `AlignLeft`-clamp children to sizeHint — tables and boards fill the content
  column (was truncating `NAME` / `STATUS` while leaving empty space on the right).
- **Section lead overlap:** more title→lead spacing + lead padding so wrapped
  lines do not stack on top of each other.
- **Working strip / preview clipping:** panel vertical policy `Minimum` (not
  `Maximum`); larger page top/section spacing so borders and toolbars are not
  painted under the next block or the scroll edge.
- **Empty states:** expand with parent; body no longer hard-capped in a way that
  hides CTAs; dashed first-run block keeps actions visible.
- **Pagination active ring:** fixed square + zero padding + constant border so
  the “1” ring no longer shifts downward.
- **Accordion rows:** min-height on triggers so collapsed dividers are not
  compressed into a tight stack.
- **Link-card focus jump:** rest border is `FOCUS_W` (2px), matching focus.
- **Select height:** max height locked to `CONTROL_H` (parity with input).
- **Working strip density:** toolbar actions use `md` so they align with inputs.

### Changed
- **Design-system polish** against web Akana v0.5 + skill invariants:
  - Named geometry tokens: `FOCUS_W`, `LEAD_W`, `TAB_H`, `NAV_STRIP_H`,
    `TEXTAREA_MIN_H`, `EMPTY_BODY_W`, `TITLE_BTN_*`, `SCROLL_W`, `SIZE_GRIP`
  - QSS and components read those tokens — fewer bare pixel literals
  - `TypographyTokens.scale` synced with desktop `FS` (12…48)
  - Tab focus ring (underline ink); painted controls use `FOCUS_W` / `RADIUS`
  - Modal shadow theme detection via `current_name()` (not ink hex match)
  - Docs aligned: `CONTROL_H` 48 desktop, label type 12px, token tables complete

## [0.5.3] - 2026-07-16

### Changed
- **Control scale (desktop):** larger hit targets across the system.
  - Inputs/selects `44 → 48` (`CONTROL_H`)
  - Buttons md/sm/lg `44 / 36 / 52` with roomier horizontal padding
  - Nav items `44`, tabs taller, pagination `36 → 40`
  - Toggle `44×24`, checkbox `20`, radio `18`, badge `28`
  - Title bar `48`, modal `480`, table rows `52`
  - UI type steps: sm `15`, xs `13`, 2xs `12` (Qt reads smaller than CSS)
- App default font `11pt`; theme chip uses real `sm` button height.

## [0.5.2] - 2026-07-16

### Changed
- **Layout philosophy:** gallery content is left-weighted (max-width column,
  free space on the **right**). Removed dual-stretch horizontal centering.
- **Empty states** default to `align="start"`; optional `center` only when needed.
- Style boards / panels pack **top-left** (no tall empty vertical stretch).
- Nav strip sizes to content and sits on the start edge.
- Lead measure ~560px; section titles use `xl` scale for denser hierarchy.

## [0.5.1] - 2026-07-16

### Added
- **Custom-painted** `AkToggle` (track + thumb), `AkCheckbox` (ink check), `AkRadio` (ring).
- **`AkField`** — label + control + helper/error (web `.ak-field`, monochrome errors).
- **`AkLinkCard`** — gallery index links (web `.ak-link`).
- **`AkNavStrip`** — horizontal segmented nav (web `.ak-nav`).
- `akana/icons.py` glyph set, `akana/util.py` repolish helpers.
- Gallery **Tokens** page: semantic swatches + primitive ramp + type/space reference.
- Pattern list with badge cells + breadcrumb/pagination (web `patterns.html` fidelity).
- Modal scrim paint + parent geometry cover; Escape to close.

### Changed
- Focus rings use **fixed 2px borders** (no padding jump on focus).
- Accordion: title left / chevron right (not text-mashed).
- Breadcrumb separators use chevron glyph.
- Theme apply repaints all custom-painted children.
- Overview: component catalog with navigable link cards.

## [0.5.0] - 2026-07-16

### Added
- **DESIGN.md**, **AGENTS.md**, **TOKENS.md**, **CHANGELOG.md**.
- Theme persistence via `QSettings`.
- Semantic `ink_hover` / `ink_active`, `CONTROL_H`, `FS["4xl"]`.
- Editorial content column capped at `MAX_W` (1080).
- `setup_venv.py`.

### Changed
- Version **0.3.x → 0.5.0** (web component inventory parity).
- Page title/lead typography closer to web h1 / lead.

## [0.3.1] - 2026-07-15

### Fixed
- Frameless gallery UI polish and Windows window chrome / snap.

## [0.3.0] - 2026-07-15

### Added
- Initial Akana Qt design system: tokens, theme, QSS, IBM Plex TTF.
- Components: button, card, input, badge, nav, modal, toggle, table,
  checkbox, radio, select, textarea, tabs, alert, accordion, breadcrumb,
  pagination, empty-state, titlebar, showcase.
- Demo gallery pages: Overview · Buttons · Forms · Feedback · Data · Patterns.
