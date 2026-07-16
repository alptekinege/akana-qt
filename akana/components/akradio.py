"""Akana Qt — monochrome radio with painted indicator.

Mirrors web `.ak-choice--radio`: RADIO_BOX circle, checked = thick ink ring.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QButtonGroup, QRadioButton, QVBoxLayout, QWidget

from akana.theme import get_theme
from akana.tokens import FOCUS_W, RADIO_BOX, SPACE
from akana.util import hand_cursor


class AkRadio(QRadioButton):
    BOX = RADIO_BOX

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("AkRadio")
        hand_cursor(self)

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        t = get_theme()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        fm = self.fontMetrics()
        y = max(0, (fm.height() - self.BOX) // 2 + 1)
        box = QRectF(0.5, y + 0.5, self.BOX - 1, self.BOX - 1)

        enabled = self.isEnabled()
        checked = self.isChecked()
        border = QColor(t["ink"] if checked and enabled else (
            t["border_strong"] if enabled else t["border"]
        ))
        bg = QColor(t["bg"] if enabled else t["surface"])

        if checked and enabled:
            # Thick ink ring, center inverse
            p.setPen(QPen(QColor(t["ink"]), 5.0))
            p.setBrush(QColor(t["inverse_text"]))
            p.drawEllipse(box.adjusted(2, 2, -2, -2))
        else:
            p.setPen(QPen(border, 1.0))
            p.setBrush(bg)
            p.drawEllipse(box)

        if self.hasFocus():
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor(t["ink"]), float(FOCUS_W)))
            pad = FOCUS_W + 1
            p.drawEllipse(box.adjusted(-pad, -pad, pad, pad))

        text_x = self.BOX + SPACE[3] + 2
        text_rect = self.rect().adjusted(text_x, 0, 0, 0)
        p.setPen(QColor(t["text"] if enabled else t["text_muted"]))
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
        h = max(self.BOX + 2 * FOCUS_W + SPACE[2], fm.height() + SPACE[2])
        sh.setWidth(w)
        sh.setHeight(h)
        return sh

    def hitButton(self, pos):  # noqa: N802
        return self.rect().contains(pos)


class AkRadioGroup(QWidget):
    """Vertical exclusive radio group (web `.ak-choice-group`)."""

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
