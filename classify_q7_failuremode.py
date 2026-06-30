"""
Q7 Failure-Mode + Model-Type Classifier — gate-independent re-measurement.

Mirrors classify_stance.py infrastructure: AsyncAnthropic, semaphore concurrency,
checkpoint/resume, confidence gating, FAILED convention.

Phases:
  smoke    — stratified 30 Alarm papers (5/yr × 6yr, seed=42), print all 30, no save.
  alarm    — all stance==Alarm rows → output/analyses/q7_classified_alarm.csv
  cautious — all stance==Caution rows → output/analyses/q7_classified_cautious.csv

Decide failure_mode + model_type from the MECHANISM DESCRIBED in title+abstract,
NOT from whether brand names appear. Prompt version tag: q7_failuremode_v1.
"""

import csv, json, time, os, sys, re, random, argparse
import asyncio
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
load_dotenv(override=True)

PROMPT_VERSION = "q7_failuremode_v1"
MODEL          = "claude-sonnet-4-6"
TEMPERATURE    = 0.0
MAX_TOKENS     = 200
CONCURRENCY    = 5
SLEEP_RETRY    = 12
MAX_RETRIES    = 3

VALID_FAILURE_MODES = {"confabulation", "misclassification", "both", "none_or_unclear"}
VALID_MODEL_TYPES   = {"generative", "discriminative", "both", "unclear"}

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")
ANALYSES    = os.path.join(OUTPUT_DIR, "analyses")
SOURCE_CSV  = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")

SYSTEM_PROMPT = """Classify an AI/medical paper on two independent axes from the MECHANISM described, not from brand names (GPT/ChatGPT/etc).

Axis A — failure_mode:
- "confabulation": AI GENERATES fabricated/unfaithful content — invented citations or references, made-up facts, plausible-but-false text, hallucinated entities, unfaithful summaries.
- "misclassification": AI produces a wrong label/score/prediction/detection — false positives/negatives, misdiagnosis, miscalibration, poor generalization, dataset shift, biased predictions.
- "both": both mechanisms explicitly described.
- "none_or_unclear": no specific mechanism, or general "AI risks" framing.

Axis B — model_type:
- "generative": LLM, chatbot, text/image/code generator.
- "discriminative": predictive / classification / detection / segmentation / risk-scoring model.
- "both": both families explicitly evaluated.
- "unclear": cannot tell.

CALIBRATION EXAMPLES:
1. "ChatGPT scored 85% on USMLE-style questions" → {"failure_mode":"misclassification","model_type":"generative","confidence":0.9,"rationale":"accuracy of LLM responses, not fabrication"}
2. "DL classifier produced false-negative mammograms" → {"failure_mode":"misclassification","model_type":"discriminative","confidence":0.95,"rationale":"predictive model with classification errors"}
3. "LLM discharge summary fabricated a drug and an invented citation" → {"failure_mode":"confabulation","model_type":"generative","confidence":0.95,"rationale":"explicit fabrication of content and references"}
4. "Measured GPT-4 hallucinated references AND diagnostic accuracy" → {"failure_mode":"both","model_type":"generative","confidence":0.9,"rationale":"both fabrication and accuracy measured"}
5. "AI errors threaten safety, need oversight" (no mechanism) → {"failure_mode":"none_or_unclear","model_type":"unclear","confidence":0.6,"rationale":"general risk framing, no mechanism specified"}

Output STRICT JSON only, no prose, no code fences:
{"failure_mode":"confabulation|misclassification|both|none_or_unclear","model_type":"generative|discriminative|both|unclear","confidence":0.0-1.0,"rationale":"<=20 words"}"""


def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        text += f"\nAbstract: {abstract}"
    return text


