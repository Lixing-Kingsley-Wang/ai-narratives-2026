"""
AI-adoption vs critical-stance by specialty (Dan's unfamiliarity hypothesis).

Hypothesis (Dan): specialties that have NOT adopted AI clinically may be more
critical out of unfamiliarity / conservatism, rather than critique grounded in
real hallucination / error experience. We rank specialties by AI clinical
adoption and correlate against critical (Alarm + Caution) rate. Dan predicts a
NEGATIVE correlation (more adoption -> less critical).

Two adoption measures:
  (a) EXTERNAL: count of FDA-cleared AI/ML-enabled medical devices per FDA
      review panel, mapped to our 18 specialty buckets. Requires a real device
      list at output/external/fda_aiml_devices.csv. If absent and the live FDA
      list cannot be fetched, this arm STOPS and prints exactly which file is
      needed -- it never fabricates device counts.
  (b) IN-CORPUS PROXY: within each specialty, the share of papers that are
      empirical evaluation/deployment (paper_type == 'evaluative') vs pure
      discourse/commentary (paper_type == 'discourse'). Partly endogenous, so
      reported as a cross-check only.

Conventions: v1 canonical, pub_year 2021-2026, drop FAILED, bootstrap n=1000
seed=42 percentile 95% CI. Reuses analysis/robustness.py (loader, bootstrap_ci).

Produces (FDA arm only runs if the device file is present):
  output/analyses/specialty_aiadoption.csv
  output/figures/specialty_aiadoption_vs_critical.png   (FDA arm)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import permutation_test, spearmanr

from analysis.robustness import (
    DATA_DIR,
    SEED,
    bootstrap_ci,
    load_classifications,
)

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"
FDA_PATH = WORKTREE / "output" / "external" / "fda_aiml_devices.csv"

# Specialty classifications (pmid -> specialty). Lives outside this worktree;
# resolve against the first existing canonical location.
_SPEC_CANDIDATES = [
    WORKTREE / "output" / "specialty_classifications.csv",
    DATA_DIR / "specialty_classifications.csv",
    Path(
        "/Users/kingslywang/repos/ai-narratives-2026/.claude/worktrees/"
        "interesting-poitras-d9a5c4/output/specialty_classifications.csv"
    ),
]


def _resolve_spec_path() -> Path:
    for p in _SPEC_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError(
        "specialty_classifications.csv not found in any canonical location:\n  "
        + "\n  ".join(str(p) for p in _SPEC_CANDIDATES)
    )


# 18 specialty buckets (matches run_specialty_critical.py).
ALL_SPECIALTIES = [
    "Radiology / Diagnostic Imaging",
    "Pathology / Laboratory Medicine",
    "Cardiology",
    "Oncology",
    "Surgery",
    "Ophthalmology",
    "Dermatology",
    "Neurology / Neuroscience",
    "Mental Health / Psychiatry",
    "Internal Medicine / Primary Care",
    "Emergency Medicine / Critical Care",
    "Pediatrics",
    "Obstetrics / Gynecology",
    "Dentistry",
    "Medical Informatics / Digital Health",
    "Nursing",
    "Medical Education",
    "Multidisciplinary / Other",
]

# FDA review-panel -> our specialty bucket. This is a SPEC (a mapping rule),
# not data: it tells the FDA arm how to aggregate real device counts once a
# real device list is supplied. Approximate by construction (see caveats).
# Keys are lowercased substrings matched against the FDA 'Panel (Lead)' field.
FDA_PANEL_TO_SPECIALTY = {
    "radiology": "Radiology / Diagnostic Imaging",
    "cardiovascular": "Cardiology",
    "neurology": "Neurology / Neuroscience",
    "ophthalmic": "Ophthalmology",
    "pathology": "Pathology / Laboratory Medicine",
    "hematology": "Pathology / Laboratory Medicine",
    "clinical chemistry": "Pathology / Laboratory Medicine",
    "immunology": "Pathology / Laboratory Medicine",
    "microbiology": "Pathology / Laboratory Medicine",
    "molecular genetics": "Pathology / Laboratory Medicine",
    "toxicology": "Pathology / Laboratory Medicine",
    "toxcicology": "Pathology / Laboratory Medicine",  # FDA list misspells this
    "general and plastic surgery": "Surgery",
    "general & plastic surgery": "Surgery",
    "orthopedic": "Surgery",
    "ear, nose, and throat": "Surgery",
    "ear nose": "Surgery",
    "obstetrics": "Obstetrics / Gynecology",
    "gynecolog": "Obstetrics / Gynecology",
    "dental": "Dentistry",
    "anesthesiology": "Emergency Medicine / Critical Care",
    "gastroenterology": "Internal Medicine / Primary Care",
    "general hospital": "Multidisciplinary / Other",
    "physical medicine": "Multidisciplinary / Other",
}

# Specialties with no meaningful FDA device panel -> structural zero adoption.
# Recorded explicitly so the FDA arm scores them 0 rather than dropping them.
FDA_STRUCTURAL_ZERO = [
    "Mental Health / Psychiatry",
    "Nursing",
    "Medical Education",
    "Medical Informatics / Digital Health",
    "Pediatrics",
    "Dermatology",
    "Oncology",
]


def attach_specialty(df: pd.DataFrame) -> pd.DataFrame:
    spec = pd.read_csv(_resolve_spec_path(), usecols=["pmid", "specialty"])
    df = df.copy()
    df["pmid"] = df["pmid"].astype(str)
    spec["pmid"] = spec["pmid"].astype(str)
    return df.merge(spec, on="pmid", how="left")


def attach_paper_type(df: pd.DataFrame) -> pd.DataFrame:
    """Merge paper_type (evaluative/discourse) from the canonical v1 CSV."""
    raw = pd.read_csv(
        DATA_DIR / "classified_medical_Q1Q2.csv",
        usecols=["pmid", "paper_type"],
        low_memory=False,
    )
    df = df.copy()
    df["pmid"] = df["pmid"].astype(str)
    raw["pmid"] = raw["pmid"].astype(str)
    return df.merge(raw, on="pmid", how="left")


def spearman_report(x: np.ndarray, y: np.ndarray) -> dict:
    """Spearman rho with two-sided, one-sided (rho<0), and permutation p.

    Dan predicts a NEGATIVE correlation, so the directional test is
    alternative='less'. The permutation p does not lean on the t-approximation
    and is the more honest value at n=18.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    rho, p_two = spearmanr(x, y)
    _, p_less = spearmanr(x, y, alternative="less")

    def _stat(a, b):
        return spearmanr(a, b).statistic

    perm = permutation_test(
        (x, y),
        _stat,
        permutation_type="pairings",
        alternative="less",
        n_resamples=10000,
        random_state=SEED,
    )
    return {
        "rho": float(rho),
        "p_two": float(p_two),
        "p_one": float(p_less),
        "p_perm_one": float(perm.pvalue),
        "n": int(len(x)),
    }


