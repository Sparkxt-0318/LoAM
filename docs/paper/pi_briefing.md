# PI briefing: the method, the ten decisions most likely to be challenged, and what to know cold

**For the PI only.** Plain language. Every number here has a D-NNN or a file behind it; the
references are in brackets so you can check, not so you need to cite them.

---

## The method in one page

**The question.** A carbon registry credits a project for a change in soil carbon. Could a
soil-sampling campaign have detected that change at all? And would detecting it have cost more
than the credits were worth?

**Why we cannot ask it directly.** Answering directly needs the project's sampling design. Almost
nobody publishes one: 999 of 999 Australian soil-carbon projects have no sampling-design field of
any kind [D-056, D-064]. One CAR project and one Verra project publish more, and even they
withhold the key numbers.

**So we invert it.** Take what *is* published: area, credits issued, interval. Turn it into a
per-hectare change, Δ. Then ask what campaign *would have been required* to detect Δ. The
equation is not ours. It is VM0042's own sample-size formula (§8.2.1, Eq. 2), which VM0042 makes
optional in the same sentence [D-057]. The one input we supply is the noise: a variance table
built from published field studies, taken at its most generous (the smallest noise the evidence
allows) [D-062].

**What comes out, per project:**
- **n_req and Cost\*:** the cheapest campaign that would detect Δ, over designs and cores per
  sample.
- **Break-even price:** the carbon price below which that campaign costs more than the credits.
- **Break-even noise scale:** how much noisier the soil could be than our table says before a
  realistic campaign stops sufficing.
- **One of three categories** [D-067]:
  - *inside reach*: detectable across our table's whole range;
  - *within the uncertainty band*: depends on where in that range the truth lies;
  - *outside reach*: not detectable even on our most generous inputs.
- **Support-mismatch ratio:** project area over the plot size our variance was measured on. It is
  enormous and unresolved [G9].
- **Where a project publishes its uncertainty deduction:** that deduction, inverted through the
  registry's own rule, gives the project's *own* stated precision. It needs none of our numbers
  [D-068].

**What it found** [`docs/phase5_population_results.md`]:
- 56 projects can be run.
- Of the 11 in our cropland scope, 8 are inside reach and 3 outside, at break-even prices from
  $0.003 to $182/tCO2e (median $0.31).
- Large claims are cheap to detect. The outside-reach projects are young, small ones with small
  credited changes.
- On their own published deductions, CAR1459's claim is 2.8× its own detection floor. VCS 4022's
  is 0.42×, conditional on decision A.

---

## The ten decisions most likely to be challenged

For each: what we did, the strongest objection, and the answer. Order is by how likely a
competent critic is to raise it.

**1. "Your variance comes from research plots, their projects are whole landscapes" (G9, D-063).**
- *What we did:* between-plot variance is from 0.02 ha replicate plots. Projects run from 37 ha
  to 1,000,000 ha. We report the mismatch on every number (median ~10,000× in scope; 25
  million× for VCS 4022) and do not refuse to run.
- *Objection:* at commercial support σ_B is a different quantity, so every number is wrong.
- *Answer:* agreed that it is unresolved, and it leads the limitations. We report, per project,
  how much larger σ_B could be before the claim leaves reach (median 3.4× in scope).
- *What the literature says* [D-070]:
  - For **stock** variance, commercial σ_B is **larger**: about 1.5–5× within a field, 5–10×
    across fields.
  - That effect is **capped**. The paired design has no σ_B term and takes over above ~2×, so in
    scope the worst case is 6 inside / 5 outside. VCS 4022 and CAR1459 stay inside reach.
  - For **change** variance, the direction is unknown. That is what the cap rests on.
- *Do not say* "our numbers apply at project scale".

**2. "Equation 2 is optional by design; you have turned a planning aid into a standard" (red
team B-1, D-059).**
- *What we did:* we never say a project should have sampled n_req. We say what n_req and its
  cost would have been, and compare it with the project's economics.
- *Answer:* the deduction is VM0042's real instrument. Our strongest result uses only that
  instrument [D-068].

**3. "Most generous assumptions — is that a confidence interval?" (red team C-2, D-062).**
- *Answer:* no. It is a corner of the input space. Each component sits at its own lower bound,
  which is a worst case for us, not a probability. That is said everywhere. A proper joint
  propagation would need a distribution per component, which we do not have, and inventing one
  would be worse.

**4. "Your between-plot input is one site in the Pacific Northwest" (D-060, G8).**
- *Answer:* yes. It is the only genuine 0–30 cm between-plot row. The broader NAPESHM figure is
  0–15 cm, and our rule D-026 forbids rescaling it. The invariance result (D-040, D-055) says
  between-plot CV does not detectably vary with climate or texture, but only to about ±2 and ±10
  CV points.

**5. "Unpaired cheaper than paired? Everyone knows revisits are better" (D-060, D-061).**
- *Answer:*
  - It follows from two choices, both written down: relocation error used undivided (9.4%), and
    between-plot error from the narrow 0–30 cm row (3.1%).
  - With the design doc's own original conventions, paired wins.
  - We do not fix the design; we take whichever is cheaper per project.
  - The sensitivity grid [D-069] shows forcing paired raises VCS 4022's n from 161 to 374, and
    CAR1459's from 4,451 to 10,430. That is 2.3×, over your 2× threshold, but neither changes
    category, and break-even prices rise only 1.6×. In-scope projects become 6 inside and 5
    outside, from 8 and 3.
  - This is the most consequential choice in the grid. Know it.

