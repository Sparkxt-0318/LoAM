
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
