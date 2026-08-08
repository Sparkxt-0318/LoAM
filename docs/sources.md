# Sources — bibliography and retrieval status

Status of every source behind `data/variance_table.csv`, as of 2026-08-07.

**Legend**
✅ full text read and values verified · 🟡 abstract or citing source only ·
🔴 not reached — values cannot be used

---

## ✅ Verified against full text

### Poeplau, Prietz & Don (2022)
*Plot-scale variability of organic carbon in temperate agricultural soils —
Implications for soil monitoring.* Journal of Plant Nutrition and Soil Science.
DOI [10.1002/jpln.202100393](https://doi.org/10.1002/jpln.202100393)

Publisher version is paywalled. An **accepted manuscript** was retrieved openly
via the German National Library (`d-nb.info/125318657X/34`) and is held at
`data/literature/poeplau2022_plot_scale_variability.pdf`.

Supplies rows: `VC-ANA-001`, `VC-WPS-001/002/003`, `VC-REL-001/002/003/004`
— the backbone of the table.

> ⚠️ **Volume and pagination unconfirmed.** The local copy is paginated 1–14
> (accepted manuscript). If you can reach the version of record, confirm the
> volume/issue/pages and update the eight citation fields in one pass.

Key values verified: within-plot SOC-stock CV by depth and land use (Table 4);
resampling MAE 5.1 (cropland) / 7.6 (grassland) Mg C ha⁻¹ at 0–30 cm;
~50% reduction for three-by-three resampling; MAE definition (Eq. 3);
20 × 20 m plots, 16 cores, 6.7 cm corer; analytical error ≈1%; the
"as great as … shifted by as much as 7 m" saturation statement.

### Fowler, Basso, Millar & Brinton (2023)
*A simple soil mass correction for a more accurate determination of soil carbon
stock changes.* Scientific Reports 13, 2242.
DOI [10.1038/s41598-023-29289-2](https://doi.org/10.1038/s41598-023-29289-2)

**Open access** — read via PMC9908890. Supplies `VC-BDC-001…004`.

Verified: the 17% figure is an **illustrative calculation** from a prescribed
scenario, described by the authors as "hypothetical but realistic" — not an
empirical measurement. Also verified: Scenario 1 sign reversal (16.2% apparent
loss on fixed depth vs 14.8% gain under ESM); residual bias ~8% at 15 cm
increments and ~6% at 10 cm.

### Even, Machmuller, Lavallee, Zelikova & Cotrufo (2025)
*Large errors in soil carbon measurements attributed to inconsistent sample
processing.* SOIL 11, 17–34.
DOI [10.5194/soil-11-17-2025](https://doi.org/10.5194/soil-11-17-2025)

**Open access.** Supplies `VC-ANA-003/004`. Not in the original anchor list;
added because it is the only source found that quantifies *processing* error,
which turns out to dominate instrument error.

> ⚠️ Depth interval (0–20 cm) was **inferred** from the sampling description.
> Confirm against the methods section before relying on these rows.

---

## 🟡 Verified from abstract or a citing source only

### Buchkowski, Polussa & Bradford (2026)
*Designing national forest inventories for accurate estimation of soil carbon
change.* Global Change Biology 32(4), e70868.
DOI [10.1111/gcb.70868](https://doi.org/10.1111/gcb.70868)

Publisher **paywalled (HTTP 402)**. Full abstract verified via
[PubMed 42037479](https://pubmed.ncbi.nlm.nih.gov/42037479/). The
[Zenodo record](https://zenodo.org/records/17976777) holds **analysis code
only**, not the manuscript.

Supplies `VC-BPS-001…004`, all marked out-of-scope (Canadian **forest**).

This source has **two distinct roles**, and conflating them is how it gets
mis-filed. Keep them separate:

**Role 1 — variance baseline: RULED OUT, permanently.**
A national **forest** inventory cannot supply a cropland variance baseline, no
matter how good the PDF turns out to be. Fetching it will *not* close gap
**G1**. If the build refuses these rows on scope grounds, **that is correct
behaviour and must not be overridden** — rules R7/R10 exist for exactly this.
The within/between SD partition it would give us (script `02_within_between.R`)
is still worth having as a *structural analogue* for `VC-BPS-003`, replacing our
interpreted 50/50 encoding — but as forest context, never as a cropland number.

**Role 2 — regression to the mean: PRIMARY SOURCE, retained.**
Buchkowski is our only source for the finding that an apparent gain of
2.3 Mg C ha⁻¹ 10 yr⁻¹ over the first remeasurement interval is consistent with
**regression to the mean** — i.e. a detected "change" that is a statistical
artifact of the design rather than a signal. That is land-use-independent
statistics, so the forest setting does **not** disqualify it.
**This is a Phase 3 dependency**, not a Phase 0 one: the simulator must be able
to reproduce the artifact, and `VC-BPS-004` is flagged as an external validation
target for it.

### Wuest (2024)
*Temporal variability is a major source of uncertainty in soil carbon
measurements.* Soil Science Society of America Journal.
DOI [10.1002/saj2.20660](https://doi.org/10.1002/saj2.20660)

Publisher **paywalled (HTTP 402)**. Abstract only. Supplies `VC-TMP-001/002` —
the only temporal anchor in the table.

> ⚠️ Volume/issue/pages **unconfirmed**. Sampling depth **assumed** to be
> 0–30 cm; the abstract does not state it.

> 🔶 **OPEN SCOPE QUESTION — for the PI, not for me to resolve.** These are
> Pacific Northwest **dryland** cropping systems. In scope on land use
> (cropland); arguably marginal on climate ("temperate"). Logged as **D-021**
> in [`DECISIONS.md`](../DECISIONS.md) and left open. The rows stay
> `in_scope: false` / `sensitivity_high` until it is decided — that is the
> conservative holding position, not an answer.

### Saby et al. (2008)
*Will European soil monitoring networks be able to detect changes in topsoil
organic carbon content?* Global Change Biology 14(10), 2432–2442.
DOI [10.1111/j.1365-2486.2008.01658.x](https://doi.org/10.1111/j.1365-2486.2008.01658.x)

Paywalled. The **values** (analytical error 2.5%; plot-scale CV 3.4%) were read
in Poeplau et al.'s discussion, not in Saby — hence `verified_secondary`. The
citation itself was verified against Poeplau's reference list.

Supplies `VC-ANA-002`, `VC-WPS-004`. Note Poeplau quotes the analytical figure
inconsistently ("2–3%" in one place, "2.5%" in another).

---

## 🔴 Not reached — values locked out of use

### Jones, Fernández-Ugalde & Scarpa (2020)
*LUCAS 2015 Topsoil Survey: Presentation of dataset and results.* Publications
Office of the European Union, EUR 30332 EN. ISBN 978-92-76-21080-1.
DOI [10.2760/616084](https://doi.org/10.2760/616084)

The catalogue record is reachable and the citation is confirmed from it, **but
the relocation statistic is not in the material we could reach.** The
80% / <10 m and 96.5% / <100 m figures appear only in secondary summaries.

`VC-REL-005/006` are therefore `verification: unverified` and
`use_as: placeholder_needs_pdf` — rule R6 locks them out of the OSSE.

**Confirmed from the record:** LUCAS topsoil is sampled to **20 cm**, not 30 cm
— a depth-basis mismatch with our scope that must be resolved regardless.

---

## What to chase next

Priority is set by **what can actually close a gap under the scope lock**, not
by how interesting the source is. An out-of-scope source cannot close an
in-scope gap however good its data — that was the error in the previous
ordering, which ranked a forest inventory first against a cropland gap.

| # | source | why it matters | can it close a gap? |
|---|--------|----------------|---------------------|
| **1** | **Poeplau et al. 2022** — site-level data | **In scope** (NE Germany cropland, temperate, 0–30 cm fixed depth). 8 cropland sites, each a 20×20 m plot: the variation *between* those sites is between-plot spatial variance, measured on known support. **The strongest candidate baseline we have for component 3.** | ✅ **G1** — the only listed source that can |
| 2 | **Wuest 2024** (SSSAJ, paywalled) | Confirm depth and sites; the only temporal anchor. Gated by the open scope question (D-021). | ⚠️ **G4**, conditionally — see D-021 |
| 3 | **LUCAS 2015 report** (JRC105923 / EUR 30332 EN) | Relocation-distance distribution. | ✅ **G6** — unlocks `VC-REL-005/006` |
| 4 | **Saby et al. 2008** (GCB, paywalled) | Promotes two `verified_secondary` values to primary. | ➖ hygiene, no gap |
| 5 | **Buchkowski et al. 2026** (GCB, paywalled) | **Not a cropland variance baseline — see Role 1/Role 2 above.** Wanted for the regression-to-the-mean finding. | ❌ cannot close G1 · 📌 **Phase 3** dependency |
| 6 | **Poeplau et al. 2022** version of record | Confirm volume/pagination only — values already verified. | ➖ citation hygiene |

### On #1 — what is actually needed

The Poeplau **text** is already held and fully verified; this is not a fetch
request. What is missing is the **site-level SOC stock data for the 8 cropland
sites** (the site characteristics table, ideally as supplementary data rather
than read off a PDF table), from which a between-plot variance can be derived.

Two caveats to settle before deriving anything, so they are recorded now rather
than discovered later:

- **n = 8.** A between-plot variance from 8 sites is imprecise, and the
  resulting confidence interval must be carried, not dropped.
- **The sites are not a random sample of temperate cropland.** They were chosen
  near German Soil Inventory points and span a wide SOC range by design, which
  probably *inflates* between-plot variance relative to a single region. That
  makes it conservative for detectability — but it is an assumption, and it
  needs a `D-NNN` entry when the derivation is done.

**Not attempted in this PR** — closing G1 is explicitly out of scope here.

Components 1, 2, 5 and 6 have verified in-scope baselines and can proceed to
Phase 1 as they stand.
