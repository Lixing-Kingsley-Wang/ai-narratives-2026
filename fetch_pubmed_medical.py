"""
PubMed Retrieval — Medical Arm
AI Narratives in Healthcare: Temporal Stance & Topic Analysis (2021–2026)

Definitive strategy: split each year into monthly queries, each well under
the 9,999 NCBI idlist cap. Collect all PMIDs across 12 months, deduplicate,
then efetch by direct &id= in batches of 200.

Output: raw_medical_YYYY.csv per year
        raw_medical_all.csv (full run, deduplicated)
"""

import csv, time, os, sys, json, xml.etree.ElementTree as ET
from datetime import date
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

# ── constants ──────────────────────────────────────────────────────────────────
BASE_URL      = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
BATCH_SIZE    = 200
SLEEP_ESEARCH = 0.5
SLEEP_EFETCH  = 0.4
SLEEP_RETRY   = 12
MAX_RETRIES   = 3
EMAIL         = os.environ["EMAIL"]
TOOL_NAME     = "ai_narratives_study"

COLUMNS = [
    "pmid", "year", "pub_date", "title", "abstract",
    "journal", "journal_abbr", "pub_type",
    "first_author", "first_affiliation", "doi",
]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

# ── query — month-scoped using PDAT ───────────────────────────────────────────
# Use YYYY/MM/DD[PDAT] range — reliable for splitting within a year
QUERY_TEMPLATE = (
    '("artificial intelligence"[MeSH] OR "machine learning"[MeSH] OR '
    '"deep learning"[tiab] OR "large language model"[tiab] OR '
    '"large language models"[tiab] OR "generative AI"[tiab] OR '
    '"generative artificial intelligence"[tiab] OR ChatGPT[tiab] OR '
    '"GPT-5"[tiab] OR "GPT-4.5"[tiab] OR "GPT-4o"[tiab] OR '
    '"GPT-4"[tiab] OR "GPT-3"[tiab] OR GPT4[tiab] OR '
    '"foundation model"[tiab] OR "foundation models"[tiab] OR '
    '"natural language processing"[MeSH]) '
    'AND (medicine[sb] OR "patients"[tiab] OR "clinical"[tiab] OR '
    '"physician"[tiab] OR "surgeon"[tiab] OR "hospital"[tiab] OR '
    '"diagnosis"[tiab] OR "treatment"[tiab] OR "healthcare"[tiab] OR '
    '"health care"[tiab]) '
    'AND ("{year_start}"[PDAT] : "{year_end}"[PDAT]) '
    'AND ("journal article"[pt] OR "editorial"[pt] OR "review"[pt] OR '
    '"comment"[pt] OR "letter"[pt]) '
    'AND english[lang]'
)


def month_date_range(year, month_idx):
    """
    Returns (start_str, end_str) for PDAT filter.
    month_idx: 1-12
    Format: YYYY/MM/DD
    """
    start = date(year, month_idx, 1)
    if month_idx == 12:
        end = date(year, 12, 31)
    else:
        end = date(year, month_idx + 1, 1)
        from datetime import timedelta
        end = end - timedelta(days=1)
    return start.strftime("%Y/%m/%d"), end.strftime("%Y/%m/%d")


def build_query(year, month_idx):
    start, end = month_date_range(year, month_idx)
    return QUERY_TEMPLATE.format(year_start=start, year_end=end)


