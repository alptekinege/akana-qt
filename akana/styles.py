"""Akana Qt — theme-aware QSS generation.

Styles target widget class names + dynamic properties so a single
`apply(window)` refresh re-themes the whole tree. Matches web components.css.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from akana import tokens
from akana.theme import get_theme

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget


def build() -> str:
    t = get_theme()
    ty = tokens.TYPOGRAPHY
    r = tokens.RADIUS
    fs = tokens.FS
    s = tokens.SPACE
    bw = tokens.BORDER_W

    ink = t["ink"]
    text = t["text"]
    text_sec = t["text_secondary"]
    text_mut = t["text_muted"]
    bg = t["bg"]
    surface = t["surface"]
    surface_2 = t["surface_2"]
    border = t["border"]
    border_s = t["border_strong"]
    inv_text = t["inverse_text"]

    return f"""
/* ---- Base ----
   Intermediate QWidgets stay transparent so toolbars/panels don't show
   nested "boxes" (opaque child edges on a different surface).
*/
QWidget {{
    background-color: transparent;
    color: {text};
    font-family: {ty.family_ui};
    font-size: {fs["md"]}px;
}}
QMainWindow, QDialog {{
    background-color: {bg};
    color: {text};
}}
QFrame#akWindowRoot {{
    background-color: {bg};
    border: {bw}px solid {border_s};
}}
QFrame#akWindowRoot[maximized="true"] {{
    border: none;
}}
QLabel {{
    background: transparent;
    color: {text};
}}
QLabel#akTitle {{
    font-size: {fs["2xl"]}px;
    font-weight: 600;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
}}
QLabel#akSectionTitle {{
    font-size: {fs["xl"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
}}
QLabel#akBrand {{
    font-size: {fs["lg"]}px;
    font-weight: 600;
    color: {ink};
}}
QLabel#akBrandSub {{
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    letter-spacing: {ty.tracking_label};
    color: {text_mut};
}}
QLabel#akLabel {{
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_label};
    text-transform: uppercase;
    color: {text_mut};
}}
QLabel#akMuted {{
    color: {text_sec};
    font-size: {fs["sm"]}px;
}}
QLabel#akLead {{
    color: {text_sec};
    font-size: {fs["md"]}px;
    max-width: 52ch;
}}
QLabel#akPanelTitle {{
    font-size: {fs["sm"]}px;
    font-weight: 500;
    color: {ink};
}}
QFrame#akSidebar {{
    background-color: {surface};
    border: none;
    border-right: {bw}px solid {border};
}}
QFrame#akNavRail {{
    background-color: transparent;
    border: none;
}}
QFrame#akDivider {{
    background-color: {border};
    border: none;
    max-height: 1px;
    min-height: 1px;
}}
QScrollArea {{
    background-color: {bg};
    border: none;
}}
QScrollArea > QWidget {{
    background-color: {bg};
}}
QAbstractScrollArea::viewport {{
    background-color: {bg};
}}

/* ---- Title bar (frameless chrome) ---- */
AkTitleBar, QFrame#AkTitleBar {{
    background-color: {surface};
    border: none;
    border-bottom: {bw}px solid {border};
}}
QLabel#akTitleMark {{
    color: {ink};
    font-size: {fs["sm"]}px;
    padding-right: 2px;
}}
QLabel#akTitleBarLabel {{
    font-size: {fs["sm"]}px;
    font-weight: 500;
    color: {ink};
}}
QLabel#akTitleBarMeta {{
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    letter-spacing: {ty.tracking_label};
    color: {text_mut};
    padding-left: 8px;
}}
QPushButton#akTitleBtn {{
    background: transparent;
    color: {text_sec};
    border: none;
    border-radius: {r.sm}px;
    font-size: 14px;
    padding: 0;
}}
QPushButton#akTitleBtn:hover {{
    background-color: {surface_2};
    color: {ink};
}}
QPushButton#akTitleBtn[role="close"]:hover {{
    background-color: {ink};
    color: {inv_text};
}}

