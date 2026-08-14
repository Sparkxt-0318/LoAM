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

> **THE THRESHOLD IS SETTLED, AND IT IS NOT OURS (D-061, 2026-08-13).**
> *VCS Methodology Requirements* §2.4 ends: "*Where the half-width of the
> two-sided 90 percent confidence interval exceeds **100 percent** of the
> reduction and removal estimate, **the project is not eligible for
> crediting**.*" Since the 90% half-width is `1.6449·SE`, that is
> `σ_rel > 60.79%`, i.e. **`UNC > 26.18%`**. The sweep runs at that single line —
> Verra's own, with no power convention chosen by us. The power-based rows below
> are kept for orientation only.

| rule | claim = MDD at 50% power | claim = MDD at 80% power |
|---|---:|---:|
| VM0042 **all versions** | UNC > **21.97%** | UNC > **15.37%** |
| CAR SEP v1.1 | UNC > **52.4%** | UNC > **36.7%** |
| ACCU / ACCM | UNC > **12.9%** | UNC > **9.0%** |

The VCS bar sits at `Δ/MDD = 0.839`: **Verra permits crediting claims down to
84% of their own 50%-power minimum detectable difference.** That relationship —
not a LoAM threshold — is the publishable form of the detectability argument.

**And `k = 0.4307` is a VCS program-wide constant, not a VM0042 one.** MR §2.4
defines `Discount = (Uncertainty / t_{α=10%}) × t_{α=66.6%}` with `1.6449` and
`0.4307`, which reduces to `0.4307·σ_rel`. Every VCS methodology implementing
§2.4 inverts identically, so the population is wider than VM0042.

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
| ~~0b~~ | ~~Confirm 31.35% is the SOC deduction~~ **ATTEMPTED — D-061, NOT CONFIRMED.** PD not public; validation report calls it "the final uncertainty deduction", project-level, undisaggregated | — | `Δ/MDD` stays conditional; the §2.4 comparison does not depend on it |
| ~~0c~~ | ~~Is there a cap?~~ **COMPLETE — D-061. No cap** at methodology or program level; **an eligibility bar instead**, `UNC > 26.18%` | — | cap sweep **deleted** |
| **1** | **Enumerate VM0042 projects — BLOCKED.** `registry.verra.org` returns the SPA shell on every route, GET and POST (3 further attempts, D-061). Web search surfaces no other project's deduction | — | **population reachable = 1. Stopped and reported, per the stop condition** |
| 2 | Per project: UNC → eligibility test at 26.18%, `Δ/MDD` beside it | ~10 min each | — |
| 3 | Distribution, count over the bar, disclosure census | 1h | — |
| 4 | Write up; extend `projects.yaml`; log D-NNN | 1h | — |

**Stage 1 is the only thing left, and it is the thing that was flagged as the
sweep's sole real risk from the start.** Everything downstream is settled: one
constant, one threshold, one published number per project.

---

## 10. Retrieval decision log (D-062, 2026-08-13)

Written so a reviewer asking *how was this corpus assembled?* can answer it
without reconstructing anything.

### 10.1 What was authorised, and the limits applied

A headless browser was authorised by the PI for **`registry.verra.org` project
pages only**, under stated constraints, all of which were applied:

| constraint | how it was honoured |
|---|---|
| Check `robots.txt` first; stop if it disallows | Checked before any browser launch. See §10.2 — including a finding that cuts against us. |
| Several seconds between requests, no parallelism | 4–6 s waits, single page object, sequential. Never exceeded 3 navigations in a run. |
| No authentication, login walls or paywalls | No credentials held, none supplied, none attempted. The probe was written to abort on a login wall; it never got far enough to test one. |
| Two rounds max, do not raise the cap | Two rounds used (§10.3). Stopped. Cap not raised. |

### 10.2 `robots.txt` — two results, one of which is against us

**`registry.verra.org/robots.txt`** returns the SPA catch-all: HTTP 200,
`content-type: text/html`, the same 2,598-byte `index.html` served for every
path. **No robots.txt is served, and no parseable directive exists** — under the
Robots Exclusion Protocol, content that yields no valid rules is not a
disallow. The authorised target paths are therefore **not disallowed**.

**`verra.org/robots.txt`**, however, *does* serve directives, and they matter:

```
User-agent: *
Disallow:/wp-content/uploads
```

**Every primary document in this project's evidence base sits under
`/wp-content/uploads`** — VM0042 v2.0/v2.1/v2.2/greenlined, the Corrections &
Clarifications, the v3.0 consultation drafts, the *Methodology Requirements*
v4.4, and Verra's worked uncertainty example.

Stated plainly rather than argued away:

- **What the directive addresses.** The Robots Exclusion Protocol governs
  automated *crawling* — discovery and traversal. These were individual,
  PI-directed retrievals of specific documents, each linked publicly from
  Verra's own methodology pages, fetched once and cached locally. No crawl, no
  traversal, no index, no bulk enumeration of that path.
