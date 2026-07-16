"""Akana Qt — monochrome modal / dialog (web `.ak-modal`).

Frameless card on a 50% ink scrim. Escape closes. Confirm / cancel actions.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QGuiApplication, QKeyEvent, QPainter
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
from akana.theme import get_theme
from akana.tokens import MODAL_W, SPACE


class AkModal(QDialog):
    """Centered frameless modal with title, content slot, and actions."""

    def __init__(self, title: str = "Dialog", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setModal(True)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._card: QFrame | None = None
        self._build_ui(title)
        # Cover parent or screen so scrim is meaningful
        self._size_to_host()

    def _size_to_host(self) -> None:
        parent = self.parentWidget()
        if parent is not None:
            self.setGeometry(parent.rect())
            # map to global for window-level dialog
            top_left = parent.mapToGlobal(parent.rect().topLeft())
            self.setGeometry(
                top_left.x(),
                top_left.y(),
                parent.width(),
                parent.height(),
            )
        else:
            screen = QGuiApplication.primaryScreen()
            if screen is not None:
                self.setGeometry(screen.availableGeometry())

    def _build_ui(self, title: str) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(SPACE[6], SPACE[6], SPACE[6], SPACE[6])
        root.setSpacing(0)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("akModalCard")
        card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        card.setFixedWidth(MODAL_W)
        card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self._card = card

        cv = QVBoxLayout(card)
        cv.setContentsMargins(SPACE[8], SPACE[8], SPACE[8], SPACE[8])
        cv.setSpacing(SPACE[3])

        title_lbl = QLabel(title)
        title_lbl.setObjectName("akModalTitle")
        title_lbl.setWordWrap(True)
        cv.addWidget(title_lbl)

        self._content = QFrame()
        self._content.setObjectName("akModalBody")
        cl = QVBoxLayout(self._content)
        cl.setContentsMargins(0, SPACE[1], 0, SPACE[3])
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
        self._apply_shadow()

    def paintEvent(self, event) -> None:  # noqa: N802
        # Scrim: monochrome 50% ink (web modal overlay)
        t = get_theme()
        ink = QColor(t["ink"])
        # Use black-ish with alpha for both themes (web uses rgba(10,10,10,0.5))
        scrim = QColor(10, 10, 10, 128)
        p = QPainter(self)
        p.fillRect(self.rect(), scrim)
        p.end()
        super().paintEvent(event)

    def _apply_shadow(self) -> None:
        if self._card is None:
            return
        theme = get_theme()
        ink = theme.get("ink", "#0a0a0a").lower()
        is_light_theme_ink = ink in ("#0a0a0a", "#000000")
        alpha = 70 if is_light_theme_ink else 120
        shadow = QGraphicsDropShadowEffect(self._card)
        shadow.setBlurRadius(28)
        shadow.setColor(QColor(0, 0, 0, alpha))
        shadow.setOffset(0, 6)
        self._card.setGraphicsEffect(shadow)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)

    def set_content(self, widget: QWidget) -> None:
        layout = self._content.layout()
        if layout is not None:
            layout.addWidget(widget)

    def set_confirm_text(self, text: str) -> None:
        self._confirm.setText(text)

    def set_cancel_text(self, text: str) -> None:
        self._cancel.setText(text)

    def showEvent(self, event) -> None:  # noqa: N802
        self._size_to_host()
        super().showEvent(event)
        self._confirm.setFocus(Qt.FocusReason.ActiveWindowFocusReason)
