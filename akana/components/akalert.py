"""Akana Qt — monochrome alert / banner.

Variants: default (surface), strong (ink left border), solid (ink fill).
"""

from __future__ import annotations

from typing import Literal

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from akana.icons import glyph
from akana.tokens import SPACE
from akana.util import AkFlowLabel, set_dyn

Variant = Literal["default", "strong", "solid"]


class AkAlert(QFrame):
    def __init__(
        self,
        title: str = "",
        text: str = "",
        *,
        variant: Variant = "default",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkAlert")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        root = QHBoxLayout(self)
        root.setContentsMargins(SPACE[5], SPACE[4], SPACE[5], SPACE[4])
        root.setSpacing(SPACE[3])

        self._icon = QLabel(glyph("alert"))
        self._icon.setObjectName("akAlertIcon")
        self._icon.setFixedWidth(16)
        self._icon.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        root.addWidget(self._icon, 0)

        col = QVBoxLayout()
        col.setSpacing(SPACE[1])
        col.setContentsMargins(0, 0, 0, 0)

        self._title = AkFlowLabel(title, object_name="akAlertTitle")
        self._title.setVisible(bool(title))
        col.addWidget(self._title)

        self._text = AkFlowLabel(text, object_name="akAlertText")
        self._text.setVisible(bool(text))
        col.addWidget(self._text)

        root.addLayout(col, 1)
        self.set_variant(variant)

    def set_variant(self, variant: Variant) -> None:
        set_dyn(self, "variant", variant)

    def set_title(self, title: str) -> None:
        self._title.setText(title)
        self._title.setVisible(bool(title))

    def set_text(self, text: str) -> None:
        self._text.setText(text)
        self._text.setVisible(bool(text))
