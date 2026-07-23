"""
TASK REP-1 — Stance classifier stability under T=1.0 (provider default).

Reruns the EXACT canonical stance classifier (classify_stance.py: model
claude-sonnet-4-6, same SYSTEM_PROMPT and build_prompt, max_tokens=120, NO
temperature parameter => provider default T=1.0) on the pre-registered
300-record validation sample, TWICE. Reports:
  - inter-run raw agreement
  - quadratic-weighted Cohen's kappa (5 ordered stance labels)
  - number/count of labels shifted, and a shift matrix

Does NOT touch canonical v1 labels or human validation codes. Writes only
new rerun labels to output/revision_checks/.

Ordinal stance order (for quadratic weights):
  Alarm(0) < Caution(1) < Neutral(2) < Cautious Optimism(3) < Advocacy(4)

Outputs:
  output/revision_checks/rep1_stance_stability_sample.csv
  output/revision_checks/rep1_stability_metrics.csv
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

REPO = Path("/Users/kingslywang/repos/ai-narratives-2026")
load_dotenv(REPO / ".env", override=True)
sys.path.insert(0, str(REPO))  # import the canonical classifier module

# Exact prompt / model parity with the production classifier.
from classify_stance import (  # noqa: E402
    MODEL,
    MAX_TOKENS,
    SYSTEM_PROMPT,
    VALID_CONFIDENCE,
    VALID_STANCES,
    build_prompt,
)

WT = Path(__file__).resolve().parents[2]
OUT = WT / "output" / "revision_checks"
OUT.mkdir(parents=True, exist_ok=True)

SAMPLE_PATH = REPO / "output" / "validation" / "kingsly_validation_full.csv"
STANCES = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]
STANCE_IDX = {s: i for i, s in enumerate(STANCES)}
CONCURRENCY = 5
MAX_RETRIES = 3
SLEEP_RETRY = 12


async def classify_one(client, sem, rec):
    async with sem:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = await client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user",
                               "content": build_prompt(rec.get("title", ""),
                                                       rec.get("abstract", ""))}],
                )
                raw = resp.content[0].text.strip()
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)
                parsed = json.loads(raw, strict=False)
                stance = parsed.get("stance", "").strip()
                conf = parsed.get("confidence", "Medium").strip()
                if stance not in VALID_STANCES:
                    raise ValueError(f"invalid stance {stance!r}")
                if conf not in VALID_CONFIDENCE:
                    conf = "Medium"
                return stance, conf
            except (json.JSONDecodeError, ValueError):
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY)
                else:
                    return "FAILED", "Low"
            except Exception:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(SLEEP_RETRY * attempt)
                else:
                    return "FAILED", "Low"
    return "FAILED", "Low"


async def run_pass(records, label):
    client = AsyncAnthropic()
    sem = asyncio.Semaphore(CONCURRENCY)
    results = [None] * len(records)
    CHUNK = 50
    done = 0
    for start in range(0, len(records), CHUNK):
        chunk = records[start:start + CHUNK]
        tasks = [classify_one(client, sem, r) for r in chunk]
        out = await asyncio.gather(*tasks)
        for j, (stance, conf) in enumerate(out):
            results[start + j] = (stance, conf)
        done += len(chunk)
        print(f"  [{label}] {done}/{len(records)} classified")
    return results


def quadratic_weighted_kappa(a, b, categories):
    """Cohen's quadratic-weighted kappa for ordered categories."""
    idx = {c: i for i, c in enumerate(categories)}
    k = len(categories)
    O = np.zeros((k, k))
    for x, y in zip(a, b):
        O[idx[x], idx[y]] += 1
    n = O.sum()
    row = O.sum(axis=1)
    col = O.sum(axis=0)
    E = np.outer(row, col) / n
    W = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            W[i, j] = (i - j) ** 2 / (k - 1) ** 2
    num = (W * O).sum()
    den = (W * E).sum()
    return 1 - num / den if den > 0 else float("nan")


def main() -> None:
    df = pd.read_csv(SAMPLE_PATH)
    df["title"] = df["title"].fillna("")
    df["abstract"] = df["abstract"].fillna("")
    records = df.to_dict("records")
    print(f"REP-1 stance stability — {len(records)} records, model={MODEL}, "
          f"T=provider-default(1.0), max_tokens={MAX_TOKENS}")
    print(f"Sample: {SAMPLE_PATH.name}\n")

    print("Run A ...")
    run_a = asyncio.run(run_pass(records, "A"))
    print("Run B ...")
    run_b = asyncio.run(run_pass(records, "B"))

    out = df[["record_id", "pmid", "pub_year", "stance"]].copy()
    out = out.rename(columns={"stance": "v1_canonical_stance"})
    out["rerun_A_stance"] = [s for s, _ in run_a]
    out["rerun_A_conf"] = [c for _, c in run_a]
    out["rerun_B_stance"] = [s for s, _ in run_b]
    out["rerun_B_conf"] = [c for _, c in run_b]
    out.to_csv(OUT / "rep1_stance_stability_sample.csv", index=False)

    # metrics computed on records where BOTH reruns produced a valid stance
    mask = out["rerun_A_stance"].isin(STANCES) & out["rerun_B_stance"].isin(STANCES)
    n_failed_A = int((~out["rerun_A_stance"].isin(STANCES)).sum())
    n_failed_B = int((~out["rerun_B_stance"].isin(STANCES)).sum())
    a = out.loc[mask, "rerun_A_stance"].tolist()
    b = out.loc[mask, "rerun_B_stance"].tolist()
    n_eval = len(a)
    n_agree = sum(1 for x, y in zip(a, b) if x == y)
    raw_agreement = n_agree / n_eval if n_eval else float("nan")
    n_shifted = n_eval - n_agree
    qwk = quadratic_weighted_kappa(a, b, STANCES)

    # shift matrix (rows = run A, cols = run B)
    shift = pd.crosstab(pd.Series(a, name="run_A"), pd.Series(b, name="run_B"))
    shift = shift.reindex(index=STANCES, columns=STANCES).fillna(0).astype(int)

    print("\n=== REP-1 inter-run stability (Run A vs Run B, T=1.0) ===")
    print(f"  records evaluated (both valid): {n_eval}  "
          f"(FAILED: A={n_failed_A}, B={n_failed_B})")
    print(f"  raw agreement: {raw_agreement:.4f}  ({n_agree}/{n_eval})")
    print(f"  labels shifted across the 5 stances: {n_shifted}")
    print(f"  quadratic-weighted kappa: {qwk:.4f}")
    print("\nShift matrix (rows=Run A, cols=Run B):")
    print(shift.to_string())

    metrics = pd.DataFrame([{
        "n_records_sample": len(records),
        "n_evaluated_both_valid": n_eval,
        "n_failed_run_A": n_failed_A,
        "n_failed_run_B": n_failed_B,
        "raw_agreement": raw_agreement,
        "n_labels_shifted": n_shifted,
        "quadratic_weighted_kappa": qwk,
        "model": MODEL,
        "temperature": "provider_default_1.0",
    }])
    metrics.to_csv(OUT / "rep1_stability_metrics.csv", index=False)
    shift.to_csv(OUT / "rep1_shift_matrix.csv")
    print(f"\nSaved: {OUT / 'rep1_stance_stability_sample.csv'}")
    print(f"Saved: {OUT / 'rep1_stability_metrics.csv'}")
    print(f"Saved: {OUT / 'rep1_shift_matrix.csv'}")


if __name__ == "__main__":
    main()
