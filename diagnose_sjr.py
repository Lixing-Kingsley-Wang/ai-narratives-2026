"""Check SJR file structure to find correct law journal filter."""
import csv, os, collections

sjr_path = r"input\sjr\sjr_2024.csv"

with open(sjr_path, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")
    rows = list(reader)

print(f"Total rows: {len(rows)}")
print(f"Columns: {list(rows[0].keys())}")

# Check Areas column values
areas_counter = collections.Counter()
for r in rows:
    areas = r.get("Areas", r.get("areas", r.get("Categories", "")))
    if areas:
        for a in areas.split(";"):
            areas_counter[a.strip()[:40]] += 1

print(f"\nTop 30 area labels:")
for area, n in areas_counter.most_common(30):
    print(f"  {n:5d}  {area}")

# Find law-related entries
print(f"\nLaw-related entries:")
for r in rows[:5000]:
    areas = r.get("Areas", r.get("areas",""))
    title = r.get("Title","")
    if any(kw in areas.lower() for kw in ["law","legal","juris"]):
        print(f"  [{r.get('SJR Best Quartile','')}] {title[:60]} | {areas[:60]}")
        if sum(1 for _ in [x for x in rows if any(kw in x.get("Areas","").lower() for kw in ["law","legal"])]) > 10:
            break
