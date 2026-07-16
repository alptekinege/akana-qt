"""Akana Qt — monochrome badge / tag (web `.ak-badge`).

Custom-painted so status pills stay legible inside QTableWidget cells
(QSS backgrounds/text often fail for cell widgets on Windows).
"""

from __future__ import annotations

from typing import Literal

from PyQt6.QtCore import QRectF, QSize, Qt
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PyQt6.QtWidgets import QFrame, QSizePolicy, QWidget

from akana.theme import get_theme
from akana.tokens import BADGE_H, FS
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
        # Let paintEvent own chrome — avoid QSS fighting cell-widget paint
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._text = (text or "").upper()
        self._variant: Variant = "default"
        self.set_variant(variant)
        self._sync_size()

    def setText(self, text: str) -> None:  # noqa: N802
        self._text = (text or "").upper()
        self._sync_size()
        self.update()

    def text(self) -> str:
        return self._text

    def set_variant(self, variant: Variant) -> None:
        self._variant = variant
        set_dyn(self, "variant", variant)
        self.update()

    def _label_font(self) -> QFont:
        font = QFont("IBM Plex Mono")
        font.setPixelSize(FS["2xs"])
        font.setWeight(QFont.Weight.Medium)
        return font

    def _sync_size(self) -> None:
        sh = self.sizeHint()
        self.setFixedSize(sh)

    def sizeHint(self) -> QSize:  # noqa: N802
        fm = QFontMetrics(self._label_font())
        pad_x = 12
        w = fm.horizontalAdvance(self._text or "·") + pad_x * 2
        return QSize(max(w, 48), BADGE_H)

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        return self.sizeHint()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        t = get_theme()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        if self._variant == "solid":
            bg = QColor(t["ink"])
            fg = QColor(t["inverse_text"])
            border = QColor(t["ink"])
        else:
            bg = QColor(t["surface_2"])
            fg = QColor(t["text"])
            border = QColor(t["border_strong"])

        # Fill full widget (opaque) so table cells cannot show through empty
        p.fillRect(self.rect(), bg)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        rad = (BADGE_H - 1) / 2.0
        p.setPen(QPen(border, 1.0))
        p.setBrush(bg)
        p.drawRoundedRect(rect, rad, rad)

        p.setFont(self._label_font())
        p.setPen(fg)
        p.drawText(
            self.rect(),
            int(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter),
            self._text,
        )
        p.end()
