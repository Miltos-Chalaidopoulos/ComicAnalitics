import csv
from ..database.db_manager import DBManager

class CSVService:
    def __init__(self, db: DBManager):
        self.db = db

    def detect_csv_type(self, csv_file):
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)

        mickey_headers = ["Issue num", "Vol num", "Main Story", "Year"]
        other_headers = [
            "Title", "Writer", "Artist", "Collection", "Publisher",
            "Issues", "Main Character", "Event", "Story Year", "category"
        ]

        if headers == mickey_headers:
            return "mickey"
        elif headers == other_headers:
            return "other"
        return None

    def import_mickey(self, csv_file):
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.db.add_mickey(
                        int(row["Issue num"]),
                        int(row["Vol num"]),
                        row["Main Story"],
                        int(row["Year"]),
                    )
                except Exception as e:
                    print(f"⚠️ Error for {row['Issue num']} - {row['Vol num']}: {e}")

    def export_mickey(self, csv_file):
        rows = self.db.search_mickey()
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["Issue num", "Vol num", "Main Story", "Year"]
            )
            writer.writeheader()
            for row in rows:
                writer.writerow(
                    {
                        "Issue num": row["issue_num"],
                        "Vol num": row["vol_num"],
                        "Main Story": row["mainstory"],
                        "Year": row["year"],
                    }
                )

    def import_other(self, csv_file):
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.db.add_other(
                        row["Title"],
                        row["Writer"],
                        row["Artist"],
                        row["Collection"],
                        row["Publisher"],
                        row["Issues"],
                        row["Main Character"],
                        True if row["Event"].lower() == "true" else False,
                        int(row["Story Year"]),
                        row["category"],
                    )
                except Exception as e:
                    print(f"⚠️ Error for {row['Title']}: {e}")

    def export_other(self, csv_file):
        rows = self.db.search_other()
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "Title", "Writer", "Artist", "Collection",
                    "Publisher", "Issues", "Main Character", "Event",
                    "Story Year", "category"
                ]
            )
            writer.writeheader()
            for row in rows:
                writer.writerow({
                    "Title": row["title"],
                    "Writer": row["writer"],
                    "Artist": row["artist"],
                    "Collection": row["collection"],
                    "Publisher": row["publisher"],
                    "Issues": row["issues"],
                    "Main Character": row["main_character"],
                    "Event": "true" if row["event"] else "false",
                    "Story Year": row["story_year"],
                    "category": row["category"],
                })
