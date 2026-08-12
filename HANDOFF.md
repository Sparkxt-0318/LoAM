# HANDOFF — overnight autonomous run, 2026-08-12

Written continuously. Newest task last. **Nothing merged. All PRs draft.**

## Branch stack, and why it is a stack

`origin/main` carries everything through PR #11. Every branch below is cut from
the previous one rather than from `main`, because each depends on the last
(D-057 needs the corpus; the design doc needs D-057). **Merge in the order
listed** and each PR's diff stays readable.

| # | branch | PR | contains |
|---|---|---|---|
| 1 | `claude/loam-d036-resolution-keieap` | **#13** | D-036 closed, D-054 opened, D-055 (inorganic carbon), correspondence dated |
| 2 | `claude/loam-registry-corpus` | **#14** | D-056, Phase 5 corpus, gap analysis |
| 3 | `claude/loam-vm0042-primary` | **#15** | D-057, VM0042 read from primary |
| 4 | `claude/loam-inverted-audit-design` | **#16** | Phase 5 inverted-audit design doc |
| 5 | `claude/loam-estimator-repair` | **#17** | D-058, estimator repair |

## ⚠️ PR #12 must be resolved BEFORE any of the above

PR #12 reverts the D-053/G3 work: it deletes `docs/g3_bounding.md`,
`scripts/g3_bounding.py`, removes D-053 from `DECISIONS.md` and from
`DECIDED_DECISIONS`, and restores the older G3 gap-row text. Its base is
`0ba64fa`, **three merges behind `origin/main`**.

Every branch above references D-053 — D-054's gating text, the G3 gap row,
D-056, D-057, D-058. If #12 merges, those become dangling references.

**Recommendation: close #12 without merging.** Two reasons.
1. What #12 appears to object to is already what D-053 *says*. D-053's own
   recommendation is "retire the flat 'add cores' claim"; it is a bounding
   analysis, not a claim.
2. **The registry corpus has since corroborated it.** CAR1459 collects **one core
   per assay**, uncomposited, at continental scale — against Potash's 4 and
   D-053's computed optimum of 1.2–3.3. Reverting D-053 would delete the analysis
   the real world just agreed with.

If the intent is to soften D-053, that is an amendment to D-053, not deletion of
the script and the doc.

---

## TASK 1 — ESTIMATOR REPAIR — **COMPLETE** (~1h of a 2h box)
Branch `claude/loam-estimator-repair` · **D-058** · `176 passed`

**New module `src/loam/logvar.py`** — debiased, information-weighted
log-variance estimation. `psi` and `psi'` in **exact closed form** (nu is always
an integer, so nu/2 is an integer or half-integer), keeping `src/loam`
standard-library only so the guard runs in CI. Verified against scipy to
**1.8e-15** across nu = 1..101, against both recurrences, and by seeded Monte
Carlo.

**D-040's joint model repaired and re-run. The conclusion HOLDS.**

| | retired spec | repaired |
|---|---|---|
| treatments / sites | 80 / 19 | **135 / 26** |
| country split | 75 USA / 5 Mexico | **75 USA / 60 Mexico** |
| `log_mean_soc` | +0.423 (t=+2.25) | +0.801 (t=+2.37) |
| `sand_frac` | +0.915 (t=+2.25) | +1.720 (t=+3.06) |
| R² | 0.0935 | **0.0722** |

Covariates explain **less** under the correct estimator. Invariance unchanged.
D-029's log-log slope reproduces at **1.223**.

**The brief's reasoning is backwards, and checking it mattered.** Excess noise
*inflates* SEs and *depresses* R², both of which favour a null — so a noisy
estimator makes a null **easier** to reach, not harder. Correcting it is a test
D-040 could have failed. It passed.

**A D-040 caveat is retired and replaced.** "75 of 80 treatments from the USA" is
no longer true of the repaired fit (75/60). It is replaced, not removed: the
re-admitted Mexican treatments are exactly the 2-replicate ones, and `sand_frac`
nearly doubles when they enter — which is what a country effect wearing a texture
hat looks like. D-040 check 1c's prohibition stands.

**Precision on the instability.** The `t = -0.37, +4.58, -4.53, +0.75` sequence is
the **inorganic-carbon** coefficient across D-055's four tiers, not a coefficient
D-040 reported. On D-040's own covariates the retired spec is comparatively well
behaved. **D-040's published numbers were never the ones flipping.**

