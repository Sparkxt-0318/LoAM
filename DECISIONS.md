# DECISIONS

Every harmonization assumption made while building the variance-component
reference table, with the reason and the consequence if the assumption is wrong.

Append-only. Do not rewrite history — supersede an entry with a new one and mark
the old one `SUPERSEDED BY D-NNN`.

Format: **D-NNN — decision.** Why. What breaks if wrong.

---

## Decision status

Machine-readable index. `src/loam/decisions.py` carries the same statuses, and
`tests/test_decision_guard.py` fails if the two disagree or if a decision is
written up below without appearing here — so this table cannot quietly fall
behind the prose.

An `open` decision may not govern a live constant or a verified baseline row.
That is enforced, not requested: see D-032.

| id | status | governs |
|----|--------|---------|
| D-001 | decided | YAML is the curated source, CSV is the artifact |
| D-002 | decided | `schema.py` is the single source of truth for columns |
| D-003 | decided | MAE → SD conversion assumes normality |
| D-004 | decided | every row carries both absolute and relative dispersion |
| D-005 | decided | paired-difference errors stay on the difference scale |
| D-006 | decided | variance shares applied multiplicatively |
| D-007 | decided | bulk-density coupling is the one genuine mean-exposure |
| D-008 | decided | layer CVs are not combined into 0–30 cm |
| D-009 | decided | Poeplau 5.1 and 7.6 Mg C/ha are not a range |
| D-010 | decided | LUCAS revisit distance interpretation |
| D-011 | decided | Buchkowski is out-of-scope forest, retained for contrast |
| D-012 | decided | Buchkowski's within≈between is qualitative |
| D-013 | decided | Fowler's 17% is illustrative, not measured |
| D-014 | decided | Wuest retained as the only temporal anchor |
| D-015 | decided | a bias never gets a harmonized SD |
| D-016 | decided | out-of-scope rows are flagged, never deleted |
| D-017 | decided | verification ladder |
| D-018 | decided | relocation and between-plot terms overlap near 100 m |
| D-019 | decided | relocation error is distance-independent within a plot |
| D-020 | decided | concentration CV is never treated as stock CV |
| D-021 | decided | PNW dryland IS in-scope temperate — classified on sourced inputs |
| D-022 | decided | circularity guard on the noise model |
| D-023 | decided | `bias_direction` recorded per row |
| D-024 | decided | `HEADLINE_DESIGNS` — RCB / CR only |
| D-025 | decided | `HEADLINE_EU_TYPE` — `Plots` only |
| D-026 | decided | `DEPTH_CM` — rows scoped to 0–15 cm, never rescaled |
| D-027 | decided | G1 is spatial + analytical combined, an upper bound |
| D-028 | decided | `IPCC_OUT_OF_SCOPE_REGIONS` — IPCC temperature regime → `VC-BPS-005/006` |
| D-029 | decided | estimator: REML nested random effects, log scale |
| D-030 | decided | NAPESHM primary for component 3, Poeplau cross-check |
| D-031 | decided | Poeplau ↔ NAPESHM corroboration is logged, not merged |
| D-032 | decided | open decisions may not govern live constants — enforced |
| D-033 | decided | IPCC climate regions are not derivable from NAPESHM; no proxy |
| D-034 | decided | `ipcc_climate.py` — classifier committed, deliberately unfed |
| D-035 | decided | schema gains `scales_with_interval` — next PR |
| D-036 | decided | analytical error vs Potash's — **1.20× like-for-like**; the residual was a typo in their reference soil, confirmed by the author |
| D-037 | decided | Potash parameters are candidate cross-checks, never merged |
| D-038 | decided | positioning vs Potash et al. 2025 in any writeup |
| D-039 | decided | **FINDING**: NAPESHM is not fully IPCC-classifiable — for the paper |
| D-040 | decided | G1 sensitivity: both `VC-BPS-005/006` caveat flags close; texture is not a stratifier |
| D-041 | decided | temporal estimator — crossed plot × occasion REML, validated against moments |
| D-042 | decided | Wuest sampling depth is heterogeneous — the assumed 0–30 cm is wrong for 4 of 5 series |
| D-043 | decided | temporal is reported as a bounded pair, separable 3.75% and combined 8.00% |
| D-044 | decided | **FINDING**: anniversary sampling does not reduce temporal variance |
| D-045 | decided | temporal variance shows no consistent covariate dependence either |
| D-046 | decided | Wuest independently corroborates the G1 between-plot baseline |
| D-047 | decided | KBS LTER corroborates in the opposite direction; licence blocks publication use |
| D-048 | decided | NEON temporal path retired, script and caveats kept |
| D-049 | decided | superseded rows are kept, not deleted; schema gains `superseded_by` |
| D-050 | decided | **PIPELINE VALIDATION**: our derivation reproduces the published temporal statistic |
| D-051 | decided | **FINDING**: components are conflated by adjacency in sources — `quantity_definition` + guard |
| D-052 | decided | every row declares a `basis`; D-020 gets mechanical teeth |
| D-053 | decided | G3 bounded: 'add cores' is unproven; disagrees with Potash's 4-core composite |
| **D-054** | **open** | which laboratory error the `analytical` component carries — carried forward from D-036 |
| D-055 | decided | **FINDING**: inorganic carbon is not the conditioning covariate; D-040 invariance survives, at a ~7% detection limit |
| D-056 | decided | **FINDING**: registry sampling designs are mostly unpublished — Phase 5 corpus started, gap quantified |
| D-057 | decided | VM0042 read from primary: 0.4307 **confirmed**, version caveat, and VM0042's own Eq. 2 **is** the inverted audit |

---

## The invariant these decisions protect

The testbed quantifies **detectability**, not soil carbon. Minimum detectable
change (MDC) is a property of the **variance structure** of the measurement
process. It does not require the underlying carbon model's mean trajectory to be
correct. Every decision below is checked against that property.

Two places where mean-dependence can leak in, and how each is contained:

1. **Unit harmonization.** Converting a CV (%) into an absolute SD (Mg C/ha)
   requires a mean stock. This is real but mild: it depends on the mean **stock
   level**, a static quantity that is directly observed and well constrained
   (temperate cropland 0–30 cm is roughly 40–80 Mg C/ha), *not* on the mean
   **trajectory**, which is the thing our carbon model is untrustworthy about.
   Contained by D-004: the dependence is flagged per row and MDC is reported in
   relative terms as primary.

2. **Bulk-density coupling (the one genuine exposure).** See D-007. This is the
   flag the brief asked for.

---

## Infrastructure

**D-001 — The curated source is `data/variance_components.yaml`; the deliverable
`data/variance_table.csv` is generated from it and never hand-edited.**
Harmonization notes run to several sentences, and prose of that length is
unreadable and unreviewable inside a 44-column CSV. YAML keeps the notes
diffable so a reviewer can see an assumption change in a pull request.
*If wrong:* nothing scientific; the CSV is regenerated by
`python -m loam.build_table` and a test fails if it goes stale.

**D-002 — `src/loam/schema.py` is the single source of truth for columns,
vocabularies and integrity rules.** The schema doc, the YAML and the CSV are all
validated against it, so they cannot drift apart silently.
*If wrong:* schema changes would have to be made in three places and would
diverge — exactly the failure mode Phase 0 cannot afford.

---

## Unit harmonization

**D-003 — Mean absolute error is converted to a standard deviation as
`SD = MAE × √(π/2) = MAE × 1.2533`.**
Poeplau et al. (2022) report MAE (their Eq. 3), but a variance budget needs an
SD. The factor is exact for a zero-mean normal.
*If wrong:* SOC resampling differences are plausibly heavier-tailed than normal,
in which case this **understates** the true SD and the testbed reports MDC as
better than it is. Affects VC-REL-001, VC-REL-002, VC-REL-003, VC-ANA-001.
Direction of the error is known and non-conservative — worth revisiting with the
raw paired data if it can be obtained.

**D-004 — Every row carries both an absolute (`sd_mg_c_ha`) and a relative
(`cv_pct`) form where possible, and any conversion between them sets
`mean_dependent = true` and records the `reference_stock_mg_c_ha` used.**
This is the core defence of the detectability claim. It makes the mean-dependent
subset of the table explicitly enumerable rather than a matter of trust: a
reviewer can filter on one column and see the entire exposure.
*If wrong:* if we had harmonized everything to absolute units, an incorrect
baseline stock would silently rescale every variance component, and the claim
that the testbed is robust to the mean model would be false. Currently exactly
**one** row (VC-ANA-004) is mean-dependent, and its reference stock comes from
the source itself, not from an assumption of ours.

**D-005 — Paired-difference errors are recorded on the difference scale, with
the per-observation equivalent (`÷ √2`) stated in the note rather than silently
substituted.**
Poeplau's resampling error is the difference between two locations. Treating a
difference SD as a single-observation SD (or vice versa) misstates MDC by √2.
*If wrong:* a factor of 1.41 in every relocation-driven MDC. Phase 1 must state
which scale it consumes. See VC-REL-001.

**D-006 — Variance *shares* (Wuest) are applied multiplicatively inside the
simulator, never added as a standalone variance term.**
Wuest reports month-to-month variance as a percentage *of the total random
error*, not as an absolute magnitude. The total random error is a Phase 1
output, not a Phase 0 input.
*If wrong:* adding a share as though it were a variance double-counts the other
five components. This is the single easiest way to corrupt the budget.

**D-007 — The bulk-density change driving the depth-convention bias is treated
as an EXOGENOUS scenario parameter, swept over a range, and is never taken from
the carbon model's own output.**
**This is the flagged risk the brief asked for.** Fowler et al. (2023) give a
17% underestimate *conditional on* bulk density falling 1.5 → 1.1 g/cm³. Whether
that change occurs is a management-response prediction — precisely the kind of
mean-model output the testbed is supposed not to depend on. If the simulator
asked the carbon model how much bulk density changed, component 6 would become
a function of the mean trajectory and the defensibility argument would collapse
for that component.
*If wrong:* component 6 stops being a measurement-error term and becomes a
process prediction. Containment: sweep bulk density change as an input and
report MDC as a surface over it, so the result is "detectability given a BD
change of X", never "detectability given our model's BD prediction".

**D-008 — Layer CVs are not combined into a 0–30 cm CV.**
Poeplau's Table 4 gives within-plot CV for 0–10 cm (9.3%) and 10–30 cm (10.2%)
separately. Combining them requires the covariance between layers, which is not
reported, and the layers are of unequal thickness.
*If wrong:* assuming independence would understate the 0–30 cm CV; assuming
perfect correlation would overstate it. Recorded as gap **G2** rather than
guessed.

---

## Corrections to the anchor values in the brief

Each anchor was checked against the source rather than accepted. Three needed
correcting; all five needed qualifying.

**D-009 — Poeplau: 5.1 and 7.6 Mg C/ha are NOT a range. 5.1 is cropland (7.5%),
7.6 is grassland (8.5%).** Under the cropland scope lock the value is **5.1**.
The grassland figure is retained as an out-of-scope contrast row (VC-REL-002).
Two further qualifications the brief did not carry: the offset was only **about
40 cm** (a best case — the smallest displacement possible when reopening a pit),
and the study reports **mean absolute error**, not SD (see D-003).
*If wrong:* using 7.6 for cropland inflates the relocation term by 49%.

**D-010 — LUCAS: the finding is that ~80% of 2015 revisits were WITHIN 10 m of
baseline, not that they "could sit up to 10 m" away.** The maximum permitted
offset was **100 m**, and ~96.5% fell within that. The risk therefore lives in
the unstated tail between 10 m and 100 m, not at 10 m.
Additionally: **LUCAS topsoil is sampled to 20 cm, not 30 cm** — a depth-basis
mismatch with our scope that must be resolved before these rows are usable.
*If wrong:* treating 10 m as the worst case understates relocation error by an
unknown but potentially large factor, because ~20% of revisits exceed it.

**D-011 — Buchkowski (CV ~40% mineral / ~70% organic) is a Canadian FOREST
inventory and is not transferable to cropland.** All four rows are marked
out-of-scope. Three independent reasons: forest rather than cropland;
genetic-horizon rather than fixed-depth sampling; and an unploughed population.
Tillage homogenizes cropland topsoil, which is why the in-scope cropland CVs in
this table are 9–10%, not 40%. The organic-horizon figure is not merely out of
scope but **structurally inapplicable** — tilled cropland topsoil has no O
horizon.
*If wrong:* importing 40% would inflate the spatial terms roughly fourfold and
make every design look undetectable.

**D-012 — Buchkowski's "within-plot comparable to between-plot" is a QUALITATIVE
claim; the 50/50 split in VC-BPS-003 is our encoding, not the paper's number.**
Recorded so the claim is machine-readable, flagged in the row so nobody mistakes
it for a measured partition.
*If wrong:* the design implications invert. If within ≈ between, adding plots
buys as much as compositing more cores within plots — which contradicts the
usual advice to composite heavily. Getting a cropland number for this is the
highest-value literature target we have (gap **G3**).

**D-013 — Fowler's 17% is an ILLUSTRATIVE calculation from a prescribed
scenario, not an empirical measurement.** The authors call it "hypothetical but
realistic" and support it by citing observed bulk-density decreases of 20–25%.
*If wrong:* nothing, provided it is used as a *mechanism with a known functional
form* (which is how component 6 should be modelled) rather than as an observed
effect size. Quoting "17%" as an empirical finding would be misrepresentation
and is the kind of thing a reviewer will check.

**D-014 — Wuest's 15–32% is retained as the only temporal anchor despite being
out of scope, marked `in_scope: false` and `sensitivity_high`, never
`baseline`.** The sites are Pacific Northwest **dryland** cropland (semi-arid),
not temperate humid cropland. Temporal variance is plausibly driven by moisture
and biological cycling, both of which differ systematically between those
systems, so even the *direction* of the transfer error is unknown. The 0–30 cm
depth in that row is **assumed, not confirmed** — the abstract does not state it
and the full text is paywalled.
*If wrong:* the temporal component is misparameterized in an unknown direction.
This is the weakest load-bearing row in the table. See gap **G4**.

---

## Structural decisions

**D-015 — A bias is never given a harmonized standard deviation.**
Enforced mechanically by rule R9. Component 6 is systematic, not random;
component 1 contains both (the drying bias in VC-ANA-003 is systematic, the
replicate error in VC-ANA-001 is random) and they are recorded as separate rows.
*If wrong:* summing a bias into a variance budget both inflates the apparent
random error and hides a directional error that no amount of replication will
reduce. This is the most likely single mistake in a table like this.

**D-016 — Out-of-scope rows are retained and flagged, never deleted.**
They record what we deliberately did *not* borrow, which is more defensible than
a table that silently contains only convenient numbers. Enforced by rules R7 and
R10: only in-scope rows can be baselines.
*If wrong:* nothing; worst case the table is larger than strictly necessary.

**D-017 — Verification is a four-level ladder: `verified_fulltext` >
`verified_abstract` > `verified_secondary` > `unverified`, and an `unverified`
row can never drive the OSSE (rule R6).**
A number read in an abstract is weaker evidence than one read in a table, and a
number read in a *citing* source is weaker still. Collapsing these would hide
which parts of the wall are load-bearing.
*If wrong:* an unchecked number silently becomes a baseline. Currently 14 of 24
rows are `verified_fulltext`; 2 are `unverified` and are locked out of use.

**D-018 — At offsets approaching 100 m, the relocation term and the
between-plot spatial term are the same physical quantity, and the six-component
decomposition stops being orthogonal.**
The six components are treated as additive variance contributions. That holds
for small offsets (Poeplau's ≤7 m, within a 20×20 m plot) but not at LUCAS-scale
relocation.
*If wrong:* Phase 1 adds both terms at large offsets and double-counts. Recorded
as gap **G5**; Phase 1 must implement relocation as *interpolation between* the
within-plot and between-plot variance regimes, not as an independent addition.

**D-019 — Relocation error is modelled as distance-INDEPENDENT within a plot.**
Poeplau found the error from a 40 cm shift was already as large as that from a
~7 m shift; spatial dependence was weak and the variogram nugget-dominated.
*If wrong:* only mildly, within a plot. But this must **not** be extrapolated
beyond ~7 m — at LUCAS offsets there is no evidence for flatness. See VC-REL-004.

**D-020 — CV of SOC *concentration* is never treated as CV of SOC *stock*.**
Saby et al.'s 3.4% is a concentration CV; stock CV compounds it with bulk-density
variance and is larger. Recorded unconverted because the
concentration–density covariance is not reported.
*If wrong:* using 3.4% as a stock CV understates the within-plot term by roughly
a factor of three relative to Poeplau's directly measured 9.3%.

**D-021 — OPEN SCOPE QUESTION, UNRESOLVED: does Pacific Northwest dryland
cropping fall inside "temperate"?** ⚠️ *Deliberately not decided. For the PI.*
Wuest (2024) is the only temporal anchor in the table (`VC-TMP-001/002`). It is
unambiguously **in scope on land use** — cropland — and unambiguously **in scope
on depth**. The question is climate. The sites are PNW dryland small-grain
systems: cool-season-wet, summer-dry, and moisture-limited in a way that
temperate humid cropland is not. Depending on site they sit around Köppen
Csb/BSk, which is "temperate" under some readings of the scope lock and not
under others.

Why it cannot be settled by fiat: temporal variance in measured SOC is
plausibly driven by moisture cycling and biological activity, and those are
precisely the axes on which dryland and humid systems differ. So the answer
changes the parameterisation, not just the label.

*Holding position until resolved:* rows stay `in_scope: false` and
`use_as: sensitivity_high` — usable as a sensitivity bound, never as a baseline.
That is conservative, not an answer, and component 4 stays a declared gap (G4)
in the meantime.

*Resolve by choosing one:* (a) admit PNW dryland to scope and promote the rows
to baseline; (b) hold the narrower reading and keep component 4 open pending a
humid-temperate source; (c) narrow the scope lock's wording so the question
cannot recur. **Do not let this be resolved implicitly by someone flipping
`in_scope` to close a gap.**

**D-022 — CIRCULARITY GUARD: the noise model is calibrated on Poeplau and
Wuest. NABO and Finland are HELD OUT ENTIRELY and reserved for Phase 4
validation.** A testbed validated against the same data that parameterised it
measures only its own self-consistency, and any reviewer will look for exactly
this. Holding out two independent national monitoring networks is what makes a
Phase 4 validation claim mean anything.
*If wrong:* there is no recoverable position — once NABO or Finnish data has
been looked at while building the noise model, it can never again serve as an
independent test, and no later analysis undoes that. **This must not be relaxed
later**, including for the tempting case where a held-out network would close an
open gap. If a gap can only be closed with held-out data, the correct outcome is
that the gap stays open.

---

## Direction-of-bias tracking

**D-023 — Every row records `bias_direction` (`inflates` / `deflates` /
`unknown`) with required reasoning.**
An inflated variance is **conservative for the sampling calculator** — it tells
someone to over-sample, which is harmless — but **anti-conservative for the
Phase 5 audit**, where it over-flags carbon projects as undetectable. The same
row feeds both deliverables, so a single table-level caveat would be wrong for
one of them no matter how it was written. Tracking direction per row is the only
way both can be served from one table.

*Consequence, fixed now so it is not relitigated later:* **Phase 5 runs the audit
on the LOW end of the variance envelope, not the central estimate.** The headline
must read *"even under the most generous noise assumptions, X% of claims fall
below detection."* An audit run on central or high estimates is not defensible,
because the critic's first move is to point at the inflating rows.

Not to be confused with `error_kind`: that describes the physical error the
source measured; `bias_direction` describes *our estimate of it* being too big or
too small. Rule R12 stops `unknown` being used to dodge the question.

Current: 14 `inflates`, 7 `unknown`, 5 `deflates`.

*The NEON temporal work carries the same property.* The between-bout variance
that `scripts/neon_temporal_variance.py` would produce absorbs relocation
variance as well as temporal variance, because NEON randomises core position
within a plot rather than revisiting a point. It is therefore an **upper bound on
temporal variance, not an estimate of it**, and if it ever becomes a row it must
be `bias_direction: inflates`.

---

## NAPESHM derivation of the between-plot baseline (G1)

Data: Soil Health Institute (2024), NAPESHM, doi:10.15482/USDA.ADC/25632270.
Derivation: `scripts/derive_g1_napeshm.py`. Rows: `VC-BPS-005` (concentration),
`VC-BPS-006` (stock).

**D-024 — Headline uses only `Randomized complete block` and `Completely
randomized` sites. The 40 sites with design `'0'` (unknown) are EXCLUDED.**
The 94 sites span 14 design types and these are not equivalent. In an RCB,
replicate EUs are true randomized replicates and their residual variance is
clean between-plot spatial variance. In split-plot and management-zone designs,
replicates may be structurally non-equivalent, and pooling them inflates the
estimate. Including the unknown-design sites would require positive evidence
that they are randomized; absence of a recorded design is not such evidence.
*Measured cost of getting this wrong:* admitting all designs moves the estimate
from 12.0% to 14.2% — the filter is worth 2.2 percentage points, so this is not
a cosmetic decision.
*Reported as sensitivity:* all-designs-pooled is in the script output.
*String-match audit (the obvious reviewer question).* The filter is an exact
string match, so every distinct `exper_design` value was checked by hand for a
near-miss. Four dropped values contain "randomiz" and none should be kept:
`'Completely randomized split splot'` (4 sites — split plot, and note the typo in
the source data), `'Randomized complete block split plot'` (1 — split plot),
`'Incomplete randomized block'` (1 — incomplete blocks are not full replicates),
and `'Randomized'` (1 — too ambiguous to classify). Nothing legitimate is lost to
a spelling accident; every exclusion is on design grounds.

**D-025 — Headline filters to `eu_type == 'Plots'`.**
Spatial variance scales with the separation between replicates, and a "field"
replicate is not the same measurement as a "plot" replicate. Other eu_types
(Fields, Strip plots, Pasture paddocks, Open range) are reported stratified,
never pooled into the headline.
*Measured effect:* small here — 11.97% vs 11.93% — because RCB/CR sites are
almost all plot-based already. The filter is retained anyway: it costs almost
nothing and removes a real confound rather than an observed one.

**D-026 — The row is SCOPED to 0-15 cm. It is NOT converted to our 0-30 cm
project scope.**
There is no depth column anywhere in NAPESHM. Sampling depth is fixed by
protocol and documented only in Norris et al. (2020), which is what the rows
cite for it. A concentration CV at 0-15 cm is not transferable to 0-30 cm stocks
without a depth-distribution assumption that carries its own error — and
Poeplau's Table 4 shows within-plot CV is not even constant with depth (9.3% at
0-10 cm, 10.2% at 10-30 cm, 25.8% at 30-50 cm). **The mismatch is resolved by
rescoping the row, not by rescaling the number.** Left open: whether Phase 1
needs a 0-30 cm between-plot term at all, or can work natively at 0-15 cm.

