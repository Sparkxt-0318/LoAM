# Right of reply — four notes (PI decision E)

**HOLD: not to be sent before mentor review.** *(PI, 2026-11-11: every note in this file is on
hold until the PI says a mentor has read it.)*

**Status: DRAFTS for the PI to send. Nothing has been sent.**

Decision E (2026-11-10):
- These notes go out **before anything is public**, whether or not the supplementary table is
  published.
- Each developer gets **three weeks** to respond.
- **The supplementary table stays unpublished until that window closes.**
- The PI sends them.

**Recipients:**
1. AgriProve Solutions, proponent of 47 of the 54 credit-issued ACCU soil projects. On hold:
   mentor review.
2. Agreena ApS, developer of VCS 4022. On hold: mentor review **and** expert review of the 0.42×
   reading (D-076). It is then sent with that section included.
3. Indigo Ag, developer of CAR1459. On hold: mentor review.
4. Corporate Carbon Solutions Pty Ltd, co-proponent of ERF104781 only (PI, 2026-11-11). On hold:
   mentor review.

**Tone** (per `docs/registry_corpus.md`): the work is about what registries require to be
published, not about any developer. No note calls a project adequate or inadequate. Each states
what was computed, from which public document, under which assumptions, and asks for
corrections.

**Fill in before sending:** `[DATE SENT]`, `[REPLY BY]` (= date sent + 21 days), `[PI NAME,
AFFILIATION]`, `[contact]`. Contact addresses were not looked up.

---

## Note 1 — AgriProve Solutions

**HOLD: not to be sent before mentor review.**

**Subject:** Soil-carbon detectability study — your projects' figures, for comment by [REPLY BY]

Dear [contact],

We are preparing a study of what the public soil-carbon credit record lets anyone check. Before
anything is published, we are writing to each developer whose projects appear in it, with that
developer's own figures and our sources, so you can correct anything we have wrong.

**What we did.**
- **The population.** We include every credit-issued project under the 2018 and 2021
  measurement-based ACCU soil methods: 54 projects. AgriProve Solutions entities are the
  registered proponent for 47 of them. One of the 47 lists Corporate Carbon Solutions Pty Ltd as
  co-proponent.
- **The question.** For each project, we compute the cheapest soil-sampling campaign that would
  have detected the project's cumulative credited change. We use the sample-size equation from
  Verra's VM0042 (§8.2.1, Eq. 2) and a variance table taken at its most generous.
- **What we have not seen.** We have not seen your sampling plans; the register does not publish
  them. Nothing below is a statement about what your campaigns actually were, or about
  compliance.

**Your figures** are in the attached table (Attachment A), one row per project. In summary:
- **At headline settings:** 33 of the 47 are *inside reach*, 3 *within our uncertainty band* and
  11 *outside reach*. Inside reach means a campaign at the densest sampling density any project
  has disclosed (one point per 8 acres), on the project's own area, would detect the credited
  change across our variance table's whole range.
- **Why some are outside.** Outside reach means detection would need a denser campaign than any
  disclosed one. It does not mean the change did not happen. The split follows project area and
  the size of the credited change. The projects outside reach are the smaller ones with the
  smallest cumulative credited change. All 11 have had a single issuance so far, as have 43 of
  the 47, so that alone does not distinguish them.
- **Who the population covers.** AgriProve entities are proponent for 47 of the 54 projects, so
  any subset of this population is mostly yours. We say so in the study and draw no conclusion
  about any developer. The manuscript text names no ACCU project or developer. Your projects
  appear only in the supplementary table.
- **Under a more expensive design** that revisits the same locations (our sensitivity S1),
  28 are inside reach and 19 outside. Both columns are in Attachment A.

**Sources, all public:**
- **The ACCU Scheme project register (CSV),** Clean Energy Regulator, as at 20 October 2026,
  for:
  - credits issued, total and by financial year;
  - crediting period;
  - project activities;
  - the "Estimation or measurement approach or model" field.
