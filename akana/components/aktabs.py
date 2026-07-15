"""Akana Qt — monochrome tabs (underline active state)."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from akana.tokens import SPACE


class AkTabButton(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("akTab")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)


class AkTabs(QFrame):
    """Tab list + stacked panels."""

    currentChanged = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("AkTabs")
        self._tabs: list[AkTabButton] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(SPACE[5])

        self._list = QFrame()
        self._list.setObjectName("akTabList")
        self._list_layout = QHBoxLayout(self._list)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(SPACE[1])
        self._list_layout.addStretch(1)
        root.addWidget(self._list)

        self._stack = QStackedWidget()
        root.addWidget(self._stack, 1)

    def add_tab(self, title: str, widget: QWidget) -> int:
        index = len(self._tabs)
        btn = AkTabButton(title, self._list)
        btn.clicked.connect(lambda _=False, i=index: self.set_current_index(i))
        # insert before stretch
        self._list_layout.insertWidget(index, btn)
        self._tabs.append(btn)
        self._stack.addWidget(widget)
        if index == 0:
            self.set_current_index(0)
        return index

    def set_current_index(self, index: int) -> None:
        for i, tab in enumerate(self._tabs):
            tab.setChecked(i == index)
        if 0 <= index < self._stack.count():
            self._stack.setCurrentIndex(index)
            self.currentChanged.emit(index)

    def current_index(self) -> int:
        return self._stack.currentIndex()
