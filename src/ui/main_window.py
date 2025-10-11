from PySide6.QtWidgets import QMainWindow, QTabWidget, QMessageBox, QFileDialog
from .mickey_tab import MickeyTab
from .superheroes_tab import SuperheroesTab
from .arkas_tab import ArkasTab
from ..database.db_manager import DBManager
from ..services.csv_edit import CSVService
from .menu_bar import MenuBarFactory
from .dialogs import SearchDialog



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = True
        self.setWindowTitle("Comics Manager")
        self.setGeometry(100, 100, 1000, 600)

        self.db = DBManager()
        self.csv_service = CSVService(self.db)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.mickey_tab = MickeyTab(self.db)
        self.superheroes_tab = SuperheroesTab(self.db)
        self.arkas_tab = ArkasTab(self.db)

        self.tabs.addTab(self.mickey_tab, "Mickey Comics")
        self.tabs.addTab(self.superheroes_tab, "Superheroes Comics")
        self.tabs.addTab(self.arkas_tab, "Arkas Comics")

        self.setMenuBar(MenuBarFactory.create(self))

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
        table_type = self.csv_service.detect_csv_type(file_path)
        try:
            if table_type == "mickey":
                self.csv_service.import_mickey(file_path)
                self.mickey_tab.refresh_table()
                QMessageBox.information(self, "Success", "Mickey CSV imported successfully!")

            elif table_type == "superheroes":
                self.csv_service.import_superheroes(file_path)
                self.superheroes_tab.refresh_table()
                QMessageBox.information(self, "Success", "Superheroes CSV imported successfully!")

            elif table_type == "arkas":
                self.csv_service.import_arkas(file_path)
                self.arkas_tab.refresh_table()
                QMessageBox.information(self, "Success", "Arkas CSV imported successfully!")

            else:
                QMessageBox.warning(self, "Error", "Unknown CSV format!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Import failed: {e}")


    def export_csv(self):
        current_tab = self.tabs.currentWidget()
        current_index = self.tabs.currentIndex()
        current_title = self.tabs.tabText(current_index)

        file_name, _ = QFileDialog.getSaveFileName(
            self, f"Export {current_title} to CSV", "", "CSV Files (*.csv)"
        )
        if not file_name:
            return

        if not file_name.lower().endswith(".csv"):
            file_name += ".csv"
        
        try:
            if current_tab == self.mickey_tab:
                rows = self.mickey_tab.get_visible_rows()
                self.csv_service.export_mickey(file_name,rows)
            elif current_tab == self.superheroes_tab:
                current_cat_widget = current_tab.tabs.currentWidget()
                category = current_tab.tabs.tabText(current_tab.tabs.currentIndex())
                rows = current_cat_widget.get_visible_rows()
                self.csv_service.export_superheroes_category(file_name, category,rows)
            elif current_tab == self.arkas_tab:
                rows = self.arkas_tab.get_visible_rows()
                self.csv_service.export_arkas(file_name,rows)

            QMessageBox.information(self, "Success", f"✅ Exported {current_title} to {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Export failed: {e}")

    def open_search_dialog(self):
        dlg = SearchDialog(self.db)
        dlg.exec()

    def show_about(self):
        QMessageBox.information(
            self,
            "About",
            "📚 Comics Analytics\nSimple app for managing comics")
