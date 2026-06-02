"""Keyword composition within hallucination-flagged papers (v1).

Filters thematic_alarm.csv to papers whose `themes` field contains
'hallucination', then measures % of those papers per year that match
generative-AI vs discriminative-AI keyword groups in title+abstract.
"""
from pathlib import Path
import re

import matplotlib.pyplot as plt
import pandas as pd

# Input data lives in the parent checkout's gitignored output dir.
DATA_DIR = Path("/Users/kingslywang/repos/ai-narratives-2026/output")
THEMES_CSV = DATA_DIR / "analysis" / "thematic_alarm.csv"

# Outputs land next to the script so they can be tracked in whichever
# working tree is running it.
OUT_DIR = Path(__file__).resolve().parent / "output"
FIG_OUT = OUT_DIR / "figures" / "hallucination_keyword_composition.png"
TABLE_OUT = OUT_DIR / "analyses" / "hallucination_keyword_composition.csv"

PATTERN_GEN = re.compile(
    r"ChatGPT|GPT-?[34]?\b|\bLLM\b|\bLLMs\b|large language model|"
    r"language model|confabulat|fabricat",
    re.IGNORECASE,
)
PATTERN_DISC = re.compile(
    r"sensitiv|specificit|\bAUC\b|\bROC\b|false positive|false negative|"
    r"misclassif|area under",
    re.IGNORECASE,
)
PATTERN_GEN_SENS = re.compile(PATTERN_GEN.pattern + r"|generative", re.IGNORECASE)


def main() -> None:
    df = pd.read_csv(THEMES_CSV)
    print(f"Loaded {len(df):,} rows from {THEMES_CSV}")

    # Step 1: hallucination subset + concatenated text
    mask_hall = df["themes"].fillna("").str.contains(r"\bhallucination\b", regex=True)
    h = df.loc[mask_hall].copy()
    h["text"] = h["title"].fillna("") + " " + h["abstract"].fillna("")
    print(f"Hallucination-flagged papers: {len(h):,}")

    # Step 2: keyword flags
    h["gen_hit"] = h["text"].str.contains(PATTERN_GEN).astype(int)
    h["disc_hit"] = h["text"].str.contains(PATTERN_DISC).astype(int)
    h["gen_hit_sens"] = h["text"].str.contains(PATTERN_GEN_SENS).astype(int)

    # Step 3: yearly aggregation 2021-2026
    h = h[(h["pub_year"] >= 2021) & (h["pub_year"] <= 2026)]
    g = h.groupby("pub_year").agg(
        n=("gen_hit", "size"),
        pct_gen=("gen_hit", lambda x: 100 * x.mean()),
        pct_disc=("disc_hit", lambda x: 100 * x.mean()),
        pct_gen_sens=("gen_hit_sens", lambda x: 100 * x.mean()),
    ).reset_index()

    print("\nYearly composition (v1, hallucination-flagged):")
    print(g[["pub_year", "n", "pct_gen", "pct_disc"]].round(1).to_string(index=False))

    print("\nSensitivity check (adding bare 'generative'):")
    print(g[["pub_year", "n", "pct_gen", "pct_gen_sens"]].round(1).to_string(index=False))

    # Persist the yearly table.
    TABLE_OUT.parent.mkdir(parents=True, exist_ok=True)
    g_out = g.copy()
    for c in ("pct_gen", "pct_disc", "pct_gen_sens"):
        g_out[c] = g_out[c].round(2)
    g_out.to_csv(TABLE_OUT, index=False)
    print(f"\nSaved table:  {TABLE_OUT}")

    # Step 4: plot
    fig, ax = plt.subplots(figsize=(10, 6))
    years = g["pub_year"].tolist()
    xlabels = ["2026*" if y == 2026 else str(int(y)) for y in years]

    ax.plot(years, g["pct_gen"], "-o", color="darkorange",
            linewidth=2.2, markersize=7, label="Generative-AI keywords")
    ax.plot(years, g["pct_disc"], "-o", color="steelblue",
            linewidth=2.2, markersize=7, label="Discriminative-AI keywords")

    for x, y in zip(years, g["pct_gen"]):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=9, color="darkorange")
    for x, y in zip(years, g["pct_disc"]):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                    xytext=(0, -14), ha="center", fontsize=9, color="steelblue")

    ax.axvline(2022.5, linestyle="--", color="grey", linewidth=1)
    ax.text(2022.55, ax.get_ylim()[1] * 0.95 if False else 5,
            "ChatGPT (Nov 2022)", rotation=90, va="bottom",
            ha="left", color="grey", fontsize=9)

    ax.set_xticks(years)
    ax.set_xticklabels(xlabels)
    ax.set_xlabel("Publication year")
    ax.set_ylabel("% of hallucination-flagged papers with keyword match")
    ax.set_title("Keyword composition within hallucination-flagged papers, by year (v1)")
    ax.set_ylim(0, max(g[["pct_gen", "pct_disc"]].max()) + 12)
    ax.legend(loc="center left")
    ax.grid(True, alpha=0.3)

    # Inline n-per-year table
    table_data = [[str(int(y)), str(int(n))] for y, n in zip(g["pub_year"], g["n"])]
    tbl = ax.table(cellText=table_data,
                   colLabels=["Year", "n"],
                   colWidths=[0.07, 0.07],
                   loc="upper right",
                   cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.1)

    plt.tight_layout()
    FIG_OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIG_OUT, dpi=300, bbox_inches="tight")
    print(f"Saved figure: {FIG_OUT}")


if __name__ == "__main__":
    main()
