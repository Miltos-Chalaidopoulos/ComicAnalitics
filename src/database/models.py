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

CREATE_OTHER_TABLE = """
CREATE TABLE IF NOT EXISTS other (
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
