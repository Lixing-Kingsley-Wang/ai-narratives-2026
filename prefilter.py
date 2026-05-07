"""
Pre-Filter — AI Narratives Study (Async version)
Uses asyncio with 10 concurrent API calls for ~10× speedup.
Resumes cleanly from existing output files.

Input:  output/filtered_medical_all_Q1Q2.csv
Output: output/prefiltered_discourse_eval.csv
        output/prefiltered_application.csv
"""

import csv, json, time, os, sys, re
import asyncio
import anthropic
from dotenv import load_dotenv
load_dotenv()

# ── constants ──────────────────────────────────────────────────────────────────
MODEL       = "claude-haiku-4-5-20251001"
MAX_TOKENS  = 120
CONCURRENCY = 8      # parallel API calls — safe for Tier 2 rate limits
SLEEP_RETRY = 10
MAX_RETRIES = 3
VALID_TYPES = {"discourse", "evaluative", "application"}

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

SYSTEM_PROMPT = """You are classifying medical journal articles into one of three categories based on whether and how they engage with artificial intelligence (AI) as a subject.

CATEGORIES:

- discourse: AI/LLM is the MAIN SUBJECT of discussion. The paper reflects on, debates, or analyses AI's role, safety, ethics, implications, governance, risks, or future in medicine. Includes editorials, perspectives, opinion pieces, and narrative reviews WHERE THE CENTRAL TOPIC IS AI ITSELF.

- evaluative: The paper TESTS or BENCHMARKS a specific AI system (especially LLMs like ChatGPT, GPT-4) and draws explicit conclusions about its accuracy, safety, reliability, limitations, or clinical readiness.

- application: The paper USES AI/ML as a technical tool to solve a clinical problem. AI is a method, not the subject. When in doubt, classify as application.

CRITICAL RULES:
- Only classify as discourse if AI/LLM is clearly the CENTRAL topic
- Only classify as evaluative if there is explicit testing of an AI system with clinical conclusions
- Everything else = application

Return ONLY valid JSON: {"paper_type": "...", "type_confidence": "..."}
No preamble, no explanation."""


def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        text += f"\nAbstract: {abstract[:300]}"
    return f"Classify this paper:\n\n{text}"


def extract_pub_year(pub_date_str):
    m = re.search(r'\b(20\d{2})\b', pub_date_str or "")
    return m.group(1) if m else ""


# ── async classification ───────────────────────────────────────────────────────
async def classify_one(client, semaphore, rec):
    """Classify a single record asynchronously."""
    title    = rec.get("title", "")
    abstract = rec.get("abstract", "")
    prompt   = build_prompt(title, abstract)

    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Use the sync client in a thread pool to avoid blocking
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: client.messages.create(
                        model=MODEL,
                        max_tokens=MAX_TOKENS,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": prompt}]
                    )
                )
                raw    = response.content[0].text.strip()
                raw    = re.sub(r'^```(?:json)?\s*', '', raw)
                raw    = re.sub(r'\s*```$', '', raw)
                parsed = json.loads(raw, strict=False)

                ptype = parsed.get("paper_type", "").strip().lower()
                conf  = parsed.get("type_confidence", "Medium").strip()

                if ptype not in VALID_TYPES:
                    ptype = "application"
                if conf not in ("High", "Medium", "Low"):
                    conf = "Medium"

                return rec, ptype, conf

            except Exception as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY * attempt)
                else:
                    return rec, "application", "Low"

    return rec, "application", "Low"


