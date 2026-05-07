"""
Q3 vs Q1/Q2 Stance Comparison — AI Narratives Study
Runs stance classification on filtered_medical_all_Q3.csv then
produces direct comparison tables and figures.

Tests hypothesis: Q3 journals show higher alarm rates than Q1/Q2,
consistent with a publication-quality gradient in AI alarmism.
"""

import csv, json, time, os, sys, re
import asyncio
import anthropic
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
load_dotenv()

MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 120
CONCURRENCY = 5
SLEEP_RETRY = 12
MAX_RETRIES = 3

VALID_STANCES = {"Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"}

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")

SYSTEM_PROMPT = """Classify the stance of a medical AI article toward AI/LLM technology.

STANCES:
- Alarm: primarily critical/skeptical. Emphasises dangers, failures, hallucinations, safety risks, ethical problems, or argues AI is not ready. Papers showing AI performs WORSE than clinicians = Alarm.
- Caution: acknowledges both promise AND significant concerns, balance tilts toward concern. Recommends safeguards before deployment.
- Neutral: purely descriptive. Reports metrics without taking a position.
- Cautious Optimism: broadly positive with caveats. Supports careful deployment.
- Advocacy: strongly pro-AI. Emphasises transformative potential, minimal caveats.

PREDICTIVE CLAIM: explicit forward-looking claim about AI's future role (yes/no).

EXAMPLES:
"ENT specialists vs ChatGPT: 1-0" → {"stance":"Alarm","confidence":"High","predictive_claim":"yes"}
"ChatGPT fails safety standards for medication advice" → {"stance":"Alarm","confidence":"High","predictive_claim":"no"}
"AI in echocardiography: promising results, validation needed" → {"stance":"Cautious Optimism","confidence":"High","predictive_claim":"no"}

KEY RULES:
- AI performs worse than humans = Alarm, not Neutral
- AI risks/ethics/governance as main topic = Alarm or Caution
- Do NOT default to Cautious Optimism

Return ONLY valid JSON: {"stance":"...","confidence":"...","predictive_claim":"..."}"""


def extract_pub_year(s):
    m = re.search(r'\b(20\d{2})\b', s or "")
    return m.group(1) if m else ""


async def classify_one(client, semaphore, rec):
    title    = rec.get("title", "")
    abstract = rec.get("abstract", "")
    prompt   = f"Title: {title}"
    if abstract and abstract.strip():
        prompt += f"\nAbstract: {abstract[:400]}"

    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await client.messages.create(
                        model=MODEL,
                        max_tokens=MAX_TOKENS,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": prompt}]
                )
                raw    = response.content[0].text.strip()
                raw    = re.sub(r'^```(?:json)?\s*', '', raw)
                raw    = re.sub(r'\s*```$', '', raw)
                parsed = json.loads(raw, strict=False)
                stance = parsed.get("stance","").strip()
                conf   = parsed.get("confidence","Medium").strip()
                pred   = parsed.get("predictive_claim","no").strip().lower()
                if stance not in VALID_STANCES:
                    raise ValueError(f"Invalid: {stance}")
                return rec, stance, conf, pred
            except Exception as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY * attempt)
                else:
                    return rec, "FAILED", "Low", "no"
    return rec, "FAILED", "Low", "no"


