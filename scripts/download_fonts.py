"""Download IBM Plex Sans/Mono TTF for Qt (QFontDatabase).

Qt does not load woff2 — we ship complete TTF from the official IBM/plex
repo (SIL OFL 1.1, RFN "Plex"). Re-run after deleting assets/fonts/*.ttf.
"""

from __future__ import annotations

import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "akana", "assets", "fonts")
os.makedirs(OUT, exist_ok=True)

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Official IBM/plex monorepo paths (complete TTF, all codepoints needed offline).
BASE_SANS = (
    "https://raw.githubusercontent.com/IBM/plex/master/"
    "packages/plex-sans/fonts/complete/ttf"
)
BASE_MONO = (
    "https://raw.githubusercontent.com/IBM/plex/master/"
    "packages/plex-mono/fonts/complete/ttf"
)

FILES = [
    (f"{BASE_SANS}/IBMPlexSans-Regular.ttf", "IBMPlexSans-Regular.ttf"),
    (f"{BASE_SANS}/IBMPlexSans-Medium.ttf", "IBMPlexSans-Medium.ttf"),
    (f"{BASE_SANS}/IBMPlexSans-SemiBold.ttf", "IBMPlexSans-SemiBold.ttf"),
    (f"{BASE_SANS}/IBMPlexSans-Bold.ttf", "IBMPlexSans-Bold.ttf"),
    (f"{BASE_MONO}/IBMPlexMono-Regular.ttf", "IBMPlexMono-Regular.ttf"),
    (f"{BASE_MONO}/IBMPlexMono-Medium.ttf", "IBMPlexMono-Medium.ttf"),
]


def main() -> None:
    for url, name in FILES:
        dst = os.path.join(OUT, name)
        print(f"GET {name}…")
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(dst, "wb") as f:
            f.write(data)
        print(f"  saved {len(data)} bytes")
    print(f"\nDone → {OUT}")
    print("License: SIL OFL 1.1 — keep OFL-IBM-Plex.txt alongside fonts.")


if __name__ == "__main__":
    main()
