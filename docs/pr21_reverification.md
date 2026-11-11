# PR #21 — claim-by-claim re-verification (D-075)

PI decision A (2026-11-10): bring PR #21 onto `main`, re-verify every claim against its
primary document, renumber. PI decision B: nothing under `verra.org/wp-content/uploads` is
fetched by us. The PI downloads those files by hand; see
[`verra_hand_download_list.md`](verra_hand_download_list.md).

**Status key:** ✅ verified from the primary document this session · 🧮 verified as arithmetic ·
⏳ pending the PI's hand download · ⚠ internal inconsistency in PR #21, flagged, not edited ·
— not re-verifiable (historical or environment-specific).

**Primary documents used:**
- **Validation report:** VCS Validation Report, AgreenaCarbon Project, v4.0, VCS.VAL.22.89
  (Earthood, 2024-12-20). Read from the terrapass.com mirror; sha256 `7dfc0bf06112…` is in
  `projects.yaml` `agreena_val_v4`.
- **Page numbers:** PDF pages, which differ from the printed page numbers in places.

## A. Claims from the VCS 4022 validation report

| # | claim (PR #21) | PR #21 locator | status | primary locator |
|---|---|---|---|---|
| A1 | applied uncertainty deduction 31.35% | "CAR ID 60" | ✅ | p. 147; CAR#60 also named on p. 58 |
| A2 | PD had 23.97% (Table 4-17) and 14.53% (§4.4.4) before CAR#60 | CAR ID 60 | ✅ | p. 147 |
| A3 | called "the final uncertainty deduction", single, not split by pool | CAR ID 60 | ✅ | p. 147 |
| A4 | MDD, S, n, n-1, t_x,U: "The parameter is not relevant and therefore not further assessed" | Data and Parameters Monitored | ✅ | p. 50 |
| A5 | "MDD, n, n-1, tx,u, parameters are missing from data and parameters to [be] monitored" | "CAR #01 item VII" | ✅ text, **locator corrected** | **CAR ID 45 item VII, p. 131.** The original reads "to me monitored". |
| A6 | Tier 1 IPCC (2019) values for EF_Ndirect used without the required justification | "CAR #01 item V" | ✅ text, **locator corrected** | **CAR ID 45 item V, p. 131** |
| A7 | uncertainty pools RothC model prediction variance and soil-sampling uncertainty | "CAR ID 21.4 PP response" | ✅, locator refined | p. 110: a response filed under the CAR whose attachments are labelled "CAR ID 21.x"; the nearest preceding CAR header reads CAR ID 20 (p. 106) |
| A8 | model RMSEs in "Table 3.9" of the non-public MVR | — | ✅ | p. 110 |
| A9 | uncertainty workbook named twice, public neither time | two filenames | ✅ | p. 84 (`CL ID 8.4_…uncert_deduction_proj.zip`), p. 111 (`CAR ID 21.4_…uncert_deduct_proj.zip`) |
| A10 | ex-ante table: baseline 12,676,641.20; project −742,116.10; leakage 87,250.58; uncertainty deduction 2,464,107.81; net 10,867,398.91 | ex-ante summary | ✅ | p. 43 |
| A11 | "3-5 PAIs" per stratum; stratum count deferred to verification | CAR response | ✅ | p. 140 |
| A12 | MDD analysis "will be performed to guide subsequent sampling efforts where prudent" | CAR response | ✅ | p. 140. The same paragraph cites "**Equation (3) of Section 8.2.1.3** of VM0042 v2.0"; see C9. |

## B. Arithmetic (no document needed)

