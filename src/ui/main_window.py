from PySide6.QtWidgets import (QMainWindow, QMenuBar, QMenu, QWidget,QVBoxLayout, QLabel, QTabWidget, QMessageBox,QFileDialog)
from PySide6.QtGui import QAction
from .mickey_tab import MickeyTab
from .other_tab import OtherTab
from ..database.db_manager import DBManager
from ..services.csv_edit import CSVService


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comics Manager")
        self.setGeometry(100, 100, 1000, 600)

        self.db = DBManager()
        self.csv_service = CSVService(self.db)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.mickey_tab = MickeyTab(self.db)
        self.other_tab = OtherTab(self.db)
        self.tabs.addTab(self.mickey_tab, "Mickey Comics")
        self.tabs.addTab(self.other_tab, "Marvel Comics")

        self._create_menu_bar()

    def _create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        import_action = QAction("📂 Import from CSV", self)
        import_action.triggered.connect(self.import_csv)
        file_menu.addAction(import_action)

        export_menu = QMenu("💾 Export to CSV", self)

        export_mickey = QAction("Mickey Comics", self)
        export_mickey.triggered.connect(self.export_mickey_csv)
        export_menu.addAction(export_mickey)

        export_other = QAction("Other Comics", self)
        export_other.triggered.connect(self.export_other_csv)
        export_menu.addAction(export_other)

        file_menu.addMenu(export_menu)

        search_action = QAction("🔍 Search", self)
        search_action.triggered.connect(self.open_search_dialog)
        file_menu.addAction(search_action)

        exit_action = QAction("❌ Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")
        preferences_action = QAction("Preferences", self)
        edit_menu.addAction(preferences_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            table_type = self.csv_service.detect_csv_type(file_path)
            if table_type == "mickey":
                self.csv_service.import_mickey(file_path)
                self.mickey_tab.refresh_table()
                QMessageBox.information(self, "Success", "Mickey CSV imported successfully!")
            elif table_type == "other":
                self.csv_service.import_other(file_path)
                self.other_tab.refresh_table()
                QMessageBox.information(self, "Success", "Other CSV imported successfully!")
            else:
                QMessageBox.warning(self, "Error", "Unknown CSV format!")

    def export_mickey_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Mickey CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.csv_service.export_mickey(file_path)
            QMessageBox.information(self, "Success", "Mickey CSV exported successfully!")

    def export_other_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Other CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.csv_service.export_other(file_path)
            QMessageBox.information(self, "Success", "Other CSV exported successfully!")

    def open_search_dialog(self):
        self.mickey_tab.search_mickey_comics()

    def show_about(self):
        QMessageBox.information(
            self, "About", "📚 Comics Analytics\n"
        )
