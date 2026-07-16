"""Akana Qt — theme-aware QSS generation.

Matches web `assets/components.css` (Akana v0.5) within QSS limits.
Focus rings use a fixed 2px border width so geometry never jumps.
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
    ch = tokens.CONTROL_H
    btn_h = tokens.BUTTON_H
    btn_sm = tokens.BUTTON_H_SM
    btn_lg = tokens.BUTTON_H_LG
    page_btn = tokens.PAGE_BTN
    nav_h = tokens.NAV_ITEM_H

    ink = t["ink"]
    ink_hover = t["ink_hover"]
    ink_active = t["ink_active"]
    text = t["text"]
    text_sec = t["text_secondary"]
    text_mut = t["text_muted"]
    bg = t["bg"]
    surface = t["surface"]
    surface_2 = t["surface_2"]
    border = t["border"]
    border_s = t["border_strong"]
    inv_text = t["inverse_text"]
    inv_bg = t["inverse_bg"]

    return f"""
/* ========== Base ========== */
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

/* Type roles */
QLabel#akTitle {{
    font-size: {fs["3xl"]}px;
    font-weight: 700;
    letter-spacing: {ty.tracking_tight};
    line-height: {ty.lh_tight};
    color: {ink};
}}
QLabel#akSectionTitle {{
    font-size: {fs["xl"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
}}
QLabel#akBrand {{
    font-size: {fs["xl"]}px;
    font-weight: 700;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
}}
QLabel#akBrandSub {{
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    letter-spacing: {ty.tracking_label};
    text-transform: uppercase;
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
QLabel#akFieldLabel {{
    font-family: {ty.family_mono};
    font-size: {fs["xs"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_label};
    text-transform: uppercase;
    color: {text_sec};
}}
QLabel#akMuted {{
    color: {text_sec};
    font-size: {fs["sm"]}px;
}}
QLabel#akLead {{
    color: {text_sec};
    font-size: {fs["lg"]}px;
    max-width: 560px;
}}
QLabel#akPanelTitle {{
    font-size: {fs["sm"]}px;
    font-weight: 500;
    color: {ink};
}}
QLabel#akHelper {{
    font-size: {fs["xs"]}px;
    color: {text_mut};
}}
QLabel#akHelperError {{
    font-size: {fs["xs"]}px;
    color: {text};
}}
QLabel#akMonoMeta {{
    font-family: {ty.family_mono};
    font-size: {fs["xs"]}px;
    color: {text_mut};
}}

/* Shell */
QFrame#akSidebar {{
    background-color: {surface};
    border: none;
    border-right: {bw}px solid {border};
}}
QFrame#akNavRail {{ background: transparent; border: none; }}
QFrame#akDivider {{
    background-color: {border};
    border: none;
    max-height: 1px;
    min-height: 1px;
}}
QScrollArea {{ background-color: {bg}; border: none; }}
QScrollArea > QWidget {{ background-color: {bg}; }}
QAbstractScrollArea::viewport {{ background-color: {bg}; }}
QFrame#akContentChrome {{ background-color: {bg}; border: none; }}
QFrame#akContentInner {{ background: transparent; border: none; }}
QFrame#akPageHero {{
    background: transparent;
    border: none;
    border-bottom: {bw}px solid {border};
}}
QStackedWidget {{ background-color: {bg}; border: none; }}

/* Title bar */
AkTitleBar, QFrame#AkTitleBar {{
    background-color: {surface};
    border: none;
    border-bottom: {bw}px solid {border};
}}
QLabel#akTitleMark {{ color: {ink}; font-size: {fs["sm"]}px; }}
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

/* Showcase */
AkShowcaseSection, QFrame#AkShowcaseSection {{ background: transparent; border: none; }}
AkStyleBoard, QFrame#AkStyleBoard {{ background: transparent; border: none; }}
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
QFrame#akToolbar {{
    background-color: {surface};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
