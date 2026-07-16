"""Akana Qt — custom frameless window title bar."""

from __future__ import annotations

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget

from akana.icons import glyph
from akana.tokens import SPACE, TITLEBAR_H
from akana.util import hand_cursor, set_dyn


class AkTitleBarButton(QPushButton):
    def __init__(self, text: str, role: str = "chrome", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("akTitleBtn")
        set_dyn(self, "role", role)
        self.setFixedSize(44, 36)
        hand_cursor(self)
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)


class AkTitleBar(QFrame):
    """Top chrome for frameless windows."""

    minimizeClicked = pyqtSignal()
    maximizeClicked = pyqtSignal()
    closeClicked = pyqtSignal()

    def __init__(
        self,
        title: str = "Akana",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkTitleBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(TITLEBAR_H)
        self._drag_origin: QPoint | None = None
        self._window: QWidget | None = None

        root = QHBoxLayout(self)
        root.setContentsMargins(SPACE[4], 0, SPACE[2], 0)
        root.setSpacing(SPACE[3])

        mark = QLabel(glyph("mark"))
        mark.setObjectName("akTitleMark")
        root.addWidget(mark)

        self._title = QLabel(title)
        self._title.setObjectName("akTitleBarLabel")
        root.addWidget(self._title)

        self._meta = QLabel("")
        self._meta.setObjectName("akTitleBarMeta")
        root.addWidget(self._meta)

        root.addStretch(1)

        self._slot = QHBoxLayout()
        self._slot.setSpacing(SPACE[2])
        root.addLayout(self._slot)

        self._min = AkTitleBarButton(glyph("minus"), "chrome")
        self._max = AkTitleBarButton(glyph("maximize"), "chrome")
        self._close = AkTitleBarButton(glyph("close"), "close")
        self._min.clicked.connect(self.minimizeClicked.emit)
        self._max.clicked.connect(self.maximizeClicked.emit)
        self._close.clicked.connect(self.closeClicked.emit)
        root.addWidget(self._min)
        root.addWidget(self._max)
        root.addWidget(self._close)

    def set_window(self, window: QWidget) -> None:
        self._window = window

    def set_title(self, title: str) -> None:
        self._title.setText(title)

    def set_meta(self, text: str) -> None:
        self._meta.setText(text)
        self._meta.setVisible(bool(text))

    def add_action(self, widget: QWidget) -> None:
        self._slot.addWidget(widget)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self._window is not None:
            child = self.childAt(event.position().toPoint())
            if isinstance(child, QPushButton) or (
                child is not None
                and child.parent() is not None
                and isinstance(child.parent(), QPushButton)
            ):
                super().mousePressEvent(event)
                return
            self._drag_origin = (
                event.globalPosition().toPoint() - self._window.frameGeometry().topLeft()
            )
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if (
            self._drag_origin is not None
            and event.buttons() & Qt.MouseButton.LeftButton
            and self._window is not None
        ):
            if self._window.isMaximized():
                self._window.showNormal()
                self._drag_origin = QPoint(self._window.width() // 2, 20)
            self._window.move(event.globalPosition().toPoint() - self._drag_origin)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_origin = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.maximizeClicked.emit()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    def set_maximized(self, maximized: bool) -> None:
        self._max.setText(glyph("restore" if maximized else "maximize"))
