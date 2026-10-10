"""
MPHEAW - Multi-Process Helping-Engine and Writer
GUI/App.py  ->  Builds the main application window.

Front-end shell connected with dynamic theme script (GUI/Themes.py).
Run from Main.py.
"""

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Support running directly or from project root (python Main.py)
try:
    from GUI.Popups.Settings import SettingsDialog
    from GUI.Popups.Dialogue_Box import show_error
    from GUI.Themes import ThemeColor, ThemeInsert, theme_notifier
except ImportError:
    from Popups.Settings import SettingsDialog
    from Popups.Dialogue_Box import show_error
    from Themes import ThemeColor, ThemeInsert, theme_notifier

from Engines.Input import InputEngine, InputRequest
from Engines.Choice import ChoiceEngine
from Engines.Error import MPHEAWError

# Optional dependency, only needed for "Save As > Document (.docx)".
try:
    from docx import Document
except ImportError:
    Document = None


def _divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    return line


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MPHEAW - Multi-Process Helping-Engine and Writer")
        self.resize(860, 640)

        # Back-end engines
        self.input_engine = InputEngine()
        self.choice_engine = ChoiceEngine()

        self._build_menus()

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 16, 20, 18)
        root.setSpacing(10)

        # Title block
        title = QLabel("MPHEAW")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("Multi-Process Helping-Engine and Writer")
        subtitle.setObjectName("SubtitleLabel")
        root.addWidget(title)
        root.addWidget(subtitle)
        
        self.divider_line = _divider()
        root.addWidget(self.divider_line)

        # Tab strip
        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_numbers_tab(), "Numbers")
        root.addWidget(self.tabs)

        # Connect dynamic theme engine
        theme_notifier.theme_changed.connect(self.apply_styles)
        self.apply_styles()

    # ------------------------------------------------------------------ #
    # Menu bar
    # ------------------------------------------------------------------ #
    def _build_menus(self):
        menubar = self.menuBar()

        # File > Save As > Text / Document
        file_menu = menubar.addMenu("File")
        save_as = file_menu.addMenu("Save As")
        save_as.addAction("Text (.txt)", self._save_as_txt)
        save_as.addAction("Document (.docx)", self._save_as_docx)

        # Options > Shortcuts / Settings
        options_menu = menubar.addMenu("Options")
        shortcuts_menu = options_menu.addMenu("Shortcuts")
        placeholder = shortcuts_menu.addAction("(shortcuts coming soon)")
        placeholder.setEnabled(False)
        shortcuts_menu.addSeparator()
        shortcuts_menu.addAction(
            "More Shortcuts...", lambda: self._open_settings("Shortcuts")
        )
        options_menu.addAction("Settings", lambda: self._open_settings("General"))

    def _open_settings(self, section):
        dialog = SettingsDialog(self, initial_section=section)
        dialog.exec()

    # ------------------------------------------------------------------ #
    # Dynamic Styling (Themes.py Integration)
    # ------------------------------------------------------------------ #
    def apply_styles(self):
        bg_color = ThemeColor[1]
        card_color = ThemeColor[5]
        accent_color = ThemeColor[15]
        text_color = ThemeColor[100]

        dynamic_stylesheet = f"""
        QMainWindow, QWidget {{
            background-color: {bg_color};
            color: {text_color};
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 14px;
        }}
        QMenuBar {{
            background-color: {card_color};
            color: {text_color};
            border-bottom: 1px solid {text_color};
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
        }}
        QMenuBar::item:selected {{
            background-color: {accent_color};
        }}
        QMenu {{
            background-color: {card_color};
            color: {text_color};
            border: 1px solid {text_color};
        }}
        QMenu::item:selected {{
            background-color: {accent_color};
        }}
        #TitleLabel {{
            font-size: 22px;
            font-weight: 700;
            color: {text_color};
        }}
        #SubtitleLabel {{
            font-size: 12px;
            color: {text_color};
        }}
        #SectionTitle {{
            font-size: 15px;
            font-weight: 700;
            color: {text_color};
        }}
        #GroupHeader {{
            font-size: 13px;
            font-weight: 700;
            color: {text_color};
            margin-top: 6px;
        }}
        #GroupHeaderSoon {{
            font-size: 13px;
            font-weight: 700;
            color: {text_color};
            margin-top: 6px;
        }}
        #SoonNote {{
            font-size: 11px;
            color: {text_color};
            font-style: italic;
        }}
        QTabWidget::pane {{
            border: 1px solid {text_color};
            border-radius: 8px;
            background: {bg_color};
            top: -1px;
        }}
        QTabBar::tab {{
            background: {card_color};
            color: {text_color};
            padding: 7px 20px;
            border: 1px solid {text_color};
            border-bottom: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background: {bg_color};
            color: {text_color};
            font-weight: 600;
        }}
        QPlainTextEdit, QTextEdit {{
            background-color: {card_color};
            color: {text_color};
            border: 1px solid {text_color};
            border-radius: 8px;
            padding: 8px;
        }}
        QCheckBox {{
            padding: 3px 0;
            color: {text_color};
        }}
        QPushButton {{
            background-color: {accent_color};
            color: {text_color};
            border: 1px solid {text_color};
            border-radius: 8px;
            padding: 9px 22px;
            font-weight: 600;
        }}
        QPushButton#Secondary {{
            background-color: {card_color};
            color: {text_color};
            border: 1px solid {text_color};
        }}
        #Card {{
            background-color: {card_color};
            border: 1px solid {text_color};
            border-radius: 12px;
        }}
        """
        self.setStyleSheet(dynamic_stylesheet)
        self.divider_line.setStyleSheet(f"color: {text_color};")

    # ------------------------------------------------------------------ #
    # Numbers tab = input page <-> results page
    # ------------------------------------------------------------------ #
    def _build_numbers_tab(self):
        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setContentsMargins(12, 14, 12, 12)

        self.stack = QStackedWidget()
        self.input_page = self._build_input_page()
        self.results_page = self._build_results_page()
        self.stack.addWidget(self.input_page)
        self.stack.addWidget(self.results_page)
        lay.addWidget(self.stack)
        return container

    def _build_input_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        columns = QHBoxLayout()
        columns.setSpacing(16)

        # Left: number input
        left_card = QWidget()
        left_card.setObjectName("Card")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(14, 14, 14, 14)
        in_label = QLabel("Enter numbers  (separated by spaces or new lines)")
        in_label.setObjectName("GroupHeader")
        self.number_input = QPlainTextEdit()
        self.number_input.setPlaceholderText("5\n12\n7\n3")
        left_layout.addWidget(in_label)
        left_layout.addWidget(self.number_input)

        # Right: choices
        right_card = QWidget()
        right_card.setObjectName("Card")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(14, 14, 14, 14)
        right_layout.setSpacing(4)

        right_layout.addWidget(self._group_header("Arrangement"))
        self.cb_ascending = QCheckBox("Ascending Order")
        self.cb_descending = QCheckBox("Descending Order")
        right_layout.addWidget(self.cb_ascending)
        right_layout.addWidget(self.cb_descending)

        right_layout.addWidget(self._group_header("Stating"))
        self.cb_greatest = QCheckBox("Greatest Number")
        self.cb_smallest = QCheckBox("Smallest Number")
        right_layout.addWidget(self.cb_greatest)
        right_layout.addWidget(self.cb_smallest)

        for name in ("Solving", "Subset", "Specials"):
            right_layout.addWidget(self._group_header(name, coming_soon=True))
            note = QLabel("more coming soon")
            note.setObjectName("SoonNote")
            right_layout.addWidget(note)

        right_layout.addWidget(_divider())
        self.cb_all = QCheckBox("All  (select every available option)")
        right_layout.addWidget(self.cb_all)
        right_layout.addStretch(1)

        self._active_boxes = [
            self.cb_ascending,
            self.cb_descending,
            self.cb_greatest,
            self.cb_smallest,
        ]
        self.cb_all.toggled.connect(self._on_all_toggled)
        for box in self._active_boxes:
            box.toggled.connect(self._on_active_toggled)

        columns.addWidget(left_card, 1)
        columns.addWidget(right_card, 1)
        layout.addLayout(columns)

        bottom = QHBoxLayout()
        
        # Theme button placed on bottom bar
        self.theme_btn = ThemeInsert['W']
        bottom.addWidget(self.theme_btn)

        bottom.addStretch(1)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self._on_next)
        bottom.addWidget(self.next_button)
        layout.addLayout(bottom)

        return page

    def _group_header(self, text, coming_soon=False):
        label = QLabel(text)
        label.setObjectName("GroupHeaderSoon" if coming_soon else "GroupHeader")
        return label

    def _build_results_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel("Results")
        header.setObjectName("SectionTitle")
        layout.addWidget(header)

        self.results_view = QTextEdit()
        self.results_view.setReadOnly(True)
        layout.addWidget(self.results_view)

        bottom = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("Secondary")
        self.back_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.input_page)
        )
        bottom.addWidget(self.back_button)
        bottom.addStretch(1)
        layout.addLayout(bottom)
        return page

    # ------------------------------------------------------------------ #
    # Behaviour
    # ------------------------------------------------------------------ #
    def _on_all_toggled(self, checked):
        for box in self._active_boxes:
            box.blockSignals(True)
            box.setChecked(checked)
            box.blockSignals(False)

    def _on_active_toggled(self, _checked):
        all_on = all(box.isChecked() for box in self._active_boxes)
        self.cb_all.blockSignals(True)
        self.cb_all.setChecked(all_on)
        self.cb_all.blockSignals(False)

    def _on_next(self):
        mode = self.tabs.tabText(self.tabs.currentIndex()).lower()
        selected = [b.text() for b in self._active_boxes if b.isChecked()]
        request = InputRequest(
            raw_text=self.number_input.toPlainText(),
            mode=mode,
            choices=selected,
        )
        result = self.input_engine.process(request)

        try:
            outcome = self.choice_engine.route(result)
        except MPHEAWError as err:
            show_error(self, err.title, err.message)
            return

        self.results_view.setPlainText(self._format_results(outcome))
        self.stack.setCurrentWidget(self.results_page)

    @staticmethod
    def _format_results(outcome):
        results = outcome["results"]
        numbers = outcome["numbers"]
        ignored = outcome["ignored"]

        lines = ["Numbers used:  " + ", ".join(str(n) for n in numbers)]
        if ignored:
            lines.append("Ignored (not whole numbers):  " + ", ".join(ignored))
        lines.append("")

        if not results:
            lines.append("(No results - the selected options aren't built yet.)")
        for choice, value in results.items():
            if isinstance(value, list):
                lines.append(f"{choice}:  " + ", ".join(str(v) for v in value))
            else:
                lines.append(f"{choice}:  {value}")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    # Save As
    # ------------------------------------------------------------------ #
    def _save_as_txt(self):
        text = self.results_view.toPlainText()
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Result as Text", "result.txt", "Text Files (*.txt)"
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def _save_as_docx(self):
        if Document is None:
            QMessageBox.warning(
                self,
                "python-docx not installed",
                "Saving as .docx needs the python-docx package.\n\n"
                "Install it with:\n    pip install python-docx",
            )
            return
        text = self.results_view.toPlainText()
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Result as Document", "result.docx", "Word Documents (*.docx)"
        )
        if not path:
            return
        doc = Document()
        for line in text.split("\n"):
            doc.add_paragraph(line)
        doc.save(path)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())