/* ---- Showcase / panels ---- */
AkShowcaseSection, QFrame#AkShowcaseSection {{
    background-color: transparent;
    border: none;
}}
AkStyleBoard, QFrame#AkStyleBoard {{
    background-color: transparent;
    border: none;
}}
QFrame#AkStyleCell {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
AkPanel, QFrame#AkPanel {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
/* Toolbar strip: no double-chrome; children sit on one surface */
QFrame#akToolbar {{
    background-color: {surface};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
QFrame#akToolbar QWidget {{
    background-color: transparent;
}}
AkPanel[tone="surface"], QFrame#AkPanel[tone="surface"] {{
    background-color: {surface};
    border-color: {border};
}}
AkPanel[tone="ink"], QFrame#AkPanel[tone="ink"] {{
    background-color: {ink};
    border-color: {ink};
}}
AkPanel[tone="ink"] QLabel,
QFrame#AkPanel[tone="ink"] QLabel {{
    color: {inv_text};
}}
AkPanel[tone="ink"] QLabel#akLabel,
QFrame#AkPanel[tone="ink"] QLabel#akLabel {{
    color: {border_s};
}}
AkPanel[tone="ink"] QLabel#akPanelTitle,
QFrame#AkPanel[tone="ink"] QLabel#akPanelTitle {{
    color: {inv_text};
}}
AkPanel[tone="ink"] QLabel#akMuted,
QFrame#AkPanel[tone="ink"] QLabel#akMuted {{
    color: {border_s};
}}
/* Ghost on ink: lighten hover */
AkPanel[tone="ink"] AkButton[variant="ghost"],
QFrame#AkPanel[tone="ink"] AkButton[variant="ghost"] {{
    color: {inv_text};
}}
AkPanel[tone="ink"] AkButton[variant="ghost"]:hover,
QFrame#AkPanel[tone="ink"] AkButton[variant="ghost"]:hover {{
    background-color: {border};
    color: {inv_text};
}}
AkPanel[tone="dashed"], QFrame#AkPanel[tone="dashed"] {{
    background-color: {surface};
    border: {bw}px dashed {border_s};
}}
QFrame#akPageHero {{
    background: transparent;
    border: none;
    border-bottom: {bw}px solid {border};
    padding-bottom: 4px;
}}
QFrame#akContentChrome {{
    background-color: {bg};
    border: none;
}}

/* ---- Button ---- */
AkButton {{
    background-color: {ink};
    color: {inv_text};
    border: {bw}px solid transparent;
    border-radius: {r.md}px;
    padding: 10px 16px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
}}
AkButton:hover {{ background-color: {ink}; color: {inv_text}; }}
AkButton:pressed {{ background-color: {ink}; color: {inv_text}; }}
AkButton:disabled {{
    background-color: {surface_2};
    color: {text_mut};
    border: {bw}px solid {border};
}}
AkButton:focus {{ border: 2px solid {ink}; }}
AkButton[variant="secondary"] {{
    background-color: transparent;
    color: {text};
    border: {bw}px solid {border_s};
}}
AkButton[variant="secondary"]:hover {{
    background-color: {surface_2};
    color: {text};
    border: {bw}px solid {border_s};
}}
AkButton[variant="secondary"]:disabled {{
    background-color: transparent;
    color: {text_mut};
    border: {bw}px solid {border};
}}
AkButton[variant="ghost"] {{
    background-color: transparent;
    color: {text};
    border: {bw}px solid transparent;
}}
AkButton[variant="ghost"]:hover {{
    background-color: {surface_2};
    color: {text};
}}
AkButton[variant="ghost"]:disabled {{
    background-color: transparent;
    color: {text_mut};
}}
/* Inverse: for use on ink / solid surfaces */
AkButton[variant="inverse"] {{
    background-color: {inv_text};
    color: {ink};
    border: {bw}px solid transparent;
}}
AkButton[variant="inverse"]:hover {{
    background-color: {inv_text};
    color: {ink};
}}
AkButton[variant="inverse"]:disabled {{
    background-color: {border_s};
    color: {text_mut};
}}
AkButton[akSize="sm"] {{ padding: 7px 12px; font-size: {fs["xs"]}px; }}
AkButton[akSize="lg"] {{ padding: 13px 22px; font-size: {fs["md"]}px; }}

