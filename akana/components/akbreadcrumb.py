"""Akana Qt — monochrome breadcrumb trail."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget

from akana.icons import glyph
from akana.tokens import SPACE
from akana.util import hand_cursor


class AkBreadcrumb(QFrame):
    """Horizontal trail: items with separators; last is current page."""

    itemClicked = pyqtSignal(int)

    def __init__(
        self,
        items: list[str] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkBreadcrumb")
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(SPACE[2])
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        if items:
            self.set_items(items)

    def set_items(self, items: list[str]) -> None:
        while self._layout.count():
            child = self._layout.takeAt(0)
            w = child.widget()
            if w is not None:
                w.deleteLater()

        for i, label in enumerate(items):
            if i > 0:
                sep = QLabel(glyph("chevron-right"))
                sep.setObjectName("akBreadcrumbSep")
                self._layout.addWidget(sep)

            is_last = i == len(items) - 1
            if is_last:
                cur = QLabel(label)
                cur.setObjectName("akBreadcrumbCurrent")
                self._layout.addWidget(cur)
            else:
                btn = QPushButton(label)
                btn.setObjectName("akBreadcrumbLink")
                hand_cursor(btn)
                btn.setFlat(True)
                idx = i
                btn.clicked.connect(lambda _=False, j=idx: self.itemClicked.emit(j))
                self._layout.addWidget(btn)

        self._layout.addStretch(1)