def _parse_response(raw):
    s = raw.strip()
    s = re.sub(r'^```(?:json)?\s*', '', s)
    s = re.sub(r'\s*```$', '', s)
    parsed = json.loads(s, strict=False)
    fm = str(parsed.get("failure_mode", "")).strip().lower()
    mt = str(parsed.get("model_type", "")).strip().lower()
    conf_raw = parsed.get("confidence", 0.0)
    try:
        conf = float(conf_raw)
    except (TypeError, ValueError):
        conf = 0.0
    conf = max(0.0, min(1.0, conf))
    rationale = str(parsed.get("rationale", "")).strip()
    if fm not in VALID_FAILURE_MODES:
        raise ValueError(f"Invalid failure_mode: {fm}")
    if mt not in VALID_MODEL_TYPES:
        raise ValueError(f"Invalid model_type: {mt}")
    # cap rationale to ~25 words to keep CSV sane
    words = rationale.split()
    if len(words) > 25:
        rationale = " ".join(words[:25])
    return fm, mt, conf, rationale


async def classify_one(client, semaphore, rec):
    title    = rec.get("title", "")
    abstract = rec.get("abstract", "")
    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": build_prompt(title, abstract)}],
                )
                raw = response.content[0].text
                fm, mt, conf, rationale = _parse_response(raw)
                return rec, fm, mt, conf, rationale, raw.strip()
            except (json.JSONDecodeError, ValueError) as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY)
                else:
                    return rec, "FAILED", "FAILED", 0.0, f"ERROR: {e}", str(e)
            except Exception as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY * attempt)
                else:
                    return rec, "FAILED", "FAILED", 0.0, f"ERROR: {e}", str(e)
    return rec, "FAILED", "FAILED", 0.0, "ERROR: semaphore", ""


