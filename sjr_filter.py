"""
SJR Journal Filter — v2
Applies Q1/Q2/Q3 quality filter to raw PubMed corpus using SCImago Journal Rankings.

Changes from v1:
  - Improved title normaliser: strips parentheticals, subtitles, stopwords, special chars
  - Hardcoded alias patch table for known PubMed vs SCImago title mismatches
  - Conference proceedings and preprint server exclusion list
  - Q3 capture arm: saves Q3 records to separate file for comparison analysis
  - Unranked ('-') journals excluded (too new for quartile assignment)

Input:  output/raw_medical_YYYY.csv
Output: output/filtered_medical_YYYY_Q1Q2.csv   — Q1+Q2 records
        output/filtered_medical_YYYY_Q3.csv      — Q3 records (comparison arm)
        output/filtered_medical_YYYY_excluded.csv — conferences, preprints, unranked
        output/filtered_medical_YYYY_unmatched.csv — not found in SJR at all

SJR CSVs: input/sjr/sjr_YYYY.csv (semicolon-delimited, from scimagojr.com)
"""

import csv, os, sys, re
from collections import defaultdict

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
SJR_DIR    = os.path.join(BASE_DIR, "input", "sjr")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
YEARS      = list(range(2021, 2027))

# ── conference proceedings and preprint servers — exclude entirely ─────────────
EXCLUDE_JOURNALS = {
    # Conference proceedings — exact normalised matches
    "annual international conference ieee engineering medicine biology society",
    "annual international conference ieee engineering medicine biology society ieee engineering medicine biology society annual international conference",
    "amia annual symposium proceedings amia symposium",
    "amia symposium",
    "studies health technology informatics",
    "proceedings spie",
    "lecture notes computer science",
    "lecture notes networks systems",
    "ifac papersonline",
    # Preprint servers
    "medrxiv",
    "medrxiv preprint server health sciences",
    "arxiv",
    "biorxiv",
    "biorxiv preprint server biology",
    "ssrn",
    "research square",
}

# Keyword fragments — if any appear in normalised title, exclude regardless
EXCLUDE_KEYWORDS = [
    "annual international conference",
    "annual symposium proceedings",
    "conference proceedings",
    "preprint server",
    "lecture notes",
]

# ── alias patch table: PubMed title → SCImago title ───────────────────────────
# Key: normalised PubMed title  Value: normalised SCImago title
# Only needed where normaliser alone can't bridge the gap
ALIAS_PATCH = {
    # MDPI journals — parenthetical country suffix in PubMed
    "sensors basel switzerland":              "sensors",
    "diagnostics basel switzerland":          "diagnostics",
    "bioengineering basel switzerland":       "bioengineering",
    "ijerph":                                 "international journal environmental research public health",
    "international journal environmental research public health basel switzerland": "international journal environmental research public health",
    # Subtitle/acronym mismatches
    "journal american medical informatics association jamia": "journal american medical informatics association",
    "abdominal radiology new york":           "abdominal radiology",
    "medicine united states":                 "medicine united states",
    "ultrasound medicine biology":            "ultrasound medicine biology",
    "medical biological engineering computing": "medical biological engineering computing",
    "biomedical physics engineering express": "biomedical physics engineering express",
    "translational vision science technology": "translational vision science technology",
    "advanced science weinheim":              "advanced science",
    "advanced science weinheim baden wurttemberg germany": "advanced science",
    "ieee transactions neural systems rehabilitation engineering publication ieee engineering medicine biology society": "ieee transactions neural systems rehabilitation engineering",
    "ieee transactions bio medical engineering": "ieee transactions biomedical engineering",
    "ieee transactions biomedical engineering": "ieee transactions biomedical engineering",
    "international journal surgery london england": "international journal surgery",
    "journal magnetic resonance imaging jmri": "journal magnetic resonance imaging",
    "european archives oto rhino laryngology official journal european federation oto rhino laryngological societies eufos affiliated german society oto rhino laryngology head neck surgery": "european archives oto rhino laryngology",
    "arthroscopy journal arthroscopic related surgery official publication arthroscopy association north america international arthroscopy association": "arthroscopy journal arthroscopic related surgery",
    "computerized medical imaging graphics official journal computerized medical imaging society": "computerized medical imaging graphics",
    "radiotherapy oncology journal european society therapeutic radiology oncology": "radiotherapy oncology",
    # Radiology AI — period vs colon mismatch
    "radiology artificial intelligence":      "radiology artificial intelligence",
    # Full title → short SCImago title
    "ajr american journal roentgenology":     "american journal roentgenology",
    "ajnr american journal neuroradiology":   "american journal neuroradiology",
    "otolaryngology head neck surgery official journal american academy otolaryngology head neck surgery": "otolaryngology head neck surgery",
    "otolaryngology head neck surgery":       "otolaryngology head neck surgery",
    "la radiologia medica":                   "radiologia medica",
    "radiologia medica":                      "radiologia medica",
    "canadian association radiologists journal journal lassociation canadienne radiologistes": "canadian association radiologists journal",
    "medicine kaunas lithuania":              "medicina",
    "medicina kaunas lithuania":              "medicina",
    "journal imaging informatics medicine":   "journal imaging informatics medicine",
}