**6. "Δ from credits ÷ area is not the SOC change" (red team A-3, C-6; D-064, D-066).**
- *Answer:* correct. It is the net credited change, after every deduction, so it understates the
  SOC claim. That makes detection *harder* in our calculation, which is conservative for the
  project.
  - ACCU: cumulative credits ÷ credited area (geometry-derived, since there is no area field).
  - CAR1459: one reporting period's SOC-only credits over that period's own area.

**7. "Your plausible campaign is Indigo's density — why that?" (D-067).**
- *Answer:* it is the densest campaign any project has disclosed, so it is a real-world anchor,
  not our choice of threshold. Limitation: on a small farm a denser grid is physically possible.
  So "outside reach" means "denser than any disclosed campaign", not "impossible". The categories
  line up with break-even price anyway: inside reach is everything up to ~$1.8/tCO2e.

**8. "The 13.2% vs 31.35% comparison" (D-059 → D-068).**
- *What changed:*
  - The audit's "implied deduction" at its own optimum is fixed by the registry's k and the
    power convention, about 13.3% for any VM0042 project. It says almost nothing about VCS 4022.
  - The informative quantity is the *ratio*. Applied ÷ implied equals the project's own minimum
    detectable difference divided by its claim.
  - An independent re-implementation confirmed the bound.
- *Two open conditions on VCS 4022's 0.42:* which VM0042 rule applied to its v2.0 crediting, and
  whether 31.35% is the SOC-only figure. **Decision A.**

**9. "Your category counts are a failure rate" (red team C-5, D-067).**
- *Answer:* there are three categories, not pass/fail. Out-of-scope projects (grazing, unresolved
  land use) are reported separately and never pooled. The population is a complete count of what
  is auditable, which is self-selected toward projects that publish. "8 of 11" describes this
  population, nothing wider.

**10. "Every project outside reach belongs to one developer" (D-067 base rate).**
- *Answer:* that developer is the proponent of 47 of the 54 credit-issued ACCU soil projects, so
  it would dominate any subset. The category follows area and credited change: its projects are
  smaller (median 173 ha against 1,824 ha) and younger (median first issuance FY2024), and 33 of
  its 47 are inside reach. We draw no developer-level inference, and the manuscript names no ACCU
  project in its text.

**Also expect:**
- **"Your costs are US Midwest"** (C-1). The break-even price scales linearly with absolute cost.
  The assay:location cost ratio is in the sensitivity grid.
- **"Why should a 45 Mg C/ha reference soil matter?"** It enters only the conversion from CV to
  absolute SD, as a level, not a trajectory (D-004).

---

## Questions you should be able to answer without notes

1. How many Australian soil-carbon projects publish a sampling design? **None of 999.** How many
   have been issued credits? **54, 462,162 ACCUs (register as at 2026-10-20).**
2. What is VM0042's Equation 2, and what does VM0042 say right after it? **n ≥ (S(t_α+t_β)/MDD)²;
   "projects are not required to take this number of samples."**
3. Name the three registries' deduction multipliers. **ACCU 0.253 (40th percentile), VM0042 0.431
   (33.3rd), CAR SEP 1.028 (15.2nd). Identical variance gives a fourfold different haircut.**
4. Why is "implied 13.2%" not evidence about VCS 4022? **At the audit's optimum it is ≤
   100k/(z_α+z_β) for any project.**
5. What does CAR1459's 11.27% imply? **A relative SE of ~11%, so its claim is ~2.8× its own 90%
   MDD. That pools sampling and model error. Its re-measurement true-up was deferred under a
   Reserve variance.**
6. What is the single biggest caveat, and its size? **G9, support.**
   - Research plots are ~0.02 ha; the median in-scope support mismatch is ~10,000×.
   - Stock σ_B is larger at commercial support (bounded). Its effect is capped by the paired
     design: worst case 6 inside / 5 outside in scope.
   - Change variance is unbounded in direction. That is the live caveat.
7. What does "inside reach" mean, exactly? **A campaign at Indigo's disclosed density, on the
   project's own area, detects the credited change even at the high corner of our variance
   table.**
8. Why were the outside-reach projects outside? **Small credited change (0.5–0.8 Mg C/ha) on small
   areas (130–190 ha): they would need 600–1,300 locations, $56–182 per credit.**
9. What is a null worth here? **Only its detection limit. The inorganic-carbon null holds above
   ~7% analytical error, which is the top third of Potash's 1–10%.**
10. How does this differ from Potash et al. 2025? **They ask whether a project is economically
    feasible. We ask whether its claim is resolvable, which their question presupposes [D-038].
    Their σ_b is geography-independent "for lack of information". Our invariance result
    supports that choice to a stated limit.**
11. What would change the headline most? **A support-scaling relationship (G9). Then a second
    region for temporal and between-plot variance (G8). Then Verra's ~200 VM0042 projects, which
    are blocked by access, not disclosure.**
12. What did we NOT find? **Any developer-level pattern. Any rate that generalises beyond the
    auditable, self-selected population.**
