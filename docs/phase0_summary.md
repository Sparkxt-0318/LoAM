# Phase 0 — closing summary

**Limits of Agricultural Monitoring (LoAM).** What Phase 0 set out to do was
assemble a defensible variance structure for minimum detectable change in
cropland soil organic carbon: six error components, each with a number, a
scope, a provenance, and an honest statement of what would break it.

**Status: closed.** Every one of the six components now carries at least one
baseline row resting on primary evidence. The test that pinned `temporal` as a
known gap has been emptied, which is the handshake that closure was meant to
require.

- **41 rows**, 22 of them baselines usable in the OSSE today
- **50 decisions** recorded, **1 open** (D-036)
- **17 rows derived by us from primary data**, up from zero at the start of the
  phase
- `117 passed`

---

## The six components

### 1. Analytical — *the weakest link, and the one open decision*

| | |
|---|---|
| Baseline | `VC-ANA-001` — **1.0%** (CV 1.25%) |
| Source | Poeplau et al. 2022, full text held |
| Rows | 4 (1 baseline, 3 sensitivity) |

**What constrains it:** a single European study, read in full. Sensitivity rows
bracket it well — 2.5% from Saby via Poeplau's discussion, a 5% air-drying
underestimation, and a 15 Mg C/ha grinding effect that is enormous but
procedural rather than typical.

**What is unresolved:** **D-036, the only open decision left.** Potash et al.
2025 — the nearest prior art — use `sigma_l = 2 Mg C/ha`, about **4%**, four
times our figure. A factor of four in the smallest component would still change
MDC conclusions, and we do not yet know whether the two numbers measure the same
thing (replicate determinations of one sample versus something wider). This is
the next PR.

### 2. Within-plot spatial

| | |
|---|---|
| Baselines | `VC-WPS-001` **9.3%** (0–10 cm), `VC-WPS-002` **10.2%** (10–30 cm) |
| Source | Poeplau et al. 2022 — 16 cores in 20 × 20 m plots |
| Rows | 4 (2 baseline) |

**What constrains it:** good direct measurement, but **per layer only**. There is
no 0–30 cm CV because the inter-layer covariance was never published, and D-008
forbids combining layer CVs without it. That is **G2**, still open.

**New this phase, and it is indirect but useful:** the Wuest series composite
three cores at two sites and one core at three others. Within-plot variance
enters the residual divided by the core count, and the observed residual ratio
between those groups (1.785) sits at √3 — implying a single-core within-plot CV
of roughly 8–9% at those sites. That is independent, from a different continent,
and lands on Poeplau's 9.3–10.2% (D-043).

### 3. Between-plot spatial — *the best-evidenced component, and now decomposed*

| | |
|---|---|
| Baselines | `VC-BPS-005` **11.9%** (concentration), `VC-BPS-006` **11.5%** (stock) |
| Source | NAPESHM — 386 / 372 experimental units, 26 sites |
| New | `VC-BPS-007…011` **3.3–5.2%** — Wuest, five series |
| Rows | 11 (7 baseline, 7 derived by us) |

**What constrains it:** NAPESHM is scoped to **0–15 cm** and never rescaled
(D-026), cover crops are nearly absent so it speaks to the tillage half of our
management scope only, and it is an **upper bound** — one sample per EU means
within-plot spatial and analytical error cannot be separated out (D-027).

**What is new:** the Wuest rows are the **first decomposed between-plot term in
the table**. Every other source measures each plot once; repeated visits are
what make the split possible. The like-for-like quantity — plot plus residual,
what a single visit to one plot would show — spans **5.3–11.3%** across the five
series, with Ritzville landing on NAPESHM's 11.5% almost exactly. **That is the
first external corroboration `VC-BPS-006` has had.**

### 4. Temporal — *closed this phase, from primary data*

