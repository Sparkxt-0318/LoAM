# Phase 5 — the inverted audit. Design document.

**DESIGN ONLY. No implementation.** Nothing in this document is built, and
nothing should be built from it until the decisions listed in
[§10](#10--decisions-the-pi-owes-before-this-can-be-built) are made. Rule 4
applies: the 393-line unfed classifier is the precedent.

> ⚠️ **READ [`inverted_audit_redteam.md`](inverted_audit_redteam.md) ALONGSIDE
> THIS.** It attacks this design and lands two hits that change what should be
> built:
>
> * **B-1 — the framing in §1 is the weak point.** VM0042's Equation (2) is
>   optional *by design*: the protocol regulates precision through the
>   **uncertainty deduction**, not through a minimum sample size. Treating an
>   optional planning aid as a mandatory standard is an argument a registry wins.
>   **The recommended restructuring — compute the implied uncertainty deduction
>   and compare it with the one actually applied — is better than what is written
>   here, and it is checkable today against VCS 4022's published 31.35%.**
> * **C-3 — §2.1's algorithm was wrong** and is corrected in place below.
>
> This document is left standing rather than rewritten because the red team is
> the record of where it is weak, and B-1's restructuring is a decision the PI
> has not yet made.

---

## 0. The one-paragraph version

Instead of asking *"was this project's sampling design adequate?"* — which needs
design disclosure that [almost nobody provides](registry_corpus.md) — ask **"what
sampling would this claim have required to be detectable, and what would it have
cost?"** The inputs are area, claimed rate and interval, all published, plus a
variance structure, which is ours. The output is a single scalar per project: the
**minimum cost over all admissible designs** of resolving the claim it sold. When
that exceeds the credit revenue, the claim indicts itself without our ever seeing
the design.

**And the method is not ours.** It is Equation (2) of VM0042, which the
methodology makes optional in the same sentence it defines it.

---

## 1. The finding this design rests on

VM0042 v2.2 §8.2.1, item 11 — verbatim (D-057):

> "A power analysis **may** be conducted to calculate the number of samples
> needed to enable accounting of a minimum detectable difference, following
> Equations (1) and (2) (FAO, 2019). **However, projects are not required to take
> this number of samples.**"

> **Equation (1)** `MDD ≥ (S / √n) × (t_α,ν + t_β,ν)`
> **Equation (2)** `n ≥ ( S × (t_α + t_β) / MDD )²`
>
> where `S` = "Standard deviation of the difference in SOC stocks between t0 and
> t1", `t_α` two-sided at a level "frequently taken as 0.05", `t_β` one-sided for
> type II error "(e.g., 90%)".

**Three consequences, and they are the whole reason this design is stronger than
the forward audit:**

1. **The audit is the protocol's own calculation.** "You are asking the wrong
   question" cannot be answered against a project's own methodology's Equation
   (2). This is the answer to the registry adversary before the registry speaks.
2. **The only input we supply is `S`.** VM0042 expects it from the project's own
   pre-sampling — *"A pre-sampling of 5 to 10 soil samples per stratum may provide
   an estimate of SOC variance where up-to-date soil data are unavailable"* — and
   no project publishes it. **Our variance table is exactly the missing input.**
   That is the same role D-038 identified for `σ_b` against Potash et al., now at
   protocol level rather than paper level.
3. **The optionality sentence is the audit's justification in the methodology's
   own words**, and it is quotable.

---

## 2. Formal statement

### 2.1 What is being solved

Given, for a project:

| symbol | meaning | source |
|---|---|---|
| `A` | project area (ha) | register |
| `τ` | claimed SOC change rate (Mg C ha⁻¹ y⁻¹) | register, or credits ÷ area ÷ years |
| `Y` | monitoring interval (y) | register |
| `Δ = τ·Y` | claimed stock change over the interval (Mg C ha⁻¹) | derived |
| `n` | number of sampling locations | **solved for** |
| `C` | cores composited per assay | **solved for** |

and given a variance structure from `data/variance_table.csv`, solve

```
n_req(C) = ⌈ ( σ_d(C) · (t_α,ν + t_β,ν) / Δ )² ⌉        [VM0042 Eq. 2]
```

`t` depends on `ν = ν(n)`, so this is a **fixed point**, not a closed form.
Stating it as a fixed point rather than plugging in a large-sample `z` matters: at
small `n` the t-multiplier is materially larger, and small `n` is exactly the
regime the audit is interested in.

> **CORRECTED 2026-08-12 — solve it by BISECTION, not by iteration.** An earlier
> version of this section claimed the fixed point "is monotone and converges in a
> handful of iterations from `n = 2`". **That is wrong, and the red team
> demonstrated it** (`docs/inverted_audit_redteam.md`, C-3). The map is
> *decreasing* in `n` — more degrees of freedom means a smaller `t` means a
> smaller right-hand side — and naive iteration on a decreasing map can cycle:
>
> | σ | Δ | naive iteration, last 6 values | bisection |
> |---|---|---|---|
> | 4.0 | 2.0 | 44.04 ×6 | 45 |
> | **3.0** | **3.0** | **12.71, 12.50, 12.71, 12.50, 12.71, 12.50** | **13** |
> | 10.0 | 1.0 | 1052.73 ×6 | 1053 |
>
> **It cycles at small `n`** — the regime this audit exists to examine. Solve
> instead by **bisection on `g(n) = n_req(n) − n`**, which is monotone and returns
> the unique integer solution directly. Anyone implementing the sentence as
> originally written would have got a non-terminating loop.

### 2.2 `σ_d` — the standard deviation of the *difference*, and it depends on a design choice nobody discloses

`σ_d` is not a table lookup. It is assembled, and **the assembly differs by
whether the project re-samples the same locations or re-randomises**:

**Paired revisit** (return to the same nominal points; incur relocation error
because you cannot sample the same core twice):

```
Var(Δ̂) = [ σ_R²  +  2·(σ_W² + σ_A²)/C  +  2·σ_T² ] / n
```

**Unpaired** (re-randomise points each campaign):

```
Var(Δ̂) = [ 2·σ_B²  +  2·(σ_W² + σ_A²)/C  +  2·σ_T² ] / n
```

with `σ_B` between-plot spatial, `σ_W` within-plot spatial, `σ_A` analytical,
`σ_T` temporal, `σ_R` relocation. Depth/BD convention enters separately (§4).

**Between-plot variance cancels in the paired design and does not in the
unpaired one.** Since `σ_B` ≈ 11.5% of stock (`VC-BPS-006`) against `σ_R` ≈ 6.65%
per observation (`VC-REL-001` under its √2 caveat), **paired revisits are
substantially cheaper for the same detectability** — and that is a falsifiable
prediction of this framework, not an assumption.

**It also lands on a real project.** CAR1459 states it will *"re-randomize"* at
resampling. Under this model Indigo therefore pays the `2σ_B²` penalty rather
than the `σ_R²` one, and needs more locations than a paired design would. That is
a concrete, checkable claim about the best-documented project in the corpus, and
it belongs in the validation set (§7).

### 2.3 The degeneracy, and how it is removed without an arbitrary choice

The brief is right that the solution is a **surface, not a point**. But two of
the three dimensions are not free:

* **Sampling density is not a third dimension.** Density ≡ `A / n`. Once `n` is
  solved, density is determined. It is an output, not a knob.
* **That leaves `(n, C)`**, which trade off along an iso-variance curve. Choosing
  a point on it *would* smuggle in an arbitrary design.

**The removal: do not choose a point. Take the infimum over the whole
admissible set.**

The audit's claim is *"no plausible campaign could have detected this."* That is
a statement about the **best case**, so the quantity to report is

```
Cost*(project) = min over C ∈ {1, 2, …, C_max}  of  n_req(C) · (C·c_loc + c_assay)
```

with `c_loc` and `c_assay` from a stated price list. **The minimiser is a
by-product; the minimum is the finding.** No design is asserted, because the
statement quantifies over all of them:

> Under the most favourable admissible design and the most generous noise
> assumptions, resolving this project's claim would have cost at least `$X`.

This is the same optimisation D-053 already performed for G3 — `C* =
√((c_assay/c_loc) · σ_W² / (σ_B² + σ_nr²))` — so the machinery exists in
`scripts/g3_bounding.py` and the cost anchors are already sourced (Potash et al.
Table 1(d): location \$15, assay \$20, field visit \$400).

**`C_max` must be bounded and justified, not left open.** Recommend `C_max = 30`,
with the note that beyond ~10 the marginal variance reduction is negligible
because `σ_W²/C` is already below the irreducible terms. Report the frontier so a
reader can see the curve is flat there.

### 2.4 Running on the **low end** of the variance envelope — committed, not optional

**The PI's requirement, adopted here as a hard rule of the method.** The audit
runs on the most generous (smallest) admissible noise, so the headline reads:

> **Even under the most generous noise assumptions in our table, X% of claims
> required more sampling than any plausible campaign could have delivered.**

Running on central estimates invites *"your variance model is inflated and so is
your conclusion"* and there is no good answer to it. Running on the low end makes
that objection self-defeating.

**The exact rule**, keyed to the `bias_direction` field (D-023):

| `bias_direction` | take | why it is the generous choice |
|---|---|---|
| `inflates` (row is an upper bound) | **`value_low`** — the lower 95% bound | smallest noise the evidence permits |
| `deflates` (row already understates) | **`value`** as tabled | already an understatement; there is no lower bound to take |
| `unknown` | **`value_low`** where present, else `value` | generous by default, flagged in output |

Concretely: `VC-BPS-006` enters at **9.6%**, not 11.5%; `VC-TMP-003` at 2.708%,
not 3.322%; `VC-ANA-001` at its tabled 1.0% (D-054 notwithstanding — see §10).

**Every audit output must carry the envelope end it was run on**, and a
central-estimate run should be produced alongside as a sensitivity — never as the
headline.

---

## 3. Which inputs come from where

| input | source | status |
|---|---|---|
| project area `A` | ACCU register (`Project Area(s)` / CEA mapping file); Verra PD; CAR monitoring plan | **published** — but the ACCU register gives lot/plan identifiers, not hectares, so area needs deriving from the CEA shapefile for the 53 credit-issuing projects |
| credits issued | ACCU register (`ACCUs Total units issued`) | **published, 999/999** |
| interval `Y` | register crediting-period dates; VM0042 mandates 5-yearly remeasurement (D-057) | **published** |
| claimed rate `τ` | derived: credits ÷ area ÷ years | **derived** — and this is the weak link, see §8 |
| significance `α`, power `1−β` | VM0042 §8.2.1: α "frequently 0.05", β "e.g. 90%" | **from the methodology** |
| uncertainty rule `k` | VM0042 0.4307 · CAR SEP 1.028 · ACCU 0.253 relative SE (D-057) | **from the methodologies, verified primary** |
| `σ_B, σ_W, σ_A, σ_T, σ_R` | `data/variance_table.csv` | **ours** — this is the contribution |
| `σ_D` depth convention | `VC-BDC-001…004`, von Haden 2020 | **ours** (§4) |
| cost anchors | Potash et al. Table 1(d) | **published**, single source — a weakness (§8) |

**The audit must use each project's own registry rule for `k`, never a common
one.** D-057 established that CAR SEP is 2.38× VM0042 and 4.06× the ACCU rule on
identical measured variance. Applying one rule across registries would
manufacture differences between projects that are purely administrative.

---

## 4. The unknown depth convention — bracket it, and the bracket is free

**Recommendation: bracket, and make the ESM branch the headline.** The brief
proposes bracketing and asks for an argument. Here is a better one than "a project
that never stated its convention has no standing to object" — true, but
adversarial rather than technical.

**The technical argument: the generous branch is the ESM branch, so the headline
costs us nothing.**

von Haden et al. 2020 Table 1, mean absolute error in SOC stock under ±2.5 cm of
compaction: **ESM 0.2–1.1%, fixed depth 2.1–23.2%.** So:

* run with **ESM** → `σ_D` small → smallest total noise → **smallest required
  `n`** → the most generous case → **this is the headline**;
* run with **fixed depth** → `σ_D` large → larger required `n` → strictly
  strengthens any finding.

The unknown therefore cannot be the reason a finding is wrong: **the branch we do
not know is the branch that would make the project look worse.** Bracketing is
not a hedge here; it is a one-sided bound with the favourable end reported.

**And for VM0042 projects the ESM branch is not even an assumption.** D-057
established that VM0042 *requires* it: *"To enable the ESM approach, soil samples
at re-sampling must be divided into at least two increments."* A VM0042 project
either used ESM or was non-compliant. So for that population the headline branch
is a **compliance requirement**, not a charitable guess.

**Argument against bracketing, stated fairly:** it doubles every output and
invites readers to quote whichever end suits them. Mitigation — report the ESM
branch as *the* number and the fixed-depth branch only in a sensitivity column,
with the one-sided logic above stated at the point of use.

---

## 5. "Implausibly large" needs a basis, not a number

Three candidate anchors. **Recommend (b) as primary with (a) as corroboration.**

**(a) Densest real campaign ever disclosed.** CAR1459's **1 point per 8 acres
(3.24 ha)** is the densest disclosed campaign in the corpus, and it is a project
with a large budget and a strong incentive to be defensible. A required density
exceeding it means the claim needed a campaign denser than anything anyone is
documented to have run. *Strength:* empirical, from a real project. *Weakness:*
n = 1 anchor, and Indigo's density was chosen for its own objective, not as a
detectability floor.

**(b) Required cost against realised credit revenue.** Compute `Cost*` from §2.3
and compare with credits issued × a stated carbon price. If resolving the claim
would have cost more than the claim was worth, **no rational developer ran that
campaign, and the register tells us they were paid anyway.**
*Strength:* the threshold is set by the project's own economics, not chosen by
us. It is unanswerable without disclosing the design. And it **fuses the two
questions D-038 separated** — Potash et al. ask "is this economically feasible?",
we ask "is this claim resolvable?", and this asks *whether resolvability was ever
economically attainable*. *Weakness:* needs a carbon price, and prices vary by
an order of magnitude across vintages and buyers. Mitigation: report
`Cost* / revenue` as a ratio at three stated prices, and report the
**break-even price** at which the campaign becomes affordable — that is
price-free and it is the cleanest single number the audit can emit.

**(c) The registry's own floor.** VM0042 requires ≥3 control sites and ≥1 per
stratum (D-057). **Not usable** — it is a floor on what must be done, not a
ceiling on what is plausible, and it is far below anything detectability implies.
Recorded so it is not reached for later.

**The recommended headline metric** is therefore the **break-even carbon price**:
*"detecting the change this project claimed would have required a campaign costing
more than the credits were worth at any price below \$P/tCO₂e."* No threshold is
chosen by us; the project's own arithmetic sets it.

---

## 6. The 53 versus the 999

**Headline on the 53 credit-issuing projects.** They have an actually-monetised
claim, so `τ` is derivable from `ACCUs ÷ area ÷ years` rather than assumed, and
they are where the money is (439,348 ACCUs). This is the sharp subset and it
should carry the finding.

**Context from all 999, explicitly conditional.** The 946 without issuance have no
claim to test. For them the audit can only ask *"if this project claims the
scheme's typical rate, what would it need?"* — which is a statement about the
scheme's design space, not about any project. Report it as a **distribution of
required cost conditional on an assumed rate**, label the assumption in the
figure, and never let a 999-based number stand next to a 53-based number without
one.

**A caution on the 53.** They are the projects that got through verification, so
they are self-selected toward whatever verification selects for. That is a
*weaker* selection effect than the forward audit's (which selects on voluntary
disclosure) but it is not zero, and it belongs in the limitations.

