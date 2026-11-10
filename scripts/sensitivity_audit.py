#!/usr/bin/env python3
"""WP3(ii): sensitivity of every headline number to the paired/unpaired choice
(D-060), the relocation scale (D-061) and the assay:location cost ratio (red
team C-1), plus the central-estimate envelope (the standing rule's required
sensitivity).

    python scripts/sensitivity_audit.py   # ~6 min on 4 cores

Writes ``data/audit/sensitivity.csv`` (one row per variant x headline
quantity) and prints a markdown table. Any headline quantity that moves by
more than 2x from baseline in any variant is flagged ``>2x`` - the threshold
at which the PI asked to be stopped and asked.

Absolute cost scale is NOT a variant: n_req and C* do not depend on it, so
break-even price scales exactly linearly with it (doubling every unit cost
doubles every break-even price) and categories do not move. Stated, not run.
"""

from __future__ import annotations

import csv
import os
import statistics
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_population_audit import load_population  # noqa: E402

from loam import build_table, inverted_audit as ia  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO_ROOT, "data", "audit", "sensitivity.csv")

VARIANTS = {
    "baseline": {},
    "force_paired": {"force_design": "paired"},
    "force_unpaired": {"force_design": "unpaired"},
    "relocation_sqrt2": {"relocation_scale": "per_observation_sqrt2"},
    "relocation_sqrt2_paired (design-doc convention)": {"relocation_scale": "per_observation_sqrt2", "force_design": "paired"},
    "assay_5 (ratio 0.33)": {"cost_assay_usd": 5.0},
    "assay_10 (ratio 0.67)": {"cost_assay_usd": 10.0},
    "assay_40 (ratio 2.67)": {"cost_assay_usd": 40.0},
    "assay_80 (ratio 5.33)": {"cost_assay_usd": 80.0},
    "central_envelope": {"envelope": "central"},
}


def run_variant(name: str) -> tuple[str, dict]:
    rows_by_id = {r["row_id"]: r for r in build_table.load_rows()}
    kwargs = VARIANTS[name]
    out = {}
    for p in load_population():
        r = ia.run_audit(p, rows_by_id, **kwargs)
        if r.auditable:
            out[r.project_id] = r
    return name, out


def headline(results: dict) -> dict[str, float | str]:
    inscope = [r for r in results.values() if r.in_loam_scope]
    graze = [r for r in results.values() if any(s.startswith("land_use:grazing") for s in r.scope_distance)]
    h = {}
    for label, group in (("in_scope", inscope), ("grazing", graze)):
        for cat in ia.REACH_CATEGORIES:
            h[f"{label}: n {cat}"] = sum(r.reach_category == cat for r in group)
    h["in_scope: median break-even price"] = statistics.median(r.break_even_price_usd_per_tco2e for r in inscope)
    h["in_scope: max break-even price"] = max(r.break_even_price_usd_per_tco2e for r in inscope)
    h["in_scope: median noise scale (generous)"] = statistics.median(r.break_even_noise_scale_at_car1459_density for r in inscope)
    h["grazing: median break-even price"] = statistics.median(r.break_even_price_usd_per_tco2e for r in graze)
    for pid in ("VCS 4022", "CAR1459"):
        r = results[pid]
        o = r.paired if r.headline_design == "paired" else r.unpaired
        h[f"{pid}: design"] = r.headline_design
        h[f"{pid}: n_req"] = o.optimum.n_req
        h[f"{pid}: C*"] = o.optimum.cores_per_assay
        h[f"{pid}: Cost*"] = o.optimum.cost_usd
        h[f"{pid}: break-even price"] = r.break_even_price_usd_per_tco2e
        h[f"{pid}: noise scale"] = r.break_even_noise_scale_at_car1459_density
        h[f"{pid}: category"] = r.reach_category
        h[f"{pid}: applied/implied"] = r.applied_deduction_pct / r.implied_deduction_pct_at_optimum
    return h


def main() -> int:
    with Pool(min(4, os.cpu_count() or 1)) as pool:
        done = dict(pool.map(run_variant, list(VARIANTS)))
    heads = {name: headline(res) for name, res in done.items()}
    base = heads["baseline"]
    rows = []
    for name, h in heads.items():
        for k, v in h.items():
            b = base[k]
            if isinstance(v, str) or isinstance(b, str):
                ratio, flag = None, ("changed" if v != b else "")
            elif "n " in k and k.split(": ")[1].startswith("n "):
                ratio, flag = None, ("changed" if v != b else "")
            else:
                ratio = (v / b) if b else None
                flag = ">2x" if ratio and (ratio > 2.0 or ratio < 0.5) else ""
            rows.append({"variant": name, "quantity": k, "value": v, "baseline": b,
                         "ratio_to_baseline": round(ratio, 4) if ratio else None, "flag": flag})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    names = list(heads)
    print("| quantity | " + " | ".join(names) + " |")
    print("|---|" + "---:|" * len(names))
    for k in base:
        cells = []
        for n in names:
            v = heads[n][k]
            r = next(x for x in rows if x["variant"] == n and x["quantity"] == k)
            s = v if isinstance(v, str) else (f"{v:,.4g}" if isinstance(v, float) else str(v))
            if r["flag"] == ">2x":
                s = f"**{s}** ⚠"
            elif r["flag"] == "changed" and n != "baseline":
                s = f"*{s}*"
            cells.append(s)
        print(f"| {k} | " + " | ".join(cells) + " |")
    n_flag = sum(r["flag"] == ">2x" for r in rows)
    print(f"\n{n_flag} headline quantities move by more than 2x in some variant; wrote {os.path.relpath(OUT, REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
