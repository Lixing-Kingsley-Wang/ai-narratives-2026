#!/usr/bin/env python3
"""
Freeze the reviewer's Phase 1 workbook -> phase1_signature_claims_FROZEN.csv (CLAIM-LEVEL).

Reads phase1_signature_claims_for_review.xlsx ('review' sheet), keeps rows the reviewer marked
keep?=keep, and emits ONE ROW PER CLAIM (unit of analysis = claim, per prereg A2). Most papers
yield one claim; a few yield two (claim_role primary/secondary, claim_id PMID / PMID-2).

All bespoke reviewer decisions are encoded EXPLICITLY below (not inferred from the sheet), because
some involve restoring a mis-pasted cell, merging result+forecast, or splitting tiers per claim:

  RESTORE  33937332 : signature_claim cell was contaminated with PMID 33529363's text; restore the
                      original on-topic claim from the machine CSV. Drop claim 2. Tier 2.
  MERGED   32767299 : use a single signature that keeps the human head-to-head (Tier-1 superiority).
           37489981 : same.
  SPLIT    34602525 : claim1 -> T3, claim2 -> T2 (2 rows)
           37686619 : claim1 -> T2, claim2 -> T2 (2 rows)
           33731170 : claim1 -> T2, claim2 -> T3 (2 rows)
           36143468 : claim1 -> T3, claim2 -> T2 (2 rows; claim2 non-clinical -> likely corpus_silent)
  Everything else: one claim per kept row = the sheet's signature_claim + flag/tier/topic/horizon.
                   (Secondary machine-claims with no reviewer note are dropped by default.)
"""
import os, csv, datetime
from openpyxl import load_workbook

OUT_DIR  = "/Users/kingslywang/repos/ai-narratives-2026/output/analyses/prophecy"
XLSX     = os.path.join(OUT_DIR, "phase1_signature_claims_for_review.xlsx")
CSV_IN   = os.path.join(OUT_DIR, "phase1_signature_claims_for_review.csv")  # original machine output
FROZEN   = os.path.join(OUT_DIR, "phase1_signature_claims_FROZEN.csv")
MANIFEST = os.path.join(OUT_DIR, "run_manifest.txt")

MERGED = {  # pmid -> (signature_claim, tier)  single primary claim
    "32767299": ("Deep-learning algorithms, more accurate than physicians at newborn-hip ultrasound "
                 "angle measurement (CNN RMSE 3.9 deg vs physician 7.1 deg), can be used in routine "
                 "practice to support/surpass physicians.", "1"),
    "37489981": ("A context-based chatbot (accGPT) outperforms trained radiologists and generic "
                 "ChatGPT in following ACR imaging-appropriateness guidelines, and such context-based "
                 "algorithms can substantially improve clinical imaging decision-making.", "1"),
}
RESTORE = {"33937332": "2"}                       # restore claim from machine CSV; tier 2
SPLIT = {  # pmid -> [(which, tier, role)]  which in {c1,c2}
    "34602525": [("c1", "3", "primary"), ("c2", "2", "secondary")],
    "37686619": [("c1", "2", "primary"), ("c2", "2", "secondary")],
    "33731170": [("c1", "2", "primary"), ("c2", "3", "secondary")],
    "36143468": [("c1", "3", "primary"), ("c2", "2", "secondary")],
}

OUT_COLS = ["claim_id", "pmid", "claim_role", "pub_year", "journal", "pub_type_simple_5",
            "specialty", "title", "signature_claim", "tier", "topic", "horizon",
            "flag_confirmed", "reviewer_note"]


def main():
    orig = {r["pmid"]: r for r in csv.DictReader(open(CSV_IN, encoding="utf-8"))}
    s = load_workbook(XLSX, data_only=True)["review"]
    H = {s.cell(1, j).value: j for j in range(1, s.max_column + 1)}

    def c(i, n):
        v = s.cell(i, H[n]).value
        return "" if v is None else str(v).strip()

    claims, dropped_papers = [], 0
    for i in range(2, s.max_row + 1):
        pmid = c(i, "pmid")
        if not pmid:
            continue
        if c(i, "keep?").lower() == "delete":
            dropped_papers += 1
            continue

        base = dict(pmid=pmid, pub_year=c(i, "pub_year"), journal=c(i, "journal"),
                    pub_type_simple_5=orig.get(pmid, {}).get("pub_type_simple_5", ""),
                    specialty=c(i, "specialty"), title=c(i, "title"),
                    topic=c(i, "topic"), horizon=c(i, "horizon") or "open-ended",
                    flag_confirmed=c(i, "flag_confirmed").lower(), reviewer_note=c(i, "reviewer_note"))

        def emit(claim_id, role, text, tier):
            row = dict(base); row.update(claim_id=claim_id, claim_role=role,
                                         signature_claim=text, tier=tier)
            claims.append(row)

        if pmid in MERGED:
            text, tier = MERGED[pmid]; emit(pmid, "primary", text, tier)
        elif pmid in RESTORE:
            emit(pmid, "primary", orig[pmid]["signature_claim"].strip(), RESTORE[pmid])
        elif pmid in SPLIT:
            for which, tier, role in SPLIT[pmid]:
                text = c(i, "signature_claim") if which == "c1" else c(i, "signature_claim_2")
                emit(pmid if role == "primary" else f"{pmid}-2", role, text, tier)
        else:
            emit(pmid, "primary", c(i, "signature_claim"), c(i, "tier"))

    with open(FROZEN, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLS); w.writeheader(); w.writerows(claims)

    # ── validation + summary ─────────────────────────────────────────────────────
    papers = {r["pmid"] for r in claims}
    from collections import Counter
    tc = Counter(r["tier"] for r in claims)
    bad = [r["claim_id"] for r in claims if not r["signature_claim"].strip()
           or r["tier"] not in ("1", "2", "3")]
    multi = sorted({r["pmid"] for r in claims if r["claim_role"] == "secondary"})

    print("=" * 60)
    print("PHASE 1 FREEZE  (claim-level)")
    print("=" * 60)
    print(f"papers kept     : {len(papers)}   (deleted: {dropped_papers})")
    print(f"claims (frozen) : {len(claims)}   [papers split into 2 claims: {multi}]")
    print(f"tier counts     : T1={tc.get('1',0)}  T2={tc.get('2',0)}  T3={tc.get('3',0)}")
    if bad:
        print(f"!! INVALID rows (blank claim or bad tier): {bad}")
    else:
        print("validation      : OK — every claim has text + tier in {1,2,3}")
    print(f"\nWrote: {FROZEN}")

    with open(MANIFEST, "a", encoding="utf-8") as m:
        m.write(
            f"\n[PHASE 1 FREEZE] {datetime.datetime.now().isoformat(timespec='seconds')}\n"
            f"  papers_kept={len(papers)} deleted={dropped_papers} claims={len(claims)} "
            f"tiers(T1,T2,T3)=({tc.get('1',0)},{tc.get('2',0)},{tc.get('3',0)})\n"
            f"  split_papers={multi}\n"
            f"  restore=33937332(33529363 mis-paste) merged=[32767299,37489981] T1-superiority-kept\n"
            f"  output={FROZEN}\n"
        )
    print(f"Manifest appended: {MANIFEST}")


if __name__ == "__main__":
    main()
