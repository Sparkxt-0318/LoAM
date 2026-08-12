# Red team — the Phase 5 inverted audit

**Attack, not implementation.** Nothing here is built. The target is
`docs/phase5_inverted_audit_design.md`, attacked as three adversaries with
different interests and different competence.

Each objection is stated **at its strongest** — the version a good scientist on
the adversary's payroll would make — then judged, then given the change that
would fix it. Where I could check an objection numerically I did, and one of
them **falsifies a prescription in my own design doc**.

---

## Provenance of this review — read before weighting it

**Every objection below is mine.** That is a limitation, and it is disclosed
rather than glossed, because the value of a red team is independence and this one
does not have it.

An independent cross-check **was attempted and failed.** Three separate agents
were given the design document cold, one per adversary persona, with no access to
my reasoning. All three read the document and produced analysis, and all three
failed to return it in the required structured form — the run aborted with
`StructuredOutput retry cap exceeded` on all three, after ~373 s and ~191k tokens.
The failure is mechanical (schema serialisation), not substantive, but the output
is unrecoverable in usable form and **no independent finding is incorporated
here.**

Per the two-attempt rule this is logged rather than retried, and it is logged in
the document rather than only in the handoff, because a reader assessing these
objections should know that nobody checked them but me.

**What that means for how to read this.** The two hardest findings are the ones
least dependent on my judgement: **C-3 is verified numerically** and either
reproduces or it does not, and **B-1 turns on a reading of VM0042's own text**,
which is quoted and can be checked in one minute against the primary. The rest are
argument, and argument from a single source.

**If an independent pass is wanted, the cheapest version is a human reading §1 and
§2.1 of the design doc with B-1 and C-3 in hand.**

---

## Required check — does the design commit to the low end of the envelope?

**Yes, explicitly, and it is load-bearing rather than decorative.**

`§2.4 "Running on the low end of the variance envelope — committed, not
optional"` states the rule as a hard rule of the method and gives the exact
mapping to `bias_direction`:

| `bias_direction` | take |
|---|---|
| `inflates` (upper bound) | `value_low` |
| `deflates` (already understates) | `value` |
| `unknown` | `value_low` where present |

with worked consequences (`VC-BPS-006` enters at **9.6%**, not 11.5%) and the
required headline form: *"even under the most generous noise assumptions in our
table, X% of claims required more sampling than any plausible campaign."* A
central-estimate run is required alongside as a sensitivity and **forbidden as
the headline**.

**No flag needed on this point — but see C-2, which shows the rule is not the
probabilistic statement its wording implies.**

---

## Adversary A — the project developer whose project got flagged

Technically sophisticated, commercially exposed, and right about more than is
comfortable.

### A-1. "Your `σ_B` is measured on research plots. Mine is a 25-hectare commercial field." — **MAJOR. Survives only with a change.**

**At its strongest:** `VC-BPS-006` is 11.5% CV between replicate experimental
units **3.6–9 m wide**, on a research station selected for uniformity, at
**0–15 cm**. My quantification unit is a commercial field of 25 ha or more at
**0–30 cm**, farmed unevenly for decades. Between-plot variance at my support is
a *different quantity*, not a noisier measurement of the same one — and your own
**D-026 forbids rescaling 0–15 cm to 0–30 cm**. So you do not have an in-scope
`σ_B` for my depth at all, and you know it: your §10 lists it as the blocker.

**Does the design survive?** Not as written. §10's **D-a** already concedes
there is no 0–30 cm within-plot row; A-1 says the *between*-plot term has the
same problem for a different reason (support, not depth), and §10 does not say
so.

**Fix:** §10 must add support/scale alongside depth as a blocking scope
question, and the audit must not run on a project whose quantification unit is
more than an order of magnitude from the support of the components. If that
excludes everything, **that is the finding** — the same shape as the corpus
result, one level down.

### A-2. "Run it on my soil, not on your table." — **MAJOR. Survives with a change, and the change improves the method.**

**At its strongest:** the low-envelope rule takes the lower CI bound of a
NAPESHM-derived distribution. That is the low end of *your sampling
uncertainty*, not the low end of the plausible range for *my field*. And your own
D-055 establishes invariance only to about **±2 CV points** — invariance at that
resolution does not license transporting a point estimate to my field.

**Does the design survive?** Yes, but only by changing what it reports.

**Fix, and it is a genuine improvement:** report the **break-even σ** — the
between-plot CV at which my claim becomes detectable at my disclosed area and
interval — alongside the break-even price. That inverts the burden one step
further: I must then assert a σ for my own soil and defend it. **In almost every
case I cannot, because I never published my pre-sampling variance either.**
Recommend adopting this as a second headline metric.

