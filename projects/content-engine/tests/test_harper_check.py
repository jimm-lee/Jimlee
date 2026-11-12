import json
import shutil

import pytest

from content_engine.harper_check import check_texts, parse_harper_json

HARPER_OUTPUT = json.dumps([
    {
        "file": "/tmp/x/brief-03-caption.txt",
        "lint_count": 1,
        "lints": [{
            "rule": "RepeatedWords", "kind": "Repetition", "span": {"char_start": 0, "char_end": 7},
            "line": 1, "column": 1, "message": "Did you mean to repeat this word?",
            "priority": 63, "suggestions": ["the"], "matched_text": "the the",
        }],
    },
    {"file": "/tmp/x/idea-01-hook.txt", "lint_count": 0, "lints": []},
])


def test_parse_maps_each_lint_back_to_its_item():
    issues = parse_harper_json(HARPER_OUTPUT)
    assert len(issues) == 1
    issue = issues[0]
    assert (issue.item, issue.rule, issue.excerpt, issue.suggestion) == (
        "brief-03-caption", "RepeatedWords", "the the", "the",
    )


def test_parse_handles_lints_without_suggestions():
    raw = json.loads(HARPER_OUTPUT)
    raw[0]["lints"][0]["suggestions"] = []
    assert parse_harper_json(json.dumps(raw))[0].suggestion == ""


def test_check_texts_returns_none_when_harper_is_not_installed():
    assert check_texts({"a": "text"}, harper_bin="definitely-not-harper") is None


@pytest.mark.skipif(shutil.which("harper-cli") is None, reason="harper-cli not installed")
def test_check_texts_finds_a_real_mistake_with_harper():
    issues = check_texts({"clean": "I went for a swim.", "broken": "I went for a a swim."})
    assert issues is not None
    assert [i.item for i in issues] == ["broken"]
