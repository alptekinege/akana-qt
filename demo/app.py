"""Akana Qt — demo gallery (full component inventory + light/dark)."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from akana import fonts, styles
from akana.components import (
    AkAccordion,
    AkAlert,
    AkBadge,
    AkBreadcrumb,
    AkButton,
    AkCard,
    AkCheckbox,
    AkEmptyState,
    AkInput,
    AkModal,
    AkNavRail,
    AkPagination,
    AkRadioGroup,
    AkSelect,
    AkTable,
    AkTabs,
    AkTextarea,
    AkToggleSwitch,
)
from akana.theme import current_name, set_theme
from akana.tokens import SPACE


def _scroll_wrap(page: QWidget) -> QScrollArea:
    area = QScrollArea()
    area.setWidgetResizable(True)
    area.setFrameShape(QFrame.Shape.NoFrame)
    area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    area.setWidget(page)
    return area


class Page(QWidget):
    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(SPACE[8], SPACE[6], SPACE[8], SPACE[8])
        root.setSpacing(SPACE[6])

        title_lbl = QLabel(title)
        title_lbl.setObjectName("akTitle")
        root.addWidget(title_lbl)

        self._body = QVBoxLayout()
        self._body.setSpacing(SPACE[5])
        root.addLayout(self._body)
        root.addStretch(1)

    def add_section(self, label: str) -> QHBoxLayout:
        block = QFrame()
        outer = QVBoxLayout(block)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(SPACE[2])

        lbl = QLabel(label)
        lbl.setObjectName("akLabel")
        outer.addWidget(lbl)

        row = QHBoxLayout()
        row.setSpacing(SPACE[3])
        outer.addLayout(row)

        self._body.addWidget(block)
        return row

    def add_widget(self, widget: QWidget) -> None:
        self._body.addWidget(widget)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akana Qt")
        self.resize(1180, 760)

        central = QWidget()
        self.setCentralWidget(central)
        main = QHBoxLayout(central)
        main.setSpacing(0)
        main.setContentsMargins(0, 0, 0, 0)

        left = QFrame()
        left.setObjectName("akSidebar")
        left.setFixedWidth(228)
        lv = QVBoxLayout(left)
        lv.setContentsMargins(SPACE[4], SPACE[4], SPACE[4], SPACE[4])
        lv.setSpacing(SPACE[3])

        brand = QLabel("Akana Qt")
        brand.setObjectName("akBrand")
        lv.addWidget(brand)

        tag = QLabel("MONOCHROME · OFFLINE")
        tag.setObjectName("akLabel")
        lv.addWidget(tag)

        self.nav = AkNavRail()
        for name in (
            "Core",
            "Form",
            "Feedback",
            "Data",
            "Patterns",
            "About",
        ):
            self.nav.add_item(name)
        self.nav.currentChanged.connect(self._on_nav)
        lv.addWidget(self.nav, 1)

        self.theme_btn = AkButton("Dark mode", variant="secondary")
        self.theme_btn.clicked.connect(self._toggle_theme)
        lv.addWidget(self.theme_btn)

        main.addWidget(left, 0)

        self.stack = QStackedWidget()
        main.addWidget(self.stack, 1)

        self.stack.addWidget(_scroll_wrap(self._build_core()))
        self.stack.addWidget(_scroll_wrap(self._build_form()))
        self.stack.addWidget(_scroll_wrap(self._build_feedback()))
        self.stack.addWidget(_scroll_wrap(self._build_data()))
        self.stack.addWidget(_scroll_wrap(self._build_patterns()))
        self.stack.addWidget(_scroll_wrap(self._build_about()))

        styles.apply(self)
        self.nav.set_current_index(0)

    def _on_nav(self, index: int) -> None:
        self.stack.setCurrentIndex(index)

    def _toggle_theme(self) -> None:
        name = "dark" if current_name() == "light" else "light"
        set_theme(name)
        self.theme_btn.setText("Light mode" if name == "dark" else "Dark mode")
        styles.apply(self)

    # ---- pages ----

    def _build_core(self) -> Page:
        page = Page("Core")

        row = page.add_section("Buttons")
        row.addWidget(AkButton("Primary", variant="primary"))
        row.addWidget(AkButton("Secondary", variant="secondary"))
        row.addWidget(AkButton("Ghost", variant="ghost"))
        dis = AkButton("Disabled", variant="primary")
        dis.setEnabled(False)
        row.addWidget(dis)
        row.addStretch(1)

        row = page.add_section("Sizes")
        row.addWidget(AkButton("Small", size="sm"))
        row.addWidget(AkButton("Medium", size="md"))
        row.addWidget(AkButton("Large", size="lg"))
        row.addStretch(1)

        row = page.add_section("Badge")
        row.addWidget(AkBadge("Default"))
        row.addWidget(AkBadge("Solid", variant="solid"))
        row.addStretch(1)

        row = page.add_section("Card")
        card = AkCard()
        card.set_title("Card title")
        card.set_body(
            "Hierarchy from type weight and spacing — not color blocks."
        )
        card.add_widget(AkButton("Action", variant="ghost", size="sm"))
        row.addWidget(card, 1)

        row = page.add_section("Nav / breadcrumb")
        crumb = AkBreadcrumb(["Home", "Library", "Data"])
        row.addWidget(crumb, 1)

        row = page.add_section("Modal")
        open_modal = AkButton("Open dialog", variant="secondary")
        open_modal.clicked.connect(self._open_modal)
        row.addWidget(open_modal)
        row.addStretch(1)

        return page

    def _build_form(self) -> Page:
        page = Page("Form")

        row = page.add_section("Input")
        row.addWidget(AkInput("Type something…"), 1)

        row = page.add_section("Textarea")
        row.addWidget(AkTextarea("Notes…"), 1)

        row = page.add_section("Select")
        row.addWidget(AkSelect(["Option A", "Option B", "Option C"]), 1)

        row = page.add_section("Checkbox")
        row.addWidget(AkCheckbox("Accept terms"))
        row.addWidget(AkCheckbox("Subscribe"))
        row.addStretch(1)

        row = page.add_section("Radio")
        group = AkRadioGroup(["Option A", "Option B", "Option C"])
        group.set_checked_index(0)
        row.addWidget(group)
        row.addStretch(1)

        row = page.add_section("Toggle")
        row.addWidget(AkToggleSwitch("Airplane mode"))
        row.addStretch(1)

        row = page.add_section("Disabled")
        d = AkInput("Disabled field")
        d.setEnabled(False)
        row.addWidget(d, 1)

        return page

    def _build_feedback(self) -> Page:
        page = Page("Feedback & navigation")

        page.add_widget(
            AkAlert(
                "Heads up",
                "Default alert uses surface + border-strong.",
                variant="default",
            )
        )
        page.add_widget(
            AkAlert(
                "Strong",
                "Ink border on the leading edge — still monochrome.",
                variant="strong",
            )
        )
        page.add_widget(
            AkAlert(
                "Solid",
                "Inverse fill for high emphasis notices.",
                variant="solid",
            )
        )

        row = page.add_section("Tabs")
        tabs = AkTabs()
        for title, body in (
            ("Overview", "Overview panel — text secondary, no tinted surfaces."),
            ("Details", "Details panel content goes here."),
            ("Activity", "Activity log placeholder."),
        ):
            panel = QLabel(body)
            panel.setObjectName("akMuted")
            panel.setWordWrap(True)
            tabs.add_tab(title, panel)
        row.addWidget(tabs, 1)

        row = page.add_section("Accordion")
        acc = AkAccordion()
        acc.add_item(
            "What is Akana?",
            "A monochrome, text-first design system. State is weight + border.",
            expanded=True,
        )
        acc.add_item(
            "Why offline fonts?",
            "IBM Plex ships as local TTF so the app never hits a CDN.",
        )
        acc.add_item(
            "Dark mode?",
            "Only the semantic layer rebinds; the gray ramp stays fixed.",
        )
        row.addWidget(acc, 1)

        row = page.add_section("Pagination")
        row.addWidget(AkPagination(total_pages=7, current=3))
        row.addStretch(1)

        return page

    def _build_data(self) -> Page:
        page = Page("Data")

        row = page.add_section("Table")
        table = AkTable(
            columns=["Name", "Role", "Status"],
            rows=[
                ["Ada Lovelace", "Engineer", "Active"],
                ["Grace Hopper", "Admiral", "Active"],
                ["Alan Turing", "Analyst", "Archived"],
            ],
        )
        table.setMinimumHeight(200)
        row.addWidget(table, 1)

        row = page.add_section("Empty state")
        empty = AkEmptyState(
            "No results",
            "Try another filter or create a new item. Dashed border, surface fill.",
        )
        empty.add_action(AkButton("Create", size="sm"))
        empty.add_action(AkButton("Clear filters", variant="ghost", size="sm"))
        row.addWidget(empty)
        row.addStretch(1)

        return page

    def _build_patterns(self) -> Page:
        page = Page("Patterns")
        note = QLabel(
            "Composition surfaces (list · form · empty · help) — same idea as "
            "web patterns.html."
        )
        note.setObjectName("akMuted")
        note.setWordWrap(True)
        page.add_widget(note)

        # List pattern
        list_card = AkCard()
        list_card.set_title("List")
        list_card.set_body("Rows with mono meta labels and ghost actions.")
        list_card.add_widget(
            AkTable(
                columns=["Item", "Meta"],
                rows=[
                    ["Invoice #1042", "Draft"],
                    ["Invoice #1043", "Sent"],
                    ["Invoice #1044", "Paid"],
                ],
            )
        )
        page.add_widget(list_card)

        # Form pattern
        form_card = AkCard()
        form_card.set_title("Form")
        form_card.add_widget(AkInput("Full name"))
        form_card.add_widget(AkSelect(["Team A", "Team B"]))
        form_card.add_widget(AkTextarea("Message"))
        actions = QWidget()
        ah = QHBoxLayout(actions)
        ah.setContentsMargins(0, SPACE[2], 0, 0)
        ah.addStretch(1)
        ah.addWidget(AkButton("Cancel", variant="secondary", size="sm"))
        ah.addWidget(AkButton("Save", size="sm"))
        form_card.add_widget(actions)
        page.add_widget(form_card)

        # Empty pattern
        empty_card = AkCard()
        empty_card.set_title("Empty")
        es = AkEmptyState("No projects", "Create your first project to get started.")
        es.add_action(AkButton("New project", size="sm"))
        empty_card.add_widget(es)
        page.add_widget(empty_card)

        # Help accordion pattern
        help_card = AkCard()
        help_card.set_title("Help")
        help_acc = AkAccordion()
        help_acc.add_item(
            "How do themes work?",
            "set_theme('dark') rebinds semantic tokens only. Call styles.apply().",
            expanded=True,
        )
        help_acc.add_item(
            "Where are fonts?",
            "akana/assets/fonts/*.ttf — registered via akana.fonts.load_fonts().",
        )
        help_card.add_widget(help_acc)
        page.add_widget(help_card)

        return page

    def _build_about(self) -> Page:
        page = Page("About")

        card = AkCard()
        card.set_title("Akana for Qt")
        plex = "loaded" if fonts.has_plex() else "fallback (system-ui)"
        card.set_body(
            "Port of the Akana web design system: monochrome, text-first, "
            "offline. Semantic tokens rebind for light/dark; primitives stay "
            "fixed. Components never reference gray-* directly.\n\n"
            f"IBM Plex: {plex}\n"
            f"Font files: {', '.join(fonts.loaded_files()) or 'none'}\n\n"
            "Inventory: button, card, input, badge, nav, modal, toggle, "
            "checkbox, radio, select, textarea, tabs, alert, accordion, "
            "breadcrumb, pagination, table, empty-state + patterns page."
        )
        page.add_widget(card)

        meta = QLabel("akana_qt v0.3 · web Akana v0.5 parity")
        meta.setObjectName("akLabel")
        page.add_widget(meta)
        return page

    def _open_modal(self) -> None:
        dlg = AkModal("Confirm action", self)
        body = QLabel(
            "Primary = ink fill. Secondary = border-strong. No accent hue."
        )
        body.setObjectName("akMuted")
        body.setWordWrap(True)
        dlg.set_content(body)
        styles.apply(dlg)
        dlg.exec()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Akana Qt")
    families = fonts.load_fonts()
    if families:
        # Default application font to Plex Sans when available.
        from PyQt6.QtGui import QFont

        app.setFont(QFont("IBM Plex Sans", 10))
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
