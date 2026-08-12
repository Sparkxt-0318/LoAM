# HANDOFF — overnight autonomous run, 2026-08-12

Written continuously. Newest task last. **Nothing merged. All PRs draft.**

## Branch stack, and why it is a stack

`origin/main` carries everything through PR #11. Every branch below is cut from
the previous one rather than from `main`, because each depends on the last
(D-057 needs the corpus; the design doc needs D-057). **Merge in the order
listed** and each PR's diff stays readable.

| # | branch | PR | contains |
|---|---|---|---|
| 1 | `claude/loam-d036-resolution-keieap` | **#13** | D-036 closed, D-054 opened, D-055 (inorganic carbon), correspondence dated |
| 2 | `claude/loam-registry-corpus` | **#14** | D-056, Phase 5 corpus, gap analysis |
| 3 | `claude/loam-vm0042-primary` | **#15** | D-057, VM0042 read from primary |
| 4 | `claude/loam-inverted-audit-design` | **#16** | Phase 5 inverted-audit design doc |
| 5 | `claude/loam-estimator-repair` | **#17** | D-058, estimator repair |

## ⚠️ PR #12 must be resolved BEFORE any of the above

PR #12 reverts the D-053/G3 work: it deletes `docs/g3_bounding.md`,
`scripts/g3_bounding.py`, removes D-053 from `DECISIONS.md` and from
`DECIDED_DECISIONS`, and restores the older G3 gap-row text. Its base is
`0ba64fa`, **three merges behind `origin/main`**.

Every branch above references D-053 — D-054's gating text, the G3 gap row,
D-056, D-057, D-058. If #12 merges, those become dangling references.

**Recommendation: close #12 without merging.** Two reasons.
1. What #12 appears to object to is already what D-053 *says*. D-053's own
   recommendation is "retire the flat 'add cores' claim"; it is a bounding
   analysis, not a claim.
2. **The registry corpus has since corroborated it.** CAR1459 collects **one core
   per assay**, uncomposited, at continental scale — against Potash's 4 and
   D-053's computed optimum of 1.2–3.3. Reverting D-053 would delete the analysis
   the real world just agreed with.

If the intent is to soften D-053, that is an amendment to D-053, not deletion of
the script and the doc.

---

## TASK 1 — ESTIMATOR REPAIR — **COMPLETE** (~1h of a 2h box)
Branch `claude/loam-estimator-repair` · **D-058** · `176 passed`

**New module `src/loam/logvar.py`** — debiased, information-weighted
log-variance estimation. `psi` and `psi'` in **exact closed form** (nu is always
an integer, so nu/2 is an integer or half-integer), keeping `src/loam`
standard-library only so the guard runs in CI. Verified against scipy to
**1.8e-15** across nu = 1..101, against both recurrences, and by seeded Monte
Carlo.

**D-040's joint model repaired and re-run. The conclusion HOLDS.**

| | retired spec | repaired |
|---|---|---|
| treatments / sites | 80 / 19 | **135 / 26** |
| country split | 75 USA / 5 Mexico | **75 USA / 60 Mexico** |
| `log_mean_soc` | +0.423 (t=+2.25) | +0.801 (t=+2.37) |
| `sand_frac` | +0.915 (t=+2.25) | +1.720 (t=+3.06) |
| R² | 0.0935 | **0.0722** |

Covariates explain **less** under the correct estimator. Invariance unchanged.
D-029's log-log slope reproduces at **1.223**.

**The brief's reasoning is backwards, and checking it mattered.** Excess noise
*inflates* SEs and *depresses* R², both of which favour a null — so a noisy
estimator makes a null **easier** to reach, not harder. Correcting it is a test
D-040 could have failed. It passed.

**A D-040 caveat is retired and replaced.** "75 of 80 treatments from the USA" is
no longer true of the repaired fit (75/60). It is replaced, not removed: the
re-admitted Mexican treatments are exactly the 2-replicate ones, and `sand_frac`
nearly doubles when they enter — which is what a country effect wearing a texture
hat looks like. D-040 check 1c's prohibition stands.

**Precision on the instability.** The `t = -0.37, +4.58, -4.53, +0.75` sequence is
the **inorganic-carbon** coefficient across D-055's four tiers, not a coefficient
D-040 reported. On D-040's own covariates the retired spec is comparatively well
behaved. **D-040's published numbers were never the ones flipping.**

**Guard:** `tests/test_logvar_estimator.py` fails if the retired idiom returns
outside a two-file allowlist, and a second test requires allowlisted files to
label it `RETIRED`. **That second test caught a real gap on its first run.**

**Repo audit:** `ic_conditioning.py` re-routed through the shared module;
`derive_temporal.py` examined and is **not** the same failure mode (nu ≈ 29 per
plot, roughly equal, consumed by rank tests). `d029_raw_slope` deliberately left
alone — different estimator, different purpose, and D-029 rests on it.
**Recommendation: leave it; debiasing it re-opens D-029.**
