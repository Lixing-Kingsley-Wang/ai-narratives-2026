"""Shared helpers for JMIR R1 Batch 2c (final figures, tables, appendices,
numbers book). Everything Batch 2c writes lives under revision_r1/final/.

* Re-uses revision_r1/scripts/r1_common.py (imported, not modified).
* JMIR number formatting (rule 6 of the Batch 2c brief).
* The numbers book (NUMBERS_BOOK_R1.csv) is the single source for every
  number printed in a figure, table or caption; c_book() reads it back.
"""

from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINAL = HERE.parent
R1 = FINAL.parent
REPO = R1.parent
sys.path.insert(0, str(R1 / "scripts"))
sys.path.insert(0, str(REPO))

import r1_common as rc  # noqa: E402

OUT = rc.OUT                      # revision_r1/outputs (Batch 1-2b results)
DATA = FINAL / "data"             # Batch 2c derived tables used by figures/tables
FIGS = FINAL / "figures"
TABLES = FINAL / "tables"
MA = FINAL / "ma"
BOOK_CSV = FINAL / "NUMBERS_BOOK_R1.csv"
BOOK_MD = FINAL / "NUMBERS_BOOK_R1.md"
for d in (DATA, FIGS, TABLES, MA):
    d.mkdir(parents=True, exist_ok=True)

Y5 = [2021, 2022, 2023, 2024, 2025]
STANCES = rc.STANCES

# Colour-blind-safe stance palette (Okabe-Ito), identical in every figure.
STANCE_COLOURS = {
    "Alarm": "#D55E00", "Caution": "#E69F00", "Neutral": "#999999",
    "Cautious Optimism": "#56B4E9", "Advocacy": "#0072B2",
    "Critical": "#D55E00", "Favourable": "#0072B2",
}
THEME_COLOURS = {"Patient safety": "#009E73", "Hallucination / errors": "#CC79A7",
                 "Governance / regulation": "#0072B2", "Ethics & bias": "#E69F00"}
HEADLINE_THEMES = ["Patient safety", "Hallucination / errors", "Governance / regulation", "Ethics & bias"]

AUTHORS = "Lixing Wang, Dan Poenaru"
TITLE_R1 = ("Evaluative Stance Toward Artificial Intelligence in the Medical Literature: "
            "Infoveillance Study of 14,058 High-Quartile Journal Abstracts, 2021-2025")
TITLE_NOTE = ("Working title: the submitted title gave 16,749 abstracts and 2021-2026; "
              "the count and window above follow the R1 analytic corpus and may change "
              "when the manuscript is revised.")


# ---------------------------------------------------------------------------
# JMIR formatting
# ---------------------------------------------------------------------------
def fn(n) -> str:
    """Integer with a thousands comma only for numbers >= 10,000."""
    n = int(round(float(n)))
    return f"{n:,}" if abs(n) >= 10000 else str(n)


def fnum(x, d=1) -> str:
    """Decimal number; thousands comma only for values >= 10,000."""
    return f"{x:,.{d}f}" if abs(x) >= 10000 else f"{x:.{d}f}"


def pct(p, d=1) -> str:
    return f"{p:.{d}f}%"


def nN(k, n) -> str:
    return f"{fn(k)}/{fn(n)}"


def ci(lo, hi, d=1, unit="%") -> str:
    """'95% CI 29.8%-32.2%'; 'to' when a bound is negative."""
    a, b = f"{lo:.{d}f}{unit}", f"{hi:.{d}f}{unit}"
    return f"95% CI {a} to {b}" if (lo < 0 or hi < 0) else f"95% CI {a}-{b}"


def ci_inner(lo, hi, d=1, unit="%") -> str:
    """Bounds only, for table cells: '29.8-32.2' or '-1.6 to 6.4'."""
    a, b = f"{lo:.{d}f}{unit}", f"{hi:.{d}f}{unit}"
    return f"{a} to {b}" if (lo < 0 or hi < 0) else f"{a}-{b}"


