# VM0042 — verification of the uncertainty rule and of `s²`

**Verification record. Primary sources only. Written 2026-08-13.**

This was commissioned as a narrow check: *is `s²` the same object in VM0042 v2.2
Eq. 74 and v2.0 Eq. 84?* (sweep scope §3a, gating the claimed 4.54× severity
ratio between versions).

The narrow answer is **yes — `s²` is identical in construction, definition and
units across versions**.

The check also falsified its own premise. **VM0042 v2.0 has no Eq. 84, no
Eq. 83, no Pathway A/B, no case N1/N3, no threshold `A`, no `t₀.₉₇₅` and no
100% cap.** v2.0 §8.6.4 is a single equation built on the same `0.4307` constant
as v2.2. The version-severity finding is void, and D-059's central identity does
not follow from the document it was attributed to.

---

## 1. Documents checked

All retrieved 2026-08-13 from verra.org, text-extracted with `pypdf`, searched
verbatim.

| # | document | pages | URL |
|---|---|---:|---|
| 1 | VM0042 **v2.0** (final, in force for VCS 4022) | 157 | `/wp-content/uploads/2023/05/VM0042-Improved-ALM-v2.0.pdf` |
| 2 | VM0042 **v2.1** (corrected 21 Jan 2025) | 168 | `/wp-content/uploads/2024/09/VM0042v2.1_ImprovedALM_corrected_21Jan2025.pdf` |
| 3 | VM0042 **v2.2** (final) | 167 | `/wp-content/uploads/2024/09/VM0042v2.2.pdf` |
| 4 | VM0042 **v2.2 greenlined** (tracked changes) | 183 | `/wp-content/uploads/2025/10/VM0042v2.2_greenlined.pdf` |
| 5 | **Corrections & Clarifications to v2.0** (22 Jan 2024, upd. 14 Mar 2024) | 40 | `/wp-content/uploads/2024/01/CC_VM0042_v2.0_22Jan2024_update14Mar2024.pdf` |
| 6 | **Draft v3.0 §8** (public consultation, 10 Feb 2026) | 75 | `/wp-content/uploads/2026/02/2_VM0042v3_main_8_clean-draft_10FEB2026.pdf` |
| 7 | **Draft v3.0 §9–10** (public consultation) | 56 | `/wp-content/uploads/2026/02/3_VM0042v3_main_9-10_clean-draft_10FEB2026.pdf` |
| 8 | Verra's worked uncertainty-deduction example (QA1, v2.0/v2.1) | 20 | `/wp-content/uploads/2024/11/Uncertainty-deduction-calculation-example-…pdf` |
| 9 | VM0042 v2.0 **final draft for public comment**, Dec 2021 | 173 | `/wp-content/uploads/2021/12/VM0042_v2.0_FinalDraft_PublicComment.pdf` |

### Verbatim search results

| string | 1 v2.0 | 2 v2.1 | 3 v2.2 | 4 v2.2-gl | 5 C&C | 6 v3§8 | 7 v3§9-10 | 8 example |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `Pathway A` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **5** |
| `Pathway B` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **3** |
| `Case N1` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **2** |
| `Case N3` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **2** |
| `Australian Carbon Credits` | 0 | – | 0 | – | – | – | – | – | **1** |
| **`0.4307`** | **1** | **1** | **1** | **1** | 0 | **1** | 0 | **2** | **0** |

(Column 9 = the Dec 2021 public-comment draft.)

The constant `0.4307` is present in **every approved version** of the
methodology, including v2.0. The pathway/case vocabulary is present in **none of
them** — and present in **the superseded draft alone**.

### Provenance of the error — identified

D-059's §8.6.4 quotations are **accurate transcriptions of document 9**, the
December 2021 final-draft-for-public-comment. That draft genuinely contains,
verbatim: "*Two cases depending on the Quantification Approach used for
estimating Direct N₂O Emissions*"; "*Pathway A is based on the relative
uncertainty of the sum of sources and sinks…*"; "*For case N1, the defined
threshold is 15%… For case N3, A is defined as 0%*"; "*Equation 83*"; a
`t`-distribution at "*significance level α = 0.975 / 0.025*"; and "*for case N1 B
is set to be 55% while for case N3, B is set to 70%. Note, The Australian Carbon
Credits Methodology uses 60%*".

