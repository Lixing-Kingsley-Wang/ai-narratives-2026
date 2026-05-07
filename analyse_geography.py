"""
Geographic Stance Analysis — AI Narratives Study
Extracts country/region from first_affiliation field and computes
stance distribution by region.

Regions: North America, Europe, China, Asia-Pacific, Middle East,
         Latin America, Africa, Other/Unknown
"""

import csv, re, collections, os

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")

# ── country → region mapping ──────────────────────────────────────────────────
COUNTRY_REGION = {
    # North America
    "usa": "North America", "united states": "North America",
    "u.s.a": "North America", "u.s.": "North America",
    "canada": "North America", "mexico": "North America",

    # Europe
    "uk": "Europe", "united kingdom": "Europe", "england": "Europe",
    "scotland": "Europe", "wales": "Europe", "ireland": "Europe",
    "germany": "Europe", "france": "Europe", "italy": "Europe",
    "spain": "Europe", "netherlands": "Europe", "belgium": "Europe",
    "switzerland": "Europe", "sweden": "Europe", "norway": "Europe",
    "denmark": "Europe", "finland": "Europe", "austria": "Europe",
    "portugal": "Europe", "greece": "Europe", "poland": "Europe",
    "czech": "Europe", "hungary": "Europe", "romania": "Europe",
    "turkey": "Europe", "israel": "Middle East",

    # China
    "china": "China", "p.r. china": "China", "people's republic of china": "China",
    "hong kong": "China", "taiwan": "China",

    # Asia-Pacific
    "japan": "Asia-Pacific", "south korea": "Asia-Pacific", "korea": "Asia-Pacific",
    "australia": "Asia-Pacific", "new zealand": "Asia-Pacific",
    "singapore": "Asia-Pacific", "india": "Asia-Pacific",
    "thailand": "Asia-Pacific", "malaysia": "Asia-Pacific",
    "indonesia": "Asia-Pacific", "iran": "Middle East",
    "saudi arabia": "Middle East", "egypt": "Middle East",
    "qatar": "Middle East", "uae": "Middle East",
    "united arab emirates": "Middle East",

    # Latin America
    "brazil": "Latin America", "argentina": "Latin America",
    "chile": "Latin America", "colombia": "Latin America",
    "mexico": "Latin America",

    # Africa
    "south africa": "Africa", "nigeria": "Africa", "kenya": "Africa",
    "ethiopia": "Africa", "ghana": "Africa",
}

VALID_STANCES = {"Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"}


def assign_region(affiliation):
    if not affiliation:
        return "Unknown"
    aff_lower = affiliation.lower()

    # Check for country keywords
    for country, region in COUNTRY_REGION.items():
        if country in aff_lower:
            return region

    # Fallback patterns
    if any(x in aff_lower for x in [".edu", "university", "college", "hospital"]):
        # US-style suffixes
        if any(x in aff_lower for x in [", tx", ", ca", ", ny", ", ma", ", fl",
                                          ", il", ", pa", ", oh", ", nc", ", wa"]):
            return "North America"

    return "Unknown"


def main():
    input_path  = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")
    output_path = os.path.join(ANALYSIS_DIR, "geographic_stance.csv")
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    with open(input_path, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("stance") in VALID_STANCES]

    print(f"Geographic Stance Analysis")
    print(f"Input: {len(rows):,} classified records")

    # Assign regions
    region_stance = collections.defaultdict(lambda: collections.Counter())
    region_year   = collections.defaultdict(lambda: collections.Counter())
    unknown_count = 0

    for r in rows:
        region = assign_region(r.get("first_affiliation", ""))
        stance = r.get("stance", "")
        year   = r.get("pub_year", "") or re.search(
            r'\b(20\d{2})\b', r.get("pub_date","") or ""
        )
        if hasattr(year, 'group'):
            year = year.group()

        region_stance[region][stance] += 1
        if year and "2021" <= str(year) <= "2026":
            region_year[f"{region}|{year}"]["critical"] += (
                1 if stance in ("Alarm","Caution") else 0
            )
            region_year[f"{region}|{year}"]["total"] += 1

        if region == "Unknown":
            unknown_count += 1

    # Print summary table
    regions_ordered = [
        "North America", "Europe", "China", "Asia-Pacific",
        "Middle East", "Latin America", "Africa", "Unknown"
    ]

    print(f"\n{'Region':<20} {'N':>6}  {'Critical%':>10}  {'Alarm%':>7}  {'Caution%':>9}  {'CautOpt%':>9}  {'Advocacy%':>10}")
    print("-" * 80)

    out_rows = []
    for region in regions_ordered:
        data  = region_stance[region]
        total = sum(data.values())
        if total == 0:
            continue
        alarm   = data.get("Alarm", 0)
        caution = data.get("Caution", 0)
        crit    = (alarm + caution) / total * 100
        opt     = data.get("Cautious Optimism", 0) / total * 100
        adv     = data.get("Advocacy", 0) / total * 100
        print(f"{region:<20} {total:>6}  {crit:>10.1f}  {alarm/total*100:>7.1f}  "
              f"{caution/total*100:>9.1f}  {opt:>9.1f}  {adv:>10.1f}")

        out_rows.append({
            "region": region, "total": total,
            "Alarm": alarm, "Caution": caution,
            "Neutral": data.get("Neutral", 0),
            "Cautious Optimism": data.get("Cautious Optimism", 0),
            "Advocacy": data.get("Advocacy", 0),
            "critical_pct": round(crit, 2),
            "alarm_pct": round(alarm/total*100, 2),
        })

    # Year trend by region (critical % only)
    print(f"\nCritical stance % by region and year:")
    years = [str(y) for y in range(2021, 2027)]
    print(f"{'Region':<20}" + "".join(f"{y:>8}" for y in years))
    print("-" * (20 + 8*len(years)))

    for region in regions_ordered:
        data  = region_stance[region]
        if sum(data.values()) < 50:  # skip tiny regions
            continue
        row_str = f"{region:<20}"
        for year in years:
            key   = f"{region}|{year}"
            d     = region_year.get(key, {})
            total = d.get("total", 0)
            crit  = d.get("critical", 0) / total * 100 if total > 0 else 0
            row_str += f"{crit:>7.0f}%"
        print(row_str)

    # Save CSV
    if out_rows:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
            w.writeheader()
            w.writerows(out_rows)
        print(f"\nSaved: {output_path}")

    print(f"\nNote: {unknown_count:,} records ({unknown_count/len(rows)*100:.1f}%) "
          f"could not be assigned to a region from affiliation data.")
    print("These are likely records with sparse affiliation fields.")


if __name__ == "__main__":
    main()