- **Carbon estimation area (CEA) mapping files** at
  `cer.gov.au/sites/default/files/projectFiles/<Project ID>_CEA.zip`. The register has no
  numeric area field. **The areas in the table are our own geodesic calculation from these
  files**, cross-checked against your project-boundary KML files.

**Assumptions you may want to correct:**
- **Credited area.** We treat the CEA as the area the credits were computed over.
- **Credited change.** We treat cumulative ACCUs issued, divided by 3.667 and by the CEA area, as
  the net credited stock change from the baseline sampling round to the latest one.
- **Approach.** 19 of your projects state a measurement-only approach in the register, and one a
  hybrid model approach; 27 leave the field blank. We read "measurement-only" as direct sampling
  without a model.

**What we would value from you, by [REPLY BY]** (three weeks from this note):
- corrections to any input or assumption above;
- anything public we missed that would change a figure;
- if you wish, a short statement we will print alongside the table, as written.

You are not asked to share sampling plans. If you chose to, we would record the realised design
and re-run your projects on it.

**Nothing from this study is public yet. The supplementary table that lists your projects will
not be published before [REPLY BY].**

With thanks,
[PI NAME, AFFILIATION]

### Attachment A — AgriProve Solutions projects (47)

† Our geodesic calculation from the published CEA shapefile, recorded as *inferred*. "Required
n" is the number of sampling locations at the cost-optimal number of cores per sample (C\*).
"Cost" uses US unit costs ($15 per location core, $20 per assay). "Break-even" is that cost per
ACCU issued. Category is under our generous variance inputs. The S1 columns force a paired
design.

