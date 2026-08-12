# HANDOFF — overnight autonomous run, 2026-08-10

Written continuously during the run. Newest task last.

**Hard rules honoured:** no merges to main, every task on its own branch with a
DRAFT PR, no D-NNN closed that needs judgement, no row promoted to `baseline`,
no implementation ahead of a decision.

---

## TASK 1 — D-036 + basis field — **COMPLETE**
Branch `claude/d036-analytical` · PR: see below · `137 passed`

### D-036: 4x -> 1.20x. STAYS OPEN.

> ⚠️ **SUPERSEDED 2026-08-12.** D-036 is now **CLOSED**. The residual described
> below as "internal to Potash" was a typographical error in their printed
> reference soil, confirmed by the author: the intended values are 1.5% SOC and
> 1.0 g/cm3, i.e. **45 Mg C/ha, not 90**, on which their stated errors imply
> sigma_l = 2.0125 against Table 1's 2. The recommendation below (which lab
> error `analytical` should carry) is carried forward as **D-054, open**. This
> section is left as written because it is a dated record of a run. See D-036
> and D-054 in DECISIONS.md for what is current.

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


## TASK 3 — detectability literature — **COMPLETE**
Branch `claude/sources-detectability` · `136 passed` · no rows written

All five citations confirmed against Crossref. Availability checked via
Unpaywall. Two retrieval attempts each; **no paywall circumvented**.

| paper | status | outcome |
|---|---|---|
| von Haden et al. 2020, GCB 26:3759 | green OA | **RETRIEVED** and read (OSTI accepted manuscript) |
| Smith 2004, GCB 10:1878 | bronze OA | **403 from Wiley bot protection** — free to read, a browser will open it |
| Bradford et al. 2023, Geoderma 440:116719 | **gold OA** | **403** from ScienceDirect and DOAJ — openly licensed, a browser will open it |
| Saby et al. 2008, GCB 14:2432 | closed | no OA location |
| de Gruijter et al. 2016, Geoderma 265:120 | closed | no OA location |

**The one real find: von Haden Table 1 is stronger than what component 6
currently rests on.** Mean absolute percentage error in SOC stock, fixed depth
vs equivalent soil mass, under simulated ±2.5 cm compaction/expansion:
**ESM 0.2–1.1%, FD 2.1–23.2%.** Our `VC-BDC-001..004` carry 17 / 16.2 / 8 / 6%
from Fowler 2023 — von Haden's FD range brackets all four, from an independent
study with an explicit ESM comparison. Also supplies a citation for the
bulk-density-change mechanism (5–20% after land-use change, tillage, residue
addition) that our BDC rows currently assert uncited.

⚠️ **Table 1's column alignment was recovered from PDF text extraction and needs
visual confirmation against the typeset version before any number is tabled.**
The range is unambiguous; the mapping of values to bulk-density rows is not.

**Blockers, logged per rule 6:** Smith 2004 and Bradford 2023 are both *openly
readable* and both blocked by bot protection, not by a paywall. Two attempts
each (publisher + alternate legitimate host). **These are one browser click for
a human** — the highest-value five minutes available to the PI in this whole
handoff, since Bradford 2023 is the paper Potash et al. are answering and
therefore the other half of the argument D-037/D-038 position against.


## TASK 4 — Phase 1 reconnaissance — **COMPLETE**
Branch `claude/phase1-recon` · `docs/phase1_design.md` · **no implementation**

pyRothC installed and smoke-tested **outside the repo**, in a scratch directory.
Not added to `pyproject.toml`. Nothing executable was written.

**Verdict: it works, it is cleanly licensed, and it is probably not what this
project needs.** CC0, 240 lines, deps numpy/pandas/scipy only, **last release
2023-06-22**. Unmaintained — but RothC 26.3 is a frozen published model, so
there is no upstream to track. If used, **vendor it**.

### Three findings that matter more than the install

**(a) RothC's `evaporation` input is D-039 all over again.** It needs *open-pan
evaporation*; WorldClim does not publish it. Substituting a computed
Penman/Hargreaves PET is **exactly the substitution D-033 refuses and D-039
documents as a finding** — made by us, inside the model this time. Sourceable,
but it is a decision, not a detail.

**(b) The premise is at real risk through ONE channel, and it is cheap to
close.** Most of our components are relative (`cv_pct`); converting to an
absolute SD needs a mean stock, and **if that mean comes from RothC's simulated
trajectory, MDC inherits RothC's level error.** Mitigation: convert using an
*observed* mean stock (NAPESHM/Wuest site means), never the simulated one, and
enforce it — *no variance component may read a stock from the truth generator*.
That is the natural successor to D-032 / D-051 / D-052.

**(c) RothC is single-layer, so it cannot generate the truth component 6
measures error against.** Fixed-depth vs ESM bias has to be imposed as a separate
observation-model step from our `VC-BDC` rows. Relevant to task 3's von Haden
find.

### The uncomfortable conclusion, stated for the PI to rule on

If MDC is defined as a pure noise property — which is what our own premise
says it is — **Phase 1 may not need a carbon model at all.** A stated change
rate plus the variance structure is sufficient. RothC would then be supplying
plausible values for one scenario parameter, a much smaller job than "truth
generator" implies, and one a table of published effect sizes could also do.

Six open questions are listed explicitly at the end of the design doc.

---

# END OF RUN

Four tasks, four branches, four **draft** PRs, all CI green. Nothing merged.
No D-NNN closed that needed judgement. No row promoted to `baseline`. No
implementation built ahead of a decision.