def p_txt(p, italic=False) -> str:
    """JMIR P: no leading zero, P<.001 floor, 3 decimals when < .01 else 2-3."""
    P = "*P*" if italic else "P"
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return f"{P} not computed"
    if p < 0.001:
        return f"{P}<.001"
    if p > 0.999:
        return f"{P}>.99"
    s = f"{p:.3f}"
    return f"{P}={s[1:] if s.startswith('0') else s}"


def pct_ci(point, lo, hi, k=None, n=None, d=1) -> str:
    s = f"{point:.{d}f}% ({ci(lo, hi, d)})"
    if k is not None and n is not None:
        s = f"{point:.{d}f}% ({nN(k, n)}; {ci(lo, hi, d)})"
    return s


def or_ci(o, lo, hi, d=2, p=None) -> str:
    s = f"OR {o:.{d}f} ({ci(lo, hi, d, unit='')})"
    return s + (f", {p_txt(p)}" if p is not None else "")


def rho_txt(rho, p, label="exact P") -> str:
    return f"ρ={rho:+.2f} ({p_txt(p)})".replace("+-", "-")


def jmir_text(v: str) -> str:
    """Hyphen for ranges; no comma in 4-digit numbers (1,472 -> 1472)."""
    v = v.replace("\u2013", "-")
    return re.sub(r"(?<![\d,.])(\d),(\d{3})(?![\d,])", r"\1\2", v)


def jmirize(s: str) -> str:
    """Re-express a Batch 2b summary string in JMIR style."""
    s = s.replace("(exact P", "(P")
    s = re.sub(r"OR/yr ([0-9.]+) \(([0-9.]+)[\u2013-]([0-9.]+)\)", r"OR \1 per year (95% CI \2-\3)", s)
    s = re.sub(r"([0-9.]+)% \(([0-9.]+)[\u2013-]([0-9.]+)\); ([0-9,]+)/([0-9,]+)",
               r"\1% (\4/\5; 95% CI \2%-\3%)", s)
    s = s.replace(" \u2192 ", " to ").replace("\u0394 ", "change ").replace(" pp)", " percentage points)")
    return jmir_text(s)


# ---------------------------------------------------------------------------
# numbers book
# ---------------------------------------------------------------------------
BOOK_FIELDS = ["id", "section", "subsection", "item", "value", "point", "lo", "hi", "k", "n",
               "p", "ci_method", "window", "source"]


class Book:
    def __init__(self):
        self.rows, self.ids = [], set()

    def add(self, id_, section, subsection, item, value, point=None, lo=None, hi=None, k=None,
            n=None, p=None, ci_method="", window="2021-2025", source=""):
        assert id_ not in self.ids, f"duplicate numbers-book id {id_}"
        self.ids.add(id_)
        clean = lambda v: "" if v is None or (isinstance(v, float) and math.isnan(v)) else v
        value = jmir_text(str(value))
        self.rows.append({"id": id_, "section": section, "subsection": subsection, "item": item,
                          "value": value, "point": clean(point), "lo": clean(lo), "hi": clean(hi),
                          "k": clean(k), "n": clean(n), "p": clean(p), "ci_method": ci_method,
                          "window": window, "source": source})

    def write(self, intro_md: str):
        with open(BOOK_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=BOOK_FIELDS)
            w.writeheader()
            w.writerows(self.rows)
        L = [intro_md]
        cur_s = cur_sub = None
        for r in self.rows:
            if r["section"] != cur_s:
                cur_s, cur_sub = r["section"], None
                L += ["", f"## {cur_s}", ""]
            if r["subsection"] != cur_sub:
                cur_sub = r["subsection"]
                L += ["", f"### {cur_sub}", "", "| ID | Item | Value | Window | Source |", "|---|---|---|---|---|"]
            v = str(r["value"]).replace("|", "\\|").replace("\n", " ")
            L.append(f"| {r['id']} | {r['item']} | {v} | {r['window']} | {r['source']} |")
        BOOK_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


def c_book() -> dict:
    """Numbers book as {id: row}."""
    with open(BOOK_CSV, encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}