# ── normaliser ────────────────────────────────────────────────────────────────
STOPWORDS = {"the", "a", "an", "of", "in", "and", "for", "on", "with",
             "its", "by", "to", "from", "at", "or"}

def normalise(t):
    t = t.lower().strip()
    t = re.sub(r"\(.*?\)", "", t)           # remove parentheticals
    t = re.sub(r":.*$", "", t)              # remove subtitle after colon
    t = re.sub(r"[^a-z0-9 ]", " ", t)      # special chars → space (handles & . / - …)
    words = [w for w in t.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(words).strip()


# ── load SJR data ─────────────────────────────────────────────────────────────
def load_sjr(year):
    path = os.path.join(SJR_DIR, f"sjr_{year}.csv")
    if not os.path.exists(path):
        print(f"  WARNING: SJR file missing for {year}: {path}")
        return {}

    title_map = {}
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            title    = row.get("Title", "").strip()
            quartile = row.get("SJR Best Quartile", "").strip()
            if title and quartile and quartile != "-":
                norm = normalise(title)
                if norm:
                    title_map[norm] = quartile

    print(f"  SJR {year}: {len(title_map)} ranked titles loaded")
    return title_map


# ── quartile lookup for one record ───────────────────────────────────────────
def get_quartile(journal_raw, title_map):
    """Returns 'Q1', 'Q2', 'Q3', or None."""
    norm = normalise(journal_raw)
    if not norm:
        return None

    # Apply alias patch first
    norm = ALIAS_PATCH.get(norm, norm)

    return title_map.get(norm)


def is_excluded(journal_raw):
    norm = normalise(journal_raw)
    if norm in EXCLUDE_JOURNALS:
        return True
    return any(kw in norm for kw in EXCLUDE_KEYWORDS)


# ── main filter ───────────────────────────────────────────────────────────────
def filter_file(input_path, year_tag):
    out_q1q2     = os.path.join(OUTPUT_DIR, f"filtered_medical_{year_tag}_Q1Q2.csv")
    out_q3       = os.path.join(OUTPUT_DIR, f"filtered_medical_{year_tag}_Q3.csv")
    out_excluded = os.path.join(OUTPUT_DIR, f"filtered_medical_{year_tag}_excluded.csv")
    out_unmatched= os.path.join(OUTPUT_DIR, f"filtered_medical_{year_tag}_unmatched.csv")

    print(f"\nFiltering: {os.path.basename(input_path)}")

    # Pre-load SJR for all years (records may span years due to indexing lag)
    sjr_cache = {str(y): load_sjr(y) for y in YEARS}

    with open(input_path, encoding="utf-8") as f:
        records = list(csv.DictReader(f))
    print(f"  Input: {len(records)} records")

    q1q2_rows, q3_rows, excluded_rows, unmatched_rows = [], [], [], []
    year_stats = defaultdict(lambda: {"total":0,"q1":0,"q2":0,"q3":0,"excluded":0,"unmatched":0})

    for rec in records:
        journal = rec.get("journal", "")
        year    = rec.get("year", "")[:4]
        year_stats[year]["total"] += 1

        # Step 1: exclude conferences and preprints
        if is_excluded(journal):
            rec["sjr_quartile"] = "EXCLUDED"
            excluded_rows.append(rec)
            year_stats[year]["excluded"] += 1
            continue

        # Step 2: look up quartile using publication year's SJR
        title_map = sjr_cache.get(year, sjr_cache.get("2024", {}))
        quartile  = get_quartile(journal, title_map)

        if quartile == "Q1":
            rec["sjr_quartile"] = "Q1"
            q1q2_rows.append(rec)
            year_stats[year]["q1"] += 1
        elif quartile == "Q2":
            rec["sjr_quartile"] = "Q2"
            q1q2_rows.append(rec)
            year_stats[year]["q2"] += 1
        elif quartile == "Q3":
            rec["sjr_quartile"] = "Q3"
            q3_rows.append(rec)
            year_stats[year]["q3"] += 1
        else:
            rec["sjr_quartile"] = ""
            unmatched_rows.append(rec)
            year_stats[year]["unmatched"] += 1

    # Write outputs
    out_cols = list(records[0].keys()) + ["sjr_quartile"] if records else []

    def write_csv(path, rows):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=out_cols)
            w.writeheader()
            w.writerows(rows)

    write_csv(out_q1q2, q1q2_rows)
    write_csv(out_q3, q3_rows)
    write_csv(out_excluded, excluded_rows)
    write_csv(out_unmatched, unmatched_rows)

    # Summary
    total    = len(records)
    n_q1q2   = len(q1q2_rows)
    n_q3     = len(q3_rows)
    n_excl   = len(excluded_rows)
    n_unm    = len(unmatched_rows)
    eligible = total - n_excl

    print(f"\n  {'Total records:':<28} {total:>6}")
    print(f"  {'Excluded (conf/preprint):':<28} {n_excl:>6}")
    print(f"  {'Eligible (after exclusion):':<28} {eligible:>6}")
    print(f"  {'Q1+Q2 (primary corpus):':<28} {n_q1q2:>6}  ({n_q1q2/eligible*100:.1f}% of eligible)")
    print(f"  {'Q3 (comparison arm):':<28} {n_q3:>6}  ({n_q3/eligible*100:.1f}% of eligible)")
    print(f"  {'Unmatched:':<28} {n_unm:>6}  ({n_unm/eligible*100:.1f}% of eligible)")

    print(f"\n  Year breakdown (Q1+Q2 | Q3 | excl | unmatched):")
    for y in sorted(year_stats):
        s = year_stats[y]
        t = s["total"]
        print(f"    {y}: {t:5d} total | "
              f"Q1={s['q1']:4d} Q2={s['q2']:4d} Q3={s['q3']:4d} | "
              f"excl={s['excluded']:4d} | unmatched={s['unmatched']:4d}")

    print(f"\n  Outputs:")
    print(f"    Q1+Q2:     {out_q1q2}")
    print(f"    Q3:        {out_q3}")
    print(f"    Excluded:  {out_excluded}")
    print(f"    Unmatched: {out_unmatched}")

    return q1q2_rows, q3_rows


# ── entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if len(sys.argv) > 1:
        year_tag   = sys.argv[1]
        input_file = os.path.join(OUTPUT_DIR, f"raw_medical_{year_tag}.csv")
    else:
        year_tag   = "all"
        input_file = os.path.join(OUTPUT_DIR, "raw_medical_all.csv")

    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)

    filter_file(input_file, year_tag)
    print(f"\nNext step: run classify_stance.py on filtered_medical_{year_tag}_Q1Q2.csv")
# patch marker
