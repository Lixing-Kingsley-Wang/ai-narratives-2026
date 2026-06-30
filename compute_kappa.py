"""
compute_kappa.py — final validation analysis for the AI-narratives bibliometric study.

Computes Cohen's kappa (unweighted / linear-weighted / quadratic-weighted) with
bootstrap 95% CIs across three sensitivity layers:

    L1 Primary:        all 300 records (NO_STANCE treated as Neutral by human)
    L2 Sensitivity A:  exclude NO_STANCE / OUT_OF_SCOPE / DATA_INSUFFICIENT
    L3 Sensitivity B:  also exclude META_DISCOURSE

Outputs:
    output/validation/disagreements.csv
    output/validation/confusion_matrices.png
    output/validation/kappa_report.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import cohen_kappa_score, confusion_matrix

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent
SHEET_PATH = REPO / "output/validation/kingsly_coding_sheet.xlsx"
FULL_PATH  = REPO / "output/validation/kingsly_validation_full.csv"
OUT_DIR    = REPO / "output/validation"

STANCE_ORDER = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]
STANCE_TO_INT = {s: i for i, s in enumerate(STANCE_ORDER)}
INT_TO_STANCE = {i: s for i, s in enumerate(STANCE_ORDER)}

N_BOOT = 1000
SEED   = 42

KAPPA_TARGET      = 0.75   # "above target" threshold for headline
KAPPA_FIGURE_GATE = 0.60   # if L2 quadratic < this, pause before figure
EXPECTED_N        = 300


# ---------------------------------------------------------------------------
# Load + join
# ---------------------------------------------------------------------------
def load_and_join() -> pd.DataFrame:
    sheet = pd.read_excel(SHEET_PATH)
    full  = pd.read_csv(FULL_PATH)

    assert len(sheet) == EXPECTED_N, f"coding sheet has {len(sheet)} rows, expected {EXPECTED_N}"
    assert len(full)  == EXPECTED_N, f"validation_full has {len(full)} rows, expected {EXPECTED_N}"
    assert sheet["record_id"].notna().all(), "null record_id in coding sheet"
    assert full["record_id"].notna().all(),  "null record_id in validation_full"
    assert sheet["record_id"].is_unique, "duplicate record_id in coding sheet"
    assert full["record_id"].is_unique,  "duplicate record_id in validation_full"

    # Pull only the cols we need from full and rename to avoid suffix collisions.
    full_slim = (full[["record_id", "pmid", "pub_year", "stance", "abstract"]]
                 .rename(columns={"stance": "llm_stance",
                                  "abstract": "abstract_full",
                                  "pub_year": "pub_year_full"}))
    merged = sheet.merge(full_slim, on="record_id", how="inner", validate="one_to_one")
    # Prefer full's pub_year if the sheet's is missing.
    merged["pub_year"] = merged["pub_year"].fillna(merged["pub_year_full"])
    merged = merged.drop(columns=["pub_year_full"])

    if len(merged) < EXPECTED_N:
        missing_sheet = set(sheet["record_id"]) - set(full["record_id"])
        missing_full  = set(full["record_id"]) - set(sheet["record_id"])
        print(f"ERROR: merge produced {len(merged)} rows (expected {EXPECTED_N}).",
              file=sys.stderr)
        print(f"  In sheet but not full: {sorted(missing_sheet)[:20]}", file=sys.stderr)
        print(f"  In full but not sheet: {sorted(missing_full)[:20]}",  file=sys.stderr)
        sys.exit(1)

    # Prefer the abstract from full (not truncated) when writing disagreements
    merged["abstract"] = merged["abstract_full"].fillna(merged["abstract"])
    merged = merged.drop(columns=["abstract_full"])

    for col in ("human_stance", "llm_stance"):
        merged[col] = merged[col].astype(str).str.strip()
        bad = ~merged[col].isin(STANCE_ORDER)
        if bad.any():
            print(f"ERROR: invalid values in {col}:", file=sys.stderr)
            print(merged.loc[bad, ["record_id", col]].to_string(), file=sys.stderr)
            sys.exit(1)

    merged["y_human"] = merged["human_stance"].map(STANCE_TO_INT)
    merged["y_llm"]   = merged["llm_stance"].map(STANCE_TO_INT)
    return merged


# ---------------------------------------------------------------------------
# Flag parsing
# ---------------------------------------------------------------------------
# Case-insensitive. NO_STANCE: bracket form anywhere; "no/non-stance" / "no/non stance" / "nonstance".
RE_NO_STANCE = re.compile(
    r"(?:\[NO[_\- ]?STANCE\])|(?:(?:no|non)[\-\s]?stance)",
    re.IGNORECASE,
)
RE_OUT_OF_SCOPE = re.compile(
    r"(?:\[OUT[_\- ]?OF[_\- ]?SCOPE\])"
    r"|(?:out[\-\s]of[\-\s]scope)"
    r"|(?:not\s+related\s+topic)"
    r"|(?:filter\s+problem)",
    re.IGNORECASE,
)
RE_DATA_INSUFFICIENT = re.compile(
    r"(?:\[DATA[_\- ]?INSUFFICIENT\])"
    r"|(?:abstract\s+too\s+short)"
    r"|(?:data\s+insufficient)",
    re.IGNORECASE,
)
RE_META_DISCOURSE = re.compile(r"\[META[_\- ]?DISCOURSE\]", re.IGNORECASE)


def parse_flags(df: pd.DataFrame) -> pd.DataFrame:
    notes = df["human_notes"].fillna("").astype(str)
    df = df.copy()
    df["flag_no_stance"]         = notes.str.contains(RE_NO_STANCE)
    df["flag_out_of_scope"]      = notes.str.contains(RE_OUT_OF_SCOPE)
    df["flag_data_insufficient"] = notes.str.contains(RE_DATA_INSUFFICIENT)
    df["flag_meta_discourse"]    = notes.str.contains(RE_META_DISCOURSE)
    return df


def print_flag_summary(df: pd.DataFrame) -> dict[str, int]:
    counts = {
        "NO_STANCE":         int(df["flag_no_stance"].sum()),
        "OUT_OF_SCOPE":      int(df["flag_out_of_scope"].sum()),
        "DATA_INSUFFICIENT": int(df["flag_data_insufficient"].sum()),
        "META_DISCOURSE":    int(df["flag_meta_discourse"].sum()),
    }
    print("\n=== Flag counts ===")
    for k, v in counts.items():
        print(f"  {k:<20} {v}")
    print("\n  Pairwise overlaps:")
    flag_cols = ["flag_no_stance", "flag_out_of_scope",
                 "flag_data_insufficient", "flag_meta_discourse"]
    labels = ["NO_STANCE", "OUT_OF_SCOPE", "DATA_INSUFFICIENT", "META_DISCOURSE"]
    any_overlap = False
    for i in range(len(flag_cols)):
        for j in range(i + 1, len(flag_cols)):
            n = int((df[flag_cols[i]] & df[flag_cols[j]]).sum())
            if n > 0:
                any_overlap = True
                print(f"    {labels[i]} & {labels[j]}: {n}")
    if not any_overlap:
        print("    (none)")
    multi = df[flag_cols].sum(axis=1) > 1
    print(f"  Rows with >1 flag: {int(multi.sum())}")
    return counts


# ---------------------------------------------------------------------------
# Kappa + bootstrap
# ---------------------------------------------------------------------------
def _safe_kappa(y_h: np.ndarray, y_l: np.ndarray, weights: str | None) -> float:
    return cohen_kappa_score(y_h, y_l, weights=weights,
                             labels=list(range(len(STANCE_ORDER))))


def bootstrap_kappa_ci(y_h: np.ndarray, y_l: np.ndarray, weights: str | None,
                       n_boot: int = N_BOOT, seed: int = SEED
                       ) -> tuple[float, float, int]:
    rng = np.random.default_rng(seed)
    n = len(y_h)
    kappas = []
    skipped = 0
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        try:
            k = _safe_kappa(y_h[idx], y_l[idx], weights=weights)
            if np.isnan(k):
                skipped += 1
                continue
            kappas.append(k)
        except ValueError:
            skipped += 1
    if not kappas:
        return (float("nan"), float("nan"), skipped)
    lo, hi = np.percentile(kappas, [2.5, 97.5])
    return float(lo), float(hi), skipped


def kappa_block(y_h: np.ndarray, y_l: np.ndarray) -> dict:
    out = {}
    for label, w in [("unweighted", None), ("linear", "linear"), ("quadratic", "quadratic")]:
        point = _safe_kappa(y_h, y_l, weights=w)
        lo, hi, skipped = bootstrap_kappa_ci(y_h, y_l, weights=w)
        out[label] = {"point": point, "ci_lo": lo, "ci_hi": hi, "skipped": skipped}
    return out


# ---------------------------------------------------------------------------
# Confusion matrix + per-stance metrics
# ---------------------------------------------------------------------------
def confusion(y_h: np.ndarray, y_l: np.ndarray) -> np.ndarray:
    return confusion_matrix(y_h, y_l, labels=list(range(len(STANCE_ORDER))))


def per_stance_metrics(cm: np.ndarray) -> pd.DataFrame:
    rows = []
    for i, stance in enumerate(STANCE_ORDER):
        tp = cm[i, i]
        human_total = cm[i, :].sum()
        llm_total   = cm[:, i].sum()
        precision = tp / llm_total if llm_total else float("nan")
        recall    = tp / human_total if human_total else float("nan")
        agree     = tp / human_total if human_total else float("nan")
        rows.append({
            "stance": stance,
            "human_n": int(human_total),
            "llm_n": int(llm_total),
            "precision": precision,
            "recall": recall,
            "agreement_rate": agree,
        })
    return pd.DataFrame(rows)


def top_disagreement_pairs(df: pd.DataFrame, k: int = 5) -> pd.DataFrame:
    dis = df[df["y_human"] != df["y_llm"]].copy()
    return (dis.groupby(["human_stance", "llm_stance"]).size()
               .reset_index(name="n")
               .sort_values("n", ascending=False)
               .head(k))


# ---------------------------------------------------------------------------
# Layer compute
# ---------------------------------------------------------------------------
LAYER_SPECS = [
    ("Primary",       lambda df: pd.Series(True, index=df.index)),
    ("Sensitivity A", lambda df: ~(df["flag_no_stance"] | df["flag_out_of_scope"]
                                   | df["flag_data_insufficient"])),
    ("Sensitivity B", lambda df: ~(df["flag_no_stance"] | df["flag_out_of_scope"]
                                   | df["flag_data_insufficient"]
                                   | df["flag_meta_discourse"])),
]


def compute_layer(df: pd.DataFrame, name: str, mask_fn) -> dict:
    sub = df[mask_fn(df)].copy()
    y_h = sub["y_human"].to_numpy()
    y_l = sub["y_llm"].to_numpy()
    cm = confusion(y_h, y_l)
    return {
        "name": name,
        "n": len(sub),
        "kappas": kappa_block(y_h, y_l),
        "cm": cm,
        "per_stance": per_stance_metrics(cm),
    }


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
def export_disagreements(df: pd.DataFrame, path: Path) -> int:
    dis = df[df["y_human"] != df["y_llm"]].copy()
    dis["disagreement_distance"] = (dis["y_human"] - dis["y_llm"]).abs()
    cols = ["record_id", "pmid", "pub_year",
            "human_stance", "llm_stance", "disagreement_distance",
            "human_notes",
            "flag_no_stance", "flag_out_of_scope",
            "flag_data_insufficient", "flag_meta_discourse",
            "title", "abstract"]
    dis = dis[cols].sort_values(["disagreement_distance", "record_id"],
                                ascending=[False, True])
    dis.to_csv(path, index=False)
    return len(dis)


def fmt_kappa(kdict: dict) -> str:
    return f"{kdict['point']:.3f} ({kdict['ci_lo']:.3f}–{kdict['ci_hi']:.3f})"


def plot_confusion_matrices(layers: list[dict], path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    for ax, layer in zip(axes, layers):
        cm = layer["cm"]
        row_sums = cm.sum(axis=1, keepdims=True)
        with np.errstate(divide="ignore", invalid="ignore"):
            pct = np.where(row_sums > 0, cm / row_sums * 100, 0)
        annot = np.empty_like(cm, dtype=object)
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                annot[i, j] = f"{cm[i, j]}\n({pct[i, j]:.0f}%)"
        sns.heatmap(cm, annot=annot, fmt="", cmap="Blues",
                    xticklabels=STANCE_ORDER, yticklabels=STANCE_ORDER,
                    cbar=True, ax=ax, annot_kws={"size": 9})
        qk = layer["kappas"]["quadratic"]["point"]
        ax.set_title(f"{layer['name']} (n={layer['n']})\nQuadratic κ = {qk:.3f}")
        ax.set_xlabel("LLM stance")
        ax.set_ylabel("Human stance")
        ax.tick_params(axis="x", rotation=30)
        ax.tick_params(axis="y", rotation=0)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def cm_ascii(cm: np.ndarray) -> str:
    header = "Human \\ LLM  | " + " | ".join(f"{s[:8]:>8}" for s in STANCE_ORDER) + " | Total"
    sep    = "-" * len(header)
    rows = [header, sep]
    for i, stance in enumerate(STANCE_ORDER):
        cells = " | ".join(f"{cm[i, j]:>8d}" for j in range(len(STANCE_ORDER)))
        rows.append(f"{stance:<13}| {cells} | {cm[i, :].sum():>5d}")
    rows.append(sep)
    totals = " | ".join(f"{cm[:, j].sum():>8d}" for j in range(len(STANCE_ORDER)))
    rows.append(f"{'Total':<13}| {totals} | {cm.sum():>5d}")
    return "\n".join(rows)


def write_markdown_report(df: pd.DataFrame, layers: list[dict],
                          flag_counts: dict, path: Path) -> None:
    lines = []
    lines.append("# Validation κ Report\n")
    lines.append(f"_Generated by `compute_kappa.py`. "
                 f"Inputs: `{SHEET_PATH.name}`, `{FULL_PATH.name}`._\n")

    lines.append("## Sample\n")
    lines.append(f"- Total stratified sample: **{len(df)} records**")
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
    expected = pd.Series([60, 60, 60, 60, 60], index=STANCE_ORDER, name="expected")
    lines.append("Stance distribution (expected assumes balanced 60/60/60/60/60 stratification):\n")
    lines.append("| Stance | Expected | LLM (Sonnet) | Human (Kingsley) |")
    lines.append("|---|---:|---:|---:|")
    for s in STANCE_ORDER:
        lines.append(f"| {s} | {expected[s]} | {l_counts[s]} | {h_counts[s]} |")
    lines.append("")
    lines.append("Discrepancy note: any non-zero gap between LLM and Human "
                 "for a stance reflects re-classification during validation, "
                 "not stratification drift.\n")

    lines.append("## κ values\n")
    lines.append("All 95% CIs are bootstrap percentile (n_boot=1000, seed=42).\n")
    lines.append("| Layer | n | Unweighted κ | Linear κ | Quadratic κ |")
    lines.append("|---|---:|---|---|---|")
    for layer in layers:
        kw = layer["kappas"]
        lines.append(f"| {layer['name']} | {layer['n']} | "
                     f"{fmt_kappa(kw['unweighted'])} | "
                     f"{fmt_kappa(kw['linear'])} | "
                     f"{fmt_kappa(kw['quadratic'])} |")
    lines.append("")
    skipped_notes = []
    for layer in layers:
        for variant, kd in layer["kappas"].items():
            if kd["skipped"] > N_BOOT * 0.05:
                skipped_notes.append(
                    f"- {layer['name']} / {variant}: {kd['skipped']}/{N_BOOT} "
                    f"bootstrap iterations skipped (>5%) — likely sparse-category resamples.")
    if skipped_notes:
        lines.append("**Bootstrap stability notes:**")
        lines.extend(skipped_notes)
        lines.append("")

    lines.append("## Confusion matrices\n")
    for layer in layers:
        lines.append(f"### {layer['name']} (n={layer['n']})\n")
        lines.append("```")
        lines.append(cm_ascii(layer["cm"]))
        lines.append("```")
        lines.append("")

    lines.append("## Top disagreement patterns (Primary layer, all 300)\n")
    pairs = top_disagreement_pairs(df, k=5)
    lines.append("| Human | LLM | n |")
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("=== compute_kappa.py ===")
    print(f"Sheet: {SHEET_PATH}")
    print(f"Full : {FULL_PATH}\n")

    df = load_and_join()
    print(f"Joined dataset: {len(df)} rows")
    df = parse_flags(df)
    flag_counts = print_flag_summary(df)

    layers = [compute_layer(df, name, mask_fn) for name, mask_fn in LAYER_SPECS]

    print("\n=== κ summary ===")
    for layer in layers:
        kw = layer["kappas"]
        print(f"\n[{layer['name']}] n={layer['n']}")
        print(f"  Unweighted κ : {fmt_kappa(kw['unweighted'])}")
        print(f"  Linear κ     : {fmt_kappa(kw['linear'])}")
        print(f"  Quadratic κ  : {fmt_kappa(kw['quadratic'])}")

    dis_path = OUT_DIR / "disagreements.csv"
    n_dis = export_disagreements(df, dis_path)
    print(f"\nDisagreements CSV: {dis_path}  ({n_dis} rows)")

    # Gate check — pause if Sensitivity A quadratic κ < 0.60
    l2_qk = layers[1]["kappas"]["quadratic"]["point"]
    if l2_qk < KAPPA_FIGURE_GATE:
        print(f"\n!!! Sensitivity A quadratic κ = {l2_qk:.3f} < {KAPPA_FIGURE_GATE} — "
              f"pausing before figure as instructed.")
        print("    (No PNG written. Edit script or rerun after investigation.)")
    else:
        fig_path = OUT_DIR / "confusion_matrices.png"
        plot_confusion_matrices(layers, fig_path)
        print(f"Confusion matrix figure: {fig_path}")

    md_path = OUT_DIR / "kappa_report.md"
    write_markdown_report(df, layers, flag_counts, md_path)
    print(f"Markdown report: {md_path}")

    headline = layers[1]["kappas"]["quadratic"]
    above = "ABOVE TARGET" if headline["point"] >= KAPPA_TARGET else "BELOW TARGET"
    print("\n=== Headline ===")
    print(f"  Quadratic-weighted κ, Sensitivity A (n={layers[1]['n']}): "
          f"{headline['point']:.3f} "
          f"(95% CI {headline['ci_lo']:.3f}–{headline['ci_hi']:.3f})")
    print(f"  Recommendation: {above} (target ≥ {KAPPA_TARGET})")


if __name__ == "__main__":
    main()
