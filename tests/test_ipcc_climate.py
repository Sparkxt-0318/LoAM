"""Every leaf and every short-circuit of IPCC Figure 3A.5.2.

The classifier is the one part of the IPCC work that could be done faithfully,
so it is worth pinning completely: all twelve regions reachable, the two
short-circuits that let a site classify without a variable we lack, and the
refusals that keep a proxy from being substituted for a missing one.
"""

from __future__ import annotations

import pytest

from loam.ipcc_climate import (
    CLIMATE_REGIONS,
    TEMPERATE_REGIONS,
    MissingClimateInput,
    classify,
    is_temperate,
)


# ---------------------------------------------------------------------------
# tropical branch: MAT > 18 AND <= 7 frost days
# ---------------------------------------------------------------------------


def test_tropical_montane_needs_only_elevation():
    assert classify(
        25, 1500, elevation_m=1500, frost_days_per_year=0
    ) == "Tropical Montane"


def test_tropical_wet_above_2000mm():
    assert classify(25, 2500, elevation_m=200, frost_days_per_year=0) == "Tropical Wet"


def test_tropical_moist_between_1000_and_2000mm():
    assert classify(25, 1500, elevation_m=200, frost_days_per_year=0) == "Tropical Moist"


def test_tropical_dry_at_or_below_1000mm():
    assert classify(25, 900, elevation_m=200, frost_days_per_year=0) == "Tropical Dry"


def test_map_exactly_2000_is_moist_not_wet():
    """The figure's tests are '> 2000' then '<= 2000 and > 1000'."""
    assert classify(25, 2000, elevation_m=0, frost_days_per_year=0) == "Tropical Moist"


def test_map_exactly_1000_is_dry_not_moist():
    assert classify(25, 1000, elevation_m=0, frost_days_per_year=0) == "Tropical Dry"


def test_elevation_exactly_1000_is_not_montane():
    """The test is '> 1000 m', so 1000 itself falls through."""
    assert classify(25, 1500, elevation_m=1000, frost_days_per_year=0) == "Tropical Moist"


def test_warm_site_with_many_frosts_is_not_tropical():
    """Both clauses must hold. 8 frost days fails the second."""
    assert classify(
        25, 1500, elevation_m=1500, frost_days_per_year=8, map_pet_ratio=0.5
    ) == "Warm Temperate Dry"


def test_frost_boundary_is_inclusive_at_seven():
    assert classify(
        25, 1500, elevation_m=200, frost_days_per_year=7
    ) == "Tropical Moist"


# ---------------------------------------------------------------------------
# temperate, boreal, polar
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mat, ratio, expected",
    [
        (15, 1.5, "Warm Temperate Moist"),
        (15, 0.5, "Warm Temperate Dry"),
        (5, 1.5, "Cool Temperate Moist"),
        (5, 0.5, "Cool Temperate Dry"),
    ],
)
def test_temperate_leaves(mat, ratio, expected):
    assert classify(mat, 800, map_pet_ratio=ratio) == expected


def test_mat_exactly_10_is_cool_not_warm():
    """'MAT > 10?' - so 10 itself goes to the cool branch.

    This boundary is load-bearing for NAPESHM, where site_mean_temp is rounded
    to whole degrees and 13 of 94 sites read exactly 10 (D-033).
    """
    assert classify(10, 800, map_pet_ratio=0.5) == "Cool Temperate Dry"


def test_mat_exactly_18_is_not_tropical():
    """'MAT > 18?' - 18 itself falls through, regardless of frost."""
    assert classify(
        18, 1500, map_pet_ratio=1.5, frost_days_per_year=0
    ) == "Warm Temperate Moist"


def test_map_pet_exactly_one_is_dry():
    """The test is '> 1', so a site exactly in balance is Dry."""
    assert classify(5, 800, map_pet_ratio=1.0) == "Cool Temperate Dry"