def critical_by_specialty(df: pd.DataFrame) -> pd.Series:
    mask = df["stance"].isin(["Alarm", "Caution"])
    out = mask.groupby(df["specialty"]).mean() * 100
    return out.reindex(ALL_SPECIALTIES).fillna(0.0)


def evaluative_share_by_specialty(df: pd.DataFrame) -> pd.Series:
    """In-corpus adoption proxy: % of papers that are empirical evaluations."""
    mask = df["paper_type"].eq("evaluative")
    out = mask.groupby(df["specialty"]).mean() * 100
    return out.reindex(ALL_SPECIALTIES).fillna(0.0)


# ---------------------------------------------------------------------------
# FDA external device counts
# ---------------------------------------------------------------------------


def _find_panel_column(cols: list[str]) -> str | None:
    for c in cols:
        cl = c.strip().lower()
        if "panel" in cl or "specialty" in cl or "advisory committee" in cl:
            return c
    return None


def load_fda_device_counts(counts_index: list[str]) -> pd.Series | None:
    """Return device counts per specialty from a real FDA list, or None.

    Maps the FDA 'Panel (Lead)' column onto our specialty buckets via
    FDA_PANEL_TO_SPECIALTY. Never fabricates: returns None (and the caller
    prints the required file) when no usable device list is available.
    """
    if not FDA_PATH.exists():
        return None

    fda = pd.read_csv(FDA_PATH, low_memory=False)
    panel_col = _find_panel_column(list(fda.columns))
    if panel_col is None:
        print(
            f"  ! {FDA_PATH} has no recognizable panel column "
            f"(columns: {list(fda.columns)}). Expected a 'Panel (Lead)' column."
        )
        return None

    panels = fda[panel_col].fillna("").astype(str).str.lower()
    mapped = pd.Series("UNMAPPED", index=fda.index, dtype=object)
    for key, spec in FDA_PANEL_TO_SPECIALTY.items():
        hit = panels.str.contains(key, regex=False)
        mapped[hit & mapped.eq("UNMAPPED")] = spec

    n_unmapped = int(mapped.eq("UNMAPPED").sum())
    if n_unmapped:
        ex = (
            fda.loc[mapped.eq("UNMAPPED"), panel_col]
            .astype(str)
            .value_counts()
            .head(8)
        )
        print(f"  ! {n_unmapped} FDA devices had panels not in the mapping; top unmapped:")
        for panel, n in ex.items():
            print(f"      {panel!r}: {n}")

    counts = (
        mapped[mapped.ne("UNMAPPED")]
        .value_counts()
        .reindex(counts_index)
        .fillna(0.0)
    )
    # Structural zeros stay 0 (already filled). Return full series.
    return counts


