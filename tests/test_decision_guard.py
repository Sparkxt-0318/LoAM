"""The open-decision guard.

D-028 was recorded as "OPEN - for the PI" and shipped as the active constant
behind two baseline rows regardless. These tests make that unrepresentable.

The pattern is the one R6 already uses on the unverified LUCAS rows: state the
condition in data, then let a test refuse to go green while it holds. R6 worked -
the LUCAS rows have stayed locked out of use for exactly as long as they have
been unverified, with no discipline required from anyone.

Expect a red suite while a live constant still rests on an open decision. That
is the guard reporting, not the guard broken. The way to green is to settle the
decision (or to stop the affected rows being load-bearing) - never to soften a
test here.
"""

from __future__ import annotations

import io
import re
from contextlib import redirect_stdout

import pytest

from loam import build_table
from loam.decisions import (
    ALL_DECISIONS,
    CONSTANT_STATES,
    CONSTANTS,
    DECIDED_DECISIONS,
    DECISION_STATES,
    OPEN_DECISIONS,
    PROPOSED_FLAG,
    Constant,
    open_decisions_referenced,
    proposed_constants,
    referenced_decisions,
    rows_exposed_to_open_decisions,
    status_of,
)

#: Verification levels that make a row load-bearing evidence, mirroring
#: tests/test_variance_table.py so the two cannot disagree about what "verified"
#: means.
BASELINE_EVIDENCE = {"derived_primary_data", "verified_fulltext"}


@pytest.fixture(scope="module")
def rows():
    return build_table.load_rows()


