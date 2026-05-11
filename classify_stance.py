"""
Stance Classifier — AI Narratives Study (Async version)
Uses asyncio with 5 concurrent Sonnet calls for ~5× speedup.
Compressed prompt reduces token cost by ~40%.

Output columns:
  pub_year, stance, confidence, predictive_claim, stance_model, stance_raw

Input:  output/prefiltered_discourse_eval.csv
Output: output/classified_medical_Q1Q2.csv
"""

import csv, json, time, os, sys, re
import asyncio
import anthropic
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
# override=True forces .env to win over shell environment vars (shell may have empty ANTHROPIC_API_KEY)
load_dotenv(override=True)

# ── constants ──────────────────────────────────────────────────────────────────
MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 120
CONCURRENCY = 5       # concurrent Sonnet calls — conservative for rate limits
SLEEP_RETRY = 12
MAX_RETRIES = 3

VALID_STANCES    = {"Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"}
VALID_CONFIDENCE = {"High", "Medium", "Low"}

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# ── compressed prompt with few-shot examples ───────────────────────────────────
SYSTEM_PROMPT = """Classify the stance of a medical AI article toward AI/LLM technology.

STANCES (Q1/Q2 journals use measured language — calibrate accordingly):
- Alarm: primarily critical/skeptical. Emphasises dangers, failures, hallucinations, safety risks, ethical problems, or argues AI is not ready. Papers showing AI performs WORSE than clinicians = Alarm.
- Caution: acknowledges both promise AND significant concerns, balance tilts toward concern. Recommends safeguards before deployment.
- Neutral: purely descriptive. Reports metrics without taking a position. No evaluative language.
- Cautious Optimism: broadly positive with caveats. Supports careful deployment.
- Advocacy: strongly pro-AI. Emphasises transformative potential, minimal caveats.

PREDICTIVE CLAIM: explicit forward-looking claim about AI's future role (yes/no).

EXAMPLES:
"ENT specialists vs ChatGPT: 1-0" → {"stance":"Alarm","confidence":"High","predictive_claim":"yes"}
"ChatGPT fails safety standards for medication advice" → {"stance":"Alarm","confidence":"High","predictive_claim":"no"}
"Implications of LLMs for dental medicine" (balanced, concern-leaning) → {"stance":"Caution","confidence":"High","predictive_claim":"no"}
"AI in echocardiography: promising results, validation needed" → {"stance":"Cautious Optimism","confidence":"High","predictive_claim":"no"}
"AI will transform radiology within five years" → {"stance":"Advocacy","confidence":"High","predictive_claim":"yes"}
"Performance benchmarking of segmentation algorithm" → {"stance":"Neutral","confidence":"High","predictive_claim":"no"}

KEY RULES:
- AI performs worse than humans = Alarm, not Neutral
- AI risks/ethics/governance as main topic = Alarm or Caution, not Neutral
- Do NOT default to Cautious Optimism

Return ONLY valid JSON: {"stance":"...","confidence":"...","predictive_claim":"..."}"""


def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        # No truncation (was [:400]). 400 chars = ~70 words = LLM saw only abstract intro,
        # missing findings/conclusions where stance signal lives. Sonnet 4.6's 200K-token
        # context easily fits any PubMed abstract (typical max ~10K chars). Cost impact
        # at corpus scale ~$15-30 incremental, negligible.
        text += f"\nAbstract: {abstract}"
    return text


def extract_pub_year(pub_date_str):
    m = re.search(r'\b(20\d{2})\b', pub_date_str or "")
    return m.group(1) if m else ""


# ── async classification ───────────────────────────────────────────────────────
async def classify_one(client, semaphore, rec):
    title    = rec.get("title", "")
    abstract = rec.get("abstract", "")

    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await client.messages.create(
                        model=MODEL,
                        max_tokens=MAX_TOKENS,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": build_prompt(title, abstract)}]
                )
                raw    = response.content[0].text.strip()
                raw    = re.sub(r'^```(?:json)?\s*', '', raw)
                raw    = re.sub(r'\s*```$', '', raw)
                parsed = json.loads(raw, strict=False)

                stance     = parsed.get("stance", "").strip()
                confidence = parsed.get("confidence", "Medium").strip()
                predictive = parsed.get("predictive_claim", "no").strip().lower()

                if stance not in VALID_STANCES:
                    raise ValueError(f"Invalid stance: {stance}")
                if confidence not in VALID_CONFIDENCE:
                    confidence = "Medium"
                if predictive not in ("yes", "no"):
                    predictive = "no"

                return rec, stance, confidence, predictive, raw

            except (json.JSONDecodeError, ValueError) as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY)
                else:
                    return rec, "FAILED", "Low", "no", f"ERROR: {e}"
            except Exception as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY * attempt)
                else:
                    return rec, "FAILED", "Low", "no", f"ERROR: {e}"

    return rec, "FAILED", "Low", "no", "ERROR: semaphore"