| | |
|---|---|
| Baselines | `VC-TMP-003/005/007/009/011` — **3.0–4.9%**, mean **3.75%** (separable) |
| Sensitivity | `VC-TMP-004/006/008/010/012` — **5.3–11.7%**, mean **8.00%** (combined) |
| Source | Wuest & Durfee 2024 — **2195 plot-months**, 76 plots, 5 series, 4 sites |
| Rows | 12 (5 baseline, 10 derived by us, 2 superseded and kept) |

**What constrains it — and this is the honest headline: one region.** Four
sites, all silt loam, all semi-arid Mediterranean, all Pacific Northwest
dryland. The provider says so themselves, and we quote them on every row rather
than paraphrase. That is **G8**, newly opened.

**Why two numbers rather than one.** The field-wide occasion term is separable
from within-plot spatial and analytical error, because both average away across
12–24 plots measured on the same date. The plot × occasion residual is not
separable — one measurement per plot per occasion. So the component is a
**bounded pair**: 3.75% is a lower bound, 8.00% an upper bound with within-plot
spatial and analytical error inside it.

**The bounds are not symmetric, and the design says which end to believe.** The
compositing contrast (see component 2) shows the residual is *dominated* by
within-plot spatial variance, so the truth sits much nearer the lower bound.
The separable rows are additive-safe; the combined rows are explicitly marked
not additive-safe, because summing them alongside the within-plot and analytical
rows double counts.

**Design consequence (D-044):** anniversary sampling — resampling in the same
calendar month — **buys nothing**. Revisits 10–14 months apart are no less
variable when they fall in the same month than when they do not, at any of the
five series. There is no repeatable seasonal cycle to schedule around. The
temporal term must be carried, not designed away.

### 5. Relocation

| | |
|---|---|
| Baselines | `VC-REL-001` MAE **5.1 Mg C/ha** (CV 9.4%), `VC-REL-003` **50%** reduction from 3×3 resampling, `VC-REL-004` saturation at **7 m** |
| Source | Poeplau et al. 2022 |
| Rows | 6 (3 baseline, 2 locked out) |

**What constrains it:** the two LUCAS rows (`VC-REL-005/006`) are `unverified`
and locked out of the OSSE by rule R6, and have been for as long as they have
been unverified — the lock has held with no discipline required from anyone.
That is **G6**. There is also no variance-versus-distance function for offsets
of 10–100 m (**G5**), where relocation and between-plot error stop being
orthogonal.

### 6. Depth / bulk-density convention — *the best-constrained component*

| | |
|---|---|
| Baselines | all four: **17%** underestimation of stock change by fixed depth, **16.2%** sign reversal between conventions, **8%** and **6%** residual bias after splitting the profile |
| Source | Fowler et al. 2023, full text |
| Rows | 4 (4 baseline, all `verified_fulltext`) |

**What constrains it:** nothing outstanding. Four of four rows rest on full text
from a single well-matched study. This is the component that behaved.

---

## Four findings

### Finding 1 — temporal variance is still the least characterized error term, despite now being derived

It entered Phase 0 as a variance *share* read off a paywalled abstract with an
**assumed** sampling depth, flagged in its own notes as the weakest load-bearing
row in the table. It leaves Phase 0 derived from 2195 plot-months of
public-domain primary data.

**It is nonetheless still the least constrained of the six, for three reasons
that the upgrade did not touch:**

1. **One region.** Every row comes from PNW dryland silt loam. No other
   component rests on a single climate.
2. **It resolves to a bracket, not a number.** 3.75% to 8.00% is a factor of
   more than two, and closing it needs a design with replicate cores per plot
   per visit — which no source we have provides.
3. **The one caveat that cuts the other way.** Samples were "processed monthly
   by the same lab", so a per-month analytical batch effect is perfectly
   confounded with the occasion term. The separable number is simultaneously a
   lower bound on total temporal variance and an upper bound on its field-wide
   part.

The correct reading is that the component moved from *unusable* to *usable with
a stated bracket and a stated region* — real progress, not resolution.

### Finding 2 — NAPESHM's reusability is provenance-dependent (D-039)

