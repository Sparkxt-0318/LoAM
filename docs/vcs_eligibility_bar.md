# The VCS eligibility bar, and what it concedes

**Phase 5 headline result. Logged as D-061.** Primary sources only.
No variance-table row is written or implied by this document.

This is a **program-level** result. It is not about VM0042, and it should not be
read as one — VM0042 is the worked example, not the subject.

---

## 1. The rule

*VCS Methodology Requirements* v4.4 (updated 4 October 2023), §2.4 *Uncertainty*,
printed p. 13, final bullet. Verbatim:

> "*Where the half-width of the two-sided 90 percent confidence interval exceeds
> **100 percent** of the reduction and removal estimate, **the project is not
> eligible for crediting**.*"

Same section, printed p. 12, the deduction procedure that VM0042 §8.6.4 and every
other §2.4-implementing methodology defers to. Verbatim:

> `Discount factor = ( Uncertainty / t_{α=10%} ) × t_{α=66.6%}`
>
> `Uncertainty` = "*Half-width of the 90% confidence interval as a percentage of
> the mean estimate*"
> `t_{α=10%}` = "*t-value for the two-sided 90% confidence interval,
> approximately **1.6449***"
> `t_{α=66.6%}` = "*t-value for a one-sided 66.67% confidence interval,
> approximately **0.4307***"

Verra's own worked example, printed p. 12, confirms the arithmetic:

> "*The project estimates the discount factor as follows: Discount factor =
> 32.9% / 1.6449 * 0.4307 = 8.6%.*"

## 2. The inversion

The 90% half-width is `1.6449 · SE`, so the first factor of the discount is
`σ_rel` exactly, and the published deduction is

```
UNC = 0.4307 · σ_rel                     σ_rel = SE(Δ)/Δ
```

The eligibility bar is `1.6449 · SE > Δ`. Therefore:

```
not eligible   ⟺   σ_rel > 1/1.6449 = 60.79%   ⟺   UNC > 26.18%
```

And with the minimum detectable difference as the methodologies themselves define
it (`MDD = (t_α + t_β)·SE`, VM0042 §8.2.1.3 Eq. 2, FAO 2019), the bar sits at

```
Δ / MDD  =  0.4307 / (1.959964 × 0.2618)  =  0.839
```

## 3. The claim

> ### The VCS program permits crediting of claims down to 84% of their own 50%-power minimum detectable difference.

Not our threshold. Not our power convention. Not our variance components.
**Verra's rule, inverted through Verra's own constant.**

A project may be credited while claiming a change it would detect less than half
the time in its own design. The bar does not sit at parity with the detection
floor — it sits *below* it, and the gap is 16%.

Everything LoAM has built — the variance table, the components, the invariance
result — is **absent from that sentence**. It is arithmetic on two numbers the
VCS program publishes about itself.

## 4. The generalisation — this is not a VM0042 finding

**`k = 0.4307` is a VCS program-wide constant.**

It is defined in the *Methodology Requirements*, not in any methodology. VM0042
§8.6.4 does not set it; it defers to §2.4 and reproduces the value. Any VCS
methodology implementing §2.4 inverts identically:

- one constant, `0.4307`, fixed at program level;
- one threshold, `UNC > 26.18%`, fixed at program level;
- one input per project — **the deduction it already publishes.**

No design disclosure, no sampling parameters, no variance estimate, no
methodology-specific reading. **The addressable surface is every VCS project that
publishes an uncertainty deduction under §2.4**, which is a far larger population
than VM0042's, and the reason this result does not belong inside a VM0042
document.

§2.4 also sets the floor that bounds that population from below: where the 90%
half-width is unlikely to exceed 10% of the estimate, "*methodologies may exclude
random uncertainty*" — so a methodology below the floor publishes no deduction to
invert.

## 5. VCS 4022, and the limit of what can be concluded

**Framing preserved from the source finding. It is not to be sharpened.**

VCS 4022 publishes an uncertainty deduction of **31.35%**. Inverted:

| quantity | value |
|---|---:|
| implied `σ_rel` | 72.79% |
| **implied 90% CI half-width** | **119.7% of the ERR estimate** |
| the §2.4 bar | 100% |
| exceedance | **19.7 points** |

