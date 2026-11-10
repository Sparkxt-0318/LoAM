# What the soil-carbon credit record lets anyone check: a disclosure census and an inverted detectability audit

**DRAFT preprint. Not for circulation.** Every number traces to a file and a decision record in
this repository; bracketed references (D-NNN, G-N) are to `DECISIONS.md`, and are kept in the
draft for checking and stripped for submission.

[Authors] · [Affiliations] · Draft of 2026-11-10

---

## Abstract

*(249 words)*

Soil-carbon credits are issued against changes in soil organic carbon (SOC), but whether a
project's sampling could have detected the change it is credited for is rarely checkable from
public documents. We ask what the public record lets anyone check. First, a complete census of
the Australian ACCU register: 999 of 999 soil-carbon projects have no field for sample count,
depth, compositing, density, depth convention or remeasurement interval, while 54 have been
issued 462,162 ACCUs. Second, the three major registries convert identical measured variance into
deductions of 0.253, 0.431 and 1.028 relative standard errors, a fourfold spread set by registry
choice alone. Third, we invert the audit. Using VM0042's own optional sample-size equation and a
variance table at its most generous, we ask what campaign each credited change would have
required, from published area, credits and interval. Of 56 projects that publish enough,
11 fall in our cropland scope. For 8, a campaign at the densest disclosed sampling density detects
the credited change, at break-even carbon prices of $0.003–0.94 per tonne. Three small, young
projects with small credited changes fall outside it. The deduction an audit "implies"
at its own optimum is fixed by the registry's rule. The published deduction is what carries
project information, read as the claim's ratio to its own detection floor. Every audit figure
rests on variance measured on research plots about 10,000 times smaller than the projects. That
support gap is the principal, unresolved limitation. The fix is a handful of registry disclosure
fields.

---

## 1. Introduction

A soil-carbon credit is a claim that SOC stocks changed by a stated amount over a stated
interval. Whether a monitoring campaign *could* resolve that change is a property of the
variance structure of the measurement, not of the carbon model behind it. The question is
therefore answerable without trusting any model's trajectory [README; D-004].

Potash et al. (2025) built the nearest prior model. Their error model asks whether a soil-carbon
project is **economically feasible** given realistic sampling costs. Our question is upstream of
theirs: whether a project's **claim is resolvable at all**. A feasibility calculation presupposes
that the change is detectable [D-038]. Their between-sample variance is fixed and
geography-independent "for lack of information". Our earlier work found between-plot CV
approximately invariant across climate, texture and inorganic carbon, to stated detection limits
(about ±2 and ±10 CV points, and ~7% analytical error). That supports their choice rather than
contradicting it [D-040, D-055; `docs/invariance_finding.md`]. Their error model has no term for
short-term fluctuation at a fixed point. Wuest and Durfee (2024) measured that at 15–32% of random
error, and our variance budget carries it as a temporal component. Their deduction constant (0.43
standard errors, after VM0042) is the hook for our comparison in §4.4 [D-038, all four
differences].

The obvious audit would read a project's sampling design and test whether it could detect the
claim. It cannot be run, because the designs are not published. That gap is our first result
(§3). The second is that the gap can be routed around. VM0042 already contains the calculation,
as its §8.2.1 Equation (2), and makes it optional in the same sentence [D-057]. Its only input
that projects do not publish is the variance, and that we can supply, generously.

## 2. Data and methods

### 2.1 The registry record

- **Australian ACCU Scheme.** Complete register, re-pulled 2026-11-10 (Last-Modified 2026-10-20;
  3,088 projects, 73 columns) [D-064].
  - Soil-carbon projects are those under the 2018 and 2021 measurement determinations (n = 999).
  - The register has no numeric area field. It publishes project-boundary files (999/999) and
    carbon-estimation-area (CEA) shapefiles for the 54 credit-issued projects. We compute
    geodesic CEA areas (GRS80) and record them as inferred.
  - Cumulative ACCUs ÷ 3.667 ÷ CEA area gives the net credited stock change Δ from the baseline
    to the latest sampling round [D-064].
- **Climate Action Reserve CAR1459.** Monitoring reports for RP4 and RP5, monitoring plan v5.4,
  RP5 verification report [D-066].
- **Verra VCS 4022.** Validation report v4.0 [D-056].
- **Other projects.** CAR1513 is registered under a soil protocol, but its credits are rice
  methane, so its SOC pool is not separable [red team A-3].
