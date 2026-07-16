"""Akana Qt — gallery link card (web index `.ak-link`).

Name + description + trailing glyph. Emits activated when clicked.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from akana.icons import glyph
from akana.tokens import SPACE
from akana.util import AkFlowLabel, hand_cursor


class AkLinkCard(QFrame):
    activated = pyqtSignal()

    def __init__(
        self,
        name: str,
        description: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkLinkCard")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        hand_cursor(self)

        root = QHBoxLayout(self)
        root.setContentsMargins(SPACE[5], SPACE[4], SPACE[5], SPACE[4])
        root.setSpacing(SPACE[4])

        col = QVBoxLayout()
        col.setSpacing(SPACE[2])
        col.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._name = AkFlowLabel(name, object_name="akLinkName")
        col.addWidget(self._name)

        self._desc = AkFlowLabel(description, object_name="akLinkDesc")
        self._desc.setVisible(bool(description))
        col.addWidget(self._desc)
        root.addLayout(col, 1)

        self._go = QLabel(glyph("arrow-right"))
        self._go.setObjectName("akLinkGo")
        self._go.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._go, 0, Qt.AlignmentFlag.AlignVCenter)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.activated.emit()
            event.accept()
            return
        super().mousePressEvent(event)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.activated.emit()
            event.accept()
            return
        super().keyPressEvent(event)

    def enterEvent(self, event) -> None:  # noqa: N802
        self.setProperty("hovered", True)
        from akana.util import repolish

        repolish(self)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self.setProperty("hovered", False)
        from akana.util import repolish

        repolish(self)
        super().leaveEvent(event)
