"""Schema for the Phase 0 variance-component reference table.

This module is the SINGLE SOURCE OF TRUTH for the table's columns, enumerations
and integrity rules. The schema doc (``docs/variance_table_schema.md``), the
curated source (``data/variance_components.yaml``) and the emitted artifact
(``data/variance_table.csv``) are all validated against what is defined here, so
they cannot silently drift apart.

Design premise
--------------
The testbed quantifies DETECTABILITY, not soil carbon. Minimum detectable change
(MDC) is a function of the variance structure of the measurement process, not of
the mean SOC trajectory produced by whatever carbon model sits underneath. Every
column below exists to keep that property auditable:

* ``mean_dependent`` marks any row whose harmonised value required a mean SOC
  stock to compute. Those rows are the only channel through which an incorrect
  mean can contaminate an MDC estimate, and they must stay individually visible.
* ``error_kind`` separates random dispersion from systematic bias. A bias term is
  not a variance term and must never be summed into a variance budget.
* ``verification`` records how deeply each number was checked. A number read from
  an abstract is not the same evidence as a number read from a table in the PDF.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

# --------------------------------------------------------------------------
# Controlled vocabularies
# --------------------------------------------------------------------------

COMPONENTS = (
    "analytical",             # 1. laboratory / analytical determination error
    "within_plot_spatial",    # 2. variance among points inside one plot
    "between_plot_spatial",   # 3. variance among plots
    "temporal",               # 4. month-to-month / within-year temporal variance
    "relocation",             # 5. error added by not resampling the same point
    "depth_bd_convention",    # 6. fixed depth vs equivalent soil mass, bulk density
)


@dataclass(frozen=True)
class ComponentDefinition:
    """What a component measures, stated independently of its name.

    ``VC-TMP-002`` sat under ``temporal`` for several PRs while reporting
    variance between replicate experimental units. It was correctly
    transcribed, correctly cited, and filed under the wrong component - because
    the number appeared BESIDE the temporal figure in the source. Nothing
    caught it: R6 tests locators, D-032 tests decision status, the staleness
    test compares YAML with CSV. None of them asks whether a number is what its
    component says it is.

    The fix is to make every component and every row state its **axis of
    variation** - the thing that differs between the two measurements being
    compared - in the same vocabulary, so a mismatch is mechanically visible.
    """

    name: str
    #: Plain language: what varies, and what is held fixed while it varies.
    definition: str
    #: Phrases that name this component's axis. A row's ``quantity_definition``
    #: is matched against these; see :data:`AXIS_TRIGGERS` for how the axis
    #: phrase is located inside the sentence.
    varies_across: tuple[str, ...]


#: Words that introduce the axis of variation. A ``quantity_definition`` must
#: contain at least one, and the EARLIEST component marker after the earliest
#: trigger decides which component the definition reads as. That convention is
#: what makes the check structural rather than a guess: "variation between
#: sampling occasions at one fixed plot" resolves to `temporal` because
#: `sampling occasions` comes before `plot`, not because a human judged it.
AXIS_TRIGGERS = ("between ", "across ", "among ")

#: How far after a trigger word to look for a component marker. Long enough for
#: "between replicate experimental units under identical management", short
#: enough that a later subordinate clause is not mistaken for a second axis.
AXIS_WINDOW_CHARS = 80

COMPONENT_DEFINITIONS: tuple[ComponentDefinition, ...] = (
    ComponentDefinition(
        "analytical",
        "Variation between repeated DETERMINATIONS OF THE SAME MATERIAL - the "
        "same soil, milled and homogenised, measured more than once or "
        "processed more than one way. Everything spatial is held fixed: there "
        "is only one field location involved.",
        ("replicate determinations", "technical replicates", "duplicate "
         "determinations", "repeat determinations", "determinations of the "
         "same sample", "analyses of the same sample", "replicate "
         "determinations of the same", "aliquots", "sample preparation "
         "treatments", "drying treatments", "grinding treatments",
         "laboratories"),
    ),
    ComponentDefinition(
        "within_plot_spatial",
        "Variation between SAMPLING POSITIONS INSIDE ONE PLOT, measured at one "
        "time by one laboratory. The plot, the date and the method are all "
        "held fixed; only the position within the plot differs.",
        ("cores within", "points within", "sampling positions within",
         "sampling points within", "cores taken within", "subsamples within",
         "microplots within", "locations within a plot",
         "positions within a plot"),
    ),
    ComponentDefinition(
        "between_plot_spatial",
        "Variation between WHOLE PLOTS or experimental units under the same "
        "management, at one time. The management, the date and the method are "
        "held fixed; only which plot differs. Note this is a different axis "
        "from within_plot_spatial, and a figure that pools the two belongs to "
        "neither.",
        ("plots", "experimental units", "replicate experimental units",
         "replicate plots", "fields"),
    ),
    ComponentDefinition(
        "temporal",
        "Variation between SAMPLING OCCASIONS AT THE SAME PLACE - the same "
        "plot revisited, or a whole field resampled on a later date. Position "
        "and method are held fixed; only when the sample was taken differs.",
        ("sampling occasions", "sampling dates", "sampling campaigns",
         "occasions", "months", "revisits of the same", "visits to the same",
         "successive visits", "dates"),
    ),
    ComponentDefinition(
        "relocation",
        "Variation between AN ORIGINAL POSITION AND A DISPLACED ONE when a "
        "point is resampled without being relocated exactly. Time is not the "
        "axis here even though resampling happens later; the axis is the "
        "offset in space between baseline and revisit positions.",
        ("original position", "original profile position", "baseline position",
         "baseline location", "revisit locations", "relocation distances",
         "offset resample", "displaced position"),
    ),
    ComponentDefinition(
        "depth_bd_convention",
        "Difference between ACCOUNTING CONVENTIONS applied to the same soil - "
        "fixed depth versus equivalent soil mass, or one bulk-density "
        "treatment versus another. Nothing about the field sampling differs; "
        "the two numbers come from the same soil under different bookkeeping.",
        ("accounting conventions", "depth conventions", "conventions",
         "fixed-depth and equivalent-soil-mass", "sampling increments"),
    ),
)

COMPONENT_DEFINITIONS_BY_NAME: dict[str, ComponentDefinition] = {
    c.name: c for c in COMPONENT_DEFINITIONS
}


def read_axis(quantity_definition: str) -> tuple[str, str | None, frozenset[str]]:
    """Return ``(axis_phrase, primary_component, all_components_matched)``.

    ``primary_component`` is whichever component's marker appears EARLIEST in
    the axis phrase, and is ``None`` when nothing matches - itself a failure
    worth reporting, since a definition that names no axis is not doing the job
    the field exists for.

    ``all_components_matched`` exists because some published figures have more
    than one axis. ``VC-BPS-001`` is a CV computed across a national plot
    network that pools plot-to-plot variation with microplot-to-microplot
    variation inside each plot; its own harmonization note says it "is NOT a
    pure between-plot term". A reader that returned only the primary component
    would file it as between-plot and say nothing, which is the same silence
    that let VC-TMP-002 through. Two matches means the quantity spans two
    components and belongs to neither.
    """
    text = " ".join(str(quantity_definition or "").lower().split())
    starts = sorted(
        pos
        for trigger in AXIS_TRIGGERS
        for pos in _find_all(text, trigger)
    )
    if not starts:
        return "", None, frozenset()

    # Resolve each trigger SEPARATELY, over a short window, and take the
    # earliest marker inside it. Scanning the whole sentence for markers instead
    # would flag "between sampling points within one plot, for plots of
    # 1-400 m2" as spanning two components - "plots" there is describing plot
    # SIZE, not naming a second axis. A guard that forces authors to contort
    # ordinary prose around it gets routed around, so the window matters.
    per_trigger: list[str] = []
    for start in starts:
        window = text[start:start + AXIS_WINDOW_CHARS]
        best_pos, best = len(window) + 1, None
        for comp in COMPONENT_DEFINITIONS:
            for marker in comp.varies_across:
                pos = window.find(marker)
                if 0 <= pos < best_pos:
                    best_pos, best = pos, comp.name
        if best is not None:
            per_trigger.append(best)

    axis = text[starts[0]:starts[0] + 140]
    primary = per_trigger[0] if per_trigger else None
    return axis, primary, frozenset(per_trigger)


def _find_all(text: str, needle: str) -> list[int]:
    out, start = [], 0
    while (pos := text.find(needle, start)) >= 0:
        out.append(pos)
        start = pos + 1
    return out

#: What physical quantity a row's number is expressed ON. Orthogonal to
#: `component` (which says what VARIES) and to `units` (which is dimensionally
#: silent about the difference between a 1% concentration CV and a 1% stock CV).
#:
#: D-020 already says a concentration CV is never treated as a stock CV. It said
#: so in prose, and prose does not fail CI - the same gap D-032 and D-051 were
#: built to close. This is the enforceable version.
BASES = (
    "concentration",   # g C per g soil; independent of bulk density and depth
    "stock",           # mass per unit area, e.g. Mg C/ha over a stated layer
    "stock_change",    # a DIFFERENCE in stock between two states or conventions
    "variance_share",  # dimensionless share of a variance budget
    "proportion",      # dimensionless share of a count or of another error
    "distance",        # a length, e.g. a relocation offset
)

#: Which units are admissible for each basis. A row claiming `stock` in units of
#: `m` is a transcription error; a row claiming `concentration` in `Mg_C_ha` has
#: skipped a conversion that needs a bulk density.
UNITS_BY_BASIS: dict[str, tuple[str, ...]] = {
    "concentration": ("pct",),
    "stock": ("Mg_C_ha", "pct"),
    "stock_change": ("Mg_C_ha", "Mg_C_ha_10yr", "pct"),
    "variance_share": ("pct",),
    "proportion": ("pct",),
    "distance": ("m",),
}

#: Dispersion statistics - the ones that can be summed into a variance budget,
#: and therefore the ones where a basis mismatch is dangerous rather than merely
#: untidy. A `bias_pct` or a `range` modifies or describes; it is not an addend.
DISPERSION_STATISTICS = ("sd", "cv_pct", "variance")

ERROR_KINDS = (
    "random",      # zero-mean dispersion; enters a variance budget
    "systematic",  # directional bias; must NOT be summed into a variance budget
    "mixed",       # source reports a term containing both; see harmonization_note
)

STATISTICS = (
    "sd",                  # standard deviation
    "cv_pct",              # coefficient of variation, percent
    "variance",            # variance in squared units
    "mae",                 # mean absolute error / deviation
    "rmse",                # root mean square error
    "mdc",                 # minimum detectable change as reported by the source
    "bias_pct",            # systematic offset, percent of the quantity
    "variance_share_pct",  # share of a total error budget, percent
    "range",               # reported spread with no distributional claim
    "mean",                # a mean value carried for context or for conversion
    "proportion_pct",      # e.g. percent of revisits within a distance band
)

UNCERTAINTY_TYPES = (
    "ci95",
    "se",
    "sd_of_estimate",
    "iqr",
    "range_across_sites",
    "range_across_studies",
    "range_across_methods",
    "not_reported",
)

HARMONIZATION_METHODS = (
    "reported_directly",        # used exactly as printed, no transform
    "mae_to_sd_gaussian",       # sd = mae * sqrt(pi/2); assumes normality
    "pct_to_absolute_via_stock",  # MEAN-DEPENDENT
    "absolute_to_pct_via_stock",  # MEAN-DEPENDENT
    "variance_to_sd",
    "variance_share",           # expressed as a share of a total error budget
    "pooled_across_strata",
    "digitised_from_figure",
    "derived_see_note",
)

#: Direction in which a row's number is likely to be WRONG as an estimate of the
#: quantity it stands in for, within our locked scope.
#:
#: NOT to be confused with ``error_kind``. ``error_kind`` describes the physical
#: error the source measured (random scatter vs systematic offset in the soil
#: measurement). ``bias_direction`` describes our *estimate of that error* being
#: too big or too small. A row can be ``error_kind: random`` and
#: ``bias_direction: inflates`` at the same time, and most of them are.
#:
#: Why it has to be tracked per row: an inflated variance is CONSERVATIVE for
#: the sampling calculator (it tells someone to over-sample, which is harmless)
#: but ANTI-CONSERVATIVE for the Phase 5 audit (it over-flags carbon projects as
#: undetectable). The same row feeds both deliverables, so the direction cannot
#: be tracked once at the table level - see DECISIONS.md D-023.
BIAS_DIRECTIONS = (
    "inflates",  # our number is likely LARGER than the truth for our scope
    "deflates",  # our number is likely SMALLER than the truth for our scope
    "unknown",   # no defensible directional argument; must say why
)

LAND_USES = ("cropland", "grassland", "forest", "mixed", "multiple", "not_applicable")

DEPTH_BASES = (
    "fixed_depth",
    "equivalent_soil_mass",
    "genetic_horizon",
    "not_applicable",
)

ANALYTICAL_METHODS = (
    "dry_combustion",
    "loss_on_ignition",
    "wet_oxidation",       # Walkley-Black and relatives
    "mir_spectroscopy",
    "vis_nir_spectroscopy",
    "mixed",
    "not_reported",
    "not_applicable",
)

BD_METHODS = (
    "core",
    "clod",
    "excavation",
    "pedotransfer",
    "not_reported",
    "not_applicable",
)

ACCESS_STATES = ("open_access", "paywalled", "preprint", "public_report")

VERIFICATION_STATES = (
    # Strongest: we hold the primary observations and computed the number
    # ourselves with a committed, re-runnable script. Stronger than reading a
    # published figure, because the derivation is inspectable rather than taken
    # on trust - but it shifts the burden onto OUR method, so such a row must
    # cite the script in `locator` alongside the dataset DOI.
    "derived_primary_data",
    "verified_fulltext",   # number read in the full text / table / figure
    "verified_abstract",   # number read in the abstract only
    "verified_secondary",  # number read in a citing source, not the original
    "unverified",          # not yet checked against any source text
)

USE_AS = (
    "baseline",                 # default parameter for the OSSE
    "sensitivity_low",
    "sensitivity_high",
    "out_of_scope_reference",   # retained for contrast; never a baseline
    "placeholder_needs_pdf",    # value recorded but not yet verifiable
)


# --------------------------------------------------------------------------
# Column specification
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Column:
    name: str
    dtype: str                       # str | float | int | bool
    required: bool
    description: str
    enum: tuple[str, ...] | None = None
    block: str = "misc"


def _c(name, dtype, required, description, enum=None, block="misc") -> Column:
    return Column(name, dtype, required, description, enum, block)


COLUMNS: tuple[Column, ...] = (
    # ---- identity -------------------------------------------------------
    _c("row_id", "str", True,
       "Stable unique key, e.g. VC-TEMP-001. Never reused or renumbered.",
       block="identity"),
    _c("component", "str", True,
       "Which of the six variance components this row parameterises.",
       COMPONENTS, "identity"),
    _c("basis", "enum", True,
       "What physical quantity the number is expressed ON: `concentration`, "
       "`stock`, `stock_change`, `variance_share`, `proportion` or `distance`. "
       "Orthogonal to `component`, which says what varies. Units cannot carry "
       "this: a 1% concentration CV and a 1% stock CV are dimensionally "
       "identical and semantically different, and summing them yields a number "
       "that means nothing. See D-020 and D-052.",
       BASES, "identity"),
    _c("quantity_definition", "str", True,
       "What the number measures, stated INDEPENDENTLY of which component it is "
       "filed under. Must name its axis of variation after 'between', 'across' "
       "or 'among' - the thing that differs between the two measurements being "
       "compared - and must not simply restate the component name. Good: "
       "'standard deviation of SOC concentration between replicate experimental "
       "units under identical management at one site, on one sampling occasion'. "
       "Bad: 'between-plot spatial variance'. See D-051.",
       block="identity"),
    _c("error_kind", "str", True,
       "Whether the term is zero-mean dispersion, a directional bias, or both. "
       "Systematic rows must never be summed into a variance budget.",
       ERROR_KINDS, "identity"),
    _c("quantity", "str", True,
       "Plain-language statement of exactly what the number measures.",
       block="identity"),

    # ---- value as reported ---------------------------------------------
    _c("statistic", "str", True,
       "The statistic the source actually reports.", STATISTICS, "as_reported"),
    _c("value", "float", True,
       "Central value exactly as printed in the source.", block="as_reported"),
    _c("units", "str", True,
       "Units of `value` as printed, e.g. Mg_C_ha, pct, g_cm3, m.",
       block="as_reported"),
    _c("value_low", "float", False,
       "Lower bound as printed, if the source gives a range or interval.",
       block="as_reported"),
    _c("value_high", "float", False,
       "Upper bound as printed.", block="as_reported"),
    _c("uncertainty_type", "str", True,
       "What the low/high bounds represent. `not_reported` is a legitimate and "
       "important answer; it must not be silently upgraded to a CI.",
       UNCERTAINTY_TYPES, "as_reported"),
    _c("n", "int", False,
       "Sample size behind the estimate (plots, cores, sites, or revisits).",
       block="as_reported"),

    # ---- harmonised ------------------------------------------------------
    _c("sd_mg_c_ha", "float", False,
       "Harmonised absolute dispersion, 1 SD, Mg C ha-1. Blank where the row is "
       "a bias or where conversion would require an unsupported assumption.",
       block="harmonised"),
    _c("cv_pct", "float", False,
       "Harmonised relative dispersion, percent of stock.", block="harmonised"),
    _c("harmonization_method", "str", True,
       "Coded transform applied to get from `value` to the harmonised columns.",
       HARMONIZATION_METHODS, "harmonised"),
    _c("harmonization_note", "str", True,
       "REQUIRED prose. States every assumption made to reach the harmonised "
       "value, and what breaks if the assumption is wrong. A row cannot enter "
       "the table with this blank.",
       block="harmonised"),
    _c("reference_stock_mg_c_ha", "float", False,
       "The mean SOC stock used for any percent/absolute conversion. Required "
       "whenever mean_dependent is true, so the dependence stays auditable.",
       block="harmonised"),
    _c("mean_dependent", "bool", True,
       "True if the harmonised value required assuming a mean SOC stock. These "
       "rows are the only route by which a wrong mean can affect an MDC result.",
       block="harmonised"),
    _c("bias_direction", "str", True,
       "Whether this row's number is likely too large (`inflates`), too small "
       "(`deflates`), or unsignable (`unknown`) as an estimate for our scope. "
       "Distinct from `error_kind` - see BIAS_DIRECTIONS.",
       BIAS_DIRECTIONS, "harmonised"),
    _c("bias_direction_reasoning", "str", True,
       "REQUIRED prose justifying `bias_direction`. For `unknown`, must state "
       "why no direction can be defended rather than being left vague.",
       block="harmonised"),

    # ---- context ---------------------------------------------------------
    _c("land_use", "str", True, "Land use of the source population.",
       LAND_USES, "context"),
    _c("management", "str", True,
       "Management context, e.g. cover_crop, reduced_till, conventional, mixed.",
       block="context"),
    _c("climate", "str", True, "Climate description as given by the source.",
       block="context"),
    _c("koppen", "str", False, "Koppen-Geiger code(s) where determinable.",
       block="context"),
    _c("soil_texture", "str", False, "Texture class or range.", block="context"),
    _c("soil_group", "str", False, "WRB / USDA classification where given.",
       block="context"),
    _c("country_region", "str", True, "Geographic extent of the source data.",
       block="context"),
    _c("depth_top_cm", "float", True, "Top of the sampled layer, cm.",
       block="context"),
    _c("depth_bottom_cm", "float", True, "Bottom of the sampled layer, cm.",
       block="context"),
    _c("depth_basis", "str", True,
       "Whether the layer is defined by fixed depth, equivalent soil mass, or "
       "genetic horizon. Mixing these silently is the classic Phase 0 error.",
       DEPTH_BASES, "context"),
    _c("site_stock_mg_c_ha", "float", False,
       "Mean SOC stock reported for the source population, for context.",
       block="context"),
    _c("site_soc_pct", "float", False, "Mean SOC concentration, percent.",
       block="context"),

    # ---- method ----------------------------------------------------------
    _c("analytical_method", "str", False, "Carbon determination method.",
       ANALYTICAL_METHODS, "method"),
    _c("bd_method", "str", False, "Bulk density determination method.",
       BD_METHODS, "method"),
    _c("support_note", "str", False,
       "Sampling support: core diameter, number of cores composited, plot area. "
       "Variance is meaningless without the support it was measured on.",
       block="method"),
    _c("spatial_extent_m", "float", False,
       "Characteristic spatial scale, m: plot dimension for spatial rows, or "
       "offset distance for relocation rows.", block="method"),
    _c("temporal_extent_months", "float", False,
       "Span or interval in months for temporal rows.", block="method"),

    # ---- provenance ------------------------------------------------------
    _c("citation", "str", True,
       "Full citation. A row without one does not go in the table.",
       block="provenance"),
    _c("doi_or_url", "str", True, "Resolvable DOI or stable URL.",
       block="provenance"),
    _c("locator", "str", True,
       "Exact location of the number in the source: abstract, table, figure or "
       "page. This is what a reviewer checks first.", block="provenance"),
    _c("access", "str", True, "Access state of the source.",
       ACCESS_STATES, "provenance"),
    _c("verification", "str", True,
       "How deeply the number was checked against the source.",
       VERIFICATION_STATES, "provenance"),
    _c("extracted_on", "str", True, "ISO date the value was extracted.",
       block="provenance"),

    # ---- OSSE use --------------------------------------------------------
    _c("in_scope", "bool", True,
       "True if the source population matches the locked scope: cropland, "
       "temperate, topsoil. Out-of-scope rows are kept as contrast, not deleted.",
       block="osse"),
    _c("use_as", "str", True, "Role this row plays in the OSSE parameterisation.",
       USE_AS, "osse"),
    _c("osse_distribution", "str", False,
       "Suggested sampling form for Phase 1, e.g. normal(0,sd). A hint, not a "
       "commitment; Phase 1 may override it.", block="osse"),
    _c("superseded_by", "str", False,
       "Row id(s) that replace this row, comma-separated. Set when a better "
       "source arrives - typically an abstract-only value replaced by our own "
       "derivation from the primary data. The superseded row is KEPT, not "
       "deleted: the trail from weak evidence to strong is the verification "
       "ladder working, and a reviewer should be able to see it (D-049).",
       block="osse"),
    _c("notes", "str", False, "Anything a reviewer would want flagged.",
       block="osse"),
)

COLUMN_NAMES: tuple[str, ...] = tuple(c.name for c in COLUMNS)
COLUMNS_BY_NAME: dict[str, Column] = {c.name: c for c in COLUMNS}
REQUIRED_COLUMNS: tuple[str, ...] = tuple(c.name for c in COLUMNS if c.required)

BLOCK_TITLES = {
    "identity": "Identity",
    "as_reported": "Value as reported",
    "harmonised": "Harmonised value",
    "context": "Soil / climate / land-use context",
    "method": "Method and support",
    "provenance": "Provenance",
    "osse": "OSSE use",
}


# --------------------------------------------------------------------------
# Integrity rules
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    """A cross-column invariant applied to a single row."""

    rule_id: str
    description: str
    check: Callable[[dict[str, Any]], bool]

    def failed(self, row: dict[str, Any]) -> bool:
        return not self.check(row)


def _blank(v: Any) -> bool:
    return v is None or (isinstance(v, str) and not v.strip())


def _is_true(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() in {"true", "yes", "1"}


RULES: tuple[Rule, ...] = (
    Rule(
        "R1-citation-required",
        "Every row carries a full citation and a resolvable DOI or URL.",
        lambda r: not _blank(r.get("citation")) and not _blank(r.get("doi_or_url")),
    ),
    Rule(
        "R2-locator-required",
        "Every row states where in the source the number appears.",
        lambda r: not _blank(r.get("locator")),
    ),
    Rule(
        "R3-harmonization-note-required",
        "Every row explains the assumption used to harmonise it.",
        lambda r: not _blank(r.get("harmonization_note")),
    ),
    Rule(
        "R4-mean-dependence-auditable",
        "A mean-dependent row must record the reference stock it used.",
        lambda r: (not _is_true(r.get("mean_dependent")))
        or not _blank(r.get("reference_stock_mg_c_ha")),
    ),
    Rule(
        "R5-mean-dependence-declared",
        "Any percent/absolute conversion must be declared mean-dependent.",
        lambda r: r.get("harmonization_method")
        not in {"pct_to_absolute_via_stock", "absolute_to_pct_via_stock"}
        or _is_true(r.get("mean_dependent")),
    ),
    Rule(
        "R6-unverified-cannot-be-baseline",
        "A number not yet checked against a source cannot drive the OSSE.",
        lambda r: r.get("verification") != "unverified"
        or r.get("use_as") == "placeholder_needs_pdf",
    ),
    Rule(
        "R7-baseline-must-be-in-scope",
        "Only rows matching the locked scope can serve as a baseline.",
        lambda r: r.get("use_as") != "baseline" or _is_true(r.get("in_scope")),
    ),
    Rule(
        "R8-depth-ordered",
        "Depth interval must be ordered and non-degenerate.",
        lambda r: _blank(r.get("depth_top_cm"))
        or _blank(r.get("depth_bottom_cm"))
        or float(r["depth_top_cm"]) < float(r["depth_bottom_cm"]),
    ),
    Rule(
        "R9-bias-not-a-variance",
        "A systematic row must not claim a harmonised standard deviation, which "
        "would let a bias be summed into a variance budget.",
        lambda r: r.get("error_kind") != "systematic"
        or _blank(r.get("sd_mg_c_ha")),
    ),
    Rule(
        "R11-bias-direction-reasoned",
        "Every row justifies its bias_direction in prose.",
        lambda r: not _blank(r.get("bias_direction_reasoning")),
    ),
    Rule(
        "R12-unknown-bias-must-say-why",
        "A bias_direction of 'unknown' must explain why no direction can be "
        "defended, so that 'unknown' cannot be used to dodge the question.",
        lambda r: r.get("bias_direction") != "unknown"
        or len(str(r.get("bias_direction_reasoning", "")).split()) >= 10,
    ),
    Rule(
        "R10-out-of-scope-not-baseline",
        "An out-of-scope reference row cannot also be marked in scope.",
        lambda r: r.get("use_as") != "out_of_scope_reference"
        or not _is_true(r.get("in_scope")),
    ),
)
