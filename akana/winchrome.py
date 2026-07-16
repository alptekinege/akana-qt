"""Windows frameless helpers — enable Win+Up / snap without nativeEvent.

Why no nativeEvent?
  PyQt6's QWidget.nativeEvent base returns ``(False, None)``. Forwarding that
  (or mishandling WM_*) makes CreateWindowEx fail with ERROR_INVALID_PARAMETER
  (\"Parametre hatalı\"). Style-bit restore after show is enough for snap.
"""

from __future__ import annotations

import ctypes
import sys
from typing import Any

GWL_STYLE = -16
WS_THICKFRAME = 0x00040000
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_SYSMENU = 0x00080000


def is_windows() -> bool:
    return sys.platform == "win32"


def _hwnd_of(window: Any) -> int | None:
    try:
        wid = window.winId()
    except Exception:
        return None
    if wid is None:
        return None
    try:
        hwnd = int(wid)
    except (TypeError, ValueError):
        return None
    return hwnd or None


def enable_snap_for_frameless(window: Any) -> bool:
    """After show(), add thick-frame + max/min so Aero Snap / Win+Up work.

    Safe: does not install nativeEvent handlers.
    """
    if not is_windows():
        return False
    hwnd = _hwnd_of(window)
    if not hwnd:
        return False
    user32 = ctypes.windll.user32
    try:
        style = user32.GetWindowLongW(hwnd, GWL_STYLE)
        new_style = style | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_SYSMENU
        if new_style == style:
            return True
        user32.SetWindowLongW(hwnd, GWL_STYLE, new_style)
        SWP_FRAMECHANGED = 0x0020
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_NOZORDER = 0x0004
        SWP_NOACTIVATE = 0x0010
        user32.SetWindowPos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE,
        )
        return True
    except Exception:
        return False
