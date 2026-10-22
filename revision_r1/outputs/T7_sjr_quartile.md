# T7 · SJR quartile feasibility (D6)

Script: `revision_r1/scripts/t7_sjr_quartile.py`. Matching reuses `sjr_filter.py` (`normalise`, `ALIAS_PATCH`, publication-year file with 2024 fallback). Nothing downstream was rerun.

## 1. What the SJR files contain

- `input/sjr/sjr_2021.csv` … `sjr_2026.csv` (semicolon-delimited). Columns include `SJR Best Quartile`, **`Categories`** (each category with its own quartile, e.g. `Hematology (Q1); Oncology (Q1)`), and **`Areas`** (subject areas, e.g. `Medicine`). `sjr_filter.py` reads only `Title` and `SJR Best Quartile`.
- `sjr_2026.csv` is identical to `sjr_2025.csv` (Methods source-of-truth §1c).
- Re-matched 97,492/97,492 included Q1/Q2 records to an SJR row (0 unmatched on re-run). Best quartile on re-match equals the stored `sjr_quartile` for 97,492/97,492.
- The `Areas` field is journal-level; categories are not tagged with an area in the file. Category → area was therefore inferred from single-area journals (column `main_area` in the csv); categories that only ever appear in multi-area journals are marked unknown.

## 2. Categories carried by included journals

283 distinct categories; full list with inferred area, record counts and membership in each candidate definition: [T7_categories_in_included_journals.csv](T7_categories_in_included_journals.csv). By inferred area:

| main_area (from single-area journals) | categories | included_records |
|---|---|---|
| Medicine | 47 | 109775 |
| Biochemistry, Genetics and Molecular Biology | 15 | 36173 |
| Computer Science | 12 | 25498 |
| Engineering | 12 | 11067 |
| Multidisciplinary | 1 | 9299 |
| Neuroscience | 9 | 8853 |
| Physics and Astronomy | 10 | 8041 |
| Chemistry | 7 | 7156 |
| Health Professions | 13 | 5040 |
| unknown (only in multi-area journals) | 4 | 4308 |
| Pharmacology, Toxicology and Pharmaceutics | 5 | 3634 |
| Mathematics | 12 | 3542 |
| Immunology and Microbiology | 6 | 3477 |
| Environmental Science | 12 | 3155 |
| Nursing | 19 | 2931 |
| Social Sciences | 23 | 2536 |
| Chemical Engineering | 8 | 2496 |
| Dentistry | 6 | 1973 |
| Materials Science | 9 | 1959 |
| Agricultural and Biological Sciences | 9 | 1698 |
| Psychology | 7 | 1326 |
| Decision Sciences | 4 | 571 |
| Arts and Humanities | 7 | 432 |
| Veterinary | 4 | 290 |
| Earth and Planetary Sciences | 9 | 209 |
| Energy | 3 | 76 |
| Business, Management and Accounting | 8 | 74 |
| Economics, Econometrics and Finance | 2 | 15 |

## 3. Candidate definitions of 'medicine-related' (none chosen)

- **D1 Medicine area (ASJC 27xx) categories**: 47 categories among included journals.
- **D2 D1 minus 'Medicine (miscellaneous)'**: 46 categories among included journals.
- **D3 broad health sciences (Medicine, Nursing, Dentistry, Health Professions, Neuroscience, Pharmacology, Immunology & Microbiology, Psychology)**: 112 categories among included journals.

## 4. Records and journals whose Q1/Q2 status depends only on a non-medical category

A record 'depends only on a non-medical category' when its journal is Q1/Q2 by best quartile but its best quartile among medicine-related categories is Q3, Q4, or the journal has no medicine-related category.

| definition | scope | records | records whose Q1/Q2 depends only on a non-medical category | % |   of which medical best = Q3 |   of which medical best = Q4 |   of which no medical category | journals (journal-title × any year) | journals total |
|---|---|---|---|---|---|---|---|---|---|
| D1 Medicine area (ASJC 27xx) categories | eligible Q1/Q2 (97,492) | 97492 | 26456 | 27.140 | 1392 | 5 | 25059 | 1219 | 4060 |
| D1 Medicine area (ASJC 27xx) categories | analytic set (16,747) | 16747 | 2781 | 16.610 | 205 | 2 | 2574 | 519 | 2465 |
| D2 D1 minus 'Medicine (miscellaneous)' | eligible Q1/Q2 (97,492) | 97492 | 37483 | 38.450 | 1046 | 1 | 36436 | 1656 | 4060 |
| D2 D1 minus 'Medicine (miscellaneous)' | analytic set (16,747) | 16747 | 4607 | 27.510 | 166 | 0 | 4441 | 748 | 2465 |
| D3 broad health sciences (Medicine, Nursing, Dentistry, Health Professions, Neuroscience, Pharmacology, Immunology & Microbiology, Psychology) | eligible Q1/Q2 (97,492) | 97492 | 21308 | 21.860 | 1217 | 4 | 20087 | 716 | 4060 |
| D3 broad health sciences (Medicine, Nursing, Dentistry, Health Professions, Neuroscience, Pharmacology, Immunology & Microbiology, Psychology) | analytic set (16,747) | 16747 | 1546 | 9.230 | 121 | 2 | 1423 | 217 | 2465 |

