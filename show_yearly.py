import csv

with open('output/analysis/02_stance_by_year.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"{'Year':<6} {'N':>6}  {'Critical%':>10}  {'Alarm%':>7}  {'Caution%':>9}  {'Neutral%':>9}  {'CautOpt%':>9}  {'Advocacy%':>10}")
print("-" * 80)
for row in rows:
    print(f"{row['year']:<6} {row['total']:>6}  "
          f"{row['critical_pct']:>10}  "
          f"{row['Alarm_pct']:>7}  "
          f"{row['Caution_pct']:>9}  "
          f"{row['Neutral_pct']:>9}  "
          f"{row['Cautious Optimism_pct']:>9}  "
          f"{row['Advocacy_pct']:>10}")
