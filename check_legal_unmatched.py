import csv, collections

with open('output/filtered_legal_unmatched.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

counter = collections.Counter(r['journal'] for r in rows if r['journal'])
print(f"Top 30 unmatched journals ({len(rows)} total unmatched):\n")
for j, n in counter.most_common(30):
    print(f"  {n:5d}  {j}")
