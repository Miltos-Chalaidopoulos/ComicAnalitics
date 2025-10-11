from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QLabel,
    QMessageBox, QCheckBox, QPlainTextEdit, QTableWidget, QTableWidgetItem,
    QScrollArea, QWidget, QTextEdit
)

class AddMickeyDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("Add Mickey Comic")
        self.setMinimumWidth(400)

        layout = QFormLayout()
        self.issue_num_input = QLineEdit()
        self.vol_num_input = QLineEdit()
        self.main_story_input = QLineEdit()
        self.year_input = QLineEdit()

        layout.addRow("Issue num:", self.issue_num_input)
        layout.addRow("Vol num:", self.vol_num_input)
        layout.addRow("Main Story:", self.main_story_input)
        layout.addRow("Year:", self.year_input)

        self.submit_btn = QPushButton("Add")
        self.submit_btn.clicked.connect(self.add_mickey)
        v_layout = QVBoxLayout()
        v_layout.addLayout(layout)
        v_layout.addWidget(self.submit_btn)
        self.setLayout(v_layout)

    def add_mickey(self):
        try:
            issue = int(self.issue_num_input.text())
            vol = int(self.vol_num_input.text())
            story = self.main_story_input.text()
            year = int(self.year_input.text())
            self.db.add_mickey(issue, vol, story, year)
            QMessageBox.information(self, "Success", "Mickey comic added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add comic: {e}")


class AddSuperheroesDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("Add Superhero Comic")
        self.setMinimumWidth(400)

        layout = QFormLayout()
        self.title_input = QLineEdit()
        self.writer_input = QLineEdit()
        self.artist_input = QLineEdit()
        self.collection_input = QLineEdit()
        self.publisher_input = QLineEdit()
        self.issues_input = QLineEdit()
        self.main_character_input = QLineEdit()
        self.event_input = QCheckBox()
        self.story_year_input = QLineEdit()
        self.category_input = QLineEdit()

        layout.addRow("Title:", self.title_input)
        layout.addRow("Writer:", self.writer_input)
        layout.addRow("Artist:", self.artist_input)
        layout.addRow("Collection:", self.collection_input)
        layout.addRow("Publisher:", self.publisher_input)
        layout.addRow("Issues:", self.issues_input)
        layout.addRow("Main Character:", self.main_character_input)
        layout.addRow("Event:", self.event_input)
        layout.addRow("Story Year:", self.story_year_input)
        layout.addRow("Category:", self.category_input)

        self.submit_btn = QPushButton("Add")
        self.submit_btn.clicked.connect(self.add_superhero)
        v_layout = QVBoxLayout()
        v_layout.addLayout(layout)
        v_layout.addWidget(self.submit_btn)
        self.setLayout(v_layout)

    def add_superhero(self):
        try:
            title = self.title_input.text()
            writer = self.writer_input.text()
            artist = self.artist_input.text()
            collection = self.collection_input.text()
            publisher = self.publisher_input.text()
            issues = self.issues_input.text()
            main_character = self.main_character_input.text()
            event = self.event_input.isChecked()
            story_year = int(self.story_year_input.text())
            category = self.category_input.text()

            self.db.add_superhero(
                title, writer, artist, collection, publisher,
                issues, main_character, event, story_year, category
            )
            QMessageBox.information(self, "Success", "Superhero comic added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add comic: {e}")


class AddArkasDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("Add Arkas Comic")
        self.setMinimumWidth(400)

        layout = QFormLayout()
        self.story_input = QLineEdit()
        self.series_input = QLineEdit()
        self.year_input = QLineEdit()

        layout.addRow("Story Name:", self.story_input)
        layout.addRow("Series Name:", self.series_input)
        layout.addRow("Year:", self.year_input)

        self.submit_btn = QPushButton("Add")
        self.submit_btn.clicked.connect(self.add_arkas)
        v_layout = QVBoxLayout()
        v_layout.addLayout(layout)
        v_layout.addWidget(self.submit_btn)
        self.setLayout(v_layout)

    def add_arkas(self):
        try:
            story = self.story_input.text()
            series = self.series_input.text()
            year = int(self.year_input.text())
            self.db.add_arkas(story, series, year)
            QMessageBox.information(self, "Success", "Arkas comic added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add comic: {e}")


class SearchDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("Database Search")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Database Tables:"))
        self.tables_display = QPlainTextEdit()
        self.tables_display.setReadOnly(True)
        self.tables_display.setPlainText(
            "Tables in database:\n\n"
            "mickey:\n"
            "    issue_num INTEGER\n"
            "    vol_num INTEGER\n"
            "    mainstory TEXT\n"
            "    year INTEGER\n"
            "    PRIMARY KEY(issue_num, vol_num)\n\n"
            "superheroes:\n"
            "    id INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "    title TEXT\n"
            "    writer TEXT\n"
            "    artist TEXT\n"
            "    collection TEXT\n"
            "    publisher TEXT\n"
            "    issues TEXT\n"
            "    main_character TEXT\n"
            "    event BOOLEAN\n"
            "    story_year INTEGER\n"
            "    category TEXT\n\n"
            "arkas:\n"
            "    id INTEGER PRIMARY KEY AUTOINCREMENT\n"
            "    story_name TEXT\n"
            "    series_name TEXT\n"
            "    year INTEGER"
        )
        layout.addWidget(self.tables_display)

        layout.addWidget(QLabel("Enter your SQL query:"))
        self.query_input = QPlainTextEdit()
        self.query_input.setPlaceholderText("e.g. SELECT * FROM mickey WHERE year > 2000;")
        self.query_input.setMaximumHeight(100)
        layout.addWidget(self.query_input)

        self.run_btn = QPushButton("Run Query")
        self.run_btn.clicked.connect(self.run_query)
        layout.addWidget(self.run_btn)

        layout.addWidget(QLabel("Results:"))
        self.results_table = QTableWidget()
        layout.addWidget(self.results_table)

        self.setLayout(layout)

    def run_query(self):
        query = self.query_input.toPlainText().strip()
        if not query:
            QMessageBox.warning(self, "Warning", "Please enter a query!")
            return
        try:
            cur = self.db.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description] if cur.description else []

            self.results_table.setUpdatesEnabled(False)
            self.results_table.clear()
            self.results_table.setColumnCount(len(headers))
            self.results_table.setRowCount(len(rows))
            self.results_table.setHorizontalHeaderLabels(headers)

            for r_idx, row in enumerate(rows):
                for c_idx, col in enumerate(headers):
                    self.results_table.setItem(r_idx, c_idx, QTableWidgetItem(str(row[col])))

            self.results_table.setUpdatesEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Query failed:\n{e}")
