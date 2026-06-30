"""
Sanity check for revised stance prompt (Path B, v2)
====================================================

Runs the revised SYSTEM_PROMPT from classify_stance_batch.py on 30 random
records from the validation set, using the synchronous API. Prints v2 output
side-by-side with v1 labels.

Purpose: verify the prompt produces well-formed JSON and isn't broken.
NOT a re-validation — no kappa computed here.

Usage:  python3 sanity_check_v2.py [--seed N]
"""
import csv, json, random, sys, time
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv(override=True)

from classify_stance_batch import (
    SYSTEM_PROMPT, MODEL, MAX_TOKENS, build_prompt, parse_response,
)

VALIDATION_PATH = "output/validation/kingsly_validation_full.csv"
N_SAMPLE = 30
SEED = 42
for i, a in enumerate(sys.argv):
    if a == "--seed" and i + 1 < len(sys.argv):
        SEED = int(sys.argv[i + 1])


def main():
    with open(VALIDATION_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows):,} validation records")

    random.seed(SEED)
    sample = random.sample(rows, N_SAMPLE)
    print(f"Sampling {N_SAMPLE} records (seed={SEED})\n")

    client = Anthropic()
    n_fail = 0
    n_meta = 0
    rows_for_table = []

    t0 = time.time()
    for i, r in enumerate(sample, 1):
        prompt = build_prompt(r.get("title", ""), r.get("abstract", ""))
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            text = ""
            for b in (resp.content or []):
                if getattr(b, "text", None):
                    text = b.text
                    break
            if not text:
                stance, conf, pred, meta, raw = "FAILED", "Low", "no", "no", "ERROR: empty content"
            else:
                stance, conf, pred, meta, raw = parse_response(text)
        except Exception as e:
            stance, conf, pred, meta, raw = "FAILED", "Low", "no", "no", f"ERROR: {e}"

        if stance == "FAILED":
            n_fail += 1
        if meta == "yes":
            n_meta += 1

        v1_stance = r.get("stance", "")
        v1_pred   = r.get("predictive_claim", "")
        same = "=" if v1_stance == stance else "≠"
        print(f"[{i:>2}/{N_SAMPLE}] pmid={r['pmid']}  v1={v1_stance:<18} v2={stance:<18} {same}  meta={meta}  pred={pred}")
        if stance == "FAILED":
            print(f"         RAW: {raw[:200]}")

        rows_for_table.append({
            "pmid": r["pmid"],
            "title": (r.get("title", "")[:80]),
            "v1_stance": v1_stance,
            "v2_stance": stance,
            "v1_pred": v1_pred,
            "v2_pred": pred,
            "v2_meta": meta,
            "v2_conf": conf,
            "v2_raw": raw[:300] if stance == "FAILED" else "",
        })

    elapsed = time.time() - t0
    print(f"\n=== SUMMARY ===")
    print(f"Records:   {N_SAMPLE}")
    print(f"Failures:  {n_fail}")
    print(f"Meta-discourse flagged: {n_meta}")
    print(f"Time:      {elapsed:.1f}s ({elapsed / N_SAMPLE:.2f}s/record)")

    out_path = "output/validation/sanity_check_v2_30records.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_for_table[0].keys()))
        w.writeheader()
        for r in rows_for_table:
            w.writerow(r)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
