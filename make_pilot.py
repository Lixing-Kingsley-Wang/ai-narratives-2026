import csv, re, random, collections

with open('output/filtered_medical_all_Q1Q2.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

by_year = collections.defaultdict(list)
for r in rows:
    m = re.search(r'20\d{2}', r.get('pub_date', ''))
    if m:
        by_year[m.group()].append(r)

print("Records per pub_year:")
for y in sorted(by_year):
    print(f"  {y}: {len(by_year[y])}")

sample = []
for y in ['2021', '2022', '2023', '2024']:
    n = min(50, len(by_year[y]))
    sample.extend(random.sample(by_year[y], n))

with open('output/pilot_200.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(sample)

print(f'\nPilot sample: {len(sample)} records written to output/pilot_200.csv')
yc = collections.Counter(
    re.search(r'20\d{2}', r.get('pub_date', '')).group()
    for r in sample
    if re.search(r'20\d{2}', r.get('pub_date', ''))
)
print("Year distribution:")
for y in sorted(yc):
    print(f"  {y}: {yc[y]}")
