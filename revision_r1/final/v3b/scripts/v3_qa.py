"""QA for the v3 build: placeholders, internal codes, number preservation, book cross-check of the manuscript text."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter

from v3_common import SRC, V3

OUT = []
def log(*a):
    OUT.append(" ".join(str(x) for x in a)); print(*a)

# 1 placeholders and internal codes in every v3 text output
files = list((V3 / "ma").glob("*_v3.md")) + list((V3 / "tables").glob("*_v3.md"))
CODE = [r"\{\{", r"\[\[MA:", r"\bR1\b", r"Batch [0-9]", r"Version 2", r"\(B[1-7]\)", r"\bB[1-7] ", r"\(A[1-4]\)", r"\bT[1-9]\b",
        r"\.py\b", r"\.csv\b", r"\bnan\b", r"narrative", r"unchanged from the submi", r"numbers book", r"\bD[1-3]\b"]
for f in files:
    t = f.read_text(encoding="utf-8")
    for pat in CODE:
        hits = [t[max(0, m.start() - 50):m.end() + 30].replace("\n", " ") for m in re.finditer(pat, t)]
        if hits and not (f.name.startswith("Multimedia_Appendix_1") and pat in (r"\.py\b", r"\.csv\b", r"\bT[1-9]\b", r"narrative", r"numbers book")):
            log(f"[codes] {f.name} {pat}: {len(hits)}", hits[:3])

# 2 numbers preserved in edited units (multiset of numeric tokens, old vs new)
NUM = re.compile(r"-?\d+(?:[.,]\d+)*")
UT_IN, UT = SRC / "ma" / "units" / "tables", V3 / "ma" / "units" / "tables"
def unit_text(s):
    return "\n".join([s["caption"]] + s["header"] + ["\t".join(map(str, r)) for r in s["rows"]] + s["notes"])
for p in sorted(UT.glob("*.json")):
    uid = p.stem
    src = UT_IN / f"{uid}_v2.json"
    src = src if src.exists() else UT_IN / f"{uid}.json"
    if not src.exists():
        continue
    a = Counter(NUM.findall(unit_text(json.loads(src.read_text()))))
    b = Counter(NUM.findall(unit_text(json.loads(p.read_text()))))
    gone, added = a - b, b - a
    if gone or added:
        log(f"[numbers] {uid}: removed {dict(gone)} | added {dict(added) if sum(added.values()) < 40 else str(sum(added.values())) + ' tokens'}")

# 3 manuscript numbers vs numbers book (every percentage, OR and CI bound must exist in the book or in a v3 table)
book_txt = (SRC / "NUMBERS_BOOK_R1_v2.csv").read_text(encoding="utf-8")
v3_txt = "\n".join(f.read_text(encoding="utf-8") for f in files)
pool = book_txt + "\n" + v3_txt + "\n" + (SRC / "ma" / "new_tables" / "MA3_period_correction.md").read_text()
for sec in ("Methods_r1_Claude_v2", "Results_r1_Claude_v3_tracked", "Discussion_r1_Claude_v2_tracked"):
    t = (V3 / "manuscript_text" / f"{sec}.txt").read_text(encoding="utf-8").replace("–", "-")
    toks = set(re.findall(r"\d+\.\d+%?|\d+/\d[\d,]*", t))
    miss = sorted(x for x in toks if x not in pool and x.rstrip("%") not in pool)
    log(f"[text vs book] {sec}: {len(toks)} decimal/fraction tokens; not found in book or v3 tables: {miss}")
(V3 / "QA_v3.md").write_text("# QA v3\n\n" + "\n\n".join(OUT) + "\n", encoding="utf-8")
