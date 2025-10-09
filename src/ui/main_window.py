from PySide6.QtWidgets import (QMainWindow,QMenuBar,QMenu,QWidget,QVBoxLayout,QLabel,QTabWidget,QMessageBox,)
from PySide6.QtGui import QAction

from .mickey_tab import MickeyTab
from .other_tab import OtherTab
from .dialogs import SearchDialog
from ..database.db_manager import DBManager
from ..services.csv_edit import CSVService


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comics Manager")
        self.setGeometry(100, 100, 1000, 600)

        self.db = DBManager()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(MickeyTab(self.db), "Mickey Comics")
        self.tabs.addTab(OtherTab(self.db), "Marvel Comics")

        self._create_menu_bar()

    def _create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        search_action = QAction("Search", self)
        search_action.triggered.connect(self.open_search_dialog)
        file_menu.addAction(search_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")
        preferences_action = QAction("Preferences", self)
        edit_menu.addAction(preferences_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def open_search_dialog(self):
        dialog = SearchDialog()
        if dialog.exec():
            query = dialog.search_input.text()
            QMessageBox.information(self, "Search", f"Search for: {query}")

    def show_about(self):
        QMessageBox.information(
            self, "About", "📚 Comics Analytics\n"
        )
