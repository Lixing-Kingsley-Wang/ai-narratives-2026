"""Quick count check for Scopus legal query across all years."""
import requests, os, re
from dotenv import load_dotenv
load_dotenv()

API_KEY  = os.getenv("SCOPUS_API_KEY")
BASE_URL = "https://api.elsevier.com/content/search/scopus"

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

total_all = 0
for year in range(2021, 2027):
    query = QUERY_TEMPLATE.format(year=year)
    params = {
        "query":      query,
        "count":      0,
        "apiKey":     API_KEY,
        "httpAccept": "application/json",
    }
    r    = requests.get(BASE_URL, params=params, timeout=20)
    n    = int(r.json().get("search-results",{}).get("opensearch:totalResults",0))
    total_all += n
    print(f"  {year}: {n:,} records")

print(f"  Total 2021-2026: {total_all:,}")
print(f"\nTarget range: 3,000-10,000 total")
if total_all > 15000:
    print("Still too broad — consider adding more restrictive terms")
elif total_all < 1000:
    print("Too narrow — consider relaxing terms")
else:
    print("Good range — proceed with fetch_scopus_legal.py")
