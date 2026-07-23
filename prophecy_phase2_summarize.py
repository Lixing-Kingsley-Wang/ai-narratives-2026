#!/usr/bin/env python3
"""
Prophecy Panel — PHASE 2b: neutral evidence status summary (Sonnet) -> adjudication worksheet.

For each frozen claim, pass the claim + its top-20 retrieved 2024-2026 abstracts to Sonnet under a
STRICTLY NEUTRAL instruction (verbatim from the protocol). The model:
  - summarizes (2-4 sentences) what the abstracts indicate about the prediction's real-world status,
  - uses ONLY the provided abstracts (no outside/post-training knowledge),
  - assigns NO verdict, states neither right nor wrong,
  - distinguishes [outcome] evidence from [restatement] (continued advocacy != outcome),
  - says so if the corpus does not speak to the prediction,
  - lists up to 5 abstracts as `PMID - finding` tagged [outcome]/[restatement].

corpus_silent = model judges nothing relevant, OR top retrieval score < a logged data-driven
threshold. Per protocol A4 this maps to too-early/unfalsifiable downstream, NEVER to not-borne-out.
The model NEVER assigns a verdict; humans fill the verdict columns.
"""
import os, sys, csv, json, re, asyncio, datetime
import numpy as np
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from tqdm.asyncio import tqdm_asyncio

csv.field_size_limit(sys.maxsize)
REPO    = "/Users/kingslywang/repos/ai-narratives-2026"
OUT_DIR = os.path.join(REPO, "output", "analyses", "prophecy")
CORPUS  = os.path.join(REPO, "output", "filtered_medical_all_Q1Q2.csv")
FROZEN  = os.path.join(OUT_DIR, "phase1_signature_claims_FROZEN.csv")
RETR    = os.path.join(OUT_DIR, "phase2_retrieval.csv")
WORKSHEET = os.path.join(OUT_DIR, "phase2_prophecy_verdicts_worksheet.csv")
RAW_JSONL = os.path.join(OUT_DIR, "phase2_raw_summaries.jsonl")
MANIFEST  = os.path.join(OUT_DIR, "run_manifest.txt")

load_dotenv(os.path.join(REPO, ".env"), override=True)
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1100
TEMPERATURE = 0.0
CONCURRENCY = 5
MAX_RETRIES = 3
SLEEP_RETRY = 12
ABS_TRIM = 2200          # chars per abstract passed to the model
SILENCE_PCTILE = 10      # top_score below this percentile of all top_scores => low-similarity flag

SYSTEM_PROMPT = """You are given a prediction made in 2021-2023 and a set of 2024-2026 medical-literature abstracts retrieved as potentially relevant. Summarize, in 2-4 sentences, what these abstracts indicate about the real-world status of the prediction as of the evidence cutoff (April 2026).

Rules:
(a) Use ONLY the provided abstracts; do not use any outside or post-training knowledge.
(b) Do NOT state whether the prediction was right or wrong, and do NOT assign any verdict.
(c) Distinguish OUTCOME evidence (a study reporting what actually happened - a deployment, a validation, a head-to-head result, a workforce/market fact) from MERE RESTATEMENT (a later paper simply repeating the same prediction or advocacy). Continued advocacy is NOT evidence the prediction came true; note it as restatement, not outcome.
(d) If the abstracts do not actually address the prediction's real-world status, state that the retrieved corpus does not speak to it.
(e) List the up-to-5 most relevant abstracts, each tagged [outcome] or [restatement]. Cite only abstracts that genuinely bear on the prediction.

Return ONLY a JSON object, no markdown fences:
{"status_summary":"2-4 sentence neutral summary","corpus_silent":true|false,"key_evidence":[{"pmid":"...","finding":"one-line finding","tag":"outcome|restatement"}]}
corpus_silent = true if the retrieved abstracts do not genuinely address the prediction's real-world status. key_evidence may be empty if nothing genuinely bears on the prediction."""


def load_corpus_subset(needed):
    sub = {}
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pid = str(row.get("pmid", "")).strip()
            if pid in needed:
                sub[pid] = {"year": str(row.get("year", "")).strip(),
                            "title": (row.get("title") or "").strip(),
                            "abstract": (row.get("abstract") or "").strip()}
    return sub


def build_user_msg(claim, abstracts):
    blocks = []
    for pid, d in abstracts:
        blocks.append(f"[PMID {pid} | {d['year']}] {d['title']}\n{d['abstract'][:ABS_TRIM]}")
    return (f"PREDICTION (made 2021-2023):\n{claim}\n\n"
            f"RETRIEVED 2024-2026 ABSTRACTS ({len(abstracts)}):\n\n" + "\n\n".join(blocks) +
            "\n\nReturn the JSON object now.")


def parse_json(raw):
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip()); raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw, strict=False)


