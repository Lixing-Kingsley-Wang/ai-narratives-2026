"""
Publication-grade world map of critical (Alarm + Caution) stance by country.

Country = first author, resolved from first_affiliation by its own local
CANON vocabulary (below) promoted to country level, plus a US-state
fallback. Per the S4-3 decision, Taiwan and Hong Kong are treated as
SEPARATE entities (analysis/extract_geography.py's region parser collapses
them into China).

Per country: n papers, critical (A+C) rate, bootstrap 95% CI (reuse
analysis.robustness.bootstrap_ci; n=1000, seed=42, percentile). Cutoff is
inclusive at n>=20; countries with 20<=n<50 are tagged low-confidence and we
report their CI widths so we can judge whether the small cutoff destabilises
the map. A second map at n>=50 is rendered for comparison.

Map: Natural Earth 110m world (light grey land), Robinson projection, one
bubble per qualifying country at its centroid, area proportional to n
(radius proportional to sqrt(n)), fill = critical rate on RdYlBu_r with a
diverging norm centered on the corpus mean (~30%). Size legend + colorbar,
no graticule.

Conventions: v1 canonical, drop FAILED, pub_year 2021-2026.

Produces:
  output/analyses/country_critical.csv
  output/figures/world_critical_map.png  / .pdf      (n>=20, primary)
  output/figures/world_critical_map_n50.png / .pdf   (n>=50, comparison)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.lines import Line2D
from pyproj import Transformer

from analysis.robustness import DATA_DIR, bootstrap_ci

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"
NE_PATH = WORKTREE / "output" / "external" / "ne_110m_admin_0_countries.geojson"

ROBINSON = "ESRI:54030"
PRIMARY_CUTOFF = 20  # inclusive cutoff for the primary map
LOW_CONF_HI = 50  # PRIMARY_CUTOFF <= n < 50 flagged low-confidence

# Canonical country name for every keyword in COUNTRY_REGION. Taiwan & Hong Kong
# overridden to separate entities (the region dict maps them to China).
CANON = {
    "usa": "United States", "united states": "United States",
    "u.s.a": "United States", "u.s.": "United States",
    "canada": "Canada", "mexico": "Mexico",
    "uk": "United Kingdom", "united kingdom": "United Kingdom",
    "england": "United Kingdom", "scotland": "United Kingdom",
    "wales": "United Kingdom", "ireland": "Ireland",
    "germany": "Germany", "france": "France", "italy": "Italy",
    "spain": "Spain", "netherlands": "Netherlands", "belgium": "Belgium",
    "switzerland": "Switzerland", "sweden": "Sweden", "norway": "Norway",
    "denmark": "Denmark", "finland": "Finland", "austria": "Austria",
    "portugal": "Portugal", "greece": "Greece", "poland": "Poland",
    "czech": "Czechia", "hungary": "Hungary", "romania": "Romania",
    "turkey": "Turkey", "israel": "Israel",
    "china": "China", "p.r. china": "China",
    "people's republic of china": "China",
    "hong kong": "Hong Kong", "taiwan": "Taiwan",
    "japan": "Japan", "south korea": "South Korea", "korea": "South Korea",
    "australia": "Australia", "new zealand": "New Zealand",
    "singapore": "Singapore", "india": "India", "thailand": "Thailand",
    "malaysia": "Malaysia", "indonesia": "Indonesia", "iran": "Iran",
    "saudi arabia": "Saudi Arabia", "egypt": "Egypt", "qatar": "Qatar",
    "uae": "United Arab Emirates", "united arab emirates": "United Arab Emirates",
    "brazil": "Brazil", "argentina": "Argentina", "chile": "Chile",
    "colombia": "Colombia", "south africa": "South Africa",
    "nigeria": "Nigeria", "kenya": "Kenya", "ethiopia": "Ethiopia",
    "ghana": "Ghana",
}

# Match specific multi-word / TW / HK keys before generic ones (e.g. China).
_MATCH_ORDER = (
    ["hong kong", "taiwan", "united arab emirates", "saudi arabia",
     "south korea", "south africa", "new zealand", "united kingdom",
     "united states", "people's republic of china", "p.r. china"]
    + [k for k in CANON if k not in (
        "hong kong", "taiwan", "united arab emirates", "saudi arabia",
        "south korea", "south africa", "new zealand", "united kingdom",
        "united states", "people's republic of china", "p.r. china")]
)

# US-state suffix fallback (from analyse_geography.assign_region).
US_STATE_SUFFIXES = [", tx", ", ca", ", ny", ", ma", ", fl",
                     ", il", ", pa", ", oh", ", nc", ", wa"]

# canonical name -> Natural Earth NAME field where they differ.
NE_NAME = {
    "United States": "United States of America",
}
# Centroids (lon, lat) for qualifying countries Natural Earth 110m lacks.
MANUAL_CENTROIDS = {
    "Hong Kong": (114.17, 22.32),
    "Singapore": (103.82, 1.35),
}


def resolve_country(aff: str) -> str | None:
    if not isinstance(aff, str) or not aff.strip():
        return None
    a = aff.lower()
    for key in _MATCH_ORDER:
        if key in a:
            return CANON[key]
    if any(s in a for s in US_STATE_SUFFIXES):
        return "United States"
    return None


def critical_rate(df: pd.DataFrame) -> float:
    return float(df["stance"].isin(["Alarm", "Caution"]).mean() * 100)


def load_country_frame() -> pd.DataFrame:
    df = pd.read_csv(
        DATA_DIR / "classified_medical_Q1Q2.csv",
        usecols=["first_affiliation", "stance", "pub_year"],
        low_memory=False,
    )
    df = df[df["stance"] != "FAILED"].copy()
    df["pub_year"] = pd.to_numeric(df["pub_year"], errors="coerce")
    df = df[(df["pub_year"] >= 2021) & (df["pub_year"] <= 2026)]
    df["country"] = df["first_affiliation"].map(resolve_country)
    return df


def build_country_table(df: pd.DataFrame) -> pd.DataFrame:
    resolved = df[df["country"].notna()].copy()
    rows = []
    for country, sub in resolved.groupby("country"):
        n = len(sub)
        if n < PRIMARY_CUTOFF:
            continue
        boot = bootstrap_ci(sub, critical_rate)  # n=1000, seed=42, 95%
        rows.append({
            "country": country,
            "n": n,
            "critical_pct": boot["point"],
            "ci_lo": boot["lower"],
            "ci_hi": boot["upper"],
            "ci_width": boot["upper"] - boot["lower"],
            "low_conf_flag": PRIMARY_CUTOFF <= n < LOW_CONF_HI,
        })
    out = pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)
    return out


# ---------------------------------------------------------------------------
# geometry / centroids
# ---------------------------------------------------------------------------


def load_world_robinson() -> gpd.GeoDataFrame:
    w = gpd.read_file(NE_PATH)
    w = w[w["NAME"] != "Antarctica"].copy()
    return w.to_crs(ROBINSON)


def centroid_lookup(world: gpd.GeoDataFrame) -> dict[str, tuple[float, float]]:
    """canonical country -> (x, y) in Robinson coords."""
    by_ne = {row["NAME"]: row.geometry.representative_point()
             for _, row in world.iterrows()}
    transformer = Transformer.from_crs("EPSG:4326", ROBINSON, always_xy=True)
    out = {}
    for canon in set(CANON.values()):
        ne = NE_NAME.get(canon, canon)
        if ne in by_ne:
            p = by_ne[ne]
            out[canon] = (p.x, p.y)
        elif canon in MANUAL_CENTROIDS:
            lon, lat = MANUAL_CENTROIDS[canon]
            out[canon] = transformer.transform(lon, lat)
    return out


# ---------------------------------------------------------------------------
# map
# ---------------------------------------------------------------------------

SIZE_SCALE = 0.9   # scatter area = SIZE_SCALE * n  (=> radius ∝ sqrt(n))
LEGEND_NS = [50, 200, 1000, 4000]


def render_map(table: pd.DataFrame, world: gpd.GeoDataFrame,
               centroids: dict, cutoff: int, norm: TwoSlopeNorm,
               cmap, out_stem: str) -> tuple[int, list[str]]:
    sel = table[table["n"] >= cutoff].copy()
    placed, missing = [], []
    xs, ys, ss, cs = [], [], [], []
    for _, r in sel.iterrows():
        c = r["country"]
        if c not in centroids:
            missing.append(c)
            continue
        x, y = centroids[c]
        xs.append(x); ys.append(y)
        ss.append(SIZE_SCALE * r["n"])
        cs.append(r["critical_pct"])
        placed.append(c)

    fig, ax = plt.subplots(figsize=(16, 8.5))
    world.plot(ax=ax, color="#e6e6e6", edgecolor="white", linewidth=0.4, zorder=1)

    sc = ax.scatter(xs, ys, s=ss, c=cs, cmap=cmap, norm=norm,
                    edgecolor="#333", linewidth=0.5, alpha=0.92, zorder=3)

    ax.set_axis_off()
    ax.set_xlim(world.total_bounds[0] * 1.02, world.total_bounds[2] * 1.02)

    # colorbar
    cbar = fig.colorbar(sc, ax=ax, fraction=0.026, pad=0.01,
                        orientation="vertical", extend="both")
    cbar.set_label("Critical stance — Alarm + Caution (%)", fontsize=10)

    # size legend (radius ∝ sqrt(n))
    handles = [
        Line2D([0], [0], marker="o", color="none",
               markerfacecolor="#bbb", markeredgecolor="#333",
               markersize=np.sqrt(SIZE_SCALE * n) * 2 / np.sqrt(np.pi),
               label=f"{n:,}")
        for n in LEGEND_NS
    ]
    leg = ax.legend(handles=handles, title="n papers", loc="lower left",
                    labelspacing=1.6, borderpad=1.1, frameon=True,
                    framealpha=0.9, fontsize=9, title_fontsize=10)
    ax.add_artist(leg)

    n_low = int(table[(table["n"] >= cutoff) & (table["low_conf_flag"])].shape[0]) \
        if cutoff < LOW_CONF_HI else 0
    note = (f"First-author country (n≥{cutoff}); {len(placed)} countries; "
            f"bubble area ∝ n, colour = % critical; Robinson projection. "
            f"Q1/Q2 medical, 2021–2026.")
    if cutoff < LOW_CONF_HI:
        note += f"  {n_low} low-confidence ({cutoff}≤n<{LOW_CONF_HI}) outlined."
    ax.set_title("Critical stance toward clinical AI by country",
                 fontsize=15, fontweight="bold", loc="left")
    ax.text(0, -0.02, note, transform=ax.transAxes, fontsize=9, color="#444",
            va="top")

    # outline low-confidence bubbles a bit heavier so they're visible
    if cutoff < LOW_CONF_HI:
        lx, ly, lsz = [], [], []
        for _, r in sel[sel["low_conf_flag"]].iterrows():
            if r["country"] in centroids:
                x, y = centroids[r["country"]]
                lx.append(x); ly.append(y); lsz.append(SIZE_SCALE * r["n"])
        ax.scatter(lx, ly, s=lsz, facecolor="none", edgecolor="black",
                   linewidth=1.6, linestyle=(0, (2, 1)), zorder=4)

    fig.tight_layout()
    png = FIGURES_DIR / f"{out_stem}.png"
    pdf = FIGURES_DIR / f"{out_stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")  # vector
    plt.close(fig)
    return len(placed), missing


def main() -> None:
    ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("World map of critical stance by first-author country (S4-3)")
    print("=" * 72)

    df = load_country_frame()
    n_all = len(df)
    n_res = int(df["country"].notna().sum())
    print(f"Papers (FAILED dropped, 2021–2026): {n_all:,}")
    print(f"Resolved to a country: {n_res:,} ({n_res / n_all * 100:.1f}%); "
          f"unknown {n_all - n_res:,} (excluded from map)")

    table = build_country_table(df)
    out_csv = ANALYSES_DIR / "country_critical.csv"
    table.to_csv(out_csv, index=False)
    print(f"\nCountries n≥{PRIMARY_CUTOFF}: {len(table)} | n≥50: {(table['n'] >= 50).sum()}")
    print(f"Saved table: {out_csv.relative_to(WORKTREE)}")

    # low-confidence band CI widths vs the rest
    low = table[table["low_conf_flag"]]
    hi = table[~table["low_conf_flag"]]
    print(f"\nLow-confidence band ({PRIMARY_CUTOFF}≤n<{LOW_CONF_HI}):")
    for _, r in low.iterrows():
        print(f"  {r['country']:<14} n={r['n']:<4} {r['critical_pct']:.1f}% "
              f"CI[{r['ci_lo']:.1f}, {r['ci_hi']:.1f}]  width={r['ci_width']:.1f}pp")
    print(f"  mean CI width  low-conf={low['ci_width'].mean():.1f}pp  "
          f"vs n≥50={hi['ci_width'].mean():.1f}pp")

    # colour norm centered on the corpus mean (~30%)
    corpus_mean = critical_rate(df[df["country"].notna()])
    vmin = float(np.floor(table["critical_pct"].min() / 5) * 5)
    vmax = float(np.ceil(table["critical_pct"].max() / 5) * 5)
    norm = TwoSlopeNorm(vmin=vmin, vcenter=corpus_mean, vmax=vmax)
    cmap = plt.get_cmap("RdYlBu_r")
    print(f"\nColour norm: vmin={vmin}, vcenter(corpus mean)={corpus_mean:.1f}, vmax={vmax}")

    world = load_world_robinson()
    centroids = centroid_lookup(world)

    print("\nRendering maps:")
    n30, miss30 = render_map(table, world, centroids, PRIMARY_CUTOFF, norm, cmap,
                             "world_critical_map")
    n50, miss50 = render_map(table, world, centroids, 50, norm, cmap,
                             "world_critical_map_n50")
    for miss in set(miss30 + miss50):
        print(f"  ! no geometry/centroid for qualifying country: {miss!r}")
    print(f"  n≥{PRIMARY_CUTOFF} map: {n30} countries -> world_critical_map.png/.pdf")
    print(f"  n≥50 map: {n50} countries -> world_critical_map_n50.png/.pdf")

    # step 6 comparison
    dropped = sorted(set(table[table["n"] >= PRIMARY_CUTOFF]["country"]) -
                     set(table[table["n"] >= 50]["country"]))
    print(f"\n[6] Cutoff comparison n≥{PRIMARY_CUTOFF} vs n≥50")
    print("-" * 72)
    dropped_desc = ", ".join(
        f"{c} (n={int(table.loc[table['country'] == c, 'n'].iloc[0])})"
        for c in dropped
    ) or "none"
    print(f"  n≥{PRIMARY_CUTOFF}: {len(table)} countries; n≥50: {(table['n'] >= 50).sum()} "
          f"countries; difference: {len(dropped)} ({dropped_desc}).")
    print("  The dropped countries are exactly the low-confidence band, with the")
    print("  widest CIs; removing them leaves every other high-n bubble unchanged.")


if __name__ == "__main__":
    main()