@pytest.fixture(scope="module")
def decisions_md() -> str:
    return (build_table.REPO_ROOT / "DECISIONS.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# the guard itself
# ---------------------------------------------------------------------------


def test_no_live_constant_rests_on_an_open_decision():
    """A constant driving a published number must have a decision behind it."""
    offenders = [
        f"{c.name} is governed by {c.governed_by}, which is still OPEN "
        f"({OPEN_DECISIONS[c.governed_by]})"
        for c in proposed_constants()
    ]
    assert not offenders, (
        "live constants resting on an undecided question:\n  - "
        + "\n  - ".join(offenders)
        + "\n\nResolve the decision in DECISIONS.md and move its id from "
        "OPEN_DECISIONS to DECIDED_DECISIONS in src/loam/decisions.py. "
        "Do not relax this test: it is the only thing standing between an "
        "unratified constant and a number someone will cite."
    )


def test_no_verified_baseline_row_rests_on_an_open_decision(rows):
    """A load-bearing row must not depend on a question nobody has answered."""
    exposure = rows_exposed_to_open_decisions(rows)
    offenders = [
        f"{row['row_id']} depends on {sorted(exposure[row['row_id']])}"
        for row in rows
        if row.get("use_as") == "baseline"
        and row.get("verification") in BASELINE_EVIDENCE
        and row["row_id"] in exposure
    ]

    assert not offenders, (
        "verified baseline rows resting on an open decision:\n  - "
        + "\n  - ".join(offenders)
        + "\n\nEither settle the decision, or demote the row out of `baseline` "
        "until it is settled."
    )


def test_exposure_is_detected_without_the_row_admitting_it(rows):
    """The guard must not reward a row for staying quiet.

    ``VC-BPS-006`` never mentions D-028, yet it comes off the same filter
    cascade as ``VC-BPS-005`` under the same unratified envelope. It is caught
    through its derivation script, not its prose. If that second route ever
    breaks, this notices before the silent row slips through.
    """
    quiet = next(
        (r for r in rows if r["row_id"] == "VC-BPS-006"), None
    )
    if quiet is None:  # row retired; the invariant it pinned went with it
        pytest.skip("VC-BPS-006 is no longer in the table")

    assert "D-028" not in open_decisions_referenced(quiet), (
        "VC-BPS-006 now cites D-028 in prose. Good - but this test was pinning "
        "the case where it does NOT, so find another silent row or drop it."
    )
    assert "D-028" in rows_exposed_to_open_decisions(rows).get("VC-BPS-006", set()), (
        "VC-BPS-006 is derived by a script that consumes the proposed "
        "CLIMATE_ENVELOPES constant, but the guard did not flag it. The "
        "script-based exposure route is broken, and a quiet row would now pass."
    )


# ---------------------------------------------------------------------------
# the structural property that makes the guard hard to defeat
# ---------------------------------------------------------------------------


def test_constant_status_is_derived_from_its_decision_not_stored():
    """The failure mode was a constant asserting more certainty than its decision.

    Status is a computed property, so 'decided constant, open decision' is not a
    state the type can hold. If someone turns it back into a stored field, this
    test is what notices.
    """
    assert "status" not in Constant.__dataclass_fields__, (
        "Constant.status became a stored field. It must stay derived from the "
        "governing decision, or a constant can once again claim to be decided "
        "while its decision is open - which is how D-028 shipped."
    )
    for const in CONSTANTS:
        expected = "proposed" if status_of(const.governed_by) == "open" else "decided"
        assert const.status == expected
        assert const.status in CONSTANT_STATES


def test_status_of_rejects_an_unregistered_decision():
    """An unknown id must raise, never default to 'decided'."""
    with pytest.raises(KeyError, match="D-999"):
        status_of("D-999")


def test_every_constant_names_a_registered_decision():
    for const in CONSTANTS:
        assert const.governed_by in ALL_DECISIONS, (
            f"{const.name} cites {const.governed_by}, which is not registered"
        )


def test_no_decision_is_both_open_and_decided():
    overlap = set(OPEN_DECISIONS) & set(DECIDED_DECISIONS)
    assert not overlap, f"decisions listed as both open and decided: {sorted(overlap)}"


def test_decision_states_are_the_declared_vocabulary():
    for did in ALL_DECISIONS:
        assert status_of(did) in DECISION_STATES


# ---------------------------------------------------------------------------
# the registry cannot drift from the document reviewers actually read
# ---------------------------------------------------------------------------

#: Table cells may be emphasised - the open ones are bolded so they stand out to
#: a human reader - so strip markdown emphasis before matching.
_STATUS_ROW = re.compile(
    r"^\|\s*\**(D-\d{3})\**\s*\|\s*\**(open|decided)\**\s*\|", re.MULTILINE
)


def _documented_statuses(text: str) -> dict[str, str]:
    return dict(_STATUS_ROW.findall(text))


def test_status_table_parser_reads_emphasised_rows():
    """The parser is load-bearing: if it silently missed rows, the drift check
    would pass by finding nothing to compare."""
    sample = (
        "| D-001 | decided | plain |\n"
        "| **D-028** | **open** | emphasised |\n"
    )
    assert _documented_statuses(sample) == {"D-001": "decided", "D-028": "open"}


def test_decisions_md_documents_the_status_of_every_decision(decisions_md):
    documented = _documented_statuses(decisions_md)
    missing = [d for d in ALL_DECISIONS if d not in documented]
    assert not missing, (
        f"decisions absent from the Decision status table in DECISIONS.md: {missing}"
    )


def test_registry_and_decisions_md_agree_on_every_status(decisions_md):
    documented = _documented_statuses(decisions_md)
    disagreements = [
        f"{did}: DECISIONS.md says {documented[did]}, registry says {status_of(did)}"
        for did in ALL_DECISIONS
        if did in documented and documented[did] != status_of(did)
    ]
    assert not disagreements, (
        "the prose and the registry disagree about what has been decided:\n  - "
        + "\n  - ".join(disagreements)
    )


def test_every_decision_written_up_in_prose_is_registered(decisions_md):
    """A D-NNN can exist in the document without the registry knowing about it.

    That is the gap D-028 fell through, so close it in both directions.
    """
    written_up = set(re.findall(r"^\*\*(D-\d{3})", decisions_md, re.MULTILINE))
    unregistered = sorted(written_up - set(ALL_DECISIONS))
    assert not unregistered, (
        f"decisions written up in DECISIONS.md but absent from the registry: "
        f"{unregistered}"
    )


def test_every_decision_cited_by_a_row_is_registered(rows):
    cited: set[str] = set()
    for row in rows:
        for value in row.values():
            cited |= referenced_decisions(value)
    unregistered = sorted(cited - set(ALL_DECISIONS))
    assert not unregistered, (
        f"rows cite decisions that are not in the registry: {unregistered}"
    )


# ---------------------------------------------------------------------------
# visibility: the flag has to actually reach the terminal
# ---------------------------------------------------------------------------


def test_build_announces_every_proposed_constant(rows):
    buf = io.StringIO()
    with redirect_stdout(buf):
        build_table.print_decision_status(rows)
    printed = buf.getvalue()

    for const in CONSTANTS:
        assert const.name in printed
        assert const.governed_by in printed

    for const in proposed_constants():
        line = next(
            ln for ln in printed.splitlines() if ln.strip().startswith(const.name)
        )
        assert PROPOSED_FLAG.strip() in line, (
            f"{const.name} rests on an open decision but the build does not say so"
        )

    if not proposed_constants():
        assert PROPOSED_FLAG.strip() not in printed, (
            "nothing is proposed, yet the build still cries wolf"
        )


def test_build_names_the_baseline_rows_exposed_to_an_open_decision(rows):
    exposure = rows_exposed_to_open_decisions(rows)
    exposed = [
        row["row_id"] for row in rows
        if row.get("use_as") == "baseline" and row["row_id"] in exposure
    ]
    buf = io.StringIO()
    with redirect_stdout(buf):
        build_table.print_decision_status(rows)
    printed = buf.getvalue()

    for row_id in exposed:
        assert row_id in printed, (
            f"{row_id} is a baseline resting on an open decision, but the build "
            "does not name it"
        )
