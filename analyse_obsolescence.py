"""
Obsolescence & Benchmark Replication Analysis — AI Narratives Study

Two analytical layers applied to classified_medical_Q1Q2.csv:

1. BENCHMARK REPLICATION FLAG
   Detects "can AI X answer questions about Y subspecialty" papers
   using title pattern matching. No API calls needed.

2. MODEL OBSOLESCENCE ANALYSIS
   Extracts named AI model from title/abstract, computes model age
   at publication (months since model release), correlates with stance.

Output:
  output/analysis/obsolescence_analysis.csv  — per-record flags
  output/analysis/model_age_vs_stance.csv    — aggregate table
  output/analysis/benchmark_replication.csv  — flagged papers only

Prints summary tables for immediate interpretation.
"""

import csv, re, os, sys
import collections
from datetime import date

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")
os.makedirs(ANALYSIS_DIR, exist_ok=True)

VALID_STANCES = {"Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"}

# ── Model release dates ────────────────────────────────────────────────────────
# (model_name_pattern, release_date, canonical_name)
MODEL_RELEASES = [
    # GPT family
    (r'\bGPT-?2\b',                          date(2019, 2, 14),  "GPT-2"),
    (r'\bGPT-?3(?:\.5)?\b|\bChatGPT\b',     date(2022, 11, 30), "GPT-3/3.5/ChatGPT"),
    (r'\bGPT-?4(?!o)\b',                     date(2023, 3, 14),  "GPT-4"),
    (r'\bGPT-?4o\b',                         date(2024, 5, 13),  "GPT-4o"),
    (r'\bGPT-?4o?\s*mini\b',                 date(2024, 7, 18),  "GPT-4o mini"),
    (r'\bo1\b|\bGPT-?o1\b',                  date(2024, 9, 12),  "o1"),
    # Google
    (r'\bBard\b',                             date(2023, 3, 21),  "Bard"),
    (r'\bGemini\b',                           date(2023, 12, 6),  "Gemini"),
    (r'\bMed-?PaLM\b',                        date(2022, 12, 26), "Med-PaLM"),
    (r'\bPaLM\b',                             date(2022, 4, 4),   "PaLM"),
    # Meta
    (r'\bLLaMA?[-\s]?2\b',                   date(2023, 7, 18),  "LLaMA-2"),
    (r'\bLLaMA?[-\s]?3\b',                   date(2024, 4, 18),  "LLaMA-3"),
    (r'\bLLaMA?\b',                           date(2023, 2, 24),  "LLaMA"),
    # Anthropic
    (r'\bClaude[-\s]?2\b',                   date(2023, 7, 11),  "Claude-2"),
    (r'\bClaude[-\s]?3\b',                   date(2024, 3, 4),   "Claude-3"),
    (r'\bClaude\b',                           date(2023, 3, 14),  "Claude"),
    # Microsoft
    (r'\bCopilot\b|\bBing\s*AI\b',           date(2023, 2, 7),   "Copilot/Bing"),
    # Other
    (r'\bFalcon\b',                           date(2023, 5, 23),  "Falcon"),
    (r'\bMistral\b',                          date(2023, 9, 27),  "Mistral"),
    (r'\bGemma\b',                            date(2024, 2, 21),  "Gemma"),
    (r'\bDeepSeek\b',                         date(2024, 1, 5),   "DeepSeek"),
]

# ── Benchmark replication patterns ────────────────────────────────────────────
# Titles matching these patterns are likely "can AI X do Y" papers

BENCHMARK_TITLE_PATTERNS = [
    # Interrogative can/does/is AI able patterns
    r'(?:can|does|is|are|could|would)\s+.{0,30}(?:chatgpt|gpt|llm|ai|claude|bard|gemini).{0,50}(?:answer|pass|perform|respond|address|solve|score|achieve)',
    r'(?:chatgpt|gpt[-\s]?\d|llm|claude|bard|gemini).{0,50}(?:answer|pass|perform|respond|address|solve|score|achieve).{0,50}(?:question|exam|test|quiz|board|certif)',
    # "Performance of X on Y" patterns
    r'performance\s+of\s+.{0,30}(?:chatgpt|gpt|llm|ai|claude|bard).{0,50}(?:exam|question|test|board|certif|quiz)',
    r'(?:chatgpt|gpt[-\s]?\d|llm).{0,50}(?:vs|versus|compared?\s+to|against).{0,50}(?:physician|doctor|specialist|expert|resident|student)',
    # Accuracy/ability assessment patterns
    r'(?:accuracy|ability|capability|performance)\s+of\s+(?:chatgpt|gpt|ai|llm)',
    r'(?:chatgpt|gpt[-\s]?\d|llm|ai).{0,30}(?:accuracy|ability|capability)\s+(?:in|on|for|to)',
    # Evaluation of named model on named specialty
    r'(?:evaluat|assess|test).{0,20}(?:chatgpt|gpt[-\s]?\d|llm|claude|bard|gemini).{0,50}(?:question|exam|quiz|board|certif)',
]

