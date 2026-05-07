"""
Legal Corpus Pipeline — AI Narratives Comparative Study
Runs the full pipeline on the legal corpus after Scopus retrieval.

Usage:
  python run_legal_pipeline.py           # full pipeline
  python run_legal_pipeline.py filter    # SJR filter only
  python run_legal_pipeline.py prefilter # discourse/eval filter only
  python run_legal_pipeline.py classify  # stance classification only
  python run_legal_pipeline.py compare   # comparison analysis only

Prerequisites:
  1. python fetch_scopus_legal.py        # retrieve from Scopus
  2. Download SJR law journal CSVs from scimagojr.com
     - Filter by Subject Area: Law
     - Save as input/sjr/sjr_law_YYYY.csv for each year
  3. Run this script
"""

import csv, os, sys, re, json, time
import asyncio
import collections
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
load_dotenv()
import anthropic as _anthropic_module

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")
SJR_DIR      = os.path.join(BASE_DIR, "input", "sjr")

VALID_STANCES = {"Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"}
YEARS         = list(range(2021, 2027))

# ── SJR filter for legal corpus ────────────────────────────────────────────────
STOPWORDS = {"the","a","an","of","in","and","for","on","with","its","by","to","from"}

def normalise(t):
    t = t.lower().strip()
    t = re.sub(r"\(.*?\)", "", t)
    t = re.sub(r":.*$", "", t)
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    words = [w for w in t.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(words).strip()


def load_sjr_law(year):
    """Load SJR for law journals from general SJR file.
    Filters by Categories column containing 'Law' (exact subcategory).
    Excludes 'Management, Monitoring, Policy and Law' (too broad).
    """
    for fname in [f"sjr_law_{year}.csv", f"sjr_{year}.csv"]:
        path = os.path.join(SJR_DIR, fname)
        if os.path.exists(path):
            title_map = {}
            with open(path, encoding="utf-8-sig") as f:
                for row in csv.DictReader(f, delimiter=";"):
                    q      = row.get("SJR Best Quartile","").strip()
                    title  = row.get("Title","").strip()
                    cats   = row.get("Categories","")

                    # Check for 'Law' or 'Issues, Ethics and Legal Aspects' category
                    # but NOT 'Management, Monitoring, Policy and Law' (too broad)
                    cat_parts = [c.strip() for c in cats.split(";")]
                    is_law = any(
                        ("law" in c.lower() or "legal aspects" in c.lower())
                        and "management, monitoring" not in c.lower()
                        for c in cat_parts
                    )

                    if is_law and title and q in ("Q1","Q2","Q3"):
                        title_map[normalise(title)] = q

            print(f"  SJR law {year} ({fname}): {len(title_map)} law journals loaded")
            return title_map

    print(f"  WARNING: No SJR file found for {year}")
    return {}


def filter_legal_corpus():
    input_path   = os.path.join(OUTPUT_DIR, "raw_legal_all.csv")
    out_q1q2     = os.path.join(OUTPUT_DIR, "filtered_legal_Q1Q2.csv")
    out_q3       = os.path.join(OUTPUT_DIR, "filtered_legal_Q3.csv")
    out_unmatched= os.path.join(OUTPUT_DIR, "filtered_legal_unmatched.csv")

    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        print("Run fetch_scopus_legal.py first.")
        return False

    with open(input_path, encoding="utf-8") as f:
        records = list(csv.DictReader(f))
    print(f"\nSJR Filter — Legal Corpus")
    print(f"Input: {len(records):,} records")

    sjr_cache = {str(y): load_sjr_law(y) for y in YEARS}

    q1q2, q3, unmatched = [], [], []
    for rec in records:
        year      = rec.get("year","")[:4]
        title_map = sjr_cache.get(year, sjr_cache.get("2024",{}))
        journal   = normalise(rec.get("journal",""))
        quartile  = title_map.get(journal)

        rec["sjr_quartile"] = quartile or ""
        if quartile in ("Q1","Q2"):
            q1q2.append(rec)
        elif quartile == "Q3":
            q3.append(rec)
        else:
            unmatched.append(rec)

    out_cols = list(records[0].keys()) + ["sjr_quartile"] if records else []
    for path, rows, label in [(out_q1q2,q1q2,"Q1/Q2"), (out_q3,q3,"Q3"),
                               (out_unmatched,unmatched,"Unmatched")]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=out_cols)
            w.writeheader()
            w.writerows(rows)
        print(f"  {label}: {len(rows):,} → {os.path.basename(path)}")

    eligible = len(q1q2) + len(q3)
    print(f"  Match rate: {(len(q1q2)+len(q3))/len(records)*100:.1f}%")
    return True


