from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QGroupBox, QMessageBox,
    QDialog, QScrollArea, QTextEdit, QHeaderView
)
from PySide6.QtCore import Qt
from ..database.db_manager import DBManager
from .dialogs import AddMickeyDialog


class MickeyTab(QWidget):
    def __init__(self, db: DBManager, main_window=None):
        super().__init__()
        self.db = db
        self.main_window = main_window

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Filters ---
        self.filter_box = QGroupBox("Filters")
        filter_layout = QVBoxLayout()
        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        self.issue_input = QLineEdit(); self.issue_input.setPlaceholderText("Issue #")
        self.vol_input = QLineEdit(); self.vol_input.setPlaceholderText("Vol #")
        self.mainstory_input = QLineEdit(); self.mainstory_input.setPlaceholderText("Main Story")
        self.year_input = QLineEdit(); self.year_input.setPlaceholderText("Year")

        for lbl_text, le in [("Issue", self.issue_input), ("Vol", self.vol_input),
                             ("Story", self.mainstory_input), ("Year", self.year_input)]:
            top_row.addWidget(QLabel(lbl_text))
            top_row.addWidget(le)

        self.year_range_input = QLineEdit(); self.year_range_input.setPlaceholderText("e.g. 2000-2005")
        self.issue_range_input = QLineEdit(); self.issue_range_input.setPlaceholderText("e.g. 10-20")
        self.exclude_range_input = QLineEdit(); self.exclude_range_input.setPlaceholderText("e.g. 15-19")

        for lbl_text, le in [("Year Range", self.year_range_input),
                             ("Issue Range", self.issue_range_input),
                             ("Missing Issues (range)", self.exclude_range_input)]:
            bottom_row.addWidget(QLabel(lbl_text))
            bottom_row.addWidget(le)

        filter_layout.addLayout(top_row)
        filter_layout.addLayout(bottom_row)

        btn_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply Filters")
        clear_btn = QPushButton("Clear Filters")
        apply_btn.clicked.connect(self.apply_filters)
        clear_btn.clicked.connect(self.clear_filters)
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        filter_layout.addLayout(btn_layout)

        self.filter_box.setLayout(filter_layout)
        layout.addWidget(self.filter_box)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["#", "Issue num", "Vol num", "Main Story", "Year"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.table)

        # --- Bottom Buttons ---
        bottom_btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Mickey Comic")
        add_btn.clicked.connect(self.add_mickey_comic)
        del_btn = QPushButton("🗑️ Delete Selected")
        del_btn.clicked.connect(self.delete_selected)
        bottom_btn_layout.addWidget(add_btn)
        bottom_btn_layout.addWidget(del_btn)
        layout.addLayout(bottom_btn_layout)

        self.refresh_table()

    # ----------------- Core -----------------
    def refresh_positions(self):
        for i in range(self.table.rowCount()):
            idx_item = QTableWidgetItem()
            idx_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            idx_item.setData(Qt.DisplayRole, i + 1)
            self.table.setItem(i, 0, idx_item)

    def refresh_table(self):
        rows = self.db.search_mickey()
        self.populate_table(rows)

    def populate_table(self, rows):
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            self.table.setItem(i, 1, QTableWidgetItem(str(row["issue_num"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row["vol_num"])))
            self.table.setItem(i, 3, QTableWidgetItem(row["mainstory"]))
            self.table.setItem(i, 4, QTableWidgetItem(str(row["year"])))

        self.table.blockSignals(False)
        self.refresh_positions()
        self.apply_theme_to_table()
        self.table.setSortingEnabled(True)

    # ----------------- Theme -----------------
    def apply_theme_to_table(self):
        if not self.main_window:
            return
        dark = self.main_window.dark_mode
        if dark:
            style = """
            QTableWidget {
                background-color: #1e1e1e;
                alternate-background-color: #2b2b2b;
                color: #ffffff;
                gridline-color: #3a3a3a;
                selection-background-color: #555555;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #dddddd;
                padding: 4px;
                border: 1px solid #3a3a3a;
            }
            """
        else:
            style = """
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f5f5f5;
                color: #000000;
                gridline-color: #cccccc;
                selection-background-color: #cce7ff;
                selection-color: #000000;
            }
            QHeaderView::section {
                background-color: #e6e6e6;
                color: #000000;
                padding: 4px;
                border: 1px solid #cccccc;
            }
            """
        self.table.setStyleSheet(style)

    # ----------------- DB Actions -----------------
    def add_mickey_comic(self):
        dialog = AddMickeyDialog(self.db, main_window=self.main_window)
        if dialog.exec():
            self.refresh_table()

    def delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            issue_num = int(self.table.item(row, 1).text())
            vol_num = int(self.table.item(row, 2).text())
            self.db.delete_mickey(issue_num, vol_num)
            QMessageBox.information(self, "Deleted", "Comic deleted successfully!")
            self.refresh_table()

    def on_item_changed(self, item):
        if item.column() == 0:
            return
        row = item.row()
        try:
            issue_num = int(self.table.item(row, 1).text())
            vol_num = int(self.table.item(row, 2).text())
            mainstory = self.table.item(row, 3).text()
            year = int(self.table.item(row, 4).text())
            self.db.update_mickey(issue_num, vol_num, mainstory, year)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update comic: {e}")

    # ----------------- Filters -----------------
    def apply_filters(self):
        kwargs = {}
        if self.issue_input.text():
            kwargs["issue_num"] = int(self.issue_input.text())
        if self.vol_input.text():
            kwargs["vol_num"] = int(self.vol_input.text())
        if self.mainstory_input.text():
            kwargs["mainstory"] = self.mainstory_input.text()
        if self.year_input.text():
            kwargs["year"] = int(self.year_input.text())
        if self.year_range_input.text():
            try:
                start, end = map(int, self.year_range_input.text().split("-"))
                kwargs["year_range"] = (start, end)
            except:
                QMessageBox.warning(self, "Error", "Invalid year range format (use start-end)")
                return
        if self.issue_range_input.text():
            try:
                start, end = map(int, self.issue_range_input.text().split("-"))
                kwargs["issue_range"] = (start, end)
            except:
                QMessageBox.warning(self, "Error", "Invalid issue range format (use start-end)")
                return
        if self.exclude_range_input.text():
            try:
                start, end = map(int, self.exclude_range_input.text().split("-"))
                missing = self.db.find_missing_issues(start, end, **kwargs)
                self.show_missing_dialog(missing)
                return
            except:
                QMessageBox.warning(self, "Error", "Invalid missing issues format (use start-end)")
                return

        results = self.db.advanced_search_mickey(**kwargs)
        self.populate_table(results)

    def show_missing_dialog(self, missing):
        dlg = QDialog(self)
        dlg.setWindowTitle("Missing Issues")
        dlg.setMinimumSize(400, 300)
        layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll_layout = QVBoxLayout()
        text = QTextEdit()
        text.setReadOnly(True)
        text.setPlainText(", ".join(map(str, missing)) if missing else "No missing issues found.")
        scroll_layout.addWidget(text)
        content.setLayout(scroll_layout)
        scroll.setWidget(content)

        layout.addWidget(scroll)
        dlg.setLayout(layout)
        dlg.exec()

    def clear_filters(self):
        self.issue_input.clear()
        self.vol_input.clear()
        self.mainstory_input.clear()
        self.year_input.clear()
        self.year_range_input.clear()
        self.issue_range_input.clear()
        self.exclude_range_input.clear()
        self.refresh_table()

    def get_visible_rows(self):
        rows = []
        for i in range(self.table.rowCount()):
            rows.append({
                "issue_num": int(self.table.item(i, 1).text()),
                "vol_num": int(self.table.item(i, 2).text()),
                "mainstory": self.table.item(i, 3).text(),
                "year": int(self.table.item(i, 4).text())
            })
        return rows
