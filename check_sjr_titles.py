"""
Check what titles SCImago uses for the unmatched journals.
Run locally against your sjr_2024.csv to find the correct SCImago title.
"""

# PubMed titles from unmatched list that are likely real Q1/Q2 journals
# We'll search the SJR file for close matches

import csv, sys, re

sjr_path = r"input\sjr\sjr_2024.csv"

def normalise(t):
    t = t.lower().strip()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

# Load all SJR titles
sjr_titles = {}
with open(sjr_path, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        title = row.get("Title", "").strip()
        quartile = row.get("SJR Best Quartile", "").strip()
        if title:
            sjr_titles[normalise(title)] = (title, quartile)

# Journals to search for
targets = [
    "Sensors (Basel, Switzerland)",
    "Diagnostics (Basel, Switzerland)",
    "Cureus",
    "Bioengineering (Basel, Switzerland)",
    "Journal of imaging informatics in medicine",
    "Medical & biological engineering & computing",
    "Journal of the American Medical Informatics Association : JAMIA",
    "Medicine",
    "Journal of magnetic resonance imaging : JMRI",
    "Computerized medical imaging and graphics",
    "Abdominal radiology (New York)",
    "IEEE transactions on neural systems and rehabilitation engineering",
    "Technology and health care",
    "International journal of surgery (London, England)",
    "Neural networks",
    "European archives of oto-rhino-laryngology",
    "Biomedical physics & engineering express",
    "Radiotherapy and oncology",
    "Translational vision science & technology",
    "Computer methods in biomechanics and biomedical engineering",
    "Ultrasound in medicine & biology",
    "Arthroscopy",
    "Advanced science (Weinheim, Baden-Wurttemberg, Germany)",
    "Current medical imaging",
]

print(f"{'PubMed title':<55} {'SJR match':<50} Q")
print("-" * 115)
for target in targets:
    norm_target = normalise(target)
    # Try progressively shorter prefix matches
    match_title, match_q = "", ""
    # Exact
    if norm_target in sjr_titles:
        match_title, match_q = sjr_titles[norm_target]
    else:
        # First 4 words
        words = norm_target.split()[:4]
        prefix = " ".join(words)
        candidates = [(k, v) for k, v in sjr_titles.items() if k.startswith(prefix)]
        if candidates:
            match_title, match_q = candidates[0][1]
    print(f"{target[:54]:<55} {match_title[:49]:<50} {match_q}")