VM0042 v2.0 §8.6.4 points to "*the latest version of the VCS Methodology
Requirements Section 2.4*" but **does not reproduce the bar**. The bar postdates
VM0042 v2.0's approval (May 2023) and predates this project's validation
(December 2024, VCS Standard v4.5).

> **Either** the bar binds through that pointer, **or** VM0042 does not implement
> a requirement it cross-references.
>
> **Both are findings. Neither is an accusation.**

Resolving which holds requires Verra's own reading of its own cross-reference,
and this record does not have it. Nothing here asserts that a rule was breached,
that credits were wrongly issued, or that any party acted improperly.

## 6. The robustness split — keep it visible

The two quantities derived from 31.35% do **not** have the same standing, because
the pool scope of that figure could not be confirmed. The project description is
not public outside the registry's client-rendered application; the validation
report calls the number "*the final uncertainty deduction*" (CAR ID 60),
singular and project-level, reported in Table 4-17 and §4.4.4 without
disaggregation — while VM0042 §8.6.4 requires deductions "*estimated and applied
separately for each ERR source*".

| finding | needs 31.35% to be SOC-specific? | standing |
|---|---|---|
| **90% half-width = 119.7% > the §2.4 bar** | **No.** Both sides refer to the same ERR estimate, whatever pools it aggregates | **ROBUST — lead with this** |
| `Δ / MDD = 0.70` at 50% power | **Yes.** MDD is defined on SOC *stocks* (§8.2.1.3 Eq. 2) | **CONDITIONAL — label as such wherever it appears** |

The conditional quantity is not withdrawn and not promoted. It carries its
condition in every table it enters, including `projects.yaml`
(`claimed_change_in_mdd_units`).

## 7. Standing methodological caution — version boundaries

`0.4307` and the eligibility bar are **both absent from MR v4.0** (19 September
2019, 78 pp.). Both are present in v4.4 (October 2023). The procedure and the bar
entered between those dates.

This is the **second** near-miss in this project caused by a protocol revision
boundary, and the pattern is now worth stating as a rule rather than an anecdote:

| # | boundary | what nearly happened |
|---|---|---|
| 1 | VM0042 v2.0 **public-comment draft** (Dec 2021) vs **approved** v2.0 (May 2023) | A two-pathway/two-case §8.6.4 was read as the rule in force. It had been removed before approval. Produced D-059's retracted identity, a wrong `k` (1.960 vs 0.4307), and a `Δ/MDD` that was wrong by a factor of 4.5 **in the direction favourable to the project** (D-060). |
| 2 | MR **v4.0** (2019) vs **v4.4** (2023) | Reading v4.0 would have found neither the constant nor the bar, and concluded no program-level rule existed. |

> **Rule: for any quantitative claim about a protocol, the version in force on
> the relevant date must be retrieved and cited, and a draft is never evidence of
> a rule in force — even when it is the only copy to hand.** Where a methodology
> defers to a program document with "the latest version of" language, the
> deferred-to document must be retrieved at its own version too, because the two
> revise on independent schedules.

Both near-misses were caught by checking a primary source that a prior session
had recorded as unobtained. Neither was caught by internal review of the
reasoning, which was in both cases internally consistent and wrong.

## 8. Sources

| document | version / date | locator used |
|---|---|---|
| *VCS Methodology Requirements* | **v4.4**, upd. 4 Oct 2023, 88 pp. | §2.4, printed pp. 12–13 |
| *VCS Methodology Requirements* | v4.0, 19 Sep 2019, 78 pp. | §2.4 — neither provision present |
| VM0042 | **v2.0 approved**, May 2023, 157 pp. | §8.6.4 Eq. (65); §8.2.1.3 Eqs. (2), (3) |
| AgreenaCarbon (VCS 4022) validation report | Earthood, Dec 2024, 151 pp. | CAR ID 60; CAR ID 21 item 5 |

Full retrieval record, verbatim-search counts and the `s²` verification:
**`vm0042_s2_verification.md`**. Corpus fields: `data/registry/projects.yaml`
(`protocol_requirements` → *VCS Program (Verra) — Methodology Requirements*).
