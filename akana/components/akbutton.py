"""Akana Qt — monochrome button (primary / secondary / ghost / inverse).

Mirrors web `.ak-btn`. State via weight, border, surface — no accent hue.
"""

from __future__ import annotations

from typing import Literal

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget

from akana.util import hand_cursor, set_dyn

Variant = Literal["primary", "secondary", "ghost", "inverse"]
Size = Literal["sm", "md", "lg"]


class AkButton(QPushButton):
    def __init__(
        self,
        text: str = "",
        *,
        variant: Variant = "primary",
        size: Size = "md",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)
        hand_cursor(self)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAutoDefault(False)
        self.setDefault(False)
        self.set_variant(variant)
        self.set_size(size)

    def set_variant(self, variant: Variant) -> None:
        set_dyn(self, "variant", variant)

    def set_size(self, size: Size) -> None:
        # Do not use property name "size" — conflicts with QWidget.size.
        set_dyn(self, "akSize", size)
