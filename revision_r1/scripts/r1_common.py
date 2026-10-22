"""Shared helpers for the JMIR R1 Batch 1 analyses (revision_r1/).

Read-only with respect to the canonical pipeline: nothing here writes outside
revision_r1/. Large gitignored inputs (classified_medical_Q1Q2.csv, the
pre-prefilter corpus, the pilot files) are read from the main checkout's
output/ directory; committed inputs are read from this repository.

Statistics conventions (unchanged from the original analysis):
  * 95% percentile bootstrap, 1000 resamples, seed 42, row-level resampling
    with replacement (np.random.default_rng(42).integers(0, n, n) per draw),
    identical to analysis/robustness.py::bootstrap_ci.
"""

from __future__ import annotations

import itertools
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
R1 = REPO / "revision_r1"
OUT = R1 / "outputs"
FIG = R1 / "figures"
INPUTS = R1 / "inputs"

# Gitignored data live in the main checkout (byte-identical to the last
# committed versions at 31ed027^; see REPORT_batch1.md).
DATA_ROOT = Path(os.environ.get(
    "R1_DATA_ROOT", "/Users/kingslywang/Documents/科研/ai-narratives-2026/output"))
REPO_OUT = REPO / "output"

STANCES = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]
CRITICAL = {"Alarm", "Caution"}
FAVOURABLE = {"Cautious Optimism", "Advocacy"}
SEED = 42
N_BOOT = 1000
YEARS_PRIMARY = [2021, 2022, 2023, 2024, 2025]
YEARS_ALL = [2021, 2022, 2023, 2024, 2025, 2026]

THEMES = ["safety_clinical", "hallucination", "regulation", "ethics_bias",
          "education", "data_privacy", "cognitive", "existential",
          "replacement", "other"]
THEME_LABELS = {
    "safety_clinical": "Patient safety", "hallucination": "Hallucination / errors",
    "regulation": "Governance / regulation", "ethics_bias": "Ethics & bias",
    "education": "Medical education", "data_privacy": "Data privacy",
    "cognitive": "Cognitive offloading", "existential": "Existential threat",
    "replacement": "Replacement fears", "other": "Other",
}

for d in (OUT, FIG):
    d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# loaders
# ---------------------------------------------------------------------------
def read_str(path, **kw) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False, **kw)


def load_v1(year_range=(2021, 2026), drop_failed=True) -> pd.DataFrame:
    """classified_medical_Q1Q2.csv exactly as analysis/robustness.py loads it
    (same row order, FAILED dropped, pub_year filtered)."""
    df = pd.read_csv(DATA_ROOT / "classified_medical_Q1Q2.csv", low_memory=False,
                     dtype={"pmid": str})
    if drop_failed:
        df = df[df["stance"] != "FAILED"].copy()
    df["pub_year"] = pd.to_numeric(df["pub_year"], errors="coerce").astype("Int64")
    if year_range is not None:
        lo, hi = year_range
        df = df[(df["pub_year"] >= lo) & (df["pub_year"] <= hi)].copy()
    df["abstract"] = df["abstract"].fillna("")
    df["has_abstract"] = df["abstract"].astype(str).str.strip().str.len() > 0
    df["critical"] = df["stance"].isin(CRITICAL)
    df["favourable"] = df["stance"].isin(FAVOURABLE)
    return df