QFrame#akToolbar QWidget {{ background-color: transparent; }}
AkPanel[tone="surface"], QFrame#AkPanel[tone="surface"] {{
    background-color: {surface};
    border-color: {border};
}}
AkPanel[tone="ink"], QFrame#AkPanel[tone="ink"] {{
    background-color: {ink};
    border-color: {ink};
}}
AkPanel[tone="ink"] QLabel,
QFrame#AkPanel[tone="ink"] QLabel {{ color: {inv_text}; }}
AkPanel[tone="ink"] QLabel#akLabel,
QFrame#AkPanel[tone="ink"] QLabel#akLabel {{ color: {border_s}; }}
AkPanel[tone="ink"] QLabel#akPanelTitle,
QFrame#AkPanel[tone="ink"] QLabel#akPanelTitle {{ color: {inv_text}; }}
AkPanel[tone="ink"] QLabel#akMuted,
QFrame#AkPanel[tone="ink"] QLabel#akMuted {{ color: {border_s}; }}
AkPanel[tone="ink"] AkButton[variant="ghost"],
QFrame#AkPanel[tone="ink"] AkButton[variant="ghost"] {{ color: {inv_text}; }}
AkPanel[tone="ink"] AkButton[variant="ghost"]:hover,
QFrame#AkPanel[tone="ink"] AkButton[variant="ghost"]:hover {{
    background-color: {border};
    color: {inv_text};
}}
AkPanel[tone="dashed"], QFrame#AkPanel[tone="dashed"] {{
    background-color: {surface};
    border: {bw}px dashed {border_s};
}}

/* Token swatch */
QFrame#akSwatch {{
    border: {bw}px solid {border};
    border-radius: {r.md}px;
    min-height: 56px;
}}
QLabel#akSwatchHex {{
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    color: {text_mut};
}}
QLabel#akSwatchName {{
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    letter-spacing: {ty.tracking_label};
    text-transform: uppercase;
    color: {text_sec};
}}

/* Link card (gallery index) */
AkLinkCard, QFrame#AkLinkCard {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
AkLinkCard[hovered="true"], QFrame#AkLinkCard[hovered="true"] {{
    border-color: {border_s};
}}
AkLinkCard:focus, QFrame#AkLinkCard:focus {{
    border: 2px solid {ink};
}}
QLabel#akLinkName {{
    font-size: {fs["lg"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_tight};
    color: {ink};
    background: transparent;
}}
QLabel#akLinkDesc {{
    font-size: {fs["sm"]}px;
    color: {text_sec};
    background: transparent;
}}
QLabel#akLinkGo {{
    color: {text_mut};
    font-size: {fs["lg"]}px;
    background: transparent;
    min-width: 20px;
}}
AkLinkCard[hovered="true"] QLabel#akLinkGo {{
    color: {ink};
}}

/* ========== Button ==========
   Always 2px border → focus never shifts layout.
   Heights tuned for desktop hit targets (larger than web CSS padding alone).
*/
AkButton {{
    background-color: {ink};
    color: {inv_text};
    border: 2px solid transparent;
    border-radius: {r.md}px;
    padding: 0 18px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
    min-height: {btn_h}px;
    max-height: {btn_h}px;
}}
AkButton:hover {{ background-color: {ink_hover}; color: {inv_text}; }}
AkButton:pressed {{ background-color: {ink_active}; color: {inv_text}; }}
AkButton:disabled {{
    background-color: {surface_2};
    color: {text_mut};
    border: 2px solid {border};
}}
AkButton:focus {{ border: 2px solid {ink}; }}

AkButton[variant="secondary"] {{
    background-color: transparent;
    color: {text};
    border: 2px solid {border_s};
}}
AkButton[variant="secondary"]:hover {{
    background-color: {surface_2};
    color: {text};
    border: 2px solid {border_s};
}}
AkButton[variant="secondary"]:pressed {{
    background-color: {surface};
    color: {ink};
}}
AkButton[variant="secondary"]:disabled {{
    background-color: transparent;
    color: {text_mut};
    border: 2px solid {border};
}}
AkButton[variant="secondary"]:focus {{ border: 2px solid {ink}; }}

