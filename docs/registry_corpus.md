# Phase 5 registry corpus — first pass, and the gap analysis

**What Phase 5 asks.** Take a registered soil carbon project, read its sampling
design, and compute whether that design could have detected the change the
project claimed. Eric Potash named this independently as the highest-impact
direction available to the testbed:

> "apply it post hoc to existing carbon projects. It would be interesting to
> know if existing projects collect sufficient samples to detect the differences
> they aim to."

**What this pass found.** For most registered soil carbon projects, **the audit
cannot be run at all** — not because the answer is uncomfortable, but because
the inputs are not published. That is the deliverable of this pass.

Data: `data/registry/projects.yaml`. Seven projects, three registries, plus one
complete registry census. Every field carries a source key, a locator and a
status. Access date throughout: 2026-08-12.

---

## The corpus

| project | registry | protocol | scope | disclosure |
|---|---|---|---|---|
| **CAR1459** Indigo U.S. Project No. 1 | Climate Action Reserve | SEP v1.1 | **in scope** — US cropland | **tier 1** — everything but the depth convention |
| **VCS 4022** AgreenaCarbon | Verra | VM0042 v2.0 | **in scope** — EU arable, 479,834 ha | **tier 2** — design exists, parameters in withheld appendices |
| **CAR1513** AgriCapture US Rice Methane | Climate Action Reserve | SEP v1.1 | out — rice methane, not SOC | **tier 3** — design deferred to a memo that is not public |
| **ERF108333** Bonnie Doone | Australian ACCU | 2021 measurement+models | out — grazing | **tier 4** — administrative record only |
| **ERF105067** Moora Plains | Australian ACCU | 2021 measurement+models | out — grazing | **tier 4** |
| **ERF104527** Cheyenne | Australian ACCU | 2021 measurement+models | out — grazing | **tier 4** |
| **ERF176354** Blewett 5 (AgriProve) | Australian ACCU | 2021 measurement+models | out — unconfirmed | **tier 4** |

Four of seven are out of LoAM's scope lock (SOC, cropland topsoil, temperate).
They are kept, not deleted — the same rule D-016 applies to variance-table rows
— because the gap analysis is about *disclosure*, and disclosure does not care
about our scope.

**The corpus is not a sample and no rate computed from it generalises.** It was
picked to span the disclosure range. The one thing here that *does* generalise
is the Australian census, because it is a complete count.

---

## Which fields could be populated, per project

Sixteen fields Phase 5 needs. ● stated · ◐ inferred by us · ✗ not disclosed ·
**⊘ withheld** (the public document names a document that holds the parameter,
and that document is not public).

| field | CAR1459 | VCS 4022 | CAR1513 | ACCU ×4 |
|---|---|---|---|---|
| registry, protocol, developer | ● | ● | ● | ● |
| geography | ● | ● | ● | ● |
| project area | ● | ● | ● | ✗ |
| practices claimed | ● | ● | ● | ● |
| quantification approach | ● | ● | ● | ✗ (1 of 4 ●) |
| model | ● | ● | ● | ✗ |
| sampling design (type) | ● | ● | ⊘ | ✗ |
| **number of samples** | ✗ | ⊘ | ⊘ | ✗ |
| **cores per composite** | **●** | ⊘ | ⊘ | ✗ |
| **sampling density** | ● | ◐ | ⊘ | ✗ |
| **sampling depth** | ● | ⊘ | ⊘ | ✗ |
| **depth increments** | ✗ | ⊘ | ⊘ | ✗ |
| **depth convention (fixed vs ESM)** | ✗ | ⊘ | ✗ | ✗ |
| **remeasurement interval** | ● | ◐ | ✗ | ✗ |
| stratification scheme | ● | ● | ● (rule only) | ✗ |
| uncertainty treatment | ● | ● | ◐ | ✗ |
| uncertainty deduction applied | ✗ | **● 31.35%** | ✗ | ✗ |
| claimed SOC change rate | ✗ | ● | ✗ | ✗ |
| credits issued | ✗ | — | ✗ | ● |

**One project of seven — CAR1459 — carries enough to attempt the audit**, and
even it is missing the depth convention.

---

## Gap 1 — the census. 999 Australian soil carbon projects publish no design at all

The Australian ACCU Scheme is the largest soil carbon crediting programme in
the world by project count. The register (CSV, as at 2026-06-30, 3025 rows) is
complete and machine-readable, so this is a census, not an estimate:

| | |
|---|---|
| registered soil carbon projects | **999** |
| of which have been issued credits | **53** |
| ACCUs issued to soil carbon projects | **439,348** |
| largest single project | **94,666 ACCUs** (ERF108333 Bonnie Doone) |

Field completeness across all 999:

| register field | populated |
|---|---|
| project name, method, activities, crediting period, ACCUs issued | **999/999 (100%)** |
| `Estimation or measurement approach or model` | **24/999 (2%)** |
| `Carbon Estimation Area mapping file URL` | 53/999 (5%) |
| `Model start date(s)` | **0/999 (0%)** |
| `Supplementary project information` | **0/999 (0%)** |

**And there is no field at all for sample count, sampling depth, cores per
composite, sampling density, depth convention or remeasurement interval.** Not
blank fields — no fields. The Clean Energy Regulator's own register page states
that project-level sampling plans and measurement reports are not published.

> **439,348 credits have been issued against soil carbon measurements whose
> sampling designs are not public, in any project, anywhere in the scheme.**

The scheme does require a sampling plan — the CER's *Sampling guidance for
measurement-based soil carbon methods* sets out how strata are defined, how
sampling locations are randomised, and how composites may be formed. The plan
must exist, must be lodged, and must not be varied. **It is simply never
published.** So the gap is not regulatory laxity about design; it is a
disclosure choice, and it is the one that blocks the audit.

## Gap 2 — `withheld`, not merely absent

Two projects name the document that holds their sampling design and do not
publish it. That is worth separating from ordinary silence, because it tells us
the number exists and someone reviewed it.

**CAR1513** — the 12-page monitoring plan says, twice:

> "See the CAR1513 V4 Soil Sampling Memo for additional consideration of
> stratification. … Location of evidence or documentation: CAR1513 V4 Soil
> Sampling Memo"

That memo is **not among the 41 public documents** for the project. Checked by
name and by pattern across every public document title.

**VCS 4022** — the validation report confirms in detail that the design was
reviewed:

> "Appendix 6: soil sampling protocol in the PD now include the description of
> sampling design, minimum data collection requirements of soil sample,
> measurement of SOC and bulk density along with statistical analysis approach
> adopted in this project."

The appendices are cited, found complete, and not reproduced. The monitored-
parameter table even lists **"N | Unitless | Number of cores"** — so the
parameter's *existence* is public and its *value* is not.

**A validation report that certifies a design without publishing it transfers
the whole verification to the validator.** That is a reasonable division of
labour for a registry. It makes independent post-hoc audit impossible.

## Gap 3 — the depth convention is missing everywhere, including tier 1

**Not one project in the corpus states whether it accounts on a fixed depth or
on an equivalent soil mass basis.** CAR1459's 102-page monitoring plan does not
contain the phrases "equivalent soil mass", "soil mass", "depth increment",
"fixed depth", "0–10" or "10–30" anywhere.

This is the one gap that changes a number rather than merely blocking a
calculation. LoAM's component 6 is the **best-constrained** in the whole
variance table:

- fixed depth understates stock change by **17%** (`VC-BDC-001`, Fowler 2023)
- conventions can **reverse the sign** of an estimate — **16.2%** (`VC-BDC-002`)
- von Haden et al. 2020 Table 1: mean absolute error in stock, **ESM 0.2–1.1%
  vs fixed depth 2.1–23.2%** under ±2.5 cm of compaction

So the single undisclosed parameter with the largest documented effect on a
credited quantity is the one that is undisclosed in **every project in the
corpus**. A Phase 5 audit that cannot read the depth convention has to run the
whole thing twice and report a bracket — which is a defensible output, and worth
saying out loud, because a project that never states its convention has no
standing to object to being audited under both.

## Gap 4 — VM0042 requires two depth increments; nobody publishes them

VM0042 requires sampling to a minimum of 30 cm and **at least two depth
increments, expressly to enable equivalent-soil-mass accounting**. VCS 4022
follows VM0042. Its increments are in Appendix 6 and are not public.

**A methodology requirement is not evidence of a project's practice**, and
nothing in `projects.yaml` records one as if it were. But it sharpens gap 3: the
methodology went to the trouble of requiring the thing that makes ESM possible,
and the registry does not publish whether it happened.

---

## What the one auditable project actually shows — and it is a direct hit on G3

CAR1459 is worth reading closely, because it answers a question LoAM has been
arguing about internally with no external data.

