"""
Scopus Retrieval — Legal Arm
AI Narratives in Healthcare vs Law: Comparative Temporal Stance Analysis

Retrieves legal scholarship on AI from Scopus API, 2021–2026.
Restricted to Q1/Q2 law journals by SJR quartile.

Requirements:
  pip install requests python-dotenv
  SCOPUS_API_KEY in .env file (from Elsevier Developer Portal via McGill)

Output: output/raw_legal_YYYY.csv per year
        output/raw_legal_all.csv (deduplicated)

Column schema matches medical corpus for pipeline compatibility:
  pmid (scopus EID), year, pub_date, title, abstract,
  journal, journal_abbr, pub_type, first_author,
  first_affiliation, doi
"""

import csv, time, os, sys, re, json
import requests
from datetime import date
from dotenv import load_dotenv
load_dotenv()

# ── constants ──────────────────────────────────────────────────────────────────
BASE_URL    = "https://api.elsevier.com/content/search/scopus"
BATCH_SIZE  = 25    # Scopus max per request for full abstracts
SLEEP       = 1.0   # Scopus rate limit: 3 req/sec with API key
SLEEP_RETRY = 15
MAX_RETRIES = 3
API_KEY     = os.getenv("SCOPUS_API_KEY")

COLUMNS = [
    "pmid", "year", "pub_date", "title", "abstract",
    "journal", "journal_abbr", "pub_type",
    "first_author", "first_affiliation", "doi",
    "scopus_eid", "cited_by",
]

# ── Scopus query ───────────────────────────────────────────────────────────────
# SUBJAREA(LAW) restricts to law journals
# TITLE-ABS-KEY searches title, abstract, and keywords
# Note: SUBJAREA(LAW) not available with this API key — using two-arm approach:
# Arm 1: Law/legal journal titles (SRCTITLE filter)
# Arm 2: AI + legal keywords in title/abstract (content filter)
# Combined with OR to maximise recall

# Focused query: AI must appear in title/abstract AND legal context required
# SRCTITLE restricted to explicit law/legal review journals only
# This avoids "law of physics", "Boyle's law" etc.

QUERY_TEMPLATE = (
    'TITLE-ABS-KEY('
    '("artificial intelligence" OR "large language model" OR "large language models" '
    'OR "ChatGPT" OR "GPT-4" OR "GPT-3" OR "generative AI" '
    'OR "generative artificial intelligence" OR "foundation model") '
    'AND '
    '("legal" OR "law review" OR "jurisprudence" OR "attorney" OR "lawyer" '
    'OR "judicial" OR "tort" OR "due process" OR "intellectual property law" '
    'OR "legal liability" OR "legal regulation" OR "legal framework" '
    'OR "court" OR "legislation" OR "legal ethics" OR "bar association")'
    ') '
    'AND PUBYEAR = {year} '
    'AND DOCTYPE(ar OR re OR ed OR le OR no)'
)

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]


def build_query(year):
    return QUERY_TEMPLATE.format(year=year)