- **Verra more widely.** The registry moved platform in 2026 and could not be enumerated by
  machine (two attempts, logged as an access wall, not a disclosure gap) [D-066].
- **Scope.** Projects are classed by stated activity (cropland, grazing/pasture, unresolved) and
  by a geographic tropical-latitude flag. Out-of-scope projects are never pooled with in-scope
  ones [D-065].

### 2.2 The inverted audit

For each project:
1. **Required n.** VM0042 Eq. (2), `n ≥ (S(t_α+t_β)/Δ)²` with α = 0.05 and power 0.90, solved
   for the smallest integer n by bisection. Naive fixed-point iteration cycles at small n
   [red team C-3; D-059].
2. **S(C).** The SD of one location's stock-change estimate with C cores per assay. It is built
   from five components, each at the low end of the evidence:
   - between-plot 3.14% (the one 0–30 cm row);
   - within-plot 8.0% (indirect);
   - analytical 1.25%;
   - temporal 2.71%;
   - relocation 9.4%.
   [D-060, D-061, D-062]
3. **Design.** Paired (revisit) and unpaired (re-randomised) designs are both solved, and the
   cheaper is reported [D-060].
4. **Cost.** n(C·c_loc + c_assay) is minimised over C = 1–30 (US costs, Potash et al. 2025
   Table 1d).
5. **Break-even price.** Cost* ÷ credited tonnes.
6. **Break-even noise scale.** The factor by which all noise could grow before a campaign at the
   densest disclosed density (CAR1459: one point per 8 acres), on the project's own area, stops
   sufficing.
7. **Three categories** [D-067]:
   - *outside reach*: noise scale < 1 under the generous inputs;
   - *inside reach*: ≥ 1 even under the high corner of the variance table;
   - *within the uncertainty band*: between.
8. **Support-mismatch ratio.** Project area ÷ 0.019 ha [D-063].

### 2.3 Robustness

- **Independent re-implementation.** n_req, the cost optimum and the deduction comparison were
  re-implemented by a separate agent from a specification alone, without access to the code
  [WP3(i)].
- **Sensitivity.** We vary the paired/unpaired choice, the relocation scale and the assay:location
  cost ratio, and run central-estimate inputs [WP3(ii)].
- **Literature.** We review how between-location variance changes with spatial support, and
  apply the reported factors as scenarios [WP3(iii); D-070].

## 3. Result 1 — the disclosure census

[Table 1: register fields and fill rates across 999 projects; `projects.yaml` registry_coverage.]

**No field exists** in the ACCU register for sample count, sampling depth, cores per composite,
sampling density, depth convention or remeasurement interval. The fields are missing outright, not
left blank. The Regulator's own page states that project sampling plans are not published. The
scheme requires a sampling plan and regulates it in detail. It does not publish it. **462,162
ACCUs have been issued against soil-carbon measurements whose sampling designs are not public,
in any project in the scheme.**

The two other registries publish more, but not the parameters that matter.
- **VCS 4022.** The validation report confirms the design was reviewed. The design itself sits
  in PD appendices that are not public, and the monitored-parameter table lists "Number of cores"
  without a value.
- **CAR1513.** The monitoring plan defers its sampling design to a memo absent from the project's
  41 public documents.
- **Depth convention.** Not one project in any registry states whether it accounts on a fixed
  depth or an equivalent soil mass basis. That is the single undisclosed parameter with the
  largest documented effect on a credited quantity: a 17% understatement, sign reversals, and
  2.1–23.2% stock error at fixed depth against 0.2–1.1% under ESM [`docs/registry_corpus.md`
  Gap 3].

## 4. Result 2 — the same variance, a fourfold different haircut

[Table 2: k = 0.253 (ACCU, 40th percentile), 0.431 (VM0042, 33.3rd), 1.028 (CAR SEP, 15.2nd);
D-057.] The three rules are one construct — a deduction proportional to the relative standard
error — at different severity. CAR's rule multiplies z₀.₇₀ by the 95% CI half-width; VM0042's
multiplies t₀.₆₆₇ by the SE; the ACCU rule credits at the 40th percentile. **Identical soil,
design and variance yield a deduction four times larger under one registry than another.** The
*credited* consequence also depends on a share factor (the fraction of credits in the deducted
pool) that none of the three publishes per pool.

