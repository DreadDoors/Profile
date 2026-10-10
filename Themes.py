import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, 
    QComboBox, QLabel, QGroupBox, QDialog
)
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QColor


class ThemeFormula:
    """Mathematical color calculator for dynamic palettes."""
    
    def __init__(self, name, mode, base_hue=0.0, base_sat=0.0, base_val=0.5, is_default=False):
        self.name = name
        self.mode = mode  # 'darker', 'lighter', or 'default'
        self.base_hue = base_hue  # 0.0 to 1.0 (HSV Hue)
        self.base_sat = base_sat  # 0.0 to 1.0
        self.base_val = base_val  # 0.0 to 1.0
        self.is_default = is_default

    def compute_color(self, index: int) -> str:
        if self.is_default:
            return ""  # Native OS/system colors

        # Step factor normalizes index 'i' across a 0 to 100 percentage scale
        step = min(max(index, 0), 100) / 100.0

        if self.mode == 'darker':
            # Higher i (0-100%) -> Darker shade (Light Themes)
            hue = self.base_hue
            sat = min(1.0, self.base_sat + (step * 0.2))
            val = max(0.0, self.base_val - step)

        elif self.mode == 'lighter':
            # Higher i (0-100%) -> Lighter shade (Dark Themes)
            hue = self.base_hue
            sat = self.base_sat
            val = min(1.0, self.base_val + step)

        else:
            hue, sat, val = 0.0, 0.0, 0.5

        color = QColor()
        color.setHsvF(hue, sat, val)
        return color.name()


class DynamicThemeArray:
    """Calculates ThemeColor[i] dynamically on demand without pre-storing."""
    
    def __init__(self):
        # Dictionary sorted specifically:
        # Defaults -> Bright Primary (RGB) -> Bright Secondary -> Dark Primary (RGB) -> Dark Secondary
        self._themes = {
            # 1. Defaults
            "Default Mode": ThemeFormula("Default Mode", mode="default", is_default=True),
            "Default Light Mode": ThemeFormula("Default Light Mode", mode="darker", base_hue=0.6, base_sat=0.05, base_val=0.95),
            "Default Dark Mode": ThemeFormula("Default Dark Mode", mode="lighter", base_hue=0.6, base_sat=0.1, base_val=0.12),
            
            # 2. Bright Themes
            "Bright White": ThemeFormula("Bright White", mode="darker", base_hue=0.0, base_sat=0.0, base_val=1.0),
            # Bright Primary (Red -> Green -> Blue)
            "Bright Red": ThemeFormula("Bright Red", mode="darker", base_hue=0.0, base_sat=1.0, base_val=1.0),
            "Bright Green": ThemeFormula("Bright Green", mode="darker", base_hue=0.333, base_sat=1.0, base_val=1.0),
            "Bright Blue": ThemeFormula("Bright Blue", mode="darker", base_hue=0.666, base_sat=1.0, base_val=1.0),
            # Bright Secondary (Yellow -> Magenta -> Cyan)
            "Bright Yellow": ThemeFormula("Bright Yellow", mode="darker", base_hue=0.166, base_sat=1.0, base_val=1.0),
            "Bright Magenta": ThemeFormula("Bright Magenta", mode="darker", base_hue=0.833, base_sat=1.0, base_val=1.0),
            "Bright Cyan": ThemeFormula("Bright Cyan", mode="darker", base_hue=0.5, base_sat=1.0, base_val=1.0),
            
            # 3. Dark Themes
            "Dark Black": ThemeFormula("Dark Black", mode="lighter", base_hue=0.0, base_sat=0.0, base_val=0.0),
            # Dark Primary (Red -> Green -> Blue)
            "Dark Red": ThemeFormula("Dark Red", mode="lighter", base_hue=0.0, base_sat=1.0, base_val=0.067),
            "Dark Green": ThemeFormula("Dark Green", mode="lighter", base_hue=0.333, base_sat=1.0, base_val=0.067),
            "Dark Blue": ThemeFormula("Dark Blue", mode="lighter", base_hue=0.666, base_sat=1.0, base_val=0.067),
            # Dark Secondary (Yellow -> Magenta -> Cyan)
            "Dark Yellow": ThemeFormula("Dark Yellow", mode="lighter", base_hue=0.166, base_sat=1.0, base_val=0.067),
            "Dark Magenta": ThemeFormula("Dark Magenta", mode="lighter", base_hue=0.833, base_sat=1.0, base_val=0.067),
            "Dark Cyan": ThemeFormula("Dark Cyan", mode="lighter", base_hue=0.5, base_sat=1.0, base_val=0.067),
        }
        self.active_theme_name = "Default Light Mode"

    def set_theme(self, name: str):
        if name in self._themes:
            self.active_theme_name = name

    def get_theme_names(self):
        return list(self._themes.keys())

    def __getitem__(self, index: int) -> str:
        """Access ThemeColor[i] to dynamically retrieve hex string."""
        formula = self._themes[self.active_theme_name]
        return formula.compute_color(index)


class ThemeManagerNotifier(QObject):
    theme_changed = Signal()


# Global Instances
ThemeColor = DynamicThemeArray()
_notifier = ThemeManagerNotifier()


class ThemeSelectorDialog(QDialog):
    """Window created by 'W' mode."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Theme")
        self.resize(260, 130)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Choose Color Theme:"))

        self.combo = QComboBox()
        self.combo.addItems(ThemeColor.get_theme_names())
        self.combo.setCurrentText(ThemeColor.active_theme_name)
        self.combo.currentTextChanged.connect(self._on_theme_selected)
        layout.addWidget(self.combo)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def _on_theme_selected(self, name: str):
        ThemeColor.set_theme(name)
        _notifier.theme_changed.emit()


class ThemeInsertFactory:
    """Handles ThemeInsert['W'], ThemeInsert['S'], and ThemeInsert['D']."""

    def __getitem__(self, mode: str):
        mode = str(mode).upper()
        if mode == 'W':
            return self._create_window_button()
        elif mode == 'S':
            return self._create_section_widget()
        elif mode == 'D':
            return self._create_dark_light_toggle()
        else:
            raise ValueError(f"Invalid mode '{mode}'. Use 'W', 'S', or 'D'.")

    def _create_window_button(self) -> QPushButton:
        btn = QPushButton("Change Theme")

        def open_dialog():
            dlg = ThemeSelectorDialog(btn.window())
            dlg.exec()

        btn.clicked.connect(open_dialog)
        return btn

    def _create_section_widget(self) -> QGroupBox:
        group = QGroupBox("Theme Settings")
        layout = QVBoxLayout(group)

        combo = QComboBox()
        combo.addItems(ThemeColor.get_theme_names())
        combo.setCurrentText(ThemeColor.active_theme_name)

        def on_change(name):
            ThemeColor.set_theme(name)
            _notifier.theme_changed.emit()

        combo.currentTextChanged.connect(on_change)
        layout.addWidget(QLabel("Active Theme:"))
        layout.addWidget(combo)
        return group

    def _create_dark_light_toggle(self) -> QPushButton:
        btn = QPushButton("Toggle Light / Dark")

        def toggle():
            if "Dark" in ThemeColor.active_theme_name:
                ThemeColor.set_theme("Default Light Mode")
            else:
                ThemeColor.set_theme("Default Dark Mode")
            _notifier.theme_changed.emit()

        btn.clicked.connect(toggle)
        return btn


# Global exports
ThemeInsert = ThemeInsertFactory()
theme_notifier = _notifier