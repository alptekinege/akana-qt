# Changelog

All notable changes to **Akana Qt** are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning follows
[SemVer](https://semver.org/). Aligned with web Akana tags where practical.

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