# ── esearch: get PMIDs for one month (single call, always < 9999) ─────────────
def esearch_month(year, month_idx):
    params = {
        "db":      "pubmed",
        "term":    build_query(year, month_idx),
        "retmax":  9999,
        "retmode": "json",
        "email":   EMAIL,
        "tool":    TOOL_NAME,
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(BASE_URL + "esearch.fcgi", params=params, timeout=30)
            r.raise_for_status()
            result = json.loads(r.text, strict=False)["esearchresult"]
            count  = int(result["count"])
            ids    = result.get("idlist", [])
            month_name = MONTHS[month_idx - 1]
            if count > len(ids):
                print(f"    WARNING {month_name}: count={count} > retrieved={len(ids)} "
                      f"— month has >9999 records, needs further splitting")
            else:
                print(f"    {month_name}: {count} records")
            return ids
        except Exception as e:
            print(f"    esearch {MONTHS[month_idx-1]} attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(SLEEP_RETRY)
            else:
                return []
    return []


# ── efetch by direct id list ───────────────────────────────────────────────────
def efetch_by_ids(pmid_list):
    params = {
        "db":      "pubmed",
        "id":      ",".join(pmid_list),
        "retmode": "xml",
        "email":   EMAIL,
        "tool":    TOOL_NAME,
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(BASE_URL + "efetch.fcgi", params=params, timeout=60)
            r.raise_for_status()
            return r.text
        except Exception as e:
            print(f"    efetch attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(SLEEP_RETRY * attempt)
            else:
                raise


# ── XML parsing ────────────────────────────────────────────────────────────────
def safe_text(element, path, default=""):
    node = element.find(path)
    return node.text.strip() if node is not None and node.text else default


def parse_pubmed_xml(xml_text):
    records = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"    XML parse error: {e}")
        return records

    for article in root.findall(".//PubmedArticle"):
        rec = {col: "" for col in COLUMNS}

        rec["pmid"] = safe_text(article, ".//PMID")

        title_node = article.find(".//ArticleTitle")
        if title_node is not None:
            rec["title"] = "".join(title_node.itertext()).strip()

        abstract_parts = []
        for atext in article.findall(".//AbstractText"):
            label = atext.get("Label", "")
            text  = "".join(atext.itertext()).strip()
            if text:
                abstract_parts.append(f"{label}: {text}" if label else text)
        rec["abstract"] = " ".join(abstract_parts)

        rec["journal"]      = safe_text(article, ".//Journal/Title")
        rec["journal_abbr"] = safe_text(article, ".//Journal/ISOAbbreviation")

        pub_year  = safe_text(article, ".//PubDate/Year")
        pub_month = safe_text(article, ".//PubDate/Month", "Jan")
        medline   = safe_text(article, ".//PubDate/MedlineDate")
        if pub_year:
            rec["pub_date"] = f"{pub_year} {pub_month}".strip()
            rec["year"]     = pub_year
        elif medline:
            rec["pub_date"] = medline
            rec["year"]     = medline[:4]

        pub_types       = [pt.text for pt in article.findall(
                           ".//PublicationTypeList/PublicationType") if pt.text]
        rec["pub_type"] = "; ".join(pub_types)

        authors = article.findall(".//AuthorList/Author")
        if authors:
            first = authors[0]
            rec["first_author"] = (
                f"{safe_text(first, 'LastName')} {safe_text(first, 'ForeName')}".strip()
            )
            aff = first.find(".//AffiliationInfo/Affiliation")
            if aff is not None:
                rec["first_affiliation"] = "".join(aff.itertext()).strip()

        for id_node in article.findall(".//ArticleIdList/ArticleId"):
            if id_node.get("IdType") == "doi":
                rec["doi"] = id_node.text or ""

        records.append(rec)

    return records


# ── deduplication ──────────────────────────────────────────────────────────────
def deduplicate_pmids(pmid_list):
    return list(dict.fromkeys(pmid_list))


def deduplicate_records(records):
    seen, out = set(), []
    for r in records:
        if r["pmid"] not in seen:
            seen.add(r["pmid"])
            out.append(r)
    return out


# ── main processing loop ───────────────────────────────────────────────────────
def process_year(year, output_dir):
    output_path = os.path.join(output_dir, f"raw_medical_{year}.csv")

    fetched_pmids = set()
    if os.path.exists(output_path):
        with open(output_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                fetched_pmids.add(row["pmid"])
        print(f"  Resuming {year}: {len(fetched_pmids)} already saved")

    # Determine which months to query based on current date
    current_year  = date.today().year
    current_month = date.today().month
    if year < current_year:
        months = list(range(1, 13))
    else:
        months = list(range(1, current_month + 1))

    print(f"\nYear {year}: collecting PMIDs across {len(months)} months...")
    all_pmids = []
    for m in months:
        ids = esearch_month(year, m)
        all_pmids.extend(ids)
        time.sleep(SLEEP_ESEARCH)

    all_pmids = deduplicate_pmids(all_pmids)
    print(f"  Total unique PMIDs for {year}: {len(all_pmids)}")

    pending = [p for p in all_pmids if p not in fetched_pmids]
    print(f"  {len(pending)} remaining to fetch")

    if not pending:
        print(f"  Already complete.")
        return 0

    mode          = "a" if fetched_pmids else "w"
    new_records   = 0
    total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE

    with open(output_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if mode == "w":
            writer.writeheader()

        for batch_idx, start in enumerate(range(0, len(pending), BATCH_SIZE)):
            batch_pmids = pending[start: start + BATCH_SIZE]

            print(f"  Batch {batch_idx+1}/{total_batches} "
                  f"({len(batch_pmids)} PMIDs)", end="", flush=True)

            try:
                xml_text = efetch_by_ids(batch_pmids)
                records  = parse_pubmed_xml(xml_text)
                written  = 0
                for rec in records:
                    if rec["pmid"] not in fetched_pmids:
                        writer.writerow(rec)
                        fetched_pmids.add(rec["pmid"])
                        written += 1
                        new_records += 1
                print(f" → {written} new")
                f.flush()

            except Exception as e:
                print(f" FAILED: {e}")
                print(f"  Progress saved. Re-run to resume.")
                break

            time.sleep(SLEEP_EFETCH)

    print(f"  Year {year}: {new_records} new records → {output_path}")
    return new_records


def merge_years(years, output_dir):
    all_records = []
    for year in years:
        path = os.path.join(output_dir, f"raw_medical_{year}.csv")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                all_records.extend(list(csv.DictReader(f)))
    deduped  = deduplicate_records(all_records)
    out_path = os.path.join(output_dir, "raw_medical_all.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(deduped)
    print(f"\nMerged: {len(all_records)} total → {len(deduped)} deduplicated → {out_path}")
    return out_path


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    years = [int(y) for y in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2021, 2027))

    print(f"AI Narratives — PubMed Medical Arm")
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
    print(f"Next step: run sjr_filter.py to apply Q1/Q2/Q3 journal filter")
