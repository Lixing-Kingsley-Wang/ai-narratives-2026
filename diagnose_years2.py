import csv, re, collections

def extract_year(s):
    m = re.search(r'\b(20\d{2})\b', s or "")
    return m.group(1) if m else ""

rows = []
with open('output/analysis/thematic_alarm.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"Total rows: {len(rows)}")
print(f"\nColumns present: {fieldnames[:8]}")

# Check first 5 rows raw
print(f"\nFirst 5 rows (key fields):")
for r in rows[:5]:
    print(f"  pmid={r.get('pmid','')} | pub_year='{r.get('pub_year','')}' | pub_date='{r.get('pub_date','')}' | themes='{r.get('themes','')}' | stance='{r.get('stance','')}'")

# Year distribution from pub_date in THIS file
year_from_pubdate = collections.Counter(extract_year(r.get('pub_date','')) for r in rows)
print(f"\nYears from pub_date in thematic file:")
for y, n in sorted(year_from_pubdate.items()):
    print(f"  '{y}': {n}")

# Check if pub_date column exists and has data
has_pubdate = sum(1 for r in rows if r.get('pub_date','').strip())
print(f"\nRows with non-empty pub_date: {has_pubdate}/{len(rows)}")