**D-027 — G1 is spatial + analytical error COMBINED, and is therefore an UPPER
BOUND on between-plot spatial variance.**
NAPESHM has no lab duplicate, split-sample or QC columns, so the two cannot be
separated. Both rows carry `bias_direction: inflates` and say so in the row text.
*Magnitude:* using VC-ANA-001's 1.25% analytical CV, the purely spatial part
would be about sqrt(12.1² − 1.25²) = 12.0%. The inflation is small — but it is
one-directional, and under D-023 it matters for Phase 5.

**D-029 — Estimator: REML nested random effects, treatment within site,
on the log scale, with a cluster bootstrap over sites.**
Three separate choices, each with a reason:
- *Nested random effects, not averaged per-treatment variances.* With 3-5
  replicates per treatment, individual treatment variances are wildly unstable,
  and averaging them weights a 3-replicate treatment equally with a 5-replicate
  one. The REML residual pools correctly.
- *Log scale.* Within-treatment SD scales with treatment mean — the log-log
  slope is about 1.2, far from the 0 that a constant-SD model assumes and close
  to the 1 that a constant-CV model assumes. So the natural parameter is a CV,
  and `CV = 100·sqrt(exp(σ²) − 1)`.
- *Cluster bootstrap over sites.* Sites are the top-level independent unit.
  Bootstrapping rows or treatments would ignore the nesting and produce
  intervals far too narrow. 600/600 resamples converged and the bootstrap median
  (11.9%) sits on the point estimate, so the estimator shows no material bias.

**D-030 — NAPESHM is the PRIMARY source for component 3; Poeplau 2022 is demoted
to an independent cross-check.**
NAPESHM is 212 EUs across 14 sites on the right continent for a North American
audit, with an explicit randomized design. Poeplau is 8 cropland sites in one
German region. Poeplau remains valuable precisely *because* it is independent —
different continent, different design, different support — and its within-plot
stock CV of 9.3-10.2% sits just below our between-plot estimate of 11.1-12.1%,
which is a coherent ordering and a genuine corroboration. It must never be the
baseline for a between-plot term: it does not measure one.

**D-028 — DECIDED 2026-08-09: scope by IPCC 2006 climate region, classified as
far as the data allow and no further.** ✅

> **The decision.** Retire the private envelope. Classify every site the tree in
> **Figure 3A.5.2 (Vol 4 Ch 3, p. 3.39)** can resolve, using MAT, MAP, elevation
> and Daymet-derived frost days. Any site reaching a node that needs MAP:PET
> returns **`unclassified`** — explicitly, never imputed, never
> nearest-neighbour filled. Scope the G1 rows by the **temperature regime**:
> Tropical is out, everything else is `Temperate/Boreal`.
>
> **Why, and this is the whole argument.** The alternative was an
> internally-invented threshold applied to all 94 sites. That classifies
> everything and is wrong in ways no reviewer can audit — the failure is in a
> threshold's *meaning*, so it shows up as neither scatter nor a widened
> interval. Partial IPCC classifies fewer sites and **names exactly which ones it
> could not**. For a project whose entire claim is knowing what cannot be
> detected, an ad hoc envelope would be **self-refuting**: it would assert a
> precision about climate that the project's own thesis says to distrust about
> carbon.
>
> **Why the temperature regime alone is sufficient rather than a compromise.**
> Vol 4 Ch 5 **Table 5.5** indexes stock-change factors on `Temperate/Boreal` —
> it does not distinguish warm from cool. So the axis we can resolve is exactly
> the axis Ch 5 needs. Only the moisture axis is missing, and it is left missing.
>
> **Why "not Tropical" means "Temperate/Boreal" here.** NAPESHM's coldest site is
> 4 °C, so under ±0.5 °C rounding no site can reach MAT ≤ 0 and the Boreal/Polar
> subtree is unreachable for this dataset. Pinned by a test.
>
> **The split: 7 classified (6 Tropical Dry, 1 Tropical Montane), 87
> unclassified**, every one of them blocked on `map_pet_ratio`. Zero sites
> classify as IPCC-temperate, which is why the rows are scoped by temperature
> regime rather than by region label. See **D-039** — the unclassified bucket is
> a finding about NAPESHM, not a footnote about us.
>
> **Frost days.** Recovered from the **Daymet** single-pixel API at each site's
> published coordinates — the source NAPESHM's own dictionary cites for every one
> of its climate columns — over 2010–2019. Validated rather than assumed:
> `floor(mean(daily series))` reproduces the published `site_meanmin_temp`,
> `site_meanmax_temp` and `site_mean_temp` integers **60/60 exact** across all 20
> sites at MAT ≥ 18, truncation convention included. That is what licenses using
> the live V4 R1 endpoint against a dictionary citing doi:10.3334/ORNLDAAC/1328.
>
> **Known fragility, recorded not buried.** `site_mean_temp` is published as a
> whole number. **20 of 94 sites sit exactly on a MAT cut point** (13 at 10, 7 at
> 18). Four of those — MXAG01, MXPU01, MXQT02, MXSL01, all with 0.2–4.2 frost
> days/yr — would become **Tropical** if their true MAT were above 18. For those
> four, integer rounding decides scope membership, not climate.
>
> > **CORRECTED 2026-08-10 (D-040): the caveat above is half the size it claims.**
> > Scope membership is not the same as influence on a number. **MXAG01 and
> > MXQT02 contribute 0 EUs to the derivation** — they are removed by D-024 /
> > D-025 before climate is applied at all, and stay at 0 even with the climate
> > filter switched off entirely. Their rounding is therefore unfalsifiable *and*
> > inconsequential. Only **MXPU01 (16 EUs) and MXSL01 (14 EUs)** can move
> > anything.
> >
> > Quantified rather than asserted, since the worst case is cheap to compute:
> > dropping both leaves concentration at **11.469%** (from 11.948, shift 0.479,
> > n 386 → 356) and stock at **10.863%** (from 11.456, shift 0.593, n 372 → 346).
> > Both shifts sit well inside the CI widths of 3.97 and 3.52.
> >
> > So the honest statement is: for **two** sites integer rounding decides scope
> > membership, and if both were misclassified the headline moves by about a
> > seventh of its confidence interval. This is the same error of conflating
> > *scope* with *sample* that produced the "10 Mexican highland sites" figure
> > corrected in D-040 — one cause, two symptoms.

*The original open question is preserved below, because it records why the
envelope was never defensible.*

**D-028 (as originally written) — OPEN SCOPE QUESTION: what climate envelope
defines "temperate" for NAPESHM?**
NAPESHM site climate spans MAT 4.0-25.0 °C and MAP 167-1543 mm, with 78 US and
16 Mexican sites. That reaches past temperate into subtropical highland and hot
desert. Letting a 25 °C, 167 mm Sonoran site into a "temperate" baseline by
default would be indefensible, so the headline currently uses a **proposed**
envelope, and the rows say it is provisional.

*Recommended envelope: MAT ≤ 15 °C AND |latitude| ≥ 30°.* Justification: the MAT
cap excludes hot climates, and the latitude floor is what excludes the Mexican
highland sites, which is the part a MAT cap alone gets wrong. Sites 19-21 at
19°N sit at MAT 15-16 °C only because of elevation; they are Köppen **Cwb**,
summer-rain and winter-dry. Köppen would call that "temperate", but the moisture
seasonality driving SOC dynamics is tropical, not temperate. The result is 14 US
sites, 212 EUs, MAT 4-15 °C, MAP 330-1282 mm, latitude 36.4-48.3°N.

*The decision barely moves the number, which should make it easier:*

| envelope | sites | EUs | conc CV | stock CV |
|---|---|---|---|---|
| MAT ≤ 12, lat ≥ 30 | 11 | 178 | 10.6% | 9.8% |
| **MAT ≤ 15, lat ≥ 30 (recommended)** | **14** | **212** | **12.1%** | **11.1%** |
| MAT ≤ 18, any lat | 26 | 386 | 11.9% | 11.5% |
| all sites | 30 | 472 | 12.0% | 11.7% |

Every candidate falls inside the recommended envelope's own 95% CI of
[10.0, 14.3]. The choice is therefore about **defensibility of scope**, not about
the estimate. *Resolve by choosing one:* (a) adopt the recommendation;
(b) a different envelope, changing one constant in
`CLIMATE_ENVELOPES`; (c) formally widen the project scope beyond temperate, which
would also reopen D-021.

**2026-08-08 — the preferred resolution was attempted and is BLOCKED.** Replacing
the private envelope with IPCC 2006 default climate regions (Vol 4 Ch 3, Figure
3A.5.2, p. 3.39) was investigated and **cannot be implemented faithfully from
NAPESHM**. Details in D-033. Neither the private envelope nor the IPCC scheme is
therefore available as a defensible answer today, and the envelope stays open.

---

## Cross-checks and guards

**D-031 — The Poeplau ↔ NAPESHM agreement is recorded as corroboration, and is
NOT merged into either row.** Logging it now, while the derivation is fresh.

*Figure correction, made before recording anything.* The comparison was proposed
as "Poeplau 7.5–8.5% at 0–30 cm". Those are **not** Poeplau's within-plot spatial
numbers — 7.5% and 8.5% are the **relocation** MAE figures from D-009 (5.1 Mg
C/ha cropland and 7.6 Mg C/ha grassland, carried by `VC-REL-001/002`), which
measure something else entirely: the error from not resampling the same point.
Poeplau's actual within-plot spatial CVs are `VC-WPS-001` **9.3% (0–10 cm)** and
`VC-WPS-002` **10.2% (10–30 cm)**, both cropland, both *n*=8. There is
deliberately **no 0–30 cm within-plot value** to quote: D-008 forbids combining
layer CVs without the inter-layer covariance, and that absence is logged as gap
**G2**. The table below uses the verified numbers.

| | NAPESHM (`VC-BPS-005/006`) | Poeplau 2022 (`VC-WPS-001/002`) |
|---|---|---|
| term | **between**-plot spatial | **within**-plot spatial |
| CV | 11.1% stock, 12.1% concentration | 9.3% (0–10 cm), 10.2% (10–30 cm) |
| depth | 0–15 cm | 0–10 and 10–30 cm, kept separate |
| region | North America (14 US sites) | Germany |
| n | 212 EUs / 61 treatments / 14 sites | 8 plots, 16 cores each |
| analytical error | **included** (D-027, upper bound) | closer to spatial-only |

NAPESHM is higher, and **should** be — but for **two** reasons, not three.

1. **Ours includes analytical error.** D-027: NAPESHM has no lab duplicate or QC
   columns, so the residual is spatial + analytical and is an upper bound.
2. **Different continent, design and support.** Independent populations, not a
   replication.

**Depth is NOT a third reason, and the earlier claim that it was is withdrawn.**
This entry originally read *"shallower depth is more variable"*, taken from the
task brief. **The numbers cited in its own support refute it:** Poeplau's layer
CVs *rise* with depth — 9.3% at 0–10 cm → 10.2% at 10–30 cm → 25.8% at
30–50 cm. Since our 0–15 cm window is *shallower* than Poeplau's 10–30 cm layer,
that trend predicts NAPESHM should come out **lower**, which is the opposite of
what this entry is explaining. The same data is read the correct way elsewhere in
this file (D-026) and in `VC-WPS-002`'s note ("essentially flat with depth over
0–30 cm, then jumps to 25.8% at 30–50 cm").

So depth is, at best, neutral here and mildly *against* the observed ordering.
Two reasons still push the right way, and the observed gap is small, so the
conclusion stands — but it stands on a narrower base than first written, and
saying "three independent reasons that all push the same way" overstated it.

*Recorded rather than quietly edited, because the failure mode is the point:* the
brief's other bad figure (7.5–8.5%) was caught and corrected two paragraphs
above, while this one was passed straight through in the same pass. Checking a
supplied *number* against the table and not checking a supplied *causal claim*
against the same table is an inconsistency in the review, not bad luck.

**Direction and magnitude both behave.** Between-plot (11.1–12.1%) sits just
above within-plot (9.3–10.2%) — the ordering theory demands, with a gap of a few
percentage points rather than a factor. That is the strongest corroboration
either estimate has: an *n*=8 German study and a North American dataset of 1,450
SOC-bearing EUs across 93 sites (212 EUs / 14 sites after the D-024/D-025/D-028
filters), built by different people for different purposes, landing a few points
apart with the sign that was predicted before either number was computed.

*Second figure correction, recorded here so it survives into the permanent
record.* The comparison was proposed against "a 1,385-EU dataset". **1,385 is a
real number from our own output but it is not the dataset size** — it is
`design_sensitivity.all_designs_all_eu_types` in
`data/processed/g1_napeshm.json` (1,385 EUs / 443 treatments / 86 sites), i.e.
the *widest fitted cohort* after the ≥2-replicate filter with the D-024 and
D-025 filters removed. The dataset holds **1,450** SOC-bearing EUs across **93**
sites (`filter_cascade` stage 1); the headline uses **212** across 14. Using
1,385 as "the dataset" understates it by 65 EUs and 7 sites.

**What this does NOT license.** It does not close G3. A within/between **ratio**
still cannot be read off two studies on two continents at two depths, and no row
claims one — see D-030. The value here is that two independent estimates
corroborate each other's *magnitude*; that is a sanity check on both, not a new
quantity. Merging them, averaging them, or deriving a ratio from them would
manufacture a number neither dataset supports.

---

**D-032 — An open decision may not govern a live constant or a verified baseline
row. Enforced in `tests/test_decision_guard.py`, not requested in prose.**

D-028 was written up as "OPEN — for the PI", and shipped as the active constant
behind `VC-BPS-005/006` regardless. Nothing objected, because the status lived
only in this document and the constant lived only in a script. **Prose does not
fail CI.**

The fix copies R6, which has worked: R6 states the condition in data (a row whose
`verification` is `unverified` cannot be `use_as: baseline`) and a rule refuses
to pass while it holds. The LUCAS rows have stayed locked out of use for exactly
as long as they have been unverified, with no discipline required from anyone.

Extended the same way:

* `src/loam/decisions.py` gives every decision a machine-readable status and
  every load-bearing constant a `governed_by` pointer to the decision behind it.
* A constant's `proposed` / `decided` status is a **derived property**, never a
  stored field. Storing it would let a constant assert `decided` beside an `open`
  decision — precisely the state that shipped. Derived, that state cannot be
  represented, and a test asserts the field stays derived.
* `python -m loam.build_table` prints `<-- PROPOSED, NOT DECIDED` for any such
  constant on every run, beside the existing `NO BASELINE` flags, and names the
  baseline rows exposed to it.
* Two tests fail while any open decision governs a live constant or is cited by a
  verified baseline row.

**Consequence, stated plainly: the suite is RED on merge of this change, and
should be.** `CLIMATE_ENVELOPES` still rests on D-028, and `VC-BPS-005/006` still
cite it. The guard is reporting a true condition that predates it. The two honest
routes to green are to **settle D-028**, or to **demote `VC-BPS-005/006` out of
`baseline`** until it is settled — which would reopen G1. Softening the test is
not a third route; it would restore exactly the silence this decision exists to
end.

---

**D-033 — The IPCC 2006 default climate regions CANNOT be derived from NAPESHM's
published columns. No proxy is substituted; the classification is not
implemented.** ⚠️ *This blocks the preferred resolution of D-028.*

