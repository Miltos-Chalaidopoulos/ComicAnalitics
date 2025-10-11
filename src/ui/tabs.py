from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QFileDialog
)
import csv


class BaseTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_table)
        btn_layout.addWidget(self.refresh_btn)
        self.layout.addLayout(btn_layout)

    def refresh_table(self):
        raise NotImplementedError

    def export_csv(self, path):
        raise NotImplementedError

    def import_csv(self, path):
        raise NotImplementedError


class MickeyTab(BaseTab):
    def refresh_table(self):
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM mickey")
        rows = cur.fetchall()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(cur.description))
        self.table.setHorizontalHeaderLabels([desc[0] for desc in cur.description])
        for r_idx, row in enumerate(rows):
            for c_idx, desc in enumerate(cur.description):
                self.table.setItem(r_idx, c_idx, QTableWidgetItem(str(row[desc[0]])))

    def export_csv(self, path):
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM mickey")
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow([row[h] for h in headers])

    def import_csv(self, path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.db.add_mickey(int(row["issue_num"]), int(row["vol_num"]), row["mainstory"], int(row["year"]))
        self.refresh_table()


class SuperheroesTab(BaseTab):
    def refresh_table(self):
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM superheroes")
        rows = cur.fetchall()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(cur.description))
        self.table.setHorizontalHeaderLabels([desc[0] for desc in cur.description])
        for r_idx, row in enumerate(rows):
            for c_idx, desc in enumerate(cur.description):
                self.table.setItem(r_idx, c_idx, QTableWidgetItem(str(row[desc[0]])))

    def export_csv(self, path):
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM superheroes")
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow([row[h] for h in headers])

    def import_csv(self, path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.db.add_superhero(
                    row["title"], row["writer"], row["artist"], row["collection"], row["publisher"],
                    row["issues"], row["main_character"], row["event"].lower() == "true",
                    int(row["story_year"]), row["category"]
                )
        self.refresh_table()


class ArkasTab(BaseTab):
    def refresh_table(self):
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM arkas")
        rows = cur.fetchall()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(cur.description))
        self.table.setHorizontalHeaderLabels([desc[0] for desc in cur.description])
        for r_idx, row in enumerate(rows):
            for c_idx, desc in enumerate(cur.description):
                self.table.setItem(r_idx, c_idx, QTableWidgetItem(str(row[desc[0]])))

    def export_csv(self, path):
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM arkas")
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow([row[h] for h in headers])

    def import_csv(self, path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.db.add_arkas(row["story_name"], row["series_name"], int(row["year"]))
        self.refresh_table()