**Guard:** `tests/test_logvar_estimator.py` fails if the retired idiom returns
outside a two-file allowlist, and a second test requires allowlisted files to
label it `RETIRED`. **That second test caught a real gap on its first run.**

**Repo audit:** `ic_conditioning.py` re-routed through the shared module;
`derive_temporal.py` examined and is **not** the same failure mode (nu ≈ 29 per
plot, roughly equal, consumed by rank tests). `d029_raw_slope` deliberately left
alone — different estimator, different purpose, and D-029 rests on it.
**Recommendation: leave it; debiasing it re-opens D-029.**


## TASK 2 — RETIRE DELIVERABLE 3 — **COMPLETE** (~40min of a 1.5h box)
Branch `claude/loam-invariance-finding` · `176 passed` · no new D-NNN (PI decision, implemented)

**`docs/invariance_finding.md`** states the positive claim:

> We searched for spatial structure in monitoring noise across climate, texture
> and soil chemistry, each time against a stated detection limit, and found none.
> A single set of variance components serves temperate cropland. **MDC varies
> with DESIGN and INTERVAL, not with PLACE.**

Four nulls, each with its limit stated:

| axis | result | limit |
|---|---|---|
| climate (D-040) | 0.300 / 0.152 shifts vs CI widths 3.97 / 3.52, **opposite directions** | ~±2 CV pts |
| texture (D-040) | spreads 2.611 / 3.690 vs widest-bin CIs 11.016 / 10.464 | ~10 CV pts |
| joint model (D-058) | weighted **R² = 0.0722** | — |
| inorganic carbon (D-055) | 8 of 9 intervals contain their reference | **~6.4–7.6%** analytical error |

**Argued as a stronger product than a map**, on four counts — distributable,
checkable by anyone with their own data, cannot manufacture structure from
non-predictive covariates, and invariance is the harder claim to make.

**New repo-wide standard adopted: *a null is only informative against a stated
detection limit.*** Three existing instances named as the template.

**What would overturn it, concretely.** The carbonate channel is cheapest and
needs **lab duplicates, not a field campaign** — a few hundred split samples
spanning 0 to >2% inorganic carbon would reach the untested lower two-thirds of
Potash's 1–10% range. Nobody has to dig anything.

**Why this matters for Phase 5:** invariance is what makes the inverted audit
tractable. If σ varied by location, auditing 999 ACCU projects would need a
per-project variance estimate nobody can supply.

Updated: `docs/phase0_summary.md` Finding 3 (rewritten), `docs/phase1_design.md`
and `scripts/derive_g1_napeshm.py` (annotated where they still promised the
surface).


## TASK 3 — ADVERSARIAL REVIEW OF THE INVERTED AUDIT — **COMPLETE**
Branch `claude/loam-inverted-audit-redteam` · `docs/inverted_audit_redteam.md` · no implementation

