"""Akana Qt — monochrome checkbox (square indicator, ink fill when checked)."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QWidget


class AkCheckbox(QCheckBox):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("AkCheckbox")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("akRole", "checkbox")
