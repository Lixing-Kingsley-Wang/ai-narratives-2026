"""
Thematic classification via Anthropic Message Batches API
==========================================================

Same prompt and rubric as classify_themes.py (Sonnet 4.6), but uses the
Batch endpoint (50% discount, no rate limits). Runs only on records with
stance Alarm or Caution.

Reads:  output/classified_medical_Q1Q2.csv  (filtered to Alarm + Caution)
Writes: output/analysis/thematic_alarm.csv

State files:
  output/themes_batch_ids.txt
  output/themes_batch_processed.txt

Usage:
  python classify_themes_batch.py            # submit (if needed) or poll
  python classify_themes_batch.py force-submit
"""
import csv, json, time, os, sys, re, math
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv(override=True)

# ── constants (mirror classify_themes.py exactly) ─────────────────────────────
MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 150
VALID_THEMES = {
    "replacement", "hallucination", "safety_clinical", "ethics_bias",
    "cognitive", "education", "regulation", "existential",
    "data_privacy", "other",
}

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")
os.makedirs(ANALYSIS_DIR, exist_ok=True)

BATCH_IDS_PATH       = os.path.join(OUTPUT_DIR, "themes_batch_ids.txt")
BATCH_PROCESSED_PATH = os.path.join(OUTPUT_DIR, "themes_batch_processed.txt")

INPUT_PATH  = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")
OUTPUT_PATH = os.path.join(ANALYSIS_DIR, "thematic_alarm.csv")

N_BATCHES = int(os.environ.get("THEMES_N_BATCHES", "1"))

SYSTEM_PROMPT = """Identify concern themes in critical medical AI papers.

THEMES (return 1-3 most prominent):
- replacement: AI replacing physicians/clinicians/jobs; job displacement fears
- hallucination: AI errors, hallucinations, factual inaccuracies, unreliable outputs
- safety_clinical: patient safety risks, clinical harm, diagnostic errors
- ethics_bias: algorithmic bias, fairness, equity, ethical problems, discrimination
- cognitive: cognitive offloading, deskilling, over-reliance, loss of clinical skills
- education: medical education, student learning, training, residency, examinations
- regulation: governance, regulation, oversight, policy, liability, accountability
- existential: existential threat to medicine, disruption of doctor-patient relationship
- data_privacy: data privacy, security, consent, patient data misuse
- other: critical concern not fitting above

Return ONLY valid JSON: {"themes": ["theme1", "theme2"]}"""


def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        text += f"\nAbstract: {abstract[:400]}"
    return f"Identify concern themes:\n\n{text}"


def extract_pub_year(s):
    m = re.search(r"\b(20\d{2})\b", s or "")
    return m.group(1) if m else ""


# ── load helpers ──────────────────────────────────────────────────────────────
def load_done_pmids():
    if not os.path.exists(OUTPUT_PATH):
        return set()
    done = set()
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            done.add(r["pmid"])
    return done