| # | claim | status |
|---|---|---|
| B1 | 31.35 / 0.4307 = 72.79% implied relative SE | 🧮 |
| B2 | 72.79% × 1.6449 = 119.7% implied 90% half-width | 🧮 |
| B3 | bar `1.6449·SE > Δ` ⟺ σ_rel > 60.79% ⟺ UNC > 26.18% | 🧮 |
| B4 | Δ/MDD at the bar = 0.4307 / (1.96 × 0.2618) = 0.839 | 🧮 |
| B5 | VCS 4022 Δ/MDD = 0.70 at 50% power, 0.49 at 80% | 🧮. D-068 (WP2, PR #24) reached 0.70 independently, and also gives 0.42 at 90% power. |
| B6 | gross ERRs 13,331,506.72; 2,464,107.81 / 13,331,506.72 = 18.48% | 🧮 (inputs ✅ A10) |
| B7 | Verra's worked example 32.9 / 1.6449 × 0.4307 = 8.6 | 🧮 arithmetic only; that the example is MR's is ⏳ C6 |

## C. Claims resting on Verra-hosted PDFs (all ⏳)

| # | claim | document needed (download list #) |
|---|---|---|
| C1 | approved VM0042 v2.0 §8.6.4 is one rule, Eq. (65), `UNC = (√s²/Δ̄ × 100) × t_{α=0.666}`, t ≈ 0.4307 (pp. 74–76) | 1 |
| C2 | no "Pathway A", "Case N1/N3", threshold A or cap in any approved version; the two-pathway construction was removed before May 2023 approval | 1, 5, 6, 7, 10 |
| C3 | s² identical in v2.0 and v2.2 (v2.0 Eqs 54/55 ≡ v2.2 Eqs 63/64; equation maps differ by +9) | 1, 6 |
| C4 | sample size optional: §8.2.1.3 item 10, verbatim | 1 |
| C5 | Eqs 36/37 apply the deduction as (1 − UNC × share); §8.2.8 sets QA for direct N₂O; Eq. 53 needs Cov(y_t, y_t−1) | 1 |
| C6 | MR v4.4 §2.4: discount factor formula, 1.6449 and 0.4307, worked example 32.9% → 8.6%, eligibility bar verbatim, no cap, 10% materiality floor | 2 |
| C7 | MR v4.0 contains neither 0.4307 nor the bar | 3 |
| C8 | 0.4307 present in v2.1, v2.2, v2.2 greenlined, the v2.0 Corrections & Clarifications, and the v3.0 draft | 5, 6, 7, 11–14 |
| C9 | MDD is §8.2.1.3 **Eq. (2)**, Eq. (3) inverts it for n. PR #21 elsewhere says MDD is "§9.3.1, Eqs 88/89" and that the PD cites a nonexistent section. **⚠** The two cannot both be right. The PD's own "Eq. (3) of §8.2.1.3" (A12) agrees with the first. | 1 |
| C10 | VM0042 §8.6.4 points to "the latest version of" MR §2.4 but does not reproduce the bar | 1, 2 |

## D. Not re-verifiable here

| # | claim | status |
|---|---|---|
| D1 | the August authorised browser failed on that container's egress (`net::ERR_CONNECTION_RESET`) | — historical, environment-specific |
| D2 | `verra.org/robots.txt` disallows `/wp-content/uploads` | ✅ re-checked 2026-11-10 |
| D3 | `registry.verra.org` serves no parseable robots.txt | ✅ re-checked 2026-11-10: `/robots.txt` returns the 2,598-byte app shell. The registry has since moved platform (D-066). |

## What this means for `main`

- **Citable as verified now:** A1–A12 (with the corrected locators) and B1–B6.
- **Not citable as verified until the C rows close:**
  - that the approved v2.0 uses k = 0.4307;
  - that VCS 4022's 31.35% is "a 0.43-SE deduction";
  - the MR §2.4 eligibility bar;
  - VCS 4022's 119.7%, 0.70× and 0.42× as anything but conditional.

  D-072 and D-073 are **open** for this reason.
- **When the PI's downloads land:** re-read each C row against the PDF and close it in D-075's
  successor. If any row fails, D-072/D-073 become corrections, and the WP2 own-deduction row for
  VCS 4022 (D-068) loses its k.
- **One incident, disclosed in D-075.** Two Verra landing pages redirected into
  `/wp-content/uploads/`, so two PDFs (MR v4.0; C&C v2.0) were downloaded against decision B.
  Both were deleted unopened, and nothing from them is used.
