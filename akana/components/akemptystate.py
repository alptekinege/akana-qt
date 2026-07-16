"""Akana Qt — monochrome empty state (web `.ak-empty`).

Default alignment is **start/left** for product chrome. Use align='center'
only when a deliberately centered empty surface is needed.
"""

from __future__ import annotations

from typing import Literal

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from akana.icons import glyph
from akana.tokens import SPACE
from akana.util import set_dyn

Align = Literal["start", "center"]


class AkEmptyState(QFrame):
    def __init__(
        self,
        title: str = "Nothing here",
        body: str = "",
        *,
        icon: str | None = None,
        align: Align = "start",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkEmptyState")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._align: Align = align
        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(SPACE[8], SPACE[8], SPACE[8], SPACE[8])
        self._root.setSpacing(SPACE[2])

        self._icon = QLabel(icon if icon is not None else glyph("empty"))
        self._icon.setObjectName("akEmptyIcon")
        self._icon.setFixedSize(48, 48)
        self._icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._icon.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._root.addWidget(self._icon)
        self._root.addSpacing(SPACE[3])

        self._title = QLabel(title)
        self._title.setObjectName("akEmptyTitle")
        self._title.setWordWrap(True)
        self._root.addWidget(self._title)

        self._body = QLabel(body)
        self._body.setObjectName("akEmptyBody")
        self._body.setWordWrap(True)
        self._body.setMaximumWidth(360)
        self._body.setVisible(bool(body))
        self._root.addWidget(self._body)

        self._actions_host = QWidget()
        self._actions = QHBoxLayout(self._actions_host)
        self._actions.setContentsMargins(0, 0, 0, 0)
        self._actions.setSpacing(SPACE[3])
        self._root.addSpacing(SPACE[4])
        self._root.addWidget(self._actions_host)

        self.set_align(align)

    def set_align(self, align: Align) -> None:
        self._align = align
        set_dyn(self, "align", align)
        if align == "center":
            ha = Qt.AlignmentFlag.AlignHCenter
            ta = Qt.AlignmentFlag.AlignCenter
            self._root.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            self._actions.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        else:
            ha = Qt.AlignmentFlag.AlignLeft
            ta = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            self._root.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            self._actions.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._root.setAlignment(self._icon, ha)
        self._root.setAlignment(self._title, ha)
        self._root.setAlignment(self._body, ha)
        self._root.setAlignment(self._actions_host, ha)
        self._title.setAlignment(ta)
        self._body.setAlignment(ta)

    def add_action(self, widget: QWidget) -> None:
        # Insert before trailing stretch if present
        stretch_at = -1
        for i in range(self._actions.count()):
            item = self._actions.itemAt(i)
            if item is not None and item.spacerItem() is not None:
                stretch_at = i
                break
        if stretch_at >= 0:
            self._actions.insertWidget(stretch_at, widget)
        else:
            self._actions.addWidget(widget)
            if self._align == "start":
                self._actions.addStretch(1)

    def set_title(self, title: str) -> None:
        self._title.setText(title)

    def set_body(self, body: str) -> None:
        self._body.setText(body)
        self._body.setVisible(bool(body))

    def set_icon(self, glyph_text: str) -> None:
        self._icon.setText(glyph_text)
