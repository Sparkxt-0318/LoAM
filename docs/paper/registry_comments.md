# Drafts — registry comments (Verra VM0042)

**Status: DRAFTS for the PI. Nothing has been submitted.**

**What was checked (2026-11-10):**
- **No VM0042 v3 consultation is open.** Verra's revision page (Development ID **M0264**) gives
  the public consultation as **11 February – 31 March 2026**, now closed; its status field reads
  "5. Independent Expert Review". So §1 below cannot be filed as a consultation submission. It is
  drafted as unsolicited technical input to Verra's methodology team, citing M0264.
- **The v3 draft text has not been read.** It is hosted under `verra.org/wp-content/uploads`,
  which `verra.org/robots.txt` disallows, and fetching it is PI decision B. §1 therefore responds
  only to the revision *summary* on Verra's public page, and says so.
- **Projects currently in public comment could not be enumerated.** The Verra registry moved to a
  new platform and is not machine-readable from here (D-066). §2 is a per-project template, to be
  instantiated once the PI's registry export lands (`docs/registry_population.md` §3).

The fields proposed are the same in both. They are the smallest set that would let anyone run
VM0042's own Equation 2 against a project's own numbers.

---

## 1. To Verra — input on the major revision of VM0042 (M0264)

**To:** methodologies@verra.org — **Subject:** M0264 VM0042 v3.0: disclosure fields that would
make Equation 2 checkable

Dear Verra methodology team,

We write after the 11 February – 31 March 2026 consultation on VM0042 v3.0 closed, so this is
offered as input for the independent expert review stage, not as a consultation response. We
have read the revision summary on your M0264 page, not the draft text. If v3.0 already does what
we propose, please treat this as support.

**Our concern is narrow: what is published, not what is required.** VM0042 already contains the
right instrument. §8.2.1 item 11, Equations (1) and (2), give the minimum detectable difference
and the sample size that would detect it. The deduction rule (§8.6.4) then converts imprecision
into forgone credits. We studied every soil-carbon project for which public documents give an
area and a credited quantity: 54 Australian ACCU projects, one Climate Action Reserve project
and one VCS project. Three things follow, set out in a short preprint we will share:

1. **The inputs to Equation 2 are almost never public.**
   - Equation 2 needs S, the standard deviation of the stock change, and the realised n.
   - In the one VCS project we could read in detail (VCS 4022), the validation report confirms
     the sampling design was reviewed but cites it to PD appendices that are not public.
   - Its parameter table names "Number of cores" without a value.
   - The validation body recorded MDD, S, n and t as "not relevant and therefore not further
     assessed".
2. **A published deduction is informative only if it is pool-specific.**
   - Under §8.6.4 the deduction is k·SE/mean with k ≈ 0.4307. A published deduction therefore
     implies the project's own relative standard error, and with it the ratio of the claimed
     change to its own minimum detectable difference. This needs no outside data.
   - That inference is only valid if the published figure is the SOC-pool deduction. VCS 4022
     publishes one undisaggregated "final uncertainty deduction".
3. **The depth convention is undisclosed everywhere we looked.** VM0042 requires two depth
   increments to make equivalent-soil-mass accounting possible. Whether ESM was used is not
   stated in any public document for any project we read, in any registry. It is the single
   undisclosed parameter with the largest documented effect on a credited quantity.

**We propose that v3.0 require the following to be published**: in the monitoring report and as
machine-readable fields on the registry. Each is something the project already computes.

| # | field | why it matters |
|---|---|---|
| 1 | realised number of sampling locations, per stratum, per sampling round | n in Eq. (1)/(2) |
| 2 | cores per composite | sets the within-location variance term |
| 3 | sampling depth, depth increments, and depth convention (fixed depth or ESM, with ESM reference mass) | the largest undisclosed effect on a credited quantity |
| 4 | dates of the baseline round and of each re-measurement round | the interval the claimed change spans |
| 5 | S, the sample standard deviation of the SOC stock change, per stratum | the one input Eq. (2) needs that no one else can supply |
| 6 | MDD per Eq. (1) at the realised design, at the stated α and power, even where Eq. (2) is not used to set n | lets a reader compare claimed change with detectable change directly |
| 7 | uncertainty deduction **by pool** (SOC, N2O, CH4, other) and **by source** (sampling, model prediction), with the t-value and degrees of freedom used | makes the deduction invertible to a pool-specific precision |
| 8 | credited area per stratum, in hectares, as a number | the denominator of every per-hectare figure |
| 9 | for QA1: whether and when the re-measurement true-up was applied | says which part of the credited change has been measured |

Items 5 and 6 matter most. With them, any reader could check whether the claimed change exceeds
what the design could detect, using VM0042's own equation and none of ours. None of the nine
requires the full sampling plan, field locations or grower data to be published.

We would be glad to share the analysis and code.

[PI name, affiliation]

---

## 2. Template — one comment per VM0042 project in public comment

**To be instantiated per project from the PI's registry export.** Fill each `[…]` from the
project's own PD, with a locator. Leave a field out rather than estimate it. Do not file for a
project whose PD has not been read in full.

> **Comment on VCS [ID] — [project name] — public comment period [dates]**
>
> We comment only on what the project description makes public about soil sampling, so that the
> stock change it will claim can later be checked against VM0042's own Equation (2). We make no
> comment on the project's eligibility, additionality or design.
>
> From the PD as published: [area — §x]; [practices — §x]; [quantification approach — §x];
> [sampling design as stated — §x, or "the PD refers to [appendix/document], which is not
> among the public documents"].
>
> We ask that the monitoring reports for this project publish:
> (1) realised sampling locations per stratum per round;
> (2) cores per composite;
> (3) depth, increments and depth convention;
> (4) baseline and re-measurement dates;
> (5) the standard deviation of SOC stock change per stratum;
> (6) MDD per §8.2.1 Eq. (1) at the realised design;
> (7) the uncertainty deduction by pool and by source, with the t-value and degrees of freedom;
> (8) credited area per stratum in hectares;
> (9) [QA1 only] whether and when the model true-up was applied.
>
> [Only if true and located:] The PD names [parameter] in its monitoring table without a value
> ([§x]); we ask that the value be published when known.
>
> These are fields the project already computes. Publishing them lets any reader apply VM0042's
> own sample-size equation to the project's own numbers.

**Projects to instantiate:** *none yet* — awaiting the registry export.

---

### Notes for the PI

- **Sources for §1:**
  - Revision page and dates: `blocked_or_deferred` entry "VM0042 v3.0 public consultation" in
    `data/registry/projects.yaml`; D-066.
  - VCS 4022 facts: `projects.yaml` VCS 4022 record.
  - MDD/S/n/t "not relevant": **verified from the primary validation report** on 2026-11-10
    (PDF p. 50, "Data and Parameters monitored"). Recorded in `projects.yaml` as
    `power_analysis_parameters_assessment`.
  - "Final uncertainty deduction", undisaggregated: verified, PDF p. 147
    (`uncertainty_deduction_pool_scope`).
  - The ratio argument: D-068.
  - Depth convention: `docs/registry_corpus.md` Gap 3.
- **Decision A affects §1 point 2 only lightly.** It argues for pool-specific disclosure,
  whichever rule VCS 4022 used. It deliberately quotes no VCS 4022 ratio.
- **PR #21's eligibility-bar finding** (MR §2.4) is deliberately left out of this draft until
  decision A.
