# Phase 5 — the inverted audit, implemented. First run.

**Code exists now.** `src/loam/student_t.py`, `src/loam/inverted_audit.py`,
`scripts/run_inverted_audit.py`, and `tests/test_student_t.py` +
`tests/test_inverted_audit.py` (72 tests between the two). Read this document before quoting
any number out of it — every figure below carries a caveat that changes what
it licenses claiming, and the caveats are not decoration.

Built against [`phase5_inverted_audit_design.md`](phase5_inverted_audit_design.md)
and [`inverted_audit_redteam.md`](inverted_audit_redteam.md), with the design
doc's own §10 decisions resolved and the red team's required changes applied
— see **DECISIONS.md D-059 through D-063** for the reasoning behind each
choice below. Run it yourself: `python scripts/run_inverted_audit.py`.

---

## The one-paragraph version

Of the seven projects in the registry corpus, **one — VCS 4022, AgreenaCarbon
— currently discloses enough (area, a claimed rate, an interval) to run the
audit at all.** Under this table's most generous noise assumptions, its claim
turns out to be **cheaply detectable**: the audit's own cost-optimal design
needs about 161 sampling locations against a project that runs 12,616 fields
over 479,834 ha, costing roughly **$8,050** against revenue of **2.7 million
tCO2e** over the same interval — a break-even carbon price of about
**$0.003/tCO2e**, several orders of magnitude below any real carbon price.
**This is not the "undetectable claim" headline the design doc anticipated,
and that is itself informative**: the one project with enough disclosure to
check turns out to look fine on this dimension. The other six projects cannot
be checked at all, for the same reason D-056 already found at the
sampling-design level — the inputs simply are not public.

---

## What actually ran, and on what

| project | registry | result |
|---|---|---|
| VCS 4022 (AgreenaCarbon) | Verra | **auditable** — see below |
| CAR1459 (Indigo US-1) | Climate Action Reserve | not_auditable: area is disclosed (100,371 acres), but neither `credits_issued` nor `claimed_abatement`/a claimed rate is — see [`registry_corpus.md`](registry_corpus.md) |
| CAR1513 (AgriCapture rice) | Climate Action Reserve | not_auditable: SOC pool not separable from a rice-methane ledger (red team A-3) |
| ERF108333 / 105067 / 104527 / 176354 | Australian ACCU | not_auditable: no area field exists in the public register at all |

**1 of 7.** This mirrors, at the audit's own input requirements (area +
claimed rate + interval), the disclosure gap D-056 already found at the
sampling-design level: the corpus was never a representative sample (it was
picked to span the disclosure range), so this is not "1/7 of registered
projects are auditable" — it is "the one project picked for being
well-documented is the one project this can run on."

---

## VCS 4022, in full

**Inputs.** Area 479,834.11 ha (stated). Claimed abatement 543,369.95
tCO2e/y (stated) → derived SOC rate **≈0.309 Mg C/ha/y**. Remeasurement
interval 5 years (inferred from VM0042's own QA1 requirement, not
project-stated). Derived **Δ = 1.544 Mg C/ha** over the interval —
understood as the *net credited* rate, smaller than the true SOC claim
(Objection 3), which makes required-n larger than it should be, i.e. the
error runs in the conservative direction this audit needs.

**Components used** (low-envelope corner bound, §2.4 — see caveat below):

