# VCS 4022 — implied vs applied uncertainty deduction

> # ⛔ RETRACTED IN PART — 2026-08-13
>
> **§2, §3 and §4 of this document describe a rule that does not exist.** The
> "two pathways × two cases", Equations 83/84, threshold `A`, cases N1/N3 and
> the `t₀.₉₇₅` multiplier are **not in VM0042 v2.0**, nor in v2.1, v2.2, the
> v2.2 greenlined text, the Corrections & Clarifications to v2.0, or the v3.0
> consultation draft. See **`vm0042_s2_verification.md`** for the primary-source
> record.
>
> VM0042 v2.0 §8.6.4 is **Equation (65)**, `UNC = (√s²/Δ̄ × 100) × t_{α=0.666}`,
> with `t ≈ 0.4307` — the same rule and the same constant as v2.2 Eq. 74.
>
> **Consequences:**
> - The identity `UNC = MDD/Δ` **does not follow** from v2.0 as derived (§4).
> - The implied relative SE is **72.79%**, not 15.99% (§5).
> - `Δ/MDD` is **0.70** at 50% power and **0.49** at 80% — the claimed change is
>   *below* its own detection floor, inverting §4's "3.19× MDD".
> - The case-N3 determination (§3) is moot: VM0042 has no cases.
>
> **What survives:** §6 (the Eqs. 36/37 share factor, 18.48% effective on gross
> ERRs), §7 (the four withheld/undisclosed inputs and the estimand mismatch), and
> the finding that the sample-size calculation is optional — with its locator
> corrected to §8.2.1.3 item 10, Equations (2) and (3).
>
> The general identity `Δ/MDD = k/((t_α+t_β)·UNC)` is unaffected; only `k` was
> wrong. Read `vm0042_s2_verification.md` in preference to §§2–5 below.

**First Phase 5 result.** Status: reported to the PI 2026-08-13, written up here.
No variance-table row is written or implied by this document.

---

## 1. The question, and the short answer

VCS 4022 (AgreenaCarbon, Verra, VM0042 v2.0) publishes an uncertainty deduction
of **31.35%**. The inverted audit asks the obvious next question: *what sampling
design does that number imply, and does it match what the project actually did?*

**The forward direction cannot be computed.** It needs four parameters VCS 4022
does not disclose, and one of them is `withheld` in the corpus's strong sense —
the public document names the file that holds it. Worse than missing inputs, the
estimand does not match: case N3 pools RothC model-prediction variance with
sampling variance, and LoAM's envelope speaks only to the second.

**The inverse direction is exact, and needs nothing that is not published.**
Under the rule actually in force, the deduction *is* the relative half-width of
the 95% confidence interval, so it inverts with no free parameter:

> VCS 4022's own arithmetic says its emission-reduction estimate carries a
> **standard error of ~16% of the estimate** (14–16% for any n ≳ 10).

And it inverts into LoAM's own currency, exactly — see §4.

---

## 2. Which rule was in force

VCS 4022 applied **VM0042 v2.0**, stated directly by the validation body:

> "The proposed project activity has applied VCS VM0042, v 2.0 methodology"
> — Validation Report §3.3.6

This matters more than a version number usually does. **v2.0's uncertainty rule
is structurally different from v2.2's — not a different constant, a different
construction.** v2.2 §8.6.4 Eq. 74 is a single formula built on
`t₀.₆₆₇ ≈ 0.4307` (D-057). That figure appears nowhere in v2.0. In its place,
v2.0 §8.6.4 (printed pp. 82–85) sets out **two pathways × two cases**:

> **Two cases depending on the Quantification Approach used for estimating
> Direct N₂O Emissions.** "*1. Case N1 is when Quantification Approach 1 is used
> for estimating direct N₂O emissions… 2. Case N3 is when Quantification
> Approach 3 is used for N₂O emission estimates.*"

> **Pathway A — relative uncertainty** (p. 83). "*Pathway A is based on the
> relative uncertainty of the sum of sources and sinks for the project minus the
> baseline. The relative uncertainty is estimated as one-half of the confidence
> limit divided by the sum of differences in sources and sinks between the
> project and baseline. If the relative uncertainty is greater than a threshold,
> A, there is an uncertainty deduction: • For case N1, the defined threshold is
> 15%. When the relative uncertainty is lower than 15%, no uncertainty deduction
> comes into effect. • For case N3, A is defined as 0%, so that there is always a
> deduction for uncertainty.*"