---

## 7. The forward audit's new role: validation, not headline

Where designs *are* known, the inverted method must return an answer consistent
with what the project actually did. If it does not, the method is wrong.

**Test V1 — CAR1459 consistency.** Run the inverted audit on Indigo's disclosed
area, claimed rate and 5-year interval. Its density rule (1 point per 8 acres
over 100,371 acres) implies of order 12,500 locations at `C = 1`. **Pass
criterion:** required `n` at the cost-optimal `C` lands within an order of
magnitude of that. **If the method says the best-documented soil carbon project
on any registry needed 100× more sampling, the method is broken** — and we should
believe that before we believe the conclusion.

**Test V2 — the paired/unpaired prediction.** §2.2 predicts that Indigo's stated
re-randomisation costs them locations relative to a paired revisit. Their own
uncertainty numbers are public in the RP1–RP5 monitoring reports. **Pass
criterion:** our predicted `Var(Δ̂)` ordering matches the direction of their
reported margin of error.

**Test V3 — the Indigo bulk-density change. The best validation target we have.**
CAR1459 raised bulk-density sampling from **1-in-5 to 1-in-3** carbon points, and
said why, verbatim: *"sampling of bulk density at a higher spatial frequency was
needed to increase the precision of our estimates of SOC stock changes."*

