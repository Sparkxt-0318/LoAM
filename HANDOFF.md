# HANDOFF — overnight autonomous run, 2026-08-10

Written continuously during the run. Newest task last.

**Hard rules honoured:** no merges to main, every task on its own branch with a
DRAFT PR, no D-NNN closed that needs judgement, no row promoted to `baseline`,
no implementation ahead of a decision.

---

## TASK 1 — D-036 + basis field — **COMPLETE**
Branch `claude/d036-analytical` · PR: see below · `137 passed`

### D-036: 4x -> 1.20x. STAYS OPEN.

Both primary sources now held. **Potash et al. 2025 is Environmental Research
Letters, doi:10.1088/1748-9326/ada16c, OPEN ACCESS** — it was never paywalled,
only unlocated. (Standing assumption contradicted: `docs/sources.md` listed it
as "to obtain". It took one Crossref query.)

**The gap was ours, not the literature's.** Poeplau reports TWO laboratory
errors and we tabled the narrower one:
- analytical, 1.2% MAPE — two technical replicates of the *same milled sample*
- subsampling, 2.5% MAPE — second aliquot of the same *sieved* sample, re-milled
  and re-analysed, so it CONTAINS the analytical step

| comparison | ours | Potash | ratio |
|---|---|---|---|
| as tabled (analytical only, no BD) vs their concentration term | 1.25% | 4% | **3.2x** |
| Poeplau subsampling-inclusive vs their concentration term | 3.13% | 4% | **1.28x** |
| + their 2% bulk-density term, stock basis | 3.72% | 4.47% | **1.20x** |

**Residual is INTERNAL to Potash.** At their own reference soil (0-30 cm, 2%
SOC, BD 1.5) the stock is 90 Mg C/ha. Their stated 4% + 2% combine to 4.47% =
**4.02 Mg/ha**, but they adopt **sigma_l = 2**. Their sentence and their
parameter disagree by 2x. Cannot be resolved from the text.

**Decision NOT made (rule 2). My recommendation:** add a second analytical row
carrying the subsampling-inclusive error (3.13% SD, concentration) and make it
the baseline, demoting VC-ANA-001 to a sensitivity row recording the
instrument-only floor. No monitoring programme re-measures the same milled
aliquot; the narrow figure understates what a real design incurs, and
understating analytical error is anti-conservative for the Phase 5 audit
(D-023). Argument against: VC-ANA-001 is the only row isolating the instrument,
and D-027 prefers decomposed terms. **PI's call.**

**Also found:** VC-ANA-001 cites Poeplau's Discussion ("~1%", -> SD 1.25%) when
the Results give the same quantity as 1.2% MAPE (-> SD 1.50%). We took the
rounded number over the precise one. Not changed — it is inside the same open
decision.

### basis field: the PR #6 guard did NOT cover it. Gap was real.

`quantity_definition` resolves the AXIS. Basis (concentration / stock /
stock_change / variance_share / proportion / distance) is orthogonal and
dimensionally silent. Added as a required enum with `tests/test_basis.py`:
units-vs-basis consistency, plus the teeth — **all baseline dispersion rows in
one component must share a basis**.

**Backfill found one live mismatch, a baseline collision:** `VC-BPS-005` is a
**concentration** CV while `VC-BPS-006` and `VC-BPS-007..011` are **stock** CVs.
All seven are baselines, all `cv_pct`/`pct`. D-020 forbids treating one as the
other — in prose, with no enforcement until now. Recorded in
`MIXED_BASIS_BY_DESIGN` rather than resolved: both are wanted, and choosing is
the PI's call. D-040 already showed they are not interchangeable even
approximately (stock 11.456% vs concentration 11.897% on a common sample).

Structural rows (`bias_pct`, `range`, `proportion_pct`) are exempt by design —
they modify a budget rather than entering one.

---

## TASK 2 — G3 bounding — **COMPLETE**
Branch `claude/g3-cores-vs-plots` · `136 passed` · analysis only, no rows

`scripts/g3_bounding.py` → `data/processed/g3_bounding.json`, written up in
`docs/g3_bounding.md`, logged as **D-053**.

**The headline reverses the expected framing.** "Add cores" holds at all five
Wuest series only if the non-reducible share `f` of the residual is **below
0.089**; it fails at all five only if `f` > 0.874. The brief expected the flip
to be hard — it is — but the *useful* constraint is the other one, and it is
the one likely to fail.

**G3 cannot close while D-036 is open.** Analytical error ALONE is 1.4–9.5% of
the residual under the instrument-only candidate and **8.7–59.3%** under the
subsampling-inclusive one. At Adams-tillage the wider candidate eats 59% of the
residual by itself. This coupling was invisible until both were traced.

**Quantitative disagreement with Potash.** Under their own price list the
budget-optimal composite is `C* = sqrt((20/15)·v_w/(v_plot+v_nr))` — budget and
field-visit cost cancel. Ours gives **1.2–3.3 cores per assay at f=0**, ~1 at
f=0.3. **They use 4.** Justifying 4 needs a variance ratio of 12; ours is
1.1–8.0. Held loosely — different scales, different constructs (their dominant
within-field term is relocation, not within-plot spatial), and `f` unidentified.
Note the scale difference *widens* the gap rather than closing it.

**Decision NOT made (rule 2).** Recommendation: retire the flat "add cores"
claim; the defensible version is "a single core per plot is likely wrong, but
the optimum is nearer 1–3 than 4, and cannot be pinned down until D-036 closes".

**What would settle it:** replicate cores per plot per visit, analysed
separately. One site, one season. No source we hold does this.

### ⚠ MERGE ORDER NOTE
PR #7 adds **D-052**, this PR adds **D-053**. Both touch the same two places —
the `DECIDED_DECISIONS` tuple in `src/loam/decisions.py` and the Decision status
table in `DECISIONS.md`. Expect a small conflict on the second merge; take both
lines. D-053 deliberately skips 052 rather than renumbering.
