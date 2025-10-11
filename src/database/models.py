# database/models.py

CREATE_MICKEY_TABLE = """
CREATE TABLE IF NOT EXISTS mickey (
    issue_num INTEGER NOT NULL,
    vol_num INTEGER NOT NULL,
    mainstory TEXT,
    year INTEGER,
    PRIMARY KEY(issue_num, vol_num)
);
"""

CREATE_SUPERHEROES_TABLE = """
CREATE TABLE IF NOT EXISTS superheroes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    writer TEXT,
    artist TEXT,
    collection TEXT,
    publisher TEXT,
    issues TEXT,
    main_character TEXT,
    event BOOLEAN,
    story_year INTEGER,
    category TEXT
);
"""

CREATE_ARKAS_TABLE = """
CREATE TABLE IF NOT EXISTS arkas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    story_name TEXT,
    series_name TEXT,
    year INTEGER
);
"""
