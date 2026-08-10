"""The misclassification guard.

``VC-TMP-002`` sat in the ``temporal`` component for several PRs while reporting
variance between replicate experimental units. It was correctly transcribed,
correctly cited, correctly harmonised - and filed under the wrong component,
because the number appeared BESIDE the temporal figure in the source. It was
misclassified by PROXIMITY.

Every existing guard missed it, and each of them was right to:

* R6 tests whether a locator has been verified. This locator was verified.
* D-032 tests whether an open decision governs a live constant. None did.
* The staleness test compares YAML with CSV. They agreed.

None of them asks the question that mattered: *is this number the kind of thing
its component says it is?* That question needs each row to state what it
measures in vocabulary that does not mention the component - which is what
``quantity_definition`` is for, and what these tests check.

The check is structural, not semantic. Every definition must name its **axis of
variation** after "between", "across" or "among", and the earliest component
marker in that phrase decides what the definition reads as. So "variation
between sampling occasions at one fixed plot" resolves to ``temporal`` because
"sampling occasions" precedes "plot" - a rule, not a judgement.

Expect this suite to fail loudly on ambiguity. That is the design. A row whose
axis cannot be read is a row nobody has been forced to think about.
"""

from __future__ import annotations

import pytest

from loam import build_table
from loam.schema import (
    AXIS_TRIGGERS,
    COMPONENT_DEFINITIONS,
    COMPONENT_DEFINITIONS_BY_NAME,
    COMPONENTS,
    read_axis,
)

#: Rows whose axis of variation genuinely does NOT match the component they are
#: filed under, each with the reason and the decision that examined it.
#:
#: This is an allowlist, so it is the obvious place to hide a problem. Two
#: things stop that. First, adding an entry is a visible edit to a test file
#: with a written reason. Second - and this is the part with teeth -
#: :func:`test_a_cross_component_row_is_never_load_bearing` forbids any row in
#: here from being a ``baseline``. A misfiled row may be kept for context; it
#: may never drive a number.
KNOWN_CROSS_COMPONENT: dict[str, str] = {
    "VC-TMP-002": (
        "The row this guard exists because of. Reports between-experimental-unit "
        "variance while filed under `temporal`, purely because the source "
        "printed it beside the temporal figure. Superseded by VC-BPS-007..011 "
        "(D-049) and kept visible on purpose; not re-filed, because moving it "
        "would erase the evidence of the failure this test was built from."
    ),
    "VC-BPS-001": (
        "Pools within-plot and between-plot variation - its own "
        "harmonization_note says so: 'this figure is NOT a pure between-plot "
        "term'. A figure that pools two components belongs to neither (D-051)."
    ),
    "VC-BPS-003": (
        "A RATIO BETWEEN two components, not a measurement of one. Its "
        "numerator is within-plot variance and it is filed under "
        "between_plot_spatial (D-051)."
    ),
    "VC-BPS-004": (
        "An MDC - an OUTPUT of a whole variance structure plus a design, alpha "
        "and power, not a variance component at all. Its axis is two inventory "
        "occasions ten years apart, crossed with the plot network (D-051)."
    ),
}


@pytest.fixture(scope="module")
def rows():
    return build_table.load_rows()


# ---------------------------------------------------------------------------
# the component definitions themselves
# ---------------------------------------------------------------------------


def test_every_component_has_a_definition():
    missing = [c for c in COMPONENTS if c not in COMPONENT_DEFINITIONS_BY_NAME]
    assert not missing, f"components with no definition: {missing}"