The scheme is IPCC 2006, Vol 4 Ch 3, **Figure 3A.5.2, p. 3.39** ("Classification
scheme for default climate regions"), read directly from the PDF. Transcribed
literally, the decision tree is:

```
MAT > 18 °C AND ≤ 7 days of frost/year ?
├─ yes → Elevation > 1000 m ?      yes → Tropical Montane
│        └─ no → MAP > 2000 mm ?   yes → Tropical Wet
│                └─ no → MAP ≤ 2000 mm and > 1000 mm ?  yes → Tropical Moist
│                        └─ no → Tropical Dry
└─ no → MAT > 10 °C ?
         ├─ yes → MAP:PET > 1 ?  yes → Warm Temperate Moist / no → Warm Temperate Dry
         └─ no → MAT > 0 °C ?
                  ├─ yes → MAP:PET > 1 ?  yes → Cool Temperate Moist / no → Cool Temperate Dry
                  └─ no → each mean monthly temperature < 10 °C ?
                           ├─ yes → MAP:PET > 1 ?  yes → Polar Moist / no → Polar Dry
                           └─ no  → MAP:PET > 1 ?  yes → Boreal Moist / no → Boreal Dry
```

Against the 94 NAPESHM sites, two required inputs are **absent and not
reconstructible**, and one branch is unreachable:

**(1) MAP:PET — required, unavailable.** It decides *every* leaf the NAPESHM
sites can reach (all four temperate outcomes). NAPESHM publishes no PET column
and no monthly climate series. The two candidate proxies both fail, for
different and checkable reasons:

* `hargreave_cmd` is a **monthly-summed one-sided deficit** — Σ months of
  max(0, Eref − P), per its dictionary entry and Wang et al. 2016. Months in
  surplus contribute zero and their surplus is discarded, so annual PET is not
  recoverable from it, even in principle. The data show the loss directly: a
  Mexican highland site with MAP 1101 mm carries CMD 1446 mm, as large as a
  desert site's, because its rain is monsoonal. CMD measures **seasonality**, not
  the annual ratio.
* `mi` is Thornthwaite's Moisture Index, and its 1948 form is
  `Im = (100·S − 60·D)/PET`. It is **not** `100·(MAP/PET − 1)`, which we verified
  rather than assumed: the naive form is falsified by the data. Observed `mi`
  floors at **−53** and never goes below −60, which is the hard floor the
  1948 formula implies as P/PET → 0 (`Im → 60·P/PET − 60`); the naive form allows
  −100. And inverting the naive form at the driest site (MXSO02: MAT 25 °C,
  MAP 167 mm) implies PET = 355 mm, which is physically impossible for a hot
  desert whose own Hargreaves deficit is 1813 mm. The 1948 reading implies
  ≈1430 mm, which is right.

  The consequence is not that `mi` is a noisy proxy — it is that **no `mi`
  threshold can reproduce the IPCC test at all.** From the water balance
  (P = AE + S, PET = AE + D), MAP:PET = 1 ⟺ S = D, and at S = D the index is
  `Im = 40·S/PET`, which **varies with S/PET** instead of taking one value. The
  IPCC contour maps to a *moving* `mi` value, and S and PET are not published
  separately.

  **How far `mi` alone *can* be pushed — a bound, replacing an earlier vague
  one.** This entry first said "23 of 94 sites sit in the band where that
  contour could fall", with no stated criterion; that number is withdrawn. The
  defensible version is a closed bracket. Substituting `S = P − PET + D` into
  `Im = (100S − 60D)/PET` gives `D = [PET·(mi+100) − 100P]/40`, and the physical
  constraints `S ≥ 0`, `D ≥ 0`, `D ≤ PET` then bound PET:

  ```
  max( 100P/(mi+100), 60P/(mi+60) )  ≤  PET  ≤  100P/(mi+60)
  ```

  Testing `PET < P` against that bracket decides the IPCC moisture split
  **exactly** at the extremes and not at all in the middle:

  | condition | conclusion | sites |
  |---|---|---|
  | `mi < 0` | lower bound > MAP → **Dry** | 35 |
  | `mi > 40` | upper bound < MAP → **Moist** | 40 |
  | `0 ≤ mi ≤ 40` | bracket straddles MAP → **undecidable** | **19** |

  So **75 of 94 sites are decidable from `mi` alone, and 19 are not.** The
  bracket also *proves* the −60 floor observed above rather than inferring it:
  `S ≥ 0` forces `mi > −60`. This is a genuinely better statement of the blocker
  — it is smaller than first claimed, exactly located, and derived rather than
  asserted. It is still fatal to the deliverable, because the scheme has to
  classify every site, not 80% of them.

**(2) Frost days — absent from NAPESHM, but OBTAINABLE. This half of the blocker
is withdrawn.** The first test needs "≤ 7 days of frost/year". NAPESHM has no
frost column anywhere (checked across all 9 SQLite tables, all 464 rows of
`dbcolumns.csv`, the XLSX dictionary and the DOCX overview), and `gdd0` cannot
substitute — it is a *growing degree-day sum above 0 °C accumulated to the
sampling date*, which censors cold entirely (a −1 °C day and a −30 °C day both
contribute 0) and is dominated by sampling date rather than climate
(r = 0.84 with day-of-year vs 0.51 with MAT; sites sharing MAT = 10 °C span
`gdd0` 0–2271).

**But "absent from the distributed CSVs" is not "not obtainable", and that
conflation was an error.** Every climate column in `sites.csv` is documented as
*"calculated by SHI from Daymet daily surface weather data set
(doi:10.3334/ORNLDAAC/1328)"* over 2010–2019, and Daymet exposes a public
single-pixel API. Querying it at each site's own published lat/long for daily
`tmin` and counting days ≤ 0 °C is **the same series NAPESHM already used,
reduced with a different operator** — not a proxy.

That identity is verifiable rather than assumed: `floor(mean(daily series))`
reproduces the published integers **39/39 exactly** across all three temperature
columns on all 13 warm sites, including the truncation convention. A different
pixel, version or window would not do that.

The resulting counts settle the clause, and they do **not** fall on one side:

| | sites | mean frost days/yr | tropical test |
|---|---|---|---|
| MXMO01/02, MXSO01/02/03, MXGT01, USTX03 | 7 | 0.0 – 2.8 | ≤ 7 → **Tropical** |
| USFL01/02, USTX05, USAL03/04, USGA01 | 6 | 20.7 – 24.4 | > 7 → **not Tropical** |

Nothing sits near the boundary — the gap is 2.8 to 20.7. Under the committed
classifier the 6 become Warm Temperate Moist (**inside** our temperate scope
lock) and the 7 become Tropical Dry/Montane (**outside** it), so this variable
decides scope membership for 13 of 94 sites. NAPESHM's own EPA/CEC ecoregion
labels split the same 13 the same way (6 Eastern Temperate Forests vs 5 Tropical
Dry Forests), which is independent corroboration.

**Two bounding arguments were tested and are dead**, recorded so they are not
retried: (a) *a mean cannot bound a count* — certifying ≤ 7 frost days from
`site_meanmin_temp` would require the annual mean daily-minimum to sit within
~0.5 °C of the annual *hottest* daily-minimum; empirically 6 sites have
`site_meanmin_temp` of 12–13 °C and still record 20.7–24.4 frost days.
(b) *`min_annualtemp_sd` cannot help* — it is the SD across ten **annual
averages** (interannual), not within-year daily variability, it is rounded to
integers taking only {0, 1}, and 8 of the 13 warm sites have it equal to 0, which
under a Normal would "certify" zero frost days as a pure rounding artifact. True
within-year daily `tmin` SD is 2.9–8.4 °C. The assumption picks the answer rather
than supporting it.

**Net: frost days require one external call to the source NAPESHM itself cites.
MAP:PET remains the blocker.**

**(3) The Polar/Boreal branch is unreachable, so its missing input is harmless.**
"Each mean monthly temperature < 10 °C" needs monthly temperatures, which NAPESHM
also lacks — but that test is only reached when MAT ≤ 0 °C, and **no NAPESHM site
is ≤ 0 °C** (minimum MAT is 4 °C). This is a genuine short-circuit, not an
approximation.

**Separately: the climate columns are integer-rounded**, which would blunt the
scheme even with the missing inputs supplied. `site_mean_temp` takes only whole
degrees, and the thresholds sit on integers: **13 sites are at exactly MAT 10**
and **7 at exactly 18**, i.e. exactly on the ">10?" and ">18?" cut points, with
true values anywhere in ±0.5 °C. A fifth of the dataset would be assigned by
rounding artifact.

**Why a PARTIAL classification does not rescue this — the decisive argument, and
it comes from Ch 5 itself.** The obvious salvage is to publish the half we can
get: classify sites Warm vs Cool Temperate from MAT alone and leave moist/dry
undetermined. **That inverts the brief's own rationale**, which was that Vol 4
Ch 5 stratifies cropland stock-change factors this way. Read against **Table
5.5, pp. 5.17–5.18** (checked verbatim), its two columns are:

* **Temperature regime** takes only `Temperate/Boreal`, `Tropical`,
  `Tropical montane`, `All`, `Temperate/Boreal and Tropical`.
  **"Warm Temperate" and "Cool Temperate" never appear.**
* **Moisture regime** splits *every* Temperate/Boreal row: F<sub>LU</sub>
  long-term cultivated **Dry 0.80 / Moist 0.69** (a 14% relative difference);
  F<sub>MG</sub> reduced till 1.02 / 1.08; no-till 1.10 / 1.15; F<sub>I</sub> low
  0.95 / 0.92.

Footnote 1 states it outright: *"Where data were sufficient, separate values were
determined for temperate and tropical temperature regimes; and dry, moist, and
wet moisture regimes."*

**So the axis we can deliver is exactly the axis Ch 5 pools, and the axis we
cannot deliver is exactly the axis it stratifies on.** A partial classification
buys nothing for the stated purpose. Worse, "Cool Temperate (moisture
undetermined)" is not an incomplete IPCC label but a **category error**: it names
an *interior node* of Figure 3A.5.2, not one of the twelve regions, and it
indexes no row of Table 5.5, whose interior node is `Temperate/Boreal` anyway.
The same holds one chapter over — Vol 4 Ch 2 Table 2.3's reference stocks are
`Cold temperate, dry / Cold temperate, moist / Warm temperate, dry / Warm
temperate, moist`, so a bare temperature label selects a *pair* of rows, never a
row.

*(One thing the temperature axis alone does settle honestly: 74 of 94 sites have
`site_mean_temp` ≤ 17, so their true MAT is below 18 even under ±0.5 °C rounding
and they are unambiguously **not Tropical** — which is a defensible scope claim
for D-028, and a real improvement on an arbitrary private envelope. It is not a
stratification and assigns none of the twelve regions.)*

**Why we stopped rather than approximated.** Substituting `mi > 0` for
`MAP:PET > 1` would look faithful, would be cited as "IPCC climate regions", and
would be wrong in a way no reader could detect from the output — the failure is
in a threshold's *meaning*, not in its precision, so it would not show up as
scatter or as a widened interval. The entire argument for adopting the IPCC
scheme (D-028's rationale: that Vol 4 Ch 5 stock-change factors are stratified
this way, so our G1 indexes to the framework a project's declared climate zone is
written in) **evaporates if the labels are ours rather than IPCC's**. A
mislabelled region is worse than an admittedly private envelope, because it
invites exactly the cross-walk it cannot support.

**Upstream documentation bug, found while checking the above and worth
recording:** `data/raw/napeshm/dbcolumns.csv` **swaps the descriptions of
`site_meanmax_temp` and `site_meanmin_temp`** — the former is described as
"10 year average of daily *minimum* temperatures" and the latter as "daily
*maximum* temperatures". The data are fine (max > min throughout); the
dictionary is wrong. Anyone trusting the description rather than the column name
would invert them.

**How to unblock, in ascending cost.** Any of these makes the classification
implementable; none can be done from the repository as it stands:

1. **Join an external PET/frost climatology to the site coordinates.** All 94
   sites have lat/long. TerraClimate or WorldClim v2 supply monthly PET and
   monthly temperature; Daymet — the source NAPESHM itself used — supplies the
   frost-day counts, and **this half is already demonstrated above**, verified
   against the published columns 39/39. This yields the real MAP:PET, real frost
   days and real monthly temperatures — a faithful implementation, at the cost of
   a new external dependency and its own provenance row. **Only MAP:PET is
   actually outstanding.**
2. **Ask the Soil Health Institute for the intermediate climate products.** `mi`
   was computed by SHI from Daymet, so S, D and PET existed at some point. If
   PET is released, MAP:PET is immediate and no new dataset is needed.
3. **Stratify by a scheme NAPESHM can actually support** — e.g. EPA Level I/II
   ecoregions, already present as `na_l1code`/`na_l2code` — and state plainly
   that it is *not* the IPCC classification and does not index to Vol 4 Ch 5.

Option 1 is the one that delivers what D-028 wants. Recorded here so the next
attempt starts from the blocker rather than rediscovering it.

---

**D-034 — The IPCC classifier is implemented and committed, but deliberately
NOT fed.** `src/loam/ipcc_climate.py`, tested at every leaf.

D-033 established that NAPESHM cannot supply MAP:PET or frost days. That is a
statement about the *data*, not about the *scheme* — the decision tree itself
transcribes exactly, so it is written down exactly, and the next attempt starts
from a tested classifier instead of re-reading a PDF.

Two properties make an unfed classifier worth committing rather than a liability:

* **It refuses rather than defaults.** `classify()` raises `MissingClimateInput`
  naming the variable it lacks. There is no fallback path, so the proxy
  substitution D-033 rules out cannot creep back in through a default argument.
* **Inputs are demanded lazily, per branch.** This makes D-033's short-circuits
  executable rather than prose: frost days are required only when MAT > 18 °C
  (so NAPESHM's missing frost column bites on 13 of 94 sites, not all 94), and
  monthly temperatures only when MAT ≤ 0 °C (so NAPESHM's missing monthly series
  costs nothing at all, its coldest site being 4 °C). Tests pin both.

It is wired to nothing. `CLIMATE_ENVELOPES` is untouched and D-028 stays open,
so **the guard from D-032 is still red, and correctly so.** Committing a
classifier is not the same as classifying anything.

---

**D-021 UPDATE — Wuest's PNW dryland sites classify as TEMPERATE under IPCC,
which is the answer D-021 asks for. NOT closed here, because the inputs were
supplied rather than sourced.** ⚠️ *Still for the PI.*

Running the stated site climate (Pendleton OR region, MAT ≈ 10 °C, MAP
300–400 mm) through `loam.ipcc_climate.classify`:

| MAT | MAP:PET | region | temperate? |
|---|---|---|---|
| 9–10 °C | 0.5–0.7 | **Cool Temperate Dry** | ✅ |
| 10.5–11 °C | 0.5–0.7 | **Warm Temperate Dry** | ✅ |

**The moist/dry half is robust.** MAP:PET > 1 would need MAP above roughly
600 mm at this MAT (Thornthwaite PET at 10 °C, mid-latitude, is ~550–650 mm);
observed MAP is 300–400 mm, giving a ratio near 0.5–0.7. "Dryland" is in any
case definitionally moisture-limited, i.e. MAP < PET. **Dry** either way.

**The cool/warm half sits exactly on a threshold** — the figure's test is
`MAT > 10?`, and the site is quoted at "approximately 10". Both branches land
in a temperate class, so *the D-021 question is answered regardless*, but the
specific region is not determined by the numbers we have.

**Why this does not close D-021 by itself.** MAT and MAP here came from the task
brief, not from Wuest (2024), whose full text is paywalled and whose depth is
already recorded as assumed rather than confirmed (D-014). Classifying a study
on second-hand climate figures would repeat, in a new place, exactly the
substitution D-033 refuses. To close D-021 properly: take the site coordinates
from the paper and join the same external climatology that unblocks D-033
(option 1 there) — **one dependency serves both**. Until then this is a strong
indication, not a classification.

`VC-TMP-001/002` are **not** promoted in this change, as instructed. Note that
promoting them would also require D-014's separate depth concern to be resolved;
climate is necessary, not sufficient.

> **D-021 IS NOW CLOSED — DECIDED 2026-08-10. Pacific Northwest dryland cropping
> is inside the temperate scope.** The condition set out above has been met: the
> inputs are no longer second-hand. Mean annual precipitation now comes from the
> **provider's own site paragraphs** in the Ag Data Commons record (Adams 401,
> Echo 265, Moro 269, Ritzville 296 mm yr⁻¹), and mean annual temperature is
> computed from the dataset's **own `avgT` column** — the study's own weather
> stations, averaged over calendar months so that the unsampled winter months do
> not bias it warm. Run through the committed classifier (`ipcc_climate`,
> partial per D-028):
>
> | site | MAT | MAP | temperature regime |
> |------|-----|-----|--------------------|
> | Adams | 11.10 °C (12 mo) | 401 mm | Warm Temperate |
> | Echo | 12.81 °C (11 mo) | 265 mm | Warm Temperate |
> | Moro | 9.72 °C (12 mo) | 269 mm | Cool Temperate |
> | Ritzville | 9.37 °C (12 mo) | 296 mm | Cool Temperate |
>
> Warm at two sites, cool at two, **Temperate at all four** — which is the axis
> the question was about. The full tree still returns `unclassified` on
> `map_pet_ratio` at every site, exactly as it does for NAPESHM, and that is
> left undetermined rather than invented. Note the dataset's own use limitation
> already describes the climate as *"semi-arid Mediterranean"*, so the moisture
> regime is qualitatively documented by the provider even though the IPCC ratio
> is not computable.
>
> Two honest limits on this. The MAT is a **study-period average from the study's
> own stations**, not a published 30-year normal; and Adams-residue and Echo are
> each missing one calendar month, which biases those two slightly warm — though
> Adams-tillage covers all twelve at the same site and gives 11.10 °C, and both
> sites are far enough from the 10 °C warm/cool boundary in the direction that
> matters that nothing turns on it. Neither limit touches the Temperate finding,
> which needs only "not tropical, not boreal" and has 6 °C of headroom at each
> end.
>
> **Scope no longer blocks promotion of a PNW-derived temporal row.** D-014's
> separate depth concern was the other half, and D-042 settles it with fact
> rather than assumption.

---

## Prior art: Potash et al. 2025 — logged, not yet implemented

**Recorded in this change; to be implemented in the NEXT one.** Nothing below
touches a variance-table row, the schema, or a constant. The paper itself is
**not yet in `data/literature/`** — it needs downloading (open access,
doi:10.1088/1748-9326/ada16c; data doi:10.6084/m9.figshare.28083182; R source
`asc.illinois.edu/soc-econ`).

Potash, E., Bradford, M. A., Oldfield, E. E., & Guan, K. (2025). Measure-and-
remeasure as an economically feasible approach to crediting soil organic carbon
at scale. *Environmental Research Letters*, **20**, 024025.

---

**D-035 — The schema needs `scales_with_interval` (true/false) per row. Our six
components are NOT all the same kind of quantity, and the table currently
pretends they are.** *To implement next PR.*

Their equation 1:

```
SE^2 =  Y*sig_b^2 / (N*p1)
      + (Y*sig_w^2 + 2*sig_n^2) / (N*p1*A*d2)
      + 2*sig_l^2 / (N*p1*A*d2/n3)
```

Read the multipliers, because they are the whole point:

* **`Y` multiplies variance in the RATE of change** — between-field (`sig_b`)
  and within-field (`sig_w`). These accumulate with the monitoring interval:
  a longer interval means more time for fields to diverge.
* **`2` multiplies measurement error** — relocation (`sig_n`) and lab
  (`sig_l`). Incurred exactly **twice**, at baseline and at remeasurement, and
  **does not grow with the interval** at all.

Our table records all six components as one undifferentiated `cv_pct`. Under
that representation, any MDC computed over a multi-year interval scales *every*
term the same way, which is wrong for at least three of the six and increasingly
wrong the longer the interval.

**And the error is not incidental — it is the exact quantity Potash et al. set
out to document.** The economy of temporal scale in their paper *is* the gap
between the `Y` terms and the `2` terms. A table that cannot represent the
distinction cannot reproduce their central result, let alone check it.

Which of our components take which value is itself a judgement to be made row by
row next PR, not asserted here. First approximation: `analytical`,
`relocation` and `depth_bd_convention` are measurement-side (`false`);
`temporal` is interval-side (`true`); the two spatial components need thought,
because our rows measure variance in the **stock** rather than in the **rate**
(see D-037).

---

**D-036 — OPEN: our analytical error and theirs differ by 4×. Resolve by
tracing both to primary sources; do not average.** ⚠️ *Unresolved.*

Their `sig_l` = **2 Mg C/ha**, which at 0–30 cm is roughly **4%** relative error
in SOC concentration. Our `VC-ANA-001` is **1%** (Poeplau et al., verified full
text, `use_as: baseline`).

A factor of four in the analytical term is not a rounding difference, and
analytical error enters twice per the D-035 multipliers, so it is not negligible
in an MDC either. **Splitting the difference or averaging would manufacture a
number neither source supports** — the same error D-031 refuses for the
within/between comparison.

Resolve by finding out what each number actually measures. Plausible and
checkable reasons for the gap, in rough order of likelihood: theirs may bundle
sampling-and-handling error with instrument error where ours isolates the
instrument; theirs is on a **stock** basis (Mg C/ha, so it inherits bulk-density
error) where ours is a **concentration** CV; and the two may assume different
numbers of composited cores.

**Guard note, stated plainly because it is a real hole:** this decision is
`open` and it bears on `VC-ANA-001`, which is a live verified baseline row — yet
the D-032 guard will **not** fire on it, because the row does not cite D-036 in
its prose and is not script-derived, the two routes the guard checks. Wiring
this exposure in means editing a row, which is out of scope for a log-only
entry. **Do it in the same PR that implements D-035**, and treat it as evidence
that the guard's two routes do not cover every way a row can depend on an open
question.

---

**D-037 — Potash et al.'s parameters are recorded as CANDIDATE cross-check
rows, not merged.** *To implement next PR.* US Midwest no-till defaults, all on
a Mg C/ha basis, 0–30 cm:

| symbol | value | quantity |
|---|---|---|
| `sig_b` | 0.5 /y | between-field variance in SOC **rate of change** |
| `sig_w` | 1 /y | within-field variance in SOC **rate of change** |
| `sig_n` | 5 | relocation error |
| `sig_l` | 2 | lab / analytical error |
| `tau` | 0.3 /y | treatment effect |
| `A` | 25 ha | field area |

**Two things must be carried with these numbers or they will be misused.**

*First, the evidence asymmetry runs in our favour, and should be recorded rather
than smoothed over.* Their `sig_b` traces to a **single Iowa study**
(Al-Kaisi & Kwaw-Mensah 2020). Ours (`VC-BPS-005/006`) traces to **1,450
SOC-bearing EUs across 93 sites**, of which 212 EUs across 14 sites survive the
D-024/D-025/D-028 filters. Where the two disagree, ours is the better-supported
estimate, and a writeup should say so plainly rather than presenting them as
peers.

*Second, and more important: `sig_b` and `sig_w` are variance in the RATE OF
CHANGE (units per year). Our between-plot rows are variance in the STOCK.* These
are different quantities with different units, and **must not be written into
the same rows or compared numerically without an explicit, logged conversion
decision.** Merging them silently would be D-020's error (concentration CV
treated as stock CV) in a new dimension, and harder to spot because the units
differ by a factor of "per year" rather than by a factor of anything visible.

This also feeds back into D-035: because their spatial terms are rate variances,
they carry `Y`; ours, being stock variances, do not obviously carry anything
until the conversion question is settled.

---

**D-038 — Potash et al. 2025 is the nearest prior art. Cite it in any writeup,
and state four differences plainly.** *To implement next PR.*

1. **Different question, and ours is upstream.** They ask *"is this project
   economically feasible?"*; we ask *"is this claim resolvable?"* Theirs
   **presupposes** ours — a feasibility calculation assumes the underlying
   change is detectable at all. Positioning us as downstream of them would
   invert the dependency.
2. **Their `sig_b` is fixed and geography-independent, and they say why:**
   explicitly "for lack of information". **Our covariate-conditioned variance
   surface is that missing information.** This is the sharpest statement of our
   contribution available, and it is in their own words.
3. **Their model has NO within-year temporal variance term at all.** Check each
   term: `sig_n` is spatial relocation, `sig_l` is lab, `sig_w` is heterogeneity
   in the *rate* of change between points in a field. **Nothing represents
   seasonal or short-term fluctuation at a fixed point** — which Wuest (2024)
   measured at 15–32% of random error. Our `temporal` gap (G4) **is also their
   gap.** That reframes our weakest component: closing it is a contribution to
   the literature, not a deficiency in our table.
