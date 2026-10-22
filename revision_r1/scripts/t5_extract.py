"""T5 helper: split the submitted manuscript (revision_r1/inputs/*.txt, made with
macOS textutil from the .docx) into numbered quantitative sentences for the
Abstract (A), Results body (R), figure captions (C) and Discussion (D)."""

import re

from r1_common import INPUTS

TXT = INPUTS / "Final Manuscript Submission LW jmir.txt"


def sections():
    t = TXT.read_text().split("\n")
    idx = lambda name, start=0: next(k for k, l in enumerate(t) if k >= start and l.strip() == name)
    a0 = idx("Abstract"); a1 = idx("Introduction", a0)
    r0 = idx("Results", a1); r1 = idx("Discussion", r0)
    d0 = r1; d1 = idx("Reflexivity", d0)
    return t[a0 + 1:a1], t[r0 + 1:r1], t[d0 + 1:d1]


def split(lines):
    out = []
    for l in lines:
        l = l.strip()
        if not l:
            continue
        for s in re.split(r"(?<=[.])\s+(?=[A-Z])", l):
            if re.search(r"\d", s):
                out.append(s.strip())
    return out


def quantitative_sentences():
    a, r, d = sections()
    caps = [l for l in r if l.strip().startswith("Figure ")]
    body = [l for l in r if not l.strip().startswith("Figure ")]
    rows = []
    for tag, lines, sec in [("A", a, "Abstract"), ("R", body, "Results"), ("C", caps, "Figure caption"),
                            ("D", d, "Discussion")]:
        for i, s in enumerate(split(lines), 1):
            rows.append((f"{tag}{i:02d}", sec, s))
    return rows


if __name__ == "__main__":
    for i, sec, s in quantitative_sentences():
        print(i, s)
