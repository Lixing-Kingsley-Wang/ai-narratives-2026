"""
A2 · Prefilter re-run on title + FULL abstract (JMIR R1 Batch 2a; D1, X2)
==========================================================================

Copy of prefilter_batch.py (commit 9c79cd5). Classification behaviour changes
ONLY in two places, as specified by the Batch 2a protocol:
  1. build_prompt sends the full abstract (no [:300] truncation); title only
     when the abstract is empty.
  2. Failure handling: a non-succeeded batch result, empty response, JSON
     parse failure, or a paper_type outside {discourse, evaluative,
     application} is recorded as FAILED — never defaulted to application.
     FAILED records are resubmitted once in a second batch.
Unchanged: MODEL, MAX_TOKENS, SYSTEM_PROMPT (SHA-256 asserted equal to
prefilter_batch.py at runtime), temperature not set, Message Batches API,
type_confidence normalisation.
Infrastructure changes: inputs read from the main checkout's output/,
all outputs and state go to revision_r1/outputs/A2/, raw results are kept
(gzip jsonl), the API key is read from the main checkout's .env without
touching os.environ, and a token-count/cost gate runs before submission.

Usage (from revision_r1/scripts/):
  python a2_prefilter_fullabstract_batch.py count        # 1,000-record token count + cost projection
  python a2_prefilter_fullabstract_batch.py submit       # round 1 (refuses if projection > ceiling)
  python a2_prefilter_fullabstract_batch.py poll         # poll + retrieve round 1
  python a2_prefilter_fullabstract_batch.py resubmit     # round 2: FAILED records once
  python a2_prefilter_fullabstract_batch.py poll2        # poll + retrieve round 2
  python a2_prefilter_fullabstract_batch.py finalize     # merged labels, cross-tabs, actual cost
"""
import csv, json, time, os, sys, re, math, gzip, hashlib, ast
from pathlib import Path
from anthropic import Anthropic
from dotenv import dotenv_values

# ── constants (identical to prefilter_batch.py) ───────────────────────────────
MODEL       = "claude-haiku-4-5-20251001"
MAX_TOKENS  = 120
VALID_TYPES = {"discourse", "evaluative", "application"}

# ── paths (R1) ────────────────────────────────────────────────────────────────
REPO       = Path(__file__).resolve().parents[2]
MAIN       = Path("/Users/kingslywang/Documents/科研/ai-narratives-2026")
DATA_ROOT  = Path(os.environ.get("R1_DATA_ROOT", str(MAIN / "output")))
OUTPUT_DIR = REPO / "revision_r1" / "outputs" / "A2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_PATH = DATA_ROOT / "filtered_medical_all_Q1Q2.csv"
PROD_DE    = DATA_ROOT / "prefiltered_discourse_eval.csv"
PROD_AP    = DATA_ROOT / "prefiltered_application.csv"
N_BATCHES  = 4

# ── pricing (claude-haiku-4-5, Anthropic list price, USD per MTok) ────────────
PRICE_IN, PRICE_OUT, BATCH_DISCOUNT = 1.00, 5.00, 0.5
COST_CEILING = 60.0
OUT_TOKENS_ASSUMED = 40   # conservative per-reply output tokens for the projection

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
        text += f"\nAbstract: {abstract}"          # R1: full abstract, no truncation
    return f"Classify this paper:\n\n{text}"


def extract_pub_year(s):
    m = re.search(r"\b(20\d{2})\b", s or "")
    return m.group(1) if m else ""


def assert_prompt_identical():
    tree = ast.parse((REPO / "prefilter_batch.py").read_text())
    orig = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(getattr(t, "id", None) == "SYSTEM_PROMPT" for t in n.targets))
    h1 = hashlib.sha256(orig.encode()).hexdigest()
    h2 = hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()
    assert h1 == h2, "SYSTEM_PROMPT differs from prefilter_batch.py"
    return h2


def make_client():
    key = dotenv_values(MAIN / ".env").get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY not found in main checkout .env")
    return Anthropic(api_key=key, max_retries=8)


def load_records():
    with open(INPUT_PATH, encoding="utf-8") as f:
        return {r["pmid"]: r for r in csv.DictReader(f)}


def request_for(r):
    return {"custom_id": r["pmid"],
            "params": {"model": MODEL, "max_tokens": MAX_TOKENS, "system": SYSTEM_PROMPT,
                       "messages": [{"role": "user", "content": build_prompt(r.get("title", ""), r.get("abstract", ""))}]}}


