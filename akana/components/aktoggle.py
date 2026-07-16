"""Akana Qt — monochrome toggle / switch with painted track + thumb.

Track surface-2 / checked ink, thumb muted → inverse-text.
Sized for desktop (larger than web 40×22).
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QWidget

from akana.theme import get_theme
from akana.tokens import SPACE, TOGGLE_H, TOGGLE_THUMB, TOGGLE_W
from akana.util import hand_cursor


class AkToggle(QWidget):
    """Standalone switch (role=switch). Emits toggled(bool)."""

    toggled = pyqtSignal(bool)

    TRACK_W = TOGGLE_W
    TRACK_H = TOGGLE_H
    THUMB = TOGGLE_THUMB
    PAD = 3

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("AkToggle")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        hand_cursor(self)
        self._checked = False
        self._label = text
        # Hit target includes optional label via sizeHint of switch only;
        # for labeled use AkToggleSwitch.
        self.setFixedSize(self.TRACK_W, self.TRACK_H)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAccessibleName(text or "Toggle")

    def isChecked(self) -> bool:  # noqa: N802
        return self._checked

    def setChecked(self, checked: bool) -> None:  # noqa: N802
        checked = bool(checked)
        if checked == self._checked:
            return
        self._checked = checked
        self.update()
        self.toggled.emit(self._checked)

    def toggle(self) -> None:
        self.setChecked(not self._checked)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
            self.toggle()
            event.accept()
            return
        super().mousePressEvent(event)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.isEnabled():
                self.toggle()
            event.accept()
            return
        super().keyPressEvent(event)

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        t = get_theme()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        enabled = self.isEnabled()
        border = QColor(t["border_strong"] if enabled else t["border"])
        if self._checked and enabled:
            track = QColor(t["ink"])
            thumb = QColor(t["inverse_text"])
            border = QColor(t["ink"])
        else:
            track = QColor(t["surface_2"] if enabled else t["surface"])
            thumb = QColor(t["text_muted"])

        # Track
        track_rect = QRectF(0.5, 0.5, self.TRACK_W - 1, self.TRACK_H - 1)
        p.setPen(QPen(border, 1.0))
        p.setBrush(track)
        p.drawRoundedRect(track_rect, self.TRACK_H / 2, self.TRACK_H / 2)

        # Thumb
        y = (self.TRACK_H - self.THUMB) / 2
        if self._checked:
            x = self.TRACK_W - self.PAD - self.THUMB
        else:
            x = self.PAD
        thumb_rect = QRectF(x, y, self.THUMB, self.THUMB)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(thumb)
        p.drawEllipse(thumb_rect)

        # Focus ring (ink, monochrome)
        if self.hasFocus():
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor(t["ink"]), 2.0))
            p.drawRoundedRect(
                QRectF(1.5, 1.5, self.TRACK_W - 3, self.TRACK_H - 3),
                (self.TRACK_H - 3) / 2,
                (self.TRACK_H - 3) / 2,
            )

        p.end()


class AkToggleSwitch(QFrame):
    """Label + switch composition (web default demo layout)."""

    def __init__(self, text: str = "Toggle", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("AkToggleSwitch")
        hand_cursor(self)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(SPACE[3])

        self._box = AkToggle()
        self._label = QLabel(text)
        self._label.setObjectName("akMuted")

        root.addWidget(self._box, 0, Qt.AlignmentFlag.AlignVCenter)
        root.addWidget(self._label, 0, Qt.AlignmentFlag.AlignVCenter)
        root.addStretch(1)

        self._box.toggled.connect(self._on_toggled)
        self._on_toggled(self._box.isChecked())

    def mousePressEvent(self, event) -> None:  # noqa: N802
        # Clicking the label row toggles (web-like)
        if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
            self._box.toggle()
            event.accept()
            return
        super().mousePressEvent(event)

    def _on_toggled(self, checked: bool) -> None:
        self._label.setObjectName("" if checked else "akMuted")
        from akana.util import repolish

        repolish(self._label)

    def isChecked(self) -> bool:  # noqa: N802
        return self._box.isChecked()

    def setChecked(self, checked: bool) -> None:  # noqa: N802
        self._box.setChecked(checked)

    def toggled(self):
        return self._box.toggled
