import os
import csv
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from database.db_manager import DBManager
from services.csv_edit import CSVService

TEST_DB = "test_csv.db"
TEST_MICKEY_CSV = "test_mickey.csv"
TEST_OTHER_CSV = "test_other.csv"


@pytest.fixture
def db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db = DBManager(db_path=TEST_DB)
    yield db
    db.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


@pytest.fixture
def csv_service(db):
    return CSVService(db)


def test_import_export_mickey(csv_service, db):
    with open(TEST_MICKEY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Issue num", "Vol num", "Main Story", "Year"])
        writer.writerow([636, 1, "Η Επιστροφή του Φάντομ Ντακ", 1978])

    csv_service.import_mickey(TEST_MICKEY_CSV)
    results = db.search_mickey(issue_num=636)
    assert len(results) == 1
    assert results[0]["mainstory"] == "Η Επιστροφή του Φάντομ Ντακ"

    export_file = "export_mickey.csv"
    csv_service.export_mickey(export_file)

    with open(export_file, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        assert rows[0]["Main Story"] == "Η Επιστροφή του Φάντομ Ντακ"

    os.remove(TEST_MICKEY_CSV)
    os.remove(export_file)


def test_import_export_other(csv_service, db):
    with open(TEST_OTHER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Title", "Writer", "Artist", "Collection", "Publisher",
            "Issues", "Main Character", "Event", "Story Year", "Category"
        ])
        writer.writerow([
            "House Of X", "Jonathan Hickman", "Pepe Larraz", "N/A", "Panini",
            "House Of X #1-6 & Powers Of X #1-6", "X-Men", "true", 2019, "Marvel"
        ])
    csv_service.import_other(TEST_OTHER_CSV)
    results = db.search_other(title="House Of X")
    assert len(results) == 1
    assert results[0]["writer"] == "Jonathan Hickman"
    assert results[0]["event"] == 1

    export_file = "export_other.csv"
    csv_service.export_other(export_file)

    with open(export_file, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        assert rows[0]["Title"] == "House Of X"
        assert rows[0]["Event"] == "true"

    os.remove(TEST_OTHER_CSV)
    os.remove(export_file)
