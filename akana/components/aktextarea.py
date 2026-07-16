"""Akana Qt — monochrome multiline text area."""

from __future__ import annotations

from PyQt6.QtWidgets import QPlainTextEdit, QWidget


class AkTextarea(QPlainTextEdit):
    def __init__(
        self,
        placeholder: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkTextarea")
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(140)
        self.setTabChangesFocus(True)
        self.document().setDocumentMargin(0)