**87 of 94 NAPESHM sites cannot be classified into an IPCC 2006 default climate
region**, and the reason is not difficulty — it is documentation. The
classification tree needs MAP:PET at every non-tropical leaf. NAPESHM publishes a
derived climate column without publishing the formula, window, or coefficient
behind it, so the ratio cannot be reconstructed and we refuse to invent it.

**The positive control is what makes this a finding rather than a complaint.**
Frost days, also absent from the CSVs, *were* recoverable — from the Daymet
endpoint NAPESHM's own dictionary cites, validated 60/60 exact against the
published integers. So the obstacle is specific and fixable: one paragraph in a
data dictionary would make 87 sites classifiable.

This belongs in the methods or discussion as a short subsection, not as a
limitations bullet — it is a reusability finding about a flagship open dataset,
and the fix is entirely within the provider's power.

### Finding 3 — one set of variance components serves temperate cropland (D-040, D-045, D-055, D-058)

> **UPDATED 2026-08-12. Deliverable 3 is RETIRED and this finding is now stated
> as a positive claim rather than as an obstacle.** Full treatment, with every
> detection limit attached, in [`docs/invariance_finding.md`](invariance_finding.md).

**The claim:** we searched for spatial structure in monitoring noise across
climate, texture and soil chemistry, each time against a stated detection limit,
and found none. **A single set of variance components serves temperate cropland.
MDC varies with DESIGN and INTERVAL, not with PLACE.**

Four independent conditioning attempts, all null:

| axis | result | detection limit |
|---|---|---|
| climate region (D-040) | shifts of **0.300** and **0.152** against CI widths of **3.97** and **3.52**, in *opposite* directions | ~±2 CV points |
| texture (D-040) | clay not monotone; spreads of **2.611** and **3.690** against widest-bin CIs of **11.016** and **10.464** | ~10 CV points |
| joint model (D-040, D-058) | weighted **R² = 0.0722** on 135 treatments / 26 sites | — |
| soil inorganic carbon (D-055) | 8 of 9 carbonate intervals contain their reference; the exception runs the *wrong way* | **~6.4–7.6%** analytical error, against Potash's stated 1–10% |

**And temporal variance behaves the same way** — no consistent dependence between
sites, within sites, by treatment, or by rotation phase (D-045).

**The joint model's R² is now 0.0722, not the 0.093 originally reported**, because
the estimator was repaired (D-058): D-040 used an unweighted OLS on `log(sd)`
restricted to n≥3, and `log s` is biased by an amount that depends on the degrees
of freedom. The covariates explain **less** under the correct estimator. That
repair was a test the null could have failed — excess noise inflates SEs and
depresses R², both of which favour a null — and it passed.

**The caveat changed shape with the repair.** D-040's caveat read "75 of 80
treatments from the USA"; the repaired fit is **75 USA / 60 Mexico**, so that
caveat no longer applies to it. It is replaced rather than removed: the
re-admitted Mexican treatments are exactly the 2-replicate ones (D-040 check 1c),
and `sand_frac` nearly doubles when they enter. **No Mexico/USA difference in this
table may be read as a climate or texture difference.**

**A repo-wide standard comes out of this: a null is only informative against a
stated detection limit.** Every null in this project carries the magnitude it
could have detected. A null without a limit is an absence of evidence passed off
as evidence of absence.

**Consequence: Deliverable 3 is retired, and Phase 5 is the headline.** Invariance
is what makes the inverted audit tractable — if σ varied by location, auditing
999 Australian projects would need a per-project variance estimate nobody can
supply. Because it does not, one component set audits the whole register.

**Framing for the writeup: this strengthens the nearest prior art.** Potash et
al. 2025 held `sigma_b` fixed and geography-independent *"for lack of
information"*, and held `sigma_l` soil-independent. We went looking for both, and
neither varies detectably. **Two load-bearing simplifications in the closest
published work surviving independent test** is a contribution, not a gap we
caught them in.


