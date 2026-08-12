# Phase 1 — truth generator: reconnaissance and design

**DESIGN DOCUMENT ONLY. Nothing is implemented, and nothing should be until the
open questions at the end are answered.** The 393-line unfed IPCC classifier is
the precedent (D-034): building ahead of the decision that justifies the build
produces code that has to be defended rather than used.

Evaluated: **pyRothC** as the Phase 1 engine. Verdict up front — *it works, it is
cleanly licensed, and it is probably not what this project needs.* The reason is
in §5, and it is a consequence of our own central claim.

---

## 1. Does it install cleanly?

Yes.

| | |
|---|---|
| Package | `pyRothC` 0.0.4, PyPI |
| Licence | **CC0 1.0 Universal** — public domain dedication, no attribution burden |
| Dependencies | `numpy>=1.20.3`, `pandas>=1.3.4`, `scipy>=1.7.3` — nothing exotic |
| Python | `>=3.7` |
| Release history | 0.0.1 → 0.0.4, all between 2023-03-04 and **2023-06-22** |
| Maintenance | **None since June 2023** — three years quiet |
| Size | ~240 lines in `RothC.py`; small enough to read in full and to vendor |

Installed and smoke-tested in an isolated target directory against our own
interpreter. It runs and produces a plausible equilibrium.

**On maintenance status:** three years of silence would normally be
disqualifying. It is not here, because RothC 26.3 is a *frozen published model* —
there is no upstream to track. A 240-line CC0 implementation of a fixed
specification is closer to a formula than to a library. **If we use it, we should
vendor it** rather than take a dependency on an unmaintained package.

## 2. Exact inputs, and what we have

`RothC(temperature, precip, evaporation, years, ks, C0, input_carbon,
farmyard_manure, clay, soil_thickness, DR, pE, bare, solver)`

| input | what it is | do we have it? |
|---|---|---|
| `temperature` | 12 monthly means, °C | ✅ WorldClim |
| `precip` | 12 monthly totals, mm | ✅ WorldClim |
| `evaporation` | 12 monthly **open-pan evaporation**, mm | ❌ **see §3 — this is the problem** |
| `clay` | percent | ✅ SoilGrids |
| `soil_thickness` | cm, default 25 | ⚠️ our scope is 0–30 cm; RothC is calibrated at 0–23/25 cm |
| `input_carbon` | annual plant C input, Mg C/ha/yr | ❌ **not observable; see §4** |
| `farmyard_manure` | Mg C/ha/yr | ⚠️ NAPESHM has management text, not amendment rates |
| `DR` | decomposable/resistant plant material ratio | ⚠️ literature default by land use (1.44 arable) |
| `bare` | is the soil bare this month | ⚠️ derivable from NAPESHM crop/rotation columns, roughly |
| `C0` | initial pool sizes (DPM, RPM, BIO, HUM, IOM) | ❌ only total SOC is observable; the split is a modelling choice |
| `ks`, `pE` | rate constants, evaporation coefficient | published defaults |

## 3. The evaporation input is D-039 again, in a new place

RothC's moisture function needs **open-pan evaporation**. WorldClim does not
publish it. WorldClim v2 gives solar radiation, wind speed and vapour pressure,
from which a *reference evapotranspiration* can be computed
(Penman–Monteith, Hargreaves) — but reference ET is **not** open-pan
evaporation, and RothC's `pE` coefficient (default 0.75) exists precisely to
convert between them in the direction the model expects.

> **Substituting a computed PET for open-pan evaporation is exactly the
> substitution D-033 refuses and D-039 documents as a finding.** We declined to
> impute MAP:PET for 87 NAPESHM sites on the grounds that a derived climate
> variable published without its formula cannot be reconstructed. Feeding
> RothC a Hargreaves ET as though it were pan evaporation would be the same
> move, made by us, inside the model.

This is not fatal — pan evaporation *is* obtainable, from station data or from
gridded products that publish it explicitly — but **it is a decision, not a
detail**, and it must be logged as one before any code is written.

## 4. `input_carbon` is unobservable, and that matters more than it looks

Annual plant carbon input is the single largest control on RothC's trajectory
and is not measured by anything we hold. Standard practice is **inverse
calibration**: run to equilibrium and solve for the `input_carbon` that
reproduces a measured SOC stock.

That is legitimate, and it has a consequence worth stating plainly: after inverse
calibration, **the model's SOC level is an input, not a prediction.** What the
model then supplies is the *shape* of the response to a management change, not
the level. For a detectability testbed that is arguably the right division of
labour — but only if the pipeline is built to respect it (§5).

## 5. CRITICAL — where our premise is at risk

Our claim is that **MDC depends on the variance structure, not on the mean
trajectory being right.** Three channels could break that, and one of them is
live.

### 5a. The mean-stock channel — REAL, and already flagged in our schema

Most of our components are **relative** (`cv_pct`). Turning a CV into an absolute
SD in Mg C/ha requires a mean stock. **If that mean comes from RothC's simulated
trajectory, MDC inherits RothC's level error directly.** Our schema has flagged
this exposure since the beginning (`mean_dependent`, rules R4/R5, D-007) — it
just has not had a truth generator to leak from yet.

