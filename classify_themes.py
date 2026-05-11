"""
Thematic Classifier — AI Narratives Study
Classifies concern themes in Alarm + Caution papers.
Uses native AsyncAnthropic client for true async performance.

Themes: replacement, hallucination, safety_clinical, ethics_bias,
        cognitive, education, regulation, existential, data_privacy, other

Output: output/analysis/thematic_alarm.csv
"""

import csv, json, time, os, sys, re
import asyncio
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
# override=True forces .env to win over shell environment vars (shell may have empty ANTHROPIC_API_KEY)
load_dotenv(override=True)

MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 150
CONCURRENCY = 5
SLEEP_RETRY = 10
MAX_RETRIES = 3

VALID_THEMES = {
    "replacement", "hallucination", "safety_clinical", "ethics_bias",
    "cognitive", "education", "regulation", "existential",
    "data_privacy", "other"
}

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")

SYSTEM_PROMPT = """Identify concern themes in critical medical AI papers.

THEMES (return 1-3 most prominent):
- replacement: AI replacing physicians/clinicians/jobs; job displacement fears
- hallucination: AI errors, hallucinations, factual inaccuracies, unreliable outputs
- safety_clinical: patient safety risks, clinical harm, diagnostic errors
- ethics_bias: algorithmic bias, fairness, equity, ethical problems, discrimination
- cognitive: cognitive offloading, deskilling, over-reliance, loss of clinical skills
- education: medical education, student learning, training, residency, examinations
- regulation: governance, regulation, oversight, policy, liability, accountability
- existential: existential threat to medicine, disruption of doctor-patient relationship
- data_privacy: data privacy, security, consent, patient data misuse
- other: critical concern not fitting above

Return ONLY valid JSON: {"themes": ["theme1", "theme2"]}"""


def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        text += f"\nAbstract: {abstract[:400]}"
    return f"Identify concern themes:\n\n{text}"


def extract_pub_year(s):
    m = re.search(r'\b(20\d{2})\b', s or "")
    return m.group(1) if m else ""


async def classify_themes(client, semaphore, rec):
    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": build_prompt(
                        rec.get("title", ""), rec.get("abstract", "")
                    )}]
                )
                raw    = response.content[0].text.strip()
                raw    = re.sub(r'^```(?:json)?\s*', '', raw)
                raw    = re.sub(r'\s*```$', '', raw)
                parsed = json.loads(raw, strict=False)
                themes = [t for t in parsed.get("themes", []) if t in VALID_THEMES]
                if not themes:
                    themes = ["other"]
                return rec, themes

            except Exception as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY)
                else:
                    return rec, ["other"]
    return rec, ["other"]


async def main_async():
    input_path  = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")
    output_path = os.path.join(ANALYSIS_DIR, "thematic_alarm.csv")
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        all_records = [r for r in csv.DictReader(f)
                       if r.get("stance") in ("Alarm", "Caution")]

    print(f"Thematic Classifier — Alarm + Caution papers")
    print(f"Model: {MODEL} | Concurrency: {CONCURRENCY}")
    print(f"Input: {len(all_records):,} critical-stance records")

    processed = set()
    if os.path.exists(output_path):
        with open(output_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                processed.add(row["pmid"])
        print(f"Resuming: {len(processed):,} already done")

    pending = [r for r in all_records if r["pmid"] not in processed]
    print(f"Pending: {len(pending):,}")
    print(f"{'='*60}")

    if not pending:
        print("Already complete.")
        print_summary(output_path)
        return

    in_cols  = list(all_records[0].keys())
    out_cols = in_cols + ["themes", "theme_1", "theme_2", "theme_3"]
    mode     = "a" if processed else "w"

    client    = AsyncAnthropic()
    semaphore = asyncio.Semaphore(CONCURRENCY)
    total     = len(pending)
    done      = 0
    theme_dist= {}
    start     = time.time()

    with open(output_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        if mode == "w":
            writer.writeheader()

        CHUNK = 50
        for chunk_start in range(0, total, CHUNK):
            chunk   = pending[chunk_start: chunk_start + CHUNK]
            tasks   = [classify_themes(client, semaphore, rec) for rec in chunk]
            results = await asyncio.gather(*tasks)

            for rec, themes in results:
                for t in themes:
                    theme_dist[t] = theme_dist.get(t, 0) + 1
                out_row           = dict(rec)
                out_row["themes"] = "|".join(themes)
                out_row["theme_1"]= themes[0] if len(themes) > 0 else ""
                out_row["theme_2"]= themes[1] if len(themes) > 1 else ""
                out_row["theme_3"]= themes[2] if len(themes) > 2 else ""
                writer.writerow(out_row)

            f.flush()
            done    += len(chunk)
            elapsed  = time.time() - start
            rate     = done / elapsed if elapsed else 0
            eta      = (total - done) / rate / 60 if rate else 0
            print(f"  [{done:5d}/{total}] {done/total*100:5.1f}%  ETA:{eta:.0f}min")

    print(f"\nComplete in {(time.time()-start)/60:.1f} minutes.")
    print_summary(output_path)


def print_summary(output_path):
    if not os.path.exists(output_path):
        return

    import collections
    theme_by_year  = collections.defaultdict(lambda: collections.Counter())
    total_by_year  = collections.Counter()

    with open(output_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            year   = row.get("pub_year", "") or extract_pub_year(row.get("pub_date", ""))
            themes = [t for t in row.get("themes", "").split("|") if t]
            if year and "2021" <= year <= "2026":
                total_by_year[year] += 1
                for t in themes:
                    theme_by_year[year][t] += 1

    years = sorted(total_by_year.keys())
    theme_order = [
        "replacement", "hallucination", "safety_clinical", "ethics_bias",
        "cognitive", "education", "regulation", "existential",
        "data_privacy", "other"
    ]

    print(f"\nTheme × Year (% of critical papers that year):")
    print(f"{'n critical:':<22}" + "".join(f"{total_by_year[y]:>8}" for y in years))
    print(f"{'Theme':<22}" + "".join(f"{y:>8}" for y in years))
    print("-" * (22 + 8 * len(years)))
    for theme in theme_order:
        row_str = f"{theme:<22}"
        for year in years:
            n   = theme_by_year[year].get(theme, 0)
            t   = total_by_year[year]
            pct = n / t * 100 if t else 0
            row_str += f"{pct:>7.0f}%"
        print(row_str)

    print(f"\nTotal critical papers analysed: {sum(total_by_year.values()):,}")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
