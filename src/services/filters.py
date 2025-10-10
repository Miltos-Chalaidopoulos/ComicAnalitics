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