# ── main ───────────────────────────────────────────────────────────────────────
async def main_async():
    pilot = len(sys.argv) > 1 and sys.argv[1] == "pilot"
    q3_mode = len(sys.argv) > 1 and sys.argv[1] == "Q3"

    if pilot:
        input_path = os.path.join(OUTPUT_DIR, "pilot_200.csv")
        out_de     = os.path.join(OUTPUT_DIR, "pilot_prefiltered_discourse_eval.csv")
        out_ap     = os.path.join(OUTPUT_DIR, "pilot_prefiltered_application.csv")
    elif sys.argv[1] == "Q3" if len(sys.argv) > 1 else False:
        input_path = os.path.join(OUTPUT_DIR, "filtered_medical_all_Q3.csv")
        out_de     = os.path.join(OUTPUT_DIR, "prefiltered_Q3_discourse_eval.csv")
        out_ap     = os.path.join(OUTPUT_DIR, "prefiltered_Q3_application.csv")
    else:
        input_path = os.path.join(OUTPUT_DIR, "filtered_medical_all_Q1Q2.csv")
        out_de     = os.path.join(OUTPUT_DIR, "prefiltered_discourse_eval.csv")
        out_ap     = os.path.join(OUTPUT_DIR, "prefiltered_application.csv")

    client = anthropic.Anthropic()

    with open(input_path, encoding="utf-8") as f:
        all_records = list(csv.DictReader(f))

    print(f"Pre-Filter — AI Narratives Study (Async, {CONCURRENCY} concurrent calls)")
    print(f"Mode: {'PILOT' if pilot else 'Q3 CORPUS' if q3_mode else 'FULL Q1/Q2 CORPUS'}")
    print(f"Input: {len(all_records):,} records")

    # Resume: load already-processed PMIDs
    processed = set()
    for path in (out_de, out_ap):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    processed.add(row["pmid"])
    if processed:
        print(f"Resuming: {len(processed):,} already done")

    pending = [r for r in all_records if r["pmid"] not in processed]
    print(f"Pending: {len(pending):,} records")
    print(f"{'='*60}")

    if not pending:
        print("Already complete.")
        return

    in_cols  = list(all_records[0].keys())
    out_cols = in_cols + ["pub_year", "paper_type", "type_confidence"]
    mode_de  = "a" if os.path.exists(out_de) else "w"
    mode_ap  = "a" if os.path.exists(out_ap) else "w"

    semaphore  = asyncio.Semaphore(CONCURRENCY)
    total      = len(pending)
    done_count = 0
    type_dist  = {}
    start_time = time.time()

    with open(out_de, mode_de, newline="", encoding="utf-8") as f_de, \
         open(out_ap, mode_ap, newline="", encoding="utf-8") as f_ap:

        writer_de = csv.DictWriter(f_de, fieldnames=out_cols)
        writer_ap = csv.DictWriter(f_ap, fieldnames=out_cols)
        if mode_de == "w": writer_de.writeheader()
        if mode_ap == "w": writer_ap.writeheader()

        # Process in chunks to allow periodic flushing and progress reporting
        CHUNK = 100
        for chunk_start in range(0, len(pending), CHUNK):
            chunk   = pending[chunk_start: chunk_start + CHUNK]
            tasks   = [classify_one(client, semaphore, rec) for rec in chunk]
            results = await asyncio.gather(*tasks)

            for rec, ptype, conf in results:
                pub_year = extract_pub_year(rec.get("pub_date", ""))
                type_dist[ptype] = type_dist.get(ptype, 0) + 1
                out_row = dict(rec)
                out_row["pub_year"]        = pub_year
                out_row["paper_type"]      = ptype
                out_row["type_confidence"] = conf
                if ptype in ("discourse", "evaluative"):
                    writer_de.writerow(out_row)
                else:
                    writer_ap.writerow(out_row)

            f_de.flush()
            f_ap.flush()
            done_count += len(chunk)

            elapsed  = time.time() - start_time
            rate     = done_count / elapsed if elapsed > 0 else 0
            eta_mins = (total - done_count) / rate / 60 if rate > 0 else 0
            dist_str = " | ".join(f"{k}:{v}" for k, v in sorted(type_dist.items()))
            print(f"  [{done_count:6d}/{total}] {done_count/total*100:5.1f}%  "
                  f"{dist_str}  ETA: {eta_mins:.0f}min")

    elapsed = time.time() - start_time
    n_de = type_dist.get("discourse", 0) + type_dist.get("evaluative", 0)
    n_ap = type_dist.get("application", 0)
    print(f"\n{'='*60}")
    print(f"Complete in {elapsed/60:.1f} minutes.")
    print(f"  Discourse + Evaluative: {n_de:,}  ({n_de/total*100:.1f}%)")
    print(f"  Application:            {n_ap:,}  ({n_ap/total*100:.1f}%)")
    print(f"\nNext step: python classify_stance.py")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
