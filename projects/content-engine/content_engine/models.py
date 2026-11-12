"""Immutable records passed between pipeline steps."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

SCORE_MIN = 1
SCORE_MAX = 10


@dataclass(frozen=True)
class Idea:
    id: int
    title: str
    hook: str
    format: str
    summary: str


@dataclass(frozen=True)
class Score:
    idea_id: int
    originality: int
    relatability: int
    emotional: int
    reason: str

    @property
    def total(self) -> float:
        return round((self.originality + self.relatability + self.emotional) / 3, 1)


@dataclass(frozen=True)
class Angle:
    name: str
    description: str
    example_hook: str


@dataclass(frozen=True)
class Brief:
    idea_id: int
    title: str
    angle: str
    hook: str
    audience: str
    core_message: str
    beginning: str
    middle: str
    end: str
    emotional_beat: str
    shots: tuple[str, ...]
    voiceover: str
    caption: str
    call_to_action: str


@dataclass(frozen=True)
class Theme:
    name: str
    description: str
    idea_ids: tuple[int, ...]


@dataclass(frozen=True)
class Slot:
    date: dt.date
    theme: str
    idea_id: int | None


@dataclass(frozen=True)
class GrammarIssue:
    item: str
    rule: str
    message: str
    excerpt: str
    suggestion: str


@dataclass(frozen=True)
class FactFlag:
    item: str
    message: str
    excerpt: str


@dataclass(frozen=True)
class Milestone:
    date: dt.date
    label: str
