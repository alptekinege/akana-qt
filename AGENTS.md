# Akana Qt — Agent Guide

Monochrome, text-first PyQt6 design system. **No accent color.** **No
decorative images.** Fonts bundled as TTF (offline). Port of web Akana.

## How to add a component (core rule)

> Write components **one by one**, each in its **own file** under
> `akana/components/`. One concept per file, real states (hover / focus /
> disabled / checked).

Concretely:

1. Create `akana/components/ak<name>.py` with class `AkName`.
2. Export from `akana/components/__init__.py`.
3. Style via **semantic** selectors in `akana/styles.py` — never hardcode
   hex in the component module. Use `akana.tokens.SPACE` / `FS` / `RADIUS`
   for layout numbers. Prefer `akana.theme.get_theme()` inside `paintEvent`
   when QSS cannot express the control (toggle/checkbox/radio).
4. Use `akana.util.set_dyn` / `repolish` for dynamic properties.
5. Prefer fixed **2px** borders for focusable controls so focus never jumps layout.
6. **Do not center whole pages.** Gallery/content columns are left-weighted:
   `max-width` + slack on the right. Pack action rows start→end. Empty states
   default `align="start"`; center only when the pattern truly needs it (modals).
7. Demo on the matching `demo/app.py` page; wire `AkLinkCard` if it is a gallery entry.
8. Update `DESIGN.md` + `CHANGELOG.md` (SemVer).

## Hard constraints

- **Monochrome only.** State = weight + border, not hue.
- **Text-first.** Hierarchy from type and spacing.
- **No images.** Glyphs / mono marks only (e.g. card icon mark).
- **Offline fonts.** TTF in `akana/assets/fonts/`; re-fetch with
  `python scripts/download_fonts.py`.
- **Tokens are 3-layer.** Components never reference `GRAY_PRIMITIVES`.
- **Dark mode** rebinds only `THEMES` semantic map.

## Folder layout

```
akana_qt/
  DESIGN.md  AGENTS.md  README.md  CHANGELOG.md  TOKENS.md  FONTS.md
  launch.py  launch.bat  setup_venv.py
  akana/
    tokens.py   theme.py   styles.py   fonts.py   winchrome.py
    assets/fonts/          # IBM Plex TTF + OFL
    components/            # one component per file
  demo/
    app.py                 # gallery
  scripts/
    download_fonts.py
```

## Theme API

```python
from akana.theme import set_theme, load_saved_theme, current_name
from akana import styles

load_saved_theme()
set_theme("dark")       # light | dark
styles.apply(window)    # rebuild QSS + placeholder palette
```

Storage: `QSettings("Akana", "AkanaQt")` key `theme` (web mirror of
`localStorage['akana-theme']`).

## QSS notes

- Target Python class names (`AkButton`) and `objectName`s (`#akNavItem`).
- Dynamic variants use properties: `variant`, `akSize`, `tone` — then
  `style.unpolish` / `polish` after changes.
- Intermediate `QWidget` backgrounds stay **transparent** so nested panels
  do not paint double chrome.
- Prefer `CONTROL_H` (48 desktop; web is 44) for inputs/selects.
- Use `FOCUS_W` (2) for focus rings so geometry never jumps.
- Layout numbers come from `SPACE` / `FS` / control tokens — not bare literals.

## Verification

```bash
# from repo root, with .venv
.venv\Scripts\python -c "from akana import styles, theme, tokens; print(tokens.FS['md'], theme.current_name())"
.venv\Scripts\python -c "from demo.app import MainWindow; print('ok')"
launch.bat
```

Check light **and** dark: focus rings, disabled, hover, nav selected, modal.
No accent colors in QSS or Python.