@pytest.mark.parametrize(
    "months, ratio, expected",
    [
        ([-20] * 12, 1.5, "Polar Moist"),
        ([-20] * 12, 0.5, "Polar Dry"),
        ([-20] * 11 + [12], 1.5, "Boreal Moist"),
        ([-20] * 11 + [12], 0.5, "Boreal Dry"),
    ],
)
def test_polar_and_boreal_leaves(months, ratio, expected):
    assert classify(-5, 400, map_pet_ratio=ratio, monthly_mean_temps_c=months) == expected


def test_one_month_at_exactly_ten_is_boreal():
    """'each mean monthly temperature < 10 °C?' - 10 is not < 10."""
    assert classify(
        -5, 400, map_pet_ratio=0.5, monthly_mean_temps_c=[-20] * 11 + [10]
    ) == "Boreal Dry"


def test_every_region_is_reachable():
    """No leaf is unreachable through a coding slip."""
    reached = {
        classify(25, 1500, elevation_m=1500, frost_days_per_year=0),
        classify(25, 2500, elevation_m=0, frost_days_per_year=0),
        classify(25, 1500, elevation_m=0, frost_days_per_year=0),
        classify(25, 500, elevation_m=0, frost_days_per_year=0),
        classify(15, 800, map_pet_ratio=1.5),
        classify(15, 800, map_pet_ratio=0.5),
        classify(5, 800, map_pet_ratio=1.5),
        classify(5, 800, map_pet_ratio=0.5),
        classify(-5, 400, map_pet_ratio=1.5, monthly_mean_temps_c=[-20] * 11 + [12]),
        classify(-5, 400, map_pet_ratio=0.5, monthly_mean_temps_c=[-20] * 11 + [12]),
        classify(-5, 400, map_pet_ratio=1.5, monthly_mean_temps_c=[-20] * 12),
        classify(-5, 400, map_pet_ratio=0.5, monthly_mean_temps_c=[-20] * 12),
    }
    assert reached == set(CLIMATE_REGIONS)


# ---------------------------------------------------------------------------
# the refusals - the whole point of the module
# ---------------------------------------------------------------------------


def test_missing_map_pet_is_refused_not_guessed():
    with pytest.raises(MissingClimateInput) as exc:
        classify(15, 800)
    assert exc.value.variable == "map_pet_ratio"


def test_missing_frost_days_is_refused_when_mat_above_18():
    with pytest.raises(MissingClimateInput) as exc:
        classify(25, 800, elevation_m=0)
    assert exc.value.variable == "frost_days_per_year"


def test_missing_elevation_is_refused_on_the_tropical_branch():
    with pytest.raises(MissingClimateInput) as exc:
        classify(25, 800, frost_days_per_year=0)
    assert exc.value.variable == "elevation_m"


def test_missing_monthly_temps_is_refused_when_mat_at_or_below_zero():
    with pytest.raises(MissingClimateInput) as exc:
        classify(-5, 400, map_pet_ratio=0.5)
    assert exc.value.variable == "monthly_mean_temps_c"


# ---------------------------------------------------------------------------
# the short-circuits that make a partly-equipped dataset usable
# ---------------------------------------------------------------------------


def test_frost_days_not_required_at_or_below_18c():
    """Why NAPESHM's missing frost column only bites on 13 of 94 sites."""
    assert classify(18, 800, map_pet_ratio=0.5) == "Warm Temperate Dry"
    assert classify(10, 800, map_pet_ratio=0.5) == "Cool Temperate Dry"


def test_monthly_temps_not_required_above_zero():
    """Why NAPESHM's missing monthly series costs nothing: min site MAT is 4 °C."""
    assert classify(4, 800, map_pet_ratio=0.5) == "Cool Temperate Dry"


def test_elevation_not_required_off_the_tropical_branch():
    assert classify(15, 800, map_pet_ratio=1.5) == "Warm Temperate Moist"


# ---------------------------------------------------------------------------
# scope lock
# ---------------------------------------------------------------------------


def test_temperate_set_is_the_four_temperate_regions():
    assert TEMPERATE_REGIONS == {
        "Warm Temperate Moist", "Warm Temperate Dry",
        "Cool Temperate Moist", "Cool Temperate Dry",
    }
    for region in CLIMATE_REGIONS:
        assert is_temperate(region) == (region in TEMPERATE_REGIONS)


