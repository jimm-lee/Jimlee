"""Flag claims in generated copy that the creator never gave the model.

Small models invent specifics to make a story land: numbers, family members,
illness, loss. On a charity or personal campaign that is risky, so every number
not found in the campaign facts, and every mention of family, illness or loss,
is listed for the creator to confirm or cut before posting.
"""

from __future__ import annotations

import re

from .models import FactFlag

LINK = re.compile(r"\S+\.(?:com|org|nz|net|io)\S*|https?://\S+", re.I)
PLACEHOLDER = re.compile(r"\[[^\]]*\]")
NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")

SENSITIVE_TERMS = (
    "brother", "brothers", "sister", "sisters", "mum", "mom", "mother", "dad", "father", "son", "daughter",
    "wife", "husband", "girlfriend", "boyfriend", "partner", "grandad", "grandfather", "nan", "grandmother",
    "uncle", "aunt", "cousin", "died", "death", "dead", "passed away", "lost", "loss", "grief", "ghost",
    "funeral", "cancer", "diagnosed", "depression", "anxiety", "suicide", "illness", "injury", "injured",
)


def _strip(text: str) -> str:
    return PLACEHOLDER.sub(" ", LINK.sub(" ", text))


def _numbers(text: str) -> list[str]:
    return [n.replace(",", "") for n in NUMBER.findall(text)]


def unsupported_numbers(text: str, facts: str) -> list[str]:
    """Numbers in `text` that never appear in `facts` (links and [placeholders] ignored)."""
    known = set(_numbers(facts))
    return list(dict.fromkeys(n for n in _numbers(_strip(text)) if n not in known))


def sensitive_mentions(text: str, facts: str) -> list[str]:
    """Family, illness and loss words in `text` that the facts don't mention."""
    cleaned = _strip(text).lower()
    known = facts.lower()
    return [
        term for term in SENSITIVE_TERMS
        if re.search(rf"\b{re.escape(term)}\b", cleaned) and not re.search(rf"\b{re.escape(term)}\b", known)
    ]


def check_brief_texts(texts: dict[str, str], facts: str) -> list[FactFlag]:
    """One flag per sentence that contains an unsupported number or a sensitive mention."""
    flags: list[FactFlag] = []
    for item, text in texts.items():
        for sentence in SENTENCE_END.split(text.strip()):
            numbers = unsupported_numbers(sentence, facts)
            terms = sensitive_mentions(sentence, facts)
            reasons = []
            if numbers:
                reasons.append("number not in your facts: " + ", ".join(numbers))
            if terms:
                reasons.append("mentions " + ", ".join(terms) + "; is this true and yours to share?")
            if reasons:
                flags.append(FactFlag(item=item, message="; ".join(reasons), excerpt=sentence.strip()))
    return flags
