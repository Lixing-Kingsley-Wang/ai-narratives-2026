"""
CrossRef Year Recovery — Async version
Uses aiohttp with 20 concurrent requests for ~20x speedup.
8,673 records at 20 concurrent × 0.9s average = ~7 minutes total.
"""

import csv, os, sys, re, json, time, asyncio
import aiohttp
from collections import Counter

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")
os.makedirs(ANALYSIS_DIR, exist_ok=True)

EMAIL       = "dan.poenaru@mcgill.ca"
BASE_URL    = "https://api.crossref.org/works/"
CONCURRENCY = 20
TIMEOUT     = 12
MAX_RETRIES = 2


async def get_year(session, semaphore, pmid, doi):
    import urllib.parse
    if not doi or not doi.strip():
        return pmid, None
    doi_enc = urllib.parse.quote(doi.strip(), safe="")
    url     = f"{BASE_URL}{doi_enc}?mailto={EMAIL}"
    headers = {"User-Agent": f"ai-narratives/1.0 (mailto:{EMAIL})"}
    async with semaphore:
        for attempt in range(MAX_RETRIES):
            try:
                async with session.get(url, headers=headers,
                                       timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                    if resp.status != 200:
                        return pmid, None
                    data = await resp.json(content_type=None)
                    msg  = data.get("message", {})
                    for field in ["published-online", "published-print", "created"]:
                        dp = msg.get(field, {}).get("date-parts", [[]])
                        if dp and dp[0]:
                            yr = dp[0][0]
                            if isinstance(yr, int) and 2019 <= yr <= 2026:
                                return pmid, yr
                    return pmid, None
            except Exception:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(1)
    return pmid, None


async def main_async():
    input_path  = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")
    output_path = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2_yearcorrected.csv")

    with open(input_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    print(f"CrossRef Year Recovery (Async, {CONCURRENCY} concurrent)")
    print(f"Input: {len(rows):,} records")

    candidates = [
        (r["pmid"], r.get("doi",""))
        for r in rows
        if r.get("pub_year","")[:4] in ("2025","2026")
        and r.get("doi","").strip()
    ]
    print(f"Candidates: {len(candidates):,}")
    print(f"Querying CrossRef...\n")

    semaphore   = asyncio.Semaphore(CONCURRENCY)
    corrections = {}
    n_done      = 0
    start       = time.time()

    connector = aiohttp.TCPConnector(limit=CONCURRENCY, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        CHUNK = 200
        for chunk_start in range(0, len(candidates), CHUNK):
            chunk   = candidates[chunk_start: chunk_start + CHUNK]
            tasks   = [get_year(session, semaphore, pmid, doi) for pmid, doi in chunk]
            results = await asyncio.gather(*tasks)
            for pmid, yr in results:
                if yr is not None:
                    corrections[pmid] = str(yr)
            n_done += len(chunk)
            elapsed = time.time() - start
            rate    = n_done / elapsed if elapsed else 0
            eta     = (len(candidates) - n_done) / rate / 60 if rate else 0
            print(f"  [{n_done:5d}/{len(candidates)}]  "
                  f"years_found={len(corrections)}  ETA:{eta:.1f}min")

    # Apply corrections
    orig_years      = {r["pmid"]: r.get("pub_year","")[:4] for r in rows}
    correction_dist = Counter()
    corrected_rows  = []
    for r in rows:
        new_r = dict(r)
        pmid  = r["pmid"]
        if pmid in corrections:
            cr_year   = corrections[pmid]
            orig_year = orig_years[pmid]
            if cr_year != orig_year and "2019" <= cr_year <= "2026":
                new_r["pub_year"] = cr_year
                correction_dist[f"{orig_year}→{cr_year}"] += 1
        corrected_rows.append(new_r)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(corrected_rows)

    before = Counter(r.get("pub_year","")[:4] for r in rows)
    after  = Counter(r.get("pub_year","")[:4] for r in corrected_rows)

    print(f"\nComplete in {(time.time()-start)/60:.1f} minutes")
    print(f"Corrections: {sum(correction_dist.values()):,}")
    print(f"\n{'Year':<6} {'Before':>8} {'After':>8} {'Change':>8}")
    print("-"*36)
    for y in sorted(set(list(before.keys()) + list(after.keys()))):
        if y and "2020" <= y <= "2027":
            diff     = after.get(y,0) - before.get(y,0)
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            print(f"{y:<6} {before.get(y,0):>8} {after.get(y,0):>8} {diff_str:>8}")

    print(f"\nCorrection patterns:")
    for pat, n in sorted(correction_dist.items(), key=lambda x: -x[1]):
        print(f"  {pat}: {n:,}")

    print(f"\nSaved: {output_path}")
    print(f"\nNext steps:")
    print(f"  copy output\\classified_medical_Q1Q2.csv output\\classified_medical_Q1Q2_original.csv")
    print(f"  copy output\\classified_medical_Q1Q2_yearcorrected.csv output\\classified_medical_Q1Q2.csv")
    print(f"  python show_yearly.py")
    print(f"  python analyse_narratives.py")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
