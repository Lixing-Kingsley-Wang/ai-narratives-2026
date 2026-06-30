# METHODS SOURCE-OF-TRUTH
## AI Narratives in Medicine — Temporal Bibliometric Analysis (2021–April 2026)

> **Purpose.** Single authoritative reference for the Methods section of the manuscript. Every prompt, codebook, model setting, and library version below is extracted *verbatim* from committed code across the repository's branches. Where the repository is silent, the entry reads **NOT FOUND IN REPO**. Do not infer.
>
> **Reading the entries.** Each item lists: (a) file path; (b) branch(es) where the file lives; (c) the most-relevant commit hash; (d) verbatim quotation of code or prompt in fenced blocks. Where multiple versions exist across branches, the *canonical* version (the one that produced the reported numbers in the manuscript) is labelled explicitly; deprecated variants are listed but flagged.
>
> **Document compiled:** 2026-05-09 (revised after retroactive commits of v2 / Q7 / specialty / 300-record validation / robustness work). **Document branch when written:** `prompt-revision-v2`.
>
> **Retroactive-commit note.** This document records the state after three commits on `prompt-revision-v2`:
> 1. `9c79cd5` — Saturday: prefilter + stance v1 + themes via Batch API (canonical for manuscript).
> 2. `2559e6b` — Stance v2 + v1/v2 comparison artifacts (supplementary, prompt-revision-v2 branch only — explicitly not for merge to `main` or any `analysis-session-*`).
> 3. `95fdc36` — Q7 failure-mode pipeline + 300-record stance validation outputs + specialty classifications + repo-root `robustness.py`. **These items were generated during analysis sessions 2/4/5 and the validation work but were not initially committed on their respective branches; they are retroactively committed here so the manuscript has a single auditable provenance.** If the analysis pipeline is later re-run from one of the `analysis-session-*` branches, regenerate from there or push these files back to those branches directly.

---

## Branch inventory

| Branch | Role | Latest relevant commit | Notes |
|---|---|---|---|
| `main` | Dan Poenaru's original v1.0 pipeline | `8500d89` | Initial commit of fetch/filter/classify/analyse scripts |
| `friday-corpus-build` | Corpus rebuild (Friday–Saturday work) | `9c79cd5` | Reverted Friday's GPT-5/4o/4.5 expansion; Apr 2026 PDAT cap; Batch API classifications |
| `analysis-session-1` | Bootstrap/robustness scaffolding | `8553c4d` | Introduces `analysis/robustness.py` |
| `analysis-session-2` | Specialty + regional analyses | `a30aaf7` | Adds `analysis/classify_specialty.py`, region/specialty temporal runs (contains both "session 2" and "session 3" per project note) |
| `analysis-session-4` | FDA AI/ML device proxy + adoption | `c6b9092` | Adds `analysis/run_specialty_aiadoption.py` and FDA panel→specialty mapping |
| `analysis-session-5` | Q7 failure-mode re-classification | `88fc832` | Adds `classify_q7_failuremode.py`; relocates `robustness.py` from `analysis/` to repo root |
| `prompt-revision-v2` *(HEAD)* | Current canonical for corpus + stance v1/v2 + themes + Q7 + specialty + validation | `95fdc36` | Adds: stance prompt v2 (commit `2559e6b`, supplementary only); retroactively committed Q7 pipeline, 300-record stance validation outputs, specialty classifications, and `robustness.py` at root (commit `95fdc36`) |

**Canonicity for reported numbers.** Where a measurement has multiple instrument versions:
- **Corpus + prefilter + stance v1 (canonical) + themes**: `prompt-revision-v2` at commit `9c79cd5` is canonical. Equivalent to `friday-corpus-build` at the same commit.
- **Stance v2 (supplementary)**: `prompt-revision-v2` at commit `2559e6b`. v2 is a sensitivity analysis only and is NOT to be merged into `main` or any `analysis-session-*` branch. The manuscript's primary reported stance numbers are v1.
- **300-record stance validation (κ)**: `prompt-revision-v2` at commit `95fdc36` (`output/validation/kappa_report.md`).
- **Specialty assignment**: `analysis-session-2` has the `classify_specialty.py` script (commit `a30aaf7`); the canonical specialty *outputs* (`output/specialty_classifications.csv`) are committed on `prompt-revision-v2` at commit `95fdc36`.
- **Country / affiliation type**: `main` (commit `8500d89`); inherited unchanged through all branches.
- **FDA device proxy**: `analysis-session-4` is canonical (and is the *only* branch with the runner script; the source CSV is still uncommitted).
- **Q7 re-classifier**: `analysis-session-5` had the original `classify_q7_failuremode.py` script (commit `88fc832`); the canonical Q7 *pipeline and outputs* (Q7 phase scripts, analyses, figures) are now also committed on `prompt-revision-v2` at commit `95fdc36`.
- **Bootstrap / stats**: `analysis-session-1+` (`analysis/robustness.py`); same logic on `analysis-session-5` and now on `prompt-revision-v2` at repo-root `robustness.py` (commit `95fdc36`).

---

## 1. Corpus construction

### 1a. PubMed query, date range, date field

