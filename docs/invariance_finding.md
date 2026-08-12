# One set of variance components serves temperate cropland

**Deliverable 3 — the spatially explicit MDC surface — is RETIRED.** Decided by
the PI, 2026-08-12. This document states what replaces it, and it is a stronger
claim than the thing it replaces.

---

## The claim

> **We searched for spatial structure in monitoring noise across climate,
> texture and soil chemistry, each time against a stated detection limit, and
> found none. A single set of variance components therefore serves temperate
> cropland. Minimum detectable change varies with DESIGN and with INTERVAL, not
> with PLACE.**

That is a positive, usable, falsifiable statement. It is not "we could not build
the surface".

---

## Why this is a better product than a map

A map of MDC would say: *look up your location, read off your noise.* What we
have instead says: *the numbers are the same wherever you are in temperate
cropland, so use these.*

**"Use these numbers anywhere in temperate cropland" beats "here is a map"** on
four counts:

1. **It is usable by people we will never meet.** A surface has to be
   distributed, versioned, interpolated at the user's coordinates, and trusted
   at locations where it was never fitted. A component table is six numbers with
   provenance.
2. **It cannot be wrong in a way a map can.** An interpolated surface fitted to
   covariates that do not predict the response produces structure that comes
   from the covariates, not the data — and it looks authoritative while doing
   it. D-040 said this plainly: *"Building it anyway would produce a map whose
   structure came from the covariates rather than from the data."*
3. **It is the harder claim to make and the more useful one to have.** Invariance
   across a covariate is a stronger statement than variation along it, because
   it holds everywhere in scope rather than at fitted points.
4. **It is checkable by anyone.** A reader with their own dataset can test
   invariance directly. Testing a surface requires the surface.

---

## The evidence, with every detection limit attached

Four independent conditioning attempts. **Each one is a null, and each one is
reported against a stated limit** — see the standard below.

### 1. Climate region (D-040)

Retiring a private climate envelope and replacing it with the IPCC 2006
temperature regime **re-admitted a third of the sample** — the single largest
scope change the project has made.

* concentration: **11.948% → 12.248%**, a shift of **0.300**
* stock: **11.456% → 11.304%**, a shift of **0.152**
* against 95% CI widths of **3.97 and 3.52**

**A thirteenth and a twenty-third of the interval, pointing in opposite
directions.** That is the pattern of noise, not of a suppressed effect.

**Detection limit:** a climate effect smaller than roughly **±2 CV points** would
not have been visible against these intervals.

### 2. Texture (D-040)

Tercile splits on clay (breaks 18.0 / 27.1%) and sand (24.2 / 39.9%):

| | high | mid | low | spread | widest bin CI |
|---|---|---|---|---|---|
| clay | 13.557% | 10.946% | 11.315% | **2.611** | **11.016** |
| sand | 13.305% | 10.871% | 9.615% | **3.690** | **10.464** |

Clay is **not monotone**. Sand is monotone in direction but the spread is
**a third of the noise on the bins**.

**Detection limit:** a three-way split of 26 sites leaves 9–12 sites per bin, and
cluster-bootstrap intervals at that size are **wider than every difference they
would separate**. Anything under ~10 CV points is invisible here.

### 3. A joint covariate model, re-run under a corrected estimator (D-040, D-058)

Given texture and carbon level together and free to use both:

| | value |
|---|---|
| weighted R² | **0.0722** |
| treatments / sites | 135 / 26 |
| `log_mean_soc` | +0.801 (t = +2.37) |
| `sand_frac` | +1.720 (t = +3.06) |

**The covariates explain 7% of the variation in between-plot variance.** Two
coefficients are nominally significant and are filed — as D-040 filed them — as
**a hypothesis, not a parameterization**.

This number is *lower* than the 0.093 D-040 originally reported, because the
estimator was repaired (D-058). **That repair was a test the null could have
failed**: excess noise inflates standard errors and depresses R², both of which
favour a null, so correcting it is what would have exposed a signal hiding
underneath. It did not.

### 4. Soil inorganic carbon (D-055)

Proposed by Eric Potash in correspondence (2026-08-11) as the mechanism most
likely to make the *analytical* term vary: organic carbon measured by difference
is noisier when the subtracted carbonate term is large.

* **Eight of nine estimable carbonate strata** contain their tier's
  zero-carbonate estimate; the one exception runs the **wrong way**.
* **No regression specification is significant** in the scope that matches
  `VC-BPS-005/006`.
* A paired contrast isolating the subtraction itself — with an **exact built-in
  null control that passed across 810 zero-carbonate treatments** — gives a
  median inflation of **2–11% in variance** and is **null at site level in every
  tier**.