def print_fda_file_requirement() -> None:
    print("\n" + "!" * 72)
    print("FDA ARM STOPPED — no usable AI/ML device list available.")
    print("!" * 72)
    print("The live FDA page could not be fetched and no local copy exists.")
    print("To run the external-adoption arm, provide this file:\n")
    print(f"    {FDA_PATH}")
    print("\nExpected: one row per FDA-cleared AI/ML-enabled medical device,")
    print("with at least a panel column (any of: 'Panel (Lead)', 'Panel',")
    print("'Specialty', 'Advisory Committee'). Source: FDA 'Artificial")
    print("Intelligence and Machine Learning (AI/ML)-Enabled Medical Devices'")
    print("downloadable spreadsheet.")
    print("\nNo device counts were fabricated. The panel->specialty mapping that")
    print("WOULD be applied once the file exists is printed below.")


def print_panel_mapping() -> None:
    print("\nFDA panel -> specialty bucket mapping (applied to real device counts):")
    # Invert for readable grouping.
    by_spec: dict[str, list[str]] = {}
    for panel, spec in FDA_PANEL_TO_SPECIALTY.items():
        by_spec.setdefault(spec, []).append(panel)
    for spec in ALL_SPECIALTIES:
        panels = by_spec.get(spec)
        if panels:
            print(f"  {spec:<40} <- {', '.join(sorted(set(panels)))}")
        elif spec in FDA_STRUCTURAL_ZERO:
            print(f"  {spec:<40} <- (no FDA panel; structural 0)")
        else:
            print(f"  {spec:<40} <- (no panel mapped)")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("AI-adoption vs critical stance by specialty — Dan's unfamiliarity test")
    print("=" * 72)

    # ---- Load v1, attach specialty + paper_type ---------------------------
    v1 = attach_paper_type(attach_specialty(load_classifications("v1")))
    print(f"v1 records (FAILED dropped, 2021-2026): {len(v1):,}")

    counts = (
        v1["specialty"].value_counts().reindex(ALL_SPECIALTIES).fillna(0).astype(int)
    )
    keep = [s for s in ALL_SPECIALTIES if counts[s] >= 30]
    rare = [s for s in ALL_SPECIALTIES if counts[s] < 30]
    for s in rare:
        print(f"  excluding {s!r} (n={counts[s]} < 30)")
    print(f"Specialties retained (n>=30): {len(keep)}")

    # ---- Step 1: reproduce critical rate per specialty --------------------
    print("\n[1] Critical (Alarm + Caution) rate by specialty — v1, bootstrap 95% CI")
    print("-" * 72)
    boot = bootstrap_ci(v1, critical_by_specialty)
    crit = boot["point"].reindex(keep).sort_values(ascending=False)
    for s in crit.index:
        print(
            f"  {s:<40} n={counts[s]:>5,}  {crit[s]:5.1f}%  "
            f"({boot['lower'][s]:5.1f}-{boot['upper'][s]:5.1f})"
        )
    print(
        f"\n  CHECK: Mental Health/Psychiatry = {crit.get('Mental Health / Psychiatry', float('nan')):.1f}% "
        f"(expect ~51.3%); Cardiology = {crit.get('Cardiology', float('nan')):.1f}% (expect ~16.8%)"
    )

    # ---- Step 3: in-corpus adoption proxy (evaluative share) --------------
    print("\n[3] In-corpus adoption proxy — % empirical-evaluation papers (vs discourse)")
    print("-" * 72)
    n_pt_missing = int(v1["paper_type"].isna().sum())
    if n_pt_missing:
        print(f"  (paper_type missing for {n_pt_missing} records — excluded from share)")
    proxy = evaluative_share_by_specialty(v1).reindex(keep).sort_values(ascending=False)
    for s in proxy.index:
        print(f"  {s:<40} n={counts[s]:>5,}  {proxy[s]:5.1f}% evaluative")

    # ---- Step 2: FDA external device counts -------------------------------
    print("\n[2] External adoption — FDA AI/ML-enabled device counts per specialty")
    print("-" * 72)
    fda_counts = load_fda_device_counts(keep)
    print_panel_mapping()

    # ---- Step 4: Spearman correlations ------------------------------------
    print("\n[4] Spearman rank correlation across specialties (Dan predicts NEGATIVE)")
    print("    one-sided = H1: rho < 0; p_perm = 10k pairing-permutation, seed=42")
    print("-" * 72)

    crit_keep = boot["point"].reindex(keep)
    proxy_keep = evaluative_share_by_specialty(v1).reindex(keep)

    # 4b: in-corpus proxy vs critical rate (always available).
    rep_b = spearman_report(proxy_keep.values, crit_keep.values)
    print(
        f"  (b) in-corpus evaluative-share vs critical-rate: rho={rep_b['rho']:+.3f}, "
        f"n={rep_b['n']}\n"
        f"        p one-sided={rep_b['p_one']:.4f}  (two-sided={rep_b['p_two']:.4f}, "
        f"perm one-sided={rep_b['p_perm_one']:.4f})"
    )

    # 4a: FDA device count vs critical rate (only if real device data present).
    rep_a = None
    if fda_counts is not None:
        rep_a = spearman_report(fda_counts.reindex(keep).values, crit_keep.values)
        print(
            f"  (a) FDA-device-count vs critical-rate:           rho={rep_a['rho']:+.3f}, "
            f"n={rep_a['n']}\n"
            f"        p one-sided={rep_a['p_one']:.4f}  (two-sided={rep_a['p_two']:.4f}, "
            f"perm one-sided={rep_a['p_perm_one']:.4f})"
        )
    else:
        print("  (a) FDA-device-count vs critical-rate:           SKIPPED (no device file)")
        print_fda_file_requirement()

    # ---- Save combined table ---------------------------------------------
    out = pd.DataFrame(
        {
            "specialty": keep,
            "n_papers": [int(counts[s]) for s in keep],
            "critical_rate_pct": [float(boot["point"][s]) for s in keep],
            "critical_ci_lo": [float(boot["lower"][s]) for s in keep],
            "critical_ci_hi": [float(boot["upper"][s]) for s in keep],
            "evaluative_share_pct": [float(proxy_keep[s]) for s in keep],
            "fda_device_count": [
                (float(fda_counts.reindex(keep)[s]) if fda_counts is not None else np.nan)
                for s in keep
            ],
        }
    )
    out_csv = ANALYSES_DIR / "specialty_aiadoption.csv"
    out.to_csv(out_csv, index=False)
    print(f"\nSaved table: {out_csv.relative_to(WORKTREE)}")

    # ---- Step 5: figure (FDA arm only) ------------------------------------
    if fda_counts is not None:
        make_figure(keep, counts, boot, fda_counts, rep_a)
    else:
        print(
            "\n[5] Figure SKIPPED — scatter needs FDA device counts. "
            "Re-run after providing the device file."
        )

    # ---- Step 6: verdict --------------------------------------------------
    print("\n[6] Verdict")
    print("-" * 72)
    report_verdict(crit, proxy_keep, rep_a, rep_b, fda_counts is not None)


