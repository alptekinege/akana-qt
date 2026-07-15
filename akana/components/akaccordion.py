"""Akana Qt — monochrome accordion / disclosure."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from akana.tokens import SPACE


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
        self._title = title

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._trigger = QPushButton()
        self._trigger.setObjectName("akAccordionTrigger")
        self._trigger.setCursor(Qt.CursorShape.PointingHandCursor)
        self._trigger.setCheckable(True)
        self._trigger.setChecked(expanded)
        self._trigger.clicked.connect(self._on_toggle)
        root.addWidget(self._trigger)

        self._panel = QLabel(body)
        self._panel.setObjectName("akAccordionPanel")
        self._panel.setWordWrap(True)
        self._panel.setVisible(expanded)
        root.addWidget(self._panel)

        self._sync_label()

    def _on_toggle(self, checked: bool) -> None:
        self._panel.setVisible(checked)
        self._sync_label()

    def _sync_label(self) -> None:
        mark = "▴" if self._trigger.isChecked() else "▾"
        self._trigger.setText(f"{self._title}    {mark}")

    def set_expanded(self, expanded: bool) -> None:
        self._trigger.setChecked(expanded)
        self._panel.setVisible(expanded)
        self._sync_label()

    def is_expanded(self) -> bool:
        return self._trigger.isChecked()


class AkAccordion(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("AkAccordion")
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
            item.setProperty("divided", True)
            style = item.style()
            if style is not None:
                style.unpolish(item)
                style.polish(item)
        self._items.append(item)
        self._root.addWidget(item)
        return item
