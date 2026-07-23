"""
Specialty classification via Anthropic Message Batches API (Haiku 4.5)
======================================================================

For each record in the v1 classified corpus, assign one of 18 clinical
specialties from title + abstract.

Reads:  output/classified_medical_Q1Q2.csv  (v1, 16,759 records)
Writes: output/specialty_classifications.csv

State files:
  output/specialty_batch_ids.txt        — submitted batch_ids
  output/specialty_batch_processed.txt  — already-retrieved batch_ids

CLI:
  python analysis/classify_specialty.py sample          # Step 2.2 sanity check (20 sync calls)
  python analysis/classify_specialty.py                 # submit if no IDs, else poll
  python analysis/classify_specialty.py force-submit    # force resubmit
"""
import csv, json, math, os, random, re, sys, time
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv(override=True)

# v1 corpus is gitignored and lives in the parent checkout.
# Classification outputs go into THIS worktree so they can be committed.
PARENT_OUTPUT = "/Users/kingslywang/repos/ai-narratives-2026/output"
HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE_OUTPUT = os.path.abspath(os.path.join(HERE, "..", "output"))

INPUT_PATH           = os.path.join(PARENT_OUTPUT,   "classified_medical_Q1Q2.csv")
OUTPUT_PATH          = os.path.join(WORKTREE_OUTPUT, "specialty_classifications.csv")
BATCH_IDS_PATH       = os.path.join(PARENT_OUTPUT,   "specialty_batch_ids.txt")
BATCH_PROCESSED_PATH = os.path.join(PARENT_OUTPUT,   "specialty_batch_processed.txt")

MODEL      = "claude-haiku-4-5"
MAX_TOKENS = 80
N_BATCHES  = int(os.environ.get("SPECIALTY_N_BATCHES", "1"))

VALID_SPECIALTIES = {
    "Radiology / Diagnostic Imaging",
    "Pathology / Laboratory Medicine",
    "Cardiology",
    "Oncology",
    "Surgery",
    "Ophthalmology",
    "Dermatology",
    "Neurology / Neuroscience",
    "Mental Health / Psychiatry",
    "Internal Medicine / Primary Care",
    "Emergency Medicine / Critical Care",
    "Pediatrics",
    "Obstetrics / Gynecology",
    "Dentistry",
    "Medical Informatics / Digital Health",
    "Nursing",
    "Medical Education",
    "Multidisciplinary / Other",
}
VALID_CONFIDENCE = {"low", "medium", "high"}

SPECIALTY_PROMPT = """You are classifying medical research papers by clinical specialty.

Read the title and abstract, then assign ONE of the following 18 categories:

1. Radiology / Diagnostic Imaging
2. Pathology / Laboratory Medicine
3. Cardiology
4. Oncology
5. Surgery (general and surgical subspecialties — orthopedic, ENT/otolaryngology, urology, neurosurgery, plastic, etc.)
6. Ophthalmology
7. Dermatology
8. Neurology / Neuroscience (non-surgical)
9. Mental Health / Psychiatry
10. Internal Medicine / Primary Care / Family Medicine (includes gastroenterology, endocrinology, rheumatology, nephrology, pulmonology, infectious disease — all non-surgical internal subspecialties)
11. Emergency Medicine / Critical Care
12. Pediatrics
13. Obstetrics / Gynecology
14. Dentistry
15. Medical Informatics / Digital Health / AI Methodology
16. Nursing
17. Medical Education
18. Multidisciplinary / Other

CLASSIFICATION RULES:

- **Single best-fit by dominant specialty.** Classify by the clinical specialty being applied to or studied, not by the AI methodology used.
  - "ChatGPT for cardiology questions" → Cardiology, not Medical Informatics.
  - "Deep learning for chest X-ray classification" → Radiology.
  - "Survey of medical students' AI literacy" → Medical Education.

- **Medical Informatics (#15)** is reserved for papers ABOUT AI itself — frameworks, taxonomies, methodology development, benchmarks not tied to a specific clinical specialty, or general "AI in medicine" overviews that don't focus on one clinical domain.

- **Multidisciplinary / Other (#18)** is for:
  - Papers spanning 2+ specialties with no dominant focus
  - Bibliometric reviews across medicine
  - Veterinary medicine
  - Rehabilitation medicine, anesthesiology when not clearly fitting elsewhere
  - Public health when not clearly Internal Medicine
  - Any paper genuinely cross-cutting without a clinical anchor

- **Pediatrics (#12)** takes priority over organ system. "AI for pediatric cardiology" → Pediatrics.

- **Oncology (#4)** takes priority over organ system EXCEPT when the paper is about a single non-cancer aspect of that organ system. "AI for breast cancer detection" → Oncology. "AI for breast lesion characterization (benign and malignant)" → Radiology if imaging-focused.

- **Surgical subspecialties** all fold into Surgery (#5). Don't split out orthopedics, ENT, urology, plastic surgery as separate.

OUTPUT FORMAT:

Respond ONLY with valid JSON. Use the SHORT category name (everything before the first parenthetical) exactly as shown:
- "Radiology / Diagnostic Imaging"
- "Pathology / Laboratory Medicine"
- "Cardiology"
- "Oncology"
- "Surgery"
- "Ophthalmology"
- "Dermatology"
- "Neurology / Neuroscience"
- "Mental Health / Psychiatry"
- "Internal Medicine / Primary Care"
- "Emergency Medicine / Critical Care"
- "Pediatrics"
- "Obstetrics / Gynecology"
- "Dentistry"
- "Medical Informatics / Digital Health"
- "Nursing"
- "Medical Education"
- "Multidisciplinary / Other"

Format:
{"specialty": "<short name>", "confidence": "<low|medium|high>"}

Respond with the JSON object and NOTHING ELSE. No code fences, no rationale, no preamble. Just the JSON.
"""


