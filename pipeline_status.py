"""
Pipeline Status Diagnostic
Run this to see exactly where the AI narratives pipeline stands.
"""
import csv, os, re

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def count_csv(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            n = sum(1 for _ in f) - 1
        size = os.path.getsize(path) / (1024*1024)
        return n, size
    except:
        return 0, 0

files = {
    "1. Raw corpus (all years)":
        "raw_medical_all.csv",
    "2. Q1+Q2 filtered (primary)":
        "filtered_medical_all_Q1Q2.csv",
    "3. Q3 filtered (comparison arm)":
        "filtered_medical_all_Q3.csv",
    "4. Pre-filter: discourse+eval":
        "prefiltered_discourse_eval.csv",
    "5. Pre-filter: application (excluded)":
        "prefiltered_application.csv",
    "6. Classified Q1+Q2 (FINAL)":
        "classified_medical_Q1Q2.csv",
    "7. Analysis: stance by quarter":
        "analysis/01_stance_by_quarter.csv",
    "8. Analysis: stance by year":
        "analysis/02_stance_by_year.csv",
}

print("AI NARRATIVES — PIPELINE STATUS")
print("="*65)
total_prefiltered = None

for label, fname in files.items():
    path   = os.path.join(OUTPUT_DIR, fname)
    result = count_csv(path)
    if result is None:
        print(f"  {label}")
        print(f"    ✗ NOT FOUND")
    else:
        n, size = result
        print(f"  {label}")
        print(f"    ✓ {n:,} records  ({size:.1f} MB)")
        if "discourse+eval" in label:
            total_prefiltered = n
        if "application" in label and total_prefiltered:
            total = n + total_prefiltered
            pct   = total_prefiltered / total * 100 if total else 0
            print(f"    → {total:,} total pre-filtered  ({pct:.1f}% retained as discourse/eval)")
    print()

# Check if pre-filter is complete
q1q2_path = os.path.join(OUTPUT_DIR, "filtered_medical_all_Q1Q2.csv")
pf_path   = os.path.join(OUTPUT_DIR, "prefiltered_discourse_eval.csv")
ap_path   = os.path.join(OUTPUT_DIR, "prefiltered_application.csv")

if os.path.exists(q1q2_path) and os.path.exists(pf_path) and os.path.exists(ap_path):
    q1q2_n = count_csv(q1q2_path)[0]
    pf_n   = count_csv(pf_path)[0]
    ap_n   = count_csv(ap_path)[0]
    done   = pf_n + ap_n
    pct    = done / q1q2_n * 100 if q1q2_n else 0
    print(f"PRE-FILTER PROGRESS: {done:,} / {q1q2_n:,} records ({pct:.1f}% complete)")
    if done < q1q2_n:
        remaining = q1q2_n - done
        mins = remaining * 0.25 / 60
        print(f"  Remaining: ~{remaining:,} records (~{mins:.0f} min at 0.25s/record)")
    else:
        print(f"  Pre-filter: COMPLETE")
    print()

# Check classified output
cl_path = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")
if os.path.exists(cl_path):
    cl_n, cl_size = count_csv(cl_path)
    stance_counts = {}
    with open(cl_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = row.get("stance","")
            stance_counts[s] = stance_counts.get(s,0) + 1
    print(f"CLASSIFICATION PROGRESS: {cl_n:,} records classified")
    print("  Stance distribution so far:")
    for s in ["Alarm","Caution","Neutral","Cautious Optimism","Advocacy","FAILED"]:
        n = stance_counts.get(s,0)
        if n:
            pct = n/cl_n*100 if cl_n else 0
            print(f"    {s:<22} {n:5,}  ({pct:.1f}%)")
    if os.path.exists(pf_path):
        pf_n = count_csv(pf_path)[0]
        if cl_n < pf_n:
            remaining = pf_n - cl_n
            hrs = remaining * 0.25 / 3600
            print(f"  Remaining: ~{remaining:,} records (~{hrs:.1f} hrs)")
        else:
            print(f"  Classification: COMPLETE")
