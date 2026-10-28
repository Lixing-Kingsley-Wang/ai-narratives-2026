"""B3 · Symmetric 'strong endorsement' re-classification of favourable records
(JMIR R1 Batch 2b; X1, D2b). Pre-specified in ANALYSIS_PLAN_batch2b.md.

Frame: production stance Cautious Optimism or Advocacy, valid stance, dated
2021 to April 2026, plus model-favourable records of the 300-record stance
validation set not already in that frame.
Classifier: claude-sonnet-4-6, Batch API, temperature 0, max_tokens 30,
system prompt read verbatim from b3_prompt.txt (SHA-256 asserted), user
message in the v1 input format (title + full abstract). Output must be
{"strong_endorsement": "yes"|"no"}; anything else is FAILED (resubmitted once).

Usage: python b3_endorsement_batch.py count|submit|poll|resubmit|poll2|finalize
"""

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import b_batch_engine as E

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "revision_r1" / "outputs" / "B3"
PROMPT_SHA = "27d28077cd7485fddcdfe4f0da3f4a3c13ad36a310bcd23f1544a5a89db50cf6"
SYSTEM_PROMPT = (Path(__file__).resolve().parent / "b3_prompt.txt").read_text()
assert hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest() == PROMPT_SHA, "B3 prompt changed"
MODEL, MAX_TOKENS, TEMPERATURE = "claude-sonnet-4-6", 30, 0
FIELDS = ["strong_endorsement", "raw"]


def build_user(r):
    text = f"Title: {r.get('title', '')}"
    if r.get("abstract", "").strip():
        text += f"\nAbstract: {r['abstract']}"
    return text


def parse(text):
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        v = json.loads(raw, strict=False)
    except json.JSONDecodeError:
        return {}, f"json_parse_error: {text[:80]}"
    flag = str(v.get("strong_endorsement", "")).strip().lower() if isinstance(v, dict) else ""
    if flag not in ("yes", "no"):
        return {}, f"invalid_value: {text[:80]}"
    return {"strong_endorsement": flag, "raw": raw}, ""


def frame():
    corpus = list(csv.DictReader(open(E.MAIN / "output" / "classified_medical_Q1Q2.csv", encoding="utf-8")))
    fav = [r for r in corpus if r["stance"] in ("Cautious Optimism", "Advocacy")
           and r["pub_year"].isdigit() and 2021 <= int(r["pub_year"]) <= 2026]
    ids = {r["pmid"] for r in fav}
    val = list(csv.DictReader(open(REPO / "output/validation/kingsly_validation_full.csv", encoding="utf-8")))
    by_id = {r["pmid"]: r for r in corpus}
    extra = [by_id[v["pmid"]] for v in val if v["stance"] in ("Cautious Optimism", "Advocacy") and v["pmid"] not in ids]
    return fav + extra, len(fav), len(extra)


if __name__ == "__main__":
    recs, n_fav, n_extra = frame()
    print(f"B3 prompt sha256 {PROMPT_SHA}; frame {len(recs):,} = {n_fav:,} corpus favourable + {n_extra} validation-only", flush=True)
    job = E.Job("b3_endorsement", OUT, MODEL, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT, recs, build_user, parse,
                ceiling=25.0, out_tokens_assumed=15, n_chunks=1)
    E.run(job, FIELDS, sys.argv)
