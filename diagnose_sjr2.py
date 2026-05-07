"""Find law journals in SJR Categories column."""
import csv, collections

sjr_path = r"input\sjr\sjr_2024.csv"

with open(sjr_path, encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

# Check Categories column for law
print("Sample Categories values:")
cats = collections.Counter()
for r in rows:
    for cat in r.get("Categories","").split(";"):
        cats[cat.strip()[:50]] += 1

for cat, n in cats.most_common(50):
    if any(kw in cat.lower() for kw in ["law","legal","juris","crimin"]):
        print(f"  {n:5d}  '{cat}'")

print("\nAll law-related journals found:")
law_journals = []
for r in rows:
    cats_str = r.get("Categories","").lower()
    if any(kw in cats_str for kw in ["law","legal","juris","crimin"]):
        law_journals.append(r)
        
print(f"Total law journals: {len(law_journals)}")
print("\nSample law journals:")
for r in law_journals[:10]:
    print(f"  [{r['SJR Best Quartile']}] {r['Title'][:60]} | {r['Categories'][:60]}")

# Show exact category strings used
print("\nExact law category strings:")
law_cats = set()
for r in law_journals:
    for cat in r.get("Categories","").split(";"):
        if any(kw in cat.lower() for kw in ["law","legal","juris","crimin"]):
            law_cats.add(cat.strip())
for cat in sorted(law_cats):
    print(f"  '{cat}'")