### 4.4 What a published deduction reveals — and what an "implied" one does not

At the audit's own cost-optimal design, n_req is defined so that SE ≤ Δ/(t_α+t_β).
- **What an implied deduction contains.** The deduction an audit *implies*, k·SE/Δ, is therefore
  at most 100k/(z_α+z_β), for any project and any variance: 13.3% under VM0042, 31.7% under CAR
  SEP, 7.8% under ACCU. The population confirms it (ACCU 5.0–7.8%; VCS 4022 13.18%; CAR1459
  31.71%), and so did the independent re-implementation [D-068].
- **What carries information.** A comparison of an implied deduction with an applied one carries
  no information about the project, beyond n. What does is the applied deduction itself. Inverted
  through the registry's own k, it gives the project's *own* stated relative SE. From that we get
  the ratio of the claimed change to the minimum difference the project's own precision could
  detect. This uses none of our variance inputs.

| project | applied | own relative SE | claimed Δ / own MDD (90% power) | (50% power) |
|---|---:|---:|---:|---:|
| CAR1459 (RP5) | 11.27% | 0.110 | **2.81** | 4.65 |
| VCS 4022 ‡ *pending expert review* | 31.35% | 0.728 | **0.42** ‡ | 0.70 ‡ |

‡ **Pending expert review, and dependent on PI decision A.** It is conditional on two points not
yet settled from primary documents. First, whether k = 0.4307 governed VCS 4022's v2.0 crediting:
it is verified for v2.2 only, and the approved v2.0 text is awaiting re-reading (D-072, open on the PR #21 port branch).
Second, whether the 31.35% is the SOC-pool deduction: the validation report calls it a single
"final uncertainty deduction" (PDF p. 147). Until both are settled and the reading has been
reviewed, this row is not quoted anywhere outside this section.

Both deductions pool sampling with model-prediction error, so these ratios describe each
project's stated precision, not its sampling alone. CAR1459's RP5 verification report records that quantification
to date rests on initial measurements plus modelling, with the re-measurement true-up deferred
under a Reserve variance determination.

## 5. Result 3 — the inverted audit across the auditable population

[Table 3: categories by group; Figure 1: break-even price by category; `docs/phase5_population_results.md`.]

| group | projects | inside reach | within band | outside reach |
|---|---:|---:|---:|---:|
| cropland, in scope† | 11 | 8 | 0 | 3 |
| grazing / pasture (out of scope) | 38 | 30 | 2 | 6 |
| land use unresolved (out of scope) | 7 | 4 | 1 | 2 |

† Cropland by stated activity. For the nine ACCU projects, "temperate" is only *not
contradicted* by latitude; it is not an IPCC climate classification [D-065]. CAR1459's own plan
lists tropical and boreal zones among those it spans.

**In scope**
- **Prices.** Median break-even price $0.31/tCO2e (range $0.003–182). Median break-even noise
  scale 1.76× (0.19–30.6×).
- **VCS 4022.** About 161 locations at 2 cores per assay detect its credited change of 1.54 Mg C/ha
  over five years, at $8,050, against 2.7 million credited tonnes: $0.003 per tonne. **The
  largest claims in the record are cheaply detectable.**
- **Outside reach.** The three outside-reach projects are young and small, with net credited
  changes of 0.55–0.81 Mg C/ha on 130–190 ha after one issuance. They would need 576–1,268
  locations, which is 3–7 per hectare and denser than any disclosed campaign, at $56–182 per
  credit.
- **Price and category.** The categories line up with break-even price without being defined on
  it. Inside reach runs to $1.74, the band is $1.04–1.79, and outside reach starts at $1.83.

**Out of scope.** The grazing projects carry the largest credited changes in the record: median
5.9 Mg C/ha, maximum 17.8, a lower-bound credited rate of up to 4.4 Mg C/ha/yr. Their
detectability (median $0.15/tCO2e) is not pooled with the in-scope result.

**Who the categories describe.** Forty-seven of the 54 ACCU projects share one proponent. That
proponent accounts for all 14 non-inside-reach projects, and 33 of its 47 are inside reach. The
categories follow area and credited change, not developer, and we draw no developer-level
inference.

**Robustness.** An independent re-implementation, written from the specification without access
to the code, reproduces every n_req, design, cost and implied deduction exactly: 0 of 336
optimisations differ. We varied the three choices a critic would challenge: the paired/unpaired
design, the relocation scale and the assay:location cost ratio (0.33–5.33). We also ran
central-estimate inputs. In-scope categories range from 6–8 inside reach and 3–5 outside, against
8 and 3 at baseline, and VCS 4022 and CAR1459 stay inside reach throughout. Break-even prices
scale linearly with absolute cost [`docs/phase5_robustness.md`; D-069]. One variant moves headline
numbers by more than 2×, and is reported as a named sensitivity.

**Sensitivity S1 — a forced paired design (D-060).** The headline takes, for each project, the
cheaper of a paired design (revisiting the same locations) and an unpaired one (re-randomising).
Under our inputs, 55 of 56 projects choose unpaired. S1 forces the paired design on every project:

| | headline (cheaper design per project) | S1: paired forced | change |
|---|---|---|---|
| VCS 4022: required n (C\*) | 161 (2) | 374 (1) | **2.3×** |
| VCS 4022: break-even price | $0.0030 | $0.0048 | 1.6× |
| CAR1459: required n (C\*) | 4,451 (2) | 10,430 (1) | **2.3×** |
| CAR1459: break-even price | $0.21 | $0.34 | 1.6× |
| in scope: inside / band / outside | 8 / 0 / 3 | 6 / 0 / 5 | two projects move outside |
| grazing: inside / band / outside | 30 / 2 / 6 | 26 / 0 / 12 | |

**S1 raises the required sample size of both projects with a published deduction by 2.3×, and
neither changes category.** It is the more expensive of the two admissible designs, so it is not
the headline (D-060 stands). It matters for a second reason: it is also the floor that the
support scenarios of §7 converge on, because the paired formula has no between-plot term.

## 6. Discussion

**What generalises, in order.** The census does, because it is a complete count of a register
that has no such fields. The cross-registry comparison does, because it is arithmetic on three
published rules. The audit distribution generalises least. The auditable population is
self-selected toward projects that published enough, and every audit figure carries the support
caveat (§7).

**What the audit says, read straight.** Under the most generous noise the evidence allows, most
credited changes in the auditable record would be cheap to detect. The ones that would not are
the smallest claims on the smallest areas. Nothing here suggests the large claims are
undetectable. The question the record cannot answer is whether they *were* detected. The designs
and realised precisions that would answer it are exactly what is not published. Where a precision
is published (two projects), it can be read against the claim directly, with no model of ours.

**Registries already hold the fix.** VM0042's Equation 2 is the right instrument. What is missing
is publication of its inputs. Nine fields would make any VM0042 claim checkable by anyone, using
VM0042's own equation: realised n per stratum; cores per composite; depth, increments and
convention; sampling dates; S; MDD at the realised design; the deduction by pool and source;
credited area per stratum; and, for measure-and-model projects, whether the re-measurement
true-up has happened. The same fields would serve the ACCU and CAR registries.

## 7. Limitations

**G9: support.** Every between-plot input is measured on research-plot support of about 0.02 ha.
The projects quantify at field to continental support: a median mismatch of ~10,000× in scope,
and 25 million× for VCS 4022. No validated relationship scales between-plot variance across that
gap, and we assume none. We report, per project, how much larger σ_B could be before each claim
leaves reach (median 3.4× in scope; 0× for the three already outside).

A literature pass (31 sources; most read at abstract level because publisher sites were
inaccessible) narrows G9 in one respect and not the other.
- **Stock variance: direction bounded.** Between-location stock variance is larger at commercial
  support than between research plots: about 1.5–5× as an SD within a field (single-core 0–30 cm
  CVs of 5–14% in cropland; Schrumpf et al. 2011), and plausibly 5–10× across fields. Applying
  those factors as scenarios, not distributions, the audit's exposure is capped. Above about 2×
  the paired design becomes cheaper, and it contains no between-plot term. So in scope the result
  bottoms out at 6 inside reach and 5 outside, and VCS 4022 and CAR1459 stay inside reach.
- **Change variance: direction not bounded.** The two available datasets disagree in sign
  (Polussa et al. 2026; Buchkowski et al. 2026). The paired floor rests on exactly that variance.

**Every "inside reach" is therefore conditional on the change-variance terms at commercial
support. These are unmeasured, and the study that would measure them is specified in the
repository.**

**Which VM0042 rule governed VCS 4022.** VCS 4022 was credited under VM0042 v2.0. The 0.4307
constant behind every VM0042 figure here is verified from the primary text of v2.2 only. It is
absent from the v2.0 public-comment draft we hold. We have not verified the approved v2.0 text on
this branch. An unmerged line of this project reports the approved v2.0 carries the same rule, and
we flag it as unverified here. Separately, VCS 4022's 31.35% is described in its validation
report as a single "final" deduction, not split by pool. The VCS 4022 row of §4.4 depends on both
points. The audit figures in §5 do not depend on either.

**Design choice: sensitivity S1, 2.3× (D-060).** Forcing a paired design on every project raises
the required sample size of VCS 4022 and CAR1459 by **2.3×** (161 → 374; 4,451 → 10,430) and
their break-even prices by 1.6×, and moves two in-scope projects from inside to outside reach
(8 / 0 / 3 → 6 / 0 / 5). The headline uses the cheaper design per project, which is unpaired for
55 of 56, because the audit's claim concerns the best admissible campaign. A reader who holds
that projects revisit their locations should read the S1 column instead (§5). It is also where
the support scenarios above bottom out.

**One region, generous inputs.** Temporal and between-plot inputs come from Pacific Northwest
dryland (G8). Within-plot variance at 0–30 cm is an indirect estimate (G2). The generous-corner
rule is a worst case for the audit, not a confidence bound.

**Δ is net credited, not measured.** Δ comes after every registry deduction, so it understates
the SOC change: conservative for the project. Measure-and-model projects' required n overstates
what a validated model would need.

**Costs and anchor.** Costs are US Midwest, and break-even prices scale linearly with them. The
"plausible campaign" is the densest disclosed one. On small farms a denser campaign is physically
possible.

**Population.** The record is self-selected, so the audit distribution is not a rate for any
scheme. Verra's roughly 200 VM0042 projects are missing because of an access wall, not a
disclosure gap.

## 8. Data and code

All inputs, scripts and decision records are in the LoAM repository: `data/registry/`,
`data/audit/`, `scripts/run_population_audit.py`, `scripts/sensitivity_audit.py`,
`scripts/independent_audit_reimpl.py`, and `DECISIONS.md` D-056 to D-070.

## References

- Potash, E., Bradford, M. A., Oldfield, E. E., & Guan, K. (2025). *Environ. Res. Lett.* 20,
  024025. doi:10.1088/1748-9326/ada16c.
- Verra (2025). VM0042 Improved Agricultural Land Management, v2.2, §8.2.1 Eq. (1)–(2), §8.6.4
  Eq. 74.
- Climate Action Reserve, CAR1459 Monitoring Report RP5 v5.8; Verification Report RP5 (Aster
  Global, 2026).
- Clean Energy Regulator, ACCU Scheme project register (CSV), as at 2026-10-20.
- Earthood (2024). VCS Validation Report, AgreenaCarbon Project, VCS.VAL.22.89 v4.0.
- Wuest, S. B., & Durfee, N. (2024). *Soil Sci. Soc. Am. J.* 88, 830–845. doi:10.1002/saj2.20660.
- [Other variance-table sources: Poeplau et al. 2022; NAPESHM; von Haden et al. 2020; Fowler et al.
  2023 — full list `docs/sources.md`.]
- Schrumpf, M., Schulze, E.-D., Kaiser, K., & Schumacher, J. (2011). *Biogeosciences* 8,
  1193–1212. doi:10.5194/bg-8-1193-2011.
- Buchkowski, R. W., Polussa, A., & Bradford, M. A. (2026). *Global Change Biology* 32, e70868.
  doi:10.1111/gcb.70868.
- Goidts, E., van Wesemael, B., & Crucifix, M. (2009). *Eur. J. Soil Sci.* 60, 723–739.
  doi:10.1111/j.1365-2389.2009.01157.x.
- Polussa, A., Oldfield, E. E., et al. (2026). *Geoderma* 473, 118007.
  doi:10.1016/j.geoderma.2026.118007.
- Lark, R. M. (2009). *Eur. J. Soil Sci.* 60, 748–756. doi:10.1111/j.1365-2389.2009.01156.x.
- [Full G9 source table, with access levels: `docs/g9_support_literature.md`.]
