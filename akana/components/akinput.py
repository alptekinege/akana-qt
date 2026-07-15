"""Akana Qt — monochrome text input.

Mirrors web `.ak-input`: border-strong, ink focus ring.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QLineEdit, QWidget


class AkInput(QLineEdit):
    def __init__(
        self,
        placeholder: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(44)
