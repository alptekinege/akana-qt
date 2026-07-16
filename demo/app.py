"""Akana Qt — polished frameless gallery with multi-style showcases."""

from __future__ import annotations

import sys

from PyQt6.QtCore import QEvent, QPoint, Qt, QRect, QTimer
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QSizeGrip,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from akana import fonts, styles, winchrome
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
    AkTitleBar,
    AkToggleSwitch,
)
from akana.components.akshowcase import AkPanel, AkShowcaseSection, AkStyleBoard
from akana.theme import current_name, set_theme
from akana.tokens import SPACE


# Edge hit margin for frameless resize (non-Windows fallback)
_EDGE = 6


def _scroll(page: QWidget) -> QScrollArea:
    area = QScrollArea()
    area.setWidgetResizable(True)
    area.setFrameShape(QFrame.Shape.NoFrame)
    area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    area.setWidget(page)
    return area


def _row(*widgets: QWidget, stretch: bool = True) -> QWidget:
    wrap = QWidget()
    lay = QHBoxLayout(wrap)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(SPACE[3])
    for w in widgets:
        lay.addWidget(w)
    if stretch:
        lay.addStretch(1)
    return wrap


def _stack(*widgets: QWidget, spacing: int | None = None) -> QWidget:
    wrap = QWidget()
    lay = QVBoxLayout(wrap)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(SPACE[3] if spacing is None else spacing)
    for w in widgets:
        lay.addWidget(w)
    return wrap


