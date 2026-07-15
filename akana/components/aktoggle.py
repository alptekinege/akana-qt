"""Akana Qt — monochrome toggle / switch.

Mirrors web `.ak-toggle`: track surface-2, checked = ink fill.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QWidget

from akana.tokens import SPACE


class AkToggle(QCheckBox):
    """Standalone themed checkbox styled as a switch track."""

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("AkToggle")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class AkToggleSwitch(QFrame):
    """Label + themed switch (web-like composition)."""

    def __init__(self, text: str = "Toggle", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("AkToggleSwitch")

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(SPACE[3])

        self._box = AkToggle()
        self._label = QLabel(text)
        self._label.setObjectName("akMuted")

        root.addWidget(self._box, 0)
        root.addWidget(self._label, 0)
        root.addStretch(1)

        self._box.toggled.connect(self._on_toggled)
        self._on_toggled(self._box.isChecked())

    def _on_toggled(self, checked: bool) -> None:
        # Checked label uses primary text color via object name swap
        self._label.setObjectName("" if checked else "akMuted")
        style = self._label.style()
        if style is not None:
            style.unpolish(self._label)
            style.polish(self._label)
        self._label.update()

    def isChecked(self) -> bool:  # noqa: N802
        return self._box.isChecked()

    def setChecked(self, checked: bool) -> None:  # noqa: N802
        self._box.setChecked(checked)

    def toggled(self):
        return self._box.toggled
