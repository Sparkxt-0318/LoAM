#!/usr/bin/env python3
"""WP2: run the inverted audit over every project that clears the gate, and
report DISTRIBUTIONS in three categories - never a pass/fail count.

    python scripts/run_population_audit.py            # writes the outputs below
    python scripts/run_population_audit.py --markdown # also prints the tables

Population: ``data/registry/projects.yaml`` (hand-curated) plus
``data/registry/projects_accu_issued.yaml`` (the 54 credit-issued ACCU soil
projects, generated, D-064). Where a project id appears in both, the
generated ACCU record is used (it carries the D-065 scope flags); the
hand-curated and generated areas/credits are test-guarded to be identical.

Outputs:
* ``data/processed/population_audit.json`` - every field of every result
  (git-ignored, reproducible);
* ``data/audit/population_audit.csv`` - one committed row per project, the
  quantities the writeup quotes.

Reporting rules (D-067, red team B-5 and C-5):
* three categories - inside reach / within the uncertainty band / outside
  reach (``loam.inverted_audit.classify_reach``);
* out-of-scope projects are reported in their own groups, with their
  ``scope_distance`` flags, and NEVER pooled into an in-scope figure;
* distributions are reported as min / quartiles / max, not as a mean or a
  proportion with an implied sampling interpretation - the population is a
  complete count of what is auditable, not a sample of anything.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
import sys

import yaml

from loam import build_table, inverted_audit as ia

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(REPO_ROOT, "data", "registry", "projects.yaml")
ACCU = os.path.join(REPO_ROOT, "data", "registry", "projects_accu_issued.yaml")
OUT_JSON = os.path.join(REPO_ROOT, "data", "processed", "population_audit.json")
OUT_CSV = os.path.join(REPO_ROOT, "data", "audit", "population_audit.csv")


def load_population() -> list[dict]:
    with open(CORPUS, encoding="utf-8") as fh:
        hand = yaml.safe_load(fh)["projects"]
    with open(ACCU, encoding="utf-8") as fh:
        gen = yaml.safe_load(fh)["projects"]
    gen_ids = {p["project_id"] for p in gen}
    pop = [p for p in hand if p["project_id"] not in gen_ids] + gen
    for p in pop:
        if "scope_distance" not in p:
            p["scope_distance"] = [] if p.get("in_loam_scope") else ["see scope_note"]
    return pop


def group_of(result: ia.AuditResult) -> str:
    if result.in_loam_scope:
        return "in_scope"
    d = result.scope_distance
    if any(x.startswith("land_use:grazing_pasture") for x in d):
        return "out_of_scope:grazing_pasture"
    if any(x.startswith("land_use:unresolved") for x in d):
        return "out_of_scope:land_use_unresolved"
    return "out_of_scope:other"


def quartiles(xs: list[float]) -> tuple[float, float, float, float, float] | None:
    xs = sorted(x for x in xs if x is not None and not math.isnan(x))
    if not xs:
        return None
    if len(xs) == 1:
        return (xs[0],) * 5
    q = statistics.quantiles(xs, n=4, method="inclusive")
    return (xs[0], q[0], q[1], q[2], xs[-1])


def fmt(x: float | None, kind: str = "g") -> str:
    if x is None:
        return "—"
    if kind == "usd":
        return f"${x:,.4f}" if x < 1 else f"${x:,.2f}"
    if kind == "x":
        return f"{x:,.3g}×"
    return f"{x:,.4g}"


def row_for(r: ia.AuditResult) -> dict:
    h = r.paired if r.headline_design == "paired" else r.unpaired
    return {
        "project_id": r.project_id,
        "group": group_of(r),
        "scope_distance": ";".join(r.scope_distance),
        "area_ha": round(r.area_ha, 2),
        "delta_mg_c_ha": round(r.delta_mg_c_ha, 4),
        "headline_design": r.headline_design,
        "n_req": h.optimum.n_req,
        "cores_per_assay": h.optimum.cores_per_assay,
        "cost_usd": round(h.optimum.cost_usd, 2),
        "revenue_tco2e": round(r.revenue_tco2e, 1) if r.revenue_tco2e else None,
        "break_even_price_usd_per_tco2e": round(r.break_even_price_usd_per_tco2e, 6) if r.break_even_price_usd_per_tco2e else None,
        "n_plausible_car1459_density": round(r.n_plausible_at_car1459_density, 1),
        "break_even_noise_scale_generous": round(r.break_even_noise_scale_at_car1459_density, 4),
        "break_even_noise_scale_high_corner": round(r.break_even_noise_scale_high_corner, 4),
        "reach_category": r.reach_category,
        "between_plot_headroom_unpaired": round(r.between_plot_headroom_unpaired, 4),
        "registry_k": r.registry_k,
        "implied_deduction_pct_at_optimum": round(r.implied_deduction_pct_at_optimum, 4),
        "applied_deduction_pct": r.applied_deduction_pct,
        "applied_over_implied": round(r.applied_deduction_pct / r.implied_deduction_pct_at_optimum, 4) if r.applied_deduction_pct else None,
        "own_implied_relative_se": round(r.own_deduction["implied_relative_se"], 4) if r.own_deduction else None,
        "own_delta_over_mdd_power90": round(r.own_deduction["delta_over_mdd_power90"], 4) if r.own_deduction else None,
        "own_delta_over_mdd_power50": round(r.own_deduction["delta_over_mdd_power50"], 4) if r.own_deduction else None,
        "support_mismatch_ratio": round(r.support_mismatch_ratio, 1),
        "qa_upper_bound_flag": r.qa_upper_bound_flag,
    }


def markdown(rows: list[dict], gated: list[ia.AuditResult]) -> str:
    out = []
    groups = ["in_scope", "out_of_scope:grazing_pasture", "out_of_scope:land_use_unresolved", "out_of_scope:other"]
    out.append("| group | projects | inside reach | within uncertainty band | outside reach |")
    out.append("|---|---:|---:|---:|---:|")
    for g in groups:
        rs = [r for r in rows if r["group"] == g]
        if not rs:
            continue
        c = {k: sum(r["reach_category"] == k for r in rs) for k in ia.REACH_CATEGORIES}
        out.append(f"| {g} | {len(rs)} | {c['inside_reach']} | {c['within_uncertainty_band']} | {c['outside_reach']} |")
    out.append("")
    metrics = [
        ("delta_mg_c_ha", "Δ, net credited (Mg C/ha)", "g"),
        ("n_req", "n_req at Cost* (locations)", "g"),
        ("cost_usd", "Cost* (USD)", "usd"),
        ("break_even_price_usd_per_tco2e", "break-even price (USD/tCO2e)", "usd"),
        ("break_even_noise_scale_generous", "break-even noise scale, generous corner", "x"),
        ("break_even_noise_scale_high_corner", "break-even noise scale, high corner", "x"),
        ("between_plot_headroom_unpaired", "σ_B headroom before claim leaves reach (G9)", "x"),
        ("implied_deduction_pct_at_optimum", "implied deduction at Cost* (%)", "g"),
        ("support_mismatch_ratio", "support-mismatch ratio", "x"),
    ]
    for g in groups:
        rs = [r for r in rows if r["group"] == g]
        if not rs:
            continue
        out.append(f"**{g}** (n = {len(rs)}) — min · Q1 · median · Q3 · max")
        out.append("")
        out.append("| quantity | min | Q1 | median | Q3 | max |")
        out.append("|---|---:|---:|---:|---:|---:|")
        for key, label, kind in metrics:
            q = quartiles([r[key] for r in rs])
            if q:
                out.append(f"| {label} | " + " | ".join(fmt(v, kind) for v in q) + " |")
        out.append("")
    out.append("**Projects with a published applied deduction** (the only ones where implied-vs-applied exists)")
    out.append("")
    out.append("| project | k | implied at Cost* | applied | applied/implied | own σ_rel | own Δ/MDD (90% power) | own Δ/MDD (50% power) |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        if r["applied_deduction_pct"] is not None:
            out.append(
                f"| {r['project_id']} | {r['registry_k']} | {r['implied_deduction_pct_at_optimum']:.2f}% | "
                f"{r['applied_deduction_pct']:.2f}% | {r['applied_over_implied']:.3f} | {r['own_implied_relative_se']:.4f} | "
                f"{r['own_delta_over_mdd_power90']:.3f} | {r['own_delta_over_mdd_power50']:.3f} |"
            )
    out.append("")
    out.append("**Not auditable**: " + "; ".join(f"{g.project_id} ({' / '.join(g.gate_reasons)[:120]})" for g in gated))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--markdown", action="store_true")
    args = ap.parse_args()
    rows_by_id = {r["row_id"]: r for r in build_table.load_rows()}
    pop = load_population()
    results, gated, rows = {}, [], []
    for p in pop:
        r = ia.run_audit(p, rows_by_id)
        results[r.project_id] = r.to_dict()
        if not r.auditable:
            gated.append(r)
            continue
        rows.append(row_for(r))
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump({"note": "WP2 population audit (D-067). See docs/phase5_population_results.md.",
                   "n_population": len(pop), "n_auditable": len(rows), "results": results}, fh, indent=1)
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["group"], r["project_id"])):
            w.writerow(r)
    print(f"{len(rows)}/{len(pop)} projects audited; wrote {os.path.relpath(OUT_CSV, REPO_ROOT)}")
    if args.markdown:
        print()
        print(markdown(rows, gated))
    return 0


if __name__ == "__main__":
    sys.exit(main())
