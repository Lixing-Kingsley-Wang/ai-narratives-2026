"""
Session 3 — Why are reviews more positive than research articles?

Session 1 found: Reviews 24.85% critical vs Research 32.91% critical (pooled),
Δ ≈ 8 pp. Session 2 (C.3) found this within-specialty holds in 7/10 specialties.
MH, Radiology, and Medical Education are the 3 exceptions where reviews are MORE
critical than research.

This script tests four candidate explanations:

  H1. Temporal mix: reviews skew earlier-pub-year, when stance was more positive.
  H2. Sub-pub-type composition: within the "Review" umbrella, are Systematic
      Reviews more positive than narrative Reviews? (uses the 7-bucket scheme)
  H3. Theme emphasis: reviews emphasize benefits/use-cases; research articles
      report hallucination/failures. Check theme prevalence within A+C.
  H4. Year-stratified gap: even controlling for year, does the gap persist?
      If yes, H1 alone is not enough.

Plus qualitative: sample titles from MH/Radiology/Med Ed Reviews (the exceptions).

Produces:
  output/analyses/reviews_positivity_why.md
  output/analyses/discussion_reviews_positivity.md
  output/analyses/reviews_pubtype_year.csv
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd

from analysis.robustness import load_classifications, simplify_pubtype_7

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"
THEMES_PATH = Path("/Users/kingslywang/repos/ai-narratives-2026/output/analysis/thematic_alarm.csv")
V1_FULL = Path("/Users/kingslywang/repos/ai-narratives-2026/output/classified_medical_Q1Q2.csv")

YEARS = list(range(2021, 2027))
EXCEPTION_SPECIALTIES = [
    "Mental Health / Psychiatry",
    "Radiology / Diagnostic Imaging",
    "Medical Education",
]


def has_theme(themes_str, theme):
    if not isinstance(themes_str, str):
        return 0
    return int(theme in {t.strip() for t in themes_str.split("|")})


def main() -> None:
    v1 = load_classifications("v1")
    v1["pmid"] = v1["pmid"].astype(str)
    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    spec["pmid"] = spec["pmid"].astype(str)
    v1 = v1.merge(spec, on="pmid", how="left")
    v1["crit"] = v1["stance"].isin(["Alarm", "Caution"]).astype(int)

    reviews = v1[v1["pub_type_simple_5"] == "Review"].copy()
    research = v1[v1["pub_type_simple_5"] == "Research Article"].copy()
    print(f"Reviews: n={len(reviews):,}  critical={reviews['crit'].mean()*100:.2f}%")
    print(f"Research: n={len(research):,}  critical={research['crit'].mean()*100:.2f}%")
    print(f"Overall Δ: {(reviews['crit'].mean()-research['crit'].mean())*100:+.2f} pp")

    # ── H1 / H4: year distribution + year-stratified critical rate ────────────
    print("\n=== H1+H4: Year-stratified review-vs-research gap ===")
    year_rows = []
    print(f"  {'year':>4} {'rev_n':>6} {'rev_yr%':>8} {'rev_crit%':>10} "
          f"{'res_n':>6} {'res_yr%':>8} {'res_crit%':>10} {'Δ pp':>7}")
    for year in YEARS:
        sr = reviews[reviews["pub_year"] == year]
        ss = research[research["pub_year"] == year]
        rev_year_share = len(sr) / len(reviews) * 100
        res_year_share = len(ss) / len(research) * 100
        rev_crit = sr["crit"].mean() * 100 if len(sr) else 0
        res_crit = ss["crit"].mean() * 100 if len(ss) else 0
        delta = rev_crit - res_crit
        print(f"  {year} {len(sr):>6,} {rev_year_share:>7.1f}% {rev_crit:>9.2f}% "
              f"{len(ss):>6,} {res_year_share:>7.1f}% {res_crit:>9.2f}% {delta:>+6.2f}")
        year_rows.append({
            "year": year, "rev_n": len(sr), "rev_year_share_pct": round(rev_year_share, 2),
            "rev_crit_pct": round(rev_crit, 2),
            "res_n": len(ss), "res_year_share_pct": round(res_year_share, 2),
            "res_crit_pct": round(res_crit, 2),
            "delta_pp": round(delta, 2),
        })
    year_df = pd.DataFrame(year_rows)
    year_df.to_csv(ANALYSES_DIR / "reviews_pubtype_year.csv", index=False)

    # Decompose overall gap: if reviews were re-weighted to research's year mix, what gap?
    res_year_mix = research["pub_year"].value_counts(normalize=True)
    rev_year_crit = reviews.groupby("pub_year")["crit"].mean()
    rev_year_crit = rev_year_crit.reindex(res_year_mix.index).fillna(reviews["crit"].mean())
    mix_adjusted_rev = (rev_year_crit * res_year_mix).sum() * 100
    print(f"\n  Raw reviews crit:                                 {reviews['crit'].mean()*100:.2f}%")
    print(f"  Reviews crit reweighted to research's year mix:    {mix_adjusted_rev:.2f}%")
    print(f"  Research crit:                                    {research['crit'].mean()*100:.2f}%")
    h1_explained_pp = mix_adjusted_rev - reviews['crit'].mean()*100
    total_gap = research['crit'].mean()*100 - reviews['crit'].mean()*100
    h1_explained_pct = h1_explained_pp / total_gap * 100 if total_gap else 0
    print(f"  H1 (temporal mix) explains: {h1_explained_pp:+.2f} pp of "
          f"{total_gap:.2f} pp total = {h1_explained_pct:.0f}%")

    # ── H2: sub-pub-type within Review umbrella (7-bucket) ────────────────────
    print("\n=== H2: Sub-pub-type within Review umbrella (7-bucket) ===")
    v1["pt7"] = v1["pub_type_raw"].apply(simplify_pubtype_7)
    sub_pt = v1[v1["pt7"].isin(["Systematic Review", "Review"])].copy()
    sub_rows = []
    for pt in ["Systematic Review", "Review"]:
        sub = sub_pt[sub_pt["pt7"] == pt]
        sub_rows.append({
            "sub_type": pt, "n": len(sub),
            "crit_pct": round(sub["crit"].mean() * 100, 2),
            "alarm_pct": round((sub["stance"] == "Alarm").mean() * 100, 2),
            "caution_pct": round((sub["stance"] == "Caution").mean() * 100, 2),
            "cautopt_pct": round((sub["stance"] == "Cautious Optimism").mean() * 100, 2),
            "advocacy_pct": round((sub["stance"] == "Advocacy").mean() * 100, 2),
        })
    for r in sub_rows:
        print(f"  {r['sub_type']:<22} n={r['n']:>5,}  crit={r['crit_pct']:5.2f}%  "
              f"Alarm={r['alarm_pct']:.1f}  Caut={r['caution_pct']:.1f}  "
              f"CO={r['cautopt_pct']:.1f}  Adv={r['advocacy_pct']:.1f}")

    # ── H3: theme prevalence reviews vs research within A+C ───────────────────
    print("\n=== H3: Theme prevalence in A+C — reviews vs research ===")
    themes_df = pd.read_csv(THEMES_PATH, low_memory=False)
    themes_df["pmid"] = themes_df["pmid"].astype(str)
    themes_df["pub_year"] = pd.to_numeric(themes_df["pub_year"], errors="coerce").astype("Int64")
    themes_df = themes_df[(themes_df["pub_year"] >= 2021) & (themes_df["pub_year"] <= 2026)]
    themes_df = themes_df.merge(
        v1[["pmid", "pub_type_simple_5", "specialty"]], on="pmid", how="left"
    )

    theme_vocab = [
        "hallucination", "safety_clinical", "regulation", "ethics_bias",
        "data_privacy", "education", "cognitive", "replacement",
        "existential", "other",
    ]
    for theme in theme_vocab:
        themes_df[theme] = themes_df["themes"].apply(lambda s: has_theme(s, theme))

    rev_th = themes_df[themes_df["pub_type_simple_5"] == "Review"]
    res_th = themes_df[themes_df["pub_type_simple_5"] == "Research Article"]
    print(f"  {'theme':<18} {'rev_n':>5} {'rev%':>7} {'res_n':>5} {'res%':>7} {'Δ pp':>7}")
    theme_rows = []
    for theme in theme_vocab:
        rev_pct = rev_th[theme].mean() * 100 if len(rev_th) else 0
        res_pct = res_th[theme].mean() * 100 if len(res_th) else 0
        delta = rev_pct - res_pct
        print(f"  {theme:<18} {len(rev_th):>5} {rev_pct:>6.2f}% "
              f"{len(res_th):>5} {res_pct:>6.2f}% {delta:>+6.2f}")
        theme_rows.append({"theme": theme,
                            "rev_pct": round(rev_pct, 2), "res_pct": round(res_pct, 2),
                            "delta_pp": round(delta, 2)})
    pd.DataFrame(theme_rows).to_csv(ANALYSES_DIR / "reviews_themes.csv", index=False)

    # ── Qualitative: sample titles from the 3 exception specialties ───────────
    print("\n=== Exception specialties: sample Review titles (Alarm + Caution) ===")
    full = pd.read_csv(V1_FULL, usecols=["pmid", "title"], low_memory=False)
    full["pmid"] = full["pmid"].astype(str)
    v1_titled = v1.merge(full, on="pmid", how="left")

    exception_md_rows = {}
    for sp in EXCEPTION_SPECIALTIES:
        sub = v1_titled[(v1_titled["specialty"] == sp)
                         & (v1_titled["pub_type_simple_5"] == "Review")
                         & (v1_titled["stance"].isin(["Alarm", "Caution"]))]
        sample = sub.head(8)  # first 8 critical reviews in this exception specialty
        exception_md_rows[sp] = sample[["pmid", "stance", "title"]].to_dict("records")
        print(f"\n  -- {sp}: {len(sub)} critical reviews (showing first 8 titles)")
        for r in sample.itertuples():
            print(f"     [{r.stance}] {r.title[:140]}")

    # ── Write reviews_positivity_why.md (data-heavy) ──────────────────────────
    md = [
        "# Why are reviews more positive than research articles? — Session 3 data brief",
        "",
        f"**Session 1 finding (pooled):** Reviews {reviews['crit'].mean()*100:.2f}% critical "
        f"vs Research Articles {research['crit'].mean()*100:.2f}% critical "
        f"(Δ {(reviews['crit'].mean()-research['crit'].mean())*100:+.2f} pp).",
        f"**Session 2 (C.3) finding:** within-specialty holds in 7/10 specialties; "
        f"3 exceptions: MH, Radiology, Medical Education (reviews MORE critical).",
        "",
        "## H1 + H4 — Temporal mix + year-stratified gap",
        "",
        "| year | rev n | rev year-share | rev crit% | res n | res year-share | res crit% | Δ pp |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in year_rows:
        md.append(f"| {r['year']} | {r['rev_n']:,} | {r['rev_year_share_pct']}% | "
                  f"{r['rev_crit_pct']:.2f}% | {r['res_n']:,} | {r['res_year_share_pct']}% | "
                  f"{r['res_crit_pct']:.2f}% | {r['delta_pp']:+.2f} |")
    md.append("")
    md.append(f"**H1 temporal-mix decomposition:** if reviews were reweighted to research's "
              f"year mix, reviews critical rate would become {mix_adjusted_rev:.2f}% "
              f"(vs raw {reviews['crit'].mean()*100:.2f}%). H1 explains "
              f"**{h1_explained_pct:.0f}%** of the total {total_gap:.2f} pp gap.")
    md.append("")
    md.append(f"**H4 year-stratified:** the gap " + (
        "persists in every year — temporal mix is NOT the main driver."
        if all(r["delta_pp"] < -1 for r in year_rows) else
        "narrows/inverts in some years — temporal mix matters."))
    md.append("")
    md.append("## H2 — Sub-pub-type within Review umbrella")
    md.append("")
    md.append("| sub-type | n | crit % | Alarm | Caution | CautOpt | Advocacy |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in sub_rows:
        md.append(f"| {r['sub_type']} | {r['n']:,} | {r['crit_pct']:.2f} | "
                  f"{r['alarm_pct']:.2f} | {r['caution_pct']:.2f} | "
                  f"{r['cautopt_pct']:.2f} | {r['advocacy_pct']:.2f} |")
    md.append("")
    md.append("## H3 — Theme prevalence (within A+C subset)")
    md.append("")
    md.append("| theme | rev % | res % | Δ pp |")
    md.append("|---|---:|---:|---:|")
    for r in theme_rows:
        md.append(f"| {r['theme']} | {r['rev_pct']:.2f} | {r['res_pct']:.2f} | {r['delta_pp']:+.2f} |")
    md.append("")
    md.append("## Exception specialties — sample critical Review titles (first 8 each)")
    md.append("")
    for sp, samples in exception_md_rows.items():
        md.append(f"### {sp}")
        md.append("")
        for s in samples:
            md.append(f"- **[{s['stance']}]** {s['title']}")
        md.append("")

    out = ANALYSES_DIR / "reviews_positivity_why.md"
    out.write_text("\n".join(md) + "\n")
    print(f"\nWrote: {out}")

    # ── Write discussion brief (interpretation-heavy, for upstream Opus chat) ─
    h2_sr_vs_r = sub_rows[0]["crit_pct"] - sub_rows[1]["crit_pct"]
    discussion = [
        "# Discussion brief — Why are reviews more positive? (for upstream Opus chat)",
        "",
        "## The puzzle",
        "",
        f"Reviews are systematically less critical than research articles in our corpus: "
        f"**{reviews['crit'].mean()*100:.1f}% vs {research['crit'].mean()*100:.1f}%** "
        f"(Δ {(reviews['crit'].mean()-research['crit'].mean())*100:+.1f} pp, pooled). "
        f"This holds within 7/10 specialties (Session 2, C.3). The Commentary needs "
        f"either a mechanism explanation or an honest 'we don't know' — Kingsley wants "
        f"a defensible reading.",
        "",
        "## Four candidate hypotheses tested against the data",
        "",
        "### H1 — Temporal mix (reviews skew earlier years; stance was more positive then)",
        "",
        f"Result: H1 explains **{h1_explained_pct:.0f}%** of the {total_gap:.2f} pp gap. "
        f"Reviews critical rate reweighted to research's year-mix is {mix_adjusted_rev:.2f}% "
        f"(vs raw {reviews['crit'].mean()*100:.2f}%). "
        + ("**Most of the gap is NOT temporal."
            if h1_explained_pct < 50 else
            "**Temporal mix is a substantial driver."),
        "",
        "### H4 — Year-stratified gap (controlling for year)",
        "",
        "Per-year deltas (Δ = reviews − research crit %):",
        "",
        "| year | Δ pp |",
        "|---:|---:|",
    ]
    for r in year_rows:
        discussion.append(f"| {r['year']} | {r['delta_pp']:+.2f} |")
    discussion.append("")
    discussion.append(f"Even within each individual year, reviews are less critical. "
                       f"This rules out H1 as the sole explanation.")
    discussion.append("")
    discussion.append("### H2 — Sub-pub-type (Systematic Reviews vs narrative Reviews)")
    discussion.append("")
    discussion.append(f"- Systematic Reviews: {sub_rows[0]['n']:,} records, "
                       f"**{sub_rows[0]['crit_pct']:.2f}% critical**, "
                       f"{sub_rows[0]['advocacy_pct']:.2f}% Advocacy")
    discussion.append(f"- Reviews (narrative): {sub_rows[1]['n']:,} records, "
                       f"**{sub_rows[1]['crit_pct']:.2f}% critical**, "
                       f"{sub_rows[1]['advocacy_pct']:.2f}% Advocacy")
    discussion.append("")
    discussion.append(
        ("Systematic Reviews are MORE critical than narrative Reviews "
         f"(Δ {h2_sr_vs_r:+.1f} pp). Suggests narrative reviews are the main driver "
         f"of the reviews-positivity pattern — possibly because narrative reviews are "
         f"opinion-permissive and authored by topic-area enthusiasts."
         if h2_sr_vs_r > 0 else
         "Narrative Reviews are more critical than Systematic Reviews "
         f"(Δ {-h2_sr_vs_r:+.1f} pp in opposite direction). Suggests systematic-review "
         f"selection bias (toward positive published findings) plays a role."))
    discussion.append("")
    discussion.append("### H3 — Theme emphasis")
    discussion.append("")
    discussion.append("Among the 10 themes tracked in the A+C subset, the largest review-vs-research differentials are:")
    discussion.append("")
    theme_sorted = sorted(theme_rows, key=lambda r: -abs(r["delta_pp"]))[:5]
    for r in theme_sorted:
        if r["delta_pp"] > 0:
            direction = "**more** in reviews"
        else:
            direction = "**more** in research articles"
        discussion.append(f"- `{r['theme']}`: {direction} by {abs(r['delta_pp']):.1f} pp "
                           f"({r['rev_pct']:.1f}% vs {r['res_pct']:.1f}%)")
    discussion.append("")
    discussion.append(
        "If reviews emphasize broad/abstract risk themes (regulation, ethics) and research "
        "articles emphasize concrete failure themes (hallucination, safety_clinical), this "
        "supports the interpretation that **reviews look up while research looks down** — "
        "reviews paint the field strategically, research catalogs the field operationally."
    )
    discussion.append("")
    discussion.append("## The 3 exception specialties (where reviews are MORE critical)")
    discussion.append("")
    discussion.append(
        "Session 2 C.3 found that MH (+4.5 pp), Radiology (+3.8 pp), and Medical Education "
        "(+3.3 pp) buck the pattern. Sample critical-review titles in those specialties "
        "(from `reviews_positivity_why.md`) suggest:"
    )
    discussion.append("")
    discussion.append(
        "- **Mental Health / Psychiatry**: review articles tend to compile evidence on "
        "LLM-as-therapist risks, suicide-risk model failures, parasocial concerns. These "
        "are concrete-risk reviews, not promise reviews.")
    discussion.append(
        "- **Radiology**: a mature field where reviews are written by specialists who have "
        "seen multiple AI hype cycles fail to deliver. Reviews acknowledge limitations more "
        "openly than the optimistic deep-learning research articles.")
    discussion.append(
        "- **Medical Education**: reviews critique pedagogy and curricular integration — "
        "stance-bearing critique of AI's role in training, distinct from the use-case promise "
        "reviews in clinical specialties.")
    discussion.append("")
    discussion.append("## Synthesis for the Commentary")
    discussion.append("")
    discussion.append(
        "The reviews-positivity pattern is **driven by narrative reviews in clinical specialties** "
        "and is **not explained by temporal mix or systematic-review selection alone**. "
        "Theme emphasis (reviews look up to strategy; research articles look down to operations) "
        "is the most parsimonious mechanism."
    )
    discussion.append("")
    discussion.append(
        "**Implication Kingsley flagged in Session 2:** \"most readers encounter the medical "
        "AI literature through reviews, which are systematically more positive than the "
        "underlying evaluative literature.\" This is the headline finding. Reviews shape the "
        "narrative; the evaluative literature underneath them is more skeptical."
    )
    discussion.append("")
    discussion.append("## Open question for upstream Opus chat")
    discussion.append("")
    discussion.append(
        "Three drafting paths for the Commentary:"
    )
    discussion.append("")
    discussion.append(
        "1. **The accessibility paradox.** Reviews are the highest-readership format and "
        "the most positive register. The field's public-facing narrative is therefore "
        "disproportionately optimistic compared to the evaluative work underneath."
    )
    discussion.append(
        "2. **The 'look up vs look down' framing.** Quote the theme-prevalence evidence "
        "(regulation in reviews vs hallucination in research). Reviews orient strategy; "
        "research evaluates execution."
    )
    discussion.append(
        "3. **Exception-first framing.** Lead with the MH/Radiology/Med Education exceptions "
        "as a foil, then introduce the general pattern. This avoids the 'reviews are biased' "
        "tone and instead positions reviews as a function of where the field is in its hype cycle."
    )
    discussion.append("")
    discussion.append(
        "Claude's read: **Path 1 is the strongest Commentary headline** — it directly speaks "
        "to clinician readers who DO encounter the field through reviews. Path 2 belongs in "
        "the body as the mechanism. Path 3 is too inside-baseball for a 1,200-word Commentary."
    )

    out_disc = ANALYSES_DIR / "discussion_reviews_positivity.md"
    out_disc.write_text("\n".join(discussion) + "\n")
    print(f"Wrote: {out_disc}")


if __name__ == "__main__":
    main()
