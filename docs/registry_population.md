# WP1: growing the auditable population

**Status: complete for ACCU and CAR1459. Verra is blocked; a hand-download procedure is at the end.**
Decisions: D-064 (ACCU area and rate), D-065 (scope flags), D-066 (CAR1459, access walls,
consultation status). Access date for everything new here: 2026-11-10.

| | before WP1 | after WP1 |
|---|---|---|
| projects that clear the audit gate | **1** (VCS 4022) | **56**: 54 credit-issued ACCU projects, CAR1459, VCS 4022 |
| of which in LoAM scope (cropland, temperate) | 1 | **11**: 9 ACCU, CAR1459\*, VCS 4022 |
| projects with a published *applied* uncertainty deduction | 1 | **2**: VCS 4022 (31.35%), CAR1459 (11.27%) |

\* CAR1459 is US cropland but its own monitoring plan lists tropical and boreal IPCC zones among
those it spans (MP v5.4 Table 6.10), with no area share given. It is kept in scope, as it was
before, and carries that note.

The out-of-scope 45 ACCU projects (38 grazing/pasture, 7 unresolved) clear the gate but are
**reported separately in WP2 and never pooled into a headline** (D-065, red team B-5).

---

## 1. ACCU: is there an area field? No. Is there an area? Yes.

The PI flagged a contradiction: `registry_corpus.md` (and D-056) said the register gives area for
999 projects; `phase5_inverted_audit_results.md` said there is no area field. Resolved from the
register itself (CSV re-pulled 2026-11-10, `Last-Modified` 2026-10-20, 3,088 rows × 73 columns,
sha256 `3481c436…bd983b7`):

| register column | what it holds | filled, of 999 soil projects |
|---|---|---|
| `Project Area(s), where the project is an area based offsets project` | cadastral **lot/plan identifiers**, e.g. `1/PS318577, 1/TP153840, …` — not hectares | 999 |
| `Project Mapping File URL` | a **KML of the project boundary** | **999** |
| `Carbon Estimation Area mapping file URL` | a **zipped shapefile of the carbon estimation areas** (the land credits are computed over) | **54 — exactly the 54 credit-issued projects** |

So: **no numeric area field exists** (the results doc was right about that), **but the boundary
files that determine area are published** (so the corpus doc's conclusion, though not its
wording, holds). Both earlier statements are corrected in place by notes pointing here.

**Derivation.** Geodesic area on GRS80 (the ellipsoid of GDA2020, which every CEA `.prj`
declares), via pyproj. Checks: a second, independent ring-sign computation agrees to 1e-4 on all
54; 99.7–100% of every CEA lies inside its own project-boundary KML. Every area is recorded as
`inferred` — it is our computation from a stated file, never a published number.

**Census, re-pulled** (definition stated explicitly for the first time: Method contains both
"Soil" and "Measurement", i.e. the 2018 and 2021 determinations; it reproduces 999 exactly):

| | 2026-06-30 (D-056) | 2026-10-20 (this pass) |
|---|---|---|
| soil carbon projects | 999 | **999** |
| credit-issued | 53 | **54** |
| ACCUs issued | 439,348 | **462,162** |
| `Estimation or measurement approach or model` filled | 24 | 26 |
| sampling-design fields of any kind | none | **none** |

**The disclosure census is unchanged in substance: 999 of 999 projects publish no sampling
design.** The 2014 grazing-systems method (30 projects, none issued) is counted separately.

### The 54 credit-issued projects

| | all 54 | in scope (9) |
|---|---|---|
| CEA area, ha | 36.7 · **184** · 3,877 (min · median · max) | 123 · **173** · 248 |
| ACCUs issued | 290 · 3,280 · 94,666 (total 462,162) | 290 · 2,334 · 5,610 (total 23,982) |
| net credited Δ, Mg C/ha (cumulative) | 0.55 · **4.86** · 17.8 | 0.55 · **4.23** · 9.41 |
| credited rate, lower bound, Mg C/ha/y | 0.15 · **1.27** · 4.36 | 0.15 · **1.27** · 3.26 |

**Δ is what the audit tests**: cumulative ACCUs ÷ 3.667 ÷ CEA area, the net credited change from
the baseline round to the latest one. The remeasurement interval cancels out of it (D-064). The
**rate** divides Δ by the time from crediting start to 30 June of the last financial year with an
issuance; issuance follows the end of a reporting period, so that time is an upper bound and the
rate is a **lower bound**. It is reported for comparison with the literature only.

