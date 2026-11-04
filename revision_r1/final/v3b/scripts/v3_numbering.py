"""Final first-citation numbering of the Multimedia Appendices (JMIR), v3.

Reads the [[MA:unit_id]] tokens, in order, from the accepted text of the revised
Methods, Results and Discussion (Methods -> Results -> Discussion), applies two
aliases and three proposed citations that are not yet in the text (listed for the
author), and writes ma_order_v3.yaml and token_label_map_v3.csv.

Appendix roles follow the first token of each kind: notes (MA1), tables (MA2), figures (MA3).
"""
from __future__ import annotations

import csv
import re

import yaml

from v3_common import V3

TXT = V3 / "manuscript_text"
SECTIONS = [("Methods", "Methods_r1_Claude_v2.txt"), ("Results", "Results_r1_Claude_v3_tracked.txt"),
            ("Discussion", "Discussion_r1_Claude_v2_tracked.txt")]
ALIAS = {"period_correction": "corrected_prevalence"}            # Methods token -> unit
NOTE_OF = {"note_stance_prompt_v1": "note_stance_prompts", "note_stance_prompt_v2": "note_stance_prompts"}
PART = {"note_stance_prompt_v1": "(a)", "note_stance_prompt_v2": "(b)"}
# citations proposed to the author (not yet in the text): inserted right after the anchor token
PROPOSED = {("Methods", "prefilter_validation", 1): "note_validation_protocol",
            ("Results", "corpus_sensitivity", 1): "temporal_robustness_fig",
            ("Results", "q3_arm", 1): "q3_fig"}
FIGURES = {"within_genre_fig", "temporal_robustness_fig", "q3_fig", "other_themes_fig", "theme_counts_fig",
           "lexicon_vs_llm_fig", "terms_fig", "generative_share_fig", "country_map_20", "forward_validation_sankey",
           "advocacy_measures_fig"}


def main():
    seq, raw = [], []
    for sec, fn in SECTIONS:
        seen = {}
        for t in re.findall(r"\[\[MA:([a-z0-9_]+)\]\]", (TXT / fn).read_text(encoding="utf-8")):
            raw.append((sec, t))
            seq.append((sec, t, False))
            seen[t] = seen.get(t, 0) + 1
            key = (sec, t, seen[t])
            if key in PROPOSED:
                seq.append((sec, PROPOSED[key], True))
    notes, tables, figs = [], [], []
    for sec, t, prop in seq:
        u = NOTE_OF.get(ALIAS.get(t, t), ALIAS.get(t, t))
        lst = notes if u.startswith("note_") else figs if u in FIGURES else tables
        if u not in lst:
            lst.append(u)
    order = {"ma1_notes": notes, "ma2_tables": tables, "ma3_figures": figs}
    (V3 / "ma" / "ma_order_v3.yaml").write_text(
        "# v3 numbering by first citation (Methods -> Results -> Discussion). Built by v3_numbering.py.\n"
        "# Three citations are proposed, not yet in the text: note_validation_protocol (Methods, Quality of\n"
        "# Measurements), temporal_robustness_fig and q3_fig (Results, critical-trend paragraph).\n"
        + yaml.safe_dump(order, sort_keys=False, allow_unicode=True), encoding="utf-8")
    nn = {u: i for i, u in enumerate(notes, 1)}
    tn = {u: i for i, u in enumerate(tables, 1)}
    fnn = {u: i for i, u in enumerate(figs, 1)}

    def label(t):
        u = ALIAS.get(t, t)
        if t in NOTE_OF:
            return f"Multimedia Appendix 1, Note {nn[NOTE_OF[t]]}{PART[t]}"
        if u.startswith("note_"):
            return f"Multimedia Appendix 1, Note {nn[u]}"
        if u in FIGURES:
            return f"Multimedia Appendix 3, Figure S{fnn[u]}"
        return f"Multimedia Appendix 2, Table S{tn[u]}"
    rows, done = [], set()
    for sec, t, prop in seq:
        if (t, prop) in done:
            continue
        done.add((t, prop))
        rows.append({"token": f"[[MA:{t}]]", "replace_with": label(t), "first_cited_in": sec,
                     "status": "PROPOSED: add this citation" if prop else "in text"})
    with open(V3 / "token_label_map_v3.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["token", "replace_with", "first_cited_in", "status"])
        w.writeheader(); w.writerows(rows)
    print(f"notes {len(notes)}, tables {len(tables)}, figures {len(figs)}; tokens in text {len(raw)}")
    for k, v in order.items():
        print(k, v)


if __name__ == "__main__":
    main()
