"""Registry of the D-NNN decisions and of the constants they govern.

Why this module exists
----------------------
D-028 (the NAPESHM climate envelope) was written down as "OPEN - for the PI",
and then merged as the active constant driving two baseline rows anyway. Nothing
in the build or the test suite objected, because the decision's status lived only
in prose and the constant lived only in a script. Prose does not fail CI.

This module makes that failure mode structurally impossible, in the same way the
R6 rule locks the unverified LUCAS rows out of use:

* every decision has a machine-readable status, ``open`` or ``decided``;
* every load-bearing constant declares which decision governs it;
* a constant's own ``proposed`` / ``decided`` status is **derived** from that
  decision, never stored beside it.

The derived status is the point. If the status were a second field, a constant
could assert ``decided`` while its decision was still ``open`` - which is exactly
the state that shipped. Because :attr:`Constant.status` is computed, that state
cannot be represented at all.

The constants themselves live here rather than in ``scripts/`` so that the build
and the tests can see them without importing the scientific stack. The derivation
script imports them from here, so there is one definition, not two.

Kept to the standard library on purpose: CI installs only ``[dev]`` (pytest and
pyyaml), and the guard has to run there.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

#: Status of a D-NNN decision. `open` means nobody has chosen yet.
DECISION_STATES = ("open", "decided")

#: Status of a load-bearing constant. `proposed` means the value is a standing
#: recommendation that has not been ratified, and every build says so out loud.
CONSTANT_STATES = ("proposed", "decided")

#: Matches a decision reference anywhere in free prose, e.g. "... (D-027)".
DECISION_REF = re.compile(r"\bD-\d{3}\b")


# --------------------------------------------------------------------------
# The decisions
# --------------------------------------------------------------------------

#: Decisions nobody has made yet, with the question each one is still asking.
#: Anything governed by one of these is provisional, by definition.
#:
#: Keep in sync with the "Decision status" table in DECISIONS.md - a test
#: compares the two and fails if they drift.
OPEN_DECISIONS: dict[str, str] = {
    "D-054": (
        "Which laboratory error should the `analytical` component carry? "
        "Poeplau et al. 2022 report two nested figures - 1.2% MAPE for two "
        "technical replicates of the same milled sample, and 2.5% MAPE for a "
        "second aliquot of the same sieved sample, which contains the first. "
        "VC-ANA-001 carries the narrower one. Carried forward from D-036, "
        "which closed on the separate question of whether our figure disagrees "
        "with Potash et al.'s (it does not - 1.20x like for like). Gates G3: "
        "the two candidates put analytical error at 1.4-9.5% or 8.7-59.3% of "
        "the Wuest residual, on opposite sides of D-053's 0.089 threshold. "
        "EVIDENCE ADDED 2026-08-12 (D-057) WITHOUT CLOSING: VM0042 Sec 8.2.1.4 "
        "requires the laboratory to report analytical error 'determined by "
        "repeated analyses of the same sample' - Poeplau's NARROW figure, i.e. "
        "what VC-ANA-001 already carries. That is evidence for the against-side, "
        "which previously rested only on D-027's prefer-the-decomposed-term "
        "logic. It does not settle the question: what a registry asks a lab to "
        "report is not the error a monitoring programme incurs. Also relevant: "
        "D-055 returned NULL on whether analytical error varies with soil "
        "inorganic carbon, at a ~7% detection limit. Held open at the PI's "
        "instruction, 2026-08-12."
    ),
}

#: Decisions that have been made. Listed by id only; the reasoning is in
#: DECISIONS.md, which is the document a reviewer reads.
DECIDED_DECISIONS: tuple[str, ...] = (
    "D-001", "D-002", "D-003", "D-004", "D-005", "D-006", "D-007", "D-008",
    "D-009", "D-010", "D-011", "D-012", "D-013", "D-014", "D-015", "D-016",
    "D-017", "D-018", "D-019", "D-020", "D-021", "D-022", "D-023", "D-024",
    "D-025", "D-026", "D-027", "D-028", "D-029", "D-030", "D-031", "D-032",
    "D-033", "D-034", "D-035", "D-036", "D-037", "D-038", "D-039", "D-040",
    "D-041", "D-042", "D-043", "D-044", "D-045", "D-046", "D-047", "D-048",
    "D-049", "D-050", "D-051", "D-052", "D-053", "D-055", "D-056",
    "D-057", "D-058",
)

ALL_DECISIONS: tuple[str, ...] = tuple(
    sorted(set(OPEN_DECISIONS) | set(DECIDED_DECISIONS))
)


def status_of(decision_id: str) -> str:
    """Return ``open`` or ``decided``. Unknown ids are an error, not a default.

    Defaulting an unrecognised id to ``decided`` would let a typo silently
    launder an open question into a settled one.
    """
    if decision_id in OPEN_DECISIONS:
        return "open"
    if decision_id in DECIDED_DECISIONS:
        return "decided"
    raise KeyError(
        f"{decision_id} is not in the decision registry. Add it to "
        "OPEN_DECISIONS or DECIDED_DECISIONS in loam/decisions.py, and to the "
        "Decision status table in DECISIONS.md."
    )


def referenced_decisions(text: Any) -> set[str]:
    """Every D-NNN mentioned in a string. Non-strings reference nothing."""
    if not isinstance(text, str):
        return set()
    return set(DECISION_REF.findall(text))


def open_decisions_referenced(row: dict[str, Any]) -> set[str]:
    """Open decisions a curated row leans on, across all of its prose fields."""
    found: set[str] = set()
    for value in row.values():
        found |= referenced_decisions(value)
    return {d for d in found if d in OPEN_DECISIONS}


# --------------------------------------------------------------------------
# The constants those decisions govern
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Constant:
    """A value that drives a derived number, tied to the decision behind it."""

    name: str
    governed_by: str          # D-NNN
    value: Any
    summary: str
    #: Derivation scripts that consume this constant. Any row produced by one of
    #: them is exposed to this constant's decision whether or not the row says
    #: so - see :func:`rows_exposed_to_open_decisions` for why that matters.
    used_by: tuple[str, ...] = ()

    @property
    def status(self) -> str:
        """``proposed`` | ``decided`` - DERIVED, never stored.

        A stored status could contradict its decision. A derived one cannot: the
        moment D-028 is marked decided, CLIMATE_ENVELOPES stops printing the
        PROPOSED banner, with no second edit to remember.
        """
        return "proposed" if status_of(self.governed_by) == "open" else "decided"

    @property
    def is_proposed(self) -> bool:
        return self.status == "proposed"


# --- D-024: designs in which replicate EUs are true randomized replicates ---
HEADLINE_DESIGNS = frozenset({"Randomized complete block", "Completely randomized"})

# --- D-025: only 'Plots' is a plot-scale measurement ------------------------
HEADLINE_EU_TYPE = "Plots"

# --- D-026: fixed by NAPESHM protocol, documented in Norris et al. 2020 -----
DEPTH_TOP_CM, DEPTH_BOTTOM_CM = 0.0, 15.0

# --- D-028 (DECIDED 2026-08-09): IPCC temperature regime --------------------
# The private envelope (MAT <= 15 AND |lat| >= 30) is RETIRED. It had no answer
# to "why that threshold". Scope is now set by the IPCC 2006 default climate
# regions, Vol 4 Ch 3 Figure 3A.5.2 p. 3.39, classified per site in
# IPCC_SITE_REGIONS_FILE by scripts/derive_ipcc_regions.py.
#
# Only the TEMPERATURE regime is used, because only it is determinable: every
# non-tropical leaf of the figure is moisture-qualified and NAPESHM publishes no
# PET. That is sufficient rather than a compromise - Vol 4 Ch 5 Table 5.5
# indexes on `Temperate/Boreal`, which pools warm and cool, so this is exactly
# the axis Ch 5 needs. The moisture axis is missing and is never invented.
#
# Why "not Tropical" is enough to mean "Temperate/Boreal" here: NAPESHM's
# coldest site is 4 C, so under +/-0.5 C rounding no site can reach MAT <= 0 and
# the Boreal/Polar subtree is unreachable for this dataset. See D-028, D-039.
IPCC_SITE_REGIONS_FILE = "data/processed/ipcc_site_regions.json"

#: Regions outside the project's scope lock. A site classified into one of these
#: is excluded; a site the tree could not resolve is retained, because for this
#: dataset "unresolved" still implies Temperate/Boreal on the temperature axis.
IPCC_OUT_OF_SCOPE_REGIONS = frozenset(
    {"Tropical Montane", "Tropical Wet", "Tropical Moist", "Tropical Dry"}
)

#: Human-readable statement of what the G1 rows are now scoped to. Quoted into
#: the rows themselves so the scope travels with the number.
IPCC_SCOPE_LABEL = (
    "IPCC 2006 temperature regime Temperate/Boreal (not Tropical); "
    "moisture regime undetermined"
)


G1_SCRIPT = "scripts/derive_g1_napeshm.py"

CONSTANTS: tuple[Constant, ...] = (
    Constant(
        "IPCC_OUT_OF_SCOPE_REGIONS",
        "D-028",
        IPCC_OUT_OF_SCOPE_REGIONS,
        f"climate scope for the G1 headline: {IPCC_SCOPE_LABEL}",
        (G1_SCRIPT, "scripts/derive_ipcc_regions.py"),
    ),
    Constant(
        "HEADLINE_DESIGNS",
        "D-024",
        HEADLINE_DESIGNS,
        "experimental designs whose replicates are true randomized replicates",
        (G1_SCRIPT,),
    ),
    Constant(
        "HEADLINE_EU_TYPE",
        "D-025",
        HEADLINE_EU_TYPE,
        "experimental-unit type carrying the headline",
        (G1_SCRIPT,),
    ),
    Constant(
        "DEPTH_CM",
        "D-026",
        (DEPTH_TOP_CM, DEPTH_BOTTOM_CM),
        "sampled layer the G1 rows are scoped to",
        (G1_SCRIPT,),
    ),
)

CONSTANTS_BY_NAME: dict[str, Constant] = {c.name: c for c in CONSTANTS}


def proposed_constants() -> tuple[Constant, ...]:
    """Live constants whose governing decision is still open."""
    return tuple(c for c in CONSTANTS if c.is_proposed)


def rows_exposed_to_open_decisions(
    rows: list[dict[str, Any]],
) -> dict[str, set[str]]:
    """Map row_id -> open decisions the row depends on. Two routes, not one.

    Prose alone is not enough, and the table proves it: ``VC-BPS-005`` mentions
    D-028 and ``VC-BPS-006`` does not, though both come out of the same filter
    cascade under the same unratified envelope. A guard that only read prose
    would clear the row that stayed quiet - rewarding silence, which is the
    opposite of the point.

    So a row is exposed if EITHER

    * it cites an open decision anywhere in its prose, OR
    * it was produced by a derivation script that consumes a proposed constant.

    The second route needs no cooperation from the row, which is what makes it
    worth having.
    """
    exposed: dict[str, set[str]] = {}
    for row in rows:
        found = open_decisions_referenced(row)

        locator = row.get("locator") or ""
        if isinstance(locator, str):
            for const in proposed_constants():
                if any(script in locator for script in const.used_by):
                    found.add(const.governed_by)

        if found:
            exposed[row["row_id"]] = found
    return exposed


#: Printed by the build for any constant resting on an open decision. Worded to
#: match the existing NO BASELINE flag, because it plays the same role: a
#: standing admission, on every run, that something is not settled.
PROPOSED_FLAG = "  <-- PROPOSED, NOT DECIDED"