AkButton[variant="ghost"] {{
    background-color: transparent;
    color: {text};
    border: 2px solid transparent;
}}
AkButton[variant="ghost"]:hover {{ background-color: {surface_2}; color: {text}; }}
AkButton[variant="ghost"]:pressed {{ background-color: {surface}; color: {ink}; }}
AkButton[variant="ghost"]:disabled {{ color: {text_mut}; background: transparent; }}
AkButton[variant="ghost"]:focus {{ border: 2px solid {ink}; }}

AkButton[variant="inverse"] {{
    background-color: {inv_text};
    color: {inv_bg};
    border: 2px solid transparent;
}}
AkButton[variant="inverse"]:hover {{
    background-color: {surface};
    color: {inv_bg};
}}
AkButton[variant="inverse"]:pressed {{
    background-color: {surface_2};
    color: {inv_bg};
}}
AkButton[variant="inverse"]:disabled {{
    background-color: {border_s};
    color: {text_mut};
}}
AkButton[variant="inverse"]:focus {{ border: 2px solid {inv_text}; }}

AkButton[akSize="sm"] {{
    padding: 0 14px;
    font-size: {fs["xs"]}px;
    min-height: {btn_sm}px;
    max-height: {btn_sm}px;
}}
AkButton[akSize="lg"] {{
    padding: 0 22px;
    font-size: {fs["md"]}px;
    min-height: {btn_lg}px;
    max-height: {btn_lg}px;
}}

/* ========== Nav ========== */
QPushButton#akNavItem {{
    background-color: transparent;
    color: {text_sec};
    border: 2px solid transparent;
    border-radius: {r.md}px;
    padding: 0 16px;
    min-height: {nav_h}px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
    text-align: left;
}}
QPushButton#akNavItem:hover {{
    color: {text};
    background-color: {surface_2};
}}
QPushButton#akNavItem:checked {{
    color: {ink};
    background-color: {bg};
    border: 2px solid {border};
    font-weight: 600;
}}
QPushButton#akNavItem:focus {{ border: 2px solid {ink}; }}

AkNavStrip, QFrame#AkNavStrip {{
    background-color: {surface};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
QPushButton#akNavStripItem {{
    background-color: transparent;
    color: {text_sec};
    border: 2px solid transparent;
    border-radius: {r.md}px;
    padding: 0 16px;
    min-height: 40px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
}}
QPushButton#akNavStripItem:hover {{
    color: {text};
    background-color: {surface_2};
}}
QPushButton#akNavStripItem:checked {{
    color: {ink};
    background-color: {bg};
    border: 2px solid transparent;
    font-weight: 600;
}}
QPushButton#akNavStripItem:focus {{ border: 2px solid {ink}; }}

/* ========== Card ========== */
AkCard {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
AkCard:hover {{ border-color: {border_s}; }}
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
QLabel#akCardAction {{
    font-family: {ty.family_mono};
    font-size: {fs["xs"]}px;
    letter-spacing: {ty.tracking_label};
    text-transform: uppercase;
    color: {ink};
    background: transparent;
    margin-top: {s[2]}px;
}}
QLabel#akCardIcon {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.md}px;
    color: {ink};
    font-size: {fs["md"]}px;
    min-width: {tokens.CARD_ICON}px;
    max-width: {tokens.CARD_ICON}px;
    min-height: {tokens.CARD_ICON}px;
    max-height: {tokens.CARD_ICON}px;
}}