### A-3. "Your `τ` is not my SOC claim." — **MAJOR. Conceded in §8 but under-weighted.**

**At its strongest:** `credits ÷ area ÷ years` is the *net credited* rate after
N₂O, CH₄, fossil fuel, leakage, buffer withholding **and the uncertainty
deduction**. It is not the SOC stock change. §8 concedes this and argues the
error runs against me, which is true — but "conservative" is not a defence when
the magnitude is unbounded. **CAR1513 is the reductio: it is registered under a
soil protocol and its credits are almost entirely rice methane.** Audit that on a
SOC power calculation and the answer is meaningless, not conservative.

**Fix:** hard eligibility gate. The audit runs only where the SOC pool is
separable from the ledger, and reports the SOC share of credits per project.
Where it is not separable, the project is `not_auditable` — a status the corpus
schema already has vocabulary for.

### A-4. "The deduction already priced my sampling choice." — **MAJOR. See B-1, which states it better.**

### A-5. "Bracketing is free in the arithmetic and not in the newspaper." — **MINOR. Survives.**

**At its strongest:** §4 shows the ESM branch is generous, so bracketing cannot
make me look worse *in the calculation*. But the fixed-depth branch will be
quoted. "One-sided bound with the favourable end reported" is a property of the
method, not of how a number travels.

**Fix:** the deliverable spec in §9 should carry the ESM number as *the* value
and the fixed-depth branch in a footnote, not a parallel column. Presentation,
not method — hence minor. Worth doing.

---

## Adversary B — the registry defending its protocol

The most dangerous adversary, because the strongest objection here is one the
design doc currently does not answer at all.

### B-1. "Equation (2) is optional BY DESIGN, and you have mistaken a diagnostic for a standard." — **FATAL as written. Survives only by reframing, and the reframing is better.**

**At its strongest — and this is the single best objection in this review:**

You lean on *"projects are not required to take this number of samples"* as
though it were an admission. It is a design choice, and a defensible one.
**VM0042 does not regulate precision through a minimum sample size. It regulates
precision through the uncertainty deduction.** Sample as little as you like: the
deduction (§8.6.4, `t₀.₆₆₇`) converts your imprecision directly into forgone
credits. That is *outcome-based* regulation, and it is arguably superior to a
minimum-n rule, because it lets each project choose its own point on the
cost/precision frontier instead of imposing one.

Equation (2) is offered as a **planning aid** for a proponent deciding how much
to spend. Making it mandatory would be redundant with the deduction and would
penalise projects that can achieve precision by other means. **Your audit takes
an optional planning tool, declares it mandatory, and calls the difference a
scandal.**

**Does the design survive?** **Not in its current framing.** §1 treats the
optionality sentence as the audit's justification. Against B-1 that reading is
naive, and a registry would say so publicly and be believed.

**The fix, and it makes the audit stronger and more checkable:**

**Stop computing required-`n`. Compute the implied uncertainty deduction.**

