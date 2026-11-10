# Phase 5, WP2: the inverted audit over the whole auditable population

**Read the caveats section before quoting any number.** Decisions: D-067 (three categories),
D-068 (the implied-deduction finding). Reproduce: `python scripts/run_population_audit.py
--markdown` (about 2.5 minutes). Per-project output: `data/audit/population_audit.csv`.

---

## The one-paragraph version

56 of 57 registered projects now clear the audit gate. That is every credit-issued ACCU soil
project under the measurement methods (54), plus CAR1459 and VCS 4022; CAR1513 is rice methane,
so its SOC pool is not separable. **Of the 11 in LoAM's scope, 8 are inside reach and 3 are
outside.** Inside reach means a campaign at the densest disclosed density, on the project's own
area, would detect the claimed change across the variance table's whole envelope. The 3 outside
are the in-scope projects with the smallest credited change on small areas (0.55–0.81 Mg C/ha on
130–190 ha). The first run's finding stands and extends: **where a claim is large relative to
the noise, it is cheaply detectable**. VCS 4022's break-even price is still $0.003/tCO2e, and
the in-scope median is $0.31. Separately, the comparison the B-1 headline rested on turns out to
carry no project information on the audit side (D-068). What it does carry is the project's
*own* published precision. On that reading, **CAR1459's published deduction implies a claim
2.8× its own 90%-power minimum detectable difference.** VCS 4022's reading is in §3, labelled
**pending expert review** and dependent on PI decision A; by PI rule (2026-11-10) it is not
quoted in summaries.

---

## 1. Three categories, by group (never pooled across groups)

| group | projects | inside reach | within uncertainty band | outside reach |
|---|---:|---:|---:|---:|
| **in scope** (cropland, south of the Tropic of Capricorn or US/EU) | **11** | **8** | **0** | **3** |
| out of scope: grazing / pasture | 38 | 30 | 2 | 6 |
| out of scope: land use unresolved (nutrients-only) | 7 | 4 | 1 | 2 |

**Definition (D-067).** Take s*, the factor by which every noise component could grow before a
campaign at CAR1459's disclosed density (1 point per 8 acres), on the project's own area, at the
cost-optimal design, stops sufficing. Compute it under the generous corner (the headline rule) and
under the high corner of the table's own envelope.

- **Outside reach:** s* < 1 under the generous corner.
- **Inside reach:** s* ≥ 1 under the high corner.
- **Within the band:** everything in between.

**The categories line up with break-even price, which was not used to define them:**

| category | projects | break-even price range (USD/tCO2e) |
|---|---:|---|
| inside reach | 42 | 0.003 – 1.74 |
| within the uncertainty band | 3 | 1.04 – 1.79 |
| outside reach | 11 | 1.83 – 182 |

So in this population "outside reach" means **detecting the claim would cost more than about
$1.8 per credit at a density no disclosed project has used**. For the small projects in that
category, a denser grid is physically possible. "Outside reach" there means *denser than the
densest disclosed campaign*, not *impossible*.

## 2. Distributions (min · Q1 · median · Q3 · max)

**In scope (n = 11)**

| quantity | min | Q1 | median | Q3 | max |
|---|---:|---:|---:|---:|---:|
| Δ, net credited (Mg C/ha) | 0.29 | 0.71 | 3.01 | 5.09 | 9.41 |
| n_req at Cost* (locations) | 10 | 17.5 | 44 | 815 | 4,451 |
| Cost* (USD) | 350 | 875 | 2,200 | 40,725 | 222,550 |
| **break-even price (USD/tCO2e)** | **0.003** | 0.15 | **0.31** | 28.4 | **182** |
| **break-even noise scale**, generous corner | **0.19×** | 0.76× | **1.76×** | 2.64× | **30.6×** |
| break-even noise scale, high corner | 0.16× | 0.65× | 1.49× | 2.26× | 25.9× |
| σ_B headroom before the claim leaves reach (G9 exposure) | 0× | 0.95× | 3.41× | 6.34× | 68.9× |
| implied deduction at Cost* (%) — *see §3, near-constant by construction* | 6.6 | 7.1 | 7.6 | 7.8 | 31.7 |
| **support-mismatch ratio** | **6,430×** | 8,660× | **9,990×** | 12,400× | **52,300,000×** |

**Out of scope: grazing / pasture (n = 38)**: break-even price 0.004 · 0.054 · **0.15** · 0.87 ·
26.8; noise scale 0.34× · 1.39× · **2.0×** · 3.0× · 13×; support mismatch 1,920× ·
**9,100×** · 203,000× (min · median · max). These are the ACCU grazing projects with the largest
credited changes (median Δ 5.9 Mg C/ha, max 17.8). Large Δ makes a claim easy to detect.

