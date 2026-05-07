"""
Prefilter for parallel split processing.
Usage: python prefilter_split.py A   (or B, C, D)

Reads:  output/splits/Q1Q2_batch_A.csv
Writes: output/splits/prefiltered_A_discourse_eval.csv
        output/splits/prefiltered_A_application.csv

After all 4 complete, run merge_splits.py to combine into
prefiltered_discourse_eval.csv and prefiltered_application.csv
"""

import csv, json, time, os, sys, re
import anthropic
from dotenv import load_dotenv
load_dotenv()

BATCH_ID = sys.argv[1].upper() if len(sys.argv) > 1 else "A"

MODEL          = "claude-haiku-4-5-20251001"
BATCH_SIZE_API = 20
MAX_TOKENS     = 800
SLEEP          = 0.12
SLEEP_RETRY    = 12
MAX_RETRIES    = 3
VALID_TYPES    = {"discourse", "evaluative", "application"}

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
SPLITS_DIR = os.path.join(BASE_DIR, "output", "splits")

SYSTEM_PROMPT = """You are classifying medical journal articles into one of three categories based on whether and how they engage with artificial intelligence (AI) as a subject.

CATEGORIES:

- discourse: AI/LLM is the MAIN SUBJECT of discussion. The paper reflects on, debates, or analyses AI's role, safety, ethics, implications, governance, risks, or future in medicine. Includes editorials, perspectives, opinion pieces, and narrative reviews WHERE THE CENTRAL TOPIC IS AI ITSELF. The paper must be primarily ABOUT AI, not just mentioning it.

- evaluative: The paper TESTS or BENCHMARKS a specific AI system (especially LLMs like ChatGPT, GPT-4, or similar) and draws explicit conclusions about its accuracy, safety, reliability, limitations, or clinical readiness. The AI system is the object of study. Must include explicit performance evaluation WITH conclusions about clinical utility or safety.

- application: The paper USES AI/ML as a technical tool to solve a clinical problem (disease detection, segmentation, prediction, drug discovery, genomics). AI is a method, not the subject. OR the paper only MENTIONS AI incidentally without making it a central focus. When in doubt, classify as application.

CRITICAL RULES:
- A paper about genomics, pharmacogenomics, heart rate variability, or clinical trials that mentions AI briefly = application
- A paper primarily about a clinical condition that uses ML for prediction = application
- Only classify as discourse if AI/LLM is clearly the CENTRAL topic
- Only classify as evaluative if there is explicit head-to-head testing of an AI system with clinical conclusions

CONFIDENCE:
- High: category is clear from title alone
- Medium: requires abstract
- Low: ambiguous

Return ONLY a JSON array with one object per article:
[{"paper_type":"...","type_confidence":"..."}, ...]
No preamble, no explanation."""


def extract_pub_year(pub_date_str):
    m = re.search(r'\b(20\d{2})\b', pub_date_str or "")
    return m.group(1) if m else ""


def classify_batch(client, records):
    items = []
    for i, (title, abstract) in enumerate(records):
        text = f"Title: {title}"
        if abstract and abstract.strip():
            text += f"\nAbstract: {abstract[:300]}"
        items.append(f"[{i+1}] {text}")

    batch_prompt = (
        "Classify each article. Return ONLY a JSON array:\n"
        '[{"paper_type":"...","type_confidence":"..."},...]\n\n'
        + "\n\n".join(items)
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": batch_prompt}]
            )
            raw = response.content[0].text.strip()
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)
            parsed = json.loads(raw, strict=False)

            if not isinstance(parsed, list) or len(parsed) != len(records):
                raise ValueError(f"Expected {len(records)}, got {len(parsed) if isinstance(parsed,list) else 'non-list'}")

            results = []
            for item in parsed:
                ptype = item.get("paper_type", "").strip().lower()
                conf  = item.get("type_confidence", "Medium").strip()
                if ptype not in VALID_TYPES:
                    ptype = "application"
                if conf not in ("High", "Medium", "Low"):
                    conf = "Medium"
                results.append((ptype, conf))
            return results

        except Exception as e:
            if attempt < MAX_RETRIES:
                time.sleep(SLEEP_RETRY)
            else:
                return [("application", "Low")] * len(records)

    return [("application", "Low")] * len(records)


def main():
    input_path = os.path.join(SPLITS_DIR, f"Q1Q2_batch_{BATCH_ID}.csv")
    out_de     = os.path.join(SPLITS_DIR, f"prefiltered_{BATCH_ID}_discourse_eval.csv")
    out_ap     = os.path.join(SPLITS_DIR, f"prefiltered_{BATCH_ID}_application.csv")

    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        print("Run split_corpus.py first.")
        sys.exit(1)

    client = anthropic.Anthropic()

    with open(input_path, encoding="utf-8") as f:
        all_records = list(csv.DictReader(f))

    # Resume
    processed = set()
    for path in (out_de, out_ap):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    processed.add(row["pmid"])

    pending = [r for r in all_records if r["pmid"] not in processed]

    print(f"Batch {BATCH_ID}: {len(all_records):,} total | {len(processed):,} done | {len(pending):,} pending")

    if not pending:
        print("Already complete.")
        return

    in_cols  = list(all_records[0].keys())
    out_cols = in_cols + ["pub_year", "paper_type", "type_confidence"]
    mode_de  = "a" if os.path.exists(out_de) else "w"
    mode_ap  = "a" if os.path.exists(out_ap) else "w"

    total     = len(pending)
    type_dist = {}

    with open(out_de, mode_de, newline="", encoding="utf-8") as f_de, \
         open(out_ap, mode_ap, newline="", encoding="utf-8") as f_ap:

        writer_de = csv.DictWriter(f_de, fieldnames=out_cols)
        writer_ap = csv.DictWriter(f_ap, fieldnames=out_cols)
        if mode_de == "w": writer_de.writeheader()
        if mode_ap == "w": writer_ap.writeheader()

        for batch_start in range(0, len(pending), BATCH_SIZE_API):
            batch      = pending[batch_start: batch_start + BATCH_SIZE_API]
            batch_recs = [(r.get("title",""), r.get("abstract","")) for r in batch]
            results    = classify_batch(client, batch_recs)

            for rec, (ptype, conf) in zip(batch, results):
                pub_year = extract_pub_year(rec.get("pub_date", ""))
                type_dist[ptype] = type_dist.get(ptype, 0) + 1
                out_row = dict(rec)
                out_row["pub_year"]        = pub_year
                out_row["paper_type"]      = ptype
                out_row["type_confidence"] = conf
                if ptype in ("discourse", "evaluative"):
                    writer_de.writerow(out_row)
                else:
                    writer_ap.writerow(out_row)

            f_de.flush()
            f_ap.flush()

            done = batch_start + len(batch)
            if done % 500 == 0 or done >= total:
                pct      = done / total * 100
                dist_str = " | ".join(f"{k}:{v}" for k, v in sorted(type_dist.items()))
                print(f"  [{done:5d}/{total}] {pct:5.1f}%  {dist_str}")

            time.sleep(SLEEP)

    print(f"Batch {BATCH_ID} complete.")


if __name__ == "__main__":
    main()