### Finding 4 — the derivation pipeline reproduces a published statistic, and the G1 code path reproduces an independent implementation (D-050)

We hold the raw data behind a published summary statistic, so we can derive that
statistic ourselves and compare. This was the highest-value check available in
Phase 0 and it cost nothing extra.

**The temporal share reproduces, robustly.** Four specifications were declared
before any of their answers were looked at:

| specification | temporal share | between-EU share |
|---|---|---|
| treatment only *(as shipped)* | **18.3%** (14.4–28.3) | 22.9% (9.4–40.8) |
| treatment + block | *not estimable* | *not estimable* |
| block only | 18.4% (13.9–26.6) | 13.6% (5.1–28.0) |
| no fixed effects | 19.5% (15.8–28.8) | 25.1% (12.1–39.6) |
| **published** | **20.0%** (15–32) | **17.0%** (2–42) |

18.3–19.5% against a published 20%, under **every** specification that can be
fitted. That is reproduction, not a lucky model choice.

**One published figure does NOT fully reproduce, and it is recorded rather than
smoothed over.** The between-EU share matches at the top (40.8% against 42%) and
loosely at the mean (22.9% against 17%), but nothing we fit reaches the published
**2%** floor — our lowest is 9.4%. We cannot say why without the full text. It
does not touch the temporal conclusion, and the discrepancy is carried on the
affected row so it travels with the number.

**The G1 code path is separately cross-validated.** `derive_g1_napeshm.py` is
nested REML on a cross-section; `derive_temporal.py` is crossed moments on a
panel — different structure, different code, written weeks apart. Run on the same
data they agree to a **mean absolute difference of 0.42 CV points** across five
series, all differences the same sign and consistent with the known
REML-versus-moments gap.

**What this validates, stated precisely, because the temptation is to claim
more.** It validates the estimator: the log-scale decomposition, the CV
convention, the REML fitting, and the specific code path behind
`VC-BPS-005/006`. It does **not** validate the NAPESHM **filter cascade** —
D-024, D-025, D-026 and D-028 are decisions about *which rows to keep*, and a
correct estimator on a wrongly chosen subset returns a wrongly scoped number
that this comparison would not notice. Those scope decisions rest on their own
arguments and on D-040's leave-out tests, not on this.

---

## What is open going into Phase 1

| | what | why it matters |
|---|---|---|
| **D-036** | Our analytical error and Potash et al.'s differ **4×** | The only open decision. Next PR. |
| **G2** | No 0–30 cm within-plot CV — inter-layer covariance unpublished | Component 2 is per-layer only |
| **G3** | Within ÷ between ratio — **substantially narrowed** | Wuest now gives both sides from the *same plots, same depth*: residual (4.1–10.7%) exceeds the pure between-plot term (3.3–5.2%) at **all five series**. Direction of the answer: **add cores before adding plots** |
| **G5** | No variance-versus-distance function for 10–100 m offsets | Components 3 and 5 are not orthogonal there |
| **G6** | LUCAS rows unverified, locked out by R6 | Needs the LUCAS 2015 report |
| **G7** | No source isolates cover-crop or reduced-till effects on *variance* | Practice-specific inflation unparameterized |
| **G8** | Every temporal row is one region | Narrowed in direction: humid temperate is *more* variable, so PNW dryland is the low end |
| — | KBS LTER written permission | Confirmed to travel with the EDI mirror; needed before any KBS number is published |
| — | External monthly PET climatology | Would classify the 87 unclassified NAPESHM sites and sharpen D-039 |

**Two things Phase 0 did not need in the end, worth remembering.** The Wuest
paper stayed paywalled and it did not matter — the dataset behind it was public
domain the whole time, and answered both the depth question and the scope
question the PDF was wanted for. And the NEON path, queued for two rounds, was
retired without ever running: it would have conflated temporal with relocation
by design. **Check for a deposited dataset before queueing a PDF, and check what
a source can actually separate before spending access on it.**
