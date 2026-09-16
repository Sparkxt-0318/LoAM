"""Phase 5 — the inverted audit. First implementation.

Ask "what sampling would this project's claim have required to be
detectable, and what would it have cost?" instead of "was this project's
sampling design adequate?" — because the second question needs a design
disclosure that :doc:`../docs/registry_corpus` shows almost nobody publishes,
and the first needs only what registries do publish: area, claimed rate,
interval, plus a variance structure, which is ours.

The method is not ours. It is VM0042's own Equation (2), Section 8.2.1 item
11 (D-057), which the methodology makes optional in the same sentence it
defines it — see ``docs/phase5_inverted_audit_design.md`` Section 1 for the
verbatim quote. Full design rationale: ``docs/phase5_inverted_audit_design.md``.
Adversarial review: ``docs/inverted_audit_redteam.md``. This module is the
first implementation of that design, with the red team's required changes
applied and the design doc's own Section 10 decisions resolved — see
DECISIONS.md D-059 through D-063 for what was decided and why, and
``docs/phase5_inverted_audit_results.md`` for the first run's numbers and
what they do and do not license claiming.

WHAT IS DELIBERATELY DIFFERENT FROM THE DESIGN DOC AS WRITTEN
---------------------------------------------------------------
1. **Headline metric is the implied-vs-applied uncertainty deduction, not
   required-n** (red team B-1). Required-n and Cost* remain here as
   intermediate quantities — ``AuditResult`` exposes both — but the top-line
   comparison a caller should quote is ``implied_deduction_pct`` against a
   project's own ``uncertainty_deduction_applied_pct``, because that pits the
   audit against the registry's own instrument rather than an optional
   planning aid a registry can wave away.
2. **Bisection, not fixed-point iteration** (red team C-3, demonstrated to
   cycle at small n). See ``n_req`` and ``loam.student_t``.
3. **The low-envelope rule is an explicit corner bound, stated as one in every
   docstring and every output field that uses it — never described as a
   confidence interval or a quantile** (red team C-2). Taking ``value_low``
   independently on every component is a deliberate worst-case-for-us corner
   of the joint space, not a joint lower quantile. A genuine joint quantile
   (red team C-2's preferred fix) is NOT implemented here; it would need a
   distributional assumption per component this module does not yet have
   evidence to defend, so the corner bound is used and labelled honestly
   instead of quietly upgraded.
4. **A ``not_auditable`` gate** for missing required inputs and for projects
   whose SOC pool is not separable from the rest of the credited ledger (red
   team A-3) — see ``gate``.
5. **A support/scale-mismatch ratio is reported, not silently ignored** (red
   team A-1). Every between-plot input in the live variance table is measured
   on research-plot support (order 0.01-0.2 ha); every project in the corpus
   quantifies at commercial-field or whole-project support (hundreds to
   hundreds of thousands of ha). That is many orders of magnitude, not the
   "order of magnitude" A-1 asks the audit to refuse past — refusing at that
   threshold would mean never running the audit on any real project, which is
   itself a finding worth being able to see rather than one this module
   should manufacture unilaterally. So the ratio is computed and returned on
   every result (``support_mismatch_ratio``) rather than gating on it. It is
   tracked as an open item, **G9** in DECISIONS.md, not resolved here.
6. **Within-plot and between-plot 0-30 cm inputs use D-059/D-060's resolution
   of design doc Sec 10 D-a**, not a table lookup, because no 0-30 cm
   within-plot row exists (G2) and only one Wuest series (``VC-BPS-007``) is a
   genuine 0-30 cm between-plot term. See ``assemble_components``.
7. **The headline design (paired vs. unpaired) is chosen by the same
   infimum-over-admissible-designs principle §2.3 already uses for C — not
   fixed by fiat** (D-060, revised from the design doc's own D-b
   recommendation). The design doc argues paired revisits are always cheaper
   because between-plot variance (~11.5%, NAPESHM) dominates relocation error
   (~6.65%, its own Sec 2.2 illustration). Checked directly rather than
   assumed: under this module's resolution of Sec 10 D-a (between-plot input
   is the narrower, genuinely-0-30cm Wuest series, ~3.1%, not the broader but
   off-depth NAPESHM figure) and D-e (relocation stays on the difference
   scale, undivided — see ``assemble_components``), UNPAIRED is sometimes the
   cheaper design. Both are always computed; whichever has the lower Cost* is
   reported as headline (the generous choice, §2.4's own logic extended to
   this axis), the other as sensitivity, and which one won is itself
   reported (``headline_design``) rather than assumed.
8. **Depth convention (ESM vs fixed depth) never enters the variance sum.**
   ``VC-BDC-001..004`` are systematic bias rows (``error_kind: systematic``);
   schema rule R9 forbids them a harmonised SD, and summing a bias into a
   variance budget is exactly what R9 exists to prevent. ESM is reported as
   the sole headline assumption (it is the generous branch, and a compliance
   requirement for VM0042 projects — Sec 4 of the design doc); the fixed-depth
   bias magnitudes are surfaced as a footnote string only (red team A-5), not
   as a parallel numeric branch.

WHAT THIS MODULE DOES NOT DO
-----------------------------
* No stochastic joint-quantile propagation (red team C-2's option (b)) — see
  point 3 above.
* No attempt to separate the SOC-only component of a project's credited rate
  from N2O/CH4/leakage/buffer-pool/uncertainty-deduction effects (Objection
  3) beyond the ``not_auditable`` gate for the clearest cases (CAR1513). The
  derived ``tau`` is the NET credited rate, understood and documented as an
  underestimate of the true SOC claim — which makes required-n an
  OVERestimate, i.e. the error is conservative in the direction the audit
  needs, and this module says so in its output rather than correcting for it.
* No stratification-aware variance reduction is estimated from first
  principles; ``required_stratification_efficiency`` reports what factor
  WOULD be needed, not what a specific stratification achieves.

``src/loam`` stays standard-library only (see ``loam.logvar`` and
``loam.student_t`` for why); this module imports only ``loam.student_t`` and
``loam.build_table`` from the package, plus the standard library.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from typing import Any

from . import student_t

# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

#: VM0042's own significance/power convention, Section 8.2.1 item 11: alpha
#: "frequently taken as 0.05" (two-sided), type II error "(e.g., 90%)"
#: (one-sided power). Used as the default everywhere in this module.
ALPHA_DEFAULT = 0.05
POWER_DEFAULT = 0.90

#: Cores per assay swept when optimising cost, design doc Sec 2.3. Recommended
#: there as C_max=30, "beyond ~10 the marginal variance reduction is
#: negligible because sigma_W^2/C is already below the irreducible terms" -
#: kept wide enough that the frontier visibly flattens rather than being cut
#: off mid-slope.
C_MAX = 30

#: Potash et al. 2025 (ERL, doi:10.1088/1748-9326/ada16c) Table 1(d). Mirrors
#: the identical constants in scripts/g3_bounding.py - same external source,
#: not re-derived, deliberately not imported across the scripts/src boundary
#: (scripts/ consumes loam, not the other way around).
COST_LOCATION_USD = 15.0
COST_ASSAY_USD = 20.0
COST_FIELD_VISIT_USD = 400.0

#: Registry deduction multipliers, k, applied to relative SE (D-057, all
#: verified from primary text). ACCU's is a footnote figure in VM0042 itself;
#: VM0042 v2.2's is Eq. 74 Sec 8.6.4; CAR SEP's is inferred from CAR1459's own
#: monitoring plan (z(70%) x 95% CI half-width / ER). The huge spread across
#: registries is itself a D-057 finding, not a modelling choice made here.
REGISTRY_K = {
    "accu": (0.253, "ACCU Scheme footnote rule, 40th percentile (D-057)"),
    "vm0042": (0.4307, "VM0042 v2.2 Sec 8.6.4 Eq. 74, t_0.667, 33.3rd percentile "
               "(D-057) - VERIFIED IN v2.2 ONLY; absent from the v2.0 text held"),
    "car_sep": (1.028, "CAR SEP v1.1, inferred from CAR1459's monitoring plan: "
                "z(70%) x 95% CI half-width / ER, 15.2nd percentile (D-057)"),
}


def registry_k(registry_name: str, protocol_name: str = "") -> tuple[float, str]:
    """Map a project's registry/protocol strings to its deduction multiplier.

    Matches on substrings because the corpus's own ``registry``/``protocol``
    fields are free text copied from source documents, not a controlled
    vocabulary (see ``data/registry/projects.yaml``). Raises rather than
    guessing when nothing matches, because a silent default here would let a
    project borrow another registry's severity - exactly the mistake D-057
    flags CAR SEP / VM0042 / ACCU as NOT being interchangeable on.
    """
    text = f"{registry_name} {protocol_name}".lower()
    if "vm0042" in text or "verra" in text or "vcs" in text:
        return REGISTRY_K["vm0042"]
    if "climate action reserve" in text or "car sep" in text or "soil enrichment protocol" in text:
        return REGISTRY_K["car_sep"]
    if "accu" in text or "clean energy regulator" in text:
        return REGISTRY_K["accu"]
    raise ValueError(
        f"no registry deduction rule for {registry_name!r} / {protocol_name!r}; "
        "add it to REGISTRY_K rather than guessing"
    )


#: tCO2e -> Mg C, the CO2:C molar mass ratio (44/12).
TCO2E_TO_MG_C = 44.0 / 12.0

#: Default reference SOC stock used only to convert relative (CV%) variance
#: components to absolute Mg C/ha so they can be summed against an absolute
#: Delta. DECISIONS.md's own stated range for temperate cropland 0-30 cm is
#: "roughly 40-80 Mg C/ha"; this is the midpoint. Every AuditResult carries
#: this value explicitly and flags mean-dependence (D-004's convention),
#: because it is exactly the kind of exposure D-004 exists to keep visible -
#: not a channel for the carbon model's untrustworthy mean TRAJECTORY (the
#: testbed's one hard invariant), just its well-constrained mean LEVEL.
DEFAULT_REFERENCE_STOCK_MG_C_HA = 60.0

#: VM0042's own control-site / density anchor, design doc Sec 5(a): the
#: densest disclosed campaign in the corpus, CAR1459's 1 point per 8 acres.
#: Used as the "densest real campaign ever disclosed" anchor for the support
#: sensitivity and for break-even-sigma's "plausible campaign" ceiling.
CAR1459_DENSITY_HA_PER_POINT = 8.0 * 0.404685642  # acres -> ha

#: Nominal support (ha) of the between-plot component this module uses as
#: primary (VC-BPS-007: "3.6 x 53 m plots", data/variance_components.yaml).
#: Used only to compute the support-mismatch ratio (point 5 above / red team
#: A-1); never used in the variance arithmetic itself.
BETWEEN_PLOT_NOMINAL_SUPPORT_HA = 3.6 * 53.0 / 10_000.0

#: Static detection-limit footnotes this audit inherits from Phase 0, per
#: design doc Objection 6: "a null is only informative against a stated
#: limit", and the audit's own nulls (an undetectable claim) inherit every
#: limit behind the components they are built from. Attached verbatim to
#: every AuditResult rather than re-derived per run.
INHERITED_DETECTION_LIMITS = (
    "analytical error vs. soil inorganic carbon: null established only above "
    "~6.4-7.6% analytical error (D-055); a carbonate-rich project below that "
    "band could have a true sigma_A this table understates.",
    "between-plot CV vs. climate/texture: invariance tested to about +/-2 CV "
    "points (climate) and +/-10 CV points (texture tercile split), not below "
    "(D-040).",
    "within-plot 0-30 cm CV is not a measured quantity at all (G2): the "
    "primary input here is an indirect estimate (D-043), not a detection "
    "limit on a direct measurement.",
)

# ---------------------------------------------------------------------------
# component selection - the low-envelope corner bound (Sec 2.4, red team C-2)
# ---------------------------------------------------------------------------


def generous_cv_pct(row: dict[str, Any]) -> tuple[float, str]:
    """The Sec 2.4 low-envelope value for one row, as a CORNER BOUND.

    Exact mapping (design doc Sec 2.4, unchanged by the red team - C-2
    objects to the WORDING, not the rule):

    * ``bias_direction == "inflates"`` (row is an upper bound): take
      ``value_low``, the smallest noise the evidence permits.
    * ``bias_direction == "deflates"`` (row already understates): take
      ``value`` as tabled; there is no lower bound to take.
    * ``bias_direction == "unknown"``: take ``value_low`` where present, else
      ``value`` - generous by default, and the caller is told so.

    This is a DELIBERATE WORST-CASE-FOR-US CORNER of the input space, not a
    probability statement (red team C-2). Taking every component's
    ``value_low`` independently does not correspond to any stated confidence
    level on the combined result, and nothing in this module's output should
    ever be read as one.
    """
    bias = row.get("bias_direction")
    central = row["cv_pct"]
    low = row.get("value_low")
    # value_low/value_high are only usable directly as CV%-scale bounds when
    # the row's own as-reported statistic already IS a CV percent (true for
    # every row this module reads that carries a low bound at all - VC-WPS-*,
    # VC-BPS-*, VC-TMP-*). A row reported on a different statistic (VC-ANA-001
    # is a MAE, VC-REL-001 a Mg_C_ha MAE) carries no printed low bound and
    # falls through to the harmonised `cv_pct` central value below regardless
    # of branch, so the scale mismatch that would otherwise matter here never
    # arises. Asserted, not silently assumed:
    if low is not None and not (row.get("statistic") == "cv_pct" and row.get("units") == "pct"):
        raise ValueError(
            f"{row.get('row_id')}: value_low is on the as-reported scale "
            f"({row.get('statistic')}/{row.get('units')}), not the harmonised "
            "cv_pct scale, and generous_cv_pct does not know how to convert it"
        )
    if bias == "deflates":
        return central, "deflates: tabled (harmonised) value taken as-is, already an understatement"
    if bias in ("inflates", "unknown"):
        if low is not None:
            return low, f"{bias}: lower bound taken as the generous corner ({low}% vs tabled {central}%)"
        return central, f"{bias}: no lower bound reported; tabled value taken"
    raise ValueError(f"{row.get('row_id')}: unrecognised bias_direction {bias!r}")


#: Design doc Sec 10 D-a's "recommended route, not taken": D-043's indirect
#: compositing-ratio estimate of single-core within-plot CV at 0-20/0-30 cm,
#: from the Wuest 3-core-vs-1-core residual ratio (1.785 against sqrt(3) =
#: 1.732). NOT a variance-table row - there is no 0-30 cm within-plot row
#: (G2) - so this is a module-level constant, not a CSV lookup, and is cited
#: exactly that way in every result that uses it. G8 applies: PNW dryland
#: only. Resolved by D-059/D-060.
WITHIN_PLOT_D043_INDIRECT = {
    "value": 8.5, "value_low": 8.0, "value_high": 9.0, "bias_direction": "unknown",
    "citation": "D-043 (docs/phase0_summary.md component 2); G8: PNW dryland only, indirect estimate",
}


def within_plot_cv_pct(rows_by_id: dict[str, dict], source: str = "d043_indirect") -> tuple[float, str]:
    """0-30 cm within-plot CV%. No table row exists at this depth (G2/D-a).

    ``"d043_indirect"`` (default, D-059/D-060's resolution): D-043's indirect
    estimate, generous end 8.0%.

    ``"layer_bracket"`` (Sec 10 D-a's stated alternative, "weaker but needs
    no new assumption"): the raw per-layer baseline rows (``VC-WPS-001``
    0-10 cm, ``VC-WPS-002`` 10-30 cm) used as bracket ENDPOINTS, not combined
    into a single SD - G2 forbids the latter, not the former.
    """
    if source == "d043_indirect":
        return (
            WITHIN_PLOT_D043_INDIRECT["value_low"],
            f"D-043 indirect estimate, generous end (G8: PNW dryland only): "
            f"{WITHIN_PLOT_D043_INDIRECT['value_low']}%",
        )
    if source == "layer_bracket":
        wps1, wps2 = rows_by_id["VC-WPS-001"], rows_by_id["VC-WPS-002"]
        low = min(wps1["value_low"], wps2["value_low"])
        return low, (
            "layer bracket, generous end (G2: VC-WPS-001/002 raw low bounds "
            f"as endpoints, not a validated 0-30 cm combination): {low}%"
        )
    raise ValueError(f"unknown within_plot source {source!r}")


def between_plot_cv_pct(rows_by_id: dict[str, dict], source: str = "wuest_0_30") -> tuple[float, str]:
    """0-30 cm between-plot CV%. Design doc Sec 10 D-a: only ``VC-BPS-007``
    (one Wuest PNW series) is a genuine 0-30 cm PURE between-plot term.
    ``VC-BPS-006`` (NAPESHM, broad evidence base) is 0-15 cm, and D-026
    forbids rescaling it to 0-30 cm - so it is offered here only as an
    explicitly off-depth sensitivity, never as the headline input.
    """
    if source == "wuest_0_30":
        cv, why = generous_cv_pct(rows_by_id["VC-BPS-007"])
        return cv, f"VC-BPS-007, 0-30 cm, single PNW series (G8-narrow): {why}"
    if source == "napeshm_0_15_off_depth_sensitivity":
        cv, why = generous_cv_pct(rows_by_id["VC-BPS-006"])
        return cv, (
            f"VC-BPS-006, 0-15 cm - D-026 FORBIDS treating this as a 0-30 cm "
            f"baseline; off-depth cross-check only, never headline: {why}"
        )
    raise ValueError(f"unknown between_plot source {source!r}")


# ---------------------------------------------------------------------------
# component assembly and sigma_d(C)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ComponentBreakdown:
    """The five variance-budget inputs to S(C), each a low-envelope CV% (Sec
    2.4), plus provenance strings for every one so a result is traceable back
    to a row id or a named constant without re-deriving it."""

    between_plot_cv_pct: float
    within_plot_cv_pct: float
    analytical_cv_pct: float
    temporal_cv_pct: float
    relocation_cv_pct: float
    reference_stock_mg_c_ha: float
    provenance: dict[str, str] = field(default_factory=dict)


def assemble_components(
    rows_by_id: dict[str, dict],
    *,
    within_plot_source: str = "d043_indirect",
    between_plot_source: str = "wuest_0_30",
    relocation_scale: str = "difference_scale",
    reference_stock_mg_c_ha: float = DEFAULT_REFERENCE_STOCK_MG_C_HA,
) -> ComponentBreakdown:
    """Assemble the five low-envelope CV% inputs S(C) is built from.

    ``relocation_scale`` resolves Objection 5 / design doc Sec 10 D-e, and it
    is LOAD-BEARING (a factor of ~sqrt(2) in S, i.e. up to ~2x in required n):

    * ``"difference_scale"`` (default, D-062's resolution): ``VC-REL-001``'s
      harmonised ``cv_pct`` (9.4%) is used AS TABLED. Its own harmonization
      note defines the source statistic as the mean of
      ``|SOC_initial - SOC_resampled|`` - i.e. it is ALREADY the SD of the
      one-time mismatch between the true original point and the actual
      (imperfectly relocated) revisit point. That is exactly what the paired
      formula's un-doubled ``sigma_R`` term represents (see ``s_of_c``): a
      single structural offset, not two independent occurrences the way
      within-plot/analytical/temporal error occur once at t0 and again,
      independently, at t1. So it is used undivided.
    * ``"per_observation_sqrt2"``: divides by sqrt(2), matching the design
      doc's OWN Sec 2.2 illustrative arithmetic ("sigma_R ~ 6.65% ... under
      its sqrt(2) caveat") - included so that comparison is reproducible
      rather than silently dropped. Using it makes paired revisits look
      relatively MORE favourable (smaller sigma_R), the opposite direction
      from what this module's default produces relative to the design doc's
      own worked illustration - see DECISIONS.md D-060 for why the default
      was changed from "paired is always headline" to "whichever design is
      cheaper is headline" once this was checked directly rather than
      assumed.
    """
    b_cv, b_why = between_plot_cv_pct(rows_by_id, between_plot_source)
    w_cv, w_why = within_plot_cv_pct(rows_by_id, within_plot_source)
    a_cv, a_why = generous_cv_pct(rows_by_id["VC-ANA-001"])
    t_cv, t_why = generous_cv_pct(rows_by_id["VC-TMP-003"])
    r_cv, r_why = generous_cv_pct(rows_by_id["VC-REL-001"])
    if relocation_scale == "difference_scale":
        r_why = (
            r_why + " (difference-scale, taken as-tabled per D-062: "
            "VC-REL-001's harmonised cv_pct is already the SD of the paired "
            "DIFFERENCE - see DIFFERENCE_SCALE below - so it enters S(C) "
            "undivided, matching the paired formula's own structure, which "
            "does not double it)"
        )
    elif relocation_scale == "per_observation_sqrt2":
        r_cv = r_cv / math.sqrt(2.0)
        r_why = (
            r_why + f" DIVIDED BY sqrt(2) -> {r_cv:.3f}% (per_observation_sqrt2: "
            "matches the design doc's own Sec 2.2 illustrative figure, not "
            "this module's default - see D-062)"
        )
    else:
        raise ValueError(f"unknown relocation_scale {relocation_scale!r}")
    return ComponentBreakdown(
        between_plot_cv_pct=b_cv,
        within_plot_cv_pct=w_cv,
        analytical_cv_pct=a_cv,
        temporal_cv_pct=t_cv,
        relocation_cv_pct=r_cv,
        reference_stock_mg_c_ha=reference_stock_mg_c_ha,
        provenance={
            "between_plot": b_why, "within_plot": w_why, "analytical": a_why,
            "temporal": t_why, "relocation": r_why,
        },
    )


#: D-062's resolution of design doc Sec 10 D-e / red team Objection 5: which
#: scale each formula input is on. ``difference_scale`` means the tabled SD
#: already measures a paired DIFFERENCE (occurs once in Var(Delta-hat), not
#: doubled); ``per_observation`` means the tabled SD measures a SINGLE
#: occasion/location's error (occurs at both t0 and t1, hence doubled in the
#: paired/unpaired formulas). Declared here, in code, and checked by
#: ``tests/test_inverted_audit.py`` - "a schema field, not prose" (Objection
#: 5's own words), implemented as a smaller-blast-radius module constant
#: rather than a src/loam/schema.py column, logged as a simplification in
#: D-062.
DIFFERENCE_SCALE = {
    "VC-REL-001": "difference_scale",   # relocation: baseline-vs-revisit, by definition
    "VC-BPS-007": "per_observation",    # between-plot: single-visit spatial term
    "VC-BPS-006": "per_observation",
    "VC-ANA-001": "per_observation",    # analytical: single determination
    "VC-TMP-003": "per_observation",    # temporal: the plot x occasion term itself
}


def s_of_c(components: ComponentBreakdown, cores_per_assay: int, paired: bool) -> float:
    """S(C), Mg C/ha - the SD of a SINGLE location's stock-change estimate at
    ``cores_per_assay`` composited cores per assay. This is VM0042 Eq. (1)/(2)'s
    ``S``, BEFORE the ``/sqrt(n)`` that turns it into an MDD - see ``n_req``.

    Paired revisit (design doc Sec 2.2, headline per D-060):

        S^2 = sigma_R^2 + 2*(sigma_W^2 + sigma_A^2)/C + 2*sigma_T^2

    Unpaired / re-randomised (sensitivity only, never headline):

        S^2 = 2*sigma_B^2 + 2*(sigma_W^2 + sigma_A^2)/C + 2*sigma_T^2

    Plain (non-log) variance addition is used here deliberately, matching
    VM0042's own Eq. (1)/(2) literally (S is an ordinary SD in Mg C/ha) -
    NOT the log-variance convention D-029 established elsewhere in Phase 0
    for regression modelling of variance. At the CV magnitudes this module
    combines (a few percent), the two conventions agree to several
    significant figures; the choice is about fidelity to VM0042's own
    instrument, not precision.
    """
    if cores_per_assay < 1:
        raise ValueError(f"cores_per_assay must be >= 1; got {cores_per_assay}")
    ref = components.reference_stock_mg_c_ha
    to_abs = lambda cv_pct: cv_pct / 100.0 * ref  # noqa: E731
    sigma_b = to_abs(components.between_plot_cv_pct)
    sigma_w = to_abs(components.within_plot_cv_pct)
    sigma_a = to_abs(components.analytical_cv_pct)
    sigma_t = to_abs(components.temporal_cv_pct)
    sigma_r = to_abs(components.relocation_cv_pct)
    c = float(cores_per_assay)
    coring_term = 2.0 * (sigma_w**2 + sigma_a**2) / c
    temporal_term = 2.0 * sigma_t**2
    if paired:
        variance = sigma_r**2 + coring_term + temporal_term
    else:
        variance = 2.0 * sigma_b**2 + coring_term + temporal_term
    return math.sqrt(variance)


# ---------------------------------------------------------------------------
# n_req - bisection on VM0042 Eq. (2)'s fixed point (red team C-3)
# ---------------------------------------------------------------------------


def n_req(
    s_mg_c_ha: float,
    delta_mg_c_ha: float,
    *,
    alpha: float = ALPHA_DEFAULT,
    power: float = POWER_DEFAULT,
    n_min: float = 2.0,
    growth_cap: float = 1.0e12,
) -> int:
    """Smallest integer ``n`` solving VM0042 Eq. (2), ``nu = n - 1``.

    ``n_req(n) = (S * (t_alpha,nu + t_beta,nu) / Delta)^2`` is DECREASING in
    ``n`` (more degrees of freedom -> smaller t-multiplier -> smaller RHS).
    Naive fixed-point iteration on a decreasing map can cycle instead of
    converging - demonstrated in ``docs/inverted_audit_redteam.md`` C-3 and
    pinned by ``tests/test_student_t.py::test_naive_fixed_point_iteration_cycles``.
    This solves ``g(n) = n_req(n) - n = 0`` by bisection instead, which is
    safe because ``g`` is monotone decreasing (n_req falls, ``-n`` falls
    faster) and therefore crosses zero exactly once.
    """
    if delta_mg_c_ha <= 0:
        raise ValueError(f"delta_mg_c_ha must be positive; got {delta_mg_c_ha}")
    if s_mg_c_ha < 0:
        raise ValueError(f"s_mg_c_ha must be non-negative; got {s_mg_c_ha}")

    def rhs(n: float) -> float:
        nu = max(n - 1.0, 1e-9)
        t_a = student_t.t_two_sided_critical(alpha, nu)
        t_b = student_t.t_one_sided_critical(power, nu)
        return (s_mg_c_ha * (t_a + t_b) / delta_mg_c_ha) ** 2

    def g(n: float) -> float:
        return rhs(n) - n

    lo, hi = n_min, n_min
    while g(hi) > 0.0:
        hi *= 2.0
        if hi > growth_cap:
            raise OverflowError(
                f"required n exceeds the search cap {growth_cap:.0e}; this "
                "delta is implausibly small relative to S for any admissible "
                "campaign"
            )
    # 40 steps on a bracket that has just been grown to bound the root gives
    # relative precision 1/2^40 - for any n this module ever computes (well
    # under 1e9), that resolves the integer answer with wide margin to spare.
    # Each step evaluates two Student's t quantiles (loam.student_t), and
    # n_req itself sits inside further bisections in this module
    # (cost_optimum sweeps C, break_even_* searches over a scale factor), so
    # keeping this tight matters for the whole module's runtime, not just one
    # call - see loam.student_t's identical note on _T_PPF_ITERATIONS.
    for _ in range(40):
        mid = (lo + hi) / 2.0
        if g(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    return math.ceil(hi)


# ---------------------------------------------------------------------------
# cost optimisation over C (Sec 2.3) - the infimum removes the (n, C) degeneracy
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CostOptimum:
    cores_per_assay: int
    n_req: int
    s_mg_c_ha: float
    cost_usd: float
    frontier: tuple[dict[str, Any], ...]


def cost_optimum(
    components: ComponentBreakdown,
    delta_mg_c_ha: float,
    *,
    paired: bool,
    c_max: int = C_MAX,
    alpha: float = ALPHA_DEFAULT,
    power: float = POWER_DEFAULT,
    cost_location_usd: float = COST_LOCATION_USD,
    cost_assay_usd: float = COST_ASSAY_USD,
) -> CostOptimum:
    """``Cost*`` (design doc Sec 2.3): the INFIMUM of cost over every
    admissible ``(n, C)`` design, C in [1, c_max]. Sampling density (``A/n``)
    is not a free third dimension - it falls out once n is solved - so this
    is the whole removal of the design doc's degeneracy: no point on the
    (n, C) trade-off curve is chosen, the minimum over the curve is reported,
    and the minimiser is a by-product exposed for inspection, not a claim
    about what any project should have done.
    """
    frontier: list[dict[str, Any]] = []
    best: dict[str, Any] | None = None
    for c in range(1, c_max + 1):
        s = s_of_c(components, c, paired)
        n = n_req(s, delta_mg_c_ha, alpha=alpha, power=power)
        cost = n * (c * cost_location_usd + cost_assay_usd)
        point = {"cores_per_assay": c, "n_req": n, "s_mg_c_ha": s, "cost_usd": cost}
        frontier.append(point)
        if best is None or cost < best["cost_usd"]:
            best = point
    assert best is not None  # c_max >= 1 is enforced by the range() above
    return CostOptimum(
        cores_per_assay=best["cores_per_assay"],
        n_req=best["n_req"],
        s_mg_c_ha=best["s_mg_c_ha"],
        cost_usd=best["cost_usd"],
        frontier=tuple(frontier),
    )


# ---------------------------------------------------------------------------
# break-even price, break-even noise scale, stratification efficiency
# ---------------------------------------------------------------------------


def break_even_carbon_price_usd_per_tco2e(cost_usd: float, revenue_tco2e: float) -> float | None:
    """Design doc Sec 5(b): the price at which Cost* exactly equals revenue.

    "Detecting the change this project claimed would have required a
    campaign costing more than the credits were worth at any price below
    $P/tCO2e." Price-free, which is why it is the recommended headline
    economic anchor rather than Cost*/revenue at an assumed price.
    """
    if revenue_tco2e <= 0:
        return None
    return cost_usd / revenue_tco2e


def _bisect_monotone_increasing(f, target: float, lo: float, hi: float, iters: int = 35) -> float:
    """Generic bisection for a function known to be monotone increasing on
    [lo, hi] with f(lo) <= target <= f(hi). Shared by the two break-even
    searches below so their monotonicity assumptions are asserted once."""
    if f(lo) > target:
        raise ValueError("f(lo) already exceeds target; bracket is wrong")
    if f(hi) < target:
        raise ValueError("f(hi) does not reach target; widen the bracket")
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def break_even_noise_scale(
    components: ComponentBreakdown, delta_mg_c_ha: float, *, paired: bool,
    cores_per_assay: int, n_plausible: float,
    alpha: float = ALPHA_DEFAULT, power: float = POWER_DEFAULT,
) -> float:
    """Red team A-2, generalised to the paired headline design.

    A-2 asks for the between-plot CV at which a project's own campaign
    becomes just sufficient - but the paired design (our headline, D-060)
    CANCELS between-plot variance entirely, so that quantity is undefined
    under the headline and only meaningful under the unpaired sensitivity
    (see ``break_even_between_plot_cv_pct`` below, which implements A-2
    literally for that case). This function is the paired-design analogue:
    the single multiplicative factor ``k`` by which EVERY component's CV
    would have to shrink together for ``n_plausible`` locations to suffice.
    ``k < 1`` means the project's own noise would have to be smaller than
    this table's generous corner bound already assumes; ``k >= 1`` means
    even a project noisier than that bound could still be detected at
    ``n_plausible``.
    """
    def n_at(k: float) -> float:
        scaled = replace(
            components,
            between_plot_cv_pct=components.between_plot_cv_pct * k,
            within_plot_cv_pct=components.within_plot_cv_pct * k,
            analytical_cv_pct=components.analytical_cv_pct * k,
            temporal_cv_pct=components.temporal_cv_pct * k,
            relocation_cv_pct=components.relocation_cv_pct * k,
        )
        s = s_of_c(scaled, cores_per_assay, paired)
        try:
            return float(n_req(s, delta_mg_c_ha, alpha=alpha, power=power))
        except OverflowError:
            return float("inf")

    lo, hi = 1e-6, 1.0
    while n_at(hi) < n_plausible:
        hi *= 2.0
        if hi > 1e9:
            return hi  # even an enormous noise scale still fits; report it as-is
    return _bisect_monotone_increasing(n_at, n_plausible, lo, hi)


def break_even_between_plot_cv_pct(
    components: ComponentBreakdown, delta_mg_c_ha: float, *,
    cores_per_assay: int, n_plausible: float,
    alpha: float = ALPHA_DEFAULT, power: float = POWER_DEFAULT,
) -> float:
    """Red team A-2, literally: the between-plot CV% at which
    ``n_plausible`` locations become just sufficient, UNDER THE UNPAIRED
    DESIGN (the only one of the two admissible designs where between-plot
    variance enters S(C) at all - see ``s_of_c``). Only meaningful as a
    sensitivity alongside the unpaired run; calling this against a paired
    S(C) would be comparing against a term that formula does not contain.
    """
    def n_at(cv_pct: float) -> float:
        scaled = replace(components, between_plot_cv_pct=cv_pct)
        s = s_of_c(scaled, cores_per_assay, paired=False)
        try:
            return float(n_req(s, delta_mg_c_ha, alpha=alpha, power=power))
        except OverflowError:
            return float("inf")

    lo, hi = 1e-6, 1000.0
    while n_at(hi) < n_plausible:
        hi *= 2.0
        if hi > 1e6:
            return hi
    return _bisect_monotone_increasing(n_at, n_plausible, lo, hi)


def required_stratification_efficiency(
    components: ComponentBreakdown, delta_mg_c_ha: float, *,
    cores_per_assay: int, n_plausible: float,
    alpha: float = ALPHA_DEFAULT, power: float = POWER_DEFAULT,
) -> float:
    """Red team B-2: the fraction ``r`` of the UNSTRATIFIED between-plot
    VARIANCE that stratification would have to remove for ``n_plausible``
    locations to suffice, under the unpaired design (see
    ``break_even_between_plot_cv_pct`` for why paired is excluded). ``r`` is
    a variance ratio, ``(cv_break_even / cv_tabled)^2`` - reported as the
    reduction FACTOR (1 - r), the more directly readable quantity: "would
    need to remove at least (1-r)*100% of the unstratified between-plot
    variance."
    """
    cv_break_even = break_even_between_plot_cv_pct(
        components, delta_mg_c_ha, cores_per_assay=cores_per_assay,
        n_plausible=n_plausible, alpha=alpha, power=power,
    )
    r = (cv_break_even / components.between_plot_cv_pct) ** 2
    return max(0.0, 1.0 - min(r, 1.0))


# ---------------------------------------------------------------------------
# implied-vs-applied uncertainty deduction - the B-1 headline
# ---------------------------------------------------------------------------


def implied_uncertainty_deduction_pct(
    k: float, s_mg_c_ha: float, n: float, delta_mg_c_ha: float,
) -> float:
    """The registry's OWN instrument (VM0042 Eq. 74 and its CAR/ACCU
    analogues, D-057), evaluated at a stated sampling intensity, per red team
    B-1: ``UNC = k * (SE / mean) * 100``, with ``SE = S(C)/sqrt(n)`` (the
    standard error of the estimated stock change) and ``mean`` the estimated
    change itself, ``Delta`` - mirroring the registries' own ratio structure,
    where the deduction scales the relative standard error of the claimed
    quantity, not of the underlying stock. This is directly comparable to a
    project's disclosed ``uncertainty_deduction_applied_pct`` WITHOUT waiting
    on any Sec 10 blocker (red team B-1's main selling point), because it
    uses the registry's own rule rather than asserting a required sample size
    is mandatory.
    """
    se = s_mg_c_ha / math.sqrt(n)
    return k * (se / delta_mg_c_ha) * 100.0


# ---------------------------------------------------------------------------
# project-level inputs, gating, and the top-level audit
# ---------------------------------------------------------------------------

#: Corpus field statuses this module will read a value from. `inferred` is
#: accepted (with lower-confidence provenance recorded), matching
#: tests/test_registry_corpus.py's own MUST_HAVE_VALUE/MUST_NOT_HAVE_VALUE
#: split - `not_disclosed` and `withheld` never carry a usable value there
#: either.
USABLE_STATUSES = {"stated", "inferred"}

HA_PER_ACRE = 0.404685642


def _field(project: dict, name: str) -> dict | None:
    block = project.get(name)
    if isinstance(block, dict) and "status" in block:
        return block
    return None


def _usable_value(project: dict, name: str) -> Any:
    block = _field(project, name)
    if block is None or block.get("status") not in USABLE_STATUSES:
        return None
    return block.get("value")


def project_area_ha(project: dict) -> float | None:
    block = _field(project, "area")
    value = _usable_value(project, "area")
    if value is None:
        return None
    units = (block or {}).get("units", "hectares")
    if units == "acres":
        return float(value) * HA_PER_ACRE
    return float(value)


def project_interval_years(project: dict, *, default_years: float = 5.0) -> tuple[float, str]:
    """Remeasurement interval Y. Falls back to VM0042's own 5-yearly
    remeasurement requirement (D-057) when the project itself does not
    disclose one, flagged as a fallback rather than a disclosure."""
    value = _usable_value(project, "remeasurement_interval_years")
    if value is not None:
        return float(value), "project-disclosed remeasurement interval"
    return default_years, f"FALLBACK: not disclosed, VM0042's own {default_years}-year requirement assumed (D-057)"


def derive_delta_mg_c_ha(project: dict, years: float) -> tuple[float | None, str]:
    """Delta = tau * Y, Mg C/ha, per design doc Sec 3. Two routes, in
    preference order:

    1. a directly stated/inferred ``claimed_soc_change_rate`` (Mg C/ha/y) -
       none in the current corpus, but preferred when present because it does
       not run through the tCO2e conversion or the net-of-deductions issue
       below;
    2. ``credits / area / years`` via whichever of ``claimed_abatement``
       (already a tCO2e/y RATE) or ``credits_issued`` (a tCO2e TOTAL) the
       project discloses.

    Objection 3 / red team A-3 / C-6: this derived tau is the NET CREDITED
    rate after N2O, CH4, fossil fuel, leakage, buffer withholding AND the
    uncertainty deduction itself - not the SOC change alone. That makes
    Delta SMALLER than the true SOC claim, which makes required-n LARGER
    than it should be: the error runs against the project, i.e. in the
    conservative direction this audit needs (Sec 8 Objection 3). Stated here,
    not corrected for.
    """
    stated = _usable_value(project, "claimed_soc_change_rate")
    if stated is not None:
        return float(stated) * years, "stated claimed_soc_change_rate x years"

    area = project_area_ha(project)
    if area is None or area <= 0:
        return None, "no usable project area"

    rate = _usable_value(project, "claimed_abatement")
    if rate is not None:
        tau = (float(rate) / TCO2E_TO_MG_C) / area
        return tau * years, (
            "derived: (claimed_abatement tCO2e/y / 3.667) / area x years - "
            "NET of N2O/CH4/leakage/buffer/uncertainty-deduction (Objection 3, conservative direction)"
        )

    credits = _usable_value(project, "credits_issued")
    if credits is not None and years > 0:
        tau = (float(credits) / TCO2E_TO_MG_C) / area / years
        return tau * years, (
            "derived: (credits_issued tCO2e total / 3.667) / area / years x years - "
            "NET of ledger deductions AND assumes credits were earned uniformly "
            "over exactly `years` (unverified timing assumption)"
        )
    return None, "no claimed_soc_change_rate, claimed_abatement or credits_issued usable"


#: Protocols/registries under which a project's credited pool is known, from
#: the corpus's own scope_note, NOT to be a primarily-SOC claim - i.e. where
#: `tau` derived from credits/area/years would test a fundamentally different
#: quantity than a power calculation on SOC stock change can speak to (red
#: team A-3). Matched by project_id because the corpus does not yet carry a
#: machine-readable "credited pool" field; see D-063.
NOT_SOC_SEPARABLE_PROJECT_IDS = {"CAR1513"}  # rice methane, not SOC (in_loam_scope: false)


def gate(project: dict) -> list[str]:
    """Reasons a project cannot be audited, empty if none. Red team A-3."""
    reasons: list[str] = []
    pid = project.get("project_id", "<unknown>")
    if pid in NOT_SOC_SEPARABLE_PROJECT_IDS:
        reasons.append(
            "SOC pool not separable from the credited ledger (red team A-3): "
            f"{project.get('scope_note', 'see corpus scope_note')}"
        )
    if project_area_ha(project) is None:
        reasons.append("no usable project area (area field not stated/inferred)")
    years, _ = project_interval_years(project)
    delta, _ = derive_delta_mg_c_ha(project, years)
    if delta is None:
        reasons.append(
            "no usable claimed rate (claimed_soc_change_rate, claimed_abatement "
            "and credits_issued are all missing, withheld or not_disclosed)"
        )
    elif delta <= 0:
        reasons.append(f"derived Delta is non-positive ({delta} Mg C/ha)")
    return reasons


# ---------------------------------------------------------------------------
# top-level result
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DesignResult:
    """Everything computed under one design assumption (paired or unpaired).

    ``is_paired`` names WHICH assumption this particular result is under; it
    is a property of the ``DesignResult`` itself, distinct from
    ``AuditResult.headline_design`` (a string naming WHICH of an
    ``AuditResult``'s two ``DesignResult``s, ``paired``/``unpaired``, won).
    """

    is_paired: bool
    s_mg_c_ha_at_c1: float
    optimum: CostOptimum


@dataclass(frozen=True)
class AuditResult:
    project_id: str
    auditable: bool
    gate_reasons: tuple[str, ...]

    area_ha: float | None = None
    interval_years: float | None = None
    interval_years_provenance: str | None = None
    delta_mg_c_ha: float | None = None
    delta_provenance: str | None = None

    components: ComponentBreakdown | None = None
    paired: DesignResult | None = None
    unpaired: DesignResult | None = None
    headline_design: str | None = None   # "paired" | "unpaired" - D-060, chosen by lower Cost*

    revenue_tco2e: float | None = None
    revenue_provenance: str | None = None
    break_even_price_usd_per_tco2e: float | None = None

    registry_k: float | None = None
    registry_k_provenance: str | None = None
    implied_deduction_pct_at_optimum: float | None = None
    applied_deduction_pct: float | None = None
    deduction_caveat: str | None = None

    break_even_noise_scale_at_car1459_density: float | None = None
    stratification_note: str | None = None

    support_mismatch_ratio: float | None = None
    qa_upper_bound_flag: bool | None = None
    qa_note: str | None = None
    esm_note: str = (
        "ESM (equivalent soil mass) is the sole headline depth-convention "
        "assumption: it is the generous branch (smallest sigma_D, design doc "
        "Sec 4) and a VM0042 compliance requirement, not an assumption "
        "(D-057). Fixed-depth systematic bias (VC-BDC-001..004: 6-17%, "
        "error_kind=systematic) is NOT summed into any variance figure here "
        "(schema rule R9) and is reported only as this footnote (red team A-5)."
    )
    detection_limits: tuple[str, ...] = INHERITED_DETECTION_LIMITS

    def to_dict(self) -> dict[str, Any]:
        def conv(v):
            if isinstance(v, CostOptimum):
                return {
                    "cores_per_assay": v.cores_per_assay, "n_req": v.n_req,
                    "s_mg_c_ha": round(v.s_mg_c_ha, 4), "cost_usd": round(v.cost_usd, 2),
                    "frontier": [
                        {k: (round(x, 4) if isinstance(x, float) else x) for k, x in p.items()}
                        for p in v.frontier
                    ],
                }
            if isinstance(v, DesignResult):
                return {
                    "is_paired": v.is_paired,
                    "s_mg_c_ha_at_c1": round(v.s_mg_c_ha_at_c1, 4),
                    "cost_optimum": conv(v.optimum),
                }
            if isinstance(v, ComponentBreakdown):
                return {
                    "between_plot_cv_pct": round(v.between_plot_cv_pct, 4),
                    "within_plot_cv_pct": round(v.within_plot_cv_pct, 4),
                    "analytical_cv_pct": round(v.analytical_cv_pct, 4),
                    "temporal_cv_pct": round(v.temporal_cv_pct, 4),
                    "relocation_cv_pct": round(v.relocation_cv_pct, 4),
                    "reference_stock_mg_c_ha": v.reference_stock_mg_c_ha,
                    "mean_dependent": True,
                    "provenance": v.provenance,
                }
            if isinstance(v, tuple):
                return list(v)
            if isinstance(v, float):
                return round(v, 6)
            return v

        out = {f: conv(getattr(self, f)) for f in self.__dataclass_fields__}
        if self.headline_design is not None:
            out["headline"] = out[self.headline_design]
        return out


def run_audit(
    project: dict,
    rows_by_id: dict[str, dict],
    *,
    within_plot_source: str = "d043_indirect",
    between_plot_source: str = "wuest_0_30",
    reference_stock_mg_c_ha: float = DEFAULT_REFERENCE_STOCK_MG_C_HA,
    c_max: int = C_MAX,
    alpha: float = ALPHA_DEFAULT,
    power: float = POWER_DEFAULT,
) -> AuditResult:
    """The full per-project audit: gate, assemble, solve, cost, and compare
    against the registry's own applied deduction. See the module docstring
    for what is and is not implemented, and DECISIONS.md D-059..D-063 for
    what each design choice below resolves."""
    pid = project.get("project_id", "<unknown>")
    reasons = gate(project)
    if reasons:
        return AuditResult(project_id=pid, auditable=False, gate_reasons=tuple(reasons))

    area = project_area_ha(project)
    years, years_why = project_interval_years(project)
    delta, delta_why = derive_delta_mg_c_ha(project, years)
    assert area is not None and delta is not None and delta > 0  # gate() already checked

    components = assemble_components(
        rows_by_id, within_plot_source=within_plot_source,
        between_plot_source=between_plot_source,
        reference_stock_mg_c_ha=reference_stock_mg_c_ha,
    )

    opt_paired = cost_optimum(components, delta, paired=True, c_max=c_max, alpha=alpha, power=power)
    paired_result = DesignResult(True, s_of_c(components, 1, paired=True), opt_paired)

    opt_unpaired = cost_optimum(components, delta, paired=False, c_max=c_max, alpha=alpha, power=power)
    unpaired_result = DesignResult(False, s_of_c(components, 1, paired=False), opt_unpaired)

    # D-060: the headline design is whichever is CHEAPER for these inputs -
    # the generous choice, by the same infimum-over-admissible-designs logic
    # Sec 2.3 already applies to C - not fixed to "paired" by fiat. See the
    # module docstring point 7 for why this differs from the design doc's own
    # D-b recommendation.
    if opt_paired.cost_usd <= opt_unpaired.cost_usd:
        headline_design, headline_result = "paired", paired_result
    else:
        headline_design, headline_result = "unpaired", unpaired_result
    opt_headline = headline_result.optimum

    # revenue and break-even price, scope-matched to `years` where possible
    # (Sec 5b / red team objection C-6: comparing Cost* against revenue over
    # a DIFFERENT span than the claim being tested would be its own error).
    revenue, revenue_why = None, None
    rate = _usable_value(project, "claimed_abatement")
    if rate is not None:
        revenue, revenue_why = float(rate) * years, "claimed_abatement (tCO2e/y) x years, scope-matched to Delta"
    else:
        credits = _usable_value(project, "credits_issued")
        if credits is not None:
            revenue, revenue_why = float(credits), (
                "credits_issued total - NOT scope-matched to `years`; may span "
                "a different period than the claim tested"
            )
    break_even_price = (
        break_even_carbon_price_usd_per_tco2e(opt_headline.cost_usd, revenue) if revenue else None
    )

    # implied-vs-applied uncertainty deduction (B-1 headline)
    k, k_why = registry_k(project.get("registry", ""), project.get("protocol", ""))
    implied = implied_uncertainty_deduction_pct(
        k, opt_headline.s_mg_c_ha, opt_headline.n_req, delta,
    )
    applied = _usable_value(project, "uncertainty_deduction_applied_pct")
    deduction_caveat = None
    if "vm0042" in f"{project.get('protocol','')}".lower() and "v2.0" in f"{project.get('protocol','')}".lower():
        deduction_caveat = (
            "project applied VM0042 v2.0; k=0.4307 is VERIFIED ONLY IN v2.2 "
            "(D-057) and is absent from the v2.0 text held - implied deduction "
            "below uses v2.2's k as the best available figure, not a confirmed "
            "rule for this project's actual crediting."
        )

    # break-even noise scale at the densest disclosed real-world campaign
    # (design doc Sec 5(a): CAR1459's 1 point per 8 acres) applied to this
    # project's own area, evaluated under whichever design is headline.
    n_plausible = area / CAR1459_DENSITY_HA_PER_POINT
    scale = break_even_noise_scale(
        components, delta, paired=(headline_design == "paired"),
        cores_per_assay=opt_headline.cores_per_assay,
        n_plausible=n_plausible, alpha=alpha, power=power,
    )
    strat_note = (
        "break_even_between_plot_cv_pct / required_stratification_efficiency "
        "are only defined under the UNPAIRED design (paired cancels "
        "between-plot variance by construction) - call them directly against "
        "`components` with paired=False, using either `paired` or `unpaired` "
        "above depending on which is currently headline (red team A-2, B-2)."
    )

    support_ratio = area / BETWEEN_PLOT_NOMINAL_SUPPORT_HA

    qa = _usable_value(project, "quantification_approach")
    qa_flag, qa_note = None, None
    if qa is not None:
        qa_flag = "measure_and_model" in str(qa)
        qa_note = (
            "QA1 (measure-and-model): required-n above is a SAMPLING-ONLY "
            "figure and OVERSTATES what this project's actual design needs, "
            "to the extent its validated model prediction error is smaller "
            "(Objection 1) - upper bound, not a point estimate."
            if qa_flag else
            "QA2 (measure-and-remeasure): required-n applies without qualification."
        )

    return AuditResult(
        project_id=pid, auditable=True, gate_reasons=(),
        area_ha=area, interval_years=years, interval_years_provenance=years_why,
        delta_mg_c_ha=delta, delta_provenance=delta_why,
        components=components, paired=paired_result, unpaired=unpaired_result,
        headline_design=headline_design,
        revenue_tco2e=revenue, revenue_provenance=revenue_why,
        break_even_price_usd_per_tco2e=break_even_price,
        registry_k=k, registry_k_provenance=k_why,
        implied_deduction_pct_at_optimum=implied, applied_deduction_pct=applied,
        deduction_caveat=deduction_caveat,
        break_even_noise_scale_at_car1459_density=scale, stratification_note=strat_note,
        support_mismatch_ratio=support_ratio,
        qa_upper_bound_flag=qa_flag, qa_note=qa_note,
    )