async def classify_q3():
    """Classify Q3 corpus for stance."""
    # Use pre-filtered Q3 if available, otherwise fall back to full Q3
    pf_path = os.path.join(OUTPUT_DIR, "prefiltered_Q3_discourse_eval.csv")
    if os.path.exists(pf_path):
        input_path  = pf_path
        output_path = os.path.join(OUTPUT_DIR, "classified_medical_Q3_filtered.csv")
        print("Using pre-filtered Q3 corpus (discourse+evaluative only)")
    else:
        input_path  = os.path.join(OUTPUT_DIR, "filtered_medical_all_Q3.csv")
        output_path = os.path.join(OUTPUT_DIR, "classified_medical_Q3.csv")
        print("Using full Q3 corpus (no pre-filter)")

    if not os.path.exists(input_path):
        print(f"Q3 input not found: {input_path}")
        return

    with open(input_path, encoding="utf-8") as f:
        all_records = list(csv.DictReader(f))

    print(f"Q3 Stance Classification")
    print(f"Input: {len(all_records):,} Q3 records")

    processed = set()
    if os.path.exists(output_path):
        with open(output_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("stance") not in ("","FAILED",None):
                    processed.add(row["pmid"])
        print(f"Resuming: {len(processed):,} done")

    pending = [r for r in all_records if r["pmid"] not in processed]
    print(f"Pending: {len(pending):,}")

    if not pending:
        print("Q3 classification already complete.")
        return

    in_cols  = list(all_records[0].keys())
    out_cols = in_cols + ["pub_year","stance","confidence","predictive_claim"]
    mode     = "a" if processed else "w"
    client   = AsyncAnthropic()
    sem      = asyncio.Semaphore(CONCURRENCY)
    total    = len(pending)
    done     = 0
    dist     = {}
    start    = time.time()

    with open(output_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        if mode == "w": writer.writeheader()

        CHUNK = 50
        for cs in range(0, len(pending), CHUNK):
            chunk   = pending[cs: cs+CHUNK]
            results = await asyncio.gather(*[classify_one(client, sem, r) for r in chunk])
            for rec, stance, conf, pred in results:
                dist[stance] = dist.get(stance, 0) + 1
                out_row = dict(rec)
                out_row["pub_year"]         = extract_pub_year(rec.get("pub_date",""))
                out_row["stance"]           = stance
                out_row["confidence"]       = conf
                out_row["predictive_claim"] = pred
                writer.writerow(out_row)
            f.flush()
            done += len(chunk)
            elapsed = time.time() - start
            rate    = done/elapsed if elapsed else 0
            eta     = (total-done)/rate/60 if rate else 0
            print(f"  [{done:5d}/{total}] {done/total*100:5.1f}%  "
                  f"{' | '.join(f'{k}:{v}' for k,v in sorted(dist.items()))}  ETA:{eta:.0f}min")

    print(f"\nQ3 classification complete in {(time.time()-start)/60:.1f} min.")


def compare_q1q2_vs_q3():
    """Produce comparison table and save to analysis CSV."""
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    def load_stance_by_year(path):
        if not os.path.exists(path):
            return {}
        import collections
        data = collections.defaultdict(lambda: collections.Counter())
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                year = row.get("pub_year","")
                if not year:
                    year = extract_pub_year(row.get("pub_date",""))
                stance = row.get("stance","")
                if year and "2021" <= year <= "2025" and stance in VALID_STANCES:
                    data[year][stance] += 1
        return data

    q1q2 = load_stance_by_year(os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv"))
    q3_filtered_path = os.path.join(OUTPUT_DIR, "classified_medical_Q3_filtered.csv")
    q3_full_path     = os.path.join(OUTPUT_DIR, "classified_medical_Q3.csv")
    if os.path.exists(q3_filtered_path):
        q3 = load_stance_by_year(q3_filtered_path)
        print("  Q3 corpus: pre-filtered (discourse+evaluative only) — comparable to Q1/Q2")
    else:
        q3 = load_stance_by_year(q3_full_path)
        print("  Q3 corpus: unfiltered — run: python prefilter.py Q3 for fair comparison")

    if not q3:
        print("Q3 classified output not found — run Q3 classification first.")
        return

    out_path = os.path.join(ANALYSIS_DIR, "05_q1q2_vs_q3_stance.csv")
    rows     = []

    print(f"\n{'='*70}")
    print(f"Q1/Q2 vs Q3 STANCE COMPARISON")
    print(f"{'='*70}")
    print(f"{'Year':<6} {'Corpus':<8} {'N':>6}  {'Critical%':>10}  {'Alarm%':>7}  {'CautOpt%':>9}")
    print("-"*55)

    for year in sorted(set(list(q1q2.keys()) + list(q3.keys()))):
        for label, data in [("Q1/Q2", q1q2), ("Q3", q3)]:
            ydata = data.get(year, {})
            total = sum(ydata.values())
            if total == 0:
                continue
            alarm    = ydata.get("Alarm", 0)
            caution  = ydata.get("Caution", 0)
            crit     = (alarm + caution) / total * 100
            alarm_pct= alarm / total * 100
            opt      = ydata.get("Cautious Optimism", 0) / total * 100
            print(f"{year:<6} {label:<8} {total:>6}  {crit:>10.1f}  {alarm_pct:>7.1f}  {opt:>9.1f}")
            rows.append({
                "year": year, "corpus": label, "total": total,
                "Alarm": alarm, "Caution": caution,
                "Neutral": ydata.get("Neutral",0),
                "Cautious Optimism": ydata.get("Cautious Optimism",0),
                "Advocacy": ydata.get("Advocacy",0),
                "critical_pct": round(crit,2),
                "alarm_pct": round(alarm_pct,2),
            })
        print()

    if rows:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"Saved: {out_path}")


async def main_async():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("classify", "all"):
        await classify_q3()

    if mode in ("compare", "all"):
        compare_q1q2_vs_q3()


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
