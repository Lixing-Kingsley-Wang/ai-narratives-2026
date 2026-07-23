"""
Geographic extraction from first_affiliation (parser-based, no LLM)
==================================================================

Reads:  output/classified_medical_Q1Q2.csv  (v1, in parent checkout)
Writes: output/geography_classifications.csv  (in worktree)

Algorithm:
  1. Lowercase + search for explicit country names (longest-alias first).
  2. If none matched, try US-state pattern (", XX " or "XX ZIP") — Canada
     province codes are excluded.
  3. If still none, try curated major US medical-research cities.
  4. Map matched country → one of 8 regions (per plan) + Unknown.

Special rules (per user):
  - "Georgia" alone is treated as US state, NOT the country. Country Georgia
    is matched only by "Tbilisi" or "Republic of Georgia".
  - Bare "Korea" defaults to South Korea (DPRK has essentially zero
    biomedical publishing footprint).
"""
import csv, os, re, sys
from collections import Counter

PARENT_OUTPUT = "/Users/kingslywang/repos/ai-narratives-2026/output"
HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE_OUTPUT = os.path.abspath(os.path.join(HERE, "..", "output"))

INPUT_PATH  = os.path.join(PARENT_OUTPUT,   "classified_medical_Q1Q2.csv")
OUTPUT_PATH = os.path.join(WORKTREE_OUTPUT, "geography_classifications.csv")

# ── 8 regions (plan's taxonomy) ───────────────────────────────────────────────
REGION_NA       = "North America"
REGION_WEU      = "Western Europe"
REGION_EEU      = "Eastern Europe"
REGION_EAS      = "East Asia"
REGION_SSEAS    = "South/Southeast Asia"
REGION_MENA     = "Middle East / North Africa"
REGION_SSA      = "Sub-Saharan Africa"
REGION_LAOC     = "Latin America / Oceania"
REGION_UNKNOWN  = "Unknown"

