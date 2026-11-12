"""
title: Harper grammar check
description: Check spelling and grammar locally with Harper (Automattic/harper). Needs harper-cli on the Open WebUI machine.
version: 0.1.0
license: MIT
"""

import json
import shutil
import subprocess

from pydantic import BaseModel, Field

HARPER_TIMEOUT_S = 60


class Tools:
    class Valves(BaseModel):
        harper_bin: str = Field(default="harper-cli", description="Path or name of the harper-cli binary.")
        dialect: str = Field(default="au", description="us, uk, au, ca or in. Australian is closest to NZ English.")
        known_words: str = Field(
            default="Aotearoa,Aoraki,Wānaka,Wanaka,Tekapo,Tāmaki,Makaurau,Kiwi,Kiwis,Māori,Kia,ora,whānau,Movember,POV",
            description="Comma-separated words Harper should not flag as misspelt.",
        )

    def __init__(self) -> None:
        self.valves = self.Valves()

    def check_grammar(self, text: str) -> str:
        """
        Check a piece of writing (a caption, hook, voice-over or script) for spelling and grammar
        mistakes with Harper, and return each problem with a suggested fix. Use this whenever the
        user asks to proofread, check or polish text.
        :param text: The exact text to check.
        :return: A list of issues with suggestions, or a note that none were found.
        """
        binary = shutil.which(self.valves.harper_bin)
        if binary is None:
            return f"Harper is not installed ({self.valves.harper_bin} not found)."
        result = subprocess.run(
            [binary, "lint", "--format", "json", "--quiet", "--dialect", self.valves.dialect],
            input=text, capture_output=True, text=True, timeout=HARPER_TIMEOUT_S, check=False,
        )
        try:
            files = json.loads(result.stdout)
        except json.JSONDecodeError:
            return f"Harper failed: {result.stderr.strip()[:300]}"
        known = {w.strip().lower() for w in self.valves.known_words.split(",") if w.strip()}
        lints = [
            lint for f in files for lint in f.get("lints", [])
            if not (lint.get("rule") == "SpellCheck" and lint.get("matched_text", "").lower() in known)
        ]
        if not lints:
            return "Harper found no spelling or grammar issues."
        lines = [
            f"- “{l.get('matched_text', '')}”: {l.get('message', '')}"
            + (f" {l['suggestions'][0]}" if l.get("suggestions") else "")
            for l in lints
        ]
        return f"Harper found {len(lints)} issue(s):\n" + "\n".join(lines)
