# Phase 5 — the corpus-wide detectability sweep

**SCOPE DOCUMENT. No implementation.** Written 2026-08-13, after D-059.
Decisions the PI owes are in §8 and nothing downstream of them is built.

---

## 1. What changed, and why this is now the headline

D-056 found Phase 5's population problem: registry sampling designs are almost
never published, the readable projects are self-selected, and any audit built on
them is biased toward "adequate".

D-057 found VM0042's Eq. (2) *is* the inverted audit — but it needs `S`, the
standard deviation of the SOC stock difference, which the methodology expects
from project pre-sampling that nobody publishes.

**D-059 removes the input.** Under VM0042 v2.0 case N3, the published uncertainty
deduction is algebraically `MDD / Δ`. The detectability ratio is not something
LoAM computes from its variance table and asserts against a project — **it is
already published, in a field the registry required, validated by a third party,
and accepted.**

The sweep is the generalisation of that to every project that publishes a
deduction under any of the four rules LoAM has read from primary sources.

---

## 2. The identity, registry-agnostic

Every uncertainty rule in the corpus has the same shape: a multiplier `k` on the
**relative standard error** of the emission-reduction estimate.

```
UNC  =  k · σ_rel                    where σ_rel = SE(Δ)/Δ
MDD  =  (t_α + t_β) · SE(Δ)          VM0042 v2.0 Eq. 88 / v2.2 Eq. (1), FAO 2019
```

Eliminating `SE(Δ)`:

> ### Δ / MDD = k / ((t_α + t_β) · UNC)

The project's own published deduction, divided by a constant that depends only on
which rule it was written under. **No design parameter, no variance estimate, no
disclosure beyond the deduction itself.**

### The four `k` values, all from primary sources

| rule | `k` (multiplier on relative SE) | source |
|---|---:|---|
| VM0042 **v2.0**, case N3, Pathway A | **1.960** | v2.0 §8.6.4 Eqs. 83/84 — the 95% half-width, `A = 0` (D-059) |
| VM0042 **v2.2**, Eq. 74 | **0.4307** | v2.2 §8.6.4, `t₀.₆₆₇` (D-057) |
| CAR SEP v1.1 | **1.028** | `z(70%) × 95% half-width`, via CAR1459's monitoring plan (D-057) |
| ACCU / ACCM | **0.2533** | 60% exceedance, per VM0042 v2.0's own footnote (D-057) |

VM0042 v2.0 **case N1** (`A = 15%`) is the same `k` with an offset: `UNC = 1.960·σ_rel − 15%`.
It is listed separately in the eligibility table (§5) because the offset makes it
a different inversion, not a different constant.

### The screening thresholds

Setting `Δ/MDD = 1` — the project claims exactly its own detection floor — gives
a published-deduction threshold per rule. **These are exact, and they are the
whole screen:**

| rule | claim = MDD at 50% power | claim = MDD at 80% power |
|---|---:|---:|
| VM0042 v2.0 case N3 | UNC ≥ **100.0%** | UNC ≥ **70.0%** |
| VM0042 v2.2 | UNC ≥ **22.0%** | UNC ≥ **15.4%** |
| CAR SEP v1.1 | UNC ≥ **52.4%** | UNC ≥ **36.7%** |
| ACCU / ACCM | UNC ≥ **12.9%** | UNC ≥ **9.0%** |

Note the first row. VM0042 v2.0 Eq. 83 caps `UNC` at `MIN{100%, …}` — and 100% is
**exactly** the point at which a case-N3 project's claim equals its MDD at 50%
power. *Any v2.0 case-N3 project reporting a capped 100% deduction is, by its own
arithmetic, claiming a change no larger than its minimum detectable difference.*
The cap is a detector. Whether any project has hit it is an empirical question
the sweep answers.

---

## 3. Two findings already visible, before the sweep runs

Both fall out of §2 and should be verified early, because if they hold they may
outrank the sweep itself.

**(a) VM0042 v2.0 is 4.54× more severe than v2.2 on identical measurements.**
`1.960 / 0.4307 = 4.54`. Concretely, VCS 4022's implied relative SE of 16.0%
produces a **31.35%** deduction under the v2.0 rule it was validated against, and
would produce **6.91%** under v2.2. Same soil, same design, same measurements, a
4.5× different haircut — decided by which version of one methodology was in force
on the validation date.

