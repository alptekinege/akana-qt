"""Akana Qt — monochrome select / combo box.

Mirrors web `.ak-select`: CONTROL_H height, border-strong, ink focus.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QComboBox, QWidget

from akana.tokens import CONTROL_H


class AkSelect(QComboBox):
    def __init__(
        self,
        items: list[str] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkSelect")
        self.setMinimumHeight(CONTROL_H)
        self.setMaximumHeight(CONTROL_H)
        if items:
            self.addItems(items)
