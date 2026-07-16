"""Akana Qt — gallery layout primitives (section / style board / panel)."""

from __future__ import annotations

from typing import Literal

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from akana.tokens import SPACE

PanelTone = Literal["default", "surface", "ink", "dashed"]


class AkShowcaseSection(QFrame):
    """Labeled block with optional lead text."""

    def __init__(
        self,
        eyebrow: str,
        title: str = "",
        lead: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkShowcaseSection")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(SPACE[4])

        head = QVBoxLayout()
        head.setSpacing(SPACE[2])
        eye = QLabel(eyebrow)
        eye.setObjectName("akLabel")
        head.addWidget(eye)
        if title:
            t = QLabel(title)
            t.setObjectName("akSectionTitle")
            t.setWordWrap(True)
            head.addWidget(t)
        if lead:
            l = QLabel(lead)
            l.setObjectName("akLead")
            l.setWordWrap(True)
            head.addWidget(l)
        root.addLayout(head)

        self._body = QVBoxLayout()
        self._body.setSpacing(SPACE[4])
        root.addLayout(self._body)

    def add_widget(self, widget: QWidget) -> None:
        self._body.addWidget(widget)

    def add_layout(self, layout) -> None:
        self._body.addLayout(layout)


class AkStyleBoard(QFrame):
    """Grid of labeled style cells — show variants side by side."""

    def __init__(
        self,
        columns: int = 2,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkStyleBoard")
        self._columns = max(1, columns)
        self._count = 0

        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(SPACE[4])
        self._grid.setVerticalSpacing(SPACE[4])

    def add_cell(self, label: str, widget: QWidget, *, span: int = 1) -> QFrame:
        cell = QFrame()
        cell.setObjectName("AkStyleCell")
        col = QVBoxLayout(cell)
        col.setContentsMargins(SPACE[4], SPACE[4], SPACE[4], SPACE[4])
        col.setSpacing(SPACE[3])

        cap = QLabel(label)
        cap.setObjectName("akLabel")
        col.addWidget(cap)
        col.addWidget(widget)
        col.addStretch(1)

        r, c = divmod(self._count, self._columns)
        self._grid.addWidget(cell, r, c, 1, span)
        self._count += span
        return cell


class AkPanel(QFrame):
    """Surface panel for grouping demos (default / surface / ink / dashed)."""

    def __init__(
        self,
        *,
        tone: PanelTone = "default",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkPanel")
        self.setProperty("tone", tone)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(False)

        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(SPACE[5], SPACE[5], SPACE[5], SPACE[5])
        self._root.setSpacing(SPACE[4])

    def set_tone(self, tone: PanelTone) -> None:
        self.setProperty("tone", tone)
        style = self.style()
        if style is not None:
            style.unpolish(self)
            style.polish(self)
        self.update()

    def add_widget(self, widget: QWidget) -> None:
        self._root.addWidget(widget)

    def add_row(self, *widgets: QWidget, stretch_last: bool = False) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(SPACE[3])
        for i, w in enumerate(widgets):
            if stretch_last and i == len(widgets) - 1:
                row.addWidget(w, 1)
            else:
                row.addWidget(w)
        if not stretch_last:
            row.addStretch(1)
        self._root.addLayout(row)
        return row

    def add_header(self, title: str, meta: str = "") -> None:
        row = QHBoxLayout()
        t = QLabel(title)
        t.setObjectName("akPanelTitle")
        row.addWidget(t)
        row.addStretch(1)
        if meta:
            m = QLabel(meta)
            m.setObjectName("akLabel")
            row.addWidget(m)
        self._root.addLayout(row)
