# G3 — add cores, or add plots? A bounding, not an answer

**Analysis only. No variance-table rows are written and nothing is decided.**
Script: `scripts/g3_bounding.py` → `data/processed/g3_bounding.json`.

---

## The claim being tested

The Wuest derivation (D-041, D-046) gives, per series, a **pure between-plot
variance** `v_plot` and a **residual** `v_resid`. The residual exceeds the
between-plot term at all five series, which reads as *"the variance is inside
the plots, so add cores before adding plots."*

That reading has a hole. `v_resid` is three things, and only one of them shrinks
when you take more cores:

```
v_resid  =  v_within      within-plot spatial   — REDUCIBLE by compositing
         +  v_analytical  per assay             — not reducible
         +  v_interaction plot × occasion       — not reducible
```

Write **`f` = (analytical + interaction) / residual**, the non-reducible share.
This design cannot identify `f` — one measurement per plot per occasion (D-043)
— so the honest move is to state how large `f` would have to be to overturn the
conclusion, and let a reader judge whether that is plausible.

---

## Result 1 — the naive condition, per series and jointly

Coring beats adding plots while the *reducible* part still exceeds the
between-plot term: `(1 − f)·v_resid > v_plot`.

| series | CV plot | CV residual | `f*` — coring wins while `f` below |
|---|---|---|---|
| Adams-tillage | 3.38% | 4.07% | **0.307** |
| Adams-residue | 5.24% | 5.49% | **0.089** |
| Echo | 3.35% | 9.01% | **0.862** |
| Moro | 3.80% | 5.91% | **0.587** |
| Ritzville | 3.77% | 10.66% | **0.874** |

- **"Add cores" holds at all five only if `f` < 0.089** (binding series:
  Adams-residue).
- **It fails at all five only if `f` > 0.874** (binding: Ritzville).
- Between those two numbers — which is most of the range — **the answer is
  series-dependent, and there is no single answer.**

The brief anticipated that flipping the conclusion would require it to flip at
all five independently, and that this would be a strong constraint. It is: 87%
of the residual would have to be non-reducible. But the *converse* is the more
useful finding — **holding the conclusion everywhere requires `f` < 0.089, which
is a much stronger constraint, and it is the one likely to fail.**

## Result 2 — `f` is not small, and D-036 controls how not-small

Analytical error **alone**, before any interaction term, as a share of the
residual:

| D-036 candidate | Adams-till | Adams-res | Echo | Moro | Ritzville |
|---|---|---|---|---|---|
| instrument only (`VC-ANA-001` as tabled, 1.25%) | 9.5% | 5.2% | 1.9% | 4.5% | 1.4% |
| subsampling-inclusive (Poeplau Results, 3.13%) | **59.3%** | **32.5%** | 12.1% | **28.0%** | 8.7% |

Under the narrow candidate, analytical alone already exceeds the joint threshold
of 0.089 at two series. Under the wider candidate it exceeds it at all five, and
at Adams-tillage it consumes 59% of the residual on its own.

> **G3 cannot be closed while D-036 is open.** Which analytical figure is right
> changes whether the "add cores" conclusion survives at all. That coupling was
> not visible before both were traced.

## Result 3 — the disagreement with Potash et al.

Their price list separates the cost of sampling a location (\$15) from running
an assay (\$20), which is the only reason compositing buys anything. Under a
fixed budget with `A` assays of `C` composited cores:

```
V = [v_plot + v_w/C + v_nr] / A ,   B = A·(C·15 + 20)
⟹  C* = sqrt( (20/15) · v_w / (v_plot + v_nr) )
```

The budget and the field-visit cost both cancel. The optimum depends only on the
assay-to-location price ratio and on how much noise compositing can remove.

| series | `C*` at `f` = 0 | `C*` at `f` = 0.3 | `f` at which `C*` = 1 |
|---|---|---|---|
| Adams-tillage | 1.39 | 0.97 | 0.275 |
| Adams-residue | 1.21 | 0.88 | 0.181 |
| Echo | 3.11 | 1.46 | 0.512 |
| Moro | 1.80 | 1.14 | 0.394 |
| Ritzville | 3.26 | 1.48 | 0.518 |

**Potash et al. composite 4 cores per assay.** Even at `f` = 0 — the assumption
most generous to compositing — our variance structure implies **1.2 to 3.3**.
At a modest `f` = 0.3 it implies **roughly 1**, i.e. do not composite at all.

To justify `C*` = 4 you need `v_w / (v_plot + v_nr)` = **12**. Our ratio of
`v_resid` to `v_plot` — an upper bound on that quantity, since it assumes `f` = 0
— is **1.1 to 8.0**, and only Echo and Ritzville get within sight of it.

> **So yes: our G3 numbers imply a different core-to-plot allocation than the
> nearest prior art. Ours say composite fewer cores and run more assays.**

**Three reasons to hold that loosely**, all of which need settling before it is
a claim rather than a flag:

1. **Different scales.** Our `v_plot` is between replicate experimental units in
   one experiment, 3.6–9 m wide, on deliberately uniform fields. Their
   between-location term is within a 25 ha commercial field. If theirs is larger
   than ours — which is likely — their `C*` is correspondingly smaller than the
   4 they use, and the disagreement widens rather than closes.
2. **Different constructs.** Their dominant within-field term is *relocation*
   (σ_r = 5 Mg/ha) against lab (σ_l = 2 Mg/ha), a variance ratio of 6.25 — the
   same order as our 1.1–8.0, but not the same quantity. Whether relocation
   error averages down with compositing is a modelling choice we have not
   verified in their SI.
3. **`f` is unidentified.** Everything above is conditional on it, and Result 2
   shows how much that matters.

---

## What this does not settle

`f` is the whole question and this design cannot measure it. Separating
within-plot spatial from plot × occasion interaction needs **replicate cores per
plot per visit**, which no source we hold provides. That is the experiment G3
actually wants, and it is small: one site, one season, 3+ cores analysed
separately per plot per month.

**Recommendation for the PI, not acted on:** treat "add cores before adding
plots" as **unproven and probably too strong**. The defensible version is
narrower — *the within-plot term is large enough that a single core per plot is
likely to be the wrong design, but the optimum is nearer 1–3 cores per assay
than the 4 used by the closest published work, and it cannot be pinned down
until D-036 closes and `f` is measured.*
