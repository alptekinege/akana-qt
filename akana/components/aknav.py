"""Akana Qt — monochrome nav rail + segmented strip (web `.ak-nav`)."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from akana.tokens import SPACE
from akana.util import hand_cursor


class AkNavItem(QPushButton):
    """Single nav entry with checkable active state."""

    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("akNavItem")
        self.setCheckable(True)
        self.setAutoExclusive(False)
        hand_cursor(self)
        self.setFlat(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumHeight(40)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_active(self, active: bool) -> None:
        self.setChecked(active)
        from akana.util import repolish

        repolish(self)


class AkNavRail(QFrame):
    """Vertical nav rail for application shells."""

    currentChanged = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("akNavRail")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._items: list[AkNavItem] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(SPACE[1])
        self._list = QVBoxLayout()
        self._list.setSpacing(SPACE[1])
        root.addLayout(self._list)
        root.addStretch(1)

    def add_item(self, text: str) -> AkNavItem:
        item = AkNavItem(text, self)
        index = len(self._items)
        item.clicked.connect(lambda _=False, i=index: self.set_current_index(i))
        self._items.append(item)
        self._list.addWidget(item)
        return item

    def set_current_index(self, index: int) -> None:
        for i, item in enumerate(self._items):
            item.set_active(i == index)
        if 0 <= index < len(self._items):
            self.currentChanged.emit(index)

    def current_index(self) -> int:
        for i, item in enumerate(self._items):
            if item.isChecked():
                return i
        return -1

    def count(self) -> int:
        return len(self._items)


class AkNavStrip(QFrame):
    """Horizontal segmented nav (web `.ak-nav` surface shell).

    Packs to content width on the left — does not stretch to full page width.
    """

    currentChanged = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("AkNavStrip")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._items: list[AkNavItem] = []

        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(SPACE[1], SPACE[1], SPACE[1], SPACE[1])
        self._row.setSpacing(SPACE[1])
        self._row.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    def add_item(self, text: str) -> AkNavItem:
        item = AkNavItem(text, self)
        item.setObjectName("akNavStripItem")
        item.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        index = len(self._items)
        item.clicked.connect(lambda _=False, i=index: self.set_current_index(i))
        self._items.append(item)
        self._row.addWidget(item)
        if index == 0:
            self.set_current_index(0)
        return item

    def set_current_index(self, index: int) -> None:
        for i, item in enumerate(self._items):
            item.set_active(i == index)
        if 0 <= index < len(self._items):
            self.currentChanged.emit(index)


class AkNav(AkNavRail):
    """Alias for naming consistency with web `ak-nav`."""
