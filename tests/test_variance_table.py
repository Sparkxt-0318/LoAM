"""Phase 0 guardrails.

These tests exist to stop the variance table degrading silently. They check the
schema contract, not the science: a number can be wrong and still pass here, but
it cannot be uncited, unharmonised, or quietly promoted from unverified to
load-bearing.
"""

from __future__ import annotations

import csv

import pytest

from loam import build_table
from loam.schema import COLUMN_NAMES, COMPONENTS, RULES
from loam.validate import ValidationError, assert_valid, validate_rows


@pytest.fixture(scope="module")
def rows():
    return build_table.load_rows()


# ---------------------------------------------------------------------------
# schema contract
# ---------------------------------------------------------------------------


def test_curated_rows_satisfy_schema(rows):
    problems = validate_rows(rows)
    assert not problems, "schema violations:\n  - " + "\n  - ".join(problems)


def test_every_row_has_a_citation_and_locator(rows):
    """The stated bar: a row without a citation does not go in the table."""
    for row in rows:
        assert row.get("citation", "").strip(), f"{row['row_id']} has no citation"
        assert row.get("doi_or_url", "").strip(), f"{row['row_id']} has no DOI/URL"
        assert row.get("locator", "").strip(), f"{row['row_id']} has no locator"


def test_every_row_documents_its_harmonization(rows):
    for row in rows:
        note = row.get("harmonization_note", "")
        assert len(note.split()) >= 12, (
            f"{row['row_id']} harmonization_note is too thin to audit: {note!r}"
        )


def test_row_ids_are_unique_and_prefixed(rows):
    ids = [r["row_id"] for r in rows]
    assert len(ids) == len(set(ids))
    for rid in ids:
        assert rid.startswith("VC-"), f"{rid} does not follow the VC-<COMP>-NNN pattern"


# ---------------------------------------------------------------------------
# the invariants that protect the detectability claim
# ---------------------------------------------------------------------------


def test_mean_dependent_rows_record_their_reference_stock(rows):
    """Mean dependence is the only route by which a wrong mean reaches an MDC."""
    for row in rows:
        if row.get("mean_dependent"):
            assert row.get("reference_stock_mg_c_ha") is not None, (
                f"{row['row_id']} is mean-dependent but records no reference stock, "
                "so the dependence cannot be audited"
            )


def test_no_baseline_row_is_mean_dependent_without_disclosure(rows):
    """Baselines may be mean-dependent, but never silently."""
    for row in rows:
        if row.get("use_as") == "baseline" and row.get("mean_dependent"):
            note = row.get("harmonization_note", "").lower()
            assert "mean" in note or "stock" in note, (
                f"{row['row_id']} is a mean-dependent baseline whose note does not "
                "explain the dependence"
            )


def test_systematic_rows_carry_no_standard_deviation(rows):
    """A bias summed into a variance budget is the classic Phase 0 error."""
    for row in rows:
        if row.get("error_kind") == "systematic":
            assert row.get("sd_mg_c_ha") is None, (
                f"{row['row_id']} is systematic but carries sd_mg_c_ha, which "
                "invites it to be summed into a variance budget"
            )


def test_unverified_rows_cannot_drive_the_osse(rows):
    for row in rows:
        if row.get("verification") == "unverified":
            assert row.get("use_as") == "placeholder_needs_pdf", (
                f"{row['row_id']} is unverified but marked '{row.get('use_as')}'"
            )


def test_baselines_are_in_scope(rows):
    for row in rows:
        if row.get("use_as") == "baseline":
            assert row.get("in_scope") is True, (
                f"{row['row_id']} is a baseline but is out of the locked scope"
            )


def test_baseline_rows_respect_the_scope_lock(rows):
    """Cropland, temperate, topsoil. Enforced in data, not in prose."""
    for row in rows:
        if row.get("use_as") != "baseline":
            continue
        assert row["land_use"] == "cropland", (
            f"{row['row_id']} is a baseline with land_use={row['land_use']!r}"
        )
        assert row["depth_top_cm"] >= 0 and row["depth_bottom_cm"] <= 30, (
            f"{row['row_id']} is a baseline outside 0-30 cm"
        )


