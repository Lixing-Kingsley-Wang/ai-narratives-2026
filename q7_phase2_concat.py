"""Phase 2 wrap-up: concat Alarm + Caution → q7_classified_ac.csv,
print combined contingency table + prompt-version consistency check."""
import csv, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(BASE, "output", "analyses", "q7_classified_alarm.csv")
C = os.path.join(BASE, "output", "analyses", "q7_classified_cautious.csv")
AC = os.path.join(BASE, "output", "analyses", "q7_classified_ac.csv")

alarm = list(csv.DictReader(open(A, encoding="utf-8")))
caut  = list(csv.DictReader(open(C, encoding="utf-8")))
cols  = list(alarm[0].keys())
allrows = alarm + caut

with open(AC, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(allrows)

print(f"Alarm rows:    {len(alarm)}")
print(f"Caution rows:  {len(caut)}")
print(f"Concatenated:  {len(allrows)}  → {AC}")
print()

# ── prompt-version consistency check ──────────────────────────────────────────
print("="*100)
print("PROMPT-VERSION CONSISTENCY CHECK")
print("="*100)
print(f"  prompt_version values: {dict(Counter(r['prompt_version'] for r in allrows))}")
print(f"  model values:          {dict(Counter(r['model'] for r in allrows))}")
pmids = [r['pmid'] for r in allrows]
dups = [p for p,c in Counter(pmids).items() if c>1]
print(f"  total rows: {len(allrows)} | unique pmids: {len(set(pmids))} | cross-stance dup pmids: {len(dups)}")
print(f"  stance values: {dict(Counter(r['stance'] for r in allrows))}")
n_failed = sum(1 for r in allrows if r['failure_mode']=='FAILED')
print(f"  FAILED rows: {n_failed}  (dropped for analysis below)")
ok = (set(r['prompt_version'] for r in allrows)=={'q7_failuremode_v1'} and
      set(r['model'] for r in allrows)=={'claude-sonnet-4-6'} and len(dups)==0)
print(f"  → CONSISTENT: {ok}")
print()

# ── combined contingency table (drop FAILED) ──────────────────────────────────
valid = [r for r in allrows if r['failure_mode']!='FAILED']
print("="*100)
print(f"COMBINED CONTINGENCY: failure_mode × model_type  (A+C, FAILED dropped, n={len(valid)})")
print("="*100)
FM = ["confabulation","misclassification","both","none_or_unclear"]
MT = ["generative","discriminative","both","unclear"]
J = Counter((r['failure_mode'], r['model_type']) for r in valid)
print(f"  {'':22s} " + "".join(f"{mt:>16s}" for mt in MT) + f"{'TOTAL':>9s}")
for fm in FM:
    row=[J.get((fm,mt),0) for mt in MT]
    print(f"  {fm:22s} " + "".join(f"{v:>16d}" for v in row) + f"{sum(row):>9d}")
tot=[sum(J.get((fm,mt),0) for fm in FM) for mt in MT]
print(f"  {'TOTAL':22s} " + "".join(f"{v:>16d}" for v in tot) + f"{sum(tot):>9d}")
print()

# row %  (within failure_mode)
print(f"  Row % (model_type within each failure_mode):")
print(f"  {'':22s} " + "".join(f"{mt:>16s}" for mt in MT))
for fm in FM:
    row=[J.get((fm,mt),0) for mt in MT]; s=sum(row) or 1
    print(f"  {fm:22s} " + "".join(f"{v/s*100:>15.1f}%" for v in row))
print()

# ── per-stance breakdown ──────────────────────────────────────────────────────
print("="*100)
print("failure_mode share by stance (drop FAILED)")
print("="*100)
for st in ["Alarm","Caution"]:
    sub=[r for r in valid if r['stance']==st]
    n=len(sub)
    fm=Counter(r['failure_mode'] for r in sub)
    gen=sum(1 for r in sub if r['model_type'] in ('generative','both'))
    print(f"  {st:8s} n={n:5d} | "
          f"confab={fm.get('confabulation',0)/n*100:4.1f}% "
          f"misc={fm.get('misclassification',0)/n*100:4.1f}% "
          f"both={fm.get('both',0)/n*100:4.1f}% "
          f"none/unclear={fm.get('none_or_unclear',0)/n*100:4.1f}% | "
          f"gen-share={gen/n*100:4.1f}%")