The design doc from this session's item 3 exists on `claude/loam-inverted-audit-design`
(PR #16), so the task ran rather than being skipped.

**REQUIRED CHECK — does the design commit to the LOW END of the variance
envelope? YES, explicitly.** §2.4 states it as a hard rule with the exact
`bias_direction` mapping (`inflates`→`value_low`, `deflates`→`value`), worked
consequences (`VC-BPS-006` enters at 9.6%, not 11.5%), and the required headline
form. A central-estimate run is required as a sensitivity and **forbidden as the
headline**. No flag needed — but see C-2 below, which shows the rule is not the
probabilistic statement its wording implies.

### Two objections that land hard

**B-1 is FATAL to the current framing, and it is the best objection in the
review.** VM0042's Equation (2) is optional *by design*: the protocol regulates
precision through the **uncertainty deduction**, not through a minimum sample
size. Sample less, get fewer credits. That is outcome-based regulation and
arguably better than a minimum-n rule. The audit currently takes an optional
planning aid, declares it mandatory, and calls the gap a scandal — **a registry
would win that exchange in public.**

*The fix makes the method better:* **stop computing required-`n`; compute the
implied uncertainty deduction and compare it with the one actually applied.**
It uses the registry's own instrument on the registry's own terms, and it is
**checkable today** against VCS 4022's published **31.35%** — no waiting on the
§10 blockers.

**C-3 falsifies a prescription in the doc, and I verified it numerically.** §2.1
says the fixed point "converges in a handful of iterations". The map is
*decreasing* in `n`, and naive iteration **cycles**: at σ=3, Δ=3 it oscillates
12.71 / 12.50 / 12.71 / 12.50 forever, while bisection returns n\*=13 cleanly. It
cycles at **small n — exactly the regime the audit cares about.** Use bisection.

### Two objections that improve the deliverable rather than defending it

- **A-2 — report the break-even σ**, not just the break-even price. The developer
  must then assert a variance for their own soil and defend it, which they
  usually cannot, because they never published their pre-sampling variance
  either.
- **B-2 — report the stratification efficiency** that would be needed to bring
  the claim inside reach. Another quantity nobody published.

Both push the burden one level deeper onto undisclosed quantities, which is the
inverted audit's own logic applied recursively.

### Everything else

10 objections across three adversaries, each stated at its strongest, judged, and
given a fix. Ten prioritised changes listed at the end of the document. **Nothing
implemented.**

**Nothing here touches the corpus finding.** These are objections to the audit,
not to the observation that 999 of 999 Australian soil carbon projects publish no
sampling design.


## TASK 4 — VM0042 PRIMARY RETRIEVAL — **COMPLETE, EARLY**
Branch `claude/loam-vm0042-primary` · **PR #15** · **D-057**

Done during item 2b of the evening session rather than in the overnight box,
because item 2b required correcting every `0.43` against the primary source and
that is the same job. Recorded here so the overnight task list is not left
looking unfinished.

**The result reverses the premise of the task.** The task was written on the
assumption that the 0.43 figure was misattributed. **It was not.**

> VM0042 v2.2 §8.6.4, Equation 74: `t0.667` = *"t-value for a one-sided student's
> t-distribution at 0.667 (66.7%) confidence interval … **Equal to approximately
> 0.4307 at large sample sizes**"*, crediting at the **33.3rd percentile**.

`z(2/3)` = 0.4307 to four places. **The attribution to VM0042 was right all
along; what was missing was a primary check, and no misattribution decision was
needed or logged.**

**Three amendments that do matter:**

1. **It is a *t*-value, not a constant.** 0.4307 is the large-sample limit, so a
   project with fewer samples takes a *larger* percentage haircut. **The
   deduction is a function of the design** — which couples it directly to the
   inverted audit's unknown.
2. **The "v2.0" qualifier is withdrawn.** 0.4307 is absent from the v2.0 document
   held (a tracked-changes redline carrying a 15%-threshold rule in one layer and
   a two-pathway rule in another). **VCS 4022 applied v2.0**, so its 31.35%
   deduction must not be described as a 0.43-SE deduction.
3. **A correction to my own earlier claim** that VM0042 and CAR SEP are
   "different constructs". Same construct, different severity:

| protocol | multiplies | effective `k` (relative SE) | credits at |
|---|---|---|---|
| ACCU | SE | **0.253** | 40th pct |
| VM0042 v2.2 | relative SE | **0.431** | 33.3rd pct |
| CAR SEP v1.1 | **1.96 × SE** | **1.028** | 15.2nd pct |

**CAR SEP is 2.38× VM0042 and 4.06× the ACCU rule on identical measured
variance.** The same soil, design and variance produce a fourfold different
haircut depending only on the registry. That is a Phase 5 finding in its own
right.

**And the find that reshaped item 3:** §8.2.1 item 11 Equation (2) is
`n ≥ (S(t_α+t_β)/MDD)²` — **the inverted audit's own equation** — followed by
*"However, projects are not required to take this number of samples."*

Also recovered as primary: ESM is **required** (≥2 increments at re-sampling,
≥30 cm, **von Haden 2020's R script** an accepted tool — our own component-6
source), 5-yearly remeasurement, ≥3 control sites and ≥1 per stratum, stratified
random sampling mandatory, and the laboratory analytical-error definition
("repeated analyses of the same sample" = Poeplau's narrow figure), **logged into
D-054 as evidence without closing it**, per instruction.

**Access-log correction, contradicting last session's entry.** Verra was logged
as an access wall. That holds for **`registry.verra.org`** (the project registry
SPA) but **not** for the **`verra.org` methodology library**, which served both
PDFs on the first attempt. The two were conflated.

---

# END OF RUN

| task | branch | PR | status |
|---|---|---|---|
| item 2 · housekeeping + VM0042 | `claude/loam-vm0042-primary` | **#15** | complete |
| item 3 · inverted audit design | `claude/loam-inverted-audit-design` | **#16** | complete, design only |
| 1 · estimator repair | `claude/loam-estimator-repair` | **#17** | complete |
| 2 · retire Deliverable 3 | `claude/loam-invariance-finding` | **#18** | complete |
| 3 · inverted audit red team | `claude/loam-inverted-audit-redteam` | **#19** | complete |
| 4 · VM0042 primary | (folded into #15) | **#15** | complete, early |

**Nothing merged. All PRs draft. No D-NNN closed that needed judgement. No row
written or promoted. No implementation built ahead of a decision.**

Decisions logged this run: **D-057** (VM0042 primary), **D-058** (estimator
repair). **D-054 stays open** with new evidence attached, per instruction.

## Blockers hit, with evidence

| blocker | evidence | attempts |
|---|---|---|
| `registry.verra.org` project registry | Angular SPA shell on 4 endpoints | 2 (logged last session) |
| CAR registry pagination | CSRF-bound POST; 302 on page 2, 411 on CSV export | 2 (logged last session) |
| approved VM0042 **v2.0** (not the public-comment draft) | the held v2.0 is a tracked-changes redline; 0.4307 absent | 1 — **worth one more try**, it settles whether VCS 4022's 31.35% is a 0.43-SE deduction |

## Decisions I did NOT make, with recommendations

1. **PR #12.** *Recommend: close without merging.* Reasoning at the top of this
   file. Short version — what it objects to is already what D-053 says, and
   CAR1459's one-core-per-assay has since corroborated D-053 against Potash's 4.
2. **D-054** — which lab error `analytical` carries. Held open per instruction.
   New evidence for the against-side from VM0042 (D-057). Note the low-envelope
   rule in the audit design would take the narrower figure anyway, so this is
   **non-blocking for Phase 5** — but it still gates G3.
3. **The design doc's six §10 decisions**, chief among them **D-a**: there is no
   0–30 cm within-plot spatial row (G2), and within-plot variance governs the
   whole compositing dimension. *Recommend:* use D-043's indirect 8–9%, with the
   caveat stated. The alternative — bound `C ∈ [1,4]` and report the envelope —
   needs no new assumption and is weaker.
4. **`d029_raw_slope`** left unweighted deliberately (D-058). *Recommend: leave
   it.* Debiasing it re-opens D-029.
5. **Whether to restructure the audit around the implied-vs-applied deduction**
   (red team B-1). *Recommend: yes.* It defeats the strongest objection, and it
   is checkable today against VCS 4022's 31.35% without waiting on D-a.

## Things that contradict a standing assumption

1. **The 0.43 figure was never misattributed** — only unverified. The task was
   written expecting a misattribution finding; the primary says otherwise.
2. **Verra's methodology library is not blocked.** Only the project registry is.
   Last session's log conflated them. **Fourth time an "unreachable" item turned
   out to be reachable** (after Potash, Wuest's dataset, and von Haden).
3. **VM0042 contains the inverted audit's own equation and declines to require
   it.** The method is the protocol's, not ours.
4. **The brief's reasoning about noise and nulls is backwards.** Excess noise
   inflates SEs *and* depresses R², both of which favour a null — so a noisy
   estimator makes a null *easier* to reach. Correcting it was a test D-040 could
   have failed.
5. **D-040's "75 of 80 from the USA" caveat no longer applies** to the repaired
   joint model (75 USA / 60 Mexico). Replaced, not removed.
6. **My own design doc prescribes an algorithm that does not terminate** at small
   `n` (red team C-3, verified). Fixed-point iteration cycles; use bisection.

## What I would do next, in priority order

1. **Resolve PR #12**, then merge #13 → #19 in stack order.
2. **Restructure the audit design around implied-vs-applied deduction** (B-1),
   and fix the iteration to bisection (C-3). Both are cheap.
3. **Validate against VCS 4022's 31.35%** — the one thing testable today.
4. **Decide D-a** (the 0–30 cm within-plot gap). Everything in Phase 5 waits on it.
5. **One more attempt at the approved VM0042 v2.0.**
6. **Reply to Potash** — the IC result is a bounded null and he asked to hear
   either way. `docs/ic_conditioning.md` is written to be quotable.
