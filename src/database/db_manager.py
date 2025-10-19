import sqlite3
import sys
from pathlib import Path
from . import models
from services import filters

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "data.db"

class DBManager:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute(models.CREATE_MICKEY_TABLE)
        cur.execute(models.CREATE_SUPERHEROES_TABLE)
        cur.execute(models.CREATE_ARKAS_TABLE)
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
        cur.execute("DELETE FROM mickey WHERE issue_num = ? AND vol_num = ?", (issue_num, vol_num))
        self.conn.commit()

    def search_mickey(self, **filters_kwargs):
        query = "SELECT * FROM mickey"
        conditions, values = [], []
        for key, val in filters_kwargs.items():
            conditions.append(f"{key} = ?")
            values.append(val)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = self.conn.cursor()
        cur.execute(query, values)
        return cur.fetchall()
    
    def advanced_search_mickey(self, **kwargs):
        query, values, exclude_range = filters.build_mickey_filters(**kwargs)
        print("QUERY:", query)
        print("VALUES:", values)
        cur = self.conn.cursor()
        cur.execute(query, values)
        return cur.fetchall()

    def find_missing_issues(self, start, end, **kwargs):
        query, values, _ = filters.build_mickey_filters(**kwargs)
        print("QUERY (missing):", query)
        print("VALUES (missing):", values)
        cur = self.conn.cursor()
        cur.execute(query, values)
        existing = {row["issue_num"] for row in cur.fetchall()}
        return [num for num in range(start, end + 1) if num not in existing]



    def add_superhero(self, title, writer, artist, collection, publisher, issues, main_character, event, story_year, category):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO superheroes 
            (title, writer, artist, collection, publisher, issues, main_character, event, story_year, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, writer, artist, collection, publisher, issues, main_character, event, story_year, category),
        )
        self.conn.commit()

    def delete_superhero(self, id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM superheroes WHERE id = ?", (id,))
        self.conn.commit()

    def search_superheroes(self, **kwargs):
        query = "SELECT * FROM superheroes"
        conditions, values = [], []
        for key, val in kwargs.items():
            conditions.append(f"{key} = ?")
            values.append(val)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = self.conn.cursor()
        cur.execute(query, values)
        return cur.fetchall()
    
    def advanced_search_superheroes(self, **kwargs):
        query, values = filters.build_superheroes_filters(**kwargs)
        print("QUERY:", query)
        print("VALUES:", values)
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

    def update_superhero(self, id, title, writer, artist, collection,publisher, issues, main_character, event, story_year, category):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE superheroes
            SET title=?, writer=?, artist=?, collection=?, publisher=?,
                issues=?, main_character=?, event=?, story_year=?, category=? 
            WHERE id = ?
        """, (title, writer, artist, collection, publisher,
            issues, main_character, event, story_year, category, id))
        self.conn.commit()

    def get_superhero_categories(self):
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT category FROM superheroes")
        rows = cur.fetchall()
        return [row["category"] for row in rows]

    def add_arkas(self, story_name, series_name, year):
        cur = self.conn.cursor()
        cur.execute( "INSERT INTO arkas (story_name, series_name, year) VALUES (?, ?, ?)", (story_name, series_name, year)) 
        self.conn.commit()
    
    def delete_arkas(self, id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM arkas WHERE id = ?", (id,))
        self.conn.commit()
    
    def search_arkas(self, **kwargs):
        query = "SELECT * FROM arkas"
        conditions, values = [], []
        for key, val in kwargs.items():
            conditions.append(f"{key} = ?")
            values.append(val)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur = self.conn.cursor()
        cur.execute(query, values)
        return cur.fetchall()

    def update_arkas(self, id, story_name, series_name, year):
        cur = self.conn.cursor()
        cur.execute("""UPDATE arkas SET story_name=?, series_name=?, year=? WHERE id=? """, (story_name, series_name, year, id))
        self.conn.commit()
    
    def close(self):
        self.conn.close()