**Mitigation, and it is cheap:** convert CV → SD using an **observed** mean stock
(NAPESHM site means, Wuest's `site_stock_mg_c_ha`, or a SoilGrids prior), never
the simulated one. Then RothC supplies the *change*, and the noise is scaled by
something measured. This should be a hard rule in the observation simulator, and
testable: no variance component may read a stock from the truth generator.

### 5b. The signal channel — a framing choice, and the safer framing is free

If the Phase 1 output is *"can we detect the change RothC predicts?"*, the answer
depends on RothC entirely. If it is *"what is the smallest change detectable
under this noise?"*, RothC is irrelevant to it.

**Recommendation: make MDC the primary output and keep it a pure noise
property.** Then run a second, clearly separate comparison — *"is a plausible
management effect larger than MDC?"* — where the effect size is a stated scenario
parameter, with RothC as one way of generating plausible values and published
effect sizes as another. Two outputs, one of which never touches the model.

### 5c. The depth channel — a real limitation of RothC specifically

RothC is a **single-layer** model. It cannot represent redistribution of carbon
with depth, which is precisely the mechanism behind component 6 and behind von
Haden's fixed-depth versus equivalent-soil-mass error (task 3, `docs/sources.md`).

So RothC **cannot generate the truth that component 6 measures error against.**
If Phase 1 wants to simulate ESM-vs-fixed-depth bias honestly, that has to be
imposed on top of RothC as a separate observation-model step, using our
`VC-BDC` rows — not derived from the engine. Worth knowing before anyone tries.

## 6. Where the variance components attach

Two groups, and the split should be enforced rather than remembered:

**Inputs to the truth generator** — none. Every one of our six components is a
property of *measurement*, not of soil. Nothing in the variance table belongs
inside RothC.

**Applied afterward, in the observation simulator:**

| component | how it attaches |
|---|---|
| 1 analytical | per assay, multiplicative on concentration (`basis: concentration`) |
| 2 within-plot spatial | per core, averaged down by compositing — this is the `v_w/C` term in D-053 |
| 3 between-plot spatial | per plot, not reduced by compositing |
| 4 temporal | per visit; **separable and combined rows must not both be applied** (D-043) |
| 5 relocation | per revisit, on the *difference*, saturating with offset (D-019, `VC-REL-004`) |
| 6 depth/BD convention | a **bias**, not a variance — applied as an offset, never summed into the variance budget (D-023, R9) |

Note components 1–4 now carry an explicit `basis` (D-052, PR #7). **The
observation simulator must pick one basis per run and convert deliberately**, and
that conversion is the only other place a mean stock can leak in.

## 7. Alternatives considered

| option | why not (or why maybe) |
|---|---|
| **SoilR / RothC in R** | Mature and better maintained, but adds an R runtime to a Python project for a 240-line model. Rejected on integration cost. |
| **Century / DayCent** | Far heavier input requirements — full N cycling, daily weather, site history. Every added input is another `input_carbon`-shaped unobservable. Rejected as disproportionate. |
| **ICBM** (two pools) | Fewer parameters, same qualitative behaviour, far less to justify. **A serious candidate** precisely because we do not need a good mean trajectory. |
| **No process model at all** — a parametric trajectory (linear, or saturating exponential toward a new equilibrium) with rate as a scenario parameter | **The option our own premise points at.** See below. |

### The uncomfortable conclusion

If §5b is taken seriously — MDC as a pure noise property — then **Phase 1 may not
need a carbon model at all.** A stated change rate, a stated equilibrium, and the
variance structure are sufficient to compute MDC and to ask whether a given
effect size clears it. RothC would then be supplying *plausible values for one
scenario parameter*, which is a much smaller job than "truth generator" implies,
and one a table of published effect sizes could also do.

This is worth deciding before building, because the two designs differ in what
has to be defended. A process-model design has to defend RothC's calibration to
every reviewer. A parametric design has to defend only the range of change rates
it scans — and that range is directly citable.

**This is not a recommendation to abandon RothC.** It is a recommendation to
> **UPDATED 2026-08-12: Deliverable 3 is RETIRED** (see
> `docs/invariance_finding.md`). The paragraph below was written while it
> was still live; the question it poses is unchanged, but the branch that
> depends on a spatially explicit surface is now closed.

decide *what the truth generator is for* first. If Phase 3's spatially explicit
surface needs mechanistic climate response — and D-040 has already put that
deliverable in question — RothC earns its place. If Phase 1 only needs a signal
to bury in noise, it does not.

---

## 8. Open questions — for the PI, explicitly

1. **Is MDC the primary Phase 1 output, as a pure noise property (§5b)?** If yes,
   the engine choice mostly stops mattering and the parametric option becomes
   the default. If no, say what the primary output is.
2. **Open-pan evaporation (§3): source it, or accept a documented PET
   substitution?** Sourcing it is the D-033-consistent answer. A substitution is
   defensible but must be a logged decision, not a default argument.
3. **`input_carbon` by inverse calibration — accepted?** It makes the SOC level
   an input rather than a prediction. I think that is fine and worth saying out
   loud, but it changes what the model is claimed to do.
4. **Vendor pyRothC (CC0, 240 lines) or depend on it?** Recommend vendoring: it
   is unmaintained, small, and implements a frozen specification.
5. **Does Phase 1 need depth resolution?** RothC cannot provide it (§5c), and
   component 6 is a depth-convention bias. If yes, RothC is the wrong engine
   and a layered model is needed.
6. **Should "no variance component may read a stock from the truth generator" be
   an enforced test?** I think yes — it is the mechanical version of the premise
   this whole project rests on, and it is the natural successor to D-032, D-051
   and D-052.

---

## 9. What was NOT done, deliberately

No truth generator. No pipeline. No pyRothC wrapper, no vendoring, no
configuration schema, no scenario definitions. `pyRothC` was installed **outside
the repository**, in a scratch directory, and is not added to
`pyproject.toml`. Nothing in this document is executable, and that is the point.
