import csv

with open('output/classified_pilot.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

from collections import defaultdict
by_stance = defaultdict(list)
for r in rows:
    by_stance[r['stance']].append(r)

for stance in ['Alarm', 'Advocacy', 'Caution', 'Cautious Optimism', 'Neutral']:
    recs = by_stance.get(stance, [])
    print(f'\n{"="*70}')
    print(f'{stance.upper()} ({len(recs)} records)')
    print(f'{"="*70}')
    for r in recs:
        print(f'  [{r["pub_year"]}] [{r["paper_type"]}] [{r["confidence"]}]')
        print(f'  TITLE: {r["title"]}')
        abstract = r.get("abstract", "")
        if abstract:
            print(f'  ABSTRACT: {abstract[:300]}')
        print()