4. **Phase 5 audit hook: `z_deduct` = 0.43 standard errors, following Verra
   VM0042.** Published, auditable, and thin — a single constant standing in
   for the entire uncertainty deduction. This is the specific number a Phase 5
   audit can test against, and the obvious place where a better variance model
   changes a real crediting outcome.
   > **VERIFIED AGAINST PRIMARY 2026-08-12 (D-057).** The figure is correct:
   > VM0042 v2.2 §8.6.4 Eq. 74 gives `t0.667` "equal to approximately **0.4307**
   > at large sample sizes", crediting at the 33.3rd percentile. It was cited
   > here from Potash et al. rather than from the methodology, so it was
   > unverified — but not misattributed. **Two amendments:** it is a *t*-value,
   > not a constant, so the deduction grows as `n` falls; and it could not be
   > located in the v2.0 text, so the version qualifier **"v2.0" is withdrawn**
   > pending the approved v2.0. See D-057.

---

**D-039 — FINDING, for the paper rather than a caveat footnote: NAPESHM cannot
be fully classified under the IPCC 2006 scheme, and the reason is a
reusability gap in the field's flagship soil-health dataset.**

**87 of 94 sites are unclassifiable**, every one of them blocked on the same
variable. Not because the sites are unusual — because NAPESHM publishes:

* **no PET**, and
* **no documented Hargreaves formulation or averaging window** — `hargreave_cmd`
  is described only as "Hargreave Climate Moisture Deficit based on 1981–2010
  normals … extracted from a GIS layer", which names neither the Hargreaves
  variant, the reference-ET convention, nor how months were aggregated.

The second point is the load-bearing one. **PET's absence alone would be
recoverable** — the coordinates are published, and external climatologies exist.
What makes it irrecoverable *as NAPESHM's own number* is that there is no
specification to reproduce. Any PET we compute would be **ours wearing an IPCC
label**, and the resulting region would be unfalsifiable against the dataset that
supposedly produced it. Frost days were recoverable precisely because the
dictionary **does** name its upstream source, which let us prove identity to
60/60 published integers. The contrast is the finding: *the same dataset is
reusable exactly where it documents provenance and unreusable where it does
not.*

**Why this belongs in the paper.** NAPESHM is the North American reference
dataset for soil health measurement — 94 sites, six years, a designed
inter-comparison. If it cannot be indexed to the IPCC climate regions that
national inventories and every Verra/CDM-lineage crediting methodology are
written in, then **its numbers cannot be carried into an inventory or a
crediting context without an undocumented translation step** — the exact step
D-028 was created to avoid. That is a structural limitation on the reuse of the
field's flagship dataset, and it is invisible until someone actually tries the
join, which is what we did.

**Stated precisely, so it cannot be read as a complaint about data quality:** the
measurements are fine. The *metadata* is incomplete in one specific,
consequential way — a derived climate column published without its formula. The
fix is small and entirely within SHI's power: publish the PET series, or the
Hargreaves specification and averaging window. One paragraph in a data
dictionary would make 87 sites classifiable.

**Recommended framing:** a short subsection in the methods or discussion,
carrying (a) the 7/87 split, (b) the frost-day recovery as the positive control
that proves the point is about documentation rather than difficulty, and (c) the
one-paragraph fix. Not a limitations bullet.

---

**D-040 — the two caveat flags on `VC-BPS-005/006` are CLOSED on evidence, the
`stock < concentration` result is confirmed on a common sample, and texture is
NOT a stratifier for this component.** Three sensitivity checks run before Phase
0 closes. No row was added, no scope changed, no constant moved; the two G1 rows
gained findings and lost two deferrals. Script: `scripts/sensitivity_g1.py`,
results `data/processed/g1_sensitivity.json`.

**Check 1 — leave-out test on the sites the scope change re-admitted.** D-028
replaced a private envelope whose *stated* purpose was to exclude Mexican
highland (Cwb, summer-rain) sites on moisture-seasonality grounds, with an IPCC
temperature axis that does not encode moisture seasonality. That was a live
worry: the axis that might have separated those sites is the one we cannot
resolve. It is also directly testable — drop them and look.

| row | with | without | shift | 95% CI width |
|-----|------|---------|-------|--------------|
| `VC-BPS-005` (concentration) | 11.948% (386 EU) | 12.248% (261 EU) | **+0.300** | 3.97 |
| `VC-BPS-006` (stock) | 11.456% (372 EU) | 11.304% (261 EU) | **−0.152** | 3.52 |

Both shifts are roughly **a thirteenth and a twenty-third of the interval**, and
they point in *opposite directions* — the pattern of noise, not of a bias the
envelope was protecting against. Note also that the sites are **8, not 10**:
10 pass the climate scope, but `MXAG01` and `MXQT02` are removed by D-024/D-025
before climate is ever applied. The earlier "10" conflated scope with sample and
is corrected on the row.

*The same conflation appears once more, in D-028's rounding-fragility caveat,
and is corrected there in place:* of the four sites whose scope membership turns
on integer rounding, `MXAG01` and `MXQT02` contribute **0 EUs**, so only
`MXPU01` and `MXSL01` can move a number. Dropping both — the full worst case —
shifts concentration 0.479 and stock 0.593, against CI widths of 3.97 and 3.52.
One cause, two symptoms, both now measured rather than asserted.

*Why the flag closes rather than defers.* A deferral says "we do not know yet".
We do know: on this quantity, at this precision, the disputed sites are worth
0.3 points and a third of the sample. Re-deriving if the moisture regime ever
arrives remains correct bookkeeping (D-028 stands), but the row no longer carries
an open worry about it, because the worry has an answer.

**Check 1b — the 55 two-replicate treatments are the SAME finding, not a second
one.** All 55 are Mexican. The USA contributes 75 treatments and **none** has
fewer than 3 replicates (Mexico 2→55, 3→5; USA 3→43, 4→29, 5→2, 6→1). So the
"weak per-treatment support" caveat and the "re-admitted sites" caveat were never
two flags: removing the Mexican sites removes every two-replicate treatment, and
the leave-out test above already tested both at once. Both close together, on one
number.

**Check 1c — the confound this leaves behind, recorded so nobody trips on it
later.** Because all 55 two-replicate treatments are Mexican and no USA
treatment has fewer than three replicates, **country and per-treatment support
are completely aliased in this sample.** Any future Mexico-vs-USA contrast is
also, unavoidably, a 2-replicate-vs-3+-replicate contrast. A country difference
in an estimated variance would therefore be indistinguishable from the sampling
behaviour of a variance estimated on one degree of freedom, which is badly
behaved and biased in a known direction. **Nothing in this table may read a
Mexico/USA difference as a climate difference**, and any analysis that splits on
country has to weight or exclude by replicate count first.

**Check 2 — `stock < concentration` survives a common-sample comparison.** The
two rows are derived on different samples (bulk density is missing on 14 EUs, one
site), so the reported gap of 0.492 points mixed a real effect with a sample
mismatch. That matters because the ordering is being used **mechanistically** —
bulk density covarying against concentration such that stock is the *less*
variable quantity — and a mechanistic claim cannot rest on a cross-sample
difference. Recomputed on the 372-EU intersection (128 treatments, 25 sites):
concentration **11.897%**, stock **11.456%**, gap **+0.441**. The mismatch
accounts for **0.051 points** of the 0.492. The ordering is a property of the
data.

**Check 3 — texture stratification: no signal, exploratory, no rows.** Tercile
splits on clay (breaks 18.0 / 27.1%) and sand (24.2 / 39.9%):

* clay — high 13.557%, mid 10.946%, low 11.315%; spread **2.611** against a
  widest bin CI of **10.556**. Not monotone, and the spread is a quarter of the
  noise on the bins.
* sand — high 13.305%, mid 10.871%, low 9.615%; spread **3.690** against a widest
  bin CI of **9.834**. Monotone in direction but still well inside the noise.

**No stratified rows are written and none should be.** A three-way split of 26
sites leaves 9–12 sites per bin, and cluster bootstrap CIs at that size are wider
than every difference they would separate.

**The three checks together are a Phase 0 RESULT, not three loose ends.**

> **Between-plot CV in cropland SOC is approximately invariant across the
> covariates a spatial MDC surface would be built from.**

The three checks were run separately and answer separate questions, but they
point at one thing. Climate region — the single largest scope change this
project has made, retiring an envelope and re-admitting a third of the sample —
moves the estimate **0.2–0.3 points against a ~4-point confidence interval**.
Binned clay shows **no monotone signal at all**. The joint model, given both
texture and carbon level at once and free to use them, reaches **R² = 0.093**.
Three independent attempts to make this quantity depend on where you are, and it
does not.

**The caveat travels with the finding, everywhere it appears:** the joint model's
sample is **75 of 80 treatments from the USA**, because excluding two-replicate
treatments excludes Mexico almost entirely (check 1b). So this is a statement
about between-plot variance in North American cropland, weighted heavily toward
the USA, at 0–15 cm. It is not a global claim, and it has not been tested on a
sample with real climatic spread — precisely because the climate axis that would
give it that spread is the one D-028 could not resolve.

**Consequence, and it is not a small one: Phase 3 Deliverable 3 — the spatially
explicit MDC surface — needs rethinking before we build toward it.** A surface
is worth drawing when the thing it maps varies over space. On this evidence the
noise term does not, or varies far less than the interpolation error of any
surface we could fit. Building it anyway would produce a map whose structure
came from the covariates rather than from the data.

Two possibilities are recorded here, **open, and deliberately not resolved now**:

1. **MDC may vary spatially through the SIGNAL rather than through the noise** —
   through treatment effect size, SOC level, or the depth distribution of change,
   none of which this table currently parameterizes. An MDC surface driven by a
   spatially varying numerator and a flat denominator is a different object from
   the one Deliverable 3 assumes, and possibly a better one.
2. **The conditioning signal may live in temporal variance**, which we have
   never tested for covariate dependence at all. If temporal variance is where
   the geography is, then the spatial surface was being built off the wrong
   component from the start.

**Framing for the writeup — this STRENGTHENS the nearest prior art.** Potash et
al. 2025 held `sigma_b` fixed and geography-independent, and said plainly that
they did so *for lack of information*. We now have the information, and it says
the assumption was approximately right. That is a load-bearing simplification in
the closest published work being independently vindicated, not a gap we caught
them in. Any writeup says it that way round. (See D-038 for the general
positioning, and D-036 for the one place we do disagree with them.)

*One result worth logging from the same scan, still not a row.* Regressing
`log(CV)` on `log(mean SOC)` and sand fraction across the 80 treatments with ≥3
replicates (SD on 1 df excluded) gives `log_mean_soc` β = +0.423 (se 0.176,
t = +2.40) and `sand_frac` β = +0.915 (se 0.370, t = +2.47) — both nominally
significant, R² = 0.093. Two cautions keep it out of the table: the sample is
75/80 USA once two-replicate treatments are dropped, so this is close to a
USA-only statement, and 9% of variance explained will not carry a stratified
baseline. It is a **hypothesis for a future dataset**, filed beside D-029 (whose
raw log-log slope reproduces at +1.223 in this run), not a parameterization.

**What breaks if wrong.** If check 1 is wrong, the G1 headline carries a bias it
has declared absent — but the test is a direct recomputation on a stated subset,
so it is wrong only if the site→country mapping is wrong, which the 55/0
replicate split independently corroborates. If check 2 is wrong, the
bulk-density mechanism loses its evidence and the two rows revert to "different
numbers from different samples". If check 3 is over-read — if someone treats the
sand coefficient as a stratifier — the table would acquire bins whose CIs overlap
completely, which is the failure R6 and D-032 exist to prevent.

---

**D-041 — the temporal component is derived from PRIMARY DATA. The estimator is
crossed plot x occasion random effects on log SOC, treatment fixed, validated
two independent ways.** Script: `scripts/derive_temporal.py`, results
`data/processed/temporal_variance.json`.

`VC-TMP-001/002` were read off Wuest & Durfee's **abstract**, because the paper
is paywalled. That gave a variance *share* (20% temporal, 17% between-replicate)
rather than a variance — a share cannot be added to anything, cannot be checked,
and carried an **assumed** 0–30 cm depth. The underlying dataset is public
domain on Ag Data Commons (doi:10.15482/USDA.ADC/25719348.v1, U.S. Public
Domain), so none of that had to stand. **2195 plot-months, 76 plots, five
monthly series, four sites.**

Per site, on log SOC:

```
log C  ~  treatment  +  (1 | plot)  +  (1 | occasion)
```

Plot and occasion are **crossed**, not nested — every plot is visited on every
occasion, and that is exactly why this design can speak about time. The occasion
effect is what all 12–24 plots do *together* on a date, so it cannot be
within-plot spatial noise (which averages away across plots) and cannot be
plot-to-plot heterogeneity (that is the plot term).

*Occasion is the sampling campaign (`SampleNo`), not the calendar date.* Four
Adams campaigns ran across two consecutive days; keying on date would split
those months into half-occasions and manufacture an occasion effect out of
nothing.

**Validated twice, on purpose.** A mixed-model optimiser is easy to trust
wrongly. Route 1 is REML via `statsmodels`; route 2 is the closed-form ANOVA
moment solution for a balanced two-way crossed design with one observation per
cell. The design is balanced (one missing Ritzville cell), so route 2 is exact.
They agree to within **0.53 CV points** at worst and 0.16–0.39 elsewhere — the
same conclusion from both, not the same decimal. Moments are reported, because
they are closed-form here and cost nothing to refit inside the bootstrap.

**The trap that made them disagree at first, recorded because it is silent:**
`MixedLM` returns `vcomp` in **sorted key order**, not in the order the
`vc_formula` dict was written. With `{'plot': ..., 'occ': ...}` the first entry
is `occ`. Reading them positionally transposes the two components and nothing
complains. Only the moment route caught it.

**Cross-check against the publication we could not read.** Our variance shares
against Wuest's reported ones:

| share | ours | published |
|-------|------|-----------|
| temporal | 18.3% (14.4–28.3) | 20% (15–32) |
| between-replicate | 22.8% (9.4–40.8) | 17% (2–42) |

Close on both, without ever reading the number off the paper. Not identical —
their model surely differs in detail — so this is corroboration that we are
measuring the same things, not a reproduction.

---

**D-042 — the depth on `VC-TMP-001/002` was ASSUMED and the assumption is
WRONG. The five series are not sampled to a common depth, and four of the five
are not on a fixed-depth basis at all.**

| series | site | depth / basis | cores composited |
|--------|------|---------------|------------------|
| AW | Adams, OR (tillage) | **0–30 cm**, six 5-cm increments | 3 (50 mm) |
| CP | Adams, OR (residue) | top **250 kg/m² equivalent soil mass** (≈20 cm) | 3 (25 mm) |
| Echo | Echo, OR | top 250 kg/m² ESM (≈20 cm) | **1** (25 mm) |
| Moro | Moro, OR | top 250 kg/m² ESM (≈20 cm) | **1** (25 mm) |
| Ritz | Ritzville, WA | top 250 kg/m² ESM (≈20 cm) | **1** (25 mm) |

So the existing "0–30 cm, `fixed_depth`" label is right for **one series in
five** and wrong for the other four, which are equivalent-soil-mass stocks to
roughly 20 cm. This is a fact from the dataset description, not an inference,
and it means no single depth label can honestly cover a pooled temporal row.

Two things follow that are easy to miss. First, four of five series are already
**ESM**, which is the convention this project prefers and which removes most of
the bulk-density/depth-convention error (component 6) from those numbers.
Second, the **core count is not decoration** — see D-043.

**The provider's own use limitation, quoted rather than paraphrased**, because
it is documented scope and not our reading: *"Soils were silt loams and the
climate was semi-arid Mediterranean pattern at all four sites tested. Other
soils and climates may produce more or less temporal variability."*

The citation is also now confirmed against Crossref — **Wuest, S. B. & Durfee,
N. (2024), SSSAJ 88(3):830–845** — replacing "volume and pages UNCONFIRMED" and
restoring the second author, who was missing.

---

**D-043 — what this design CAN and CANNOT separate, and therefore why the
temporal component gets a bounded pair rather than a single number.**

Three components come out per site. Two are usable and their meanings are not
interchangeable:

* **`v_occ` — field-wide month-to-month movement. SEPARABLE.** Clean of
  within-plot spatial and of analytical error, both of which average away across
  plots. A **lower bound** on temporal variance, because plot-specific timing
  effects are excluded from it.
* **`v_resid` — plot × occasion + within-plot spatial + analytical. NOT
  separable.** One measurement per plot per occasion; nothing inside can be
  split off by this design.
* `v_occ + v_resid` — what a monitoring programme actually meets when it
  revisits one plot on a new date. An **upper bound** on temporal variance.

| series | between-plot | **occasion** | residual | **combined** (95% CI) |
|--------|--------------|--------------|----------|------------------------|
| AW | 3.38% | 3.32% | 4.07% | **5.25%** [4.7, 5.7] |
| CP | 5.24% | 3.12% | 5.49% | **6.32%** [5.2, 7.4] |
| Echo | 3.35% | 4.42% | 9.01% | **10.05%** [9.1, 10.5] |
| Moro | 3.80% | 3.02% | 5.92% | **6.64%** [5.8, 7.2] |
| Ritz | 3.77% | 4.85% | 10.66% | **11.73%** [10.8, 12.3] |

**Separable temporal: mean 3.75%, range 3.02–4.85%** — strikingly tight across
five series, three years and four sites.
**Combined temporal: mean 8.00%, range 5.25–11.73%.**

**The bounds are not symmetric, and the design says which end to believe.** Two
series composite **three** cores into the analysed value; three analyse **one**.
Within-plot spatial variance enters the residual divided by the core count;
plot-specific timing and analytical error do not. If the residual were pure
within-plot spatial noise, the single-core sites would sit √3 = **1.732** above
the three-core sites. Observed: **8.53% against 4.78%, a ratio of 1.785.**

That is at — very slightly past — the boundary. The moment solve wants a
negative remainder for analytical error and plot-specific timing, and clips at
zero. The honest reading is not "within-plot spatial is 8.9% and everything else
is nil"; it is that **the residual is dominated by within-plot spatial variance,
so the combined figure substantially overstates temporal variance and the true
term sits much closer to the separable 3.75% than to the combined 8.00%.**

Confounded with site — the three-core series are also the two highest-carbon,
deepest-sampled ones, and it is two sites against three. It bounds; it does not
identify. But it is the only handle the design offers on a term the design
otherwise cannot split, and it points one way.

**One caveat that runs the other direction, and belongs on any row.** Samples
were "processed monthly by the same lab", so a per-month analytical batch effect
would be **perfectly confounded with the occasion effect**. `v_occ` is therefore
itself an upper bound on the field-wide temporal term. It is a lower bound on
*total* temporal variance and an upper bound on the *field-wide* part; those are
different statements and the rows must not blur them.

**Consequence for the rows: the combined number is `combined`, and its
`bias_direction` is `inflates`.** No row may present 8.00% as temporal variance
without that label.

---

**D-044 — FINDING: sampling on the anniversary does not buy anything. The
temporal signal is not a repeatable seasonal cycle.**

The standard advice for beating seasonality is to resample in the same calendar
month. This dataset can test that directly, and it fails. SD of the log
difference between two visits to the same plot, 10–14 months apart:

| series | all pairs | **same calendar month** | different month |
|--------|-----------|-------------------------|-----------------|
| AW | 5.92% | 6.01% | 5.89% |
| CP | 8.64% | 8.91% | 8.55% |
| Echo | 13.38% | 12.46% | 13.71% |
| Moro | 8.74% | 8.38% | 8.86% |
| Ritz | 16.85% | 16.60% | 16.93% |

Same-month is **higher** at three sites and lower at two, by fractions of a
point either way. There is no reproducible seasonal cycle to cancel: the
month-to-month movement is year-specific and month-specific, which is what a
weather-driven term looks like and not what a phenological one looks like.

**This matters for the OSSE design directly.** Anniversary sampling is a lever
the simulator could have pulled to reduce temporal noise for free. It cannot.
The temporal term has to be carried, not scheduled away.

*Second, quieter result from the same analysis:* at four of five sites the
observed paired-difference SD matches what independent occasions would predict
(√2 × combined CV) to within a few tenths — Ritzville 16.85% observed against
16.6% predicted, Echo 13.38% against 14.2%. So **occasions may be treated as
independent in an MDC calculation**, which is the assumption the simulator
already makes. Adams-tillage is the exception (5.92% observed against 7.4%
predicted, implying real positive autocorrelation across a year); it is also the
most heavily composited and deepest series.

---

**D-045 — temporal variance shows NO consistent covariate dependence either.
The invariance result of D-040 is not confined to the spatial component.**

D-040 recorded that between-plot variance is approximately invariant across the
covariates an MDC surface would use, and flagged as an open possibility that
"the conditioning signal may live in temporal variance, which we have never
tested". It has now been tested.

