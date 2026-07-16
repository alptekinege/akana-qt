"""Akana Qt — monochrome accordion / disclosure.

Web layout: full-width trigger with title left, chevron right; panel below.
Collapsed items keep a stable min-height so divider lines never stack tight.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from akana.icons import glyph
from akana.tokens import SPACE
from akana.util import AkFlowLabel, hand_cursor, set_dyn


class AkAccordionItem(QFrame):
    def __init__(
        self,
        title: str,
        body: str = "",
        *,
        expanded: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("akAccordionItem")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._title_text = title

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._trigger = QPushButton()
        self._trigger.setObjectName("akAccordionTrigger")
        hand_cursor(self._trigger)
        self._trigger.setCheckable(True)
        self._trigger.setChecked(expanded)
        self._trigger.setFlat(True)
        self._trigger.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        # Stable row height when collapsed (prevents divider compression)
        self._trigger.setMinimumHeight(SPACE[12])
        self._trigger.clicked.connect(self._on_toggle)

        row = QHBoxLayout(self._trigger)
        row.setContentsMargins(SPACE[5], SPACE[4], SPACE[5], SPACE[4])
        row.setSpacing(SPACE[3])

        self._title_lbl = QLabel(title)
        self._title_lbl.setObjectName("akAccordionTitle")
        self._title_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._title_lbl.setWordWrap(True)
        row.addWidget(self._title_lbl, 1)

        self._chev = QLabel(glyph("chevron-down"))
        self._chev.setObjectName("akAccordionChevron")
        self._chev.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._chev.setFixedWidth(18)
        self._chev.setAlignment(Qt.AlignmentFlag.AlignCenter)
        row.addWidget(self._chev, 0)

        root.addWidget(self._trigger)

        self._panel = AkFlowLabel(body, object_name="akAccordionPanel")
        self._panel.setVisible(expanded)
        root.addWidget(self._panel)

        self._sync_chrome()

    def _on_toggle(self, checked: bool) -> None:
        self._panel.setVisible(checked)
        self._sync_chrome()

    def _sync_chrome(self) -> None:
        open_ = self._trigger.isChecked()
        self._chev.setText(glyph("chevron-up" if open_ else "chevron-down"))
        set_dyn(self._chev, "expanded", open_)
        set_dyn(self._trigger, "expanded", open_)

    def set_expanded(self, expanded: bool) -> None:
        self._trigger.setChecked(expanded)
        self._panel.setVisible(expanded)
        self._sync_chrome()

    def is_expanded(self) -> bool:
        return self._trigger.isChecked()


class AkAccordion(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("AkAccordion")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._items: list[AkAccordionItem] = []
        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(0, 0, 0, 0)
        self._root.setSpacing(0)

    def add_item(
        self,
        title: str,
        body: str = "",
        *,
        expanded: bool = False,
    ) -> AkAccordionItem:
        item = AkAccordionItem(title, body, expanded=expanded, parent=self)
        if self._items:
            set_dyn(item, "divided", True)
        self._items.append(item)
        self._root.addWidget(item)
        return item
