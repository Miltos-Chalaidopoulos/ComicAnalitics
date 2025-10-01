import sqlite3
from pathlib import Path
from database import models

DB_FILE = Path(__file__).parent / "data.db"

class DBManager:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute(models.CREATE_MICKEY_TABLE)
        cur.execute(models.CREATE_OTHER_TABLE)
        self.conn.commit()

    def add_mickey(self, issue_num, vol_num, mainstory, year):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO mickey (issue_num, vol_num, mainstory, year) VALUES (?, ?, ?, ?)",
            (issue_num, vol_num, mainstory, year),
        )
        self.conn.commit()

    def delete_mickey(self, issue_num, vol_num):
        cur = self.conn.cursor()
        cur.execute(
            "DELETE FROM mickey WHERE issue_num = ? AND vol_num = ?",
            (issue_num, vol_num),
        )
        self.conn.commit()

    def search_mickey(self, **filters):
        query = "SELECT * FROM mickey"
        conditions, values = [], []
        for key, val in filters.items():
            conditions.append(f"{key} = ?")
            values.append(val)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = self.conn.cursor()
        cur.execute(query, values)
        return cur.fetchall()

    def add_other(self, title, writer, artist, collection, publisher, issues, main_character, event, story_year, category):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO other 
            (title, writer, artist, collection, publisher, issues, main_character, event, story_year, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, writer, artist, collection, publisher, issues, main_character, event, story_year, category),
        )
        self.conn.commit()

    def delete_other(self, id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM other WHERE id = ?", (id,))
        self.conn.commit()

    def search_other(self, **filters):
        query = "SELECT * FROM other"
        conditions, values = [], []
        for key, val in filters.items():
            conditions.append(f"{key} = ?")
            values.append(val)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = self.conn.cursor()
        cur.execute(query, values)
        return cur.fetchall()

    def close(self):
        self.conn.close()
