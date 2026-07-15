"""Akana Qt — monochrome badge / tag.

Mirrors web `.ak-badge`: mono uppercase, pill radius; optional solid.
"""

from __future__ import annotations

from typing import Literal

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from akana.tokens import SPACE

Variant = Literal["default", "solid"]


class AkBadge(QFrame):
    def __init__(
        self,
        text: str = "",
        *,
        variant: Variant = "default",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setFixedHeight(26)

        root = QHBoxLayout(self)
        root.setContentsMargins(9, 3, 9, 3)
        root.setSpacing(SPACE[1])

        self._label = QLabel(text.upper() if text else "")
        self._label.setWordWrap(False)
        root.addWidget(self._label)

        self.set_variant(variant)

    def setText(self, text: str) -> None:  # noqa: N802 — Qt naming
        self._label.setText(text.upper() if text else "")

    def text(self) -> str:
        return self._label.text()

    def set_variant(self, variant: Variant) -> None:
        self.setProperty("variant", variant)
        style = self.style()
        if style is not None:
            style.unpolish(self)
            style.polish(self)
        self.update()
