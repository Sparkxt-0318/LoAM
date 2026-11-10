# Drafts — right of reply to each developer named

**Status: DRAFTS for the PI. Nothing has been sent.** One short, neutral note per developer whose
project is named in the manuscript or identifiable in its supplementary table
(`data/audit/population_audit.csv`). Each note gives that developer's own numbers and the public
source for every input, and invites corrections before publication. The reply window is left
for the PI to set.

**Tone, per `docs/registry_corpus.md`:** this is about what registries require to be published,
not about any developer. No note characterises a project as adequate or inadequate. Each states
what was computed, from which public document, under which stated assumptions.

**The same three paragraphs open every note** (shown once here, and marked ¶A–¶C in each note):

> ¶A. We are preparing a preprint on how much of the soil-carbon credit record can be checked
> from public documents alone. For each project that publishes an area and a credited quantity,
> we compute what soil-sampling campaign would have been needed to detect the credited change.
> We use VM0042's own sample-size equation (§8.2.1, Eq. 2) and a variance table taken at its
> most generous. We do not have, and do not claim to have, your sampling data.
>
> ¶B. Every input we used for your project is listed below with its public source. Every number
> depends on assumptions we state in the paper: research-plot variance applied to commercial
> support, a 60 Mg C/ha reference stock, and US cost figures. None of it is a finding about your
> project's compliance.
>
> ¶C. If any input is wrong, or a public document we missed would change it, we would be
> grateful to hear by [date]. We will correct the input and note the correction. If you would
> like a short response printed alongside the table, we will include it as written.

---

## 1. Agreena ApS — VCS 4022, AgreenaCarbon Project

Dear [contact],

¶A ¶B

**Inputs (all from the VCS validation report v4.0, Earthood, VCS.VAL.22.89, 20 Dec 2024, as
mirrored publicly):** area 479,834.11 ha (§3.1); average 543,369.95 tCO2e/yr (summary, §3.1);
applied uncertainty deduction 31.35% (corrective action log, "consistently reported in PD Table
4-17"); interval 5 years (inferred from VM0042's QA1 requirement, not stated by the project).

**What we computed:**
- **Detection cost.** A campaign of about 161 locations (2 cores per assay, re-randomised) would
  detect the credited change of 1.54 Mg C/ha net over 5 years. Its cost of about $8,050 implies
  a break-even carbon price of $0.003/tCO2e.
- **What your published deduction implies.** Read through VM0042's k = 0.4307, 31.35%
  corresponds to a relative standard error of about 73% of the estimate. On that reading the
  credited change is about 0.42× its own minimum detectable difference at 90% power, and 0.70×
  at 50% power.
- **What that rests on, and two points we may have wrong.** It is a calculation on the published
  figure, not on your data.
  - It assumes the 31.35% is the SOC-pool deduction. The validation report calls it "the final
    uncertainty deduction" without splitting it by pool.
  - It assumes k = 0.4307 applied to your v2.0 crediting.
  - We would particularly value a correction on either point.

¶C

---

## 2. Indigo Ag — CAR1459, Indigo U.S. Project No. 1

Dear [contact],

¶A ¶B

We also want to say plainly that CAR1459 publishes more about its sampling design than any other
project we read, and the paper says so.

**Inputs (Climate Action Reserve public document list for CAR1459):** RP5 SOC credits
1,065,452.3 tCO2e over 2,463,690.6 acres (Monitoring Report v5.8, Table 7); applied uncertainty
deduction 11.27% (RP5, Table 13) and 14.17% (RP4, Monitoring Report v4.5, Table 12); sampling
density 1 point per 8 acres under Design 1 (Monitoring Plan, Table 5.2); one 30 cm core per
carbon sample (Monitoring Plan v3.1, §6.4.1.2).

**What we computed:**
- **Detection cost.** A campaign of about 4,451 locations would detect the RP5 credited change of
  0.29 Mg C/ha net, at a break-even price of $0.21/tCO2e.
- **What your published deduction implies.** Read through CAR SEP's rule (z₀.₇₀ × the 95%
  half-width, effective k = 1.028), 11.27% corresponds to a relative standard error of about 11%.
  On that reading the credited change is about 2.8× its own minimum detectable difference at 90%
  power.
- **One sentence quoted from the RP5 Verification Report (§5.2.3).** We quote it as written: it
  says quantification through RP5 rests on the initial SOC measurements, and that the
  re-measurement true-up was deferred under variance determination 2025-VAR-2-DET-CAR1459.
  Please tell us if that is out of date.

¶C

---

## 3. AgriCapture Inc — CAR1513, AgriCapture US Rice Methane Project

Dear [contact],

¶A

CAR1513 appears in the paper only in the disclosure census, not in the audit. Its credits are
predominantly rice methane under the Soil Enrichment Protocol, so the SOC pool cannot be separated
from the ledger, and we do not audit it.

**What the paper says, with sources:** the Soil Enrichment Monitoring Plan v4 (§9) twice refers
to "the CAR1513 V4 Soil Sampling Memo" for stratification and soil sampling. We did not find that
memo among the 41 public documents listed for the project on 2026-08-12, so we record the sampling
design as **withheld** (named but not public) rather than undisclosed. If the memo is public and
we missed it, we would like to correct that.

¶C

---

## 4. AgriProve Solutions — 47 ACCU projects in the supplementary table

Dear [contact],

¶A ¶B

**Why this note covers 47 projects.** AgriProve Solutions is the registered proponent of 47 of
the 54 credit-issued projects under the 2018 and 2021 measurement methods (ACCU register,
Last-Modified 2026-10-20). All 54 appear in the supplementary table. None is named in the
manuscript text.

**Inputs (ACCU register and the published Carbon Estimation Area files):** credits issued (total
and by financial year), crediting period, project activities, and the "Estimation or measurement
approach or model" field where filled. The CEA area is our geodesic computation from the published
CEA shapefile, since the register has no numeric area field. Every value, with its file URL, is in
`data/registry/projects_accu_issued.yaml`.

**What the table shows, and what it does not:**
- **The split.** For 33 of the 47, a campaign at the densest density disclosed by any project we
  read would detect the cumulative credited change. 3 sit within our uncertainty band and 11
  outside it.
- **Why.** The split follows project area and credited change, not the proponent. Projects
  outside reach are the smaller ones with the smallest cumulative credited change, often after a
  single issuance. Outside reach means detection would need a denser campaign than any disclosed,
  not that the change did not occur.
- **What we cannot see.** We have no access to your sampling plans, which the register does not
  publish. Your actual campaigns may well be denser.
- **Per-project values.** [attach the 47 rows of `population_audit.csv`]

¶C

---

## 5. The other seven ACCU proponents

Seven credit-issued projects have other proponents (including ERF108333 Bonnie Doone, ERF105067
Moora Plains and ERF104527 Cheyenne, which the earlier corpus discusses by name). All seven are
inside reach in our calculation. A single short note in the form of §4, with that proponent's own
rows attached, is enough. Proponent names are in the register; they are not reproduced here.

---

### Notes for the PI

- **Who gets a note depends on what the manuscript names.** The current draft names VCS 4022,
  CAR1459 and CAR1513 in text, and the ACCU projects only in the supplementary table. If the
  supplementary table is dropped, notes 4 and 5 are optional.
- **The VCS 4022 paragraph depends on decision A.** If you decide k = 0.4307 does not apply to
  v2.0, delete the second bullet of "What we computed" in note 1.
- **Contact addresses are not included** and none were looked up.