/* ---- Nav ----
   Always reserve 1px border so checked state doesn't change geometry
   (avoids clipped bottom edge / layout jump).
*/
QPushButton#akNavItem {{
    background-color: transparent;
    color: {text_sec};
    border: {bw}px solid transparent;
    border-radius: {r.md}px;
    padding: 10px 14px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
    text-align: left;
}}
QPushButton#akNavItem:hover {{
    color: {text};
    background-color: {surface_2};
    border: {bw}px solid transparent;
}}
QPushButton#akNavItem:checked {{
    color: {ink};
    background-color: {bg};
    border: {bw}px solid {border};
    font-weight: 600;
}}
QPushButton#akNavItem:checked:hover {{
    background-color: {bg};
    border: {bw}px solid {border};
    color: {ink};
}}

/* ---- Card ---- */
AkCard {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
QLabel#akCardTitle {{
    font-size: {fs["lg"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
    background: transparent;
}}
QLabel#akCardBody {{
    font-size: {fs["sm"]}px;
    color: {text_sec};
    background: transparent;
}}

/* ---- Input / Textarea / Select ---- */
AkInput, QLineEdit {{
    background-color: {bg};
    color: {text};
    border: {bw}px solid {border_s};
    border-radius: {r.md}px;
    padding: 10px 14px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    selection-background-color: {ink};
    selection-color: {inv_text};
}}
AkInput:focus, QLineEdit:focus {{
    border: 2px solid {ink};
    padding: 9px 13px;
}}
AkInput:disabled, QLineEdit:disabled {{
    color: {text_mut};
    background-color: {surface_2};
    border-color: {border};
}}
AkTextarea, QPlainTextEdit, QTextEdit {{
    background-color: {bg};
    color: {text};
    border: {bw}px solid {border_s};
    border-radius: {r.md}px;
    padding: 12px 14px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    selection-background-color: {ink};
    selection-color: {inv_text};
}}
AkTextarea:focus, QPlainTextEdit:focus, QTextEdit:focus {{
    border: 2px solid {ink};
}}
AkSelect, QComboBox {{
    background-color: {bg};
    color: {text};
    border: {bw}px solid {border_s};
    border-radius: {r.md}px;
    padding: 8px 14px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    min-height: 28px;
}}
AkSelect:hover, QComboBox:hover {{ border-color: {ink}; }}
AkSelect:focus, QComboBox:focus {{ border: 2px solid {ink}; }}
AkSelect::drop-down, QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
AkSelect::down-arrow, QComboBox::down-arrow {{
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {text_mut};
    margin-right: 10px;
}}
AkSelect QAbstractItemView, QComboBox QAbstractItemView {{
    background: {bg};
    color: {text};
    border: {bw}px solid {border_s};
    selection-background-color: {surface_2};
    selection-color: {ink};
    outline: none;
}}

/* ---- Badge ---- */
AkBadge {{
    background-color: {surface};
    border: {bw}px solid {border_s};
    border-radius: {r.pill}px;
}}
AkBadge QLabel {{
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_label};
    color: {text_sec};
    background: transparent;
}}
AkBadge[variant="solid"] {{
    background-color: {ink};
    border-color: {ink};
}}
AkBadge[variant="solid"] QLabel {{ color: {inv_text}; }}

