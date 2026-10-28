"""B6 · Re-fetch MeSH descriptors and author keywords for the 16,759 retained
PMIDs (JMIR R1 Batch 2b; D5). NCBI E-utilities efetch (db=pubmed,
retmode=xml), 200 PMIDs per request, ≤3 requests/s (no NCBI API key), with
tool/email as in fetch_pubmed_medical.py (email read from the main
checkout's .env; never printed or written). Raw XML is stored gzipped per
batch (resumable); a parsed table is written afterwards.

Usage: python b6_fetch_mesh.py fetch | parse
"""

from __future__ import annotations

import csv
import gzip
import sys
import time
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

from dotenv import dotenv_values

REPO = Path(__file__).resolve().parents[2]
MAIN = Path("/Users/kingslywang/Documents/科研/ai-narratives-2026")
OUT = REPO / "revision_r1" / "outputs" / "B6"
RAW = OUT / "raw"
URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH, SLEEP, TOOL, RETRIES = 200, 0.4, "ai_narratives_study", 3


def pmids():
    with open(MAIN / "output" / "prefiltered_discourse_eval.csv", encoding="utf-8") as f:
        ids = [r["pmid"] for r in csv.DictReader(f)]
    assert len(ids) == len(set(ids)) == 16759
    return sorted(ids, key=int)


def fetch():
    RAW.mkdir(parents=True, exist_ok=True)
    email = dotenv_values(MAIN / ".env").get("EMAIL")
    if not email:
        sys.exit("EMAIL not found in main checkout .env")
    ids = pmids()
    for b in range(0, len(ids), BATCH):
        out = RAW / f"batch_{b // BATCH:03d}.xml.gz"
        if out.exists():
            continue
        data = urllib.parse.urlencode({"db": "pubmed", "retmode": "xml", "id": ",".join(ids[b:b + BATCH]),
                                       "tool": TOOL, "email": email}).encode()
        for attempt in range(1, RETRIES + 1):
            try:
                # curl with system trust (TLS verification on); POST body via stdin so the
                # email never appears in argv. The python.org Python here lacks a CA bundle.
                r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "120", "--data-binary", "@-", URL],
                                   input=data, capture_output=True, check=True)
                xml = r.stdout
                ET.fromstring(xml)  # must parse
                break
            except Exception as e:
                print(f"  batch {b // BATCH}: attempt {attempt} failed ({type(e).__name__})", flush=True)
                if attempt == RETRIES:
                    raise
                time.sleep(12 * attempt)
        with gzip.open(out, "wb") as f:
            f.write(xml)
        print(f"  batch {b // BATCH:03d}: {len(ids[b:b + BATCH])} PMIDs, {len(xml):,} bytes", flush=True)
        time.sleep(SLEEP)


def parse():
    rows = []
    for p in sorted(RAW.glob("batch_*.xml.gz")):
        root = ET.fromstring(gzip.open(p).read())
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext("./MedlineCitation/PMID")
            mesh = []
            for mh in art.findall("./MedlineCitation/MeshHeadingList/MeshHeading"):
                dn = mh.find("DescriptorName")
                if dn is not None and dn.text:
                    major = dn.get("MajorTopicYN", "N") == "Y" or any(q.get("MajorTopicYN") == "Y" for q in mh.findall("QualifierName"))
                    mesh.append(f"{''.join(dn.itertext()).strip()}{'*' if major else ''}")
            kws = ["".join(k.itertext()).strip() for k in art.findall("./MedlineCitation/KeywordList/Keyword")]
            kws = [k for k in kws if k]
            rows.append({"pmid": pmid, "mesh": "|".join(mesh), "n_mesh": len(mesh),
                         "keywords": "|".join(kws), "n_keywords": len(kws)})
    ids = set(pmids())
    got = {r["pmid"] for r in rows}
    with open(OUT / "b6_mesh_keywords.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["pmid", "mesh", "n_mesh", "keywords", "n_keywords"])
        w.writeheader(); w.writerows(r for r in rows if r["pmid"] in ids)
    print(f"parsed {len(rows):,} articles; requested {len(ids):,}; missing {len(ids - got)}; extra {len(got - ids)}")
    (OUT / "b6_fetch_missing_pmids.txt").write_text("\n".join(sorted(ids - got, key=int)) + "\n")


if __name__ == "__main__":
    {"fetch": fetch, "parse": parse}[sys.argv[1]]()
