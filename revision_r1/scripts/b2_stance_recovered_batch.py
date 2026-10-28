"""
B2 · v1 stance on the records recovered by the full-abstract prefilter re-run
=============================================================================
(JMIR R1 Batch 2b; D1, X2). Copy of classify_stance_batch.py.v1_backup, which
is byte-identical to the production batch script at commit 9c79cd5. Kept
verbatim from it: MODEL, MAX_TOKENS, VALID_*, SYSTEM_PROMPT (SHA-256 asserted
equal to classify_stance.py and to 9c79cd5:classify_stance_batch.py),
build_prompt and parse_response (which already returns FAILED on any parse
failure; no default stance). Temperature not set. Changed: the frame (the
2,850 records with production = application and full-abstract =
discourse/evaluative), output location (revision_r1/outputs/B2/), one
resubmission of FAILED records, and the token-count cost gate (ceiling USD 25),
all via b_batch_engine.

Usage: python b2_stance_recovered_batch.py count|submit|poll|resubmit|poll2|finalize
"""
import ast, csv, hashlib, json, re, subprocess, sys
from pathlib import Path

import b_batch_engine as E

# ── constants (verbatim from the production v1 batch script) ──────────────────
MODEL       = "claude-sonnet-4-6"
MAX_TOKENS  = 120
VALID_STANCES    = {"Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"}
VALID_CONFIDENCE = {"High", "Medium", "Low"}

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


# ── R1 wiring ─────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "revision_r1" / "outputs" / "B2"
FIELDS = ["stance", "confidence", "predictive_claim", "stance_raw"]


def _prompt_of(src):
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "SYSTEM_PROMPT" for t in n.targets):
            return ast.literal_eval(n.value)


def assert_prompt():
    h = lambda s: hashlib.sha256(s.encode()).hexdigest()
    ref1 = _prompt_of((REPO / "classify_stance.py").read_text())
    ref2 = _prompt_of(subprocess.run(["git", "show", "9c79cd5:classify_stance_batch.py"], cwd=REPO,
                                     capture_output=True, text=True, check=True).stdout)
    assert h(SYSTEM_PROMPT) == h(ref1) == h(ref2), "v1 SYSTEM_PROMPT mismatch"
    return h(SYSTEM_PROMPT)


def parse(text):
    stance, conf, pred, raw = parse_response(text)
    if stance == "FAILED":
        return {}, raw
    return {"stance": stance, "confidence": conf, "predictive_claim": pred, "stance_raw": raw}, ""


def frame():
    lab = list(csv.DictReader(open(REPO / "revision_r1/outputs/A2/a2_fullabstract_labels.csv")))
    rec = {r["pmid"] for r in lab if r["label_production"] == "application"
           and r["label_fullabstract"] in ("discourse", "evaluative")}
    corpus = E.MAIN / "output" / "filtered_medical_all_Q1Q2.csv"
    rows = [r for r in csv.DictReader(open(corpus, encoding="utf-8")) if r["pmid"] in rec]
    assert len(rows) == len(rec) == 2850, (len(rows), len(rec))
    return rows


if __name__ == "__main__":
    print(f"v1 SYSTEM_PROMPT sha256 {assert_prompt()}", flush=True)
    job = E.Job("b2_stance", OUT, MODEL, MAX_TOKENS, None, SYSTEM_PROMPT, frame(),
                lambda r: build_prompt(r.get("title", ""), r.get("abstract", "")), parse,
                ceiling=25.0, out_tokens_assumed=40)
    E.run(job, FIELDS, sys.argv)
