# Fonts — IBM Plex (SIL OFL 1.1)

Akana Qt ships **IBM Plex Sans** and **IBM Plex Mono** as local TTF files
under `akana/assets/fonts/`.

## Why TTF (not woff2)

Qt’s `QFontDatabase.addApplicationFont()` supports TrueType/OpenType.
The web Akana package uses woff2 for browsers; this port uses the same
families and weights as **complete TTF** from the official IBM/plex repo.

## Files

| File | Family | Weight |
|------|--------|--------|
| IBMPlexSans-Regular.ttf | IBM Plex Sans | 400 |
| IBMPlexSans-Medium.ttf | IBM Plex Sans | 500 |
| IBMPlexSans-SemiBold.ttf | IBM Plex Sans | 600 |
| IBMPlexSans-Bold.ttf | IBM Plex Sans | 700 |
| IBMPlexMono-Regular.ttf | IBM Plex Mono | 400 |
| IBMPlexMono-Medium.ttf | IBM Plex Mono | 500 |

## License

- License text: `akana/assets/fonts/OFL-IBM-Plex.txt`
- SIL Open Font License 1.1
- Reserved Font Name **“Plex”** — do not rename derivatives to “Plex”

## Re-download

```bash
python scripts/download_fonts.py
```

Source: [IBM/plex](https://github.com/IBM/plex) packages  
`plex-sans` / `plex-mono` → `fonts/complete/ttf/`.

## Runtime

```python
from PyQt6.QtWidgets import QApplication
from akana import fonts

app = QApplication([])
fonts.load_fonts()
```

If files are missing, the UI falls back to system-ui (still monochrome).
