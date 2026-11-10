#!/usr/bin/env python3
"""WP3(i): diff the independent re-implementation against loam.inverted_audit.

    python scripts/independent_audit_reimpl.py <cases.json> <out.json>   # the independent file
    python scripts/compare_independent_reimpl.py <cases.json> <reimpl_out.json>

``scripts/independent_audit_reimpl.py`` was written by a separate agent from
a formula specification, without reading ``src/loam/inverted_audit.py``,
``src/loam/student_t.py`` or their tests (its docstring records this, and one
incidental exposure: a DECISIONS.md changelog line giving VCS 4022's 13.2% /
unpaired). This script recomputes every case with the package, under the
same three variants, and reports every disagreement in n_req, C*, Cost*,
headline design and implied deduction. It writes nothing but stdout.
"""

from __future__ import annotations

import json
import sys

from loam import build_table, inverted_audit as ia


def ours(cases, rows_by_id, variant):
    reloc = "per_observation_sqrt2" if variant == "relocation_per_observation_sqrt2" else "difference_scale"
    c_assay = 60.0 if variant == "assay_cost_60" else ia.COST_ASSAY_USD
    comps = ia.assemble_components(rows_by_id, relocation_scale=reloc)
    out = {}
    for c in cases:
        d = c["delta_mg_c_ha"]
        p = ia.cost_optimum(comps, d, paired=True, cost_assay_usd=c_assay)
        u = ia.cost_optimum(comps, d, paired=False, cost_assay_usd=c_assay)
        head = "paired" if p.cost_usd <= u.cost_usd else "unpaired"
        h = p if head == "paired" else u
        out[c["case_id"]] = {
            "paired": {"C": p.cores_per_assay, "n_req": p.n_req, "S": p.s_mg_c_ha, "cost": p.cost_usd},
            "unpaired": {"C": u.cores_per_assay, "n_req": u.n_req, "S": u.s_mg_c_ha, "cost": u.cost_usd},
            "headline_design": head,
            "implied_deduction_pct": ia.implied_uncertainty_deduction_pct(c["k"], h.s_mg_c_ha, h.n_req, d),
        }
    return out


def main(cases_path: str, reimpl_path: str) -> int:
    cases = json.load(open(cases_path))
    theirs = json.load(open(reimpl_path))
    rows_by_id = {r["row_id"]: r for r in build_table.load_rows()}
    total_bad = 0
    for variant in ("default", "relocation_per_observation_sqrt2", "assay_cost_60"):
        mine = ours(cases, rows_by_id, variant)
        bad = []
        for cid, m in mine.items():
            t = theirs[variant][cid]
            for design in ("paired", "unpaired"):
                for key in ("C", "n_req"):
                    if m[design][key] != t[design][key]:
                        bad.append(f"{cid} {design} {key}: ours {m[design][key]} theirs {t[design][key]}")
                for key in ("S", "cost"):
                    if abs(m[design][key] - t[design][key]) > 1e-4 * max(1.0, abs(t[design][key])):
                        bad.append(f"{cid} {design} {key}: ours {m[design][key]:.6f} theirs {t[design][key]:.6f}")
            if m["headline_design"] != t["headline_design"]:
                bad.append(f"{cid} headline: ours {m['headline_design']} theirs {t['headline_design']}")
            if abs(m["implied_deduction_pct"] - t["implied_deduction_pct"]) > 1e-4:
                bad.append(f"{cid} implied: ours {m['implied_deduction_pct']:.6f} theirs {t['implied_deduction_pct']:.6f}")
        print(f"{variant}: {len(mine)} cases x 2 designs; {len(bad)} disagreements")
        for b in bad:
            print("   ", b)
        total_bad += len(bad)
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
