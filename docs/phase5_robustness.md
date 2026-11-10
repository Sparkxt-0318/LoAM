# Phase 5, WP3: robustness of the audit

Decision: D-069. Three checks: (i) an independent re-implementation, diffed; (ii) the sensitivity
of every headline number to the three choices most open to challenge; (iii) a literature pass on
G9, how between-location variance changes with spatial support.

---

## (i) Independent re-implementation — 0 disagreements

**What was done.** A separate agent was given a written specification of the method:
- the five component CVs and the reference stock;
- the paired and unpaired S(C) formulas;
- VM0042 Eq. (2) with its t-quantiles and α/power;
- the cost function and the C = 1–30 sweep;
- the headline-design rule;
- the implied-deduction formula.

It was forbidden to read `src/loam/inverted_audit.py`, `src/loam/student_t.py`, their tests, the
runner, or any processed output. It wrote `scripts/independent_audit_reimpl.py` from scratch,
using scipy's t-distribution where the package uses its own pure-Python one. It solved n_req by
integer bracketing on g(n) = n − RHS(n), not by the package's bisection, and self-checked that
against a brute-force scan on 400 random cases.

**Disclosed contamination.** While looking up D-060/D-061, its search printed one changelog line
from `DECISIONS.md` giving VCS 4022's implied 13.2% and unpaired headline. It saw that number
before running its code, and said so. Its formulas follow the specification, not that number.
The I/O default paths were changed afterwards by the commissioning session; no other line was
touched, and the file says so.

**Result** (`python scripts/compare_independent_reimpl.py data/audit/reimpl_cases.json <out>`):

| variant | cases | disagreements in n_req, C\*, S, Cost\*, headline design, implied deduction |
|---|---:|---:|
| default | 56 × 2 designs | **0** |
| relocation ÷ √2 | 56 × 2 designs | **0** |
| assay cost $60 (ratio 4) | 56 × 2 designs | **0** |

That covers 336 optimisations, including one exact paired/unpaired cost tie (ERF162497), which
both implementations break toward paired. The agent also derived, unprompted, that the implied
deduction at the optimum is bounded by k·100/(z_α + z_β) and lies at 0.645–0.9997 of that bound
across the population. That is the D-068 finding, reached independently.

**What this does and does not establish.** The package computes what the method says. It does not
establish that the method's inputs are right: both implementations share the same component
values and conventions by construction. Those are what (ii) and (iii) address.

## (ii) Sensitivity — the categories hold; two n_req figures move by more than 2× under a forced paired design

`python scripts/sensitivity_audit.py` (all 56 projects × 10 variants; full output
`data/audit/sensitivity.csv`). Baseline: per-project cheaper design (D-060), relocation undivided
(D-061), $15 per location and $20 per assay (ratio 1.33), generous corner.

| quantity | baseline | force paired | force unpaired | reloc ÷√2 | reloc ÷√2 + paired *(design-doc convention)* | assay $5 (0.33) | assay $10 (0.67) | assay $40 (2.67) | assay $80 (5.33) | central inputs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **in scope: inside / band / outside** | **8 / 0 / 3** | 6 / 0 / 5 | 8 / 0 / 3 | 8 / 0 / 3 | 7 / 1 / 3 | 6 / 0 / 5 | 7 / 0 / 4 | 8 / 0 / 3 | 8 / 0 / 3 | 8 / 0 / 3 |
| grazing: inside / band / outside | 30 / 2 / 6 | 26 / 0 / 12 | 30 / 2 / 6 | 30 / 2 / 6 | 29 / 1 / 8 | 26 / 3 / 9 | 29 / 3 / 6 | 31 / 2 / 5 | 32 / 1 / 5 | 30 / 0 / 8 |
| in scope: median break-even price | $0.31 | 0.47 | 0.31 | 0.31 | 0.38 | 0.20 | 0.25 | 0.42 | 0.62 | 0.36 |
| in scope: max break-even price | $182 | 298 | 182 | 182 | 226 | 120 | 145 | 242 | 342 | 216 |
| in scope: median noise scale | 1.76× | 1.15× | 1.76× | 1.76× | 1.58× | 1.37× | 1.37× | 1.99× | 1.99× | 1.61× |
| grazing: median break-even price | $0.145 | 0.206 | 0.145 | 0.145 | 0.171 | 0.089 | 0.111 | 0.203 | **0.299 ⚠** | 0.167 |
| VCS 4022: n_req (C\*) | 161 (2) | **374 (1) ⚠** | 161 (2) | 161 (2) | 200 (2) | 265 (1) | 161 (2) | 126 (3) | 109 (4) | 191 (2) |
| VCS 4022: break-even price | $0.0030 | 0.0048 | 0.0030 | 0.0030 | 0.0037 | 0.0020 | 0.0024 | 0.0039 | 0.0056 | 0.0035 |
| VCS 4022: category | inside | inside | inside | inside | inside | inside | inside | inside | inside | inside |
| CAR1459: n_req (C\*) | 4,451 (2) | **10,430 (1) ⚠** | 4,451 (2) | 4,451 (2) | 5,543 (2) | 7,371 (1) | 4,451 (2) | 3,478 (3) | 2,699 (**5 ⚠**) | 5,292 (2) |
| CAR1459: break-even price | $0.21 | 0.34 | 0.21 | 0.21 | 0.26 | 0.14 | 0.17 | 0.28 | 0.39 | 0.25 |
| CAR1459: category | inside | inside | inside | inside | inside | inside | inside | inside | inside | inside |
| applied / implied (VCS 4022; CAR1459) | 2.378; 0.356 | 2.368; 0.355 | = | = | 2.375; 0.356 | 2.371; 0.355 | = | 2.380; 0.356 | 2.387; 0.356 | 2.375; 0.355 |

