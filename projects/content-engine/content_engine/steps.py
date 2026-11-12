"""The five pipeline steps. Each asks the model for schema-shaped JSON and cleans it up."""

from __future__ import annotations

import json
import logging
from typing import Any

from . import prompts
from .calendar_plan import normalise_themes
from .models import Angle, Brief, Idea, Score, Theme
from .ollama_client import JsonModel
from .scoring import clamp_score

log = logging.getLogger(__name__)

MAX_IDEA_ROUNDS = 3
MAX_SCORE_ROUNDS = 3
SCORE_BATCH = 5


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def generate_ideas(model: JsonModel, objective: str, creator: str, count: int = 20) -> list[Idea]:
    """Step 1: `count` distinct ideas, asking again if the model comes up short."""
    collected: list[dict[str, str]] = []
    titles: set[str] = set()
    for _ in range(MAX_IDEA_ROUNDS):
        missing = count - len(collected)
        if missing <= 0:
            break
        prompt = prompts.ideas_prompt(objective, missing, [c["title"] for c in collected], first=not collected)
        reply = model.ask_json(prompts.system(creator), prompt, prompts.IDEAS_SCHEMA)
        for raw in reply.get("ideas", []):
            title = _text(raw.get("title"))
            if not title or title.lower() in titles:
                continue
            titles.add(title.lower())
            collected.append({k: _text(raw.get(k)) for k in ("title", "hook", "format", "summary")})
    if len(collected) < count:
        raise RuntimeError(f"The model produced only {len(collected)} of {count} ideas; try again or use a larger model.")
    return [Idea(id=n, **fields) for n, fields in enumerate(collected[:count], start=1)]


def score_ideas(model: JsonModel, objective: str, creator: str, ideas: list[Idea]) -> dict[int, Score]:
    """Step 2: originality, relatability and emotional potential, 1-10 each.

    Small models sometimes return nothing for a long list, so ideas are scored in
    batches and any the model skips are asked about again.
    """
    scores: dict[int, Score] = {}
    for _ in range(MAX_SCORE_ROUNDS):
        missing = [idea for idea in ideas if idea.id not in scores]
        for start in range(0, len(missing), SCORE_BATCH):
            batch = missing[start:start + SCORE_BATCH]
            prompt = prompts.score_prompt(objective, _ideas_json(batch))
            reply = model.ask_json(prompts.system(creator), prompt, prompts.SCORES_SCHEMA)
            scores.update(_parse_scores(reply, {idea.id for idea in batch} - set(scores)))
    unscored = [idea.id for idea in ideas if idea.id not in scores]
    if unscored:
        log.warning("The model never scored ideas %s; they rank last.", unscored)
    return scores


def _parse_scores(reply: Any, wanted: set[int]) -> dict[int, Score]:
    scores: dict[int, Score] = {}
    for raw in reply.get("scores", []):
        idea_id = _int_or_none(raw.get("id"))
        if idea_id not in wanted or idea_id in scores:
            continue
        scores[idea_id] = Score(
            idea_id=idea_id,
            originality=clamp_score(raw.get("originality")),
            relatability=clamp_score(raw.get("relatability")),
            emotional=clamp_score(raw.get("emotional")),
            reason=_text(raw.get("reason")),
        )
    return scores


def find_angles(model: JsonModel, objective: str, creator: str, idea: Idea) -> list[Angle]:
    """Step 3: different storytelling angles on one idea."""
    reply = model.ask_json(prompts.system(creator), prompts.angles_prompt(objective, _idea_json(idea)), prompts.ANGLES_SCHEMA)
    angles = [
        Angle(_text(a.get("name")), _text(a.get("description")), _text(a.get("example_hook")))
        for a in reply.get("angles", [])
    ]
    return [a for a in angles if a.name]


def write_brief(model: JsonModel, objective: str, creator: str, idea: Idea, angle: Angle) -> Brief:
    """Step 4: a creative brief for one idea, told through the chosen angle."""
    prompt = prompts.brief_prompt(objective, _idea_json(idea), json.dumps(angle.__dict__))
    raw = model.ask_json(prompts.system(creator), prompt, prompts.BRIEF_SCHEMA)
    fields = {k: _text(raw.get(k)) for k in prompts.BRIEF_TEXT_FIELDS}
    return Brief(
        idea_id=idea.id,
        angle=angle.name,
        shots=tuple(_text(s) for s in raw.get("shots", []) if _text(s)),
        **fields,
    )


def group_themes(model: JsonModel, objective: str, creator: str, ideas: list[Idea], theme_count: int = 3) -> tuple[Theme, ...]:
    """Step 5a: recurring themes the calendar is built around."""
    prompt = prompts.themes_prompt(objective, _ideas_json(ideas), theme_count)
    reply = model.ask_json(prompts.system(creator), prompt, prompts.THEMES_SCHEMA)
    themes = [
        Theme(
            _text(t.get("name")) or f"Theme {n}",
            _text(t.get("description")),
            tuple(i for i in (_int_or_none(x) for x in t.get("idea_ids", [])) if i is not None),
        )
        for n, t in enumerate(reply.get("themes", []), start=1)
    ]
    return normalise_themes(themes, ideas)


def _idea_json(idea: Idea) -> str:
    return json.dumps(idea.__dict__, ensure_ascii=False)


def _ideas_json(ideas: list[Idea]) -> str:
    return json.dumps([idea.__dict__ for idea in ideas], ensure_ascii=False, indent=1)
