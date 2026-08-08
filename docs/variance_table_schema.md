# Variance table — schema

Machine-readable definition lives in [`src/loam/schema.py`](../src/loam/schema.py).
That module is authoritative; this document explains it. A test fails if the two
drift apart.

- **Curated source:** `data/variance_components.yaml` (edit this)
- **Deliverable:** `data/variance_table.csv` (generated — never edit)
- **Rebuild:** `python -m loam.build_table`

---

## What this table is

One row per *published estimate* of an error term standing between a true SOC
change and a measured one. Not one row per component — a component may have
several rows from different sources, depths or land uses, and the disagreement
between them is information we want to keep, not average away.

Six components:

| # | `component` | what it covers |
|---|-------------|----------------|
| 1 | `analytical` | laboratory determination, sample processing, drying |
| 2 | `within_plot_spatial` | variation among points inside one plot |
| 3 | `between_plot_spatial` | variation among plots |
| 4 | `temporal` | month-to-month variation at a fixed location |
| 5 | `relocation` | error from not resampling the same point |
| 6 | `depth_bd_convention` | fixed depth vs equivalent soil mass; bulk density |

---

## Four design choices that carry the weight

### 1. Random and systematic terms are separated (`error_kind`)

Component 6 is a **bias**, not a variance. A bias summed into a variance budget
inflates apparent random error while hiding a directional error that replication
will never reduce. Rule **R9** mechanically forbids a `systematic` row from
carrying a harmonized `sd_mg_c_ha`.

Component 1 contains both kinds, recorded as separate rows: replicate scatter is
random (`VC-ANA-001`), the air-drying offset is systematic (`VC-ANA-003`).

### 2. Mean-dependence is flagged per row (`mean_dependent`)

The testbed's defensibility rests on MDC depending on variance structure rather
than on the mean SOC trajectory. The one place a mean can leak in is unit
conversion: turning a CV (%) into an absolute SD (Mg C/ha) needs a mean stock.

Any such conversion **must** set `mean_dependent: true` and record
`reference_stock_mg_c_ha` (rules **R4**, **R5**). The exposure is therefore a
single-column filter, not a matter of trust. Note that the dependence is on mean
**stock level** — static, directly observed, well constrained — not on the mean
**trajectory**, which is what the underlying carbon model is untrustworthy
about.

### 3. Direction of error is tracked per row (`bias_direction`)

Whether this row's number is likely **too large** (`inflates`), **too small**
(`deflates`), or unsignable (`unknown`) as an estimate for our scope.

**Not the same as `error_kind`.** `error_kind` describes the physical error the
source measured — random scatter vs a systematic offset *in the soil
measurement*. `bias_direction` describes *our estimate of that error* being too
big or too small. Most rows are `error_kind: random` **and** `bias_direction:
inflates` simultaneously; that is not a contradiction.

It has to be per-row because the same row feeds two deliverables with opposite
risk postures:

| | inflated variance is… |
|---|---|
| **Sampling calculator** | **conservative** — tells someone to over-sample. Harmless. |
| **Phase 5 audit** | **anti-conservative** — over-flags carbon projects as undetectable. |

So a single table-level caveat would be wrong for one of them no matter which
way it was written. See `DECISIONS.md` **D-023**, which also fixes the
consequence: Phase 5 runs on the **low end** of the variance envelope, not the
central estimate, so the headline reads *"even under the most generous noise
assumptions, X% of claims fall below detection."*

Rule **R12** stops `unknown` from becoming a dodge — it requires a substantive
explanation of why no direction can be defended.

Current distribution: 14 `inflates`, 7 `unknown`, 5 `deflates`.

### 4. Evidence strength is graded (`verification`)

`verified_fulltext` > `verified_abstract` > `verified_secondary` > `unverified`.

An `unverified` row is locked out of use by rule **R6** — it may sit in the
table with `use_as: placeholder_needs_pdf`, but it can never be a baseline.

---

## Columns

46 columns in seven blocks. Required columns are marked ●.

### Identity

| column | type | | meaning |
|---|---|---|---|
| `row_id` | str | ● | Stable key, `VC-<COMP>-NNN`. Never reused or renumbered. |
| `component` | enum | ● | Which of the six components. |
| `error_kind` | enum | ● | `random` / `systematic` / `mixed`. |
| `quantity` | str | ● | Plain-language statement of what the number measures. |

### Value as reported

Recorded exactly as printed, before any transformation.

| column | type | | meaning |
|---|---|---|---|
| `statistic` | enum | ● | What the source reports: `sd`, `cv_pct`, `mae`, `bias_pct`, `variance_share_pct`, `mdc`, … |
| `value` | float | ● | Central value as printed. |
| `units` | str | ● | Units as printed (`Mg_C_ha`, `pct`, `m`, …). |
| `value_low` / `value_high` | float | | Bounds as printed. |
| `uncertainty_type` | enum | ● | What those bounds *are*. `not_reported` is a legitimate answer and must never be silently upgraded to a CI. |
| `n` | int | | Sample size (plots, cores, sites, revisits). |

### Harmonized value

