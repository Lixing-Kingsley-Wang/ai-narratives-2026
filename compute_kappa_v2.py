"""
compute_kappa_v2.py — EXPLORATORY κ analysis for the v2 (revised prompt) re-classification.

Same logic as compute_kappa.py, but the LLM stance is sourced from the v2
batch output (classified_medical_Q1Q2_v2_pre_predclaim_fix.csv) instead of
the frozen `stance` column in kingsly_validation_full.csv (which has v1).

Joins on pmid. Outputs to output/validation/kappa_report_v2_exploratory.md.

EXPLORATORY ONLY — the official validation κ stands at the v1 value
(0.789 Quadratic Sensitivity A) reported in kappa_report.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse helpers from compute_kappa
from compute_kappa import (
    STANCE_ORDER, STANCE_TO_INT, EXPECTED_N, N_BOOT,
    parse_flags, print_flag_summary,
    kappa_block, confusion, per_stance_metrics,
    export_disagreements, fmt_kappa, plot_confusion_matrices,
    cm_ascii, top_disagreement_pairs,
    compute_layer, LAYER_SPECS,
)

REPO = Path(__file__).resolve().parent
SHEET_PATH = REPO / "output/validation/kingsly_coding_sheet.xlsx"
FULL_PATH  = REPO / "output/validation/kingsly_validation_full.csv"
V2_PATH    = REPO / "output/classified_medical_Q1Q2_v2_pre_predclaim_fix.csv"
OUT_DIR    = REPO / "output/validation"
OUT_MD     = OUT_DIR / "kappa_report_v2_exploratory.md"


def load_and_join_v2() -> pd.DataFrame:
    sheet = pd.read_excel(SHEET_PATH)
    full  = pd.read_csv(FULL_PATH)
    v2    = pd.read_csv(V2_PATH, dtype=str, low_memory=False)

    assert len(sheet) == EXPECTED_N, f"coding sheet has {len(sheet)} rows, expected {EXPECTED_N}"
    assert len(full)  == EXPECTED_N, f"validation_full has {len(full)} rows, expected {EXPECTED_N}"

    # Build v2 lookup: pmid -> stance
    v2["pmid"] = v2["pmid"].astype(str)
    v2_lookup = dict(zip(v2["pmid"], v2["stance"]))

    # Bring pmid + v2 stance into the validation slice
    full_slim = full[["record_id", "pmid", "pub_year", "abstract"]].rename(
        columns={"abstract": "abstract_full", "pub_year": "pub_year_full"}
    )
    full_slim["pmid"] = full_slim["pmid"].astype(str)
    full_slim["llm_stance"] = full_slim["pmid"].map(v2_lookup)

    merged = sheet.merge(full_slim, on="record_id", how="inner", validate="one_to_one")
    merged["pub_year"] = merged["pub_year"].fillna(merged["pub_year_full"])
    merged = merged.drop(columns=["pub_year_full"])
    merged["abstract"] = merged["abstract_full"].fillna(merged["abstract"])
    merged = merged.drop(columns=["abstract_full"])

    missing_v2 = merged["llm_stance"].isna().sum()
    if missing_v2:
        print(f"WARNING: {missing_v2} validation records have no v2 label.", file=sys.stderr)
        # Drop them so kappa computation can proceed
        merged = merged[merged["llm_stance"].notna()].copy()

    # Drop FAILED rows from v2 (they were 4 total in the full corpus)
    n_failed = int((merged["llm_stance"] == "FAILED").sum())
    if n_failed:
        print(f"NOTE: dropping {n_failed} v2 FAILED rows from kappa computation.")
        merged = merged[merged["llm_stance"] != "FAILED"].copy()

    for col in ("human_stance", "llm_stance"):
        merged[col] = merged[col].astype(str).str.strip()
        bad = ~merged[col].isin(STANCE_ORDER)
        if bad.any():
            print(f"ERROR: invalid values in {col}:", file=sys.stderr)
            print(merged.loc[bad, ["record_id", col]].to_string(), file=sys.stderr)
            sys.exit(1)

    merged["y_human"] = merged["human_stance"].map(STANCE_TO_INT)
    merged["y_llm"]   = merged["llm_stance"].map(STANCE_TO_INT)
    print(f"Joined dataset: {len(merged)} rows (after dropping FAILED / missing v2)")
    return merged


def write_v2_report(df: pd.DataFrame, layers: list[dict],
                    flag_counts: dict, path: Path) -> None:
    lines = []
    lines.append("# Validation κ Report — v2 (revised prompt), EXPLORATORY\n")
    lines.append("**This is an exploratory κ pass on the v2 re-classification.** "
                 "The official, pre-registered validation κ stands at the v1 value "
                 "(see `kappa_report.md`). This pass is for diagnostic purposes only "
                 "and was NOT used to select the v2 prompt — the 300-record validation "
                 "set was sampled before v2 existed.\n")
    lines.append(f"_LLM stance source: `{V2_PATH.name}` (revised prompt, batch v2a)._")
    lines.append(f"_Human stance source: `{SHEET_PATH.name}`._\n")

    lines.append("## Sample\n")
    lines.append(f"- Total records (after dropping v2 FAILED): **{len(df)}**")
    lines.append("- Flag counts:")
    for k, v in flag_counts.items():
        lines.append(f"    - {k}: {v}")
    flag_cols = ["flag_no_stance", "flag_out_of_scope",
                 "flag_data_insufficient", "flag_meta_discourse"]
    multi = df[flag_cols].sum(axis=1) > 1
    lines.append(f"- Records with more than one flag: **{int(multi.sum())}**")
    lines.append("")

    lines.append("## Distribution\n")
    h_counts = df["human_stance"].value_counts().reindex(STANCE_ORDER, fill_value=0)
    l_counts = df["llm_stance"].value_counts().reindex(STANCE_ORDER, fill_value=0)
    lines.append("| Stance | LLM v2 | Human (Kingsley) |")
    lines.append("|---|---:|---:|")
    for s in STANCE_ORDER:
        lines.append(f"| {s} | {l_counts[s]} | {h_counts[s]} |")
    lines.append("")

    lines.append("## κ values\n")
    lines.append(f"All 95% CIs are bootstrap percentile (n_boot={N_BOOT}, seed=42).\n")
    lines.append("| Layer | n | Unweighted κ | Linear κ | Quadratic κ |")
    lines.append("|---|---:|---|---|---|")
    for layer in layers:
        kw = layer["kappas"]
        lines.append(f"| {layer['name']} | {layer['n']} | "
                     f"{fmt_kappa(kw['unweighted'])} | "
                     f"{fmt_kappa(kw['linear'])} | "
                     f"{fmt_kappa(kw['quadratic'])} |")
    lines.append("")

    lines.append("## Confusion matrices (v2 LLM)\n")
    for layer in layers:
        lines.append(f"### {layer['name']} (n={layer['n']})\n")
        lines.append("```")
        lines.append(cm_ascii(layer["cm"]))
        lines.append("```")
        lines.append("")

    lines.append("## Top disagreement patterns (Primary layer)\n")
    pairs = top_disagreement_pairs(df, k=10)
    lines.append("| Human | LLM v2 | n |")
    lines.append("|---|---|---:|")
    for _, r in pairs.iterrows():
        lines.append(f"| {r['human_stance']} | {r['llm_stance']} | {int(r['n'])} |")
    lines.append("")

    lines.append("## Per-stance metrics (Primary layer)\n")
    ps = layers[0]["per_stance"]
    lines.append("| Stance | Human n | LLM n | Precision | Recall | Agreement |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for _, r in ps.iterrows():
        lines.append(f"| {r['stance']} | {r['human_n']} | {r['llm_n']} | "
                     f"{r['precision']:.3f} | {r['recall']:.3f} | {r['agreement_rate']:.3f} |")
    lines.append("")

    path.write_text("\n".join(lines))


def main() -> None:
    print("=== compute_kappa_v2.py (EXPLORATORY) ===")
    print(f"Sheet: {SHEET_PATH}")
    print(f"v2   : {V2_PATH}\n")

    df = load_and_join_v2()
    df = parse_flags(df)
    flag_counts = print_flag_summary(df)

    layers = [compute_layer(df, name, mask_fn) for name, mask_fn in LAYER_SPECS]

    print("\n=== v2 κ summary (EXPLORATORY) ===")
    for layer in layers:
        kw = layer["kappas"]
        print(f"\n[{layer['name']}] n={layer['n']}")
        print(f"  Unweighted κ : {fmt_kappa(kw['unweighted'])}")
        print(f"  Linear κ     : {fmt_kappa(kw['linear'])}")
        print(f"  Quadratic κ  : {fmt_kappa(kw['quadratic'])}")

    write_v2_report(df, layers, flag_counts, OUT_MD)
    print(f"\nMarkdown report: {OUT_MD}")


if __name__ == "__main__":
    main()