def make_figure(keep, counts, boot, fda_counts, rep_a) -> None:
    crit = boot["point"].reindex(keep)
    fda = fda_counts.reindex(keep)
    x = fda.values.astype(float)
    y = crit.values.astype(float)
    sizes = np.array([counts[s] for s in keep], dtype=float)
    sizes = 40 + 360 * (sizes - sizes.min()) / max(np.ptp(sizes), 1)

    # log x; shift zeros to 0.5 so they plot on a log axis.
    x_plot = np.where(x <= 0, 0.5, x)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(x_plot, y, s=sizes, color="#2C7FB8", alpha=0.75, edgecolor="white", zorder=3)

    for s, xp, yp in zip(keep, x_plot, y):
        label = s.split(" / ")[0]
        ax.annotate(
            label,
            (xp, yp),
            xytext=(0, 6),
            textcoords="offset points",
            fontsize=8,
            fontweight="normal",
            color="#444",
            ha="center",
        )

    # rank/regression line in log space over the mapped (non-zero) points.
    pos = x > 0
    if pos.sum() >= 3:
        lx = np.log10(x[pos])
        coef = np.polyfit(lx, y[pos], 1)
        xs = np.linspace(lx.min(), lx.max(), 100)
        ax.plot(10 ** xs, np.polyval(coef, xs), "--", color="#C0392B", lw=1.5,
                label=f"OLS fit (log x)  Spearman rho={rep_a['rho']:+.2f}, "
                      f"p(1-sided)={rep_a['p_one']:.3f}")
        ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

    ax.set_xscale("log")
    ax.set_xlabel("FDA AI/ML-enabled device count (log scale; 0 plotted at 0.5)", fontsize=10)
    ax.set_ylabel("% Critical (Alarm + Caution)", fontsize=10)
    ax.set_title(
        "Cleared-Device Availability and Critical Stance Across Specialty/Domain Categories, 2021–2026",
        fontsize=11, fontweight="bold",
    )
    ax.grid(True, which="both", ls=":", alpha=0.4)
    fig.tight_layout(rect=[0, 0.07, 1, 1])
    fig.text(
        0.5, 0.01,
        "Point size proportional to n papers per specialty. "
        "Zero FDA-device count plotted at x=0.5 on log scale.",
        ha="center", va="bottom", fontsize=7.5, color="#444444",
    )
    out_fig = FIGURES_DIR / "specialty_aiadoption_vs_critical.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\n[5] Figure saved: {out_fig.relative_to(WORKTREE)}")


