"""Print Phase 1 summary stats on q7_classified_alarm.csv."""
import csv, os, random
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "output", "analyses", "q7_classified_alarm.csv")

with open(P, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"n = {len(rows)}")
print(f"FAILED: {sum(1 for r in rows if r['failure_mode']=='FAILED')}")
print()

# confidence distribution (binned)
conf = [float(r['confidence']) for r in rows if r['failure_mode']!='FAILED']
bins = [0,0.5,0.7,0.8,0.9,1.001]
labels = ['<0.5','0.5-0.7','0.7-0.8','0.8-0.9','0.9-1.0']
counts = [0]*5
for c in conf:
    for i in range(5):
        if bins[i] <= c < bins[i+1]:
            counts[i] += 1; break
print("Confidence distribution (non-FAILED):")
for lbl, n in zip(labels, counts):
    pct = n/len(conf)*100
    print(f"  {lbl:8s} {n:4d}  ({pct:5.1f}%)")
print(f"  mean = {sum(conf)/len(conf):.3f}, median = {sorted(conf)[len(conf)//2]:.3f}")
print()

# joint failure_mode × model_type
print("Joint failure_mode × model_type (excl FAILED):")
fmts = ["confabulation","misclassification","both","none_or_unclear"]
mts  = ["generative","discriminative","both","unclear"]
joint = Counter((r['failure_mode'], r['model_type']) for r in rows if r['failure_mode']!='FAILED')
print(f"  {'':22s} " + "  ".join(f"{mt:>15s}" for mt in mts) + f"  {'TOTAL':>8s}")
for fm in fmts:
    row = [joint.get((fm, mt), 0) for mt in mts]
    print(f"  {fm:22s} " + "  ".join(f"{v:>15d}" for v in row) + f"  {sum(row):>8d}")
totals = [sum(joint.get((fm, mt), 0) for fm in fmts) for mt in mts]
print(f"  {'TOTAL':22s} " + "  ".join(f"{v:>15d}" for v in totals) + f"  {sum(totals):>8d}")
print()

# failure_mode × pub_year (counts + %)
print("failure_mode × pub_year (counts):")
years = ["2021","2022","2023","2024","2025","2026"]
by = Counter((r['failure_mode'], r['pub_year']) for r in rows if r['failure_mode']!='FAILED')
print(f"  {'':22s} " + "  ".join(f"{y:>8s}" for y in years) + f"  {'TOTAL':>8s}")
for fm in fmts:
    row = [by.get((fm, y), 0) for y in years]
    print(f"  {fm:22s} " + "  ".join(f"{v:>8d}" for v in row) + f"  {sum(row):>8d}")
year_tot = [sum(by.get((fm, y), 0) for fm in fmts) for y in years]
print(f"  {'TOTAL':22s} " + "  ".join(f"{v:>8d}" for v in year_tot) + f"  {sum(year_tot):>8d}")
print()
print("failure_mode × pub_year (% within year):")
print(f"  {'':22s} " + "  ".join(f"{y:>8s}" for y in years))
for fm in fmts:
    row = []
    for i, y in enumerate(years):
        v = by.get((fm, y), 0)
        pct = v/year_tot[i]*100 if year_tot[i] else 0
        row.append(f"{pct:>7.1f}%")
    print(f"  {fm:22s} " + "  ".join(row))
print()

# generative-share per year (model_type in generative or both)
print("model_type generative-share by year (model_type in {generative, both}):")
gby = Counter()
tby = Counter()
for r in rows:
    if r['failure_mode']=='FAILED': continue
    y = r['pub_year']
    tby[y] += 1
    if r['model_type'] in ('generative','both'):
        gby[y] += 1
for y in years:
    pct = gby[y]/tby[y]*100 if tby[y] else 0
    print(f"  {y}  {gby[y]:>4d}/{tby[y]:<4d}  {pct:5.1f}%")
print()

# 30 random rows with rationale (seed=42)
print("="*120)
print("30 RANDOM ROWS (seed=42)")
print("="*120)
# Need to merge title from source
src = os.path.join(BASE, "output", "classified_medical_Q1Q2.csv")
title_by = {}
with open(src, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        title_by[r['pmid']] = r.get('title','')

rng = random.Random(42)
sample = rng.sample(rows, 30)
sample.sort(key=lambda r: (r['pub_year'], r['pmid']))
for r in sample:
    t = (title_by.get(r['pmid'],'')[:90]).replace("\n"," ")
    print(f"[{r['pub_year']}] pmid={r['pmid']:>9s}  fm={r['failure_mode']:<18s} mt={r['model_type']:<14s} conf={float(r['confidence']):.2f}")
    print(f"          title: {t!r}")
    print(f"          rationale: {r['rationale']}")
