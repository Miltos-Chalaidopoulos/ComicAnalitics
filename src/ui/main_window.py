from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QFileDialog, QApplication, QDialog,
    QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QTextEdit
)
from PySide6.QtGui import QAction, QKeySequence, QDesktopServices
from PySide6.QtCore import Qt, QUrl
import shutil
from pathlib import Path

from .mickey_tab import MickeyTab
from .superheroes_tab import SuperheroesTab
from .arkas_tab import ArkasTab
from ..database.db_manager import DBManager
from ..services.csv_edit import CSVService
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

        self.mickey_tab = MickeyTab(self.db, main_window=self)
        self.superheroes_tab = SuperheroesTab(self.db, main_window=self)
        self.arkas_tab = ArkasTab(self.db, main_window=self)

        self.tabs.addTab(self.mickey_tab, "Mickey Comics")
        self.tabs.addTab(self.superheroes_tab, "Superhero Comics")
        self.tabs.addTab(self.arkas_tab, "Arkas Comics")

        self.setMenuBar(self.create_menu_bar())

    # -------------------- Theme-aware dialogs --------------------
    def show_user_guide_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("User Guide")
        dlg.setMinimumSize(500, 400)
        layout = QVBoxLayout(dlg)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll_layout = QVBoxLayout(content)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setPlainText(
            "📖 Comics Analytics User Guide\n\n"
            "• Reset , Open and Backup database are still experimental, use with caution.\n"
            "• Mickey csv files should start with Issue num,Vol num,Main Story,Year\n"
            "• Superhero csv files should start with Title,Writer,Artist,Collection,Publisher,Issues,Main Character,Event,Story Year,Category\n"
            "• Arkas csv files should start with Story Name,Series Name,Year\n"
            "• First Superhero entry should be imported from csv"
        )
        scroll_layout.addWidget(text)
        content.setLayout(scroll_layout)
        scroll.setWidget(content)

        layout.addWidget(scroll)

        if self.dark_mode:
            dlg.setStyleSheet("""
                QDialog { background-color: #2b2b2b; }
                QTextEdit { background-color: #1e1e1e; color: #dddddd; border: 1px solid #444444; }
            """)
        else:
            dlg.setStyleSheet("""
                QDialog { background-color: #f0f0f0; }
                QTextEdit { background-color: #ffffff; color: #000000; border: 1px solid #aaa; }
            """)

        dlg.exec()

    def show_about_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About")
        dlg.setMinimumSize(300, 150)
        layout = QVBoxLayout(dlg)

        label = QLabel("📚 Comics Analytics\nSimple app for managing comics")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dlg.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignCenter)

        if self.dark_mode:
            dlg.setStyleSheet("""
                QDialog { background-color: #2b2b2b; }
                QLabel { color: #dddddd; font-size: 14pt; }
                QPushButton { background-color: #3c3c3c; color: #ffffff; border-radius: 5px; padding: 5px 15px; }
                QPushButton:hover { background-color: #555555; }
            """)
        else:
            dlg.setStyleSheet("""
                QDialog { background-color: #f0f0f0; }
                QLabel { color: #000000; font-size: 14pt; }
                QPushButton { background-color: #dddddd; color: #000000; border-radius: 5px; padding: 5px 15px; }
                QPushButton:hover { background-color: #cccccc; }
            """)

        dlg.exec()

    # -------------------- Menu Bar --------------------
    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        import_action = QAction("Import from CSV", self)
        import_action.setShortcut(QKeySequence.Open)
        import_action.triggered.connect(self.import_csv)
        file_menu.addAction(import_action)

        export_action = QAction("Export to CSV", self)
        export_action.setShortcut(QKeySequence.Save)
        export_action.triggered.connect(self.export_csv)
        file_menu.addAction(export_action)

        search_action = QAction("Search", self)
        search_action.setShortcut(QKeySequence.Find)
        search_action.triggered.connect(self.open_search_dialog)
        file_menu.addAction(search_action)

        file_menu.addSeparator()

        # Reset Database
        reset_db_action = QAction("Reset Database", self)
        reset_db_action.setShortcut("Ctrl+R")
        def reset_db():
            from PySide6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self,
                "Confirm Reset",
                "Are you sure you want to reset the database? This will delete all data!",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
            db_path = self.db.db_path
            self.db.close()
            if Path(db_path).exists():
                Path(db_path).unlink()
            self.db = DBManager(db_path)
            for tab in [self.mickey_tab, self.superheroes_tab, self.arkas_tab]:
                tab.db = self.db
                if hasattr(tab, "refresh_table"):
                    tab.refresh_table()
                else:
                    tab.refresh_categories()
            QMessageBox.information(self, "Reset", "Database has been reset!")
        reset_db_action.triggered.connect(reset_db)
        file_menu.addAction(reset_db_action)

        # Backup DB
        backup_db_action = QAction("Backup Database", self)
        backup_db_action.setShortcut("Ctrl+B")
        def backup_db():
            target_file, _ = QFileDialog.getSaveFileName(self, "Backup Database As", "", "SQLite DB (*.db)")
            if not target_file:
                return
            self.db.conn.commit()
            shutil.copy(self.db.db_path, target_file)
            QMessageBox.information(self, "Backup", f"Database backed up to:\n{target_file}")
        backup_db_action.triggered.connect(backup_db)
        file_menu.addAction(backup_db_action)

        # Open DB
        open_db_action = QAction("Open Database", self)
        open_db_action.setShortcut("Ctrl+D")
        def open_db():
            new_path, _ = QFileDialog.getOpenFileName(self, "Open Database", "", "SQLite DB (*.db)")
            if not new_path:
                return
            self.db.close()
            self.db = DBManager(new_path)
            for tab in [self.mickey_tab, self.superheroes_tab, self.arkas_tab]:
                tab.db = self.db
                if hasattr(tab, "refresh_table"):
                    tab.refresh_table()
                else:
                    tab.refresh_categories()
            QMessageBox.information(self, "Database Opened", f"Database changed to:\n{new_path}")
        open_db_action.triggered.connect(open_db)
        file_menu.addAction(open_db_action)

        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        for name, shortcut in [("Undo", QKeySequence.Undo), ("Redo", QKeySequence.Redo),
                               ("Cut", QKeySequence.Cut), ("Copy", QKeySequence.Copy),
                               ("Paste", QKeySequence.Paste)]:
            action = QAction(name, self)
            action.setShortcut(shortcut)
            action.triggered.connect(lambda _, n=name: QMessageBox.information(self, "Info", f"{n} not implemented yet"))
            edit_menu.addAction(action)
        edit_menu.addSeparator()

        preferences_action = QAction("Toggle Dark/Light Mode", self)
        preferences_action.triggered.connect(self.toggle_theme)
        edit_menu.addAction(preferences_action)

        # Help menu
        help_menu = menubar.addMenu("Help")
        user_guide_action = QAction("User Guide", self)
        user_guide_action.setShortcut("F1")
        user_guide_action.triggered.connect(self.show_user_guide_dialog)
        help_menu.addAction(user_guide_action)

        report_bug_action = QAction("Report Bug", self)
        report_bug_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/Miltos-Chalaidopoulos/ComicAnalitics/issues")))
        help_menu.addAction(report_bug_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        return menubar

    # -------------------- Theme Toggle --------------------
    def toggle_theme(self):
        app = QApplication.instance()
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            app.setStyleSheet("""
                QMainWindow { background-color: #2b2b2b; }
                QMenuBar { background-color: #1e1e1e; color: #ffffff; }
                QMenuBar::item:selected { background-color: #3c3c3c; }
                QMenu { background-color: #2b2b2b; color: #ffffff; }
                QMenu::item:selected { background-color: #3c3c3c; }
                QTabWidget::pane { border: 1px solid #444444; background: #2b2b2b; }
                QTabBar::tab { background: #2b2b2b; color: #ffffff; padding: 8px; border: 1px solid #444444; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; }
                QTabBar::tab:selected { background: #444444; }
                QLabel { color: #dddddd; }
                QPushButton { background-color: #3c3c3c; color: #ffffff; border-radius: 5px; padding: 5px 10px; }
                QPushButton:hover { background-color: #555555; }
                QLineEdit { background-color: #1e1e1e; color: #ffffff; border: 1px solid #444444; border-radius: 5px; padding: 4px; }
            """)
        else:
            app.setStyleSheet("""
                QMainWindow { background-color: #f0f0f0; }
                QMenuBar { background-color: #e0e0e0; color: #000000; }
                QMenuBar::item:selected { background-color: #cccccc; }
                QMenu { background-color: #f0f0f0; color: #000000; }
                QMenu::item:selected { background-color: #cccccc; }
                QTabWidget::pane { border: 1px solid #aaa; background: #f0f0f0; }
                QTabBar::tab { background: #e0e0e0; color: #000; padding: 8px; border: 1px solid #aaa; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; }
                QTabBar::tab:selected { background: #ffffff; }
                QLabel { color: #000000; }
                QPushButton { background-color: #dddddd; color: #000; border-radius: 5px; padding: 5px 10px; }
                QPushButton:hover { background-color: #cccccc; }
                QLineEdit { background-color: #ffffff; color: #000000; border: 1px solid #aaa; border-radius: 5px; padding: 4px; }
            """)

        self.mickey_tab.apply_theme_to_table()
        self.arkas_tab.apply_theme_to_table()
        for cat_table in self.superheroes_tab.category_tables.values():
            cat_table.apply_theme_to_table()

    # -------------------- CSV / Search Methods --------------------
    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
        table_type = self.csv_service.detect_csv_type(file_path)
        try:
            if table_type == "mickey":
                self.csv_service.import_mickey(file_path)
                self.mickey_tab.refresh_table()
            elif table_type == "superheroes":
                self.csv_service.import_superheroes(file_path)
                self.superheroes_tab.refresh_categories()
            elif table_type == "arkas":
                self.csv_service.import_arkas(file_path)
                self.arkas_tab.refresh_table()
            else:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Error", "Unknown CSV format!")
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
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
                self.csv_service.export_mickey(file_name, rows)
            elif current_tab == self.superheroes_tab:
                current_cat_widget = current_tab.tabs.currentWidget()
                category = current_tab.tabs.tabText(current_tab.tabs.currentIndex())
                rows = current_cat_widget.get_visible_rows()
                self.csv_service.export_superheroes_category(file_name, category, rows)
            elif current_tab == self.arkas_tab:
                rows = self.arkas_tab.get_visible_rows()
                self.csv_service.export_arkas(file_name, rows)
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Export failed: {e}")

    def open_search_dialog(self):
        dlg = SearchDialog(self.db, main_window=self)
        dlg.exec()

