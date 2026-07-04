#!/usr/bin/env python3
"""
Prophecy Panel — PHASE 1: claim extraction, flag validation, tiering (BLIND to reality).

For each of the 92 candidate papers (Advocacy, 2021-2023, v1 predictive-claim flag),
using ONLY that paper's own title + abstract:
  1. validate the predictive-claim flag       -> flag_confirmed {yes,no} + flag_reason
  2. extract the signature claim (+ optional secondary)
  3. assign tier by claim STRUCTURE (frozen 3-tier taxonomy)
  4. record topic (free-text theme) and horizon (explicit timeframe / open-ended)

HARD RULE: the model must use ONLY the paper's own 2021-2023 text. It must NOT use any
post-2023 training knowledge of what actually happened. Tier is a function of claim
structure, never of whether the prediction happens to be known to have come true.

Output: phase1_signature_claims_for_review.csv  (human reviews -> freezes -> Phase 2).
This script NEVER assigns a verdict.
"""

import os, sys, csv, json, re, asyncio, hashlib, random, datetime
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from tqdm.asyncio import tqdm_asyncio

# ── paths ───────────────────────────────────────────────────────────────────────
REPO        = "/Users/kingslywang/repos/ai-narratives-2026"
ENV_PATH    = os.path.join(REPO, ".env")
OUT_DIR     = os.path.join(REPO, "output", "analyses", "prophecy")
INPUT_CSV   = os.path.join(OUT_DIR, "prophecy_panel_candidates_2021_2023.csv")
OUTPUT_CSV  = os.path.join(OUT_DIR, "phase1_signature_claims_for_review.csv")
RAW_JSONL   = os.path.join(OUT_DIR, "phase1_raw_responses.jsonl")
MANIFEST    = os.path.join(OUT_DIR, "run_manifest.txt")

# ── model / run config (frozen) ─────────────────────────────────────────────────
load_dotenv(ENV_PATH, override=True)   # .env wins over any empty shell var
MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 700
TEMPERATURE = 0.0          # determinism lever (API exposes no seed; logged as-is)
CONCURRENCY = 5
MAX_RETRIES = 3
SLEEP_RETRY = 12
SEED        = 20260630     # numpy/random seed (no model effect at T=0; logged for completeness)

VALID_FLAG = {"yes", "no"}
VALID_TIER = {"1", "2", "3", ""}

# ── frozen system prompt ─────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are adjudicating, for a PRE-REGISTERED forward-validation study, the predictive content of a 2021-2023 medical-AI paper. You are given ONLY that paper's own title and (sometimes) abstract.

ABSOLUTE BLINDNESS RULE — read carefully:
- Use ONLY the paper's own text shown to you. Judge the claim purely on what THIS 2021-2023 paper says.
- Do NOT use any knowledge of what happened after 2023. Do NOT let any belief about whether the prediction "came true" influence the flag, the signature claim, or the tier.
- Tier is a function of the CLAIM'S STRUCTURE, never of its real-world outcome.

Your job has five parts.

1) VALIDATE THE PREDICTIVE-CLAIM FLAG.
   Does the text contain a SPECIFIC, FORWARD-LOOKING claim about AI's future role (a prediction/bet about what AI will do, become, replace, enable, or transform)?
   - flag_confirmed = "yes" only if a specific forward-looking claim is present.
   - flag_confirmed = "no" for purely descriptive/retrospective work, a bland descriptive title with no forward claim, or vague aspiration with no claim content.
   - For TITLE-ONLY records (no abstract), judge from the title alone. A descriptive title with no forward claim => "no".
   - flag_reason: one short line justifying yes/no, quoting/pointing to the forward-looking language (or noting its absence).

2) EXTRACT THE SIGNATURE CLAIM.
   The single MOST SPECIFIC, MOST FALSIFIABLE prediction the paper makes, as one verbatim-or-close sentence.
   - If flag_confirmed = "no", set signature_claim = "" (empty).
   - If the paper makes TWO genuinely independent major predictions, put the primary in signature_claim and the secondary in signature_claim_2. Most papers leave signature_claim_2 = "".

