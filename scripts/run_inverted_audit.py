#!/usr/bin/env python3
"""Phase 5: run the inverted audit over the registry corpus.

    python scripts/run_inverted_audit.py

Loads ``data/registry/projects.yaml`` and ``data/variance_components.yaml``,
runs ``loam.inverted_audit.run_audit`` on every project, prints a one-line
summary per project, and writes the full per-project results to
``data/processed/inverted_audit.json``.

WHAT THIS SCRIPT DOES NOT DO
-----------------------------
It does not decide whether a project's claim was "real" or "fraudulent" -
only whether the claim was DETECTABLE under a generous reading of our own
variance table, and what that would have cost. It does not count failures
across the corpus into a headline percentage: with a seven-project,
hand-curated corpus where only one project (VCS 4022) currently has enough
disclosed inputs to be auditable at all, a percentage would imply a sample
this is not. See ``docs/phase5_inverted_audit_results.md`` for what the first
run's numbers do and do not license claiming, and DECISIONS.md D-059..D-063
for what was decided to make this runnable.
"""

from __future__ import annotations

import json
import os

import yaml

from loam import build_table, inverted_audit as ia

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(REPO_ROOT, "data", "registry", "projects.yaml")
OUT = os.path.join(REPO_ROOT, "data", "processed", "inverted_audit.json")


def _summary_line(result: ia.AuditResult) -> str:
    if not result.auditable:
        return f"  {result.project_id:<10} NOT AUDITABLE: {'; '.join(result.gate_reasons)}"
    headline = result.paired if result.headline_design == "paired" else result.unpaired
    h = headline.optimum
    price = (
        f"${result.break_even_price_usd_per_tco2e:.4f}/tCO2e"
        if result.break_even_price_usd_per_tco2e is not None else "n/a (no revenue figure)"
    )
    implied = result.implied_deduction_pct_at_optimum
    applied = result.applied_deduction_pct
    dedn = f"implied {implied:.2f}%" + (f" vs applied {applied:.2f}%" if applied is not None else " (applied not disclosed)")
    return (
        f"  {result.project_id:<10} [{result.headline_design:<8}] n_req={h.n_req:<8} "
        f"C*={h.cores_per_assay:<3} Cost*=${h.cost_usd:,.0f}  break-even={price}  {dedn}  "
        f"support_mismatch={result.support_mismatch_ratio:,.0f}x"
    )


def main() -> int:
    rows_by_id = {r["row_id"]: r for r in build_table.load_rows()}
    with open(CORPUS, encoding="utf-8") as fh:
        corpus = yaml.safe_load(fh)

    print("Phase 5 inverted audit - per project (headline design chosen per project by "
          "lower Cost*, D-060 - paired and unpaired are both computed, never assumed)\n")
    results: dict[str, dict] = {}
    n_auditable = 0
    for project in corpus["projects"]:
        result = ia.run_audit(project, rows_by_id)
        results[result.project_id] = result.to_dict()
        print(_summary_line(result))
        if result.auditable:
            n_auditable += 1

    total = len(corpus["projects"])
    print(
        f"\n{n_auditable}/{total} corpus projects carry enough disclosed inputs "
        "(area + a claimed rate) to run the audit at all. This mirrors, at the "
        "audit's own input requirements, the disclosure gap D-056 already "
        "found at the sampling-design level - see docs/registry_corpus.md and "
        "docs/phase5_inverted_audit_results.md."
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "note": (
                    "First Phase 5 inverted-audit run. Headline design (paired "
                    "vs. unpaired) is chosen PER PROJECT by lower Cost* (D-060) "
                    "and reported as `headline_design`/`headline`; both "
                    "`paired` and `unpaired` are always computed and kept. "
                    "Low-envelope values are a deliberate worst-case-for-us "
                    "CORNER BOUND (red team C-2), not a confidence interval. "
                    "See docs/phase5_inverted_audit_results.md before quoting "
                    "any single number out of context."
                ),
                "n_auditable": n_auditable,
                "n_total": total,
                "results": results,
            },
            fh,
            indent=2,
        )
    print(f"\nwrote {os.path.relpath(OUT, REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
