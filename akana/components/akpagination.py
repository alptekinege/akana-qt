"""Akana Qt — monochrome pagination controls."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSizePolicy, QWidget

from akana.tokens import PAGE_BTN, SPACE
from akana.util import hand_cursor


class AkPagination(QFrame):
    """Prev / page numbers / next. Emits pageChanged (1-based).

    Buttons are fixed squares; QSS uses a constant border width so the active
    ring never shifts geometry (no vertical misalignment).
    """

    pageChanged = pyqtSignal(int)

    def __init__(
        self,
        total_pages: int = 5,
        current: int = 1,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkPagination")
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._total = max(1, total_pages)
        self._current = min(max(1, current), self._total)
        self._page_btns: list[QPushButton] = []
        side = PAGE_BTN

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(SPACE[1])
        self._layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self._prev = self._make_btn("‹", side, checkable=False)
        self._prev.clicked.connect(lambda: self.set_page(self._current - 1))
        self._layout.addWidget(self._prev, 0, Qt.AlignmentFlag.AlignVCenter)

        for n in range(1, self._total + 1):
            btn = self._make_btn(str(n), side, checkable=True)
            page = n
            btn.clicked.connect(lambda _=False, p=page: self.set_page(p))
            self._layout.addWidget(btn, 0, Qt.AlignmentFlag.AlignVCenter)
            self._page_btns.append(btn)

        self._next = self._make_btn("›", side, checkable=False)
        self._next.clicked.connect(lambda: self.set_page(self._current + 1))
        self._layout.addWidget(self._next, 0, Qt.AlignmentFlag.AlignVCenter)

        self._sync()

    def _make_btn(self, text: str, side: int, *, checkable: bool) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("akPageBtn")
        btn.setCheckable(checkable)
        btn.setFixedSize(side, side)
        btn.setFlat(True)
        btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        hand_cursor(btn)
        return btn

    def set_page(self, page: int) -> None:
        page = min(max(1, page), self._total)
        changed = page != self._current
        self._current = page
        self._sync()
        if changed:
            self.pageChanged.emit(self._current)

    def current_page(self) -> int:
        return self._current

    def _sync(self) -> None:
        for i, btn in enumerate(self._page_btns, start=1):
            btn.setChecked(i == self._current)
        self._prev.setEnabled(self._current > 1)
        self._next.setEnabled(self._current < self._total)