**A design change made on variance grounds, documented as such, by a developer
with skin in the game.** Scoped as a test:

* model the stock estimate as `stock = conc × BD × depth`, with BD measured at a
  fraction `φ` of points and interpolated elsewhere, so its contribution to
  `Var(stock)` carries an interpolation penalty that falls with `φ`;
* compute predicted `Var(Δ̂)` at `φ = 0.2` and `φ = 0.333`;
* **pass criterion, direction:** the model must predict a *reduction*. If it
  predicts none, the framework is missing the mechanism Indigo acted on.
* **pass criterion, magnitude:** the predicted fractional reduction must sit
  within a factor of ~2 of the change in their reported margin of error across
  the reporting periods that straddle the switch.

Direction is the real test; magnitude is a bonus, because their reported margin
of error moved for many reasons at once.

**A dependency worth naming:** V3 needs `VC-BDC-*` to speak about *measurement*
error in bulk density, and those four rows are all `bias_pct` on a
`stock_change` basis — they are convention biases, not BD measurement variances.
**There may be no row in the table that supports V3.** If so, V3 is a proposal
for a new row, not a test, and it should be reported that way.

---

## 8. What could make this wrong — adversarially, against my own design

**Objection 1, and it is the strongest: model-assisted estimation.** VM0042
Equation (2) is a **sampling-only** MDD. Quantification Approach 1 projects use a
biogeochemical model, and the model borrows strength across space and time, so a
sampling-only required-`n` **overstates** what a measure-and-model design needs.
Most of the corpus — CAR1459 (DayCent-CR), VCS 4022 (RothC), CAR1513 (DNDC) — is
measure-and-model. **This objection is largely correct and the design must
concede it.**

