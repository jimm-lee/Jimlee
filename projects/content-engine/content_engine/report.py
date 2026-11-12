"""Render a finished plan as Markdown."""

from __future__ import annotations

from dataclasses import dataclass

from .models import Angle, Brief, GrammarIssue, Idea, Score, Slot, Theme


@dataclass(frozen=True)
class Plan:
    objective: str
    model: str
    created: str
    ideas: tuple[Idea, ...]
    ranked: tuple[tuple[Idea, Score], ...]
    selected_ids: tuple[int, ...]
    angles: dict[int, tuple[Angle, ...]]
    briefs: tuple[Brief, ...]
    themes: tuple[Theme, ...]
    calendar: tuple[Slot, ...]
    grammar: tuple[GrammarIssue, ...] | None


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def render(plan: Plan) -> str:
    sections = [
        _header(plan),
        _ideas(plan),
        _scores(plan),
        _angles(plan),
        _briefs(plan),
        _calendar(plan),
        _grammar(plan),
    ]
    return "\n\n".join(sections) + "\n"


def _header(plan: Plan) -> str:
    return (
        f"# Content plan\n\n**Campaign objective:** {plan.objective}\n\n"
        f"Generated {plan.created} with `{plan.model}` on Ollama; copy checked with Harper. "
        f"The {len(plan.selected_ids)} highest-scoring ideas (★) get angles and full briefs."
    )


def _ideas(plan: Plan) -> str:
    rows = [f"| {i.id} | {cell(i.title)} | {cell(i.hook)} | {cell(i.format)} | {cell(i.summary)} |" for i in plan.ideas]
    return "## 1. Ideas\n\n| # | Title | Hook | Format | Story |\n|---|---|---|---|---|\n" + "\n".join(rows)


def _scores(plan: Plan) -> str:
    rows = []
    for position, (idea, score) in enumerate(plan.ranked, start=1):
        star = " ★" if idea.id in plan.selected_ids else ""
        rows.append(
            f"| {position} | {idea.id}{star} | {cell(idea.title)} | {score.originality} | "
            f"{score.relatability} | {score.emotional} | **{score.total}** | {cell(score.reason)} |"
        )
    return (
        "## 2. Scores\n\nOriginality, relatability and emotional potential, 1–10 each; total is the mean.\n\n"
        "| Rank | # | Title | Orig. | Relat. | Emot. | Total | Why |\n|---|---|---|---|---|---|---|---|\n"
        + "\n".join(rows)
    )


def _angles(plan: Plan) -> str:
    titles = {i.id: i.title for i in plan.ideas}
    parts = ["## 3. Storytelling angles\n\nThe first angle for each idea is the one its brief uses."]
    for idea_id in plan.selected_ids:
        lines = [
            f"- **{a.name}**{' (used)' if n == 0 else ''}: {a.description} *Hook:* \u201c{a.example_hook}\u201d"
            for n, a in enumerate(plan.angles.get(idea_id, ()))
        ]
        parts.append(f"### #{idea_id} {titles[idea_id]}\n\n" + "\n".join(lines or ["- (no angles returned)"]))
    return "\n\n".join(parts)


def _briefs(plan: Plan) -> str:
    parts = ["## 4. Creative briefs"]
    for b in plan.briefs:
        shots = "\n".join(f"{n}. {s}" for n, s in enumerate(b.shots, start=1))
        parts.append(
            f"### #{b.idea_id} {b.title}\n\n"
            f"| | |\n|---|---|\n"
            f"| **Angle** | {cell(b.angle)} |\n| **Hook** | {cell(b.hook)} |\n"
            f"| **Audience** | {cell(b.audience)} |\n| **Core message** | {cell(b.core_message)} |\n"
            f"| **Emotional beat** | {cell(b.emotional_beat)} |\n| **Call to action** | {cell(b.call_to_action)} |\n\n"
            f"**Beginning:** {b.beginning}\n\n**Middle:** {b.middle}\n\n**End:** {b.end}\n\n"
            f"**Shots**\n\n{shots}\n\n**Voice-over**\n\n> {b.voiceover}\n\n**Caption**\n\n> {b.caption}"
        )
    return "\n\n".join(parts)


def _calendar(plan: Plan) -> str:
    ideas = {i.id: i for i in plan.ideas}
    themes = "\n".join(f"- **{t.name}**: {t.description} ({len(t.idea_ids)} ideas)" for t in plan.themes)
    rows = []
    for slot in plan.calendar:
        idea = ideas.get(slot.idea_id) if slot.idea_id is not None else None
        what = f"#{idea.id}{' ★' if idea.id in plan.selected_ids else ''} {cell(idea.title)}" if idea else "*Open slot: repurpose or respond to the week*"
        hook = cell(idea.hook) if idea else ""
        rows.append(f"| {slot.date:%a %d %b} | {cell(slot.theme)} | {what} | {hook} |")
    return (
        "## 5. Content calendar\n\nEach posting day keeps the same theme every week so the audience knows what's coming.\n\n"
        f"{themes}\n\n| Date | Theme | Idea | Hook |\n|---|---|---|---|\n" + "\n".join(rows)
    )


def _grammar(plan: Plan) -> str:
    heading = "## Grammar check (Harper)"
    if plan.grammar is None:
        return f"{heading}\n\nSkipped: `harper-cli` is not installed."
    if not plan.grammar:
        return f"{heading}\n\nNo issues found in the hooks, voice-overs, captions or calls to action."
    rows = [
        f"| {cell(i.item)} | {cell(i.excerpt)} | {cell(i.message)} | {cell(i.suggestion)} |"
        for i in plan.grammar
    ]
    return (
        f"{heading}\n\n{len(plan.grammar)} things to look at. Harper checks against Australian English, "
        "the closest dialect it has to New Zealand English.\n\n"
        "| Where | Text | Issue | Suggestion |\n|---|---|---|---|\n" + "\n".join(rows)
    )