class Page(QWidget):
    def __init__(
        self,
        eyebrow: str,
        title: str,
        lead: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(SPACE[8], SPACE[6], SPACE[8], SPACE[10])
        root.setSpacing(SPACE[8])

        hero = QFrame()
        hero.setObjectName("akPageHero")
        hv = QVBoxLayout(hero)
        hv.setContentsMargins(0, 0, 0, SPACE[5])
        hv.setSpacing(SPACE[2])
        eye = QLabel(eyebrow)
        eye.setObjectName("akLabel")
        hv.addWidget(eye)
        t = QLabel(title)
        t.setObjectName("akTitle")
        t.setWordWrap(True)
        hv.addWidget(t)
        if lead:
            l = QLabel(lead)
            l.setObjectName("akLead")
            l.setWordWrap(True)
            hv.addWidget(l)
        root.addWidget(hero)

        self._body = QVBoxLayout()
        self._body.setSpacing(SPACE[8])
        root.addLayout(self._body)
        root.addStretch(1)

    def add(self, widget: QWidget) -> None:
        self._body.addWidget(widget)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akana Qt")
        self.resize(1240, 820)
        self.setMinimumSize(920, 600)
        # Frameless UI; on Windows we restore thick-frame via winchrome so
        # Win+Up / snap / maximize keep working.
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window
        )
        self._resize_edge: str | None = None
        self._resize_origin = QPoint()
        self._resize_geom = QRect()
        # Windows snap styles applied after show; no nativeEvent hooks
        # (PyQt6 super().nativeEvent returns (False, None) → CreateWindowEx fails).
        self._snap_enabled = False

        # Outer border chrome
        self.shell = QFrame()
        self.shell.setObjectName("akWindowRoot")
        self.shell.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCentralWidget(self.shell)
        outer = QVBoxLayout(self.shell)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ---- Title bar ----
        self.titlebar = AkTitleBar("Akana Qt")
        self.titlebar.set_window(self)
        self.titlebar.set_meta("v0.3 · monochrome")
        self.titlebar.minimizeClicked.connect(self.showMinimized)
        self.titlebar.maximizeClicked.connect(self._toggle_max)
        self.titlebar.closeClicked.connect(self.close)

        self.theme_chip = AkButton("Dark", variant="ghost", size="sm")
        self.theme_chip.setFixedHeight(28)
        self.theme_chip.clicked.connect(self._toggle_theme)
        self.titlebar.add_action(self.theme_chip)
        outer.addWidget(self.titlebar)

        # ---- Body: sidebar + content ----
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        left = QFrame()
        left.setObjectName("akSidebar")
        left.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        left.setFixedWidth(240)
        lv = QVBoxLayout(left)
        lv.setContentsMargins(SPACE[4], SPACE[5], SPACE[4], SPACE[4])
        lv.setSpacing(SPACE[4])

        brand_block = QVBoxLayout()
        brand_block.setSpacing(4)
        brand = QLabel("Akana")
        brand.setObjectName("akBrand")
        brand_block.addWidget(brand)
        sub = QLabel("DESIGN SYSTEM · QT")
        sub.setObjectName("akBrandSub")
        brand_block.addWidget(sub)
        lv.addLayout(brand_block)

        div = QFrame()
        div.setObjectName("akDivider")
        div.setFixedHeight(1)
        lv.addWidget(div)

        nav_label = QLabel("PAGES")
        nav_label.setObjectName("akLabel")
        lv.addWidget(nav_label)

        self.nav = AkNavRail()
        for name in (
            "Overview",
            "Buttons",
            "Forms",
            "Feedback",
            "Data",
            "Patterns",
        ):
            self.nav.add_item(name)
        self.nav.currentChanged.connect(self._on_nav)
        lv.addWidget(self.nav, 1)

        foot = QLabel("IBM Plex · offline\nNo accent · no CDN")
        foot.setObjectName("akMuted")
        foot.setWordWrap(True)
        lv.addWidget(foot)

        body.addWidget(left, 0)

        content = QFrame()
        content.setObjectName("akContentChrome")
        content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        cv = QVBoxLayout(content)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(0)

        self.stack = QStackedWidget()
        cv.addWidget(self.stack, 1)

        # Size grip (native resize also works on Windows via NCHITTEST)
        grip_row = QHBoxLayout()
        grip_row.setContentsMargins(0, 0, 4, 4)
        grip_row.addStretch(1)
        grip = QSizeGrip(content)
        grip.setFixedSize(16, 16)
        grip_row.addWidget(grip)
        cv.addLayout(grip_row)

        body.addWidget(content, 1)
        outer.addLayout(body, 1)

        # Pages
        self.stack.addWidget(_scroll(self._page_overview()))
        self.stack.addWidget(_scroll(self._page_buttons()))
        self.stack.addWidget(_scroll(self._page_forms()))
        self.stack.addWidget(_scroll(self._page_feedback()))
        self.stack.addWidget(_scroll(self._page_data()))
        self.stack.addWidget(_scroll(self._page_patterns()))

        styles.apply(self)
        self.nav.set_current_index(0)
        self._sync_window_chrome()

    # ---- window chrome ----

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        # After HWND exists: add WS_MAXIMIZEBOX / thick frame so Win+Up works.
        # Deferred — must not run during CreateWindowEx.
        if winchrome.is_windows() and not self._snap_enabled:
            QTimer.singleShot(0, self._enable_snap_styles)

    def _enable_snap_styles(self) -> None:
        if self._snap_enabled:
            return
        if winchrome.enable_snap_for_frameless(self):
            self._snap_enabled = True

    def changeEvent(self, event: QEvent) -> None:
        super().changeEvent(event)
        if event.type() == QEvent.Type.WindowStateChange:
            self._sync_window_chrome()

    def _sync_window_chrome(self) -> None:
        maximized = self.isMaximized()
        self.titlebar.set_maximized(maximized)
        self.shell.setProperty("maximized", maximized)
        style = self.shell.style()
        if style is not None:
            style.unpolish(self.shell)
            style.polish(self.shell)
        self.shell.update()

    def _toggle_max(self) -> None:
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        self._sync_window_chrome()

    def _toggle_theme(self) -> None:
        name = "dark" if current_name() == "light" else "light"
        set_theme(name)
        self.theme_chip.setText("Light" if name == "dark" else "Dark")
        self.titlebar.set_meta(f"v0.3 · {name}")
        styles.apply(self)
        self._sync_window_chrome()

    def _on_nav(self, index: int) -> None:
        self.stack.setCurrentIndex(index)

    def _hit_edge(self, pos: QPoint) -> str | None:
        if self.isMaximized():
            return None
        r = self.rect()
        x, y = pos.x(), pos.y()
        left = x <= _EDGE
        right = x >= r.width() - _EDGE
        top = y <= _EDGE
        bottom = y >= r.height() - _EDGE
        if top and left:
            return "tl"
        if top and right:
            return "tr"
        if bottom and left:
            return "bl"
        if bottom and right:
            return "br"
        if left:
            return "l"
        if right:
            return "r"
        if top:
            return "t"
        if bottom:
            return "b"
        return None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            edge = self._hit_edge(event.position().toPoint())
            if edge:
                self._resize_edge = edge
                self._resize_origin = event.globalPosition().toPoint()
                self._resize_geom = self.geometry()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._resize_edge and event.buttons() & Qt.MouseButton.LeftButton:
            self._do_resize(event.globalPosition().toPoint())
            event.accept()
            return
        if not self.isMaximized():
            edge = self._hit_edge(event.position().toPoint())
            cursors = {
                "l": Qt.CursorShape.SizeHorCursor,
                "r": Qt.CursorShape.SizeHorCursor,
                "t": Qt.CursorShape.SizeVerCursor,
                "b": Qt.CursorShape.SizeVerCursor,
                "tl": Qt.CursorShape.SizeFDiagCursor,
                "br": Qt.CursorShape.SizeFDiagCursor,
                "tr": Qt.CursorShape.SizeBDiagCursor,
                "bl": Qt.CursorShape.SizeBDiagCursor,
            }
            self.setCursor(
                cursors.get(edge, Qt.CursorShape.ArrowCursor)
                if edge
                else Qt.CursorShape.ArrowCursor
            )
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._resize_edge = None
        super().mouseReleaseEvent(event)

    def _do_resize(self, global_pos: QPoint) -> None:
        delta = global_pos - self._resize_origin
        g = QRect(self._resize_geom)
        e = self._resize_edge
        min_w, min_h = self.minimumWidth(), self.minimumHeight()
        if e in ("r", "tr", "br"):
            g.setWidth(max(min_w, self._resize_geom.width() + delta.x()))
        if e in ("b", "bl", "br"):
            g.setHeight(max(min_h, self._resize_geom.height() + delta.y()))
        if e in ("l", "tl", "bl"):
            new_w = max(min_w, self._resize_geom.width() - delta.x())
            g.setLeft(self._resize_geom.right() - new_w + 1)
        if e in ("t", "tl", "tr"):
            new_h = max(min_h, self._resize_geom.height() - delta.y())
            g.setTop(self._resize_geom.bottom() - new_h + 1)
        self.setGeometry(g)

    # ---- pages ----

    def _page_overview(self) -> Page:
        page = Page(
            "01 · Overview",
            "Clarity without decoration.",
            "Akana is monochrome and text-first. Hierarchy comes from type "
            "weight, spacing, and border — never hue.",
        )

        # Three tone panels
        board = AkStyleBoard(columns=3)
        for tone, title, body in (
            ("default", "Default", "Page background. Primary reading surface."),
            ("surface", "Surface", "Raised areas, rails, quiet containers."),
            ("ink", "Ink", "Maximum emphasis. Inverse type on fill."),
        ):
            p = AkPanel(tone=tone)  # type: ignore[arg-type]
            p.add_header(title, tone.upper())
            muted = QLabel(body)
            muted.setObjectName("akMuted")
            muted.setWordWrap(True)
            p.add_widget(muted)
            if tone == "ink":
                p.add_row(
                    AkButton("Inverse", variant="inverse", size="sm"),
                    AkButton("Ghost", variant="ghost", size="sm"),
                )
            else:
                p.add_row(
                    AkButton("Primary", size="sm"),
                    AkButton("Secondary", variant="secondary", size="sm"),
                )
            board.add_cell(f"Tone · {tone}", p)
        page.add(board)

        sec = AkShowcaseSection(
            "Snapshot",
            "Working strip",
            "A dense row of mixed components — how Akana reads in product UI.",
        )
        toolbar = QFrame()
        toolbar.setObjectName("akToolbar")
        toolbar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        tv = QVBoxLayout(toolbar)
        tv.setContentsMargins(SPACE[5], SPACE[4], SPACE[5], SPACE[4])
        tv.setSpacing(SPACE[3])
        head = QHBoxLayout()
        ht = QLabel("Toolbar")
        ht.setObjectName("akPanelTitle")
        head.addWidget(ht)
        head.addStretch(1)
        hm = QLabel("COMPOSITION")
        hm.setObjectName("akLabel")
        head.addWidget(hm)
        tv.addLayout(head)
        row = QHBoxLayout()
        row.setSpacing(SPACE[3])
        row.addWidget(AkBadge("Live"))
        row.addWidget(AkBadge("Mono", variant="solid"))
        row.addWidget(AkInput("Search library…"), 1)
        row.addWidget(AkSelect(["All", "Draft", "Published"]))
        row.addWidget(AkButton("Filter", variant="secondary", size="sm"))
        row.addWidget(AkButton("New", size="sm"))
        tv.addLayout(row)
        sec.add_widget(toolbar)
        page.add(sec)

        return page

    def _page_buttons(self) -> Page:
        page = Page(
            "02 · Buttons",
            "Weight carries intent.",
            "Primary fills with ink. Secondary outlines. Ghost stays quiet "
            "until hover. Sizes share the same geometry language.",
        )

        board = AkStyleBoard(columns=2)

        # Variants cell
        v = AkPanel()
        v.add_header("Variants", "3")
        v.add_row(
            AkButton("Primary", variant="primary"),
            AkButton("Secondary", variant="secondary"),
            AkButton("Ghost", variant="ghost"),
        )
        dis = AkButton("Disabled", variant="primary")
        dis.setEnabled(False)
        dis2 = AkButton("Disabled", variant="secondary")
        dis2.setEnabled(False)
        v.add_row(dis, dis2)
        board.add_cell("Style matrix", v)

        # Sizes
        s = AkPanel(tone="surface")
        s.add_header("Scale", "SM · MD · LG")
        s.add_row(
            AkButton("Small", size="sm"),
            AkButton("Medium", size="md"),
            AkButton("Large", size="lg"),
        )
        s.add_row(
            AkButton("Small", variant="secondary", size="sm"),
            AkButton("Medium", variant="secondary", size="md"),
            AkButton("Large", variant="secondary", size="lg"),
        )
        board.add_cell("Size ladder", s)

        # Inverse surface
        inv = AkPanel(tone="ink")
        inv.add_header("On ink", "INVERSE")
        inv.add_widget(
            QLabel("Ghost and secondary on the strongest surface.")
        )
        inv.add_row(
            AkButton("Continue", variant="inverse", size="sm"),
            AkButton("Skip", variant="ghost", size="sm"),
        )
        board.add_cell("Inverse context", inv)

        # Action cluster
        act = AkPanel()
        act.add_header("Clusters", "DIALOG / TOOLBAR")
        act.add_row(
            AkButton("Cancel", variant="secondary", size="sm"),
            AkButton("Save draft", variant="ghost", size="sm"),
            AkButton("Publish", size="sm"),
        )
        open_m = AkButton("Open modal…", variant="secondary")
        open_m.clicked.connect(self._open_modal)
        act.add_row(open_m)
        board.add_cell("Real actions", act)

        page.add(board)
        return page

    def _page_forms(self) -> Page:
        page = Page(
            "03 · Forms",
            "Quiet fields. Loud focus.",
            "Inputs use border-strong at rest and ink at focus. Labels stay "
            "mono uppercase — never colored.",
        )

        board = AkStyleBoard(columns=2)

        fields = AkPanel()
        fields.add_header("Fields", "DEFAULT")
        fields.add_widget(_stack(
            _field("Email", AkInput("you@example.com")),
            _field("Role", AkSelect(["Designer", "Engineer", "Writer"])),
            _field("Notes", AkTextarea("Optional context…")),
        ))
        board.add_cell("Standard", fields)

        dense = AkPanel(tone="surface")
        dense.add_header("Choices", "BINARY · EXCLUSIVE · SWITCH")
        dense.add_widget(AkCheckbox("Email me product updates"))
        dense.add_widget(AkCheckbox("Share usage analytics"))
        rg = AkRadioGroup(["Public", "Unlisted", "Private"])
        rg.set_checked_index(1)
        dense.add_widget(rg)
        dense.add_widget(AkToggleSwitch("Two-factor authentication"))
        board.add_cell("Selection", dense)

        names = QWidget()
        nh = QHBoxLayout(names)
        nh.setContentsMargins(0, 0, 0, 0)
        nh.setSpacing(SPACE[3])
        nh.addWidget(AkInput("First name"), 1)
        nh.addWidget(AkInput("Last name"), 1)
        split = AkPanel()
        split.add_header("Inline", "COMPACT ROW")
        split.add_widget(names)
        split.add_widget(_row(
            AkSelect(["TR", "EN", "DE"]),
            AkButton("Apply", size="sm"),
            AkButton("Reset", variant="ghost", size="sm"),
        ))
        board.add_cell("Toolbar form", split)

        disabled = AkPanel(tone="dashed")
        disabled.add_header("Disabled", "MUTED")
        d = AkInput("Read only value")
        d.setEnabled(False)
        disabled.add_widget(d)
        db = AkButton("Unavailable", variant="secondary", size="sm")
        db.setEnabled(False)
        disabled.add_row(db)
        board.add_cell("States", disabled)

        page.add(board)
        return page

    def _page_feedback(self) -> Page:
        page = Page(
            "04 · Feedback",
            "Signal without color.",
            "Alerts escalate through border weight and fill — default, strong, "
            "then solid ink. Tabs and accordion keep motion optional.",
        )

        sec = AkShowcaseSection("Alerts", "Three levels of attention")
        sec.add_widget(
            AkAlert(
                "Default",
                "Surface fill, border-strong. Everyday notices.",
                variant="default",
            )
        )
        sec.add_widget(
            AkAlert(
                "Strong",
                "Ink edge on the leading side. Needs a decision soon.",
                variant="strong",
            )
        )
        sec.add_widget(
            AkAlert(
                "Solid",
                "Full ink fill for blocking or irreversible context.",
                variant="solid",
            )
        )
        page.add(sec)

        board = AkStyleBoard(columns=2)

        tabs_panel = AkPanel()
        tabs_panel.add_header("Tabs", "UNDERLINE ACTIVE")
        tabs = AkTabs()
        for title, body in (
            ("Overview", "Overview copy sits in secondary text. No tinted panels."),
            ("Specs", "Token tables and API notes would land here."),
            ("Changelog", "v0.3 · frameless shell · style boards."),
        ):
            lab = QLabel(body)
            lab.setObjectName("akMuted")
            lab.setWordWrap(True)
            tabs.add_tab(title, lab)
        tabs_panel.add_widget(tabs)
        board.add_cell("Navigation", tabs_panel)

        acc_panel = AkPanel(tone="surface")
        acc_panel.add_header("Accordion", "DISCLOSURE")
        acc = AkAccordion()
        acc.add_item(
            "Why no accent color?",
            "State is weight and border. Accent would become a crutch and "
            "break dark-mode semantics.",
            expanded=True,
        )
        acc.add_item(
            "How is dark mode done?",
            "Only the semantic layer rebinds. The gray ramp never flips itself.",
        )
        acc.add_item(
            "Can I use system chrome?",
            "You can — this gallery prefers a custom title bar for product feel.",
        )
        acc_panel.add_widget(acc)
        board.add_cell("Help pattern", acc_panel)

        page.add(board)

        trail = AkPanel()
        trail.add_header("Trail & pages", "BREADCRUMB · PAGINATION")
        trail.add_widget(AkBreadcrumb(["Library", "Components", "Feedback"]))
        trail.add_widget(AkPagination(total_pages=8, current=2))
        page.add(trail)
        return page

    def _page_data(self) -> Page:
        page = Page(
            "05 · Data",
            "Tables read like type, not grids.",
            "Mono headers, quiet row hover, no zebra rainbows. Empty states "
            "use dashed borders — invitation, not error.",
        )

        table_panel = AkPanel()
        table_panel.add_header("Table", "3 COLUMNS")
        table = AkTable(
            columns=["Name", "Role", "Status"],
            rows=[
                ["Ada Lovelace", "Engineer", "Active"],
                ["Grace Hopper", "Admiral", "Active"],
                ["Alan Turing", "Analyst", "Archived"],
                ["Katherine Johnson", "Mathematician", "Active"],
            ],
        )
        table.setMinimumHeight(240)
        table_panel.add_widget(table)
        page.add(table_panel)

        board = AkStyleBoard(columns=2)
        empty = AkEmptyState(
            "No matches",
            "Adjust filters or create a record. Dashed surface keeps the state soft.",
        )
        empty.add_action(AkButton("Create", size="sm"))
        empty.add_action(AkButton("Clear", variant="ghost", size="sm"))
        board.add_cell("Empty · default", empty)

        ink_empty_host = AkPanel(tone="ink")
        ink_empty_host.add_header("Empty · inverse", "ON INK")
        body = QLabel("When the surrounding chrome is ink, keep actions light.")
        body.setObjectName("akMuted")
        body.setWordWrap(True)
        ink_empty_host.add_widget(body)
        ink_empty_host.add_row(
            AkButton("Import", variant="inverse", size="sm"),
            AkButton("Dismiss", variant="ghost", size="sm"),
        )
        board.add_cell("Inverse empty", ink_empty_host)
        page.add(board)
        return page

    def _page_patterns(self) -> Page:
        page = Page(
            "06 · Patterns",
            "Composition over isolation.",
            "Same components, different jobs: list, form, empty, help — "
            "mirroring web patterns.html.",
        )

        # List
        list_p = AkPanel()
        list_p.add_header("List", "INVOICES")
        list_p.add_widget(
            AkTable(
                columns=["Document", "Client", "State"],
                rows=[
                    ["INV-1042", "Northwind", "Draft"],
                    ["INV-1043", "Contoso", "Sent"],
                    ["INV-1044", "Fabrikam", "Paid"],
                ],
            )
        )
        list_p.add_row(
            AkButton("Export", variant="ghost", size="sm"),
            AkButton("New invoice", size="sm"),
        )
        page.add(list_p)

        board = AkStyleBoard(columns=2)

        form = AkPanel(tone="surface")
        form.add_header("Form", "CREATE PROJECT")
        form.add_widget(_field("Name", AkInput("Apollo redesign")))
        form.add_widget(_field("Visibility", AkSelect(["Private", "Team", "Public"])))
        form.add_widget(_field("Brief", AkTextarea("Goals, constraints, success metrics…")))
        form.add_row(
            AkButton("Cancel", variant="secondary", size="sm"),
            AkButton("Create project", size="sm"),
        )
        board.add_cell("Form surface", form)

        help_p = AkPanel()
        help_p.add_header("Help", "FAQ")
        help_acc = AkAccordion()
        help_acc.add_item(
            "Theme switching",
            "set_theme('dark'); styles.apply(window) — one shot for the tree.",
            expanded=True,
        )
        help_acc.add_item(
            "Custom title bar",
            "AkTitleBar + FramelessWindowHint. Drag, double-click maximize, edge resize.",
        )
        help_acc.add_item(
            "Fonts",
            "akana.fonts.load_fonts() after QApplication; TTF under assets/fonts.",
        )
        help_p.add_widget(help_acc)
        board.add_cell("Help accordion", help_p)

        page.add(board)

        empty_p = AkPanel(tone="dashed")
        empty_p.add_header("Empty project", "FIRST RUN")
        es = AkEmptyState(
            "Nothing here yet",
            "Start with a pattern above, or open the modal for a confirm flow.",
        )
        es.add_action(AkButton("Get started", size="sm"))
        empty_p.add_widget(es)
        page.add(empty_p)
        return page

    def _open_modal(self) -> None:
        dlg = AkModal("Publish changes?", self)
        body = QLabel(
            "Primary action uses ink. Secondary stays outlined. "
            "The dialog shell is frameless-friendly and monochrome."
        )
        body.setObjectName("akMuted")
        body.setWordWrap(True)
        dlg.set_content(body)
        dlg.set_confirm_text("Publish")
        dlg.set_cancel_text("Keep editing")
        styles.apply(dlg)
        dlg.exec()


def _field(label: str, widget: QWidget) -> QWidget:
    wrap = QWidget()
    lay = QVBoxLayout(wrap)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(SPACE[2])
    cap = QLabel(label)
    cap.setObjectName("akLabel")
    lay.addWidget(cap)
    lay.addWidget(widget)
    return wrap


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Akana Qt")
    if fonts.load_fonts():
        app.setFont(QFont("IBM Plex Sans", 10))
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