> **Equation 83.**
> `UNC_t = MIN{100%, MAX[0, (ΔF̄_{t,0.975} − ΔF̄_{t,0.025}) / (2·ΔF̄_t) × 100% − A]}`

> **Equation 84.**
> `ΔF̄_{t,0.975} = t₀.₉₇₅·√(Σ_ℓ s²_{Δℓ,t})` and `ΔF̄_{t,0.025} = t₀.₀₂₅·√(Σ_ℓ s²_{Δℓ,t})`

> **Pathway B — probability of exceedance** (p. 85, Eqs. 85/86). "*B The
> probability of exceedance %, for case N1 B is set to be 55% while for case N3,
> B is set to 70%. Note, The Australian Carbon Credits Methodology uses 60%*"

### Correction to D-057

D-057 read the v2.0 redline as carrying "a 15%-threshold rule in one layer and a
two-pathway rule in another", i.e. as tracked-changes noise. **That reading was
wrong.** The 15% threshold *is* Pathway A's threshold `A` for case N1. Both
pathways and both cases sit in one coherent v2.0 section. The rule is one rule,
and it is legible.

Two drafting defects in v2.0, recorded because a reader reproducing this will hit
them. Eq. 84 omits the `+ ΔF̄_t` term that Eq. 86 carries — harmless, because
Eq. 83's numerator is a difference and the mean cancels. And Eq. 85 labels a
*retained fraction* as an "uncertainty deduction", so Pathway B's UNC runs the
opposite way to Pathway A's.

---

## 3. Which case — determined from primary evidence

The validation report never names a pathway or a case. But case selection turns
on exactly one thing: which Quantification Approach was used for **direct N₂O**.

v2.0 §8.2.8 makes the test mechanical — QA1 uses Eq. 11 (modelled N₂O flux);
QA3 uses Eq. 12 (default emission factors). The validation report settles it in
its own corrective-action log:

> CAR #01, item V — "*EF_Ndirect; Frac_GASF,l,S; Frac_GASM,l,S; Frac_LEACH,l,S;
> EF_Nleach; N_content,g; EF_Nvolat, C, M_wp,OF,i,t, MB,g,wp,l,t: No
> justification to use the **Tier 1 value from Chapter 11, Volume 4 in IPCC
> (2019)** is provided, as required by the methodology.*"

IPCC Tier 1 default emission factors for `EF_Ndirect` = Quantification Approach
3. Consistent with §3.3.6: "*The project is using quantification approach 1 and
3*" — QA1 for SOC and methanogenesis, QA3 for the defaults.

**→ Case N3. A = 0%.** Logged as **D-059**, because it is our inference and it is
load-bearing: reading this as case N1 (A = 15%) would put the implied relative SE
at **23.65%** instead of **15.99%**, a 48% error.

---

## 4. The identity: relative uncertainty **is** MDD ÷ claimed change

This is the section that makes VCS 4022 a Phase 5 result rather than an anecdote.

Under case N3 (`A = 0`), Eq. 83 reduces to the relative half-width, and Eq. 84
makes that half-width `t₀.₉₇₅ · SE(Δ)` — because `t₀.₀₂₅ = −t₀.₉₇₅`, so

```
UNC  =  t₀.₉₇₅ · SE(Δ) / Δ
```

Now take VM0042 v2.0's *own* minimum-detectable-difference equation, §9.3.1
Eq. 88:

```
MDD  ≥  (S/√n) · (t_α,ν + t_β,ν)
```

`S/√n` is `SE(Δ)`. At 50% power, `t_β = 0`, leaving `MDD = t₀.₉₇₅ · SE(Δ)` —
**algebraically identical to Eq. 83's numerator.** Therefore, under case N3:

> ### UNC = MDD / Δ
>
> **VM0042's uncertainty deduction is the ratio of the project's minimum
> detectable difference to the change it claims.**

