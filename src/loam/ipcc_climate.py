"""IPCC 2006 default climate regions, Figure 3A.5.2.

Source: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 4
(Agriculture, Forestry and Other Land Use), Chapter 3 (Consistent Representation
of Lands), Annex 3A.5, **Figure 3A.5.2, page 3.39** - "Classification scheme for
default climate regions". Transcribed from the figure itself, not from memory or
a secondary source. The figure's own caption states the classification is based
on elevation, MAT, MAP, MAP:PET and frost occurrence.

Why this module exists at all, given it is not wired to anything
----------------------------------------------------------------
The scheme itself is implementable exactly; what is missing is the *data* to
feed it. NAPESHM publishes no PET and no frost-day count, so the 94 sites cannot
be classified - see DECISIONS.md D-033 for the full argument and D-034 for why
the classifier is nonetheless committed.

So the decision tree is coded here faithfully and tested against every leaf, and
:func:`classify` raises :class:`MissingClimateInput` naming the exact variable it
lacks rather than substituting a proxy. An unfed classifier that refuses to guess
is honest; a fed one that guessed would not be.

Design note: inputs are demanded lazily, only on the branch that actually needs
them. That is not an optimisation - it is what makes the Polar/Boreal
short-circuit visible. Monthly temperatures are required only when MAT <= 0 °C,
so a dataset without them can still classify every site warmer than that, which
is exactly NAPESHM's situation for that one branch.

Stdlib only: CI installs the `dev` extra and nothing heavier.
"""

from __future__ import annotations

#: The twelve default climate regions, exactly as named in Figure 3A.5.2.
CLIMATE_REGIONS = (
    "Tropical Montane",
    "Tropical Wet",
    "Tropical Moist",
    "Tropical Dry",
    "Warm Temperate Moist",
    "Warm Temperate Dry",
    "Cool Temperate Moist",
    "Cool Temperate Dry",
    "Boreal Moist",
    "Boreal Dry",
    "Polar Moist",
    "Polar Dry",
)

#: Regions that fall inside the project's "temperate" scope lock. Warm and Cool
#: Temperate only - Boreal and Polar are colder than the lock, Tropical warmer.
TEMPERATE_REGIONS = frozenset(
    {
        "Warm Temperate Moist",
        "Warm Temperate Dry",
        "Cool Temperate Moist",
        "Cool Temperate Dry",
    }
)


class MissingClimateInput(ValueError):
    """A variable the decision tree needs on this branch was not supplied.

    Deliberately an error rather than a fallback. Every proxy considered for the
    two variables NAPESHM lacks was shown to be wrong in kind, not merely
    imprecise (D-033), so a default here would launder a known-bad substitution
    into a published label.
    """

    def __init__(self, variable: str, why: str, problem: str = "was not supplied") -> None:
        super().__init__(f"{variable} is required {why}, and {problem}")
        self.variable = variable


def _finite(value, variable: str, why: str) -> float:
    """Reject None and NaN alike.

    NaN has to be caught explicitly, and the reason is nasty: every comparison
    against NaN is False, so an unguarded NaN does not error - it silently takes
    the 'No' branch at each test and falls out at a leaf. A NaN frost count made
    a 25 °C site 'Warm Temperate Moist'; a NaN precipitation fabricated
    'Tropical Dry' whole. Both look like ordinary answers.

    This is exactly the failure the module exists to prevent, arriving through
    the value rather than through a default, so it is checked at the same gate.
    """
    if value is None:
        raise MissingClimateInput(variable, why)
    if isinstance(value, float) and value != value:  # NaN
        raise MissingClimateInput(
            variable, why,
            "was NaN - which would otherwise take the 'No' branch at every test "
            "and fall out at a leaf, since all comparisons against NaN are False",
        )
    return value


def _need(value, variable: str, why: str):
    """Demand a per-branch optional input. Sequences are checked element-wise."""
    if isinstance(value, (list, tuple)):
        if not value:
            # all([]) is True, which would have made an empty series 'Polar'.
            raise MissingClimateInput(variable, why, "was an empty sequence")
        for element in value:
            _finite(element, variable, why)
        return value
    return _finite(value, variable, why)


