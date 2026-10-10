"""
MPHEAW - GUI/Popups/Settings.py

The Settings popup window. It is a dialog with a left-hand sidebar listing
sections (General, Display, Personalize, Shortcuts) and a right-hand panel
that shows the selected section.

All sections are empty placeholders for now. The window can be opened pointing
at a specific section:
    SettingsDialog(parent, initial_section="General")     # from Options > Settings
    SettingsDialog(parent, initial_section="Shortcuts")   # from Options > Shortcuts > More Shortcuts
"""

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

SECTIONS = ["General", "Display", "Personalize", "Shortcuts"]

DIALOG_STYLE = """
QDialog {
    background-color: #f5f6f8;
}
QListWidget {
    background-color: #eceef3;
    border: none;
    border-right: 1px solid #e1e4ea;
    outline: 0;
    font-size: 14px;
    padding-top: 6px;
}
QListWidget::item {
    padding: 9px 14px;
    color: #4a5160;
}
QListWidget::item:selected {
    background-color: #2b3a67;
    color: #ffffff;
}
#SettingsHeader {
    font-size: 18px;
    font-weight: 700;
    color: #2b3a67;
}
#SettingsBody {
    font-size: 13px;
    color: #98a0ad;
    font-style: italic;
}
"""


class SettingsDialog(QDialog):
    def __init__(self, parent=None, initial_section="General"):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(580, 410)
        self.setStyleSheet(DIALOG_STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(160)
        for name in SECTIONS:
            self.sidebar.addItem(name)

        # Right-hand pages (one empty placeholder per section for now)
        self.pages = QStackedWidget()
        for name in SECTIONS:
            self.pages.addWidget(self._make_page(name))

        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        self.show_section(initial_section)

    def _make_page(self, name):
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(22, 20, 22, 20)
        header = QLabel(name)
        header.setObjectName("SettingsHeader")
        body = QLabel("Nothing here yet - coming soon.")
        body.setObjectName("SettingsBody")
        v.addWidget(header)
        v.addWidget(body)
        v.addStretch(1)
        return page

    def show_section(self, name):
        """Select and display a section by name."""
        if name in SECTIONS:
            index = SECTIONS.index(name)
            self.sidebar.setCurrentRow(index)
            self.pages.setCurrentIndex(index)
