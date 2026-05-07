"""
Merge split prefilter outputs into single files.
Run after all 4 prefilter_split.py jobs complete.

Combines:
  output/splits/prefiltered_A_discourse_eval.csv
  output/splits/prefiltered_B_discourse_eval.csv
  output/splits/prefiltered_C_discourse_eval.csv
  output/splits/prefiltered_D_discourse_eval.csv

Into:
  output/prefiltered_discourse_eval.csv
  output/prefiltered_application.csv
"""

import csv, os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
SPLITS_DIR = os.path.join(BASE_DIR, "output", "splits")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def merge(suffix, out_name):
    all_rows = []
    fieldnames = None
    for batch_id in ["A", "B", "C", "D"]:
        path = os.path.join(SPLITS_DIR, f"prefiltered_{batch_id}_{suffix}.csv")
        if not os.path.exists(path):
            print(f"  WARNING: missing {path}")
            continue
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if fieldnames is None:
                fieldnames = reader.fieldnames
            rows = list(reader)
            all_rows.extend(rows)
            print(f"  Batch {batch_id}: {len(rows):,} records")

    out_path = os.path.join(OUTPUT_DIR, out_name)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(all_rows)
    print(f"  → {out_name}: {len(all_rows):,} records total\n")
    return len(all_rows)

print("Merging prefilter split outputs...")
print("\nDiscourse + Evaluative:")
n_de = merge("discourse_eval", "prefiltered_discourse_eval.csv")
print("Application:")
n_ap = merge("application", "prefiltered_application.csv")

total = n_de + n_ap
print(f"Summary: {total:,} total | {n_de:,} discourse+eval ({n_de/total*100:.1f}%) | {n_ap:,} application")
print(f"\nNext step: python classify_stance.py")