### Top 20 journals by record count — D1 Medicine area (ASJC 27xx) categories

| journal | records | analytic_records | best_q | medical_best | categories |
|---|---|---|---|---|---|
| Scientific Reports | 6263 | 343 | Q1 | none | Multidisciplinary (Q1) |
| PLOS ONE | 1926 | 139 | Q1 | none | Multidisciplinary (Q1) |
| Diagnostics | 765 | 87 | Q2 | none | Clinical Biochemistry (Q2) |
| Nature Communications | 550 | 33 | Q1 | none | Biochemistry, Genetics and Molecular Biology (miscellaneous) (Q1); Chemistry (miscellaneous) (Q1); Multidiscip |
| IEEE Transactions on Medical Imaging | 528 | 3 | Q1 | none | Computer Science Applications (Q1); Electrical and Electronic Engineering (Q1); Radiological and Ultrasound Te |
| Bioengineering | 487 | 62 | Q2 | none | Bioengineering (Q2) |
| Briefings in Bioinformatics | 425 | 18 | Q1 | none | Information Systems (Q1); Molecular Biology (Q1) |
| Medical and Biological Engineering and Computing | 380 | 5 | Q2 | none | Biomedical Engineering (Q2); Computer Science Applications (Q2) |
| Heliyon | 275 | 18 | Q1 | none | Multidisciplinary (Q1) |
| IEEE Transactions on Biomedical Engineering | 268 | 3 | Q1 | none | Biomedical Engineering (Q1) |
| BMC Oral Health | 257 | 108 | Q1 | none | Dentistry (miscellaneous) (Q1) |
| Frontiers in Artificial Intelligence | 246 | 77 | Q1/Q2 | none | Artificial Intelligence (Q1) |
| Computational and Mathematical Methods in Medicine (discontinued) | 240 | 2 | Q2 | Q3 | Applied Mathematics (Q2); Biochemistry, Genetics and Molecular Biology (miscellaneous) (Q2); Modeling and Simu |
| Scientific Data | 223 | 7 | Q1 | none | Computer Science Applications (Q1); Education (Q1); Information Systems (Q1); Library and Information Sciences |
| BMC Bioinformatics | 220 | 2 | Q1 | none | Applied Mathematics (Q1); Biochemistry (Q1); Computer Science Applications (Q1); Molecular Biology (Q2); Struc |
| Frontiers in Neuroscience | 206 | 15 | Q2 | none | Neuroscience (miscellaneous) (Q2) |
| Neural Networks | 193 | 4 | Q1 | none | Artificial Intelligence (Q1); Cognitive Neuroscience (Q1) |
| PeerJ Computer Science | 183 | 7 | Q1/Q2 | none | Computer Science (miscellaneous) (Q2) |
| Analytical Chemistry | 171 | 1 | Q1 | none | Analytical Chemistry (Q1) |
| Bioinformatics | 166 | 2 | Q1 | none | Biochemistry (Q1); Computational Mathematics (Q1); Computational Theory and Mathematics (Q1); Computer Science |

### Top 20 journals by record count — D2 D1 minus 'Medicine (miscellaneous)'

| journal | records | analytic_records | best_q | medical_best | categories |
|---|---|---|---|---|---|
| Scientific Reports | 6263 | 343 | Q1 | none | Multidisciplinary (Q1) |
| Sensors | 2196 | 64 | Q1 | none | Analytical Chemistry (Q1); Electrical and Electronic Engineering (Q1); Instrumentation (Q1); Atomic and Molecu |
| PLOS ONE | 1926 | 139 | Q1 | none | Multidisciplinary (Q1) |
| Diagnostics | 765 | 87 | Q2 | none | Clinical Biochemistry (Q2) |
| Nature Communications | 550 | 33 | Q1 | none | Biochemistry, Genetics and Molecular Biology (miscellaneous) (Q1); Chemistry (miscellaneous) (Q1); Multidiscip |
| IEEE Transactions on Medical Imaging | 528 | 3 | Q1 | none | Computer Science Applications (Q1); Electrical and Electronic Engineering (Q1); Radiological and Ultrasound Te |
| Frontiers in Medicine | 520 | 118 | Q1 | none | Medicine (miscellaneous) (Q1) |
| Bioengineering | 487 | 62 | Q2 | none | Bioengineering (Q2) |
| International Journal of Molecular Sciences | 479 | 22 | Q1 | none | Catalysis (Q1); Computer Science Applications (Q1); Inorganic Chemistry (Q1); Medicine (miscellaneous) (Q1); O |
| Briefings in Bioinformatics | 425 | 18 | Q1 | none | Information Systems (Q1); Molecular Biology (Q1) |
| Journal of Clinical Medicine | 405 | 175 | Q1/Q2 | none | Medicine (miscellaneous) (Q2) |
| BMJ Open | 387 | 85 | Q1 | none | Medicine (miscellaneous) (Q1) |
| Medical and Biological Engineering and Computing | 380 | 5 | Q2 | none | Biomedical Engineering (Q2); Computer Science Applications (Q2) |
| Computational and Mathematical Methods in Medicine (discontinued) | 352 | 5 | Q2 | none | Applied Mathematics (Q2); Biochemistry, Genetics and Molecular Biology (miscellaneous) (Q2); Modeling and Simu |
| Heliyon | 275 | 18 | Q1 | none | Multidisciplinary (Q1) |
| JAMA Network Open | 271 | 103 | Q1 | none | Medicine (miscellaneous) (Q1) |
| IEEE Transactions on Biomedical Engineering | 268 | 3 | Q1 | none | Biomedical Engineering (Q1) |
| BMC Oral Health | 257 | 108 | Q1 | none | Dentistry (miscellaneous) (Q1) |
| Journal of Translational Medicine | 249 | 15 | Q1 | none | Biochemistry, Genetics and Molecular Biology (miscellaneous) (Q1); Medicine (miscellaneous) (Q1) |
| Artificial Intelligence in Medicine | 248 | 31 | Q1 | none | Artificial Intelligence (Q1); Medicine (miscellaneous) (Q1) |

