"""A4 helper · Fill copies of the coding templates with random answers, for
end-to-end testing of the scoring scripts. Output files are clearly named
SYNTHETIC and are never used for real results.

Usage:
  python a4_make_synthetic.py theme     <template.xlsx> <out.xlsx> [seed]
  python a4_make_synthetic.py prefilter <template.xlsx> <out.xlsx> [seed]
"""

import sys

import numpy as np
from openpyxl import load_workbook

THEMES = ["replacement", "hallucination", "safety_clinical", "ethics_bias", "cognitive",
          "education", "regulation", "existential", "data_privacy", "other"]


def main():
    kind, src, dst = sys.argv[1:4]
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 2026
    rng = np.random.default_rng(seed)
    wb = load_workbook(src)
    ws = wb["Coding"]
    hdr = [c.value for c in ws[1]]
    for r in range(2, ws.max_row + 1):
        if kind == "theme":
            # mostly 1–3 ticks; occasional 0 or 4 to exercise the validity rules
            k = rng.choice([0, 1, 2, 3, 4], p=[0.02, 0.38, 0.38, 0.2, 0.02])
            for t in rng.choice(THEMES, k, replace=False, p=np.r_[np.full(9, 0.105), 0.055]):
                ws.cell(row=r, column=hdr.index(t) + 1, value=1)
        else:
            lab = rng.choice(["discourse", "evaluative", "application", ""], p=[0.15, 0.1, 0.73, 0.02])
            ws.cell(row=r, column=hdr.index("human_label") + 1, value=lab or None)
            if rng.random() < 0.15:
                ws.cell(row=r, column=hdr.index("borderline") + 1, value="Y")
        ws.cell(row=r, column=hdr.index("notes") + 1, value="SYNTHETIC")
    wb.save(dst)
    print(f"synthetic {kind} workbook: {dst}")


if __name__ == "__main__":
    main()
