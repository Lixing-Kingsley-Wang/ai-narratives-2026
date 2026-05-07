import csv, collections

with open('output/classified_pilot_200.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

by_stance = collections.defaultdict(list)
for r in rows:
    by_stance[r['stance']].append(r)

for stance in ['Alarm', 'Caution', 'Neutral', 'Cautious Optimism', 'Advocacy', 'FAILED']:
    recs = by_stance.get(stance, [])
    print(f'\n--- {stance} ({len(recs)} records) ---')
    for r in recs[:4]:
        year  = r.get('pub_year', r.get('year', ''))
        title = r.get('title', '')[:120]
        conf  = r.get('confidence', '')
        model = r.get('stance_model', '')
        print(f'  [{year}] [{conf}] [{model}] {title}')