# ── check API key ──────────────────────────────────────────────────────────────
def check_api_key():
    if not API_KEY:
        print("ERROR: SCOPUS_API_KEY not found in environment or .env file.")
        print("Get your API key from: https://dev.elsevier.com/")
        print("McGill institutional access required.")
        print("Add to .env file: SCOPUS_API_KEY=your-key-here")
        return False

    # Test with a minimal query
    params = {
        "query":   "artificial intelligence",
        "count":   1,
        "field":   "dc:identifier",
        "apiKey":  API_KEY,
        "httpAccept": "application/json",
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=15)
        if r.status_code == 200:
            print(f"Scopus API key valid. Ready to retrieve.")
            return True
        elif r.status_code == 401:
            print(f"ERROR: API key rejected (401). Check key and institutional access.")
            return False
        elif r.status_code == 429:
            print(f"ERROR: Rate limit hit (429). Wait a minute and retry.")
            return False
        else:
            print(f"ERROR: Unexpected status {r.status_code}: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"ERROR: Connection failed: {e}")
        return False


# ── get total count for a year ─────────────────────────────────────────────────
def get_count(year):
    params = {
        "query":      build_query(year),
        "count":      0,
        "apiKey":     API_KEY,
        "httpAccept": "application/json",
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(BASE_URL, params=params, timeout=30)
            r.raise_for_status()
            data  = r.json()
            count = int(data["search-results"]["opensearch:totalResults"])
            return count
        except Exception as e:
            print(f"  count attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(SLEEP_RETRY)
            else:
                return 0
    return 0


# ── fetch one batch ────────────────────────────────────────────────────────────
def fetch_batch(year, start):
    params = {
        "query":   build_query(year),
        "start":   start,
        "count":   BATCH_SIZE,
        "field":   (
            "dc:identifier,eid,dc:title,dc:description,prism:publicationName,"
            "prism:coverDate,prism:doi,dc:creator,affiliation,"
            "prism:aggregationType,subtype,subtypeDescription,citedby-count"
        ),
        "apiKey":  API_KEY,
        "httpAccept": "application/json",
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(BASE_URL, params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"    fetch attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(SLEEP_RETRY * attempt)
            else:
                raise
    raise RuntimeError("Max retries exceeded")


# ── parse Scopus JSON entry ────────────────────────────────────────────────────
def parse_entry(entry):
    rec = {col: "" for col in COLUMNS}

    # ID — use EID as primary key (maps to 'pmid' column for pipeline compatibility)
    eid = entry.get("eid", "")
    rec["scopus_eid"] = eid
    rec["pmid"]       = eid  # reuse pmid column as unique ID

    rec["title"]    = entry.get("dc:title", "").strip()
    rec["abstract"] = entry.get("dc:description", "").strip()
    rec["journal"]  = entry.get("prism:publicationName", "").strip()
    rec["doi"]      = entry.get("prism:doi", "").strip()
    rec["cited_by"] = entry.get("citedby-count", "")

    # Date
    cover_date = entry.get("prism:coverDate", "")  # format: YYYY-MM-DD
    if cover_date:
        parts = cover_date.split("-")
        year  = parts[0] if parts else ""
        month = MONTHS[int(parts[1])-1] if len(parts) > 1 and parts[1].isdigit() else ""
        rec["pub_date"] = f"{year} {month}".strip()
        rec["year"]     = year

    # Author + affiliation
    creator = entry.get("dc:creator", "")
    rec["first_author"] = creator.strip()

    affiliations = entry.get("affiliation", [])
    if affiliations and isinstance(affiliations, list):
        aff = affiliations[0]
        parts = [
            aff.get("affilname",""),
            aff.get("affiliation-city",""),
            aff.get("affiliation-country",""),
        ]
        rec["first_affiliation"] = ", ".join(p for p in parts if p)

    # Publication type
    subtype = entry.get("subtypeDescription", entry.get("subtype",""))
    rec["pub_type"] = subtype

    return rec


# ── deduplication ──────────────────────────────────────────────────────────────
def deduplicate(records):
    seen, out = set(), []
    for r in records:
        key = r.get("doi") or r.get("scopus_eid") or r.get("pmid")
        if key and key not in seen:
            seen.add(key)
            out.append(r)
    return out


# ── process one year ───────────────────────────────────────────────────────────
def process_year(year, output_dir):
    output_path = os.path.join(output_dir, f"raw_legal_{year}.csv")

    # Resume
    fetched_eids = set()
    if os.path.exists(output_path):
        with open(output_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                fetched_eids.add(row["scopus_eid"])
        print(f"  Resuming {year}: {len(fetched_eids)} already saved")

    print(f"\nYear {year}:")
    count = get_count(year)
    print(f"  Total records: {count}")

    if count == 0:
        print(f"  No records — skipping")
        return 0

    time.sleep(SLEEP)

    mode        = "a" if fetched_eids else "w"
    new_records = 0
    total_batches = (count + BATCH_SIZE - 1) // BATCH_SIZE

    with open(output_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if mode == "w":
            writer.writeheader()

        for batch_idx, start in enumerate(range(0, count, BATCH_SIZE)):
            print(f"  Batch {batch_idx+1}/{total_batches} "
                  f"(records {start}–{min(start+BATCH_SIZE-1, count-1)})",
                  end="", flush=True)

            try:
                data    = fetch_batch(year, start)
                entries = data.get("search-results", {}).get("entry", [])
                written = 0
                for entry in entries:
                    rec = parse_entry(entry)
                    if rec["scopus_eid"] and rec["scopus_eid"] not in fetched_eids:
                        writer.writerow(rec)
                        fetched_eids.add(rec["scopus_eid"])
                        written += 1
                        new_records += 1
                print(f" → {written} new")
                f.flush()

            except Exception as e:
                print(f" FAILED: {e}")
                print(f"  Progress saved. Re-run to resume.")
                break

            time.sleep(SLEEP)

    print(f"  Year {year}: {new_records} new records → {output_path}")
    return new_records


def merge_years(years, output_dir):
    all_records = []
    for year in years:
        path = os.path.join(output_dir, f"raw_legal_{year}.csv")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                all_records.extend(list(csv.DictReader(f)))
    deduped  = deduplicate(all_records)
    out_path = os.path.join(output_dir, "raw_legal_all.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(deduped)
    print(f"\nMerged: {len(all_records)} total → {len(deduped)} deduplicated → {out_path}")
    return out_path


# ── entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Check API key first
    if not check_api_key():
        print("\nTo get Scopus API access:")
        print("1. Ask your McGill librarian for an Elsevier API key")
        print("2. Or register at https://dev.elsevier.com/ with your McGill email")
        print("3. Add SCOPUS_API_KEY=your-key to your .env file")
        sys.exit(1)

    years = [int(y) for y in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2021, 2027))

    print(f"\nScopus Legal Arm Retrieval")
    print(f"Years: {years}")
    print(f"Output: {output_dir}")
    print(f"{'='*60}")

    total = 0
    for year in years:
        total += process_year(year, output_dir)

    if len(years) > 1:
        merge_years(years, output_dir)

    print(f"\n{'='*60}")
    print(f"Done. Total new records: {total}")
    print(f"Next step: run sjr_filter.py on raw_legal_all.csv")
    print(f"  (SJR law journal files needed in input/sjr/)")