3) ASSIGN TIER by claim STRUCTURE (frozen definitions):
   - Tier 1 — Specific superiority / replacement: a testable head-to-head or displacement claim (AI will outperform / replace clinicians, or has done so in a way predicted to generalize). Highest falsifiability.
   - Tier 2 — Capability deployment: a concrete mechanism entering clinical use / drug development / workflow (will be deployed, adopted, embedded, accelerate a pipeline). Medium falsifiability.
   - Tier 3 — Diffuse transformation: "revolutionize / paradigm shift / next frontier" with NO mechanism and NO horizon. Lowest falsifiability.
   TIE-BREAKERS (apply in order):
   - If a claim has ANY concrete, testable element, it is NOT Tier 3.
   - If it names a comparison/benchmark against humans, it is Tier 1.
   If flag_confirmed = "no", set tier = "".

4) TOPIC: a short free-text specialty/theme tag (e.g. "dermatology imaging", "drug discovery", "clinical NLP"). Secondary attribute only.

5) HORIZON: any explicit timeframe stated in the claim ("by 2025", "within five years", "next decade"). If none is stated, output "open-ended".

Return ONLY a JSON object, no prose, no markdown fences, with EXACTLY these keys:
{"flag_confirmed":"yes|no","flag_reason":"...","signature_claim":"...","signature_claim_2":"...","tier":"1|2|3 or empty string","topic":"...","horizon":"..."}"""


def build_user_msg(title: str, abstract: str) -> str:
    title = (title or "").strip()
    abstract = (abstract or "").strip()
    if abstract:
        body = f"TITLE:\n{title}\n\nABSTRACT:\n{abstract}"
    else:
        body = f"TITLE-ONLY RECORD (no abstract available). Judge from the title alone.\n\nTITLE:\n{title}"
    return body + "\n\nReturn the JSON object now."


def parse_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw, strict=False)


async def classify_one(client, sem, rec):
    title    = rec.get("title", "")
    abstract = rec.get("abstract", "")
    async with sem:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = await client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": build_user_msg(title, abstract)}],
                )
                raw = resp.content[0].text
                p = parse_json(raw)

                flag = str(p.get("flag_confirmed", "")).strip().lower()
                tier = str(p.get("tier", "")).strip()
                tier = re.sub(r"(?i)^tier\s*", "", tier)          # "Tier 2" -> "2"
                if flag not in VALID_FLAG:
                    raise ValueError(f"bad flag_confirmed: {flag!r}")
                if tier not in VALID_TIER:
                    raise ValueError(f"bad tier: {tier!r}")

                out = {
                    "flag_confirmed":    flag,
                    "flag_reason":       str(p.get("flag_reason", "")).strip(),
                    "signature_claim":   str(p.get("signature_claim", "")).strip(),
                    "signature_claim_2": str(p.get("signature_claim_2", "")).strip(),
                    "tier":              tier,
                    "topic":             str(p.get("topic", "")).strip(),
                    "horizon":           str(p.get("horizon", "")).strip() or "open-ended",
                }
                return rec, out, raw, None
            except Exception as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY * attempt)
                else:
                    return rec, None, "", f"ERROR after {MAX_RETRIES} tries: {e}"


async def main():
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows)} candidates from {INPUT_CSV}")

    random.seed(SEED)
    try:
        import numpy as np; np.random.seed(SEED)
    except Exception:
        pass

    client = AsyncAnthropic()
    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [classify_one(client, sem, rec) for rec in rows]
    results = await tqdm_asyncio.gather(*tasks, desc="Phase 1 (Sonnet)")

    out_cols = ["pmid", "pub_year", "journal", "pub_type_simple_5", "specialty", "title",
                "has_abstract", "flag_confirmed", "flag_reason", "signature_claim",
                "signature_claim_2", "tier", "topic", "horizon"]

    failures = 0
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fo, \
         open(RAW_JSONL, "w", encoding="utf-8") as fr:
        w = csv.DictWriter(fo, fieldnames=out_cols)
        w.writeheader()
        for rec, out, raw, err in results:
            has_abs = "yes" if (rec.get("abstract") or "").strip() else "no"
            if err:
                failures += 1
                out = {k: "" for k in ("flag_confirmed", "flag_reason", "signature_claim",
                                       "signature_claim_2", "tier", "topic", "horizon")}
                out["flag_reason"] = err
            row = {
                "pmid": rec.get("pmid", ""), "pub_year": rec.get("pub_year", ""),
                "journal": rec.get("journal", ""), "pub_type_simple_5": rec.get("pub_type_simple_5", ""),
                "specialty": rec.get("specialty", ""), "title": rec.get("title", ""),
                "has_abstract": has_abs, **out,
            }
            if not out.get("horizon"):
                row["horizon"] = "open-ended"
            w.writerow(row)
            fr.write(json.dumps({"pmid": rec.get("pmid", ""), "raw": raw}, ensure_ascii=False) + "\n")

    # ── summary ──────────────────────────────────────────────────────────────────
    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        done = list(csv.DictReader(f))
    n = len(done)
    yes = [r for r in done if r["flag_confirmed"] == "yes"]
    title_only = [r for r in done if r["has_abstract"] == "no"]
    to_yes = sum(1 for r in title_only if r["flag_confirmed"] == "yes")
    tiers = {t: sum(1 for r in yes if r["tier"] == t) for t in ("1", "2", "3")}

    print("\n" + "=" * 64)
    print("PHASE 1 SUMMARY (machine pre-pass — human review pending)")
    print("=" * 64)
    print(f"Total candidates              : {n}")
    print(f"flag_confirmed = yes          : {len(yes)}")
    print(f"FLAG PRECISION (yes / {n})     : {len(yes)/n:.3f}")
    print(f"Tier counts (confirmed only)  : T1={tiers['1']}  T2={tiers['2']}  T3={tiers['3']}")
    print(f"Title-only records            : {len(title_only)}  "
          f"(confirmed={to_yes}, rejected={len(title_only)-to_yes})")
    if failures:
        print(f"!! API failures (flag blank)  : {failures}  (re-run to fill)")
    print(f"\nWrote: {OUTPUT_CSV}")
    print(f"Raw  : {RAW_JSONL}")

    # ── manifest ─────────────────────────────────────────────────────────────────
    sys_hash = hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()[:16]
    with open(MANIFEST, "a", encoding="utf-8") as m:
        m.write(
            f"\n[PHASE 1] {datetime.datetime.now().isoformat(timespec='seconds')}\n"
            f"  model={MODEL} temperature={TEMPERATURE} max_tokens={MAX_TOKENS}\n"
            f"  concurrency={CONCURRENCY} seed={SEED} system_prompt_sha256_16={sys_hash}\n"
            f"  input={INPUT_CSV} n_candidates={n}\n"
            f"  flag_confirmed_yes={len(yes)} flag_precision={len(yes)/n:.3f} "
            f"tiers(T1,T2,T3)=({tiers['1']},{tiers['2']},{tiers['3']}) "
            f"title_only={len(title_only)} api_failures={failures}\n"
            f"  output={OUTPUT_CSV}\n"
        )
    print(f"Manifest appended: {MANIFEST}")
    print("\n⛔ HUMAN REVIEW GATE — do NOT proceed to Phase 2.")
    print("   Review/correct every flag_confirmed, signature_claim, tier; delete false positives;")
    print("   save the approved file as phase1_signature_claims_FROZEN.csv, then say 'proceed'.")


if __name__ == "__main__":
    asyncio.run(main())
