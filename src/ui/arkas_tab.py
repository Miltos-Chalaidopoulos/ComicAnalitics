from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,QGroupBox, QMessageBox)
from PySide6.QtCore import Qt
from ..database.db_manager import DBManager
from .dialogs import AddArkasDialog
from ..services import filters

class ArkasTab(QWidget):
    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.filter_box = QGroupBox("Filters")
        filter_layout = QHBoxLayout()
        self.story_input = QLineEdit(); self.story_input.setPlaceholderText("Story Name")
        self.series_input = QLineEdit(); self.series_input.setPlaceholderText("Series Name")
        self.year_input = QLineEdit(); self.year_input.setPlaceholderText("Year")
        self.year_range_input = QLineEdit(); self.year_range_input.setPlaceholderText("e.g. 2000-2005")

        for lbl_text, le in [("Story", self.story_input), ("Series", self.series_input),
                             ("Year", self.year_input), ("Year Range", self.year_range_input)]:
            filter_layout.addWidget(QLabel(lbl_text))
            filter_layout.addWidget(le)

        btn_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply Filters"); apply_btn.clicked.connect(self.apply_filters)
        clear_btn = QPushButton("Clear Filters"); clear_btn.clicked.connect(self.clear_filters)
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(clear_btn)
        filter_layout.addLayout(btn_layout)

        self.filter_box.setLayout(filter_layout)
        layout.addWidget(self.filter_box)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["#", "Story Name", "Series Name", "Year"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        bottom_btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Arkas Comic"); add_btn.clicked.connect(self.add_arkas_comic)
        del_btn = QPushButton("🗑️ Delete Selected"); del_btn.clicked.connect(self.delete_selected)
        bottom_btn_layout.addWidget(add_btn); bottom_btn_layout.addWidget(del_btn)
        layout.addLayout(bottom_btn_layout)

        self.refresh_table()

    def refresh_positions(self):
        for i in range(self.table.rowCount()):
            idx_item = QTableWidgetItem()
            idx_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            idx_item.setData(Qt.DisplayRole, i+1)
            self.table.setItem(i, 0, idx_item)

    def refresh_table(self):
        rows = self.db.search_arkas()
        self.populate_table(rows)

    def populate_table(self, rows):
        self.table.blockSignals(True)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 1, QTableWidgetItem(row["story_name"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["series_name"]))
            self.table.setItem(i, 3, QTableWidgetItem(str(row["year"])))
        self.table.blockSignals(False)
        self.refresh_positions()

    def add_arkas_comic(self):
        dialog = AddArkasDialog(self.db)
        if dialog.exec():
            self.refresh_table()

    def delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            id = row + 1
            self.db.delete_arkas(id)
            QMessageBox.information(self, "Deleted", "Arkas comic deleted successfully!")
            self.refresh_table()

    def apply_filters(self):
        kwargs = {}
        if self.story_input.text(): kwargs["story_name"] = self.story_input.text()
        if self.series_input.text(): kwargs["series_name"] = self.series_input.text()
        if self.year_input.text(): kwargs["year"] = int(self.year_input.text())
        if self.year_range_input.text():
            try:
                start, end = map(int, self.year_range_input.text().split("-"))
                kwargs["year_range"] = (start,end)
            except:
                QMessageBox.warning(self, "Error", "Invalid year range format")
                return
        query, values = filters.build_arkas_filters(**kwargs)
        cur = self.db.conn.cursor(); cur.execute(query, values)
        self.populate_table(cur.fetchall())

    def clear_filters(self):
        self.story_input.clear(); self.series_input.clear()
        self.year_input.clear(); self.year_range_input.clear()
        self.refresh_table()

    def get_visible_rows(self):
        rows = []
        for i in range(self.table.rowCount()):
            story_name = self.table.item(i, 1).text()
            series_name = self.table.item(i, 2).text()
            year = int(self.table.item(i, 3).text())
            rows.append({
                "story_name": story_name,
                "series_name": series_name,
                "year": year
            })
        return rows
