"""
Industry vs Academia Stance Analysis — AI Narratives Study
Classifies first_affiliation as industry, academia, or mixed
based on keyword matching, then compares stance distributions.
"""

import csv, re, collections, os

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")

VALID_STANCES = {"Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"}

INDUSTRY_KEYWORDS = [
    "google", "deepmind", "microsoft", "openai", "meta ", "facebook",
    "amazon", "apple ", "nvidia", "ibm ", "intel ",
    "babylon health", "tempus", "flatiron", "nuance", "azure", "aws ",
    "philips", "siemens", "ge healthcare", "ge medical", "general electric",
    "medtronic", "stryker", "johnson & johnson", "j&j", "abbott",
    "roche", "novartis", "pfizer", "astrazeneca", "merck",
    "bayer", "sanofi", "gsk", "glaxosmithkline",
    "mckinsey", "deloitte", "accenture", "iqvia", "covance",
    "inc.", "ltd.", "llc", "corp.", "gmbh", " co.,", "holdings",
]

ACADEMIA_KEYWORDS = [
    "university", "université", "universität", "universidad",
    "college", "institute", "hospital", "clinic", "medical center",
    "medical centre", "school of medicine", "faculty of medicine",
    "department of", "national institutes", "nih ",
]


def classify_affiliation(aff):
    if not aff:
        return "unknown"
    aff_lower = aff.lower()
    has_industry = any(kw in aff_lower for kw in INDUSTRY_KEYWORDS)
    has_academia = any(kw in aff_lower for kw in ACADEMIA_KEYWORDS)
    if has_industry and has_academia:
        return "mixed"
    elif has_industry:
        return "industry"
    elif has_academia:
        return "academia"
    return "unknown"


def get_year(r):
    year = r.get("pub_year","") or ""
    if not year:
        m = re.search(r'\b(20\d{2})\b', r.get("pub_date","") or "")
        year = m.group() if m else ""
    return year


def print_table(label, data_dict, sectors):
    print(f"\n{label}")
    print(f"{'Sector':<14} {'N':>7}  {'Critical%':>10}  {'Alarm%':>7}  "
          f"{'Caution%':>9}  {'CautOpt%':>9}  {'Advocacy%':>10}")
    print("-" * 78)
    out_rows = []
    for sector in sectors:
        data  = data_dict[sector]
        total = sum(data.values())
        if total == 0:
            continue
        alarm  = data.get("Alarm", 0)
        caut   = data.get("Caution", 0)
        crit   = (alarm + caut) / total * 100
        opt    = data.get("Cautious Optimism", 0) / total * 100
        adv    = data.get("Advocacy", 0) / total * 100
        print(f"{sector:<14} {total:>7,}  {crit:>10.1f}  {alarm/total*100:>7.1f}  "
              f"{caut/total*100:>9.1f}  {opt:>9.1f}  {adv:>10.1f}")
        out_rows.append({
            "sector": sector, "total": total,
            "Alarm": alarm, "Caution": caut,
            "Neutral": data.get("Neutral",0),
            "Cautious Optimism": data.get("Cautious Optimism",0),
            "Advocacy": data.get("Advocacy",0),
            "critical_pct": round(crit,2),
            "advocacy_pct": round(adv,2),
        })
    return out_rows


def main():
    input_path = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    with open(input_path, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("stance") in VALID_STANCES]

    print(f"Industry vs Academia + Publication Type Analysis")
    print(f"Input: {len(rows):,} records\n")

    # ── Industry vs Academia ──────────────────────────────────────────────────
    sector_stance = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        sector = classify_affiliation(r.get("first_affiliation",""))
        sector_stance[sector][r["stance"]] += 1

    out1 = print_table(
        "INDUSTRY vs ACADEMIA",
        sector_stance,
        ["academia", "industry", "mixed", "unknown"]
    )

    # Year trend
    sector_year = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        sector = classify_affiliation(r.get("first_affiliation",""))
        year   = get_year(r)
        if year and "2021" <= year <= "2026":
            sector_year[f"{sector}|{year}"]["total"] += 1
            if r["stance"] in ("Alarm","Caution"):
                sector_year[f"{sector}|{year}"]["critical"] += 1

    years = [str(y) for y in range(2021, 2027)]
    print(f"\nCritical % by sector and year:")
    print(f"{'Sector':<12}" + "".join(f"{y:>8}" for y in years))
    print("-" * (12 + 8*len(years)))
    for sector in ["academia","industry","mixed"]:
        if sum(sector_stance[sector].values()) < 30:
            continue
        row_str = f"{sector:<12}"
        for year in years:
            d    = sector_year.get(f"{sector}|{year}", {})
            t    = d.get("total",0)
            crit = d.get("critical",0)/t*100 if t else 0
            row_str += f"{crit:>7.0f}%"
        print(row_str)

    print(f"\nTop industry affiliations detected:")
    ind_aff = collections.Counter(
        r.get("first_affiliation","")[:80]
        for r in rows
        if classify_affiliation(r.get("first_affiliation","")) == "industry"
    )
    for aff, n in ind_aff.most_common(8):
        print(f"  {n:4d}  {aff}")

    # Save
    if out1:
        path = os.path.join(ANALYSIS_DIR, "industry_vs_academia.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out1[0].keys()))
            w.writeheader()
            w.writerows(out1)
        print(f"\nSaved: {path}")

    # ── Publication Type ──────────────────────────────────────────────────────
    def simplify_pubtype(pt):
        if "Editorial" in pt:      return "Editorial"
        if "Letter" in pt:         return "Letter"
        if "Systematic Review" in pt: return "Systematic Review"
        if "Review" in pt:         return "Review"
        if "Comment" in pt:        return "Comment"
        if "News" in pt:           return "News"
        return "Original Article"

    pt_stance = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        pt = simplify_pubtype(r.get("pub_type",""))
        pt_stance[pt][r["stance"]] += 1

    out2 = print_table(
        "\nPUBLICATION TYPE",
        pt_stance,
        ["Editorial","Letter","Comment","News","Systematic Review","Review","Original Article"]
    )

    if out2:
        path = os.path.join(ANALYSIS_DIR, "pubtype_stance.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out2[0].keys()))
            w.writeheader()
            w.writerows(out2)
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