# ── country → region ──────────────────────────────────────────────────────────
COUNTRY_TO_REGION = {
    # North America
    "USA": REGION_NA, "Canada": REGION_NA,

    # Western Europe
    "United Kingdom": REGION_WEU, "Germany": REGION_WEU, "France": REGION_WEU,
    "Italy": REGION_WEU, "Spain": REGION_WEU, "Netherlands": REGION_WEU,
    "Switzerland": REGION_WEU, "Sweden": REGION_WEU, "Belgium": REGION_WEU,
    "Austria": REGION_WEU, "Ireland": REGION_WEU, "Portugal": REGION_WEU,
    "Norway": REGION_WEU, "Denmark": REGION_WEU, "Finland": REGION_WEU,
    "Iceland": REGION_WEU, "Greece": REGION_WEU, "Luxembourg": REGION_WEU,
    "Malta": REGION_WEU, "Cyprus": REGION_WEU, "Monaco": REGION_WEU,
    "Liechtenstein": REGION_WEU, "Andorra": REGION_WEU, "San Marino": REGION_WEU,

    # Eastern Europe
    "Poland": REGION_EEU, "Russia": REGION_EEU, "Czech Republic": REGION_EEU,
    "Hungary": REGION_EEU, "Romania": REGION_EEU, "Bulgaria": REGION_EEU,
    "Ukraine": REGION_EEU, "Belarus": REGION_EEU, "Slovakia": REGION_EEU,
    "Slovenia": REGION_EEU, "Croatia": REGION_EEU, "Serbia": REGION_EEU,
    "Bosnia and Herzegovina": REGION_EEU, "Lithuania": REGION_EEU,
    "Latvia": REGION_EEU, "Estonia": REGION_EEU, "Moldova": REGION_EEU,
    "Albania": REGION_EEU, "North Macedonia": REGION_EEU,
    "Montenegro": REGION_EEU, "Kosovo": REGION_EEU,

    # East Asia
    "China": REGION_EAS, "Japan": REGION_EAS, "South Korea": REGION_EAS,
    "Taiwan": REGION_EAS, "Hong Kong": REGION_EAS, "Singapore": REGION_EAS,
    "Macau": REGION_EAS, "Mongolia": REGION_EAS, "North Korea": REGION_EAS,

    # South / Southeast Asia
    "India": REGION_SSEAS, "Pakistan": REGION_SSEAS, "Bangladesh": REGION_SSEAS,
    "Sri Lanka": REGION_SSEAS, "Nepal": REGION_SSEAS, "Bhutan": REGION_SSEAS,
    "Afghanistan": REGION_SSEAS, "Thailand": REGION_SSEAS,
    "Vietnam": REGION_SSEAS, "Indonesia": REGION_SSEAS,
    "Malaysia": REGION_SSEAS, "Philippines": REGION_SSEAS,
    "Myanmar": REGION_SSEAS, "Cambodia": REGION_SSEAS, "Laos": REGION_SSEAS,
    "Brunei": REGION_SSEAS, "East Timor": REGION_SSEAS, "Maldives": REGION_SSEAS,

    # Middle East / North Africa
    "Saudi Arabia": REGION_MENA, "Iran": REGION_MENA, "Israel": REGION_MENA,
    "Turkey": REGION_MENA, "Egypt": REGION_MENA, "UAE": REGION_MENA,
    "Jordan": REGION_MENA, "Lebanon": REGION_MENA, "Qatar": REGION_MENA,
    "Bahrain": REGION_MENA, "Kuwait": REGION_MENA, "Oman": REGION_MENA,
    "Iraq": REGION_MENA, "Syria": REGION_MENA, "Yemen": REGION_MENA,
    "Palestine": REGION_MENA, "Morocco": REGION_MENA, "Algeria": REGION_MENA,
    "Tunisia": REGION_MENA, "Libya": REGION_MENA, "Sudan": REGION_MENA,

    # Sub-Saharan Africa
    "South Africa": REGION_SSA, "Nigeria": REGION_SSA, "Kenya": REGION_SSA,
    "Ethiopia": REGION_SSA, "Ghana": REGION_SSA, "Tanzania": REGION_SSA,
    "Uganda": REGION_SSA, "Cameroon": REGION_SSA, "Senegal": REGION_SSA,
    "Zimbabwe": REGION_SSA, "Zambia": REGION_SSA, "Rwanda": REGION_SSA,
    "Mozambique": REGION_SSA, "Botswana": REGION_SSA, "Mali": REGION_SSA,
    "Burkina Faso": REGION_SSA, "Cote d'Ivoire": REGION_SSA,
    "Madagascar": REGION_SSA, "Malawi": REGION_SSA, "Angola": REGION_SSA,
    "Benin": REGION_SSA, "Burundi": REGION_SSA, "Sierra Leone": REGION_SSA,
    "Liberia": REGION_SSA, "Niger": REGION_SSA, "Gambia": REGION_SSA,
    "Namibia": REGION_SSA, "DRC": REGION_SSA, "Republic of Congo": REGION_SSA,
    "Eswatini": REGION_SSA, "Lesotho": REGION_SSA, "Mauritius": REGION_SSA,
    "Seychelles": REGION_SSA, "Eritrea": REGION_SSA, "South Sudan": REGION_SSA,
    "Somalia": REGION_SSA, "Togo": REGION_SSA,

    # Latin America / Oceania (plan groups these together)
    "Brazil": REGION_LAOC, "Mexico": REGION_LAOC, "Argentina": REGION_LAOC,
    "Chile": REGION_LAOC, "Colombia": REGION_LAOC, "Peru": REGION_LAOC,
    "Venezuela": REGION_LAOC, "Ecuador": REGION_LAOC, "Bolivia": REGION_LAOC,
    "Paraguay": REGION_LAOC, "Uruguay": REGION_LAOC, "Cuba": REGION_LAOC,
    "Dominican Republic": REGION_LAOC, "Costa Rica": REGION_LAOC,
    "Panama": REGION_LAOC, "Guatemala": REGION_LAOC, "Honduras": REGION_LAOC,
    "El Salvador": REGION_LAOC, "Nicaragua": REGION_LAOC, "Haiti": REGION_LAOC,
    "Jamaica": REGION_LAOC, "Trinidad and Tobago": REGION_LAOC,
    "Puerto Rico": REGION_LAOC,
    "Australia": REGION_LAOC, "New Zealand": REGION_LAOC, "Fiji": REGION_LAOC,
    "Papua New Guinea": REGION_LAOC,

    # Caucasus / Central Asia — splice into Eastern Europe (regional norm)
    "Georgia (country)": REGION_EEU, "Armenia": REGION_EEU,
    "Azerbaijan": REGION_EEU, "Kazakhstan": REGION_EEU,
    "Uzbekistan": REGION_EEU, "Kyrgyzstan": REGION_EEU,
    "Tajikistan": REGION_EEU, "Turkmenistan": REGION_EEU,
}