def test_is_temperate_rejects_a_non_region():
    with pytest.raises(ValueError, match="not an IPCC default climate region"):
        is_temperate("Cool Temperate")  # missing the moist/dry half


# ---------------------------------------------------------------------------
# NaN: the refusal guarantee's blind spot
# ---------------------------------------------------------------------------

NAN = float("nan")


@pytest.mark.parametrize(
    "kwargs, expected_variable, was_fabricating",
    [
        # Every one of these silently returned a plausible-looking region before
        # NaN was gated, because each comparison against NaN is False and the
        # value therefore takes the 'No' branch at every test.
        (dict(mat_c=25, map_mm=800, frost_days_per_year=NAN, map_pet_ratio=1.5),
         "frost_days_per_year", "Warm Temperate Moist"),
        (dict(mat_c=25, map_mm=NAN, frost_days_per_year=0, elevation_m=100),
         "map_mm", "Tropical Dry"),
        (dict(mat_c=15, map_mm=800, map_pet_ratio=NAN),
         "map_pet_ratio", "Warm Temperate Dry"),
        (dict(mat_c=NAN, map_mm=800, map_pet_ratio=1.5),
         "mat_c", None),
        (dict(mat_c=25, map_mm=800, frost_days_per_year=0, elevation_m=NAN),
         "elevation_m", None),
    ],
)
def test_nan_is_refused_not_silently_branched(kwargs, expected_variable, was_fabricating):
    """A NaN must raise, naming the variable - never fall through to a leaf."""
    with pytest.raises(MissingClimateInput) as exc:
        classify(**kwargs)
    assert exc.value.variable == expected_variable


def test_nan_inside_monthly_temps_is_refused():
    """A sequence is only as good as its worst element."""
    with pytest.raises(MissingClimateInput) as exc:
        classify(-5, 400, map_pet_ratio=0.5, monthly_mean_temps_c=[-20] * 11 + [NAN])
    assert exc.value.variable == "monthly_mean_temps_c"


def test_empty_monthly_temps_is_refused():
    """all([]) is True, which would have made an empty series 'Polar'."""
    with pytest.raises(MissingClimateInput) as exc:
        classify(-5, 400, map_pet_ratio=0.5, monthly_mean_temps_c=[])
    assert exc.value.variable == "monthly_mean_temps_c"


def test_required_arguments_are_gated_too():
    """The two positional arguments are not reached by the per-branch checks."""
    for kwargs in (
        dict(mat_c=None, map_mm=800, map_pet_ratio=1.0),
        dict(mat_c=15, map_mm=None, map_pet_ratio=1.0),
    ):
        with pytest.raises(MissingClimateInput):
            classify(**kwargs)


# ---------------------------------------------------------------------------
# item 3: the Wuest result, pinned so a threshold edit cannot silently stale it
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mat", [9.0, 9.5, 10.0])
@pytest.mark.parametrize("ratio", [0.5, 0.7])
def test_wuest_pnw_below_the_ten_degree_cut_is_cool_temperate_dry(mat, ratio):
    """D-021: Wuest's PNW dryland sites, MAT at or below the `>10?` cut."""
    assert classify(mat, 350, map_pet_ratio=ratio) == "Cool Temperate Dry"


@pytest.mark.parametrize("mat", [10.5, 11.0])
@pytest.mark.parametrize("ratio", [0.5, 0.7])
def test_wuest_pnw_above_the_ten_degree_cut_is_warm_temperate_dry(mat, ratio):
    assert classify(mat, 350, map_pet_ratio=ratio) == "Warm Temperate Dry"


@pytest.mark.parametrize("mat", [9.0, 9.5, 10.0, 10.5, 11.0])
def test_wuest_is_temperate_either_side_of_the_boundary(mat):
    """The load-bearing claim in the D-021 update: temperate whichever way it falls."""
    assert is_temperate(classify(mat, 350, map_pet_ratio=0.6))