No assumption, no undisclosed parameter, no LoAM input. It follows from two
equations in the same document.

Read back onto VCS 4022's published 31.35%:

| power convention | multiplier on MDD₅₀ | claimed change, in MDD units |
|---|---|---|
| 50% power (`t_β = 0`) | 1.000 | **3.19 × MDD** |
| 80% power (`t_β = t₀.₈₀`) | 1.429 | **2.23 × MDD** |

So VCS 4022 states, in the registry's own machinery, that its claimed SOC change
sits between two and three times its own detection floor.

**Two consequences.**

*For the method.* The inverted audit does not have to argue that MDD is the right
lens — VM0042 already computes MDD/Δ every year, under a different name. For any
case-N3 project that publishes a deduction, the detectability ratio is a
**republication of a number the registry already accepted**, not a LoAM
construct. That is a much harder finding to dismiss than one built on our
variance table.

*For the reading of the finding in §6.* The same project that computes MDD/Δ
annually has MDD itself formally recorded as "not relevant."

---

## 5. What inverts, and what does not

### 5.1 The inversion (exact)

With `A = 0`, `UNC = 31.35%` **is** the relative 95% half-width. Dividing out `t`:

| df | t₀.₉₇₅ | implied relative SE |
|---:|---:|---:|
| 2 | 4.303 | 7.29% |
| 9 | 2.262 | 13.86% |
| 29 | 2.045 | 15.33% |
| 99 | 1.984 | 15.80% |
| ∞ | 1.960 | **16.00%** |

The only inferred input is `df`, and above n ≈ 30 it moves the answer by less
than a percentage point. The sensitivity is one-sided and bounded: fewer samples
means a *smaller* implied SE, so 16% is the ceiling.

### 5.2 The forward direction (not computable)

Computing an implied deduction from LoAM's variance envelope requires:

| input | status in VCS 4022 | evidence |
|---|---|---|
| **n** — sample units | not disclosed at validation | PD gives "3–5 PAIs per stratum"; the number of strata is deferred — "*strata area and soil sampling points within them… **will be reported at verification***" |
| **ρ** — t₀/t₁ correlation | not disclosed | Eq. 53 requires `Cov(y_t, y_{t−1})`; no value published |
| **σ_model** — RothC prediction variance | **withheld** | "*Table 3.9 – Summary Statistics for PC/CZ/CFG Combinations*" in the MVR, a named non-public document |
| the uncertainty calculation itself | **withheld** | `CAR ID 21.4_TR_AgreenaCarbon uncert_deduct_proj.zip` and `CL ID 8.4_TR_AgreenaCarbon 2023-09-06_uncert_deduction_proj.zip` — named in the validation report, not public |

And a fifth problem that is not about disclosure at all. **The estimand does not
match.** Case N3 pools model and sampling error — the project participant says so
directly:

> CAR #21.4 response — "*To calculate the uncertainty deductions we make use of
> both the **model prediction variance**, which is determined using the formulas
> specified in Section 8.6 of VM0042, **and the uncertainty derived from our soil
> sampling data**.*"

LoAM's envelope covers only the second. And LoAM's between-plot rows measure
variance *between replicate plots within one site* — 3.4–3.8% where within-plot
and analytical error are removed (`VC-BPS-007…011`), 11.5–11.9% as single-visit
upper bounds (`VC-BPS-005/006`). VCS 4022's sample unit is a **field within a
stratum, across ten countries**. LoAM has no row for that quantity.

Running the low end of the envelope through Eq. 83 would produce a number. The
number would be about a different population. **It is not produced here.**

---

## 6. 31.35% is not a 31.35% haircut

The validation report's own ex-ante summary table:

| baseline | project | leakage | uncertainty deduction | net |
|---:|---:|---:|---:|---:|
| 12,676,641.20 | −742,116.10 | 87,250.58 | 2,464,107.81 | 10,867,398.91 |

Internally exact: gross 13,331,506.72 − 2,464,107.81 = 10,867,398.91. Which makes
the **effective deduction on gross ERRs 18.48%, not 31.35%**.