**Verra removed that entire construction before approving v2.0 in May 2023** and
replaced it with the single Eq. (65) rule. Nothing was invented; the wrong
document was read. The prior record said so itself and flagged the risk —
`projects.yaml` carried "*The APPROVED v2.0 has not been obtained; Section 8.6.4
is read from the [draft]*" and listed obtaining it as a blocked item. **This
check closes that item, in the direction that invalidates the result.**

The lesson is narrow and worth keeping: *a public-comment draft is not evidence
of the rule in force, even when it is the only copy to hand.* VCS 4022 was
validated against approved v2.0 (May 2023), 17 months after document 9.

---

## 2. What v2.0 §8.6.4 actually says

Printed pp. 74–76. Quoted verbatim:

> **Equation (65).**
> `UNC_{Δ•,t} = Uncertainty × t_{α=0.666}`
> `Uncertainty = ( √(s²_{Δ•,t}) / Δ̄•,t ) × 100`

> `UNC_{Δ•,t}` = "*Uncertainty deduction for gas or pool • to be applied in
> verification period t (%)*"
> `Uncertainty` = "*Half-width of the one standard deviation interval as a
> percentage of the mean of the ERR estimate for gas or pool • in verification
> period t (%)*"
> `s²_{Δ•,t}` = "*Variance of the estimate of mean emission reductions from gas
> or pool • at time t. See Figure 3 to determine how this is estimated based on
> the methods employed in the project (t CO₂e/ha)²*"
> `t_{α=0.666}` = "*Critical value of a one-sided student's t-distribution at
> significance level α = 0.666 (66.6%) with degrees of freedom appropriate to the
> sampling design used. **Equal to approximately 0.4307 at large sample sizes**
> (dimensionless)*"

There is no `MIN{}`, no `MAX{}`, no threshold subtraction, and no case split.
The section is a single probability-of-exceedance rule at the 33.3rd percentile.

## 3. What v2.2 §8.6.4 says

Printed pp. 81–82:

> **Equation (74).**
> `UNC_{Δ•,t} = ( ( √(s²_{Δ•,t}) / Δ̄•,t ) × 100 ) × t_{0.667}`

> `t_{0.667}` = "*t-value for a one-sided student's t-distribution at 0.667
> (66.7%) confidence interval with degrees of freedom appropriate to the sampling
> design used. **Equal to approximately 0.4307 at large sample sizes**
> (dimensionless)*"

**v2.0 Eq. (65) and v2.2 Eq. (74) are the same rule with the same constant.**
The differences are cosmetic: an equation number, "gas or pool" → "GHG or C
pool", "emission reductions" → "reductions and removals", and "significance
level α = 0.666" → "0.667 confidence interval".

---

## 4. Is `s²` the same object? — yes, at three levels

**(a) Same definition.** Both define `s²_{Δ•,t}` as the variance of the mean
ERR estimate for the gas or pool at time `t`, in `(t CO₂e/ha)²`, pointing to the
section's equation map.

**(b) Same construction pipeline.** §8.6's subsection tree is identical
heading-for-heading:

```
8.6 Uncertainty
  8.6.1   Quantification Approach 1
    8.6.1.1    Analytical Calculation of Error Propagation
      8.6.1.1.1  Model Prediction Error
      8.6.1.1.2  Model Input and Measurement Error
      8.6.1.1.3  Sampling Error
      8.6.1.1.4  Combined Sample and Model Error
    8.6.1.2    Monte Carlo Simulation
      8.6.1.2.1  Combined Sample and Model Error
      8.6.1.2.2  Monte Carlo Propagation of Model Input Error
      8.6.1.2.3  Monte Carlo Error
    8.6.1.3    Remeasurement, Model True-Up and Cumulative Crediting¹
  8.6.2   Quantification Approach 2
    8.6.2.1    Alternative SOC Measurement Methods
    8.6.2.2    Extensions to Other Sampling Designs
  8.6.3   Quantification Approach 3
  8.6.4   Uncertainty Deductions
```