* **Between sites** — a site's SOC level against its combined temporal CV:
  Spearman rho **−0.700, p = 0.188** (n = 5). Suggestive of *lower* variability
  at higher carbon, and nowhere near significant on five points. It is also
  fully confounded: the two high-carbon sites are the two three-core composites
  (D-043). Among the three single-core sites, mean SOC of 1493 / 1903 / 1932
  g m⁻² maps onto temporal CV of 10.05 / 6.64 / 11.73% — **not monotone**, which
  removes most of what the rho was carrying.
* **Within sites, plot SOC level** — signs are **inconsistent across sites**:
  Adams-residue rho −0.671 (p = 0.017), Echo +0.547 (p = 0.028), Ritzville
  +0.610 (p = 0.002), Adams-tillage +0.070, Moro +0.448. Three "significant"
  results pointing two different directions is not a covariate effect.
* **Within sites, treatment** — F-test on per-plot temporal SD: not significant
  at four of five sites (p = 0.42, 0.09, 0.52, 0.57); Echo alone reaches
  p = 0.031, which is what one expects from five tests.
* **Rotation phase (wheat vs fallow)** — a genuine within-plot, time-varying
  driver, and the cleanest test here. Residual SD in wheat against fallow:
  Echo 8.12 / 8.24%, Moro 5.37 / 5.24%, Ritzville 9.91 / 10.36%. **Three sites,
  three near-identical pairs.** Whether a plot is carrying a crop or lying
  fallow does not measurably change how much its carbon measurement moves.

**So the second of D-040's two open possibilities is now closed, negatively.**
The conditioning signal for a spatially explicit MDC surface is not in temporal
variance either. Possibility (i) — that MDC varies spatially through the
**signal** rather than the noise — is now the only one of the two still
standing, and Phase 3 Deliverable 3 should be reconsidered on that basis.

