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
MDD  =  (t_α + t_β) · SE(Δ)          VM0042 §8.2.1.3 Eq. (2), FAO 2019
```

Eliminating `SE(Δ)`:

> ### Δ / MDD = k / ((t_α + t_β) · UNC)

The project's own published deduction, divided by a constant that depends only on
which rule it was written under. **No design parameter, no variance estimate, no
disclosure beyond the deduction itself.**

### The four `k` values, all from primary sources

> **Corrected 2026-08-13 (D-060).** The v2.0 row below previously read `1.960`
> with a case/pathway split. That was wrong — see `vm0042_s2_verification.md`.
> VM0042 has had **one** uncertainty rule since v2.0, and the version dimension
> collapses out of the sweep.

| rule | `k` (multiplier on relative SE) | source |
|---|---:|---|
| VM0042 **v2.0**, Eq. 65 | **0.4307** | v2.0 §8.6.4, `t_{α=0.666}` (D-060) |
| VM0042 **v2.1** | **0.4307** | §8.6.4 (D-060) |
| VM0042 **v2.2**, Eq. 74 | **0.4307** | v2.2 §8.6.4, `t₀.₆₆₇` (D-057) |
| VM0042 **v3.0 draft** | **0.4307** | draft §8, 10 Feb 2026 (D-060) |
| CAR SEP v1.1 | **1.028** | `z(70%) × 95% half-width`, via CAR1459's monitoring plan (D-057) |
| ACCU / ACCM | **0.2533** | 60% exceedance (D-057) |

There are no VM0042 cases and no pathways. Any project under any version of
VM0042 inverts with the same constant, which removes the version-determination
step from the sweep's per-project work.

### The screening thresholds

Setting `Δ/MDD = 1` — the project claims exactly its own detection floor — gives
a published-deduction threshold per rule. **These are exact, and they are the
whole screen:**

| rule | claim = MDD at 50% power | claim = MDD at 80% power |
|---|---:|---:|
| VM0042 **all versions** | UNC > **21.97%** | UNC > **15.37%** |
| CAR SEP v1.1 | UNC > **52.4%** | UNC > **36.7%** |
| ACCU / ACCM | UNC > **12.9%** | UNC > **9.0%** |

> **Corrected 2026-08-13 (D-060).** The former first row (v2.0 case N3, 100.0% /
> 70.0%) is deleted, and with it the claim that VM0042's `MIN{100%, …}` cap marks
> the `Δ = MDD` line. **VM0042 Eq. 65/74 has no cap** — no `MIN`, no `MAX`, no
> threshold subtraction. The planned cap sweep has nothing to sweep for unless a
> cap is found in *VCS Methodology Requirements* §2.4, which §8.6.4 defers to and
> which has not been retrieved.

The 21.97% / 15.37% line is the whole VM0042 screen, and it applies to every
project under the methodology regardless of version or quantification approach.

---

## 3. Two findings already visible, before the sweep runs

Both fall out of §2 and should be verified early, because if they hold they may
outrank the sweep itself.

**(a) ~~VM0042 v2.0 is 4.54× more severe than v2.2~~ — VOID (D-060, verified
2026-08-13).**

The check was run. `s²` **is** the same object in both versions — same
definition, same §8.6 subsection tree, same upstream equations symbol-for-symbol
(v2.0 Eqs. 54/55 ≡ v2.2 Eqs. 63/64). But the premise failed: **v2.0's multiplier
is also 0.4307**, not 1.960. There is no ratio. See
`vm0042_s2_verification.md`.

What the check produced instead, on VCS 4022's published 31.35%:

| quantity | as recorded (D-059) | corrected |
|---|---:|---:|
| implied relative SE | 15.99% | **72.79%** |
| `Δ/MDD` at 50% power | 3.19 | **0.70** |
| `Δ/MDD` at 80% power | 2.23 | **0.49** |

The claimed change is **below** its own minimum detectable difference. Note that
§2's threshold table already said so — 31.35% > 21.97% — while §3a said the
opposite. That internal contradiction is what the check surfaced.

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
4. ~~**Verify §3a before or after the sweep?**~~ **DONE 2026-08-13 (D-060)** —
   verified first, per PI direction. Outcome in `vm0042_s2_verification.md`: `s²`
   is identical across versions, but the v2.0 rule was misrecorded and §3a is
   void. This was the right call: the sweep would have run with `k = 1.960` on
   every pre-October-2025 project and produced systematically wrong `Δ/MDD`.
5. **How hard to push on Verra retrieval.** A headless browser would very likely
   work and was ruled out of scope last session. Two attempts then log, or
   authorise the browser? *Unchanged — still open, and now the only thing
   between the corrected identity and the distribution.*
6. **NEW — is 31.35% the Eq. 65 deduction for SOC?** The corrected `Δ/MDD = 0.70`
   depends on it. The PD and validation report are not in the container. Re-pull
   and confirm before the number leaves the repo.
7. **NEW — retrieve *VCS Methodology Requirements* §2.4.** VM0042 §8.6.4 defers
   to it. It is the only remaining place a cap on `UNC` could live, and the cap
   sweep depends entirely on whether one exists.

---

## 9. Staging and time box

| stage | work | box | stop condition |
|---|---|---|---|
| ~~0~~ | ~~Verify §3a~~ **COMPLETE — D-060**, `vm0042_s2_verification.md` | — | reported |
| 0b | Re-pull VCS 4022 PD; confirm 31.35% is the Eq. 65 SOC deduction | 30 min | if it is not, §7 of the verification record is withdrawn too |
| 0c | Retrieve *VCS Methodology Requirements* §2.4; is there a cap? | 30 min | no cap → cap sweep is deleted, not deferred |
| 1 | Enumerate VM0042 projects; count reached | 1.5h | < 10 projects → stop and report |
| 2 | Per project: UNC → `Δ/MDD` with `k = 0.4307` | ~15 min each | — |
| 3 | Distribution, count below floor, disclosure census | 1h | — |
| 4 | Write up; extend `projects.yaml`; log D-NNN | 1h | — |

Stage 2 is now materially cheaper than scoped: no version determination, no case
determination, no pathway determination. One published number per project and one
constant.

**No variance-table row is written or promoted at any stage.** The sweep consumes
published registry arithmetic; it does not consume LoAM's variance components.
Those enter at part 2 (§6), which is out of scope here.