*The honest form of the audit under it:* required-`n` is the requirement **for the
measurement pathway**, and a model substitutes only to the extent its *validated*
prediction error is smaller — a quantity VM0042 §8.6.1.1.1 requires projects to
quantify and propagate. So:
* on **QA2 (measure-and-remeasure)** projects the audit applies without
  qualification;
* on **QA1** projects it is an upper bound on required sampling, and the audit
  must say so in the same sentence as the result;
* the gap between them is itself reportable: *how much detectability is the model
  being asked to supply?* That reframes the objection as a finding.

**Objection 2: scope and support mismatch.** Our `σ_B` comes from replicate
experimental units 3.6–9 m wide on deliberately uniform research fields at
**0–15 cm** (NAPESHM, D-026), and from PNW dryland plots at 0–20/0–30 cm (Wuest,
G8). Projects are commercial fields at **0–30 cm**, often 25 ha or larger. Between-
plot CV at field scale could be larger (more heterogeneity) or the field-mean SE
smaller (vastly more locations). **We do not know the sign.** See §10 — this is a
decision, not a caveat.

**Objection 3: `τ` is derived, not published.** `credits ÷ area ÷ years` conflates
the SOC change with everything else in the ledger — N₂O, CH₄, fossil fuel,
leakage, buffer-pool withholding, and the uncertainty deduction itself. **The
derived `τ` is not the SOC rate; it is the net credited rate after deductions.**
Using it as `MDD` therefore tests a *smaller* number than the SOC change the
project actually claims, which makes required `n` **larger** than it should be —
i.e. this error runs *against* the project. That must be stated, and the audit
should where possible recover the SOC-only component (VM0042 requires per-pool
reporting) rather than lean on the conservative direction.