| column | type | | meaning |
|---|---|---|---|
| `sd_mg_c_ha` | float | | Absolute 1 SD. Blank for bias rows (R9) and where conversion is unsupported. |
| `cv_pct` | float | | Relative dispersion, % of stock. |
| `harmonization_method` | enum | ● | Coded transform, e.g. `mae_to_sd_gaussian`, `reported_directly`. |
| `harmonization_note` | str | ● | **Required prose.** Every assumption made, and what breaks if it is wrong. |
| `reference_stock_mg_c_ha` | float | | Mean stock used for any %↔absolute conversion. Required when `mean_dependent`. |
| `mean_dependent` | bool | ● | Did this row need an assumed mean stock? |
| `bias_direction` | enum | ● | `inflates` / `deflates` / `unknown` — see below. |
| `bias_direction_reasoning` | str | ● | **Required prose** justifying the direction. `unknown` must say *why* it can't be signed. |

### Context

| column | type | | meaning |
|---|---|---|---|
| `land_use` | enum | ● | `cropland`, `grassland`, `forest`, … |
| `management` | str | ● | e.g. `cover_crop`, `reduced_till`, `mixed`. |
| `climate` | str | ● | As described by the source. |
| `koppen` | str | | Köppen–Geiger code where determinable. |
| `soil_texture` | str | | Texture class or range. |
| `soil_group` | str | | WRB / USDA classification. |
| `country_region` | str | ● | Geographic extent of the source data. |
| `depth_top_cm` / `depth_bottom_cm` | float | ● | Sampled layer. |
| `depth_basis` | enum | ● | `fixed_depth` / `equivalent_soil_mass` / `genetic_horizon`. Mixing these silently is the classic Phase 0 error. |
| `site_stock_mg_c_ha` | float | | Mean stock reported for the population. |
| `site_soc_pct` | float | | Mean SOC concentration. |

### Method and support

| column | type | | meaning |
|---|---|---|---|
| `analytical_method` | enum | | `dry_combustion`, `loss_on_ignition`, … |
| `bd_method` | enum | | `core`, `clod`, `pedotransfer`, … |
| `support_note` | str | | Core diameter, compositing, plot area. **A variance is meaningless without the support it was measured on.** |
| `spatial_extent_m` | float | | Plot dimension, or offset distance for relocation rows. |
| `temporal_extent_months` | float | | Span or interval for temporal rows. |

### Provenance

| column | type | | meaning |
|---|---|---|---|
| `citation` | str | ● | Full citation. A row without one does not go in the table. |
| `doi_or_url` | str | ● | Resolvable DOI or stable URL. |
| `locator` | str | ● | Exact position in the source — table, figure, section. This is what a reviewer checks first. |
| `access` | enum | ● | `open_access` / `paywalled` / `preprint` / `public_report`. |
| `verification` | enum | ● | See the ladder above. |
| `extracted_on` | str | ● | ISO date. |

### OSSE use

| column | type | | meaning |
|---|---|---|---|
| `in_scope` | bool | ● | Matches the locked scope (cropland, temperate, topsoil)? |
| `use_as` | enum | ● | `baseline` / `sensitivity_low` / `sensitivity_high` / `out_of_scope_reference` / `placeholder_needs_pdf`. |
| `osse_distribution` | str | | Suggested sampling form for Phase 1. A hint, not a commitment. |
| `notes` | str | | Anything a reviewer would want flagged. |

---

## Integrity rules

Enforced in `schema.py` and exercised by `tests/test_variance_table.py`.

| id | rule |
|----|------|
| R1 | Every row carries a citation and a resolvable DOI/URL. |
| R2 | Every row states where in the source the number appears. |
| R3 | Every row explains its harmonization assumption. |
| R4 | A mean-dependent row records the reference stock it used. |
| R5 | Any %↔absolute conversion must be declared mean-dependent. |
| R6 | An unverified number can never drive the OSSE. |
| R7 | Only in-scope rows can be baselines. |
| R8 | Depth intervals are ordered and non-degenerate. |
| R9 | A systematic row carries no harmonized SD. |
| R10 | An out-of-scope reference row is not also marked in scope. |
| R11 | Every row justifies its `bias_direction` in prose. |
| R12 | `unknown` must explain why no direction can be defended — it cannot be a dodge. |

Beyond the rules, the test suite pins current coverage: components with no
in-scope baseline (`temporal`, `between_plot_spatial`) are asserted to *still*
have none, so closing a gap is a deliberate, visible change rather than drift.

---

## Adding a row

1. Read the source. Record `verification` honestly — abstract-only is
   `verified_abstract`, and a number read in a citing paper is
   `verified_secondary`.
2. Copy `value`/`units` exactly as printed. Do not pre-convert.
3. Fill `harmonization_note` with the assumption **and its failure mode**. "Used
   as printed" is fine when true; a blank note fails the build.
4. Set `in_scope` against the scope lock, not against convenience.
5. If a conversion needed a mean stock, set `mean_dependent: true` and record it.
6. Set `bias_direction` by asking: *is this number likely too big or too small
   for **our** scope?* Transfers across land use, climate, depth or support
   almost always have a signable direction — reach for `unknown` only when two
   effects genuinely push opposite ways, and say so.
7. Log the assumption in [`DECISIONS.md`](../DECISIONS.md) with a new `D-NNN`.
8. `python -m loam.build_table && pytest`