### Top 20 journals by record count — D3 broad health sciences (Medicine, Nursing, Dentistry, Health Professions, Neuroscience, Pharmacology, Immunology & Microbiology, Psychology)

| journal | records | analytic_records | best_q | medical_best | categories |
|---|---|---|---|---|---|
| Scientific Reports | 6263 | 343 | Q1 | none | Multidisciplinary (Q1) |
| PLOS ONE | 1926 | 139 | Q1 | none | Multidisciplinary (Q1) |
| Diagnostics | 765 | 87 | Q2 | none | Clinical Biochemistry (Q2) |
| Nature Communications | 550 | 33 | Q1 | none | Biochemistry, Genetics and Molecular Biology (miscellaneous) (Q1); Chemistry (miscellaneous) (Q1); Multidiscip |
| IEEE Transactions on Medical Imaging | 528 | 3 | Q1 | none | Computer Science Applications (Q1); Electrical and Electronic Engineering (Q1); Radiological and Ultrasound Te |
| Bioengineering | 487 | 62 | Q2 | none | Bioengineering (Q2) |
| Briefings in Bioinformatics | 425 | 18 | Q1 | none | Information Systems (Q1); Molecular Biology (Q1) |
| Medical and Biological Engineering and Computing | 380 | 5 | Q2 | none | Biomedical Engineering (Q2); Computer Science Applications (Q2) |
| Heliyon | 275 | 18 | Q1 | none | Multidisciplinary (Q1) |
| IEEE Transactions on Biomedical Engineering | 268 | 3 | Q1 | none | Biomedical Engineering (Q1) |
| Frontiers in Artificial Intelligence | 246 | 77 | Q1/Q2 | none | Artificial Intelligence (Q1) |
| Computational and Mathematical Methods in Medicine (discontinued) | 240 | 2 | Q2 | Q3 | Applied Mathematics (Q2); Biochemistry, Genetics and Molecular Biology (miscellaneous) (Q2); Modeling and Simu |
| Scientific Data | 223 | 7 | Q1 | none | Computer Science Applications (Q1); Education (Q1); Information Systems (Q1); Library and Information Sciences |
| BMC Bioinformatics | 220 | 2 | Q1 | none | Applied Mathematics (Q1); Biochemistry (Q1); Computer Science Applications (Q1); Molecular Biology (Q2); Struc |
| PeerJ Computer Science | 183 | 7 | Q1/Q2 | none | Computer Science (miscellaneous) (Q2) |
| Analytical Chemistry | 171 | 1 | Q1 | none | Analytical Chemistry (Q1) |
| Mathematical Biosciences and Engineering | 166 | 2 | Q2 | Q3 | Agricultural and Biological Sciences (miscellaneous) (Q2); Applied Mathematics (Q2); Computational Mathematics |
| Bioinformatics | 166 | 2 | Q1 | none | Biochemistry (Q1); Computational Mathematics (Q1); Computational Theory and Mathematics (Q1); Computer Science |
| IEEE/ACM Transactions on Computational Biology and Bioinformatics | 160 | 0 | Q2 | none | Applied Mathematics (Q2); Biotechnology (Q2); Genetics (Q2) |
| JMIR Medical Education | 156 | 121 | Q1 | none | Education (Q1) |

## 5. Side finding: Q4 journals are counted as 'unmatched'

`sjr_filter.py` routes any quartile other than Q1/Q2/Q3 (including **Q4** and `-`) to the unmatched file (`filter_file`, `else:` branch, lines 207–210). Methods calls the 7,922 'unmatched'. Re-looking up the 7,922 with the same rules:

| SJR status | count |
|---|---|
| title not in SJR file | 5092 |
| listed, no quartile ('-') | 1494 |
| Q4 | 1336 |

