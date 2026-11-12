"""Grammar and spelling checks with Harper (https://github.com/Automattic/harper).

Harper runs locally, so nothing the model writes leaves the machine.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

from .models import GrammarIssue

log = logging.getLogger(__name__)

# Harper has no New Zealand dialect; Australian is the closest (colour, organise, practise).
DEFAULT_DIALECT = "au"
DICTIONARY = Path(__file__).resolve().parent.parent / "dictionary.txt"
HARPER_TIMEOUT_S = 300


def parse_harper_json(output: str) -> list[GrammarIssue]:
    """Turn `harper-cli lint --format json` output into issues keyed by file stem."""
    issues: list[GrammarIssue] = []
    for file_result in json.loads(output):
        item = Path(file_result["file"]).stem
        for lint in file_result.get("lints", []):
            suggestions = lint.get("suggestions") or []
            issues.append(GrammarIssue(
                item=item,
                rule=lint.get("rule", ""),
                message=lint.get("message", ""),
                excerpt=lint.get("matched_text", ""),
                suggestion=suggestions[0] if suggestions else "",
            ))
    return issues


def check_texts(
    texts: dict[str, str], harper_bin: str = "harper-cli", dialect: str = DEFAULT_DIALECT
) -> list[GrammarIssue] | None:
    """Lint each text separately. Returns None if Harper is not installed.

    Keys become file names, so they should be short slugs like `brief-03-caption`.
    """
    binary = shutil.which(harper_bin)
    if binary is None:
        log.warning("%s not found; skipping the grammar check.", harper_bin)
        return None
    with tempfile.TemporaryDirectory() as folder:
        paths = []
        for key, text in texts.items():
            path = Path(folder) / f"{key}.txt"
            path.write_text(text + "\n", encoding="utf-8")
            paths.append(str(path))
        command = [binary, "lint", "--format", "json", "--quiet", "--dialect", dialect]
        if DICTIONARY.exists():
            command += ["--user-dict-path", str(DICTIONARY)]
        result = subprocess.run(
            command + paths, capture_output=True, text=True, timeout=HARPER_TIMEOUT_S, check=False
        )
    if not result.stdout.strip():
        log.warning("Harper produced no output (exit %s): %s", result.returncode, result.stderr.strip()[:300])
        return None
    issues = parse_harper_json(result.stdout)
    order = {key: index for index, key in enumerate(texts)}
    return sorted(issues, key=lambda issue: order.get(issue.item, len(order)))