def load_source(stance_filter):
    with open(SOURCE_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = [r for r in rows if r.get("stance") == stance_filter]
    # restrict to pub_year 2021–2026 (drops FAILED stance and any odd years)
    out = [r for r in out if r.get("pub_year") in {"2021","2022","2023","2024","2025","2026"}]
    return out


def stratified_smoke_sample(alarm_rows, per_year=5, seed=42):
    rng = random.Random(seed)
    by_year = {}
    for r in alarm_rows:
        by_year.setdefault(r["pub_year"], []).append(r)
    years = ["2021","2022","2023","2024","2025","2026"]
    picked = []
    shortfall_years = []
    for y in years:
        pool = by_year.get(y, [])
        if len(pool) >= per_year:
            picked.extend(rng.sample(pool, per_year))
        else:
            picked.extend(pool)
            shortfall_years.append((y, per_year - len(pool)))
    # fill shortfall from adjacent years
    for y, need in shortfall_years:
        picked_ids = {r["pmid"] for r in picked}
        idx = years.index(y)
        neighbors = []
        for d in (1,2,3,4,5):
            for s in (-1, 1):
                j = idx + s*d
                if 0 <= j < len(years):
                    neighbors.append(years[j])
        candidates = []
        seen = set()
        for ny in neighbors:
            if ny in seen: continue
            seen.add(ny)
            for r in by_year.get(ny, []):
                if r["pmid"] not in picked_ids:
                    candidates.append(r)
            if len(candidates) >= need: break
        rng.shuffle(candidates)
        picked.extend(candidates[:need])
    picked.sort(key=lambda r: (r["pub_year"], r["pmid"]))
    return picked


async def run_smoke():
    alarm = load_source("Alarm")
    print(f"Loaded {len(alarm)} Alarm rows.")
    sample = stratified_smoke_sample(alarm, per_year=5, seed=42)
    print(f"Smoke sample: {len(sample)} rows (target 30).")
    client = AsyncAnthropic()
    sem = asyncio.Semaphore(CONCURRENCY)
    t0 = time.time()
    results = await asyncio.gather(*[classify_one(client, sem, r) for r in sample])
    elapsed = time.time() - t0

    print()
    print("="*120)
    print(f"PHASE 0 SMOKE RESULTS (prompt version = {PROMPT_VERSION}, model = {MODEL}, n = {len(results)})")
    print("="*120)
    n_failed = 0
    fm_dist, mt_dist = {}, {}
    for rec, fm, mt, conf, rationale, raw in results:
        if fm == "FAILED":
            n_failed += 1
        fm_dist[fm] = fm_dist.get(fm, 0) + 1
        mt_dist[mt] = mt_dist.get(mt, 0) + 1
        title100 = (rec.get("title","")[:100]).replace("\n"," ")
        print(f"[{rec.get('pub_year','')}] {title100!r}")
        print(f"   failure_mode={fm} | model_type={mt} | confidence={conf:.2f} | rationale={rationale}")
    print("="*120)
    print(f"FAILED count: {n_failed}/{len(results)}")
    print(f"failure_mode dist: {dict(sorted(fm_dist.items()))}")
    print(f"model_type   dist: {dict(sorted(mt_dist.items()))}")
    print(f"Elapsed: {elapsed:.1f}s")
    print()
    print('PHASE 0 done — inspect 30 rows (esp. pre-2023 → discriminative/misclassification, '
          'post-2023 → generative/confabulation, and that "high-accuracy-but-not-fabrication" '
          'cases are generative+misclassification). Do NOT proceed until told to continue.')


async def run_phase(stance, out_name):
    rows = load_source(stance)
    print(f"Loaded {len(rows)} {stance} rows (pub_year 2021–2026).")
    out_path = os.path.join(ANALYSES, out_name)
    os.makedirs(ANALYSES, exist_ok=True)
    out_cols = ["pmid","pub_year","stance","failure_mode","model_type",
                "confidence","rationale","prompt_version","model"]
    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("failure_mode") not in ("", "FAILED", None):
                    done.add(row["pmid"])
        print(f"Resuming: {len(done)} already classified.")
    pending = [r for r in rows if r["pmid"] not in done]
    print(f"Pending: {len(pending)}")
    if not pending:
        print("Already complete.")
        return out_path

    client = AsyncAnthropic()
    sem = asyncio.Semaphore(CONCURRENCY)
    mode = "a" if done else "w"
    t0 = time.time()
    n_failed = 0
    fm_dist, mt_dist = {}, {}
    with open(out_path, mode, newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        if mode == "w":
            w.writeheader()
        CHUNK = 50
        for cs in range(0, len(pending), CHUNK):
            chunk = pending[cs: cs+CHUNK]
            results = await asyncio.gather(*[classify_one(client, sem, r) for r in chunk])
            for rec, fm, mt, conf, rationale, raw in results:
                if fm == "FAILED": n_failed += 1
                fm_dist[fm] = fm_dist.get(fm, 0) + 1
                mt_dist[mt] = mt_dist.get(mt, 0) + 1
                w.writerow({
                    "pmid": rec["pmid"],
                    "pub_year": rec.get("pub_year",""),
                    "stance": rec.get("stance",""),
                    "failure_mode": fm,
                    "model_type": mt,
                    "confidence": f"{conf:.3f}",
                    "rationale": rationale,
                    "prompt_version": PROMPT_VERSION,
                    "model": MODEL,
                })
            f.flush()
            done_n = cs + len(chunk)
            elapsed = time.time() - t0
            rate = done_n/elapsed if elapsed>0 else 0
            eta = (len(pending)-done_n)/rate/60 if rate>0 else 0
            print(f"  [{done_n}/{len(pending)}] failed={n_failed} fm={dict(sorted(fm_dist.items()))} ETA={eta:.0f}min")
    print(f"Done in {(time.time()-t0)/60:.1f} min. Saved → {out_path}")
    return out_path


async def main_async():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["smoke","alarm","cautious"])
    args = ap.parse_args()
    if args.phase == "smoke":
        await run_smoke()
    elif args.phase == "alarm":
        await run_phase("Alarm", "q7_classified_alarm.csv")
    elif args.phase == "cautious":
        await run_phase("Caution", "q7_classified_cautious.csv")


if __name__ == "__main__":
    asyncio.run(main_async())