# ---------------------------------------------------------------------------
# bootstrap
# ---------------------------------------------------------------------------
def boot_indices(n, n_boot=N_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    for _ in range(n_boot):
        yield rng.integers(0, n, size=n)


def boot_group_share(groups, success, levels, n_boot=N_BOOT, seed=SEED):
    """Joint row-level bootstrap of per-group shares (as robustness.bootstrap_ci
    applied to a crosstab normalised by row). Groups absent in a resample get
    share 0 (robustness.py fills NaN with 0.0).
    Returns DataFrame: level, k, n, point, lo, hi (percent)."""
    groups = np.asarray(groups)
    success = np.asarray(success, dtype=float)
    codes = np.array([levels.index(g) if g in levels else -1 for g in groups])
    keep = codes >= 0
    L = len(levels)

    def share(idx):
        c = codes[idx]
        s = success[idx]
        m = c >= 0
        num = np.bincount(c[m], weights=s[m], minlength=L)
        den = np.bincount(c[m], minlength=L)
        with np.errstate(invalid="ignore", divide="ignore"):
            out = np.where(den > 0, num / den * 100, 0.0)
        return out

    full = np.arange(len(groups))
    point = share(full)
    draws = np.array([share(i) for i in boot_indices(len(groups), n_boot, seed)])
    lo, hi = np.percentile(draws, [2.5, 97.5], axis=0)
    k = np.bincount(codes[keep], weights=success[keep], minlength=L).astype(int)
    n = np.bincount(codes[keep], minlength=L)
    return pd.DataFrame({"level": levels, "k": k, "n": n, "point": point,
                         "lo": lo, "hi": hi})


def boot_scalar(fn, n, n_boot=N_BOOT, seed=SEED):
    """Percentile CI for a statistic fn(idx) of a row-indexed sample."""
    vals = []
    for idx in boot_indices(n, n_boot, seed):
        v = fn(idx)
        if v is not None and not (isinstance(v, float) and math.isnan(v)):
            vals.append(v)
    if not vals:
        return float("nan"), float("nan")
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return float(lo), float(hi)


# ---------------------------------------------------------------------------
# agreement statistics
# ---------------------------------------------------------------------------
def confusion(h, m, labels):
    h = list(h); m = list(m)
    cm = np.zeros((len(labels), len(labels)), dtype=int)
    for a, b in zip(h, m):
        cm[labels.index(a), labels.index(b)] += 1
    return cm


def cohen_kappa_cm(cm, weights=None):
    cm = np.asarray(cm, dtype=float)
    n = cm.sum()
    if n == 0:
        return float("nan")
    k = cm.shape[0]
    if weights is None:
        w = 1 - np.eye(k)
    else:
        i, j = np.indices((k, k))
        w = np.abs(i - j) / (k - 1) if weights == "linear" else ((i - j) / (k - 1)) ** 2
    row = cm.sum(1); col = cm.sum(0)
    exp = np.outer(row, col) / n
    den = (w * exp).sum()
    if den == 0:
        return float("nan")
    return 1 - (w * cm).sum() / den


def gwet_ac1_cm(cm):
    cm = np.asarray(cm, dtype=float)
    n = cm.sum(); q = cm.shape[0]
    pa = np.trace(cm) / n
    pi = (cm.sum(0) + cm.sum(1)) / (2 * n)
    pe = (pi * (1 - pi)).sum() / (q - 1)
    return (pa - pe) / (1 - pe) if pe != 1 else float("nan")


def pabak_cm(cm):
    cm = np.asarray(cm, dtype=float)
    q = cm.shape[0]; pa = np.trace(cm) / cm.sum()
    return (q * pa - 1) / (q - 1)


def kappa_max_cm(cm):
    cm = np.asarray(cm, dtype=float)
    n = cm.sum(); row = cm.sum(1) / n; col = cm.sum(0) / n
    pe = (row * col).sum(); pmax = np.minimum(row, col).sum()
    return (pmax - pe) / (1 - pe)


def binary_metrics_cm(tp, fn, fp, tn):
    """Metrics for a 2x2 with positive class P. Rows human, cols model."""
    n = tp + fn + fp + tn
    sens = tp / (tp + fn) if tp + fn else float("nan")
    spec = tn / (tn + fp) if tn + fp else float("nan")
    ppv = tp / (tp + fp) if tp + fp else float("nan")
    npv = tn / (tn + fn) if tn + fn else float("nan")
    f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else float("nan")
    acc = (tp + tn) / n
    cm = np.array([[tp, fn], [fp, tn]])
    return {"sensitivity": sens, "specificity": spec, "PPV": ppv, "NPV": npv,
            "F1": f1, "accuracy": acc, "kappa": cohen_kappa_cm(cm),
            "AC1": gwet_ac1_cm(cm), "PABAK": pabak_cm(cm),
            "prevalence_human": (tp + fn) / n}


def per_class_prf(cm, labels):
    cm = np.asarray(cm, dtype=float)
    out = {}
    for i, lab in enumerate(labels):
        tp = cm[i, i]; fn = cm[i].sum() - tp; fp = cm[:, i].sum() - tp
        p = tp / (tp + fp) if tp + fp else float("nan")
        r = tp / (tp + fn) if tp + fn else float("nan")
        f = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else float("nan")
        out[lab] = {"precision": p, "recall": r, "F1": f, "support": int(cm[i].sum())}
    return out


# ---------------------------------------------------------------------------
# trend statistics
# ---------------------------------------------------------------------------
def spearman_exact(x, y):
    """Spearman rho with exact two-sided permutation P (all n! orderings).
    Also returns scipy's asymptotic (t-approximation) P for comparison."""
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    rho = stats.spearmanr(x, y).statistic
    p_asym = stats.spearmanr(x, y).pvalue
    n = len(x)
    rx = stats.rankdata(x)
    ry = stats.rankdata(y)
    count = 0; total = 0
    for perm in itertools.permutations(range(n)):
        r = stats.pearsonr(rx, ry[list(perm)]).statistic if np.std(ry) > 0 else 0.0
        total += 1
        if abs(r) >= abs(rho) - 1e-12:
            count += 1
    return float(rho), count / total, float(p_asym)


def logit_irls(X, y, max_iter=100, tol=1e-10):
    """Unpenalised logistic regression by IRLS. X includes intercept column.
    Returns beta, Wald SE, log-likelihood."""
    X = np.asarray(X, dtype=float); y = np.asarray(y, dtype=float)
    beta = np.zeros(X.shape[1])
    for _ in range(max_iter):
        eta = X @ beta
        p = 1 / (1 + np.exp(-eta))
        W = p * (1 - p)
        H = X.T @ (X * W[:, None])
        g = X.T @ (y - p)
        step = np.linalg.solve(H, g)
        beta = beta + step
        if np.max(np.abs(step)) < tol:
            break
    eta = X @ beta
    p = 1 / (1 + np.exp(-eta))
    W = p * (1 - p)
    cov = np.linalg.inv(X.T @ (X * W[:, None]))
    ll = float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return beta, np.sqrt(np.diag(cov)), ll


def logit_trend(year, outcome, centre=None):
    """outcome ~ year (continuous, centred). Returns OR per year, Wald 95% CI,
    Wald P, and likelihood-ratio P."""
    year = np.asarray(year, dtype=float); y = np.asarray(outcome, dtype=float)
    c = np.mean(year) if centre is None else centre
    X = np.column_stack([np.ones_like(year), year - c])
    beta, se, ll = logit_irls(X, y)
    p0 = y.mean()
    ll0 = float(np.sum(y * np.log(p0) + (1 - y) * np.log(1 - p0)))
    z = beta[1] / se[1]
    return {"centre": c, "n": int(len(y)), "events": int(y.sum()),
            "OR": float(np.exp(beta[1])),
            "OR_lo": float(np.exp(beta[1] - 1.959963984540054 * se[1])),
            "OR_hi": float(np.exp(beta[1] + 1.959963984540054 * se[1])),
            "P_wald": float(2 * stats.norm.sf(abs(z))),
            "P_LR": float(stats.chi2.sf(2 * (ll - ll0), 1))}


# ---------------------------------------------------------------------------
# formatting
# ---------------------------------------------------------------------------
def fmt_p(p):
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return "NA"
    if p < 0.001:
        return "<.001"
    s = f"{p:.3f}"
    return s[1:] if s.startswith("0") else s


def pct_ci(point, lo, hi, k=None, n=None, d=1):
    s = f"{point:.{d}f}% ({lo:.{d}f}–{hi:.{d}f})"
    if k is not None and n is not None:
        s = f"{s}; {int(k):,}/{int(n):,}"
    return s


def md_table(df: pd.DataFrame, floatfmt="{:.3f}") -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating)):
                cells.append("" if math.isnan(v) else floatfmt.format(v))
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)