*Verification required before this is stated as a result:* confirm that `s²` in
v2.2 Eq. 74 has the same content as `Σ s²_{Δℓ,t}` in v2.0 Eq. 84. If v2.2 also
changed what enters the variance, part of the 4.54× is compositional rather than a
severity change. **Do not report the ratio until this is checked.**

**(b) Published deduction percentages are not comparable across registries *or*
across versions of one methodology** — and the corpus already says so in two
independent ways: through `k` (§2) and through the Eqs. 36/37 share factor, which
made VCS 4022's 31.35% an 18.48% effective deduction on gross ERRs (D-059). Any
league table of "which registry deducts most" that reads PD headline percentages
is wrong twice over.

---

## 4. Population, and the retrieval problem

This is the real risk in the sweep, and it is a retrieval risk, not a method risk.

| population | size | deduction published? | reachable? |
|---|---:|---|---|
| Verra VM0042 projects | **unknown — task 1** | yes, in the PD and restated in validation/verification reports | `registry.verra.org` is SPA-blocked (4 endpoints, 2 attempts, D-056). Reports are mirrored by third parties — VCS 4022's came from a Terrapass mirror. |
| CAR Soil Enrichment projects | **unknown** — pagination blocked (D-056) | yes, in monitoring/verification reports | first page enumerated only; CAR1459 reached by direct ID |
| ACCU soil carbon projects | **999** (census, D-056) | **no** — the register has no uncertainty field | register is fully machine-readable, but carries nothing to invert |

**The ACCU population is the largest and is out of reach for this method.** 999
projects, 53 with credits, 439,348 ACCUs, and no published deduction to invert.
That has to be stated plainly in any write-up: the sweep covers the registries
that publish an uncertainty statistic, which is not the registry with the most
projects. It is a real limit on generality and it is not a reason to skip the
sweep — it is the same finding D-056 already made, arriving from a second
direction.

**Time-boxed retrieval plan, two attempts per target:**

1. Enumerate VM0042 projects. Try, in order: Verra's public project-database
   export; the VCS project search behind a headless browser; third-party
   aggregators. **1.5h, then stop and report the count reached.**
2. For each project reached, pull the validation *and* verification reports.
   Deductions appear in both; verification reports carry the *realised* figure
   and are the better source.
3. Log every blocked target in `blocked_or_deferred` with attempt counts, as now.

If task 1 returns fewer than ~10 projects, **stop and report** rather than
running a sweep on a corpus too small to distribute.

---

## 5. Per-project cost: the case determination is not free

VCS 4022 showed what one project costs. Neither the PD nor the validation report
named a version-case or a pathway; the case had to be reconstructed from a
corrective-action-log entry about IPCC Tier 1 emission factors, and getting it
wrong would have moved the answer 48% (D-059).

**Every project therefore needs four fields established before its `k` is known:**

| field | how it is determined | stated in documents? |
|---|---|---|
| methodology **version** | validation report, usually §3.3.6 | yes, reliably |
| **case** N1 vs N3 | which Quantification Approach was used for **direct N₂O** — v2.0 §8.2.8 makes the test mechanical (QA1 → modelled, QA3 → default factors) | **no** — reconstructed |
| **pathway** A vs B | inferred from the form in which the deduction is applied; Pathway A yields a percentage applied multiplicatively (Eqs. 36/37), Pathway B a retained fraction | **no** — inferred, and weakly |
| published **UNC** | PD uncertainty table, restated in validation/verification | yes |

Two of the four are inferences. **Every project record must carry them as
`inferred` with the counterfactual attached**, exactly as VCS 4022's does — never
folded into a `stated` field. Budget ~45 min per project for the case
determination alone; it is a document read, not a lookup.

**Automation stance:** the retrieval is scriptable, the case determination is not.
Do not write a classifier for it. (The 393-line unfed classifier is the standing
precedent.)

---

## 6. What the sweep cannot do

Three limits, all of which must appear in the write-up beside any result.

**(a) It measures self-consistency, not truth.** `Δ/MDD` is computed from the
project's *own* variance estimate. A project that understated its variance gets a
flattering ratio, and the sweep cannot tell. **The sweep can find projects whose
own arithmetic condemns them; it cannot find projects whose arithmetic is wrong.**

