import urllib.request, json, time

doi = "10.1177/1357633X231167613"
url = f"https://api.crossref.org/works/{doi}?mailto=dan.poenaru@mcgill.ca"
print(f"Testing: {url[:60]}...")

try:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ai-narratives/1.0 (mailto:dan.poenaru@mcgill.ca)"}
    )
    start = time.time()
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    elapsed = time.time() - start
    print(f"Success in {elapsed:.1f}s")
    msg = data.get("message", {})
    print(f"Title: {msg.get('title',['?'])[0][:50]}")
    for field in ["published-online", "published-print"]:
        dp = msg.get(field, {}).get("date-parts", [[]])
        if dp and dp[0]:
            print(f"{field}: {dp[0][0]}")
except Exception as e:
    print(f"FAILED: {e}")