/* ========== Input / Textarea / Select ==========
   Always 2px border; rest color = border_strong.
*/
AkInput, QLineEdit {{
    background-color: {bg};
    color: {text};
    border: 2px solid {border_s};
    border-radius: {r.md}px;
    padding: 0 13px;
    min-height: {ch}px;
    max-height: {ch}px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    selection-background-color: {ink};
    selection-color: {inv_text};
}}
AkInput:hover, QLineEdit:hover {{ border-color: {ink}; }}
AkInput:focus, QLineEdit:focus {{ border: 2px solid {ink}; }}
AkInput:disabled, QLineEdit:disabled {{
    color: {text_mut};
    background-color: {surface_2};
    border-color: {border};
}}
AkInput[akError="true"], QLineEdit[akError="true"] {{
    border: 2px solid {ink};
}}

AkTextarea, QPlainTextEdit, QTextEdit {{
    background-color: {bg};
    color: {text};
    border: 2px solid {border_s};
    border-radius: {r.md}px;
    padding: 11px 13px;
    min-height: 140px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    selection-background-color: {ink};
    selection-color: {inv_text};
}}
AkTextarea:hover, QPlainTextEdit:hover, QTextEdit:hover {{ border-color: {ink}; }}
AkTextarea:focus, QPlainTextEdit:focus, QTextEdit:focus {{ border: 2px solid {ink}; }}
AkTextarea:disabled, QPlainTextEdit:disabled, QTextEdit:disabled {{
    color: {text_mut};
    background-color: {surface_2};
    border-color: {border};
}}
AkTextarea[akError="true"], QPlainTextEdit[akError="true"] {{
    border: 2px solid {ink};
}}

AkSelect, QComboBox {{
    background-color: {bg};
    color: {text};
    border: 2px solid {border_s};
    border-radius: {r.md}px;
    padding: 0 13px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    min-height: {ch}px;
}}
AkSelect:hover, QComboBox:hover {{ border-color: {ink}; }}
AkSelect:focus, QComboBox:focus {{ border: 2px solid {ink}; }}
AkSelect:disabled, QComboBox:disabled {{
    color: {text_mut};
    background-color: {surface_2};
    border-color: {border};
}}
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
    padding: 4px;
}}

/* Hide native checkbox/radio indicators — custom paintEvent owns them */
AkCheckbox::indicator, AkRadio::indicator {{
    width: 0;
    height: 0;
    border: none;
    background: transparent;
}}

/* ========== Badge ========== */
AkBadge, QFrame#AkBadge {{
    background-color: {surface};
    border: {bw}px solid {border_s};
    border-radius: {r.pill}px;
}}
AkBadge QLabel, QFrame#AkBadge QLabel {{
    font-family: {ty.family_mono};
    font-size: {fs["2xs"]}px;
    font-weight: 500;
    letter-spacing: {ty.tracking_label};
    color: {text_sec};
    background: transparent;
}}
AkBadge[variant="solid"], QFrame#AkBadge[variant="solid"] {{
    background-color: {ink};
    border-color: {ink};
}}
AkBadge[variant="solid"] QLabel, QFrame#AkBadge[variant="solid"] QLabel {{
    color: {inv_text};
}}

/* ========== Alert ========== */
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
AkAlert[variant="solid"] QLabel#akAlertText {{
    color: {inv_text};
}}

/* ========== Tabs ========== */
AkTabs, QFrame#AkTabs {{ background: transparent; border: none; }}
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
    padding: 12px 16px;
    min-height: 44px;
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

/* ========== Accordion ========== */
AkAccordion {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
QFrame#akAccordionItem {{ background: transparent; border: none; }}
QFrame#akAccordionItem[divided="true"] {{
    border-top: {bw}px solid {border};
}}
QPushButton#akAccordionTrigger {{
    background-color: {bg};
    color: {ink};
    border: none;
    border-radius: 0;
    text-align: left;
    padding: 0;
}}
QPushButton#akAccordionTrigger:hover {{ background-color: {surface}; }}
QLabel#akAccordionTitle {{
    font-size: {fs["sm"]}px;
    font-weight: 500;
    color: {ink};
    background: transparent;
}}
QLabel#akAccordionChevron {{
    font-size: {fs["sm"]}px;
    color: {text_mut};
    background: transparent;
}}
QLabel#akAccordionChevron[expanded="true"] {{ color: {ink}; }}
QLabel#akAccordionPanel {{
    color: {text_sec};
    font-size: {fs["sm"]}px;
    background: transparent;
    padding: 0 {s[5]}px {s[5]}px {s[5]}px;
}}

