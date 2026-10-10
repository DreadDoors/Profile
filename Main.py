"""
MPHEAW - Multi-Process Helping-Engine and Writer
Main.py  ->  Entry point. Run THIS file to start the application.

It creates the QApplication, builds the main window (defined in GUI/App.py),
shows it, and starts the Qt event loop.
"""

import sys

from PySide6.QtWidgets import QApplication

from GUI.App import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()