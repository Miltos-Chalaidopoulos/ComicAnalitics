import sqlite3
from pathlib import Path
from . import models
from ..services import filters

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
    
    def advanced_search_mickey(self, **kwargs):
        query, values, exclude_range = filters.build_mickey_filters(**kwargs)
        cur = self.conn.cursor()
        cur.execute(query, values)
        results = cur.fetchall()
        if exclude_range is not None:
            start, end = exclude_range
            existing = {row["issue_num"] for row in results}
            missing = [num for num in range(start, end+1) if num not in existing]
            return missing
        return results

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
    
    def advanced_search_other(self, **kwargs):
        query, values = filters.build_other_filters(**kwargs)
        cur = self.conn.cursor()
        cur.execute(query, values)
        return cur.fetchall()

    def update_mickey(self, issue_num, vol_num, mainstory, year):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE mickey
            SET mainstory = ?, year = ?
            WHERE issue_num = ? AND vol_num = ?
        """, (mainstory, year, issue_num, vol_num))
        self.conn.commit()

    def update_other(self, id, title, writer, artist, collection,publisher, issues, main_character, event, story_year, category):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE other
            SET title=?, writer=?, artist=?, collection=?, publisher=?,
                issues=?, main_character=?, event=?, story_year=?, category=? 
            WHERE id = ?
        """, (title, writer, artist, collection, publisher,
            issues, main_character, event, story_year, category, id))
        self.conn.commit()


    def close(self):
        self.conn.close()
