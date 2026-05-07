import csv, os, sys
print("Step 1: imports OK")

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
print(f"Step 2: BASE_DIR={BASE_DIR}")

input_path = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")
print(f"Step 3: input_path={input_path}")
print(f"Step 4: file exists={os.path.exists(input_path)}")

with open(input_path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(f"Step 5: loaded {len(rows)} rows")
print(f"Step 6: columns={list(rows[0].keys())}")

candidates = [
    r for r in rows
    if r.get("year","")[:4] in ("2025","2026")
    and r.get("doi","").strip()
]
print(f"Step 7: candidates={len(candidates)}")

if not candidates:
    print("ERROR: no candidates found")
    sys.exit(1)

print(f"Step 8: first candidate doi='{candidates[0].get('doi','')}'")
print("Step 9: testing CrossRef query...")

import urllib.request, urllib.parse, json
doi = candidates[0]["doi"]
doi_enc = urllib.parse.quote(doi.strip(), safe="")
url = f"https://api.crossref.org/works/{doi_enc}?mailto=dan.poenaru@mcgill.ca"
print(f"  URL: {url[:80]}")

req = urllib.request.Request(url, headers={"User-Agent": "ai-narratives/1.0 (mailto:dan.poenaru@mcgill.ca)"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())

msg = data.get("message", {})
print(f"  CrossRef title: {msg.get('title',['?'])[0][:60]}")
for field in ["published-print", "published-online", "created"]:
    dp = msg.get(field, {}).get("date-parts", [[]])
    if dp and dp[0]:
        print(f"  {field}: {dp[0][0]}")

print("All steps passed.")
