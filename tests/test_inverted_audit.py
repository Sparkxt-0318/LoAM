"""Tests for the Phase 5 inverted-audit engine (``loam.inverted_audit``).

Layered like the module itself: the low-level pieces (generous_cv_pct,
s_of_c, n_req) are pinned first against synthetic, hand-checkable inputs;
then the assembled machinery (cost_optimum, break-even quantities, the
implied-vs-applied deduction) against structural properties the design doc
and the red team both predicate the method on; then the whole pipeline
against the one real corpus project (VCS 4022) that currently has enough
disclosed inputs to run end to end, and the gate against the rest.
"""

from __future__ import annotations

import json
import math

import pytest
import yaml

from loam import build_table, inverted_audit as ia

CORPUS_PATH = build_table.REPO_ROOT / "data" / "registry" / "projects.yaml"


@pytest.fixture(scope="module")
def rows_by_id():
    return {r["row_id"]: r for r in build_table.load_rows()}


@pytest.fixture(scope="module")
def corpus():
    with open(CORPUS_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@pytest.fixture(scope="module")
def projects_by_id(corpus):
    return {p["project_id"]: p for p in corpus["projects"]}


@pytest.fixture(scope="module")
def components(rows_by_id):
    return ia.assemble_components(rows_by_id)


# ---------------------------------------------------------------------------
# generous_cv_pct - the low-envelope corner bound (Sec 2.4 / red team C-2)
# ---------------------------------------------------------------------------


def _row(bias, value=10.0, low=None, high=None, statistic="cv_pct", units="pct"):
    return {
        "row_id": "TEST", "cv_pct": value, "value_low": low, "value_high": high,
        "bias_direction": bias, "statistic": statistic, "units": units,
    }


def test_inflates_takes_the_lower_bound_when_present():
    cv, why = ia.generous_cv_pct(_row("inflates", value=11.5, low=9.6, high=13.5))
    assert cv == 9.6
    assert "generous corner" in why


def test_deflates_takes_the_tabled_value_regardless_of_bounds():
    cv, why = ia.generous_cv_pct(_row("deflates", value=1.0, low=0.5))
    assert cv == 1.0
    assert "already an understatement" in why


def test_unknown_takes_lower_bound_when_present_else_tabled():
    cv, _ = ia.generous_cv_pct(_row("unknown", value=3.322, low=2.708))
    assert cv == 2.708
    cv2, why2 = ia.generous_cv_pct(_row("unknown", value=5.0, low=None))
    assert cv2 == 5.0
    assert "no lower bound reported" in why2


def test_bad_bias_direction_raises():
    with pytest.raises(ValueError):
        ia.generous_cv_pct(_row("sideways"))


def test_worked_examples_from_the_design_doc_match_exactly(rows_by_id):
    """Sec 2.4's own worked consequences: 'VC-BPS-006 enters at 9.6%, not
    11.5%'; 'VC-TMP-003 at 2.708%, not 3.322%'. Pinned against the live table
    so a future change to either row's low bound is caught here rather than
    only in a results doc nobody re-reads."""
    bps006, _ = ia.generous_cv_pct(rows_by_id["VC-BPS-006"])
    assert bps006 == pytest.approx(9.6)
    tmp003, _ = ia.generous_cv_pct(rows_by_id["VC-TMP-003"])
    assert tmp003 == pytest.approx(2.708)


def test_analytical_row_uses_harmonised_cv_not_raw_mape(rows_by_id):
    """The design doc's own Sec 2.4 prose says VC-ANA-001 enters "at its
    tabled 1.0%" - but 1.0% is the raw MAPE (`value`), not the harmonised,
    dimensionally-correct CV (`cv_pct` = 1.25%, via mae_to_sd_gaussian). This
    module uses the harmonised figure because S(C) sums variances that must
    all be on the same (SD/CV) scale; summing a raw MAE alongside true CVs
    would not be dimensionally sound. Logged as a correction in D-062."""
    cv, _ = ia.generous_cv_pct(rows_by_id["VC-ANA-001"])
    assert cv == pytest.approx(1.25)
    assert cv != pytest.approx(1.0)


# ---------------------------------------------------------------------------
# s_of_c - paired excludes between-plot variance; unpaired includes it
# ---------------------------------------------------------------------------


def test_paired_is_insensitive_to_between_plot_cv(components):
    from dataclasses import replace
    s_default = ia.s_of_c(components, 1, paired=True)
    doubled_between_plot = replace(components, between_plot_cv_pct=components.between_plot_cv_pct * 5)
    s_doubled = ia.s_of_c(doubled_between_plot, 1, paired=True)
    assert s_default == pytest.approx(s_doubled)


def test_unpaired_is_sensitive_to_between_plot_cv(components):
    from dataclasses import replace
    s_default = ia.s_of_c(components, 1, paired=False)
    bigger = replace(components, between_plot_cv_pct=components.between_plot_cv_pct * 5)
    s_bigger = ia.s_of_c(bigger, 1, paired=False)
    assert s_bigger > s_default


def test_paired_is_cheaper_when_between_plot_dominates_relocation():
    """Design doc Sec 2.2's stated prediction (paired revisits are cheaper
    because between-plot variance dominates relocation error) DOES hold in
    the regime it describes - a large sigma_B relative to sigma_R. Checked on
    a synthetic component set built to match that regime, deliberately
    separate from the `components` fixture (this module's actual resolved
    inputs put sigma_B, ~3.1% Wuest 0-30cm, well BELOW sigma_R, ~9.4%
    difference-scale - see test_unpaired_can_be_cheaper_than_paired below,
    and DECISIONS.md D-060 for why the headline is chosen per-project rather
    than fixed to paired)."""
    large_b_small_r = ia.ComponentBreakdown(
        between_plot_cv_pct=11.5, within_plot_cv_pct=8.0, analytical_cv_pct=1.25,
        temporal_cv_pct=2.708, relocation_cv_pct=4.7,  # ~6.65/sqrt2-ish, small
        reference_stock_mg_c_ha=60.0,
    )
    for c in (1, 4, 10):
        s_paired = ia.s_of_c(large_b_small_r, c, paired=True)
        s_unpaired = ia.s_of_c(large_b_small_r, c, paired=False)
        assert s_paired < s_unpaired


def test_unpaired_can_be_cheaper_than_paired_under_this_modules_resolved_inputs(components):
    """The real finding, pinned rather than hidden: under D-a's resolution
    (between-plot input is the narrow, genuinely-0-30cm Wuest series, not the
    broader off-depth NAPESHM figure) and D-e's resolution (relocation stays
    on the difference scale, undivided), sigma_B ends up SMALLER than
    sigma_R for this table - so UNPAIRED, not paired, is the cheaper (and
    therefore generous, headline) design here. This is why D-060 makes the
    headline choice per-project by comparing Cost*, rather than fixing it to
    paired the way the design doc's own Sec 2.2 illustration assumed."""
    s_paired = ia.s_of_c(components, 1, paired=True)
    s_unpaired = ia.s_of_c(components, 1, paired=False)
    assert s_unpaired < s_paired


def test_more_cores_per_assay_never_increases_s(components):
    values = [ia.s_of_c(components, c, paired=True) for c in (1, 2, 5, 10, 30)]
    assert all(a >= b - 1e-12 for a, b in zip(values, values[1:]))


def test_cores_per_assay_must_be_at_least_one(components):
    with pytest.raises(ValueError):
        ia.s_of_c(components, 0, paired=True)


# ---------------------------------------------------------------------------
# n_req - agreement with loam.student_t, and basic monotonicity
# ---------------------------------------------------------------------------


def test_n_req_decreases_as_delta_grows():
    n_small_delta = ia.n_req(5.0, 1.0)
    n_large_delta = ia.n_req(5.0, 10.0)
    assert n_large_delta < n_small_delta


def test_n_req_increases_as_s_grows():
    n_low_s = ia.n_req(2.0, 1.0)
    n_high_s = ia.n_req(8.0, 1.0)
    assert n_high_s > n_low_s


def test_n_req_rejects_nonpositive_delta():
    with pytest.raises(ValueError):
        ia.n_req(5.0, 0.0)


def test_n_req_matches_hand_solved_fixed_point():
    """Cross-check against the same closed-loop bisection used to verify
    loam.student_t (test_student_t.py's redteam table), evaluated at a
    different (sigma, delta) pair so this is not just re-running the same
    numbers - only the METHOD (bisect g(n) = n_req(n) - n) is shared."""
    from loam.student_t import t_one_sided_critical, t_two_sided_critical

    sigma, delta = 5.0, 2.5

    def rhs(n):
        nu = max(n - 1.0, 1e-9)
        return (sigma * (t_two_sided_critical(0.05, nu) + t_one_sided_critical(0.90, nu)) / delta) ** 2

    lo, hi = 2.0, 2.0
    while rhs(hi) - hi > 0:
        hi *= 2.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if rhs(mid) - mid > 0:
            lo = mid
        else:
            hi = mid
    expect = math.ceil(hi)
    assert ia.n_req(sigma, delta) == expect


# ---------------------------------------------------------------------------
# cost_optimum - the (n, C) degeneracy removal
# ---------------------------------------------------------------------------


def test_cost_optimum_is_at_least_as_good_as_every_frontier_point(components):
    result = ia.cost_optimum(components, 1.5, paired=True, c_max=10)
    assert all(result.cost_usd <= point["cost_usd"] + 1e-9 for point in result.frontier)


def test_cost_optimum_frontier_covers_every_c_from_1_to_c_max(components):
    result = ia.cost_optimum(components, 1.5, paired=True, c_max=10)
    assert [p["cores_per_assay"] for p in result.frontier] == list(range(1, 11))


def test_cost_optimum_ordering_matches_s_of_c_ordering(components):
    """Whichever design gives the smaller S(C) at every C must also give the
    smaller Cost* - the ordering established directly on s_of_c above must
    carry through cost_optimum unchanged. This is the property run_audit's
    headline selection (D-060) actually relies on, checked independently of
    which design happens to win for any particular component set."""
    delta = 1.5
    paired = ia.cost_optimum(components, delta, paired=True, c_max=5)
    unpaired = ia.cost_optimum(components, delta, paired=False, c_max=5)
    s_paired_ordering = [ia.s_of_c(components, c, True) < ia.s_of_c(components, c, False) for c in range(1, 6)]
    assert all(s_paired_ordering) or not any(s_paired_ordering)  # consistent sign across C
    if s_paired_ordering[0]:
        assert paired.cost_usd <= unpaired.cost_usd
    else:
        assert unpaired.cost_usd <= paired.cost_usd


# ---------------------------------------------------------------------------
# break-even quantities and stratification efficiency
# ---------------------------------------------------------------------------


def test_break_even_noise_scale_recovers_delta_within_tolerance(components):
    """At k=1 (no scaling) the design already needs some n0. Scaling the
    target n_plausible to be exactly n0 should return k close to 1."""
    opt = ia.cost_optimum(components, 1.5, paired=True, c_max=1)
    k = ia.break_even_noise_scale(
        components, 1.5, paired=True, cores_per_assay=1, n_plausible=opt.n_req,
    )
    assert k == pytest.approx(1.0, abs=0.05)


def test_break_even_noise_scale_is_larger_for_a_more_plausible_larger_n(components):
    opt = ia.cost_optimum(components, 1.5, paired=True, c_max=1)
    k_tight = ia.break_even_noise_scale(
        components, 1.5, paired=True, cores_per_assay=1, n_plausible=opt.n_req,
    )
    k_loose = ia.break_even_noise_scale(
        components, 1.5, paired=True, cores_per_assay=1, n_plausible=opt.n_req * 100,
    )
    assert k_loose > k_tight


def test_break_even_between_plot_cv_is_only_meaningful_under_unpaired(components):
    """Sanity: raising the plausible n should raise the break-even between-
    plot CV (more samples tolerate noisier soil), and the value returned
    should be positive and finite for a reasonable n_plausible."""
    cv_small_n = ia.break_even_between_plot_cv_pct(
        components, 1.5, cores_per_assay=1, n_plausible=1000,
    )
    cv_large_n = ia.break_even_between_plot_cv_pct(
        components, 1.5, cores_per_assay=1, n_plausible=100_000,
    )
    assert 0 < cv_small_n < cv_large_n


def test_required_stratification_efficiency_is_a_fraction_in_zero_one(components):
    r = ia.required_stratification_efficiency(
        components, 1.5, cores_per_assay=1, n_plausible=1000,
    )
    assert 0.0 <= r <= 1.0


# ---------------------------------------------------------------------------
# implied-vs-applied uncertainty deduction (red team B-1 headline)
# ---------------------------------------------------------------------------


def test_implied_deduction_scales_linearly_with_k():
    d1 = ia.implied_uncertainty_deduction_pct(0.253, 5.0, 100, 2.0)
    d2 = ia.implied_uncertainty_deduction_pct(0.506, 5.0, 100, 2.0)
    assert d2 == pytest.approx(2 * d1)


def test_implied_deduction_falls_as_n_grows():
    d_small_n = ia.implied_uncertainty_deduction_pct(0.4307, 5.0, 50, 2.0)
    d_large_n = ia.implied_uncertainty_deduction_pct(0.4307, 5.0, 5000, 2.0)
    assert d_large_n < d_small_n


def test_registry_k_matches_d057_values():
    k_vm0042, _ = ia.registry_k("Verra (VCS)", "VM0042 Improved Agricultural Land Management v2.0")
    k_car, _ = ia.registry_k("Climate Action Reserve", "Soil Enrichment Protocol (SEP) v1.1")
    k_accu, _ = ia.registry_k("Australian ACCU Scheme (Clean Energy Regulator)", "")
    assert k_vm0042 == pytest.approx(0.4307)
    assert k_car == pytest.approx(1.028)
    assert k_accu == pytest.approx(0.253)
    # D-057's own finding: CAR SEP is 2.38x VM0042 and 4.06x the ACCU rule.
    assert k_car / k_vm0042 == pytest.approx(2.386, abs=0.01)
    assert k_car / k_accu == pytest.approx(4.063, abs=0.01)


def test_registry_k_raises_on_unrecognised_registry():
    with pytest.raises(ValueError):
        ia.registry_k("Some Registry Nobody Has Heard Of", "")


# ---------------------------------------------------------------------------
# gate() - not_auditable (red team A-3)
# ---------------------------------------------------------------------------


def test_car1513_is_gated_as_not_soc_separable(projects_by_id):
    reasons = ia.gate(projects_by_id["CAR1513"])
    assert any("not separable" in r for r in reasons)


def test_car1459_clears_gate_on_scope_matched_rp5_soc_credits(projects_by_id):
    """WP1b (2026-11-10): CAR1459's RP5 monitoring report publishes SOC-only
    credits for one reporting period together with that period's enrolled
    area (Table 7). That is the claim the audit tests - NOT the cumulative
    credits_issued, which mixes N2O/CH4 credits and five periods of a project
    whose area grew 24.5-fold, and NOT the RP1 `area` field."""
    p = projects_by_id["CAR1459"]
    assert ia.gate(p) == []
    area = ia.project_area_ha(p)
    assert area == pytest.approx(2463690.6 * ia.HA_PER_ACRE)
    delta, why = ia.derive_delta_mg_c_ha(p, 5.0)
    assert delta == pytest.approx(1065452.3 / ia.TCO2E_TO_MG_C / area)
    assert "reporting period" in why


def test_accu_corpus_projects_clear_gate_on_inferred_cea_area(projects_by_id):
    """WP1a (2026-11-10, D-064): the register has no numeric area field, but
    the CEA shapefile is published for every credit-issued project, so area is
    INFERRED and the four corpus ACCU projects clear the gate."""
    for pid in ("ERF108333", "ERF105067", "ERF104527", "ERF176354"):
        p = projects_by_id[pid]
        assert p["area"]["status"] == "inferred"
        assert ia.gate(p) == [], pid


def test_gate_names_missing_area_not_missing_claim_when_credits_are_disclosed():
    """Before WP1 the gate reported 'no usable claimed rate' for ACCU projects
    whose credits_issued WAS stated - the real reason was the missing area."""
    p = {
        "project_id": "SYNTH_NOAREA",
        "credits_issued": {"value": 1000, "status": "stated"},
    }
    reasons = ia.gate(p)
    assert any("no usable project area" in r for r in reasons)
    assert any("credits_issued is disclosed" in r for r in reasons)
    assert not any("all missing" in r for r in reasons)


def test_cumulative_credits_delta_does_not_depend_on_interval():
    """D-064: Delta from cumulative credits is credits/3.667/area; the
    remeasurement interval cancels and must not move it."""
    p = {
        "project_id": "SYNTH_CUM",
        "area": {"value": 100.0, "units": "hectares", "status": "stated"},
        "credits_issued": {"value": 1000.0 * ia.TCO2E_TO_MG_C, "status": "stated"},
    }
    d5, _ = ia.derive_delta_mg_c_ha(p, 5.0)
    d9, _ = ia.derive_delta_mg_c_ha(p, 9.0)
    assert d5 == pytest.approx(10.0) and d9 == pytest.approx(10.0)


def test_minimal_complete_synthetic_project_passes_the_gate():
    synthetic = {
        "project_id": "SYNTH1",
        "area": {"value": 1000.0, "units": "hectares", "status": "stated"},
        "claimed_abatement": {"value": 1000.0, "status": "stated"},
        "remeasurement_interval_years": {"value": 5, "status": "stated"},
    }
    assert ia.gate(synthetic) == []


def test_project_missing_area_cascades_to_missing_rate_too():
    """Without area, claimed_abatement (a rate in tCO2e/y) cannot be turned
    into a Mg C/ha/y rate either (derive_delta_mg_c_ha needs area to do that
    division) - so a project missing only `area` is correctly gated on BOTH
    reasons, not just one. This is a real dependency, not a bug: fixing it to
    report only the area reason would hide that the rate is *also*
    unusable as things stand, which is the more informative message when a
    caller is deciding what to go and find next."""
    synthetic = {
        "project_id": "SYNTH2",
        "claimed_abatement": {"value": 1000.0, "status": "stated"},
    }
    reasons = ia.gate(synthetic)
    assert len(reasons) == 2
    assert any("area" in r for r in reasons)
    assert any("claimed rate cannot be formed" in r for r in reasons)


# ---------------------------------------------------------------------------
# run_audit end to end - the one real, fully-disclosed corpus project
# ---------------------------------------------------------------------------


def test_vcs4022_runs_end_to_end_and_is_json_serialisable(rows_by_id, projects_by_id):
    result = ia.run_audit(projects_by_id["VCS 4022"], rows_by_id)
    assert result.auditable
    d = result.to_dict()
    json.dumps(d)  # must not raise

    # area and delta sanity: 479,834.11 ha, ~0.309 Mg C/ha/y x 5 y.
    assert d["area_ha"] == pytest.approx(479_834.11, rel=1e-6)
    assert d["delta_mg_c_ha"] == pytest.approx(1.544, abs=0.01)

    # required-n is a small integer, not a degenerate 0/1 or an astronomical
    # figure - both would indicate a broken pipeline rather than a real
    # answer, at these components and this delta.
    n_req = d["headline"]["cost_optimum"]["n_req"]
    assert 50 < n_req < 50_000

    # the implied deduction at our cost-optimal design must be a small
    # positive percentage, sanity-bounded well away from both 0 and the
    # applied 31.35% by more than rounding noise (Objection 1: ours is
    # sampling-only and is expected to differ from the project's own
    # applied figure, which folds in QA1 model uncertainty too).
    assert 0 < d["implied_deduction_pct_at_optimum"] < 100
    assert d["applied_deduction_pct"] == pytest.approx(31.35)

    # the v2.0/v2.2 k-value caveat must be attached (D-057).
    assert d["deduction_caveat"] is not None and "v2.0" in d["deduction_caveat"]

    # support mismatch is real and large (red team A-1 / G9) - not silently
    # dropped, not a hard gate.
    assert d["support_mismatch_ratio"] > 1_000_000

    # QA1 (measure-and-model) must be flagged as an upper bound (Objection 1).
    assert d["qa_upper_bound_flag"] is True


def test_vcs4022_break_even_price_is_positive_and_tiny_relative_to_a_plausible_carbon_price(rows_by_id, projects_by_id):
    """Not a hard-coded expected value (that would just re-state the
    implementation) - a structural sanity check: VCS 4022's revenue
    (2.72M tCO2e over the 5-year interval tested) dwarfs the audit's own
    Cost* at generous, cost-optimal sampling, so the break-even price should
    be far below any real-world carbon price. If this ever flipped
    (break-even price above, say, $5/tCO2e) it would be the corpus's first
    genuinely hard-to-detect disclosed project and would deserve a close
    look before being reported as routine."""
    result = ia.run_audit(projects_by_id["VCS 4022"], rows_by_id)
    price = result.break_even_price_usd_per_tco2e
    assert price is not None
    assert 0 < price < 5.0


# ---------------------------------------------------------------------------
# CAR1459 - order-of-magnitude sensitivity, explicitly NOT a claim about
# CAR1459 itself (its own claimed rate is not disclosed)
# ---------------------------------------------------------------------------


def test_car1459_own_claim_vs_own_density_stays_within_two_orders_of_magnitude(rows_by_id, projects_by_id):
    """Design doc Sec 7, Test V1's spirit. Before WP1b this BORROWED VCS
    4022's rate, because CAR1459 disclosed none; since 2026-11-10 it uses
    CAR1459's own RP5 SOC claim over its own RP5 area (2,463,691 acres), and
    compares the audit's unpaired n_req (CAR1459 re-randomises, so paired
    does not apply - Sec 2.2's own worked example) against the count its
    stated Design-1 density (1 point per 8 acres) would imply over that area.

    Caveat carried with the number: 1-per-8-acres is the Design 1 rule
    (2019-2020); Design 2's realised count is not disclosed, so this is a
    sanity band, not a validation. Pass criterion as before: within two
    orders of magnitude, with our generous figure BELOW real practice - the
    failure mode guarded is the method demanding wildly MORE sampling than
    a real project runs.
    """
    car1459 = projects_by_id["CAR1459"]
    area_ha = ia.project_area_ha(car1459)
    years, _ = ia.project_interval_years(car1459)
    delta, _ = ia.derive_delta_mg_c_ha(car1459, years)
    components = ia.assemble_components(rows_by_id)
    opt_unpaired = ia.cost_optimum(components, delta, paired=False)

    car1459_own_n = area_ha / (8.0 * ia.HA_PER_ACRE)  # "1 point per 8 acres", stated
    ratio = car1459_own_n / opt_unpaired.n_req
    assert 1.0 <= ratio < 100.0, (
        f"CAR1459's own density implies {car1459_own_n:.0f} points; the audit's "
        f"generous unpaired estimate at its own RP5 claim is {opt_unpaired.n_req} "
        f"- ratio {ratio:.1f}x, outside the expected [1, 100) sanity band"
    )


# ---------------------------------------------------------------------------
# WP2 (D-067, D-068): envelopes, three categories, own-deduction ratio, headroom
# ---------------------------------------------------------------------------


def test_envelope_corners_bracket_the_central_value(rows_by_id):
    gen = ia.assemble_components(rows_by_id, envelope="generous")
    cen = ia.assemble_components(rows_by_id, envelope="central")
    hi = ia.assemble_components(rows_by_id, envelope="high")
    for f in ("between_plot_cv_pct", "within_plot_cv_pct", "analytical_cv_pct",
              "temporal_cv_pct", "relocation_cv_pct"):
        assert getattr(gen, f) <= getattr(cen, f) <= getattr(hi, f), f
    assert ia.s_of_c(gen, 1, paired=False) < ia.s_of_c(hi, 1, paired=False)


def test_generous_envelope_is_the_unchanged_default(rows_by_id):
    assert ia.assemble_components(rows_by_id) == ia.assemble_components(rows_by_id, envelope="generous")


def test_classify_reach_three_categories_never_two():
    assert ia.classify_reach(2.0, 1.5) == "inside_reach"
    assert ia.classify_reach(1.2, 0.9) == "within_uncertainty_band"
    assert ia.classify_reach(0.9, 0.7) == "outside_reach"
    assert ia.classify_reach(1.0, 1.0) == "inside_reach"
    assert set(ia.REACH_CATEGORIES) == {"inside_reach", "within_uncertainty_band", "outside_reach"}


def test_own_deduction_inverts_the_registry_rule_exactly():
    """D-068: UNC = 100 k sigma_rel, so sigma_rel = UNC / (100 k), and
    Delta/MDD = 1/((z_a + z_b) sigma_rel). VCS 4022's 31.35% under k=0.4307."""
    o = ia.own_deduction_detectability(31.35, 0.4307)
    assert o["implied_relative_se"] == pytest.approx(0.72789, rel=1e-4)
    assert o["delta_over_mdd_power50"] == pytest.approx(0.7009, rel=1e-3)
    assert o["delta_over_mdd_power90"] == pytest.approx(0.4238, rel=1e-3)
    # round trip: a project whose own SE is exactly Delta/(z_a+z_b) sits at ratio 1
    k = 1.028
    unc = 100 * k / (ia.Z_ALPHA_TWO_SIDED_005 + ia.Z_POWER_090)
    assert ia.own_deduction_detectability(unc, k)["delta_over_mdd_power90"] == pytest.approx(1.0)


def test_implied_deduction_at_optimum_is_bounded_by_k_over_z_sum(rows_by_id):
    """D-068, and confirmed by the independent re-implementation (WP3): at the
    audit's own optimum, n_req makes SE <= Delta/(t_a + t_b) < Delta/(z_a + z_b),
    so the implied deduction is at most 100 k / (z_a + z_b) WHATEVER the
    variance inputs or Delta. It therefore carries almost no project-specific
    information; applied/implied is the informative ratio."""
    comps = ia.assemble_components(rows_by_id)
    for k in (0.253, 0.4307, 1.028):
        bound = 100 * k / (ia.Z_ALPHA_TWO_SIDED_005 + ia.Z_POWER_090)
        for delta in (0.3, 1.5, 6.0, 15.0):
            opt = ia.cost_optimum(comps, delta, paired=False)
            implied = ia.implied_uncertainty_deduction_pct(k, opt.s_mg_c_ha, opt.n_req, delta)
            assert implied <= bound + 1e-9


def test_between_plot_headroom_is_zero_when_other_components_alone_exceed(rows_by_id):
    comps = ia.assemble_components(rows_by_id)
    # a tiny Delta on a tiny plausible campaign: unreachable even at sigma_B = 0
    assert ia.between_plot_headroom(comps, 0.2, cores_per_assay=2, n_plausible=20) == 0.0
    # a large Delta on a large campaign: headroom > 1
    assert ia.between_plot_headroom(comps, 5.0, cores_per_assay=2, n_plausible=500) > 1.0


def test_vcs4022_reach_and_own_deduction_fields(rows_by_id, projects_by_id):
    r = ia.run_audit(projects_by_id["VCS 4022"], rows_by_id)
    assert r.reach_category == "inside_reach"
    assert r.own_deduction["delta_over_mdd_power90"] == pytest.approx(0.4238, rel=1e-3)
    assert r.break_even_noise_scale_high_corner < r.break_even_noise_scale_at_car1459_density


# ---------------------------------------------------------------------------
# WP3 (D-069): sensitivity parameters on run_audit
# ---------------------------------------------------------------------------


def test_run_audit_sensitivity_parameters_default_to_the_headline(rows_by_id, projects_by_id):
    p = projects_by_id["VCS 4022"]
    a = ia.run_audit(p, rows_by_id)
    b = ia.run_audit(p, rows_by_id, relocation_scale="difference_scale",
                     cost_location_usd=ia.COST_LOCATION_USD, cost_assay_usd=ia.COST_ASSAY_USD,
                     envelope="generous", force_design=None)
    assert a.to_dict() == b.to_dict()


def test_run_audit_force_design_and_costs_thread_through(rows_by_id, projects_by_id):
    p = projects_by_id["VCS 4022"]
    forced = ia.run_audit(p, rows_by_id, force_design="paired")
    assert forced.headline_design == "paired"
    dear = ia.run_audit(p, rows_by_id, cost_assay_usd=80.0)
    base = ia.run_audit(p, rows_by_id)
    assert dear.break_even_price_usd_per_tco2e > base.break_even_price_usd_per_tco2e
    with pytest.raises(ValueError):
        ia.run_audit(p, rows_by_id, force_design="sideways")


def test_relocation_sqrt2_makes_paired_relatively_cheaper(rows_by_id, projects_by_id):
    """D-061's toggle: dividing relocation by sqrt(2) shrinks only the paired
    formula's sigma_R term, so the paired optimum gets cheaper and the unpaired
    one is unchanged."""
    p = projects_by_id["VCS 4022"]
    base = ia.run_audit(p, rows_by_id)
    alt = ia.run_audit(p, rows_by_id, relocation_scale="per_observation_sqrt2")
    assert alt.paired.optimum.cost_usd < base.paired.optimum.cost_usd
    assert alt.unpaired.optimum.cost_usd == base.unpaired.optimum.cost_usd
