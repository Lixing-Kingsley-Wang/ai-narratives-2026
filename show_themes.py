import csv, collections, re

def extract_pub_year(s):
    m = re.search(r'\b(20\d{2})\b', s or "")
    return m.group(1) if m else ""

theme_by_year = collections.defaultdict(lambda: collections.Counter())
total_by_year = collections.Counter()

with open('output/analysis/thematic_alarm.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        year   = row.get("pub_year","") or extract_pub_year(row.get("pub_date",""))
        themes = [t for t in row.get("themes","").split("|") if t]
        if year and "2021" <= year <= "2026":
            total_by_year[year] += 1
            for t in themes:
                theme_by_year[year][t] += 1

years = sorted(total_by_year.keys())
theme_order = [
    "replacement", "hallucination", "safety_clinical", "ethics_bias",
    "cognitive", "education", "regulation", "existential",
    "data_privacy", "other"
]

print(f"Theme x Year (% of critical papers that year):")
print(f"{'n critical:':<22}" + "".join(f"{total_by_year[y]:>8}" for y in years))
print(f"{'Theme':<22}" + "".join(f"{y:>8}" for y in years))
print("-" * (22 + 8 * len(years)))
for theme in theme_order:
    row_str = f"{theme:<22}"
    for year in years:
        n   = theme_by_year[year].get(theme, 0)
        t   = total_by_year[year]
        pct = n / t * 100 if t else 0
        row_str += f"{pct:>7.0f}%"
    print(row_str)

print(f"\nTotal: {sum(total_by_year.values()):,} critical papers")
