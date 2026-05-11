"""
Stance classification via Anthropic Message Batches API
========================================================

Same prompt and rubric as classify_stance.py (Sonnet 4.6, no abstract
truncation), but uses the Batch endpoint:
  • 50% discount on input/output tokens
  • No per-minute rate limits
  • Async — submit returns, results in 1-24h

Reads:  output/prefiltered_discourse_eval.csv  (16,759 records)
Writes: output/classified_medical_Q1Q2.csv

State files:
  output/stance_batch_ids.txt        — submitted batch_ids
  output/stance_batch_processed.txt  — already-retrieved batch_ids

Usage:
  python classify_stance_batch.py            # submit (if needed) or poll
  python classify_stance_batch.py force-submit
"""
import csv, json, time, os, sys, re, math
from anthropic import Anthropic
from dotenv import load_dotenv
# override=True forces .env to win over shell environment vars
load_dotenv(override=True)

# ── constants (mirror classify_stance.py exactly) ─────────────────────────────
MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 120
VALID_STANCES    = {"Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"}
VALID_CONFIDENCE = {"High", "Medium", "Low"}

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")
BATCH_IDS_PATH       = os.path.join(OUTPUT_DIR, "stance_batch_ids.txt")
BATCH_PROCESSED_PATH = os.path.join(OUTPUT_DIR, "stance_batch_processed.txt")

INPUT_PATH = os.path.join(OUTPUT_DIR, "prefiltered_discourse_eval.csv")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")

N_BATCHES = int(os.environ.get("STANCE_N_BATCHES", "1"))

SYSTEM_PROMPT = """Classify the stance of a medical AI article toward AI/LLM technology.

STANCES (Q1/Q2 journals use measured language — calibrate accordingly):
- Alarm: primarily critical/skeptical. Emphasises dangers, failures, hallucinations, safety risks, ethical problems, or argues AI is not ready. Papers showing AI performs WORSE than clinicians = Alarm.
- Caution: acknowledges both promise AND significant concerns, balance tilts toward concern. Recommends safeguards before deployment.
- Neutral: purely descriptive. Reports metrics without taking a position. No evaluative language.
- Cautious Optimism: broadly positive with caveats. Supports careful deployment.
- Advocacy: strongly pro-AI. Emphasises transformative potential, minimal caveats.

PREDICTIVE CLAIM: explicit forward-looking claim about AI's future role (yes/no).

EXAMPLES:
"ENT specialists vs ChatGPT: 1-0" → {"stance":"Alarm","confidence":"High","predictive_claim":"yes"}
"ChatGPT fails safety standards for medication advice" → {"stance":"Alarm","confidence":"High","predictive_claim":"no"}
"Implications of LLMs for dental medicine" (balanced, concern-leaning) → {"stance":"Caution","confidence":"High","predictive_claim":"no"}
"AI in echocardiography: promising results, validation needed" → {"stance":"Cautious Optimism","confidence":"High","predictive_claim":"no"}
"AI will transform radiology within five years" → {"stance":"Advocacy","confidence":"High","predictive_claim":"yes"}
"Performance benchmarking of segmentation algorithm" → {"stance":"Neutral","confidence":"High","predictive_claim":"no"}

KEY RULES:
- AI performs worse than humans = Alarm, not Neutral
- AI risks/ethics/governance as main topic = Alarm or Caution, not Neutral
- Do NOT default to Cautious Optimism

Return ONLY valid JSON: {"stance":"...","confidence":"...","predictive_claim":"..."}"""


def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        # Full abstract — Friday's edit removed the [:400] truncation
        text += f"\nAbstract: {abstract}"
    return text


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
            if r.get("stance") not in ("", "FAILED", None):
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


# ── parse one Sonnet response ─────────────────────────────────────────────────
def parse_response(text):
    raw = text.strip()
    raw_orig = raw
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        parsed = json.loads(raw, strict=False)
    except json.JSONDecodeError:
        return "FAILED", "Low", "no", f"ERROR: {raw_orig[:100]}"

    stance = parsed.get("stance", "").strip()
    conf   = parsed.get("confidence", "Medium").strip()
    pred   = parsed.get("predictive_claim", "no").strip().lower()

    if stance not in VALID_STANCES:
        return "FAILED", "Low", "no", f"ERROR: invalid stance {stance}"
    if conf not in VALID_CONFIDENCE:
        conf = "Medium"
    if pred not in ("yes", "no"):
        pred = "no"

    return stance, conf, pred, raw


# ── retrieve a batch and append to output ─────────────────────────────────────
def write_batch_results(client, batch_id, records_by_pmid, done_pmids):
    in_cols = list(next(iter(records_by_pmid.values())).keys())
    # Match classify_stance.py output schema exactly
    out_cols = in_cols + ["pub_year", "stance", "stance_model",
                          "confidence", "predictive_claim", "stance_raw"]

    # Dedupe in_cols if pub_year is already in input (it is, from prefilter)
    if "pub_year" in in_cols:
        out_cols = in_cols + ["stance", "stance_model",
                              "confidence", "predictive_claim", "stance_raw"]

    mode = "a" if os.path.exists(OUTPUT_PATH) else "w"

    n_written = n_skip = n_fail = 0
    stance_dist = {}

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
                stance, conf, pred, raw = "FAILED", "Low", "no", "ERROR: batch result not succeeded"
                n_fail += 1
            else:
                msg = result.result.message
                # Defensively extract text — some succeeded responses have empty content arrays
                text = ""
                for block in (msg.content or []):
                    if getattr(block, "text", None):
                        text = block.text
                        break
                if not text:
                    stance, conf, pred, raw = "FAILED", "Low", "no", "ERROR: empty content"
                    n_fail += 1
                else:
                    stance, conf, pred, raw = parse_response(text)
                    if stance == "FAILED":
                        n_fail += 1

            stance_dist[stance] = stance_dist.get(stance, 0) + 1

            out_row = dict(rec)
            if "pub_year" not in out_row:
                out_row["pub_year"] = extract_pub_year(rec.get("pub_date", ""))
            out_row["stance"]           = stance
            out_row["stance_model"]     = "sonnet"
            out_row["confidence"]       = conf
            out_row["predictive_claim"] = pred
            out_row["stance_raw"]       = raw

            writer.writerow(out_row)
            done_pmids.add(pmid)
            n_written += 1

    print(f"    wrote: {n_written:,}  skip(dup)={n_skip}  fails={n_fail}")
    print(f"    stance_dist: {stance_dist}")
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
            print(f"  ...{short}: {status:<11}  succ={rc.succeeded:>6,}  "
                  f"proc={rc.processing:>6,}  err={rc.errored}  ({done_pct:.1f}%)")

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
        ids = submit_in_chunks(client, pending, N_BATCHES)
        save_batch_ids(ids)
        print(f"\nSubmitted {len(ids)} batch(es). Saved to {BATCH_IDS_PATH}")
        print("Re-run this script to poll & retrieve results.")
        return

    print(f"Resuming from {len(existing_ids)} previously-submitted batch(es)")
    poll_and_retrieve(client, existing_ids, records_by_pmid)


if __name__ == "__main__":
    main()
