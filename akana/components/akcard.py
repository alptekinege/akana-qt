"""Akana Qt — monochrome card container.

Mirrors web `.ak-card`: bg, soft border, large radius, optional icon mark,
title, body, and mono text action.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from akana.tokens import CARD_ICON, SPACE


class AkCard(QFrame):
    """Monochrome card with optional icon / title / body / action helpers."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setObjectName("AkCard")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(SPACE[6], SPACE[6], SPACE[6], SPACE[6])
        self._root.setSpacing(SPACE[2])

        self._icon: QLabel | None = None
        self._title: QLabel | None = None
        self._body: QLabel | None = None
        self._action: QLabel | None = None

    def set_icon_mark(self, glyph: str = "◆") -> QLabel:
        """Web-style 38×38 bordered icon mark (text glyph, not an image)."""
        if self._icon is None:
            self._icon = QLabel()
            self._icon.setObjectName("akCardIcon")
            self._icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._icon.setFixedSize(CARD_ICON, CARD_ICON)
            self._icon.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            self._root.insertWidget(0, self._icon)
        self._icon.setText(glyph)
        return self._icon

    def set_title(self, text: str) -> QLabel:
        if self._title is None:
            self._title = QLabel()
            self._title.setObjectName("akCardTitle")
            self._title.setWordWrap(True)
            idx = 1 if self._icon is not None else 0
            self._root.insertWidget(idx, self._title)
        self._title.setText(text)
        return self._title

    def set_body(self, text: str) -> QLabel:
        if self._body is None:
            self._body = QLabel()
            self._body.setObjectName("akCardBody")
            self._body.setWordWrap(True)
            idx = self._root.count()
            # insert after title if present
            if self._title is not None:
                idx = self._root.indexOf(self._title) + 1
            elif self._icon is not None:
                idx = 1
            else:
                idx = 0
            self._root.insertWidget(idx, self._body)
        self._body.setText(text)
        return self._body

    def set_action(self, text: str) -> QLabel:
        """Mono uppercase text action (web `.ak-card__action`)."""
        if self._action is None:
            self._action = QLabel()
            self._action.setObjectName("akCardAction")
            self._root.addWidget(self._action)
        self._action.setText(text)
        return self._action

    def add_widget(self, widget: QWidget) -> None:
        self._root.addWidget(widget)

    def set_content(self, widget: QWidget) -> None:
        """Replace content with a single child widget (legacy API)."""
        while self._root.count():
            item = self._root.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
        self._icon = None
        self._title = None
        self._body = None
        self._action = None
        self._root.addWidget(widget)
