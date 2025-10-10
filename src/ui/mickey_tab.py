from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QHBoxLayout, QLabel, QGroupBox,
    QDialog, QScrollArea, QTextEdit
)
from PySide6.QtCore import Qt
from ..database.db_manager import DBManager
from .dialogs import AddMickeyDialog


class MickeyTab(QWidget):
    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        layout = QVBoxLayout()

        filter_box = QGroupBox("Filters")
        filter_layout = QVBoxLayout()

        row1 = QHBoxLayout()
        self.issue_input = QLineEdit(); self.issue_input.setPlaceholderText("Issue #")
        self.vol_input = QLineEdit(); self.vol_input.setPlaceholderText("Vol #")
        self.mainstory_input = QLineEdit(); self.mainstory_input.setPlaceholderText("Main Story")
        self.year_input = QLineEdit(); self.year_input.setPlaceholderText("Year")

        row1.addWidget(QLabel("Issue:")); row1.addWidget(self.issue_input)
        row1.addWidget(QLabel("Vol:")); row1.addWidget(self.vol_input)
        row1.addWidget(QLabel("Story:")); row1.addWidget(self.mainstory_input)
        row1.addWidget(QLabel("Year:")); row1.addWidget(self.year_input)

        row2 = QHBoxLayout()
        self.year_range_input = QLineEdit(); self.year_range_input.setPlaceholderText("e.g. 2000-2005")
        self.issue_range_input = QLineEdit(); self.issue_range_input.setPlaceholderText("e.g. 10-20")
        self.exclude_range_input = QLineEdit(); self.exclude_range_input.setPlaceholderText("e.g. 15-19")

        row2.addWidget(QLabel("Year Range:")); row2.addWidget(self.year_range_input)
        row2.addWidget(QLabel("Issue Range:")); row2.addWidget(self.issue_range_input)
        row2.addWidget(QLabel("Missing Issues (range):")); row2.addWidget(self.exclude_range_input)

        btns = QHBoxLayout()
        apply_btn = QPushButton("Apply Filters")
        clear_btn = QPushButton("Clear Filters")
        apply_btn.clicked.connect(self.apply_filters)
        clear_btn.clicked.connect(self.clear_filters)
        btns.addWidget(apply_btn)
        btns.addWidget(clear_btn)
        btns.addStretch()

        filter_layout.addLayout(row1)
        filter_layout.addLayout(row2)
        filter_layout.addLayout(btns)
        filter_box.setLayout(filter_layout)

        layout.addWidget(filter_box)

        add_btn = QPushButton("➕ Add Mickey Comic")
        add_btn.clicked.connect(self.add_mickey_comic)
        layout.addWidget(add_btn)

        del_btn = QPushButton("🗑️ Delete Selected")
        del_btn.clicked.connect(self.delete_selected)
        layout.addWidget(del_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["#", "Issue num", "Vol num", "Main Story", "Year"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)

        self.table.itemChanged.connect(self.on_item_changed)
        self.table.horizontalHeader().sortIndicatorChanged.connect(self.refresh_positions)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.refresh_table()

    def refresh_positions(self):
        """Refreces # column"""
        for i in range(self.table.rowCount()):
            index_item = self.table.item(i, 0)
            if not index_item:
                index_item = QTableWidgetItem()
                index_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(i, 0, index_item)
            else:
                index_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            index_item.setData(Qt.DisplayRole, i + 1)

    def refresh_table(self):
        rows = self.db.search_mickey()
        self.populate_table(rows)

    def populate_table(self, rows):
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            index_item = QTableWidgetItem()
            index_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            index_item.setData(Qt.DisplayRole, i + 1)
            self.table.setItem(i, 0, index_item)

            issue_item = QTableWidgetItem()
            issue_item.setData(Qt.DisplayRole, int(row["issue_num"]))
            self.table.setItem(i, 1, issue_item)

            vol_item = QTableWidgetItem(str(row["vol_num"]))
            self.table.setItem(i, 2, vol_item)

            self.table.setItem(i, 3, QTableWidgetItem(row["mainstory"]))

            year_item = QTableWidgetItem()
            year_item.setData(Qt.DisplayRole, int(row["year"]))
            self.table.setItem(i, 4, year_item)

        self.table.setSortingEnabled(True)
        self.table.blockSignals(False)
        self.refresh_positions()

    def add_mickey_comic(self):
        dialog = AddMickeyDialog(self.db)
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
        if missing:
            text.setPlainText(", ".join(map(str, missing)))
        else:
            text.setPlainText("No missing issues found.")
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