# ── main ───────────────────────────────────────────────────────────────────────
async def main_async():
    arm = sys.argv[1] if len(sys.argv) > 1 else "full"

    if arm == "pilot":
        input_path  = os.path.join(OUTPUT_DIR, "pilot_prefiltered_discourse_eval.csv")
        output_path = os.path.join(OUTPUT_DIR, "classified_pilot.csv")
    elif arm == "Q3":
        input_path  = os.path.join(OUTPUT_DIR, "filtered_medical_all_Q3.csv")
        output_path = os.path.join(OUTPUT_DIR, "classified_medical_Q3.csv")
    else:
        input_path  = os.path.join(OUTPUT_DIR, "prefiltered_discourse_eval.csv")
        output_path = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")

    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        sys.exit(1)

    client = AsyncAnthropic()

    with open(input_path, encoding="utf-8") as f:
        all_records = list(csv.DictReader(f))

    print(f"Stance Classifier — Async ({CONCURRENCY} concurrent Sonnet calls)")
    print(f"Input:  {os.path.basename(input_path)}")
    print(f"Output: {os.path.basename(output_path)}")
    print(f"Records: {len(all_records):,}")

    # Resume
    classified_pmids = set()
    if os.path.exists(output_path):
        with open(output_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("stance") not in ("", "FAILED", None):
                    classified_pmids.add(row["pmid"])
        print(f"Resuming: {len(classified_pmids):,} already classified")

    pending = [r for r in all_records if r["pmid"] not in classified_pmids]
    print(f"Pending: {len(pending):,} records")
    print(f"{'='*60}")

    if not pending:
        print("Already complete.")
        _print_summary(output_path)
        return

    in_cols  = list(all_records[0].keys())
    out_cols = in_cols + ["pub_year", "stance", "stance_model",
                          "confidence", "predictive_claim", "stance_raw"]

    mode = "a" if classified_pmids else "w"

    semaphore  = asyncio.Semaphore(CONCURRENCY)
    total      = len(pending)
    done_count = 0
    stance_dist= {}
    n_failed   = 0
    start_time = time.time()

    with open(output_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        if mode == "w":
            writer.writeheader()

        CHUNK = 50
        for chunk_start in range(0, len(pending), CHUNK):
            chunk   = pending[chunk_start: chunk_start + CHUNK]
            tasks   = [classify_one(client, semaphore, rec) for rec in chunk]
            results = await asyncio.gather(*tasks)

            for rec, stance, confidence, predictive, raw in results:
                pub_year = extract_pub_year(rec.get("pub_date", ""))
                stance_dist[stance] = stance_dist.get(stance, 0) + 1
                if stance == "FAILED":
                    n_failed += 1

                out_row = dict(rec)
                out_row["pub_year"]         = pub_year
                out_row["stance"]           = stance
                out_row["stance_model"]     = "sonnet"
                out_row["confidence"]       = confidence
                out_row["predictive_claim"] = predictive
                out_row["stance_raw"]       = raw
                writer.writerow(out_row)

            f.flush()
            done_count += len(chunk)

            elapsed  = time.time() - start_time
            rate     = done_count / elapsed if elapsed > 0 else 0
            eta_mins = (total - done_count) / rate / 60 if rate > 0 else 0
            dist_str = " | ".join(f"{k}:{v}" for k, v in sorted(stance_dist.items())
                                  if k != "FAILED")
            print(f"  [{done_count:6d}/{total}] {done_count/total*100:5.1f}%  "
                  f"{dist_str}  failed={n_failed}  ETA:{eta_mins:.0f}min")

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"Complete in {elapsed/60:.1f} minutes.")
    _print_summary(output_path)


def _print_summary(output_path):
    if not os.path.exists(output_path):
        return
    stance_dist = {}
    total = 0
    with open(output_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = row.get("stance", "")
            stance_dist[s] = stance_dist.get(s, 0) + 1
            total += 1
    print(f"\nFinal stance distribution ({total:,} records):")
    for s in ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy", "FAILED"]:
        n = stance_dist.get(s, 0)
        if n:
            print(f"  {s:<22} {n:6,}  ({n/total*100:.1f}%)")
    print(f"\nNext step: python analyse_narratives.py")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
