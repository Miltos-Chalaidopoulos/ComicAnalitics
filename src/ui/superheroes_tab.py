from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from ..database.db_manager import DBManager
from .dialogs import AddSuperheroesDialog


class CategoryTable(QWidget):
    def __init__(self, db: DBManager, category: str, parent_tab):
        super().__init__()
        self.db = db
        self.category = category
        self.parent_tab = parent_tab
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "#","Title","Writer","Artist","Collection","Publisher",
            "Issues","Main Character","Event","Story Year"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemChanged.connect(self.on_item_changed)
        self.layout.addWidget(self.table)

        self.refresh_table()

    def refresh_table(self, filters: dict = None):
        if filters is None:
            filters = {}
        filters["category"] = self.category
        rows = self.db.advanced_search_superheroes(**filters)
        self.populate_table(rows)

    def populate_table(self, rows):
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            idx_item = QTableWidgetItem()
            idx_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            idx_item.setData(Qt.DisplayRole, i+1)
            self.table.setItem(i, 0, idx_item)

            self.table.setItem(i, 1, QTableWidgetItem(row["title"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["writer"]))
            self.table.setItem(i, 3, QTableWidgetItem(row["artist"]))
            self.table.setItem(i, 4, QTableWidgetItem(row["collection"]))
            self.table.setItem(i, 5, QTableWidgetItem(row["publisher"]))
            self.table.setItem(i, 6, QTableWidgetItem(row["issues"]))
            self.table.setItem(i, 7, QTableWidgetItem(row["main_character"]))
            self.table.setItem(i, 8, QTableWidgetItem("Yes" if row["event"] else "No"))

            year_item = QTableWidgetItem()
            year_item.setData(Qt.DisplayRole, row["story_year"])
            self.table.setItem(i, 9, year_item)
        self.table.setSortingEnabled(True)
        self.table.blockSignals(False)

    def on_item_changed(self, item):
        if item.column() == 0:
            return
        row = item.row()
        try:
            comic_id = self.table.item(row, 1).data(Qt.UserRole) or int(row)
            values = [self.table.item(row, col).text() for col in range(1, 10)]
            title, writer, artist, collection, publisher, issues, main_char, event, story_year = values
            event_bool = event.lower() in ("yes", "true", "1")
            story_year = int(story_year)
            self.db.update_superhero(comic_id, title, writer, artist, collection, publisher,
                                     issues, main_char, event_bool, story_year, self.category)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update comic: {e}")

    def add_superhero_comic(self):
        dialog = AddSuperheroesDialog(self.db)
        if dialog.exec():
            self.parent_tab.refresh_categories()
            self.parent_tab.select_category_tab(self.category)

    def delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            comic_id = self.table.item(row, 1).data(Qt.UserRole) or int(row)
            self.db.delete_superhero(comic_id)
            QMessageBox.information(self, "Deleted", "Comic deleted successfully!")
            self.refresh_table()

    def get_visible_rows(self):
        rows = []
        for i in range(self.table.rowCount()):
            title = self.table.item(i, 1).text()
            writer = self.table.item(i, 2).text()
            artist = self.table.item(i, 3).text()
            collection = self.table.item(i, 4).text()
            publisher = self.table.item(i, 5).text()
            issues = self.table.item(i, 6).text()
            main_character = self.table.item(i, 7).text()
            event = self.table.item(i, 8).text().lower() in ("yes", "true", "1")
            story_year = int(self.table.item(i, 9).text())

            rows.append({
                "title": title,
                "writer": writer,
                "artist": artist,
                "collection": collection,
                "publisher": publisher,
                "issues": issues,
                "main_character": main_character,
                "event": event,
                "story_year": story_year,
                "category": self.category
            })
        return rows

class SuperheroesTab(QWidget):
    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.filter_box = QGroupBox("Filters")
        filter_layout = QVBoxLayout()
        self.filter_inputs = {}

        top_row_layout = QHBoxLayout()
        bottom_row_layout = QHBoxLayout()

        top_labels = ["Title", "Writer", "Artist", "Collection", "Publisher"]
        bottom_labels = ["Issues", "Main Character", "Event", "Year Range"]

        for lbl_text in top_labels:
            lbl = QLabel(lbl_text)
            le = QLineEdit()
            le.setPlaceholderText(f" {lbl_text}")
            top_row_layout.addWidget(lbl)
            top_row_layout.addWidget(le)
            self.filter_inputs[lbl_text.lower().replace(" ", "_")] = le

        for lbl_text in bottom_labels:
            lbl = QLabel(lbl_text)
            le = QLineEdit()
            if lbl_text == "Year Range":
                le.setPlaceholderText("e.g. 2000-2005")
            elif lbl_text == "Event":
                le.setPlaceholderText("Yes or No")
            else:
                le.setPlaceholderText(f"{lbl_text}")
            bottom_row_layout.addWidget(lbl)
            bottom_row_layout.addWidget(le)
            self.filter_inputs[lbl_text.lower().replace(" ", "_")] = le

        filter_layout.addLayout(top_row_layout)
        filter_layout.addLayout(bottom_row_layout)

        btn_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply Filters")
        apply_btn.clicked.connect(self.apply_filters)
        clear_btn = QPushButton("Clear Filters")
        clear_btn.clicked.connect(self.clear_filters)
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        filter_layout.addLayout(btn_layout)

        self.filter_box.setLayout(filter_layout)
        layout.addWidget(self.filter_box)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.category_tables = {}
        self.refresh_categories()

        bottom_btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Superhero Comic")
        add_btn.clicked.connect(self.add_comic_current_tab)
        del_btn = QPushButton("🗑️ Delete Selected")
        del_btn.clicked.connect(self.delete_current_tab)
        bottom_btn_layout.addWidget(add_btn)
        bottom_btn_layout.addWidget(del_btn)
        layout.addLayout(bottom_btn_layout)

    def refresh_categories(self):
        categories = self.db.get_superhero_categories()
        self.tabs.clear()
        self.category_tables = {}
        for cat in categories:
            table_widget = CategoryTable(self.db, category=cat, parent_tab=self)
            self.category_tables[cat] = table_widget
            self.tabs.addTab(table_widget, cat)

    def select_category_tab(self, category):
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == category:
                self.tabs.setCurrentIndex(i)
                break

    def apply_filters(self):
        filters = {}
        for key, le in self.filter_inputs.items():
            if le.text():
                if key == "event":
                    filters[key] = le.text().lower() in ("yes","true","1")
                elif key == "year_range":
                    try:
                        start,end = map(int, le.text().split("-"))
                        filters["year_range"] = (start,end)
                    except:
                        QMessageBox.warning(self,"Error","Invalid year range format (start-end)")
                        return
                else:
                    filters[key] = le.text()
        for cat_table in self.category_tables.values():
            cat_table.refresh_table(filters)

    def clear_filters(self):
        for le in self.filter_inputs.values():
            le.clear()
        for cat_table in self.category_tables.values():
            cat_table.refresh_table()

    def add_comic_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.add_superhero_comic()

    def delete_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.delete_selected()
