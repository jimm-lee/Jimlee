"""Turn model scores into a ranking and pick the ideas worth briefing."""

from __future__ import annotations

from typing import Any

from .models import SCORE_MAX, SCORE_MIN, Idea, Score


def clamp_score(value: Any) -> int:
    """Coerce a model-supplied score into the 1-10 range."""
    try:
        number = int(round(float(value)))
    except (TypeError, ValueError):
        return SCORE_MIN
    return max(SCORE_MIN, min(SCORE_MAX, number))


def rank(ideas: list[Idea], scores: dict[int, Score]) -> list[tuple[Idea, Score]]:
    """Best first: highest mean score, then most original, then earliest idea."""
    paired = [
        (idea, scores.get(idea.id) or Score(idea.id, SCORE_MIN, SCORE_MIN, SCORE_MIN, "Not scored"))
        for idea in ideas
    ]
    return sorted(paired, key=lambda pair: (-pair[1].total, -pair[1].originality, pair[0].id))


def select_top(ranked: list[tuple[Idea, Score]], count: int) -> list[tuple[Idea, Score]]:
    return ranked[:count]
