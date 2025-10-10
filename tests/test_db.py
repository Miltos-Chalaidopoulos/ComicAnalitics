import sys
from pathlib import Path
import os
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from database.db_manager import DBManager

TEST_DB = "test_data.db"

@pytest.fixture
def db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db = DBManager(db_path=TEST_DB)
    yield db
    db.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_add_mickey(db):
    db.add_mickey(1, 1, "Main Story", 1990)
    results = db.search_mickey(issue_num=1)
    assert len(results) == 1
    assert results[0]["mainstory"] == "Main Story"

def test_delete_mickey(db):
    db.add_mickey(2, 1, "Story 2", 1995)
    db.delete_mickey(2, 1)
    results = db.search_mickey(issue_num=2)
    assert len(results) == 0

def test_search_mickey_filters(db):
    db.add_mickey(3, 1, "Story 3", 2000)
    db.add_mickey(3, 2, "Story 4", 2001)
    results = db.search_mickey(issue_num=3, vol_num=2)
    assert len(results) == 1
    assert results[0]["mainstory"] == "Story 4"


def test_add_other(db):
    db.add_other("Title", "Writer", "Artist", "Collection", "Publisher",
                 "Issues", "Character", True, 2000, "Category")
    results = db.search_other(main_character="Character")
    assert len(results) == 1
    assert results[0]["title"] == "Title"

def test_delete_other(db):
    db.add_other("DeleteMe", "Writer", "Artist", "Collection", "Publisher",
                 "Issues", "Hero", False, 1999, "Category")
    rec = db.search_other(title="DeleteMe")[0]
    db.delete_other(rec["id"])
    results = db.search_other(title="DeleteMe")
    assert len(results) == 0

def test_search_other_filters(db):
    db.add_other("Title1", "Writer1", "Artist1", "Collection", "Publisher",
                 "Issues", "CharacterA", True, 2000, "Category1")
    db.add_other("Title2", "Writer2", "Artist2", "Collection", "Publisher",
                 "Issues", "CharacterB", False, 2001, "Category2")
    results = db.search_other(main_character="CharacterA")
    assert len(results) == 1
    assert results[0]["title"] == "Title1"

def test_search_other_multiple_filters(db):
    db.add_other("TitleX", "WriterX", "ArtistX", "Collection", "Publisher",
                 "Issues", "CharacterX", True, 2020, "CategoryX")
    results = db.search_other(main_character="CharacterX", story_year=2020, event=True)
    assert len(results) == 1
    assert results[0]["title"] == "TitleX"

def test_empty_search_returns_all(db):
    db.add_mickey(10, 1, "Story10", 2010)
    db.add_mickey(11, 1, "Story11", 2011)
    results = db.search_mickey()
    assert len(results) == 2

    db.add_other("TitleY", "WriterY", "ArtistY", "Collection", "Publisher",
                 "Issues", "CharacterY", True, 2022, "CategoryY")
    results = db.search_other()
    assert len(results) == 1

def test_advanced_search_mickey_exact(db):
    db.add_mickey(100, 1, "Exact Match", 2000)
    results = db.advanced_search_mickey(issue_num=100)
    assert len(results) == 1
    assert results[0]["mainstory"] == "Exact Match"

def test_advanced_search_mickey_year_range(db):
    db.add_mickey(101, 1, "Story A", 1995)
    db.add_mickey(102, 1, "Story B", 2005)
    results = db.advanced_search_mickey(year_range=(1990, 2000))
    assert len(results) == 1
    assert results[0]["mainstory"] == "Story A"

def test_advanced_search_mickey_issue_range(db):
    for i in range(200, 205):
        db.add_mickey(i, 1, f"Story {i}", 2010)
    results = db.advanced_search_mickey(issue_range=(201, 203))
    assert len(results) == 3

def test_advanced_search_mickey_exclude_range(db):
    for i in range(300, 305):
        db.add_mickey(i, 1, f"Story {i}", 2015)
    missing = db.advanced_search_mickey(exclude_issue_range=(300, 305))
    # Βάλαμε 300-304, λείπει το 305
    assert 305 in missing

def test_advanced_search_other_exact(db):
    db.add_other("House Of X", "Hickman", "Larraz", "N/A", "Marvel",
                 "HOX #1-6", "X-Men", True, 2019, "Marvel")
    results = db.advanced_search_other(writer="Hickman", category="Marvel")
    assert len(results) == 1
    assert results[0]["title"] == "House Of X"

def test_advanced_search_other_year_range(db):
    db.add_other("Event A", "WriterA", "ArtistA", "CollA", "PublisherA",
                 "Issues", "HeroA", True, 2010, "CatA")
    db.add_other("Event B", "WriterB", "ArtistB", "CollB", "PublisherB",
                 "Issues", "HeroB", False, 2020, "CatB")
    results = db.advanced_search_other(story_year_range=(2005, 2015))
    assert len(results) == 1
    assert results[0]["title"] == "Event A"

def test_advanced_search_other_multiple_filters(db):
    db.add_other("TitleX", "WriterX", "ArtistX", "CollectionX", "PublisherX",
                 "IssuesX", "HeroX", True, 2021, "CategoryX")
    results = db.advanced_search_other(writer="WriterX", main_character="HeroX", event=True)
    assert len(results) == 1
    assert results[0]["title"] == "TitleX"
