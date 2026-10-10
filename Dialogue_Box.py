"""
MPHEAW - GUI/Popups/Dialogue_Box.py

Shows popup dialogs. DISPLAY ONLY -- it holds no error definitions or message
text of its own. The GUI catches an error (defined in Engines/Error.py) and
passes its title + message here to be shown.
"""

from PySide6.QtWidgets import QMessageBox


def show_error(parent, title, message):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Critical)
    box.setWindowTitle(title)
    box.setText(message)
    box.exec()
