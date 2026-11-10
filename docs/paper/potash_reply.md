# Draft — reply to Eric Potash

**Status: DRAFT for the PI to edit and send. Nothing has been sent.** Sources for every number
are given in the notes at the end; strip them before sending. The correspondence record is
`docs/sources.md` §"Eric Potash"; his three quotes used below are verbatim from it.

---

**Subject:** Inorganic carbon result, and the post-hoc audit you suggested

Dear Eric,

Thank you again for the correction on the reference soil. We now carry 45 Mg C/ha everywhere
and cite your note for it, since there is no erratum.

Two things you asked to hear about either way.

**1. Inorganic carbon.** You suggested that soils with high inorganic carbon might show more
variable organic carbon measurements, perhaps 1% to 10% in total error. We tested this in
NAPESHM, where SOC is reported as total C minus inorganic C. **The result is null, but bounded.**
Between-plot CV is not detectably higher in carbonate-bearing soils, at a detection limit of
about **6.4–7.6%** analytical error, depending on the sample tier. So the test could only have
seen the top third of your range. Anything from 1% to roughly 6% would have passed through
unseen, and we say so in those words. Two things limit it:
- Inorganic carbon in NAPESHM is almost entirely a site property (98–100% of its variance is
  between sites).
- Inside our scope filters, every carbonate-bearing treatment is a two-replicate Mexican one,
  so the test is not identifiable there.

The cheap way to settle it is lab duplicates on a few hundred split samples spanning 0 to >2%
inorganic C, not a field campaign. The write-up is short: [link to `docs/ic_conditioning.md`].

**2. The post-hoc audit.** You wrote that it "would be interesting to know if existing projects
collect sufficient samples to detect the differences they aim to." Almost no registry publishes
sampling designs: 999 of 999 Australian soil-carbon projects have no sampling-design field of
any kind. So we inverted the question and asked what sampling each claim would have *required*,
using VM0042's own Equation 2 and our variance table at its most generous. The inputs are only
area, credits and interval.

Run across every project that publishes enough (56: all 54 credit-issued ACCU projects under
the measurement methods, plus CAR1459 and VCS 4022), the answer is mostly reassuring:
- **Most claims are cheaply detectable.** For 8 of the 11 projects in our cropland scope, a
  campaign at Indigo's disclosed density would detect the claimed change, at break-even carbon
  prices from $0.003 to about $1 per tonne.
- **The three that would not** are young projects with small credited changes on small areas.
- **One design choice matters most.** If every project is forced to revisit the same locations
  rather than re-randomise, the required n for the two projects that publish a deduction rises
  2.3×. Neither changes category. We report it as a named sensitivity.

**3. Two results we would most like you to check.** Both touch the deduction term in your model
(your z_deduct = 0.43, after VM0042), and we have not circulated either.

*(a) The audit's "implied" deduction is fixed by k, not by the soil.*
- At the audit's own cost-optimal design, n is chosen by VM0042 Eq. 2 so that SE ≤ Δ/(t_α + t_β).
- The deduction that design implies, k·SE/Δ, is therefore at most k/(z_α + z_β), which is
  **k / 3.24** at α = 0.05 and 90% power.
- That holds for every project and every variance: about 13.3% under VM0042, 31.7% under CAR's
  SEP and 7.8% under the ACCU rule. Our population run sits exactly there.
- An independent re-implementation, written without seeing our code, derived the same bound.
- **The consequence:** comparing an "implied" deduction with an applied one carries no project
  information. What does is the applied deduction itself, inverted through k.

Have we got that right, or is there a sense in which the implied figure should carry information
that we are missing?

*(b) What that inversion gives for VCS 4022: 0.42×, and we are treating it as pending expert
review.*
- **The calculation.**
  - VCS 4022 publishes a 31.35% uncertainty deduction.
  - Divided by k = 0.4307, that is a relative SE of about 0.73 of the estimate.
  - So Δ/MDD = 1/((z_α + z_β) × 0.73) ≈ **0.42** at 90% power, and 0.70 at 50%.
  - On that reading, the credited change is smaller than the project's own stated precision
    could detect.
  - For comparison, CAR1459's published 11.27% gives **2.8×** by the same route, using CAR's
    effective k of 1.028.
