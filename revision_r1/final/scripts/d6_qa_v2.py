"""Batch 2d · QA of the v2 outputs against NUMBERS_BOOK_R1_v2.csv, reusing the Batch 2c checks
(c6_qa.book_numbers / check_text, imported). Run with revision_r1/.venv.
Output: revision_r1/final/QA_batch2d.md
"""

from __future__ import annotations

import csv
import json
import re

import c_common as _cc
_cc.BOOK_CSV = _cc.FINAL / "NUMBERS_BOOK_R1_v2.csv"
import c6_qa as Q  # noqa: E402  (BOOK is read from the v2 book at import)
from docx import Document  # noqa: E402

FINAL, MA = _cc.FINAL, _cc.MA


def main():
    rows = []
    ids = {}
    for f, key in ((FINAL / "tables/table_ids_used_v2.csv", "table"), (FINAL / "figures/figure_ids_used_v2.csv", "figure"),
                   (MA / "new_tables/new_tables_ids_used.csv", "table")):
        for r in csv.DictReader(open(f)):
            ids.setdefault(r[key], set()).add(r["id"])
    for name in ("Table2", "Table3"):
        Q.check_text(f"Main {name}_v2", (FINAL / f"tables/{name}_v2.md").read_text(), Q.book_numbers(ids[name]), rows)
    for name in ("Fig2", "Fig3"):
        Q.check_text(f"Main {name}_caption_v2", (FINAL / f"figures/{name}_caption_v2.md").read_text(), Q.book_numbers(ids[name]), rows)
    for f in sorted((MA / "units/tables").glob("*_v2.json")):
        spec = json.loads(f.read_text())
        txt = " | ".join([spec["caption"]] + spec["header"] + [" | ".join(map(str, r)) for r in spec["rows"]] + spec["notes"])
        pts = [float(Q.BOOK[i]["point"]) for i in spec["book_ids"] if Q.BOOK[i]["point"] not in ("", None)]
        Q.check_text(f"MA3 unit {f.stem}", txt, Q.book_numbers(spec["book_ids"]), rows, pts)
    for f in sorted((MA / "units/figures").glob("*_caption_v2.md")):
        stem = f.stem.replace("_caption_v2", "")
        bid = json.loads((MA / "units/figures" / f"{stem}.json").read_text())["book_ids"]
        Q.check_text(f"MA2 unit {f.stem}", f.read_text(), Q.book_numbers(bid), rows)
    for name in ("MA3_lexicon_decomposition", "MA3_period_correction"):
        Q.check_text(f"New {name}", (MA / f"new_tables/{name}.md").read_text(), Q.book_numbers(ids[name]), rows)
    tot = sum(r[1] for r in rows); bad = [(w, t, c) for w, _, b in rows for t, c in b]
    L = ["# QA · Batch 2d outputs (v2)\n", "Script: `revision_r1/final/scripts/d6_qa_v2.py` (reuses the Batch 2c checks). Each "
         "table or caption is matched only against the v2 book rows its builder read.\n",
         f"Numeric tokens checked: {tot:,} in {len(rows)} tables/captions; left for review: {len(bad)}.\n",
         "| Table or caption | Tokens | Not matched |", "|---|---|---|"]
    for w, n, b in rows:
        L.append(f"| {w} | {n} | {'none' if not b else '; '.join(f'`{t}`: …{c}…' for t, c in b).replace('|', '/')} |")
    L.append("\n## Word tables\n")
    for f in [FINAL / "tables/Table2_v2.docx", FINAL / "tables/Table3_v2.docx", MA / "Multimedia_Appendix_3_R1_v2.docx",
              MA / "new_tables/MA3_lexicon_decomposition.docx", MA / "new_tables/MA3_period_correction.docx"]:
        d = Document(str(f))
        L.append(f"- {f.relative_to(FINAL)}: {len(d.tables)} Word table(s), {len(d.inline_shapes)} images")
    L.append("\n## Format scan\n")
    files = [FINAL / "tables/Table2_v2.md", FINAL / "tables/Table3_v2.md", FINAL / "figures/Fig2_caption_v2.md",
             FINAL / "figures/Fig3_caption_v2.md", MA / "Multimedia_Appendix_3_R1_v2.md", MA / "Multimedia_Appendix_2_R1_v2.md",
             MA / "new_tables/MA3_lexicon_decomposition.md", MA / "new_tables/MA3_period_correction.md"]
    for lab, pat in (("lowercase p value", r"(?<![A-Za-z])p\s?[=<]\s?0?\.\d"), ("leading zero in P", r"P\s?[=<>]\s?0\.\d"),
                     ("Cohen's", r"Cohen['’]s"), ("comma in a 4-digit number", r"(?<![\d,.])\d,\d{3}(?![\d,])"),
                     ("en dash in a range", r"\d–\d"), ("'Wald CI' left in a v2 file", r"Wald CI")):
        hits = [f"{f.name} ({len(re.findall(pat, f.read_text()))})" for f in files if re.search(pat, f.read_text())]
        L.append(f"- {lab}: {'none' if not hits else ', '.join(hits)}")
    (FINAL / "QA_batch2d.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"QA v2: {tot} tokens, {len(bad)} left for review")
    for b in bad:
        print(b)


if __name__ == "__main__":
    main()
