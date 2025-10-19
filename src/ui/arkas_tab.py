from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from database.db_manager import DBManager
from ui.dialogs import AddArkasDialog
from services import filters


class ArkasTab(QWidget):
    def __init__(self, db: DBManager, main_window=None):
        super().__init__()
        self.db = db
        self.main_window = main_window

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.filter_box = QGroupBox("Filters")
        filter_layout = QHBoxLayout()

        self.story_input = QLineEdit()
        self.story_input.setPlaceholderText("Story Name")

        self.series_input = QLineEdit()
        self.series_input.setPlaceholderText("Series Name")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Year")

        self.year_range_input = QLineEdit()
        self.year_range_input.setPlaceholderText("e.g. 2000-2005")

        for label, widget in [
            ("Story", self.story_input),
            ("Series", self.series_input),
            ("Year", self.year_input),
            ("Year Range", self.year_range_input),
        ]:
            filter_layout.addWidget(QLabel(label))
            filter_layout.addWidget(widget)

        btn_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply Filters")
        clear_btn = QPushButton("Clear Filters")
        apply_btn.clicked.connect(self.apply_filters)
        clear_btn.clicked.connect(self.clear_filters)
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(clear_btn)

        filter_layout.addLayout(btn_layout)
        self.filter_box.setLayout(filter_layout)
        layout.addWidget(self.filter_box)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["#", "ID", "Story Name", "Series Name", "Year"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.table)

        bottom_btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Arkas Comic")
        add_btn.clicked.connect(self.add_arkas_comic)
        del_btn = QPushButton("🗑️ Delete Selected")
        del_btn.clicked.connect(self.delete_selected)
        bottom_btn_layout.addWidget(add_btn)
        bottom_btn_layout.addWidget(del_btn)
        layout.addLayout(bottom_btn_layout)

        self.refresh_table()

    def refresh_positions(self):
        for i in range(self.table.rowCount()):
            idx_item = QTableWidgetItem()
            idx_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            idx_item.setData(Qt.DisplayRole, i + 1)
            self.table.setItem(i, 0, idx_item)

    def refresh_table(self):
        rows = self.db.search_arkas()
        self.populate_table(rows)

    def populate_table(self, rows):
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        rows = [dict(row) for row in rows]
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            id_item = QTableWidgetItem(str(row.get("id", "")))
            id_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 1, id_item)

            self.table.setItem(i, 2, QTableWidgetItem(row.get("story_name", "")))
            self.table.setItem(i, 3, QTableWidgetItem(row.get("series_name", "")))
            year_item = QTableWidgetItem(str(row.get("year", "")))
            self.table.setItem(i, 4, year_item)

        self.table.blockSignals(False)
        self.refresh_positions()
        self.apply_theme_to_table()
        self.table.setSortingEnabled(True)
        self.table.hideColumn(1)

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

    def add_arkas_comic(self):
        dialog = AddArkasDialog(self.db, main_window=self.main_window)
        if dialog.exec():
            self.refresh_table()

    def delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            try:
                comic_id = int(self.table.item(row, 1).text())
                story_name = self.table.item(row, 2).text()
                self.db.delete_arkas(comic_id)
                QMessageBox.information(self, "Deleted", f"'{story_name}' deleted successfully!")
                self.refresh_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "No Selection", "Please select a comic to delete.")

    def on_item_changed(self, item):
        if item.column() in [0, 1]:
            return
        row = item.row()
        try:
            comic_id = int(self.table.item(row, 1).text())
            story_name = self.table.item(row, 2).text()
            series_name = self.table.item(row, 3).text()
            year_text = self.table.item(row, 4).text()
            year = int(year_text) if year_text.isdigit() else None

            self.db.update_arkas(comic_id, story_name, series_name, year)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update comic: {e}")

    def apply_filters(self):
        kwargs = {}
        if self.story_input.text():
            kwargs["story_name"] = self.story_input.text().strip()
        if self.series_input.text():
            kwargs["series_name"] = self.series_input.text().strip()
        if self.year_input.text():
            try:
                kwargs["year"] = int(self.year_input.text())
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Year must be a number.")
                return
        if self.year_range_input.text():
            try:
                start, end = map(int, self.year_range_input.text().split("-"))
                kwargs["year_range"] = (start, end)
            except Exception:
                QMessageBox.warning(self, "Invalid Format", "Year range must be in format: 2000-2005.")
                return

        query, values = filters.build_arkas_filters(**kwargs)
        cur = self.db.conn.cursor()
        cur.execute(query, values)
        rows = cur.fetchall()
        self.populate_table(rows)

    def clear_filters(self):
        self.story_input.clear()
        self.series_input.clear()
        self.year_input.clear()
        self.year_range_input.clear()
        self.refresh_table()

    def get_visible_rows(self):
        rows = []
        for i in range(self.table.rowCount()):
            story = self.table.item(i, 2).text()
            series = self.table.item(i, 3).text()
            year = int(self.table.item(i, 4).text()) if self.table.item(i, 4).text().isdigit() else None
            rows.append({"story_name": story, "series_name": series, "year": year})
        return rows