# ---------------------------------------------------------------------------
# coverage: the table must be honest about what it does not have
# ---------------------------------------------------------------------------


def test_all_six_components_are_represented(rows):
    present = {r["component"] for r in rows}
    missing = set(COMPONENTS) - present
    assert not missing, f"components with no rows at all: {sorted(missing)}"


@pytest.mark.parametrize("component", COMPONENTS)
def test_component_baseline_coverage_is_declared(component, rows):
    """Documents which components are unusable today.

    Two components are knowingly without an in-scope baseline. This test pins
    that fact so that fixing it is a deliberate, visible change rather than
    something that drifts.
    """
    known_gaps = {"temporal", "between_plot_spatial"}
    has_baseline = any(
        r["component"] == component and r.get("use_as") == "baseline" for r in rows
    )
    if component in known_gaps:
        assert not has_baseline, (
            f"{component} now has a baseline - good news. Remove it from "
            "known_gaps here and close the gap in DECISIONS.md."
        )
    else:
        assert has_baseline, f"{component} lost its baseline row"


# ---------------------------------------------------------------------------
# the rules themselves actually bite
# ---------------------------------------------------------------------------


def test_rules_reject_a_row_with_no_citation(rows):
    bad = dict(rows[0])
    bad["citation"] = "   "
    with pytest.raises(ValidationError, match="R1-citation-required"):
        assert_valid([bad])


def test_rules_reject_a_bias_masquerading_as_a_variance(rows):
    bad = dict(rows[0])
    bad["error_kind"] = "systematic"
    bad["sd_mg_c_ha"] = 3.0
    with pytest.raises(ValidationError, match="R9-bias-not-a-variance"):
        assert_valid([bad])


def test_rules_reject_promoting_an_unverified_row(rows):
    bad = dict(rows[0])
    bad["verification"] = "unverified"
    bad["use_as"] = "baseline"
    with pytest.raises(ValidationError, match="R6-unverified-cannot-be-baseline"):
        assert_valid([bad])


def test_rules_reject_undeclared_mean_dependence(rows):
    bad = dict(rows[0])
    bad["harmonization_method"] = "pct_to_absolute_via_stock"
    bad["mean_dependent"] = False
    with pytest.raises(ValidationError, match="R5-mean-dependence-declared"):
        assert_valid([bad])


def test_every_rule_has_a_description():
    for rule in RULES:
        assert rule.description.strip()


# ---------------------------------------------------------------------------
# the emitted artifact matches the source
# ---------------------------------------------------------------------------


def test_csv_is_in_sync_with_yaml(rows, tmp_path):
    """Guards against a hand-edited CSV drifting away from the curated YAML."""
    committed = build_table.OUTPUT_CSV
    assert committed.exists(), "run `python -m loam.build_table` and commit the CSV"

    regenerated = tmp_path / "variance_table.csv"
    build_table.write_csv(rows, regenerated)

    assert regenerated.read_text(encoding="utf-8") == committed.read_text(
        encoding="utf-8"
    ), "data/variance_table.csv is stale - regenerate it with `python -m loam.build_table`"


def test_schema_doc_documents_every_column():
    """The schema doc is prose, so nothing but a test keeps it honest."""
    doc = (
        build_table.REPO_ROOT / "docs" / "variance_table_schema.md"
    ).read_text(encoding="utf-8")
    undocumented = [c for c in COLUMN_NAMES if f"`{c}`" not in doc]
    assert not undocumented, (
        f"columns missing from docs/variance_table_schema.md: {undocumented}"
    )


def test_csv_has_exactly_the_schema_columns():
    with build_table.OUTPUT_CSV.open(encoding="utf-8", newline="") as fh:
        header = next(csv.reader(fh))
    assert header == list(COLUMN_NAMES)