The two reconcile through Eqs. 36/37, which apply the deduction as
`(1 − UNC × share)`, each stream scaled by its fraction of gross ERRs.
18.483/31.35 = 0.5896, consistent with a reductions:removals split of ≈71:29.
That split is not verifiable from public documents, so this is **a consistency
check that passes, not independent confirmation**.

The caution stands either way. **31.35% is an uncertainty statistic, not the
fraction of credits withheld.** Any cross-registry comparison of deduction
severity that takes the PD headline at face value overstates this project's
haircut by roughly 70%. This directly qualifies the D-057 severity table
(ACCU 0.253 · VM0042 0.431 · CAR SEP 1.028): those are `k` multipliers on a
standard error, and the *credited* consequence depends on a share factor that
none of the three registries publishes.

---

## 7. The finding: MDD, formally not relevant

VM0042 v2.0's monitored-parameter tables say, of the sample-size calculation:

> "*Calculation of the number of required samples to detect a minimum difference
> is **optional** for projects.*"

VCS 4022 took the option, and the record of it is unusually complete because the
validator forced the question. CAR #01 item VII found the MDD parameters missing
from the PD's monitoring tables entirely:

> "*M_OAwp,i,t; CC_wp,l,t; p (crop product); **MDD, n, n−1, t_x,u**, parameters
> are missing from data and parameters to be monitored.*"

Agreena added them. The validation body then assessed all five:

| parameter | frequency | VVB assessment |
|---|---|---|
| **MDD** — minimum detectable difference of SOC stocks between two points in time | NA | "*The parameter is not relevant and therefore not further assessed.*" |
| **S** — standard deviation of the difference in SOC stocks between t₀ and t₁ | NA | "*not relevant and therefore not further assessed*" |
| **n** — number of samples required to detect a minimum difference | NA | "*not relevant and therefore not further assessed*" |
| **n − 1** — degrees of freedom | NA | "*not relevant and therefore not further assessed*" |
| **t_x,u** — t-value at a given power and significance level | NA | "*not relevant and therefore not further assessed*" |

A 479,834 ha project claiming 543,370 tCO₂e/year over a 20-year crediting period,
validated, with its minimum detectable difference formally recorded as not
relevant — while, by §4, computing MDD/Δ every year and calling it the
uncertainty deduction.

Two details worth keeping. The PD's commitment is prospective and conditional:
MDD analysis "*becomes possible, and **will be performed** to guide subsequent
sampling efforts **where prudent**.*" And it cites the wrong locator —
"*Equation (3) of Section 8.2.1.3 of VM0042 v2.0*". v2.0 has no §8.2.1.3; its MDD
equations are 88/89 in §9.3.1. In v2.2, §8.2.1.3 is "Collection and Processing of
Soil Samples". Neither the project participant nor the validation body caught it.

---

## 8. What this changes

1. **The inverted audit has a published anchor.** §4's identity means a case-N3
   project's deduction is a detectability ratio the registry already accepted.
   Where a deduction is published, LoAM does not need to supply `S` at all.
2. **Case determination is now a required field**, not a detail. N1 vs N3 changes
   the implied SE by 48%, and neither the PD nor the validation report states it —
   it has to be reconstructed from which N₂O quantification approach was used.
3. **Published deduction percentages are not comparable across projects** without
   the Eq. 36/37 share factor (§6). The D-057 severity table needs that caveat.
4. **The corpus-wide sweep is the next result**, not more depth on this project.
   See `docs/phase5_n3_sweep_scope.md`.

## 9. Reproduction

Primary documents, both held and both retrieved first attempt:

* `agreena_val_v4` — VCS Validation Report of AgreenaCarbon Project, v4.0,
  Report ID VCS.VAL.22.89, Earthood Services Private Limited, 2024-12-20, 151 pp.
* `vm0042_v20_draft` — VM0042 v2.0 final-draft public-comment redline, 2021-12-01,
  173 pp. Header "Version 2**1**.0 19 October 20**20**21 December 2021" confirms
  the redline runs v1.0 → v2.0, so the inserted layer is v2.0.

Outstanding: the **approved** v2.0 (as against the public-comment draft) has not
been obtained. §8.6.4's two-pathway structure is read from the draft's inserted
layer. Nothing in this document depends on 0.4307, which is a v2.2 figure and is
absent from v2.0.