/* ---- Checkbox (square) ---- */
AkCheckbox {{
    spacing: {s[3]}px;
    color: {text};
    background: transparent;
    font-size: {fs["sm"]}px;
}}
AkCheckbox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: {r.sm}px;
    border: {bw}px solid {border_s};
    background-color: {bg};
}}
AkCheckbox::indicator:checked {{
    background-color: {ink};
    border-color: {ink};
}}
AkCheckbox::indicator:disabled {{
    background-color: {surface};
    border-color: {border};
}}

/* ---- Radio ---- */
AkRadio, QRadioButton {{
    spacing: 8px;
    color: {text};
    background: transparent;
    font-size: {fs["sm"]}px;
}}
AkRadio::indicator, QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: {bw}px solid {border_s};
    background-color: {bg};
}}
AkRadio::indicator:checked, QRadioButton::indicator:checked {{
    border: 5px solid {ink};
    background-color: {inv_text};
}}

/* ---- Toggle switch ---- */
AkToggle {{
    spacing: {s[3]}px;
    color: {text};
    background: transparent;
    font-size: {fs["sm"]}px;
}}
AkToggle::indicator {{
    width: 40px;
    height: 22px;
    border-radius: 11px;
    border: {bw}px solid {border_s};
    background-color: {surface_2};
}}
AkToggle::indicator:checked {{
    background-color: {ink};
    border-color: {ink};
}}
AkToggle::indicator:disabled {{
    background-color: {surface};
    border-color: {border};
}}
QFrame#AkToggleSwitch {{
    background: transparent;
    border: none;
}}

/* ---- Alert ---- */
AkAlert {{
    background-color: {surface};
    border: {bw}px solid {border_s};
    border-radius: {r.md}px;
}}
AkAlert[variant="strong"] {{
    background-color: {bg};
    border: {bw}px solid {ink};
    border-left: 3px solid {ink};
}}
AkAlert[variant="solid"] {{
    background-color: {ink};
    border: {bw}px solid {ink};
}}
QLabel#akAlertIcon {{
    color: {ink};
    font-family: {ty.family_mono};
    font-weight: 600;
    font-size: {fs["sm"]}px;
    background: transparent;
}}
AkAlert[variant="solid"] QLabel#akAlertIcon {{ color: {inv_text}; }}
QLabel#akAlertTitle {{
    font-weight: 500;
    font-size: {fs["sm"]}px;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
    background: transparent;
}}
AkAlert[variant="solid"] QLabel#akAlertTitle {{ color: {inv_text}; }}
QLabel#akAlertText {{
    font-size: {fs["sm"]}px;
    color: {text_sec};
    background: transparent;
}}
AkAlert[variant="solid"] QLabel#akAlertText {{ color: {inv_text}; }}

/* ---- Tabs ---- */
AkTabs, QFrame#AkTabs {{
    background: transparent;
    border: none;
}}
QFrame#akTabList {{
    background: transparent;
    border: none;
    border-bottom: {bw}px solid {border};
}}
QPushButton#akTab {{
    background: transparent;
    color: {text_sec};
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 0;
    padding: 10px 14px;
    margin-bottom: -1px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
}}
QPushButton#akTab:hover {{ color: {text}; }}
QPushButton#akTab:checked {{
    color: {ink};
    border-bottom: 2px solid {ink};
    background: transparent;
}}

/* ---- Accordion ---- */
AkAccordion {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
QFrame#akAccordionItem {{
    background: transparent;
    border: none;
}}
QFrame#akAccordionItem[divided="true"] {{
    border-top: {bw}px solid {border};
}}
QPushButton#akAccordionTrigger {{
    background-color: {bg};
    color: {ink};
    border: none;
    border-radius: 0;
    padding: {s[4]}px {s[5]}px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
    text-align: left;
}}
QPushButton#akAccordionTrigger:hover {{ background-color: {surface}; }}
QPushButton#akAccordionTrigger:checked {{ background-color: {bg}; }}
QLabel#akAccordionPanel {{
    color: {text_sec};
    font-size: {fs["sm"]}px;
    background: transparent;
    padding: 0 {s[5]}px {s[5]}px {s[5]}px;
}}

