"""
Validation Sample Export — for Kingsly
Exports a stratified random sample of 300 records for human validation
of LLM stance classification. Stratified by year and stance to ensure
representation of all categories.

Output: output/validation/kingsly_validation_sample.csv
        output/validation/kingsly_coding_sheet.csv  (title+abstract only, no LLM stance)

After Kingsly codes the sheet, run compute_kappa.py to get Cohen's κ.
"""

import csv, os, re, random, collections

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
VAL_DIR    = os.path.join(OUTPUT_DIR, "validation")
os.makedirs(VAL_DIR, exist_ok=True)

random.seed(42)  # reproducible sample

VALID_STANCES = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]
TARGET_N      = 300

# Sampling targets — oversample rare stances
STANCE_TARGETS = {
    "Alarm":             40,   # 3.3% of corpus — oversample to ensure κ reliability
    "Caution":           60,
    "Neutral":           70,
    "Cautious Optimism": 100,
    "Advocacy":          30,   # 1.9% — oversample
}

def get_year(r):
    year = r.get("pub_year","") or ""
    if not year:
        m = re.search(r'\b(20\d{2})\b', r.get("pub_date","") or "")
        year = m.group() if m else ""
    return year


def main():
    input_path = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")

    with open(input_path, encoding="utf-8") as f:
        all_rows = [r for r in csv.DictReader(f)
                    if r.get("stance") in VALID_STANCES
                    and r.get("abstract","").strip()]  # require abstract for coding

    print(f"Validation Sample Export")
    print(f"Input: {len(all_rows):,} records with abstracts")
    print(f"Target sample: {TARGET_N} records (stratified by stance)\n")

    # Group by stance
    by_stance = collections.defaultdict(list)
    for r in all_rows:
        by_stance[r["stance"]].append(r)

    # Sample
    sample = []
    for stance, target in STANCE_TARGETS.items():
        pool      = by_stance[stance]
        n         = min(target, len(pool))
        selected  = random.sample(pool, n)
        sample.extend(selected)
        print(f"  {stance:<22} pool={len(pool):5,}  sampled={n}")

    random.shuffle(sample)  # mix stances so Kingsly can't guess from order

    # Add a record_id for tracking
    for i, r in enumerate(sample):
        r["record_id"] = f"VAL_{i+1:04d}"

    print(f"\nTotal sample: {len(sample)} records")

    # ── File 1: Full record with LLM stance (for researcher reference) ────────
    full_path = os.path.join(VAL_DIR, "kingsly_validation_full.csv")
    full_cols = ["record_id", "pmid", "pub_year", "pub_date", "title",
                 "abstract", "journal", "stance", "confidence",
                 "predictive_claim", "paper_type"]
    with open(full_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=full_cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(sample)
    print(f"\nFull reference file (with LLM stance): {full_path}")

    # ── File 2: Coding sheet (NO LLM stance — for Kingsly) ───────────────────
    coding_path = os.path.join(VAL_DIR, "kingsly_coding_sheet.xlsx")
    coding_cols = ["record_id", "pub_year", "title", "abstract", "journal",
                   "human_stance", "human_notes"]

    coding_rows = []
    for r in sample:
        coding_rows.append({
            "record_id":    r["record_id"],
            "pub_year":     r.get("pub_year","") or get_year(r),
            "title":        r.get("title",""),
            # full abstract preserved (was truncated to 600 chars by Dan's original — broke validation coding)
            "abstract":     r.get("abstract",""),
            "journal":      r.get("journal",""),
            "human_stance": "",   # Kingsly fills this in
            "human_notes":  "",   # optional comments
        })

    # XLSX with ergonomics: stance dropdown, text wrap, frozen header, column widths
    import pandas as pd
    from openpyxl.styles import Alignment
    from openpyxl.worksheet.datavalidation import DataValidation

    df = pd.DataFrame(coding_rows, columns=coding_cols)
    with pd.ExcelWriter(coding_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="coding")
        ws = writer.sheets["coding"]
        # column widths: A=record_id B=pub_year C=title D=abstract E=journal F=human_stance G=human_notes
        for col, w in {"A": 12, "B": 8, "C": 55, "D": 90, "E": 28, "F": 20, "G": 30}.items():
            ws.column_dimensions[col].width = w
        # wrap title (C) and abstract (D)
        for row in ws.iter_rows(min_row=2, min_col=3, max_col=4):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
        # dropdown for human_stance (column F)
        dv = DataValidation(
            type="list",
            formula1='"Alarm,Caution,Neutral,Cautious Optimism,Advocacy"',
            allow_blank=True,
        )
        dv.error = "Must be one of: Alarm, Caution, Neutral, Cautious Optimism, Advocacy"
        dv.errorTitle = "Invalid stance"
        ws.add_data_validation(dv)
        dv.add(f"F2:F{len(df)+1}")
        ws.freeze_panes = "A2"
    print(f"Coding sheet for Kingsly (no LLM stance): {coding_path}")

    # ── Instructions for Kingsly ──────────────────────────────────────────────
    instructions_path = os.path.join(VAL_DIR, "coding_instructions.txt")
    with open(instructions_path, "w", encoding="utf-8") as f:
        f.write("""STANCE CODING INSTRUCTIONS — AI Narratives Validation Study
=============================================================

Thank you for helping validate this study. You will be coding
300 medical journal articles for their stance toward AI/LLM
technology in medicine.

TASK: For each article, read the title and abstract and assign
ONE of the following stance labels in the 'human_stance' column:

STANCE DEFINITIONS:
-------------------
Alarm
  The paper is primarily CRITICAL or SKEPTICAL of AI.
  Emphasises dangers, failures, hallucinations, safety risks,
  ethical problems, or argues AI is not ready/safe for clinical
  use. Papers showing AI performs WORSE than clinicians = Alarm.
  Example: "ChatGPT fails safety standards for medication advice"

Caution
  Acknowledges both promise AND significant concerns, with the
  balance tilting toward concern. Recommends safeguards or
  further validation before deployment.
  Example: "Implications of LLMs for dental medicine" (mixed
  but concern-leaning)

Neutral
  Purely descriptive. Reports AI performance metrics or methods
  without taking a clear evaluative position. No clear message
  about whether AI is good or bad for medicine.
  Example: "Performance benchmarking of segmentation algorithm"

Cautious Optimism
  BROADLY POSITIVE about AI with some caveats. Emphasises
  potential benefits, supports deployment with appropriate
  safeguards.
  Example: "AI in echocardiography: promising results,
  validation needed"

Advocacy
  STRONGLY and UNAMBIGUOUSLY pro-AI. Emphasises transformative
  potential, strongly supports deployment, minimal caveats.
  Example: "AI will revolutionise radiology within five years"

IMPORTANT NOTES:
----------------
- Base your coding ONLY on the title and abstract provided
- If a paper tests AI and finds it performs WORSE than humans,
  code as Alarm (not Neutral)
- If you are unsure between two stances, pick the one that
  better reflects the OVERALL MESSAGE of the abstract
- Use the 'human_notes' column for any comments or uncertainties
- Code each paper independently — do not look at surrounding
  papers for context

VALIDITY:
---------
Your codes will be compared to an LLM classification to compute
inter-rater reliability (Cohen's κ). Target κ ≥ 0.75.

If you have questions, contact Dan Poenaru.

RETURN the completed coding sheet to Dan when finished.
""")
    print(f"Coding instructions: {instructions_path}")

    # ── Year and stance distribution of sample ────────────────────────────────
    print(f"\nSample distribution:")
    year_counts = collections.Counter(
        get_year(r) for r in sample
    )
    for y in sorted(year_counts):
        print(f"  {y}: {year_counts[y]}")


if __name__ == "__main__":
    main()