# ── prefilter for legal corpus ─────────────────────────────────────────────────
PREFILTER_SYSTEM = """Classify legal journal articles into categories based on AI engagement.

- discourse: AI/LLM is the MAIN SUBJECT. Paper debates AI's legal implications, regulation, liability, rights, governance, or impact on legal practice. Must be primarily ABOUT AI in law.
- evaluative: Paper TESTS or ASSESSES an AI legal tool and draws conclusions about its reliability or fitness for legal use.
- application: Paper USES AI as a method for legal research/analysis. AI is a tool, not the subject. When in doubt = application.

Return ONLY valid JSON: {"paper_type": "...", "type_confidence": "..."}"""


async def prefilter_legal():
    input_path = os.path.join(OUTPUT_DIR, "filtered_legal_Q1Q2.csv")
    out_de     = os.path.join(OUTPUT_DIR, "prefiltered_legal_discourse_eval.csv")
    out_ap     = os.path.join(OUTPUT_DIR, "prefiltered_legal_application.csv")

    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        return False

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print('ERROR: ANTHROPIC_API_KEY not set. Run: $env:ANTHROPIC_API_KEY="sk-ant-..."')
        return False
    client = AsyncAnthropic(api_key=api_key)
    with open(input_path, encoding="utf-8") as f:
        all_records = list(csv.DictReader(f))

    processed = set()
    for path in (out_de, out_ap):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    processed.add(row["pmid"])

    pending = [r for r in all_records if r["pmid"] not in processed]
    print(f"\nPre-Filter — Legal Corpus")
    print(f"Input: {len(all_records):,} | Pending: {len(pending):,}")

    if not pending:
        print("Already complete.")
        return True

    out_cols = list(all_records[0].keys()) + ["pub_year","paper_type","type_confidence"]
    mode_de  = "a" if os.path.exists(out_de) else "w"
    mode_ap  = "a" if os.path.exists(out_ap) else "w"

    sem   = asyncio.Semaphore(5)
    total = len(pending)
    done  = 0
    dist  = {}
    start = time.time()

    async def classify_one(rec):
        title    = rec.get("title","")
        abstract = rec.get("abstract","")
        prompt   = f"Title: {title}"
        if abstract.strip():
            prompt += f"\nAbstract: {abstract[:300]}"
        async with sem:
            for attempt in range(1, 4):
                try:
                    resp = await client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=80,
                        system=PREFILTER_SYSTEM,
                        messages=[{"role":"user","content":f"Classify:\n\n{prompt}"}]
                    )
                    raw = resp.content[0].text.strip()
                    # Extract JSON from anywhere in response
                    json_match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
                    if not json_match:
                        raise ValueError("No JSON found")
                    parsed = json.loads(json_match.group(), strict=False)
                    ptype  = parsed.get("paper_type","").strip().lower()
                    conf   = parsed.get("type_confidence","Medium").strip()
                    if ptype not in {"discourse","evaluative","application"}:
                        ptype = "application"
                    if conf not in ("High","Medium","Low"):
                        conf = "Medium"
                    return rec, ptype, conf
                except Exception as e:
                    if attempt < 3:
                        await asyncio.sleep(3)
        return rec, "application", "Low"

    with open(out_de, mode_de, newline="", encoding="utf-8") as f_de, \
         open(out_ap, mode_ap, newline="", encoding="utf-8") as f_ap:
        wde = csv.DictWriter(f_de, fieldnames=out_cols)
        wap = csv.DictWriter(f_ap, fieldnames=out_cols)
        if mode_de == "w": wde.writeheader()
        if mode_ap == "w": wap.writeheader()

        CHUNK = 50
        for cs in range(0, total, CHUNK):
            chunk   = pending[cs:cs+CHUNK]
            results = await asyncio.gather(*[classify_one(r) for r in chunk])
            for rec, ptype, conf in results:
                m = re.search(r'\b(20\d{2})\b', rec.get("pub_date","") or "")
                out_row = dict(rec)
                out_row["pub_year"]        = m.group() if m else ""
                out_row["paper_type"]      = ptype
                out_row["type_confidence"] = conf
                dist[ptype] = dist.get(ptype,0) + 1
                if ptype in ("discourse","evaluative"):
                    wde.writerow(out_row)
                else:
                    wap.writerow(out_row)
            f_de.flush(); f_ap.flush()
            done += len(chunk)
            elapsed = time.time()-start
            rate    = done/elapsed if elapsed else 0
            eta     = (total-done)/rate/60 if rate else 0
            print(f"  [{done:5d}/{total}] {done/total*100:5.1f}%  "
                  f"{' | '.join(f'{k}:{v}' for k,v in sorted(dist.items()))}  ETA:{eta:.0f}min")

    n_de = dist.get("discourse",0)+dist.get("evaluative",0)
    n_ap = dist.get("application",0)
    print(f"\nComplete. Discourse+Eval: {n_de} ({n_de/total*100:.1f}%) | "
          f"Application: {n_ap} ({n_ap/total*100:.1f}%)")
    return True


