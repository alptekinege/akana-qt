"""Akana Qt — monochrome text input.

Mirrors web `.ak-input`: border-strong, ink focus ring, CONTROL_H height.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QLineEdit, QWidget

from akana.tokens import CONTROL_H


class AkInput(QLineEdit):
    def __init__(
        self,
        placeholder: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(CONTROL_H)
        self.setMaximumHeight(CONTROL_H)
