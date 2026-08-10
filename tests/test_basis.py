"""The basis guard — dimensional silence is the failure mode here.

D-051 gave every row an **axis** (what varies). This file gives every row a
**basis** (what the number is expressed on). They are orthogonal, and the second
is the one units cannot help with.

``VC-ANA-001`` is 1.25%, a CV of SOC **concentration**. Potash et al. 2025 use
``sigma_l`` = 2 Mg C/ha, a **stock** error that explicitly bundles bulk-density
error. Both would render as ``pct`` after a harmonisation step, and summing them
into one budget produces a number with no meaning — not a type error, not a unit
error, just a wrong answer that looks fine.

The table already knew this. D-020 says "concentration CV is never treated as
stock CV". It said it in prose, and prose does not fail CI — the same gap D-032
closed for open decisions and D-051 closed for components. This is the
enforceable version.

The teeth are in :func:`test_baseline_dispersion_rows_share_a_basis_per_component`.
Structural rows are exempt on purpose: a ``bias_pct`` or a ``range`` modifies or
describes a budget, it is not summed into one.
"""

from __future__ import annotations

import pytest

from loam import build_table
from loam.schema import BASES, COMPONENTS, DISPERSION_STATISTICS, UNITS_BY_BASIS

#: Components that legitimately carry more than one basis among their baseline
#: dispersion rows, with the decision that examined the coexistence. An entry
#: here is NOT permission to sum across the bases — it is a record that both are
#: wanted and that the OSSE must pick one deliberately.
MIXED_BASIS_BY_DESIGN: dict[str, str] = {
    "between_plot_spatial": (
        "VC-BPS-005 is a CONCENTRATION CV and VC-BPS-006/007-011 are STOCK CVs. "
        "Both are wanted: concentration is what the laboratory measures and is "
        "free of bulk-density error, stock is what a carbon claim is denominated "
        "in. D-020 already forbids treating one as the other, and D-040 showed "
        "the stock CV runs BELOW the concentration CV on a common sample "
        "(11.456% against 11.897%), so the two are not interchangeable even "
        "approximately. The OSSE must choose one basis per run and say which "
        "(D-020, D-052)."
    ),
}


@pytest.fixture(scope="module")
def rows():
    return build_table.load_rows()


def test_every_row_declares_a_basis(rows):
    missing = [r["row_id"] for r in rows if not str(r.get("basis") or "").strip()]
    assert not missing, f"rows with no basis: {missing}"


def test_every_basis_is_in_the_vocabulary(rows):
    bad = [
        f"{r['row_id']}: {r['basis']!r}" for r in rows if r["basis"] not in BASES
    ]
    assert not bad, f"rows with an unrecognised basis: {bad}"


def test_units_are_admissible_for_the_declared_basis(rows):
    """A stock in metres, or a concentration in Mg C/ha, is a transcription slip.

    Weaker than the mismatch this file exists for — units and basis disagreeing
    is at least *visible* — but it costs nothing and it pins the mapping.
    """
    offenders = [
        f"{r['row_id']}: basis {r['basis']!r} with units {r['units']!r} "
        f"(admissible: {UNITS_BY_BASIS[r['basis']]})"
        for r in rows
        if r["basis"] in UNITS_BY_BASIS
        and r["units"] not in UNITS_BY_BASIS[r["basis"]]
    ]
    assert not offenders, (
        "rows whose units are inadmissible for their basis:\n  - "
        + "\n  - ".join(offenders)
    )


def test_baseline_dispersion_rows_share_a_basis_per_component(rows):
    """THE GUARD. Two baselines in one component, on different bases, are a trap.

    Restricted to dispersion statistics because those are the summable ones. A
    ``bias_pct`` row like VC-REL-003 (a 50% error reduction) or a ``range`` row
    like VC-REL-004 (a saturation distance) modifies or describes a budget; it
    is never an addend, so a differing basis there is not dangerous.
    """
    offenders = []
    for comp in COMPONENTS:
        bases: dict[str, list[str]] = {}
        for row in rows:
            if (
                row["component"] != comp
                or row.get("use_as") != "baseline"
                or row["statistic"] not in DISPERSION_STATISTICS
            ):
                continue
            bases.setdefault(row["basis"], []).append(row["row_id"])
        if len(bases) > 1 and comp not in MIXED_BASIS_BY_DESIGN:
            detail = "; ".join(f"{b}: {sorted(ids)}" for b, ids in sorted(bases.items()))
            offenders.append(f"{comp} mixes bases among its baselines — {detail}")

    assert not offenders, (
        "components whose baseline dispersion rows do not share a basis:\n  - "
        + "\n  - ".join(offenders)
        + "\n\nThese numbers are dimensionally identical and semantically "
        "different; summing them yields a number that means nothing. Either "
        "demote one, convert one (which needs a bulk density and makes the row "
        "mean-dependent), or add the component to MIXED_BASIS_BY_DESIGN with a "
        "decision explaining why both are wanted."
    )


def test_mixed_basis_entries_cite_a_decision_and_are_still_mixed(rows):
    """No stale exemptions, and no exemption without a written reason."""
    stale = []
    for comp, reason in MIXED_BASIS_BY_DESIGN.items():
        assert comp in COMPONENTS, f"{comp} is not a component"
        assert "D-0" in reason, (
            f"{comp} is exempted without citing a decision. An exemption nobody "
            "wrote up is an exemption nobody decided about."
        )
        bases = {
            r["basis"] for r in rows
            if r["component"] == comp
            and r.get("use_as") == "baseline"
            and r["statistic"] in DISPERSION_STATISTICS
        }
        if len(bases) <= 1:
            stale.append(f"{comp} no longer mixes bases (now {sorted(bases)})")
    assert not stale, (
        "stale MIXED_BASIS_BY_DESIGN entries:\n  - " + "\n  - ".join(stale)
        + "\n\nRemove them; the list records live coexistence, not history."
    )


def test_a_concentration_row_never_carries_an_absolute_stock_sd(rows):
    """Converting concentration to Mg C/ha needs a bulk density, and that is a
    mean-dependence that must be declared (R4/R5), not slipped in."""
    offenders = [
        r["row_id"] for r in rows
        if r["basis"] == "concentration"
        and str(r.get("sd_mg_c_ha") or "").strip()
        and not r.get("mean_dependent")
    ]
    assert not offenders, (
        f"concentration rows carrying an absolute SD without declaring "
        f"mean-dependence: {offenders}"
    )
