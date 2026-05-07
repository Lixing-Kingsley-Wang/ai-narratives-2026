"""
Smarter SJR title lookup using token overlap scoring.
Finds best SCImago match for each unmatched PubMed journal title.
"""
import csv, re, collections

sjr_path = r"input\sjr\sjr_2024.csv"

def normalise(t):
    t = t.lower().strip()
    t = re.sub(r"\(.*?\)", "", t)          # remove parentheticals
    t = re.sub(r":.*$", "", t)             # remove subtitle after colon
    t = re.sub(r"[^a-z0-9 ]", " ", t)     # remove special chars incl &
    t = re.sub(r"\b(the|a|an|of|in|and|for|on|with)\b", "", t)  # stopwords
    return re.sub(r"\s+", " ", t).strip()

def token_overlap(a, b):
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))

# Load SJR
sjr_entries = []
with open(sjr_path, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f, delimiter=";"):
        title    = row.get("Title", "").strip()
        quartile = row.get("SJR Best Quartile", "").strip()
        issn     = row.get("Issn", "").strip()
        if title:
            sjr_entries.append((normalise(title), title, quartile, issn))

targets = [
    "Sensors (Basel, Switzerland)",
    "Diagnostics (Basel, Switzerland)",
    "Cureus",
    "Bioengineering (Basel, Switzerland)",
    "Medical & biological engineering & computing",
    "Journal of the American Medical Informatics Association : JAMIA",
    "Medicine",
    "Abdominal radiology (New York)",
    "Biomedical physics & engineering express",
    "Translational vision science & technology",
    "Advanced science (Weinheim, Baden-Wurttemberg, Germany)",
    "Ultrasound in medicine & biology",
    "Journal of imaging informatics in medicine",
    "Current medical imaging",
    "Technology and health care",
]

print(f"{'PubMed title':<55} {'Best SJR match':<48} {'Q':<4} {'Score'}")
print("-" * 120)
for target in targets:
    norm_t = normalise(target)
    best_score, best_title, best_q, best_issn = 0, "", "", ""
    for norm_s, orig_s, q, issn in sjr_entries:
        score = token_overlap(norm_t, norm_s)
        if score > best_score:
            best_score, best_title, best_q, best_issn = score, orig_s, q, issn
    print(f"{target[:54]:<55} {best_title[:47]:<48} {best_q:<4} {best_score:.2f}")