/* ========== Breadcrumb ========== */
AkBreadcrumb {{ background: transparent; border: none; }}
QPushButton#akBreadcrumbLink {{
    background: transparent;
    color: {text_sec};
    border: none;
    padding: 2px 4px;
    font-size: {fs["sm"]}px;
}}
QPushButton#akBreadcrumbLink:hover {{ color: {ink}; }}
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

/* ========== Pagination ========== */
AkPagination {{ background: transparent; border: none; }}
QPushButton#akPageBtn {{
    background: transparent;
    color: {text_sec};
    border: 2px solid transparent;
    border-radius: {r.md}px;
    min-width: {page_btn}px;
    min-height: {page_btn}px;
    padding: 0 {s[2]}px;
    font-family: {ty.family_ui};
    font-size: {fs["sm"]}px;
    font-weight: 500;
}}
QPushButton#akPageBtn:hover {{
    background-color: {surface};
    color: {text};
}}
QPushButton#akPageBtn:checked {{
    border: 2px solid {ink};
    color: {ink};
    background-color: {bg};
}}
QPushButton#akPageBtn:disabled {{
    color: {text_mut};
    background: transparent;
}}
QPushButton#akPageBtn:focus {{ border: 2px solid {ink}; }}

/* ========== Table ========== */
QFrame#AkTableWrap, AkTable {{
    background-color: {bg};
    border: {bw}px solid {border};
    border-radius: {r.lg}px;
}}
QTableWidget#AkTable, AkTable QTableWidget {{
    background-color: {bg};
    color: {text};
    border: none;
    gridline-color: transparent;
    font-size: {fs["sm"]}px;
    outline: none;
    selection-background-color: {surface};
    selection-color: {ink};
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
QTableCornerButton::section {{
    background: {bg};
    border: none;
}}

/* ========== Empty (start-aligned by default) ========== */
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
    font-size: {fs["xl"]}px;
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

/* ========== Modal ========== */
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
QFrame#akModalBody {{ background: transparent; border: none; }}

/* Pattern block title */
QLabel#akPatternTitle {{
    font-family: {ty.family_mono};
    font-size: {fs["xs"]}px;
    letter-spacing: {ty.tracking_label};
    text-transform: uppercase;
    color: {text_mut};
    padding-bottom: {s[3]}px;
    border-bottom: {bw}px solid {border};
    margin-bottom: {s[2]}px;
}}

/* Scrollbar */
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

QSizeGrip {{ background: transparent; width: 16px; height: 16px; }}
"""


def apply(widget: QWidget) -> None:
    """Apply generated QSS and muted placeholder palette to *widget*."""
    from PyQt6.QtWidgets import QWidget as _QW

    widget.setStyleSheet(build())
    _apply_placeholder_palette(widget)
    # Custom-painted widgets need a full update after theme change
    widget.update()
    for child in widget.findChildren(_QW):
        child.update()


def _apply_placeholder_palette(root: QWidget) -> None:
    try:
        from PyQt6.QtGui import QColor, QPalette
        from PyQt6.QtWidgets import QLineEdit, QPlainTextEdit, QTextEdit
    except Exception:
        return

    muted = QColor(get_theme().get("text_muted", "#8a8a8a"))
    for cls in (QLineEdit, QPlainTextEdit, QTextEdit):
        for w in root.findChildren(cls):
            pal = w.palette()
            pal.setColor(QPalette.ColorRole.PlaceholderText, muted)
            w.setPalette(pal)
