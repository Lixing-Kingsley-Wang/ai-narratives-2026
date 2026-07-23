#!/usr/bin/env python3
"""
Prophecy Panel — PHASE 2a: build evidence corpus, MedCPT embed (cached), retrieve top-k.

Evidence = full medical-AI corpus filtered to (year in {2024,2025,2026}) AND (non-empty abstract).
The 2021-2023 prediction papers are excluded automatically by the year filter.

MedCPT (NCBI), confirmed from the official model cards:
  - Query-Encoder  : signature claim -> tokenizer(max_length=64) -> CLS (last_hidden_state[:,0,:])
  - Article-Encoder: [title, abstract] pair -> tokenizer(max_length=512) -> CLS
  - Similarity: dot product of CLS embeddings (model card does not state a metric; MedCPT is trained
    with contrastive inner-product and NCBI's retrieval examples score by dot product). Raw embeddings
    are cached so cosine is recomputable. Choice logged to run_manifest.txt.

Embeddings are cached to .npy; re-runs load from cache (no re-embedding). Usage:
  python prophecy_phase2_embed_retrieve.py smoke   # tiny self-test (model load + 3 vectors)
  python prophecy_phase2_embed_retrieve.py         # full build + retrieval
"""
import os, sys, csv, json, datetime, hashlib
import numpy as np

csv.field_size_limit(sys.maxsize)

REPO    = "/Users/kingslywang/repos/ai-narratives-2026"
OUT_DIR = os.path.join(REPO, "output", "analyses", "prophecy")
CORPUS  = os.path.join(REPO, "output", "filtered_medical_all_Q1Q2.csv")
FROZEN  = os.path.join(OUT_DIR, "phase1_signature_claims_FROZEN.csv")
EMB_DIR = os.path.join(OUT_DIR, "embeddings"); os.makedirs(EMB_DIR, exist_ok=True)
EV_EMB  = os.path.join(EMB_DIR, "evidence_article_embeds.npy")
EV_PMID = os.path.join(EMB_DIR, "evidence_pmids.npy")
EV_META = os.path.join(EMB_DIR, "evidence_meta.json")
Q_EMB   = os.path.join(EMB_DIR, "claim_query_embeds.npy")
Q_IDS   = os.path.join(EMB_DIR, "claim_ids.npy")
RETR    = os.path.join(OUT_DIR, "phase2_retrieval.csv")
MANIFEST= os.path.join(OUT_DIR, "run_manifest.txt")

EVIDENCE_YEARS = {"2024", "2025", "2026"}
CUTOFF   = "2026-04"
TOP_K    = 20
Q_MAXLEN = 64
A_MAXLEN = 512
BATCH    = 64
SEED     = 20260630
QUERY_MODEL   = "ncbi/MedCPT-Query-Encoder"
ARTICLE_MODEL = "ncbi/MedCPT-Article-Encoder"


def load_models():
    import torch
    from transformers import AutoTokenizer, AutoModel
    torch.manual_seed(SEED); np.random.seed(SEED)
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"device: {dev}")
    qt = AutoTokenizer.from_pretrained(QUERY_MODEL)
    qm = AutoModel.from_pretrained(QUERY_MODEL).to(dev).eval()
    at = AutoTokenizer.from_pretrained(ARTICLE_MODEL)
    am = AutoModel.from_pretrained(ARTICLE_MODEL).to(dev).eval()
    rev = {"query": getattr(qm.config, "_commit_hash", "unknown"),
           "article": getattr(am.config, "_commit_hash", "unknown")}
    return torch, dev, (qt, qm), (at, am), rev


def embed(torch, dev, tok, model, items, max_len, pair, desc):
    from tqdm import tqdm
    out = []
    for s in tqdm(range(0, len(items), BATCH), desc=desc):
        batch = items[s:s + BATCH]
        enc = tok(batch, truncation=True, padding=True, return_tensors="pt", max_length=max_len)
        enc = {k: v.to(dev) for k, v in enc.items()}
        with torch.no_grad():
            cls = model(**enc).last_hidden_state[:, 0, :]
        out.append(cls.float().cpu().numpy())
    return np.vstack(out)


def load_evidence():
    ev_pmid, ev_title, ev_abs = [], [], []
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if str(row.get("year", "")).strip() in EVIDENCE_YEARS and (row.get("abstract") or "").strip():
                ev_pmid.append(str(row["pmid"]).strip())
                ev_title.append((row.get("title") or "").strip())
                ev_abs.append((row.get("abstract") or "").strip())
    return ev_pmid, ev_title, ev_abs


