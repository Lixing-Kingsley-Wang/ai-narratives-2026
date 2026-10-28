"""B7 · Numeric corrections table (JMIR R1 Batch 2b; E13, D8).
old value → corrected value → source, for every Batch 1 discrepancy that
changes a printed number, plus text-only corrections listed separately.
Output: revision_r1/outputs/B7_corrections.md (+ csv for Table S3)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from r1_common import OUT, load_v1, md_table, spearman_exact

GENRES = ["discourse", "evaluative"]


def table_s3(years):
    """Within-genre critical share, per-cell bootstrap (1000 resamples) with deterministic seeds
    42 + cell_index, cells sorted by genre then year (replaces cv1_within_genre.py's hash() seeds)."""
    v = load_v1(year_range=(2021, 2026))
    rows, idx = [], 0
    for g in GENRES:
        for y in years:
            x = v[(v.paper_type == g) & (v.pub_year == y)]["critical"].to_numpy(dtype=float)
            rng = np.random.default_rng(42 + idx)
            draws = [x[rng.integers(0, len(x), len(x))].mean() * 100 for _ in range(1000)]
            lo, hi = np.percentile(draws, [2.5, 97.5])
            rows.append({"genre": g, "year": y, "cell_index": idx, "seed": 42 + idx, "k": int(x.sum()), "n": len(x),
                         "critical_%": x.mean() * 100, "lo": lo, "hi": hi})
            idx += 1
    t = pd.DataFrame(rows)
    out = {}
    for g in GENRES:
        s = t[t.genre == g]
        rho, p, _ = spearman_exact(list(s.year), s["critical_%"].to_numpy())
        out[g] = (rho, p)
    return t, out


def jp(p):
    return "<.001" if p < 0.001 else f"{p:.3f}".lstrip("0")


def main():
    L = ["# B7 · Numeric corrections (E13, D8)\n",
         "Old value (as printed in the submitted manuscript/supplement) → corrected value → source. Numbers only; "
         "the manuscript is not edited here.\n"]
    tr = pd.read_csv(OUT / "T4_trend_tests.csv")
    ann = pd.read_csv(OUT / "T4_annual_all_domains.csv")

    # 1. Table S1
    printed = {"Alarm": ".072", "Caution": ".072", "Neutral": ".019", "Cautious Optimism": ".329", "Advocacy": ".003",
               "Critical (Alarm+Caution)": ".072"}
    rows = []
    for o, pv in printed.items():
        a = tr[(tr.domain == "Stance") & (tr.outcome == o) & (tr.window == "2021–2026 (submitted)")].iloc[0]
        b = tr[(tr.domain == "Stance") & (tr.outcome == o) & (tr.window == "2021–2025")].iloc[0]
        rows.append({"Table S1 row": o, "printed P (2021–2026)": pv, "ρ 2021–2026": f"{a.rho:+.3f}",
                     "exact permutation P 2021–2026": jp(a.P_exact_perm), "ρ 2021–2025": f"{b.rho:+.3f}",
                     "exact permutation P 2021–2025": jp(b.P_exact_perm)})
    L += ["## 1. Table S1 P values → exact permutation P (all rows)\n",
          "Source: `outputs/T4_trend_tests.csv` (t4_temporal.py; all 6! or 5! orderings). The printed values except "
          "Advocacy are scipy's asymptotic t-approximation. Minimum attainable two-sided P: 2/720 = .003 (6 points), "
          "2/120 = .017 (5 points).\n", md_table(pd.DataFrame(rows)), ""]

    # 2. Table S3
    L.append("## 2. Table S3 regenerated with deterministic per-cell seeds\n")
    printed_s3 = {("discourse", 2021): "30.2 (26.7–33.3)", ("discourse", 2022): "31.2 (28.0–34.2)",
                  ("discourse", 2023): "35.3 (32.4–37.9)", ("discourse", 2024): "37.5 (35.3–39.5)",
                  ("discourse", 2025): "35.4 (33.7–37.4)", ("discourse", 2026): "37.8 (35.2–40.5)",
                  ("evaluative", 2021): "14.6 (11.0–18.6)", ("evaluative", 2022): "13.3 (10.2–16.7)",
                  ("evaluative", 2023): "22.5 (19.6–25.3)", ("evaluative", 2024): "28.6 (26.5–30.8)",
                  ("evaluative", 2025): "26.8 (25.1–28.4)", ("evaluative", 2026): "28.1 (25.8–30.5)"}
    for win, ys in (("2021–2026 (submitted window)", [2021, 2022, 2023, 2024, 2025, 2026]),
                    ("2021–2025 (primary window)", [2021, 2022, 2023, 2024, 2025])):
        t, sp = table_s3(ys)
        t.to_csv(OUT / f"B7_tableS3_{'2021_2026' if 2026 in ys else '2021_2025'}.csv", index=False)
        show = pd.DataFrame({"genre": t.genre, "year": t.year, "seed": t.seed,
                             "printed % (CI)": [printed_s3[(g, y)] for g, y in zip(t.genre, t.year)],
                             "corrected % (CI); n/N": [f"{p:.1f} ({lo:.1f}–{hi:.1f}); {k}/{n}" for p, lo, hi, k, n in
                                                       zip(t["critical_%"], t.lo, t.hi, t.k, t.n)]})
        L += [f"**{win}** — Spearman ρ (exact P): discourse {sp['discourse'][0]:+.2f} ({jp(sp['discourse'][1])}); "
              f"evaluative {sp['evaluative'][0]:+.2f} ({jp(sp['evaluative'][1])}).\n", md_table(show), ""]
    L.append("Seeds: 42 + cell_index with cells sorted by genre then year; each cell resampled on its own (as the original "
             "design), replacing `42 + hash((genre, year)) % 10000`. Point estimates are unchanged.\n")

    # 3. Table S9 n's
    x = pd.read_csv(OUT / "T5_crosssectional_both_windows.csv")
    reg = x[(x.analysis == "Region critical") & (x.window == "2021–Apr 2026 (submitted)")]
    printed_n = {"North America": 4964, "Western Europe": 4298, "East Asia": 3262, "Middle East / North Africa": 1706,
                 "South/Southeast Asia": 785, "Latin America / Oceania": 753, "Eastern Europe": 330,
                 "Sub-Saharan Africa": 68, "Unknown": 593}
    rr = [{"region": r.group, "printed n": f"{printed_n[r.group]:,}", "corrected n (16,747)": f"{int(r.n):,}",
           "critical % (CI), unchanged": f"{r.value:.1f} ({r.lo:.1f}–{r.hi:.1f}); {int(r.k):,}/{int(r.n):,}"}
          for r in reg.itertuples()]
    L += ["## 3. Table S9 and Results region n's on the 16,747 denominator\n",
          "Source: `outputs/T5_crosssectional_both_windows.csv`. The printed n's sum to 16,759 (before the 10 stance "
          "failures and 2 records dated 2020 were excluded); the percentages were already computed on 16,747.\n",
          md_table(pd.DataFrame(rr)), ""]

    # 4–7
    gate = ann[(ann.domain == "Mechanism, hallucination-gated") & (ann.window == "2021–2026 (submitted)")]
    L += ["## 4–7. Single values\n",
          "| # | item | printed | corrected | source |", "|---|---|---|---|---|",
          "| 4 | Commentary critical rate (Results; Table S10) | 53.9% | **53.8%** (56/104 = 53.85%) | T5 cross-sectional |",
          "| 5 | Q1/Q2 share of eligible records (Methods) | 88.0% | **88.1%** (98,626/112,011 = 88.05%) | `output/sjr.log` |",
          "| 7a | Failure-mode κ_max (Methods) | 0.76 | **0.755** (0.7549) | T3 |",
          "| 7b | Model-type Gwet AC1 (Methods) | 0.89 | **0.885** (0.8847) | T3 |",
          "| 8a | Prefilter κ 95% CI (Methods) | 0.35–0.68 | **0.345–0.646** (bootstrap, 1000, seed 42; original code not found) | T1 |",
          "| 8b | Prefilter raw agreement / κ | 85.5% / 0.51 | unchanged (171/200; 0.511) | T1 |", ""]
    L += ["## 6. Fabrication-involved share among hallucination-gated, abstract-present critical records, by year\n",
          "Printed (Abstract; Results R29): \"rose from 0% in 2021 to roughly 21–23% from 2023 onward\". Corrected values "
          "(confabulation or both; source `outputs/T4_annual_all_domains.csv`):\n",
          "| year | share (bootstrap 95% CI) | exact Clopper–Pearson 95% CI | n/N |", "|---|---|---|---|"]
    from scipy.stats import beta
    for r in gate[gate.outcome == "Fabrication-involved (confabulation or both)"].itertuples():
        clo = 0.0 if r.k == 0 else beta.ppf(0.025, r.k, r.N - r.k + 1)
        chi = 1.0 if r.k == r.N else beta.ppf(0.975, r.k + 1, r.N - r.k)
        L.append(f"| {r.year}{' (Jan–Apr)' if r.year == 2026 else ''} | {r.pct:.1f}% ({r.lo:.1f}–{r.hi:.1f}) | "
                 f"{clo*100:.1f}–{chi*100:.1f} | {r.k}/{r.N} |")
    L.append("")

    L += ["## 8. Text-only corrections (no printed number changes)\n",
          "- **Stance prompt (new in Batch 2b).** Supplementary Note 2 prints the v2 prompt (current `classify_stance_batch.py`, "
          "8,164 characters); all reported stance labels come from the v1 prompt (SHA-256 `b3949917…`, `classify_stance.py` "
          "= `9c79cd5:classify_stance_batch.py`). The Methods' Advocacy definition (\"both transformative language … and "
          "minimal or no acknowledged caveats\") paraphrases v2; v1 reads \"Advocacy: strongly pro-AI. Emphasises "
          "transformative potential, minimal caveats.\"",
          "- Prefilter API: first 2,500 records synchronous, 94,992 via one Message Batch (Methods says Batch API).",
          "- Prefilter failure defaults: 96 records defaulted to `application`.",
          "- Pilot sampling design not documented; `make_pilot.py` does not match the committed pilot.",
          "- SJR \"unmatched\" (7,922) includes 1,336 Q4 and 1,494 no-quartile titles.",
          "- Regions (Table S9) come from `geography_classifications.csv`, not from grouping the 90.3%-resolved countries.",
          "- Review subtype rule (PubMed Publication Type substrings; Scoping Review → narrative; Meta-Analysis has no rule).",
          "- Stance validation sample drawn only from abstract-present records.",
          "- Human stance codebook (`coding_instructions.txt`) shorter than the classifier prompt.",
          "- Generative share for the specialty correlation computed among abstract-present critical records.",
          "- Missing PubDate months are stored as January.", ""]
    (OUT / "B7_corrections.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:20]))


if __name__ == "__main__":
    main()