# ── alias → canonical (longer aliases first to win) ───────────────────────────
COUNTRY_ALIASES = {
    # USA — many variants
    "united states of america": "USA", "united states": "USA",
    "u.s.a.": "USA", "u.s.a": "USA", "u.s.": "USA", "usa": "USA",
    "u s a": "USA",

    # UK
    "united kingdom": "United Kingdom", "great britain": "United Kingdom",
    "u.k.": "United Kingdom", "uk": "United Kingdom",
    "england": "United Kingdom", "scotland": "United Kingdom",
    "wales": "United Kingdom", "northern ireland": "United Kingdom",

    # Canada
    "canada": "Canada",

    # China (mainland + SARs + Taiwan separate)
    "people's republic of china": "China", "p.r. china": "China",
    "pr china": "China", "p.r.china": "China", "mainland china": "China",
    "china": "China",
    "hong kong": "Hong Kong", "macau": "Macau", "macao": "Macau",
    "taiwan": "Taiwan", "republic of china": "Taiwan",

    # Korea
    "republic of korea": "South Korea", "south korea": "South Korea",
    "north korea": "North Korea", "dprk": "North Korea",
    "korea": "South Korea",  # bare → South per user decision

    # Other East/SE/S Asia
    "japan": "Japan", "singapore": "Singapore", "mongolia": "Mongolia",
    "india": "India", "pakistan": "Pakistan", "bangladesh": "Bangladesh",
    "sri lanka": "Sri Lanka", "nepal": "Nepal", "bhutan": "Bhutan",
    "afghanistan": "Afghanistan", "thailand": "Thailand",
    "vietnam": "Vietnam", "viet nam": "Vietnam",
    "indonesia": "Indonesia", "malaysia": "Malaysia",
    "philippines": "Philippines", "myanmar": "Myanmar", "burma": "Myanmar",
    "cambodia": "Cambodia",
    "lao people's democratic republic": "Laos", "laos": "Laos",
    "brunei": "Brunei",
    "east timor": "East Timor", "timor-leste": "East Timor",
    "maldives": "Maldives",

    # Western Europe
    "germany": "Germany", "france": "France", "italy": "Italy",
    "spain": "Spain", "españa": "Spain",
    "netherlands": "Netherlands", "the netherlands": "Netherlands",
    "switzerland": "Switzerland", "sweden": "Sweden", "belgium": "Belgium",
    "austria": "Austria", "ireland": "Ireland", "portugal": "Portugal",
    "norway": "Norway", "denmark": "Denmark", "finland": "Finland",
    "iceland": "Iceland", "greece": "Greece", "luxembourg": "Luxembourg",
    "malta": "Malta", "cyprus": "Cyprus", "monaco": "Monaco",
    "liechtenstein": "Liechtenstein", "andorra": "Andorra",
    "san marino": "San Marino",

    # Eastern Europe
    "poland": "Poland",
    "russian federation": "Russia", "russia": "Russia",
    "czech republic": "Czech Republic", "czechia": "Czech Republic",
    "hungary": "Hungary", "romania": "Romania", "bulgaria": "Bulgaria",
    "ukraine": "Ukraine", "belarus": "Belarus", "slovakia": "Slovakia",
    "slovenia": "Slovenia", "croatia": "Croatia", "serbia": "Serbia",
    "bosnia and herzegovina": "Bosnia and Herzegovina", "bosnia": "Bosnia and Herzegovina",
    "lithuania": "Lithuania", "latvia": "Latvia", "estonia": "Estonia",
    "moldova": "Moldova", "albania": "Albania",
    "north macedonia": "North Macedonia", "macedonia": "North Macedonia",
    "montenegro": "Montenegro", "kosovo": "Kosovo",

    # Caucasus / Central Asia
    "tbilisi": "Georgia (country)", "republic of georgia": "Georgia (country)",
    "armenia": "Armenia", "azerbaijan": "Azerbaijan",
    "kazakhstan": "Kazakhstan", "uzbekistan": "Uzbekistan",
    "kyrgyzstan": "Kyrgyzstan", "tajikistan": "Tajikistan",
    "turkmenistan": "Turkmenistan",

    # MENA
    "saudi arabia": "Saudi Arabia", "iran": "Iran",
    "islamic republic of iran": "Iran", "israel": "Israel",
    "türkiye": "Turkey", "turkiye": "Turkey", "turkey": "Turkey",
    "egypt": "Egypt", "u.a.e.": "UAE", "uae": "UAE",
    "united arab emirates": "UAE",
    "jordan": "Jordan", "lebanon": "Lebanon", "qatar": "Qatar",
    "bahrain": "Bahrain", "kuwait": "Kuwait", "oman": "Oman",
    "iraq": "Iraq", "syria": "Syria", "yemen": "Yemen",
    "palestine": "Palestine", "morocco": "Morocco", "algeria": "Algeria",
    "tunisia": "Tunisia", "libya": "Libya", "sudan": "Sudan",

    # Sub-Saharan Africa
    "south africa": "South Africa", "nigeria": "Nigeria", "kenya": "Kenya",
    "ethiopia": "Ethiopia", "ghana": "Ghana", "tanzania": "Tanzania",
    "uganda": "Uganda", "cameroon": "Cameroon", "senegal": "Senegal",
    "zimbabwe": "Zimbabwe", "zambia": "Zambia", "rwanda": "Rwanda",
    "mozambique": "Mozambique", "botswana": "Botswana", "mali": "Mali",
    "burkina faso": "Burkina Faso", "ivory coast": "Cote d'Ivoire",
    "cote d'ivoire": "Cote d'Ivoire", "côte d'ivoire": "Cote d'Ivoire",
    "madagascar": "Madagascar", "malawi": "Malawi", "angola": "Angola",
    "benin": "Benin", "burundi": "Burundi", "sierra leone": "Sierra Leone",
    "liberia": "Liberia", "niger": "Niger", "gambia": "Gambia",
    "namibia": "Namibia",
    "democratic republic of the congo": "DRC", "drc": "DRC",
    "republic of congo": "Republic of Congo", "congo": "Republic of Congo",
    "eswatini": "Eswatini", "swaziland": "Eswatini",
    "lesotho": "Lesotho", "mauritius": "Mauritius",
    "seychelles": "Seychelles", "eritrea": "Eritrea",
    "south sudan": "South Sudan", "somalia": "Somalia", "togo": "Togo",

    # Latin America / Oceania
    "brazil": "Brazil", "brasil": "Brazil",
    "mexico": "Mexico", "méxico": "Mexico",
    "argentina": "Argentina", "chile": "Chile", "colombia": "Colombia",
    "peru": "Peru", "venezuela": "Venezuela", "ecuador": "Ecuador",
    "bolivia": "Bolivia", "paraguay": "Paraguay", "uruguay": "Uruguay",
    "cuba": "Cuba", "dominican republic": "Dominican Republic",
    "costa rica": "Costa Rica", "panama": "Panama", "guatemala": "Guatemala",
    "honduras": "Honduras", "el salvador": "El Salvador",
    "nicaragua": "Nicaragua", "haiti": "Haiti", "jamaica": "Jamaica",
    "trinidad and tobago": "Trinidad and Tobago",
    "puerto rico": "Puerto Rico",
    "australia": "Australia", "new zealand": "New Zealand",
    "fiji": "Fiji", "papua new guinea": "Papua New Guinea",
}