def load_records():
    """Only Alarm + Caution records."""
    records_by_pmid = {}
    with open(INPUT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("stance") in ("Alarm", "Caution"):
                records_by_pmid[r["pmid"]] = r
    return records_by_pmid


def load_batch_ids():
    if not os.path.exists(BATCH_IDS_PATH):
        return []
    with open(BATCH_IDS_PATH) as f:
        return [line.strip() for line in f if line.strip()]


def save_batch_ids(ids):
    with open(BATCH_IDS_PATH, "w") as f:
        for bid in ids:
            f.write(bid + "\n")


def load_processed_ids():
    if not os.path.exists(BATCH_PROCESSED_PATH):
        return set()
    with open(BATCH_PROCESSED_PATH) as f:
        return set(line.strip() for line in f if line.strip())


def mark_processed(bid):
    with open(BATCH_PROCESSED_PATH, "a") as f:
        f.write(bid + "\n")


# ── submit ────────────────────────────────────────────────────────────────────
def submit_in_chunks(client, pending, n_chunks):
    chunk_size = math.ceil(len(pending) / n_chunks)
    print(f"Splitting {len(pending):,} records into {n_chunks} chunk(s) of ~{chunk_size:,}")

    batch_ids = []
    for i in range(n_chunks):
        chunk = pending[i * chunk_size : (i + 1) * chunk_size]
        if not chunk:
            break

        requests = []
        for r in chunk:
            prompt = build_prompt(r.get("title", ""), r.get("abstract", ""))
            requests.append({
                "custom_id": r["pmid"],
                "params": {
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": prompt}],
                },
            })

        batch = client.messages.batches.create(requests=requests)
        batch_ids.append(batch.id)
        print(f"  Batch {i+1}/{n_chunks}: {batch.id} ({len(chunk):,} reqs, status={batch.processing_status})")

    return batch_ids


# ── parse one Sonnet response into themes ─────────────────────────────────────
def parse_response(text):
    raw = text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        parsed = json.loads(raw, strict=False)
    except json.JSONDecodeError:
        return ["other"]
    themes = [t for t in parsed.get("themes", []) if t in VALID_THEMES]
    if not themes:
        themes = ["other"]
    return themes[:3]  # cap at 3 per prompt


# ── retrieve batch and append to output ───────────────────────────────────────
def write_batch_results(client, batch_id, records_by_pmid, done_pmids):
    in_cols = list(next(iter(records_by_pmid.values())).keys())
    out_cols = in_cols + ["themes", "theme_1", "theme_2", "theme_3"]

    mode = "a" if os.path.exists(OUTPUT_PATH) else "w"

    n_written = n_skip = 0
    theme_dist = {}

    with open(OUTPUT_PATH, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        if mode == "w":
            writer.writeheader()

        for result in client.messages.batches.results(batch_id):
            pmid = result.custom_id
            if pmid in done_pmids:
                n_skip += 1
                continue
            rec = records_by_pmid.get(pmid)
            if rec is None:
                continue

            if result.result.type != "succeeded":
                themes = ["other"]
            else:
                msg = result.result.message
                # Defensively extract text
                text = ""
                for block in (msg.content or []):
                    if getattr(block, "text", None):
                        text = block.text
                        break
                if not text:
                    themes = ["other"]
                else:
                    themes = parse_response(text)

            for t in themes:
                theme_dist[t] = theme_dist.get(t, 0) + 1

            out_row = dict(rec)
            out_row["themes"]  = "|".join(themes)
            out_row["theme_1"] = themes[0] if len(themes) > 0 else ""
            out_row["theme_2"] = themes[1] if len(themes) > 1 else ""
            out_row["theme_3"] = themes[2] if len(themes) > 2 else ""
            writer.writerow(out_row)
            done_pmids.add(pmid)
            n_written += 1

    print(f"    wrote: {n_written:,}  skip(dup)={n_skip}")
    print(f"    theme_dist: {theme_dist}")
    return n_written


# ── poll all; retrieve as each ends ───────────────────────────────────────────
def poll_and_retrieve(client, batch_ids, records_by_pmid, sleep_s=60):
    processed = load_processed_ids()
    pending = [b for b in batch_ids if b not in processed]
    print(f"Polling {len(pending)} batch(es), {len(processed)} already retrieved")

    while pending:
        statuses = []
        for bid in list(pending):
            b = client.messages.batches.retrieve(bid)
            statuses.append((bid, b.processing_status, b.request_counts))

        print(f"\n[poll @ {time.strftime('%H:%M:%S')}]")
        for bid, status, rc in statuses:
            short = bid[-14:]
            total = rc.succeeded + rc.errored + rc.canceled + rc.expired + rc.processing
            done_pct = ((rc.succeeded + rc.errored + rc.canceled + rc.expired) / total * 100) if total else 0
            print(f"  ...{short}: {status:<11}  succ={rc.succeeded:>5,}  "
                  f"proc={rc.processing:>5,}  err={rc.errored}  ({done_pct:.1f}%)")

        done_pmids = load_done_pmids()
        for bid, status, rc in statuses:
            if status == "ended":
                print(f"  → retrieving {bid[-14:]}...")
                write_batch_results(client, bid, records_by_pmid, done_pmids)
                mark_processed(bid)
                pending.remove(bid)

        if pending:
            time.sleep(sleep_s)

    print("\nAll batches retrieved.")


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    force_submit = len(sys.argv) > 1 and sys.argv[1] == "force-submit"
    client = Anthropic()
    records_by_pmid = load_records()
    done = load_done_pmids()
    pending = [r for pmid, r in records_by_pmid.items() if pmid not in done]
    print(f"Alarm+Caution corpus: {len(records_by_pmid):,}  done: {len(done):,}  pending: {len(pending):,}")

    existing_ids = load_batch_ids()

    if not existing_ids or force_submit:
        if not pending:
            print("Nothing pending; nothing to submit.")
            return
        ids = submit_in_chunks(client, pending, N_BATCHES)
        save_batch_ids(ids)
        print(f"\nSubmitted {len(ids)} batch(es). Saved to {BATCH_IDS_PATH}")
        print("Re-run this script to poll & retrieve results.")
        return

    print(f"Resuming from {len(existing_ids)} previously-submitted batch(es)")
    poll_and_retrieve(client, existing_ids, records_by_pmid)


if __name__ == "__main__":
    main()
