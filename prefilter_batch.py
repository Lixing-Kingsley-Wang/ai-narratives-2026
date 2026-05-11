"""
Prefilter via Anthropic Message Batches API — multi-batch parallel version
==========================================================================

Splits the pending corpus into N parallel batches (default 5) and submits
them simultaneously. This raises the chance that *some* batch slots get
picked up quickly even if a single 95K batch sits in queue. Results are
written incrementally as each batch finishes — partial progress survives
restart.

State files in output/:
  prefilter_batch_ids.txt        — one batch_id per line (all submitted)
  prefilter_batch_processed.txt  — batch_ids whose results have been written

Idempotent:
  • First run: splits, submits N batches, saves ids, exits.
  • Subsequent runs: polls all batches; retrieves each as it ends; writes
    results into prefiltered_*.csv. Skip any pmid already written.
  • Re-running after partial completion is safe — picks up where we left off.

Usage:
  python prefilter_batch.py                # submit (if needed) or poll
  python prefilter_batch.py force-submit   # force NEW submission (rare)

Optional env: PREFILTER_N_BATCHES (default 5)
"""
import csv, json, time, os, sys, re, math
from anthropic import Anthropic
from dotenv import load_dotenv
# override=True forces .env to win over shell environment vars
load_dotenv(override=True)

# ── constants (mirror prefilter.py exactly) ───────────────────────────────────
MODEL       = "claude-haiku-4-5-20251001"
MAX_TOKENS  = 120
VALID_TYPES = {"discourse", "evaluative", "application"}

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")
BATCH_IDS_PATH       = os.path.join(OUTPUT_DIR, "prefilter_batch_ids.txt")
BATCH_PROCESSED_PATH = os.path.join(OUTPUT_DIR, "prefilter_batch_processed.txt")

INPUT_PATH = os.path.join(OUTPUT_DIR, "filtered_medical_all_Q1Q2.csv")
OUT_DE     = os.path.join(OUTPUT_DIR, "prefiltered_discourse_eval.csv")
OUT_AP     = os.path.join(OUTPUT_DIR, "prefiltered_application.csv")

N_BATCHES = int(os.environ.get("PREFILTER_N_BATCHES", "5"))

SYSTEM_PROMPT = """You are classifying medical journal articles into one of three categories based on whether and how they engage with artificial intelligence (AI) as a subject.

CATEGORIES:

- discourse: AI/LLM is the MAIN SUBJECT of discussion. The paper reflects on, debates, or analyses AI's role, safety, ethics, implications, governance, risks, or future in medicine. Includes editorials, perspectives, opinion pieces, and narrative reviews WHERE THE CENTRAL TOPIC IS AI ITSELF.

- evaluative: The paper TESTS or BENCHMARKS a specific AI system (especially LLMs like ChatGPT, GPT-4) and draws explicit conclusions about its accuracy, safety, reliability, limitations, or clinical readiness.

- application: The paper USES AI/ML as a technical tool to solve a clinical problem. AI is a method, not the subject. When in doubt, classify as application.

CRITICAL RULES:
- Only classify as discourse if AI/LLM is clearly the CENTRAL topic
- Only classify as evaluative if there is explicit testing of an AI system with clinical conclusions
- Everything else = application

Return ONLY valid JSON: {"paper_type": "...", "type_confidence": "..."}
No preamble, no explanation."""


def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        text += f"\nAbstract: {abstract[:300]}"
    return f"Classify this paper:\n\n{text}"


def extract_pub_year(s):
    m = re.search(r"\b(20\d{2})\b", s or "")
    return m.group(1) if m else ""


# ── load helpers ──────────────────────────────────────────────────────────────
def load_done_pmids():
    done = set()
    for path in (OUT_DE, OUT_AP):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    done.add(r["pmid"])
    return done


