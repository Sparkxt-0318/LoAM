# Verra documents for the PI to download by hand (decision B)

**Why by hand:** `verra.org/robots.txt` disallows `/wp-content/uploads`, and per PI decision B
(2026-11-10) nothing under that path is fetched by us.

**How to save each one:**
- Put it at the path given, inside the repo. `data/registry/raw/` is git-ignored, so nothing is
  committed by accident.
- Keep the filename exactly as listed; the re-verification reads these paths.

**Where each URL came from:** the two sources recorded in the repo, or Verra's own HTML pages
read this session. The provenance column says which. No URL was guessed.

**Disclosure:** rows 3 and 7 were obtained from a server redirect that also downloaded the PDF
against decision B. The PDFs were deleted unopened; see D-075.

**Decision B now covers the whole of `verra.org`** (PI, 2026-11-11, recorded as D-076 on the WP4
branch). No request of any kind goes to that host from a session; every file below is downloaded
by hand.

**The PI's stated order:** Priority 1 (rows 1–4) and the VCS 4022 Project Description (row 16)
first. Tell the session when they are in place; it then records sha256s and re-reads the C rows
in `pr21_reverification.md`.

**Folder:** `data/registry/raw/verra/methodology/` unless stated otherwise.

## Priority 1 — settles D-072 / D-073 (re-verifying PR #21)

| # | document | URL | save as | provenance of URL | settles |
|---|---|---|---|---|---|
| 1 | VM0042 Improved Agricultural Land Management, **v2.0, approved** (May 2023) | https://verra.org/wp-content/uploads/2023/05/VM0042-Improved-ALM-v2.0.pdf | `VM0042_v2.0_approved_2023-05.pdf` | Verra VM0042 page (read 2026-11-10); PR #21 `vm0042_v20` | C1–C5, C9, C10 |
| 2 | VCS **Methodology Requirements v4.4**, updated 4 Oct 2023 | https://verra.org/wp-content/uploads/2023/08/VCS-Methodology-Requirements-v4.4-updated-4-Oct-2023.pdf | `VCS_Methodology_Requirements_v4.4_2023-10-04.pdf` | PR #21 `vcs_mr_v44` | C6, C10 |
| 3 | VCS **Methodology Requirements v4.0** | https://verra.org/wp-content/uploads/2023/04/VCS_Methodology_Requirements_v4.0.pdf | `VCS_Methodology_Requirements_v4.0.pdf` | redirect target of `verra.org/documents/vcs-methodology-requirements/` (2026-11-10; see disclosure) | C7 |
| 4 | Uncertainty deduction calculation example following QA1, VM0042 v2.0/v2.1 (Nov 2024) | https://verra.org/wp-content/uploads/2024/11/Uncertainty-deduction-calculation-example-following-quantification-approach1-vm0042-v2.0-v2.1.pdf | `VM0042_uncertainty_deduction_example_QA1_v2.0-v2.1_2024-11.pdf` | Verra VM0042 page (2026-11-10) | **Not in PR #21.** It is Verra's own worked example for the v2.0 rule, an independent check on which k applied to VCS 4022 |

## Priority 2 — 0.4307 across versions, and the retracted reading's provenance

| # | document | URL | save as | provenance of URL | settles |
|---|---|---|---|---|---|
| 5 | VM0042 **v2.1** (corrected 21 Jan 2025) | https://verra.org/wp-content/uploads/2024/09/VM0042v2.1_ImprovedALM_corrected_21Jan2025.pdf | `VM0042_v2.1_corrected_2025-01-21.pdf` | Verra VM0042 page; PR #21 `vm0042_v21` | C2, C8 |
| 6 | VM0042 **v2.2**, greenlined (Oct 2025) — the D-057 source | https://verra.org/wp-content/uploads/2025/10/VM0042v2.2_greenlined.pdf | `VM0042_v2.2_greenlined_2025-10.pdf` | `projects.yaml` `vm0042_v22` | C2, C3, C8; re-checks D-057 |
| 7 | Corrections & Clarifications to VM0042 **v2.0** (22 Jan 2024, upd. 14 Mar 2024) | https://verra.org/wp-content/uploads/2024/01/CC_VM0042_v2.0_22Jan2024_update14Mar2024.pdf | `VM0042_v2.0_CorrectionsClarifications_2024-03-14.pdf` | PR #21 `vm0042_v20_cc`; also the redirect target of its landing page (see disclosure) | C2, C8 |
| 8 | Corrections & Clarifications to VM0042 v2.1 (10 Oct 2025) | https://verra.org/wp-content/uploads/2025/10/CorrectionsClarificationsVM0042v2.1_10OCT2025-1.pdf | `VM0042_v2.1_CorrectionsClarifications_2025-10-10.pdf` | Verra VM0042 page | C8 |
| 9 | Corrections & Clarifications to VM0042 v2.2 (11 Jun 2026) | https://verra.org/wp-content/uploads/2026/06/VM0042v2.2_CC_11JUN2026.pdf | `VM0042_v2.2_CorrectionsClarifications_2026-06-11.pdf` | Verra VM0042 page | C8; any change to §8.6.4 since v2.2 |
| 10 | VM0042 v2.0 final draft for public comment (Dec 2021), the redline D-071 misread | https://verra.org/wp-content/uploads/2021/12/VM0042_v2.0_FinalDraft_PublicComment.pdf | `VM0042_v2.0_FinalDraft_PublicComment_2021-12.pdf` | `projects.yaml` `vm0042_v20_draft` | C2 (what was removed before approval) |

