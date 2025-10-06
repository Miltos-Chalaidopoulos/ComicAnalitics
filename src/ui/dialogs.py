from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox

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

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Mickey Comics")
        self.setMinimumWidth(300)

        layout = QFormLayout()
        self.search_input = QLineEdit()
        layout.addRow("Search Query:", self.search_input)

        self.submit_btn = QPushButton("Search")
        self.submit_btn.clicked.connect(self.accept)
        v_layout = QVBoxLayout()
        v_layout.addLayout(layout)
        v_layout.addWidget(self.submit_btn)
        self.setLayout(v_layout)

class AddOtherDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("Add Other Comic")
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
        self.submit_btn.clicked.connect(self.add_other)
        v_layout = QVBoxLayout()
        v_layout.addLayout(layout)
        v_layout.addWidget(self.submit_btn)
        self.setLayout(v_layout)

    def add_other(self):
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

            self.db.add_other(
                title, writer, artist, collection, publisher,
                issues, main_character, event, story_year, category
            )
            QMessageBox.information(self, "Success", "Other comic added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add comic: {e}")
