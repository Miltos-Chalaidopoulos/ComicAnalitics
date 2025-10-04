from typing import List, Tuple, Optional

def build_mickey_filters(
    issue_num: Optional[int] = None,
    vol_num: Optional[int] = None,
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


def build_other_filters(
    title: Optional[str] = None,
    writer: Optional[str] = None,
    artist: Optional[str] = None,
    collection: Optional[str] = None,
    publisher: Optional[str] = None,
    main_character: Optional[str] = None,
    story_year_range: Optional[Tuple[int, int]] = None,
    category: Optional[str] = None,
    event: Optional[bool] = None
) -> Tuple[str, List]:
    """
    SQL query for table other
    returns (query, values).
    """
    conditions = []
    values = []

    if title is not None:
        conditions.append("title = ?")
        values.append(title)

    if writer is not None:
        conditions.append("writer = ?")
        values.append(writer)

    if artist is not None:
        conditions.append("artist = ?")
        values.append(artist)

    if collection is not None:
        conditions.append("collection = ?")
        values.append(collection)

    if publisher is not None:
        conditions.append("publisher = ?")
        values.append(publisher)

    if main_character is not None:
        conditions.append("main_character = ?")
        values.append(main_character)

    if story_year_range is not None:
        start, end = story_year_range
        conditions.append("story_year BETWEEN ? AND ?")
        values.extend([start, end])

    if category is not None:
        conditions.append("category = ?")
        values.append(category)

    if event is not None:
        conditions.append("event = ?")
        values.append(1 if event else 0)

    query = "SELECT * FROM other"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    return query, values
