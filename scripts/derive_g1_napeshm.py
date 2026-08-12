#!/usr/bin/env python3
"""Derive the between-plot spatial variance baseline (gap G1) from NAPESHM.

Standalone and reproducible. Not part of the package build and not imported by
``loam`` - it produces a number that is then hand-curated into
``data/variance_components.yaml`` with its assumptions, like any other row.

WHAT IS BEING DERIVED
---------------------
Within-treatment, within-site replicate variance in soil organic carbon.
Replicate experimental units under identical management at one site differ only
by spatial heterogeneity plus analytical error, so that variance IS between-plot
spatial variance for our purposes.

DATA
----
Soil Health Institute (2024). North American Project to Evaluate Soil Health
Measurements [data set]. doi:10.15482/USDA.ADC/25632270
Design documented in Norris et al. (2020), Agronomy Journal.

Expected at ``data/raw/napeshm/`` (gitignored). Download:
    curl -sSL -o napeshm.zip https://ndownloader.figshare.com/files/46794877
    # md5 b6a0a7cd8123c556c82a0d3384084a83
    unzip napeshm.zip && mv "CSV Files"/*.csv data/raw/napeshm/

FILTER DECISIONS - each has a D-NNN entry in DECISIONS.md
---------------------------------------------------------
D-024  Experimental design is heterogeneous across the 94 sites. Only
       'Randomized complete block' and 'Completely randomized' give replicates
       that are true randomized replicates. The 40 sites with design '0'
       (unknown) are EXCLUDED from the headline.
D-025  EU type is heterogeneous. Spatial variance scales with the separation
       between replicates, so 'Plots' only for the headline; other eu_types are
       reported stratified, never pooled in.
D-026  Depth is not in the dataset. Fixed by protocol at 0-15 cm and documented
       only in Norris et al. (2020). This row is scoped to 0-15 cm and is NOT
       converted to our 0-30 cm project scope.
D-027  Analytical error is not separable - no lab duplicate or QC columns exist.
       The estimate is spatial + analytical COMBINED, i.e. an UPPER BOUND on
       between-plot spatial variance.
D-028  DECIDED 2026-08-09. Scope is the IPCC 2006 default climate regions
       (Vol 4 Ch 3 Figure 3A.5.2 p. 3.39), classified per site by
       scripts/derive_ipcc_regions.py. Only the TEMPERATURE regime is used,
       because only it is determinable: sites classified Tropical are out of
       scope, and every other NAPESHM site is Temperate/Boreal since the
       Boreal/Polar subtree is unreachable (coldest site 4 C). The moisture
       regime is undetermined and is never invented. Replaces a private
       MAT<=15 AND |lat|>=30 envelope that had no answer to "why that
       threshold".
D-033  Why the classification is PARTIAL. Frost days are recovered from Daymet
       (the source NAPESHM's own dictionary cites), validated 60/60 against its
       published temperature integers. MAP:PET is NOT recoverable - neither
       `mi` (Thornthwaite 1948) nor `hargreave_cmd` (a one-sided monthly
       deficit) reproduces it, and NAPESHM documents no Hargreaves formulation
       or averaging window. Every non-tropical leaf of the figure is
       moisture-qualified, so 87 of 94 sites end `unclassified` - explicitly,
       never imputed. See D-039 for why that is a finding about the dataset.

ESTIMATOR
---------
Nested random effects, treatment nested within site, fitted by REML:

    y_ijk = mu + site_i + treatment_j(i) + e_ijk

``e_ijk`` - the residual - is the within-treatment (between-replicate-EU)
variance we want. Per-treatment variances are NOT averaged: with 2-4 replicates
each, individual treatment variances are wildly unstable, and averaging them
weights a 2-replicate treatment equally with a 6-replicate one.

Fitted on the LOG scale because within-treatment SD scales with treatment mean
(log-log slope ~1.2, well away from the 0 that a constant-SD model assumes), so
the natural parameterisation is a constant CV rather than a constant SD. On the
log scale, CV = 100 * sqrt(exp(sigma^2) - 1).

Confidence intervals by cluster bootstrap over SITES, which is the top-level
independent sampling unit. Resampling rows or treatments would ignore the
nesting and give intervals that are far too narrow.

USAGE
-----
    python scripts/derive_g1_napeshm.py
    python scripts/derive_g1_napeshm.py --bootstrap 2000 --out /tmp/g1.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd

# The filter constants live in the package, not here, so that the build and the
# test suite can see what governs them without importing pandas. See
# loam/decisions.py: each one is tied to the D-NNN that settles it, and
# IPCC_OUT_OF_SCOPE_REGIONS carries the D-028 scope decision.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from loam.decisions import (  # noqa: E402
    CONSTANTS_BY_NAME,
    DEPTH_BOTTOM_CM,
    DEPTH_TOP_CM,
    HEADLINE_DESIGNS,
    HEADLINE_EU_TYPE,
    IPCC_OUT_OF_SCOPE_REGIONS,
    IPCC_SCOPE_LABEL,
    IPCC_SITE_REGIONS_FILE,
    PROPOSED_FLAG,
)

warnings.filterwarnings("ignore")

DATA = "data/raw/napeshm/"


# ---------------------------------------------------------------------------
# load + filter
# ---------------------------------------------------------------------------


def load() -> pd.DataFrame:
    need = ["soildata.csv", "sites.csv", "treatments.csv"]
    missing = [f for f in need if not os.path.exists(DATA + f)]
    if missing:
        sys.exit(
            f"missing {missing} in {DATA}\n"
            "data/raw/ is gitignored - see this script's docstring for the "
            "download command."
        )
    if not os.path.exists(IPCC_SITE_REGIONS_FILE):
        sys.exit(
            f"missing {IPCC_SITE_REGIONS_FILE}\n"
            "D-028 scopes this derivation by IPCC climate region. Run:\n"
            "    python scripts/derive_ipcc_regions.py"
        )
    soil = pd.read_csv(DATA + "soildata.csv", low_memory=False)
    sites = pd.read_csv(DATA + "sites.csv", low_memory=False)
    # `sitecode` is deliberately NOT taken from sites.csv: soildata.csv already
    # carries it, and merging both would suffix them into sitecode_x/_y.
    site_cols = [
        "siteid", "exper_design", "eu_type", "site_mean_temp",
        "site_precip", "country", "state_prov", "site_latitude",
    ]
    df = soil.merge(sites[site_cols], on="siteid", how="left")

    # D-028: attach the per-site IPCC classification. `unclassified` is carried
    # through as a value, never dropped and never filled - for this dataset it
    # still pins the temperature regime (see IPCC_SCOPE_LABEL).
    with open(IPCC_SITE_REGIONS_FILE, encoding="utf-8") as fh:
        regions = {r["sitecode"]: r["region"] for r in json.load(fh)["sites"]}
    df["ipcc_region"] = df.sitecode.map(regions)
    return df


def _with_replicates(d: pd.DataFrame, min_reps: int = 2) -> pd.DataFrame:
    counts = d.groupby("treatmentid").size()
    return d[d.treatmentid.isin(counts[counts >= min_reps].index)]


def filter_cascade(df: pd.DataFrame, in_scope: bool = True) -> tuple[pd.DataFrame, list]:
    """Apply filters in order, recording survivors at each stage.

    ``in_scope=False`` keeps every site regardless of IPCC region, as a contrast.
    """
    rows = []

    def note(label, d):
        rows.append(
            {
                "stage": label,
                "eus": len(d),
                "sites": int(d.siteid.nunique()),
                "treatments": int(d.treatmentid.nunique()),
            }
        )

    note("0. all EUs in soildata.csv", df)
    d = df[df.b_soc.notna()]
    note("1. b_soc non-null", d)
    d = d[d.exper_design.isin(HEADLINE_DESIGNS)]
    note("2. D-024 design is RCB or CR", d)
    d = d[d.eu_type == HEADLINE_EU_TYPE]
    note(f"3. D-025 eu_type == {HEADLINE_EU_TYPE!r}", d)
    if in_scope:
        d = d[~d.ipcc_region.isin(IPCC_OUT_OF_SCOPE_REGIONS)]
    note("4. D-028 IPCC temperature regime (not Tropical)", d)
    d = _with_replicates(d)
    note("5. treatments with >=2 replicates", d)
    return d.copy(), rows


# ---------------------------------------------------------------------------
# estimator
# ---------------------------------------------------------------------------


def add_targets(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    # (a) SOC concentration, %. Direct, no extra assumptions.
    d["log_soc"] = np.log(d.b_soc)
    # (b) SOC stock, Mg/ha over the protocol depth. Requires bd_2mm, whose own
    #     measurement error is thereby propagated into the variance (D-027).
    #     stock = (b_soc/100) * bd * depth_cm * 100 == b_soc * bd * depth_cm
    d["stock"] = d.b_soc * d.bd_2mm * (DEPTH_BOTTOM_CM - DEPTH_TOP_CM)
    d["log_stock"] = np.log(d.stock.where(d.stock > 0))
    return d


def residual_var(d: pd.DataFrame, col: str) -> float | None:
    """REML residual variance from treatment-nested-within-site random effects."""
    import statsmodels.formula.api as smf

    sub = d[d[col].notna()]
    sub = _with_replicates(sub)
    if sub.treatmentid.nunique() < 5 or sub.siteid.nunique() < 3:
        return None
    try:
        res = smf.mixedlm(
            f"{col} ~ 1",
            data=sub,
            groups=sub["siteid"],
            re_formula="1",
            vc_formula={"trt": "0 + C(treatmentid)"},
        ).fit(reml=True, method="lbfgs")
    except Exception:
        return None
    return float(res.scale) if res.converged else None


def cv_from_logvar(v: float | None) -> float | None:
    """Log-scale residual variance -> coefficient of variation, percent."""
    return None if v is None else float(100.0 * np.sqrt(np.expm1(v)))


def bootstrap_cv(d: pd.DataFrame, col: str, n: int, seed: int = 20260808):
    """Cluster bootstrap over sites. Sites are the independent unit."""
    rng = np.random.default_rng(seed)
    sites = d.siteid.unique()
    out = []
    for _ in range(n):
        pick = rng.choice(sites, size=len(sites), replace=True)
        parts = []
        for k, s in enumerate(pick):
            chunk = d[d.siteid == s].copy()
            # relabel so a site drawn twice acts as two independent groups
            chunk["siteid"] = f"{s}__b{k}"
            chunk["treatmentid"] = chunk["treatmentid"].astype(str) + f"__b{k}"
            parts.append(chunk)
        cv = cv_from_logvar(residual_var(pd.concat(parts, ignore_index=True), col))
        if cv is not None and np.isfinite(cv):
            out.append(cv)
    if len(out) < max(20, n // 10):
        return None
    a = np.array(out)
    return {
        "ci95_low": round(float(np.percentile(a, 2.5)), 3),
        "ci95_high": round(float(np.percentile(a, 97.5)), 3),
        "bootstrap_median": round(float(np.median(a)), 3),
        "n_successful": len(a),
    }


def estimate(d: pd.DataFrame, col: str, n_boot: int) -> dict:
    v = residual_var(d, col)
    cv = cv_from_logvar(v)
    sub = _with_replicates(d[d[col].notna()])
    out = {
        "n_eus": len(sub),
        "n_treatments": int(sub.treatmentid.nunique()),
        "n_sites": int(sub.siteid.nunique()),
        "residual_log_variance": None if v is None else round(v, 6),
        "cv_pct": None if cv is None else round(cv, 3),
    }
    if cv is not None and n_boot:
        out["ci"] = bootstrap_cv(d, col, n_boot)
    return out


# ---------------------------------------------------------------------------


def texture_strata(d: pd.DataFrame, col: str, n_boot: int) -> dict:
    """CV by clay tercile.

    Was the seed of the Phase 3 spatially explicit MDC surface. That deliverable
    is RETIRED (2026-08-12, docs/invariance_finding.md) because this scan and
    three others returned nulls against stated detection limits. Kept as a
    diagnostic - it is the evidence for the retirement, not a step toward the
    thing retired.
    """
    if "b_clay" not in d.columns or d.b_clay.notna().sum() < 30:
        return {"note": "b_clay unavailable"}
    sub = d[d.b_clay.notna()].copy()
    qs = sub.b_clay.quantile([1 / 3, 2 / 3]).values
    sub["stratum"] = np.where(
        sub.b_clay <= qs[0], "low_clay",
        np.where(sub.b_clay <= qs[1], "mid_clay", "high_clay"),
    )
    out = {"tercile_breaks_pct_clay": [round(float(q), 2) for q in qs]}
    for name, part in sub.groupby("stratum"):
        part = _with_replicates(part)
        est = estimate(part, col, n_boot)
        est["clay_range_pct"] = [
            round(float(part.b_clay.min()), 1), round(float(part.b_clay.max()), 1)
        ]
        est["mean_soc_pct"] = round(float(part.b_soc.mean()), 3)
        out[name] = est
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--out", default="data/processed/g1_napeshm.json")
    args = ap.parse_args()

    df = load()
    result = {
        "dataset": "NAPESHM, Soil Health Institute (2024), doi:10.15482/USDA.ADC/25632270",
        "depth_cm": [DEPTH_TOP_CM, DEPTH_BOTTOM_CM],
        "depth_source": "Norris et al. 2020 Agronomy Journal - NOT in the dataset (D-026)",
        "estimator": "REML nested random effects, treatment within site, log scale; "
                     "cluster bootstrap over sites",
        "caveat": "spatial + analytical COMBINED - an UPPER BOUND on between-plot "
                  "spatial variance (D-027)",
    }

    for const in CONSTANTS_BY_NAME.values():
        if const.is_proposed:
            print(f"{const.name} ({const.governed_by}){PROPOSED_FLAG}")

    # headline cascade under the DECIDED IPCC scope (D-028)
    dh, cascade = filter_cascade(df, in_scope=True)
    dh = add_targets(dh)
    result["ipcc_scope"] = IPCC_SCOPE_LABEL
    result["filter_cascade"] = cascade

    print(f"{'stage':<40}{'EUs':>6}{'sites':>7}{'trts':>6}")
    for r in cascade:
        print(f"{r['stage']:<40}{r['eus']:>6}{r['sites']:>7}{r['treatments']:>6}")

    if len(dh) < 60 or dh.treatmentid.nunique() < 20:
        print(
            f"\nSTOP: only {len(dh)} EUs / {dh.treatmentid.nunique()} treatments "
            "survive. Too few to support a stable variance component.",
            file=sys.stderr,
        )
        return 4

    # climate scope: the decided scope, and the no-scope contrast (D-028)
    print("\n--- climate scope (D-028 DECIDED: IPCC temperature regime) ---")
    result["climate_scope"] = {}
    for name, scoped in (("ipcc_temperate_boreal", True), ("all_sites_no_scope", False)):
        d, _ = filter_cascade(df, in_scope=scoped)
        d = add_targets(d)
        if len(d) < 40:
            continue
        block = {"scope": IPCC_SCOPE_LABEL if scoped else "no climate scope"}
        for label, col in (("concentration", "log_soc"), ("stock", "log_stock")):
            block[label] = estimate(d, col, args.bootstrap if scoped else 0)
        block["countries"] = d.country.value_counts().to_dict()
        block["mat_range"] = [float(d.site_mean_temp.min()), float(d.site_mean_temp.max())]
        block["ipcc_regions"] = d.ipcc_region.value_counts().to_dict()
        result["climate_scope"][name] = block
        c, s = block["concentration"], block["stock"]
        print(f"  {name:<24} n={c['n_eus']:>3} EU / {c['n_sites']:>2} sites  "
              f"conc CV={c['cv_pct']}%  stock CV={s['cv_pct']}%  {block['countries']}")

    # What the scope actually excluded, named rather than merely counted.
    excluded = df[df.b_soc.notna() & df.ipcc_region.isin(IPCC_OUT_OF_SCOPE_REGIONS)]
    result["excluded_by_ipcc_scope"] = {
        "n_eus": int(len(excluded)),
        "n_sites": int(excluded.siteid.nunique()),
        "sites": sorted(excluded.sitecode.dropna().unique().tolist()),
        "regions": excluded.ipcc_region.value_counts().to_dict(),
    }
    print(f"\n  excluded as Tropical: {len(excluded)} EUs / "
          f"{excluded.siteid.nunique()} sites {result['excluded_by_ipcc_scope']['regions']}")

    # design / eu_type sensitivity (D-024, D-025)
    print("\n--- design & eu_type sensitivity (D-024, D-025) ---")
    result["design_sensitivity"] = {}
    base = df[df.b_soc.notna()]
    variants = {
        "headline_rcb_cr_plots": base[
            base.exper_design.isin(HEADLINE_DESIGNS) & (base.eu_type == "Plots")],
        "all_designs_plots": base[base.eu_type == "Plots"],
        "rcb_cr_all_eu_types": base[base.exper_design.isin(HEADLINE_DESIGNS)],
        "all_designs_all_eu_types": base,
    }
    for name, v in variants.items():
        v = add_targets(_with_replicates(v))
        est = estimate(v, "log_soc", 0)
        result["design_sensitivity"][name] = est
        print(f"  {name:<28} n={est['n_eus']:>4} EU / {est['n_sites']:>2} sites  "
              f"conc CV={est['cv_pct']}%")

    # texture stratification
    print("\n--- texture stratification (evidence for the D-040 invariance finding) ---")
    result["texture_strata_concentration"] = texture_strata(dh, "log_soc", 0)
    result["texture_strata_stock"] = texture_strata(dh, "log_stock", 0)
    for k, v in result["texture_strata_concentration"].items():
        if isinstance(v, dict) and "cv_pct" in v:
            print(f"  {k:<12} clay {v['clay_range_pct']}%  n={v['n_eus']:>3} EU  "
                  f"CV={v['cv_pct']}%  (mean SOC {v['mean_soc_pct']}%)")

    head = result["climate_scope"]["ipcc_temperate_boreal"]
    print(f"\n=== HEADLINE (D-028 decided: {IPCC_SCOPE_LABEL}) ===")
    for label in ("concentration", "stock"):
        e = head[label]
        ci = e.get("ci")
        band = f"  95% CI [{ci['ci95_low']}, {ci['ci95_high']}]" if ci else ""
        print(f"  {label:<14} CV = {e['cv_pct']}%{band}   "
              f"(n={e['n_eus']} EU, {e['n_treatments']} trt, {e['n_sites']} sites)")

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