*A note that belongs with these numbers.* The median credited rate across the 54 (≥1.27 Mg C/ha/y,
net) is several times the ~0.3 Mg C/ha/y Potash et al. take as typical (and VCS 4022's 0.31). That is
a statement about the population, recorded because it is what the register implies. It is
not a statement about any project: the register publishes no SOC measurement against which a
credited rate could be checked, and large Δ makes a claim *easier* to detect, not harder.

## 2. CAR1459: credits retrieved, and a second published deduction

From the Reserve's public document list and registry tab (sources `car1459_*` in `projects.yaml`):

| reporting period | area (acres) | credits issued (tCO2e) | applied UNC |
|---|---|---|---|
| RP1 (to 2020-12-31) | 100,372 | 22,225 | — |
| RP2 (to 2021-12-31) | 423,740 | 111,389 | — |
| RP3 (to 2022-12-31) | 1,289,361 | 163,048 | — |
| RP4 (to 2023-12-31) | 1,517,893 | 630,634 | **14.17%** |
| RP5 (to 2024-12-20) | **2,463,691** | 1,186,565 | **11.27%** |
| cumulative | | **2,113,861** (2,033,891 SOC + 80,639 non-SOC) | |

**What the audit uses**: RP5's SOC-only credits (1,065,452.3 tCO2e, Table 7) over RP5's own area,
Δ = **0.291 Mg C/ha** net — the one claim/area pair the source document scope-matches itself.
The cumulative total mixes non-SOC credits and five periods over an area that grew 24.5-fold.

Two things recorded as the documents state them:
- **The applied deduction is published**: 11.27% (RP5), recalculated by the verifier (RP5
  Verification Report §5.2.4). Under CAR SEP's rule that is a relative SE of ~10.96%, pooling
  sampling, model-input and model-prediction error.
- **Quantification through RP5 rests on initial measurements plus DayCent-CR.** The RP5
  Verification Report §5.2.3: *"Quantification was based on the initial SOC measurements, with the
  earliest samples being taken in October 2019"*; the 5-yearly re-measurement "true-up" was
  deferred by Reserve variance determination 2025-VAR-2-DET-CAR1459. This is the Reserve's own
  documented process. It matters to the audit's meaning: the audit asks what re-measurement
  would detect the claim, and as of RP5 none had been applied.

Still not disclosed: the realised number of sample points (MP v5.4 gives the rules only).

## 3. Verra: an access wall, and the hand-download procedure

**Two attempts, both walled** (D-066): `registry.verra.org` now serves an S&P Global "Platts"
single-page app with Okta sign-in; the old `/uiapi` search returns the HTML shell, and the app
bundle names no API. An enumeration-only fallback (CarbonPlan OffsetsDB API) returns
`DEPLOYMENT_NOT_FOUND`. Web search finds no machine-readable list of VM0042 project IDs; Verra
itself says about 200 projects are listed under earlier VM0042 versions (late 2025). **This is an
access wall, not a disclosure gap, and is never counted as one.**

I cannot give exact project IDs without the registry, so the most efficient hand step is **one
export, then per-project documents**:

**Step 1 — one export (about five minutes).** In a browser at `https://registry.verra.org/`:
Programs → VCS → filter Methodology = **VM0042** (all versions), Status = **all** (Registered,
Under validation, Under development, Registration requested, …). Export the list (the new
registry advertises "customizable reporting tools"; if there is no export button, copy the table).
Save as `data/registry/raw/verra/verra_vm0042_projects.csv` with at least: project ID, name,
proponent, status, methodology version, country, estimated annual ERRs, and the public-comment
URL where one exists.

**Step 2 — per project, these documents**, saved as
`data/registry/raw/verra/VCS<ID>/<doctype>_<version-or-date>.pdf`:

| doctype | why the audit needs it |
|---|---|
| `PD` (Project Description), **with all appendices** | area, practices, quantification approach; sampling design if published (VCS 4022's is in Appendices 6 and 9) |
| `ValidationReport` | VCS 4022's applied deduction (31.35%) came from here |
| `MonitoringReport` (each) | realised ERRs, area, **applied uncertainty deduction per period** |
| `VerificationReport` (each) | the verifier's confirmation of the deduction |
| any uncertainty workbook (`.xlsx`/`.zip`) | VCS 4022's validation report names `uncert_deduct_proj.zip`, not public |

**Priority, if time is short:** (a) every project with status *Under validation (public comment
period open)* — PD only, plus the public-comment URL (WP4 needs these); (b) every project with at
least one issuance — Monitoring and Verification Reports first (they carry the applied deduction);
(c) everything else.

Once Step 1 lands, `scripts/` will grow a reader for it, and every field enters `projects.yaml`
with status/source/locator exactly as VCS 4022 did.

**One standing constraint, carried from PR #21 and not yet a decision on `main`:**
`verra.org/robots.txt` disallows `/wp-content/uploads`, where Verra's methodology PDFs live. No
file under that path was fetched this session. Project documents are served by the registry, not
from that path.
