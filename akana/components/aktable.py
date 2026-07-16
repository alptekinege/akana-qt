"""Akana Qt — monochrome data table (web `.ak-table`)."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from akana.tokens import FS, SPACE


class AkTable(QFrame):
    """Bordered wrap + QTableWidget styled as .ak-table."""

    def __init__(
        self,
        columns: list[str] | None = None,
        rows: list[list[str]] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkTableWrap")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.table = QTableWidget(self)
        self.table.setObjectName("AkTable")
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table.setTabKeyNavigation(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(52)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        # Quiet corner
        self.table.setCornerButtonEnabled(False)
        layout.addWidget(self.table)

        if columns:
            self.set_columns(columns)
        if rows:
            self.set_rows(rows)

    def set_columns(self, columns: list[str]) -> None:
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels([c.upper() for c in columns])
        # Header uses QSS mono; keep labels readable
        header = self.table.horizontalHeader()
        font = QFont("IBM Plex Mono", FS["2xs"])
        font.setWeight(QFont.Weight.Medium)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.8)
        header.setFont(font)

    def set_rows(self, rows: list[list[str]]) -> None:
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                self._set_cell(r, c, cell)
        self.table.resizeRowsToContents()
        for r in range(self.table.rowCount()):
            self.table.setRowHeight(r, max(52, self.table.rowHeight(r)))

    def add_row(self, cells: list[str]) -> None:
        r = self.table.rowCount()
        self.table.insertRow(r)
        for c, cell in enumerate(cells):
            self._set_cell(r, c, cell)
        self.table.setRowHeight(r, 52)

    def _set_cell(self, r: int, c: int, cell: str | QWidget) -> None:
        if isinstance(cell, QWidget):
            self.table.setCellWidget(r, c, cell)
            return
        item = QTableWidgetItem(str(cell))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        item.setTextAlignment(
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        )
        # Padding via item data is limited; QSS item padding handles rest
        self.table.setItem(r, c, item)

    def set_cell_widget(self, row: int, column: int, widget: QWidget) -> None:
        self.table.setCellWidget(row, column, widget)
