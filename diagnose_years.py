import csv, collections, re

with open('output/analysis/thematic_alarm.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")

# Check pub_year field
year_counter = collections.Counter(r.get('pub_year','') for r in rows)
print(f"\npub_year distribution:")
for y, n in sorted(year_counter.items()):
    print(f"  '{y}': {n}")

# Check pub_date field
print(f"\nSample pub_date values:")
for r in rows[:10]:
    print(f"  pub_year='{r.get('pub_year','')}' | pub_date='{r.get('pub_date','')}'")

# Try extracting year from pub_date manually
def extract_year(s):
    m = re.search(r'\b(20\d{2})\b', s or "")
    return m.group(1) if m else ""

recovered = collections.Counter(
    extract_year(r.get('pub_date','')) for r in rows
)
print(f"\nYears recoverable from pub_date:")
for y, n in sorted(recovered.items()):
    print(f"  {y}: {n}")
