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
        brief = {k: "x" for k in keys} | {"caption": "the the text", "voiceover": "I do it for my brother."}
        return brief | {"shots": ["a", "b"]}


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
    assert "## ⚠ Confirm before posting" in report
    assert "I do it for my brother." in report


def test_context_file_is_added_to_what_the_model_knows(tmp_path):
    creator = tmp_path / "creator.md"
    creator.write_text("A creator in Tauranga.")
    context = tmp_path / "campaign.md"
    context.write_text("Fight on 3 December.")
    args = engine.parse_args(["x", "--creator-file", str(creator), "--context-file", str(context)])
    background = engine.load_background(args)
    assert "A creator in Tauranga." in background and "Fight on 3 December." in background


def test_theme_count_is_capped_at_the_number_of_posting_days():
    assert engine.parse_args(["x", "--themes", "5", "--days", "mon,fri"]).themes == 2


def test_parse_args_rejects_unknown_weekdays():
    with pytest.raises(SystemExit):
        engine.parse_args(["x", "--days", "mon,funday"])


def test_next_monday_is_always_in_the_future():
    monday = dt.date(2026, 11, 16)
    assert engine.next_monday(monday) == monday + dt.timedelta(days=7)
    assert engine.next_monday(monday + dt.timedelta(days=2)) == monday + dt.timedelta(days=7)


def test_slug_is_short_and_url_safe():
    assert engine.slug("Get 1,000 new followers — by Christmas!") == "get-1-000-new-followers-by-christmas"


def test_milestones_are_parsed_and_shown_in_the_calendar(fake_model, tmp_path):
    args = engine.parse_args([
        "Fight", "--count", "6", "--top", "1", "--themes", "2", "--weeks", "1", "--days", "mon,thu",
        "--start", "2026-11-16", "--out", str(tmp_path),
        "--milestone", "2026-11-28=Fight night", "--milestone", "2026-11-19=Weigh-in",
    ])
    assert [(m.date.isoformat(), m.label) for m in args.milestones] == [
        ("2026-11-19", "Weigh-in"), ("2026-11-28", "Fight night"),
    ]
    report = (engine.run(args) / "plan.md").read_text()
    calendar = report.split("## 5. Content calendar")[1].split("## Grammar")[0]
    rows = [line for line in calendar.splitlines() if line.startswith("| ") and "Date" not in line]
    assert [r.split(" | ")[0] for r in rows] == ["| Mon 16 Nov", "| Thu 19 Nov", "| Thu 19 Nov", "| Sat 28 Nov"]
    assert "📍 **Weigh-in**" in rows[1] and "📍 **Fight night**" in rows[3]


def test_bad_milestones_are_rejected():
    with pytest.raises(SystemExit):
        engine.parse_args(["x", "--milestone", "28 Nov=Fight"])
