"""
Theme trends: absolute COUNT vs RATE over time (denominator-dilution test).

Question (S4-2): is the 'regulation' theme genuinely declining in ABSOLUTE
terms, or is its RATE falling only because hallucination / patient-safety
exploded and inflated the per-year A+C denominator (the same denominator
artifact as the 2024 alarm peak)?

Method: load the A+C (Alarm + Caution) subset with theme labels, explode the
multi-theme `themes` field to one row per (paper, theme), then for every
theme x pub_year compute both the absolute count of flagged papers and the
rate (% of that year's A+C papers). The per-year A+C total is emitted as an
explicit denominator column so the dilution is visible. Spearman over years on
the COUNT (not rate) tells us whether a theme falls / is flat / rises in
absolute terms; the rate trend can diverge when the denominator grows.

2026 is a PARTIAL year (study window ends ~Apr 2026), so its absolute counts
are deflated for every theme. The count Spearman is therefore reported over
2021-2026 (as requested) AND over 2021-2025 (full years) as a sensitivity.

Conventions: v1 canonical, pub_year 2021-2026, A+C subset already FAILED-free.
Reuses analysis/robustness.py for the THEMES_PATH constant.

Produces:
  output/analyses/theme_count_vs_rate.csv
  output/figures/theme_regulation_ethics_dual.png   (focused dual view)
  output/figures/theme_count_vs_rate.png            (10-theme small multiples)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from analysis.robustness import THEMES_PATH

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"

YEARS = [2021, 2022, 2023, 2024, 2025, 2026]
PARTIAL_YEAR = 2026  # study window ends ~Apr 2026; counts deflated.

# Canonical 10-theme list (classify_themes.py:26-28).
CANONICAL_THEMES = [
    "replacement",
    "hallucination",
    "safety_clinical",
    "ethics_bias",
    "cognitive",
    "education",
    "regulation",
    "existential",
    "data_privacy",
    "other",
]

FOCUS = ["regulation", "ethics_bias"]  # the two declining abstract themes

DELIM_CANDIDATES = ["|", ";", ",", "/", "+"]


def detect_delimiter(series: pd.Series) -> str:
    """Pick the delimiter that appears most across the themes field."""
    sample = series.dropna().astype(str)
    totals = {d: int(sample.str.count(rf"\{d}").sum()) for d in DELIM_CANDIDATES}
    best = max(totals, key=totals.get)
    if totals[best] == 0:
        # single-theme-per-row; any delimiter is a no-op split.
        best = "|"
    print(f"  delimiter detection (occurrences): {totals} -> using {best!r}")
    return best


def load_exploded() -> tuple[pd.DataFrame, pd.Series]:
    """Return (exploded one-row-per-(paper,theme), per-year A+C denominator)."""
    df = pd.read_csv(THEMES_PATH, usecols=["pmid", "pub_year", "stance", "themes"],
                     low_memory=False)
    df["pub_year"] = pd.to_numeric(df["pub_year"], errors="coerce").astype("Int64")
    df = df[df["pub_year"].isin(YEARS)].copy()
    print(f"  A+C subset: {len(df):,} papers; stances: "
          f"{dict(df['stance'].value_counts())}")

    denom = df["pub_year"].value_counts().reindex(YEARS).fillna(0).astype(int)

    delim = detect_delimiter(df["themes"])
    df["theme_list"] = (
        df["themes"].fillna("").astype(str).str.split(rf"\{delim}", regex=True)
    )
    ex = df.explode("theme_list")
    ex["theme"] = ex["theme_list"].str.strip()
    ex = ex[ex["theme"] != ""]

    # Guard: every token must be a canonical theme.
    seen = set(ex["theme"].unique())
    unknown = seen - set(CANONICAL_THEMES)
    if unknown:
        print(f"  ! non-canonical theme tokens found (dropped): {sorted(unknown)}")
        ex = ex[ex["theme"].isin(CANONICAL_THEMES)]

    # A paper tagged with the same theme twice would double-count; dedupe.
    ex = ex.drop_duplicates(subset=["pmid", "theme"])
    return ex, denom


def build_count_rate_table(ex: pd.DataFrame, denom: pd.Series) -> pd.DataFrame:
    """Long table: theme x year x {count, rate_pct, denominator}."""
    counts = (
        ex.groupby(["theme", "pub_year"]).size()
        .unstack(fill_value=0)
        .reindex(index=CANONICAL_THEMES, columns=YEARS, fill_value=0)
    )
    rows = []
    for theme in CANONICAL_THEMES:
        for y in YEARS:
            c = int(counts.loc[theme, y])
            d = int(denom[y])
            rows.append(
                {
                    "theme": theme,
                    "pub_year": y,
                    "count": c,
                    "rate_pct": (100.0 * c / d) if d else 0.0,
                    "ac_denominator": d,
                    "partial_year": y == PARTIAL_YEAR,
                }
            )
    return pd.DataFrame(rows)


def classify_trend(rho: float, p: float) -> str:
    if rho <= -0.5:
        return "FALL"
    if rho >= 0.5:
        return "RISE"
    return "flat"


def spearman_counts(table: pd.DataFrame, years: list[int]) -> dict:
    """Per-theme Spearman of count vs year over the given years."""
    out = {}
    for theme in CANONICAL_THEMES:
        sub = table[(table["theme"] == theme) & (table["pub_year"].isin(years))]
        sub = sub.sort_values("pub_year")
        c = sub["count"].values.astype(float)
        if np.ptp(c) == 0:
            rho, p = 0.0, 1.0
        else:
            rho, p = spearmanr(sub["pub_year"].values, c)
        out[theme] = {"rho": float(rho), "p": float(p),
                      "trend": classify_trend(float(rho), float(p)),
                      "first": int(c[0]), "last": int(c[-1]),
                      "peak": int(c.max())}
    return out


def main() -> None:
    ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("Theme COUNT vs RATE over time — denominator-dilution test (S4-2)")
    print("=" * 72)

    print("\n[1] Load A+C subset, auto-detect delimiter, explode to (paper, theme)")
    print("-" * 72)
    ex, denom = load_exploded()
    print(f"  exploded rows (paper x theme): {len(ex):,}")
    print("  per-year A+C denominator (total critical papers/year):")
    for y in YEARS:
        tag = "  <-- PARTIAL YEAR" if y == PARTIAL_YEAR else ""
        print(f"    {y}: {denom[y]:>5,}{tag}")

    print("\n[2] theme x year -> count, rate (% of A+C that year), denominator")
    print("-" * 72)
    table = build_count_rate_table(ex, denom)
    out_csv = ANALYSES_DIR / "theme_count_vs_rate.csv"
    table.to_csv(out_csv, index=False)
    print(f"  saved table: {out_csv.relative_to(WORKTREE)}")

    # Pretty per-focus-theme print of count and rate trajectories.
    for theme in FOCUS:
        sub = table[table["theme"] == theme].sort_values("pub_year")
        cs = "  ".join(f"{y}:{int(r['count'])}" for y, r in
                       zip(sub["pub_year"], sub.to_dict("records")))
        rs = "  ".join(f"{y}:{r['rate_pct']:.1f}%" for y, r in
                       zip(sub["pub_year"], sub.to_dict("records")))
        print(f"  [{theme}] count  {cs}")
        print(f"  [{theme}] rate   {rs}")

    print("\n[3] Spearman over years on COUNT (Dan's absolute-decline test)")
    print("    trend rule: rho<=-0.5 FALL, >=+0.5 RISE, else flat")
    print("-" * 72)
    sp_all = spearman_counts(table, YEARS)
    sp_full = spearman_counts(table, [2021, 2022, 2023, 2024, 2025])
    print(f"  {'theme':<16}{'count 21->26':<16}{'peak':<7}"
          f"{'rho(21-26)':<12}{'trend':<7}{'rho(21-25)':<12}{'trend25':<7}")
    # rank themes by 2021-26 count rho ascending (most-declining first)
    for theme in sorted(CANONICAL_THEMES, key=lambda t: sp_all[t]["rho"]):
        a, f = sp_all[theme], sp_full[theme]
        traj = f"{a['first']}->{a['last']}"
        print(f"  {theme:<16}{traj:<16}{a['peak']:<7}"
              f"{a['rho']:+.2f} (p={a['p']:.2f}) {a['trend']:<7}"
              f"{f['rho']:+.2f}      {f['trend']:<7}")

    print("\n[4] Figures")
    print("-" * 72)
    make_focus_figure(table, sp_all, sp_full)
    make_small_multiples(table, sp_all)

    print("\n[5/6] Verdict — rate decline: real absolute decline vs dilution?")
    print("-" * 72)
    report_verdict(table, sp_all, sp_full, denom)


# ---------------------------------------------------------------------------
# figures
# ---------------------------------------------------------------------------

FOCUS_COLORS = {"regulation": "#C0392B", "ethics_bias": "#2C7FB8"}


def _mark_partial(ax, years):
    """Shade the partial-year region so deflated counts are not over-read."""
    if PARTIAL_YEAR in years:
        ax.axvspan(PARTIAL_YEAR - 0.5, PARTIAL_YEAR + 0.5, color="#bbb",
                   alpha=0.18, zorder=0)


def make_focus_figure(table, sp_all, sp_full) -> None:
    fig, (axc, axr) = plt.subplots(1, 2, figsize=(13, 5.2))

    # Left: absolute count, with the A+C denominator on a secondary axis.
    for theme in FOCUS:
        sub = table[table["theme"] == theme].sort_values("pub_year")
        axc.plot(sub["pub_year"], sub["count"], "-o", color=FOCUS_COLORS[theme],
                 lw=2, label=f"{theme} (count)")
    denom_sub = (table[table["theme"] == "regulation"]
                 .sort_values("pub_year"))
    ax2 = axc.twinx()
    ax2.plot(denom_sub["pub_year"], denom_sub["ac_denominator"], "--",
             color="#777", lw=1.6, label="A+C denominator (all critical papers)")
    ax2.set_ylabel("A+C papers that year (denominator)", color="#555", fontsize=9)
    ax2.tick_params(axis="y", labelcolor="#555")
    _mark_partial(axc, YEARS)
    axc.set_title("Absolute COUNT of flagged papers per year", fontsize=11,
                  fontweight="bold")
    axc.set_xlabel("Publication year")
    axc.set_ylabel("Flagged-paper count")
    axc.set_xticks(YEARS)
    # combined legend
    h1, l1 = axc.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    axc.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5, framealpha=0.9)

    # Right: rate (% of that year's A+C papers).
    for theme in FOCUS:
        sub = table[table["theme"] == theme].sort_values("pub_year")
        axr.plot(sub["pub_year"], sub["rate_pct"], "-o", color=FOCUS_COLORS[theme],
                 lw=2, label=f"{theme} (rate)")
    _mark_partial(axr, YEARS)
    axr.set_title("RATE: % of that year's A+C papers", fontsize=11,
                  fontweight="bold")
    axr.set_xlabel("Publication year")
    axr.set_ylabel("% of A+C papers")
    axr.set_xticks(YEARS)
    axr.legend(loc="upper right", fontsize=9, framealpha=0.9)

    reg = sp_all["regulation"]
    fig.suptitle(
        "Regulation & ethics_bias: absolute count vs rate "
        f"(regulation count rho 21-26={reg['rho']:+.2f}, "
        f"21-25={sp_full['regulation']['rho']:+.2f}; shaded 2026 = partial year)",
        fontsize=11, fontweight="bold",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = FIGURES_DIR / "theme_regulation_ethics_dual.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  (a) focused dual view: {out.relative_to(WORKTREE)}")


def make_small_multiples(table, sp_all) -> None:
    fig, axes = plt.subplots(2, 5, figsize=(18, 7.2), sharex=True)
    # order panels by count-trend rho ascending (most declining first)
    order = sorted(CANONICAL_THEMES, key=lambda t: sp_all[t]["rho"])
    for ax, theme in zip(axes.flat, order):
        sub = table[table["theme"] == theme].sort_values("pub_year")
        ax.bar(sub["pub_year"], sub["count"], color="#2C7FB8", alpha=0.45,
               label="count")
        ax.set_ylabel("count", color="#2C7FB8", fontsize=8)
        ax.tick_params(axis="y", labelcolor="#2C7FB8")
        axr = ax.twinx()
        axr.plot(sub["pub_year"], sub["rate_pct"], "-o", color="#C0392B", lw=1.8,
                 ms=4, label="rate")
        axr.set_ylabel("rate %", color="#C0392B", fontsize=8)
        axr.tick_params(axis="y", labelcolor="#C0392B")
        _mark_partial(ax, YEARS)
        sp = sp_all[theme]
        ax.set_title(f"{theme}\ncount rho={sp['rho']:+.2f} [{sp['trend']}]",
                     fontsize=9.5, fontweight="bold")
        ax.set_xticks(YEARS)
        ax.tick_params(axis="x", labelrotation=45, labelsize=7)
    fig.suptitle(
        "Per-theme COUNT (bars) vs RATE (line) over 2021-2026  "
        "— shaded 2026 = partial year; panels ordered by count-trend",
        fontsize=12, fontweight="bold",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = FIGURES_DIR / "theme_count_vs_rate.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  (b) 10-theme small multiples: {out.relative_to(WORKTREE)}")


# ---------------------------------------------------------------------------
# verdict
# ---------------------------------------------------------------------------


def report_verdict(table, sp_all, sp_full, denom) -> None:
    denom_growth = denom[2025] / denom[2021]
    print(f"  Denominator grew {denom[2021]} (2021) -> {denom[2025]} (2025) "
          f"= {denom_growth:.1f}x  (hallucination/safety inflate this).")

    def verdict_for(theme: str) -> str:
        a, f = sp_all[theme], sp_full[theme]
        # Rate trend sign (peak-to-2025, robust to partial 2026).
        sub = table[table["theme"] == theme].sort_values("pub_year")
        rate25 = sub[sub["pub_year"] == 2025]["rate_pct"].iloc[0]
        rate_peak = sub["rate_pct"].max()
        rate_falling = rate25 < rate_peak - 1.0
        # Absolute trend: trust full-year (2021-25) Spearman to avoid 2026 bias.
        if f["rho"] >= 0.5:
            absol = "RISING in absolute count"
        elif f["rho"] <= -0.5:
            absol = "FALLING in absolute count"
        else:
            absol = "roughly FLAT in absolute count"
        if not rate_falling:
            return f"rate not clearly falling; {absol}."
        if "RISING" in absol or "FLAT" in absol:
            return (f"rate falls but count is {absol.split(' in')[0].lower()} "
                    f"=> DILUTION, not real decline.")
        return "rate AND count both fall => REAL absolute decline."

    for theme in FOCUS:
        a, f = sp_all[theme], sp_full[theme]
        sub = table[table["theme"] == theme].sort_values("pub_year")
        c21 = sub[sub["pub_year"] == 2021]["count"].iloc[0]
        c25 = sub[sub["pub_year"] == 2025]["count"].iloc[0]
        print(f"\n  >> {theme.upper()}")
        print(f"     count 2021={c21} -> 2025={c25} (peak {a['peak']}); "
              f"Spearman count rho 21-25={f['rho']:+.2f}, 21-26={a['rho']:+.2f}")
        print(f"     VERDICT: {verdict_for(theme)}")

    # Explicit headline for regulation.
    reg_v = verdict_for("regulation")
    print("\n  " + "=" * 60)
    print(f"  REGULATION HEADLINE: {reg_v}")
    print("  " + "=" * 60)

    print("\n  Caveats:")
    print("   * 2026 is a PARTIAL year — absolute counts deflated; verdict leans")
    print("     on the 2021-2025 full-year count trend, not the 2026 dip.")
    print("   * Multi-label themes: a paper can carry several themes, so theme")
    print("     counts sum to more than the A+C denominator (rates are per-theme).")


if __name__ == "__main__":
    main()