**Detection limit: ~6.4–7.6% analytical error.** Potash's stated range is
**1–10%**, so this test covers only its **top third**. An inflation in the lower
two-thirds would not have shown up, and **is not ruled out**.

### And temporal variance behaves the same way (D-045)

No consistent dependence between sites, within sites, by treatment, or by
rotation phase. D-044 adds the design consequence: **anniversary sampling buys
nothing** — same-calendar-month revisits are no less variable than off-month ones
at any of five series.

---

## The repo-wide standard this establishes

> **A null is only informative against a stated detection limit.**

Adopted repo-wide, 2026-08-12. Every null result in this project must carry the
magnitude of effect it could have detected. A null without a limit is not a
finding — it is an absence of evidence being passed off as evidence of absence,
and it is the single easiest way for this project to mislead someone.

The standard already has teeth in three places, and they are the template:

* **D-055** states its limit in the finding itself (~7% analytical error) and
  computes it from the reference stratum's own bootstrap interval.
* **`scripts/ic_conditioning.py`** has a `power_statement()` function whose only
  job is to emit the limit alongside the result.
* **D-058** records that the estimator repair was a test the null could fail, and
  why.

**This is the project's own logic turned inward.** LoAM exists to say that
detectability is a property of the variance structure rather than of a mean
trajectory. That applies to our own findings exactly as it applies to a
monitoring programme's.

---

## The caveats that travel with the claim

**Scope.** North American and European temperate cropland, weighted heavily
toward the USA, at **0–15 cm** for the between-plot term (D-026 forbids
rescaling) and PNW dryland for the temporal term (**G8**). "Anywhere in temperate
cropland" is the claim's *reach*; this is its *evidence base*, and they are not
the same size.

**The aliasing, restated because D-058 changed its shape.** D-040's caveat read
"75 of 80 treatments from the USA". Under the repaired estimator the joint model
runs on **135 treatments, 75 USA / 60 Mexico** — the USA-dominance caveat no
longer applies to that fit. **It is replaced, not removed:** the re-admitted
Mexican treatments are exactly the 2-replicate ones (D-040 check 1c), and
`sand_frac` nearly doubles when they enter, which is what a country effect
wearing a texture hat looks like. **No Mexico/USA difference in this table may be
read as a climate or texture difference.**

**Four nulls are not a proof of invariance.** They are four failures to find
structure, each bounded. The honest form is *"invariant at the precision we can
reach"*, and that precision is stated above for each.

---

## What would overturn this

Stated concretely, because a claim that cannot be overturned is not a claim.

**For the carbonate/analytical channel — the cheapest to close.** Lab duplicates
on carbonate soils would test the mechanism *directly* rather than through a
bundled between-plot residual. To reach the lower two-thirds of Potash's 1–10%
range, a study needs an analytical-error estimate with a standard error small
enough to separate 1% from 3%. **That is a routine QA exercise**, not a field
campaign: a few hundred split samples spanning 0 to >2% inorganic carbon, from
one laboratory, analysed as replicate pairs. Nobody has to dig anything.

**For the spatial channel.** A dataset with replicate experimental units, **3+
replicates**, spanning a real climate gradient, **within one country** so country
does not alias the gradient, at a **common depth**. NAPESHM fails the last two
exactly where it matters. This is a bigger ask, and the invariance result is what
makes it lower priority.

**For the temporal channel (G8).** Any second region. KBS LTER already indicates
humid temperate is *more* variable than PNW dryland (D-047), so the direction is
known and the magnitude is not; the blocker is a written-permission licence, not
data.

**What would NOT overturn it:** a single site with an unusual CV. The claim is
about whether noise varies *systematically with mappable covariates*, and one
outlier is what a null with a stated limit already anticipates.

---

## Consequences

**For Phase 3.** Deliverable 3 is retired. The two possibilities D-040 left open
are **both still open and neither is a surface**: MDC may vary spatially through
the **signal** — treatment effect size, SOC level, depth distribution of change —
none of which this table parameterizes; or the conditioning may live somewhere
none of our data can see.

**For Phase 5, which is now the headline.** Invariance is what makes the inverted
audit tractable at all. If `σ` varied by location, auditing 999 Australian
projects would need a per-project variance estimate nobody can supply. Because it
does not, **one component set audits the whole register** — and the retirement of
Deliverable 3 is what licenses that. See `docs/phase5_inverted_audit_design.md`.

**For the writeup, and it cuts the friendly way (D-038).** Potash et al. held
`σ_b` fixed and geography-independent *"for lack of information"*, and held `σ_l`
soil-independent. We went looking for both. Neither varies detectably.
**Two load-bearing simplifications in the nearest prior art surviving independent
test** is a contribution to the literature, not a gap we caught them in. Any
writeup says it that way round.