**Out of scope: land use unresolved (n = 7)**: break-even price 0.13 · 0.23 · **1.74** · 2.43 ·
3.10; noise scale 0.72× · 1.02× · **1.27×** · 2.09× · 3.44×.

**Headline design:** unpaired for 55 of 56 projects, paired for 1 (D-060's per-project choice).
**Independent re-implementation** (WP3): 0 disagreements in n_req, C\*, Cost\*, design or
implied deduction across all 56 projects, under three variants.

## 3. Implied versus applied deduction — and why the comparison changed shape

**Finding (D-068).** At the audit's own cost-optimal design, n_req is defined so that SE ≤
Δ/(t_α + t_β). The "implied deduction" k·SE/Δ is therefore bounded by **100k/(z_α + z_β)** for
every project, whatever its variance or claim: 13.3% for VM0042, 31.7% for CAR SEP, 7.8% for ACCU.
The population run shows exactly that (ACCU 5.0–7.8%, VCS 4022 13.18%, CAR1459 31.71%). The
independent re-implementation derived the same bound without seeing this code. **"Implied 13.2%"
is a property of VM0042's k and the power convention, not of VCS 4022.**

What the comparison does carry is the ratio. Divide a project's *published* deduction by its
registry's k to get the relative SE the project itself is claiming. Set that against the change
it claims:

| project | registry k | applied | own relative SE | **own Δ / MDD (90% power)** | own Δ / MDD (50% power) |
|---|---:|---:|---:|---:|---:|
| CAR1459 (RP5) | 1.028 | 11.27% | 0.110 | **2.81** | 4.65 |
| VCS 4022 — *pending expert review; dependent on decision A* | 0.4307 | 31.35% | 0.728 | **0.42** | 0.70 |

These use **none of our variance components**: only the registry's own rule and the project's
own published number. Read plainly:
- **CAR1459:** its claimed RP5 change is 2.8× the smallest change its own stated precision could
  detect at 90% power.
- **VCS 4022 (pending expert review):** on this reading its claimed change is below that
  threshold, 0.42× at 90% power and 0.70× at 50% power. Not to be quoted outside this section
  until reviewed (PI rule, 2026-11-10).

**Two conditions travel with the VCS 4022 row (PI decision A; D-072 and D-075 in the PR #21
port, Sparkxt-0318/LoAM#27):**
1. **Which rule applies.** It assumes k = 0.4307 governs VCS 4022's v2.0 crediting. On `main`
   that is verified for v2.2 only (D-057). Unmerged PR #21 reports the approved v2.0 uses the same
   rule.
2. **What the 31.35% covers.** It assumes the 31.35% is the SOC deduction. The validation report
   calls it "the final uncertainty deduction", not disaggregated by pool (verified from the
   primary document, PDF p. 147). Only the project description would settle it.

Both deductions also pool sampling with model-prediction error (VM0042 QA1, CAR SEP), so the
ratios describe each project's own stated precision, not its sampling alone. For the 54 ACCU
projects no applied deduction is published, so this comparison does not exist for them.

## 4. What these numbers do not license

- **Not a verdict on any project or registry.** Every figure is conditional on the variance table
  (one region for temporal and between-plot, G8), on research-plot support (G9, below), and on
  generous inputs. Projects are identified only in `data/audit/population_audit.csv`, with their
  public sources.
- **G9 dominates.** The in-scope support-mismatch median is ~10,000×; VCS 4022's is 25 million×.
  The σ_B headroom row shows how much larger commercial-support σ_B could be before each claim
  leaves reach: a median of 3.4× in scope, 0× for the three already outside. Nothing here bounds
  what the true factor is. WP3(iii) is the literature pass on that.
- **Not a rate.** The population is a complete count of what is auditable, which is self-selected
  toward projects that published enough. "8 of 11" describes this population and nothing wider.
- **ACCU Δ is cumulative and net.** It is the change from the baseline round to the latest, after
  ACCU's own deductions, which understates the SOC claim (conservative). Young projects with one
  small issuance have small Δ, and they are the in-scope "outside reach" cases.
- **Measurement-only projects.** 22 of the 54 ACCU projects state a measurement-only approach, so
  for them n_req applies without the QA1 upper-bound caveat. 30 state nothing.
- **No developer-level inference.** One proponent, AgriProve Solutions, is registered for 47 of the
  54 credit-issued ACCU soil projects. It therefore accounts for all 14 projects outside reach or
  within the band, and also for 33 inside reach. The category follows area and credited change.
  Its projects are smaller (median CEA 173 ha against 1,824 ha for the other seven) and younger
  (median first issuance FY2024 against FY2023), and a smaller area caps the plausible campaign.
  Fourteen of 47 against 0 of 7 is what that base rate and those sizes produce. It is not a
  finding about the developer, and no ACCU project or developer is named in the manuscript text.