# US states (full names) — fold into USA. Multi-word ones must come BEFORE
# overlapping country names ("new mexico" before "mexico") via longest-first.
# "Georgia" defaults to US state per project decision (country Georgia only
# matched by "tbilisi" or "republic of georgia").
US_STATE_NAMES = [
    "alabama","alaska","arizona","arkansas","california","colorado",
    "connecticut","delaware","florida","georgia","hawaii","idaho","illinois",
    "indiana","iowa","kansas","kentucky","louisiana","maine","maryland",
    "massachusetts","michigan","minnesota","mississippi","missouri","montana",
    "nebraska","nevada","new hampshire","new jersey","new mexico","new york",
    "north carolina","north dakota","ohio","oklahoma","oregon","pennsylvania",
    "rhode island","south carolina","south dakota","tennessee","texas",
    "utah","vermont","virginia","washington","west virginia","wisconsin",
    "wyoming","washington d.c.","washington dc",
]
for _state in US_STATE_NAMES:
    COUNTRY_ALIASES[_state] = "USA"

# Sorted longest-first so multi-word aliases win
ALIASES_SORTED = sorted(COUNTRY_ALIASES.items(), key=lambda kv: -len(kv[0]))
ALIAS_RE = [
    (re.compile(r"\b" + re.escape(alias) + r"\b", re.IGNORECASE), country)
    for alias, country in ALIASES_SORTED
]

