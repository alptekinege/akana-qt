"""Akana Qt — monochrome card container.

Mirrors web `.ak-card`: bg surface, soft border, large radius.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from akana.tokens import SPACE


class AkCard(QFrame):
    """Monochrome card with optional title/body helpers."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setObjectName("AkCard")

        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(SPACE[6], SPACE[6], SPACE[6], SPACE[6])
        self._root.setSpacing(SPACE[2])

        self._title: QLabel | None = None
        self._body: QLabel | None = None

    def set_title(self, text: str) -> QLabel:
        if self._title is None:
            self._title = QLabel()
            self._title.setObjectName("akCardTitle")
            self._title.setWordWrap(True)
            self._root.insertWidget(0, self._title)
        self._title.setText(text)
        return self._title

    def set_body(self, text: str) -> QLabel:
        if self._body is None:
            self._body = QLabel()
            self._body.setObjectName("akCardBody")
            self._body.setWordWrap(True)
            # after title if present
            idx = 1 if self._title is not None else 0
            self._root.insertWidget(idx, self._body)
        self._body.setText(text)
        return self._body

    def add_widget(self, widget: QWidget) -> None:
        self._root.addWidget(widget)

    def set_content(self, widget: QWidget) -> None:
        """Replace content with a single child widget (legacy API)."""
        while self._root.count():
            item = self._root.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
        self._title = None
        self._body = None
        self._root.addWidget(widget)