# ── parse one Haiku response (R1: failures are FAILED, never application) ─────
def parse_response(text):
    raw = text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        parsed = json.loads(raw, strict=False)
    except json.JSONDecodeError:
        return "FAILED", "", "json_parse_error"
    if not isinstance(parsed, dict):
        return "FAILED", "", "json_not_object"
    ptype = str(parsed.get("paper_type", "")).strip().lower()
    if ptype not in VALID_TYPES:
        return "FAILED", "", "paper_type_out_of_vocabulary"
    conf = str(parsed.get("type_confidence", "Medium")).strip()
    if conf not in ("High", "Medium", "Low"):
        conf = "Medium"
    return ptype, conf, ""


# ── state helpers ─────────────────────────────────────────────────────────────
def ids_path(rnd):       return OUTPUT_DIR / f"batch_ids_round{rnd}.txt"
def processed_path(rnd): return OUTPUT_DIR / f"batch_processed_round{rnd}.txt"
def raw_path(rnd):       return OUTPUT_DIR / f"raw_round{rnd}.jsonl.gz"
def parsed_path(rnd):    return OUTPUT_DIR / f"parsed_round{rnd}.csv"


def read_lines(p):
    return [l.strip() for l in open(p) if l.strip()] if p.exists() else []


def submit(client, recs, rnd):
    if read_lines(ids_path(rnd)):
        sys.exit(f"round {rnd} already submitted ({ids_path(rnd)})")
    n_chunks = N_BATCHES if rnd == 1 else 1
    size = math.ceil(len(recs) / n_chunks)
    ids = []
    for i in range(n_chunks):
        chunk = recs[i * size:(i + 1) * size]
        if not chunk:
            break
        b = client.messages.batches.create(requests=[request_for(r) for r in chunk])
        ids.append(b.id)
        with open(ids_path(rnd), "a") as f:
            f.write(b.id + "\n")
        print(f"  round {rnd} batch {i+1}/{n_chunks}: {len(chunk):,} requests, status={b.processing_status}", flush=True)
    return ids


def write_results(client, bid, rnd, records):
    exists = parsed_path(rnd).exists()
    n = n_fail = 0
    with gzip.open(raw_path(rnd), "at", encoding="utf-8") as fr, \
         open(parsed_path(rnd), "a", newline="", encoding="utf-8") as fp:
        w = csv.DictWriter(fp, fieldnames=["pmid", "year", "label_fullabstract", "type_confidence",
                                           "failed", "fail_reason", "input_tokens", "output_tokens", "round"])
        if not exists:
            w.writeheader()
        for result in client.messages.batches.results(bid):
            fr.write(result.model_dump_json() + "\n")
            pmid = result.custom_id
            in_t = out_t = 0
            if result.result.type != "succeeded":
                label, conf, reason = "FAILED", "", f"batch_{result.result.type}"
            else:
                msg = result.result.message
                in_t, out_t = msg.usage.input_tokens, msg.usage.output_tokens
                text = ""
                for block in (msg.content or []):
                    if getattr(block, "text", None):
                        text = block.text
                        break
                if not text:
                    label, conf, reason = "FAILED", "", "empty_response"
                else:
                    label, conf, reason = parse_response(text)
            rec = records.get(pmid, {})
            w.writerow({"pmid": pmid, "year": extract_pub_year(rec.get("pub_date", "")),
                        "label_fullabstract": label, "type_confidence": conf,
                        "failed": int(label == "FAILED"), "fail_reason": reason,
                        "input_tokens": in_t, "output_tokens": out_t, "round": rnd})
            n += 1
            n_fail += label == "FAILED"
    print(f"    retrieved {bid[-12:]}: {n:,} results, FAILED={n_fail}", flush=True)


def poll(client, rnd, records, sleep_s=120):
    ids = read_lines(ids_path(rnd))
    done = set(read_lines(processed_path(rnd)))
    pending = [b for b in ids if b not in done]
    while pending:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] round {rnd}", flush=True)
        for bid in list(pending):
            b = client.messages.batches.retrieve(bid)
            rc = b.request_counts
            print(f"  ...{bid[-12:]} {b.processing_status:<11} succ={rc.succeeded:,} err={rc.errored} "
                  f"exp={rc.expired} canc={rc.canceled} proc={rc.processing:,}", flush=True)
            if b.processing_status == "ended":
                write_results(client, bid, rnd, records)
                with open(processed_path(rnd), "a") as f:
                    f.write(bid + "\n")
                pending.remove(bid)
        if pending:
            time.sleep(sleep_s)
    print(f"round {rnd}: all batches retrieved", flush=True)


def cost(in_tok, out_tok):
    return (in_tok * PRICE_IN + out_tok * PRICE_OUT) / 1e6 * BATCH_DISCOUNT


