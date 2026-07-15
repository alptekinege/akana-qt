"""Akana Qt — monochrome nav rail / items.

Mirrors web `.ak-nav` / `.ak-nav__item` active states (weight + surface).
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget

from akana.tokens import SPACE


class AkNavItem(QPushButton):
    """Single nav entry with checkable active state."""

    def __init__(
        self,
        text: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)
        self.setObjectName("akNavItem")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)

    def set_active(self, active: bool) -> None:
        self.setChecked(active)


class AkNavRail(QFrame):
    """Vertical nav rail."""

    currentChanged = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        # Transparent host — parent supplies surface chrome (e.g. #akSidebar).
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

    def count(self) -> int:
        return len(self._items)


class AkNav(AkNavRail):
    """Alias for naming consistency with web `ak-nav`."""
