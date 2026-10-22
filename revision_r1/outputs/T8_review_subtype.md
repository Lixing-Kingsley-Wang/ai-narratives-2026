# T8 · Review-subtype provenance (X5)

Script: `revision_r1/scripts/t8_review_subtype.py`.

## 1. The rule (verbatim)

File `analysis/robustness.py` (imported by the publication-type analyses, e.g. `analysis/run_pubtype_stance.py`, `analysis/run_reviews_positivity_why.py`); functions `simplify_pubtype_7` (lines 49–68) and `simplify_pubtype_5` (lines 71–85). The repo-root copy `robustness.py` cited in Supplementary Note 1 is byte-identical.

```python
  49  def simplify_pubtype_7(pt: str) -> str:
  50      """Bucket the compound PubMed pub_type string into 7 categories.
  51  
  52      Precedence matches analyse_industry.simplify_pubtype: Editorial > Letter
  53      > Systematic Review > Review > Comment > News > Research Article.
  54      """
  55      pt = pt or ""
  56      if "Editorial" in pt:
  57          return "Editorial"
  58      if "Letter" in pt:
  59          return "Letter"
  60      if "Systematic Review" in pt:
  61          return "Systematic Review"
  62      if "Review" in pt:
  63          return "Review"
  64      if "Comment" in pt:
  65          return "Comment"
  66      if "News" in pt:
  67          return "News"
  68      return "Research Article"
  69  
  70  
  71  def simplify_pubtype_5(pt: str) -> str:
  72      """Collapse the 7-bucket scheme into the 5 categories from the brief.
  73  
  74      Systematic Review folds into Review; Comment folds into Commentary;
  75      News folds into Research Article (rare).
  76      """
  77      seven = simplify_pubtype_7(pt)
  78      if seven == "Systematic Review":
  79          return "Review"
  80      if seven == "Comment":
  81          return "Commentary"
  82      if seven == "News":
  83          return "Research Article"
  84      return seven
  85  
```

So the subtype is decided **only by PubMed Publication Type strings** (case-sensitive substring test on the semicolon-joined `pub_type` field from `PublicationType` in the PubMed XML). No title/abstract text, no LLM, and no MeSH heading is used. 'Systematic Review' = the record carries the PubMed type `Systematic Review` (and no Editorial or Letter type, which take precedence). 'Review (narrative)' = carries `Review` but not `Systematic Review` (and no Editorial/Letter). The label 'narrative' is therefore a residual category: any PubMed `Review` that is not tagged `Systematic Review` (including every record tagged `Scoping Review` without `Systematic Review`; see sections 2–3). 

## 2. PubMed tags in each subtype

| subtype | PubMed tag | records carrying tag | of subtype N |
|---|---|---|---|
| Systematic Review | Journal Article | 980 | 980 |
| Systematic Review | Systematic Review | 980 | 980 |
| Systematic Review | Meta-Analysis | 262 | 980 |
| Systematic Review | Research Support, Non-U.S. Gov't | 130 | 980 |
| Systematic Review | Review | 61 | 980 |
| Systematic Review | Research Support, N.I.H., Extramural | 23 | 980 |
| Systematic Review | Comparative Study | 23 | 980 |
| Systematic Review | Research Support, U.S. Gov't, Non-P.H.S. | 4 | 980 |
| Systematic Review | Network Meta-Analysis | 4 | 980 |
| Systematic Review | Scoping Review | 4 | 980 |
| Systematic Review | Research Support, U.S. Gov't, P.H.S. | 1 | 980 |
| Systematic Review | Retracted Publication | 1 | 980 |
| Review (narrative) | Journal Article | 4464 | 4464 |
| Review (narrative) | Review | 4122 | 4464 |
| Review (narrative) | Research Support, Non-U.S. Gov't | 414 | 4464 |
| Review (narrative) | Scoping Review | 374 | 4464 |
| Review (narrative) | Research Support, N.I.H., Extramural | 136 | 4464 |
| Review (narrative) | Research Support, U.S. Gov't, Non-P.H.S. | 25 | 4464 |
| Review (narrative) | Historical Article | 11 | 4464 |
| Review (narrative) | Meta-Analysis | 10 | 4464 |
| Review (narrative) | Consensus Statement | 9 | 4464 |
| Review (narrative) | Comparative Study | 8 | 4464 |
| Review (narrative) | Research Support, N.I.H., Intramural | 7 | 4464 |
| Review (narrative) | Retracted Publication | 7 | 4464 |

Full list: [T8_tags_by_subtype.csv](T8_tags_by_subtype.csv).

## 3. Meta-Analysis

There is no Meta-Analysis rule. A record tagged `Meta-Analysis` goes wherever its other tags send it: to Systematic Review if it also carries `Systematic Review`, to Review (narrative) if it carries `Review` only, and to Research Article if it carries neither (the substring 'Review' does not occur in 'Meta-Analysis').

Records tagged Meta-Analysis in the analytic set: 286. Assigned bucket (rows) × presence of the Systematic Review tag:

| pt7 | SR tag | no SR tag | All |
|---|---|---|---|
| Research Article | 0 | 14 | 14 |
| Review | 0 | 10 | 10 |
| Systematic Review | 262 | 0 | 262 |
| All | 262 | 24 | 286 |

- Records carrying a `Review` or `Systematic Review` tag but assigned to Editorial or Letter by precedence: 8 (Letter: 5, Editorial: 3).
- Records carrying `Systematic Review` but not assigned to Systematic Review: 0.
- Because the test is a substring test, 342 of the 4,464 'Review (narrative)' records carry no exact `Review` tag and were captured through another tag containing 'Review' (Scoping Review: 342).

## 4. Reproduction of Table S11

**Reproduced exactly** (n, critical, Alarm, Caution, Cautious Optimism, Advocacy to one decimal).

| Subtype | n | Critical % | Alarm % | Caution % | Cautious Optimism % | Advocacy % | Neutral % |
|---|---|---|---|---|---|---|---|
| Systematic Review | 980 | 29.3 | 3.0 | 26.3 | 68.2 | 0.3 | 2.2 |
| Review (narrative) | 4464 | 23.9 | 0.7 | 23.2 | 72.0 | 2.1 | 2.0 |

Both subtypes fold into the five-category 'Review' (n = 5,444 = 980 + 4,464).

