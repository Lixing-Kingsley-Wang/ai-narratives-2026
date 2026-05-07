import csv

with open('output/analysis/03_specialty_stance.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Specialty stance analysis ({len(rows)} specialties)\n")
print(f"{'Specialty':<38} {'N':>6}  {'Critical%':>10}  {'Alarm%':>7}  {'Caution%':>9}  {'CautOpt%':>9}")
print("-" * 85)
for r in rows:
    print(f"{r['specialty']:<38} {r['total']:>6}  "
          f"{r['critical_pct']:>10}  "
          f"{r['Alarm_pct']:>7}  "
          f"{r['Caution_pct']:>9}  "
          f"{r['Cautious Optimism_pct']:>9}")
