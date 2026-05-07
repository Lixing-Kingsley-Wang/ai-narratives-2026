"""
Cohen's Kappa Computation — AI Narratives Validation
Run after Kingsly returns completed kingsly_coding_sheet.csv

Computes:
  - Overall Cohen's κ (LLM vs human)
  - Per-stance precision, recall, F1
  - Confusion matrix
  - κ by year (to check for temporal drift)

Usage: python compute_kappa.py
"""

import csv, os, re, collections

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
VAL_DIR    = os.path.join(OUTPUT_DIR, "validation")

VALID_STANCES = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]


def cohen_kappa(y_true, y_pred, labels):
    n = len(y_true)
    if n == 0:
        return 0.0

    # Observed agreement
    p_o = sum(1 for a, b in zip(y_true, y_pred) if a == b) / n

    # Expected agreement
    true_counts = collections.Counter(y_true)
    pred_counts = collections.Counter(y_pred)
    p_e = sum(
        (true_counts.get(l, 0) / n) * (pred_counts.get(l, 0) / n)
        for l in labels
    )

    if p_e == 1.0:
        return 1.0
    return (p_o - p_e) / (1 - p_e)


def get_year(r):
    year = r.get("pub_year","") or ""
    if not year:
        m = re.search(r'\b(20\d{2})\b', r.get("pub_date","") or "")
        year = m.group() if m else ""
    return year


def main():
    coding_path = os.path.join(VAL_DIR, "kingsly_coding_sheet.csv")
    full_path   = os.path.join(VAL_DIR, "kingsly_validation_full.csv")

    if not os.path.exists(coding_path):
        print(f"Coding sheet not found: {coding_path}")
        print("Run export_validation.py first, send to Kingsly, then place returned file here.")
        return

    # Load coding sheet
    with open(coding_path, encoding="utf-8") as f:
        coding = {r["record_id"]: r for r in csv.DictReader(f)}

    # Load full reference
    with open(full_path, encoding="utf-8") as f:
        full = {r["record_id"]: r for r in csv.DictReader(f)}

    # Match and validate
    y_human, y_llm, years = [], [], []
    skipped = 0

    for rec_id, human_row in coding.items():
        human_stance = human_row.get("human_stance","").strip()
        if not human_stance or human_stance not in VALID_STANCES:
            skipped += 1
            continue
        llm_row = full.get(rec_id)
        if not llm_row:
            skipped += 1
            continue
        llm_stance = llm_row.get("stance","").strip()
        if llm_stance not in VALID_STANCES:
            skipped += 1
            continue

        y_human.append(human_stance)
        y_llm.append(llm_stance)
        years.append(get_year(llm_row))

    n = len(y_human)
    print(f"Validation Kappa Analysis")
    print(f"Records coded: {n}  |  Skipped: {skipped}\n")

    if n == 0:
        print("No valid coded records found.")
        return

    # Overall kappa
    kappa = cohen_kappa(y_human, y_llm, VALID_STANCES)
    agreement = sum(1 for a,b in zip(y_human,y_llm) if a==b) / n * 100
    print(f"Overall Cohen's κ:    {kappa:.3f}")
    print(f"Overall agreement:    {agreement:.1f}%")

    # Interpret
    if kappa >= 0.80:
        interp = "Almost perfect"
    elif kappa >= 0.75:
        interp = "Substantial — meets publication threshold"
    elif kappa >= 0.60:
        interp = "Moderate — consider prompt revision"
    else:
        interp = "Fair/Poor — requires revision"
    print(f"Interpretation:       {interp}\n")

    # Confusion matrix
    print("Confusion matrix (rows=human, cols=LLM):")
    header = f"{'Human \\ LLM':<22}" + "".join(f"{s[:8]:>10}" for s in VALID_STANCES)
    print(header)
    print("-" * len(header))
    for hs in VALID_STANCES:
        row_str = f"{hs:<22}"
        for ls in VALID_STANCES:
            count = sum(1 for h,l in zip(y_human,y_llm) if h==hs and l==ls)
            row_str += f"{count:>10}"
        print(row_str)

    # Per-stance metrics
    print(f"\nPer-stance metrics:")
    print(f"{'Stance':<22} {'Precision':>10} {'Recall':>8} {'F1':>6} {'N human':>8}")
    print("-" * 58)
    for stance in VALID_STANCES:
        tp = sum(1 for h,l in zip(y_human,y_llm) if h==stance and l==stance)
        fp = sum(1 for h,l in zip(y_human,y_llm) if h!=stance and l==stance)
        fn = sum(1 for h,l in zip(y_human,y_llm) if h==stance and l!=stance)
        n_human = sum(1 for h in y_human if h==stance)
        prec = tp/(tp+fp) if (tp+fp) > 0 else 0
        rec  = tp/(tp+fn) if (tp+fn) > 0 else 0
        f1   = 2*prec*rec/(prec+rec) if (prec+rec) > 0 else 0
        print(f"{stance:<22} {prec:>10.3f} {rec:>8.3f} {f1:>6.3f} {n_human:>8}")

    # Kappa by year
    print(f"\nKappa by year:")
    year_data = collections.defaultdict(lambda: {"human":[], "llm":[]})
    for h, l, y in zip(y_human, y_llm, years):
        if y and "2021" <= y <= "2026":
            year_data[y]["human"].append(h)
            year_data[y]["llm"].append(l)

    for year in sorted(year_data.keys()):
        yh = year_data[year]["human"]
        yl = year_data[year]["llm"]
        yk = cohen_kappa(yh, yl, VALID_STANCES)
        ya = sum(1 for a,b in zip(yh,yl) if a==b)/len(yh)*100
        print(f"  {year}: κ={yk:.3f}  agreement={ya:.1f}%  n={len(yh)}")

    # Save results
    results_path = os.path.join(VAL_DIR, "kappa_results.txt")
    with open(results_path, "w", encoding="utf-8") as f:
        f.write(f"Cohen's κ = {kappa:.3f}\n")
        f.write(f"Overall agreement = {agreement:.1f}%\n")
        f.write(f"N = {n}\n")
        f.write(f"Interpretation: {interp}\n")
    print(f"\nResults saved: {results_path}")


if __name__ == "__main__":
    main()