# ── US-state fallback ─────────────────────────────────────────────────────────
US_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
    "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
    "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
    "TX","UT","VT","VA","WA","WV","WI","WY","DC",
}
# pattern: ", XX " or ", XX." or ", XX," or ", XX-" or end-of-string
US_STATE_RE = re.compile(
    r",\s*(" + "|".join(US_STATES) + r")\b"
)

# ── US major-medical-city fallback ────────────────────────────────────────────
US_CITY_RE = re.compile(
    r"\b(?:" + "|".join([
        "Bethesda", "New York", "Boston", "Philadelphia", "Chicago",
        "Los Angeles", "San Francisco", "Houston", "Cleveland", "Baltimore",
        "Atlanta", "Rochester", "Pittsburgh", "Seattle", "Durham",
        "St\\. Louis", "Saint Louis", "Cincinnati", "Detroit", "Miami",
        "Phoenix", "San Diego", "Dallas", "Nashville", "Minneapolis",
        "Indianapolis", "Denver", "Portland, OR", "New Haven", "Iowa City",
        "Ann Arbor", "Chapel Hill", "Charleston", "Birmingham, AL",
        "Memphis", "Louisville", "Columbus", "Tampa", "Orlando", "Jacksonville",
    ]) + r")\b",
    re.IGNORECASE,
)


def assign(aff):
    """Return (country, region) for one affiliation string."""
    if not aff or not str(aff).strip():
        return None, REGION_UNKNOWN
    text = str(aff)

    # Pass 1: explicit country
    for rx, country in ALIAS_RE:
        if rx.search(text):
            return country, COUNTRY_TO_REGION.get(country, REGION_UNKNOWN)

    # Pass 2: US-state pattern
    if US_STATE_RE.search(text):
        return "USA", REGION_NA

    # Pass 3: major US medical-research city
    if US_CITY_RE.search(text):
        return "USA", REGION_NA

    return None, REGION_UNKNOWN


def main():
    # Quick dev mode for sanity-check (-n N samples to stdout, no write)
    sample_n = None
    if len(sys.argv) > 1 and sys.argv[1] == "sample":
        sample_n = int(sys.argv[2]) if len(sys.argv) > 2 else 25

    os.makedirs(WORKTREE_OUTPUT, exist_ok=True)

    n = n_known = n_unknown = 0
    country_counts = Counter()
    region_counts = Counter()
    rows_out = []

    with open(INPUT_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            aff = r.get("first_affiliation", "") or ""
            country, region = assign(aff)
            n += 1
            if region == REGION_UNKNOWN:
                n_unknown += 1
            else:
                n_known += 1
            country_counts[country or "(none)"] += 1
            region_counts[region] += 1
            rows_out.append({
                "pmid": r["pmid"],
                "first_affiliation_short": aff[:200],
                "country": country or "",
                "region": region,
            })

    if sample_n:
        # print sample
        import random
        rng = random.Random(42)
        idxs = rng.sample(range(len(rows_out)), sample_n)
        print(f"=== {sample_n} random extractions (seed=42) ===")
        for i, ix in enumerate(idxs, 1):
            r = rows_out[ix]
            aff = r["first_affiliation_short"]
            aff_show = aff if len(aff) <= 150 else aff[:147] + "..."
            print(f"[{i:2}] pmid={r['pmid']:>10}  {r['country']!s:<22} {r['region']}")
            print(f"     {aff_show}")
    else:
        with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as fout:
            w = csv.DictWriter(fout, fieldnames=["pmid","first_affiliation_short","country","region"])
            w.writeheader()
            w.writerows(rows_out)
        print(f"Wrote {len(rows_out):,} rows to {OUTPUT_PATH}")

    print(f"\n=== Geography distribution (n={n:,}) ===")
    print(f"Known: {n_known:,} ({n_known/n*100:.1f}%)   Unknown: {n_unknown:,} ({n_unknown/n*100:.1f}%)")
    print(f"\nRegions:")
    for region, count in region_counts.most_common():
        pct = count/n*100
        print(f"  {region:<32} {count:>6,}  ({pct:.1f}%)")
    print(f"\nTop 15 countries:")
    for country, count in country_counts.most_common(15):
        print(f"  {country:<28} {count:>6,}")


if __name__ == "__main__":
    main()
