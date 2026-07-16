"""Akana Qt — gallery layout primitives (section / style board / panel).

Layout is **start/top** biased: cells share a row without vertical centering
theater; panels pack content to the top-left.
"""

from __future__ import annotations

from typing import Literal

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from akana.tokens import SPACE
from akana.util import set_dyn

PanelTone = Literal["default", "surface", "ink", "dashed"]


class AkShowcaseSection(QFrame):
    """Labeled block with optional lead text (left-aligned measure)."""

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
        root.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        head = QVBoxLayout()
        head.setSpacing(SPACE[2])
        head.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        eye = QLabel(eyebrow)
        eye.setObjectName("akLabel")
        head.addWidget(eye, 0, Qt.AlignmentFlag.AlignLeft)
        if title:
            t = QLabel(title)
            t.setObjectName("akSectionTitle")
            t.setWordWrap(True)
            head.addWidget(t, 0, Qt.AlignmentFlag.AlignLeft)
        if lead:
            l = QLabel(lead)
            l.setObjectName("akLead")
            l.setWordWrap(True)
            l.setMaximumWidth(560)  # ~60ch at lead size
            head.addWidget(l, 0, Qt.AlignmentFlag.AlignLeft)
        root.addLayout(head)

        self._body = QVBoxLayout()
        self._body.setSpacing(SPACE[4])
        self._body.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        root.addLayout(self._body)

    def add_widget(self, widget: QWidget) -> None:
        self._body.addWidget(widget, 0, Qt.AlignmentFlag.AlignLeft)

    def add_layout(self, layout) -> None:
        self._body.addLayout(layout)


class AkStyleBoard(QFrame):
    """Grid of labeled style cells — top-aligned, equal columns."""

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
        self._grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def add_cell(self, label: str, widget: QWidget, *, span: int = 1) -> QFrame:
        cell = QFrame()
        cell.setObjectName("AkStyleCell")
        cell.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        cell.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        col = QVBoxLayout(cell)
        col.setContentsMargins(SPACE[4], SPACE[4], SPACE[4], SPACE[4])
        col.setSpacing(SPACE[3])
        col.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        cap = QLabel(label)
        cap.setObjectName("akLabel")
        col.addWidget(cap, 0, Qt.AlignmentFlag.AlignLeft)
        col.addWidget(widget, 0, Qt.AlignmentFlag.AlignLeft)
        # No trailing stretch — avoid tall empty “centered” voids in short cells

        r, c = divmod(self._count, self._columns)
        self._grid.addWidget(
            cell, r, c, 1, span, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
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
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(SPACE[5], SPACE[5], SPACE[5], SPACE[5])
        self._root.setSpacing(SPACE[4])
        self._root.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def set_tone(self, tone: PanelTone) -> None:
        set_dyn(self, "tone", tone)

    def add_widget(self, widget: QWidget) -> None:
        self._root.addWidget(widget, 0, Qt.AlignmentFlag.AlignLeft)

    def add_row(self, *widgets: QWidget, stretch_last: bool = False) -> QHBoxLayout:
        """Horizontal cluster packed to the **start** (left)."""
        row = QHBoxLayout()
        row.setSpacing(SPACE[3])
        row.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        for i, w in enumerate(widgets):
            if stretch_last and i == len(widgets) - 1:
                row.addWidget(w, 1)
            else:
                row.addWidget(w, 0)
        if not stretch_last:
            row.addStretch(1)  # free space on the right, not both sides
        self._root.addLayout(row)
        return row

    def add_header(self, title: str, meta: str = "") -> None:
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        t = QLabel(title)
        t.setObjectName("akPanelTitle")
        row.addWidget(t, 0)
        row.addStretch(1)
        if meta:
            m = QLabel(meta)
            m.setObjectName("akLabel")
            row.addWidget(m, 0)
        self._root.addLayout(row)
