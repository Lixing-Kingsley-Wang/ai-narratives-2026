"""
Scopus API Diagnostic
Tests different query formulations to find what works with your API key.
Run this before fetch_scopus_legal.py to confirm query syntax.
"""

import requests, os, json
from dotenv import load_dotenv
load_dotenv()

API_KEY  = os.getenv("SCOPUS_API_KEY")
BASE_URL = "https://api.elsevier.com/content/search/scopus"

def test_query(label, query, extra_params=None):
    params = {
        "query":      query,
        "count":      5,
        "apiKey":     API_KEY,
        "httpAccept": "application/json",
    }
    if extra_params:
        params.update(extra_params)
    try:
        r = requests.get(BASE_URL, params=params, timeout=20)
        data  = r.json()
        total = data.get("search-results", {}).get("opensearch:totalResults", "ERROR")
        error = data.get("service-error", {})
        status_msg = f"HTTP {r.status_code} | Total: {total}"
        if error:
            status_msg += f" | Error: {error}"
        print(f"  [{label}] {status_msg}")
        if total not in ("0", "ERROR", 0):
            # Show first title
            entries = data.get("search-results",{}).get("entry",[])
            if entries:
                print(f"    Sample: {entries[0].get('dc:title','')[:80]}")
        return int(total) if str(total).isdigit() else 0
    except Exception as e:
        print(f"  [{label}] FAILED: {e}")
        return 0

print("Scopus API Diagnostic")
print("="*60)

# Test 1: Broadest possible — just AI
print("\nTest 1: Broad AI query (no subject filter)")
test_query("broad AI", 'TITLE-ABS-KEY("artificial intelligence")')

# Test 2: AI + law keywords, no SUBJAREA
print("\nTest 2: AI + law keywords (no SUBJAREA)")
test_query("AI+law noSUBJ",
    'TITLE-ABS-KEY("artificial intelligence" AND "law")')

# Test 3: SUBJAREA alone
print("\nTest 3: SUBJAREA(LAW) alone")
test_query("SUBJAREA only", 'SUBJAREA(LAW)')

# Test 4: Full query with SUBJAREA
print("\nTest 4: Full query with SUBJAREA(LAW)")
test_query("full+SUBJAREA",
    'TITLE-ABS-KEY("artificial intelligence" OR "ChatGPT") AND SUBJAREA(LAW)')

# Test 5: Using SRCTITLE for law journals instead of SUBJAREA
print("\nTest 5: Using journal title filter instead of SUBJAREA")
test_query("journal filter",
    'TITLE-ABS-KEY("artificial intelligence" OR "ChatGPT") '
    'AND SRCTITLE("law" OR "legal" OR "jurisprudence")')

# Test 6: DOCTYPE filter
print("\nTest 6: Full query + year + DOCTYPE")
test_query("full+year+doctype",
    'TITLE-ABS-KEY("artificial intelligence" OR "ChatGPT") '
    'AND SUBJAREA(LAW) AND PUBYEAR = 2023',
    {"field": "dc:identifier,dc:title,prism:publicationName"})

# Test 7: Try with different subject area codes
print("\nTest 7: SUBJAREA(SOCI) — Social Sciences (may include law)")
test_query("SOCI",
    'TITLE-ABS-KEY("artificial intelligence" OR "ChatGPT") AND SUBJAREA(SOCI)')

# Test 8: No subject filter, law in title/abstract
print("\nTest 8: Law in title/abstract, no subject filter, 2023")
test_query("law in text",
    'TITLE-ABS-KEY(("artificial intelligence" OR "ChatGPT") '
    'AND ("law" OR "legal" OR "regulation" OR "liability")) '
    'AND PUBYEAR = 2023')

print("\n" + "="*60)
print("Recommendation: use whichever query above returns >0 results")
print("The working query syntax will be patched into fetch_scopus_legal.py")
