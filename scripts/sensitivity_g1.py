#!/usr/bin/env python3
"""Three sensitivity checks on the G1 rows, run before Phase 0 closes.

Exploratory. Writes NO variance-table rows and changes NO scope. Its outputs
are recorded as prose on the existing rows and in DECISIONS.md.

1. LEAVE-OUT: the 10 Mexican highland sites (MAT 15-18) that D-028's IPCC scope
   re-admitted after the retired |lat| >= 30 floor had excluded them. If
   dropping them shifts G1 by less than the CI width, the moisture-seasonality
   concern behind that floor is empirically moot FOR THIS QUANTITY and the flag
   on the rows can close. Also asks whether those same sites are the source of
   the 55 two-replicate treatments - if so, two flags are one flag.

2. COMMON SAMPLE: VC-BPS-005 (n=386) and VC-BPS-006 (n=372) sit on different EU
   sets because bd_2mm is missing for 14 EUs. The stock < concentration result
   is used as a MECHANISTIC claim about fixed-depth stock-change bias, so it
   must not rest on a cross-sample artefact. Recompute both on the intersection.

3. TEXTURE SCAN: G1 moved 0.2 points across a scope change that doubled n,
   which suggests between-plot CV may be near-invariant to climate region. Check
   whether it stratifies on texture instead. Phase 3 planning input only.

USAGE
-----
    python scripts/sensitivity_g1.py                 # 500 / 300 resamples
    python scripts/sensitivity_g1.py --bootstrap 200 # faster, wider CIs
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import warnings
from collections import Counter

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

_spec = importlib.util.spec_from_file_location(
    "g1", os.path.join(os.path.dirname(__file__), "derive_g1_napeshm.py")
)
g1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g1)


def est(d: pd.DataFrame, col: str, n_boot: int, seed: int = 20260810) -> dict:
    """Point estimate + cluster-bootstrap CI, using the headline estimator."""
    sub = g1._with_replicates(d[d[col].notna()])
    cv = g1.cv_from_logvar(g1.residual_var(sub, col))
    out = {
        "cv_pct": None if cv is None else round(cv, 3),
        "n_eus": len(sub),
        "n_treatments": int(sub.treatmentid.nunique()),
        "n_sites": int(sub.siteid.nunique()),
    }
    if cv is not None and n_boot:
        ci = g1.bootstrap_cv(sub, col, n_boot, seed=seed)
        if ci:
            out["ci95"] = [ci["ci95_low"], ci["ci95_high"]]
            out["ci_width"] = round(ci["ci95_high"] - ci["ci95_low"], 3)
            out["n_boot_ok"] = ci["n_successful"]
    return out


def fmt(e: dict) -> str:
    ci = e.get("ci95")
    band = f"[{ci[0]:5.2f}, {ci[1]:5.2f}] w={e['ci_width']:5.2f}" if ci else " (no CI)"
    return (f"CV={e['cv_pct']:6.3f}%  {band}  "
            f"n={e['n_eus']:>4} EU / {e['n_treatments']:>3} trt / {e['n_sites']:>2} sites")


def joint_covariate_model(dh: pd.DataFrame) -> dict:
    """Do texture and SOC level jointly predict between-plot variability?

    The binned scan (check 3) tests one covariate at a time, which is the wrong
    shape for this question: sand and SOC are negatively correlated, so binning
    on either one partly cancels the other's effect. A joint model separates
    them.

    Response is log(within-treatment SD of log SOC) - i.e. log CV - per
    treatment. Treatments with only 2 replicates are excluded: an SD on one
    degree of freedom carries almost no information and they are all from the
    same 8 sites, so including them would let one country drive the fit.
    """
    from scipy import stats

    d = g1._with_replicates(dh[dh.log_soc.notna()])
    g = d.groupby("treatmentid")
    tr = pd.DataFrame({
        "sd_log": g.log_soc.std(ddof=1), "mean_soc": g.b_soc.mean(),
        "clay": g.b_clay.mean(), "sand": g.b_sand.mean(),
        "n": g.size(), "country": g.country.first(),
    }).dropna()
    tr = tr[(tr.n >= 3) & (tr.sd_log > 0)]

    out = {"n_treatments": int(len(tr)),
           "by_country": {k: int(v) for k, v in tr.country.value_counts().items()},
           "spearman": {}}
    for v in ("mean_soc", "clay", "sand"):
        rho, p = stats.spearmanr(tr[v], tr.sd_log)
        out["spearman"][v] = {"rho": round(float(rho), 3), "p": round(float(p), 4)}

    X = np.column_stack([np.ones(len(tr)), np.log(tr.mean_soc.values),
                         tr.sand.values / 100])
    y = np.log(tr.sd_log.values)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = float(resid @ resid) / (len(tr) - X.shape[1])
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * s2)
    out["ols_log_cv"] = {
        name: {"beta": round(float(b), 3), "se": round(float(s), 3),
               "t": round(float(b / s), 2)}
        for name, b, s in zip(["intercept", "log_mean_soc", "sand_frac"], beta, se)
    }
    out["r2"] = round(1 - float(resid @ resid)
                      / float(((y - y.mean()) ** 2).sum()), 3)

    # D-029 cites a log-log slope of ~1.2 for raw SD vs mean. Reproduce it here
    # so the log-scale justification is checked against the current scope rather
    # than inherited from the retired one. 0 = constant SD, 1 = constant CV.
    raw = pd.DataFrame({"sd": g.b_soc.std(ddof=1), "mean": g.b_soc.mean()}).dropna()
    raw = raw[(raw.sd > 0) & (raw["mean"] > 0)]
    out["d029_raw_slope"] = round(
        float(np.polyfit(np.log(raw["mean"].values), np.log(raw.sd.values), 1)[0]), 3)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap", type=int, default=500)
    ap.add_argument("--bootstrap-texture", type=int, default=300)
    ap.add_argument("--out", default="data/processed/g1_sensitivity.json")
    args = ap.parse_args()

    df = g1.load()
    dh, _ = g1.filter_cascade(df, in_scope=True)
    dh = g1.add_targets(dh)
    result = {"note": "exploratory; no variance-table rows written"}

    # ---------------------------------------------------------------- 1 -----
    print("=" * 78)
    print("1. LEAVE-OUT: the 10 re-admitted Mexican highland sites (MAT 15-18)")
    print("=" * 78)
    mex = dh[dh.country == "Mexico"]
    print(f"  in-scope Mexican sites: {mex.siteid.nunique()}  "
          f"({len(mex)} EUs, MAT {mex.site_mean_temp.min():.0f}-"
          f"{mex.site_mean_temp.max():.0f} C)")
    without = dh[dh.country != "Mexico"]

    block = {}
    for label, col in (("concentration", "log_soc"), ("stock", "log_stock")):
        full = est(dh, col, args.bootstrap)
        drop = est(without, col, args.bootstrap)
        shift = round(abs(full["cv_pct"] - drop["cv_pct"]), 3)
        width = min(full.get("ci_width", 1e9), drop.get("ci_width", 1e9))
        block[label] = {"with_mexico": full, "without_mexico": drop,
                        "shift": shift, "narrower_ci_width": width,
                        "shift_lt_ci_width": bool(shift < width)}
        print(f"\n  {label}")
        print(f"    with Mexico    {fmt(full)}")
        print(f"    without Mexico {fmt(drop)}")
        print(f"    shift = {shift:.3f} pts vs narrower CI width {width:.3f} "
              f"-> {'SMALLER than CI width' if shift < width else 'MATERIAL'}")
    result["leave_out_mexico"] = block

    # are the Mexican sites the source of the 2-replicate treatments?
    print("\n  Are the 10 Mexican sites the source of the 55 two-replicate treatments?")
    reps_by_country = {}
    conc = g1._with_replicates(dh[dh.log_soc.notna()])
    for country, part in conc.groupby("country"):
        sizes = part.groupby("treatmentid").size()
        reps_by_country[country] = {
            "n_treatments": int(len(sizes)),
            "n_two_replicate": int((sizes == 2).sum()),
            "replicate_hist": {int(k): int(v) for k, v in
                               sizes.value_counts().sort_index().items()},
        }
        print(f"    {country:8} {len(sizes):>3} treatments, "
              f"{int((sizes == 2).sum()):>3} of them 2-replicate  "
              f"{reps_by_country[country]['replicate_hist']}")
    result["two_replicate_by_country"] = reps_by_country

    # ---------------------------------------------------------------- 2 -----
    print("\n" + "=" * 78)
    print("2. COMMON SAMPLE: both targets on the identical EU set")
    print("=" * 78)
    common = dh[dh.log_soc.notna() & dh.log_stock.notna()]
    common = g1._with_replicates(common)
    print(f"  intersection: {len(common)} EUs / {common.treatmentid.nunique()} trt / "
          f"{common.siteid.nunique()} sites")
    cc = est(common, "log_soc", args.bootstrap)
    cs = est(common, "log_stock", args.bootstrap)
    gap_common = round(cc["cv_pct"] - cs["cv_pct"], 3)
    gap_reported = round(block["concentration"]["with_mexico"]["cv_pct"]
                         - block["stock"]["with_mexico"]["cv_pct"], 3)
    print(f"    concentration {fmt(cc)}")
    print(f"    stock         {fmt(cs)}")
    print(f"\n    gap on common sample : {gap_common:+.3f} pts")
    print(f"    gap as reported      : {gap_reported:+.3f} pts (different samples)")
    print(f"    stock < concentration on the common sample? "
          f"{'YES - survives' if gap_common > 0 else 'NO - DOES NOT SURVIVE'}")
    result["common_sample"] = {
        "n_eus": len(common), "concentration": cc, "stock": cs,
        "gap_common_sample": gap_common, "gap_as_reported": gap_reported,
        "stock_below_concentration": bool(gap_common > 0),
    }

    # ---------------------------------------------------------------- 3 -----
    print("\n" + "=" * 78)
    print("3. TEXTURE SCAN (exploratory, no rows)")
    print("=" * 78)
    tex = {}
    for var in ("b_clay", "b_sand"):
        sub = dh[dh[var].notna()].copy()
        if len(sub) < 60:
            continue
        qs = sub[var].quantile([1 / 3, 2 / 3]).values
        sub["bin"] = np.where(sub[var] <= qs[0], f"low_{var[2:]}",
                     np.where(sub[var] <= qs[1], f"mid_{var[2:]}", f"high_{var[2:]}"))
        tex[var] = {"tercile_breaks_pct": [round(float(q), 2) for q in qs], "bins": {}}
        print(f"\n  {var}  terciles at {qs[0]:.1f} / {qs[1]:.1f} %")
        for name, part in sub.groupby("bin"):
            e = est(part, "log_soc", args.bootstrap_texture)
            e["range_pct"] = [round(float(part[var].min()), 1),
                              round(float(part[var].max()), 1)]
            e["mean_soc_pct"] = round(float(part.b_soc.mean()), 3)
            tex[var]["bins"][name] = e
            print(f"    {name:<11} {var[2:]} {e['range_pct']}%  {fmt(e)}  "
                  f"meanSOC={e['mean_soc_pct']}%")
        cvs = [b["cv_pct"] for b in tex[var]["bins"].values() if b["cv_pct"]]
        widths = [b.get("ci_width", 0) for b in tex[var]["bins"].values()]
        spread = round(max(cvs) - min(cvs), 3)
        tex[var]["spread_across_bins"] = spread
        tex[var]["max_ci_width"] = round(max(widths), 3)
        tex[var]["spread_exceeds_ci"] = bool(spread > max(widths))
        print(f"    spread across bins = {spread:.3f} pts vs widest CI "
              f"{max(widths):.3f} -> "
              f"{'SIGNAL' if spread > max(widths) else 'no signal above noise'}")
    result["texture_scan"] = tex

    print("\n  Joint model - are texture and SOC level entangled?")
    jm = joint_covariate_model(dh)
    result["joint_covariate_model"] = jm
    print(f"    {jm['n_treatments']} treatments with >=3 reps {jm['by_country']}")
    for v, s in jm["spearman"].items():
        print(f"    spearman {v:9} rho={s['rho']:+.3f} p={s['p']:.3f}")
    for name, c in jm["ols_log_cv"].items():
        if name == "intercept":
            continue
        print(f"    OLS {name:13} beta={c['beta']:+.3f} t={c['t']:+.2f} "
              f"{'SIGNIFICANT' if abs(c['t']) > 2 else 'ns'}")
    print(f"    R2 = {jm['r2']}   (D-029 raw log-log slope reproduces at "
          f"{jm['d029_raw_slope']:+.3f})")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