def main(smoke=False):
    torch, dev, (qt, qm), (at, am), rev = load_models()

    if smoke:
        ev = embed(torch, dev, at, am, [["Deep learning for melanoma", "We trained a CNN..."],
                                        ["Sepsis biomarkers", "A cohort study of..."]], A_MAXLEN, True, "smoke-article")
        q = embed(torch, dev, qt, qm, ["AI will outperform dermatologists at melanoma diagnosis"], Q_MAXLEN, False, "smoke-query")
        print("article embeds:", ev.shape, "| query embeds:", q.shape)
        print("dot scores (query vs 2 articles):", (q @ ev.T)[0])
        return

    # ── claims ───────────────────────────────────────────────────────────────────
    claims = list(csv.DictReader(open(FROZEN, encoding="utf-8")))
    claim_ids = [c["claim_id"] for c in claims]
    claim_txt = [c["signature_claim"] for c in claims]
    print(f"claims: {len(claims)}")

    # ── evidence corpus ────────────────────────────────────────────────────────────
    ev_pmid, ev_title, ev_abs = load_evidence()
    n_ev = len(ev_pmid)
    print(f"evidence corpus (year in {sorted(EVIDENCE_YEARS)} & non-empty abstract): {n_ev} rows")

    # ── article embeddings (cached) ────────────────────────────────────────────────
    cached = (os.path.exists(EV_EMB) and os.path.exists(EV_PMID)
              and len(np.load(EV_PMID, allow_pickle=True)) == n_ev)
    if cached:
        print("loading cached article embeddings")
        ev_emb = np.load(EV_EMB); ev_pmid = list(np.load(EV_PMID, allow_pickle=True))
    else:
        articles = [[t, a] for t, a in zip(ev_title, ev_abs)]
        ev_emb = embed(torch, dev, at, am, articles, A_MAXLEN, True, "embed articles")
        np.save(EV_EMB, ev_emb); np.save(EV_PMID, np.array(ev_pmid, dtype=object))
        json.dump({"n_evidence": n_ev, "cutoff": CUTOFF, "years": sorted(EVIDENCE_YEARS),
                   "article_model": ARTICLE_MODEL, "revision": rev["article"], "dim": int(ev_emb.shape[1])},
                  open(EV_META, "w"), indent=2)
    print("article embeds:", ev_emb.shape)

    # ── query embeddings ────────────────────────────────────────────────────────────
    q_emb = embed(torch, dev, qt, qm, claim_txt, Q_MAXLEN, False, "embed claims")
    np.save(Q_EMB, q_emb); np.save(Q_IDS, np.array(claim_ids, dtype=object))

    # ── retrieve top-k (dot product) ────────────────────────────────────────────────
    ev_pmid_arr = np.array(ev_pmid, dtype=object)
    with open(RETR, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["claim_id", "retrieved_pmids_top20", "retrieved_scores_top20", "top_score"])
        for i, cid in enumerate(claim_ids):
            scores = ev_emb @ q_emb[i]
            top = np.argpartition(-scores, TOP_K)[:TOP_K]
            top = top[np.argsort(-scores[top])]
            pmids = [str(ev_pmid_arr[j]) for j in top]
            scs = [round(float(scores[j]), 3) for j in top]
            w.writerow([cid, "|".join(pmids), "|".join(map(str, scs)), scs[0]])
    print(f"wrote retrieval -> {RETR}")

    with open(MANIFEST, "a", encoding="utf-8") as m:
        m.write(
            f"\n[PHASE 2a EMBED/RETRIEVE] {datetime.datetime.now().isoformat(timespec='seconds')}\n"
            f"  query_model={QUERY_MODEL}@{rev['query']} article_model={ARTICLE_MODEL}@{rev['article']}\n"
            f"  pooling=CLS(last_hidden_state[:,0,:]) q_maxlen={Q_MAXLEN} a_maxlen={A_MAXLEN} "
            f"similarity=dot_product seed={SEED} device={dev}\n"
            f"  evidence_rows={n_ev} years={sorted(EVIDENCE_YEARS)} cutoff={CUTOFF} top_k={TOP_K} "
            f"claims={len(claims)}\n"
            f"  note=similarity metric not stated on model card; dot product chosen per MedCPT "
            f"contrastive training + NCBI retrieval examples; raw embeds cached for recompute\n"
            f"  embeds={EV_EMB}\n"
        )
    print("manifest appended.")


if __name__ == "__main__":
    main(smoke=(len(sys.argv) > 1 and sys.argv[1] == "smoke"))
