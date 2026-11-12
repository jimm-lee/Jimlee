import datetime as dt

from content_engine.calendar_plan import build_calendar, normalise_themes
from content_engine.models import Idea, Theme

MONDAY = dt.date(2026, 11, 16)
MON, WED, FRI = 0, 2, 4


def ideas(n: int) -> list[Idea]:
    return [Idea(id=i, title=f"{i}", hook="", format="", summary="") for i in range(1, n + 1)]


def test_normalise_themes_drops_duplicates_unknowns_and_empty_themes():
    themes = [
        Theme("A", "", (1, 2, 2, 99)),
        Theme("B", "", (2, 3)),
        Theme("Empty", "", ()),
    ]
    result = normalise_themes(themes, ideas(3))
    assert [(t.name, t.idea_ids) for t in result] == [("A", (1, 2)), ("B", (3,))]


def test_normalise_themes_gives_unassigned_ideas_to_smallest_theme():
    themes = [Theme("A", "", (1, 2, 3)), Theme("B", "", (4,))]
    result = normalise_themes(themes, ideas(6))
    assert sorted(i for t in result for i in t.idea_ids) == [1, 2, 3, 4, 5, 6]
    assert result[1].idea_ids == (4, 5, 6)


def test_normalise_themes_keeps_the_largest_themes_and_folds_in_the_rest():
    themes = [
        Theme("Small", "", (1,)),
        Theme("Big", "", (2, 3, 4)),
        Theme("Medium", "", (5, 6)),
        Theme("Tiny", "", (7,)),
    ]
    result = normalise_themes(themes, ideas(7), max_themes=2)
    assert [t.name for t in result] == ["Big", "Medium"]
    assert sorted(i for t in result for i in t.idea_ids) == [1, 2, 3, 4, 5, 6, 7]


def test_each_weekday_keeps_the_same_theme_every_week():
    themes = [Theme("A", "", (1, 2)), Theme("B", "", (3, 4)), Theme("C", "", (5, 6))]
    slots = build_calendar(themes, [1, 2, 3, 4, 5, 6], MONDAY, weeks=2, post_weekdays=(MON, WED, FRI))
    assert [s.date.weekday() for s in slots] == [MON, WED, FRI] * 2
    assert [s.theme for s in slots] == ["A", "B", "C", "A", "B", "C"]


def test_ideas_are_scheduled_best_ranked_first_and_never_repeated():
    themes = [Theme("A", "", (1, 2, 3))]
    slots = build_calendar(themes, [3, 1, 2], MONDAY, weeks=4, post_weekdays=(MON,))
    assert [s.idea_id for s in slots] == [3, 1, 2, None]


def test_calendar_starts_on_first_posting_day_on_or_after_start():
    themes = [Theme("A", "", (1,))]
    tuesday = MONDAY + dt.timedelta(days=1)
    slots = build_calendar(themes, [1], tuesday, weeks=1, post_weekdays=(MON, FRI))
    assert slots[0].date == MONDAY + dt.timedelta(days=4)
    assert len(slots) == 2