BENCHMARK_COMPILED = [re.compile(p, re.IGNORECASE) for p in BENCHMARK_TITLE_PATTERNS]

# Additional positive signals in abstract
BENCHMARK_ABSTRACT_SIGNALS = [
    r'(?:questions?\s+(?:from|about|related\s+to)|answered?\s+\d+\s+question)',
    r'(?:pass(?:ed|ing)?\s+(?:the|a|an)\s+\w+\s+exam)',
    r'(?:\d+\s+(?:multiple[- ]choice|mcq|mcqs)\s+question)',
]
BENCHMARK_ABSTRACT_COMPILED = [re.compile(p, re.IGNORECASE) for p in BENCHMARK_ABSTRACT_SIGNALS]


def is_benchmark_replication(title, abstract):
    """Returns True if paper is likely a benchmark replication study."""
    # Check title patterns
    title_match = any(p.search(title) for p in BENCHMARK_COMPILED)
    if not title_match:
        return False
    # Require at least one abstract signal for confirmation
    abstract_match = any(p.search(abstract or "") for p in BENCHMARK_ABSTRACT_COMPILED)
    return abstract_match


def extract_model(title, abstract):
    """Extract the primary AI model mentioned, return (canonical_name, release_date) or (None, None)."""
    text = f"{title} {abstract or ''}"
    for pattern, release_date, canonical in MODEL_RELEASES:
        if re.search(pattern, text, re.IGNORECASE):
            return canonical, release_date
    return None, None


def get_pub_year_month(r):
    """Extract publication year and approximate date from record."""
    pub_date = r.get("pub_date", "") or ""
    year_str  = r.get("pub_year", "") or ""

    if not year_str:
        m = re.search(r'\b(20\d{2})\b', pub_date)
        year_str = m.group() if m else ""

    month = 7  # default to mid-year if no month
    month_map = {
        "jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
        "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12,
    }
    for k, v in month_map.items():
        if k in pub_date.lower():
            month = v
            break

    try:
        return date(int(year_str), month, 15), year_str
    except:
        return None, year_str


def compute_model_age_months(pub_date_obj, release_date):
    """Months between model release and publication."""
    if not pub_date_obj or not release_date:
        return None
    delta = (pub_date_obj.year - release_date.year) * 12 + \
            (pub_date_obj.month - release_date.month)
    return max(0, delta)


def age_category(months):
    if months is None:
        return "unknown"
    if months <= 6:
        return "0-6m (current)"
    elif months <= 12:
        return "7-12m (recent)"
    elif months <= 24:
        return "13-24m (aging)"
    else:
        return "25m+ (obsolete)"