- **Two conditions we have not been able to settle from primary documents:**
  1. whether k = 0.4307 is the rule that applied under VM0042 v2.0 (verified for v2.2);
  2. whether the 31.35% is the SOC-pool deduction. The validation report calls it a single
     "final uncertainty deduction".
- **And one question of principle.** Both projects' deductions pool sampling with
  model-prediction error, so the "MDD" here describes the project's stated precision, not its
  sampling alone.

Is reading a published deduction this way sound? Would you be comfortable with this result
being reported at all, and if so, with what caveat? We would rather you tell us it is wrong now
than after it is public.

The large caveat is support. Our between-plot variance comes from research plots of about
0.02 ha, while projects quantify at field to continental scale. From the literature we could
read, stock variance is clearly larger at commercial support. That effect is capped, though,
because past about 2× the paired design wins, and it has no between-plot term. In scope the worst
case is then 6 of 11 inside reach. What we could not bound is the variance of *change* at field
scale. Your two-stage model's fitted within- and between-field change parameters are the closest
thing to that number we know of. If you could share them, they would let us test the floor
directly.

**Would you be willing to read the audit section of the draft?** About eight pages; points
(a) and (b) above are where we most want your view. Your model
is the nearest prior art, and we position the audit as upstream of the feasibility question
your paper answers, not as a substitute for it. We would rather hear now if you think we have
any of it wrong.

With thanks,
[PI name]

---

### Notes for the PI (delete before sending)

| claim in the letter | source |
|---|---|
| 45 Mg C/ha, typo confirmed | `docs/sources.md` §Eric Potash item 1; D-036 |
| his three quotes | `docs/sources.md` §Eric Potash items 2 and 3, verbatim |
| 6.4–7.6% detection limit, top third of 1–10% | `docs/ic_conditioning.md` §"What this test could have detected"; D-055 |
| 97.9–99.8% between-site | D-055 1a |
| Mexican two-replicate alias | D-055; D-040 check 1c |
| 999/999 no sampling-design field | `data/registry/projects.yaml` `registry_coverage` (2026-10-20 entry); D-064 |
| 56 projects, 8 of 11 inside reach, $0.003–~$1 | `docs/phase5_population_results.md` §1–2; `data/audit/population_audit.csv`; D-067. In-scope inside-reach break-even prices run $0.003–$0.94. |
| implied deduction bounded by 100k/(z_α+z_β) | D-068; confirmed by the independent re-implementation (WP3) |
| k / 3.24 bound; 13.3 / 31.7 / 7.8% | D-068; `docs/phase5_robustness.md` §(i) (independent derivation) |
| 0.42× / 0.70× (VCS 4022), 2.8× (CAR1459) | D-068; `docs/phase5_population_results.md` §3. **The 0.42× is pending expert review (PI rule, 2026-11-10); this letter is a request for that review.** Conditions: D-072 (open, PR #21 port) and the p. 147 scope wording |
| 2.3× under forced paired design | sensitivity S1; D-069; manuscript §5 and §7 |
| ~0.02 ha research plots; support mismatch | G9; D-063 |
| stock σ_B larger at commercial support; capped by paired design; change unbounded | D-070; `docs/g9_support_literature.md` |
| "your fitted change parameters" | Potash et al. 2025 models within- and between-field variability of change (abstract, per `docs/g9_support_literature.md` S13); the values were not read here |

**Before sending:**
- Per your instruction of 2026-11-10, section 3 asks him specifically about the k / 3.24 result
  and the 0.42× reading.
- The 0.42× is presented as pending expert review, with both conditions stated. Nothing in the
  letter presents it as a finding.
- **The letter shares an unpublished, unreviewed figure with one outside reader, by design.**
  If you would rather he see the derivation before the number, move the sentence "So Δ/MDD
  ≈ 0.42 at 90% power" below the two conditions.