def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        text += f"\nAbstract: {abstract}"
    return text


# ── state helpers ─────────────────────────────────────────────────────────────
def load_done_pmids():
    if not os.path.exists(OUTPUT_PATH):
        return set()
    done = set()
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("specialty") not in ("", "FAILED", None):
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


# ── parse ──────────────────────────────────────────────────────────────────────
_JSON_OBJ_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


def parse_response(text):
    raw = (text or "").strip()
    m = _JSON_OBJ_RE.search(raw)
    if not m:
        return "FAILED", "low", f"ERROR: no JSON found {raw[:140]}"
    snippet = m.group(0)
    try:
        parsed = json.loads(snippet, strict=False)
    except json.JSONDecodeError:
        return "FAILED", "low", f"ERROR: bad JSON {raw[:140]}"

    spec = (parsed.get("specialty") or "").strip()
    conf = (parsed.get("confidence") or "medium").strip().lower()

    if spec not in VALID_SPECIALTIES:
        return "FAILED", "low", f"ERROR: invalid specialty {spec!r}"
    if conf not in VALID_CONFIDENCE:
        conf = "medium"
    return spec, conf, snippet


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
            requests.append({
                "custom_id": r["pmid"],
                "params": {
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "system": SPECIALTY_PROMPT,
                    "messages": [{"role": "user",
                                  "content": build_prompt(r.get("title",""), r.get("abstract",""))}],
                },
            })
        batch = client.messages.batches.create(requests=requests)
        batch_ids.append(batch.id)
        print(f"  Batch {i+1}/{n_chunks}: {batch.id} ({len(chunk):,} reqs, status={batch.processing_status})")
    return batch_ids


# ── retrieve ──────────────────────────────────────────────────────────────────
OUT_COLS = ["pmid", "title", "pub_year", "journal", "specialty", "confidence", "specialty_raw"]


def write_batch_results(client, batch_id, records_by_pmid, done_pmids):
    mode = "a" if os.path.exists(OUTPUT_PATH) else "w"
    n_written = n_skip = n_fail = 0
    dist = {}

    with open(OUTPUT_PATH, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUT_COLS)
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
                spec, conf, raw = "FAILED", "low", "ERROR: batch result not succeeded"
                n_fail += 1
            else:
                msg = result.result.message
                text = ""
                for block in (msg.content or []):
                    if getattr(block, "text", None):
                        text = block.text
                        break
                if not text:
                    spec, conf, raw = "FAILED", "low", "ERROR: empty content"
                    n_fail += 1
                else:
                    spec, conf, raw = parse_response(text)
                    if spec == "FAILED":
                        n_fail += 1

            dist[spec] = dist.get(spec, 0) + 1
            writer.writerow({
                "pmid": pmid,
                "title": rec.get("title", ""),
                "pub_year": rec.get("pub_year", ""),
                "journal": rec.get("journal", ""),
                "specialty": spec,
                "confidence": conf,
                "specialty_raw": raw,
            })
            done_pmids.add(pmid)
            n_written += 1

    print(f"    wrote: {n_written:,}  skip(dup)={n_skip}  fails={n_fail}")
    print(f"    dist: {dist}")
    return n_written


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


# ── sanity-check (Step 2.2): synchronous on 20 random records ────────────────
def sample_sync(client, records_by_pmid, n=20, seed=42):
    rng = random.Random(seed)
    pmids = sorted(records_by_pmid.keys())
    sample_pmids = rng.sample(pmids, n)

    print(f"\n=== Specialty classifier sanity check — {n} random records (seed={seed}) ===")
    print(f"Model: {MODEL}\n")
    dist = {}
    n_fail = 0
    for i, pmid in enumerate(sample_pmids, 1):
        r = records_by_pmid[pmid]
        title = r.get("title", "")
        abstract = r.get("abstract", "") or ""
        prompt = build_prompt(title, abstract)

        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=MAX_TOKENS,
                system=SPECIALTY_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text if resp.content else ""
            spec, conf, raw = parse_response(text)
        except Exception as e:
            spec, conf, raw = "FAILED", "low", f"EXCEPTION: {e}"

        if spec == "FAILED":
            n_fail += 1
        dist[spec] = dist.get(spec, 0) + 1

        title_show = title if len(title) <= 110 else title[:107] + "..."
        print(f"[{i:2}] pmid={pmid}  {spec}  ({conf})")
        print(f"     {title_show}")
        if spec == "FAILED":
            print(f"     RAW: {raw[:120]}")

    print("\n=== Distribution ===")
    for spec, count in sorted(dist.items(), key=lambda x: -x[1]):
        print(f"  {count:2}  {spec}")
    print(f"\nFAILED: {n_fail}/{n}")


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    client = Anthropic()
    records_by_pmid = load_records()
    done = load_done_pmids()
    pending = [r for pmid, r in records_by_pmid.items() if pmid not in done]
    print(f"Corpus: {len(records_by_pmid):,}  done: {len(done):,}  pending: {len(pending):,}")

    if "sample" in args:
        sample_sync(client, records_by_pmid, n=20, seed=42)
        return

    force_submit = "force-submit" in args
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
