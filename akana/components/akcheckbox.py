"""Akana Qt — monochrome checkbox with ink check mark.

Mirrors web `.ak-choice` square: 18×18, radius-sm, checked = ink + inverse glyph.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QCheckBox, QStyle, QStyleOptionButton, QWidget

from akana.icons import glyph
from akana.theme import get_theme
from akana.tokens import CHECK_BOX, FS
from akana.util import hand_cursor


class AkCheckbox(QCheckBox):
    BOX = CHECK_BOX

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("AkCheckbox")
        hand_cursor(self)
        # Leave room for custom indicator; hide native via stylesheet empty
        # and paint ourselves in paintEvent for reliable check glyph.

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        t = get_theme()
        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # Indicator box geometry (left, vertically centered with first line)
        fm = self.fontMetrics()
        y = max(0, (fm.height() - self.BOX) // 2 + 1)
        box = QRectF(0.5, y + 0.5, self.BOX - 1, self.BOX - 1)

        enabled = self.isEnabled()
        checked = self.isChecked()
        border = QColor(t["border_strong"] if enabled else t["border"])
        bg = QColor(t["bg"] if enabled else t["surface"])
        if checked and enabled:
            bg = QColor(t["ink"])
            border = QColor(t["ink"])

        p.setPen(QPen(border, 1.0))
        p.setBrush(bg)
        p.drawRoundedRect(box, 4, 4)

        if checked:
            p.setPen(QColor(t["inverse_text"] if enabled else t["text_muted"]))
            font = QFont(self.font())
            font.setPixelSize(FS["sm"])
            font.setBold(True)
            p.setFont(font)
            p.drawText(box, int(Qt.AlignmentFlag.AlignCenter), glyph("check"))

        if self.hasFocus():
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor(t["ink"]), 2.0))
            p.drawRoundedRect(box.adjusted(-2, -2, 2, 2), 5, 5)

        # Label
        text_x = self.BOX + 14
        text_rect = self.rect().adjusted(text_x, 0, 0, 0)
        color = QColor(t["text"] if enabled else t["text_muted"])
        p.setPen(color)
        p.setFont(self.font())
        p.drawText(
            text_rect,
            int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft),
            self.text(),
        )
        p.end()

    def sizeHint(self):  # noqa: N802
        sh = super().sizeHint()
        fm = self.fontMetrics()
        w = self.BOX + 14 + fm.horizontalAdvance(self.text()) + 8
        h = max(self.BOX + 8, fm.height() + 8)
        sh.setWidth(w)
        sh.setHeight(h)
        return sh

    def hitButton(self, pos):  # noqa: N802
        # Entire widget is clickable
        return self.rect().contains(pos)
