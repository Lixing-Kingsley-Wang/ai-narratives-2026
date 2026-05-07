"""
Split filtered_medical_all_Q1Q2.csv into per-year files for parallel processing.
Run this once, then open 4 terminals and run prefilter on each year simultaneously.
"""
import csv, os, re, collections

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
input_path = os.path.join(OUTPUT_DIR, "filtered_medical_all_Q1Q2.csv")

print("Loading corpus...")
with open(input_path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
    fieldnames = list(rows[0].keys())

# Group by pub_year extracted from pub_date
by_year = collections.defaultdict(list)
for r in rows:
    m = re.search(r'20\d{2}', r.get('pub_date', '') or '')
    year = m.group() if m else r.get('year', 'unknown')[:4]
    by_year[year].append(r)

print(f"Total records: {len(rows):,}")
print(f"\nYear distribution:")
for year in sorted(by_year.keys()):
    print(f"  {year}: {len(by_year[year]):,}")

# Write per-year files
splits_dir = os.path.join(OUTPUT_DIR, "splits")
os.makedirs(splits_dir, exist_ok=True)

# Group into 4 balanced batches
years = sorted(k for k in by_year.keys() if '2021' <= k <= '2026')
batches = {
    'A': ['2021'],
    'B': ['2022'],
    'C': ['2023', '2024'],
    'D': ['2025', '2026'],
}

for batch_id, batch_years in batches.items():
    batch_rows = []
    for y in batch_years:
        batch_rows.extend(by_year.get(y, []))
    
    path = os.path.join(splits_dir, f"Q1Q2_batch_{batch_id}.csv")
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(batch_rows)
    print(f"  Batch {batch_id} ({', '.join(batch_years)}): {len(batch_rows):,} records → {path}")

print(f"""
Done. Now open 4 PowerShell terminals and run one in each:
  Terminal 1: python prefilter_split.py A
  Terminal 2: python prefilter_split.py B
  Terminal 3: python prefilter_split.py C
  Terminal 4: python prefilter_split.py D
""")