# ── stance classification for legal corpus ─────────────────────────────────────
STANCE_SYSTEM = """Classify the stance of a legal journal article toward AI/LLM technology.

STANCES (legal discourse uses measured academic language — calibrate accordingly):
- Alarm: primarily critical/skeptical of AI in law. Emphasises dangers, due process risks, bias, unreliability, threats to justice, or argues AI is not ready for legal deployment.
- Caution: acknowledges both promise AND significant concerns. Recommends safeguards, oversight, or further validation before legal deployment.
- Neutral: purely descriptive. Reports on AI legal developments without evaluative stance.
- Cautious Optimism: broadly positive about AI in law with caveats. Supports careful adoption.
- Advocacy: strongly pro-AI in legal contexts. Emphasises efficiency, access to justice benefits, minimal caveats.

PREDICTIVE CLAIM: explicit forward-looking claim about AI's future role in law (yes/no).

EXAMPLES:
"AI judges threaten due process: a constitutional analysis" → {"stance":"Alarm","confidence":"High","predictive_claim":"yes"}
"Algorithmic bias in criminal sentencing: empirical evidence" → {"stance":"Alarm","confidence":"High","predictive_claim":"no"}
"ChatGPT and legal research: opportunities and risks" → {"stance":"Caution","confidence":"High","predictive_claim":"no"}
"Machine learning for contract review: validation study" → {"stance":"Cautious Optimism","confidence":"High","predictive_claim":"no"}
"AI will democratise access to legal services" → {"stance":"Advocacy","confidence":"High","predictive_claim":"yes"}

Return ONLY valid JSON: {"stance":"...","confidence":"...","predictive_claim":"..."}"""


