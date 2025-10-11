from typing import List, Tuple, Optional

def build_mickey_filters(
    issue_num: Optional[int] = None,
    vol_num: Optional[int] = None,
    mainstory: Optional[str] = None,
    year: Optional[int] = None,
    year_range: Optional[Tuple[int, int]] = None,
    issue_range: Optional[Tuple[int, int]] = None,
    exclude_issue_range: Optional[Tuple[int, int]] = None
) -> Tuple[str, List, Optional[Tuple[int, int]]]:
    """
    SQL query for table mickey
    returns (query, values, exclude_range).
    """
    conditions = []
    values = []

    if issue_num is not None:
        conditions.append("issue_num = ?")
        values.append(issue_num)

    if vol_num is not None:
        conditions.append("vol_num = ?")
        values.append(vol_num)

    if mainstory is not None:
        conditions.append("mainstory = ?")
        values.append(mainstory)

    if year is not None:
        conditions.append("year = ?")
        values.append(year)

    if year_range is not None:
        start, end = year_range
        conditions.append("year BETWEEN ? AND ?")
        values.extend([start, end])

    if issue_range is not None:
        start, end = issue_range
        conditions.append("issue_num BETWEEN ? AND ?")
        values.extend([start, end])

    query = "SELECT * FROM mickey"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    return query, values, exclude_issue_range

def build_superheroes_filters(
    title: Optional[str] = None,
    writer: Optional[str] = None,
    artist: Optional[str] = None,
    collection: Optional[str] = None,
    publisher: Optional[str] = None,
    issues: Optional[str] = None,
    main_character: Optional[str] = None,
    event: Optional[bool] = None,
    story_year: Optional[int] = None,
    year_range: Optional[Tuple[int, int]] = None,
    category: Optional[str] = None
) -> Tuple[str, List]:
    conditions = []
    values = []

    if title: conditions.append("title = ?"); values.append(title)
    if writer: conditions.append("writer = ?"); values.append(writer)
    if artist: conditions.append("artist = ?"); values.append(artist)
    if collection: conditions.append("collection = ?"); values.append(collection)
    if publisher: conditions.append("publisher = ?"); values.append(publisher)
    if issues: conditions.append("issues = ?"); values.append(issues)
    if main_character: conditions.append("main_character = ?"); values.append(main_character)
    if event is not None: conditions.append("event = ?"); values.append(event)
    if story_year is not None: conditions.append("story_year = ?"); values.append(story_year)
    if category: conditions.append("category = ?"); values.append(category)
    if year_range:
        start, end = year_range
        conditions.append("story_year BETWEEN ? AND ?")
        values.extend([start, end])

    query = "SELECT * FROM superheroes"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    return query, values

def build_arkas_filters(
    story_name: Optional[str] = None,
    series_name: Optional[str] = None,
    year: Optional[int] = None,
    year_range: Optional[Tuple[int,int]] = None
) -> Tuple[str, List]:
    conditions, values = [], []

    if story_name: conditions.append("story_name = ?"); values.append(story_name)
    if series_name: conditions.append("series_name = ?"); values.append(series_name)
    if year is not None: conditions.append("year = ?"); values.append(year)
    if year_range:
        start, end = year_range
        conditions.append("year BETWEEN ? AND ?")
        values.extend([start, end])

    query = "SELECT * FROM arkas"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    return query, values