> **"At each carbon sampling location, an individual 30-cm sample was
> collected."** Carbon samples are **not composited**. One core, one assay, one
> point. Compositing is used only for pH and texture.

Set that against **D-053 / G3**, where we bounded the cores-per-plot question
and found that the budget-optimal composite from our variance structure is
**1.2–3.3 cores per assay**, against the **4** assumed by Potash et al. — a
disagreement we recorded and held loosely for want of a third opinion.

**Here is the third opinion, and it is at continental scale, from the most
completely documented soil carbon project on any registry: C = 1.**

That does not settle G3 — Indigo's design is not optimised for the same
objective, it interpolates bulk density rather than measuring it everywhere, and
one core per point at 1 point per 8 acres is a different object from one core
per experimental plot. But it moves the disagreement with Potash from
"ours versus theirs" to "ours and the largest real deployment on one side,
theirs on the other", and that is worth a sentence in any writeup.

Two more from CAR1459 that are hard to get anywhere else:

- **Sampling density: 1 point per 8 acres (3.24 ha)** — a real, disclosed, at-scale
  number to put beside our MDC curves.
- **Bulk density frequency was raised from 1-in-5 to 1-in-3 carbon points
  explicitly "to increase the precision of our estimates of SOC stock changes."**
  A design change made on variance grounds, documented as such, by a project
  developer. That is a natural validation target for the calculator: does our
  variance structure predict that the 1-in-3 change was worth its cost?

---

## Two access walls, which are NOT disclosure gaps and must not be counted as such

Logged per the two-attempts rule, and separated deliberately — conflating "we
could not fetch it" with "they did not publish it" would inflate the finding.

**Verra's registry was not machine-reachable from this environment.** Every path
tried — `/uiapi/resource/resourceSummary/search`, `/uiapi/resource/resource/search`,
`/uiapi/asset/asset/search`, `/app/projectDetail/VCS/<id>` — returns the Angular
single-page-application shell. The one Verra project here was reached through a
validation report mirrored on a third-party site. **Verra project design
documents are public in principle**, and a browser would very likely open them.
This is the same pattern that cost us three items already (Potash, Wuest's
dataset, Smith 2004 / Bradford 2023): an access wall wearing a paywall's coat.

**The Climate Action Reserve report paginates by CSRF-bound POST.** Page 1 (50
projects) was enumerated; a page-2 POST returned 302 and a CSV export returned
411. So only one Soil Enrichment project was found by enumeration (CAR1513);
CAR1459 was reached by direct ID. **No CAR-wide census appears in this file**,
and none should be inferred.

**One thing in the brief did not survive checking.** The brief describes VM0042
as using "0.43 SE". The rule verified here is the **CAR SEP** rule, which is
different: `UNC = z(70%) × (half-width of the 95% CI) / ER`, with z(70%) =
0.5244. The VM0042 uncertainty rule was **not** read from the methodology this
session and is not recorded. The two must not be quoted alongside each other
until it is.

---

## What this changes about Phase 5

**Phase 5 has a population problem before it has a method problem.** The design
assumed a corpus of projects whose designs could be read. On this evidence the
readable population is small, and it is not a random subset — it is the projects
whose developers chose to publish, which is plausibly the projects with the most
defensible designs. **Any Phase 5 result will be biased toward finding that
projects sample adequately**, and that caveat has to travel with the finding from
the start rather than be discovered at the end.

**Three ways forward, in the order they are worth doing.**

1. **Audit the disclosed projects properly and report the gap alongside.** "We
   could audit 1 of 7, and here is why" is a publishable result about MRV
   transparency in its own right — arguably a stronger one than the audit,
   because it does not depend on the audit's assumptions being accepted.
2. **Invert the question for the undisclosed majority.** For a project that
   published only its area, its practice and its credits, ask: *what sampling
   design would have been required for this claim to be detectable?* That needs
   no design disclosure at all — only area, claimed rate and interval, all of
   which the ACCU register does publish for 999 projects. It turns the gap from
   a blocker into the method. **This is the strongest idea to come out of this
   pass and it should be scoped next.**
3. **Get the Verra corpus.** It is public, it is in scope, and it is one browser
   session away. Highest value per minute of anything on this list.

**A note on tone for the writeup.** Nothing here is a case against any project.
CAR1459 discloses more than most published *papers* do, and it should be named
for that, not used as a foil. The finding is about what registries require to be
published, not about what developers are hiding — and the one lever that would
fix it is a registry field, not an accusation.
