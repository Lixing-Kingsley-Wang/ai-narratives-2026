"""Shared helpers for the Batch 2a human-coding instruments.

Codebook text is never retyped: classifier system prompts are read from the
source file with `ast` (no import, so no .env load or API client), and the
file's last commit hash and the prompt's SHA-256 are recorded alongside.
"""

from __future__ import annotations

import ast
import hashlib
import subprocess

from openpyxl.styles import Alignment, Font, PatternFill

from r1_common import REPO, R1

CODING = R1 / "coding"
CODING.mkdir(parents=True, exist_ok=True)
NO_ABSTRACT = "[No abstract available. Code from the title.]"
YELLOW = PatternFill("solid", fgColor="FFF2CC")
HEADER = PatternFill("solid", fgColor="D9D9D9")


def read_system_prompt(relpath: str) -> str:
    """Value of the module-level SYSTEM_PROMPT assignment, read via ast."""
    tree = ast.parse((REPO / relpath).read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "SYSTEM_PROMPT" for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f"SYSTEM_PROMPT not found in {relpath}")


def last_commit(relpath: str) -> str:
    return subprocess.run(["git", "log", "-1", "--format=%H", "--", relpath], cwd=REPO,
                          capture_output=True, text=True, check=True).stdout.strip()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def block_between(prompt: str, start_marker: str, end_marker: str) -> str:
    """Verbatim slice of the prompt from start_marker up to (not including) end_marker."""
    i = prompt.index(start_marker)
    j = prompt.index(end_marker, i)
    return prompt[i:j].rstrip("\n")


def show_text(abstract) -> str:
    a = "" if abstract is None else str(abstract)
    return a if a.strip() else NO_ABSTRACT


def write_readme(ws, title: str, sections: list[tuple[str, str]]):
    """sections: (heading, body). Bodies are written one line per row so the
    verbatim prompt text keeps its line breaks."""
    ws.column_dimensions["A"].width = 120
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=14)
    r = 3
    for heading, body in sections:
        ws.cell(row=r, column=1, value=heading).font = Font(bold=True, size=12)
        r += 1
        for line in body.split("\n"):
            c = ws.cell(row=r, column=1, value=line)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            r += 1
        r += 1
    return r


def style_header(ws, ncols: int):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = Font(bold=True)
        cell.fill = HEADER
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "D2"