**(b) The MDD is of the whole estimate, not of the soil campaign — and this
direction flatters LoAM's thesis, so it must be said out loud.** For QA1
measure-and-model projects the pooled `Σ s²_{Δℓ,t}` includes model prediction
variance (VCS 4022's participant confirms it in as many words). The pooled SE is
*larger* than the sampling-only SE, so the effective MDD is larger and `Δ/MDD` is
*smaller* than a sampling-only reading would give. That is anti-conservative for
us. **Findings must therefore be phrased as "the project's total estimate sits
X× above its detection floor", never "the sampling design sits X× above".** The
pooled quantity is the one the credit actually rests on, which makes it the more
relevant number — but it is not a statement about the soil campaign.

**(c) The 50%-power convention is ours.** `t_β = 0` is what makes the identity
exact. Report both 50% and 80% throughout; never report one alone.

### Where LoAM's variance table re-enters — as a cross-check, not an input

Limit (a) is the opening for Phase 5 part 2, and it is the right sequencing.
Once the sweep has each project's **implied relative SE** (`UNC/k`, exact), that
number can be compared against what LoAM's variance envelope says is achievable
for a design of that scale. A project whose implied SE is *below* the envelope's
low end is claiming a precision the measurement literature does not support.

That comparison is where the variance table belongs — **auditing the implied σ,
not supplying it.** It also needs the estimand problem solved first: LoAM's
between-plot rows measure replicate plots within one site, and these projects
sample fields within strata across countries. **That gap is a prerequisite for
part 2 and is not in scope here.**

---

## 7. What the sweep produces

1. **A distribution of `Δ/MDD` across every project that publishes a deduction**,
   at 50% and 80% power, with version/case/pathway on every row.
2. **A count, not an estimate, of projects below their own detection floor** —
   `Δ/MDD < 1`. Exact, because the threshold is exact.
3. **The version and registry effect** (§3a), if it survives verification: the
   same measurements taken to four different registries produce deductions
   spanning 4.05% to 31.36%.
4. **The disclosure census extended**: for every project reached, whether case and
   pathway were *stated* or had to be reconstructed. VCS 4022 is n = 1 with both
   reconstructed. If that rate holds, it is a finding about registry transparency
   in its own right — a required deduction whose governing rule the documents do
   not identify.

---

## 8. Decisions the PI owes before this runs

1. **Is `Δ/MDD` the headline metric, or the implied relative SE?** They carry the
   same information. `Δ/MDD` is more legible and is LoAM's own language; implied
   SE is more directly comparable to the variance table and to Potash et al.
   *Recommendation: `Δ/MDD` for the headline, implied SE carried in every row.*
2. **Power convention for the headline number** — 50% (where the identity is
   exact) or 80% (where the claim is stronger and the arithmetic needs one extra
   constant). *Recommendation: 80% for the headline, 50% reported beside it, on
   the grounds that 50%-power detectability is not a defensible standard for a
   credited claim.*
3. **Does the sweep include out-of-scope projects?** Most CAR SEP and all ACCU
   soil projects are grazing, not cropland. The identity does not care about
   scope. LoAM's scope lock does. *Recommendation: compute for all, report
   in-scope and out-of-scope separately, never pooled — the same rule D-016
   applies to variance-table rows.*
4. **Verify §3a before or after the sweep?** It is ~1h of methodology reading and
   may be a bigger result than the sweep. *Recommendation: before — if the `s²`
   contents differ between versions, several downstream framings change.*
5. **How hard to push on Verra retrieval.** A headless browser would very likely
   work and was ruled out of scope last session. Two attempts then log, or
   authorise the browser?

---

## 9. Staging and time box

| stage | work | box | stop condition |
|---|---|---|---|
| 0 | Verify §3a: is `s²` the same object in v2.2 Eq. 74 and v2.0 Eq. 84? | 1h | report either way |
| 1 | Enumerate VM0042 projects; count reached | 1.5h | < 10 projects → stop and report |
| 2 | Per project: version, case, pathway, UNC → `Δ/MDD` | 45 min each | — |
| 3 | Distribution, count below floor, disclosure census | 1h | — |
| 4 | Write up; extend `projects.yaml`; log D-NNN | 1h | — |

**No variance-table row is written or promoted at any stage.** The sweep consumes
published registry arithmetic; it does not consume LoAM's variance components.
Those enter at part 2 (§6), which is out of scope here.