def test_no_component_definition_leans_on_the_component_name():
    """A definition that restates the name explains nothing.

    'between_plot_spatial: between-plot spatial variance' would pass any naive
    consistency check while carrying no information, which is precisely the
    failure mode that let VC-TMP-002 through.
    """
    for comp in COMPONENT_DEFINITIONS:
        parts = comp.name.split("_")
        # The failure mode is the ASSEMBLED name reappearing - "within-plot
        # spatial", "between plot spatial" - not the individual words. "within"
        # and "between" are ordinary English and a definition of a spatial term
        # can hardly avoid them.
        forms = {sep.join(parts) for sep in (" ", "-", "_")}
        forms |= {sep.join(parts[:2]) for sep in (" ", "-", "_")}
        text = comp.definition.lower()
        leaked = sorted(f for f in forms if f in text)
        assert not leaked, (
            f"{comp.name}'s definition restates its own name ({leaked}). "
            "State what varies and what is held fixed instead."
        )


def test_component_markers_do_not_collide():
    """Two components claiming the same marker would make the axis unreadable."""
    seen: dict[str, str] = {}
    for comp in COMPONENT_DEFINITIONS:
        for marker in comp.varies_across:
            assert marker not in seen, (
                f"marker {marker!r} is claimed by both {seen[marker]} and "
                f"{comp.name}; the axis would be ambiguous"
            )
            seen[marker] = comp.name


# ---------------------------------------------------------------------------
# the guard
# ---------------------------------------------------------------------------


def test_every_row_defines_what_it_measures(rows):
    missing = [r["row_id"] for r in rows if not str(r.get("quantity_definition") or "").strip()]
    assert not missing, (
        f"rows with no quantity_definition: {missing}. Every row must say what "
        "it measures independently of where it is filed."
    )


def test_every_definition_names_an_axis_of_variation(rows):
    offenders = []
    for row in rows:
        axis, comp, _ = read_axis(row["quantity_definition"])
        if not axis:
            offenders.append(
                f"{row['row_id']}: no {'/'.join(t.strip() for t in AXIS_TRIGGERS)} "
                "clause - the definition never says what differs between the two "
                "measurements being compared"
            )
        elif comp is None:
            offenders.append(
                f"{row['row_id']}: axis {axis!r} matches no component's markers"
            )
    assert not offenders, (
        "definitions that do not name a readable axis:\n  - "
        + "\n  - ".join(offenders)
        + "\n\nRewrite so the axis follows 'between'/'across'/'among', or add a "
        "marker to the component in schema.py if the vocabulary is genuinely "
        "missing. Do not weaken this test."
    )


def test_no_row_is_filed_under_a_component_its_definition_contradicts(rows):
    """THE GUARD. What VC-TMP-002 needed and nothing provided."""
    offenders = []
    for row in rows:
        rid = row["row_id"]
        axis, reads_as, _ = read_axis(row["quantity_definition"])
        if reads_as is None or reads_as == row["component"]:
            continue
        if rid in KNOWN_CROSS_COMPONENT:
            continue
        offenders.append(
            f"{rid} is filed under {row['component']!r} but its definition "
            f"reads as {reads_as!r} (axis: {axis!r})"
        )
    assert not offenders, (
        "rows filed under a component their own definition contradicts:\n  - "
        + "\n  - ".join(offenders)
        + "\n\nThis is the VC-TMP-002 failure repeating. Either re-file the row, "
        "or - if the mismatch is real and the row is kept for context - add it "
        "to KNOWN_CROSS_COMPONENT with a reason and a D-NNN, which also bars it "
        "from ever being a baseline."
    )


def test_a_cross_component_row_is_never_load_bearing(rows):
    """The teeth on the allowlist.

    An allowlist with no cost is a silencer. This is the cost: a row whose axis
    disagrees with its component may be kept for contrast, but it may not drive
    a number in the OSSE. If someone wants a misfiled row to be load-bearing,
    they have to re-file it first.
    """
    offenders = [
        f"{r['row_id']} ({r['component']})" for r in rows
        if r["row_id"] in KNOWN_CROSS_COMPONENT and r.get("use_as") == "baseline"
    ]
    assert not offenders, (
        "rows on the cross-component allowlist that are also baselines:\n  - "
        + "\n  - ".join(offenders)
        + "\n\nA row whose definition contradicts its component cannot be "
        "load-bearing. Re-file it, or demote it."
    )


