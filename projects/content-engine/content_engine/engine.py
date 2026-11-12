"""Run the whole pipeline: ideas -> scores -> angles -> briefs -> calendar -> Harper check."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import re
from dataclasses import asdict
from pathlib import Path

from . import steps
from .calendar_plan import build_calendar
from .harper_check import check_texts
from .models import Angle, Brief, Idea
from .ollama_client import DEFAULT_HOST, DEFAULT_MODEL, OllamaClient
from .report import Plan, render
from .scoring import rank, select_top

log = logging.getLogger("content_engine")

PROJECT_DIR = Path(__file__).resolve().parent.parent
WEEKDAYS = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
FALLBACK_ANGLE = Angle("Straight story", "Tell it as it happened.", "")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Turn one campaign objective into ideas, briefs and a content calendar.")
    parser.add_argument("objective", help="The campaign objective, in a sentence or two.")
    parser.add_argument("--creator-file", type=Path, default=PROJECT_DIR / "creator.md", help="Who the content is for and about.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Ollama address.")
    parser.add_argument("--count", type=int, default=20, help="How many ideas to generate.")
    parser.add_argument("--top", type=int, default=5, help="How many top ideas get angles and briefs.")
    parser.add_argument("--themes", type=int, default=3, help="How many recurring themes.")
    parser.add_argument("--weeks", type=int, default=4, help="Calendar length in weeks.")
    parser.add_argument("--days", default="mon,wed,fri", help="Posting days, e.g. mon,wed,fri.")
    parser.add_argument("--start", type=dt.date.fromisoformat, default=None, help="Calendar start date (YYYY-MM-DD); default next Monday.")
    parser.add_argument("--out", type=Path, default=None, help="Output folder; default runs/<date>-<objective>.")
    parser.add_argument("--no-harper", action="store_true", help="Skip the Harper grammar check.")
    args = parser.parse_args(argv)
    try:
        args.post_weekdays = tuple(WEEKDAYS[d.strip().lower()[:3]] for d in args.days.split(","))
    except KeyError:
        parser.error(f"--days must be weekday names like mon,wed,fri (got {args.days!r})")
    if min(args.count, args.top, args.themes, args.weeks) < 1:
        parser.error("--count, --top, --themes and --weeks must all be at least 1")
    posting_days = len(set(args.post_weekdays))
    if args.themes > posting_days:
        log.warning("Only %d posting days, so using %d themes (each day owns one).", posting_days, posting_days)
        args.themes = posting_days
    return args


def next_monday(today: dt.date) -> dt.date:
    return today + dt.timedelta(days=(7 - today.weekday()) % 7 or 7)


def slug(text: str, limit: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:limit].rstrip("-")


def texts_to_check(ideas: list[Idea], briefs: list[Brief]) -> dict[str, str]:
    texts = {f"idea-{i.id:02d}-hook": i.hook for i in ideas if i.hook}
    for b in briefs:
        for field in ("hook", "voiceover", "caption", "call_to_action"):
            value = getattr(b, field)
            if value:
                texts[f"brief-{b.idea_id:02d}-{field.replace('_', '-')}"] = value
    return texts


def run(args: argparse.Namespace) -> Path:
    creator = args.creator_file.read_text(encoding="utf-8").strip()
    model = OllamaClient(model=args.model, host=args.host)
    today = dt.date.today()

    log.info("1/5 Generating %d ideas with %s…", args.count, args.model)
    ideas = steps.generate_ideas(model, args.objective, creator, args.count)

    log.info("2/5 Scoring ideas…")
    ranked = rank(ideas, steps.score_ideas(model, args.objective, creator, ideas))
    selected = [idea for idea, _ in select_top(ranked, args.top)]

    angles: dict[int, tuple[Angle, ...]] = {}
    briefs: list[Brief] = []
    for n, idea in enumerate(selected, start=1):
        log.info("3-4/5 Angles and brief %d/%d: %s", n, len(selected), idea.title)
        angles[idea.id] = tuple(steps.find_angles(model, args.objective, creator, idea))
        chosen = angles[idea.id][0] if angles[idea.id] else FALLBACK_ANGLE
        briefs.append(steps.write_brief(model, args.objective, creator, idea, chosen))

    log.info("5/5 Grouping %d recurring themes and building the calendar…", args.themes)
    themes = steps.group_themes(model, args.objective, creator, ideas, args.themes)
    calendar = build_calendar(themes, [i.id for i, _ in ranked], args.start or next_monday(today), args.weeks, args.post_weekdays)

    grammar = None
    if not args.no_harper:
        log.info("Checking the copy with Harper…")
        found = check_texts(texts_to_check(ideas, briefs))
        grammar = tuple(found) if found is not None else None

    plan = Plan(
        objective=args.objective, model=args.model, created=today.isoformat(),
        ideas=tuple(ideas), ranked=tuple(ranked), selected_ids=tuple(i.id for i in selected),
        angles=angles, briefs=tuple(briefs), themes=themes, calendar=tuple(calendar), grammar=grammar,
    )
    out = args.out or PROJECT_DIR / "runs" / f"{today.isoformat()}-{slug(args.objective)}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "plan.md").write_text(render(plan), encoding="utf-8")
    (out / "plan.json").write_text(json.dumps(asdict(plan), indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    out = run(parse_args(argv))
    log.info("Done: %s", out / "plan.md")


if __name__ == "__main__":
    main()