- **What is nonetheless true.** The directive exists, it is unqualified, and a
  reviewer is entitled to know that the documents underpinning every finding in
  this project were retrieved from a path Verra's `robots.txt` asks automated
  agents not to fetch.
- **What it does not affect.** Document *content*. Eq. (65), `0.4307`, and the
  §2.4 eligibility bar say what they say; they are also obtainable by hand from
  a browser, and the locators in this repo let any reader verify them
  independently.
- **Standing rule adopted here.** No automated or bulk retrieval under
  `verra.org/wp-content/uploads`. Documents already held are retained and cited.
  **Any future bulk fetch from that path is a PI decision, not an agent
  decision**, and is flagged as an open question rather than assumed.

### 10.3 Why rendering a public project page is not circumvention

Recorded because the question is legitimate and should not be left implicit.

`registry.verra.org` project detail pages are **published, unauthenticated, and
intended for public reading** — Verra links them from its own site and from
press material, and each is the canonical public record of a registered project.
The obstacle is not a control that withholds them; it is that the pages are
**client-rendered**, so an HTTP client receives the application shell rather than
the content a human reader sees.

Running the page's own JavaScript reproduces exactly what an ordinary visitor
receives. It does not defeat authentication, does not evade a paywall, does not
use credentials, does not exploit a flaw, and does not reach anything a member
of the public cannot read by opening the same URL. **What it changes is
throughput, not entitlement** — which is why the rate limit, the sequencing and
the two-round cap were imposed as conditions rather than treated as optional.

Had a login wall, a paywall or a terms gate appeared, the constraint was to
stop. That remains the rule if this is attempted from another environment.

### 10.4 What actually happened — and it was not Verra

**The browser could not be made to work in this container, for reasons that have
nothing to do with Verra.**

The egress proxy accepts only `CONNECT` tunnels. Chromium's navigations were
reset at the network layer for **every** host tried, including
`https://example.com/`:

```
net::ERR_CONNECTION_RESET   https://example.com/
net::ERR_CONNECTION_RESET   https://verra.org/
net::ERR_CONNECTION_RESET   https://registry.verra.org/app/projectDetail/VCS/4022
```

Round 1: default launch, then explicit `proxy=` configuration. Round 2: explicit
`--proxy-server`, `--proxy-bypass-list=<-loopback>`, QUIC disabled, background
networking and component updates disabled, certificate errors ignored. Identical
reset each time. The proxy's own failure log records only Chromium's plain-HTTP
telemetry to `clients2.google.com` being refused for being non-`CONNECT` — the
HTTPS navigations do not appear in it at all.

`curl` reaches the same hosts from the same shell without difficulty. **The
limitation is this environment's browser egress, not the target.**

### 10.5 The three-way distinction — do not merge these

The corpus has now met three different failure modes, and collapsing them into a
single "we couldn't get the data" number would destroy the finding:

| | mode | example | what it evidences |
|---|---|---|---|
| 1 | **Disclosure gap** | ACCU register: 999 soil projects, **no field of any kind** for sample count, depth, cores per composite, density or interval; `Estimation or measurement approach` populated for 24/999 | About the **registry**. Complete-population evidence — the strongest kind, because nothing is missing from it. |
| 2 | **Access wall** | `registry.verra.org` serves a client-rendered shell; no systematic read without executing the page | About the **delivery mechanism**. The data is public but not auditable at population scale. |
| 3 | **Environment limitation** | Chromium cannot reach *any* host from this container | About **us**. Carries no information about Verra whatsoever. |

**(1) is a finding about disclosure. (2) is a finding about auditability.
(3) is not a finding about Verra at all**, and must never be reported as though
it were.

### 10.6 The finding that survives the failure

Recorded beside the ACCU census, and jointly stronger than either alone:

> **The two largest soil-carbon registries publish design and uncertainty data in
> forms that cannot be systematically audited — by complete-population evidence
> for one, and by access-wall evidence for the other.**
>
> ACCU: **999** soil projects, **zero** sampling-design fields. Verra: project
> records public and individually readable, but reachable only one client-
> rendered page at a time.
>
> Neither statement depends on a variance component, a detectability threshold,
> or anything LoAM computes.

**Population reachable in this environment: n = 1. No distribution is reported
and none was estimated.** The threshold (§2, `UNC > 26.18%`), the constant
(`k = 0.4307`) and the method are all settled and unaffected. Only the sample is
missing, and the sweep is now correctly a **second-order** question: the Phase 5
headline rests on `vcs_eligibility_bar.md`, which is complete at n = 1 plus a
program-level rule.

Stage 2 is now materially cheaper than scoped: no version determination, no case
determination, no pathway determination. One published number per project and one
constant.

**No variance-table row is written or promoted at any stage.** The sweep consumes
published registry arithmetic; it does not consume LoAM's variance components.
Those enter at part 2 (§6), which is out of scope here.
