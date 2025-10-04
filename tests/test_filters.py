import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services import filters    


def test_build_mickey_filters_simple():
    query, values, exclude = filters.build_mickey_filters(issue_num=5, vol_num=1)
    assert "issue_num = ?" in query
    assert "vol_num = ?" in query
    assert values == [5, 1]
    assert exclude is None


def test_build_mickey_filters_with_year_range():
    query, values, _ = filters.build_mickey_filters(year_range=(1990, 2000))
    assert "year BETWEEN ? AND ?" in query
    assert values == [1990, 2000]


def test_build_mickey_filters_with_issue_range():
    query, values, _ = filters.build_mickey_filters(issue_range=(10, 20))
    assert "issue_num BETWEEN ? AND ?" in query
    assert values == [10, 20]


def test_build_mickey_filters_with_exclude():
    query, values, exclude = filters.build_mickey_filters(exclude_issue_range=(5, 10))
    assert "issue_num" not in query
    assert exclude == (5, 10)


def test_build_other_filters_single_field():
    query, values = filters.build_other_filters(writer="Hickman")
    assert "writer = ?" in query
    assert values == ["Hickman"]


def test_build_other_filters_multiple_fields():
    query, values = filters.build_other_filters(writer="Hickman", category="Marvel", event=True)
    assert "writer = ?" in query
    assert "category = ?" in query
    assert "event = ?" in query
    assert values == ["Hickman", "Marvel", 1]


def test_build_other_filters_with_year_range():
    query, values = filters.build_other_filters(story_year_range=(2010, 2020))
    assert "story_year BETWEEN ? AND ?" in query
    assert values == [2010, 2020]
