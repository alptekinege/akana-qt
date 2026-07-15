"""Akana Qt — monochrome modal / dialog.

Mirrors web `.ak-modal`: bg panel, border-strong, title + actions.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from akana.components.akbutton import AkButton
from akana.tokens import SPACE


class AkModal(QDialog):
    """Centered frameless modal with title, content slot, and actions."""

    def __init__(self, title: str = "Dialog", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setModal(True)
        self.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._build_ui(title)

    def _build_ui(self, title: str) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(SPACE[6], SPACE[6], SPACE[6], SPACE[6])
        root.setSpacing(0)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("akModalCard")
        card.setFixedWidth(440)
        card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        cv = QVBoxLayout(card)
        cv.setContentsMargins(SPACE[8], SPACE[8], SPACE[8], SPACE[8])
        cv.setSpacing(SPACE[3])

        title_lbl = QLabel(title)
        title_lbl.setObjectName("akModalTitle")
        cv.addWidget(title_lbl)

        self._content = QFrame()
        self._content.setObjectName("akModalBody")
        cl = QVBoxLayout(self._content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(SPACE[2])
        cv.addWidget(self._content, 1)

        actions = QFrame()
        ah = QHBoxLayout(actions)
        ah.setContentsMargins(0, SPACE[3], 0, 0)
        ah.setSpacing(SPACE[3])
        ah.addStretch(1)

        self._cancel = AkButton("Cancel", variant="secondary")
        self._cancel.clicked.connect(self.reject)
        self._confirm = AkButton("Confirm", variant="primary")
        self._confirm.clicked.connect(self.accept)
        ah.addWidget(self._cancel)
        ah.addWidget(self._confirm)
        cv.addWidget(actions)

        root.addWidget(card)

        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)

    def set_content(self, widget: QWidget) -> None:
        layout = self._content.layout()
        if layout is not None:
            layout.addWidget(widget)

    def set_confirm_text(self, text: str) -> None:
        self._confirm.setText(text)

    def set_cancel_text(self, text: str) -> None:
        self._cancel.setText(text)
