"""Akana Qt — monochrome checkbox with ink check mark.

Mirrors web `.ak-choice` square: CHECK_BOX side, radius-sm,
checked = ink + inverse glyph.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QCheckBox, QStyle, QStyleOptionButton, QWidget

from akana.icons import glyph
from akana.theme import get_theme
from akana.tokens import CHECK_BOX, FOCUS_W, FS, RADIUS, SPACE
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
        p.drawRoundedRect(box, RADIUS.sm, RADIUS.sm)

        if checked:
            p.setPen(QColor(t["inverse_text"] if enabled else t["text_muted"]))
            font = QFont(self.font())
            font.setPixelSize(FS["sm"])
            font.setBold(True)
            p.setFont(font)
            p.drawText(box, int(Qt.AlignmentFlag.AlignCenter), glyph("check"))

        if self.hasFocus():
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor(t["ink"]), float(FOCUS_W)))
            pad = FOCUS_W
            p.drawRoundedRect(
                box.adjusted(-pad, -pad, pad, pad),
                RADIUS.sm + 1,
                RADIUS.sm + 1,
            )

        # Label
        text_x = self.BOX + SPACE[3] + 2
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
        from akana.tokens import FOCUS_W, SPACE

        sh = super().sizeHint()
        fm = self.fontMetrics()
        gap = SPACE[3] + 2
        w = self.BOX + gap + fm.horizontalAdvance(self.text()) + SPACE[2]
        # Room for focus ring outside the box
        h = max(self.BOX + 2 * FOCUS_W + SPACE[2], fm.height() + SPACE[2])
        sh.setWidth(w)
        sh.setHeight(h)
        return sh

    def hitButton(self, pos):  # noqa: N802
        # Entire widget is clickable
        return self.rect().contains(pos)