def count(client, records, n_sample=1000, seed=42):
    import random
    rng = random.Random(seed)
    pm = sorted(records, key=int)
    sample = rng.sample(pm, n_sample)
    toks = []
    for i, p in enumerate(sample, 1):
        r = request_for(records[p])["params"]
        res = client.messages.count_tokens(model=MODEL, system=r["system"], messages=r["messages"])
        toks.append(res.input_tokens)
        if i % 100 == 0:
            print(f"  counted {i}/{n_sample}", flush=True)
    n = len(records)
    mean = sum(toks) / len(toks)
    proj_in = mean * n
    proj_out = OUT_TOKENS_ASSUMED * n
    proj = {"sample_n": n_sample, "seed": seed, "population_n": n, "mean_input_tokens": mean,
            "min_input_tokens": min(toks), "max_input_tokens": max(toks),
            "projected_input_tokens": proj_in, "assumed_output_tokens_per_request": OUT_TOKENS_ASSUMED,
            "projected_output_tokens": proj_out, "price_per_mtok_in": PRICE_IN, "price_per_mtok_out": PRICE_OUT,
            "batch_discount": BATCH_DISCOUNT, "projected_cost_usd": cost(proj_in, proj_out),
            "ceiling_usd": COST_CEILING}
    (OUTPUT_DIR / "cost_projection.json").write_text(json.dumps(proj, indent=2))
    with open(OUTPUT_DIR / "count_tokens_sample.csv", "w") as f:
        f.write("sample_index,input_tokens\n")
        for i, t in enumerate(toks):
            f.write(f"{i},{t}\n")
    print(json.dumps(proj, indent=2))


def actual_cost():
    tot_in = tot_out = 0
    for rnd in (1, 2):
        if parsed_path(rnd).exists():
            with open(parsed_path(rnd)) as f:
                for r in csv.DictReader(f):
                    tot_in += int(r["input_tokens"] or 0)
                    tot_out += int(r["output_tokens"] or 0)
    return tot_in, tot_out, cost(tot_in, tot_out)


def finalize(records):
    import pandas as pd
    prod = pd.concat([pd.read_csv(PROD_DE, dtype=str, keep_default_na=False, usecols=["pmid", "paper_type"]),
                      pd.read_csv(PROD_AP, dtype=str, keep_default_na=False, usecols=["pmid", "paper_type"])])
    r1 = pd.read_csv(parsed_path(1), dtype=str, keep_default_na=False)
    assert r1["pmid"].is_unique and len(r1) == len(records), "round 1 incomplete or duplicated"
    merged = r1.set_index("pmid")
    if parsed_path(2).exists():
        r2 = pd.read_csv(parsed_path(2), dtype=str, keep_default_na=False).set_index("pmid")
        merged.loc[r2.index, ["label_fullabstract", "type_confidence", "failed", "fail_reason", "round"]] = \
            r2[["label_fullabstract", "type_confidence", "failed", "fail_reason", "round"]]
    merged = merged.reset_index()
    merged["label_production"] = merged["pmid"].map(dict(zip(prod["pmid"], prod["paper_type"])))
    out = merged[["pmid", "year", "label_production", "label_fullabstract", "type_confidence", "failed",
                  "fail_reason", "round"]]
    out.to_csv(OUTPUT_DIR / "a2_fullabstract_labels.csv", index=False)
    tot_in, tot_out, usd = actual_cost()
    (OUTPUT_DIR / "actual_cost.json").write_text(json.dumps(
        {"input_tokens": tot_in, "output_tokens": tot_out, "cost_usd": usd}, indent=2))
    print(f"final FAILED: {int(out['failed'].astype(int).sum())}; actual cost ${usd:.2f}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    h = assert_prompt_identical()
    print(f"SYSTEM_PROMPT sha256 {h[:16]}… identical to prefilter_batch.py", flush=True)
    records = load_records()
    print(f"Corpus: {len(records):,}", flush=True)
    if cmd == "finalize":
        return finalize(records)
    client = make_client()
    if cmd == "count":
        count(client, records)
    elif cmd == "submit":
        proj = json.loads((OUTPUT_DIR / "cost_projection.json").read_text())
        if proj["projected_cost_usd"] > COST_CEILING:
            sys.exit(f"projected ${proj['projected_cost_usd']:.2f} exceeds ceiling ${COST_CEILING}; ask before submitting")
        submit(client, [records[p] for p in sorted(records, key=int)], 1)
    elif cmd == "poll":
        poll(client, 1, records)
    elif cmd == "resubmit":
        _, _, spent = actual_cost()
        failed = [r["pmid"] for r in csv.DictReader(open(parsed_path(1))) if r["failed"] == "1"]
        print(f"round-1 FAILED: {len(failed)}; spent so far ${spent:.2f}", flush=True)
        if not failed:
            return
        if spent + cost(len(failed) * 2000, len(failed) * MAX_TOKENS) > COST_CEILING:
            sys.exit("resubmission could exceed the ceiling; ask before submitting")
        submit(client, [records[p] for p in failed], 2)
    elif cmd == "poll2":
        poll(client, 2, records)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
