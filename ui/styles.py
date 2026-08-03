"""
Zorin OS / Fluent Design inspired stylesheets for FlowMate.
"""

DARK_THEME = """
/* Global Base */
QMainWindow, QDialog {
    background-color: #0F172A;
    color: #F8FAFC;
}

QWidget {
    font-family: 'Segoe UI', Inter, -apple-system, sans-serif;
    font-size: 13px;
    color: #CBD5E1;
}

/* Sidebar styling */
#Sidebar {
    background-color: #090D16;
    border-right: 1px solid #1E293B;
}

#SidebarNavButton {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
    font-weight: 600;
}

#SidebarNavButton:hover {
    background-color: #1E293B;
    color: #F8FAFC;
}

#SidebarNavButton:checked {
    background-color: #3B82F6;
    color: #FFFFFF;
}

/* Card Widget Container */
.CardWidget {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
}

/* Stat Cards */
#StatCard {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
}

#StatValue {
    font-size: 26px;
    font-weight: 800;
    color: #38BDF8;
}

#StatLabel {
    font-size: 12px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Headings */
QLabel#HeaderTitle {
    font-size: 22px;
    font-weight: 700;
    color: #F8FAFC;
}

QLabel#SectionTitle {
    font-size: 16px;
    font-weight: 700;
    color: #38BDF8;
}

/* Buttons */
QPushButton {
    background-color: #3B82F6;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #2563EB;
}

QPushButton:pressed {
    background-color: #1D4ED8;
}

QPushButton:disabled {
    background-color: #334155;
    color: #64748B;
}

QPushButton#btnPrimary {
    background-color: #10B981;
}

QPushButton#btnPrimary:hover {
    background-color: #059669;
}

QPushButton#btnDanger {
    background-color: #EF4444;
}

QPushButton#btnDanger:hover {
    background-color: #DC2626;
}

QPushButton#btnSecondary {
    background-color: #334155;
    color: #F8FAFC;
}

QPushButton#btnSecondary:hover {
    background-color: #475569;
}

/* Inputs & Form Controls */
QLineEdit, QComboBox, QSpinBox {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
    selection-background-color: #3B82F6;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #38BDF8;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

/* Table Widget */
QTableWidget {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: #1E293B;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #1E293B;
}

QTableWidget::item:selected {
    background-color: #1E293B;
    color: #38BDF8;
}

QHeaderView::section {
    background-color: #1E293B;
    color: #94A3B8;
    font-weight: 700;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #334155;
}

/* Status Badges */
#StatusBadgeWatching {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10B981;
    border: 1px solid #10B981;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 700;
}

#StatusBadgeStopped {
    background-color: rgba(239, 68, 68, 0.15);
    color: #EF4444;
    border: 1px solid #EF4444;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 700;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #0F172A;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #334155;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

LIGHT_THEME = """
QMainWindow, QDialog {
    background-color: #F8FAFC;
    color: #0F172A;
}

QWidget {
    font-family: 'Segoe UI', Inter, -apple-system, sans-serif;
    font-size: 13px;
    color: #334155;
}

#Sidebar {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

#SidebarNavButton {
    background-color: transparent;
    color: #64748B;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
    font-weight: 600;
}

#SidebarNavButton:hover {
    background-color: #F1F5F9;
    color: #0F172A;
}

#SidebarNavButton:checked {
    background-color: #2563EB;
    color: #FFFFFF;
}

.CardWidget, #StatCard {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

#StatValue {
    font-size: 26px;
    font-weight: 800;
    color: #2563EB;
}

#StatLabel {
    font-size: 12px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
}

QLabel#HeaderTitle {
    font-size: 22px;
    font-weight: 700;
    color: #0F172A;
}

QLabel#SectionTitle {
    font-size: 16px;
    font-weight: 700;
    color: #2563EB;
}

QPushButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1D4ED8;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 12px;
    color: #0F172A;
}

QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
}

QHeaderView::section {
    background-color: #F1F5F9;
    color: #475569;
    font-weight: 700;
    padding: 10px;
}

#StatusBadgeWatching {
    background-color: #DCFCE7;
    color: #15803D;
    border: 1px solid #86EFAC;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 700;
}

#StatusBadgeStopped {
    background-color: #FEE2E2;
    color: #B91C1C;
    border: 1px solid #FCA5A5;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 700;
}
"""
