import datetime as dt
import json
from typing import Any

import pytest

from content_engine import engine


class SchemaFake:
    """Answers each step based on which schema it was asked for."""

    def __init__(self, *_: Any, **__: Any) -> None:
        self.model = "fake"

    def ask_json(self, system: str, prompt: str, schema: dict[str, Any]) -> Any:
        keys = set(schema["properties"])
        if keys == {"ideas"}:
            return {"ideas": [
                {"title": f"Idea {n}", "hook": f"Hook {n}", "format": "reel", "summary": "s"} for n in range(6)
            ]}
        if keys == {"scores"}:
            return {"scores": [
                {"id": n, "originality": n, "relatability": 5, "emotional": 5, "reason": "r"} for n in range(1, 7)
            ]}
        if keys == {"angles"}:
            return {"angles": [{"name": "Confession", "description": "d", "example_hook": "h"}]}
        if keys == {"themes"}:
            return {"themes": [
                {"name": "Cold Mondays", "description": "d", "idea_ids": [1, 2, 3]},
                {"name": "Table talk", "description": "d", "idea_ids": [4, 5, 6]},
            ]}
        return {k: "the the text" if k == "caption" else "x" for k in keys} | {"shots": ["a", "b"]}


@pytest.fixture
def fake_model(monkeypatch):
    monkeypatch.setattr(engine, "OllamaClient", SchemaFake)


def test_full_run_writes_report_and_json(fake_model, tmp_path):
    args = engine.parse_args([
        "Grow saves", "--count", "6", "--top", "2", "--themes", "2", "--weeks", "2",
        "--days", "mon,thu", "--start", "2026-11-16", "--out", str(tmp_path),
    ])
    out = engine.run(args)

    report = (out / "plan.md").read_text()
    data = json.loads((out / "plan.json").read_text())
    assert "## 5. Content calendar" in report
    assert "#6 ★ Idea 5" in report  # idea 6 scored highest, so it leads and is briefed
    assert data["selected_ids"] == [6, 5]
    assert [s["theme"] for s in data["calendar"]] == ["Cold Mondays", "Table talk"] * 2
    assert len(data["briefs"]) == 2


def test_parse_args_rejects_unknown_weekdays():
    with pytest.raises(SystemExit):
        engine.parse_args(["x", "--days", "mon,funday"])


def test_next_monday_is_always_in_the_future():
    monday = dt.date(2026, 11, 16)
    assert engine.next_monday(monday) == monday + dt.timedelta(days=7)
    assert engine.next_monday(monday + dt.timedelta(days=2)) == monday + dt.timedelta(days=7)


def test_slug_is_short_and_url_safe():
    assert engine.slug("Get 1,000 new followers — by Christmas!") == "get-1-000-new-followers-by-christmas"
