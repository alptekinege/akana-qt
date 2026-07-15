# Akana Qt

Monochrome, text-first, offline design system for Qt (PyQt6).  
Aligned with web [Akana](https://github.com/alptekinege/Akana) v0.5.

## Invariants

1. **Monochrome only** — no accent hue; state = weight + border  
2. **Text-first** — hierarchy from type + spacing  
3. **Offline** — bundled IBM Plex TTF (SIL OFL 1.1); no CDN  
4. **3-layer tokens** — primitive → semantic → component; dark rebinds **only** semantic  

## Run

```bat
launch.bat
```

```bash
python launch.py
```

## Structure

```
akana_qt/
├── launch.py / launch.bat
├── scripts/download_fonts.py    # re-fetch IBM Plex TTF from IBM/plex
├── akana/
│   ├── tokens.py                # Layer 1 primitives
│   ├── theme.py                 # Layer 2 light/dark
│   ├── styles.py                # QSS from semantic tokens
│   ├── fonts.py                 # QFontDatabase registration
│   ├── assets/fonts/            # *.ttf + OFL-IBM-Plex.txt
│   └── components/              # one component per file
└── demo/app.py                  # gallery (core · form · feedback · data · patterns)
```

## Components (web parity)

| Group | Components |
|-------|------------|
| Core | button, card, input, badge, nav, modal |
| Form | checkbox, radio, select, textarea, toggle |
| Feedback / nav | alert, tabs, accordion, breadcrumb, pagination |
| Data / content | table, empty-state |
| Composition | Patterns page (list · form · empty · help) |

## Fonts

Qt cannot load woff2. We ship **complete TTF** from the official IBM/plex monorepo:

- `IBMPlexSans` 400 / 500 / 600 / 700  
- `IBMPlexMono` 400 / 500  

```bash
python scripts/download_fonts.py
```

At runtime:

```python
from akana import fonts
fonts.load_fonts()  # after QApplication()
```

License: `akana/assets/fonts/OFL-IBM-Plex.txt` (SIL OFL 1.1, RFN “Plex”).

## Theme

```python
from akana.theme import set_theme
from akana import styles

set_theme("dark")   # or "light"
styles.apply(window)
```

| Semantic (light) | Role |
|------------------|------|
| `bg` | page (`gray-0`) |
| `surface` / `surface_2` | raised areas |
| `border` / `border_strong` | dividers & controls |
| `ink` | strongest mark (buttons, focus) |
| `text` / `text_secondary` / `text_muted` | type hierarchy |
| `inverse_bg` / `inverse_text` | on-ink content |

Components use **semantic** keys only — never `gray-*` primitives.
