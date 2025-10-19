import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # default dark theme
    app.setStyleSheet("""
        QMainWindow { background-color: #2b2b2b; }
        QMenuBar { background-color: #1e1e1e; color: #ffffff; }
        QMenuBar::item:selected { background-color: #3c3c3c; }
        QMenu { background-color: #2b2b2b; color: #ffffff; }
        QMenu::item:selected { background-color: #3c3c3c; }
        QTabWidget::pane { border: 1px solid #444444; background: #2b2b2b; }
        QTabBar::tab { background: #2b2b2b; color: #ffffff; padding: 8px; border: 1px solid #444444; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; }
        QTabBar::tab:selected { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #444444, stop:1 #2b2b2b); }
        QLabel { color: #dddddd; }
        QPushButton { background-color: #3c3c3c; color: #ffffff; border-radius: 5px; padding: 5px 10px; }
        QPushButton:hover { background-color: #555555; }
        QLineEdit { background-color: #1e1e1e; color: #ffffff; border: 1px solid #444444; border-radius: 5px; padding: 4px; }
    """)

    window = MainWindow()
    window.dark_mode = True
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