| Project ID | name | registered proponent | CEA area (ha)† | ACCUs issued | Δ, net (Mg C/ha) | required n (C\*) | cost (USD) | break-even (USD/t) | category | S1: paired n | S1 category |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| ERF101952 | Sandalwood Carbon Project | Agriprove Solutions Pty Ltd | 64.2 | 2,072 | 8.80 | 11 (1) | 385 | 0.19 | inside | 14 | inside |
| ERF104781 | Grounds Keeping Carbon Project | Agriprove Solutions Pty Ltd; Corporate Carbon Solutions Pty Ltd | 100.2 | 3,067 | 8.34 | 8 (2) | 400 | 0.13 | inside | 15 | inside |
| ERF118394 | Prosper Carbon Project | Agriprove Solutions Pty Ltd | 92.1 | 4,531 | 13.41 | 6 (1) | 210 | 0.05 | inside | 8 | inside |
| ERF118395 | Hallmark Carbon Project | Agriprove Solutions Pty Ltd | 36.7 | 2,068 | 15.36 | 5 (1) | 175 | 0.08 | inside | 6 | inside |
| ERF118397 | Prestige Carbon Project | Agriprove Solutions Pty Ltd | 60.4 | 2,463 | 11.13 | 8 (1) | 280 | 0.11 | inside | 10 | inside |
| ERF122082 | Trophy Carbon Project | Agriprove Solutions Pty Ltd | 116.1 | 5,947 | 13.97 | 6 (1) | 210 | 0.04 | inside | 7 | inside |
| ERF143770 | Fysh Carbon Project | Agriprove Solutions Pty Ltd | 394.3 | 3,559 | 2.46 | 65 (2) | 3,250 | 0.91 | inside | 149 | outside |
| ERF149373 | Watson Carbon Project | Agriprove Solutions Pty Ltd | 260.6 | 5,585 | 5.84 | 14 (2) | 700 | 0.13 | inside | 28 | inside |
| ERF154609 | Lyne Carbon Project | Agriprove Solutions Pty Ltd | 210.0 | 1,114 | 1.45 | 183 (2) | 9,150 | 8.21 | outside | 425 | outside |
| ERF158304 | McClean Carbon Project | Agriprove Solutions Pty Ltd | 347.9 | 4,942 | 3.87 | 28 (2) | 1,400 | 0.28 | inside | 62 | inside |
| ERF158470 | Smith Carbon Project | Agriprove Solutions Pty Ltd | 505.2 | 1,362 | 0.74 | 702 (2) | 35,100 | 25.77 | outside | 1,641 | outside |
| ERF159517 | Kelly Carbon Project | Agriprove Solutions Pty Ltd | 98.7 | 4,448 | 12.30 | 7 (1) | 245 | 0.06 | inside | 8 | inside |
| ERF159853 | Lynch Carbon Project | Agriprove Solutions Pty Ltd | 156.1 | 641 | 1.12 | 304 (2) | 15,200 | 23.71 | outside | 708 | outside |
| ERF160172 | Mountain View Carbon Project | Agriprove Solutions Pty Ltd | 99.9 | 457 | 1.25 | 245 (2) | 12,250 | 26.81 | outside | 571 | outside |
| ERF162497 | McLachlan Carbon Project | Agriprove Solutions Pty Ltd | 93.1 | 6,060 | 17.75 | 5 (1) | 175 | 0.03 | inside | 5 | inside |
| ERF166949 | Evatt Carbon Project - Breust 1 | Agriprove Solutions Pty Ltd | 211.3 | 2,334 | 3.01 | 44 (2) | 2,200 | 0.94 | inside | 100 | outside |
| ERF166967 | Scully Carbon Project | Agriprove Solutions Pty Ltd | 226.4 | 4,478 | 5.39 | 16 (2) | 800 | 0.18 | inside | 33 | inside |
| ERF166972 | Ashley Carbon Project | Agriprove Solutions Pty Ltd | 173.0 | 515 | 0.81 | 576 (2) | 28,800 | 55.92 | outside | 1,346 | outside |
| ERF167123 | Lazzarini Carbon Project 2 | Agriprove Solutions Pty Ltd | 276.4 | 2,234 | 2.20 | 80 (2) | 4,000 | 1.79 | band | 185 | outside |
| ERF167124 | Lazzarini Carbon Project 3 | Agriprove Solutions Pty Ltd | 229.3 | 4,009 | 4.77 | 19 (2) | 950 | 0.24 | inside | 41 | inside |
| ERF168644 | Swartz Carbon Project 4 | Agriprove Solutions Co No.1 Pty Ltd | 148.5 | 3,176 | 5.83 | 14 (2) | 700 | 0.22 | inside | 29 | inside |
| ERF168650 | Swartz Carbon Project 9 | Agriprove Solutions Co No.1 Pty Ltd | 177.1 | 2,976 | 4.58 | 21 (2) | 1,050 | 0.35 | inside | 45 | inside |
| ERF169436 | Howson Carbon Project 4 | Agriprove Solutions Co No.1 Pty Ltd | 166.0 | 5,009 | 8.23 | 8 (2) | 400 | 0.08 | inside | 16 | inside |
| ERF169439 | Howson Carbon Project 7 | Agriprove Solutions Co No.1 Pty Ltd | 250.3 | 3,591 | 3.91 | 27 (2) | 1,350 | 0.38 | inside | 60 | inside |
| ERF169446 | Howson Carbon Project 14 | Agriprove Solutions Co No.1 Pty Ltd | 309.4 | 5,623 | 4.96 | 18 (2) | 900 | 0.16 | inside | 39 | inside |
| ERF169476 | Howson Carbon Project 15 | Agriprove Solutions Co No.1 Pty Ltd | 184.8 | 3,706 | 5.47 | 15 (2) | 750 | 0.20 | inside | 32 | inside |
| ERF170331 | Barwick Carbon Project 1 | Agriprove Solutions Pty Ltd | 172.9 | 3,036 | 4.79 | 19 (2) | 950 | 0.31 | inside | 41 | inside |
| ERF170334 | Barwick Carbon Project 3 | Agriprove Solutions Pty Ltd | 248.3 | 5,610 | 6.16 | 13 (2) | 650 | 0.12 | inside | 26 | inside |
| ERF170337 | Barwick Carbon Project 4 | Agriprove Solutions Pty Ltd | 122.7 | 1,902 | 4.23 | 24 (2) | 1,200 | 0.63 | inside | 52 | outside |
| ERF172195 | Morrison Carbon Project 1 | Agriprove Solutions Pty Ltd | 184.0 | 1,693 | 2.51 | 62 (2) | 3,100 | 1.83 | outside | 143 | outside |
| ERF172197 | Morrison Carbon Project 2 | Agriprove Solutions Pty Ltd | 109.4 | 1,980 | 4.94 | 18 (2) | 900 | 0.45 | inside | 39 | outside |
| ERF172203 | Morrison Carbon Project 5 | Agriprove Solutions Pty Ltd | 111.4 | 1,484 | 3.63 | 31 (2) | 1,550 | 1.04 | band | 70 | outside |
| ERF172205 | Morrison Carbon Project 7 | Agriprove Solutions Pty Ltd | 121.9 | 1,495 | 3.34 | 36 (2) | 1,800 | 1.20 | band | 82 | outside |
| ERF173466 | Killen Carbon Project | Agriprove Solutions Co No.1 Pty Ltd | 47.1 | 2,996 | 17.33 | 5 (1) | 175 | 0.06 | inside | 6 | inside |
| ERF173553 | McClelland Carbon Project | Agriprove Solutions Pty Ltd | 108.8 | 1,008 | 2.53 | 62 (2) | 3,100 | 3.08 | outside | 141 | outside |
| ERF173776 | Guilfoyle Carbon Project 7 | Agriprove Solutions Pty Ltd | 190.6 | 382 | 0.55 | 1,268 (2) | 63,400 | 165.97 | outside | 2,968 | outside |
| ERF174333 | Viner Carbon Project | Agriprove Solutions Co No.1 Pty Ltd | 61.3 | 2,509 | 11.17 | 8 (1) | 280 | 0.11 | inside | 10 | inside |
| ERF175414 | Messner Carbon Project 1 | Agriprove Solutions Pty Ltd | 665.9 | 3,327 | 1.36 | 206 (2) | 10,300 | 3.10 | outside | 480 | outside |
| ERF175975 | Fife Carbon Project | Agriprove Solutions Pty Ltd | 157.6 | 5,435 | 9.41 | 10 (1) | 350 | 0.06 | inside | 13 | inside |
| ERF175981 | Hodges Carbon Project | Agriprove Solutions Pty Ltd | 131.9 | 290 | 0.60 | 1,053 (2) | 52,650 | 181.55 | outside | 2,466 | outside |
| ERF176354 | Blewett Carbon Project 5 | Agriprove Solutions Co No.2 Pty Ltd | 355.1 | 9,253 | 7.11 | 10 (2) | 500 | 0.05 | inside | 20 | inside |
| ERF176357 | Blewett Carbon Project 8 | Agriprove Solutions Co No.2 Pty Ltd | 381.8 | 8,451 | 6.04 | 13 (2) | 650 | 0.08 | inside | 27 | inside |
| ERF176430 | Jones Carbon Project 2 | Agriprove Solutions Pty Ltd | 170.3 | 8,009 | 12.82 | 6 (1) | 210 | 0.03 | inside | 8 | inside |
| ERF176437 | Jones Carbon Project 8 | Agriprove Solutions Pty Ltd | 489.8 | 1,453 | 0.81 | 580 (2) | 29,000 | 19.96 | outside | 1,355 | outside |
| ERF176439 | Jones Carbon Project 9 | Agriprove Solutions Pty Ltd | 265.6 | 2,979 | 3.06 | 43 (2) | 2,150 | 0.72 | inside | 97 | outside |
| ERF179167 | Ryan Carbon Project 2 | Agriprove Solutions Co No.2 Pty Ltd | 293.9 | 4,839 | 4.49 | 21 (2) | 1,050 | 0.22 | inside | 46 | inside |
| ERF180115 | Duncan Carbon Project 2 | Agriprove Solutions Co No.2 Pty Ltd | 113.3 | 6,254 | 15.05 | 5 (1) | 175 | 0.03 | inside | 7 | inside |

