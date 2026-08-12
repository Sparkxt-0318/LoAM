# Inorganic carbon as a conditioning covariate — result

**Question.** D-040 found between-plot CV in cropland SOC approximately
invariant across every covariate a spatially explicit MDC surface would be built
from. Eric Potash, in correspondence (August 2026), named a candidate the table
had never tested:

> "those 4% and 2% error numbers are representative but can vary quite a lot
> depending on the soil. For example, soils with high inorganic carbon have
> higher variability in their organic carbon measurements. I wouldn't be
> surprised if the total variability can vary as low as 1% or as high as 10%."

NAPESHM measures inorganic carbon directly (`b_ic`, Chittick calcimeter) and
reports `b_soc` as `b_total_c − b_ic`, so the mechanism is present in the data
by construction.

**Answer, in one line.** *Inorganic carbon is not the missing conditioning
signal for between-plot variability in NAPESHM — but the test could only have
detected the top third of the range Potash named, and inside the project's own
scope filters it could not have run at all.*

Script: `scripts/ic_conditioning.py` → `data/processed/ic_conditioning.json`.
Logged as **D-055**. **No variance-table row was written.**

---

## What is actually being measured

Not analytical error. The response is the same quantity as `VC-BPS-005`: the
within-treatment, within-site residual CV among replicate experimental units,
which per D-027 bundles

> between-plot spatial + within-plot spatial + analytical

with no way to separate them, because NAPESHM samples each experimental unit
once. Potash's mechanism is analytical — determining organic carbon *by
difference* is noisier when the subtracted term is large. **This test therefore
cannot isolate an analytical effect and does not claim to.** What it can do is
ask whether the bundled quantity rises with inorganic carbon, and — through the
paired contrast below — bound how much of any rise comes from the subtraction.

---

## 1a — the distribution, reported before anything was fitted

| | |
|---|---|
| experimental units | **1453**, `b_ic` reported for **all** of them, none missing |
| exactly zero | **1192 (82.0%)** |
| positive | **261 (18.0%)**, median of positives **0.31%**, max **3.16%** |
| sites | **93** total; **25** with any positive value; **68** entirely zero |
| `b_soc == b_total_c − b_ic` | exact to 1e-6 on **1449 of 1450** — an identity, not a description |

**Inorganic carbon is a site property, not a plot property.** Between-site
variance accounts for **97.9–99.8%** of its total variance depending on the
sample tier, and only 6–19 of 26–81 sites show any within-site spread at all.
That fixes the honest unit of analysis at the *site*, and it caps the effective
sample size at the number of carbonate-bearing sites — which is 25 before
filters and as few as 6 after them.

The carbonate mass is concentrated in a handful of places: `MXOA01` (2.94%),
`MXMO01` (2.66%), `MXPU01` (1.23%), `USTX05` (0.90%), `MXSL01` (0.57%),
`USID01` (0.50%). **Four of the top six are Mexican.**

---

## 1b — the answer depends on which filters you keep, and that is the finding

### In the scope the project actually uses, the test is not identifiable

Applying D-024 (randomized designs), D-025 (`Plots` only) and D-028 (IPCC
temperature regime) — the exact cascade behind `VC-BPS-005/006`:

* 27 of 135 treatments have any inorganic carbon; **25 of those 27 are Mexican**
* the 2 non-Mexican ones carry **trace** amounts (0.022% and 0.014%)
* **every treatment above 0.05% inorganic carbon has exactly 2 replicates**

So inorganic carbon is aliased with country, and country is aliased with
per-treatment replicate support — which is **exactly the confound D-040 check 1c
recorded in advance**:

> "all 55 two-replicate treatments are Mexican and no USA treatment has fewer
> than three replicates, so country and per-treatment support are completely
> aliased in this sample."

D-040 wrote that down as a caution about future analyses. This is the first
analysis it bites, and it bites completely: **IC, country and replicate count
are mutually aliased, and no estimator repairs that.**

