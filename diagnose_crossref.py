import csv, collections

with open('output/classified_medical_Q1Q2.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")
print(f"Columns: {list(rows[0].keys())[:8]}")

# Check pub_year values
yr = collections.Counter(r.get('pub_year','')[:4] for r in rows)
print(f"\npub_year distribution:")
for y, n in sorted(yr.items()):
    print(f"  '{y}': {n}")

# Check DOI coverage
has_doi = sum(1 for r in rows if r.get('doi','').strip())
print(f"\nRecords with DOI: {has_doi}/{len(rows)}")

# Check candidates specifically
candidates = [
    r for r in rows
    if r.get('pub_year','')[:4] in ('2025','2026')
    and r.get('doi','').strip()
]
print(f"\nCandidates (pub_year 2025-2026 with DOI): {len(candidates)}")

# Show sample
print(f"\nSample 2025 records:")
for r in rows[:3]:
    if r.get('pub_year','')[:4] == '2025':
        print(f"  pub_year='{r['pub_year']}' doi='{r.get('doi','')[:40]}'")

# Also check raw 2025 count
n2025 = sum(1 for r in rows if r.get('pub_year','')[:4] == '2025')
n2025doi = sum(1 for r in rows if r.get('pub_year','')[:4] == '2025' and r.get('doi','').strip())
print(f"\n2025 records: {n2025} | with DOI: {n2025doi}")
