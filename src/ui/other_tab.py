from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from ..database.db_manager import DBManager
from .dialogs import AddOtherDialog


class OtherTab(QWidget):
    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        layout = QVBoxLayout()

        add_btn = QPushButton("➕ Add Other Comic")
        add_btn.clicked.connect(self.add_other_comic)
        layout.addWidget(add_btn)

        del_btn = QPushButton("🗑️ Delete Selected")
        del_btn.clicked.connect(self.delete_selected)
        layout.addWidget(del_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Title", "Writer", "Artist", "Collection", "Publisher",
            "Issues", "Main Character", "Event", "Story Year", "Category"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemChanged.connect(self.on_item_changed)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        rows = self.db.search_other()
        self.table.blockSignals(True)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            item0 = QTableWidgetItem(row["title"])
            item0.setData(Qt.UserRole, row["id"])
            self.table.setItem(i, 0, item0)
            self.table.setItem(i, 1, QTableWidgetItem(row["writer"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["artist"]))
            self.table.setItem(i, 3, QTableWidgetItem(row["collection"]))
            self.table.setItem(i, 4, QTableWidgetItem(row["publisher"]))
            self.table.setItem(i, 5, QTableWidgetItem(row["issues"]))
            self.table.setItem(i, 6, QTableWidgetItem(row["main_character"]))
            self.table.setItem(i, 7, QTableWidgetItem("Yes" if row["event"] else "No"))
            year_item = QTableWidgetItem()
            year_item.setData(Qt.DisplayRole, row["story_year"])
            self.table.setItem(i, 8, year_item)
            self.table.setItem(i, 9, QTableWidgetItem(row["category"]))
        self.table.blockSignals(False)

    def add_other_comic(self):
        dialog = AddOtherDialog(self.db)
        if dialog.exec():
            self.refresh_table()

    def delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            comic_id = self.table.item(row, 0).data(Qt.UserRole)
            self.db.delete_other(comic_id)
            QMessageBox.information(self, "Deleted", "Comic deleted successfully!")
            self.refresh_table()

    def on_item_changed(self, item):
        row = item.row()
        try:
            comic_id = self.table.item(row, 0).data(Qt.UserRole)
            values = [self.table.item(row, col).text() for col in range(10)]

            title, writer, artist, collection, publisher, issues, main_character, event, story_year, category = values
            event_bool = event.lower() in ("yes", "true", "1")
            story_year = int(story_year)

            self.db.update_other(
                comic_id, title, writer, artist, collection, publisher,
                issues, main_character, event_bool, story_year, category
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update comic: {e}")