**File:** `fetch_pubmed_medical.py`
**Branches with canonical content:** `main`, `friday-corpus-build`, `prompt-revision-v2`, all `analysis-session-*`
**Canonical commit:** `841c99b` (revert of Friday's GPT additions; unchanged through `9c79cd5`)

**Verbatim `QUERY_TEMPLATE` (canonical):**

```python
QUERY_TEMPLATE = (
    '("artificial intelligence"[MeSH] OR "machine learning"[MeSH] OR '
    '"deep learning"[tiab] OR "large language model"[tiab] OR '
    '"large language models"[tiab] OR "generative AI"[tiab] OR '
    '"generative artificial intelligence"[tiab] OR ChatGPT[tiab] OR '
    '"GPT-4"[tiab] OR "GPT-3"[tiab] OR GPT4[tiab] OR '
    '"foundation model"[tiab] OR "foundation models"[tiab] OR '
    '"natural language processing"[MeSH]) '
    'AND (medicine[sb] OR "patients"[tiab] OR "clinical"[tiab] OR '
    '"physician"[tiab] OR "surgeon"[tiab] OR "hospital"[tiab] OR '
    '"diagnosis"[tiab] OR "treatment"[tiab] OR "healthcare"[tiab] OR '
    '"health care"[tiab]) '
    'AND ("{year_start}"[PDAT] : "{year_end}"[PDAT]) '
    'AND ("journal article"[pt] OR "editorial"[pt] OR "review"[pt] OR '
    '"comment"[pt] OR "letter"[pt]) '
    'AND english[lang]'
)
```

**Deprecated variant (commit `9f7093b` on `friday-corpus-build`, reverted by `841c99b`).** The Friday session briefly added these three terms; senior-author guidance reverted them. They are not present in canonical output:

```python
'"GPT-5"[tiab] OR "GPT-4.5"[tiab] OR "GPT-4o"[tiab] OR '
```

Sensitivity-analysis effect (recorded in the local archive `output/archive_friday_with_gpt5_4o_45/`): adding these three terms added **49 records (0.05%)** to the post-SJR Q1/Q2 corpus.

**Date range, date field, and 2026 cutoff.** The query is constructed month-by-month via PDAT (PubMed publication date) using these constants at the top of `fetch_pubmed_medical.py`:

```python
CUTOFF_YEAR  = 2026
CUTOFF_MONTH = 4  # April 2026
```

and this month-loop in `process_year`:

```python
current_year  = date.today().year
current_month = date.today().month
if year < current_year:
    months = list(range(1, 13))
else:
    max_month = current_month
    # Apply corpus cutoff: never fetch beyond the configured cutoff year/month
    if year == CUTOFF_YEAR:
        max_month = min(max_month, CUTOFF_MONTH)
    months = list(range(1, max_month + 1))
```

The fetch therefore runs `("{year_start}"[PDAT] : "{year_end}"[PDAT])` for monthly windows from **January 2021** through **April 2026**. The query parameter `[PDAT]` is **publication date** (cover date), not `[EDAT]` (entry date).

**`pub_year` field — definitive resolution.** The `pub_year` column in committed outputs is *not* PDAT, and *not* EDAT. It is parsed from PubMed's XML `PubDate/Year` element by `parse_pubmed_xml` in `fetch_pubmed_medical.py`:

```python
pub_year  = safe_text(article, ".//PubDate/Year")
pub_month = safe_text(article, ".//PubDate/Month", "Jan")
medline   = safe_text(article, ".//PubDate/MedlineDate")
if pub_year:
    rec["pub_date"] = f"{pub_year} {pub_month}".strip()
    rec["year"]     = pub_year
elif medline:
    rec["pub_date"] = medline
    rec["year"]     = medline[:4]
```

That is, `pub_year` is the **publication-year integer from `PubDate/Year`**, falling back to the first four characters of `MedlineDate` when `PubDate/Year` is absent. It reflects the article's publication date as encoded by the publisher, not the indexing date. The `[PDAT]` query range is the *retrieval* filter; the `pub_year` column is the *content* of the retrieved record.

**Explanation of the ~2,691 records dated 2026.** Records are fetched by their PubMed `[PDAT]` falling in Jan–Apr 2026. PubMed routinely indexes ahead-of-print versions with future cover dates; a single Saturday `apply_date_cutoff` inline operation (see §10b) additionally drops records whose `PubDate` field shows May 2026 or later. After this two-stage filter, the 2026 stratum is partial — covering papers physically published Jan–Apr 2026, where "published" means the PubDate cover date encoded in the XML.

### 1b. Deduplication

**File:** `fetch_pubmed_medical.py` (same canonical commit as 1a).

Two-stage dedup. Both stages are exact PMID-equality on the canonical PubMed PMID:

```python
def deduplicate_pmids(pmid_list):
    return list(dict.fromkeys(pmid_list))
```
*(In-year dedup across the 12 monthly PMID lists for one year; preserves first-seen order.)*

```python
def deduplicate_records(records):
    seen, out = set(), []
    for r in records:
        if r["pmid"] not in seen:
            seen.add(r["pmid"])
            out.append(r)
    return out
```
*(Cross-year dedup, called by `merge_years()`, producing `raw_medical_all.csv`.)*

**Reported figure**: 130,181 monthly-collected records → **116,117 deduplicated PMIDs** in `raw_medical_all.csv` (Saturday Batch run, prompt-revision-v2). Reduction = 14,064 cross-year duplicates (papers whose monthly PDAT crossed a year boundary or were re-indexed).

### 1c. SJR Q1/Q2 mapping

**File:** `sjr_filter.py`
**Branches with canonical content:** all branches; byte-identical content since commit `8500d89`
**SJR source files:** `input/sjr/sjr_2021.csv` … `input/sjr/sjr_2026.csv` (committed; semicolon-delimited)

**SJR data version.** The committed SJR CSVs are downloads from `scimagojr.com` per the docstring of `sjr_filter.py` ("SJR CSVs: input/sjr/sjr_YYYY.csv (semicolon-delimited, from scimagojr.com)"). One file per year, 2021–2026. The 2026 file is identical to the 2025 file (the script substitutes when an exact-year SJR file is absent, but in this repo a `sjr_2026.csv` is committed; per `load_sjr`, the latest available year falls back if missing).

**Quartile definition.** The script reads SCImago's `"SJR Best Quartile"` column — i.e., the **best quartile across all subject categories** assigned to that journal. A journal that is Q1 in *any* subject (e.g. Q1 in Computer Science) is treated as Q1 here even if it is Q2 or Q3 in a strictly medical category.

**Verbatim title-normalisation logic:**

```python
STOPWORDS = {"the", "a", "an", "of", "in", "and", "for", "on", "with",
             "its", "by", "to", "from", "at", "or"}

def normalise(t):
    t = t.lower().strip()
    t = re.sub(r"\(.*?\)", "", t)           # remove parentheticals
    t = re.sub(r":.*$", "", t)              # remove subtitle after colon
    t = re.sub(r"[^a-z0-9 ]", " ", t)      # special chars → space (handles & . / - …)
    words = [w for w in t.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(words).strip()
```

**Verbatim quartile lookup:**

```python
def get_quartile(journal_raw, title_map):
    """Returns 'Q1', 'Q2', 'Q3', or None."""
    norm = normalise(journal_raw)
    if not norm:
        return None
    # Apply alias patch first
    norm = ALIAS_PATCH.get(norm, norm)
    return title_map.get(norm)
```

**Matching is by normalised TITLE, not ISSN.** The script does not read ISSN.

**Hardcoded alias-patch table (excerpt; full table at `sjr_filter.py:63-102`):**

```python
ALIAS_PATCH = {
    "sensors basel switzerland":              "sensors",
    "diagnostics basel switzerland":          "diagnostics",
    "bioengineering basel switzerland":       "bioengineering",
    "ijerph":                                 "international journal environmental research public health",
    "international journal environmental research public health basel switzerland":
                                              "international journal environmental research public health",
    "journal american medical informatics association jamia":
                                              "journal american medical informatics association",
    # ... (40+ entries — see file for full list)
}
```

**Exclude-set (conferences/preprints), verbatim:**

```python
EXCLUDE_JOURNALS = {
    "annual international conference ieee engineering medicine biology society",
    "annual international conference ieee engineering medicine biology society "
    "ieee engineering medicine biology society annual international conference",
    "amia annual symposium proceedings amia symposium",
    "amia symposium",
    "studies health technology informatics",
    "proceedings spie",
    "lecture notes computer science",
    "lecture notes networks systems",
    "ifac papersonline",
    "medrxiv",
    "medrxiv preprint server health sciences",
    "arxiv",
    "biorxiv",
    "biorxiv preprint server biology",
    "ssrn",
    "research square",
}

EXCLUDE_KEYWORDS = [
    "annual international conference",
    "annual symposium proceedings",
    "conference proceedings",
    "preprint server",
    "lecture notes",
]
```

**How 97,492 was reached.** Reading the Saturday re-fetch log (`output/sjr.log` at `prompt-revision-v2` runtime, summary in `output/prefilter_batch_submit.log`):

```
Total records:           116,117
Excluded (conf/preprint):   4,106
Eligible (post-exclusion): 112,011
Q1+Q2 (primary corpus):    98,626   (88.0% of eligible)
Q3 (comparison arm):        5,463
Unmatched:                  7,922
```

After a post-fetch April-2026 `PubDate` cutoff (see §10b), `filtered_medical_all_Q1Q2.csv` drops to **97,492** records (1,134 records with `PubDate` in May 2026 or later removed). This is the canonical input to the prefilter.

### 1d. PubMed publication-type collapsing

**NOT applied at the fetch/filter/classify stages.** The raw `pub_type` field is stored verbatim from PubMed's XML `PublicationType` elements as a semicolon-joined string (e.g., `"Editorial; Letter"`). All committed classifier prompts and inputs use this raw form.

**Downstream collapsing rules are defined in `analysis/robustness.py`** (`analysis-session-1` through `analysis-session-4`; relocated to repo-root `robustness.py` on `analysis-session-5`). The 5-bucket scheme used in figures and tables:

```python
def simplify_pubtype_7(pt: str) -> str:
    """Bucket the compound PubMed pub_type string into 7 categories.
    Precedence: Editorial > Letter > Systematic Review > Review > Comment > News > Research Article.
    """
    pt = pt or ""
    if "Editorial" in pt:
        return "Editorial"
    if "Letter" in pt:
        return "Letter"
    if "Systematic Review" in pt:
        return "Systematic Review"
    if "Review" in pt:
        return "Review"
    if "Comment" in pt:
        return "Comment"
    if "News" in pt:
        return "News"
    return "Research Article"


def simplify_pubtype_5(pt: str) -> str:
    """Collapse 7-bucket into 5 categories per brief.
    - Systematic Review → Review
    - Comment → Commentary
    - News → Research Article
    """
    seven = simplify_pubtype_7(pt)
    if seven == "Systematic Review":
        return "Review"
    if seven == "Comment":
        return "Commentary"
    if seven == "News":
        return "Research Article"
    return seven
```

The five buckets used in reporting: **`{Research Article, Editorial, Review, Commentary, Letter}`**. Precedence rules are as listed (first-match in the chain above; e.g., a paper tagged "Editorial; Letter" is collapsed to `Editorial`).

---

## 2. Prefilter — Haiku 4.5, Batch API

**Canonical file:** `prefilter_batch.py` @ `prompt-revision-v2` (commit `9c79cd5`)
**Async non-batch version (also committed):** `prefilter.py` @ same branch, same commit. Both files share identical `MODEL`, `MAX_TOKENS`, `SYSTEM_PROMPT`, `build_prompt`, and `parse_response`. The Batch API path was introduced because Tier-1 rate limits made the async path infeasible at 95K records.

**Verbatim SYSTEM_PROMPT:**

```text
You are classifying medical journal articles into one of three categories based on whether and how they engage with artificial intelligence (AI) as a subject.

CATEGORIES:

- discourse: AI/LLM is the MAIN SUBJECT of discussion. The paper reflects on, debates, or analyses AI's role, safety, ethics, implications, governance, risks, or future in medicine. Includes editorials, perspectives, opinion pieces, and narrative reviews WHERE THE CENTRAL TOPIC IS AI ITSELF.

- evaluative: The paper TESTS or BENCHMARKS a specific AI system (especially LLMs like ChatGPT, GPT-4) and draws explicit conclusions about its accuracy, safety, reliability, limitations, or clinical readiness.

- application: The paper USES AI/ML as a technical tool to solve a clinical problem. AI is a method, not the subject. When in doubt, classify as application.

CRITICAL RULES:
- Only classify as discourse if AI/LLM is clearly the CENTRAL topic
- Only classify as evaluative if there is explicit testing of an AI system with clinical conclusions
- Everything else = application

Return ONLY valid JSON: {"paper_type": "...", "type_confidence": "..."}
No preamble, no explanation.
```

**Verbatim `build_prompt` (user message):**

```python
def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        text += f"\nAbstract: {abstract[:300]}"
    return f"Classify this paper:\n\n{text}"
```

> Abstract truncation: **first 300 characters** of the abstract are passed; titles are passed in full. Records with empty abstracts have only the title.

**Few-shot examples in prompt: NONE.** The prompt is zero-shot. *(Note: the *stance* classifier prompt does contain few-shot examples; the prefilter does not.)*

**Inclusion / routing rule.** Every record is assigned exactly one of `{discourse, evaluative, application}`. No record is dropped at this stage. Records classified `discourse` or `evaluative` are appended to `output/prefiltered_discourse_eval.csv`; records classified `application` are appended to `output/prefiltered_application.csv`. The downstream stance classifier consumes only `prefiltered_discourse_eval.csv`.

**Definition of "discourse + evaluative" for the manuscript.** These are the records that proceed to stance classification. From the Saturday run: 16,759 records (8,899 discourse + 7,860 evaluative); the remaining 80,733 application records are excluded from stance analysis.

**Model and request configuration:**

```python
MODEL       = "claude-haiku-4-5-20251001"
MAX_TOKENS  = 120
```

| Setting | Value | Notes |
|---|---|---|
| model | `claude-haiku-4-5-20251001` | Dated alias of Haiku 4.5 |
| max_tokens | `120` | |
| temperature | *omitted from API call* | Defaults to Anthropic API default (T=1.0 for Claude 4.x family) |
| system | `SYSTEM_PROMPT` above | passed as `system` parameter |
| messages | `[{"role":"user","content": build_prompt(...)}]` | single user turn |
| response_format / structured output | none | JSON parsed from raw `content[0].text` post-hoc |
| Batch settings | `N_BATCHES = 5` (default; can be overridden by env `PREFILTER_N_BATCHES`); poll interval 60s | |

**Response parsing (verbatim from `prefilter_batch.py`):**

```python
raw = re.sub(r"^```(?:json)?\s*", "", text)
raw = re.sub(r"\s*```$", "", raw)
parsed = json.loads(raw, strict=False)
ptype = parsed.get("paper_type", "").strip().lower()
if ptype not in VALID_TYPES:
    ptype = "application"
conf = parsed.get("type_confidence", "Medium").strip()
if conf not in ("High", "Medium", "Low"):
    conf = "Medium"
```

with `VALID_TYPES = {"discourse", "evaluative", "application"}`. On parse failure, the record defaults to `("application", "Low")`.

**Pilot validation (n=200, hand-coded by Kingsley vs Haiku):** raw agreement **85.5%**, Cohen's κ **0.511** (95% CI 0.347–0.676; "moderate" per Landis-Koch). Per-class recall: application 94%, discourse 64%, evaluative 31%. Pilot input + Haiku comparison committed at `output/pilot_200.xlsx`, `output/pilot_200.csv`, `output/pilot_200_full_haiku.csv` on `prompt-revision-v2`.

---

## 3. Stance classifier — Sonnet 4.6 (v1 canonical)

**Canonical file:** `classify_stance.py` @ `prompt-revision-v2` (commit `9c79cd5`)
**Batch variant:** `classify_stance_batch.py` @ same commit (used to produce the canonical `output/classified_medical_Q1Q2.csv`)
**Pre-canonical version:** `classify_stance.py` @ `main` (`8500d89`) — differs from canonical only in (a) abstract truncation `[:400]` and (b) `load_dotenv()` without `override=True`. SYSTEM_PROMPT and few-shot examples are byte-identical between versions.

### Verbatim SYSTEM_PROMPT (canonical, v1)

```text
Classify the stance of a medical AI article toward AI/LLM technology.

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

Return ONLY valid JSON: {"stance":"...","confidence":"...","predictive_claim":"..."}
```

### Five stance definitions — verbatim block

```text
- Alarm: primarily critical/skeptical. Emphasises dangers, failures, hallucinations, safety risks, ethical problems, or argues AI is not ready. Papers showing AI performs WORSE than clinicians = Alarm.
- Caution: acknowledges both promise AND significant concerns, balance tilts toward concern. Recommends safeguards before deployment.
- Neutral: purely descriptive. Reports metrics without taking a position. No evaluative language.
- Cautious Optimism: broadly positive with caveats. Supports careful deployment.
- Advocacy: strongly pro-AI. Emphasises transformative potential, minimal caveats.
```

### Flags `{NO_STANCE, OUT_OF_SCOPE, DATA_INSUFFICIENT, META_DISCOURSE}`

**NOT FOUND IN REPO.** No version of `classify_stance.py` or `classify_stance_batch.py` on any branch (`main`, `friday-corpus-build`, `analysis-session-1..5`, `prompt-revision-v2`) defines a flag taxonomy with these names. The classifier returns one of five stances plus a literal sentinel `"FAILED"` when JSON parsing or stance validation fails. No `NO_STANCE`, `OUT_OF_SCOPE`, `DATA_INSUFFICIENT`, or `META_DISCOURSE` field is emitted, and no SYSTEM_PROMPT mentions them.

If the manuscript Methods asserts a four-flag scheme, that claim **must be re-checked** against either (a) an uncommitted file the author still holds locally, or (b) a manual re-coding step done outside the pipeline. The committed pipeline has no such flags.

### Title+abstract vs title-only handling

The classifier always passes `Title: {title}` and, if the abstract is non-empty, `Abstract: {abstract}` (canonical v1, no truncation). There is no separate title-only path; records with an empty abstract are sent with the title alone. Verbatim:

```python
def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        # No truncation (was [:400]). 400 chars = ~70 words = LLM saw only abstract intro,
        # missing findings/conclusions where stance signal lives. Sonnet 4.6's 200K-token
        # context easily fits any PubMed abstract (typical max ~10K chars). Cost impact
        # at corpus scale ~$15-30 incremental, negligible.
        text += f"\nAbstract: {abstract}"
    return text
```

### Model and request configuration (canonical)

```python
MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 120
```

| Setting | Value | Notes |
|---|---|---|
| model | `claude-sonnet-4-6` | |
| max_tokens | `120` | |
| temperature | *omitted from API call* | Defaults to API default (T=1.0) |
| system | SYSTEM_PROMPT above | |
| messages | one user turn, `Title:… \nAbstract:…` (full abstract) | |
| structured output | none — JSON parsed post-hoc from raw text | |
| Batch (canonical) | one batch of ≤100,000 requests; `N_BATCHES=1`; poll interval 60s | |

**Output schema** (CSV columns appended by classifier): `pub_year`, `stance`, `stance_model = "sonnet"`, `confidence`, `predictive_claim`, `stance_raw` (raw JSON returned by model). Reported stance values are one of `{Alarm, Caution, Neutral, Cautious Optimism, Advocacy, FAILED}`.

### What differs in v2

A v2 stance prompt **was committed on 2026-05-09** as supplementary sensitivity analysis. **v2 lives only on `prompt-revision-v2`** at commit `2559e6b` and is explicitly NOT to be propagated to `main` or to any `analysis-session-*` branch. The canonical reported numbers in the manuscript are from v1 (commit `9c79cd5`); v2 is a sensitivity check, intended as a brief supplementary mention.

**File:** `classify_stance_batch.py` @ `prompt-revision-v2` (commit `2559e6b`). Pre-v2 snapshot retained as `classify_stance_batch.py.v1_backup` at the same commit.

#### Verbatim v2 SYSTEM_PROMPT

```text
You are an expert classifier of academic medical literature. Your task is to classify the STANCE of medical journal articles toward AI/LLM technology in medicine. Read the title and abstract, then assign ONE of the following five stance labels.

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
```

#### What v2 changes vs v1

- **New output field**: `meta_discourse` (yes/no) — survey-style "what does population X think about AI" papers are flagged so they don't get counted as authorial stance.
- **More structured rubric**: explicit "WHERE TO FIND THE AUTHORS' STANCE" section directs attention to the conclusion/discussion (last 30–40% of abstract), and explicit "BACKGROUND FRAMING is NOT stance" guidance.
- **Tightened Advocacy threshold**: v2 requires BOTH transformative language AND minimal caveats; v1 had only a sketchier definition.
- **Five common pitfalls** explicitly enumerated.
- The five stance categories themselves are unchanged.

#### v1 → v2 effect on the corpus (16,759 stance-eligible records)

From `output/comparison_v1_v2.md` @ commit `2559e6b`:

| Stance | v1 n | v2 n | Δ |
|---|---:|---:|---:|
| Alarm | 916 | 588 | −328 |
| Caution | 4,245 | 3,667 | −578 |
| Neutral | 838 | 2,916 | **+2,078** |
| Cautious Optimism | 10,515 | 9,397 | −1,118 |
| Advocacy | 235 | 187 | −48 |
| FAILED | 10 | 4 | −6 |

- **80.1% (13,429) of records keep the same stance** between v1 and v2.
- **19.9% (3,330) migrate**; the dominant flow is CO → Neutral (1,322 records) and Caution → Neutral (763 records), consistent with v2's stricter "stance must come from the conclusion, not background framing" rule.
- v2 is *more conservative* — it triples the Neutral class as papers that v1 read as positive based on background framing are reclassified as descriptive.

**Per author guidance, v1 remains the manuscript-canonical stance assignment.** v2 should be referenced only as a sensitivity analysis showing that the *direction* of temporal stance trends is robust to a stricter rubric, even though the absolute proportions shift.

### 300-record stance validation (κ on v1)

**File:** `output/validation/kappa_report.md` @ `prompt-revision-v2` (commit `95fdc36`)
**Inputs:** `output/validation/kingsly_coding_sheet.xlsx` (Kingsley's 300 hand-codes) vs `output/validation/kingsly_validation_full.csv` (LLM v1 stances)

**Sample.** 300 records, stratified by LLM-assigned stance per `export_validation.py`. Stratification targets were 60 per stance, achieved as a per-stance min(target, pool size):
- Alarm: pool 844 → sampled 40
- Caution: pool 3,905 → sampled 60
- Neutral: pool 635 → sampled 70
- Cautious Optimism: pool 10,184 → sampled 100
- Advocacy: pool 178 → sampled 30

**Human-coding flags (in addition to a stance label).** During hand-coding Kingsley applied four orthogonal flags from the coding sheet, recorded as columns in `kingsly_coding_sheet.xlsx`. They are *not* output by the LLM; they are author-applied during validation to mark records the rubric should treat specially:

| Flag | n in 300 | Meaning (per `coding_instructions.txt` and `compute_kappa.py`) |
|---|---:|---|
| `NO_STANCE` | 73 | Record does not contain a stance-bearing claim (e.g. methods-only paper that slipped through prefilter) |
| `OUT_OF_SCOPE` | 2 | Not actually about medical AI |
| `DATA_INSUFFICIENT` | 0 | Abstract too short / missing to support any stance assignment |
| `META_DISCOURSE` | 14 | Reports a population's attitudes toward AI rather than taking a stance (matches v2's `meta_discourse` output field) |
| (records with >1 flag) | 7 | Kingsley applied two or more flags to the same record |

Flags are used to build sensitivity-analysis subsets ("Sensitivity A" drops `NO_STANCE`; "Sensitivity B" drops `NO_STANCE` and `META_DISCOURSE`). The flag↔stance relationship is **not mutually exclusive** — a record can have both a stance label and one or more flags; flagged records are *excluded from selected sensitivity κ values* rather than overriding the stance assignment.

**κ values (all 95% CIs by percentile bootstrap, n_boot=1000, seed=42):**

| Layer | n | Unweighted κ | Linear κ | Quadratic κ |
|---|---:|---|---|---|
| **Primary** (all 300) | 300 | 0.564 (0.494–0.630) | 0.659 (0.596–0.722) | 0.752 (0.685–0.811) |
| **Sensitivity A** (excl. `NO_STANCE`) | 225 | 0.560 (0.470–0.637) | 0.687 (0.614–0.748) | 0.789 (0.724–0.841) |
| **Sensitivity B** (excl. `NO_STANCE` + `META_DISCOURSE`) | 218 | 0.570 (0.483–0.651) | 0.698 (0.624–0.761) | 0.799 (0.731–0.853) |

**Interpretation per Landis-Koch**: quadratic κ ≥ 0.75 ("substantial agreement") on the primary sample and ≥ 0.78 on both sensitivity subsets. Unweighted κ sits in the 0.55–0.57 band ("moderate agreement"); the weighted (linear / quadratic) κ values are what the manuscript should report, since stance is an ordered categorical scale and disagreements between adjacent labels (e.g. CO ↔ Neutral) are not equivalent to disagreements between distant labels (e.g. Advocacy ↔ Alarm).

**Confusion matrix — primary (n=300), rows = human, columns = LLM v1.** Reproduced verbatim from `kappa_report.md`:

```
Human \ LLM      | Alarm | Caution | Neutral | Cautious | Advocacy | Total
---------------------------------------------------------------------------
Alarm            |    31 |       4 |       0 |        1 |        0 |    36
Caution          |     8 |      34 |       3 |       14 |        0 |    59
Neutral          |     0 |      10 |      57 |       17 |        4 |    88
Cautious Optimism|     1 |      12 |      10 |       61 |        9 |    93
Advocacy         |     0 |       0 |       0 |        7 |       17 |    24
---------------------------------------------------------------------------
Total            |    40 |      60 |      70 |      100 |       30 |   300
```

**Dominant disagreement patterns** (informative for §10): LLM tends to call records `Cautious Optimism` that Kingsley calls `Neutral` (n=17) or `Caution` (n=14), consistent with the v1→v2 reclassification pattern (v1 reads background-framing positivity as stance; v2 corrects this). Few `Alarm`↔`Advocacy` opposite-end errors (1 total in the off-diagonal extremes), supporting the use of weighted κ.

---

## 4. Theme classifier — Sonnet 4.6

**Canonical file:** `classify_themes.py` @ `prompt-revision-v2` (commit `9c79cd5`)
**Batch variant:** `classify_themes_batch.py` @ same commit (used to produce canonical `output/analysis/thematic_alarm.csv`)

### Verbatim SYSTEM_PROMPT

```text
Identify concern themes in critical medical AI papers.

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

Return ONLY valid JSON: {"themes": ["theme1", "theme2"]}
```

### Ten theme definitions — verbatim block

```text
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
```

### LITERAL "hallucination" gate text given to the classifier

The exact one-line definition seen by the model is:

```text
hallucination: AI errors, hallucinations, factual inaccuracies, unreliable outputs
```

**It does *not* read "hallucination (make up info)" or anything similar.** This text is byte-identical on every branch where `classify_themes.py` exists: `main`, `friday-corpus-build`, `analysis-session-1..5`, `prompt-revision-v2`. No variant phrasing was found anywhere in committed code.

### Multilabel / co-occurrence rules

- The prompt instructs the model to return **1 to 3 themes**, "most prominent".
- The script post-processes the returned `themes` array: keeps only members of `VALID_THEMES`, falls back to `["other"]` if nothing valid is returned, and **caps at 3** themes per record (`themes[:3]` in `classify_themes_batch.py`).
- Stored on disk as both a pipe-joined string column (`themes = "theme1|theme2"`) and three separate columns (`theme_1`, `theme_2`, `theme_3`) — empty string for unfilled slots.

### Subset applied to

From `classify_themes.py` and `classify_themes_batch.py`:

```python
all_records = [r for r in csv.DictReader(f)
               if r.get("stance") in ("Alarm", "Caution")]
```

i.e., only records with stance `Alarm` or `Caution`. From the Saturday canonical run: **5,161 records** (916 Alarm + 4,245 Caution).

### Model and request configuration

```python
MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 150
```

| Setting | Value | Notes |
|---|---|---|
| model | `claude-sonnet-4-6` | |
| max_tokens | `150` | (higher than stance — themes list can be longer) |
| temperature | *omitted* | Defaults to API default (T=1.0) |
| structured output | none — JSON parsed post-hoc | |
| abstract truncation | `[:400]` characters | **Note: themes still truncates, unlike stance which removed truncation in v1.1.** See §10c. |

### `build_prompt` (verbatim)

```python
def build_prompt(title, abstract):
    text = f"Title: {title}"
    if abstract and abstract.strip():
        text += f"\nAbstract: {abstract[:400]}"
    return f"Identify concern themes:\n\n{text}"
```

---

## 5. Specialty assignment

**Script file:** `analysis/classify_specialty.py` @ `analysis-session-2` (commit `a30aaf7`) — only branch with the runner script
**Output file (canonical):** `output/specialty_classifications.csv` @ `prompt-revision-v2` (commit `95fdc36`) — 16,745 records with specialty + confidence
**Note:** the runner script lives only on `analysis-session-2`; the outputs were retroactively committed on `prompt-revision-v2` (this branch) so the manuscript has a single auditable provenance.

**Method:** LLM classification via Anthropic Message Batches API (Haiku 4.5).

### Verbatim SYSTEM_PROMPT

```text
You are classifying medical research papers by clinical specialty.

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
```

### Full specialty taxonomy (canonical short-name list)

```
Radiology / Diagnostic Imaging
Pathology / Laboratory Medicine
Cardiology
Oncology
Surgery
Ophthalmology
Dermatology
Neurology / Neuroscience
Mental Health / Psychiatry
Internal Medicine / Primary Care
Emergency Medicine / Critical Care
Pediatrics
Obstetrics / Gynecology
Dentistry
Medical Informatics / Digital Health
Nursing
Medical Education
Multidisciplinary / Other
```

### Model and request configuration

Per `analysis/classify_specialty.py` @ `analysis-session-2`:
- model: `claude-haiku-4-5-20251001` *(verify in file; agent reported Haiku 4.5 batch)*
- temperature: *omitted (defaults to 1.0)*
- response_format / structured output: none — JSON parsed from raw text
- Batch API: yes (Anthropic Message Batches)

**Coverage.** Reported in agent audit: 16,745 / 16,758 records (99.9%). The 13 unclassified records are likely empty-abstract failures.

### "Rare specialty n<30" rule

The exclusion rule is **applied downstream** in plotting/CI scripts, not in `classify_specialty.py` itself. Per the agent audit, the rule lives in `q7_s5_1_a_specialty.py` (likely on `analysis-session-5`) at approximately line 74. The exact verbatim text **was not extracted by the audit and should be verified directly before stating it in Methods**. The semantics reported: specialties with n < 30 are flagged `low_confidence` and **excluded from bootstrap CI computation, but not filtered from the dataset**.

> **Action item:** before publishing the Methods sentence about the n<30 rule, run `git show analysis-session-5:q7_s5_1_a_specialty.py` (or whatever the actual path is) and paste the verbatim threshold logic into this section. Until verified, treat the rule as "exists in the analysis pipeline, exact wording not yet confirmed."

---

## 6. Country & affiliation

### First-author determination

**Method:** PubMed XML, first author in document order. From `fetch_pubmed_medical.py` (`main`, `8500d89`; unchanged through `prompt-revision-v2`):

```python
authors = article.findall(".//AuthorList/Author")
if authors:
    first = authors[0]
    rec["first_author"] = (
        f"{safe_text(first, 'LastName')} {safe_text(first, 'ForeName')}".strip()
    )
    aff = first.find(".//AffiliationInfo/Affiliation")
    if aff is not None:
        rec["first_affiliation"] = "".join(aff.itertext()).strip()
```

i.e., `first_author = LastName ForeName` joined with a space; `first_affiliation` = the first `<Affiliation>` text under the first author's `<AffiliationInfo>` block. **No corresponding-author logic.** Records with no parseable AuthorList → empty first_author and first_affiliation.

### Country resolution

**File:** `analyse_geography.py`
**Branches:** all (introduced on `main` at `8500d89`, byte-identical across branches)

**Method:** regex/substring lookup against an explicit country→region table; fallback rule for US state-abbreviation suffixes. Verbatim table:

```python
COUNTRY_REGION = {
    # North America
    "usa": "North America", "united states": "North America",
    "u.s.a": "North America", "u.s.": "North America",
    "canada": "North America", "mexico": "North America",

    # Europe
    "uk": "Europe", "united kingdom": "Europe", "england": "Europe",
    "scotland": "Europe", "wales": "Europe", "ireland": "Europe",
    "germany": "Europe", "france": "Europe", "italy": "Europe",
    "spain": "Europe", "netherlands": "Europe", "belgium": "Europe",
    "switzerland": "Europe", "sweden": "Europe", "norway": "Europe",
    "denmark": "Europe", "finland": "Europe", "austria": "Europe",
    "portugal": "Europe", "greece": "Europe", "poland": "Europe",
    "czech": "Europe", "hungary": "Europe", "romania": "Europe",
    "turkey": "Europe", "israel": "Middle East",

    # China
    "china": "China", "p.r. china": "China", "people's republic of china": "China",
    "hong kong": "China", "taiwan": "China",

    # Asia-Pacific
    "japan": "Asia-Pacific", "south korea": "Asia-Pacific", "korea": "Asia-Pacific",
    "australia": "Asia-Pacific", "new zealand": "Asia-Pacific",
    "singapore": "Asia-Pacific", "india": "Asia-Pacific",
    "thailand": "Asia-Pacific", "malaysia": "Asia-Pacific",
    "indonesia": "Asia-Pacific", "iran": "Middle East",
    "saudi arabia": "Middle East", "egypt": "Middle East",
    "qatar": "Middle East", "uae": "Middle East",
    "united arab emirates": "Middle East",

    # Latin America
    "brazil": "Latin America", "argentina": "Latin America",
    "chile": "Latin America", "colombia": "Latin America",
    "mexico": "Latin America",

    # Africa
    "south africa": "Africa", "nigeria": "Africa", "kenya": "Africa",
    "ethiopia": "Africa", "ghana": "Africa",
}
```

> **Note one duplicate key**: `"mexico"` appears under both "North America" and "Latin America". In a Python `dict` literal, the **second occurrence wins**, so `mexico → Latin America` is what is actually used at runtime. If the manuscript reports Mexico under North America, that disagrees with the committed code; verify against output files.

**Fallback for `.edu` / US state suffixes**, verbatim:

```python
if any(x in aff_lower for x in [", tx", ", ca", ", ny", ", ma", ", fl",
                                ", il", ", pa", ", oh", ", nc", ", wa"]):
    return "North America"
```

**Coverage statistic ~90.3%.** **NOT FOUND IN REPO** as a literal number. The agent audit traced country-resolution logic but did not surface a committed file that asserts 90.3% coverage. If the manuscript intends to report ~90.3%, recompute against `output/raw_medical_all.csv` or `classified_medical_Q1Q2.csv` directly using `analyse_geography.py` and pull the actual coverage % from that run.

### Affiliation-type heuristic

**File:** `analyse_industry.py` @ `main` (`8500d89`); byte-identical across all branches.

**Categories returned: `{industry, academia, mixed, unknown}`** — note these are not `{industry, academic_clinical, mixed, other}`. The committed code uses `academia` (not `academic_clinical`) and `unknown` (not `other`).

```python
INDUSTRY_KEYWORDS = [
    "google", "deepmind", "microsoft", "openai", "meta ", "facebook",
    "amazon", "apple ", "nvidia", "ibm ", "intel ",
    "babylon health", "tempus", "flatiron", "nuance", "azure", "aws ",
    "philips", "siemens", "ge healthcare", "ge medical", "general electric",
    "medtronic", "stryker", "johnson & johnson", "j&j", "abbott",
    "roche", "novartis", "pfizer", "astrazeneca", "merck",
    "bayer", "sanofi", "gsk", "glaxosmithkline",
    "mckinsey", "deloitte", "accenture", "iqvia", "covance",
    "inc.", "ltd.", "llc", "corp.", "gmbh", " co.,", "holdings",
]

ACADEMIA_KEYWORDS = [
    "university", "université", "universität", "universidad",
    "college", "institute", "hospital", "clinic", "medical center",
    "medical centre", "school of medicine", "faculty of medicine",
    "department of", "national institutes", "nih ",
]

def classify_affiliation(aff):
    if not aff:
        return "unknown"
    aff_lower = aff.lower()
    has_industry = any(kw in aff_lower for kw in INDUSTRY_KEYWORDS)
    has_academia = any(kw in aff_lower for kw in ACADEMIA_KEYWORDS)
    if has_industry and has_academia:
        return "mixed"
    elif has_industry:
        return "industry"
    elif has_academia:
        return "academia"
    return "unknown"
```

**Coverage ~98.4%** — the agent audit reports 16,485 / 16,759 first-affiliation fields populated. The value is computable directly from `first_affiliation` non-emptiness in `classified_medical_Q1Q2.csv`; it is not a hard-coded number in the script.

---

## 7. FDA AI/ML device proxy

**File:** `analysis/run_specialty_aiadoption.py`
**Branch:** `analysis-session-4` (only)
**Commit:** `c6b9092`

**Data source.** The script reads from `output/external/fda_aiml_devices.csv`. **This CSV is NOT committed to any branch** of the repository. The script's docstring describes it as the FDA's "Artificial Intelligence and Machine Learning (AI/ML)-Enabled Medical Devices" downloadable spreadsheet (`fda.gov`).

> **Version / date of FDA file: NOT FOUND IN REPO.** The committed code references the file but contains no URL pin, no date stamp, and no version constant. To make the Methods reproducible, **the author must record (a) the exact `fda.gov` URL and download date, and (b) the FDA-list snapshot version**, and ideally commit the CSV itself to the repo or note its SHA-256.

**Total device count: NOT FOUND IN REPO.** Because the source CSV is not committed, the total is not in the repo. Reading `output/external/fda_aiml_devices.csv` locally would yield the count.

### Device → specialty mapping (verbatim)

```python
FDA_PANEL_TO_SPECIALTY = {
    "radiology": "Radiology / Diagnostic Imaging",
    "cardiovascular": "Cardiology",
    "neurology": "Neurology / Neuroscience",
    "ophthalmic": "Ophthalmology",
    "pathology": "Pathology / Laboratory Medicine",
    "hematology": "Pathology / Laboratory Medicine",
    "clinical chemistry": "Pathology / Laboratory Medicine",
    "immunology": "Pathology / Laboratory Medicine",
    "microbiology": "Pathology / Laboratory Medicine",
    "molecular genetics": "Pathology / Laboratory Medicine",
    "toxicology": "Pathology / Laboratory Medicine",
    "toxcicology": "Pathology / Laboratory Medicine",  # FDA list misspells this
    "general and plastic surgery": "Surgery",
    "general & plastic surgery": "Surgery",
    "orthopedic": "Surgery",
    "ear, nose, and throat": "Surgery",
    "ear nose": "Surgery",
    "obstetrics": "Obstetrics / Gynecology",
    "gynecolog": "Obstetrics / Gynecology",
    "dental": "Dentistry",
    "anesthesiology": "Emergency Medicine / Critical Care",
    "gastroenterology": "Internal Medicine / Primary Care",
    "general hospital": "Multidisciplinary / Other",
    "physical medicine": "Multidisciplinary / Other",
}
```

### Structural-zero specialties (verbatim)

```python
# Specialties with no meaningful FDA device panel -> structural zero adoption.
# Recorded explicitly so the FDA arm scores them 0 rather than dropping them.
FDA_STRUCTURAL_ZERO = [
    "Mental Health / Psychiatry",
    "Nursing",
    "Medical Education",
    "Medical Informatics / Digital Health",
    "Pediatrics",
    "Dermatology",
    "Oncology",
]
```

### Mapping logic (verbatim, the function that joins FDA panels to corpus specialties)

```python
def load_fda_device_counts(counts_index: list[str]) -> pd.Series | None:
    """Return device counts per specialty from a real FDA list, or None.

    Maps the FDA 'Panel (Lead)' column onto our specialty buckets via
    FDA_PANEL_TO_SPECIALTY. Never fabricates: returns None (and the caller
    prints the required file) when no usable device list is available.
    """
    if not FDA_PATH.exists():
        return None

    fda = pd.read_csv(FDA_PATH, low_memory=False)
    panel_col = _find_panel_column(list(fda.columns))
    if panel_col is None:
        print(
            f"  ! {FDA_PATH} has no recognizable panel column "
            f"(columns: {list(fda.columns)}). Expected a 'Panel (Lead)' column."
        )
        return None

    panels = fda[panel_col].fillna("").astype(str).str.lower()
    mapped = pd.Series("UNMAPPED", index=fda.index, dtype=object)
    for key, spec in FDA_PANEL_TO_SPECIALTY.items():
        hit = panels.str.contains(key, regex=False)
        mapped[hit & mapped.eq("UNMAPPED")] = spec

    n_unmapped = int(mapped.eq("UNMAPPED").sum())
    if n_unmapped:
        ex = (
            fda.loc[mapped.eq("UNMAPPED"), panel_col]
            .astype(str)
            .value_counts()
            .head(8)
        )
        print(f"  ! {n_unmapped} FDA devices had panels not in the mapping; top unmapped:")
        for panel, n in ex.items():
            print(f"      {panel!r}: {n}")

    counts = (
        mapped[mapped.ne("UNMAPPED")]
        .value_counts()
        .reindex(counts_index)
        .fillna(0.0)
    )
    # Structural zeros stay 0 (already filled). Return full series.
    return counts
```

Matching is **case-insensitive substring** against the FDA "Panel (Lead)" column; first match wins (the loop reassigns only where current mapping is still `UNMAPPED`).

---

## 8. Q7 re-classifier — failure-mode × model-type

**Canonical script:** `classify_q7_failuremode.py` @ `prompt-revision-v2` (commit `95fdc36`)
**Original location:** same filename on `analysis-session-5` at commit `88fc832` (byte-identical)
**Pipeline scripts (Q7 phases 1–3 + specialty + plateau analyses):** all on `prompt-revision-v2` at commit `95fdc36` (`q7_abstract_filter.py`, `q7_build_adjudication_xlsx.py`, `q7_build_coding_xlsx.py`, `q7_build_validation.py`, `q7_kappa.py`, `q7_kappa_compare.py`, `q7_phase1_figure.py`, `q7_phase1_summary.py`, `q7_phase2_concat.py`, `q7_phase3_analyses.py`, `q7_s5_1_a_specialty.py`, `q7_s5_1_b_plateau.py`)
**Outputs:** all `output/analyses/q7_*` and `output/figures/q7_*.png` committed on `prompt-revision-v2` at commit `95fdc36`

**What Q7 refers to.** "Q7" is the manuscript's research-question 7 — a follow-up classification on records with `stance = Alarm` (and optionally `Caution`) intended to separate "AI errors" into two mechanistically distinct failure modes: confabulation (generation of fabricated content) versus misclassification (predictive errors). The script and its outputs use the prefix `q7_` (e.g. `output/analyses/q7_classified_ac.csv`, `q7_kappa_report.md`).

### Verbatim SYSTEM_PROMPT

```text
Classify an AI/medical paper on two independent axes from the MECHANISM described, not from brand names (GPT/ChatGPT/etc).

Axis A — failure_mode:
- "confabulation": AI GENERATES fabricated/unfaithful content — invented citations or references, made-up facts, plausible-but-false text, hallucinated entities, unfaithful summaries.
- "misclassification": AI produces a wrong label/score/prediction/detection — false positives/negatives, misdiagnosis, miscalibration, poor generalization, dataset shift, biased predictions.
- "both": both mechanisms explicitly described.
- "none_or_unclear": no specific mechanism, or general "AI risks" framing.

Axis B — model_type:
- "generative": LLM, chatbot, text/image/code generator.
- "discriminative": predictive / classification / detection / segmentation / risk-scoring model.
- "both": both families explicitly evaluated.
- "unclear": cannot tell.

CALIBRATION EXAMPLES:
1. "ChatGPT scored 85% on USMLE-style questions" → {"failure_mode":"misclassification","model_type":"generative","confidence":0.9,"rationale":"accuracy of LLM responses, not fabrication"}
2. "DL classifier produced false-negative mammograms" → {"failure_mode":"misclassification","model_type":"discriminative","confidence":0.95,"rationale":"predictive model with classification errors"}
3. "LLM discharge summary fabricated a drug and an invented citation" → {"failure_mode":"confabulation","model_type":"generative","confidence":0.95,"rationale":"explicit fabrication of content and references"}
4. "Measured GPT-4 hallucinated references AND diagnostic accuracy" → {"failure_mode":"both","model_type":"generative","confidence":0.9,"rationale":"both fabrication and accuracy measured"}
5. "AI errors threaten safety, need oversight" (no mechanism) → {"failure_mode":"none_or_unclear","model_type":"unclear","confidence":0.6,"rationale":"general risk framing, no mechanism specified"}

Output STRICT JSON only, no prose, no code fences:
{"failure_mode":"confabulation|misclassification|both|none_or_unclear","model_type":"generative|discriminative|both|unclear","confidence":0.0-1.0,"rationale":"<=20 words"}
```

### `failure_mode` definitions (verbatim from prompt)

- **`confabulation`** — AI GENERATES fabricated/unfaithful content — invented citations or references, made-up facts, plausible-but-false text, hallucinated entities, unfaithful summaries.
- **`misclassification`** — AI produces a wrong label/score/prediction/detection — false positives/negatives, misdiagnosis, miscalibration, poor generalization, dataset shift, biased predictions.
- **`both`** — both mechanisms explicitly described.
- **`none_or_unclear`** — no specific mechanism, or general "AI risks" framing.

Validation constant (in the same file):

```python
VALID_FAILURE_MODES = {"confabulation", "misclassification", "both", "none_or_unclear"}
```

### `model_type` definitions (verbatim from prompt)

- **`generative`** — LLM, chatbot, text/image/code generator.
- **`discriminative`** — predictive / classification / detection / segmentation / risk-scoring model.
- **`both`** — both families explicitly evaluated.
- **`unclear`** — cannot tell.

```python
VALID_MODEL_TYPES = {"generative", "discriminative", "both", "unclear"}
```

### Model and request configuration (verbatim)

```python
MODEL          = "claude-sonnet-4-6"
TEMPERATURE    = 0.0
MAX_TOKENS     = 200
CONCURRENCY    = 5
```

| Setting | Value |
|---|---|
| model | `claude-sonnet-4-6` |
| **temperature** | **`0.0`** (explicitly set — unique among classifiers in this pipeline, all of which omit `temperature` and default to T=1.0) |
| max_tokens | `200` |
| concurrency | 5 |
| JSON shape required | `{"failure_mode": …, "model_type": …, "confidence": float 0.0-1.0, "rationale": "<=20 words"}` |

The `rationale` field is captured (up to 20 words per prompt). On parse failure or invalid category, fields default consistently (`failure_mode → "none_or_unclear"`, `model_type → "unclear"`).

---

## 9. Stats & reproducibility

### Bootstrap

**File:** `analysis/robustness.py` on `analysis-session-1..4`; relocated to repo root `robustness.py` on `analysis-session-5`. The function content is identical across these locations.
**Canonical commit (session-1):** `8553c4d`

**Verbatim core function:**

```python
def bootstrap_ci(
    df: pd.DataFrame,
    agg_fn: Callable[[pd.DataFrame], Union[float, pd.Series, pd.DataFrame]],
    n_boot: int = N_BOOT_DEFAULT,
    seed: int = SEED,
    confidence: float = 0.95,
) -> dict:
    """Resample df rows with replacement, apply agg_fn, percentile CI."""
    rng = np.random.default_rng(seed)
    point = agg_fn(df)
    kind, point_norm, idx = _coerce_agg(point)

    lo_q = (1 - confidence) / 2 * 100
    hi_q = 100 - lo_q

    n = len(df)

    def _sample():
        return df.iloc[rng.integers(0, n, size=n)].reset_index(drop=True)

    if kind == "scalar":
        samples = np.empty(n_boot)
        for i in range(n_boot):
            samples[i] = float(agg_fn(_sample()))
        return {
            "point": point_norm,
            "lower": float(np.percentile(samples, lo_q)),
            "upper": float(np.percentile(samples, hi_q)),
            "distribution": samples,
        }
```

| Parameter | Value |
|---|---|
| `n_boot` (iterations) | `N_BOOT_DEFAULT = 1000` |
| seed | `SEED = 42` (numpy `default_rng(seed)`) |
| CI method | **percentile** (2.5th and 97.5th by default) |
| confidence | 0.95 (configurable) |
| sample | rows resampled with replacement, size `n = len(df)` |

### Spearman correlation and trend tests

Used widely across `analysis/run_*.py` scripts on `analysis-session-1..5`. Always imported as `from scipy.stats import spearmanr` and called as `rho, p = spearmanr(YEARS, pts)`. Per-stance, per-region, per-specialty, per-theme variants exist in:

- `analysis/run_temporal_stance.py` (session-1+) — overall stance × year
- `analysis/run_region_temporal.py` (session-2+) — region × year
- `analysis/run_specialty_temporal.py` (session-2+) — specialty × year
- `analysis/run_theme_count_vs_rate.py` (session-4+) — theme × year

Verbatim theme-trend variant:

```python
def spearman_counts(table: pd.DataFrame, years: list[int]) -> dict:
    """Per-theme Spearman of count vs year over the given years."""
    out = {}
    for theme in CANONICAL_THEMES:
        sub = table[(table["theme"] == theme) & (table["pub_year"].isin(years))]
        sub = sub.sort_values("pub_year")
        c = sub["count"].values.astype(float)
        if np.ptp(c) == 0:
            rho, p = 0.0, 1.0
        else:
            rho, p = spearmanr(sub["pub_year"].values, c)
        out[theme] = {"rho": float(rho), "p": float(p), "trend": classify_trend(...)}
    return out
```

### Permutation tests

**NOT FOUND IN REPO.** No script imports `scipy.stats.permutation_test` or implements a permutation-based test. If the manuscript references permutation testing, **verify before stating**.

### Library versions

From the prompt-revision-v2 venv (`venv/lib/python3.12/site-packages/*.dist-info/`):

| Library | Version |
|---|---|
| **Python** | 3.12.3 |
| **pandas** | 3.0.2 |
| **numpy** | 2.4.4 |
| **scipy** | 1.17.1 |
| **matplotlib** | 3.10.9 |
| **geopandas** | 1.1.3 |
| **anthropic** | 0.100.0 |
| **statsmodels** | **NOT INSTALLED** |
| **openpyxl** | 3.1.5 |
| **python-dotenv** | 1.2.2 |
| **aiohttp** | 3.13.5 |
| **requests** | 2.33.1 |

> The `venv/` is gitignored and not part of the repo. The versions above were observed in the active virtualenv at the time this document was written; they should be locked into a `requirements.txt` before publication.

**Natural Earth version: NOT FOUND IN REPO.** No Natural Earth shapefile is committed under `input/`, `data/`, or anywhere else. `geopandas` is installed but its bundled Natural Earth dataset has been deprecated; if the manuscript reports a world map using `geopandas.datasets.naturalearth_lowres`, that path is removed in `geopandas >= 1.0`. The actual mapping path used by the committed `analysis/run_country_critical_map.py` should be re-checked.

---

## 10. Discrepancies & ambiguities

> These are the items most likely to embarrass the Methods section if stated without re-verification. Each entry identifies what the committed code actually does versus what session summaries / earlier drafts may have asserted.

### a. The four flags `{NO_STANCE, OUT_OF_SCOPE, DATA_INSUFFICIENT, META_DISCOURSE}` — resolved

These flags are **human-coder labels applied during the 300-record validation**, not LLM output. They live in `output/validation/kingsly_coding_sheet.xlsx` as additional columns Kingsley filled in by hand while coding stance. Flag counts on the 300-record sample: NO_STANCE 73, OUT_OF_SCOPE 2, DATA_INSUFFICIENT 0, META_DISCOURSE 14 (7 records had multiple flags).

The v1 LLM stance classifier does NOT emit these flags. The v2 LLM stance classifier emits a single `meta_discourse` field (yes/no) that overlaps semantically with the human `META_DISCOURSE` flag.

**Methods statement should clarify**: "stance v1 output is one of five categories plus a FAILED sentinel; for the 300-record validation the human coder additionally applied four orthogonal flags (NO_STANCE, OUT_OF_SCOPE, DATA_INSUFFICIENT, META_DISCOURSE) to mark records the rubric should treat specially. Flags are used to build sensitivity-analysis subsets (Sensitivity A: exclude NO_STANCE; Sensitivity B: exclude NO_STANCE and META_DISCOURSE) rather than overriding stance assignments."

### b. April 2026 cutoff was applied in two stages — both are needed

The fetch query itself caps `[PDAT]` at April 2026 via the `CUTOFF_YEAR=2026, CUTOFF_MONTH=4` constants and the `process_year` month-loop. *Additionally*, a one-shot inline pandas filter (executed during the Saturday session, not in any committed `.py` script) removed records where the **`PubDate` cover-date** parsed to May 2026 or later. The Q1/Q2 file dropped from 98,626 → 97,492 (1,134 records), Q3 from 5,463 → 5,433. **No committed `.py` script performs this PubDate-based cutoff.** Documentation note for the manuscript: the canonical Q1/Q2 corpus of 97,492 reflects *both* an `[PDAT] ≤ Apr 2026` query window *and* a post-fetch `PubDate ≤ Apr 2026` filter.

### c. Abstract truncation differs across classifiers

| Step | Truncation | File |
|---|---|---|
| Prefilter (Haiku) | **first 300 chars** | `prefilter.py:50`, `prefilter_batch.py` |
| Stance (Sonnet, canonical v1) | **none** (full abstract) | `classify_stance.py` @ `9c79cd5+` |
| Stance (Sonnet, pre-canonical) | `[:400]` chars | `classify_stance.py` @ `8500d89` |
| Themes (Sonnet) | `[:400]` chars | `classify_themes.py`, `classify_themes_batch.py` |

The themes classifier still truncates at 400 chars. If the manuscript claims uniform "no truncation" or "1500-char truncation" across the LLM stack, that is incorrect; only stance v1.1+ removed truncation.

### d. `pub_year` reflects PubDate (publication date), not EDAT / index date

See §1a above. The retrieval filter is PDAT; the *stored* column is the publisher-encoded publication year. These are usually consistent but can diverge for ahead-of-print papers.

### e. Q3 comparison arm has Dan's pre-existing outputs, but the Saturday re-run did NOT include Q3

`output/filtered_medical_all_Q3.csv` was regenerated by the Saturday SJR re-run (5,433 records post-cutoff). However, neither `prefilter.py Q3` nor `classify_stance.py Q3` was executed in the canonical Saturday session; Dan's pre-existing `output/prefiltered_Q3_discourse_eval.csv` (committed at `main`, `8500d89`) is what's on disk. **If the manuscript reports Q1/Q2 vs Q3 comparisons, those Q3 numbers come from Dan's prior pipeline run, not the Saturday Batch-API run.** Re-run if a like-for-like comparison is needed.

### f. The `prompt-revision-v2` branch — resolved

v2 was committed at `2559e6b` on `prompt-revision-v2`. v1 stays canonical; v2 is supplementary only (per author guidance, not to be merged to `main` or any `analysis-session-*`). v1→v2 reclassification: 80.1% unchanged, 19.9% migrated (chiefly CO and Caution → Neutral as v2 enforces "stance must come from the conclusion, not background framing").

### g. Specialty / FDA / Q7 — partially resolved on `prompt-revision-v2`

`prompt-revision-v2` at commit `95fdc36` now contains:
- `classify_q7_failuremode.py` (root-level, byte-identical to the `analysis-session-5` copy at `88fc832`) plus the full Q7 phase pipeline (`q7_*.py` scripts) and outputs (`output/analyses/q7_*`, `output/figures/q7_*.png`)
- `output/specialty_classifications.csv` (specialty outputs; the *runner script* `analysis/classify_specialty.py` still lives only on `analysis-session-2`)
- `robustness.py` at repo root (relocated from `analysis/robustness.py`)

**Still on `analysis-session-4` only:** `analysis/run_specialty_aiadoption.py` (FDA proxy runner). The FDA source CSV (`output/external/fda_aiml_devices.csv`) is uncommitted on every branch.

**For Methods reproducibility**: `prompt-revision-v2` is the most-complete single branch for reproducing the manuscript's outputs. The FDA proxy run still requires checking out `analysis-session-4` and supplying the uncommitted FDA CSV.

### h. `analysis/robustness.py` vs `robustness.py` location swap

On `analysis-session-1..4`, this lives at `analysis/robustness.py`. On `analysis-session-5`, it lives at repo-root `robustness.py`. Content of `bootstrap_ci` is identical, but **import paths differ across branches**; any cross-branch tooling that does `from analysis.robustness import bootstrap_ci` will fail on session-5 and vice versa. Methods text should reference the function name, not a specific import path.

### i. Mexico is a duplicate key in `COUNTRY_REGION` → resolves to Latin America at runtime

See §6 country resolution. If the manuscript reports Mexico under North America, that disagrees with the executed code (which silently overrode it to Latin America via the duplicate-key behaviour of Python dict literals). Verify against actual output rows.

### j. Coverage figures `~90.3%` (country) and `~98.4%` (affiliation) are not pinned in code

These percentages are not constants in any committed script. They are inferred from running the resolution functions over the corpus. Before stating either number in the manuscript, recompute against `output/classified_medical_Q1Q2.csv` using the current canonical scripts and report the actual %.

### k. FDA AI/ML device file is not committed

`output/external/fda_aiml_devices.csv` is consumed by the FDA proxy script but is absent from every branch. The Methods section must (i) state the download URL, (ii) state the download date, (iii) ideally commit the snapshot used to compute reported numbers.

### l. Temperatures are inconsistent across LLM calls

| Step | `temperature` setting | Default applied |
|---|---|---|
| Prefilter (Haiku) | omitted | T=1.0 |
| Stance (Sonnet) | omitted | T=1.0 |
| Themes (Sonnet) | omitted | T=1.0 |
| Specialty (Haiku) | omitted | T=1.0 |
| **Q7 re-classifier (Sonnet)** | **explicit `TEMPERATURE = 0.0`** | T=0.0 |

The Q7 step is deterministic (T=0); the rest of the pipeline is stochastic (T=1). The Methods should state this difference explicitly; the manuscript may want to re-run prefilter / stance / themes at T=0 if temperature stability is needed for replication.

### m. Cohen's κ values — resolved

- **Prefilter pilot (n=200, Haiku 4.5 vs Kingsley):** raw agreement 85.5%, unweighted κ = 0.51 (CI 0.35–0.68). See §2.
- **300-record stance validation (n=300, Sonnet 4.6 v1 vs Kingsley):**
  - Primary (all 300): unweighted κ = 0.564 (0.494–0.630); linear κ = 0.659; quadratic κ = **0.752** (0.685–0.811).
  - Sensitivity A (excl. NO_STANCE, n=225): quadratic κ = 0.789 (0.724–0.841).
  - Sensitivity B (excl. NO_STANCE + META_DISCOURSE, n=218): quadratic κ = 0.799 (0.731–0.853).
  - Report weighted (quadratic) κ as the primary number for an ordered-categorical outcome.
- `coding_instructions.txt` (Dan's text, retained verbatim) states a target of "κ ≥ 0.75"; the quadratic κ on the primary sample (0.752) hits this. The unweighted κ (0.564) is moderate; do not lead the Methods with the unweighted value for an ordinal scale.

### n. The `n < 30 rare specialty` rule is referenced but its verbatim threshold has not been re-verified

The agent audit reports a downstream rule that flags specialties with fewer than 30 records as `low_confidence` and excludes them from bootstrap CI; this lives in `analysis-session-5`'s analysis scripts (likely `q7_s5_1_a_specialty.py`). The exact line and surrounding logic were not extracted verbatim. **Before publishing the Methods sentence on the rare-specialty rule, run `git show analysis-session-5:<path>` for the threshold and paste the literal code here.**

---

## Appendix A — File locations for each committed instrument

| Instrument | Canonical file | Branch | Commit |
|---|---|---|---|
| PubMed fetch | `fetch_pubmed_medical.py` | prompt-revision-v2 | `9c79cd5` |
| SJR filter | `sjr_filter.py` | (identical on all) | `8500d89` |
| SJR data tables | `input/sjr/sjr_{2021..2026}.csv` | (identical on all) | `8500d89` |
| Prefilter (canonical, Batch) | `prefilter_batch.py` | prompt-revision-v2 | `9c79cd5` |
| Prefilter (async) | `prefilter.py` | prompt-revision-v2 | `9c79cd5` |
| **Stance v1 (canonical)** | `classify_stance.py`, `classify_stance_batch.py` | prompt-revision-v2 | `9c79cd5` |
| **Stance v2 (supplementary)** | `classify_stance_batch.py` | **prompt-revision-v2 only** | `2559e6b` |
| Stance v1 backup snapshot | `classify_stance_batch.py.v1_backup` | prompt-revision-v2 | `2559e6b` |
| Themes (canonical, Batch) | `classify_themes_batch.py` | prompt-revision-v2 | `9c79cd5` |
| Themes (async) | `classify_themes.py` | prompt-revision-v2 | `9c79cd5` |
| Specialty runner | `analysis/classify_specialty.py` | analysis-session-2 | `a30aaf7` |
| Specialty outputs | `output/specialty_classifications.csv` | prompt-revision-v2 | `95fdc36` |
| Geography (country) | `analyse_geography.py` | (identical on all) | `8500d89` |
| Affiliation type | `analyse_industry.py` | (identical on all) | `8500d89` |
| FDA proxy runner | `analysis/run_specialty_aiadoption.py` | analysis-session-4 | `c6b9092` |
| Q7 re-classifier (canonical) | `classify_q7_failuremode.py` | prompt-revision-v2 | `95fdc36` (originated `88fc832` @ analysis-session-5) |
| Q7 pipeline scripts | `q7_*.py` (13 files at repo root) | prompt-revision-v2 | `95fdc36` |
| Q7 outputs | `output/analyses/q7_*` and `output/figures/q7_*.png` | prompt-revision-v2 | `95fdc36` |
| Robustness (bootstrap, canonical) | `robustness.py` | prompt-revision-v2 | `95fdc36` |
| Robustness (legacy paths) | `analysis/robustness.py` | analysis-session-1..4 | `8553c4d` |
| Compute κ (v1) | `compute_kappa.py` | prompt-revision-v2 | `95fdc36` |
| Compute κ (v1/v2) | `compute_kappa_v2.py` | prompt-revision-v2 | `2559e6b` |
| Validation export | `export_validation.py` | prompt-revision-v2 | `9c79cd5` |
| Coding sheet (300 records, with codes) | `output/validation/kingsly_coding_sheet.xlsx` | prompt-revision-v2 | `95fdc36` |
| Validation κ report | `output/validation/kappa_report.md` | prompt-revision-v2 | `95fdc36` |
| Validation confusion matrices | `output/validation/confusion_matrices.png` | prompt-revision-v2 | `95fdc36` |
| Validation disagreements | `output/validation/disagreements.csv` | prompt-revision-v2 | `95fdc36` |
| v1/v2 comparison | `output/comparison_v1_v2.md` | prompt-revision-v2 | `2559e6b` |
| v1/v2 human-comparison | `output/validation/v1_v2_human_comparison.csv` | prompt-revision-v2 | `2559e6b` |
| Pilot input (200 records) | `output/pilot_200.xlsx` | prompt-revision-v2 | `9c79cd5` |
| Pilot agreement | `output/pilot_200_full_haiku.csv` | prompt-revision-v2 | `9c79cd5` |
| Stance v1 canonical output | `output/classified_medical_Q1Q2.csv` | prompt-revision-v2 | `9c79cd5` |
| Stance v2 supplementary output | `output/classified_medical_Q1Q2_v2_pre_predclaim_fix.csv` | prompt-revision-v2 | `2559e6b` |
| Themes canonical output | `output/analysis/thematic_alarm.csv` | prompt-revision-v2 | `9c79cd5` |

## Appendix B — Items the author must re-verify before publication

1. The `n<30` rare-specialty threshold's verbatim text (§5) — now in `q7_s5_1_a_specialty.py` @ commit `95fdc36`.
2. The literal country-resolution coverage (~90.3%) — recompute (§6).
3. The literal affiliation-type coverage (~98.4%) — recompute (§6).
4. FDA AI/ML devices file's download URL, snapshot date, and total count (§7) — source CSV still uncommitted.
5. ~~The four-flag stance taxonomy (§3, §10a)~~ — **resolved**: they are human-coder flags on the 300-record sheet, not LLM output.
6. ~~The "stance v1 vs v2" distinction (§3, §10f)~~ — **resolved**: v2 prompt committed at `2559e6b`, supplementary only.
7. Whether the Q3 comparison arm uses Dan's prior pipeline (committed) or a fresh Batch-API re-run (§10e). The session 2 fixup at commit `95fdc36` points `classify_stance.py Q3` at `prefiltered_Q3_discourse_eval.csv` instead of raw `filtered_medical_all_Q3.csv`, but no record of an actual Q3 Batch-API rerun on Saturday's corpus is in the repo. **If the manuscript reports Q3 numbers, re-verify which Q3 pipeline produced them.**
8. ~~Cohen's κ for the 300-record stance validation (§10m)~~ — **resolved**: report quadratic κ = 0.752 (primary) for ordered-categorical scale.
9. Natural Earth shapefile / dataset version if a world map appears in the manuscript (§9).
10. Exact pandas / scipy / matplotlib / geopandas pinned versions in a `requirements.txt` (§9).