| stratum (treatment-mean IC) | CV | 95% CI | n |
|---|---|---|---|
| zero | **11.575%** | [9.66, 13.45] | 330 EU / 108 trt / 22 sites |
| 0–0.1% | not estimable | — | 6 EU / 2 trt / 2 sites |
| 0.1–0.5% | not estimable | — | 12 EU / 6 trt / 2 sites |
| > 0.5% | **14.384%** | [6.18, **17.92**] | 38 EU / 19 trt / 4 sites, **all Mexican, all 2-replicate** |

The high-carbonate stratum sits 2.8 points above the reference and its interval
is **11.7 points wide** — it contains the reference estimate, and most of the
plausible range besides. Two of the four strata cannot be estimated at all.

### Where it *is* identifiable, between-plot CV is flat

Dropping D-024 admits 22 further carbonate treatments with 3+ replicates, all
from the USA. This is **not** the `VC-BPS-005/006` quantity and must never be
compared with it — the replicates are not randomized replicates. It is reported
because it is where the power is.

| stratum | T2 (D-024 dropped) | T3 (D-025 dropped) | T4 (both dropped) |
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

### The regression agrees, and shows the confound doing its work

Per-treatment log within-treatment variance, debiased for degrees of freedom
(so 2-replicate treatments contribute at their true information content rather
than being dropped), site-clustered standard errors. Coefficient on inorganic
carbon, in log-variance units per 1% IC:

| model | T1 headline | T2 | T4 |
|---|---|---|---|
| M2 linear dose | +0.176 (t=+0.50) | +0.130 (t=+0.56) | −0.018 (t=−0.07) |
| M4 + D-040 covariates | +0.227 (t=+0.80) | +0.345 (t=+1.25) | +0.236 (t=+0.86) |
| **M5 + climate (MI, MAT)** | **+0.064 (t=+0.26)** | +0.452 (t=+1.52) | +0.335 (t=+1.29) |
| **M6 + climate (MAP, MAT)** | **+0.069 (t=+0.28)** | +0.421 (t=+1.60) | +0.316 (t=+1.33) |
| M7 + country | +0.403 (t=+1.36) | +0.504 (t=**+2.08**) | +0.367 (t=+1.44) |
| M8 + pH | +0.140 (t=+0.63) | +0.112 (t=+0.41) | +0.152 (t=+0.54) |

**Not one specification in the headline tier is significant**, and Spearman's
rho over all 135 treatments is +0.079 (p = 0.37).

Two things are worth reading off this table rather than skipping past.

**Conditioning on climate collapses the coefficient in the headline tier** —
from +0.227 to +0.064, a **72% reduction**. That is what a confound looks like
from the inside: the raw association is mostly aridity, and once aridity is in
the model the carbonate term has almost nothing left to explain. In the wider
tiers climate conditioning does *not* shrink it, which is the honest
counter-observation and the reason this is stated as "consistent with" rather
than "demonstrates".

**Conditioning on pH also collapses it**, in every tier (t = +0.41 to +0.63).
Inorganic carbon and pH correlate at rho = **+0.692** across the 93 sites, so
these are two measurements of one soil-chemical axis and they cannot both be in
a story about mechanism.

**A methodological aside worth keeping.** D-040's own specification — unweighted
OLS on log(SD), restricted to 3+ replicates — returns t = −0.37, **+4.58** and
+0.75 across the three tiers, changing sign twice. The properly weighted version
of the same contrast is flat everywhere. When a specification flips sign across
nested samples while its debiased counterpart does not, that is the
specification talking, not the soil. **The one "significant" IC result in this
whole analysis comes from that specification, in one tier.**

---

## The paired subtraction test — the sharpest instrument here, and it is null at the honest unit

`b_soc = b_total_c − b_ic`. Total carbon is measured directly; organic carbon is
not. So for each treatment compare, across the *same* replicate units,

```
Δ = log Var(log b_soc) − log Var(log b_total_c)
```

Two properties make this the strongest test available:

* degrees of freedom are identical for both variances, so the `E[log s²]` bias
  cancels **exactly** — no correction needed;
* every zero-carbonate treatment has `b_soc ≡ b_total_c`, so `Δ ≡ 0` **by
  construction**. A built-in null control.

