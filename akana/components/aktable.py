"""Akana Qt — monochrome data table."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class AkTable(QFrame):
    """Bordered table wrap + QTableWidget styled as .ak-table."""

    def __init__(
        self,
        columns: list[str] | None = None,
        rows: list[list[str]] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkTableWrap")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.table = QTableWidget(self)
        self.table.setObjectName("AkTable")
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        layout.addWidget(self.table)

        if columns:
            self.set_columns(columns)
        if rows:
            self.set_rows(rows)

    def set_columns(self, columns: list[str]) -> None:
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

    def set_rows(self, rows: list[list[str]]) -> None:
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                item = QTableWidgetItem(cell)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(r, c, item)

    def add_row(self, cells: list[str]) -> None:
        r = self.table.rowCount()
        self.table.insertRow(r)
        for c, cell in enumerate(cells):
            item = QTableWidgetItem(cell)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(r, c, item)
