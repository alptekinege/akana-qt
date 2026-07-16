"""Akana Qt — monochrome badge / tag (web `.ak-badge`)."""

from __future__ import annotations

from typing import Literal

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from akana.tokens import BADGE_H, SPACE
from akana.util import set_dyn

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
        self.setObjectName("AkBadge")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(BADGE_H)
        self.setSizePolicy(
            self.sizePolicy().horizontalPolicy(),
            self.sizePolicy().verticalPolicy(),
        )

        root = QHBoxLayout(self)
        root.setContentsMargins(11, 4, 11, 4)
        root.setSpacing(SPACE[1])
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._label = QLabel(text.upper() if text else "")
        self._label.setWordWrap(False)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._label)

        self.set_variant(variant)

    def setText(self, text: str) -> None:  # noqa: N802
        self._label.setText(text.upper() if text else "")

    def text(self) -> str:
        return self._label.text()

    def set_variant(self, variant: Variant) -> None:
        set_dyn(self, "variant", variant)