async def summarize_one(client, sem, claim_row, abstracts):
    msg = build_user_msg(claim_row["signature_claim"], abstracts)
    async with sem:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = await client.messages.create(
                    model=MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE,
                    system=SYSTEM_PROMPT, messages=[{"role": "user", "content": msg}])
                p = parse_json(resp.content[0].text)
                ke = p.get("key_evidence", []) or []
                ke_str = " || ".join(
                    f"{e.get('pmid','')} - {str(e.get('finding','')).strip()} [{e.get('tag','')}]"
                    for e in ke[:5])
                return claim_row["claim_id"], {
                    "evidence_status_summary": str(p.get("status_summary", "")).strip(),
                    "model_corpus_silent": bool(p.get("corpus_silent", False)),
                    "key_evidence": ke_str,
                }, resp.content[0].text, None
            except Exception as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY * attempt)
                else:
                    return claim_row["claim_id"], None, "", f"ERROR: {e}"


async def main():
    claims = {c["claim_id"]: c for c in csv.DictReader(open(FROZEN, encoding="utf-8"))}
    retr = {r["claim_id"]: r for r in csv.DictReader(open(RETR, encoding="utf-8"))}

    top_scores = np.array([float(retr[cid]["top_score"]) for cid in claims])
    thresh = float(np.percentile(top_scores, SILENCE_PCTILE))
    print(f"top_score distribution: min={top_scores.min():.1f} med={np.median(top_scores):.1f} "
          f"max={top_scores.max():.1f} | low-sim threshold (p{SILENCE_PCTILE})={thresh:.1f}")

    needed = set()
    for cid in claims:
        needed.update(retr[cid]["retrieved_pmids_top20"].split("|"))
    print(f"loading {len(needed)} retrieved abstracts from corpus...")
    corp = load_corpus_subset(needed)

    client = AsyncAnthropic()
    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = []
    for cid, c in claims.items():
        pmids = retr[cid]["retrieved_pmids_top20"].split("|")
        abstracts = [(p, corp[p]) for p in pmids if p in corp]
        tasks.append(summarize_one(client, sem, c, abstracts))
    results = dict()
    raws = []
    for cid, out, raw, err in await tqdm_asyncio.gather(*tasks, desc="Phase 2b (Sonnet)"):
        results[cid] = (out, err); raws.append((cid, raw))

    out_cols = ["claim_id", "pmid", "claim_role", "pub_year", "tier", "topic", "horizon",
                "signature_claim", "retrieved_pmids_top20", "top_score", "corpus_silent",
                "low_similarity", "evidence_status_summary", "key_evidence",
                "verdict", "verdict_evidence_pmid", "external_evidence_used",
                "ambiguous_flag", "adjudicator_note"]
    silent_n = 0; fail = 0
    with open(WORKSHEET, "w", newline="", encoding="utf-8") as f, open(RAW_JSONL, "w", encoding="utf-8") as fr:
        w = csv.DictWriter(f, fieldnames=out_cols); w.writeheader()
        for cid, c in claims.items():
            out, err = results[cid]
            ts = float(retr[cid]["top_score"]); low = ts < thresh
            if err:
                fail += 1
                out = {"evidence_status_summary": err, "model_corpus_silent": False, "key_evidence": ""}
            silent = bool(out["model_corpus_silent"] or low)
            if silent:
                silent_n += 1
            w.writerow({
                "claim_id": cid, "pmid": c["pmid"], "claim_role": c["claim_role"],
                "pub_year": c["pub_year"], "tier": c["tier"], "topic": c["topic"],
                "horizon": c["horizon"], "signature_claim": c["signature_claim"],
                "retrieved_pmids_top20": retr[cid]["retrieved_pmids_top20"],
                "top_score": ts, "corpus_silent": "TRUE" if silent else "FALSE",
                "low_similarity": "TRUE" if low else "FALSE",
                "evidence_status_summary": out["evidence_status_summary"],
                "key_evidence": out["key_evidence"],
                "verdict": "", "verdict_evidence_pmid": "", "external_evidence_used": "",
                "ambiguous_flag": "", "adjudicator_note": "",
            })
        for cid, raw in raws:
            fr.write(json.dumps({"claim_id": cid, "raw": raw}, ensure_ascii=False) + "\n")

    with open(MANIFEST, "a", encoding="utf-8") as m:
        m.write(
            f"\n[PHASE 2b SUMMARIZE] {datetime.datetime.now().isoformat(timespec='seconds')}\n"
            f"  model={MODEL} temperature={TEMPERATURE} claims={len(claims)} "
            f"corpus_silent={silent_n} api_failures={fail}\n"
            f"  silence=model_judgment OR top_score<p{SILENCE_PCTILE}({thresh:.1f}); maps to "
            f"too_early/unfalsifiable, never not_borne_out\n  output={WORKSHEET}\n")

    print("\n" + "=" * 70)
    print("PHASE 2 COMPLETE — adjudication worksheet written (NO verdicts assigned).")
    print("=" * 70)
    print(f"claims={len(claims)}  corpus_silent={silent_n}  api_failures={fail}")
    print(f"-> {WORKSHEET}")
    print("\nREMINDER: Verdicts are unfilled. Silence != failure: corpus_silent rows default to")
    print("too_early unless the human finds positive contrary evidence. Not_borne_out REQUIRES")
    print("positive contrary evidence.")


if __name__ == "__main__":
    asyncio.run(main())
