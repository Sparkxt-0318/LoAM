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
| **D-021** | **open** | whether PNW dryland is in-scope temperate → `VC-TMP-001/002` |
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
| **D-036** | **open** | our analytical error vs Potash's differ 4× → `VC-ANA-001` |
| D-037 | decided | Potash parameters are candidate cross-checks, never merged |
| D-038 | decided | positioning vs Potash et al. 2025 in any writeup |
| D-039 | decided | **FINDING**: NAPESHM is not fully IPCC-classifiable — for the paper |
| D-040 | decided | G1 sensitivity: both `VC-BPS-005/006` caveat flags close; texture is not a stratifier |

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
   VM0042 v2.0.** Published, auditable, and thin — a single constant standing in
   for the entire uncertainty deduction. This is the specific number a Phase 5
   audit can test against, and the obvious place where a better variance model
   changes a real crediting outcome.

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

## Open evidence gaps

| id | gap | consequence | status |
|----|-----|-------------|--------|
| ~~**G1**~~ | ~~No in-scope **between-plot** cropland variance. Only forest (Buchkowski).~~ | — | ✅ **CLOSED** 2026-08-08 by `VC-BPS-005/006`, derived from NAPESHM (D-024…D-030). Scoped to 0-15 cm; upper bound. |
| **G2** | No 0–30 cm within-plot CV; only 0–10 and 10–30 separately, without inter-layer covariance. | Component 2 baseline is per-layer only. | open — needs Poeplau supplementary data |
| **G3** | The within-plot ÷ between-plot **ratio** is unknown for cropland. | Determines whether to add plots or add cores — the central design question. | open — **narrowed**: Poeplau's within-plot stock CV (9.3–10.2%, 0-10/10-30 cm) now sits just below the NAPESHM between-plot stock CV (11.1%, 0-15 cm), implying a ratio near 1 and echoing Buchkowski's forest finding. NOT closed — different studies, continents and depths, so this is suggestive only and no row claims it. |
| **G4** | Only temporal source is dryland Pacific Northwest, paywalled, depth unconfirmed. | Component 4 has no in-scope baseline. | open — needs Wuest PDF |
| **G5** | No variance-versus-distance function for offsets of 10–100 m. | Relocation error at LUCAS scale is unquantified; components 3 and 5 not orthogonal there. | open |
| **G6** | The two LUCAS rows are unverified against the primary report. | Locked out of use by rule R6. | open — needs LUCAS PDF |
| **G7** | No source yet isolates cover-crop or reduced-till effects on *variance* (as opposed to mean). | Practice-specific variance inflation is unparameterized. | open |

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
| 2026-08-10 | D-040 | **Three sensitivity checks before Phase 0 closes. No new rows, no scope change, no constant moved.** (1) Leave-out test on the re-admitted Mexican highland sites — 8, not 10 (MXAG01/MXQT02 fall to D-024/D-025 first): concentration 11.948 → 12.248%, stock 11.456 → 11.304%, shifts of **0.300** and **0.152** against CI widths of 3.97 and 3.52, in opposite directions. **Both caveat flags CLOSED**, not deferred. (1b) All **55** two-replicate treatments are Mexican; the USA's 75 have **none** below 3 replicates — so the weak-support flag and the re-admitted-sites flag were one flag, tested once. (2) On the 372-EU intersection, concentration **11.897%** vs stock **11.456%** — gap **+0.441** where the cross-sample headline gives 0.492, so the sample mismatch is 0.051 of it and `stock < concentration` **survives** as a property of the data. (3) Texture terciles show no signal (clay spread 2.611 vs 10.556 CI; sand 3.690 vs 9.834) — **no rows written**; a joint model does find `log(mean SOC)` and sand fraction nominally significant (R² = 0.093) but on a 75/80-USA sample, filed as a hypothesis, not a parameterization. `VC-BPS-005/006` prose updated; no value changed. |
| 2026-08-08 | D-031, D-032, D-033; **D-028 still open** | Open-decision guard: decisions and the constants they govern are now machine-readable (`src/loam/decisions.py`), the build prints `<-- PROPOSED, NOT DECIDED`, and two tests refuse to pass while an open decision governs a live constant — **the suite is red on merge, by design** (D-032). Replacing the private climate envelope with IPCC 2006 climate regions was attempted and is **blocked**: MAP:PET and frost-day counts are not derivable from NAPESHM, and no proxy is substituted (D-033). Poeplau ↔ NAPESHM corroboration logged, with a figure correction (D-031). No variance-table values changed. |