Same caveat structure as D-040, and it must travel: four sites, all dryland silt
loams in a semi-arid Mediterranean climate (D-042's quoted use limitation). This
is a demonstration that the covariates *available here* do not condition
temporal variance. It is not a demonstration that none ever could.

---

**D-046 — the Wuest series independently corroborate the G1 between-plot
baseline, which nothing else in the table has done.**

`VC-BPS-005/006` are derived from NAPESHM, which measures **one sample per
experimental unit**. Under D-027 that makes the G1 rows between-plot **plus**
within-plot **plus** analytical, combined — an upper bound. The matching
quantity here is `v_plot + v_resid`: one core, in one plot, on one date.

| series | AW | CP | Moro | Echo | Ritz |
|--------|----|----|------|------|------|
| plot + residual CV | 5.29% | 7.60% | 7.03% | 9.62% | **11.32%** |

`VC-BPS-006` (stock, NAPESHM, 0–15 cm) is **11.46%**. Ritzville — the largest
series, 24 plots, single core, ESM stock — lands at **11.32%**.

Read carefully, because the agreement is easy to over-claim. Different continent,
different depth, different crop, and the five series span 5.3–11.3% rather than
clustering on 11.5. The claim is only this: **an independent dataset, derived
independently, produces a like-for-like between-plot number in the same range,
with its top end sitting on ours.** That is the first external check the G1
headline has had. No row changes on the strength of it, and G3 stays open.

---

**D-047 — KBS LTER is retained as corroboration but the corroboration points the
OTHER WAY, and it cannot carry a row without a licence step.**

The purpose of a second source was to test the standing objection that Pacific
Northwest dryland is unrepresentative — that dryland moisture swings inflate
temporal variance relative to humid temperate cropland. KBS LTER table 102
(southwest Michigan, humid temperate row-crop, 0–25 cm, **142 experimental units
over six occasions, 1996–2000**) is open, primary, and about as different a
regime as North America offers.

Decomposed identically: between-plot **10.99%**, occasion **7.71%**, residual
**13.75%**, combined **15.80%**.

**Larger than every Wuest series, not smaller.** So the objection is not
supported in the direction it is usually raised: on this comparison PNW dryland
is the **low** end of temporal variability, and using it would understate the
term for humid cropland rather than overstate it.

**Two reasons this is corroboration and not a row.**

1. **The between-year term is contaminated.** Field-wide occasion means swing
   **22.6%** across five years. Soil carbon at 0–25 cm cannot move that much
   that fast; that is method or laboratory drift between annual campaigns, not
   temporal variability. The only clean window is **within** a year: 2000-05-03
   to 2000-06-27, eight weeks, 140 EUs, mean shift +4.86%, SD of the paired
   difference **17.85%**, implying **12.62%** per visit. Still above Wuest, and
   still the same direction.
2. **The core relocation protocol inside a plot is not documented**, so the
   paired difference carries within-plot spatial error twice and is an upper
   bound of unknown tightness. The quantity is also a **concentration**, not a
   stock, so it is never compared with Wuest on an absolute scale — only as a CV.

**Licence, and it is a real constraint on the paper, not a formality.** The KBS
file states: *"These Data are copyrighted and use in a publication requires
written permission as detailed in our Terms of use."* The Wuest data are U.S.
Public Domain and carry no such condition. **Written permission must be obtained
before any KBS-derived number appears in a publication.** Until it is, KBS may
inform our reading and may not be published as a value. Neither raw file is
committed in any case — `data/raw/` is gitignored and `--fetch` re-downloads
both.

Martin & Sprunger 2022 (Front. Soil Sci. 2:917885), the paper that pointed at
KBS, is **not** the source of these numbers: its data statement is "available
from the authors", i.e. not deposited, so there was nothing to derive from. It
is recorded in `docs/sources.md` as the pointer it was.

**The two sources are reported side by side and are NOT merged into one row.**
Different climate, different quantity, different cadence, different licence.

---

**D-048 — the NEON temporal path is RETIRED. Superseded by primary data that is
better on every axis that mattered.**

`scripts/neon_temporal_variance.py` is kept, with its docstring caveats intact,
so the path stays documented and nobody re-derives the same dead end. It is no
longer a route to closing the temporal component.

Why it was never going to be enough, stated once and for the record:

* **Access** — needs a token and therefore a fresh session; it has blocked twice.
* **Support** — 4 agricultural sites and 42 site-years.
* **Cadence** — between-bout, not monthly. The month-to-month term is precisely
  what we needed and precisely what NEON does not resolve.
* **Confounding, the decisive one** — NEON randomises core position within the
  plot between bouts. Its "temporal" difference therefore contains the full
  within-plot spatial variance, making it an upper bound on temporal variance
  rather than an estimate of it.

Wuest beats it on all four: public domain and already downloaded, 2195
plot-months at 76 plots, genuinely monthly, and sampling **within 30 cm or a few
metres of the previous month's location** at fixed plots rather than
re-randomising. That last point is a matter of degree rather than of kind —
Wuest's residual is itself dominated by within-plot spatial variance (D-043), so
the same confound exists, just an order of magnitude smaller in offset and,
crucially, **bounded from two directions** by the separable occasion term. NEON
offered no such bound.

If NEON is ever wanted for something else — between-bout variance at scale,
say — the script is there and the caveats are in it.

---

**D-049 — a superseded row is KEPT, not deleted. The schema gains
`superseded_by` to say so in data rather than in prose.**

`VC-TMP-001/002` were variance *shares* read off a paywalled abstract with an
assumed sampling depth. They are now replaced by rows derived from the primary
data behind that same paper. The tempting move is to delete them, leaving the
table showing only good numbers.

We keep them, and the reason is not sentiment. The table's central claim about
itself is the **verification ladder** (D-017): every number declares how deeply
it was checked, and `baseline` status requires primary evidence. A reader can
only trust that ladder if they can see something climb it. `VC-TMP-001`
entering at `verified_abstract`, sitting flagged for two months as the weakest
load-bearing row in the table, and being replaced by `derived_primary_data` from
the same study — *with the two agreeing* — is the strongest evidence the ladder
works that this project will ever produce. Deleting the rung we climbed from
would throw that away to make the table look tidier.

New optional column, `superseded_by`: row id(s) that replace this row, comma
separated. It records a replacement; it does not itself change a row's role.
A superseded row keeps its `use_as`, so whatever already excluded it from the
OSSE still does.

Note the second supersession is not like the first. `VC-TMP-002` was never a
temporal quantity at all — it reports variance between replicate experimental
units, which is component 3, and it sat in the temporal block only because it
was printed beside the temporal figure. It is superseded by `VC-BPS-007` … `011`,
not by the temporal rows. Filing an abstract's numbers where the abstract put
them, rather than where they belong, is its own small lesson.

**What breaks if wrong.** If superseded rows were deleted instead, the table
would silently lose the record of its own corrections, and D-050's comparison —
the single most valuable check in Phase 0 — would have nothing to point at.

---

**D-050 — PIPELINE VALIDATION: our derivation reproduces Wuest & Durfee's
published temporal statistic, and the G1 code path reproduces an independently
written implementation. One published figure does NOT reproduce, and that is
recorded rather than smoothed over.**

This is the highest-value check available in Phase 0, and it was free: we hold
the raw data behind a published summary statistic, so we can derive the
statistic ourselves and compare.

**Part 1 — the temporal share reproduces, robustly.** Published: month-to-month
variance 15–32% of total random error, mean ~20%. Rather than fit one model and
declare victory, four pre-declared specifications were run, differing in which
plot-level fixed effects are absorbed:

| specification | temporal share | between-EU share |
|---------------|----------------|------------------|
| A — treatment only *(as shipped)* | **18.3%** (14.4–28.3) | 22.9% (9.4–40.8) |
| B — treatment + block *(RCB)* | **not estimable** | not estimable |
| C — block only | 18.4% (13.9–26.6) | 13.6% (5.1–28.0) |
| D — no fixed effects | 19.5% (15.8–28.8) | 25.1% (12.1–39.6) |
| **published (Wuest abstract)** | **20.0%** (15–32) | **17.0%** (2–42) |

The temporal share lands at 18.3–19.5% against a published 20%, with a range
overlapping the published one, **under every specification that can be fitted**.
That is reproduction, not a lucky model choice.

*Why specification B cannot be fitted, recorded because it looks like a bug and
is not:* in a randomized complete block design with one plot per treatment-block
cell, treatment and block **jointly identify the plot**. Absorbing both leaves
zero degrees of freedom for a plot term. Block is therefore not separable from
the plot effect in this design, and specification A — absorbing treatment, so
the plot term means "between replicate experimental units" — is the one that
matches the published quantity's own wording.

**Part 2 — the between-EU share only partly reproduces. This is a finding.**
Published 17%, range 2–42%. We recover the **upper end almost exactly** (40.8%
against 42%) and the mean loosely (22.9% against 17%), but **nothing we fit
reaches the published 2% floor** — our lowest is 9.4%, and the lowest across all
specifications is 5.1%. A near-zero variance component at one site would explain
it, and moment and REML estimators can both return zero at a boundary, but we
cannot confirm that without the full text, which is paywalled.

Recorded honestly: **the conclusion the paper is cited for reproduces; a
secondary number in the same abstract does not fully reproduce, and we do not
know why.** It does not touch the temporal result, and `VC-TMP-002` carries the
discrepancy in its own notes so it travels with the number rather than living
only here.

**Part 3 — the G1 code path is cross-validated against an independent
implementation.** This is the part that actually bears on NAPESHM.

`derive_g1_napeshm.py:residual_var` is nested REML on a cross-section — one
measurement per experimental unit, treatment nested in site. `derive_temporal.py`
is crossed plot × occasion moments on a panel. Different structure, different
code, written weeks apart. A Wuest series with occasion playing the role of site
is a NAPESHM-shaped input, and the G1 residual then estimates exactly
`v_plot + v_resid` from the crossed model:

| series | G1 code path | crossed model | difference |
|--------|--------------|---------------|------------|
| Adams-tillage | 4.83% | 5.29% | −0.46 |
| Adams-residue | 6.88% | 7.60% | −0.72 |
| Echo | 9.14% | 9.62% | −0.48 |
| Moro | 6.76% | 7.03% | −0.28 |
| Ritzville | 11.18% | 11.32% | −0.14 |

**Mean absolute difference 0.42 CV points.** The differences are all the same
sign, and small — consistent with the REML-versus-moments gap already documented
in D-041, where REML also sat slightly low. Two independently written estimators
agreeing to within half a CV point on five datasets is a genuine check on the
implementation behind `VC-BPS-005/006`.

**What this validates, and what it does NOT — stated precisely, because the
temptation is to claim more.**

*Validated:* the log-scale variance decomposition, the
`CV = 100*sqrt(exp(sigma^2)-1)` convention (D-029), the REML fitting, the
handling of a raw CSV into variance components, and — via Part 3 — the specific
G1 code path that produced the between-plot baseline.

*Not validated, and no amount of agreement here could validate it:* the NAPESHM
**filter cascade**. D-024 (which designs count), D-025 (which EU types count),
D-026 (the depth scope) and D-028 (the climate scope) are decisions about *which
rows to keep*, not about arithmetic. A perfectly correct estimator applied to a
wrongly chosen subset returns a wrongly scoped number, and this comparison would
not notice. The cluster bootstrap **over sites** is also untested here, because
the Wuest bootstrap resamples occasions instead.

So: the estimator is corroborated, the scope decisions still rest on their own
arguments — which is what D-040's leave-out tests were for.

**What breaks if wrong.** If Part 1 were wrong, our decomposition would be
measuring something other than what the source measured, and every derived
temporal row would be mislabelled. If Part 3 were wrong, the G1 baseline would
be an artefact of one implementation. Both are checkable by re-running
`scripts/derive_temporal.py` against the public-domain data, which is why the
comparison is in the repository rather than only in prose.

---

**D-051 — FINDING: variance components are reported ADJACENTLY in the literature
and get conflated by whoever reads them next. The schema now makes each row
state its axis of variation, and a test refuses rows filed against it.**

**The failure this is built from.** `VC-TMP-002` sat in the `temporal` component
across several PRs while reporting variance between replicate experimental
units. It was correctly transcribed, correctly cited, correctly harmonised, and
filed under the wrong component — **because the number appeared beside the
temporal figure in its source.** Misclassification by proximity.

**Every existing guard missed it, and each was right to.** R6 asks whether a
locator has been verified; this one had. D-032 asks whether an open decision
governs a live constant; none did. The staleness test compares YAML with CSV;
they agreed. None of them asks *is this number the kind of thing its component
says it is* — and no amount of care in the existing checks would have got there,
because the row was internally consistent. It surfaced only when D-049 forced a
supersession target to be named and the quantity had to be stated plainly enough
for the mismatch to become visible.

**Why this is a finding and not just a schema change.** The conflation did not
originate with us. Wuest & Durfee print a temporal variance share and a
between-experimental-unit variance share side by side, as any careful paper
would — they are comparing them, and the comparison is the result. The error
enters **downstream**, when someone lifts one number into a budget. We are that
downstream reader, we made exactly that error, and we made it while actively
trying not to.

That generalises. A soil-carbon meta-analysis assembling error terms from
published papers is doing precisely what we did, at scale, usually without a
line-level provenance trail to catch it. **The claim for the paper: adjacency in
a source is a systematic source of component conflation in downstream error
budgets, and the defence is not care — it is requiring every number to state its
axis of variation independently of where it is filed.** It belongs beside D-039
(provenance-dependent reusability) and D-040 (invariance across covariates) as a
finding about why a table like this has to exist at all.

**The mechanism.** Each component in `schema.py` carries a `definition` — what
varies, what is held fixed — and the phrases naming its **axis of variation**.
Each row carries `quantity_definition`, required. The axis is whatever follows
*between* / *across* / *among*; the earliest marker after each trigger resolves
that clause to a component. Structural, not semantic, and deliberately so — the
brief was not to build a classifier but to make a mismatch impossible to miss.

Three ways to fail, all loud: the axis disagrees with the filed component; no
readable axis is named at all; or **one definition names axes for two different
components**, which means the figure pools them and measures neither.

**The allowlist has teeth, because an allowlist without them is a silencer.**
`KNOWN_CROSS_COMPONENT` records genuine mismatches with a reason — and
`test_a_cross_component_row_is_never_load_bearing` forbids any row in it from
being a `baseline`. A misfiled row may be kept for contrast; it may never drive
a number. Re-filing it is the only way to promote it.

**Backfilling all 41 rows found three more, not one.** This is the result, not a
setback:

| row | filed under | reads as | why |
|-----|-------------|----------|-----|
| `VC-TMP-002` | `temporal` | `between_plot_spatial` | the original failure |
| `VC-BPS-001` | `between_plot_spatial` | **pooled** with `within_plot_spatial` | its own harmonization_note already said "this figure is NOT a pure between-plot term" — in prose, which does not fail CI |
| `VC-BPS-003` | `between_plot_spatial` | `within_plot_spatial` (also pooled) | it is a RATIO between two components; its numerator is the within-plot term |
| `VC-BPS-004` | `between_plot_spatial` | `temporal` | it is an **MDC** — an output of a whole variance structure plus a design, alpha and power. Not a variance component at all |

**None of the four is load-bearing** — `VC-TMP-002` is `sensitivity_high` and
superseded, the other three are `out_of_scope_reference`. So no published number
moves. That is the reassuring half. The unreassuring half is that three of them
had sat undetected since the table was built, and one of them was confessing in
its own prose the whole time.

**`VC-BPS-004` is the sharpest case.** An MDC is what this project *produces*.
Filing one as an input variance component is a category error one step worse
than filing a number under the wrong axis, and it is the kind of thing that,
left alone, ends up inside a variance budget as though it were a variance.

**What breaks if wrong.** If the axis reader is too permissive, a future misfiled
row passes and the guard provides false assurance — mitigated by pinning the
reader's behaviour on eight declared examples plus a regression test built from
`VC-TMP-002`'s real definition. If it is too strict, authors contort prose to get
past it, which is worse than no guard at all; that is why markers are resolved in
a short window after each trigger rather than anywhere in the sentence — the
first draft flagged "between sampling points within one plot, for plots of
1–400 m²" as spanning two components, when "plots" there was describing plot
size.

---

**D-036 UPDATE — TRACED TO BOTH PRIMARY SOURCES. The 4x discrepancy is
LARGELY RESOLVED: it collapses to ~1.2x once like is compared with like. The
residual is not between the two studies at all — it is INTERNAL to Potash et al.
D-036 STAYS OPEN, because closing it requires a judgement that is the PI's.**

Both sources are now held. Potash et al. 2025 is **Environmental Research
Letters**, doi:10.1088/1748-9326/ada16c, **open access** — it was never
paywalled, only unlocated. Poeplau et al. 2022 was already in
`data/literature/`.

**What Potash actually says, verbatim:** *"The SOC changes are not observed
directly but with error due to relocation (σ_r) since we cannot sample the same
core twice (Poeplau et al 2022, Lark 2009), as well as lab error (σ_l). Note
that our choice of σ_l = 2 Mg ha⁻¹ corresponds to a relative error of 4% in SOC
concentration and 2% in bulk density for 0–30 cm samples with average SOC
concentration 2% and bulk density 1.5 g cm⁻³."* Table 1 lists it as **"Lab
measurement SD (Mg ha⁻¹) 2"**, alongside **"Relocation SD (Mg ha⁻¹) 5"**.

**THE FINDING THAT DOES THE WORK — Poeplau reports TWO laboratory errors, and
we put the narrower one in the table.** From their Results, verbatim: *"The
average laboratory errors of SOC content caused by subsampling the same sieved
sample and the analytical MAPE were 2.5 and 1.2% across all sites, depth
increments and land uses."*

* **analytical error** — *"averaging the deviations between the two technical
  replicates of each original milled sample"*. The innermost step only: one
  milled sample, measured twice.
* **subsampling error** — *"a second aliquot was taken from each of the sieved
  P1 samples before milling, milled again and analysed"*. This re-mills and
  re-analyses, so it **contains** the analytical step and adds within-sample
  heterogeneity.

`VC-ANA-001` carries the analytical error alone. Potash's `σ_l` is a whole-lab
pathway error — their parameter table notes that compositing more cores per
assay *increases* lab error in the estimate, which only makes sense if `σ_l` is
a per-assay error covering everything from composite to reported stock,
**including bulk density**, which they say explicitly.

**Like for like:**

| comparison | ours | Potash | ratio |
|---|---|---|---|
| as the table stands (analytical only, no BD) vs their concentration term | 1.25% | 4% | **3.2x** |
| Poeplau's *subsampling-inclusive* lab error vs their concentration term | 3.13% | 4% | **1.28x** |
| the same, plus their 2% bulk-density term, on a stock basis | 3.72% | 4.47% | **1.20x** |

MAPE→SD uses the same normality conversion as D-003 (×1.2533).

**So: units, depth and bulk density explain very little; the WHOLE of the gap is
explained by which of Poeplau's two lab errors we picked.** That is a result
about our own table, not about a disagreement in the literature.

**The residual is inside Potash, not between the papers.** At their own stated
reference soil — 0–30 cm, 2% SOC, BD 1.5 g cm⁻³ — the stock is **90 Mg C/ha**.
Their stated 4% concentration and 2% bulk-density errors combine in quadrature
to 4.47%, which is **4.02 Mg C/ha** — not the 2 Mg C/ha they adopt. Their
`σ_l = 2` is **2.22%** of that stock. Their own sentence therefore does not
reconcile with their own parameter, by a factor of two, in the conservative
direction (they use the smaller value).

Two readings, and we cannot choose between them from the text: either `σ_l = 2`
is right and the "4% and 2%" sentence is loose, or the sentence is right and
`σ_l` should be ~4. **It matters**, because in their formulation lab error
enters the budget twice — baseline and remeasurement — and does not scale with
the monitoring interval, so it dominates at short intervals, which is exactly
where projects want to claim early detection.

**A smaller thing found on the way, about our own row.** `VC-ANA-001`'s
`harmonization_note` cites *"about 1%"* from Poeplau's Discussion (*"we found
the analytical error to be a negligible source of uncertainty (≈1%)"*) and
converts to SD 1.25%. The Results section gives the same quantity as **1.2%
MAPE**, which converts to **1.50%**. We took the rounded Discussion figure over
the precise Results figure. Small, but it is the more authoritative number and
the row should use it.

**WHY THIS STAYS OPEN.** What remains is not a fact to look up but a choice
about what `analytical` should mean in this table:

* **Recommendation (mine): add a second analytical row carrying Poeplau's
  subsampling-inclusive lab error (2.5% MAPE → 3.13% SD, concentration basis)
  and make it the baseline**, demoting `VC-ANA-001` to a sensitivity row that
  records the instrument-only floor. Reason: every other component in this table
  is scoped to what a monitoring programme actually incurs, and no programme
  ever re-measures the same milled aliquot — it subsamples a composite. The
  narrow figure understates the error a real design faces, and understating
  analytical error is anti-conservative for the Phase 5 audit (D-023).
* **Against it:** `VC-ANA-001` is the only row in the table measuring the
  instrument in isolation, and D-027's logic — prefer the decomposed term where
  one exists — cuts the other way.

Either way `VC-ANA-002` (Saby, 2.5% concentration, `verified_secondary`) turns
out to sit almost exactly on Poeplau's subsampling-inclusive figure, which is
mild corroboration that ~2.5–3% is the right order for a whole-pathway lab error
on concentration.

**No row is changed by this entry.** Adding or re-roling an analytical row is
the judgement above, and it is the PI's.

**What breaks if wrong.** If the two Poeplau errors are not nested as read —
if the subsampling comparison somehow excluded the analytical step — then 2.5%
and 1.2% would combine rather than subsume, giving 2.77% MAPE and a slightly
larger figure; the conclusion is unchanged. If Potash's `σ_l = 2` is the
intended value and the "4%" sentence is the loose one, then our subsampling-
inclusive figure (3.13% concentration, 2.82 Mg C/ha at their reference soil)
**exceeds** theirs, and the disagreement reverses sign rather than closing.

---

**D-052 — every row declares a BASIS. Axis and basis are orthogonal, and a
basis mismatch is dimensionally silent.**

D-051 gave every row an **axis** — what varies. It does not say what the number
is expressed **on**, and units cannot: a 1% CV of SOC *concentration* and a 1%
CV of SOC *stock* are dimensionally identical and semantically different.
Summing them yields a number, not an error — no type error, no unit error, just
a wrong answer that looks fine. D-036 is the live instance: a 1.25%
concentration error and a 4%-with-bulk-density stock error, argued about for two
rounds as though they were the same quantity.

The table already knew. **D-020 says "a concentration CV is never treated as a
stock CV".** It said so in prose. This is the enforceable version — the same
move D-032 made for open decisions and D-051 made for components.

New required enum `basis`: `concentration`, `stock`, `stock_change`,
`variance_share`, `proportion`, `distance`. `tests/test_basis.py` checks it
against each row's units and — the part with teeth — requires that **all
baseline dispersion rows within one component share a basis**, since those are
the summable ones. Structural rows are exempt by design: a `bias_pct` like
`VC-REL-003` (a 50% error reduction) or a `range` like `VC-REL-004` (a
saturation distance) modifies a budget rather than entering one.

**Backfilling all 41 rows found one live mismatch, and it is a baseline
collision.** `VC-BPS-005` is a **concentration** CV; `VC-BPS-006` and
`VC-BPS-007…011` are **stock** CVs. All seven are baselines, all are `cv_pct` in
`pct`, and nothing distinguished them mechanically. It is recorded in
`MIXED_BASIS_BY_DESIGN` rather than resolved, because both are wanted —
concentration is what the laboratory measures and is free of bulk-density error;
stock is what a carbon claim is denominated in — and choosing one is the PI's
call. Note D-040 already showed the two are not interchangeable even
approximately: on a common sample the stock CV runs **below** the concentration
CV, 11.456% against 11.897%.

**The exemption is a record, not permission to sum across.** The OSSE must pick
one basis per run and say which.

**What breaks if wrong.** If the basis vocabulary is too coarse — if `stock` is
hiding a fixed-depth versus equivalent-soil-mass distinction that matters — then
two rows could share a basis and still not be summable. That distinction is
currently carried by `depth_basis`, and the two fields should be read together;
if that proves insufficient, `basis` is where the split belongs.
**D-053 — G3 BOUNDED, NOT CLOSED. "Add cores before adding plots" is unproven
and probably too strong, and it cannot be settled while D-036 is open.**

Recorded as a computation, not a judgement: `scripts/g3_bounding.py`,
`data/processed/g3_bounding.json`, written up in `docs/g3_bounding.md`. No row
is written and no design choice is made.

The Wuest residual exceeds the pure between-plot term at all five series, which
reads as "the variance is inside the plots". But the residual is within-plot
spatial **plus** analytical **plus** plot x occasion interaction, and only the
first is reducible by taking more cores. Writing `f` for the non-reducible
share, coring wins while `(1 - f) * v_resid > v_plot`:

| series | `f*` |
|---|---|
| Adams-tillage | 0.307 |
| Adams-residue | **0.089** |
| Echo | 0.862 |
| Moro | 0.587 |
| Ritzville | **0.874** |

**"Add cores" holds at ALL FIVE only if `f` < 0.089. It fails at all five only
if `f` > 0.874.** The brief expected the flip to be hard because it must happen
at five sites independently — true, but the useful finding is the other
direction: holding the conclusion *everywhere* needs `f` below 9%, and that is
the constraint likely to fail.

**It probably does fail, and D-036 decides by how much.** Analytical error alone
— before any interaction term — is 1.4–9.5% of the residual under the
instrument-only candidate and **8.7–59.3%** under the subsampling-inclusive one.
At Adams-tillage the wider candidate consumes 59% of the residual by itself.
**G3 cannot be closed while D-036 is open**, and that coupling only became
visible once both were traced to primary sources.

**A quantitative disagreement with the nearest prior art.** Under Potash et al.'s
own price list (location $15, assay $20) the budget-optimal compositing is
`C* = sqrt((20/15) * v_w / (v_plot + v_nr))` — budget and field-visit cost both
cancel. Our variance structure gives **C\* = 1.2 to 3.3 at `f` = 0**, falling to
**about 1 at `f` = 0.3**. **Potash use 4.** Justifying 4 needs
`v_w / (v_plot + v_nr) = 12`; our `v_resid / v_plot`, an upper bound on it, is
1.1 to 8.0.

Held loosely for three reasons, each of which would need settling first: our
plots are 3.6–9 m experimental units on uniform fields against their 25 ha
commercial fields; their dominant within-field term is relocation (5 Mg/ha vs
lab 2 Mg/ha), not the same construct as our within-plot term; and `f` is
unidentified. Note the first reason widens the disagreement rather than closing
it — a larger between-location term at their scale implies a *smaller* `C*`,
not a larger one.

**What would settle it:** replicate cores per plot per visit, analysed
separately. One site, one season, three or more cores per plot per month. No
source we hold does this, and it is the experiment G3 actually wants.

**Recommendation, not acted on.** Retire the flat claim. The defensible version
is narrower: *a single core per plot is likely the wrong design, but the optimum
is nearer 1–3 cores per assay than the 4 used by the closest published work, and
it cannot be pinned down until D-036 closes and `f` is measured.*

**What breaks if wrong.** If relocation error does average down with compositing
in Potash's formulation — we did not verify this in their SI — then their
effective `v_w` is much larger than ours and `C* = 4` may be right for their
scale while ours stays right for a research plot, and the "disagreement" is
really a scale difference. That check is the first thing to do before this
becomes a claim in a paper.


**D-036 — CLOSED 2026-08-12 by correspondence with the author. The residual was
a typographical error in the printed reference soil. Confirmed intended values
reconcile Potash et al.'s sentence with their own Table 1 to within rounding,
and nothing is left to resolve between the two studies.**

Eric Potash (University of Illinois), corresponding author of Potash et al.
2025, was asked directly about the inconsistency the previous entry recorded.
His answer: **the reference soil as printed is a typo.** The intended values are
**1.5% SOC and 1.0 g cm⁻³**, not the 2% and 1.5 g cm⁻³ in the published
sentence.

**The arithmetic closes exactly.** At 0–30 cm,

| | as printed (typo) | as intended |
|---|---|---|
| reference soil | 2% SOC, BD 1.5 | **1.5% SOC, BD 1.0** |
| stock | 90 Mg C/ha | **45 Mg C/ha** |
| 4% concentration ⊕ 2% bulk density | 4.4721% | 4.4721% |
| implied `σ_l` | 4.025 Mg/ha | **2.0125 Mg/ha** |
| Table 1 states | 2 | **2** |
| agreement | off by **2.01×** | off by **0.6%** — i.e. rounding |

So the 2× the previous entry found was real arithmetic on a mis-set number, and
its cause is now known. **Their sentence and their parameter agree.**

**One reading in the previous entry is WITHDRAWN.** It recorded the discrepancy
as sitting "in the conservative direction (they use the smaller value)". There
was never a smaller value. `σ_l = 2` is precisely what their stated relative
errors imply on the soil they meant, and their lab error is **4.47% of stock**,
not the 2.22% that the printed soil made it look like.

**The like-for-like comparison is unchanged and now unqualified.** It never
depended on the reference stock, because it compares *relative* errors:

| comparison | ours | Potash | ratio |
|---|---|---|---|
| Poeplau subsampling-inclusive lab error vs their concentration term | 3.13% | 4% | 1.28× |
| the same, plus their 2% bulk-density term, on a stock basis | 3.72% | 4.47% | **1.20×** |

**D-036 as posed — "our analytical error and theirs differ by 4×, resolve by
tracing both to primary sources" — is answered.** The gap is 1.20×, all of it
attributable to which of Poeplau's two laboratory errors our table picked, and
the apparent internal contradiction in the nearer source is a typesetting
error. There is no disagreement in the literature to adjudicate.

**A CONSEQUENCE THAT REACHES BEYOND `σ_l`, AND IT IS THE MORE USEFUL HALF.**
Every other parameter in Potash's Table 1 is given in **absolute Mg C/ha only**.
Expressing any of them as a relative error requires the reference stock — and
that stock is **45 Mg/ha, not 90**. Every relative expression of their
parameters therefore **doubles**:

| symbol | value | quantity | % of 90 (wrong) | **% of 45 (right)** |
|---|---|---|---|---|
| `σ_n` | 5 Mg/ha | relocation SD | 5.56% | **11.11%** |
| `σ_l` | 2 Mg/ha | lab SD | 2.22% | **4.44%** |
| `σ_w` | 1 Mg/ha/y | within-field SD of *rate* | 1.11%/y | **2.22%/y** |
| `σ_b` | 0.5 Mg/ha/y | between-field SD of *rate* | 0.56%/y | **1.11%/y** |
| `τ` | 0.3 Mg/ha/y | treatment effect | 0.33%/y | **0.67%/y** |

**This changes the direction of one of our comparisons with them.** `VC-REL-001`
carries a relocation MAE of 5.1 Mg C/ha → SD 6.39 on a *difference* scale
(CV 9.4%), or 4.52 Mg/ha per observation (CV 6.65%) under the √2 caveat the row
itself states. Against the printed reference stock their `σ_n` read 5.56% — just
below our per-observation figure, i.e. rough parity. Against the corrected one
it reads **11.11%, about 1.7× ours**. Their relocation term is the larger, not
the smaller. Logged as a candidate cross-check under D-037; **not merged**, and
no row changes.

**Nothing in the live table used the 90 Mg/ha figure** — checked across
`data/variance_components.yaml`, `src/`, `scripts/` and `tests/`. It appeared
only in the D-036 update's prose and in `HANDOFF.md`, both of which now carry a
pointer here. **G3's arithmetic is unaffected**: `scripts/g3_bounding.py`
compares *ratios* of Potash's parameters, and a common reference stock cancels.

**WHAT THIS DOES NOT CLOSE.** The previous entry gave two reasons for staying
open. This settles the first. The second — *which* laboratory error the
`analytical` component should carry — is a choice about our own table, not a
fact about theirs, and it is carried forward unchanged as **D-054**. G3's gate
moves with it: `G3 cannot close while D-054 is open` now replaces the reference
to D-036.

**What breaks if wrong.** The correspondence is private and there is no
published erratum. Anyone reading Table 1 against the printed sentence will
reach the same 2× we did, so any writeup that leans on their parameters must
state the corrected reference soil explicitly and attribute it — a footnote, not
a silent substitution. If the published sentence is ever the one that is right
and the correspondence misremembered, `σ_l` should be ~4 Mg/ha rather than 2 and
their lab term doubles again; the like-for-like 1.20× is untouched either way,
because it uses their relative errors and not their stock.

**Locator.** E. Potash (University of Illinois), personal communication to the
PI, **2026-08-11, 13:35 UTC** — third of three exchanged messages, the reply
confirming the reference-soil typo. Date supplied by the PI 2026-08-12.

---

**D-054 — OPEN. Which laboratory error should the `analytical` component carry:
the instrument-only floor, or the whole-lab-pathway error?** ⚠️ *Unresolved —
carried forward from D-036, which closed on a different question.*

D-036 was posed as a discrepancy with the literature and it is answered as one.
This is the part of it that was never about the literature, separated out rather
than allowed to lapse when its parent closed. Recording it as its own decision
is the point: an open question that disappears because the entry containing it
was closed is exactly the failure mode D-032 exists to make impossible.

**The question.** Poeplau et al. 2022 report **two** nested laboratory errors:

* **analytical**, 1.2% MAPE — two technical replicates of the *same milled
  sample*. The innermost step only.
* **subsampling**, 2.5% MAPE — a second aliquot of the same *sieved* sample,
  re-milled and re-analysed. Contains the analytical step and adds within-sample
  heterogeneity.

`VC-ANA-001` carries the first (converted to SD 1.25%). Potash's `σ_l` is a
whole-pathway per-assay error covering everything from composite to reported
stock, bulk density included.

**Recommendation, unchanged from the D-036 update, and still the PI's call:**
add a second analytical row carrying the subsampling-inclusive error
(2.5% MAPE → **3.13% SD**, concentration basis) and make it the baseline,
demoting `VC-ANA-001` to a sensitivity row recording the instrument-only floor.
No monitoring programme re-measures the same milled aliquot; it subsamples a
composite. Understating analytical error is anti-conservative for the Phase 5
audit (D-023).
**Against:** `VC-ANA-001` is the only row in the table isolating the instrument,
and D-027's logic — prefer the decomposed term where one exists — cuts the other
way.

**A smaller correction bundled in, so it is not lost either.** `VC-ANA-001`'s
`harmonization_note` quotes *"about 1%"* from Poeplau's **Discussion** and
converts to SD 1.25%. The **Results** give the same quantity as **1.2% MAPE**,
which converts to **1.50%**. We took the rounded figure over the precise one.
Fix it in whichever PR settles this.

**What this gates.** G3 (D-053): 'add cores before adding plots' holds at all
five Wuest series only if the non-reducible share of the residual is below
0.089, and analytical error alone is **1.4–9.5%** of the residual under the
instrument-only candidate but **8.7–59.3%** under the subsampling-inclusive one.
The two candidates land on opposite sides of the threshold, so **G3 cannot close
while this is open.**

**Why no constant is registered against it.** The exposure is through a row's
prose, not through a derivation script, so `rows_exposed_to_open_decisions` will
now catch `VC-ANA-001` if and only if the row cites D-054. It does not yet, and
citing it means editing a row — which is what this decision is *about*, and
therefore out of scope for a log-only entry. **This is the same hole D-036
recorded and did not close.** It is recorded again rather than quietly dropped,
and it is a second piece of evidence that the guard's two routes do not cover
every way a row can depend on an open question.


**D-055 — FINDING: inorganic carbon is NOT the conditioning covariate for
between-plot variability. D-040's invariance result survives a fourth
independent attempt — but the test has a detection limit of about 7% analytical
error, and Potash's stated range starts at 1%, so the null is bounded and the
bound is part of the finding.** Prompted by author correspondence (2026-08-11);
script `scripts/ic_conditioning.py`, results `data/processed/ic_conditioning.json`,
written up in `docs/ic_conditioning.md`. **No variance-table row written — the
brief said report first, and this is the report.**

**The hypothesis, in the author's words:** *"soils with high inorganic carbon
have higher variability in their organic carbon measurements. I wouldn't be
surprised if the total variability can vary as low as 1% or as high as 10%."*
The mechanism is analytical: NAPESHM reports `b_soc` as `b_total_c - b_ic`, so
organic carbon is measured **by difference** and the subtracted term carries its
own error. This was a live and specific candidate answer to D-040's invariance
problem, and it is directly testable in data we already hold.

**WHAT THE RESPONSE ACTUALLY IS, because the temptation is to overclaim.** The
same quantity as `VC-BPS-005`: within-treatment, within-site residual CV among
replicate EUs, which per D-027 bundles between-plot spatial + within-plot
spatial + analytical with no way to separate them. **The mechanism is
analytical; the measurement is not.** Nothing here may be described as an
analytical-error result.

**1a — the distribution, reported before anything was fitted.** 1453 EUs,
`b_ic` reported for **all** of them. **1192 (82.0%) are exactly zero**; 261
(18.0%) positive, median of positives 0.31%, max 3.16%. 25 of 93 sites carry any
carbonate; 68 are entirely zero. `b_soc == b_total_c - b_ic` holds to 1e-6 on
1449 of 1450 — an identity, which is what licenses the paired test below.
**Inorganic carbon is a site property**: 97.9-99.8% of its variance is between
sites, so the honest unit is the site and the effective sample size is the
number of carbonate sites — 25 before filters, as few as 6 after.

**THE HEADLINE TIER CANNOT RUN THE TEST, AND THAT IS THE FIRST RESULT.** Under
D-024 + D-025 + D-028 — the exact cascade behind `VC-BPS-005/006` — 27 of 135
treatments carry any carbonate, **25 of them Mexican**, the other two at trace
levels (0.022%, 0.014%). **Every treatment above 0.05% has exactly two
replicates.** Inorganic carbon is aliased with country, and country is aliased
with replicate support.

**That is D-040 check 1c coming true.** It recorded the country/support alias as
a caution for future analyses. This is the first analysis it bites, and it bites
completely: three variables mutually aliased, which no estimator repairs. Two of
four carbonate strata are **not estimable at all** (2 and 6 treatments across 2
sites each); the one that is sits at 14.384% against the zero-carbonate 11.575%,
with a **95% interval 11.7 points wide** that contains the reference.

**WHERE THE TEST IS IDENTIFIABLE, THE ANSWER IS FLAT.** Dropping D-024 admits 22
more carbonate treatments with 3+ replicates (all USA). This is **not** the
`VC-BPS-005/006` quantity and must never be compared with it. On it:

| stratum (treatment-mean IC) | T2 [95% CI] | T3 [95% CI] | T4 [95% CI] |
|---|---|---|---|
| zero | 14.303% [12.62, 15.54] | 11.627% [10.06, 13.55] | 14.553% [12.89, 15.59] |
| 0–0.1% | 13.280% [9.71, 16.78] | not estimable | 17.267% [11.60, 22.97] |
| 0.1–0.5% | 14.894% [5.84, 16.59] | **6.820%** [6.16, 7.31] | 18.286% [11.63, 25.94] |
| > 0.5% | 14.131% [6.04, 17.66] | 13.997% [5.49, 18.80] | **13.293%** [5.64, 16.97] |

**Eight of the nine estimable carbonate intervals contain their own tier's
zero-carbonate estimate.** The single exception runs the **wrong way for the
hypothesis**: T3's 0.1–0.5% bin sits at 6.82% with an interval of [6.16, 7.31],
entirely *below* its 11.63% reference. And the ordering is **not monotone in any
tier** — in T4 the highest CV is in the **middle** carbonate bin and the lowest
is in the **top** one, also below the reference.

A dose-response that runs down as often as up is not a dose-response.

**The regression agrees, and shows the confound working.** Debiased
log-variance per treatment (`E[log s^2] = log sigma^2 + psi(nu/2) - log(nu/2)`,
weighted by `1/psi'(nu/2)`), site-clustered SEs. **Not one specification in the
headline tier is significant**; Spearman rho = +0.079, p = 0.37 over 135
treatments. Two readings worth keeping:

* **Conditioning on climate shrinks the headline coefficient by 72%**, +0.227 to
  +0.064 — and this must NOT be reported as the confound seen from the inside.
  The shrinkage does not replicate: in T2 and T4 climate conditioning *raises*
  it (+0.345 → +0.452, +0.236 → +0.335). One tier of four, on a coefficient
  never distinguishable from zero, is not evidence of confounding any more than
  the raw coefficient was evidence of an effect. **What the conditioning tests
  DO establish is that the confound is structurally unresolvable here**:
  inorganic carbon, aridity, pH and country are collinear at site level, and the
  headline tier contains FOUR carbonate sites (nine in the widest). Conditioning
  on climate with four carbonate sites cannot separate a carbonate effect from an
  aridity effect even in principle. **There is no effect to adjudicate, and this
  design could never have adjudicated one.**
* **Conditioning on pH collapses it in every tier.** Inorganic carbon and pH
  correlate at **rho = +0.692** across 93 sites; they are two measurements of one
  soil-chemical axis and cannot both carry a mechanism.

**A methodological result about our own past specification.** D-040's joint
model — unweighted OLS on log(SD), 3+ replicates only — returns t = -0.37,
**+4.58** and +0.75 across three nested tiers, **changing sign twice**. The
debiased, weighted version of the same contrast is flat in all of them. The one
"significant" carbonate result in this entire analysis comes from that
specification, in one tier. **When a specification flips sign across nested
samples while its debiased counterpart does not, the specification is talking,
not the soil.** D-040's substantive conclusion is unaffected — it was a null,
and a noisy estimator makes a null harder to reach, not easier — but the
estimator should not be reused as it stands.

**THE PAIRED SUBTRACTION TEST — the sharpest instrument available, with a
built-in null control.** For each treatment, across the same replicate EUs,
`Delta = log Var(log b_soc) - log Var(log b_total_c)`. Degrees of freedom are
identical, so the `E[log s^2]` bias **cancels exactly**; and every zero-carbonate
treatment has `b_soc` identical to `b_total_c`, so `Delta == 0` **by
construction**. **The null control passes exactly in all four tiers** — max
|Delta| = 0.0 across 108, 255, 124 and 323 treatments.

Being a within-treatment paired contrast, it is immune to every site-level
confound: climate, parent material, country, management, laboratory.

Median variance ratio SOC:total-C is **1.02-1.11** — a 1-5% inflation in CV.
Spearman(IC, Delta) at **treatment** level is significant in the three narrower
tiers (+0.29 to +0.43, p = 0.027-0.044) and **not** in the widest one (+0.110,
p = 0.33). At **site** level — the honest unit, since carbonate is a site
property — it is positive in every tier and **significant in none** (p = 0.20 to
0.65, n = 6 to 19 sites). Per-site ratios run from **0.092 to 14.77**, scattered
either side of 1. The single site that looks like the mechanism, `MXOA01`
(IC 2.94%, ratio 14.8), consists of two-replicate treatments — one degree of
freedom per variance.

**Site level (1c) points the other way.** The df-weighted CV is 0.4-3.1 points
higher for carbonate sites in every tier, but the **rank correlation is negative
in every tier** (-0.101 to -0.215) and the one-sided test for "high exceeds low"
returns p = 0.56 to 0.95. The binned difference is about which sites land in a
bin of 4-9, not about carbonate content.

**THE CONFOUND, MEASURED.** Site-level Spearman against mean inorganic carbon,
n = 93: pH **+0.692** (p < 1e-10), clay +0.359 (0.0004), Hargreaves moisture
deficit +0.337 (0.0009), Thornthwaite MI **-0.311** (0.0024), MAP -0.289
(0.0050), MAT +0.096 (ns), **SOC concentration -0.030 (ns)**. Carbonate soils
here are drier, higher-pH and finer-textured; Mexican sites carry **15x** the
mean inorganic carbon of USA sites. So the aridity confound the brief named is
real and measurable — and it is not a temperature effect and not an SOC-level
effect. (`mi` and `hargreave_cmd` are used **only** as aridity covariates; D-033
forbids treating either as an IPCC MAP:PET ratio and nothing here does.)

**WHAT THIS COULD HAVE DETECTED — the project's own logic, turned inward.** A
null is only informative against a stated detection limit, and detectability is
what this project claims to measure. Under D-027 the reference CV is
`sqrt(spatial^2 + analytical^2)`; an analytical term `a` replacing the
`a0 = 3.13%` already inside it gives `sqrt(cv0^2 + a^2 - a0^2)`. The smallest
`a` clearing the upper end of the reference interval:

| tier | reference CV | 95% CI | minimum detectable analytical error |
|---|---|---|---|
| T1 headline | 11.575% | [9.66, 13.45] | **7.54%** |
| T2 | 14.303% | [12.62, 15.54] | **6.83%** |
| T3 | 11.627% | [10.06, 13.55] | **7.62%** |
| T4 widest | 14.553% | [12.89, 15.59] | **6.41%** |

**Potash's range is 1-10%. This design could only ever have detected the top
third of it**, in every tier. The finding is therefore stated with its limit
attached:

> Between-plot CV in NAPESHM cropland is not detectably higher in
> carbonate-bearing soils, **at a detection limit of about 7% analytical error**.
> An inflation in the lower two-thirds of the range the author named would not
> have shown up, and this test does not rule it out.

Two contrasts show that the surviving "effects" are noise. In the headline tier
the implied added error in the one estimable carbonate stratum is **8.54%** —
inside Potash's range and above the limit, and resting entirely on 4 Mexican
sites of 2-replicate treatments with an interval 11.7 points wide. And in the
widest tier the implied added errors are **mutually incoherent**: **9.29%** for
the 0–0.1% bin, **11.07%** for the 0.1–0.5% bin, and **none at all** for the
> 0.5% bin, which is *less* variable than zero-carbonate. **No mechanism driven
by carbonate content can produce that ordering.** These are what a detection
limit looks like when strata are estimated on almost no information.

**CONSEQUENCE FOR PHASE 3.** D-040 left two possibilities open. The one this
tested — that the conditioning signal sits in the analytical term rather than
the spatial one — is **not supported**, subject to the limit above. Both of
D-040's original possibilities stay open: MDC may vary spatially through the
**signal**, or the conditioning may live somewhere none of our data can see.
Deliverable 3 still needs rethinking and this does not rescue it.

**WHAT WOULD SETTLE IT.** A dataset with (a) replicate EUs under identical
management, (b) 3+ replicates, (c) carbonate spanning 0 to >2%, and (d) that
variation occurring **within** climate zone and **within** country. NAPESHM has
(a) and (c) and fails (b) and (d) exactly where it matters. Lab duplicates on
carbonate soils would be better still — they would test the analytical mechanism
directly instead of through a bundled between-plot residual.

**FRAMING, and it cuts the friendly way (D-038).** Potash et al. held `sigma_l`
fixed and soil-independent in the published model, and the author's own view in
correspondence is that it should vary. We went looking for that variation in the
largest suitable open dataset and could not find it above a 7% limit. **That is
a second load-bearing simplification in the nearest prior art surviving an
independent test**, after `sigma_b` geography-independence (D-040). Any writeup
says it that way round.

**What breaks if wrong.** If the calcimeter error is proportional to carbonate
content with a small coefficient — say 5% of `b_ic` — then at the median
positive carbonate of 0.31% it contributes 0.016% absolute to a soil averaging
~1.5% SOC, i.e. about 1% relative, far below anything this design resolves. In
that case the mechanism is real, our test is simply blind to it at NAPESHM's
carbonate levels, and the place to look is soils above 2% inorganic carbon —
which NAPESHM has at exactly three sites, all Mexican, all 2-replicate. The
finding would then be about NAPESHM's coverage rather than about soils.


**D-056 — FINDING: the Phase 5 audit cannot be run on most registered soil
carbon projects, because the sampling designs are not published. The corpus is
started, the gap is quantified, and the gap is the more publishable half.**
Corpus `data/registry/projects.yaml`, written up in `docs/registry_corpus.md`,
schema guarded by `tests/test_registry_corpus.py`. Seven projects, three
registries, one complete registry census. No variance-table row is touched.

**Why this was started now.** Potash independently named the Phase 5 post-hoc
audit as the highest-impact direction available (correspondence, August 2026;
see `docs/sources.md`). It is data collection with a long lead time and no
upstream dependency, so it is the thing most likely to bottleneck month 5 if
left until month 5.

**THE CENSUS, which is the part that generalises.** The Australian ACCU Scheme
register is complete and machine-readable (3025 rows, as at 2026-06-30), so this
is a count and not an estimate:

* **999** registered soil carbon projects
* **53** have been issued credits; **439,348 ACCUs** issued in total
* `Estimation or measurement approach or model` populated for **24 of 999 (2%)**
* `Model start date(s)` **0/999**; `Supplementary project information` **0/999**
* **no field exists** for sample count, sampling depth, cores per composite,
  sampling density, depth convention or remeasurement interval — not blank
  fields, no fields — and the Regulator's own register page states that
  project-level sampling plans and measurement reports are not published

> **439,348 credits have been issued against soil carbon measurements whose
> sampling designs are not public, in any project, anywhere in that scheme.**

The scheme *requires* a sampling plan and regulates it in detail. It is simply
never published. So this is a disclosure choice, not regulatory laxity — which
matters, because it means one registry field would fix it.

**`withheld` IS A SEPARATE FINDING FROM `not_disclosed`, and the schema keeps
them apart.** Two projects name the document that holds their design and do not
publish it. CAR1513's monitoring plan says twice "See the CAR1513 V4 Soil
Sampling Memo"; that memo is not among the project's 41 public documents.
VCS 4022's validation report confirms in detail that PD Appendices 6 and 9 hold
the sampling design and were found complete, and does not reproduce them — its
monitored-parameter table even lists "N | Unitless | Number of cores", so the
parameter's existence is public and its value is not. **A validation report that
certifies a design without publishing it transfers the entire verification to
the validator**, which is defensible for a registry and fatal for independent
post-hoc audit.

**THE GAP THAT CHANGES A NUMBER RATHER THAN BLOCKING A CALCULATION: not one
project in the corpus states its depth convention.** CAR1459's 102-page
monitoring plan contains none of "equivalent soil mass", "soil mass", "depth
increment", "fixed depth", "0-10" or "10-30". That is the parameter our
component 6 says matters most — fixed depth understates stock change by 17%
(`VC-BDC-001`), conventions can reverse the sign (16.2%, `VC-BDC-002`), and von
Haden 2020 puts fixed-depth error at 2.1-23.2% against ESM's 0.2-1.1%. **A
Phase 5 audit that cannot read the convention has to run twice and report a
bracket** — a defensible output, and one a project that never stated its
convention has no standing to object to.

**A DIRECT HIT ON G3 FROM THE ONE AUDITABLE PROJECT.** CAR1459 (Indigo, CAR SEP
v1.1, 100,371 acres, 175 growers, 16 states) states: *"At each carbon sampling
location, an individual 30-cm sample was collected."* **Carbon samples are not
composited — one core per assay.** Compositing is used only for pH and texture.
D-053 bounded the budget-optimal composite from our variance structure at
**1.2-3.3 cores per assay against Potash et al.'s 4**, and held the
disagreement loosely for want of a third opinion. **The third opinion is C = 1,
at continental scale, from the most completely documented soil carbon project on
any registry.** It does not settle G3 — different objective, interpolated bulk
density, and one core per point at 1 point per 8 acres is not one core per
experimental plot — but it moves the disagreement from "ours versus theirs" to
"ours and the largest real deployment on one side, theirs on the other".

Two further numbers from CAR1459 that are hard to get anywhere else: **sampling
density 1 point per 8 acres (3.24 ha)**, and a bulk-density frequency raised
from 1-in-5 to 1-in-3 carbon points explicitly *"to increase the precision of
our estimates of SOC stock changes"* — a design change made on variance grounds
and documented as such, which is a natural validation target for the calculator.

**A CORRECTION TO THE BRIEF, recorded because it would otherwise propagate.**
The brief describes VM0042 as using "0.43 SE". What is verified here is the
**CAR SEP** rule, which is a different construct: `UNC = z(70%) x (half-width of
the 95% CI) / ER`, with z(70%) = 0.5244. VM0042's uncertainty rule was **not**
read from the methodology this session and is not recorded anywhere in the
corpus. The two must not be quoted alongside each other until it is.

**TWO ACCESS WALLS, DELIBERATELY NOT COUNTED AS DISCLOSURE GAPS.** Verra's
registry returned the single-page-application shell on every path tried (four
endpoints, two attempts); the one Verra project here came via a validation
report mirrored on a third-party site. **Verra PDDs are public in principle and
a browser would very likely open them** — the same access-wall-wearing-a-
paywall's-coat pattern that has now cost us four items. And the Climate Action
Reserve report paginates by CSRF-bound POST (302 on page 2, 411 on CSV export),
so only page 1 was enumerated and **no CAR-wide census exists in this file**.
Conflating "we could not fetch it" with "they did not publish it" would inflate
the finding, so the schema and the writeup keep them apart.

**THE CONSEQUENCE FOR PHASE 5, and it is a real one.** Phase 5 has a
**population problem before it has a method problem**. The readable population
is small and it is not a random subset — it is the projects whose developers
chose to publish, plausibly the ones with the most defensible designs. **Any
Phase 5 result will be biased toward finding that projects sample adequately**,
and that caveat travels with the finding from the start rather than being
discovered at the end.

**THE STRONGEST IDEA TO COME OUT OF THIS PASS, recorded and not acted on.**
Invert the question for the undisclosed majority. For a project that published
only its area, its practice and its credits, ask *what sampling design would
have been required for this claim to be detectable?* That needs **no design
disclosure at all** — only area, claimed rate and interval, which the ACCU
register does publish for all 999 projects. It turns the gap from a blocker into
the method, and it makes the 999 an asset rather than a dead end. **Scope it
before building the audit that needs designs.**

**What breaks if wrong.** If Verra's registry turns out to publish PDDs with
full sampling appendices — likely, and one browser session away — then the
readable population is much larger than this pass suggests and the bias caveat
weakens accordingly. The Australian census is unaffected either way: it is a
complete count of a register that has no such fields. If a Phase 5 audit is ever
published, **the corpus must be re-pulled and re-dated**, because registries
change and every source here carries an access date of 2026-08-12 for exactly
that reason.

**Tone, for the writeup.** Nothing here is a case against any project. CAR1459
discloses more than most published papers do and should be named for that, not
used as a foil. The finding is about what registries require to be published.

---


**D-057 — VM0042 RETRIEVED AND READ. The 0.43 figure is CORRECT and is now
verified against the primary source — the attribution was never wrong, only
unverified. Three things were wrong or missing around it, and one of them
reframes Phase 5 entirely: VM0042 contains the inverted audit's own equation and
explicitly declines to require it.**
Sources: VM0042 v2.2 (greenlined, October 2025), 183 pp., and the v2.0
final-draft-for-public-comment (December 2021), 173 pp. Both retrieved directly
from verra.org and held. Registered in `docs/sources.md`.

**WHAT THE PRIMARY SAYS, verbatim.** VM0042 v2.2 §8.6.4, Equation 74:

> `t0.667` = "t-value for a one-sided student's t-distribution at 0.667 (66.7%)
> confidence interval with degrees of freedom appropriate to the sampling design
> used. **Equal to approximately 0.4307 at large sample sizes** (dimensionless)"

and Figure 4's caption: the value used in calculating VCUs issued "is determined
by applying an uncertainty deduction based on the **33.3rd percentile** of the
estimated probability distribution". The method is probability-of-exceedance,
per VCS Methodology Requirements §2.4.

**So `z_deduct = 0.43` is real, it is VM0042's, and it is 0.4307.** The PI's
concern was that the figure had been attributed to VM0042 while sourced from
Potash et al. It had — but the attribution turns out to be right. `z(2/3)` =
0.4307 to four places, matching the methodology's stated value exactly. **No
misattribution decision is needed. What was missing was verification, and it is
now supplied.**

**CORRECTION 1 — it is a t-value, not a constant.** "Approximately 0.4307" is
the LARGE-SAMPLE LIMIT. At small degrees of freedom the one-sided t at 66.7% is
larger, so **a project with few samples takes a bigger percentage haircut for the
same relative standard error.** Recording `z_deduct = 0.43` as a constant loses
that, and it is not a detail: it couples the deduction to `n`, which is exactly
the variable the Phase 5 inverted audit solves for. The deduction is a function
of the design, not a fixed price.

**CORRECTION 2 — the version. 0.4307 CANNOT be attributed to v2.0 on the
evidence held, and v2.0 is the version this repo cites and the version our one
Verra corpus project used.** The v2.2 front matter says plainly that "Revisions
to the uncertainty section were prepared by Dan Kane and Jaclyn Kachelmeyer,
TerraCarbon LLC" — the uncertainty section is not original to v2.0. The document
labelled v2.0 is a tracked-changes redline carrying more than one layer of text,
and **neither layer contains 0.4307**:

* one layer (Equation 46) defines `UNC` as "the extent to which the half width of
  the 95% confidence interval, as a percentage of the mean, exceeds the threshold
  of **15%**" — a threshold rule, with no deduction at all below 15%;
* another layer offers **two pathways** — Pathway A, a relative-uncertainty
  threshold (15% for case N1, **0%** for case N3, so always a deduction), and
  Pathway B, probability of exceedance with **B = 55%** for case N1 and **70%**
  for case N3.

**Consequence for the corpus: `VCS 4022` (AgreenaCarbon) applied VM0042 v2.0, so
its 31.35% deduction was NOT computed under the 0.4307 rule** and must not be
described as a 0.43-SE deduction. Its row is corrected accordingly.

**CORRECTION 3 — TO MY OWN STATEMENT, and it is the more useful version.** I
recorded in D-056 that VM0042's rule and the CAR SEP rule are "a different
construct". That is wrong in form and right in effect. Both are the same
construct — deduct `k x` a relative dispersion — with different `k` and different
dispersion measures. Quantified:

| protocol | rule | multiplies | effective `k` in relative-SE units | credits at |
|---|---|---|---|---|
| **ACCU** (per VM0042's own note) | 60% probability of exceedance | SE | **0.253** | 40th pct |
| **Verra VM0042 v2.2** | `t0.667` = 0.4307 | relative SE | **0.431** | 33.3rd pct |
| **CAR SEP v1.1** | `z(70%)` = 0.5244 x **95% CI half-width** | 1.96 x SE | **1.028** | 15.2nd pct |

**CAR SEP is 2.38x more conservative than VM0042, and 4.06x more conservative
than the Australian rule, on identical measured variance.** That is a finding
worth a paragraph of its own in any Phase 5 writeup: *the same soil, the same
sampling design and the same variance produce a fourfold different uncertainty
haircut depending only on which registry the project is listed with.* It is also
the reason the two rules must never be quoted as though interchangeable. (CAR's
`s(ER_t)` is explicitly "Margin of error of the 95% confidence interval", i.e.
1.96 SE, not the SE — that factor is the whole of the difference.)

**AND THE FINDING THAT RESHAPES PHASE 5. VM0042 §8.2.1, item 11, verbatim:**

> "A power analysis **may** be conducted to calculate the number of samples
> needed to enable accounting of a minimum detectable difference, following
> Equations (1) and (2) (FAO, 2019). **However, projects are not required to take
> this number of samples.**"

with Equation (1) `MDD >= (S / sqrt(n)) x (t_alpha,v + t_beta,v)` and Equation
(2):

> `n >= ( S x (t_alpha + t_beta) / MDD )^2`

where `S` = "Standard deviation of the difference in SOC stocks between t0 and
t1", `t_alpha` two-sided at a significance level "frequently taken as 0.05", and
`t_beta` one-sided for type II error "(e.g., 90%)".

**Equation (2) IS the inverted audit.** The method the PI adopted this session —
*given the claim, solve for the sampling it would have required* — is not an
external standard we are imposing. It is **the methodology's own calculation,
written into the methodology, and made optional in the same sentence.**

That changes the posture of Phase 5 in three ways, all of them strengthening:

1. **It answers the registry's strongest objection before it is raised.** "You
   are asking the wrong question" fails when the question is Equation (2) of the
   protocol the project registered under.
2. **The only thing we supply is `S`.** VM0042 expects `S` from the project's own
   pre-sampling ("A pre-sampling of 5 to 10 soil samples per stratum may provide
   an estimate of SOC variance where up-to-date soil data are unavailable").
   Nobody publishes it. **Our variance table is exactly the missing input** — the
   same role D-038 identified for `sigma_b` against Potash et al., now at
   protocol level.
3. **"Projects are not required to take this number of samples" is quotable, and
   it is the audit's justification in the methodology's own words.**

**OTHER PRIMARY REQUIREMENTS NOW HELD** (v2.2; all previously inferred or
unknown in the corpus, now sourced):

* **Depth.** Minimum **30 cm** for reporting SOC stock changes; soils "must be
  sampled deeper than the minimum 30 cm" where extrapolation would otherwise be
  needed; "Where possible, soils should be sampled to 50 cm depth".
* **ESM is required, not optional.** "To enable the ESM approach, soil samples at
  re-sampling **must** be divided into at least two increments." Accepted tools
  are the Wendt & Hauser (2013) spreadsheet and **the von Haden et al. (2020) R
  script** — which is *our own component 6 corroborating source*. The methodology
  and our table are pointing at the same paper.
* **Remeasurement.** "SOC stocks must be directly remeasured **every five
  years**"; monitoring at least every five years.
* **Quantification Approach 2 is measure-and-remeasure, SOC only**, "relevant
  where models are unavailable or have not yet been validated or parameterized,
  or where project proponents prefer to use a direct measurement approach".
* **Stratified random sampling is required.** At least **three control sites**
  across the project area, "more will decrease uncertainty, particularly where
  the total number of control sites is less than ten", and **at least one control
  site per stratum**.
* **Laboratory.** Dry combustion (Dumas) preferred; NIR, Vis-NIR, MIR, LIBS and
  INS permitted under Appendix 4 criteria; ISO/IEC 17025 where possible; **all
  samples across the project lifetime in the same laboratory**.

**A DIRECT INPUT TO D-054, which stays open.** VM0042 requires the laboratory to
"quantify and report analytical error statistics (**determined by repeated
analyses of the same sample**)". That is Poeplau's *narrow* analytical error —
technical replicates of one milled sample — not the subsampling-inclusive one.
So the registry that governs the largest in-scope project in our corpus defines
the reportable analytical error exactly as `VC-ANA-001` currently carries it.
**This is evidence for the against-side of D-054**, which had rested only on
D-027's prefer-the-decomposed-term logic. It does not settle it: what a registry
asks a laboratory to report is not the error a monitoring programme incurs, and
D-054's question is which of those the table should represent. **Logged, not
acted on. D-054 remains open at the PI's instruction.**

**What breaks if wrong.** The 0.4307 verification is quotation from a held
primary document and is safe. The version claim is weaker: it rests on a redline
PDF that renders tracked changes, so the approved v2.0 text may differ from
either layer I can read. **If the approved v2.0 does contain 0.4307, correction 2
is withdrawn and VCS 4022's deduction can be read against it.** Obtaining the
approved v2.0 (not the public-comment draft) would settle it and is a small job.
The cross-protocol severity table depends on reading CAR's `s(ER_t)` as the 95%
CI half-width, which the CAR1459 monitoring plan states in two places; if it
were the standard error instead, CAR's `k` falls to 0.524 and the ratio to
VM0042 falls from 2.38x to 1.22x — still the same ordering, a smaller gap.

**Access note, contradicting last session's log.** The previous entry recorded
Verra's registry as machine-unreachable and flagged it as an access wall. That
holds for the **project registry** (`registry.verra.org`, an Angular SPA) but
**not** for the **methodology library** (`verra.org/wp-content/uploads/...`),
which served both PDFs on the first attempt. The two were conflated. Methodology
documents are directly retrievable; project design documents are not.

---

---

## Open evidence gaps

| id | gap | consequence | status |
|----|-----|-------------|--------|
| ~~**G1**~~ | ~~No in-scope **between-plot** cropland variance. Only forest (Buchkowski).~~ | — | ✅ **CLOSED** 2026-08-08 by `VC-BPS-005/006`, derived from NAPESHM (D-024…D-030). Scoped to 0-15 cm; upper bound. |
| **G2** | No 0–30 cm within-plot CV; only 0–10 and 10–30 separately, without inter-layer covariance. | Component 2 baseline is per-layer only. | open — needs Poeplau supplementary data |
| **G3** | The within-plot / between-plot **ratio** is unknown for cropland. | Determines whether to add plots or add cores. | open — **BOUNDED 2026-08-10 (D-053), not closed**. 'Add cores' holds at all five Wuest series only if the non-reducible share of the residual is below **9%**; analytical error alone is 1.4–9.5% or 8.7–59.3% depending on which candidate is right, so **G3 cannot close while D-054 is open** (the gate moved from D-036, which closed 2026-08-12 on a different question). Budget-optimal compositing from our numbers is **1.2–3.3 cores per assay against Potash's 4**. Settling it needs replicate cores per plot per visit — an experiment nobody we hold has run. |
| ~~**G4**~~ | ~~Only temporal source is dryland Pacific Northwest, paywalled, depth unconfirmed.~~ | — | ✅ **CLOSED** 2026-08-10 by `VC-TMP-003/005/007/009/011`, derived from the Wuest & Durfee public-domain dataset (D-041…D-044). The paywall was never the blocker: the data behind the paper was open. Depth is now fact, not assumption, and heterogeneous (D-042). **One region remains a real limitation** — see G8. |
| **G5** | No variance-versus-distance function for offsets of 10–100 m. | Relocation error at LUCAS scale is unquantified; components 3 and 5 not orthogonal there. | open |
| **G6** | The two LUCAS rows are unverified against the primary report. | Locked out of use by rule R6. | open — needs LUCAS PDF |
| **G7** | No source yet isolates cover-crop or reduced-till effects on *variance* (as opposed to mean). | Practice-specific variance inflation is unparameterized. | open |
| **G8** | Every temporal row comes from ONE region: four sites, all silt loam, all semi-arid Mediterranean, all Pacific Northwest dryland. | Component 4 is derived but not generalised. The provider says so themselves (D-042). | open — **narrowed in direction**: KBS LTER (humid temperate row-crop) is *more* variable, not less, so PNW dryland is the low end and using it understates rather than overstates (D-047). Blocked from becoming a row by a written-permission licence, confirmed to travel with the EDI mirror. |

---

## Log

| date | entries | note |
|------|---------|------|
| 2026-08-07 | D-001 … D-020, G1 … G7 | Phase 0 initial build. 24 rows, 6 components, 14 verified against full text. |
| 2026-08-08 | D-021 (open), D-022 | CI + CSV staleness guard. Re-prioritised `docs/sources.md`: Poeplau to top for G1, Buchkowski re-filed by role. No variance-table rows changed. |
| 2026-08-08 | D-023 … D-027, D-029, D-030; **D-028 open** | `bias_direction` added to the schema and backfilled across all 24 existing rows. **G1 CLOSED** by `VC-BPS-005/006`, derived from NAPESHM: between-plot CV 12.1% (concentration) and 11.1% (stock) at 0-15 cm, n=212 EUs / 61 treatments / 14 sites. 26 rows. Climate envelope left open for the PI. |
| 2026-08-09 | **D-028 CLOSED**; D-039 | **D-028 decided: partial IPCC classification.** Private envelope retired. 94 sites classified against Figure 3A.5.2 with frost days recovered from Daymet (validated 60/60 against NAPESHM's own published temperature integers): **7 classified** (6 Tropical Dry, 1 Tropical Montane), **87 unclassified**, all blocked on `map_pet_ratio`, never imputed. G1 re-scoped to the IPCC **temperature** regime (Temperate/Boreal), which is what Table 5.5 indexes on. **`VC-BPS-005/006` RE-DERIVED, not re-labelled**: concentration 12.1% → **11.9%** [9.9, 14.0], stock 11.1% → **11.5%** [9.6, 13.5]; n rises 212 → 386 EUs and 14 → 26 sites. The scope change re-admits 10 Mexican highland sites the latitude floor was built to exclude — recorded as a caveat on the rows, because the IPCC axis that might have separated them is the undetermined one. The D-032 guard now passes. D-039 logs the unclassified bucket as a finding about NAPESHM's reusability, for the paper. |
| 2026-08-09 | **corrections** to D-031 and D-033 | Adversarial re-audit of the committed work. **D-031 reason 1 withdrawn**: "shallower depth is more variable" is refuted by the very layer CVs it cited (9.3 → 10.2 → 25.8% *rise* with depth), so the corroboration rests on two reasons, not three. **D-033 frost half withdrawn**: frost-day counts *are* faithfully obtainable from Daymet — the source NAPESHM itself cites — verified by reproducing the published temperature integers 39/39; the 13 warm sites split 7 Tropical / 6 not, so the variable decides scope membership and is not harmless. **MAP:PET remains the sole blocker**, now bounded exactly: 35 sites Dry, 40 Moist, **19 undecidable** from `mi` (replacing an unfounded "23"). Added the decisive Table 5.5 argument — Ch 5 pools warm/cool and stratifies on moist/dry, so a partial classification is worthless. Fixed a NaN hole that let `ipcc_climate.classify` fabricate three leaves. Registered both IPCC chapters in `docs/sources.md`. No variance-table row changed. |
| 2026-08-09 | D-034, D-035, D-037, D-038; **D-036 open**; D-021 updated | IPCC classifier committed and tested but deliberately unfed (D-034) — D-028 still blocked, guard still red. Wuest's PNW sites classify **Cool Temperate Dry** (Warm Temperate Dry if MAT > 10), i.e. **temperate either way**, but D-021 stays open because the climate inputs were supplied rather than sourced. Potash et al. 2025 logged as prior art: schema needs `scales_with_interval` (D-035), a 4× analytical-error discrepancy is **open** (D-036), their parameters are candidate cross-checks never to be merged (D-037), positioning recorded (D-038). Six sources added to `docs/sources.md` as **to obtain**, including Smith 2004 and Saby et al. 2008 — the two foundational detectability papers, neither currently cited. No variance-table row, schema field or constant changed. |
| 2026-08-10 | D-041 … D-048; **D-021 CLOSED**; D-040 extended | **The temporal component is derived from primary data.** The Wuest & Durfee dataset behind the paywalled paper is **public domain on Ag Data Commons** — 2195 plot-months, 76 plots, five monthly series, four PNW dryland sites — so the abstract's variance *shares* are replaced by a derivation (D-041: crossed plot × occasion, REML cross-checked against closed-form moments; our shares 18.3%/22.8% reproduce the published 20%/17% without reading them off the paper). **The assumed 0–30 cm depth is wrong for four of five series** (D-042): those are 250 kg m⁻² equivalent-soil-mass stocks, ≈20 cm. The residual is not separable, so temporal is reported as a **bounded pair — separable 3.75% (3.02–4.85), combined 8.00% (5.25–11.73)** — and the compositing contrast (3-core vs 1-core sites, ratio 1.785 against √3 = 1.732) says the residual is dominated by within-plot spatial variance, so the truth sits near the **lower** bound (D-043). **FINDING: anniversary sampling buys nothing** — same-calendar-month revisits are no less variable than off-month ones at any site (D-044). **Temporal variance shows no consistent covariate dependence either** (D-045), which closes the second of D-040's two open possibilities, negatively. Wuest independently corroborates the G1 between-plot baseline: like-for-like `plot + residual` spans 5.3–11.3% against `VC-BPS-006`'s 11.46% (D-046). KBS LTER corroborates in the **opposite direction to the usual objection** — humid temperate is *more* variable than PNW dryland — but carries method drift between years and a **written-permission licence** (D-047). NEON path retired (D-048). **D-021 closed**: all four sites classify Temperate on sourced inputs. **No variance-table row written — reported first, as instructed.** |
| 2026-08-10 | D-040 extended | Two additions. **(a) Geographic confound recorded**: country and per-treatment support are completely aliased — all 55 two-replicate treatments are Mexican, no USA treatment is below three replicates — so no Mexico/USA difference may ever be read as a climate difference. **(b) The invariance finding elevated from hypothesis to a stated Phase 0 result**: between-plot CV in cropland SOC is approximately invariant across the covariates a spatial MDC surface would be built from (climate moves it 0.2–0.3 pts against a ~4-pt CI; clay shows no monotone signal; the joint model reaches R² = 0.093), with the 75/80-USA caveat attached. **Consequence: Phase 3 Deliverable 3 needs rethinking**, with two possibilities recorded and not resolved — MDC may vary spatially through the *signal*, or through *temporal* variance. Framing recorded: this **strengthens** Potash et al., who assumed `sigma_b` geography-independent "for lack of information" and turn out to have been approximately right. |
| 2026-08-10 | D-040 | **Three sensitivity checks before Phase 0 closes. No new rows, no scope change, no constant moved.** (1) Leave-out test on the re-admitted Mexican highland sites — 8, not 10 (MXAG01/MXQT02 fall to D-024/D-025 first): concentration 11.948 → 12.248%, stock 11.456 → 11.304%, shifts of **0.300** and **0.152** against CI widths of 3.97 and 3.52, in opposite directions. **Both caveat flags CLOSED**, not deferred. (1b) All **55** two-replicate treatments are Mexican; the USA's 75 have **none** below 3 replicates — so the weak-support flag and the re-admitted-sites flag were one flag, tested once. (2) On the 372-EU intersection, concentration **11.897%** vs stock **11.456%** — gap **+0.441** where the cross-sample headline gives 0.492, so the sample mismatch is 0.051 of it and `stock < concentration` **survives** as a property of the data. (3) Texture terciles show no signal (clay spread 2.611 vs 10.556 CI; sand 3.690 vs 9.834) — **no rows written**; a joint model does find `log(mean SOC)` and sand fraction nominally significant (R² = 0.093) but on a 75/80-USA sample, filed as a hypothesis, not a parameterization. `VC-BPS-005/006` prose updated; no value changed. |
| 2026-08-12 | **D-036 CLOSED**; D-054 (open), D-055 | **D-036 closed by author correspondence.** Eric Potash confirms the reference soil printed in Potash et al. 2025 is a **typo**: the intended values are 1.5% SOC and 1.0 g cm⁻³, i.e. **45 Mg C/ha** at 0–30 cm, not 90. Their stated 4% + 2% errors then imply **σ_l = 2.0125 Mg/ha** against Table 1's 2 — agreement to 0.6%, and the 2× the previous entry found is explained. The like-for-like gap with our table stands at **1.20×**, all of it attributable to which of Poeplau's two lab errors we tabled. **Consequence beyond σ_l:** every relative expression of their absolute parameters doubles — `σ_n` is **11.11%** of stock, not 5.56%, which moves their relocation term from rough parity with `VC-REL-001` to about **1.7× larger**. Nothing in the live table used 90 Mg/ha; G3's arithmetic is unaffected because it compares ratios. **The half of D-036 that was never about the literature — which lab error the `analytical` component should carry — is carried forward as D-054 (open) rather than allowed to lapse, and G3's gate moves with it.** **D-055: inorganic carbon is NOT the conditioning covariate** for between-plot variability, tested at Potash's own suggestion. `b_ic` is zero at **82.0%** of 1453 EUs and is a **site** property (97.9–99.8% of its variance is between sites). In the `VC-BPS-005/006` scope the test is **not identifiable** — every treatment above 0.05% IC is Mexican and 2-replicate, which is D-040 check 1c's alias biting for the first time. Where it is identifiable the answer is **flat and non-monotone**: all 11 carbonate intervals contain their tier's zero-carbonate estimate, no regression specification is significant in the headline tier, climate conditioning collapses the coefficient by **72%**, and pH (rho **+0.692** with IC) collapses it in every tier. A paired `Var(log SOC)` vs `Var(log total C)` contrast with an exact built-in null control (max |Δ| = 0.0 across 810 zero-carbonate treatments) gives a median inflation of only **2–11% in variance** and is **null at site level in every tier**. **Detection limit stated: ~6.4–7.6% analytical error**, against Potash's 1–10% — so the null covers only the top third of his range and is written that way. Also found: **D-040's own joint-model specification changes sign twice across nested samples** while its debiased counterpart stays flat; its conclusion is unaffected but the estimator should not be reused. **No variance-table row written — reported first, as instructed.** |
| 2026-08-12 | D-056 | **Phase 5 registry corpus started; the gap is the finding.** `data/registry/projects.yaml` (7 projects, 3 registries, schema-guarded by `tests/test_registry_corpus.py`) and `docs/registry_corpus.md`. **Census, not estimate:** the Australian ACCU register carries **999** soil carbon projects, **53** issued credits, **439,348 ACCUs** — and **no field of any kind** for sample count, depth, cores per composite, sampling density, depth convention or remeasurement interval; `Estimation or measurement approach or model` is populated for **24/999 (2%)**. The schema separates **`withheld`** (the public document names a document holding the parameter, and it is not public — CAR1513's Soil Sampling Memo, VCS 4022's PD Appendices 6 and 9) from **`not_disclosed`**, because those are different findings. **Not one project states its depth convention**, including the 102-page CAR1459 plan — the one undisclosed parameter our component 6 says changes the number (17% understatement, 16.2% sign reversal, von Haden's 2.1–23.2% vs ESM 0.2–1.1%). **G3 gets a third opinion:** CAR1459 collects **one core per assay**, uncomposited, at 1 point per 8 acres across 100,371 acres — against Potash's 4 and our D-053 optimum of 1.2–3.3. **Correction to the brief:** the 0.43-SE rule attributed to VM0042 is not what CAR SEP uses (z(70%) × 95% CI half-width ÷ ER); VM0042's own rule was not read and is not recorded. **Two access walls logged, not counted as disclosure gaps** — Verra's registry served only its SPA shell (4 endpoints, 2 attempts) and the CAR report paginates by CSRF-bound POST, so no CAR-wide census exists here. **Consequence: Phase 5 has a population problem before a method problem** — the readable projects are self-selected, so any audit is biased toward 'adequate'. Strongest idea, recorded not acted on: **invert the question** and ask what design the claim would have required, which needs no design disclosure and makes all 999 usable. No variance-table row touched. |
| 2026-08-12 | D-057; D-054 evidence (still open); D-036/D-055 dated | **VM0042 retrieved and read from primary — the 0.43 figure is CONFIRMED, not misattributed.** v2.2 §8.6.4 Eq. 74 gives `t0.667` "equal to approximately **0.4307** at large sample sizes", crediting at the **33.3rd percentile**; `z(2/3)` = 0.4307 to four places. It had been cited from Potash et al. rather than the methodology — unverified, not wrong. **Three amendments.** (1) It is a **t-value, not a constant**: 0.4307 is the large-sample limit, so a project with fewer samples takes a *larger* haircut — the deduction is a function of the design, which couples it to the inverted audit's unknown. (2) **The "v2.0" qualifier is withdrawn**: 0.4307 is absent from the v2.0 public-comment redline, which carries a 15%-threshold rule in one layer and a two-pathway rule (Pathway B at 55%/70% exceedance) in another. **VCS 4022 applied v2.0, so its 31.35% deduction must not be described as a 0.43-SE deduction.** (3) **Correction to my own D-056 claim** that VM0042 and CAR SEP are "different constructs": they are the same construct at different severity, and quantified it is a large difference — **ACCU 0.253 · VM0042 0.431 · CAR SEP 1.028** relative SE (CAR multiplies the 95% CI *half-width*, = 1.96 SE), i.e. **CAR SEP is 2.38× VM0042 and 4.06× the ACCU rule on identical measured variance.** The same soil, design and variance yield a fourfold different haircut depending only on the registry. **AND THE FINDING THAT RESHAPES PHASE 5:** VM0042 §8.2.1 item 11 Eq. (2) is `n ≥ (S(t_α+t_β)/MDD)²` — **the inverted audit's own equation** — followed by "**However, projects are not required to take this number of samples.**" The method is the methodology's own calculation, made optional in the same sentence, and the only input we supply is `S`, which VM0042 expects from project pre-sampling that nobody publishes. **Also recovered as primary** (all previously unknown or inferred): ESM is **required** (≥2 increments at re-sampling, ≥30 cm, **von Haden 2020's R script** an accepted tool — our own component-6 source), 5-yearly remeasurement, ≥3 control sites and ≥1 per stratum, stratified random sampling mandatory, and the laboratory analytical-error definition ("repeated analyses of the same sample" = Poeplau's narrow figure) which is **direct evidence for D-054's against-side and is logged there without closing it**. Recorded in a new `protocol_requirements` block in `data/registry/projects.yaml`, kept structurally separate from project records so a requirement can never masquerade as a disclosure. **Access-log correction:** last session flagged Verra as an access wall; that holds for `registry.verra.org` (SPA) but **not** for the `verra.org` methodology library, which served both PDFs first try. The two were conflated. |
| 2026-08-08 | D-031, D-032, D-033; **D-028 still open** | Open-decision guard: decisions and the constants they govern are now machine-readable (`src/loam/decisions.py`), the build prints `<-- PROPOSED, NOT DECIDED`, and two tests refuse to pass while an open decision governs a live constant — **the suite is red on merge, by design** (D-032). Replacing the private climate envelope with IPCC 2006 climate regions was attempted and is **blocked**: MAP:PET and frost-day counts are not derivable from NAPESHM, and no proxy is substituted (D-033). Poeplau ↔ NAPESHM corroboration logged, with a figure correction (D-031). No variance-table values changed. |
