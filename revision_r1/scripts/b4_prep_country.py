"""B4 helper (run with the project venv, which has geopandas): resolve the
first-author country with the Table S7 resolver for every analytic record
(2021–2026) and save pmid → country for b4_regression.py."""
import sys
from r1_common import OUT, REPO, load_v1
sys.path.insert(0, str(REPO))
from analysis.run_country_critical_map import resolve_country  # noqa: E402

v = load_v1(year_range=(2021, 2026))
v.assign(country=v["first_affiliation"].map(resolve_country))[["pmid", "country"]].to_csv(
    OUT / "B4" / "b4_country_resolved.csv", index=False)
print(len(v), v["first_affiliation"].map(resolve_country).notna().sum())
