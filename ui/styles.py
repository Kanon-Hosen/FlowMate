"""
Professional Zorin OS / Modern Fluent Design Stylesheet for FlowMate.
"""

DARK_THEME = """
/* Global Base */
QMainWindow, QDialog {
    background-color: #0B0F19;
    color: #F8FAFC;
}

QWidget {
    font-family: "Ubuntu", "Inter", "Cantarell", "Fira Sans", "Segoe UI", sans-serif;
    font-size: 13px;
    color: #CBD5E1;
}

/* Sidebar styling */
#Sidebar {
    background-color: #070A11;
    border-right: 1px solid #1E293B;
}

#SidebarNavButton {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.3px;
}

#SidebarNavButton:hover {
    background-color: #1E293B;
    color: #F8FAFC;
}

#SidebarNavButton:checked {
    background-color: #6366F1;
    color: #FFFFFF;
    font-weight: 700;
}

/* Card Widget Containers */
.CardWidget {
    background-color: #131C2E;
    border: 1px solid #23324C;
    border-radius: 12px;
}

/* Stat Cards */
#StatCard {
    background-color: #131C2E;
    border: 1px solid #23324C;
    border-top: 3px solid #6366F1;
    border-radius: 12px;
}

#StatValue {
    font-size: 28px;
    font-weight: 800;
    color: #818CF8;
    letter-spacing: -0.5px;
}

#StatLabel {
    font-size: 11px;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* Headings */
QLabel#HeaderTitle {
    font-size: 24px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.3px;
}

QLabel#SectionTitle {
    font-size: 16px;
    font-weight: 700;
    color: #818CF8;
}

/* Base Buttons */
QPushButton {
    background-color: #6366F1;
    color: #FFFFFF;
    border: 1px solid #6366F1;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #4F46E5;
    border-color: #818CF8;
}

QPushButton:pressed {
    background-color: #4338CA;
}

QPushButton:disabled {
    background-color: #1E293B;
    color: #64748B;
    border-color: #1E293B;
}

/* Accent Buttons */
QPushButton#btnPrimary {
    background-color: #10B981;
    border-color: #10B981;
}

QPushButton#btnPrimary:hover {
    background-color: #059669;
    border-color: #34D399;
}

QPushButton#btnDanger {
    background-color: #F43F5E;
    border-color: #F43F5E;
}

QPushButton#btnDanger:hover {
    background-color: #E11D48;
    border-color: #FB7185;
}

QPushButton#btnSecondary {
    background-color: #1E293B;
    color: #F8FAFC;
    border: 1px solid #334155;
}

QPushButton#btnSecondary:hover {
    background-color: #334155;
    border-color: #475569;
}

/* Inputs & Form Controls */
QLineEdit, QComboBox, QSpinBox {
    background-color: #0B0F19;
    border: 1px solid #23324C;
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
    selection-background-color: #6366F1;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1.5px solid #6366F1;
    background-color: #0F172A;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

/* Table Widget */
QTableWidget {
    background-color: #0B0F19;
    border: 1px solid #23324C;
    border-radius: 8px;
    gridline-color: #1E293B;
    outline: none;
}

QTableWidget::item {
    padding: 10px 8px;
    border-bottom: 1px solid #1E293B;
}

QTableWidget::item:selected {
    background-color: #1E293B;
    color: #818CF8;
}

QHeaderView::section {
    background-color: #131C2E;
    color: #94A3B8;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 12px 10px;
    border: none;
    border-bottom: 2px solid #23324C;
}

/* Status Badges */
#StatusBadgeWatching {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(52, 211, 153, 0.4);
    border-radius: 12px;
    padding: 5px 14px;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.5px;
}

#StatusBadgeStopped {
    background-color: rgba(244, 63, 94, 0.15);
    color: #FB7185;
    border: 1px solid rgba(251, 113, 133, 0.4);
    border-radius: 12px;
    padding: 5px 14px;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.5px;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #0B0F19;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #23324C;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #334155;
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
    font-family: "Ubuntu", "Inter", "Cantarell", "Fira Sans", "Segoe UI", sans-serif;
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
    font-size: 13px;
    font-weight: 600;
}

#SidebarNavButton:hover {
    background-color: #F1F5F9;
    color: #0F172A;
}

#SidebarNavButton:checked {
    background-color: #4F46E5;
    color: #FFFFFF;
}

.CardWidget, #StatCard {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 3px solid #4F46E5;
    border-radius: 12px;
}

#StatValue {
    font-size: 28px;
    font-weight: 800;
    color: #4F46E5;
}

#StatLabel {
    font-size: 11px;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
}

QLabel#HeaderTitle {
    font-size: 24px;
    font-weight: 800;
    color: #0F172A;
}

QLabel#SectionTitle {
    font-size: 16px;
    font-weight: 700;
    color: #4F46E5;
}

QPushButton {
    background-color: #4F46E5;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #4338CA;
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
    padding: 5px 14px;
    font-weight: 700;
}

#StatusBadgeStopped {
    background-color: #FEE2E2;
    color: #B91C1C;
    border: 1px solid #FCA5A5;
    border-radius: 12px;
    padding: 5px 14px;
    font-weight: 700;
}
"""
