"""Shared helpers for Akana Qt widgets (repolish, a11y, geometry)."""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFontMetrics, QResizeEvent, QTextDocument, QTextOption
from PyQt6.QtWidgets import QLabel, QSizePolicy, QWidget


def repolish(widget: QWidget) -> None:
    """Force QSS re-evaluation after dynamic property changes."""
    style = widget.style()
    if style is not None:
        style.unpolish(widget)
        style.polish(widget)
    widget.update()


def set_dyn(widget: QWidget, name: str, value: Any) -> None:
    """Set a dynamic property and repolish."""
    widget.setProperty(name, value)
    repolish(widget)


def clear_layout(layout) -> None:
    """Remove and delete all items from a layout."""
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w is not None:
            w.setParent(None)
            w.deleteLater()
        child = item.layout()
        if child is not None:
            clear_layout(child)


def hand_cursor(widget: QWidget) -> None:
    widget.setCursor(Qt.CursorShape.PointingHandCursor)


def configure_flow_label(
    label: QLabel,
    *,
    max_width: int | None = None,
) -> QLabel:
    """Make a QLabel wrap and report full multi-line height to layouts.

    Qt + QSS often under-allocates height for word-wrapped labels (especially
    with max-width / padding), which clips the 2nd line into a “dotted” strip.
    """
    label.setWordWrap(True)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    if max_width is not None:
        label.setMaximumWidth(max_width)
    # Prefer layout spacing over QSS padding (padding is ignored by heightForWidth)
    label.setContentsMargins(0, 0, 0, 0)
    return label


class AkFlowLabel(QLabel):
    """Word-wrapped label with reliable height-for-width (page leads, empty copy)."""

    def __init__(
        self,
        text: str = "",
        *,
        object_name: str = "",
        max_width: int | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)
        if object_name:
            self.setObjectName(object_name)
        configure_flow_label(self, max_width=max_width)
        self._max_w = max_width

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        w = max(1, width)
        if self._max_w is not None:
            w = min(w, self._max_w)
        m = self.contentsMargins()
        inner = max(1, w - m.left() - m.right())
        text = self.text() or ""
        if not text:
            return QFontMetrics(self.font()).height() + m.top() + m.bottom()

        # QTextDocument matches painted wrap better than QFontMetrics alone
        doc = QTextDocument()
        doc.setDefaultFont(self.font())
        opt = QTextOption()
        opt.setWrapMode(QTextOption.WrapMode.WordWrap)
        doc.setDefaultTextOption(opt)
        doc.setDocumentMargin(0)
        doc.setPlainText(text)
        doc.setTextWidth(inner)
        # +4px slack for descent / stylesheet font delta before polish
        return int(doc.size().height()) + m.top() + m.bottom() + 4

    def sizeHint(self) -> QSize:  # noqa: N802
        if self.width() > 0:
            w = self.width()
        elif self._max_w is not None:
            w = self._max_w
        else:
            w = max(super().sizeHint().width(), 200)
        return QSize(w, self.heightForWidth(w))

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        sh = self.sizeHint()
        return QSize(40, sh.height())

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        # Lock min height to full wrapped measure so layouts cannot clip lines
        h = self.heightForWidth(max(self.width(), 1))
        if abs(self.minimumHeight() - h) > 1:
            self.setMinimumHeight(h)
            self.updateGeometry()

    def setText(self, text: str) -> None:  # noqa: N802
        super().setText(text)
        if self.width() > 0:
            self.setMinimumHeight(self.heightForWidth(self.width()))
        self.updateGeometry()

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        # After QSS font polish, recompute height
        if self.width() > 0:
            h = self.heightForWidth(self.width())
            if abs(self.minimumHeight() - h) > 1:
                self.setMinimumHeight(h)
                self.updateGeometry()