¹ retitled "Cumulative Modeling" in v2.2 — the only heading difference.

The equation maps (v2.0 Figure 4, v2.2 Figure 5) route the same four paths into
the deduction, renumbered by a uniform **+9**:

| path | v2.0 | v2.2 |
|---|---|---|
| QA1, analytical error propagation | Eqs. 51–55 | Eqs. 60–64 |
| QA1, Monte Carlo simulation | Eqs. 56–60 | Eqs. 65–69 |
| QA2, conventional lab analysis | Eqs. 61–62 | Eqs. 70–71 |
| QA2, proximal sensing | Eqs. 61 & 63/64 | Eqs. 70 & 72/73 |
| → deduction | Eq. 65 | Eq. 74 |

**(c) Same equations.** The combined sample-and-model error equation — the one
that determines what enters `s²` — is identical symbol-for-symbol:

| | v2.0 | v2.2 |
|---|---|---|
| combined | `s²_{Δ•,t} = s²_{sampling,Δ•,t}/A² + s²_model` (54) | *same* (63) |
| model term | `s²_model = Σ_{h=1..H} (A²_h/A²)·s²_{model,h}` (55) | *same* (64) |

Surrounding prose is also identical, down to the citations (Cochran 1977
Eq. 13.39; Som 1995 Eq. 25.10) and the note that only sampling error is divided
by `A²`.

> **Conclusion (a):** `s²` has the same content in both versions. Model
> prediction variance is pooled with sampling variance in both. Nothing about
> the variance changed between v2.0 and v2.2.

> **Conclusion (b):** because the multiplier is also the same (`0.4307`), the
> claimed **4.54× version-severity ratio does not exist**. Sweep scope §3a is
> withdrawn in full.

---

## 5. Where the MDD equation actually lives

D-059 attributed the MDD to "v2.0 §9.3.1 Eq. 88". There is no Eq. 88 in v2.0.
The MDD is in **§8.2.1.3, printed p. 29, Equations (2) and (3)**:

> `MDD ≥ (S/√n) × (t_{α,ν} + t_{β,ν})`  (2)
> `n ≥ ( S × (t_α + t_β) / MDD )²`  (3)
>
> `S` = "*Standard deviation of the difference in SOC stocks between t₀ and t₁*"
> `t_α` = "*Two-sided critical value of the t-distribution at a given
> significance level (α) frequently taken as 0.05*"
> `t_β` = "*One-sided quartile of the t-distribution corresponding to a
> probability of type II error β*"

This is the equation D-057 correctly identified as "Eq. (2)". §9.2's monitored-
parameter table lists `MDD` against "Equations (2), (3)" — consistent.

**The optionality finding survives, with a corrected locator.** §8.2.1.3 item 10:

> "*A power analysis may be conducted to calculate the number of samples needed
> to enable accounting of a minimum detectable difference, following Equations
> (2) and (3) (FAO, 2019). **However, projects are not required to take this
> number of samples.***"

---

## 6. The identity, repaired

The general form in sweep scope §2 is **correct and unaffected**:

```
UNC = k · σ_rel              σ_rel = SE(Δ)/Δ
MDD = (t_α + t_β) · SE(Δ)
⇒   Δ / MDD  =  k / ( (t_α + t_β) · UNC )
```

Only the `k` for VM0042 v2.0 was wrong. Corrected table:

| rule | `k` | source |
|---|---:|---|
| VM0042 **v2.0** Eq. 65 | **0.4307** | §8.6.4, `t_{α=0.666}` — *this record* |
| VM0042 **v2.1** | **0.4307** | §8.6.4 — *this record* |
| VM0042 **v2.2** Eq. 74 | **0.4307** | §8.6.4, `t₀.₆₆₇` (D-057) |
| VM0042 **v3.0 draft** | **0.4307** | draft §8 — *this record* |
| CAR SEP v1.1 | 1.028 | unchanged (D-057) |
| ACCU / ACCM | 0.2533 | unchanged (D-057) |

