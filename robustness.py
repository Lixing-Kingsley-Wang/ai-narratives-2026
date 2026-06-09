"""
Robustness utilities for v1/v2 stance classification comparison.

v1 is canonical (Sensitivity A, kappa=0.789). v2 is robustness comparator
only. All analyses report v1 as the primary result; v2 figures and tables
are labelled exploratory.

Data lives outside the repo (gitignored). DATA_DIR is an absolute path
constant pointing to the parent checkout's output directory. Edit DATA_DIR
if running from another machine.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Literal, Union

import numpy as np
import pandas as pd

DATA_DIR = Path("/Users/kingslywang/repos/ai-narratives-2026/output")

V1_PATH = DATA_DIR / "classified_medical_Q1Q2.csv"
V2_PATH = DATA_DIR / "classified_medical_Q1Q2_v2_pre_predclaim_fix.csv"
THEMES_PATH = DATA_DIR / "analysis" / "thematic_alarm.csv"

STANCES = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]
SEED = 42
N_BOOT_DEFAULT = 1000

# ---------------------------------------------------------------------------
# pub_type bucketing
# ---------------------------------------------------------------------------

PUBTYPE_BUCKETS_7 = [
    "Editorial",
    "Letter",
    "Comment",
    "News",
    "Systematic Review",
    "Review",
    "Research Article",
]

PUBTYPE_BUCKETS_5 = ["Research Article", "Editorial", "Review", "Commentary", "Letter"]


def simplify_pubtype_7(pt: str) -> str:
    """Bucket the compound PubMed pub_type string into 7 categories.

    Precedence matches analyse_industry.simplify_pubtype: Editorial > Letter
    > Systematic Review > Review > Comment > News > Research Article.
    """
    pt = pt or ""
    if "Editorial" in pt:
        return "Editorial"
    if "Letter" in pt:
        return "Letter"
    if "Systematic Review" in pt:
        return "Systematic Review"
    if "Review" in pt:
        return "Review"
    if "Comment" in pt:
        return "Comment"
    if "News" in pt:
        return "News"
    return "Research Article"


def simplify_pubtype_5(pt: str) -> str:
    """Collapse the 7-bucket scheme into the 5 categories from the brief.

    Systematic Review folds into Review; Comment folds into Commentary;
    News folds into Research Article (rare).
    """
    seven = simplify_pubtype_7(pt)
    if seven == "Systematic Review":
        return "Review"
    if seven == "Comment":
        return "Commentary"
    if seven == "News":
        return "Research Article"
    return seven


# ---------------------------------------------------------------------------
# loaders
# ---------------------------------------------------------------------------


def load_classifications(
    version: Literal["v1", "v2"],
    drop_failed: bool = True,
    year_range: tuple[int, int] | None = (2021, 2026),
) -> pd.DataFrame:
    """Load v1 or v2 with canonical column names; filter FAILED + year range.

    Returns DataFrame with at least: pmid, pub_year, pub_type_simple_7,
    pub_type_simple_5, pub_type_raw, journal, stance, predictive_claim,
    and (v2 only) meta_discourse.
    """
    if version == "v1":
        path = V1_PATH
    elif version == "v2":
        path = V2_PATH
    else:
        raise ValueError(f"version must be 'v1' or 'v2', got {version!r}")

    df = pd.read_csv(path, low_memory=False)

    n_total = len(df)
    n_failed = (df["stance"] == "FAILED").sum()
    if drop_failed:
        df = df[df["stance"] != "FAILED"].copy()

    df["pub_year"] = pd.to_numeric(df["pub_year"], errors="coerce").astype("Int64")
    if year_range is not None:
        lo, hi = year_range
        df = df[(df["pub_year"] >= lo) & (df["pub_year"] <= hi)].copy()

    df["pub_type_raw"] = df["pub_type"].fillna("")
    df["pub_type_simple_7"] = df["pub_type_raw"].map(simplify_pubtype_7)
    df["pub_type_simple_5"] = df["pub_type_raw"].map(simplify_pubtype_5)

    keep = [
        "pmid",
        "pub_year",
        "pub_type_raw",
        "pub_type_simple_7",
        "pub_type_simple_5",
        "journal",
        "stance",
        "predictive_claim",
    ]
    if version == "v2" and "meta_discourse" in df.columns:
        keep.append("meta_discourse")

    out = df[keep].copy()
    out.attrs["version"] = version
    out.attrs["n_total"] = int(n_total)
    out.attrs["n_failed"] = int(n_failed)
    out.attrs["n_after_filter"] = int(len(out))
    return out


def attach_themes(df: pd.DataFrame) -> pd.DataFrame:
    """Left-join theme columns onto a v1 frame via pmid. v1-only."""
    if df.attrs.get("version") != "v1":
        raise ValueError("Themes are only classified on v1 records.")
    themes = pd.read_csv(THEMES_PATH, low_memory=False)
    themes = themes[["pmid", "themes", "theme_1", "theme_2", "theme_3"]]
    return df.merge(themes, on="pmid", how="left")


# ---------------------------------------------------------------------------
# bootstrap
# ---------------------------------------------------------------------------


def _coerce_agg(value):
    """Normalize agg_fn output to (kind, ndarray-or-frame, index)."""
    if isinstance(value, (int, float, np.integer, np.floating)):
        return "scalar", float(value), None
    if isinstance(value, pd.Series):
        return "series", value, value.index
    if isinstance(value, pd.DataFrame):
        return "frame", value, (value.index, value.columns)
    raise TypeError(f"agg_fn must return scalar, Series, or DataFrame; got {type(value)!r}")


def bootstrap_ci(
    df: pd.DataFrame,
    agg_fn: Callable[[pd.DataFrame], Union[float, pd.Series, pd.DataFrame]],
    n_boot: int = N_BOOT_DEFAULT,
    seed: int = SEED,
    confidence: float = 0.95,
) -> dict:
    """Resample df rows with replacement, apply agg_fn, percentile CI."""
    rng = np.random.default_rng(seed)
    point = agg_fn(df)
    kind, point_norm, idx = _coerce_agg(point)

    lo_q = (1 - confidence) / 2 * 100
    hi_q = 100 - lo_q

    n = len(df)

    def _sample():
        return df.iloc[rng.integers(0, n, size=n)].reset_index(drop=True)

    if kind == "scalar":
        samples = np.empty(n_boot)
        for i in range(n_boot):
            samples[i] = float(agg_fn(_sample()))
        return {
            "point": point_norm,
            "lower": float(np.percentile(samples, lo_q)),
            "upper": float(np.percentile(samples, hi_q)),
            "distribution": samples,
        }

    if kind == "series":
        rows = []
        for _ in range(n_boot):
            s = agg_fn(_sample())
            rows.append(s.reindex(idx).fillna(0.0))
        dist = pd.DataFrame(rows).reset_index(drop=True)
        lower = dist.quantile(lo_q / 100)
        upper = dist.quantile(hi_q / 100)
        return {
            "point": point_norm,
            "lower": lower,
            "upper": upper,
            "distribution": dist,
        }

    # DataFrame: stack to a multi-index series for resampling, then unstack
    rows = []
    row_idx, col_idx = idx
    for _ in range(n_boot):
        frame = agg_fn(_sample()).reindex(index=row_idx, columns=col_idx).fillna(0.0)
        rows.append(frame.stack(future_stack=True))
    dist = pd.DataFrame(rows).reset_index(drop=True)
    lower = dist.quantile(lo_q / 100).unstack()
    upper = dist.quantile(hi_q / 100).unstack()
    return {
        "point": point_norm,
        "lower": lower.reindex(index=row_idx, columns=col_idx),
        "upper": upper.reindex(index=row_idx, columns=col_idx),
        "distribution": dist,
    }


# ---------------------------------------------------------------------------
# robustness verdict
# ---------------------------------------------------------------------------


def robustness_verdict(
    v1_result: Union[float, pd.Series, pd.DataFrame],
    v2_result: Union[float, pd.Series, pd.DataFrame],
    tolerance_pp: float = 3.0,
) -> dict:
    """Per-cell verdict: 'robust' if |v1-v2|<tol, else 'sensitive'.

    'directionally consistent' bucket only applies when the input has a
    natural reference; for raw distributions this collapses to robust vs
    sensitive. Verdicts and summary metrics returned in a dict.
    """
    if isinstance(v1_result, (int, float, np.integer, np.floating)):
        v1_arr = np.array([float(v1_result)])
        v2_arr = np.array([float(v2_result)])
        index = None
        shape = "scalar"
    elif isinstance(v1_result, pd.Series):
        v1_arr = v1_result.values.astype(float)
        v2_arr = v2_result.reindex(v1_result.index).fillna(0).values.astype(float)
        index = v1_result.index
        shape = "series"
    elif isinstance(v1_result, pd.DataFrame):
        v1_arr = v1_result.values.astype(float)
        v2_arr = (
            v2_result.reindex(index=v1_result.index, columns=v1_result.columns)
            .fillna(0)
            .values.astype(float)
        )
        index = (v1_result.index, v1_result.columns)
        shape = "frame"
    else:
        raise TypeError(f"unsupported type {type(v1_result)!r}")

    diff = v2_arr - v1_arr
    abs_diff = np.abs(diff)
    verdicts = np.where(abs_diff < tolerance_pp, "robust", "sensitive")

    if shape == "scalar":
        cell_verdicts = str(verdicts[0])
    elif shape == "series":
        cell_verdicts = pd.Series(verdicts, index=index)
    else:
        cell_verdicts = pd.DataFrame(verdicts, index=index[0], columns=index[1])

    summary = {
        "n_cells": int(abs_diff.size),
        "n_robust": int((abs_diff < tolerance_pp).sum()),
        "n_sensitive": int((abs_diff >= tolerance_pp).sum()),
        "max_abs_diff": float(abs_diff.max()),
        "mean_abs_diff": float(abs_diff.mean()),
        "tolerance_pp": float(tolerance_pp),
    }
    return {"cell_verdicts": cell_verdicts, "summary": summary}


# ---------------------------------------------------------------------------
# dual analysis: orchestrator
# ---------------------------------------------------------------------------


def _format_value_with_ci(point, lower, upper, fmt="{:.1f}") -> str:
    return f"{fmt.format(point)} ({fmt.format(lower)}–{fmt.format(upper)})"


def _result_to_long_df(boot: dict, kind: str) -> pd.DataFrame:
    """Flatten a bootstrap_ci result to a long-format DataFrame for CSV save."""
    if kind == "scalar":
        return pd.DataFrame(
            [{"point": boot["point"], "ci_lower": boot["lower"], "ci_upper": boot["upper"]}]
        )
    if kind == "series":
        return pd.DataFrame(
            {
                "group": boot["point"].index,
                "point": boot["point"].values,
                "ci_lower": boot["lower"].values,
                "ci_upper": boot["upper"].values,
            }
        )
    # frame: row × col × {point, lower, upper}
    pt = boot["point"].stack(future_stack=True).rename("point")
    lo = boot["lower"].stack(future_stack=True).rename("ci_lower")
    hi = boot["upper"].stack(future_stack=True).rename("ci_upper")
    out = pd.concat([pt, lo, hi], axis=1).reset_index()
    return out


def dual_analysis(
    agg_fn: Callable[[pd.DataFrame], Union[float, pd.Series, pd.DataFrame]],
    agg_name: str,
    output_dir: Path | str,
    n_boot: int = N_BOOT_DEFAULT,
    *,
    v1_df: pd.DataFrame | None = None,
    v2_df: pd.DataFrame | None = None,
    tolerance_pp: float = 3.0,
    value_fmt: str = "{:.1f}",
) -> dict:
    """Run agg_fn on v1 and v2, bootstrap each, save CSVs + markdown report."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if v1_df is None:
        v1_df = load_classifications("v1")
    if v2_df is None:
        v2_df = load_classifications("v2")

    boot_v1 = bootstrap_ci(v1_df, agg_fn, n_boot=n_boot)
    boot_v2 = bootstrap_ci(v2_df, agg_fn, n_boot=n_boot)
    kind, _, _ = _coerce_agg(boot_v1["point"] if not isinstance(boot_v1["point"], float)
                              else boot_v1["point"])
    # Re-detect kind cleanly from the raw point objects
    if isinstance(boot_v1["point"], float):
        kind = "scalar"
    elif isinstance(boot_v1["point"], pd.Series):
        kind = "series"
    else:
        kind = "frame"

    df_v1 = _result_to_long_df(boot_v1, kind)
    df_v2 = _result_to_long_df(boot_v2, kind)
    df_v1.to_csv(output_dir / f"{agg_name}_v1.csv", index=False)
    df_v2.to_csv(output_dir / f"{agg_name}_v2.csv", index=False)

    verdict = robustness_verdict(boot_v1["point"], boot_v2["point"], tolerance_pp)

    # Build markdown
    md = [f"# Robustness report — {agg_name}", ""]
    md.append(f"- v1 records: {len(v1_df):,}")
    md.append(f"- v2 records: {len(v2_df):,}")
    md.append(f"- Bootstrap n = {n_boot}, seed = {SEED}, 95% CI")
    md.append(f"- Tolerance for 'robust' verdict: {tolerance_pp} pp")
    md.append("")
    md.append("## Verdict summary")
    s = verdict["summary"]
    md.append(f"- Cells: {s['n_cells']}, robust: {s['n_robust']}, sensitive: {s['n_sensitive']}")
    md.append(
        f"- Max |v1-v2| diff: **{s['max_abs_diff']:.2f} pp**, mean: {s['mean_abs_diff']:.2f} pp"
    )
    md.append("")
    md.append("## v1 vs v2 (point estimates with 95% CI)")
    md.append("")
    if kind == "scalar":
        md.append(
            f"- v1: {_format_value_with_ci(boot_v1['point'], boot_v1['lower'], boot_v1['upper'], value_fmt)}"
        )
        md.append(
            f"- v2: {_format_value_with_ci(boot_v2['point'], boot_v2['lower'], boot_v2['upper'], value_fmt)}"
        )
        md.append(f"- verdict: **{verdict['cell_verdicts']}**")
    elif kind == "series":
        md.append("| group | v1 | v2 | Δ (pp) | verdict |")
        md.append("|---|---|---|---:|---|")
        for g in boot_v1["point"].index:
            v1_str = _format_value_with_ci(
                boot_v1["point"][g], boot_v1["lower"][g], boot_v1["upper"][g], value_fmt
            )
            v2_pt = boot_v2["point"].get(g, 0.0)
            v2_lo = boot_v2["lower"].get(g, 0.0)
            v2_hi = boot_v2["upper"].get(g, 0.0)
            v2_str = _format_value_with_ci(v2_pt, v2_lo, v2_hi, value_fmt)
            delta = v2_pt - boot_v1["point"][g]
            cv = verdict["cell_verdicts"].get(g, "n/a")
            md.append(f"| {g} | {v1_str} | {v2_str} | {delta:+.2f} | {cv} |")
    else:
        # frame: one row per (row_idx, col)
        md.append("| row | col | v1 | v2 | Δ (pp) | verdict |")
        md.append("|---|---|---|---|---:|---|")
        for r in boot_v1["point"].index:
            for c in boot_v1["point"].columns:
                v1_pt = boot_v1["point"].loc[r, c]
                v1_lo = boot_v1["lower"].loc[r, c]
                v1_hi = boot_v1["upper"].loc[r, c]
                v2_pt = boot_v2["point"].loc[r, c] if c in boot_v2["point"].columns and r in boot_v2["point"].index else 0.0
                v2_lo = boot_v2["lower"].loc[r, c] if c in boot_v2["lower"].columns and r in boot_v2["lower"].index else 0.0
                v2_hi = boot_v2["upper"].loc[r, c] if c in boot_v2["upper"].columns and r in boot_v2["upper"].index else 0.0
                delta = v2_pt - v1_pt
                cv = verdict["cell_verdicts"].loc[r, c]
                md.append(
                    f"| {r} | {c} | {_format_value_with_ci(v1_pt, v1_lo, v1_hi, value_fmt)} "
                    f"| {_format_value_with_ci(v2_pt, v2_lo, v2_hi, value_fmt)} "
                    f"| {delta:+.2f} | {cv} |"
                )

    (output_dir / f"{agg_name}_robustness.md").write_text("\n".join(md) + "\n")

    return {
        "v1_result": boot_v1,
        "v2_result": boot_v2,
        "verdict": verdict,
        "files": [
            output_dir / f"{agg_name}_v1.csv",
            output_dir / f"{agg_name}_v2.csv",
            output_dir / f"{agg_name}_robustness.md",
        ],
    }
