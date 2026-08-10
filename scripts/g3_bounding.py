#!/usr/bin/env python3
"""G3: add cores, or add plots? Bound the conclusion instead of asserting it.

    python scripts/g3_bounding.py

The claim on the table
----------------------
The Wuest derivation (D-041, D-046) gives, per series, a PURE between-plot
variance ``v_plot`` and a residual ``v_resid``. The residual exceeds the
between-plot term at all five series, which reads as "the variance is inside
the plots, so add cores before adding plots".

That reading has a hole in it. ``v_resid`` is three things:

    v_resid  =  v_within   (within-plot spatial - REDUCIBLE by taking more cores)
             +  v_analytical (per assay - NOT reducible by coring)
             +  v_interaction (plot x occasion - NOT reducible by coring)

Only the first shrinks when you add cores. So write

    f = (v_analytical + v_interaction) / v_resid          the NON-REDUCIBLE share

and the question becomes: how large must ``f`` be before adding cores stops
being the better move? This script answers that per series, then jointly, and
then again under Potash et al.'s cost structure - because "better" without a
cost is not a decision.

What this script does NOT do
----------------------------
It writes no rows and settles nothing. ``f`` is not identified by this design -
one measurement per plot per occasion cannot separate within-plot spatial from
plot x occasion interaction (D-043). What CAN be done is state how much of the
residual would have to be non-reducible to overturn the conclusion, and let a
reader judge whether that is plausible.
"""

from __future__ import annotations

import json
import os

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPORAL = os.path.join(REPO_ROOT, "data", "processed", "temporal_variance.json")
OUT = os.path.join(REPO_ROOT, "data", "processed", "g3_bounding.json")

#: Potash et al. 2025 (ERL, doi:10.1088/1748-9326/ada16c), table 1(d). Their
#: cost structure is the reason to trust a cost-weighted answer over a
#: variance-only one: sampling a location and running an assay are priced
#: separately, which is exactly what makes compositing worth anything.
COST_LOCATION = 15.0   # $ to sample and process one location in a field
COST_ASSAY = 20.0      # $ to analyse one (possibly composited) sample
COST_FIELD_VISIT = 400.0  # $ to visit a field at all

#: The two candidate analytical errors from D-036, as CV percent on
#: concentration. Which one is right is an OPEN decision, and this script shows
#: that G3's answer depends on it - which is worth knowing before either is
#: settled.
ANALYTICAL_CANDIDATES = {
    "instrument_only (VC-ANA-001 as tabled)": 1.25,
    "subsampling_inclusive (Poeplau Results)": 3.13,
}


def log_var(cv_pct: float) -> float:
    """CV percent -> log-scale variance, inverse of the D-029 convention."""
    return float(np.log1p((cv_pct / 100.0) ** 2))


def cv_pct(v: float) -> float:
    return float(100.0 * np.sqrt(np.expm1(max(v, 0.0))))


def critical_f_variance_only(v_plot: float, v_resid: float) -> float:
    """Largest non-reducible share for which coring still beats adding plots.

    The naive condition is that the REDUCIBLE part of the residual still
    exceeds the between-plot term:  (1 - f) * v_resid > v_plot.
    """
    return float(max(0.0, 1.0 - v_plot / v_resid))


def optimal_composite(v_plot: float, v_resid: float, f: float) -> float:
    """Cores per assay that minimise variance for a FIXED BUDGET.

    This is the design question Potash et al. actually face, and the one our
    variance structure can speak to. Their price list separates the cost of
    sampling a location (``COST_LOCATION``) from the cost of running an assay
    (``COST_ASSAY``), which is the only reason compositing buys anything.

    With ``A`` assays of ``C`` composited cores each, budget
    ``B = A * (C * COST_LOCATION + COST_ASSAY)`` and

        V = [ v_plot + v_w/C + v_nr ] / A

    Substituting A and minimising over C gives

        C* = sqrt( (COST_ASSAY / COST_LOCATION) * v_w / (v_plot + v_nr) )

    Note what is NOT in it: the field-visit cost and the budget both cancel.
    The optimum depends only on the assay-to-location price ratio and on how
    much of the noise is reducible by compositing.
    """
    v_w = (1.0 - f) * v_resid
    v_nr = f * v_resid
    denom = v_plot + v_nr
    if denom <= 0:
        return float("inf")
    return float(np.sqrt((COST_ASSAY / COST_LOCATION) * v_w / denom))


def f_where_compositing_stops_paying(v_plot: float, v_resid: float) -> float:
    """Non-reducible share at which C* falls to 1 - i.e. do not composite at all.

    Solving ``C* = 1`` for ``f``:

        f = [ k*v_resid - v_plot ] / [ (k + 1) * v_resid ],
        k = COST_ASSAY / COST_LOCATION
    """
    k = COST_ASSAY / COST_LOCATION
    return float(max(0.0, (k * v_resid - v_plot) / ((k + 1.0) * v_resid)))


