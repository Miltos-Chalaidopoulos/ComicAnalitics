from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog
)
from .dialogs import AddMickeyDialog
from ..database.db_manager import DBManager
from ..services.csv_edit import CSVService
from PySide6.QtCore import Qt


class MickeyTab(QWidget):
    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        layout = QVBoxLayout()

        csv_import_btn = QPushButton("📂 Import from CSV")
        csv_import_btn.clicked.connect(self.import_csv)
        layout.addWidget(csv_import_btn)

        csv_export_btn = QPushButton("💾 Export to CSV")
        csv_export_btn.clicked.connect(self.export_csv)
        layout.addWidget(csv_export_btn)

        add_btn = QPushButton("➕ Add Mickey Comic")
        add_btn.clicked.connect(self.add_mickey_comic)
        layout.addWidget(add_btn)

        del_btn = QPushButton("🗑️ Delete Selected")
        del_btn.clicked.connect(self.delete_selected)
        layout.addWidget(del_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Issue num", "Vol num", "Main Story", "Year"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)

        self.table.itemChanged.connect(self.on_item_changed)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        rows = self.db.search_mickey()
        self.table.blockSignals(True)
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            issue_item = QTableWidgetItem()
            issue_item.setData(Qt.DisplayRole, int(row["issue_num"]))
            issue_item.setData(Qt.UserRole, row["issue_num"])
            self.table.setItem(i, 0, issue_item)

            vol_item = QTableWidgetItem(str(row["vol_num"]))
            self.table.setItem(i, 1, vol_item)

            self.table.setItem(i, 2, QTableWidgetItem(row["mainstory"]))

            year_item = QTableWidgetItem()
            year_item.setData(Qt.DisplayRole, int(row["year"]))
            self.table.setItem(i, 3, year_item)

        self.table.blockSignals(False)

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            service = CSVService(self.db)
            service.import_mickey(file_path)
            QMessageBox.information(self, "Success", "CSV imported successfully!")
            self.refresh_table()

    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            service = CSVService(self.db)
            service.export_mickey(file_path)
            QMessageBox.information(self, "Success", "CSV exported successfully!")

    def add_mickey_comic(self):
        dialog = AddMickeyDialog(self.db)
        if dialog.exec():
            self.refresh_table()

    def delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            issue_num = int(self.table.item(row, 0).text())
            vol_num = int(self.table.item(row, 1).text())
            self.db.delete_mickey(issue_num, vol_num)
            QMessageBox.information(self, "Deleted", "Comic deleted successfully!")
            self.refresh_table()

    def on_item_changed(self, item):
        row = item.row()
        try:
            issue_num = int(self.table.item(row, 0).text())
            vol_num = int(self.table.item(row, 1).text())
            mainstory = self.table.item(row, 2).text()
            year = int(self.table.item(row, 3).text())
            self.db.update_mickey(issue_num, vol_num, mainstory, year)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update comic: {e}")