def test_allowlist_has_no_stale_entries(rows):
    """An entry that no longer describes a mismatch must be removed.

    Otherwise the allowlist quietly grows into a permanent exemption list, and a
    row could be re-filed correctly while keeping its licence to be wrong.
    """
    by_id = {r["row_id"]: r for r in rows}
    stale = []
    for rid in KNOWN_CROSS_COMPONENT:
        row = by_id.get(rid)
        if row is None:
            stale.append(f"{rid} is no longer in the table")
            continue
        _, reads_as, _matched = read_axis(row.get("quantity_definition", ""))
        if reads_as == row["component"] and len(_matched) == 1:
            stale.append(
                f"{rid} now reads as {reads_as!r}, matching where it is filed"
            )
    assert not stale, (
        "stale KNOWN_CROSS_COMPONENT entries:\n  - " + "\n  - ".join(stale)
        + "\n\nRemove them. The allowlist records live mismatches, not history."
    )


def test_every_allowlisted_row_cites_a_decision(rows):
    by_id = {r["row_id"]: r for r in rows}
    for rid, reason in KNOWN_CROSS_COMPONENT.items():
        assert "D-0" in reason, (
            f"{rid} is allowlisted without citing a decision. A mismatch that "
            "nobody wrote up is a mismatch nobody decided about."
        )
        assert rid in by_id


def test_no_row_pools_two_components(rows):
    """A figure spanning two axes belongs to neither, and must say so.

    `VC-BPS-001` is the case in hand: a CV computed across a national plot
    network that mixes plot-to-plot variation with microplot-to-microplot
    variation inside each plot. Its harmonization_note already admits this in
    prose - "this figure is NOT a pure between-plot term" - but prose does not
    fail CI, which is the whole lesson of D-032. Now the component field has to
    admit it too.
    """
    offenders = []
    for row in rows:
        if row["row_id"] in KNOWN_CROSS_COMPONENT:
            continue
        axis, _, matched = read_axis(row["quantity_definition"])
        if len(matched) > 1:
            offenders.append(
                f"{row['row_id']} (filed {row['component']!r}) names axes for "
                f"{sorted(matched)} - axis: {axis!r}"
            )
    assert not offenders, (
        "rows whose definition spans more than one component:\n  - "
        + "\n  - ".join(offenders)
        + "\n\nA pooled figure is not a measurement of either component. Split "
        "it, re-file it, or allowlist it - which also bars it from being a "
        "baseline."
    )


# ---------------------------------------------------------------------------
# the reader itself is load-bearing, so pin its behaviour
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "definition,expected",
    [
        # the axis wins over later mentions of other components
        ("variation between sampling occasions at one fixed plot", "temporal"),
        ("variation between plots on one sampling occasion", "between_plot_spatial"),
        ("variation between cores within a plot on one date", "within_plot_spatial"),
        ("difference between replicate determinations of the same sample",
         "analytical"),
        ("difference between an original position and its displaced resample",
         "relocation"),
        ("difference between accounting conventions applied to one profile",
         "depth_bd_convention"),
        # no trigger word at all
        ("the plot-to-plot standard deviation", None),
        # trigger present, no known marker
        ("variation between things nobody has named", None),
    ],
)
def test_read_axis_resolves_the_declared_examples(definition, expected):
    assert read_axis(definition)[1] == expected


def test_read_axis_is_what_would_have_caught_vc_tmp_002():
    """The regression test for the original failure, stated as a fact.

    This is VC-TMP-002's real definition. Filed under `temporal`, it reads as
    `between_plot_spatial` - which is what a guard needed to say two months ago.
    """
    definition = (
        "share of total random error attributable to variation between "
        "replicate experimental units under identical management, at one "
        "sampling occasion"
    )
    assert read_axis(definition)[1] == "between_plot_spatial"
