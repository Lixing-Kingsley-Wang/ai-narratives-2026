"""Quick diagnostics on raw_medical_2024.csv"""
import csv, collections, os

path = r"output/raw_medical_2024.csv"

rows = []
with open(path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Total records: {len(rows)}")

# Abstract coverage
has_abstract = sum(1 for r in rows if r["abstract"].strip())
print(f"Has abstract:  {has_abstract} ({has_abstract/len(rows)*100:.1f}%)")

# Affiliation coverage
has_aff = sum(1 for r in rows if r["first_affiliation"].strip())
print(f"Has affiliation: {has_aff} ({has_aff/len(rows)*100:.1f}%)")

# Pub type distribution
pt_counter = collections.Counter()
for r in rows:
    for pt in r["pub_type"].split(";"):
        pt = pt.strip()
        if pt:
            pt_counter[pt] += 1
print(f"\nTop pub types:")
for pt, n in pt_counter.most_common(10):
    print(f"  {n:6d}  {pt}")

# Top 15 journals
journal_counter = collections.Counter(r["journal"] for r in rows if r["journal"])
print(f"\nTop 15 journals:")
for j, n in journal_counter.most_common(15):
    print(f"  {n:5d}  {j}")

# Year distribution (sanity check — should all be 2024)
year_counter = collections.Counter(r["year"] for r in rows)
print(f"\nYear distribution:")
for y, n in sorted(year_counter.items()):
    print(f"  {y}: {n}")
