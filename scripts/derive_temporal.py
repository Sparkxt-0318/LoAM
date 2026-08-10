#!/usr/bin/env python3
"""Derive the temporal variance component from primary data, two sources.

Standalone and reproducible. Not part of the package build and not imported by
the test suite, in the same way as ``derive_g1_napeshm.py``.

    python scripts/derive_temporal.py --fetch      # download both sources first
    python scripts/derive_temporal.py              # derive from local copies

Why this exists
---------------
``VC-TMP-001/002`` were read off the ABSTRACT of Wuest & Durfee 2024 (a variance
SHARE of 20% temporal against 17% between-replicate, with ranges) because the
paper is paywalled. A share is not a variance: it cannot be added to anything,
its depth was ASSUMED to be 0-30 cm, and it could not be checked. The underlying
dataset turns out to be public domain on Ag Data Commons, so none of that has to
stand.

Sources
-------
PRIMARY - Wuest, S. B. & Durfee, N. (2024). "Data from: Temporal variability is
a major source of uncertainty in soil carbon measurements." Ag Data Commons,
doi:10.15482/USDA.ADC/25719348.v1. **U.S. Public Domain.** Five monthly series
of up to three years at four dryland sites in Oregon and Washington. 2195
plot-months. The paper is Wuest & Durfee 2024, SSSAJ 88(3):830-845,
doi:10.1002/saj2.20660.

CORROBORATION - W.K. Kellogg Biological Station LTER, "Soil Total Carbon and
Nitrogen (1993 to 2014)", table 102, https://lter.kbs.msu.edu/datatables/102.
Humid temperate row-crop in southwest Michigan - a different climate regime
entirely, which is the point. **NOT public domain**: KBS data are copyrighted
and publication requires written permission (see LICENCE NOTE below). Neither
raw file is committed; ``data/raw/`` is gitignored and both are re-fetched by
``--fetch``.

The estimator
-------------
Per site, on log SOC, with the treatment as a fixed effect so that the plot term
means "between replicate experimental units" rather than "between treatments":

    log C  ~  treatment  +  (1 | plot)  +  (1 | occasion)

Plot and occasion are CROSSED, not nested - every plot is visited on every
occasion. That is the whole reason this design can say anything about time: the
occasion effect is what all plots do together on a given date, so it cannot be
within-plot spatial noise (that would average away across 12-24 plots) and it
cannot be plot-to-plot heterogeneity (that is the plot term).

Three components come out:

``v_plot``   between replicate EUs - the G1 quantity, not the target here.
``v_occ``    field-wide month-to-month movement. SEPARABLE temporal variance.
``v_resid``  plot x occasion interaction + within-plot spatial + analytical.
             NOT separable: there is one measurement per plot per occasion, so
             nothing inside this term can be split off by this design.

What the two temporal numbers mean
----------------------------------
``v_occ`` alone is a LOWER BOUND on temporal variance: real plot-specific
timing effects live in the residual and are excluded from it.

``v_occ + v_resid`` is what a monitoring programme actually faces when it
revisits one plot at a new date, and it is an UPPER BOUND on temporal variance
because within-plot spatial and analytical error are inside it. That is the
combined row, and its bias direction is ``inflates``.

The true temporal term is between the two. We report both rather than pick.

Estimator validation
--------------------
Two independent routes, because a mixed-model optimiser is easy to trust wrongly:

1. REML via statsmodels ``MixedLM`` with crossed variance components.
2. Closed-form ANOVA moment estimates for a balanced two-way crossed design with
   one observation per cell:  v_plot = (MS_plot - MS_e)/q,
   v_occ = (MS_occ - MS_e)/p,  v_resid = MS_e.

The Wuest design is balanced apart from a single missing Ritzville cell, so
route 2 is exact and needs no optimiser (dropping the occasion that carries the
hole leaves 24 x 30 = 720 of 743 observations there; the other four series are
used whole). The two routes agree to within 0.53 percentage points of CV at
worst - Adams-residue's residual, 5.49% by moments against 4.97% by REML - and
to within 0.16-0.39 points elsewhere. That is agreement on every conclusion
drawn here, not agreement to the decimal, and the moment estimates are the ones
reported because they are closed-form for this design. Route 2 is also what the
bootstrap uses, because it costs nothing to refit.

TRAP, and the reason the two disagreed at first: ``MixedLM`` returns ``vcomp``
in SORTED key order, not in the order the ``vc_formula`` dict was written. With
keys ``{'plot': ..., 'occ': ...}`` the first entry is ``occ``. Reading them
positionally silently transposes the two components, which is survivable here
only because the ANOVA route caught it.

LICENCE NOTE - KBS
------------------
The KBS file carries: "These Data are copyrighted and use in a publication
requires written permission as detailed in our Terms of use". That is a real
constraint on the paper, not on this script. Any row derived from it must record
the requirement, and permission has to be obtained before publication. The Wuest
data carry no such condition.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WUEST_DIR = os.path.join(REPO_ROOT, "data", "raw", "wuest2024")
WUEST_FILES = {
    "SOC_variability.csv": "https://ndownloader.figshare.com/files/45998844",
    "SOC_variability_dictionary.csv": "https://ndownloader.figshare.com/files/45998847",
}
KBS_DIR = os.path.join(REPO_ROOT, "data", "raw", "kbs_lter")
KBS_FILES = {
    "kbs102_soil_total_c_n.csv": "https://lter.kbs.msu.edu/datatables/102.csv",
}
OUT = os.path.join(REPO_ROOT, "data", "processed", "temporal_variance.json")

#: Sampling depth and support, per Wuest experiment, taken from the dataset
#: description rather than assumed. THIS IS THE FACT THAT REPLACES THE 0-30 cm
#: ASSUMPTION on VC-TMP-001/002: only one of the five series is 0-30 cm.
#:
#: ``cores`` is the number of cores composited into the single value analysed
#: for a plot on an occasion. It matters because within-plot spatial variance
#: enters the residual divided by it - which is the one handle this design gives
#: on how much of the residual is spatial rather than temporal.
WUEST_SUPPORT = {
    "AW": dict(
        site="Adams, OR (Columbia Plateau CRC) - 'Adams-tillage'",
        depth="0-30 cm, six 5-cm increments", depth_top=0.0, depth_bottom=30.0,
        basis="fixed_depth", cores=3, core_mm=50,
        relocation="each month 30 cm further down the crop row",
        treatments="no-till / residue incorporated / residue replaced, annual winter wheat",
    ),
    "CP": dict(
        site="Adams, OR - 'Adams-residue' (chaff plots)",
        depth="top 250 kg/m2 equivalent soil mass (about 20 cm)",
        depth_top=0.0, depth_bottom=20.0, basis="equivalent_soil_mass",
        cores=3, core_mm=25,
        relocation="within 30 cm of the previous month's sample",
        treatments="no residue removed / chaff removed / chaff+straw removed",
    ),
    "Echo": dict(
        site="Echo, OR", depth="top 250 kg/m2 equivalent soil mass (about 20 cm)",
        depth_top=0.0, depth_bottom=20.0, basis="equivalent_soil_mass",
        cores=1, core_mm=25,
        relocation="within a few metres of the same location each month",
        treatments="till vs no-till winter wheat-fallow, both rotation phases",
    ),
    "Moro": dict(
        site="Moro, OR", depth="top 250 kg/m2 equivalent soil mass (about 20 cm)",
        depth_top=0.0, depth_bottom=20.0, basis="equivalent_soil_mass",
        cores=1, core_mm=25,
        relocation="within a few metres of the same location each month",
        treatments="no-till vs minimum-till winter wheat-fallow, both phases",
    ),
    "Ritz": dict(
        site="Ritzville, WA", depth="top 250 kg/m2 equivalent soil mass (about 20 cm)",
        depth_top=0.0, depth_bottom=20.0, basis="equivalent_soil_mass",
        cores=1, core_mm=25,
        relocation="within a few metres of the same location each month",
        treatments="two 3-year rotations, no-till vs conservation tillage",
    ),
}

#: Verbatim from the dataset's own "Use limitations" field. Quoted, not
#: paraphrased, because it is the provider's stated scope and not our inference.
WUEST_USE_LIMITATION = (
    "Soils were silt loams and the climate was semi-arid Mediterranean pattern "
    "at all four sites tested. Other soils and climates may produce more or "
    "less temporal variability."
)

KBS_TERMS = (
    "These Data are copyrighted and use in a publication requires written "
    "permission as detailed in our Terms of use: "
    "https://lter.kbs.msu.edu/data/terms-of-use/"
)


# ---------------------------------------------------------------------------
# fetching
# ---------------------------------------------------------------------------


def fetch() -> None:
    for directory, files in ((WUEST_DIR, WUEST_FILES), (KBS_DIR, KBS_FILES)):
        os.makedirs(directory, exist_ok=True)
        for name, url in files.items():
            dest = os.path.join(directory, name)
            print(f"  fetching {name} ...", end=" ", flush=True)
            with urllib.request.urlopen(url, timeout=180) as r, open(dest, "wb") as f:
                f.write(r.read())
            print(f"{os.path.getsize(dest)} bytes")


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------


def load_wuest() -> pd.DataFrame:
    """One row per plot per monthly campaign. SOC is a stock in g C/m2.

    ``SampleNo`` is the campaign, not ``Date``: four Adams campaigns ran over
    two consecutive days, and using the raw date would split those months into
    two half-occasions and manufacture an occasion effect out of nothing.

    The SOC column is renamed off ``C`` because patsy reads ``C(...)`` in a
    formula as its categorical-coding function, not as a column.
    """
    path = os.path.join(WUEST_DIR, "SOC_variability.csv")
    d = pd.read_csv(path, parse_dates=["Date", "Weatherdate"]).rename(
        columns={"C": "soc"})
    d = d.drop(columns=[c for c in ("OrN", "minN") if c in d.columns])
    d["occ"] = d.SampleNo.astype(int).astype(str)
    d["eu"] = d.Expt.astype(str) + "-" + d.Plot.astype(str)
    d["trt"] = d.Trt1.astype(str)          # constant within plot; Trt2 is not
    d["log_c"] = np.log(d.soc.where(d.soc > 0))
    return d.dropna(subset=["log_c"])


def load_kbs() -> pd.DataFrame:
    """KBS LTER table 102, 0-25 cm only - the one depth with a repeated panel.

    SOC is a CONCENTRATION (g C per 100 g soil), not a stock. It is never
    compared with the Wuest stocks on an absolute scale, only as a CV.
    """
    path = os.path.join(KBS_DIR, "kbs102_soil_total_c_n.csv")
    d = pd.read_csv(path, comment="#")
    d["soc"] = pd.to_numeric(d["C"], errors="coerce")
    d = d.drop(columns=[c for c in ("C", "N", "CN_Ratio") if c in d.columns])
    d["Sample_Date"] = pd.to_datetime(d.Sample_Date, errors="coerce")
    d["Depth"] = d.Depth.astype(str).str.strip()
    d = d[(d.Depth == "0-25") & (d.soc > 0)].dropna(subset=["Sample_Date"])
    d["eu"] = (d.Plot.astype(str) + "-" + d.Rep.astype(str)
                 + "-" + d.Cover.astype(str))
    d["occ"] = d.Sample_Date.dt.strftime("%Y-%m-%d")
    d["trt"] = d.Mgmnt.astype(str) + "|" + d.Cover.astype(str)
    d["Expt"] = "KBS-LFL"
    d["log_c"] = np.log(d.soc)
    return d


# ---------------------------------------------------------------------------
# the estimator
# ---------------------------------------------------------------------------


def cv_pct(v: float) -> float:
    """Log-scale variance -> CV in percent. Same convention as D-029."""
    return float(100.0 * np.sqrt(np.expm1(max(v, 0.0))))


def anova_components(g: pd.DataFrame) -> dict | None:
    """Closed-form moment estimates, balanced two-way crossed, 1 obs per cell.

    Holes are removed by dropping whole EUs or whole occasions, whichever keeps
    more cells - dropping columns first would have cost every occasion at KBS,
    where five EUs of 142 are short a visit, while at Ritzville it is one
    occasion that is short an EU.
    """
    g = g.copy()
    g["y"] = g.log_c - g.groupby("trt").log_c.transform("mean")
    tab = g.pivot_table(index="eu", columns="occ", values="y")

    def _cols_first(t):
        t = t.loc[:, ~t.isna().any(axis=0)]
        return t.dropna(axis=0, how="any")

    def _rows_first(t):
        t = t.dropna(axis=0, how="any")
        return t.loc[:, ~t.isna().any(axis=0)]

    tab = max((_cols_first(tab), _rows_first(tab)), key=lambda t: t.size)
    p, q = tab.shape
    n_trt = g.trt.nunique()
    if p - n_trt < 2 or q < 3:
        return None
    a = tab.to_numpy(dtype=float)
    grand = a.mean()
    rm, cm = a.mean(axis=1), a.mean(axis=0)
    ms_p = (q * ((rm - grand) ** 2).sum()) / (p - n_trt)
    ms_o = (p * ((cm - grand) ** 2).sum()) / (q - 1)
    resid = a - rm[:, None] - cm[None, :] + grand
    ms_e = (resid ** 2).sum() / ((p - n_trt) * (q - 1))
    return {
        "v_plot": max((ms_p - ms_e) / q, 0.0),
        "v_occ": max((ms_o - ms_e) / p, 0.0),
        "v_resid": float(ms_e),
        "n_plots": int(p), "n_occasions": int(q), "n_obs": int(p * q),
    }


def reml_components(g: pd.DataFrame) -> dict | None:
    """REML crossed random effects. Cross-check on :func:`anova_components`."""
    import statsmodels.formula.api as smf

    warnings.simplefilter("ignore")
    g = g.copy()
    g["_grp"] = 1
    try:
        res = smf.mixedlm(
            "log_c ~ C(trt)", data=g, groups=g["_grp"],
            vc_formula={"eu": "0 + C(eu)", "occ": "0 + C(occ)"},
        ).fit(reml=True, method="lbfgs")
    except Exception:
        return None
    if not res.converged:
        return None
    # vcomp comes back in SORTED key order: ('occ', 'plot'). Do not index by
    # the order the dict was written in - see the module docstring.
    order = sorted(["eu", "occ"])
    v = dict(zip(order, (float(x) for x in res.vcomp)))
    return {"v_plot": v["eu"], "v_occ": v["occ"], "v_resid": float(res.scale)}


def bootstrap_occasions(g: pd.DataFrame, n_boot: int, seed: int = 20260810) -> dict:
    """Block bootstrap over OCCASIONS - the independent unit along time.

    Plots are fixed by design and resampling them would answer a different
    question. Uses the moment estimator, which is exact for this design and
    costs nothing to refit.
    """
    rng = np.random.default_rng(seed)
    occ = g.occ.unique()
    keep = {"v_occ": [], "v_resid": [], "v_time_total": [], "v_plot": []}
    for _ in range(n_boot):
        pick = rng.choice(occ, size=len(occ), replace=True)
        parts = []
        for k, o in enumerate(pick):
            chunk = g[g.occ == o].copy()
            chunk["occ"] = f"{o}__b{k}"
            parts.append(chunk)
        a = anova_components(pd.concat(parts, ignore_index=True))
        if a is None:
            continue
        keep["v_occ"].append(a["v_occ"])
        keep["v_resid"].append(a["v_resid"])
        keep["v_plot"].append(a["v_plot"])
        keep["v_time_total"].append(a["v_occ"] + a["v_resid"])
    out = {}
    for k, vals in keep.items():
        if len(vals) < max(20, n_boot // 10):
            out[k] = None
            continue
        arr = np.array([cv_pct(v) for v in vals])
        out[k] = {
            "ci95_low": round(float(np.percentile(arr, 2.5)), 3),
            "ci95_high": round(float(np.percentile(arr, 97.5)), 3),
            "n_successful": int(len(arr)),
        }
    return out


def decompose(g: pd.DataFrame, n_boot: int) -> dict | None:
    a = anova_components(g)
    if a is None:
        return None
    r = reml_components(g)
    total = a["v_plot"] + a["v_occ"] + a["v_resid"]
    out = {
        "n_obs": int(len(g)), "n_plots": a["n_plots"],
        "n_occasions": a["n_occasions"], "n_treatments": int(g.trt.nunique()),
        "balanced_cells": a["n_obs"],
        "mean_soc": round(float(g.soc.mean()), 3),
        "cv_between_plot_pct": round(cv_pct(a["v_plot"]), 3),
        "cv_occasion_pct": round(cv_pct(a["v_occ"]), 3),
        "cv_residual_pct": round(cv_pct(a["v_resid"]), 3),
        "cv_time_total_pct": round(cv_pct(a["v_occ"] + a["v_resid"]), 3),
        "share_between_plot_pct": round(100 * a["v_plot"] / total, 1),
        "share_occasion_pct": round(100 * a["v_occ"] / total, 1),
        "share_residual_pct": round(100 * a["v_resid"] / total, 1),
        "log_variances": {k: round(a[k], 8) for k in
                          ("v_plot", "v_occ", "v_resid")},
    }
    if r is not None:
        out["reml_check_cv_pct"] = {
            "between_plot": round(cv_pct(r["v_plot"]), 3),
            "occasion": round(cv_pct(r["v_occ"]), 3),
            "residual": round(cv_pct(r["v_resid"]), 3),
        }
        out["reml_max_abs_diff_pct_points"] = round(max(
            abs(cv_pct(r["v_plot"]) - cv_pct(a["v_plot"])),
            abs(cv_pct(r["v_occ"]) - cv_pct(a["v_occ"])),
            abs(cv_pct(r["v_resid"]) - cv_pct(a["v_resid"])),
        ), 4)
    out["bootstrap"] = bootstrap_occasions(g, n_boot)
    return out


# ---------------------------------------------------------------------------
# what a repeat visit actually sees
# ---------------------------------------------------------------------------


def revisit(g: pd.DataFrame, date_col: str = "Date") -> dict:
    """SD of the log difference between two visits to the SAME plot.

    This is the quantity an MDC calculation needs, with the plot effect already
    cancelled by the pairing. Split by whether the two visits fall in the same
    calendar month, which is the standard advice for beating seasonality: if
    anniversary sampling works, the same-month column has to be smaller.
    """
    recs = []
    for _, gp in g.groupby("eu"):
        gp = gp.sort_values(date_col)
        v = gp.log_c.to_numpy()
        dt = gp[date_col].to_numpy()
        mo = gp[date_col].dt.month.to_numpy()
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                lag = (dt[j] - dt[i]).astype("timedelta64[D]").astype(int) / 30.44
                recs.append((lag, v[j] - v[i], bool(mo[i] == mo[j])))
    r = pd.DataFrame(recs, columns=["lag", "diff", "same_month"])

    def sd(sel, min_n=30):
        s = r[sel]
        return (round(float(100 * s["diff"].std(ddof=1)), 3)
                if len(s) >= min_n else None)

    ann = (r.lag >= 10) & (r.lag <= 14)
    return {
        "n_pairs": int(len(r)),
        "sd_pct_lag_3_5_months": sd((r.lag >= 3) & (r.lag <= 5)),
        "sd_pct_lag_10_14_months": sd(ann),
        "sd_pct_lag_10_14_same_calendar_month": sd(ann & r.same_month),
        "sd_pct_lag_10_14_different_month": sd(ann & ~r.same_month),
        "n_same_month_pairs": int((ann & r.same_month).sum()),
    }


# ---------------------------------------------------------------------------
# covariate dependence - the Phase 3 question
# ---------------------------------------------------------------------------


def covariate_dependence(d: pd.DataFrame, per_site: dict) -> dict:
    """Does temporal variability track anything a spatial MDC surface would use?

    Asked at two levels because they answer different questions:

    * BETWEEN sites - does a site's temporal CV track its SOC level? Five sites,
      so this is a look, not a test.
    * WITHIN a site - does a plot's own temporal deviation track its treatment,
      its rotation phase, or its SOC level? Here the occasion effect is common
      to every plot and cancels, so what is being tested is the residual term.
    """
    from scipy import stats

    sites = sorted(per_site)
    soc = np.array([per_site[s]["mean_soc"] for s in sites])
    cvt = np.array([per_site[s]["cv_time_total_pct"] for s in sites])
    rho, p = stats.spearmanr(soc, cvt)
    out = {
        "between_sites": {
            "sites": sites,
            "mean_soc": [round(float(x), 1) for x in soc],
            "cv_time_total_pct": [round(float(x), 2) for x in cvt],
            "spearman_rho": round(float(rho), 3), "p": round(float(p), 4),
            "n": len(sites),
        },
        "within_site": {},
    }

    for expt, g in d.groupby("Expt"):
        g = g.copy()
        # residual = observation minus its plot mean minus its occasion mean.
        g["r"] = (g.log_c
                  - g.groupby("eu").log_c.transform("mean")
                  - g.groupby("occ").log_c.transform("mean")
                  + g.log_c.mean())
        per_eu = g.groupby("eu").agg(
            sd=("r", lambda x: x.std(ddof=1)), soc=("soc", "mean"),
            trt=("trt", "first"))
        rec = {"n_plots": int(len(per_eu))}
        rho, p = stats.spearmanr(per_eu.soc, per_eu.sd)
        rec["soc_level"] = {"spearman_rho": round(float(rho), 3),
                            "p": round(float(p), 4)}
        groups = [x.to_numpy() for _, x in per_eu.groupby("trt").sd if len(x) > 1]
        if len(groups) > 1:
            f, p = stats.f_oneway(*groups)
            rec["treatment"] = {"levels": int(len(groups)),
                                "F": round(float(f), 3), "p": round(float(p), 4)}
        if "wfsam" in g.columns and g.wfsam.nunique() > 1:
            # rotation phase is a WITHIN-plot, time-varying covariate: the same
            # plot is in wheat some months and fallow others.
            by = {k: float(v.std(ddof=1)) for k, v in g.groupby("wfsam").r if len(v) > 5}
            if len(by) > 1:
                rec["rotation_phase_residual_sd_pct"] = {
                    k: round(100 * v, 3) for k, v in by.items()}
        out["within_site"][expt] = rec
    return out


def compositing_contrast(per_site: dict) -> dict:
    """How much of the residual is within-plot spatial rather than temporal?

    Two Adams series composite THREE cores into the value analysed; the three
    Till/No-till series analyse ONE. Within-plot spatial variance enters the
    residual divided by the number of cores; genuine plot-specific temporal
    movement and analytical error do not. So if the residual were pure
    within-plot spatial noise, the single-core sites would sit a factor of
    sqrt(3) = 1.732 above the three-core sites in CV.

    This is confounded with site - the three-core sites are also the two wetter,
    higher-carbon ones - so it bounds rather than identifies. It is reported
    because it is the only handle the design offers on a term the design cannot
    otherwise split.
    """
    three = [s for s in per_site if WUEST_SUPPORT.get(s, {}).get("cores") == 3]
    one = [s for s in per_site if WUEST_SUPPORT.get(s, {}).get("cores") == 1]
    if not three or not one:
        return {}
    m3 = float(np.mean([per_site[s]["cv_residual_pct"] for s in three]))
    m1 = float(np.mean([per_site[s]["cv_residual_pct"] for s in one]))
    # v_resid = v_within/k + v_other  =>  solve the two-site-group means for
    # v_within, in log-variance units.
    v3 = float(np.mean([per_site[s]["log_variances"]["v_resid"] for s in three]))
    v1 = float(np.mean([per_site[s]["log_variances"]["v_resid"] for s in one]))
    v_within = max((v1 - v3) / (1 - 1 / 3), 0.0)
    v_other = v1 - v_within
    # The observed ratio slightly EXCEEDS sqrt(3), so the naive solve wants a
    # negative remainder and clips at zero. Report that rather than hide it: a
    # boundary solution says the data are consistent with the residual being
    # essentially all within-plot spatial, and says nothing more precise.
    at_boundary = v_other <= 0
    return {
        "three_core_sites": three, "one_core_sites": one,
        "mean_residual_cv_3_core_pct": round(m3, 3),
        "mean_residual_cv_1_core_pct": round(m1, 3),
        "observed_ratio": round(m1 / m3, 3),
        "ratio_if_residual_were_all_within_plot_spatial": round(float(np.sqrt(3)), 3),
        "implied_within_plot_spatial_cv_pct": round(cv_pct(v_within), 3),
        "implied_other_cv_pct": round(cv_pct(max(v_other, 0.0)), 3),
        "solution_at_boundary": bool(at_boundary),
        "reading": (
            "the observed ratio is at or just above sqrt(3), so the moment "
            "solve leaves nothing for analytical error or plot-specific timing "
            "and clips at zero. Read as: the residual is DOMINATED by "
            "within-plot spatial variance, therefore the combined temporal "
            "number overstates temporal variance and the separable one is much "
            "the closer of the two bounds."
        ),
        "caveat": (
            "confounded with site: the three-core series are also the two "
            "highest-carbon, deepest-sampled ones. Two sites against three. "
            "Bounds the split, does not identify it."
        ),
    }


# ---------------------------------------------------------------------------


#: Wuest & Durfee's own published variance shares, from the abstract. The one
#: thing in this file taken from prose rather than derived - it is the thing
#: being checked AGAINST, so it has to come from them.
PUBLISHED_SHARES = {
    "temporal": {"mean": 20.0, "low": 15.0, "high": 32.0},
    "between_eu": {"mean": 17.0, "low": 2.0, "high": 42.0},
}


def specification_sweep(d: pd.DataFrame) -> dict:
    """Do the published shares reproduce, or did one model choice get lucky?

    Four specifications, declared before looking at any of their answers, that
    differ in which plot-level fixed effects are absorbed before the variance
    components are taken. Reporting the spread is the check; picking the
    closest-matching one would be reverse-engineering the answer.

    Specification B is expected to be UNESTIMABLE and is included for exactly
    that reason: in a randomized complete block with one plot per
    treatment-block cell, treatment and block jointly identify the plot, so
    absorbing both leaves no degrees of freedom for a plot term. That is a
    property of the design, not a bug, and it is why specification A - which
    absorbs treatment alone, making the plot term "between replicate
    experimental units" - is the one that matches the published wording.
    """
    specs = {
        "A_treatment_only": ["trt"],
        "B_treatment_and_block": ["trt", "Block"],
        "C_block_only": ["Block"],
        "D_no_fixed_effects": None,
    }
    out = {}
    for name, absorb in specs.items():
        occ_sh, plot_sh = [], []
        for _, g in d.groupby("Expt"):
            g = g.copy()
            # Count the absorbed levels BEFORE residualising - they are the
            # degrees of freedom the plot mean square loses. Computing this
            # after the fact (when the absorbed column has been collapsed) is
            # the obvious mistake, and it silently makes specification B look
            # estimable on 4 df instead of correctly reporting 0.
            n_abs = g.groupby(absorb).ngroups if absorb else 1
            if absorb:
                g["log_c"] = g.log_c - g.groupby(absorb).log_c.transform("mean")
            tab = g.pivot_table(index="eu", columns="occ", values="log_c")
            tab = tab.loc[:, ~tab.isna().any(axis=0)].dropna(axis=0, how="any")
            p, q = tab.shape
            if p - n_abs < 2:
                occ_sh = plot_sh = None
                break
            a = tab.to_numpy(float)
            grand, rm, cm = a.mean(), a.mean(axis=1), a.mean(axis=0)
            ms_p = q * ((rm - grand) ** 2).sum() / (p - n_abs)
            ms_o = p * ((cm - grand) ** 2).sum() / (q - 1)
            res = a - rm[:, None] - cm[None, :] + grand
            ms_e = (res ** 2).sum() / ((p - n_abs) * (q - 1))
            vp, vo = max((ms_p - ms_e) / q, 0), max((ms_o - ms_e) / p, 0)
            tot = vp + vo + ms_e
            occ_sh.append(100 * vo / tot)
            plot_sh.append(100 * vp / tot)
        if occ_sh is None:
            out[name] = {"estimable": False, "why": (
                "treatment and block jointly identify the plot in this RCB, "
                "leaving no degrees of freedom for a plot term")}
            continue
        out[name] = {
            "estimable": True,
            "temporal_share_pct": {
                "mean": round(float(np.mean(occ_sh)), 1),
                "min": round(float(min(occ_sh)), 1),
                "max": round(float(max(occ_sh)), 1)},
            "between_eu_share_pct": {
                "mean": round(float(np.mean(plot_sh)), 1),
                "min": round(float(min(plot_sh)), 1),
                "max": round(float(max(plot_sh)), 1)},
        }
    out["published"] = PUBLISHED_SHARES
    return out


def g1_cross_validation(d: pd.DataFrame) -> dict:
    """Run the G1 code path on this data and compare with the crossed model.

    ``derive_g1_napeshm.residual_var`` is nested REML on a CROSS-SECTION, one
    measurement per experimental unit. ``decompose`` above is crossed moments on
    a PANEL. Different structure, different code, written weeks apart.

    A Wuest series with OCCASION playing the role of site is a NAPESHM-shaped
    input, and the G1 residual then estimates between-EU-within-treatment
    variance pooled over occasions - which is ``v_plot + v_resid`` from the
    crossed model, the same quantity by construction. If the two agree, the
    implementation behind VC-BPS-005/006 is checked against something that did
    not produce it.
    """
    sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
    import derive_g1_napeshm as g1

    rows, diffs = {}, []
    for e, g in d.groupby("Expt"):
        a = anova_components(g)
        if a is None:
            continue
        crossed = cv_pct(a["v_plot"] + a["v_resid"])
        cs = g.copy()
        cs["siteid"] = cs.occ.astype(str)
        cs["treatmentid"] = cs.occ.astype(str) + "|" + cs.trt.astype(str)
        v = g1.residual_var(cs, "log_c")
        if v is None:
            continue
        got = g1.cv_from_logvar(v)
        diffs.append(got - crossed)
        rows[e] = {"g1_code_path_cv_pct": round(got, 3),
                   "crossed_model_cv_pct": round(crossed, 3),
                   "difference": round(got - crossed, 3)}
    return {
        "per_series": rows,
        "mean_abs_difference_cv_points": round(float(np.mean(np.abs(diffs))), 3),
        "all_same_sign": bool(len(set(np.sign(diffs))) == 1),
        "reads": (
            "validates the estimator core and the G1 code path. Does NOT "
            "validate the NAPESHM filter cascade (D-024/025/026/028) or the "
            "cluster bootstrap over sites, neither of which this exercises."
        ),
    }


#: Mean annual precipitation, from the dataset description's own site
#: paragraphs. Provider-stated, not our inference and not a supplied guess -
#: which is the whole reason D-021 could not be closed before.
WUEST_MAP_MM = {"AW": 401, "CP": 401, "Echo": 265, "Moro": 269, "Ritz": 296}


def d021_scope(d: pd.DataFrame) -> dict:
    """Run the committed IPCC classifier on the four Wuest sites.

    D-021 asked whether Pacific Northwest dryland cropping is inside the
    project's temperate scope. It stayed open through D-034 because the climate
    inputs had been SUPPLIED by hand rather than sourced - a classification is
    only worth as much as its inputs.

    Both inputs are now sourced from the dataset itself: MAP from the provider's
    site paragraphs, and MAT from the dataset's own ``avgT`` column, averaged
    over calendar months so that the missing winter samplings do not bias it
    warm. This is a study-period average from the study's own weather stations,
    not a published 30-year normal, and it is labelled as such.

    Partial classification per D-028: the moisture axis needs MAP:PET, which is
    no more available here than it was for NAPESHM, so it is left undetermined
    rather than invented. The temperature axis is what D-021 actually asks
    about.
    """
    sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
    from loam.ipcc_climate import classify_partial

    d = d.copy()
    d["m"] = d.Weatherdate.dt.month
    monthly = d.groupby(["Expt", "m"]).avgT.mean().unstack()
    out = {}
    for expt in sorted(WUEST_MAP_MM):
        if expt not in monthly.index:
            continue
        months = monthly.loc[expt].dropna()
        mat = float(months.mean())
        region, blocker = classify_partial(mat, float(WUEST_MAP_MM[expt]))
        out[expt] = {
            "mat_c_study_period": round(mat, 2),
            "calendar_months_covered": int(len(months)),
            "map_mm_provider_stated": WUEST_MAP_MM[expt],
            "ipcc_region": region,
            "blocking_variable": blocker,
            "temperature_regime": ("Warm Temperate" if mat > 10 else
                                   "Cool Temperate"),
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true",
                    help="download both raw sources before deriving")
    ap.add_argument("--bootstrap", type=int, default=500)
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    if args.fetch:
        print("fetching raw sources")
        fetch()

    missing = [p for p in (os.path.join(WUEST_DIR, "SOC_variability.csv"),
                           os.path.join(KBS_DIR, "kbs102_soil_total_c_n.csv"))
               if not os.path.exists(p)]
    if missing:
        print("missing raw data (run with --fetch):", *missing, sep="\n  ")
        return 1

    result: dict = {
        "estimator": (
            "crossed random effects, plot x occasion, treatment fixed, log "
            "scale; balanced two-way ANOVA moment estimates cross-checked "
            "against REML; block bootstrap over occasions"
        ),
        "cv_convention": "CV = 100*sqrt(exp(sigma^2)-1), same as D-029",
    }

    # ---------------- Wuest, primary --------------------------------------
    w = load_wuest()
    print(f"\nWUEST 2024  n={len(w)} plot-months, {w.Expt.nunique()} series, "
          f"{w.eu.nunique()} plots")
    print("  NOTE the depth is NOT uniform across the five series:")
    for e in sorted(WUEST_SUPPORT):
        s = WUEST_SUPPORT[e]
        print(f"    {e:5} {s['depth']:52} {s['cores']} core(s)")

    per_site: dict = {}
    print(f"\n  {'series':6}{'betw-plot':>11}{'occasion':>10}{'residual':>10}"
          f"{'TIME TOTAL':>12}   shares plot/occ/resid")
    for e, g in w.groupby("Expt"):
        r = decompose(g, args.bootstrap)
        if r is None:
            continue
        r.update({k: v for k, v in WUEST_SUPPORT[e].items()})
        r["revisit"] = revisit(g)
        per_site[e] = r
        b = r["bootstrap"].get("v_time_total") or {}
        ci = (f"[{b['ci95_low']:.1f}, {b['ci95_high']:.1f}]"
              if b else "[--]")
        print(f"  {e:6}{r['cv_between_plot_pct']:10.2f}%{r['cv_occasion_pct']:9.2f}%"
              f"{r['cv_residual_pct']:9.2f}%{r['cv_time_total_pct']:11.2f}% {ci:>14}"
              f"   {r['share_between_plot_pct']:4.1f}/{r['share_occasion_pct']:4.1f}/"
              f"{r['share_residual_pct']:4.1f}")

    occ = [per_site[s]["cv_occasion_pct"] for s in per_site]
    tot = [per_site[s]["cv_time_total_pct"] for s in per_site]
    shares_occ = [per_site[s]["share_occasion_pct"] for s in per_site]
    shares_plot = [per_site[s]["share_between_plot_pct"] for s in per_site]
    summary = {
        "separable_temporal_cv_pct": {
            "mean": round(float(np.mean(occ)), 3),
            "min": round(float(min(occ)), 3), "max": round(float(max(occ)), 3)},
        "combined_temporal_cv_pct": {
            "mean": round(float(np.mean(tot)), 3),
            "min": round(float(min(tot)), 3), "max": round(float(max(tot)), 3)},
        "share_occasion_pct": {
            "mean": round(float(np.mean(shares_occ)), 1),
            "min": round(float(min(shares_occ)), 1),
            "max": round(float(max(shares_occ)), 1)},
        "share_between_plot_pct": {
            "mean": round(float(np.mean(shares_plot)), 1),
            "min": round(float(min(shares_plot)), 1),
            "max": round(float(max(shares_plot)), 1)},
    }
    print(f"\n  SEPARABLE temporal (occasion only): mean {summary['separable_temporal_cv_pct']['mean']}% "
          f"range {summary['separable_temporal_cv_pct']['min']}-{summary['separable_temporal_cv_pct']['max']}%")
    print(f"  COMBINED  temporal (occ+residual):  mean {summary['combined_temporal_cv_pct']['mean']}% "
          f"range {summary['combined_temporal_cv_pct']['min']}-{summary['combined_temporal_cv_pct']['max']}%")
    print(f"\n  published-abstract check - our variance SHARES vs Wuest's reported:")
    print(f"    temporal          ours mean {summary['share_occasion_pct']['mean']}% "
          f"({summary['share_occasion_pct']['min']}-{summary['share_occasion_pct']['max']})"
          f"   published 20% (15-32)")
    print(f"    between-replicate ours mean {summary['share_between_plot_pct']['mean']}% "
          f"({summary['share_between_plot_pct']['min']}-{summary['share_between_plot_pct']['max']})"
          f"   published 17% (2-42)")

    print("\n  repeat visit to the same plot - SD of the log difference:")
    print(f"    {'series':6}{'3-5 mo':>9}{'10-14 mo':>10}{'same month':>12}{'other month':>13}")
    for e in per_site:
        r = per_site[e]["revisit"]
        f = lambda k: f"{r[k]:.2f}%" if r[k] is not None else "  --"
        print(f"    {e:6}{f('sd_pct_lag_3_5_months'):>9}"
              f"{f('sd_pct_lag_10_14_months'):>10}"
              f"{f('sd_pct_lag_10_14_same_calendar_month'):>12}"
              f"{f('sd_pct_lag_10_14_different_month'):>13}")

    comp = compositing_contrast(per_site)
    if comp:
        print(f"\n  compositing contrast: residual CV {comp['mean_residual_cv_1_core_pct']}% "
              f"at 1-core sites vs {comp['mean_residual_cv_3_core_pct']}% at 3-core, "
              f"ratio {comp['observed_ratio']} (sqrt(3)={comp['ratio_if_residual_were_all_within_plot_spatial']} "
              f"if the residual were all within-plot spatial)")

    cov = covariate_dependence(w, per_site)
    bs = cov["between_sites"]
    print(f"\n  covariate dependence, between sites: SOC level vs temporal CV "
          f"rho={bs['spearman_rho']:+.3f} p={bs['p']:.3f} (n={bs['n']})")
    for e, rec in cov["within_site"].items():
        line = (f"    {e:6} soc rho={rec['soc_level']['spearman_rho']:+.3f} "
                f"p={rec['soc_level']['p']:.3f}")
        if "treatment" in rec:
            line += f" | trt F={rec['treatment']['F']:.2f} p={rec['treatment']['p']:.3f}"
        if "rotation_phase_residual_sd_pct" in rec:
            ph = rec["rotation_phase_residual_sd_pct"]
            line += " | phase " + " ".join(f"{k}={v:.2f}%" for k, v in sorted(ph.items()))
        print(line)

    print("\n  D-050 PIPELINE VALIDATION - does our derivation reproduce the "
          "published statistic?")
    sweep = specification_sweep(w)
    print(f"    {'specification':24}{'temporal share':>26}{'between-EU share':>26}")
    for name, s in sweep.items():
        if name == "published":
            continue
        if not s["estimable"]:
            print(f"    {name:24}{'NOT ESTIMABLE - ' + s['why'][:40]:>26}")
            continue
        t, b = s["temporal_share_pct"], s["between_eu_share_pct"]
        print(f"    {name:24}{t['mean']:15.1f}% ({t['min']:4.1f}-{t['max']:4.1f})"
              f"{b['mean']:15.1f}% ({b['min']:4.1f}-{b['max']:4.1f})")
    p = PUBLISHED_SHARES
    print(f"    {'PUBLISHED (abstract)':24}"
          f"{p['temporal']['mean']:15.1f}% ({p['temporal']['low']:4.1f}-{p['temporal']['high']:4.1f})"
          f"{p['between_eu']['mean']:15.1f}% ({p['between_eu']['low']:4.1f}-{p['between_eu']['high']:4.1f})")

    xval = g1_cross_validation(w)
    print("\n  G1 code path vs an independently written implementation:")
    for e, x in xval["per_series"].items():
        print(f"    {e:6}{x['g1_code_path_cv_pct']:8.2f}%  vs "
              f"{x['crossed_model_cv_pct']:6.2f}%   {x['difference']:+.2f}")
    print(f"    mean absolute difference {xval['mean_abs_difference_cv_points']} "
          f"CV points, all same sign: {xval['all_same_sign']}")

    scope = d021_scope(w)
    print("\n  D-021 scope check - IPCC partial classification of the four sites:")
    for e, s in scope.items():
        print(f"    {e:5} MAT {s['mat_c_study_period']:5.2f} C "
              f"({s['calendar_months_covered']} months) MAP {s['map_mm_provider_stated']:3} mm "
              f"-> {s['temperature_regime']:14} "
              f"[full tree: {s['ipcc_region']}, blocked on {s['blocking_variable']}]")
    print("    every site is Temperate on the temperature axis, warm or cool")

    result["wuest"] = {
        "d050_specification_sweep": sweep,
        "d050_g1_cross_validation": xval,
        "d021_scope_check": scope,
        "doi_data": "10.15482/USDA.ADC/25719348.v1",
        "doi_paper": "10.1002/saj2.20660",
        "licence": "U.S. Public Domain",
        "use_limitation_verbatim": WUEST_USE_LIMITATION,
        "n_obs": int(len(w)),
        "per_series": per_site,
        "summary": summary,
        "compositing_contrast": comp,
        "covariate_dependence": cov,
    }

    # ---------------- KBS, corroboration ----------------------------------
    k = load_kbs()
    kr = decompose(k, args.bootstrap)
    print(f"\nKBS LTER table 102, 0-25 cm  n={len(k)} obs, {k.eu.nunique()} EUs, "
          f"{k.occ.nunique()} occasions, {k.Year.nunique()} years")
    print(f"  between-plot {kr['cv_between_plot_pct']:.2f}%  occasion "
          f"{kr['cv_occasion_pct']:.2f}%  residual {kr['cv_residual_pct']:.2f}%  "
          f"TIME TOTAL {kr['cv_time_total_pct']:.2f}%")

    # The occasion means move by more than SOC can physically move in a year,
    # so the annual series is not usable as a temporal estimate on its own.
    occ_means = k.groupby("occ").log_c.mean()
    swing = float(100 * (occ_means.max() - occ_means.min()))
    print(f"  field-wide occasion means swing {swing:.1f}% across 5 years - "
          f"larger than real SOC change can be, so the between-year term is "
          f"read as method drift, not signal")

    pair = k[k.Year == 2000].pivot_table(index="eu", columns="occ",
                                         values="log_c").dropna()
    within_season = None
    if {"2000-05-03", "2000-06-27"} <= set(pair.columns):
        dif = pair["2000-06-27"] - pair["2000-05-03"]
        within_season = {
            "window": "2000-05-03 to 2000-06-27 (8 weeks)",
            "n_eus": int(len(pair)),
            "mean_shift_pct": round(float(100 * dif.mean()), 3),
            "sd_paired_log_diff_pct": round(float(100 * dif.std(ddof=1)), 3),
            "implied_per_visit_cv_pct": round(
                float(100 * dif.std(ddof=1) / np.sqrt(2)), 3),
        }
        print(f"  clean within-season pair {within_season['window']}, "
              f"n={within_season['n_eus']} EUs: mean shift "
              f"{within_season['mean_shift_pct']:+.2f}%, SD of paired difference "
              f"{within_season['sd_paired_log_diff_pct']:.2f}% => per visit "
              f"{within_season['implied_per_visit_cv_pct']:.2f}%")

    result["kbs"] = {
        "source": "https://lter.kbs.msu.edu/datatables/102",
        "licence_note": KBS_TERMS,
        "depth_cm": [0, 25], "quantity": "concentration (g C / 100 g)",
        "decomposition": kr,
        "occasion_mean_swing_pct": round(swing, 2),
        "within_season_pair": within_season,
        "caveat": (
            "between-year occasion effects are contaminated by method drift, "
            "so only the within-season pair is used. Core relocation protocol "
            "within a plot is not documented, so the paired difference is an "
            "upper bound that includes within-plot spatial error twice."
        ),
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"\nwrote {os.path.relpath(args.out, REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
