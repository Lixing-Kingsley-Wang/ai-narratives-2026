"""
TASK STAT-8 — FDA drop-structural-zeros sensitivity.

Recompute the Spearman correlation between specialty critical_rate and
FDA_cleared_device_count after dropping structural-zero specialties
(those with 0 mapped FDA devices). Report rho, two-sided p, and
n_specialties for the reduced set, and compare against the full-18 result.

Source of the per-specialty critical_rate and FDA device counts:
committed artifact output/analyses/specialty_aiadoption.csv, produced by
analysis/run_specialty_aiadoption.py (v1 canonical critical rate; FDA counts
from output/external/fda_aiml_devices.csv mapped by FDA review panel). This
task does NOT rerun classification.

Outputs:
  output/revision_checks/stat8_fda_drop_zero_sensitivity.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

WT = Path(__file__).resolve().parents[2]
OUT = WT / "output" / "revision_checks"
OUT.mkdir(parents=True, exist_ok=True)

# committed artifact lives in the parent checkout's tracked output/analyses/
SRC_CANDIDATES = [
    Path("/Users/kingslywang/repos/ai-narratives-2026/output/analyses/specialty_aiadoption.csv"),
    WT / "output" / "analyses" / "specialty_aiadoption.csv",
]


def resolve_src() -> Path:
    for p in SRC_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("specialty_aiadoption.csv not found in: "
                            + ", ".join(str(p) for p in SRC_CANDIDATES))


def main() -> None:
    src = resolve_src()
    df = pd.read_csv(src)
    print(f"Source: {src}")
    print(f"Specialties in file: {len(df)}")

    df = df[["specialty", "n_papers", "critical_rate_pct", "fda_device_count"]].copy()

    # ---- Full set ---------------------------------------------------------
    rho_full, p_full = spearmanr(df["critical_rate_pct"], df["fda_device_count"])
    n_full = len(df)

    # ---- Drop structural zeros (fda_device_count == 0) --------------------
    zeros = df[df["fda_device_count"] == 0]
    reduced = df[df["fda_device_count"] > 0].copy()
    rho_red, p_red = spearmanr(reduced["critical_rate_pct"], reduced["fda_device_count"])
    n_red = len(reduced)

    print("\nStructural-zero specialties dropped (fda_device_count == 0):")
    for s in zeros["specialty"]:
        print(f"  - {s}")

    print(f"\nFULL set:    n={n_full}  rho={rho_full:+.3f}  p(two-sided)={p_full:.4f}")
    print(f"REDUCED set: n={n_red}  rho={rho_red:+.3f}  p(two-sided)={p_red:.4f}")
    inverse_full = rho_full < 0
    inverse_red = rho_red < 0
    print(f"\nInverse (negative) gradient in FULL set:    {inverse_full}")
    print(f"Inverse (negative) gradient in REDUCED set: {inverse_red}")
    survives = inverse_full and inverse_red
    print(f"Inverse gradient SURVIVES removal of structural zeros: {survives}")

    res = pd.DataFrame([
        {"set": "full", "n_specialties": n_full, "spearman_rho": rho_full,
         "p_two_sided": p_full, "structural_zeros_dropped": 0,
         "inverse_gradient": inverse_full},
        {"set": "drop_structural_zeros", "n_specialties": n_red, "spearman_rho": rho_red,
         "p_two_sided": p_red, "structural_zeros_dropped": int(len(zeros)),
         "inverse_gradient": inverse_red},
    ])
    res.to_csv(OUT / "stat8_fda_drop_zero_sensitivity.csv", index=False)
    # record which specialties were dropped for auditability
    zeros[["specialty", "n_papers", "critical_rate_pct", "fda_device_count"]].to_csv(
        OUT / "stat8_structural_zero_specialties.csv", index=False)
    print(f"\nSaved: {OUT / 'stat8_fda_drop_zero_sensitivity.csv'}")
    print(f"Saved: {OUT / 'stat8_structural_zero_specialties.csv'}")


if __name__ == "__main__":
    main()
