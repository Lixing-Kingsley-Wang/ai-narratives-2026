"""Check year vs pub_year vs pub_date in classified output."""
import csv, re, collections

def extract_year(s):
    m = re.search(r'\b(20\d{2})\b', s or "")
    return m.group() if m else ""

with open('output/classified_medical_Q1Q2.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total: {len(rows)}")
print(f"\nSample of first 5 rows (year fields):")
for r in rows[:5]:
    print(f"  year='{r.get('year','')}' | pub_year='{r.get('pub_year','')}' | pub_date='{r.get('pub_date','')}'")

# Count by each year field
year_raw    = collections.Counter(r.get('year','')[:4] for r in rows)
year_pubyr  = collections.Counter(r.get('pub_year','')[:4] for r in rows)
year_pubdate= collections.Counter(extract_year(r.get('pub_date','')) for r in rows)

print(f"\n{'Year':<6} {'raw year':>10} {'pub_year':>10} {'pub_date':>10}")
print("-"*40)
for y in sorted(set(list(year_raw.keys())+list(year_pubyr.keys())+list(year_pubdate.keys()))):
    if y and "2020" <= y <= "2027":
        print(f"{y:<6} {year_raw.get(y,0):>10} {year_pubyr.get(y,0):>10} {year_pubdate.get(y,0):>10}")
