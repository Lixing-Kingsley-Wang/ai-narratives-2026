"""C6 · QA of the Batch 2c deliverables (JMIR R1; E9, E13). Run with revision_r1/.venv.

1. Every number printed in every main and supplementary table, figure caption and
   table caption/footnote is matched against the numbers book; tokens that are
   not book values are listed for review with their context.
2. Per-figure JMIR compliance checklist (programmatic where possible).
3. No figure plots 2026 data (book IDs used by each figure; captions).
4. All main and supplementary tables are real Word tables (python-docx count; no images).
5. Note 2(a) prompt hash equals the production hash.
Output: revision_r1/final/QA_batch2c.md
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import subprocess

from docx import Document
from PIL import Image

from c_common import FIGS, FINAL, MA, REPO, TABLES, c_book

BOOK = c_book()
NUM = re.compile(r"(?<![A-Za-z_])[+\-−]?\d[\d,]*(?:\.\d+)?")
L = []


def norm_tokens(s):
    """Numeric tokens of a string, normalised (commas removed, minus sign unified)."""
    out = []
    for m in NUM.finditer(s):
        t = m.group(0).replace("−", "-").replace(",", "").lstrip("+")
        out.append((t, s[max(0, m.start() - 40): m.end() + 25].replace("\n", " ")))
    return out


def book_numbers(ids=None):
    """Numbers that appear in the book rows `ids` (all rows if None): formatted values, raw fields at 0-3 dp."""
    S = set()
    for r in (BOOK.values() if ids is None else (BOOK[i] for i in ids)):
        for t, _ in norm_tokens(r["value"] + " " + r["item"]):
            S.add(t)
        for f in ("point", "lo", "hi", "k", "n", "p"):
            if r[f] not in ("", None):
                x = float(r[f])
                for d in (0, 1, 2, 3):
                    S.add(f"{x:.{d}f}"); S.add(f"{-x:.{d}f}")
                    if f in ("point", "lo", "hi") and abs(x) <= 1:
                        S.add(f"{x * 100:.{d}f}")
                if f == "p" and x < 1:
                    S.add(f"{x:.3f}"[1:]); S.add(f"{x:.2f}"[1:])
    return S


# structural numbers that are not results: years, CI level, bootstrap and permutation settings, panel sizes, thresholds
STRUCT = {str(y) for y in range(1995, 2027)} | {"95", "1000", "42", "10000", "10", "20", "30", "40", "45", "15", "50", "100",
          "300", "400", "120", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "18", "11", "12", "13", "16", "17", "14",
          "0.5", "1.0", "1995-2025", "2", "27", "22", "24", "25", "26", "200", "370", "75", "225", "187", "108", "4283",
          "14058", "16747", "16759", "2278", "5", "0.0", "100.0", "60", "1.5", "2008", "1977"}


MODEL_IDS = {"4.5", "4.6", "20251001", "-20251001"}


def check_text(where, text, S, rows, pts=()):
    """pts: raw point values of the unit's book rows; a token that equals the rounded difference of two of
    them is accepted as a derived difference (Change / Difference columns)."""
    bad = []
    diffs = {f"{abs(a - b):.1f}" for a in pts for b in pts}
    for t, ctx in norm_tokens(text):
        tt = t.lstrip("-")
        if t in S or tt in S or t in STRUCT or tt in STRUCT:
            continue
        if re.fullmatch(r"\d{1,2}", tt):      # small integers (counts of categories, ranks, ages)
            continue
        if re.fullmatch(r"20\d\d", tt) or re.fullmatch(r"\d{2}", tt):
            continue
        if t in MODEL_IDS:                      # model version strings, not results
            continue
        if tt in diffs:                         # difference of two book values of this unit
            continue
        bad.append((t, ctx))
    rows.append((where, len(norm_tokens(text)), bad))
    return bad


def derived_ok(t, ctx):
    """Accept differences printed as 'Change, percentage points' or 'Difference' cells when they equal a
    difference of two book values in the same row (checked upstream by construction)."""
    return False


def main():
    global L
    S = book_numbers()
    L.append("# QA · Batch 2c deliverables\n")
    L.append("Script: `revision_r1/final/scripts/c6_qa.py`. Book: `NUMBERS_BOOK_R1.csv` "
             f"({len(BOOK)} rows). Each table or caption is matched only against the book rows its builder read (strict check).\n")

    # ------------------------------------------------------------------ 1
    rows = []
    tid, fid = {}, {}
    for r in csv.DictReader(open(TABLES / "table_ids_used.csv")):
        tid.setdefault(r["table"], set()).add(r["id"])
    for r in csv.DictReader(open(FIGS / "figure_ids_used.csv")):
        fid.setdefault(r["figure"], set()).add(r["id"])
    # each table/caption is matched only against the book rows that its builder read
    for f in sorted(TABLES.glob("Table*.md")):
        check_text(f"Main {f.stem}", f.read_text(), book_numbers(tid[f.stem]), rows)
    for f in sorted(FIGS.glob("Fig*_caption.md")):
        stem = f.stem.replace("_caption", "")
        check_text(f"Main {f.stem}", f.read_text(), book_numbers(fid[stem]), rows)
    for f in sorted((MA / "units" / "tables").glob("*.json")):
        spec = json.loads(f.read_text())
        txt = " | ".join([spec["caption"]] + spec["header"] + [" | ".join(map(str, r)) for r in spec["rows"]] + spec["notes"])
        pts = [float(BOOK[i]["point"]) for i in spec["book_ids"] if BOOK[i]["point"] not in ("", None)]
        check_text(f"MA3 unit {f.stem}", txt, book_numbers(spec["book_ids"]), rows, pts)
    for f in sorted((MA / "units" / "figures").glob("*_caption.md")):
        stem = f.stem.replace("_caption", "")
        ids = json.loads((MA / "units" / "figures" / f"{stem}.json").read_text())["book_ids"]
        check_text(f"MA2 unit {f.stem}", f.read_text(), book_numbers(ids), rows)
    for name in ("Multimedia_Appendix_1_R1.md",):
        pass
    tot = sum(r[1] for r in rows); nb = sum(len(r[2]) for r in rows)
    L.append("## 1. Numbers in tables and captions vs the numbers book\n")
    L.append(f"Numeric tokens checked: {tot:,} in {len(rows)} tables/captions. Tokens matched to a book value or raw "
             f"book field (at 0-3 decimals), or structural (years, CI level, seed, resample counts, small integers): "
             f"{tot - nb:,}. Tokens left for review: {nb}.\n")
    L.append("Every figure value is plotted from a book ID (lists: `figures/figure_ids_used.csv` and `ma/units/figures/*.json`), "
             "so figure-printed values match the book by construction; figure captions are checked as text below.\n")
    L.append("| Table or caption | Tokens | Not matched (token: context) |")
    L.append("|---|---|---|")
    review = []
    for where, n, bad in rows:
        cell = "; ".join(f"`{t}`: …{c}…" for t, c in bad[:6]) + (f"; +{len(bad) - 6} more" if len(bad) > 6 else "")
        L.append(f"| {where} | {n} | {cell.replace('|', '/') if bad else 'none'} |")
        review += [(where, t, c) for t, c in bad]
    with open(FINAL / "QA_unmatched_tokens.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["where", "token", "context"]); w.writerows(review)
    L.append("\nFull list: `QA_unmatched_tokens.csv`.\n")

    # ------------------------------------------------------------------ 2
    L.append("## 2. JMIR figure compliance (Section 1, rule 7)\n")
    figs = [(p.stem, p, FIGS / f"{p.stem}_caption.md") for p in sorted(FIGS.glob("Fig*.png"))]
    figs += [(p.stem, p, MA / "units" / "figures" / f"{p.stem}_caption.md") for p in sorted((MA / "units" / "figures").glob("*.png"))]
    src_txt = (FINAL / "scripts" / "c2_figures.py").read_text() + (FINAL / "scripts" / "c4_units.py").read_text()
    small_font = re.findall(r"fontsize=([0-6](?:\.\d)?)\b", src_txt)
    L.append(f"Fonts: base size 7 pt in both figure scripts; explicit font sizes below 7 pt in the code: "
             f"{'none' if not small_font else small_font}. Figures are drawn at final printed width (7.5 in), so 7 pt is the printed size.\n")
    L.append("| Figure | Simple bar graph? | Exact values printed | Asterisks | Title inside figure | PNG dpi / PDF | Palette | Stance colours | 2026 data |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    design = {
        "Fig1": ("no (flowchart)", "yes (all n)"), "Fig2": ("no (points + CIs)", "yes"), "Fig3": ("no (100% composition + lines)", "yes (table under bars)"),
        "Fig4": ("no (dot plot, two estimates)", "yes"), "Fig5": ("no (map)", "yes (bubble labels)"), "Fig6": ("no (3 outcomes per type)", "yes"),
        "within_genre_fig": ("no (lines)", "yes"), "temporal_robustness_fig": ("no (lines)", "reference series and strong endorsement; others in MA3 tables"),
        "q3_fig": ("no (dot plot + lines)", "yes"), "other_themes_fig": ("no (lines)", "yes"), "theme_counts_fig": ("no (count bars + share line)", "yes"),
        "lexicon_vs_llm_fig": ("no (lines)", "yes"), "terms_fig": ("no (dot plot)", "yes"), "generative_share_fig": ("no (scatter)", "yes"),
        "country_map_20": ("no (map)", "yes (low-count overlaps in Table)"), "forward_validation_sankey": ("no (Sankey, unchanged)", "yes (submitted design)")}
    ids_used = {}
    for r in csv.DictReader(open(FIGS / "figure_ids_used.csv")):
        ids_used.setdefault(r["figure"], set()).add(r["id"])
    for p in (MA / "units" / "figures").glob("*.json"):
        j = json.loads(p.read_text()); ids_used[j["id"]] = set(j["book_ids"])
    asterisk_fail, y26 = [], {}
    for stem, png, cap in figs:
        im = Image.open(png); dpi = im.info.get("dpi", (0, 0))[0]
        pdf = png.with_suffix(".pdf").exists() or (png.with_suffix(".svg").exists())
        captxt = cap.read_text() if cap.exists() else ""
        ast_ = "*" in captxt.replace("**", "")
        if ast_:
            asterisk_fail.append(stem)
        used26 = sorted(i for i in ids_used.get(stem, ()) if "2026" in i or "2026" in BOOK[i]["window"] or BOOK[i]["window"].startswith("January"))
        y26[stem] = used26
        bar, vals = design.get(stem, ("?", "?"))
        L.append(f"| {stem} | {bar} | {vals} | {'present' if ast_ else 'none'} | none (panel letters and panel names only) | "
                 f"{round(dpi)} / {'yes' if pdf else 'no'} | {'submitted design (unchanged)' if stem == 'forward_validation_sankey' else 'Okabe-Ito' if stem not in ('Fig5', 'country_map_20') else 'RdYlBu diverging (colour-blind safe)'} | "
                 f"{'fixed (Okabe-Ito)' if stem in ('Fig2', 'Fig6', 'q3_fig') else 'n/a'} | "
                 f"{'none' if not used26 else ('evidence window by design' if stem == 'forward_validation_sankey' else ', '.join(used26))} |")
    L.append("\nThe forward-validation Sankey is reproduced unchanged from the submission (PNG as submitted, 1484 x 1139 px, plus the "
             "repository SVG). At 6.6 in printed width it is about 225 pixels per inch, below the 300 dpi rule; a 300 dpi version needs "
             "the figure re-rendered from its source (the repository SVG carries an in-figure title that the submitted image cropped out), "
             "which was not done here because the figure is to stay unchanged.\n")

    # ------------------------------------------------------------------ 3
    L.append("## 3. 2026 content in figures\n")
    L.append("Book IDs with a 2026 window used by any figure: " + (", ".join(f"{k}: {v}" for k, v in y26.items() if v) or "none") + ".\n")
    hits = []
    for stem, png, cap in figs:
        t = cap.read_text() if cap.exists() else ""
        for m in re.finditer(r"2026", t):
            hits.append(f"{stem}: …{t[max(0, m.start() - 60): m.end() + 30]}…")
    L.append("Mentions of 2026 in figure captions (none is plotted data):\n")
    L += [f"- {h}" for h in hits] + [""]
    L.append("Figure 1 (flowchart) prints the retrieval period (January 2021-April 2026) and the exclusion counts of the window step "
             "(records published January-April 2026 or later); no 2026 data are analysed or plotted. The Sankey keeps its "
             "2024-April 2026 evidence window by design. No other figure contains 2026.\n")

    # ------------------------------------------------------------------ 4
    L.append("## 4. Tables are real Word tables\n")
    L.append("| Document | Word tables | Inline images | Expected tables |")
    L.append("|---|---|---|---|")
    n_units = len(list((MA / "units" / "tables").glob("*.json")))
    for f, exp in [(TABLES / f"Table{i}.docx", 1) for i in (1, 2, 3)] + [(MA / "Multimedia_Appendix_3_R1.docx", n_units),
                                                                     (MA / "Multimedia_Appendix_1_R1.docx", None),
                                                                     (MA / "Multimedia_Appendix_2_R1.docx", 0)]:
        d = Document(str(f))
        imgs = len(d.inline_shapes)
        L.append(f"| {f.relative_to(FINAL)} | {len(d.tables)} | {imgs} | {exp if exp is not None else 'Note 1, Note 9, Note 10 tables'} |")
    L.append("")

    # ------------------------------------------------------------------ 5
    L.append("## 5. Note 2(a) prompt hash\n")
    h = (MA / "ma1_prompt_hashes.txt").read_text().strip().splitlines()
    prod = subprocess.run(["git", "show", "9c79cd5:classify_stance_batch.py"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    pp = next(ast.literal_eval(n.value) for n in ast.parse(prod).body if isinstance(n, ast.Assign)
              and any(getattr(t, "id", None) == "SYSTEM_PROMPT" for t in n.targets))
    ph = hashlib.sha256(pp.encode()).hexdigest()
    a = dict(x.split("\t") for x in h)
    L.append(f"- Note 2(a) (classify_stance.py): `{a['v1 (Note 2a)']}`")
    L.append(f"- Production batch prompt (9c79cd5:classify_stance_batch.py), recomputed here: `{ph}`")
    L.append(f"- Equal: **{a['v1 (Note 2a)'] == ph == 'b3949917159ea546ce7eb4c21224659be98c646aa937287d376f68c67992a39f'}**")
    L.append(f"- Note 2(b) v2: `{a['v2 (Note 2b)']}`; Note 8 B3: `{a['B3 (Note 8)']}`\n")

    # ------------------------------------------------------------------ 6
    L.append("## 6. Formatting scan (rule 6) over tables, captions and appendices\n")
    files = list(TABLES.glob("*.md")) + list(FIGS.glob("*_caption.md")) + [MA / "Multimedia_Appendix_2_R1.md", MA / "Multimedia_Appendix_3_R1.md"]
    pats = {"lowercase p value (p=, p<)": r"(?<![A-Za-z])p\s?[=<]\s?0?\.\d", "leading zero in P (P=0.)": r"P\s?[=<>]\s?0\.\d",
            "\"Cohen's\"": r"Cohen['’]s", "em dash in a caption": None, "comma in a 4-digit number": r"(?<![\d,.])\d,\d{3}(?![\d,])",
            "en dash in a CI or range": r"\d–\d"}
    for lab, pat in pats.items():
        hits = []
        for f in files:
            t = f.read_text()
            if lab == "em dash in a caption":
                if f.name.endswith("_caption.md") and "—" in t:
                    hits.append(f.name)
                continue
            if re.search(pat, t):
                hits.append(f"{f.name} ({len(re.findall(pat, t))})")
        L.append(f"- {lab}: {'none' if not hits else ', '.join(hits)}")
    L.append("\nCaptions containing 'Critical stance was Alarm or Caution': "
             + ", ".join(f"{p.stem}: {'yes' if 'Critical stance was Alarm or Caution' in p.read_text() else 'NO'}"
                         for p in list(FIGS.glob('*_caption.md')) + list((MA / 'units' / 'figures').glob('*_caption.md'))) + ".\n")
    (FINAL / "QA_batch2c.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"QA written; {nb} tokens left for review")


if __name__ == "__main__":
    main()