# ── main ───────────────────────────────────────────────────────────────────────
def main():
    input_path = os.path.join(OUTPUT_DIR, "classified_medical_Q1Q2.csv")
    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Obsolescence & Benchmark Replication Analysis")
    print(f"Input: {len(rows):,} records\n")

    # Process each record
    results = []
    benchmark_rows = []
    n_benchmark  = 0
    model_counts = collections.Counter()
    age_stance   = collections.defaultdict(lambda: collections.Counter())
    year_benchmark = collections.Counter()
    year_total     = collections.Counter()

    for r in rows:
        title    = r.get("title", "")
        abstract = r.get("abstract", "")
        stance   = r.get("stance", "")
        pub_date_obj, year_str = get_pub_year_month(r)

        # Benchmark replication
        is_bench = is_benchmark_replication(title, abstract)
        if is_bench:
            n_benchmark += 1
            if year_str and "2021" <= year_str <= "2026":
                year_benchmark[year_str] += 1

        if year_str and "2021" <= year_str <= "2026":
            year_total[year_str] += 1

        # Model extraction
        model_name, release_date = extract_model(title, abstract)
        age_months = compute_model_age_months(pub_date_obj, release_date)
        age_cat    = age_category(age_months)

        if model_name:
            model_counts[model_name] += 1
        if stance in VALID_STANCES:
            age_stance[age_cat][stance] += 1

        out_row = dict(r)
        out_row["is_benchmark_replication"] = "yes" if is_bench else "no"
        out_row["model_named"]              = model_name or ""
        out_row["model_release_date"]       = release_date.isoformat() if release_date else ""
        out_row["model_age_months"]         = age_months if age_months is not None else ""
        out_row["model_age_category"]       = age_cat
        results.append(out_row)

        if is_bench:
            benchmark_rows.append(out_row)

    # ── Print results ──────────────────────────────────────────────────────────

    print(f"{'='*60}")
    print(f"1. BENCHMARK REPLICATION PAPERS")
    print(f"{'='*60}")
    print(f"Total flagged: {n_benchmark:,} / {len(rows):,} "
          f"({n_benchmark/len(rows)*100:.1f}%)\n")

    print(f"By year (% of that year's papers):")
    for year in sorted(year_total.keys()):
        n    = year_benchmark.get(year, 0)
        t    = year_total[year]
        print(f"  {year}: {n:4d} / {t:5d}  ({n/t*100:.1f}%)")

    # Stance of benchmark papers
    bench_stances = collections.Counter(
        r.get("stance","") for r in benchmark_rows
        if r.get("stance","") in VALID_STANCES
    )
    non_bench_stances = collections.Counter(
        r.get("stance","") for r in results
        if r.get("stance","") in VALID_STANCES
        and r.get("is_benchmark_replication") == "no"
    )
    total_bench     = sum(bench_stances.values())
    total_non_bench = sum(non_bench_stances.values())

    print(f"\nStance — benchmark vs non-benchmark:")
    print(f"{'Stance':<22} {'Benchmark%':>12} {'Non-bench%':>12}")
    print("-"*48)
    for s in ["Alarm","Caution","Neutral","Cautious Optimism","Advocacy"]:
        bp  = bench_stances.get(s,0)/total_bench*100     if total_bench     else 0
        nbp = non_bench_stances.get(s,0)/total_non_bench*100 if total_non_bench else 0
        print(f"{s:<22} {bp:>11.1f}% {nbp:>11.1f}%")

    print(f"\n{'='*60}")
    print(f"2. MODEL OBSOLESCENCE ANALYSIS")
    print(f"{'='*60}")

    n_with_model = sum(1 for r in results if r["model_named"])
    print(f"Records with named AI model: {n_with_model:,} / {len(rows):,} "
          f"({n_with_model/len(rows)*100:.1f}%)\n")

    print(f"Most cited models:")
    for model, n in model_counts.most_common(12):
        print(f"  {n:5d}  {model}")

    print(f"\nStance by model age at publication:")
    age_order = ["0-6m (current)", "7-12m (recent)",
                 "13-24m (aging)", "25m+ (obsolete)", "unknown"]
    print(f"{'Age category':<22} {'N':>6}  {'Critical%':>10}  "
          f"{'Alarm%':>7}  {'CautOpt%':>9}")
    print("-"*60)

    age_rows = []
    for age_cat in age_order:
        data  = age_stance[age_cat]
        total = sum(data.values())
        if total == 0:
            continue
        alarm  = data.get("Alarm",0)
        caut   = data.get("Caution",0)
        crit   = (alarm+caut)/total*100
        opt    = data.get("Cautious Optimism",0)/total*100
        print(f"{age_cat:<22} {total:>6}  {crit:>10.1f}  "
              f"{alarm/total*100:>7.1f}  {opt:>9.1f}")
        age_rows.append({
            "age_category":age_cat, "total":total,
            "Alarm":alarm, "Caution":caut,
            "Neutral":data.get("Neutral",0),
            "Cautious Optimism":data.get("Cautious Optimism",0),
            "Advocacy":data.get("Advocacy",0),
            "critical_pct":round(crit,2),
            "alarm_pct":round(alarm/total*100,2),
        })

    # GPT-3.5 published late — specific finding
    late_gpt35 = [
        r for r in results
        if "GPT-3" in r.get("model_named","")
        and r.get("model_age_months","") != ""
        and int(r["model_age_months"]) >= 18
    ]
    if late_gpt35:
        print(f"\nGPT-3.5 papers published ≥18 months after release: {len(late_gpt35)}")
        late_stances = collections.Counter(r.get("stance","") for r in late_gpt35
                                           if r.get("stance","") in VALID_STANCES)
        lt = sum(late_stances.values())
        for s in ["Alarm","Caution","Neutral","Cautious Optimism","Advocacy"]:
            n = late_stances.get(s,0)
            print(f"  {s:<22} {n:4d}  ({n/lt*100:.1f}%)")

    # ── Save outputs ───────────────────────────────────────────────────────────
    out_cols = list(rows[0].keys()) + [
        "is_benchmark_replication", "model_named",
        "model_release_date", "model_age_months", "model_age_category"
    ]

    path1 = os.path.join(ANALYSIS_DIR, "obsolescence_analysis.csv")
    with open(path1, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        w.writeheader()
        w.writerows(results)
    print(f"\nSaved: {path1}")

    path2 = os.path.join(ANALYSIS_DIR, "model_age_vs_stance.csv")
    if age_rows:
        with open(path2, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(age_rows[0].keys()))
            w.writeheader()
            w.writerows(age_rows)
        print(f"Saved: {path2}")

    path3 = os.path.join(ANALYSIS_DIR, "benchmark_replication.csv")
    if benchmark_rows:
        with open(path3, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=out_cols)
            w.writeheader()
            w.writerows(benchmark_rows)
        print(f"Saved: {path3}")
        print(f"\nSample benchmark replication titles:")
        for r in benchmark_rows[:10]:
            print(f"  [{r.get('pub_year','')}] {r.get('title','')[:100]}")


if __name__ == "__main__":
    main()
