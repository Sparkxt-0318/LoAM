# Sources — bibliography and retrieval status

Status of every source behind `data/variance_table.csv`, as of 2026-08-08.

**Legend**
🟢 primary data held, derived by us · ✅ full text read and values verified ·
🟡 abstract or citing source only · 🔴 not reached — values cannot be used

---

## 🟢 Primary data held — derived by us

### Soil Health Institute (2024) — NAPESHM
*North American Project to Evaluate Soil Health Measurements* [data set].
DOI [10.15482/USDA.ADC/25632270](https://doi.org/10.15482/USDA.ADC/25632270)
Design and the 0–15 cm sampling protocol: Norris, C. E., et al. (2020).
*Introducing the North American project to evaluate soil health measurements.*
Agronomy Journal 112(4), 3195–3215.

**Open access.** Held at `data/raw/napeshm/` (gitignored — re-download below).
Derivation: `scripts/derive_g1_napeshm.py` → `data/processed/g1_napeshm.json`.

```bash
curl -sSL -o napeshm.zip https://ndownloader.figshare.com/files/46794877
# md5 b6a0a7cd8123c556c82a0d3384084a83
unzip napeshm.zip && mv "CSV Files"/*.csv data/raw/napeshm/
```

**PRIMARY SOURCE for component 3 (between-plot spatial).** Supplies
`VC-BPS-005` (concentration, CV 12.1%) and `VC-BPS-006` (stock, CV 11.1%),
which together close gap **G1**.

Why it takes primacy: 212 experimental units across 61 treatments and 14 sites,
with an explicit randomized design, on the right continent for a North American
audit. Replicate EUs under identical management at one site differ only by
spatial heterogeneity plus analytical error.

Three limits that travel with every number derived from it:

- **0–15 cm**, fixed by protocol and **absent from the dataset entirely** — the
  depth is cited to Norris et al., not to the data (D-026). Rows are *scoped* to
  0–15 cm, never rescaled to our 0–30 cm project scope.
- **Upper bound, not a point estimate.** No lab duplicate, split-sample or QC
  columns exist, so analytical error cannot be separated from spatial error
  (D-027). Both rows carry `bias_direction: inflates`.
- **Climate envelope unresolved** (D-028). Site MAT spans 4–25 °C and includes
  16 Mexican sites. The headline uses a *proposed* temperate envelope; the
  estimate moves only 10.6–12.1% across every candidate, so the open question is
  about defensibility of scope rather than about the number.

Cover crops are nearly absent (58 of 61 treatments have none), so NAPESHM
constrains the **tillage** half of our management scope and says little about
the cover-crop half.

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

> **Role change (D-030).** Poeplau is **no longer the candidate baseline for
> component 3** — NAPESHM is (above). Poeplau is now an **independent
> cross-check**, and that is a promotion in usefulness, not a demotion in
> quality: different continent, different design, different support, 8 sites
> against 14. Its within-plot stock CV of **9.3–10.2%** sits just below the
> NAPESHM between-plot estimate of **11.1–12.1%**, which is the ordering you
> would expect if both are right, and is the strongest corroboration either
> number has. It must never *be* the between-plot baseline: it does not measure
> a between-plot term.
>
> This also narrows gap **G3** without closing it — see the gaps table in
> `DECISIONS.md`. A within/between ratio near 1 in cropland would echo
> Buchkowski's forest finding, but two different studies on two continents at
> two depths cannot establish that, and no row claims it.
>
> Poeplau remains the sole source for `VC-ANA-001`, `VC-WPS-001/002/003` and
> `VC-REL-001/002/003/004`, which are unaffected.

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

**G1 is now closed** by the NAPESHM derivation, which changes this ordering: the
remaining gaps are temporal (G4) and relocation (G5/G6).

| # | source | why it matters | can it close a gap? |
|---|--------|----------------|---------------------|
| **1** | **Wuest 2024** (SSSAJ, paywalled) | Confirm depth and sites; still the only temporal anchor, and `temporal` is now the **only** component without a baseline. Gated by the open scope question D-021. | ⚠️ **G4**, conditionally — see D-021 |
| 2 | **LUCAS 2015 report** (JRC105923 / EUR 30332 EN) | Relocation-distance distribution. | ✅ **G6** — unlocks `VC-REL-005/006` |
| 3 | **Saby et al. 2008** (GCB, paywalled) | Promotes two `verified_secondary` values to primary. | ➖ hygiene, no gap |
| 4 | **Buchkowski et al. 2026** (GCB, paywalled) | **Not a cropland variance baseline — see Role 1/Role 2 above.** Wanted for the regression-to-the-mean finding. | ❌ never could close G1 · 📌 **Phase 3** dependency |
| 5 | **Poeplau et al. 2022** — site-level data | Would give a *second, independent* between-plot estimate (8 German sites) against NAPESHM's 14 North American ones. No longer needed to close G1, but the strongest available check on it. | ➖ corroboration, not a gap |
| 6 | **Poeplau et al. 2022** version of record | Confirm volume/pagination only — values already verified. | ➖ citation hygiene |

### On #5 — still worth doing, for a different reason

Now that NAPESHM closes G1, the Poeplau site-level data is no longer load-bearing
— it is the best available **independent replication**. Two caveats stand
whenever it is attempted:

- **n = 8.** A between-plot variance from 8 sites is imprecise, and the resulting
  confidence interval must be carried, not dropped.
- **The sites are not a random sample of temperate cropland.** They were chosen
  near German Soil Inventory points and span a wide SOC range by design, which
  probably *inflates* between-plot variance relative to a single region. That
  makes it conservative for detectability — but it is an assumption needing its
  own `D-NNN` when the derivation is done.

Components 1, 2, 3, 5 and 6 have verified in-scope baselines and can proceed to
Phase 1 as they stand.

---

## 📥 To obtain

Not yet held. Logged so the next literature pass starts from a list rather than
from memory. None of these is currently cited by any row.

| source | why | priority |
|---|---|---|
| **Potash, Bradford, Oldfield & Guan 2025**, *Environ. Res. Lett.* **20** 024025, doi:10.1088/1748-9326/ada16c (**open access**; data doi:10.6084/m9.figshare.28083182; R source `asc.illinois.edu/soc-econ`) | **Nearest prior art.** Their error model splits interval-scaling from measurement error, which our schema cannot currently represent — see D-035. Parameters and positioning logged in D-036/D-037/D-038. | **1 — highest** |
| **Smith 2004**, *Global Change Biology*, "How long before a change in soil organic carbon can be detected?" | **Foundational detectability paper — we cite nothing from it.** This is the question the whole testbed asks, asked twenty years earlier. Not citing it is a real hole in the writeup, not a nicety. | **2** |
| **Saby et al. 2008**, *Global Change Biology*, European soil-monitoring networks | The other foundational detectability paper, and the primary source behind two rows currently held at `verified_secondary`. Closes both a citation gap and a verification gap. | **3** |
| **von Haden et al. 2020**, *Global Change Biology* **26** 3759 | Equivalent soil mass vs fixed depth. Directly bears on D-007 and D-026, and on the `VC-BDC-*` rows — the mechanism behind our depth-convention component. | 4 |
| **Bradford et al. 2023**, *Geoderma* **440** 116719 | Same group as Potash et al.; likely the source of several of their parameter choices. | 5 |
| **de Gruijter et al. 2016**, *Geoderma* **265** 120 | Sampling design for soil monitoring — the design-side counterpart to our variance-side question. | 6 |

**Smith 2004 and Saby et al. 2008 are the two foundational detectability papers
and we currently cite neither.** That is the most conspicuous omission in the
bibliography as it stands; everything else on this list is an improvement,
those two are a gap.