Run the machinery to get `σ_d`, then evaluate the registry's *own* rule — `k ×
(SE/mean)`, with `k` = 0.4307 for VM0042, 1.028 for CAR SEP, 0.253 for the ACCU
rule (D-057) — at the sampling intensity the project plausibly used, and compare
with **the deduction the project actually applied.**

Three reasons this is better:

1. It is the registry's own regulatory instrument, evaluated on the registry's
   own terms. B-1 has no purchase on it.
2. **It is directly checkable against a published number today.** VCS 4022's
   applied deduction is **31.35%** (D-057) — a real figure from a real
   validation report. The method can be validated against it *now*, without
   waiting on the §10 blockers.
3. It changes the claim from *"you should have sampled more"* — which invites
   B-1 — to *"the deduction you applied implies a precision your design could not
   have delivered"*, which is an internal-consistency finding and much harder to
   answer.

**Recommend restructuring the design doc around this.** Required-`n` becomes an
intermediate quantity; the implied-versus-applied deduction becomes the headline.

### B-2. "Stratification reduces variance and your σ is unstratified." — **MAJOR. Survives with a change.**

**At its strongest:** VM0042 **requires** stratified random sampling and requires
at least one control site per stratum (D-057). Good stratification on soil type,
parent material and topography — which VCS 4022 documents — materially reduces
within-stratum variance. Your `σ_B` is a within-treatment residual pooled across
sites: an *unstratified* quantity. Required-`n` computed from it **overstates**
what a stratified design needs.

**Fix:** state required-`n` explicitly as *"the requirement for an unstratified
design"*, and report the **stratification efficiency** — the variance reduction
factor — that would be needed to bring the claim inside reach. That is another
quantity the project has not published and would have to assert.

### B-3. "Compositing too — and your own G2 blocks you." — **MAJOR. Already conceded in §10 as D-a; strengthened here.**

The `C` dimension is governed by within-plot variance, and **G2 forbids a 0–30 cm
within-plot CV**. So the audit cannot currently price the one design lever that
most directly reduces cost. §10 says this. B-3 adds that the fallback — D-043's
indirect 8–9% — comes from **PNW dryland at 0–20/0–30 cm (G8)**, which is the
narrowest scope in the whole table.

### B-4. "Buffer pool and conservative defaults already cover this risk." — **MINOR. Survives.**

**At its strongest:** VM0042 requires the *most conservative* emission factor
across baseline and project, and a non-permanence buffer is withheld on top of
the uncertainty deduction. Your audit prices detectability as though none of
that existed.

**Why it survives:** the buffer addresses *reversal*, not *measurement
precision*, and conservative EFs address the non-SOC pools. Neither substitutes
for detectability of the SOC change. **But the design doc should say this**,
because it is the obvious rejoinder and its absence looks like an oversight.

### B-5. "Your components are not validated for my geography, and you have said so yourself." — **MAJOR. Survives with disclosure.**

G8: every temporal row is one region — PNW dryland silt loam. D-055's caveat: the
invariance evidence is North American cropland weighted toward the USA. Applying
this to Queensland grazing land is a scope transfer nobody has validated.
**Fix:** the deliverable must carry a scope-distance flag per project, and
out-of-envelope projects reported separately rather than pooled into a headline
percentage.

---

## Adversary C — the disinterested statistician

### C-1. "Your infimum is an infimum over one price list." — **MINOR. Survives with labelling.**

**At its strongest:** §2.3 claims the degeneracy is removed by taking the minimum
over all admissible designs. But the cost functional is
`n(C)·(C·c_loc + c_assay)`, so the minimiser depends entirely on the ratio
`c_assay/c_loc`, and §3 concedes **every cost number traces to one source**
(Potash Table 1(d), US Midwest commercial). The infimum is over designs *at one
price list*, which is not the same as over all designs.

**Verified, and it partly exonerates the doc:** the optimum is interior, so
`C_max` is a safety rail rather than a hidden choice — that part of §2.3 is
sound. The price *ratio* is the live parameter.

**Fix:** report the break-even price as a function of `c_assay/c_loc` over a
stated range, and label the headline as conditional on the ratio.

### C-2. "Your 'most generous assumptions' is a union of marginals, not a joint bound." — **MAJOR. Survives, but the wording must change.**

**At its strongest:** §2.4 takes `value_low` for each of six components
*independently*. If each bound is a 2.5% marginal quantile, the joint event that
all six sit at their lower bounds simultaneously has probability far below any
sensible confidence level — it is not "the low end of the envelope", it is a
corner of it that corresponds to no plausible state of the world.

**Does the design survive?** Yes — the error is **conservative in the direction
the audit needs** (it understates noise, so it understates required `n`, so it
under-flags projects). But **the phrase "most generous noise assumptions" implies
a probabilistic statement the construction does not make**, and a statistician
will say so in public.

**Fix:** either (a) state it plainly as a deliberate worst-case-for-us corner
bound with no confidence interpretation attached, or (b) propagate the component
uncertainties by simulation and take a genuine lower quantile of `σ_d`. **(a) is
honest and free; (b) is better and cheap.** Recommend (b), with (a) as the
fallback.

### C-3. "Your fixed point oscillates, and it oscillates exactly where you care." — **MAJOR, and DEMONSTRATED. Does not survive as written.**

**At its strongest:** §2.1 says the fixed point *"is monotone and converges in a
handful of iterations from n = 2"*. The map is **decreasing** in `n` — larger `n`
means more degrees of freedom, smaller `t`, smaller right-hand side — and naive
iteration on a decreasing map can cycle rather than converge.

**Checked numerically, and the objection is right:**

| σ | Δ | naive iteration, last 6 values | bisection |
|---|---|---|---|
| 4.0 | 2.0 | 44.04 ×6 | 45 |
| 6.0 | 1.5 | 170.11 ×6 | 171 |
| **3.0** | **3.0** | **12.71, 12.50, 12.71, 12.50, 12.71, 12.50** | **13** |
| 10.0 | 1.0 | 1052.73 ×6 | 1053 |

**It cycles at small `n`** — the regime where `t` changes fastest with `ν`, and
the regime the audit is most interested in, because small `n` is where claims
fail.

**Fix:** replace fixed-point iteration with **bisection on `g(n) = n_req(n) − n`**,
which is monotone and gives the unique integer solution directly. The design doc
prescribes the wrong algorithm and must be corrected before anything is built.
**This is the one place a reader could have implemented §2.1 as written and got a
non-terminating loop.**

### C-4. "`σ_B` does not cancel in your paired design; you have assumed it does." — **MAJOR. Survives with a stated assumption.**

**At its strongest:** §2.2's paired formula drops `σ_B` entirely and carries
`σ_R²` instead. That is only exact if relocation error captures the *whole* of
the imperfect cancellation. Revisiting "the same nominal point" cancels the plot
deviation to the extent the point is the same; `σ_R` is defined as the error from
not sampling the same core twice, which is a *different* construct from the
residual plot-level deviation at a re-found location.

Also: the factor of **2** on the temporal term assumes the two occasions are
independent.

**Both survive, and D-044 is why the second does:** anniversary sampling buys
nothing — same-calendar-month revisits are no less variable than off-month ones
at any of five Wuest series, so there is no repeatable seasonal component to
induce correlation. **The doc should cite D-044 at that factor of 2**; at present
the 2 appears unjustified.

**Fix:** state the `σ_R`-captures-all-of-it assumption explicitly rather than
letting the algebra imply it, and cite D-044 for the factor of 2.

### C-5. "999 one-sided comparisons, and you want to quote a percentage." — **MAJOR. Survives with a change.**

**At its strongest:** §9's headline is *"X of the 53 …"*. Each project's verdict
is an estimate with its own uncertainty, and thresholding 53 or 999 noisy
statistics and counting the failures gives a proportion with **its own sampling
error plus a selection effect at the threshold**. Projects near the boundary flip
on noise.

**Fix:** report the **distribution of the break-even statistic**, not a count of
failures. If a proportion is quoted it needs an interval, and projects within the
uncertainty band of the threshold should be reported as a third category rather
than forced to a side.

### C-6. "Δ is already net of the deduction, so you are testing the wrong target." — **MINOR, and it compounds A-3.**

`τ` derived from issued credits is post-deduction. So `Δ` is smaller than the
SOC change actually claimed, which inflates required `n`. §8 notes the direction.
**But under B-1's reframing this stops being a nuisance and becomes the point** —
if the deduction is the object of study, its presence in `Δ` is signal, not
contamination. Another reason to adopt B-1's fix.

---

## Verdict

**One objection is fatal to the current framing: B-1.** The audit as written
treats an optional planning provision as a mandatory standard, and a registry
would win that exchange in public. **The fix is available, cheap, and makes the
method better** — compute the implied uncertainty deduction and compare it with
the one actually applied, which is the registry's own instrument and is
checkable today against VCS 4022's published **31.35%**.

**One objection falsifies a prescription in the doc: C-3**, demonstrated
numerically. Bisection, not fixed-point iteration.

**Two objections improve the deliverable rather than defending against it:**
A-2's **break-even σ** and B-2's **stratification efficiency**. Both push the
burden further onto quantities the project has not published — which is the
inverted audit's whole logic, applied one level deeper.

**Nothing here changes the corpus finding.** The disclosure gap (D-056) stands
untouched: these are objections to the *audit*, not to the observation that 999
of 999 Australian soil carbon projects publish no sampling design.

### Changes the design doc needs, in priority order

1. **Restructure around the implied-versus-applied uncertainty deduction** (B-1).
2. **Bisection, not fixed-point iteration** (C-3) — a demonstrated defect.
3. **Add support/scale to §10's blocking scope questions** (A-1).
4. **Re-word the low-envelope rule** as a corner bound, or propagate properly
   (C-2).
5. **Add a `not_auditable` gate** where the SOC pool is not separable (A-3).
6. **Add break-even σ and stratification efficiency** as reported quantities
   (A-2, B-2).
7. **Cite D-044 for the factor of 2**, and state the `σ_R` assumption (C-4).
8. **Report distributions, not counts** (C-5).
9. **Answer the buffer-pool rejoinder explicitly** (B-4).
10. **ESM as the value, fixed depth as a footnote** (A-5).

**None of these is implemented.** They are recommendations against a design
document, and the design document itself is still awaiting the six decisions in
its own §10.
