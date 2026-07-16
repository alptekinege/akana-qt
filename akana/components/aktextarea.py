"""Akana Qt — monochrome multiline text area.

Mirrors web `.ak-textarea` with a roomier desktop minimum height.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QPlainTextEdit, QWidget

from akana.tokens import TEXTAREA_MIN_H


class AkTextarea(QPlainTextEdit):
    def __init__(
        self,
        placeholder: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkTextarea")
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(TEXTAREA_MIN_H)
        self.setTabChangesFocus(True)
        self.document().setDocumentMargin(0)
