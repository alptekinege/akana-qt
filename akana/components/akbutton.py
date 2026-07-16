"""Akana Qt — monochrome button (primary / secondary / ghost).

Mirrors web `.ak-btn` + variants. Primary = ink fill + inverse text.
State via weight/border/opacity — no accent hue.
"""

from __future__ import annotations

from typing import Literal

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget

Variant = Literal["primary", "secondary", "ghost", "inverse"]
Size = Literal["sm", "md", "lg"]


class AkButton(QPushButton):
    def __init__(
        self,
        text: str = "",
        *,
        variant: Variant = "primary",
        size: Size = "md",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_variant(variant)
        self.set_size(size)

    def set_variant(self, variant: Variant) -> None:
        self.setProperty("variant", variant)
        self._repolish()

    def set_size(self, size: Size) -> None:
        # Do not use property name "size" — conflicts with QWidget.size.
        self.setProperty("akSize", size)
        self._repolish()

    def _repolish(self) -> None:
        style = self.style()
        if style is not None:
            style.unpolish(self)
            style.polish(self)
        self.update()