| task | branch | PR | status |
|---|---|---|---|
| 1 · D-036 + `basis` | `claude/d036-analytical` | **#7** | complete |
| 2 · G3 bounding | `claude/g3-cores-vs-plots` | **#8** | complete |
| 3 · detectability literature | `claude/sources-detectability` | **#9** | complete, 2 blocked |
| 4 · Phase 1 recon | `claude/phase1-recon` | **#10** | complete, design doc only |
| — · this handoff | `claude/handoff` | **#11** | — |

**Nothing was time-boxed out.** All four finished inside their boxes.

## ⚠️ Merge mechanics — read before merging anything

1. **`HANDOFF.md` will conflict.** Each task branch was cut from `main` and each
   carries only its own section, because `>>` created a fresh file on each. **This
   branch has the superset — take this version on any conflict.**
2. **PR #7 adds D-052, PR #8 adds D-053.** Both touch the `DECIDED_DECISIONS`
   tuple in `src/loam/decisions.py` and the Decision status table in
   `DECISIONS.md`. Take both lines. D-053 deliberately skips 052 rather than
   renumbering across branches.
3. **#7 changes the schema** (adds required `basis`, 48 → 49 columns). Merging it
   after #8/#9/#10 is fine — none of those touch the schema or the YAML rows.
   Merging **#7 first** is marginally cleaner.

## Blockers hit, with evidence

| blocker | evidence | attempts |
|---|---|---|
| **Smith 2004** unreachable | HTTP 403, Wiley bot protection. Unpaywall says **bronze OA** — free to read | 2 |
| **Bradford 2023** unreachable | HTTP 403 from ScienceDirect *and* DOAJ. Unpaywall says **gold OA** — openly licensed | 2 |
| Saby 2008, de Gruijter 2016 | Unpaywall: closed, no OA location anywhere | 1 each (definitive) |
| von Haden Table 1 alignment | PDF text extraction garbled column mapping; range recovered, per-row mapping not | flagged, not guessed |

**The two 403s are access walls, not paywalls, and both papers are openly
readable. A browser opens them in one click — that is the highest-value five
minutes in this handoff**, because Bradford 2023 is the paper Potash et al. are
answering and therefore the other half of the argument D-037/D-038 position us
against.

## Decisions I did NOT make, with recommendations

1. **D-036 — which analytical error should `VC-ANA-001` carry?**
   *Recommend:* add a subsampling-inclusive row (3.13% SD, concentration) as the
   baseline, demote `VC-ANA-001` to the instrument-only floor. No monitoring
   programme re-measures the same milled aliquot, and understating analytical
   error is anti-conservative for the Phase 5 audit (D-023).
   *Against:* it is the only row isolating the instrument, and D-027 prefers
   decomposed terms.
2. **Potash's internal inconsistency** — `σ_l` = 2 Mg/ha vs the 4.02 their own
   stated relative errors imply. *Recommend:* raise it with the authors; it is
   not resolvable from the text and it is worth a footnote either way.
3. **`VC-BPS-005` vs `VC-BPS-006/007–011`** — concentration and stock CVs
   coexisting as baselines. *Recommend:* keep both, but make the OSSE declare one
   basis per run. Recorded in `MIXED_BASIS_BY_DESIGN`, not resolved.
4. **G3 / add-cores-vs-add-plots.** *Recommend:* retire the flat claim. The
   defensible version is "a single core per plot is likely wrong, but the optimum
   is nearer 1–3 cores per assay than Potash's 4, and cannot be pinned down until
   D-036 closes."
5. **Phase 1 engine.** *Recommend:* decide what the truth generator is FOR before
   choosing one. Six explicit questions at the end of `docs/phase1_design.md`.
6. **`VC-BPS-004`** (an MDC filed as a variance component) — allowlisted in PR #6,
   still not re-filed. It may deserve its own `use_as`, since an MDC is a project
   *output*.

## Things that contradict a standing assumption

1. **Potash et al. 2025 was never paywalled.** `sources.md` listed it as "to
   obtain"; it is open-access in ERL and one Crossref query found it. Second time
   this pattern has cost us — Wuest's dataset was public domain while we queued
   the PDF. **Check for an open version before queueing a retrieval.**
2. **The D-036 "4× discrepancy" was largely our own filing choice**, not a
   disagreement in the literature. Poeplau reports two lab errors; we tabled the
   narrower one and compared it to Potash's wider one for two rounds.
3. **"Add cores before adding plots" does not survive contact with the
   arithmetic.** Holding it at all five series needs the non-reducible share of
   the residual below 9%; analytical error alone can exceed that.
4. **G3 and D-036 are coupled** — G3 cannot close while D-036 is open. Neither
   entry knew about the other before both were traced.
5. **RothC needs open-pan evaporation, which WorldClim does not publish.** The
   PET problem that produced D-039 reappears inside the Phase 1 engine.
6. **Our own premise has a live leak.** If CV-based components are scaled by a
   *simulated* mean stock, MDC inherits the truth generator's level error. Cheap
   to close, but it needs an enforced rule.

## What I would do next, in priority order

1. **Open Smith 2004 and Bradford 2023 in a browser** (5 minutes, unblocks #9).
2. **Settle D-036** — it gates G3, and the evidence is now assembled.
3. **Merge #7 first**, then #8, #9, #10, taking this branch's `HANDOFF.md`.
4. **Answer question 1 in `docs/phase1_design.md`** — is MDC a pure noise
   property? Everything else about Phase 1 follows from it.
5. **Confirm von Haden Table 1 visually** and decide whether component 6 gains a
   corroborating row.
6. **Decide `VC-BPS-004`'s home** — an MDC is not a variance component.
7. Lower priority, unchanged: KBS written permission (needs a human email),
   external PET for the 87 unclassified NAPESHM sites, the LUCAS report (G6).