**Objection 4: cost anchors from a single source.** Every cost number traces to
Potash et al. Table 1(d). Their price list is US Midwest commercial. Applying it
to Queensland grazing land is a scope transfer nobody has validated. Mitigation:
report the **break-even price** (§5), which is a ratio and therefore less
sensitive to the absolute price level, and treat `c_assay/c_loc` — the only
quantity `C*` depends on — as the parameter to sensitivity-test.

**Objection 5: `σ_d` is the SD of a difference and our rows are not.** D-005
already requires paired-difference errors to stay on the difference scale, and
`VC-REL-001` carries an explicit √2 ambiguity between per-observation and
difference-scale SD. **Getting this factor wrong changes required `n` by 2×.**
The design must declare, per component, which scale it is on, and the declaration
must be testable — a schema field, not prose.

**Objection 6, the uncomfortable one: our own detection limits.** D-055 established
that our null on inorganic carbon holds only above ~7% analytical error. If the
true analytical term for a carbonate-rich project sits in the untested 1–6% band,
our `σ_A` is wrong for that project and we cannot say by how much. **The audit
inherits every detection limit in the variance table**, and the low-end rule
(§2.4) makes that worse rather than better, because it takes the smallest
admissible value in each component. Recommend: every audit output carries the
detection-limit statement of its weakest input component, and "a null is only
informative against a stated limit" applies to the audit's own nulls too.

---

## 9. What the deliverable looks like

Per project, one row:

| field | example |
|---|---|
| project id, registry, protocol | `ERF108333`, ACCU, 2021 measurement+models |
| `A`, `τ` (derived), `Y`, credits | 94,666 ACCUs |
| `σ_d` at the low envelope end, with each component named | — |
| `n_req` at cost-optimal `C`; the `(n, C)` frontier | — |
| implied density vs CAR1459's 3.24 ha/point | — |
| `Cost*`, and the **break-even carbon price** | — |
| ESM headline / fixed-depth sensitivity | — |
| QA1 upper-bound flag | — |
| every detection limit inherited | — |

Plus two figures: the distribution of break-even price across the 53, and the
`(n, C)` frontier for a worked example.

**The headline sentence the method is built to support:**

> Even under the most generous noise assumptions in our variance table, and under
> the most favourable sampling design admissible, detecting the change that X of
> the 53 credit-issuing Australian soil carbon projects claimed would have cost
> more than the credits were worth.

---

## 10. Decisions the PI owes before this can be built

Per hard rule 9, these are listed, not assumed. **Nothing is implemented until
they are made.**

**D-a — THE BLOCKER. The audit needs a 0–30 cm variance structure and the table
does not have one.** Projects report 0–30 cm. Our rows are:

| component | 0–30 cm row? |
|---|---|
| analytical | ✅ `VC-ANA-001` (concentration, 0–30) |
| between-plot spatial | ⚠️ `VC-BPS-006` is **0–15 cm** and D-026 **forbids rescaling**; `VC-BPS-007` is 0–30 but a *pure* between-plot term from one PNW series (3.38%) |
| **within-plot spatial** | ❌ **none.** Only 0–10 and 10–30 separately, and **G2 forbids combining them** without the unpublished inter-layer covariance |
| temporal | ✅ `VC-TMP-003` (0–30) |
| relocation | ✅ `VC-REL-001` (0–30) |
| depth/BD convention | ✅ `VC-BDC-001…004` (0–30) |

**Within-plot spatial at 0–30 cm is the gap, and it is the component that governs
the entire `C` dimension** — compositing averages down within-plot variance and
nothing else. Without it, `n_req(C)` cannot be evaluated at `C > 1`.

*Recommended route, not taken:* D-043's compositing contrast supplies an indirect
estimate — the Wuest 3-core versus 1-core residual ratio of **1.785 against
√3 = 1.732** implies a single-core within-plot CV of roughly **8–9%** at
0–20/0–30 cm. That is derived, already logged, and the right order. It is
*indirect*, and using it is a decision. **The alternative — bounding `C` between
1 and 4 and reporting the envelope — is weaker but needs no new assumption.**

**D-b — paired or unpaired as the default.** §2.2 shows they differ by `σ_R²`
against `2σ_B²`, a large factor. Almost no project discloses which it used
(CAR1459 does: re-randomised). *Recommend:* run the **paired** form as the
headline, because it is the cheaper one and therefore the generous one under
§2.4, with unpaired as sensitivity.

**D-c — which analytical figure.** This is **D-054**, still open. The audit is
sensitive to it: 1.25% versus 3.13% concentration CV. D-057 added evidence for the
narrow figure from VM0042's own laboratory requirement. Under §2.4's generous
rule the audit would take the *narrower* one regardless, which conveniently makes
this decision non-blocking for the headline — but it must be stated, not glossed.

**D-d — basis.** `VC-BPS-005` is a **concentration** CV and `VC-BPS-006` a
**stock** CV (D-052, `MIXED_BASIS_BY_DESIGN`). The audit is a stock-change
calculation and must declare one basis per run. *Recommend:* stock throughout,
which means `VC-BPS-006`, `VC-BPS-007…011`, and `VC-TMP-*`.

**D-e — difference-scale declaration.** Objection 5. Needs a schema field
recording, per row, whether the dispersion is per-observation or
difference-scale. That is a schema change and therefore a decision.

**D-f — is Phase 5 the headline deliverable?** The brief says yes and Deliverable
3 is retired. If so, `docs/phase0_summary.md` and any scope document still
promising a spatially explicit MDC surface need updating. Flagged here; not done
in this document.

---

## 11. What this document deliberately does not do

* **No code.** Not a script, not a stub, not a constant.
* **No new variance-table rows, and no promotion.**
* **No claim about any project.** Every project reference is an input example or a
  validation target.
* **No threshold chosen by us.** §5 recommends the break-even price precisely so
  that the project's own economics sets the bar.
* **No estimate of how many projects would fail.** That number does not exist
  until D-a is decided, and quoting one before then would be exactly the
  build-ahead-of-decision failure rule 4 exists to prevent.
