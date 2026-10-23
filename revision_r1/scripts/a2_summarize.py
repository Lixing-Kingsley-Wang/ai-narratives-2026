"""A2 summary · aggregate production × full-abstract cross-tabs by year, flip
counts, FAILED count, projected vs actual cost. Aggregates only.
Output: revision_r1/outputs/A2/A2_summary.md (+ csv)
"""

from __future__ import annotations

import json

import pandas as pd

from r1_common import OUT, md_table

A2 = OUT / "A2"
LAB = ["discourse", "evaluative", "application", "FAILED"]
KEEP = {"discourse", "evaluative"}


def main():
    d = pd.read_csv(A2 / "a2_fullabstract_labels.csv", dtype=str, keep_default_na=False)
    proj = json.loads((A2 / "cost_projection.json").read_text())
    act = json.loads((A2 / "actual_cost.json").read_text())
    d["year_band"] = d["year"].where(d["year"].isin([str(y) for y in range(2021, 2027)]), "other (2018/2020)")

    long = pd.crosstab([d["year_band"], d["label_production"]], d["label_fullabstract"]).reindex(columns=LAB, fill_value=0)
    long.to_csv(A2 / "A2_crosstab_by_year.csv")
    overall = pd.crosstab(d["label_production"], d["label_fullabstract"], margins=True, margins_name="Total").reindex(
        columns=LAB + ["Total"], fill_value=0)

    pk = d["label_production"].isin(KEEP); fk = d["label_fullabstract"].isin(KEEP)
    fa = d["label_fullabstract"] == "application"; failed = d["label_fullabstract"] == "FAILED"
    flips = d.assign(app_to_keep=(~pk) & fk, keep_to_app=pk & fa).groupby("year_band")[["app_to_keep", "keep_to_app"]].sum()
    flips["production_application"] = d[~pk].groupby("year_band").size()
    flips["production_retained"] = d[pk].groupby("year_band").size()
    flips["app_to_keep_%"] = flips.app_to_keep / flips.production_application * 100
    flips["keep_to_app_%"] = flips.keep_to_app / flips.production_retained * 100
    flips["full_keep_rate_%"] = d.groupby("year_band").apply(lambda g: g["label_fullabstract"].isin(KEEP).mean() * 100)
    flips["production_keep_rate_%"] = d.groupby("year_band").apply(lambda g: g["label_production"].isin(KEEP).mean() * 100)
    flips.loc["Total"] = [int(((~pk) & fk).sum()), int((pk & fa).sum()), int((~pk).sum()), int(pk.sum()),
                          ((~pk) & fk).sum() / (~pk).sum() * 100, (pk & fa).sum() / pk.sum() * 100,
                          fk.mean() * 100, pk.mean() * 100]
    flips.to_csv(A2 / "A2_flips_by_year.csv")

    L = ["# A2 · Full-abstract prefilter re-run — summary (aggregates only)\n",
         f"Records: {len(d):,}. Final FAILED: **{int(failed.sum())}** "
         f"(round 1 FAILED: {int((pd.read_csv(A2 / 'parsed_round1.csv', dtype=str).failed == '1').sum())}; resubmitted once).\n",
         f"Projected cost (1,000-record exact token count): **${proj['projected_cost_usd']:.2f}**. "
         f"Actual cost from returned usage: **${act['cost_usd']:.2f}** "
         f"({act['input_tokens']:,} input, {act['output_tokens']:,} output tokens; Batch pricing $0.50/$2.50 per MTok).\n",
         "## Production (rows) × full-abstract (columns), all records\n",
         md_table(overall.reset_index(), "{:.0f}"), "",
         "## Flips by year\n",
         "app_to_keep = production application → full-abstract discourse/evaluative; keep_to_app = production retained → "
         "full-abstract application.\n",
         md_table(flips.reset_index(), "{:.1f}"), "",
         "## Cross-tab by year (production label × full-abstract label)\n",
         md_table(long.reset_index(), "{:.0f}")]
    (A2 / "A2_summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:8]))
    print(flips.to_string())


if __name__ == "__main__":
    main()