**The null control passes exactly in all four tiers** — max |Δ| = 0.0 across
108, 255, 124 and 323 zero-carbonate treatments. The estimator is doing what it
claims.

| tier | median Var(SOC)/Var(TC) | sign split | sign test | Spearman(IC, Δ), treatment | Spearman, **site** |
|---|---|---|---|---|---|
| T1 headline | 1.085 | 17↑ / 10↓ | p = 0.25 | +0.426 (p = **0.027**) | +0.371 (p = 0.47, n=6) |
| T2 | 1.105 | 31↑ / 17↓ | p = 0.059 | +0.292 (p = **0.044**) | +0.379 (p = 0.20, n=13) |
| T3 | 1.031 | 18↑ / 14↓ | p = 0.60 | +0.366 (p = **0.040**) | +0.190 (p = 0.65, n=8) |
| T4 widest | 1.022 | 43↑ / 36↓ | p = 0.58 | +0.110 (p = 0.33) | +0.193 (p = 0.43, n=19) |

**Read the last column, not the second-to-last.** Inorganic carbon is a site
property — 97.9–99.8% of its variance is between sites — so a treatment-level
p-value on 19 sites is pseudo-replicated. At the site level the correlation is
positive in every tier and **significant in none**. And the treatment-level
significance itself **disappears in the widest tier**, which is the one with the
most carbonate sites.

The median inflation is **2–11%** in variance, i.e. **1–5% in CV**. In the
widest tier the median within-treatment CV is **9.467% for SOC against 9.311%
for total carbon** — a 1.7% relative difference.

The per-site ratios show why nothing is significant: they run from **0.092**
(`USCO03`, IC 0.23%) to **14.77** (`MXOA01`, IC 2.94%), scattered above and
below 1 in roughly equal numbers. `MXOA01` is the single site that looks like
the mechanism, and its treatments have two replicates each — one degree of
freedom per variance.

---

## 1c — site level

Pooled within-treatment sums of squares per site over pooled degrees of freedom,
which is how variances estimated on 1–5 df each should be combined.

| tier | high-IC sites (> 0.1%) | low-IC sites | Spearman(IC, site CV) | Mann-Whitney high > low |
|---|---|---|---|---|
| T1 | 4 sites, 14.713% | 22 sites, 11.658% | **−0.191** (p = 0.35) | p = 0.86 |
| T2 | 6 sites, 14.743% | 53 sites, 14.297% | −0.100 (p = 0.45) | p = 0.77 |
| T3 | 5 sites, 12.904% | 25 sites, 11.821% | −0.215 (p = 0.25) | p = 0.95 |
| T4 | 9 sites, 16.838% | 71 sites, 14.537% | −0.101 (p = 0.37) | p = 0.56 |

The df-weighted contrast is 0.4–3.1 points higher for carbonate sites in every
tier — but **the rank correlation is negative in every tier**, and the
one-sided test for "high exceeds low" returns p = 0.56 to 0.95. The binned
difference comes from which sites land in a bin of 4–9, not from any monotone
relationship with carbonate content.

---

## The confound, measured rather than asserted

Site-level Spearman correlations of mean inorganic carbon against, over 93
sites:

| covariate | rho | p |
|---|---|---|
| **pH** | **+0.692** | < 1e-10 |
| clay | +0.359 | 0.0004 |
| Hargreaves climate moisture deficit | +0.337 | 0.0009 |
| Thornthwaite moisture index | −0.311 | 0.0024 |
| mean annual precipitation | −0.289 | 0.0050 |
| mean annual temperature | +0.096 | 0.36 |
| **SOC concentration** | **−0.030** | **0.77** |

Carbonate soils in NAPESHM are drier, higher-pH and finer-textured, and Mexican
sites carry **15× the mean inorganic carbon** of USA sites (0.517% vs 0.035%).
The aridity confound the brief warned about is real and measurable. It is *not*
a temperature effect and it is *not* an SOC-level effect.