def load_records():
    records_by_pmid = {}
    with open(INPUT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
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


# ── submit N parallel batches ─────────────────────────────────────────────────
def submit_in_chunks(client, pending, n_chunks):
    chunk_size = math.ceil(len(pending) / n_chunks)
    print(f"Splitting {len(pending):,} records into {n_chunks} chunks of ~{chunk_size:,}")

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


# ── parse one Haiku response ──────────────────────────────────────────────────
def parse_response(text):
    raw = text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        parsed = json.loads(raw, strict=False)
    except json.JSONDecodeError:
        return "application", "Low"
    ptype = parsed.get("paper_type", "").strip().lower()
    if ptype not in VALID_TYPES:
        ptype = "application"
    conf = parsed.get("type_confidence", "Medium").strip()
    if conf not in ("High", "Medium", "Low"):
        conf = "Medium"
    return ptype, conf


# ── retrieve a single completed batch and append to outputs ───────────────────
def write_batch_results(client, batch_id, records_by_pmid, done_pmids):
    in_cols = list(next(iter(records_by_pmid.values())).keys())
    out_cols = in_cols + ["pub_year", "paper_type", "type_confidence"]

    mode_de = "a" if os.path.exists(OUT_DE) else "w"
    mode_ap = "a" if os.path.exists(OUT_AP) else "w"

    n_de = n_ap = n_err = n_skip = 0
    type_dist = {}

    with open(OUT_DE, mode_de, newline="", encoding="utf-8") as f_de, \
         open(OUT_AP, mode_ap, newline="", encoding="utf-8") as f_ap:
        writer_de = csv.DictWriter(f_de, fieldnames=out_cols)
        writer_ap = csv.DictWriter(f_ap, fieldnames=out_cols)
        if mode_de == "w":
            writer_de.writeheader()
        if mode_ap == "w":
            writer_ap.writeheader()

        for result in client.messages.batches.results(batch_id):
            pmid = result.custom_id
            if pmid in done_pmids:
                n_skip += 1
                continue
            rec = records_by_pmid.get(pmid)
            if rec is None:
                n_err += 1
                continue

            if result.result.type != "succeeded":
                n_err += 1
                ptype, conf = "application", "Low"
            else:
                msg = result.result.message
                # Defensively extract text — some succeeded responses have empty content arrays
                text = ""
                for block in (msg.content or []):
                    if getattr(block, "text", None):
                        text = block.text
                        break
                if not text:
                    n_err += 1
                    ptype, conf = "application", "Low"
                else:
                    ptype, conf = parse_response(text)

            type_dist[ptype] = type_dist.get(ptype, 0) + 1

            out_row = dict(rec)
            out_row["pub_year"]        = extract_pub_year(rec.get("pub_date", ""))
            out_row["paper_type"]      = ptype
            out_row["type_confidence"] = conf

            if ptype in ("discourse", "evaluative"):
                writer_de.writerow(out_row)
                n_de += 1
            else:
                writer_ap.writerow(out_row)
                n_ap += 1
            done_pmids.add(pmid)

    print(f"    wrote: de={n_de:,}  app={n_ap:,}  skip(dup)={n_skip}  err={n_err}  "
          f"types={type_dist}")
    return n_de + n_ap


# ── poll all batches; retrieve as each ends ───────────────────────────────────
def poll_and_retrieve(client, batch_ids, records_by_pmid, sleep_s=60):
    processed = load_processed_ids()
    pending = [b for b in batch_ids if b not in processed]
    print(f"Polling {len(pending)} batch(es), {len(processed)} already retrieved")

    while pending:
        statuses = []
        for bid in list(pending):
            b = client.messages.batches.retrieve(bid)
            statuses.append((bid, b.processing_status, b.request_counts))

        # Print summary
        print(f"\n[poll @ {time.strftime('%H:%M:%S')}]")
        for bid, status, rc in statuses:
            short = bid[-14:]
            total = rc.succeeded + rc.errored + rc.canceled + rc.expired + rc.processing
            done_pct = ((rc.succeeded + rc.errored + rc.canceled + rc.expired) / total * 100) if total else 0
            print(f"  ...{short}: {status:<11}  succ={rc.succeeded:>6,}  "
                  f"proc={rc.processing:>6,}  err={rc.errored}  ({done_pct:.1f}%)")

        # Retrieve any newly-ended batches
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
    print(f"Corpus: {len(records_by_pmid):,}  done: {len(done):,}  pending: {len(pending):,}")

    existing_ids = load_batch_ids()

    if not existing_ids or force_submit:
        if not pending:
            print("Nothing pending; nothing to submit.")
            return
        if force_submit and existing_ids:
            print("force-submit: ignoring existing batch ids in file")
        ids = submit_in_chunks(client, pending, N_BATCHES)
        save_batch_ids(ids)
        print(f"\nSubmitted {len(ids)} batches. Saved to {BATCH_IDS_PATH}")
        print("Re-run this script to poll & retrieve results.")
        return

    print(f"Resuming from {len(existing_ids)} previously-submitted batch(es)")
    poll_and_retrieve(client, existing_ids, records_by_pmid)


if __name__ == "__main__":
    main()