| component | value | source |
|---|---|---|
| between-plot | 3.14% | `VC-BPS-007`, the one genuine 0–30 cm between-plot row (D-060) |
| within-plot | 8.0% | D-043's indirect estimate — no table row exists at this depth (G2) |
| analytical | 1.25% | `VC-ANA-001`, harmonised (not the design doc's own loose "1.0%" — see below) |
| temporal | 2.71% | `VC-TMP-003` |
| relocation | 9.4% | `VC-REL-001`, **undivided** — a correction to the design doc's own worked example (D-061) |

**Headline design: UNPAIRED, not paired.** This is the single most
consequential implementation finding: the design doc's Sec 2.2 argues paired
revisits are always cheaper because between-plot variance dominates
relocation error. Checked directly against this table's own resolved inputs,
it is the other way round — between-plot (3.14%) is *smaller* than
relocation (9.4%) — so unpaired comes out cheaper. The headline is now
chosen per project by comparing `Cost*(paired)` against `Cost*(unpaired)`,
the same infimum-over-admissible-designs logic §2.3 already applies to the
number of cores per assay, rather than fixed to "paired" by fiat. See D-060.

**Cost-optimal design:** 2 cores per assay, **161 locations**, **$8,050**.
The full 1–30 core frontier is flat past about 10 cores (`data/processed/
inverted_audit.json`), matching §2.3's own prediction.

**Break-even carbon price: $0.0030/tCO2e.** Detecting this claim would have
cost more than the credits were worth only below three-tenths of a cent per
tCO2e — a price nobody trades at. **Break-even noise scale: 30.6×** — the
noise would have to be over thirty times larger than this table's already-
generous estimate, at CAR1459's own disclosed density applied to this
project's area, before the claim stopped being resolvable.

**Implied vs. applied uncertainty deduction (the B-1 headline metric):**
at the audit's own cost-optimal design, VM0042's own rule (`k=0.4307`)
implies an uncertainty deduction of **13.2%**. VCS 4022 actually applied
**31.35%** (stated, corrective-action-logged in its validation report).
**13.2% is the right order of magnitude, not the right number, and that is
expected**: this audit computes a *sampling-only* figure, while VCS 4022 is a
QA1 measure-and-model project whose applied deduction folds in model
prediction uncertainty too (Objection 1) — so 31.35% > 13.2% is internally
consistent, not a red flag. **A caveat that changes how much weight this
comparison can bear:** VCS 4022 applied VM0042 **v2.0**; the 0.4307 figure is
verified only in **v2.2** (D-057) and is absent from the v2.0 text held. The
comparison uses v2.2's rule as the best available figure, not a confirmed
one for this project's actual crediting.

**Support-scale mismatch (red team A-1): ~25 million-fold.** Every
between-plot input this table can supply is measured on research-plot
support (`VC-BPS-007`'s own stated plots are 3.6 × 53 m, about 0.019 ha).
VCS 4022 quantifies at whole-project support, 479,834 ha. That ratio is
**~25,148,538**, many orders of magnitude past even a generous reading of
red team A-1's "order of magnitude" refusal threshold. This module does not
gate on it — refusing to run at that threshold would mean the audit could
never run on any real commercial project, which is itself the finding, not
something this module should decide unilaterally — but it is reported on
every result and tracked as a new open gap, **G9**. **Every number above
should be read with this caveat attached**: it is a statement about
detectability at research-plot support, extrapolated to whole-project
support with no validated upscaling relationship, in either direction.

---

## Corrections this implementation makes to the design doc, disclosed rather than silently applied

Both of these were caught by writing tests that checked the design doc's own
stated claims directly, rather than by inspection — the same discipline the
red team's own C-3 finding came from, one level further into the code.

1. **`VC-ANA-001` enters at 1.25%, not the design doc's own quoted "1.0%".**
   1.0% is the row's raw MAPE (`value`); 1.25% is the harmonised,
   dimensionally-correct CV (`mae_to_sd_gaussian`, `SD = MAE × sqrt(π/2)`).
   Summing a raw MAE alongside true CVs in a variance budget would not be
   dimensionally sound. Small effect (a 1.25 percentage-point term inside a
   sum of squares that variance-dominates elsewhere) but worth recording as
   exactly the kind of small transcription slip this project's whole
   apparatus (D-051, the quantity-definition guard) exists to catch.

2. **`VC-REL-001` enters undivided (9.4%), not the design doc's own
   illustrative "~6.65% per observation".** The row's own harmonization note
   defines the source statistic as the mean of
   `|SOC_initial - SOC_resampled|` — already the SD of a *one-time* mismatch
   between the true original point and the actual, imperfectly-relocated
   revisit point. That is exactly what the paired formula's un-doubled
   `sigma_R` term represents structurally (within-plot/analytical/temporal
   error occur independently at both t0 and t1, hence doubled; relocation
   error is a single structural offset, not a second independent draw). This
   is the change that, combined with #3 below, flips the paired/unpaired
   ordering. A `relocation_scale="per_observation_sqrt2"` code path
   reproduces the design doc's own convention for direct comparison.

3. **Between-plot input is the narrow, in-depth-scope Wuest row
   (`VC-BPS-007`, 3.1%), not the broader NAPESHM row the design doc's own
   illustration implicitly leaned on (`VC-BPS-006`, 9.6–11.5%).**
   `VC-BPS-006` is 0–15 cm, and D-026 forbids rescaling it to the project's
   0–30 cm scope. This is D-a's resolution, not a new correction, but it
   compounds with #2 to move the paired/unpaired ordering.

The design doc is left standing, uncorrected in place, per the same
convention already used at its own top for the C-3/B-1 corrections — this
document and DECISIONS.md D-059–D-063 are the record of what changed and why.

---

## What this run does *not* license claiming

* **Not a verdict on VCS 4022, or on Verra, or on carbon markets.** One
  project, checked under generous assumptions with a known, large,
  unresolved support-scale caveat (G9), coming out "cheaply detectable" is
  a data point, not a clearance.
* **Not a percentage of the corpus, or of the scheme.** 1/7 is a fact about
  this hand-picked, disclosure-spanning corpus, not a rate that generalises
  — the census figures in [`registry_corpus.md`](registry_corpus.md) are
  what generalise, and they still show 999/999 Australian soil carbon
  projects with no sampling-design field of any kind.
* **Not a claim about paired vs. unpaired sampling in general.** The
  ordering found here (unpaired cheaper) is a property of *this table's*
  currently-resolved between-plot and relocation inputs, both of which carry
  their own open caveats (G8's single-region between-plot evidence; D-054's
  still-open analytical-error question). A different resolution of either
  could flip it back.
* **Every figure inherits every detection limit behind its inputs**
  (Objection 6) — attached to every audit result as `detection_limits`: the
  ~6.4–7.6% analytical/inorganic-carbon null (D-055), the ~2/10 CV-point
  climate/texture invariance limits (D-040), and the fact that the
  within-plot input is not a measured quantity at all (G2).

## What would most change these numbers next

In priority order, matching what the numbers above are most sensitive to:

1. **G9 — a validated support-scale relationship** for between-plot variance
   from research-plot to commercial-field support. Nothing here bounds the
   direction, let alone the magnitude.
2. **D-054 closing** — which analytical-error figure is right. Currently
   non-blocking (the generous rule takes the narrower figure regardless),
   but it would stop being non-blocking the moment a different component
   becomes the binding one.
3. **A second, disclosed project.** One data point cannot be checked against
   itself; a second auditable project (or CAR1459's own `credits_issued`,
   which the corpus notes is retrievable but was not fetched this pass)
   would let the paired/unpaired finding and the implied-vs-applied
   comparison be checked against an independent case.