---

## Note 2 — Agreena ApS (VCS 4022, AgreenaCarbon Project)

**HOLD: not to be sent before mentor review.**

**HOLD: not to be sent before the 0.42× reading has passed expert review.** Expert review is done
only when a named reviewer with soil-carbon statistics expertise has replied in writing on
**both** the k / 3.24 derivation and the 0.42× reading, and any correction they raise has been
applied and logged as a D-NNN. Silence does not count (PI, 2026-11-11; D-076). Once review has
passed, this note goes out **with** the section "A second calculation…" included, updated for any
correction.

**Subject:** Soil-carbon detectability study — VCS 4022 figures, for comment by [REPLY BY]

Dear [contact],

We are preparing a study of what the public soil-carbon credit record lets anyone check. Before
anything is published, we are writing to each developer whose project is named in it, with that
project's figures and our sources, so you can correct anything we have wrong. Nothing below is a
finding about the project's compliance.

**Inputs.** All are from the VCS Validation Report, AgreenaCarbon Project, v4.0, VCS.VAL.22.89
(Earthood, 20 December 2024), as mirrored publicly. Page numbers are PDF pages.
- area 479,834.11 ha (§3.1);
- average emission reductions and removals 543,369.95 tCO2e per year (summary, §3.1);
- applied uncertainty deduction 31.35% (p. 147, CAR#60);
- remeasurement interval 5 years. This is *inferred* from VM0042's measure-and-model requirement;
  the project does not state it.

**What we computed:**
- **Detection cost.** Sampling about **161 locations**, at 2 cores per sample with re-randomised
  locations, would detect the credited change of 1.54 Mg C/ha net over five years. That costs
  about **$8,050** against about 2.7 million credited tonnes, a **break-even carbon price of
  $0.003 per tonne**.
- **Category: inside reach**, with large margin. The noise could be 30× our generous estimate
  before a campaign at the densest disclosed sampling density stopped sufficing.
- **If the same locations are revisited** (our sensitivity S1), the requirement is about 374
  locations and $0.005 per tonne. The project is still inside reach.
- **The large caveat we state** is that our variance comes from research plots of about 0.02 ha,
  while the project spans about 480,000 ha.

**A second calculation, which we mark as pending expert review.** A published uncertainty
deduction can be read back through the registry's own rule.
- **The reading.** Under VM0042's t ≈ 0.4307, 31.35% corresponds to a relative standard error of
  about 73% of the estimate. On that reading, the credited change would be about 0.42× the
  smallest change the project's own stated precision could detect at 90% power, or 0.70× at 50%
  power.
- **Its status.** This is being reviewed by outside experts before we decide whether to report
  it. It uses only the published figure, not our variance estimates.
- **It rests on two points we may have wrong:**
  1. that t ≈ 0.4307 is the rule that applied under VM0042 v2.0;
  2. that the 31.35% is the deduction for the soil organic carbon pool. The validation report
     calls it "the final uncertainty deduction" (p. 147) without a split by source, and we have
     not seen the project description's §4.4.4 or Table 4-17.

  **A correction on either point would change or remove this calculation.**

**Two facts we also report from the validation report**, quoted as written:
- the parameters MDD, S, n, n−1 and t are each assessed as "not relevant and therefore not
  further assessed" (p. 50);
- the PD's uncertainty value changed from 23.97% and 14.53% to 31.35% under CAR#60 (p. 147).

**What we would value from you, by [REPLY BY]** (three weeks from this note):
- corrections to any input above;
- in particular, whether the 31.35% is the SOC-pool deduction, and which equation produced it;
- if you wish, a short statement we will print as written.

**Nothing from this study is public yet, and nothing will be published before [REPLY BY].**

With thanks,
[PI NAME, AFFILIATION]

---

## Note 3 — Indigo Ag (CAR1459, Indigo U.S. Project No. 1)

**HOLD: not to be sent before mentor review.**

**Subject:** Soil-carbon detectability study — CAR1459 figures, for comment by [REPLY BY]

Dear [contact],

We are preparing a study of what the public soil-carbon credit record lets anyone check. Before
anything is published, we are writing to each developer whose project is named in it, with that
project's figures and our sources, so you can correct anything we have wrong. We also want to
say plainly that CAR1459 publishes more about its sampling design than any other project we
read, and the study says so.

**Inputs.** All are from the Climate Action Reserve public document list for CAR1459:
- RP5 SOC credits, 1,065,452.3 tCO2e over 2,463,690.6 acres (Monitoring Report v5.8, Table 7);
- cumulative credits issued, 2,113,861 tCO2e (Table 16);
- applied uncertainty deduction, 11.27% in RP5 (Table 13; recalculated by the verifier, RP5
  Verification Report §5.2.4) and 14.17% in RP4 (Monitoring Report v4.5, Table 12);
- sampling density, one point per 8 acres under Design 1 (Monitoring Plan v5.4, Table 5.2);
- one 30 cm core per carbon sample (Monitoring Plan v3.1, §6.4.1.2).

**What we computed:**
- **Detection cost.** Sampling about **4,451 locations**, at 2 cores per sample with
  re-randomised locations, would detect RP5's credited change of 0.29 Mg C/ha net. That costs
  about **$222,550** against 1,065,452 RP5 SOC credits, a **break-even price of $0.21 per tonne**.
- **Category: inside reach.** The noise could be 8× our generous estimate before a campaign at
  your own disclosed density stopped sufficing.
- **If the same locations are revisited** (our sensitivity S1), the requirement is about 10,430
  locations and $0.34 per tonne. The project is still inside reach.
- **What your published deduction implies.** Read through the SEP rule as we understand it
  (z₀.₇₀ × the 95% CI half-width, an effective multiplier of 1.028 on the relative standard
  error), 11.27% corresponds to a relative standard error of about 11%. On that reading, the RP5
  credited change is about **2.8×** the smallest change the project's own stated precision could
  detect at 90% power. We note that this precision pools sampling and model error, as the
  monitoring plan states.
- **One sentence quoted from the RP5 Verification Report (§5.2.3)**, as written: quantification
  through RP5 "was based on the initial SOC measurements", and the re-measurement true-up was
  deferred under variance determination 2025-VAR-2-DET-CAR1459.

**Points we may have wrong, and would value a correction on, by [REPLY BY]** (three weeks from
this note):
1. **The multiplier.** We read the SEP v1.1 rule from your monitoring plan, not from the
   protocol itself.
2. **The sample count.** It is the realised number of sampling points in RP5. The plan gives the
   rules but not the count, so our figure is a rule, not a realised design.
3. **The true-up.** Whether the deferral is still current.
4. **A statement.** If you wish, a short statement we will print as written.

**Nothing from this study is public yet, and nothing will be published before [REPLY BY].**

With thanks,
[PI NAME, AFFILIATION]

---

## Note 4 — Corporate Carbon Solutions Pty Ltd (ERF104781 only)

**HOLD: not to be sent before mentor review.**

**Subject:** Soil-carbon detectability study — ERF104781 figures, for comment by [REPLY BY]

Dear [contact],

We are preparing a study of what the public soil-carbon credit record lets anyone check. Before
anything is published, we are writing to every registered proponent whose project appears in it,
with that project's own figures and our sources, so you can correct anything we have wrong.
**This note covers one project only: ERF104781, Grounds Keeping Carbon Project**, where the ACCU
register lists Corporate Carbon Solutions Pty Ltd as co-proponent.

**What we did.** For every credit-issued project under the 2018 and 2021 measurement-based ACCU
soil methods (54 projects), we compute the cheapest soil-sampling campaign that would have
detected the project's cumulative credited change. We use the sample-size equation from Verra's
VM0042 (§8.2.1, Eq. 2) and a variance table taken at its most generous. We have not seen the
project's sampling plan; the register does not publish sampling plans. Nothing below is a
statement about what the project's campaigns were, or about compliance.

**Inputs for ERF104781.** All are from public sources; the area is our own calculation.
- **ACCU Scheme project register (CSV),** Clean Energy Regulator, as at 20 October 2026:
  - 3,067 ACCUs issued: 406 in FY2018/19, 1,498 in FY2019/20, 1,163 in FY2024/25;
  - crediting period 28 October 2016 to 27 October 2041;
  - location: Victoria, postcode 3818;
  - activities: altering the stocking rate, duration or intensity of grazing; re-establishing or
    rejuvenating a pasture; using legume species;
  - the "Estimation or measurement approach or model" field is blank.
- **Carbon estimation area (CEA).** `cer.gov.au/sites/default/files/projectFiles/ERF104781_CEA.zip`.
  The register has no numeric area field, so **the area is our geodesic calculation from this
  shapefile: 100.2 ha**. It lies entirely within the project boundary in `ERF104781.kml`, which
  we compute at 124.5 ha.

**What we computed:**
- **Credited change.** Cumulative ACCUs ÷ 3.667 ÷ CEA area gives a net credited change of about
  **8.3 Mg C/ha** from the baseline sampling round to the latest one.
- **Detection cost.** Sampling about **8 locations**, at 2 cores per sample with re-randomised
  locations, would detect that change. That costs about **$400** (US unit costs), a
  **break-even price of $0.13 per ACCU**.
- **Category: inside reach.** A campaign at the densest sampling density any project has
  disclosed (one point per 8 acres, about 31 points on this area) would detect the change across
  our variance table's whole range.
- **If the same locations are revisited** (our sensitivity S1), the requirement is about 15
  locations and $0.17 per ACCU. The project is still inside reach.
- **Scope.** The project's stated activities are grazing and pasture, which is outside the
  cropland focus of our main results. It appears only in the supplementary table, where the
  manuscript reports grazing projects separately and never pools them with cropland.

**Assumptions you may want to correct:**
- **Credited area.** We treat the CEA as the area the credits were computed over.
- **Credited change.** We treat cumulative ACCUs as the net credited change from the baseline
  round to the latest one.

**What we would value from you, by [REPLY BY]** (three weeks from this note):
- corrections to any input or assumption above;
- anything public we missed;
- if you wish, a short statement we will print alongside the table, as written.

**Nothing from this study is public yet. The supplementary table that lists ERF104781 will not
be published before [REPLY BY].**

With thanks,
[PI NAME, AFFILIATION]

---

### Notes for the PI (not for sending)

- **Note 2 keeps the 0.42× section, and the whole note is on hold** (PI, 2026-11-11). It goes out
  only after the reading passes expert review under D-076, and then with the section included.
- **Corporate Carbon Solutions is not copied on Note 1** (PI, 2026-11-11). They get their own
  Note 4, covering ERF104781 only.
- **Earlier drafts also had notes for AgriCapture (CAR1513) and the seven other ACCU
  proponents.** Decision E names three recipients, so those are dropped. CAR1513 appears in the
  manuscript only in the disclosure census.
- **Sources for every figure:**
  - `data/audit/population_audit.csv`;
  - `data/registry/projects.yaml` (VCS 4022, CAR1459);
  - `data/registry/projects_accu_issued.yaml`;
  - S1 per project: `run_audit(..., force_design="paired")`, as in `scripts/sensitivity_audit.py`.
