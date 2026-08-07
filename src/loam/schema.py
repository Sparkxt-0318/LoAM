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
        "R10-out-of-scope-not-baseline",
        "An out-of-scope reference row cannot also be marked in scope.",
        lambda r: r.get("use_as") != "out_of_scope_reference"
        or not _is_true(r.get("in_scope")),
    ),
)