⚠ = moves by more than 2× from baseline. Four entries do:
- **VCS 4022 and CAR1459 n_req under a forced paired design** (2.3× each). This is the size of
  D-060's choice. Forcing the more expensive design costs more samples, but the break-even price
  moves only 1.6× and neither project changes category.
- **CAR1459's C\*** at the highest assay cost (2 → 5). This is an intermediate: when assays cost
  more, compositing pays.
- **The grazing median break-even price** at the highest assay cost (2.06×).

**No in-scope category count, median price or VCS 4022/CAR1459 category moves by 2× under any
variant.**

**What this establishes.**
1. **The qualitative result is robust to the three challenged choices.** In every variant most
   in-scope projects are inside reach (6–8 of 11), every outside-reach count is 3–5, and VCS 4022
   and CAR1459 stay inside reach with break-even prices below $0.01 and $0.40 respectively.
2. **Relocation scale (D-061) has no effect on its own**, because 55 of 56 headline designs are
   unpaired, and σ_R does not enter the unpaired formula. It matters only combined with a paired
   design: the design doc's own original convention, which moves VCS 4022's n_req to 200.
3. **The paired/unpaired choice (D-060) is the most consequential of the three.** Forcing paired
   moves two in-scope projects from inside to outside reach, and doubles the grazing
   outside-reach count.
4. **Cost ratio** moves break-even prices roughly in proportion, within 0.6–2×. A cheaper assay
   pushes C\* to 1 and needs more locations. **Absolute cost scale** is not a variant: n_req and
   C\* do not depend on it, so break-even prices scale exactly linearly with it, and categories
   do not move.
5. **Central-estimate inputs** (sensitivity only, per the standing rule) change no in-scope
   category and move prices by 1.1–1.2×.
6. **The own-deduction ratio** (applied ÷ implied) is insensitive to every variant (±0.4%). It
   does not use our variance inputs, beyond n's degrees of freedom.

## (iii) G9 — how between-location variance changes with support (D-070)

Full literature report: [`g9_support_literature.md`](g9_support_literature.md). It has 31 sources,
each with access level (full text / abstract / cited / title) and locator, an access-wall log,
and unverified leads. Most publisher hosts were walled from this environment, so only four
sources were read in full. The verdict is weighted accordingly.

**Stock: the direction can be bounded — between-location σ_B is LARGER at commercial support
than the 3.1% research-plot input.** Evidence is moderate. Theory and every source found agree,
but no study compares the two on the same ground.
- **Support.** The input is a variance between 0.02 ha plot means, which averages out
  short-range structure. More than half of SOC variance sits at 5–60 m or within 1 ha
  (Robertson et al. 1997, abstract; de Blécourt et al. 2017, full text).
- **Extent.** Variance cannot fall as extent grows. The CV of SOC stock rises from 5% to 35%
  across scales (Goidts et al. 2009, abstract).
- **Magnitude.** Single 0–30 cm cores within 1–2 ha cropland sites give **5, 10 and 14%** CV
  (Schrumpf et al. 2011, full text, Table 2). That is ~1.5–5× the input as an SD, and probably
  a lower bound for larger fields. Across fields or regions the factor is ~5–10×, with low
  confidence.

**Change: the direction cannot be bounded.**
- On 80 commercial fields over a year, between-field variability in *change* was >7× smaller
  (as an SD) than in level (Polussa et al. 2026, abstract).
- In a national forest network over 10 years, change variance was at or above stock variance,
  with regression to the mean (Buchkowski et al. 2026, full text).
- Status and change are different variables (Lark 2009, abstract).

**What this does to the audit — a scenario bracket, no distribution assumed.** The literature's
endpoints are applied as multipliers on σ_B, and the design is re-chosen per project
(`python scripts/sensitivity_audit.py --g9`):

| σ_B multiplier | in scope: inside / band / outside | grazing | VCS 4022 | CAR1459 |
|---|---|---|---|---|
| 1 (baseline) | **8 / 0 / 3** | 30 / 2 / 6 | inside, n 161, $0.003 | inside, n 4,451, $0.21 |
| 1.5 | 6 / 2 / 3 | 29 / 1 / 8 | inside, n 200, $0.004 | inside, n 5,546, $0.26 |
| 5 | **6 / 0 / 5** | 26 / 0 / 12 | inside, n 374 (paired), $0.005 | inside, n 10,430 (paired), $0.34 |
| 10 | 6 / 0 / 5 | 26 / 0 / 12 | as ×5 | as ×5 |

From σ_B ≈ 2.1× (where 2σ_B² = σ_R²), the paired design is cheaper, **and the paired formula
contains no σ_B**. So ×5 and ×10 reproduce §(ii)'s forced-paired column exactly. The stock side
of G9 cannot push the audit below that floor:
- in scope, **6 of 11 inside reach and 5 outside**;
- VCS 4022 and CAR1459 inside reach throughout.

**What G9 now means.** The floor rests on the paired design's change-variance terms: relocation
(`VC-REL-001`, itself a field resampling error from Poeplau et al. 2022), within-plot,
analytical and temporal. Those are precisely the terms whose support-scaling the literature
cannot bound. **G9 is narrowed from "unknown in either direction" to "bounded for stock;
unbounded for change, which is what the paired floor depends on".** It is not closed.

**The study that would close it** is specified in the literature file (§2.2, §3). It is a nested
design (cores, cells, research plots, fields, farms) around one research site, with paired
georeferenced remeasurement, ESM, the same lab, duplicate cores at 0–2 m offsets, and REML
variance components of *change* at each level.
