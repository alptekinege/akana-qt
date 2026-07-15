"""Akana Qt — monochrome radio button."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QButtonGroup, QRadioButton, QVBoxLayout, QWidget

from akana.tokens import SPACE


class AkRadio(QRadioButton):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("AkRadio")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class AkRadioGroup(QWidget):
    """Vertical group of exclusive radios."""

    def __init__(
        self,
        labels: list[str] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACE[3])
        self._radios: list[AkRadio] = []
        for label in labels or []:
            self.add_option(label)

    def add_option(self, text: str) -> AkRadio:
        radio = AkRadio(text, self)
        self._group.addButton(radio, len(self._radios))
        self.layout().addWidget(radio)  # type: ignore[union-attr]
        self._radios.append(radio)
        return radio

    def checked_index(self) -> int:
        return self._group.checkedId()

    def set_checked_index(self, index: int) -> None:
        btn = self._group.button(index)
        if btn is not None:
            btn.setChecked(True)
