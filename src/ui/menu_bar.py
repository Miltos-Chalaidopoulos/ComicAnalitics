from PySide6.QtWidgets import QMenuBar, QMessageBox, QFileDialog, QApplication
from PySide6.QtGui import QAction, QKeySequence, QDesktopServices
from PySide6.QtCore import QUrl
import shutil
from pathlib import Path

class MenuBarFactory:
    @staticmethod
    def create(main_window):
        menubar = QMenuBar(main_window)
        file_menu = menubar.addMenu("File")

        import_action = QAction("Import from CSV", main_window)
        import_action.setShortcut(QKeySequence.Open)
        import_action.triggered.connect(main_window.import_csv)
        file_menu.addAction(import_action)

        export_action = QAction("Export to CSV", main_window)
        export_action.setShortcut(QKeySequence.Save)
        export_action.triggered.connect(main_window.export_csv)
        file_menu.addAction(export_action)

        search_action = QAction("Search", main_window)
        search_action.setShortcut(QKeySequence.Find)
        search_action.triggered.connect(main_window.open_search_dialog)
        file_menu.addAction(search_action)

        file_menu.addSeparator()

        reset_db_action = QAction("Reset Database", main_window)
        reset_db_action.setShortcut("Ctrl+R")
        def reset_db():
            reply = QMessageBox.question(
                main_window,
                "Confirm Reset",
                "Are you sure you want to reset the database? This will delete all data!",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

            db_path = main_window.db.db_path
            main_window.db.close()
            if Path(db_path).exists():
                Path(db_path).unlink()

            from ..database.db_manager import DBManager
            main_window.db = DBManager(db_path)

            for tab in [main_window.mickey_tab, main_window.superheroes_tab, main_window.arkas_tab]:
                tab.db = main_window.db
                tab.refresh_table()

            QMessageBox.information(main_window, "Reset", "Database has been reset!")
        reset_db_action.triggered.connect(reset_db)
        file_menu.addAction(reset_db_action)

        backup_db_action = QAction("Backup Database", main_window)
        backup_db_action.setShortcut("Ctrl+B")
        def backup_db():
            target_file, _ = QFileDialog.getSaveFileName(main_window, "Backup Database As", "", "SQLite DB (*.db)")
            if not target_file:
                return
            main_window.db.conn.commit()
            shutil.copy(main_window.db.db_path, target_file)
            QMessageBox.information(main_window, "Backup", f"Database backed up to:\n{target_file}")
        backup_db_action.triggered.connect(backup_db)
        file_menu.addAction(backup_db_action)

        open_db_action = QAction("Open Database", main_window)
        open_db_action.setShortcut("Ctrl+D")
        def open_db():
            new_path, _ = QFileDialog.getOpenFileName(main_window, "Open Database", "", "SQLite DB (*.db)")
            if not new_path:
                return
            main_window.db.close()
            from ..database.db_manager import DBManager
            main_window.db = DBManager(new_path)
            for tab in [main_window.mickey_tab, main_window.superheroes_tab, main_window.arkas_tab]:
                tab.db = main_window.db
                tab.refresh_table()
            QMessageBox.information(main_window, "Database Opened", f"Database changed to:\n{new_path}")
        open_db_action.triggered.connect(open_db)
        file_menu.addAction(open_db_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", main_window)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(main_window.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")

        for name, shortcut in [("Undo", QKeySequence.Undo), ("Redo", QKeySequence.Redo),
                               ("Cut", QKeySequence.Cut), ("Copy", QKeySequence.Copy),
                               ("Paste", QKeySequence.Paste)]:
            action = QAction(name, main_window)
            action.setShortcut(shortcut)
            action.triggered.connect(lambda _, n=name: QMessageBox.information(main_window, "Info", f"{n} not implemented yet"))
            edit_menu.addAction(action)

        edit_menu.addSeparator()
        preferences_action = QAction("Toggle Dark/Light Mode", main_window)
        def toggle_theme():
            app = QApplication.instance()
            if not hasattr(main_window, "dark_mode"):
                main_window.dark_mode = True

            if main_window.dark_mode:
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
                main_window.dark_mode = False
            else:
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
                main_window.dark_mode = True

        preferences_action.triggered.connect(toggle_theme)
        edit_menu.addAction(preferences_action)
        help_menu = menubar.addMenu("Help")

        user_guide_action = QAction("User Guide", main_window)
        user_guide_action.setShortcut("F1")
        user_guide_action.triggered.connect(
            lambda: QMessageBox.information(
                main_window,
                "User Guide",
                "📖 Comics Analytics User Guide\n\n"
                "• Reset , Open and Backup database are still experimental, use with caution.\n"
                "• Mickey csv files should start with Issue num,Vol num,Main Story,Year\n"
                "• Superhero csv files should start with Title,Writer,Artist,Collection,Publisher,Issues,Main Character,Event,Story Year,Category\n"
                "• Arkas csv files should start with Story Name,Series Name,Year\n"
            )
        )
        help_menu.addAction(user_guide_action)

        report_bug_action = QAction("Report Bug", main_window)
        def open_bug_report():
            url = "https://github.com/Miltos-Chalaidopoulos/ComicAnalitics/issues"
            QDesktopServices.openUrl(QUrl(url))
        report_bug_action.triggered.connect(open_bug_report)
        help_menu.addAction(report_bug_action)

        about_action = QAction("About", main_window)
        about_action.triggered.connect(main_window.show_about)
        help_menu.addAction(about_action)

        return menubar
