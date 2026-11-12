from typing import Any

import pytest

from content_engine.models import Angle, Idea
from content_engine.steps import (
    find_angles,
    generate_ideas,
    group_themes,
    score_ideas,
    write_brief,
)


class FakeModel:
    """Returns queued replies in order and records each prompt."""

    def __init__(self, replies: list[Any]) -> None:
        self.replies = list(replies)
        self.prompts: list[str] = []

    def ask_json(self, system: str, prompt: str, schema: dict[str, Any]) -> Any:
        self.prompts.append(prompt)
        return self.replies.pop(0)


def raw_ideas(n: int, start: int = 0) -> dict:
    return {
        "ideas": [
            {"title": f"T{start + i}", "hook": "h", "format": "reel", "summary": "s"}
            for i in range(n)
        ]
    }


def test_generate_ideas_asks_again_until_it_has_enough_and_renumbers():
    model = FakeModel([raw_ideas(12), raw_ideas(10, start=12)])
    ideas = generate_ideas(model, "objective", "creator", count=20)
    assert [i.id for i in ideas] == list(range(1, 21))
    assert "8 more" in model.prompts[1]


def test_generate_ideas_skips_blank_and_duplicate_titles():
    reply = raw_ideas(3)
    reply["ideas"].append({"title": "t0", "hook": "", "format": "", "summary": ""})
    reply["ideas"].append({"title": "  ", "hook": "", "format": "", "summary": ""})
    ideas = generate_ideas(FakeModel([reply]), "o", "c", count=3)
    assert [i.title for i in ideas] == ["T0", "T1", "T2"]


def test_generate_ideas_fails_clearly_when_model_keeps_returning_nothing():
    with pytest.raises(RuntimeError, match="only 0 of 5"):
        generate_ideas(FakeModel([{"ideas": []}] * 3), "o", "c", count=5)


def test_score_ideas_clamps_and_ignores_unknown_ids():
    ideas = [Idea(1, "a", "", "", ""), Idea(2, "b", "", "", "")]
    reply = {
        "scores": [
            {"id": 1, "originality": 12, "relatability": 7, "emotional": 0, "reason": "r"},
            {"id": 42, "originality": 5, "relatability": 5, "emotional": 5, "reason": ""},
        ]
    }
    scores = score_ideas(FakeModel([reply, {"scores": []}, {"scores": []}]), "o", "c", ideas)
    assert list(scores) == [1]
    assert (scores[1].originality, scores[1].emotional) == (10, 1)


def scores_for(*ids: int) -> dict:
    return {"scores": [
        {"id": i, "originality": 5, "relatability": 5, "emotional": 5, "reason": ""} for i in ids
    ]}


def test_score_ideas_scores_in_batches_of_five():
    ideas = [Idea(i, str(i), "", "", "") for i in range(1, 8)]
    model = FakeModel([scores_for(1, 2, 3, 4, 5), scores_for(6, 7)])
    assert sorted(score_ideas(model, "o", "c", ideas)) == list(range(1, 8))
    assert len(model.prompts) == 2


def test_score_ideas_asks_again_for_ideas_the_model_skipped():
    ideas = [Idea(i, str(i), "", "", "") for i in (1, 2, 3)]
    model = FakeModel([{"scores": []}, scores_for(1, 3), scores_for(2)])
    assert sorted(score_ideas(model, "o", "c", ideas)) == [1, 2, 3]
    assert '"id": 2' in model.prompts[2] and '"id": 1' not in model.prompts[2]


def test_find_angles_drops_unnamed_angles():
    reply = {
        "angles": [
            {"name": "Confession", "description": "d", "example_hook": "h"},
            {"name": "", "description": "d", "example_hook": "h"},
        ]
    }
    angles = find_angles(FakeModel([reply]), "o", "c", Idea(1, "a", "", "", ""))
    assert [a.name for a in angles] == ["Confession"]


def test_write_brief_keeps_idea_id_and_angle():
    reply = {
        "title": "Title", "hook": "Hook", "audience": "A", "core_message": "M",
        "beginning": "B", "middle": "Mi", "end": "E", "emotional_beat": "EB",
        "shots": ["one", "two"], "voiceover": "VO", "caption": "C", "call_to_action": "CTA",
    }
    brief = write_brief(FakeModel([reply]), "o", "c", Idea(7, "a", "", "", ""), Angle("Twist", "", ""))
    assert (brief.idea_id, brief.angle, brief.shots) == (7, "Twist", ("one", "two"))


def test_group_themes_cleans_up_model_output():
    ideas = [Idea(i, str(i), "", "", "") for i in (1, 2, 3)]
    reply = {"themes": [{"name": "A", "description": "", "idea_ids": [1, 1, 9]}]}
    themes = group_themes(FakeModel([reply]), "o", "c", ideas, theme_count=2)
    assert sorted(i for t in themes for i in t.idea_ids) == [1, 2, 3]


def test_group_themes_never_returns_more_themes_than_asked_for():
    ideas = [Idea(i, str(i), "", "", "") for i in range(1, 7)]
    reply = {"themes": [{"name": f"T{i}", "description": "", "idea_ids": [i]} for i in range(1, 7)]}
    themes = group_themes(FakeModel([reply]), "o", "c", ideas, theme_count=3)
    assert len(themes) == 3
    assert sorted(i for t in themes for i in t.idea_ids) == list(range(1, 7))