/* ---- Breadcrumb ---- */
AkBreadcrumb {{
    background: transparent;
    border: none;
}}
QPushButton#akBreadcrumbLink {{
    background: transparent;
    color: {text_sec};
    border: none;
    padding: 2px 4px;
    font-size: {fs["sm"]}px;
    text-decoration: none;
}}
QPushButton#akBreadcrumbLink:hover {{
    color: {ink};
    text-decoration: underline;
}}
QLabel#akBreadcrumbSep {{
    color: {text_mut};
    font-size: {fs["sm"]}px;
    background: transparent;
}}
QLabel#akBreadcrumbCurrent {{
    color: {ink};
    font-weight: 500;
    font-size: {fs["sm"]}px;
    background: transparent;
}}

/* ---- Pagination ---- */
AkPagination {{
    background: transparent;
    border: none;
}}
QPushButton#akPageBtn {{
    background: transparent;
    color: {text_sec};
    border: {bw}px solid transparent;
    border-radius: {r.md}px;
    min-width: 36px;
    min-height: 36px;
    padding: 0 {s[2]}px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
}}
QPushButton#akPageBtn:hover {{
    background-color: {surface};
    color: {text};
}}
QPushButton#akPageBtn:checked,
QPushButton#akPageBtn[current="true"] {{
    border: {bw}px solid {ink};
    color: {ink};
    background-color: {bg};
}}
QPushButton#akPageBtn:disabled {{
    color: {text_mut};
    background: transparent;
}}

/* ---- Table ---- */
QFrame#AkTableWrap, AkTable {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
QTableWidget#AkTable, AkTable QTableWidget {{
    background-color: {bg};
    color: {text};
    border: none;
    border-radius: {r.lg}px;
    gridline-color: {border};
    font-size: {fs["sm"]}px;
    outline: none;
}}
QTableWidget#AkTable::item {{
    padding: {s[4]}px {s[5]}px;
    border-bottom: {bw}px solid {border};
}}
QTableWidget#AkTable::item:selected {{
    background-color: {surface};
    color: {ink};
}}
QTableWidget#AkTable::item:hover {{
    background-color: {surface};
}}
QHeaderView::section {{
    background-color: {bg};
    color: {text_sec};
    border: none;
    border-bottom: {bw}px solid {border};
    padding: {s[4]}px {s[5]}px;
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_label};
    text-transform: uppercase;
}}

/* ---- Empty state ---- */
AkEmptyState, QFrame#AkEmptyState {{
    background-color: {surface};
    border: {bw}px dashed {border_s};
    border-radius: {r.lg}px;
}}
QLabel#akEmptyIcon {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.md}px;
    color: {ink};
    font-size: {fs["lg"]}px;
}}
QLabel#akEmptyTitle {{
    font-size: {fs["lg"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
    background: transparent;
}}
QLabel#akEmptyBody {{
    font-size: {fs["sm"]}px;
    color: {text_sec};
    background: transparent;
}}

/* ---- Modal ---- */
QFrame#akModalCard {{
    background-color: {bg};
    border: {bw}px solid {border_s};
    border-radius: {r.lg}px;
}}
QLabel#akModalTitle {{
    font-size: {fs["xl"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
    background: transparent;
}}

/* ---- Scrollbar ---- */
QScrollBar:vertical, QScrollBar:horizontal {{
    background: {bg};
    border: none;
    width: 10px;
    height: 10px;
    margin: 0;
}}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background: {border};
    border-radius: 5px;
    min-height: 32px;
    min-width: 32px;
}}
QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {{
    background: {text_mut};
}}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}

QStackedWidget {{
    background-color: {bg};
    border: none;
}}
"""


def apply(widget: QWidget) -> None:
    """Apply generated QSS to *widget* (typically the main window)."""
    widget.setStyleSheet(build())
