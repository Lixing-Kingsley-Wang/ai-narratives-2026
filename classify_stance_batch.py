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
# v2 = revised prompt re-classification. Original v1 preserved
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2_v2.csv")

N_BATCHES = int(os.environ.get("STANCE_N_BATCHES", "1"))

SYSTEM_PROMPT = """You are an expert classifier of academic medical literature. Your task is to classify the STANCE of medical journal articles toward AI/LLM technology in medicine. Read the title and abstract, then assign ONE of the following five stance labels.

=== STANCE DEFINITIONS ===

Alarm
  The paper is primarily CRITICAL or SKEPTICAL of AI. Emphasises dangers, failures, hallucinations, safety risks, ethical problems, or argues AI is not ready/safe for clinical use. Papers showing AI performs WORSE than clinicians = Alarm.
  Example: "ChatGPT fails safety standards for medication advice"

Caution
  Acknowledges both promise AND significant concerns, with the balance tilting toward concern. Recommends safeguards or further validation before deployment.
  Example: "Implications of LLMs for dental medicine" (mixed but concern-leaning)

Neutral
  The authors do not take a clear evaluative position on AI. Includes:
  - Methodology papers presenting algorithms/pipelines without endorsing AI broadly
  - Application papers using AI as a tool without evaluating AI itself
  - Bibliometric reviews, scoping reviews, workshop summaries, protocols
  - Performance benchmarks reporting metrics descriptively
  - Papers whose only positive/negative language appears in background framing

  Key diagnostic question: Do the authors themselves argue for or against AI's value in their conclusion? If they only describe, summarize, or report methodology without an evaluative interpretation, it is Neutral — even if the background contains positive framing.
  Example: "Performance benchmarking of segmentation algorithm"

Cautious Optimism
  BROADLY POSITIVE about AI with some caveats. Emphasises potential benefits, supports deployment with appropriate safeguards. May contain transformative-sounding language but ALSO acknowledges substantial caveats, limitations, or open challenges.
  Example: "AI in echocardiography: promising results, validation needed"

Advocacy
  STRONGLY and UNAMBIGUOUSLY pro-AI. Requires BOTH:
  (a) Transformative language (e.g., "revolutionize", "paradigm shift", "transform", "completely reinvent", "herald a new era") AND
  (b) Minimal or no acknowledged caveats.

  Strongly positive findings or endorsement language WITHOUT transformative claims are Cautious Optimism, not Advocacy. Transformative language WITH substantial caveats is also Cautious Optimism. Both conditions must hold for Advocacy.
  Example: "AI will revolutionise radiology within five years"

=== WHERE TO FIND THE AUTHORS' STANCE ===

Medical AI abstracts typically follow a structured pattern:
- BACKGROUND/OBJECTIVE/INTRODUCTION: sets up the topic. Often contains positive field-level framing ("AI is revolutionizing medicine", "transformative potential", "rapid advancements have shown promise"). This is the *convention* of the field, NOT the paper's stance. Do not classify based on background language alone.
- METHODS/RESULTS: describes what was done and found.
- CONCLUSION/DISCUSSION/FUTURE DIRECTIONS: where the authors interpret findings and take a position.

The stance you assign should reflect the authors' position as expressed in the CONCLUSION and DISCUSSION (typically the last 30-40% of the abstract). For evaluative studies, the stance comes from how the authors interpret their findings, not from background framing. For perspective/review papers, the stance comes from the explicit position the authors take at the end.

If the conclusion is descriptive, methodological, or scope-defining ("we present X", "we review Y", "this provides a framework for Z") and contains no explicit authorial evaluation of AI's value, classify as Neutral — regardless of how positive the background language is.

=== META-DISCOURSE / SURVEY PAPERS ===

Some papers measure attitudes, perceptions, knowledge, literacy, acceptance, or readiness toward AI among patients, students, clinicians, or other populations. These papers REPORT what surveyed populations think about AI; they do not themselves take a stance on AI.

For such papers:
- The findings of the survey (e.g., "70% of clinicians were positive about AI", "patients expressed concerns about data privacy") describe the population's views, NOT the authors' stance.
- The presence of words like "positive", "optimistic", "concerned", or "skeptical" in the conclusion typically describes the surveyed population.
- Classify these as Neutral by default and set meta_discourse to "yes".

Exception: If the authors editorialize in the conclusion or future-directions beyond reporting the findings — e.g., "These results urgently demand regulatory action" or "We strongly recommend immediate AI integration" — apply the rubric to that explicit authorial position (still set meta_discourse to "yes").

Common signals that a paper is meta-discourse:
- Title contains "perception", "attitude", "acceptance", "readiness", "literacy", "knowledge", "perspectives", "views"
- Methods describe a survey, questionnaire, interview, or cross-sectional attitudinal study
- Findings report what a sampled population thinks rather than what AI does

=== COMMON PITFALLS TO AVOID ===

1. BACKGROUND FRAMING: Sentences like "AI is revolutionizing medicine" or "transformative advances in AI" at the start of abstracts are field convention. They do NOT constitute the paper's stance.

2. WORD-LEVEL OVERREADING: A single occurrence of "transformative", "promising", or "revolutionary" in the background does not make a paper Advocacy or CO. The full abstract — especially the conclusion — must support the stance.

3. METHODOLOGICAL FEASIBILITY FINDINGS: Findings like "X was feasible" or "the algorithm achieved 80% accuracy" are descriptive results, not evaluative stances. Without the authors interpreting the feasibility as supporting deployment, these are Neutral, not CO.

4. ADVOCACY THRESHOLD: Strongly positive findings or measured endorsement language ("can outperform", "improves accuracy", "should be considered as adjunct") without transformative language are Cautious Optimism, not Advocacy. Advocacy requires both transformative claims AND minimal caveats — both conditions.

5. SURVEY FINDINGS ARE NOT AUTHORS' STANCE: When a paper measures attitudes, the surveyed population's views are NOT the authors' stance. The authors of an attitudinal survey are Neutral unless they editorialize beyond their findings.

=== KEY RULES ===

- Base classification only on title and abstract.
- If the paper tests AI and finds it performs WORSE than clinicians, code as Alarm.
- For papers showing AI better than clinicians, classify by the strength of the authors' interpretation: measured findings = CO; transformative framing + minimal caveats = Advocacy.
- Pick the stance that best reflects the OVERALL MESSAGE of the authors in their conclusion.

=== EXAMPLES ===

"ENT specialists vs ChatGPT: 1-0" → {"stance":"Alarm","confidence":"High","predictive_claim":"yes","meta_discourse":"no"}
"ChatGPT fails safety standards for medication advice" → {"stance":"Alarm","confidence":"High","predictive_claim":"no","meta_discourse":"no"}
"Implications of LLMs for dental medicine" (balanced, concern-leaning) → {"stance":"Caution","confidence":"High","predictive_claim":"no","meta_discourse":"no"}
"AI in echocardiography: promising results, validation needed" → {"stance":"Cautious Optimism","confidence":"High","predictive_claim":"no","meta_discourse":"no"}
"AI will transform radiology within five years" → {"stance":"Advocacy","confidence":"High","predictive_claim":"yes","meta_discourse":"no"}
"Performance benchmarking of segmentation algorithm" → {"stance":"Neutral","confidence":"High","predictive_claim":"no","meta_discourse":"no"}

=== OUTPUT FORMAT ===

Output field definitions:
- predictive_claim: explicit forward-looking claim about AI's future role (yes/no).
- meta_discourse: paper measures attitudes/perceptions/acceptance/literacy about AI in a population (yes/no). See META-DISCOURSE section above.

Respond ONLY with valid JSON in this exact format:
{"stance":"<Alarm|Caution|Neutral|Cautious Optimism|Advocacy>","confidence":"<High|Medium|Low>","predictive_claim":"<yes|no>","meta_discourse":"<yes|no>"}
"""


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
        return "FAILED", "Low", "no", "no", f"ERROR: {raw_orig[:100]}"

    stance = parsed.get("stance", "").strip()
    conf   = parsed.get("confidence", "Medium").strip()
    pred   = str(parsed.get("predictive_claim", "no")).strip().lower()
    meta   = str(parsed.get("meta_discourse", "no")).strip().lower()

    if stance not in VALID_STANCES:
        return "FAILED", "Low", "no", "no", f"ERROR: invalid stance {stance}"
    if conf not in VALID_CONFIDENCE:
        conf = "Medium"
    if pred in ("true", "yes"): pred = "yes"
    elif pred in ("false", "no"): pred = "no"
    else: pred = "no"
    if meta in ("true", "yes"): meta = "yes"
    elif meta in ("false", "no"): meta = "no"
    else: meta = "no"

    return stance, conf, pred, meta, raw


# ── retrieve a batch and append to output ─────────────────────────────────────
def write_batch_results(client, batch_id, records_by_pmid, done_pmids):
    in_cols = list(next(iter(records_by_pmid.values())).keys())
    # Match classify_stance.py output schema exactly
    out_cols = in_cols + ["pub_year", "stance", "stance_model",
                          "confidence", "predictive_claim", "meta_discourse", "stance_raw"]

    # Dedupe in_cols if pub_year is already in input (it is, from prefilter)
    if "pub_year" in in_cols:
        out_cols = in_cols + ["stance", "stance_model",
                              "confidence", "predictive_claim", "meta_discourse", "stance_raw"]

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
                stance, conf, pred, meta, raw = "FAILED", "Low", "no", "no", "ERROR: batch result not succeeded"
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
                    stance, conf, pred, meta, raw = "FAILED", "Low", "no", "no", "ERROR: empty content"
                    n_fail += 1
                else:
                    stance, conf, pred, meta, raw = parse_response(text)
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
            out_row["meta_discourse"]   = meta
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