## Priority 3 — the v3.0 drafts, for the registry comment (WP4)

The consultation closed 2026-03-31. These let the comment respond to the draft text rather
than only Verra's summary page.

| # | document | URL | save as | provenance of URL |
|---|---|---|---|---|
| 11 | Draft VM0042 v3.0, Sections 1–7 (clean, 10 Feb 2026) | https://verra.org/wp-content/uploads/2026/02/1_VM0042v3_main_1-7_clean-draft_10FEB2026.pdf | `VM0042_v3.0_draft_s1-7_2026-02-10.pdf` | Verra M0264 revision page (2026-11-10) |
| 12 | Draft VM0042 v3.0, Section 8 (clean) | https://verra.org/wp-content/uploads/2026/02/2_VM0042v3_main_8_clean-draft_10FEB2026.pdf | `VM0042_v3.0_draft_s8_2026-02-10.pdf` | M0264 page; PR #21 `vm0042_v30_draft` |
| 13 | Draft VM0042 v3.0, Sections 9–10 (clean) | https://verra.org/wp-content/uploads/2026/02/3_VM0042v3_main_9-10_clean-draft_10FEB2026.pdf | `VM0042_v3.0_draft_s9-10_2026-02-10.pdf` | M0264 page |
| 14 | Draft VM0042 v3.0, Appendices (clean) | https://verra.org/wp-content/uploads/2026/02/4_VM0042v3_appendices_clean-draft_10FEB2026.pdf | `VM0042_v3.0_draft_appendices_2026-02-10.pdf` | M0264 page |
| 15 | Draft VM0042 Soil Sampling and Analysis Handbook (26 Feb 2026) | https://verra.org/wp-content/uploads/2026/02/7_VM0042-SSAHandbook_draft_26FEB2026-1.pdf | `VM0042_SSA_Handbook_draft_2026-02-26.pdf` | M0264 page |

Optional, same page (save in the same folder, keeping Verra's own filename), only if the
comment goes further:
- greenlined §1–7: https://verra.org/wp-content/uploads/2026/02/1_VM0042v3_main_1-7_greenlined-draft_10FEB2026.pdf
- greenlined §8: https://verra.org/wp-content/uploads/2026/02/2_VM0042v3_main_8_greenlined-draft_10FEB2026.pdf
- greenlined appendices: https://verra.org/wp-content/uploads/2026/02/4_VM0042v3_appendices_greenlined-draft_10FEB2026.pdf
- VMD0053 v3.0 draft: https://verra.org/wp-content/uploads/2026/02/5_VMD0053v3_main_clean-draft_10FEB2026.pdf
- MVR template draft: https://verra.org/wp-content/uploads/2026/03/6_VMD0053v3_MVR-template_clean-draft_10FEB2026.pdf

## Project documents (not under `wp-content`; Verra registry UI only)

Folder: `data/registry/raw/verra/VCS4022/`. **No exact URL can be given**: the registry is a
client-rendered app that we cannot read (D-066). Find them in a browser at
`registry.verra.org` → VCS 4022 → Documents.

| # | document | save as | settles |
|---|---|---|---|
| 16 | VCS 4022 **Project Description**, latest registered version, incl. §4.4.4, Table 4-17, Appendices 6 and 9 | `PD_<version>_<YYYY-MM-DD>.pdf` | **whether 31.35% is the SOC-pool deduction** (the second condition on the 0.42× / 0.70× reading); sampling design, if the appendices are attached |
| 17 | any VCS 4022 monitoring or verification report, if one exists | `MonitoringReport_<period>_<date>.pdf`, `VerificationReport_<period>_<date>.pdf` | realised applied deduction after validation |
| 18 | the full VM0042 project export (for WP1c and the per-project public comments) | `verra_vm0042_projects.csv` in `data/registry/raw/verra/` | see `docs/registry_population.md` §3 |

**When the files are in place**, tell the session. It will compute and record the sha256 of
each file, re-read each C row in `pr21_reverification.md`, and close or correct D-072, D-073 and
D-075.
