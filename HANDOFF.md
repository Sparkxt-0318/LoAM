
---

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
