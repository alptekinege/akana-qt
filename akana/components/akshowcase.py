"""Akana Qt — gallery layout primitives (section / style board / panel).

Layout is **start/top** biased: content packs to the top-left, but children
**expand horizontally** to the content measure so tables and panels are not
squeezed to sizeHint width.
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

from akana.tokens import LEAD_W, SPACE
from akana.util import AkFlowLabel, set_dyn

PanelTone = Literal["default", "surface", "ink", "dashed"]


def _h_expand(w: QWidget) -> None:
    """Prefer full column width; height from content (no vertical squish)."""
    w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)


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
        _h_expand(self)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(SPACE[5])
        root.setAlignment(Qt.AlignmentFlag.AlignTop)

        head = QVBoxLayout()
        # Title → lead needs more air than SPACE[2] or wrapped lines stack
        head.setSpacing(SPACE[3])
        head.setAlignment(Qt.AlignmentFlag.AlignTop)

        eye = QLabel(eyebrow)
        eye.setObjectName("akLabel")
        head.addWidget(eye)

        if title:
            t = QLabel(title)
            t.setObjectName("akSectionTitle")
            t.setWordWrap(True)
            t.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            head.addWidget(t)

        if lead:
            l = QLabel(lead)
            l.setObjectName("akLead")
            l.setWordWrap(True)
            l.setMaximumWidth(LEAD_W)
            # Minimum height-for-width so multi-line leads never overlap siblings
            l.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
            l.setContentsMargins(0, SPACE[1], 0, SPACE[1])
            head.addWidget(l)

        root.addLayout(head)

        self._body = QVBoxLayout()
        self._body.setSpacing(SPACE[4])
        self._body.setAlignment(Qt.AlignmentFlag.AlignTop)
        root.addLayout(self._body)

    def add_widget(self, widget: QWidget) -> None:
        _h_expand(widget)
        # No AlignLeft — that forces sizeHint width and breaks tables/boards
        self._body.addWidget(widget)

    def add_layout(self, layout) -> None:
        self._body.addLayout(layout)


class AkStyleBoard(QFrame):
    """Grid of labeled style cells — top-aligned, equal columns, full width."""

    def __init__(
        self,
        columns: int = 2,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkStyleBoard")
        self._columns = max(1, columns)
        self._count = 0
        _h_expand(self)

        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(SPACE[4])
        self._grid.setVerticalSpacing(SPACE[4])
        self._grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Equal column stretch so cells share the content measure
        for c in range(self._columns):
            self._grid.setColumnStretch(c, 1)

    def add_cell(self, label: str, widget: QWidget, *, span: int = 1) -> QFrame:
        cell = QFrame()
        cell.setObjectName("AkStyleCell")
        cell.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # Expanding width; Minimum height so content is never clipped by Maximum
        cell.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        col = QVBoxLayout(cell)
        col.setContentsMargins(SPACE[4], SPACE[4], SPACE[4], SPACE[4])
        col.setSpacing(SPACE[3])
        col.setAlignment(Qt.AlignmentFlag.AlignTop)

        cap = QLabel(label)
        cap.setObjectName("akLabel")
        col.addWidget(cap)

        _h_expand(widget)
        col.addWidget(widget)

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
        # Minimum (not Maximum) vertical — Maximum clips nested tables/empty
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(SPACE[5], SPACE[5], SPACE[5], SPACE[5])
        self._root.setSpacing(SPACE[4])
        self._root.setAlignment(Qt.AlignmentFlag.AlignTop)

    def set_tone(self, tone: PanelTone) -> None:
        set_dyn(self, "tone", tone)

    def add_widget(self, widget: QWidget) -> None:
        _h_expand(widget)
        self._root.addWidget(widget)

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
