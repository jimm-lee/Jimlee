"""Lay ideas out on a calendar where each posting weekday owns a recurring theme."""

from __future__ import annotations

import datetime as dt

from .models import Idea, Slot, Theme

DAYS_PER_WEEK = 7


def normalise_themes(
    themes: list[Theme], ideas: list[Idea], max_themes: int | None = None
) -> tuple[Theme, ...]:
    """Make every idea belong to exactly one of at most `max_themes` themes.

    Small models repeat ids, invent ids, forget ideas and return more themes than
    asked for, so: keep the first mention of each real id, drop empty themes, keep
    only the largest `max_themes` themes, and hand leftover ideas to the smallest
    theme one at a time.
    """
    known = {idea.id for idea in ideas}
    seen: set[int] = set()
    cleaned: list[Theme] = []
    for theme in themes:
        ids = tuple(i for i in dict.fromkeys(theme.idea_ids) if i in known and i not in seen)
        seen.update(ids)
        if ids:
            cleaned.append(Theme(theme.name, theme.description, ids))
    if not cleaned:
        return (Theme("Everything", "All ideas", tuple(sorted(known))),)
    if max_themes is not None and len(cleaned) > max_themes:
        largest = sorted(range(len(cleaned)), key=lambda k: (-len(cleaned[k].idea_ids), k))[:max_themes]
        cleaned = [cleaned[k] for k in sorted(largest)]
        seen = {i for theme in cleaned for i in theme.idea_ids}
    for leftover in sorted(known - seen):
        smallest = min(range(len(cleaned)), key=lambda k: len(cleaned[k].idea_ids))
        target = cleaned[smallest]
        cleaned[smallest] = Theme(target.name, target.description, target.idea_ids + (leftover,))
    return tuple(cleaned)


def posting_dates(start: dt.date, weeks: int, post_weekdays: tuple[int, ...]) -> list[dt.date]:
    """Every posting day in `weeks` weeks, starting at the first one on or after `start`."""
    days = sorted(set(post_weekdays))
    first = min(
        start + dt.timedelta(days=(weekday - start.weekday()) % DAYS_PER_WEEK) for weekday in days
    )
    end = first + dt.timedelta(days=weeks * DAYS_PER_WEEK)
    return [
        first + dt.timedelta(days=offset)
        for offset in range((end - first).days)
        if (first + dt.timedelta(days=offset)).weekday() in days
    ]


def build_calendar(
    themes: list[Theme] | tuple[Theme, ...],
    rank_order: list[int],
    start: dt.date,
    weeks: int,
    post_weekdays: tuple[int, ...],
) -> list[Slot]:
    """Give each posting weekday a fixed theme and fill it with that theme's best ideas.

    A slot whose theme has run out of ideas gets `idea_id=None` (an open slot).
    """
    position = {idea_id: index for index, idea_id in enumerate(rank_order)}
    queues = {
        theme.name: sorted(theme.idea_ids, key=lambda i: position.get(i, len(position)))
        for theme in themes
    }
    weekday_theme = {
        weekday: themes[index % len(themes)].name
        for index, weekday in enumerate(sorted(set(post_weekdays)))
    }
    slots: list[Slot] = []
    used: dict[str, int] = {name: 0 for name in queues}
    for day in posting_dates(start, weeks, post_weekdays):
        theme = weekday_theme[day.weekday()]
        queue = queues[theme]
        idea_id = queue[used[theme]] if used[theme] < len(queue) else None
        used[theme] += 1
        slots.append(Slot(day, theme, idea_id))
    return slots