`mi` and `hargreave_cmd` are used here **only as aridity covariates**. D-033
forbids treating either as an IPCC MAP:PET ratio and nothing here derives a
climate region from them.

---

## What this test could have detected — the project's own logic, turned inward

A null result is only informative against a stated detection limit. LoAM's whole
claim is that detectability is a property of the variance structure, so the
claim applies to this test as much as to a monitoring programme.

Take the zero-carbonate stratum as the reference. Under D-027 its CV is
`sqrt(spatial² + analytical²)`. An analytical term `a` replacing the `a₀ ≈ 3.13%`
already inside it raises the CV to `sqrt(cv₀² + a² − a₀²)`. The smallest `a`
whose predicted CV clears the upper end of the reference interval is the
smallest inflation this sample could have separated from noise:

| tier | reference CV | 95% CI | **minimum detectable analytical error** |
|---|---|---|---|
| T1 headline | 11.575% | [9.66, 13.45] | **7.54%** |
| T2 | 14.303% | [12.62, 15.54] | **6.83%** |
| T3 | 11.627% | [10.06, 13.55] | **7.62%** |
| T4 widest | 14.553% | [12.89, 15.59] | **6.41%** |

**Potash's stated range is 1% to 10%.** This design could only ever have
detected the **top third of it**. Anything from 1% to 6.4% would have passed
through invisibly, in every tier.

So the null is real but bounded, and the bound is the useful part:

> Between-plot CV in NAPESHM cropland is not detectably higher in
> carbonate-bearing soils, **at a detection limit of about 7% analytical error**.
> An analytical inflation in the lower two-thirds of the range the author named
> would not have shown up in this test, and this test does not rule it out.

Two contrasts make the point that the surviving "effects" are noise, not signal.

**In the headline tier** the implied added error in the one estimable carbonate
stratum is **8.54%** — inside Potash's range and above the detection limit, and
resting entirely on **4 Mexican sites of 2-replicate treatments** with an
interval 11.7 points wide.

**In the widest tier the implied added errors are mutually incoherent**:

| stratum | CV | implied added error |
|---|---|---|
| 0–0.1% IC | 17.267% | **9.29%** |
| 0.1–0.5% IC | 18.286% | **11.07%** |
| **> 0.5% IC** | 13.293% | **none — this stratum is *less* variable than zero-carbonate** |

The *lowest* carbonate bin implies a 9% added analytical error and the *highest*
implies a negative one. A mechanism driven by carbonate content cannot produce
that ordering. **These numbers are what a detection limit looks like when strata
are estimated on almost no information — not evidence of an effect.**

---

## What this means for D-040 and Phase 3

**D-040's invariance result survives a fourth independent attempt.** Climate
region, binned texture, a joint texture-and-carbon model, and now soil
inorganic carbon: four covariates, no signal above noise in the quantity a
spatial MDC surface would map.

**The analytical term is not the missing signal either — with a stated caveat.**
The brief posed this as the possible answer to D-040's invariance problem: if
the conditioning lives in the analytical component rather than the spatial one,
Phase 3 Deliverable 3 has a foundation again. On this evidence it does not, and
the two candidate explanations D-040 left open are **both still open** — MDC may
vary spatially through the *signal*, or the conditioning may live somewhere
none of our data can see.

**What would actually settle it.** A dataset with (a) replicate experimental
units under identical management, (b) 3+ replicates, (c) carbonate content
spanning 0 to >2%, and (d) that variation occurring **within** climate zone and
**within** country. NAPESHM has (a) and (c) but fails (b) and (d) exactly where
it matters. Lab duplicates would be better still: they would test the analytical
mechanism directly rather than through a bundled between-plot residual.

**And a note for the writeup, because it cuts the friendly way.** Potash et al.
held `σ_l` fixed and soil-independent in their published model, and the author's
own view in correspondence is that it should vary. We went looking for that
variation in the largest suitable open dataset and could not find it above a 7%
detection limit. **That is a second load-bearing simplification in the nearest
prior art surviving an independent test** — the first was `σ_b`
geography-independence (D-040). Any writeup says it that way round.