def _verdict_phrase(rep: dict) -> str:
    if rep["rho"] >= 0:
        return "does NOT support"
    return "supports" if rep["p_one"] < 0.05 else "is directionally consistent with"


def report_verdict(crit, proxy, rep_a, rep_b, fda_available) -> None:
    derm = crit.get("Dermatology", float("nan"))
    derm_proxy = proxy.get("Dermatology", float("nan"))
    median_crit = crit.median()

    if fda_available:
        sign = "NEGATIVE" if rep_a["rho"] < 0 else "POSITIVE"
        print(
            f"- FDA-device adoption vs critical: rho={rep_a['rho']:+.3f} ({sign}), "
            f"p(1-sided)={rep_a['p_one']:.4f} (perm {rep_a['p_perm_one']:.4f}); "
            f"{_verdict_phrase(rep_a)} Dan's prediction."
        )
    else:
        print("- FDA-device arm: NOT RUN (device file absent); external correlation pending.")

    sign_b = "NEGATIVE" if rep_b["rho"] < 0 else "POSITIVE"
    print(
        f"- In-corpus proxy vs critical: rho={rep_b['rho']:+.3f} ({sign_b}), "
        f"p(1-sided)={rep_b['p_one']:.4f} (perm {rep_b['p_perm_one']:.4f}); "
        f"{_verdict_phrase(rep_b)} Dan's prediction."
    )

    print(
        f"- Dermatology: critical={derm:.1f}% (corpus median {median_crit:.1f}%), "
        f"evaluative-share={derm_proxy:.1f}%."
    )
    print("\nCaveats (state in any write-up):")
    print("  * FDA panel->specialty mapping is APPROXIMATE (one panel can span buckets;")
    print("    GI/Urology, ENT, anesthesiology assignments are judgment calls).")
    print("  * FDA list is US-CENTRIC — a proxy for adoption, not a global measure.")
    print("  * In-corpus evaluative-share is PARTLY ENDOGENOUS (paper mix co-varies with")
    print("    stance). Both measures reported; do not over-claim causation.")


if __name__ == "__main__":
    main()