**VM0042 has had one uncertainty rule since v2.0.** The version dimension
collapses out of the sweep entirely — a simplification, not a loss.

### The screening thresholds are unchanged where they were already right

`Δ/MDD < 1` ⟺ `UNC > k/(t_α + t_β)`:

| rule | claim = MDD at 50% power | at 80% power |
|---|---:|---:|
| VM0042 (all versions) | UNC > **21.97%** | UNC > **15.37%** |
| CAR SEP v1.1 | UNC > 52.4% | UNC > 36.7% |
| ACCU / ACCM | UNC > 12.9% | UNC > 9.0% |

The v2.2 row of the old table (22.0% / 15.4%) was already correct and now
applies to every VM0042 project. The v2.0 row (100.0% / 70.0%) is deleted.

---

## 7. VCS 4022, recomputed

Conditional on the published `UNC = 31.35%` being the Eq. 65 deduction — see
the caveat in §8 — the corrected arithmetic **inverts the D-059 conclusion**:

| quantity | D-059 (`k = 1.960`) | corrected (`k = 0.4307`) |
|---|---:|---:|
| implied relative SE | 15.99% | **72.79%** |
| `Δ / MDD` at 50% power | 3.19 | **0.70** |
| `Δ / MDD` at 80% power | 2.23 | **0.49** |

D-059 reported a claim comfortably above its detection floor. The rule actually
in force says the opposite: **VCS 4022's claimed change is smaller than its own
minimum detectable difference** — about 70% of the 50%-power floor, and half the
80%-power floor.

This was already implied by the sweep scope's *own* threshold table: 31.35% sits
above the 21.97% line. §3a and §2 of that document contradicted each other, and
the contradiction is what this check surfaced.

---

## 8. What remains unverified

1. **The provenance of 31.35%.** Not re-checked here — the VCS 4022 PD and
   validation report are not in this container. The recorded locator is the
   validation report's corrective-action log, CAR ID 60. Before the corrected
   `Δ/MDD = 0.70` is published anywhere, confirm that 31.35% is the Eq. 65
   deduction for **SOC** and not a differently-scoped figure (§4.4.4 of the PD
   reportedly carries a 14.53% that was superseded).
2. **The case-N3 determination (D-059 §3).** Moot — there are no cases. The
   underlying observation that VCS 4022 used IPCC 2019 Tier 1 defaults for
   `EF_Ndirect` still stands as a fact about the project, but it selects nothing.
3. **Whether any cap on `UNC` exists at program level.** None exists in VM0042.
   §8.6.4 defers to *VCS Methodology Requirements* §2.4, which was not retrieved.
   Until it is, the planned "cap sweep" has no cap to sweep for.
4. ~~**Where the Eq. 83/84 text came from.**~~ **Resolved** — the December 2021
   public-comment draft (document 9). See §1. Nothing outstanding.

---

## 9. Effect on the record

| claim | status |
|---|---|
| `s²` identical across v2.0/v2.2 | **confirmed** |
| VM0042 `k = 0.4307` in all versions | **confirmed** |
| Generalised identity `Δ/MDD = k/((t_α+t_β)·UNC)` | **holds** |
| VM0042 sample-size calculation is optional | **holds** (locator corrected to §8.2.1.3 item 10) |
| Eqs. 36/37 share factor ⇒ 18.48% effective on gross ERRs | **unaffected** |
| v2.0 is 4.54× more severe than v2.2 | **void** |
| v2.0 §8.6.4 = two pathways × two cases | **void — no such text** |
| `UNC = MDD/Δ` under case N3 | **void as derived** (rests on Eq. 83) |
| VCS 4022 claim = 3.19× MDD | **void — inverts to 0.70×** |
| 100% cap is a detector | **void — no cap exists** |
