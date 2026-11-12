"""Prompt text and JSON schemas for each step.

The prompts lean on the Stage 1 storytelling fundamentals: three-act structure,
curiosity hooks, emotional storytelling (relatability and vulnerability),
audience psychology (why people watch and share) and natural voice-over.
"""

from __future__ import annotations

from typing import Any

BRIEF_TEXT_FIELDS = (
    "title", "hook", "audience", "core_message", "beginning", "middle", "end",
    "emotional_beat", "voiceover", "caption", "call_to_action",
)


def system(creator: str) -> str:
    return (
        "You are a short-form video story editor helping one creator plan Instagram reels.\n"
        f"About the creator:\n{creator}\n\n"
        "Principles you always apply:\n"
        "- Every piece has a beginning, middle and end, even at 15-30 seconds.\n"
        "- Hooks create curiosity in the first two seconds; never start with a greeting.\n"
        "- Ordinary, relatable moments and honest vulnerability beat impressive footage.\n"
        "- People share things that say something about themselves; people save things they will use.\n"
        "- Voice-over and captions sound like a person talking, not an advert.\n"
        "Never invent facts about the creator: no family members, relationships, illnesses, injuries, losses, "
        "past events, weights, times or statistics beyond what you were told. If a story needs a personal detail "
        "you weren't given, write it as a [placeholder] in square brackets for the creator to fill in.\n"
        "Write in New Zealand English. Be specific and concrete; avoid cliches like 'journey' and 'game-changer'."
    )


def ideas_prompt(objective: str, count: int, existing_titles: list[str], first: bool) -> str:
    avoid = "" if first else (
        f"\nYou already suggested these, so give {count} more that are clearly different:\n- "
        + "\n- ".join(existing_titles)
    )
    return (
        f"Campaign objective: {objective}\n\n"
        f"Generate {count} distinct content ideas for this objective. Mix formats "
        "(reel montage, talking to camera, POV, voice-over story, carousel) and emotional tones. "
        "For each, give a short title, the opening hook line (under 15 words), the format and a "
        "one-sentence summary of the story." + avoid
    )


def score_prompt(objective: str, ideas_json: str) -> str:
    return (
        f"Campaign objective: {objective}\n\nIdeas:\n{ideas_json}\n\n"
        "Score every idea from 1 to 10 on:\n"
        "- originality: would the audience have seen this many times before? (10 = fresh)\n"
        "- relatability: would an ordinary viewer see themselves in it? (10 = very)\n"
        "- emotional: how strongly could it make someone feel something? (10 = strongly)\n"
        "Be critical and use the whole range; most ideas should not score above 7. "
        "Give a one-sentence reason. Return one entry per idea using its id."
    )


def angles_prompt(objective: str, idea_json: str) -> str:
    return (
        f"Campaign objective: {objective}\nIdea: {idea_json}\n\n"
        "Suggest 4 different storytelling angles for this idea, such as a confession, "
        "a before-and-after transformation, a contrarian take, a POV, a list, a letter to "
        "someone, or a small everyday moment that stands for something bigger. "
        "For each, name the angle, explain in one sentence how the story would be told, "
        "and write an example hook. Put the angle you think is strongest first."
    )


def brief_prompt(objective: str, idea_json: str, angle_json: str) -> str:
    return (
        f"Campaign objective: {objective}\nIdea: {idea_json}\nAngle: {angle_json}\n\n"
        "Write a creative brief for a 15-30 second vertical reel told through this angle. "
        "It must work without impressive footage: the story carries it. Include the title, "
        "the hook (on-screen caption, under 15 words), the audience, the one core message, "
        "the beginning, middle and end (one or two sentences each), the emotional beat, "
        "4-7 shots that the creator could film on a phone, a natural spoken voice-over script "
        "of at most 60 words, the post caption, and a soft call to action."
    )


def themes_prompt(objective: str, ideas_json: str, theme_count: int) -> str:
    return (
        f"Campaign objective: {objective}\n\nIdeas:\n{ideas_json}\n\n"
        f"Group these ideas into exactly {theme_count} recurring content themes the audience "
        "would come to expect each week (for example a weekly series). Give each theme a short, "
        "catchy name, a one-sentence description, and the ids of the ideas that belong to it. "
        "Every idea id must appear in exactly one theme."
    )


def _object(properties: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "properties": properties, "required": list(properties)}


def _list_of(item: dict[str, Any]) -> dict[str, Any]:
    return {"type": "array", "items": item}


STRING: dict[str, Any] = {"type": "string"}
INTEGER: dict[str, Any] = {"type": "integer"}

IDEAS_SCHEMA = _object({"ideas": _list_of(_object(
    {"title": STRING, "hook": STRING, "format": STRING, "summary": STRING}
))})

SCORES_SCHEMA = _object({"scores": _list_of(_object(
    {"id": INTEGER, "originality": INTEGER, "relatability": INTEGER, "emotional": INTEGER, "reason": STRING}
))})

ANGLES_SCHEMA = _object({"angles": _list_of(_object(
    {"name": STRING, "description": STRING, "example_hook": STRING}
))})

BRIEF_SCHEMA = _object({
    **{field: STRING for field in BRIEF_TEXT_FIELDS},
    "shots": _list_of(STRING),
})

THEMES_SCHEMA = _object({"themes": _list_of(_object(
    {"name": STRING, "description": STRING, "idea_ids": _list_of(INTEGER)}
))})