def main() -> int:
    with open(TEMPORAL, encoding="utf-8") as fh:
        series = json.load(fh)["wuest"]["per_series"]

    result: dict = {
        "question": (
            "how much of the Wuest residual must be non-reducible (analytical "
            "+ plot x occasion interaction) before adding cores stops beating "
            "adding plots?"
        ),
        "note": "analysis only; no variance-table rows are written",
        "potash_costs": {
            "location_usd": COST_LOCATION, "assay_usd": COST_ASSAY,
            "field_visit_usd": COST_FIELD_VISIT,
            "source": "Potash et al 2025 ERL table 1(d)",
        },
    }

    print("G3 - add cores or add plots? Critical non-reducible share f*\n")
    print("f = (analytical + plot x occasion) / residual. Coring wins while f < f*.\n")
    print(f"  {'series':6}{'v_plot':>10}{'v_resid':>10}{'CV_plot':>9}{'CV_res':>9}"
          f"{'f* variance':>13}{'C* at f=0':>10}{'f no-comp':>12}")

    per_series = {}
    for name, rec in series.items():
        lv = rec["log_variances"]
        vp, vr = lv["v_plot"], lv["v_resid"]
        f_var = critical_f_variance_only(vp, vr)
        c_star0 = optimal_composite(vp, vr, 0.0)
        f_nocomp = f_where_compositing_stops_paying(vp, vr)
        per_series[name] = {
            "v_plot": round(vp, 8), "v_resid": round(vr, 8),
            "cv_plot_pct": round(cv_pct(vp), 3),
            "cv_resid_pct": round(cv_pct(vr), 3),
            "n_plots": rec["n_plots"],
            "critical_f_variance_only": round(f_var, 4),
            "optimal_cores_per_assay_at_f0": round(c_star0, 2),
            "optimal_cores_per_assay_at_f0.3": round(optimal_composite(vp, vr, 0.3), 2),
            "f_at_which_compositing_stops_paying": round(f_nocomp, 4),
        }
        print(f"  {name:6}{vp:10.6f}{vr:10.6f}{cv_pct(vp):8.2f}%{cv_pct(vr):8.2f}%"
              f"{f_var:13.3f}{c_star0:10.2f}{f_nocomp:12.3f}")

    f_stars = [v["critical_f_variance_only"] for v in per_series.values()]
    binding_low, binding_high = min(f_stars), max(f_stars)
    result["per_series"] = per_series
    result["joint"] = {
        "holds_at_all_five_if_f_below": round(binding_low, 4),
        "fails_at_all_five_if_f_above": round(binding_high, 4),
        "binding_series_low": min(per_series, key=lambda k: per_series[k]["critical_f_variance_only"]),
        "binding_series_high": max(per_series, key=lambda k: per_series[k]["critical_f_variance_only"]),
    }
    print(f"\n  JOINT: 'add cores' holds at ALL FIVE only if f < {binding_low:.3f} "
          f"(binding series {result['joint']['binding_series_low']})")
    print(f"         it fails at ALL FIVE only if f > {binding_high:.3f} "
          f"(binding series {result['joint']['binding_series_high']})")
    print("         between those, the answer is series-dependent - there is no "
          "single answer")

    # --- how much of f is analytical alone? This is D-036's coupling. --------
    print("\n  ANALYTICAL ALONE as a share of the residual (D-036 is unresolved,"
          " and it MATTERS here):")
    analytical = {}
    for label, cv in ANALYTICAL_CANDIDATES.items():
        v_ana = log_var(cv)
        shares = {n: v_ana / per_series[n]["v_resid"] for n in per_series}
        analytical[label] = {
            "cv_pct": cv, "log_variance": round(v_ana, 8),
            "share_of_residual": {k: round(v, 4) for k, v in shares.items()},
            "min_share": round(min(shares.values()), 4),
            "max_share": round(max(shares.values()), 4),
        }
        line = "  ".join(f"{n} {100*s:5.1f}%" for n, s in shares.items())
        print(f"    {label:44} {line}")
    result["analytical_share_of_residual"] = analytical

    lo_share = analytical["instrument_only (VC-ANA-001 as tabled)"]["max_share"]
    hi_share = analytical["subsampling_inclusive (Poeplau Results)"]["max_share"]
    result["d036_coupling"] = {
        "max_analytical_share_instrument_only": lo_share,
        "max_analytical_share_subsampling_inclusive": hi_share,
        "exceeds_joint_threshold": bool(hi_share > binding_low),
        "reading": (
            "analytical error ALONE, before any interaction term, can exceed "
            "the joint threshold under the wider D-036 candidate. G3 therefore "
            "cannot be closed while D-036 is open."
        ),
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
