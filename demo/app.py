"""Akana Qt — design-system gallery (web index + patterns parity)."""

from __future__ import annotations

import sys

from PyQt6.QtCore import QEvent, QPoint, Qt, QRect, QTimer
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QSizeGrip,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from akana import __version__, fonts, styles, winchrome
from akana.components import (
    AkAccordion,
    AkAlert,
    AkBadge,
    AkBreadcrumb,
    AkButton,
    AkCard,
    AkCheckbox,
    AkEmptyState,
    AkField,
    AkInput,
    AkLinkCard,
    AkModal,
    AkNavRail,
    AkNavStrip,
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
from akana.theme import current_name, get_theme, load_saved_theme, set_theme
from akana.tokens import (
    FS,
    GRAY_PRIMITIVES,
    LEAD_W,
    MAX_W,
    RADIUS,
    SIZE_GRIP,
    SPACE,
)
from akana.util import AkFlowLabel

_EDGE = 6

# Sidebar order — link cards jump here
PAGE_INDEX = {
    "Overview": 0,
    "Tokens": 1,
    "Buttons": 2,
    "Forms": 3,
    "Feedback": 4,
    "Data": 5,
    "Patterns": 6,
}


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


def _pattern_title(text: str) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName("akPatternTitle")
    return lab


class Page(QWidget):
    """Gallery page: left-weighted column, max measure, free space on the right.

    Not a centered marketing column — content starts under the sidebar edge
    and stops at MAX_W. Children expand horizontally so tables/panels fill
    the content measure (AlignLeft-only was squeezing them to sizeHint).
    """

    def __init__(
        self,
        eyebrow: str,
        title: str,
        lead: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Horizontal: content left · slack right (never dual-stretch center)
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.setAlignment(Qt.AlignmentFlag.AlignTop)

        inner = QFrame()
        inner.setObjectName("akContentInner")
        inner.setMaximumWidth(MAX_W)
        # Preferred height grows with content (scroll area needs accurate height)
        inner.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        root = QVBoxLayout(inner)
        # Top pad leaves room for bordered preview cards at the scroll edge
        root.setContentsMargins(SPACE[8], SPACE[8], SPACE[8], SPACE[16])
        root.setSpacing(SPACE[10])
        root.setAlignment(Qt.AlignmentFlag.AlignTop)

        hero = QFrame()
        hero.setObjectName("akPageHero")
        hero.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        hv = QVBoxLayout(hero)
        hv.setContentsMargins(0, 0, 0, SPACE[6])
        hv.setSpacing(SPACE[3])
        hv.setAlignment(Qt.AlignmentFlag.AlignTop)
        eye = QLabel(eyebrow)
        eye.setObjectName("akLabel")
        hv.addWidget(eye)
        t = AkFlowLabel(title, object_name="akTitle")
        t.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        hv.addWidget(t)
        if lead:
            # AkFlowLabel fixes 2nd-line clipping that looked like “dots” in SS
            l = AkFlowLabel(lead, object_name="akLead", max_width=LEAD_W)
            l.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            hv.addWidget(l)
        root.addWidget(hero)

        self._body = QVBoxLayout()
        self._body.setSpacing(SPACE[10])
        self._body.setAlignment(Qt.AlignmentFlag.AlignTop)
        root.addLayout(self._body)
        root.addStretch(1)

        # stretch=1 expands to MAX_W; remaining window width stays empty on the right
        row.addWidget(inner, 1, Qt.AlignmentFlag.AlignTop)
        outer.addLayout(row, 1)

    def add(self, widget: QWidget) -> None:
        # Expand horizontally to the content measure (MAX_W column)
        sp = widget.sizePolicy()
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, sp.verticalPolicy())
        # Full content width — do not AlignLeft (that clamps to sizeHint)
        self._body.addWidget(widget)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akana Qt")
        self.resize(1280, 860)
        self.setMinimumSize(960, 620)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window
        )
        self._resize_edge: str | None = None
        self._resize_origin = QPoint()
        self._resize_geom = QRect()
        self._snap_enabled = False

        self.shell = QFrame()
        self.shell.setObjectName("akWindowRoot")
        self.shell.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCentralWidget(self.shell)
        outer = QVBoxLayout(self.shell)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.titlebar = AkTitleBar("Akana Qt")
        self.titlebar.set_window(self)
        self.titlebar.set_meta(self._meta_label())
        self.titlebar.minimizeClicked.connect(self.showMinimized)
        self.titlebar.maximizeClicked.connect(self._toggle_max)
        self.titlebar.closeClicked.connect(self.close)

        self.theme_chip = AkButton(
            self._theme_chip_label(), variant="secondary", size="sm"
        )
        self.theme_chip.clicked.connect(self._toggle_theme)
        self.titlebar.add_action(self.theme_chip)
        outer.addWidget(self.titlebar)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        left = QFrame()
        left.setObjectName("akSidebar")
        left.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        left.setFixedWidth(260)
        lv = QVBoxLayout(left)
        lv.setContentsMargins(SPACE[4], SPACE[5], SPACE[4], SPACE[4])
        lv.setSpacing(SPACE[4])

        brand_block = QVBoxLayout()
        brand_block.setSpacing(SPACE[1])
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
        self._page_names = list(PAGE_INDEX.keys())
        for name in self._page_names:
            self.nav.add_item(name)
        self.nav.currentChanged.connect(self._on_nav)
        lv.addWidget(self.nav, 1)

        foot = QLabel(
            f"IBM Plex · offline\nNo accent · no CDN\nv{__version__} · web parity"
        )
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

        grip_row = QHBoxLayout()
        grip_row.setContentsMargins(0, 0, SPACE[1], SPACE[1])
        grip_row.addStretch(1)
        grip = QSizeGrip(content)
        grip.setFixedSize(SIZE_GRIP, SIZE_GRIP)
        grip_row.addWidget(grip)
        cv.addLayout(grip_row)

        body.addWidget(content, 1)
        outer.addLayout(body, 1)

        self.stack.addWidget(_scroll(self._page_overview()))
        self.stack.addWidget(_scroll(self._page_tokens()))
        self.stack.addWidget(_scroll(self._page_buttons()))
        self.stack.addWidget(_scroll(self._page_forms()))
        self.stack.addWidget(_scroll(self._page_feedback()))
        self.stack.addWidget(_scroll(self._page_data()))
        self.stack.addWidget(_scroll(self._page_patterns()))

        styles.apply(self)
        self.nav.set_current_index(0)
        self._sync_window_chrome()

    def _meta_label(self) -> str:
        return f"v{__version__} · {current_name()}"

    def _theme_chip_label(self) -> str:
        return "Light" if current_name() == "dark" else "Dark"

    def go_page(self, name: str) -> None:
        idx = PAGE_INDEX.get(name)
        if idx is not None:
            self.nav.set_current_index(idx)

    # ---- chrome ----

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
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
        from akana.util import repolish

        repolish(self.shell)

    def _toggle_max(self) -> None:
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        self._sync_window_chrome()

    def _toggle_theme(self) -> None:
        name = "dark" if current_name() == "light" else "light"
        set_theme(name)
        self.theme_chip.setText(self._theme_chip_label())
        self.titlebar.set_meta(self._meta_label())
        styles.apply(self)
        self._sync_window_chrome()
        # Rebuild token swatches if page is live — full stylesheet covers colors;
        # re-apply swatch fill colors explicitly
        self._refresh_swatches()

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
            "Monochrome, text-first.",
            "A clean, minimal interface system built on ink and whitespace. "
            "No accent color, no decorative images — hierarchy comes from type, "
            "spacing, and small glyphs. Akana = ak + ana (clarity + source). "
            f"Qt port v{__version__}, aligned with web Akana v0.5.",
        )

        # Principles
        board = AkStyleBoard(columns=3)
        for tone, title, body in (
            ("default", "Ink", "The only strong tone. Headlines, primary actions, focus."),
            ("surface", "Surface", "Quiet structure. Rails, panels, hover fills."),
            ("ink", "Inverse", "Solid fill for maximum emphasis. Inverse type only."),
        ):
            p = AkPanel(tone=tone)  # type: ignore[arg-type]
            p.add_header(title, "PRINCIPLE")
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
            board.add_cell(f"{title}", p)
        page.add(board)

        # Component catalog (web index)
        cat = AkShowcaseSection(
            "Components",
            "Open a surface",
            "Same inventory as web gallery. Jump to the live demo page.",
        )
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(SPACE[4])
        grid.setVerticalSpacing(SPACE[4])
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        catalog = [
            ("Buttons", "Actions, variants, sizes", "Buttons"),
            ("Forms", "Fields, choices, switches", "Forms"),
            ("Feedback", "Alerts, tabs, accordion", "Feedback"),
            ("Data", "Tables & empty states", "Data"),
            ("Patterns", "List · form · empty · help", "Patterns"),
            ("Tokens", "Ramp, type, space", "Tokens"),
        ]
        for i, (name, desc, target) in enumerate(catalog):
            card = AkLinkCard(name, desc)
            card.activated.connect(lambda t=target: self.go_page(t))
            grid.addWidget(card, i // 2, i % 2)
        wrap = QWidget()
        wrap.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        wrap.setLayout(grid)
        cat.add_widget(wrap)
        page.add(cat)

        # Working strip
        sec = AkShowcaseSection(
            "Composition",
            "Working strip",
            "How Akana reads in product density — badges, field, select, actions.",
        )
        toolbar = QFrame()
        toolbar.setObjectName("akToolbar")
        toolbar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        toolbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        tv = QVBoxLayout(toolbar)
        tv.setContentsMargins(SPACE[5], SPACE[4], SPACE[5], SPACE[4])
        tv.setSpacing(SPACE[4])
        head = QHBoxLayout()
        ht = QLabel("Library")
        ht.setObjectName("akPanelTitle")
        head.addWidget(ht)
        head.addStretch(1)
        hm = QLabel("LIVE")
        hm.setObjectName("akLabel")
        head.addWidget(hm)
        tv.addLayout(head)
        row = QHBoxLayout()
        row.setSpacing(SPACE[3])
        row.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(AkBadge("Draft"), 0, Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(AkBadge("Mono", variant="solid"), 0, Qt.AlignmentFlag.AlignVCenter)
        # Match control height (md) so the strip does not mix 48px fields with 36px chips
        row.addWidget(AkInput("Search components…"), 1, Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(
            AkSelect(["All", "Core", "Form", "Feedback"]),
            0,
            Qt.AlignmentFlag.AlignVCenter,
        )
        row.addWidget(
            AkButton("Filter", variant="secondary", size="md"),
            0,
            Qt.AlignmentFlag.AlignVCenter,
        )
        row.addWidget(AkButton("New", size="md"), 0, Qt.AlignmentFlag.AlignVCenter)
        tv.addLayout(row)
        sec.add_widget(toolbar)
        page.add(sec)

        return page

    def _page_tokens(self) -> Page:
        page = Page(
            "02 · Tokens",
            "Three layers. One ink ramp.",
            "Primitive grays never appear in components. Semantic tokens rebind "
            "for dark mode. Layout uses SPACE, FS, RADIUS, CONTROL_H, FOCUS_W.",
        )

        # Semantic swatches for active theme
        sec = AkShowcaseSection(
            "Semantic",
            f"Active · {current_name()}",
            "These are the only colors components should reference.",
        )
        self._swatch_host = QWidget()
        self._swatch_grid = QGridLayout(self._swatch_host)
        self._swatch_grid.setContentsMargins(0, 0, 0, 0)
        self._swatch_grid.setHorizontalSpacing(SPACE[3])
        self._swatch_grid.setVerticalSpacing(SPACE[3])
        self._swatch_grid.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        self._swatch_frames: list[tuple[QFrame, str]] = []
        self._build_semantic_swatches()
        sec.add_widget(self._swatch_host)
        page.add(sec)

        # Primitive ramp (fixed) — left-packed, labels under chips start-aligned
        prim = AkShowcaseSection(
            "Primitive",
            "Gray ramp",
            "Theme-agnostic. Do not use directly in widget code.",
        )
        ramp = QHBoxLayout()
        ramp.setSpacing(SPACE[2])
        ramp.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        for key in (
            "gray-0", "gray-50", "gray-100", "gray-200", "gray-300",
            "gray-400", "gray-500", "gray-600", "gray-700", "gray-800",
            "gray-850", "gray-900", "gray-950",
        ):
            cell = QVBoxLayout()
            cell.setSpacing(SPACE[1])
            cell.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            sw = QFrame()
            sw.setObjectName("akSwatch")
            sw.setFixedSize(SPACE[12], SPACE[12])
            sw.setStyleSheet(
                f"QFrame#akSwatch {{ background-color: {GRAY_PRIMITIVES[key]}; "
                f"border: 1px solid {get_theme()['border']}; "
                f"border-radius: {RADIUS.md}px; }}"
            )
            cell.addWidget(sw, 0, Qt.AlignmentFlag.AlignLeft)
            n = QLabel(key.replace("gray-", ""))
            n.setObjectName("akSwatchName")
            n.setAlignment(Qt.AlignmentFlag.AlignLeft)
            cell.addWidget(n, 0, Qt.AlignmentFlag.AlignLeft)
            w = QWidget()
            w.setLayout(cell)
            ramp.addWidget(w, 0, Qt.AlignmentFlag.AlignLeft)
        ramp.addStretch(1)
        ramp_w = QWidget()
        ramp_w.setLayout(ramp)
        prim.add_widget(ramp_w)
        page.add(prim)

        # Type / space reference
        ref = AkStyleBoard(columns=2)
        type_p = AkPanel()
        type_p.add_header("Type scale", "DESKTOP PX")
        for name, key in (
            ("2xs · label", "2xs"),
            ("xs", "xs"),
            ("sm · control", "sm"),
            ("md · body", "md"),
            ("lg · lead", "lg"),
            ("xl", "xl"),
            ("2xl · section", "2xl"),
            ("3xl · page", "3xl"),
        ):
            px = FS[key]
            lab = QLabel(f"{name}  ·  {px}px")
            lab.setObjectName("akMuted")
            f = lab.font()
            f.setPixelSize(px if px <= 22 else min(px, 22))
            lab.setFont(f)
            type_p.add_widget(lab)
        ref.add_cell("Typography", type_p)

        space_p = AkPanel(tone="surface")
        space_p.add_header("Spacing", "4PX BASE")
        for k in (1, 2, 3, 4, 5, 6, 8, 12):
            v = SPACE[k]
            row = QHBoxLayout()
            cap = QLabel(f"space-{k}")
            cap.setObjectName("akMonoMeta")
            row.addWidget(cap)
            bar = QFrame()
            bar.setFixedHeight(SPACE[2])
            bar.setFixedWidth(v)
            bar.setStyleSheet(
                f"background: {get_theme()['ink']}; border: none; "
                f"border-radius: {RADIUS.sm // 2}px;"
            )
            row.addWidget(bar)
            row.addWidget(QLabel(f"{v}px"))
            row.addStretch(1)
            wrap = QWidget()
            wrap.setLayout(row)
            space_p.add_widget(wrap)
        ref.add_cell("Rhythm", space_p)
        page.add(ref)

        return page

    def _build_semantic_swatches(self) -> None:
        # Clear
        while self._swatch_grid.count():
            item = self._swatch_grid.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        self._swatch_frames.clear()

        t = get_theme()
        keys = [
            "bg", "surface", "surface_2", "border", "border_strong",
            "ink", "text", "text_secondary", "text_muted",
            "inverse_bg", "inverse_text", "ink_hover",
        ]
        for i, key in enumerate(keys):
            cell = QVBoxLayout()
            cell.setSpacing(SPACE[1])
            cell.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            sw = QFrame()
            sw.setObjectName("akSwatch")
            sw.setMinimumHeight(56)
            hex_v = t[key]
            sw.setStyleSheet(
                f"QFrame#akSwatch {{ background-color: {hex_v}; "
                f"border: 1px solid {t['border']}; border-radius: 8px; }}"
            )
            cell.addWidget(sw)
            n = QLabel(key)
            n.setObjectName("akSwatchName")
            n.setAlignment(Qt.AlignmentFlag.AlignLeft)
            cell.addWidget(n)
            h = QLabel(hex_v)
            h.setObjectName("akSwatchHex")
            h.setAlignment(Qt.AlignmentFlag.AlignLeft)
            cell.addWidget(h)
            wrap = QWidget()
            wrap.setLayout(cell)
            self._swatch_grid.addWidget(
                wrap, i // 4, i % 4, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
            )
            self._swatch_frames.append((sw, key))

    def _refresh_swatches(self) -> None:
        if not hasattr(self, "_swatch_grid"):
            return
        self._build_semantic_swatches()

    def _page_buttons(self) -> Page:
        page = Page(
            "03 · Buttons",
            "Weight carries intent.",
            "Primary fills with ink. Secondary outlines with border-strong. "
            "Ghost stays quiet until hover. Focus always uses a 2px ink ring "
            "without shifting layout.",
        )

        board = AkStyleBoard(columns=2)

        v = AkPanel()
        v.add_header("Variants", "PRIMARY · SECONDARY · GHOST")
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

        inv = AkPanel(tone="ink")
        inv.add_header("On ink", "INVERSE")
        inv_copy = QLabel("Use inverse fill when the host surface is ink.")
        inv_copy.setObjectName("akMuted")
        inv_copy.setWordWrap(True)
        inv.add_widget(inv_copy)
        inv.add_row(
            AkButton("Continue", variant="inverse", size="sm"),
            AkButton("Skip", variant="ghost", size="sm"),
        )
        board.add_cell("Inverse context", inv)

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

        # Segmented nav demo
        nav_sec = AkShowcaseSection(
            "Nav strip",
            "Horizontal segment",
            "Web `.ak-nav` — surface shell, active item on bg with weight.",
        )
        strip = AkNavStrip()
        for label in ("Overview", "Specs", "Activity", "Settings"):
            strip.add_item(label)
        nav_sec.add_widget(strip)
        page.add(nav_sec)

        return page

    def _page_forms(self) -> Page:
        page = Page(
            "04 · Forms",
            "Quiet fields. Loud focus.",
            "AkField composes mono label + control + helper. Errors use ink "
            "border and body-colored helper — never a red accent.",
        )

        board = AkStyleBoard(columns=2)

        fields = AkPanel()
        fields.add_header("Fields", "AKFIELD")
        email = AkField("Email", AkInput("you@example.com"), helper="We'll never share it.")
        role = AkField("Role", AkSelect(["Designer", "Engineer", "Writer"]))
        notes = AkField("Notes", AkTextarea("Optional context…"))
        fields.add_widget(_stack(email, role, notes, spacing=SPACE[4]))
        board.add_cell("Standard", fields)

        err = AkPanel(tone="surface")
        err.add_header("Validation", "INK ONLY")
        bad = AkField("Workspace slug", AkInput("My Workspace!"))
        bad.set_error("Use lowercase letters, numbers, and hyphens.")
        err.add_widget(bad)
        err.add_widget(
            AkField("Display name", AkInput("Ada"), helper="Shown on invoices.")
        )
        board.add_cell("Error state", err)

        dense = AkPanel()
        dense.add_header("Choices", "CHECK · RADIO · SWITCH")
        dense.add_widget(AkCheckbox("Email me product updates"))
        dense.add_widget(AkCheckbox("Share usage analytics"))
        rg = AkRadioGroup(["Public", "Unlisted", "Private"])
        rg.set_checked_index(1)
        dense.add_widget(rg)
        dense.add_widget(AkToggleSwitch("Two-factor authentication"))
        dense.add_widget(AkToggleSwitch("Marketing emails"))
        board.add_cell("Selection", dense)

        disabled = AkPanel(tone="dashed")
        disabled.add_header("Disabled", "MUTED")
        d = AkInput("Read only value")
        d.setEnabled(False)
        disabled.add_widget(AkField("Locked", d, helper="Contact an admin to edit."))
        db = AkButton("Unavailable", variant="secondary", size="sm")
        db.setEnabled(False)
        disabled.add_row(db)
        board.add_cell("States", disabled)

        page.add(board)
        return page

    def _page_feedback(self) -> Page:
        page = Page(
            "05 · Feedback",
            "Signal without color.",
            "Alerts escalate through border weight and fill — default, strong, "
            "then solid ink. Disclosure keeps the chevron on the right.",
        )

        sec = AkShowcaseSection("Alerts", "Three levels of attention")
        sec.add_widget(
            AkAlert(
                "Default",
                "Surface fill, border-strong. Everyday notices and confirmations.",
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
            ("Changelog", f"v{__version__} · painted controls · stable focus · AkField."),
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
            "break dark-mode semantics — every “success green” would need a twin.",
            expanded=True,
        )
        acc.add_item(
            "How is dark mode done?",
            "Only the semantic layer rebinds. The gray ramp never flips itself. "
            "Components keep the same token names.",
        )
        acc.add_item(
            "What about icons?",
            "Web uses 1px SVG. Qt uses a small monochrome glyph set in akana.icons — "
            "no image assets, no CDN.",
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
            "06 · Data",
            "Tables read like type, not grids.",
            "Mono uppercase headers, quiet row hover, no zebra stripes. "
            "Empty states use dashed borders — invitation, not error.",
        )

        table_panel = AkPanel()
        table_panel.add_header("Table", "SELECT A ROW")
        table = AkTable(
            columns=["Name", "Role", "Status"],
            rows=[
                ["Ada Lovelace", "Engineer", "Active"],
                ["Grace Hopper", "Admiral", "Active"],
                ["Alan Turing", "Analyst", "Archived"],
                ["Katherine Johnson", "Mathematician", "Active"],
            ],
        )
        table.setMinimumHeight(280)
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
        body = QLabel("When surrounding chrome is ink, keep actions light.")
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
            "07 · Patterns",
            "Components in context.",
            "Small compositions using only Akana tokens and components — "
            "mirroring web patterns.html: list, form, empty, help.",
        )

        # List pattern: breadcrumb + table + badges + pagination
        list_p = AkPanel()
        list_p.add_widget(_pattern_title("List · breadcrumb + table + pagination"))
        list_p.add_widget(AkBreadcrumb(["Home", "Workspace", "Projects"]))
        head = QHBoxLayout()
        count = QLabel("12 projects")
        count.setObjectName("akLabel")
        head.addWidget(count)
        head.addStretch(1)
        head.addWidget(AkButton("New", size="sm"))
        head_w = QWidget()
        head_w.setLayout(head)
        list_p.add_widget(head_w)

        table = AkTable(
            columns=["Name", "Status", "Updated"],
            rows=[
                ["Akana gallery", "", "Today"],
                ["Invoice export", "", "Yesterday"],
                ["Archive 2024", "", "Mon"],
            ],
        )
        # Badge cells
        table.set_cell_widget(0, 1, _badge_cell("Active"))
        table.set_cell_widget(1, 1, _badge_cell("Live", solid=True))
        table.set_cell_widget(2, 1, _badge_cell("Paused"))
        table.setMinimumHeight(220)
        list_p.add_widget(table)
        list_p.add_widget(AkPagination(total_pages=3, current=1))
        page.add(list_p)

        board = AkStyleBoard(columns=2)

        form = AkPanel(tone="surface")
        form.add_widget(_pattern_title("Form · create project"))
        form.add_widget(AkField("Name", AkInput("Apollo redesign")))
        form.add_widget(AkField("Visibility", AkSelect(["Private", "Team", "Public"])))
        form.add_widget(
            AkField("Brief", AkTextarea("Goals, constraints, success metrics…"))
        )
        form.add_row(
            AkButton("Cancel", variant="secondary", size="sm"),
            AkButton("Create project", size="sm"),
        )
        board.add_cell("Form surface", form)

        help_p = AkPanel()
        help_p.add_widget(_pattern_title("Help · FAQ accordion"))
        help_acc = AkAccordion()
        help_acc.add_item(
            "Theme switching",
            "set_theme('dark'); styles.apply(window). Preference persists in QSettings "
            "(organization Akana, application AkanaQt).",
            expanded=True,
        )
        help_acc.add_item(
            "Custom title bar",
            "AkTitleBar + FramelessWindowHint. Drag, double-click maximize, edge resize. "
            "On Windows, winchrome restores snap after show.",
        )
        help_acc.add_item(
            "Fonts",
            "akana.fonts.load_fonts() after QApplication; TTF under akana/assets/fonts. "
            "Re-bundle with scripts/download_fonts.py.",
        )
        help_p.add_widget(help_acc)
        board.add_cell("Help accordion", help_p)
        page.add(board)

        empty_p = AkPanel(tone="dashed")
        empty_p.add_widget(_pattern_title("Empty · first run"))
        es = AkEmptyState(
            "Nothing here yet",
            "Start with a pattern above, or open the modal for a confirm flow.",
        )
        start_btn = AkButton("Get started", size="sm")
        modal_btn = AkButton("Open modal…", variant="secondary", size="sm")
        modal_btn.clicked.connect(self._open_modal)
        es.add_action(start_btn)
        es.add_action(modal_btn)
        empty_p.add_widget(es)
        # Full-width empty block so CTA stays above the scroll bottom
        page.add(empty_p)
        return page

    def _open_modal(self) -> None:
        dlg = AkModal("Publish changes?", self)
        body = QLabel(
            "Primary action uses ink. Secondary stays outlined. "
            "Escape cancels. The scrim is monochrome — no brand tint."
        )
        body.setObjectName("akMuted")
        body.setWordWrap(True)
        dlg.set_content(body)
        dlg.set_confirm_text("Publish")
        dlg.set_cancel_text("Keep editing")
        styles.apply(dlg)
        dlg.exec()


def _badge_cell(text: str, *, solid: bool = False) -> QWidget:
    wrap = QWidget()
    lay = QHBoxLayout(wrap)
    lay.setContentsMargins(SPACE[4], SPACE[2], SPACE[4], SPACE[2])
    lay.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    lay.addWidget(AkBadge(text, variant="solid" if solid else "default"), 0)
    lay.addStretch(1)
    return wrap


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Akana Qt")
    app.setOrganizationName("Akana")
    if fonts.load_fonts():
        app.setFont(QFont("IBM Plex Sans", 11))
    load_saved_theme()
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