async def classify_legal():
    input_path  = os.path.join(OUTPUT_DIR, "prefiltered_legal_discourse_eval.csv")
    output_path = os.path.join(OUTPUT_DIR, "classified_legal_Q1Q2.csv")

    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        return False

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print('ERROR: ANTHROPIC_API_KEY not set.')
        return False
    client = AsyncAnthropic(api_key=api_key)
    with open(input_path, encoding="utf-8") as f:
        all_records = list(csv.DictReader(f))

    processed = set()
    if os.path.exists(output_path):
        with open(output_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("stance") not in ("","FAILED",None):
                    processed.add(row["pmid"])

    pending = [r for r in all_records if r["pmid"] not in processed]
    print(f"\nStance Classification — Legal Corpus")
    print(f"Input: {len(all_records):,} | Pending: {len(pending):,}")

    if not pending:
        print("Already complete.")
        return True

    out_cols = list(all_records[0].keys()) + ["stance","confidence","predictive_claim"]
    mode     = "a" if processed else "w"
    sem      = asyncio.Semaphore(5)
    total    = len(pending)
    done     = 0
    dist     = {}
    start    = time.time()

    async def classify_one(rec):
        title    = rec.get("title","")
        abstract = rec.get("abstract","")
        prompt   = f"Title: {title}"
        if abstract.strip():
            prompt += f"\nAbstract: {abstract[:400]}"
        async with sem:
            for attempt in range(1, 4):
                try:
                    resp = await client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=120,
                        system=STANCE_SYSTEM,
                        messages=[{"role":"user","content":prompt}]
                    )
                    raw = resp.content[0].text.strip()
                    json_match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
                    if not json_match:
                        raise ValueError("No JSON found")
                    parsed = json.loads(json_match.group(), strict=False)
                    stance = parsed.get("stance","").strip()
                    conf   = parsed.get("confidence","Medium").strip()
                    pred   = parsed.get("predictive_claim","no").strip().lower()
                    if stance not in VALID_STANCES:
                        raise ValueError(f"Invalid: {stance}")
                    return rec, stance, conf, pred
                except Exception as e:
                    if attempt < 3:
                        await asyncio.sleep(5)
        return rec, "FAILED", "Low", "no"

    with open(output_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        if mode == "w": writer.writeheader()

        CHUNK = 50
        for cs in range(0, total, CHUNK):
            chunk   = pending[cs:cs+CHUNK]
            results = await asyncio.gather(*[classify_one(r) for r in chunk])
            for rec, stance, conf, pred in results:
                dist[stance] = dist.get(stance,0)+1
                out_row = dict(rec)
                out_row["stance"]           = stance
                out_row["confidence"]       = conf
                out_row["predictive_claim"] = pred
                writer.writerow(out_row)
            f.flush()
            done += len(chunk)
            elapsed = time.time()-start
            rate    = done/elapsed if elapsed else 0
            eta     = (total-done)/rate/60 if rate else 0
            print(f"  [{done:5d}/{total}] {done/total*100:5.1f}%  "
                  f"{' | '.join(f'{k}:{v}' for k,v in sorted(dist.items()) if k!='FAILED')}  "
                  f"ETA:{eta:.0f}min")

    print(f"\nClassification complete.")
    return True


# ── final comparison: medicine vs law ─────────────────────────────────────────
def compare_medicine_law():
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    def load_by_year(path, year_field="pub_year"):
        if not os.path.exists(path):
            return {}
        data = collections.defaultdict(lambda: collections.Counter())
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                year   = row.get(year_field,"")
                if not year:
                    m = re.search(r'\b(20\d{2})\b', row.get("pub_date","") or "")
                    year = m.group() if m else ""
                stance = row.get("stance","")
                if year and "2021" <= year <= "2025" and stance in VALID_STANCES:
                    data[year][stance] += 1
        return data

    med  = load_by_year(os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv"))
    law  = load_by_year(os.path.join(OUTPUT_DIR, "classified_legal_Q1Q2.csv"))

    if not law:
        print("Legal classified output not found. Run full pipeline first.")
        return

    print(f"\n{'='*70}")
    print(f"MEDICINE vs LEGAL SCHOLARSHIP — STANCE COMPARISON")
    print(f"{'='*70}")
    print(f"{'Year':<6} {'Domain':<12} {'N':>6}  {'Critical%':>10}  "
          f"{'Alarm%':>7}  {'CautOpt%':>9}")
    print("-"*55)

    out_rows = []
    for year in sorted(set(list(med.keys()) + list(law.keys()))):
        for label, data in [("Medicine", med), ("Law", law)]:
            ydata = data.get(year, {})
            total = sum(ydata.values())
            if total == 0:
                continue
            alarm  = ydata.get("Alarm",0)
            caut   = ydata.get("Caution",0)
            crit   = (alarm+caut)/total*100
            opt    = ydata.get("Cautious Optimism",0)/total*100
            print(f"{year:<6} {label:<12} {total:>6}  {crit:>10.1f}  "
                  f"{alarm/total*100:>7.1f}  {opt:>9.1f}")
            out_rows.append({
                "year":year, "domain":label, "total":total,
                "critical_pct":round(crit,2),
                "alarm_pct":round(alarm/total*100,2),
                "cautious_optimism_pct":round(opt,2),
            })
        print()

    out_path = os.path.join(ANALYSIS_DIR, "medicine_vs_law_stance.csv")
    if out_rows:
        with open(out_path,"w",newline="",encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
            w.writeheader()
            w.writerows(out_rows)
        print(f"Saved: {out_path}")


# ── entry point ────────────────────────────────────────────────────────────────
async def main_async():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("filter","all"):
        if not filter_legal_corpus():
            return

    if mode in ("prefilter","all"):
        if not await prefilter_legal():
            return

    if mode in ("classify","all"):
        await classify_legal()

    if mode in ("compare","all"):
        compare_medicine_law()


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
