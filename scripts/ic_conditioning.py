#!/usr/bin/env python3
"""Is inorganic carbon a conditioning covariate for between-plot variability?

EXPLORATORY. Writes NO variance-table rows, changes NO scope, moves NO constant.
Its output is a JSON blob and a printed report; whether anything is tabled is a
separate judgement (rule: report before writing rows).

WHY
---
D-040 found between-plot CV approximately invariant across every covariate a
spatially explicit MDC surface would be built from - climate region, clay, sand,
SOC level. That challenges Phase 3 Deliverable 3, which needs SOMETHING to vary.

Eric Potash (author of Potash et al. 2025, ERL 20 024025), in correspondence
2026-08-11, named a candidate the table has never tested:

    "those 4% and 2% error numbers are representative but can vary quite a lot
    depending on the soil. For example, soils with high inorganic carbon have
    higher variability in their organic carbon measurements. I wouldn't be
    surprised if the total variability can vary as low as 1% or as high as 10%."

NAPESHM measures inorganic carbon directly (``b_ic``, Chittick calcimeter, %)
and reports ``b_soc`` as ``b_total_c - b_ic`` (dry combustion minus calcimeter).
So the mechanism is present in the data by construction, and testable.

WHAT IS BEING MEASURED - STATED PRECISELY, BECAUSE THE TEMPTATION IS TO OVERCLAIM
--------------------------------------------------------------------------------
The response is the SAME quantity as ``VC-BPS-005``: within-treatment,
within-site residual CV among replicate experimental units. Per D-027 that
bundles

    between-plot spatial + within-plot spatial + analytical

and NAPESHM cannot separate them (one sample per EU). Potash's mechanism is
ANALYTICAL - determining organic carbon by difference is noisier when the
subtracted term is large. This script therefore CANNOT show a purely analytical
effect, and does not claim one. What it can show is whether the bundled
between-plot quantity rises with inorganic carbon, and - through the paired
contrast in section 4 - how much of any rise is attributable to the subtraction
itself rather than to whatever else differs about carbonate soils.

THE CONFOUND, NAMED IN ADVANCE
------------------------------
Inorganic carbon tracks aridity and carbonate parent material. An IC effect may
be a climate effect wearing a different hat. Three separate answers to that are
run: conditioning on aridity/temperature covariates (section 3), a within-site
contrast, and the paired SOC-vs-total-C test (section 4), which is immune to
every site-level confound because it compares two quantities measured on the
same soil samples.

ESTIMATORS
----------
1. STRATIFIED REML - identical to ``scripts/derive_g1_napeshm.py``: nested random
   effects, treatment within site, log scale, cluster bootstrap over sites. Same
   code path, imported not copied. This is what makes section 2 comparable to
   ``VC-BPS-005/006``.

2. LOG-VARIANCE REGRESSION - per-treatment sample variance of ``log(b_soc)``,
   debiased. For nu = n-1 degrees of freedom and Gaussian data,

       E[log s^2] = log sigma^2 + psi(nu/2) - log(nu/2)
       Var[log s^2] = psi'(nu/2)

   so ``y = log(s^2) - psi(nu/2) + log(nu/2)`` is unbiased for ``log sigma^2``
   and ``w = 1/psi'(nu/2)`` is the right weight. This is a strict improvement on
   D-040's unweighted OLS on ``log(sd)`` restricted to n>=3: it is unbiased at
   every replicate count, so 2-replicate treatments contribute at their true
   (small) information content instead of being dropped. D-040's specification
   is run alongside it for comparability. Standard errors are cluster-robust by
   SITE, matching the bootstrap's clustering.

3. PAIRED SUBTRACTION CONTRAST - see section 4.

FILTERS
-------
The headline tier applies D-024, D-025 and D-028 exactly as the G1 derivation
does, so the numbers are comparable to VC-BPS-005/006. Relaxed tiers are
reported alongside and are explicitly NOT comparable - dropping D-024 admits
sites whose replicates are not randomized replicates, and dropping D-025 admits
experimental units that are not plots. They are shown because the headline tier
turns out not to identify the effect at all, and the reason it does not is
itself the finding.

USAGE
-----
    python scripts/ic_conditioning.py
    python scripts/ic_conditioning.py --bootstrap 200      # faster, wider CIs
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from loam.decisions import (  # noqa: E402
    HEADLINE_DESIGNS,
    HEADLINE_EU_TYPE,
    IPCC_OUT_OF_SCOPE_REGIONS,
)

_spec = importlib.util.spec_from_file_location(
    "g1", os.path.join(os.path.dirname(__file__), "derive_g1_napeshm.py")
)
g1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g1)

#: Treatment-mean inorganic carbon (%) cut points for the stratified estimates.
#: Chosen from the distribution in section 1 BEFORE any CV was computed: zero is
#: its own stratum because 82% of experimental units sit exactly there, and the
#: positive mass splits near 0.1 and 0.5.
IC_STRATA = ((0.0, 0.0), (0.0, 0.1), (0.1, 0.5), (0.5, np.inf))

#: Sample tiers. Each says which D-NNN filters it applies, because the whole
#: point of the tier table is that the answer depends on which ones you keep.
TIERS = (
    ("T1_headline", "D-024 + D-025 + D-028 (comparable to VC-BPS-005/006)", True, True),
    ("T2_all_designs", "D-025 + D-028; D-024 DROPPED - not randomized replicates", False, True),
    ("T3_all_eu_types", "D-024 + D-028; D-025 DROPPED - not plot-scale", True, False),
    ("T4_climate_only", "D-028 only; D-024 and D-025 both DROPPED", False, False),
)


# ---------------------------------------------------------------------------
# sample construction
# ---------------------------------------------------------------------------


#: Site columns the G1 loader does not merge, needed here for the confound test.
#: `mi` (Thornthwaite moisture index) and `hargreave_cmd` are used ONLY as
#: aridity covariates. D-033 forbids treating either as an IPCC MAP:PET ratio,
#: and nothing here does - no climate REGION is derived from them.
EXTRA_SITE_COLS = ["mi", "hargreave_cmd", "na_l1name", "site_elevation"]


def attach_site_covariates(df: pd.DataFrame) -> pd.DataFrame:
    sites = pd.read_csv(g1.DATA + "sites.csv", low_memory=False)
    return df.merge(sites[["siteid"] + EXTRA_SITE_COLS], on="siteid", how="left")


def tier_sample(df: pd.DataFrame, use_d024: bool, use_d025: bool,
                in_scope: bool = True) -> pd.DataFrame:
    d = df[df.b_soc.notna()]
    if use_d024:
        d = d[d.exper_design.isin(HEADLINE_DESIGNS)]
    if use_d025:
        d = d[d.eu_type == HEADLINE_EU_TYPE]
    if in_scope:
        d = d[~d.ipcc_region.isin(IPCC_OUT_OF_SCOPE_REGIONS)]
    d = g1._with_replicates(d)
    return g1.add_targets(d).copy()


def with_ic(d: pd.DataFrame) -> pd.DataFrame:
    """Attach the treatment-mean inorganic carbon and its stratum label.

    The stratifier has to be constant within treatment: the response is a
    WITHIN-treatment residual, so a covariate that varies inside the treatment
    would be partly explaining the thing it is meant to condition.
    """
    d = d.copy()
    d["ic_trt"] = d.groupby("treatmentid").b_ic.transform("mean")
    labels, bounds = [], []
    for lo, hi in IC_STRATA:
        labels.append("ic_zero" if hi == 0.0 else
                      f"ic_{lo:g}_to_{'inf' if np.isinf(hi) else f'{hi:g}'}")
        bounds.append((lo, hi))
    def lab(v):
        for name, (lo, hi) in zip(labels, bounds):
            if hi == 0.0:
                if v <= 0:
                    return name
            elif lo < v <= hi:
                return name
        return labels[-1]
    d["ic_stratum"] = d.ic_trt.map(lab)
    d["ic_pos"] = (d.ic_trt > 0).astype(float)
    return d


# ---------------------------------------------------------------------------
# 1. distribution  (task 1a)
# ---------------------------------------------------------------------------


def ic_distribution(df: pd.DataFrame) -> dict:
    ic = df.b_ic
    per_site = df.groupby("sitecode").b_ic.agg(["size", "mean", "min", "max"])
    per_site["frac_pos"] = df.groupby("sitecode").b_ic.apply(lambda x: float((x > 0).mean()))
    pos_sites = per_site[per_site["max"] > 0].sort_values("mean", ascending=False)

    # b_soc is DEFINED as b_total_c - b_ic. Check that, because everything in
    # section 4 rests on it being an identity rather than a description.
    tri = df.dropna(subset=["b_soc", "b_total_c", "b_ic"])
    resid = (tri.b_total_c - tri.b_ic - tri.b_soc).abs()
    off = tri[resid > 1e-6]

    return {
        "n_eus_total": int(len(df)),
        "n_eus_b_ic_reported": int(ic.notna().sum()),
        "n_eus_b_ic_missing": int(ic.isna().sum()),
        "n_eus_ic_zero": int((ic == 0).sum()),
        "n_eus_ic_positive": int((ic > 0).sum()),
        "frac_positive": round(float((ic > 0).mean()), 4),
        "quantiles_all_eus": {str(q): round(float(ic.quantile(q)), 4)
                              for q in (0, .25, .5, .75, .9, .95, .99, 1)},
        "quantiles_positive_only": {str(q): round(float(ic[ic > 0].quantile(q)), 4)
                                    for q in (0, .1, .25, .5, .75, .9, 1)},
        "mean_pct": round(float(ic.mean()), 4),
        "max_pct": round(float(ic.max()), 4),
        "n_sites_total": int(df.sitecode.nunique()),
        "n_sites_any_positive": int((per_site["max"] > 0).sum()),
        "n_sites_all_zero": int((per_site["max"] == 0).sum()),
        "sites_with_ic": [
            {"sitecode": k, "n_eus": int(v["size"]), "mean_ic": round(float(v["mean"]), 4),
             "max_ic": round(float(v["max"]), 4), "frac_eus_positive": round(float(v.frac_pos), 3)}
            for k, v in pos_sites.iterrows()
        ],
        "identity_b_soc_eq_total_c_minus_ic": {
            "n_checked": int(len(tri)),
            "n_exact_to_1e-6": int((resid <= 1e-6).sum()),
            "n_off": int(len(off)),
            "max_abs_residual_pct": round(float(resid.max()), 6),
            "off_eucodes": off.eucode.tolist()[:10],
        },
    }


# ---------------------------------------------------------------------------
# 2. stratified REML  (task 1b, headline estimator)
# ---------------------------------------------------------------------------


def stratified_reml(d: pd.DataFrame, col: str, n_boot: int, seed: int = 20260812) -> dict:
    """Run the G1 estimator inside each IC stratum. NOT ESTIMABLE is an answer."""
    out = {}
    for name, part in d.groupby("ic_stratum"):
        part = g1._with_replicates(part[part[col].notna()])
        trt = part.groupby("treatmentid")
        block = {
            "n_eus": int(len(part)),
            "n_treatments": int(part.treatmentid.nunique()),
            "n_sites": int(part.sitecode.nunique()),
            "sites": sorted(part.sitecode.unique().tolist()),
            "countries": part.country.value_counts().to_dict(),
            "n_treatments_ge3_reps": int((trt.size() >= 3).sum()),
            "ic_trt_range": [round(float(part.ic_trt.min()), 4),
                             round(float(part.ic_trt.max()), 4)],
            "mean_soc_pct": round(float(part.b_soc.mean()), 3),
        }
        v = g1.residual_var(part, col)
        cv = g1.cv_from_logvar(v)
        if cv is None:
            block["cv_pct"] = None
            block["not_estimable_because"] = (
                f"{block['n_treatments']} treatments / {block['n_sites']} sites - "
                "the G1 estimator requires >=5 treatments and >=3 sites"
            ) if (block["n_treatments"] < 5 or block["n_sites"] < 3) else "REML did not converge"
        else:
            block["cv_pct"] = round(cv, 3)
            if n_boot:
                ci = g1.bootstrap_cv(part, col, n_boot, seed=seed)
                if ci:
                    block["ci95"] = [ci["ci95_low"], ci["ci95_high"]]
                    block["ci_width"] = round(ci["ci95_high"] - ci["ci95_low"], 3)
                    block["n_boot_ok"] = ci["n_successful"]
        out[name] = block
    return out


def identifiability_audit(d: pd.DataFrame) -> dict:
    """Can this sample separate IC from country and from replicate support?

    D-040 check 1c recorded that country and per-treatment replicate support are
    completely aliased in NAPESHM. If IC is aliased with country too, then the
    three are mutually aliased and no amount of estimation fixes it. That is a
    property of the design, so it is checked before anything is fitted.
    """
    t = d.groupby("treatmentid").agg(
        n=("euid", "size"), ic=("ic_trt", "first"),
        site=("sitecode", "first"), country=("country", "first"))
    pos = t[t.ic > 0]
    xt = pd.crosstab(t.n, [t.ic > 0, t.country])
    return {
        "n_treatments": int(len(t)),
        "n_treatments_ic_positive": int(len(pos)),
        "ic_positive_countries": pos.country.value_counts().to_dict(),
        "ic_positive_sites": sorted(pos.site.unique().tolist()),
        "ic_positive_replicate_hist": {int(k): int(v)
                                       for k, v in pos.n.value_counts().sort_index().items()},
        "ic_zero_replicate_hist": {int(k): int(v) for k, v in
                                   t[t.ic <= 0].n.value_counts().sort_index().items()},
        "n_ic_positive_with_ge3_reps": int((pos.n >= 3).sum()),
        "ic_positive_ge3_countries": pos[pos.n >= 3].country.value_counts().to_dict(),
        "crosstab_reps_by_icpos_country": {str(k): {str(c): int(x) for c, x in v.items()}
                                           for k, v in xt.to_dict("index").items()},
        "ic_aliased_with_country": bool(len(pos) and pos.country.nunique() == 1),
    }


# ---------------------------------------------------------------------------
# 3. log-variance regression  (task 1b, functional form + confound conditioning)
# ---------------------------------------------------------------------------


def treatment_table(d: pd.DataFrame, col: str = "log_soc") -> pd.DataFrame:
    """One row per treatment: debiased log within-treatment variance + covariates."""
    from scipy.special import digamma, polygamma

    sub = g1._with_replicates(d[d[col].notna()])
    g = sub.groupby("treatmentid")
    t = pd.DataFrame({
        "n": g.size(),
        "s2": g[col].var(ddof=1),
        "ic": g.ic_trt.first(),
        "mean_soc": g.b_soc.mean(),
        "clay": g.b_clay.mean(),
        "sand": g.b_sand.mean(),
        "ph": g.b_ph.mean(),
        "site": g.sitecode.first(),
        "country": g.country.first(),
        "mat": g.site_mean_temp.first(),
        "map": g.site_precip.first(),
        "mi": g["mi"].first(),
        "hargreave_cmd": g["hargreave_cmd"].first(),
        "ecoregion": g["na_l1name"].first(),
    })
    t = t[(t.s2 > 0) & t.s2.notna()]
    nu = (t.n - 1).astype(float)
    # Unbiased for log(sigma^2) at every replicate count; weight by information.
    t["y"] = np.log(t.s2) - digamma(nu / 2) + np.log(nu / 2)
    t["w"] = 1.0 / polygamma(1, nu / 2)
    t["nu"] = nu
    return t


def wls_cluster(t: pd.DataFrame, terms: list[str], label: str) -> dict | None:
    """Weighted least squares with site-clustered standard errors."""
    cols = [c for c in terms if c not in ("const",)]
    sub = t.dropna(subset=cols + ["y", "w"])
    X = np.column_stack([np.ones(len(sub))] + [sub[c].values.astype(float) for c in cols])
    names = ["const"] + cols
    if len(sub) <= X.shape[1] + 1 or sub.site.nunique() < 3:
        return {"model": label, "not_estimable": True,
                "n_treatments": int(len(sub)), "n_sites": int(sub.site.nunique())}
    W = np.diag(sub.w.values)
    y = sub.y.values
    XtW = X.T @ W
    try:
        bread = np.linalg.inv(XtW @ X)
    except np.linalg.LinAlgError:
        return {"model": label, "not_estimable": True, "reason": "singular design"}
    beta = bread @ (XtW @ y)
    r = y - X @ beta
    meat = np.zeros((X.shape[1], X.shape[1]))
    for _, idx in sub.groupby("site").groups.items():
        pos = sub.index.get_indexer(idx)
        u = (X[pos].T @ (W[np.ix_(pos, pos)] @ r[pos])).reshape(-1, 1)
        meat += u @ u.T
    G = sub.site.nunique()
    scale = G / max(G - 1, 1)
    V = bread @ meat @ bread * scale
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    ss_tot = float(((y - np.average(y, weights=sub.w.values)) ** 2 * sub.w.values).sum())
    ss_res = float((r ** 2 * sub.w.values).sum())
    return {
        "model": label,
        "n_treatments": int(len(sub)),
        "n_sites": int(G),
        "weighted_r2": round(1 - ss_res / ss_tot, 4) if ss_tot > 0 else None,
        "coefficients": {
            nm: {"beta": round(float(b), 4), "se_cluster_site": round(float(s), 4),
                 "t": round(float(b / s), 2) if s > 0 else None}
            for nm, b, s in zip(names, beta, se)
        },
    }


def regression_block(d: pd.DataFrame) -> dict:
    """Functional form, effect size, and whether IC survives climate conditioning."""
    t = treatment_table(d)
    t = t.assign(
        ic_pos=(t.ic > 0).astype(float),
        log1p_ic=np.log1p(t.ic),
        log_mean_soc=np.log(t.mean_soc),
        sand_frac=t.sand / 100.0,
        clay_frac=t.clay / 100.0,
        map_m=t["map"] / 1000.0,
        mi_z=(t.mi - t.mi.mean()) / t.mi.std(ddof=0) if t.mi.std(ddof=0) > 0 else t.mi * 0,
        usa=(t.country == "USA").astype(float),
    )
    from scipy import stats
    out = {
        "n_treatments": int(len(t)),
        "n_sites": int(t.site.nunique()),
        "n_treatments_ic_positive": int((t.ic > 0).sum()),
        "replicate_hist": {int(k): int(v) for k, v in t.n.value_counts().sort_index().items()},
        "spearman_ic_vs_logvar": None,
        "models": [],
    }
    if len(t) > 5:
        rho, p = stats.spearmanr(t.ic, t.y)
        out["spearman_ic_vs_logvar"] = {"rho": round(float(rho), 3), "p": round(float(p), 4)}
        rho2, p2 = stats.spearmanr(t.ic[t.ic > 0], t.y[t.ic > 0]) if (t.ic > 0).sum() > 5 else (np.nan, np.nan)
        out["spearman_within_positive_ic"] = (
            None if np.isnan(rho2) else {"rho": round(float(rho2), 3), "p": round(float(p2), 4),
                                         "n": int((t.ic > 0).sum())})

    specs = [
        (["ic_pos"], "M1 binary: any inorganic carbon"),
        (["ic"], "M2 linear dose in IC (%)"),
        (["log1p_ic"], "M3 log1p(IC)"),
        (["ic", "log_mean_soc", "sand_frac"], "M4 + D-040 covariates (SOC level, sand)"),
        (["ic", "log_mean_soc", "sand_frac", "mi_z", "mat"],
         "M5 + climate conditioning (Thornthwaite MI, MAT)"),
        (["ic", "log_mean_soc", "sand_frac", "map_m", "mat"],
         "M6 + climate conditioning (MAP, MAT)"),
        (["ic", "log_mean_soc", "sand_frac", "usa"], "M7 + country"),
        (["ic", "log_mean_soc", "sand_frac", "ph"], "M8 + pH"),
    ]
    for terms, label in specs:
        r = wls_cluster(t, terms, label)
        if r:
            out["models"].append(r)

    # D-040's own specification, for comparability: unweighted OLS on log(sd),
    # n>=3 only, no debiasing.
    t3 = t[t.n >= 3]
    if len(t3) > 6 and t3.site.nunique() >= 3:
        t3 = t3.assign(y=np.log(np.sqrt(t3.s2)), w=1.0)
        out["d040_specification"] = wls_cluster(
            t3, ["ic", "log_mean_soc", "sand_frac"],
            "D-040 spec: unweighted OLS on log(SD), n>=3 only")

    # How much IC variation is WITHIN site? If none, no within-site model exists.
    if len(t):
        gs = t.groupby("site").ic
        out["ic_variation_within_site"] = {
            "n_sites": int(t.site.nunique()),
            "n_sites_with_any_within_site_ic_spread": int((gs.max() - gs.min() > 1e-9).sum()),
            "max_within_site_ic_range": round(float((gs.max() - gs.min()).max()), 4),
            "share_of_ic_variance_between_sites": round(float(
                1 - (t.ic - t.groupby("site").ic.transform("mean")).var(ddof=0)
                / t.ic.var(ddof=0)), 4) if t.ic.var(ddof=0) > 0 else None,
        }
    return out


# ---------------------------------------------------------------------------
# 4. paired subtraction contrast  (mechanism, immune to site confounds)
# ---------------------------------------------------------------------------


def paired_subtraction(d: pd.DataFrame) -> dict:
    """Does measuring SOC BY DIFFERENCE inflate its between-plot variance?

    ``b_soc = b_total_c - b_ic``. Total carbon is measured directly by dry
    combustion; organic carbon is not. So for each treatment compare

        Delta = log Var(log b_soc) - log Var(log b_total_c)

    across the SAME replicate experimental units. Two properties make this the
    sharpest test available here:

    * The degrees of freedom are identical for both variances, so the E[log s^2]
      bias term cancels EXACTLY in the difference - no correction needed.
    * Every treatment with zero inorganic carbon has ``b_soc == b_total_c``
      identically, hence ``Delta == 0`` by construction. That is a built-in null
      control: any estimator that returns a non-zero effect there is broken.

    Because it is a within-treatment paired contrast, every site-level confound
    - climate, parent material, country, management, laboratory - cancels.

    WHAT IT DOES NOT SEPARATE. ``Delta > 0`` means the carbonate term added
    variance to the SOC estimate. That term contains BOTH calcimeter measurement
    error AND genuine between-plot spatial variation in carbonate content. Both
    are real contributors to the measured between-plot variance of SOC, and only
    the first is analytical. The test bounds the subtraction's total contribution
    without attributing it.
    """
    from scipy import stats

    sub = d[d.b_soc.notna() & d.b_total_c.notna() & (d.b_soc > 0) & (d.b_total_c > 0)].copy()
    sub["log_tc"] = np.log(sub.b_total_c)
    sub = g1._with_replicates(sub)
    g = sub.groupby("treatmentid")
    t = pd.DataFrame({
        "n": g.size(),
        "v_soc": g.log_soc.var(ddof=1),
        "v_tc": g.log_tc.var(ddof=1),
        "ic": g.ic_trt.first(),
        "ic_sd": g.b_ic.std(ddof=1),
        "mean_soc": g.b_soc.mean(),
        "site": g.sitecode.first(),
        "country": g.country.first(),
    }).dropna(subset=["v_soc", "v_tc"])
    t = t[(t.v_soc > 0) & (t.v_tc > 0)]
    t["delta"] = np.log(t.v_soc) - np.log(t.v_tc)
    t["cv_soc"] = 100 * np.sqrt(np.expm1(t.v_soc))
    t["cv_tc"] = 100 * np.sqrt(np.expm1(t.v_tc))

    zero, pos = t[t.ic <= 0], t[t.ic > 0]
    out = {
        "n_treatments": int(len(t)),
        "null_control_ic_zero": {
            "n_treatments": int(len(zero)),
            "max_abs_delta": round(float(zero.delta.abs().max()), 12) if len(zero) else None,
            "passes": bool(len(zero) and zero.delta.abs().max() < 1e-9),
        },
        "ic_positive": {
            "n_treatments": int(len(pos)),
            "n_sites": int(pos.site.nunique()),
            "countries": pos.country.value_counts().to_dict(),
        },
    }
    if len(pos) >= 3:
        ratio = np.exp(pos.delta)
        out["ic_positive"].update({
            "median_variance_ratio_soc_over_tc": round(float(np.median(ratio)), 4),
            "mean_delta_log": round(float(pos.delta.mean()), 4),
            "n_delta_positive": int((pos.delta > 0).sum()),
            "n_delta_negative": int((pos.delta < 0).sum()),
            "sign_test_p_two_sided": round(float(
                stats.binomtest(int((pos.delta > 0).sum()), len(pos), 0.5).pvalue), 5),
            "median_cv_soc_pct": round(float(pos.cv_soc.median()), 3),
            "median_cv_tc_pct": round(float(pos.cv_tc.median()), 3),
            "spearman_delta_vs_ic": None,
        })
        rho, p = stats.spearmanr(pos.ic, pos.delta)
        out["ic_positive"]["spearman_delta_vs_ic"] = {
            "rho": round(float(rho), 3), "p": round(float(p), 4)}
        # per-site medians: the honest unit, since IC is a site property
        per_site = pos.groupby("site").agg(
            n_trt=("delta", "size"), ic=("ic", "mean"),
            median_delta=("delta", "median"),
            median_ratio=("delta", lambda x: float(np.exp(np.median(x)))),
            median_cv_soc=("cv_soc", "median"), median_cv_tc=("cv_tc", "median"))
        out["ic_positive"]["by_site"] = [
            {"sitecode": k, "n_treatments": int(v.n_trt), "mean_ic_pct": round(float(v.ic), 4),
             "median_variance_ratio": round(float(v.median_ratio), 4),
             "median_cv_soc_pct": round(float(v.median_cv_soc), 3),
             "median_cv_tc_pct": round(float(v.median_cv_tc), 3)}
            for k, v in per_site.sort_values("ic", ascending=False).iterrows()]
        if per_site.shape[0] >= 4:
            rho_s, p_s = stats.spearmanr(per_site.ic, per_site.median_delta)
            out["ic_positive"]["spearman_site_level"] = {
                "rho": round(float(rho_s), 3), "p": round(float(p_s), 4),
                "n_sites": int(per_site.shape[0])}
    return out


# ---------------------------------------------------------------------------
# 5. site-level contrast  (task 1c)
# ---------------------------------------------------------------------------


def site_level(d: pd.DataFrame, col: str = "log_soc") -> dict:
    """Pooled within-treatment CV per site, against that site's inorganic carbon.

    Pooling sums squares over the site's treatments and divides by summed df,
    which is the right way to combine variances estimated on 1-5 df each -
    averaging per-treatment CVs would weight a 2-replicate treatment as heavily
    as a 6-replicate one, the error D-029 rejects.
    """
    from scipy import stats

    sub = g1._with_replicates(d[d[col].notna()])
    g = sub.groupby(["sitecode", "treatmentid"])
    ss = (g[col].var(ddof=1) * (g.size() - 1)).groupby("sitecode").sum()
    dfree = (g.size() - 1).groupby("sitecode").sum()
    ic = sub.groupby("sitecode").b_ic.mean()
    soc = sub.groupby("sitecode").b_soc.mean()
    n_trt = sub.groupby("sitecode").treatmentid.nunique()
    country = sub.groupby("sitecode").country.first()
    mi = sub.groupby("sitecode")["mi"].first()
    site = pd.DataFrame({"ss": ss, "df": dfree, "ic": ic, "mean_soc": soc,
                         "n_trt": n_trt, "country": country, "mi": mi}).dropna(subset=["ss", "df"])
    site = site[site.df >= 2]
    site["pooled_var"] = site.ss / site.df
    site["cv_pct"] = 100 * np.sqrt(np.expm1(site.pooled_var))

    hi = site[site.ic > 0.1]
    lo = site[site.ic <= 0.1]
    out = {
        "n_sites": int(len(site)),
        "cut_pct_ic": 0.1,
        "high_ic": {"n_sites": int(len(hi)),
                    "median_cv_pct": round(float(hi.cv_pct.median()), 3) if len(hi) else None,
                    "df_weighted_cv_pct": round(float(
                        100 * np.sqrt(np.expm1((hi.ss.sum() / hi.df.sum())))), 3) if len(hi) else None,
                    "sitecodes": sorted(hi.index.tolist())},
        "low_ic": {"n_sites": int(len(lo)),
                   "median_cv_pct": round(float(lo.cv_pct.median()), 3) if len(lo) else None,
                   "df_weighted_cv_pct": round(float(
                       100 * np.sqrt(np.expm1((lo.ss.sum() / lo.df.sum())))), 3) if len(lo) else None},
        "per_site": [
            {"sitecode": k, "country": v.country, "mean_ic_pct": round(float(v.ic), 4),
             "mean_soc_pct": round(float(v.mean_soc), 3), "n_treatments": int(v.n_trt),
             "df": int(v.df), "within_treatment_cv_pct": round(float(v.cv_pct), 3)}
            for k, v in site.sort_values("ic", ascending=False).iterrows()],
    }
    if len(site) >= 6:
        rho, p = stats.spearmanr(site.ic, site.cv_pct)
        out["spearman_ic_vs_site_cv"] = {"rho": round(float(rho), 3), "p": round(float(p), 4),
                                         "n_sites": int(len(site))}
        pos = site[site.ic > 0]
        if len(pos) >= 5:
            rho2, p2 = stats.spearmanr(pos.ic, pos.cv_pct)
            out["spearman_within_positive_sites"] = {
                "rho": round(float(rho2), 3), "p": round(float(p2), 4), "n_sites": int(len(pos))}
        if len(hi) >= 2 and len(lo) >= 2:
            u, pu = stats.mannwhitneyu(hi.cv_pct, lo.cv_pct, alternative="greater")
            out["mannwhitney_high_gt_low"] = {"U": float(u), "p_one_sided": round(float(pu), 4)}
    return out


# ---------------------------------------------------------------------------
# 6. the confound, measured rather than asserted
# ---------------------------------------------------------------------------


def confound_block(d: pd.DataFrame) -> dict:
    """How strongly is inorganic carbon tied to aridity, temperature and pH?"""
    from scipy import stats

    site = d.groupby("sitecode").agg(
        ic=("b_ic", "mean"), mi=("mi", "first"), mat=("site_mean_temp", "first"),
        map_mm=("site_precip", "first"), cmd=("hargreave_cmd", "first"),
        ph=("b_ph", "mean"), clay=("b_clay", "mean"), soc=("b_soc", "mean"),
        country=("country", "first")).dropna(subset=["ic"])
    out = {"n_sites": int(len(site)), "spearman_site_level": {}}
    for v in ("mi", "mat", "map_mm", "cmd", "ph", "clay", "soc"):
        s = site.dropna(subset=[v])
        if len(s) >= 6:
            rho, p = stats.spearmanr(s.ic, s[v])
            out["spearman_site_level"][v] = {
                "rho": round(float(rho), 3), "p": round(float(p), 4), "n_sites": int(len(s))}
    out["ic_by_country"] = {
        k: {"n_sites": int(len(v)), "mean_ic_pct": round(float(v.ic.mean()), 4),
            "n_sites_ic_positive": int((v.ic > 0).sum())}
        for k, v in site.groupby("country")}
    return out


# ---------------------------------------------------------------------------
# 7. what this test could have detected  (the project's own logic, turned inward)
# ---------------------------------------------------------------------------


def implied_analytical(cv_high: float | None, cv_zero: float | None) -> float | None:
    """Extra error term implied by a CV difference, in quadrature.

    Under D-027 the residual is ``sqrt(spatial^2 + analytical^2)``. If carbonate
    soils differ only by a larger analytical term, the added term is
    ``sqrt(cv_high^2 - cv_zero^2)``. A negative radicand means the carbonate
    stratum is LESS variable and the mechanism is not present in that contrast -
    returned as None, never as a small positive number.
    """
    if cv_high is None or cv_zero is None:
        return None
    d = cv_high ** 2 - cv_zero ** 2
    return round(float(np.sqrt(d)), 3) if d > 0 else None


def power_statement(strata: dict, baseline_analytical_pct: float = 3.13) -> dict:
    """Minimum analytical inflation this design could have distinguished.

    LoAM's whole claim is that detectability is a property of the variance
    structure, not of a mean trajectory. That applies to this test as much as to
    a monitoring programme: a null result is only informative against a stated
    detection limit. So state one.

    Take the zero-carbonate stratum as the reference. Its 95% cluster-bootstrap
    interval is how precisely we know that CV. An added analytical term ``a``
    raises the CV to ``sqrt(cv0^2 + a^2 - a0^2)``, where ``a0`` is the analytical
    error already inside ``cv0``. The smallest ``a`` whose predicted CV clears
    the upper end of the reference interval is the smallest inflation this
    sample could have separated from noise.
    """
    zero = strata.get("ic_zero", {})
    cv0, ci = zero.get("cv_pct"), zero.get("ci95")
    if cv0 is None or not ci:
        return {"not_computable": "no interval on the zero-carbonate stratum"}
    a0 = baseline_analytical_pct
    target = ci[1]                              # upper end of the reference CI
    need2 = target ** 2 - cv0 ** 2 + a0 ** 2
    mdi = float(np.sqrt(need2)) if need2 > 0 else None
    out = {
        "reference_stratum_cv_pct": cv0,
        "reference_ci95": ci,
        "assumed_analytical_already_inside_pct": a0,
        "min_detectable_analytical_pct": None if mdi is None else round(mdi, 3),
        "potash_stated_range_pct": [1.0, 10.0],
    }
    if mdi is not None:
        out["detects_top_of_potash_range"] = bool(mdi < 10.0)
        out["detects_middle_of_potash_range"] = bool(mdi < 5.0)
        out["blind_below_pct"] = round(mdi, 3)
    for name, block in strata.items():
        if name == "ic_zero":
            continue
        out.setdefault("implied_added_term_by_stratum", {})[name] = {
            "cv_pct": block.get("cv_pct"),
            "implied_added_error_pct": implied_analytical(block.get("cv_pct"), cv0),
            "n_sites": block.get("n_sites"),
            "countries": block.get("countries"),
        }
    return out


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap", type=int, default=400)
    ap.add_argument("--out", default="data/processed/ic_conditioning.json")
    args = ap.parse_args()

    df = attach_site_covariates(g1.load())
    result = {
        "note": "EXPLORATORY - no variance-table row is written by this script",
        "dataset": "NAPESHM, Soil Health Institute (2024), doi:10.15482/USDA.ADC/25632270",
        "response": ("within-treatment within-site residual CV of log SOC CONCENTRATION at "
                     "0-15 cm - the same quantity as VC-BPS-005, which per D-027 bundles "
                     "between-plot spatial + within-plot spatial + analytical error"),
        "covariate": "b_ic, inorganic carbon %, Chittick calcimeter (NAPESHM data dictionary)",
        "prompted_by": "Potash correspondence 2026-08-11",
    }

    # ------------------------------------------------------------- 1a -------
    print("=" * 78)
    print("1a. DISTRIBUTION OF INORGANIC CARBON (all EUs, before any filter)")
    print("=" * 78)
    dist = ic_distribution(df)
    result["distribution_all_eus"] = dist
    print(f"  {dist['n_eus_total']} EUs, b_ic reported for {dist['n_eus_b_ic_reported']} "
          f"({dist['n_eus_b_ic_missing']} missing)")
    print(f"  exactly zero : {dist['n_eus_ic_zero']:>5}  "
          f"({1 - dist['frac_positive']:.1%})")
    print(f"  positive     : {dist['n_eus_ic_positive']:>5}  ({dist['frac_positive']:.1%})   "
          f"max {dist['max_pct']}%")
    print(f"  quantiles, all EUs      : {dist['quantiles_all_eus']}")
    print(f"  quantiles, positives    : {dist['quantiles_positive_only']}")
    print(f"  sites: {dist['n_sites_total']} total, {dist['n_sites_any_positive']} with any "
          f"IC > 0, {dist['n_sites_all_zero']} entirely zero")
    idn = dist["identity_b_soc_eq_total_c_minus_ic"]
    print(f"  identity b_soc == b_total_c - b_ic : {idn['n_exact_to_1e-6']}/{idn['n_checked']} "
          f"exact to 1e-6 (max residual {idn['max_abs_residual_pct']}%)")
    print("\n  sites carrying inorganic carbon:")
    for s in dist["sites_with_ic"][:14]:
        print(f"    {s['sitecode']:<8} n={s['n_eus']:>3}  mean {s['mean_ic']:>6.3f}%  "
              f"max {s['max_ic']:>6.3f}%  {s['frac_eus_positive']:.0%} of EUs positive")

    # ------------------------------------------------------------- tiers ----
    result["tiers"] = {}
    for key, desc, d024, d025 in TIERS:
        d = with_ic(tier_sample(df, d024, d025))
        block = {"filters": desc, "n_eus": int(len(d)),
                 "n_treatments": int(d.treatmentid.nunique()),
                 "n_sites": int(d.sitecode.nunique()),
                 "n_eus_ic_positive": int((d.b_ic > 0).sum())}
        print("\n" + "=" * 78)
        print(f"TIER {key} - {desc}")
        print(f"  {block['n_eus']} EU / {block['n_treatments']} trt / {block['n_sites']} sites; "
              f"{block['n_eus_ic_positive']} EUs with IC > 0")
        print("=" * 78)

        aud = identifiability_audit(d)
        block["identifiability"] = aud
        print(f"  IC-positive treatments: {aud['n_treatments_ic_positive']} "
              f"{aud['ic_positive_countries']}  sites {aud['ic_positive_sites']}")
        print(f"  their replicate counts: {aud['ic_positive_replicate_hist']}   "
              f"(IC-zero: {aud['ic_zero_replicate_hist']})")
        print(f"  IC-positive treatments with >=3 replicates: "
              f"{aud['n_ic_positive_with_ge3_reps']} {aud['ic_positive_ge3_countries']}")
        if aud["ic_aliased_with_country"]:
            print("  *** INORGANIC CARBON IS PERFECTLY ALIASED WITH COUNTRY IN THIS TIER ***")

        print("\n  1b. stratified REML (G1 estimator, cluster bootstrap over sites)")
        strat = stratified_reml(d, "log_soc", args.bootstrap)
        block["stratified_reml_concentration"] = strat
        for name in sorted(strat):
            b = strat[name]
            if b["cv_pct"] is None:
                print(f"    {name:<14} NOT ESTIMABLE - {b['not_estimable_because']} "
                      f"[{b['n_eus']} EU / {b['n_treatments']} trt / {b['n_sites']} sites]")
            else:
                ci = b.get("ci95")
                band = f"  95% CI [{ci[0]:.2f}, {ci[1]:.2f}] w={b['ci_width']:.2f}" if ci else ""
                print(f"    {name:<14} CV = {b['cv_pct']:6.3f}%{band}   "
                      f"[{b['n_eus']} EU / {b['n_treatments']} trt / {b['n_sites']} sites, "
                      f"{b['countries']}]")

        print("\n  1b. log-variance regression (debiased, site-clustered SEs)")
        reg = regression_block(d)
        block["regression"] = reg
        sp = reg.get("spearman_ic_vs_logvar")
        if sp:
            print(f"    spearman(IC, log within-treatment variance) rho={sp['rho']:+.3f} "
                  f"p={sp['p']:.4f}   n={reg['n_treatments']} treatments")
        for m in reg["models"]:
            if m.get("not_estimable"):
                print(f"    {m['model']:<52} NOT ESTIMABLE")
                continue
            c = m["coefficients"]
            key_term = "ic" if "ic" in c else ("ic_pos" if "ic_pos" in c else "log1p_ic")
            k = c[key_term]
            flag = "SIGNIFICANT" if k["t"] is not None and abs(k["t"]) > 2 else "ns"
            print(f"    {m['model']:<52} beta[{key_term}]={k['beta']:+.4f} "
                  f"se={k['se_cluster_site']:.4f} t={k['t']:+.2f} {flag}  "
                  f"(n={m['n_treatments']}, {m['n_sites']} sites)")
        if "d040_specification" in reg and not reg["d040_specification"].get("not_estimable"):
            m = reg["d040_specification"]
            k = m["coefficients"]["ic"]
            print(f"    {m['model']:<52} beta[ic]={k['beta']:+.4f} t={k['t']:+.2f}")
        iv = reg.get("ic_variation_within_site")
        if iv:
            print(f"    IC variance between sites: {iv['share_of_ic_variance_between_sites']}; "
                  f"{iv['n_sites_with_any_within_site_ic_spread']}/{iv['n_sites']} sites have "
                  f"any within-site spread")

        print("\n  4. paired subtraction contrast: Var(log SOC) vs Var(log total C)")
        pair = paired_subtraction(d)
        block["paired_subtraction"] = pair
        nc = pair["null_control_ic_zero"]
        print(f"    null control (IC == 0): {nc['n_treatments']} treatments, "
              f"max |delta| = {nc['max_abs_delta']} -> "
              f"{'PASSES' if nc['passes'] else 'FAILS'}")
        p = pair["ic_positive"]
        if p.get("median_variance_ratio_soc_over_tc") is not None:
            print(f"    IC > 0: {p['n_treatments']} treatments / {p['n_sites']} sites "
                  f"{p['countries']}")
            print(f"      median Var(SOC)/Var(total C) = "
                  f"{p['median_variance_ratio_soc_over_tc']:.3f}   "
                  f"({p['n_delta_positive']} up / {p['n_delta_negative']} down, "
                  f"sign test p={p['sign_test_p_two_sided']})")
            print(f"      median within-treatment CV: SOC {p['median_cv_soc_pct']}%  vs  "
                  f"total C {p['median_cv_tc_pct']}%")
            s = p.get("spearman_delta_vs_ic")
            if s:
                print(f"      spearman(IC, log ratio) rho={s['rho']:+.3f} p={s['p']:.4f}")
            ss = p.get("spearman_site_level")
            if ss:
                print(f"      site level: rho={ss['rho']:+.3f} p={ss['p']:.4f} "
                      f"(n={ss['n_sites']} sites)")
            for row in p.get("by_site", []):
                print(f"        {row['sitecode']:<8} IC {row['mean_ic_pct']:>6.3f}%  "
                      f"ratio {row['median_variance_ratio']:>7.3f}  "
                      f"CV_SOC {row['median_cv_soc_pct']:>6.2f}%  "
                      f"CV_TC {row['median_cv_tc_pct']:>6.2f}%")
        else:
            print("    IC > 0: too few treatments for the contrast")

        print("\n  1c. site level")
        sl = site_level(d)
        block["site_level"] = sl
        print(f"    {sl['n_sites']} sites with >=2 df.  high IC (>{sl['cut_pct_ic']}%): "
              f"{sl['high_ic']['n_sites']} sites, df-weighted CV "
              f"{sl['high_ic']['df_weighted_cv_pct']}%  |  low IC: "
              f"{sl['low_ic']['n_sites']} sites, df-weighted CV "
              f"{sl['low_ic']['df_weighted_cv_pct']}%")
        for k in ("spearman_ic_vs_site_cv", "spearman_within_positive_sites"):
            if k in sl:
                v = sl[k]
                print(f"    {k}: rho={v['rho']:+.3f} p={v['p']:.4f} (n={v['n_sites']})")
        if "mannwhitney_high_gt_low" in sl:
            print(f"    Mann-Whitney high>low one-sided p="
                  f"{sl['mannwhitney_high_gt_low']['p_one_sided']}")

        print("\n  7. what this tier could have detected")
        pw = power_statement(strat)
        block["power"] = pw
        if "not_computable" in pw:
            print(f"    {pw['not_computable']}")
        else:
            print(f"    reference (zero carbonate) CV {pw['reference_stratum_cv_pct']}% "
                  f"CI {pw['reference_ci95']}")
            print(f"    smallest analytical error separable from that noise: "
                  f"{pw['min_detectable_analytical_pct']}%  "
                  f"(Potash's stated range 1-10%)")
            for nm, v in pw.get("implied_added_term_by_stratum", {}).items():
                imp = v["implied_added_error_pct"]
                if v["cv_pct"] is None:
                    verdict = "no estimate - stratum was NOT ESTIMABLE"
                elif imp is None:
                    verdict = "NONE - stratum is LESS variable than zero-carbonate"
                else:
                    verdict = f"{imp}%"
                print(f"    {nm:<14} CV {v['cv_pct']}% -> implied added error "
                      f"{verdict}  [{v['n_sites']} sites {v['countries']}]")

        result["tiers"][key] = block

    # ------------------------------------------------------------- 6 --------
    print("\n" + "=" * 78)
    print("6. THE CONFOUND, MEASURED (site level, all sites)")
    print("=" * 78)
    conf = confound_block(df[df.b_soc.notna()])
    result["confound"] = conf
    for v, s in conf["spearman_site_level"].items():
        print(f"    spearman(site mean IC, {v:<7}) rho={s['rho']:+.3f} p={s['p']:.4f} "
              f"n={s['n_sites']}")
    print(f"    by country: {conf['ic_by_country']}")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