def classify(
    mat_c: float,
    map_mm: float,
    *,
    elevation_m: float | None = None,
    frost_days_per_year: float | None = None,
    map_pet_ratio: float | None = None,
    monthly_mean_temps_c: list[float] | None = None,
) -> str:
    """Return the IPCC default climate region for one site.

    Parameters follow the figure's own vocabulary:

    ``mat_c``
        Mean annual temperature, °C.
    ``map_mm``
        Mean annual precipitation, mm.
    ``elevation_m``
        Required only on the tropical branch (``MAT > 18`` and few frosts).
    ``frost_days_per_year``
        Required only when ``mat_c > 18``; below that the first test is False on
        the temperature clause alone and frost cannot change the outcome.
    ``map_pet_ratio``
        MAP divided by potential evapotranspiration. Required on every
        non-tropical branch - it is the moist/dry split for all eight of them.
    ``monthly_mean_temps_c``
        The twelve monthly means. Required only when ``mat_c <= 0``, to separate
        Polar from Boreal.

    Raises :class:`MissingClimateInput` naming the variable if a needed one is
    absent or NaN.
    """
    # The two REQUIRED arguments are gated here, because `_need` only ever sees
    # the per-branch optional ones. Until this existed, the module's central
    # "refuses rather than defaults" guarantee did not cover its own required
    # inputs - a NaN MAP fabricated a whole leaf.
    mat_c = _finite(mat_c, "mat_c", "for every branch of the classification")
    map_mm = _finite(map_mm, "map_mm", "for every branch of the classification")

    # --- Is it tropical? MAT > 18 °C AND <= 7 days of frost/year -------------
    # Short-circuit on temperature first: when MAT <= 18 the conjunction is
    # False whatever the frost count, so a dataset with no frost column can
    # still classify every site at or below 18 °C.
    if mat_c > 18:
        frost = _need(
            frost_days_per_year,
            "frost_days_per_year",
            "because MAT > 18 °C puts this site on the tropical test, whose "
            "second clause is '<= 7 days of frost/year'",
        )
        if frost <= 7:
            return _tropical(map_mm, elevation_m)

    # --- Not tropical --------------------------------------------------------
    if mat_c > 10:
        return "Warm Temperate Moist" if _moist(map_pet_ratio, "Warm Temperate") \
            else "Warm Temperate Dry"

    if mat_c > 0:
        return "Cool Temperate Moist" if _moist(map_pet_ratio, "Cool Temperate") \
            else "Cool Temperate Dry"

    months = _need(
        monthly_mean_temps_c,
        "monthly_mean_temps_c",
        "because MAT <= 0 °C puts this site on the 'each mean monthly "
        "temperature < 10 °C?' test that separates Polar from Boreal",
    )
    if all(t < 10 for t in months):
        return "Polar Moist" if _moist(map_pet_ratio, "Polar") else "Polar Dry"
    return "Boreal Moist" if _moist(map_pet_ratio, "Boreal") else "Boreal Dry"


def _tropical(map_mm: float, elevation_m: float | None) -> str:
    elevation = _need(
        elevation_m,
        "elevation_m",
        "on the tropical branch, where 'elevation > 1000 m?' is the first test",
    )
    if elevation > 1000:
        return "Tropical Montane"
    if map_mm > 2000:
        return "Tropical Wet"
    # The figure states this as "MAP <= 2000 mm and > 1000 mm?", which the
    # preceding test has already halved; kept explicit to match the figure.
    if 1000 < map_mm <= 2000:
        return "Tropical Moist"
    return "Tropical Dry"


def _moist(map_pet_ratio: float | None, branch: str) -> bool:
    """The MAP:PET > 1 test, which decides moist vs dry on all eight non-tropical leaves."""
    ratio = _need(
        map_pet_ratio,
        "map_pet_ratio",
        f"on the {branch} branch, where 'MAP:PET > 1?' is the moist/dry split",
    )
    return ratio > 1


def is_temperate(region: str) -> bool:
    """Whether a region sits inside the project's temperate scope lock."""
    if region not in CLIMATE_REGIONS:
        raise ValueError(f"{region!r} is not an IPCC default climate region")
    return region in TEMPERATE_REGIONS
