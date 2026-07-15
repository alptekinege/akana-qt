"""Akana Qt — monochrome select / combo box."""

from __future__ import annotations

from PyQt6.QtWidgets import QComboBox, QWidget


class AkSelect(QComboBox):
    def __init__(
        self,
        items: list[str] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkSelect")
        self.setMinimumHeight(44)
        if items:
            self.addItems(items)
