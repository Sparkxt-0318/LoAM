# G9 literature pass: how SOC between-location variance depends on support

**Provenance.** Written 2026-11-10 by a separate research agent briefed only on the G9 question (WP3(iii)), reproduced here unedited below this note. Every claim carries an access code (FT = full text read; AB = abstract only; CIT = seen cited; TI = title only). Most publisher hosts were blocked from this environment, so only four sources were read in full; the access-wall log is §4. Nothing behind a wall was used as evidence. How the audit uses this: `docs/phase5_robustness.md` §(iii) and DECISIONS.md D-070.

---


Prepared 2026-11-10. Scope: how the spatial (between-location) variance of SOC **stock** and of SOC **stock change** depends on sampling support and extent, and whether a sigma_B taken from replicate research plots (0.02 ha plots, 3.6 m x 53 m, one site; CV about 3.1 % at 0-30 cm; about 11.5 % at 0-15 cm in a broader cross-site dataset) under- or over-states the sigma_B for sample locations spread over commercial fields (tens to hundreds of ha) and projects (100 ha to 1,000,000 ha).

## How to read this file

**Access codes** (used in every row and every claim):

- **FT**: I read the full text myself; the locator points to a page, section, table or figure.
- **AB**: I read the abstract only. The locator says where the abstract came from: PubMed (eutils), OpenAlex, or Semantic Scholar.
- **CIT**: I saw the claim only as cited in another paper, which I name.
- **TI**: I saw the title or bibliographic metadata only (Crossref).

**Other conventions:**

- Numbers are copied as the source gives them. Where I derived a number (a ratio, or a CV backed out of an MDD), it is marked **[my calculation]** and the inputs are shown.
- Distinctions kept throughout: stock vs concentration; stock vs stock change; depth; land use; and whether a variance is within a field or site, between fields or sites, or between regions.

**Access situation:** most publisher hosts were blocked in this session. These include ScienceDirect, Wiley Online Library, ACSESS (Cloudflare challenge), Springer (JavaScript challenge), IOP, MDPI, CSIRO, institutional repositories, arXiv, eScholarship, Dryad and Zenodo (see §4). Only bg.copernicus.org, soil.copernicus.org, PMC/eutils, OpenAlex (single-record lookups), Crossref and Semantic Scholar were readable. So most of the quantitative MRV literature (Bradford, Stanley, Potash, Poeplau, Polussa, Goidts) is represented here at **abstract level only**. Only four sources were read in full text: Schrumpf et al. 2011, Buchkowski et al. 2026, Martin et al. 2011 and de Blécourt et al. 2017.

---

## 1. Source table

| # | Citation | DOI / URL | Access | Land use | Depth | Support / extent | Quantity | Reported variance / CV (exact, with units) | Locator |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Schrumpf M, Schulze ED, Kaiser K, Schumacher J (2011) How accurately can soil organic carbon stocks and stock changes be quantified by soil inventories? *Biogeosciences* 8:1193–1212 | 10.5194/bg-8-1193-2011 | **FT** | 3 croplands, 3 grasslands, 6 forests (Europe) | 0–5, 0–10, 0–30, 0–60 cm | Single cores (inner diameter 8.3 and 8.7 cm), 100 points per site on a regular grid at 10–15 m spacing; cropland/grassland plots 1–2 ha; forests 7–8 ha (Hainich 24 ha). **Within-site** | OC **stock**, by volume and by equivalent soil mass | 0–0.30 m, by volume (mean, s.d. in g OC m−2; CV %). **Croplands:** Carlow 6036, 852, **14 %**; Gebesee 8650, 473, **5 %**; Grignon 8241, 812, **10 %**. **Grasslands:** Laqueuille 15 713, 1254, **8 %**; Bugac 9232, 1552, **17 %**; Easter Bush 9260, 1014, **11 %**. **Forests:** Hainich 14 %, Hesse 16 %, Soroe 34 %, LeBray 24 %, Wetzstein 26 %. 0–0.10 m cropland CVs: 21 %, 9 %, 12 %. Text: "The CV decreased with increasing soil volume considered". MDD assumes "Paired re-sampling and constant variability of OC stocks for the second sampling period". Note: the methods text gives β = 0.10 but the Table 2 caption gives β = 0.2. | Sampling design: Sect. 2.2, p. 1196. Corer: p. 1197. Table 2, pp. 1198–1199. MDD method: p. 1201. CV vs volume: Sect. 3.2, p. 1203. MDD results: Sect. 3.3, p. 1204 |
| S2 | Buchkowski RW, Polussa A, Bradford MA (2026) Designing national forest inventories for accurate estimation of soil carbon change. *Global Change Biology* 32:e70868 | 10.1111/gcb.70868 (PMC13112338) | **FT** | Forest (Canada NFI) | Mineral 0–15 cm; organic horizon | Up to 4 microplots per plot at the ends of two 30 m transects. Remeasurement offset 2 m clockwise. 532 plots, national extent ("tens to thousands of kilometers"). **Within-site vs between-site** | **Stock** and **stock change** (paired microplots, about 10 yr) | **Stock:** "Between-site standard deviation in soil carbon stock was 44% and 70% of the mean value for the mineral and organic horizons, respectively. Within-site variation was only slightly lower at 41% and 68%". Simulation inputs: "empirical within and between average standard deviation of 17.3 and 19.0 Mg ha−1" (horizon not named in that sentence). **Change:** "between-site standard deviation for change in soil carbon stocks was 18.5 and 18.9 Mg ha−1 over a 10-year period for mineral and organic horizons… Within-site standard deviation was larger at 31.5 and 46.7 Mg ha−1 10 year−1". Patterns are consistent with regression to the mean; the first-interval change of 2.3 Mg ha−1 10 yr−1 was not reproduced in the second interval (n = 51 plots). | Abstract; Sect. 2.1 (design); Sect. 2.2.1–2.2.3 (Eq. 1–7, simulation inputs); Sect. 3.1 and Fig. 2; Sect. 3.2 and Fig. 3; Fig. 6 |
| S3 | Martin MP, Wattenbach M, Smith P, et al. (2011) Spatial distribution of soil organic carbon stocks in France. *Biogeosciences* 8:1053–1065 | 10.5194/bg-8-1053-2011 | **FT** | All land uses; "various crops" n = 817 | 0–30 cm | Composite of 25 cores, stratified random within 20 m x 20 m. 16 km x 16 km grid; national extent (about 2200 sites). **Between sites, national** | **Stock** | Forest: median 7.00 kg m−2, SD 3.42 kg m−2. Permanent grassland: median 7.57 kg m−2, SD 3.51 kg m−2. "Dispersion of values on cultivated areas, excluding permanent grasslands was low (**1.85 kg m−2**)". The cropland median is not given in the text; it is plotted in Fig. 2 only. | Sect. 2.1, p. 1054. Fig. 2 caption, p. 1056. Sect. 3.1, p. 1058 |
| S4 | de Blécourt M, Corre MD, Paudel E, Harrison RD, Brumme R, Veldkamp E (2017) Spatial variability in soil organic carbon in a tropical montane landscape… *SOIL* 3:123–137 | 10.5194/soil-3-123-2017 | **FT** | Mostly forest; tea and grassland (SW China) | 0–0.15, 0.15–0.3, 0–0.9 m | Subplots (10 m radius) within 1 ha plots; 27 plots 0.5–12 km apart within a 10 000 ha landscape. **Nested ANOVA (REML)** | **Stock** and concentration | "variability within plots accounted for more than 50 % of the overall variance in SOC stocks to a depth of 0.9 m and the topsoil SOC concentrations". For soil properties in the top 0.3 m (Fig. 3a): "the variability among plots (nested within land-use type) and among subplots (nested within plots) contributed relatively equally". The paper also cites Chaplot et al. 2009 (Laos), where "85 % of the variance in SOCc and SOCs occurred at a 20 m scale" (**CIT**). | Abstract; Sect. 3.3; Fig. 3; Discussion p. 132 |
| S5 | Goidts E, van Wesemael B, Crucifix M (2009) Magnitude and sources of uncertainties in SOC stock assessments at various scales. *Eur J Soil Sci* 60:723–739 | 10.1111/j.1365-2389.2009.01157.x | **AB** (OpenAlex) | Agriculture (cropland and grassland), southern Belgium | not in abstract | "different scales and spatial landscape units"; field up to region | **Stock** | "the coefficient of variation of the SOC stock increased across scales (from 5 to 35%), and was higher for grassland than for cropland". **Note:** the French résumé in the same abstract says the opposite on land use ("plus élevé pour les cultures que pour les prairies"). Also: the regional monitoring "allows the detection of an average SOC stock change of 20% within 11 years if very high rates… (1 t C ha–1 year–1)". Buchkowski et al. (S2) cite it as CV "up to 30%" (**CIT**). | Abstract |
| S6 | Conant RT, Paustian K (2002) Spatial variability of SOC in grasslands: implications for detecting change at different scales. *Environ Pollut* 116 Suppl 1:S127–S135 | 10.1016/S0269-7491(01)00265-2 | **AB** (PubMed 11833900) | Grassland (USA) | not in abstract | County, state and national scale (NRCS pedon database) plus farm-level data | **Stock change** detectability | Changes "can be verified (alpha=0.1) after 5 years with collection of 34, 224, 501 samples at the county, state, or national scales, respectively". At farm level, "equivalent numbers of cores and distinct groups of cores (microplots) results in lowest soil C coefficients of variation". Buchkowski et al. (S2) cite CV "10%–24% (Conant and Paustian 2002)" (**CIT**). | Abstract |
| S7 | Conant RT, Smith GR, Paustian K (2003) Spatial variability of soil carbon in forested and cultivated sites: implications for change detection. *J Environ Qual* 32:278–286 | 10.2134/jeq2003.2780 | **AB** (PubMed 12549567) | Tilled cropland and forest (TN, WA) | not in abstract | 6 cores in each of 3 microplots, plus 6 more cores to simulate resampling | **Stock change** detectability | "differences on the order of 2.0 Mg C ha(-1) could be detected by… cores from at least five (tilled) or two (forest) microplots in Tennessee". "consistent intramicroplot differences at all sites will enable detection of much more modest changes if the same microplots are resampled". | Abstract |
| S8 | Zhang W, Weindorf DC, Zhu Y (2011) Soil organic carbon variability in croplands: implications for sampling design. *Soil Science* 176:367–371 | 10.1097/SS.0b013e31821eb7d2 | **AB** (OpenAlex) | Cropland (compilation) | various | 117 CVs from 41 studies; varying sampling area and interval | SOC **concentration** | "mostly low (CV, <15%) to moderately (CV, 15%-35%) variable. Significant linear relationships existed between the CV and sample size, and between the CV and log (sampling area)… also… between the CV and log (sampling interval)". The **sign** of the CV–area slope is not stated in the abstract. It is implied positive by "suggesting that stratified sampling may reduce SOC variation". | Abstract |
| S9 | Polussa A, Oldfield EE, Runge T, Evans EK, et al. (2026) Counterfactual designs for quantifying management effects on soil carbon change at multi-field scales. *Geoderma* 473:118007 | 10.1016/j.geoderma.2026.118007 | **AB** (OpenAlex) | Commercial cropland, Hudson Valley NY | 0–15 cm | 80 commercial fields; 0.6 ha per core (about 10 locations per field; 796 points). Two time points about 1 yr apart. **Within-field vs between-field** | **Concentration** (%C), level and **change** | "Spatial variability in soil carbon was large both within and among fields (between field SD 0.59 %C). Using the difference in soil carbon between the time points removed persistent spatial signal and reduced between-field variability in change more than seven times (SD 0.08 %); within-field variability remained high. Minimum detectable differences from repeated measurement were roughly six-times smaller than those inferred from spatial data alone (0.33 vs. 0.056 %C)". | Abstract |
| S10 | Poeplau C, Prietz R, Don A (2022) Plot-scale variability of organic carbon in temperate agricultural soils—implications for soil monitoring. *J Plant Nutr Soil Sci* 185:403–416 | 10.1002/jpln.202100393 | **AB** (OpenAlex) | 8 croplands and grasslands, NE Germany | 0–30 cm | Profile pits resampled after "a minimum shift in sampling location"; 16 cores per site | **Stock**; resampling error, i.e. change at zero true change | "Spatial dependence of all assessed parameters was weak." "the resampling of one profile by one induced a high mean absolute error of 5.1 and 7.6 Mg C ha–1 at a 0–30 cm depth for croplands and grasslands (7.5% and 8.5%). This error was reduced by approximately 50% when three profiles were resampled by three profiles." S2 cites the CV as "~9% (Poeplau et al. 2022)" (**CIT**). | Abstract |
| S11 | Bradford MA, Eash L, Polussa A, et al. (2023) Testing the feasibility of quantifying change in agricultural soil carbon stocks through empirical sampling. *Geoderma* 440:116719 | 10.1016/j.geoderma.2023.116719 | **AB** (OpenAlex) | Cropland, 45 fields | not in abstract | Within-field high density ("0.1 ha sample–1"); simulated designs at 1.2 vs 4.0 ha per sample; 10–30 fields | **Stock change** (simulated) | "stock change estimates for individual fields are inaccurate and variable, where marked losses and gains in SOC stocks are frequently estimated even when no change has occurred". At project level, with higher density and about 30 fields, "∼ 80 % of the estimates falling within 20 % of the simulated stock change". No CV values in the abstract. | Abstract |
| S12 | Stanley PL, Spertus JV, Chiartas JL, Stark PB, Bowles TM (2023) Valid inferences about soil carbon in heterogeneous landscapes. *Geoderma* 430:116323 | 10.1016/j.geoderma.2022.116323 | **AB** (OpenAlex) | 1 rangeland, 7 croplands (California) | not in abstract | 662 + 455 samples | Stock and concentration | "spatial heterogeneity is a primary driver of uncertainty". "common sample sizes of 10–30 cores cannot reliably detect the modest changes in SOC". Advises compositing "less than is currently common". No CV values in the abstract. | Abstract |
| S13 | Potash E, Bradford MA, Oldfield EE, Guan K (2025) Measure-and-remeasure as an economically feasible approach to crediting SOC at scale. *Environ Res Lett* 20:024025 | 10.1088/1748-9326/ada16c | **AB** (OpenAlex) | Cropland projects (modelled) | not in abstract | Two-stage cluster sampling: fields, then points within fields | **Stock change** | The model accounts for "within-field and between-field variability in SOC change, as well as measurement error". Parameter values are not in the abstract. | Abstract |
| S14 | Potash E, Guan K, Margenot AJ, et al. (2022) How to estimate SOC stocks of agricultural fields? *Geoderma* 411:115693 | 10.1016/j.geoderma.2021.115693 | **AB** (Semantic Scholar) | Cropland, 1 field | 0–60 cm | High-density single field | **Stock** | Balanced and stratified sampling using Sentinel-2 and TWI covariates "offer substantial improvements over simple random sampling". No variance values in the abstract. | Abstract |
| S15 | Necpálová M, Anex RP, Kravchenko AN, et al. (2014) What does it take to detect a change in soil carbon stock? *J Soil Water Conserv* 69:517–531 | 10.2489/jswc.69.6.517 | **AB** (OpenAlex) | Cropland **research plots**, 13 sites in the US Midwest | 4 depths; values quoted for 0–10 cm | RCBD replicate plots at each site | **Concentration**; between-treatment difference and change over time | "At 0 to 10 cm… MDDs with five replications ranged from 1.04 g C kg−1… 6%) to 7.15 g C kg−1… 31%) for comparison of two treatments; and from 0.46 g C kg−1… 3%) to 3.12 g C kg−1… 13%) for SOC change over time." MDD was "correlated with SOC variability and soil texture". [my calculation, assumption-laden: if MDD = (t_α/2 + t_β)·√(2/5)·CV with α = 0.05 and β = 0.15, the implied residual between-plot CV is about 2.4–12.4 % with df = 4, or about 3.2–16.4 % with large df.] | Abstract |
| S16 | Wuest SB, Durfee N (2024) Temporal variability is a major source of uncertainty in soil carbon measurements. *SSSAJ* 88:830–845 | 10.1002/saj2.20660 | **AB** (OpenAlex) | Dryland cropland field experiments, US Pacific NW; 12 commercial fields | not in abstract | Monthly sampling for up to 3 yr | Concentration or stock (not specified in abstract); variance components | "The variance from month-to-month was 15%–32% of the random error, averaging 20%. This was often greater than the variance between replicate experimental units (2%–42%, averaging 17%)." | Abstract |
| S17 | Lark RM (2009) Estimating the regional mean status and change of soil properties: two distinct objectives for soil survey. *Eur J Soil Sci* 60:748–756 | 10.1111/j.1365-2389.2009.01156.x | **AB** (OpenAlex) | General / SOC model example | n/a | Regional | Status vs **change** | "the status and change of an indicator are different variables and so their variability may differ… information on the variability of the change in soil is not in general available". "Paired sampling… is generally preferable… unless the error from relocation… is large". Monitoring requirements "might not be apparent until a reconnaissance resampling is undertaken". | Abstract |
| S18 | Papritz A, Webster R (1995) Estimating temporal change in soil monitoring: I. Statistical theory; II. Sampling from simulated fields. *Eur J Soil Sci* 46:1–12; 13–27 | 10.1111/j.1365-2389.1995.tb01808.x ; 10.1111/j.1365-2389.1995.tb01809.x | **AB** (OpenAlex) | Theory and simulation | n/a | Finite fields | **Change** | "Pairing the sampling positions on the different occasions increases the precision of design–based estimation if the observations are positively cross–correlated." (Part I). Part II confirms this in simulation. | Abstracts |
| S19 | Ellert BH, Janzen HH, Entz T (2002) Assessment of a method to measure temporal change in soil carbon storage. *SSSAJ* 66:1687–1695 | 10.2136/sssaj2002.1687 | **AB** (OpenAlex) | Cropland microsites | layers to more than 35 cm | Microsite 4 m x 7 m; interspersed cores at time 1 and time 2 | **Change** (3.64 Mg C ha−1 coal added) | "coal C recovery ranged from 91 to 106%" for paired temporal differences in equivalent mass. With spatial comparisons, "coal C became undetectable when soil thickness exceeded 35 cm". | Abstract |
| S20 | Lark RM (2012) Some considerations on aggregate sample supports for soil inventory and monitoring. *Eur J Soil Sci* 63:86–95 | 10.1111/j.1365-2389.2011.01415.x | **AB** (OpenAlex) | Transect, central England | not in abstract | Core support vs two 20 m x 20 m aggregate supports | SOC **content** | "both the precision and the consistency of data collected on an aggregate support are better than data on a core support". Gives a method to compute aggregate-support statistics from the core-support covariance ("discrete regularization"). | Abstract |
| S21 | Smith HF (1938) An empirical law describing heterogeneity in the yields of agricultural crops. *J Agric Sci* 28:1–23 | 10.1017/S0021859600050516 | **AB** (OpenAlex) | Crop **yield** (not SOC) | n/a | Plots of varying area within blank trials | Yield variance vs plot area | "the regression of the logarithms of the variances for plots of different areas on the logarithms of their areas was approximately linear… most such experiments conform to the same law". | Abstract |
| S22 | Cambardella CA, Moorman TB, Novak JM, et al. (1994) Field-scale variability of soil properties in central Iowa soils. *SSSAJ* 58:1501–1511 | 10.2136/sssaj1994.03615995005800050033x | **AB** (OpenAlex) | Cropland, 2 Iowa fields | not in abstract | Within-field variograms | Organic C **concentration** | Organic C was "strongly spatially dependent" at both sites (nugget less than 25 % of total semivariance). | Abstract |
| S23 | Robertson GP, Klingensmith KM, Klug MJ, et al. (1997) Soil resources, microbial activity, and primary production across an agricultural ecosystem. *Ecol Appl* 7:158–170 | 10.1890/1051-0761(1997)007[0158:SRMAAP]2.0.CO;2 | **AB** (OpenAlex) | Cropland, 48 ha (Michigan) | not in abstract | About 600 locations; lags 1–1200 m | Total C among many properties | "for most properties and processes >50% of sample variance was spatially dependent at a scale of 5–60 m". Total C is not singled out in the abstract. | Abstract |
| S24 | Saby N, Bellamy P, Morvan X, Arrouays D, et al. (2008) Will European soil-monitoring networks be able to detect changes in topsoil organic carbon content? *Global Change Biol* 14:2432–2442 | 10.1111/j.1365-2486.2008.01658.x | **AB** (OpenAlex); value **CIT** | National networks, Europe | topsoil | National | Concentration **change** (MDC) | Abstract: MDCs "differed considerably among the soil-monitoring networks", with about 10 yr needed for large changes. No numbers in the abstract. S2 cites a CV of "4% (Saby et al. 2008)" (**CIT**; quantity and scale not specified there). | Abstract; S2 Discussion |
| S25 | Garten CT, Wullschleger SD (1999) Soil carbon inventories under a bioenergy crop (switchgrass): measurement limitations. *J Environ Qual* 28:1359–1365 | 10.2134/jeq1999.00472425002800040041x | **AB** (OpenAlex) | Switchgrass field trials | 0–40 cm | 4 field-trial locations | **Stock** MDD | "a difference of ≈50 mg SOC/cm2 or 5 Mg SOC/ha, which is ≈10 to 15% of existing SOC, could be detected with… (n = 16)… ≈2 to 3%… only with exceedingly large sample sizes (n > 100)". | Abstract |
| S26 | Allen DE, Pringle MJ, Page KL, Dalal RC (2010) A review of sampling designs for the measurement of SOC in Australian grazing lands. *Rangeland J* 32:227–246 | 10.1071/RJ09043 | **AB** (OpenAlex) | Grazing lands | n/a | Review | Stock and **change** | "paired sites are the most efficient way of detecting a temporal change in SOC stock… an efficient sampling scheme to estimate baseline status is not likely to be an efficient sampling scheme to estimate temporal change". | Abstract |
| S27 | Skøien JO, Blöschl G (2006) Sampling scale effects in random fields and implications for environmental monitoring. *Environ Monit Assess* 114:521–552 | 10.1007/s10661-006-4939-z | **AB** (PubMed 16583302) | Generic random fields | n/a | Spacing, extent, support ("scale triplet") | Apparent spatial variance | "the biases can be up to two orders of magnitude… the bias of the spatial variance is different for different components of the scale triplet… All sampling scale effects are relative to the underlying correlation length". The abstract does not state the direction for each component. | Abstract |
| S28 | Kravchenko AN, Robertson GP (2011) Whole-profile soil carbon stocks: the danger of assuming too much from analyses of too little. *SSSAJ* 75:235–240 | 10.2136/sssaj2010.0076 | **AB** (Semantic Scholar) | Research experiments | whole profile | Replicated plots | Stock and concentration | "the chances of detecting even substantial (e.g., 50%) differences among experimental treatments can be as low as 20 to 60% due to the natural variability". | Abstract |
| S29 | Maillard É, McConkey BG, Angers DA (2017) Increased uncertainty in soil carbon stock measurement with spatial scale and sampling profile depth in world grasslands: a systematic analysis. *Agric Ecosyst Environ* 236:268–276 | 10.1016/j.agee.2016.11.024 | **TI** (Crossref); value **CIT** | Grassland, global review | various | various | **Stock** | The title asserts that uncertainty increases with spatial scale. S2 cites "values for grasslands ranging from 0.5% to 89% with a mean of 22% (Maillard et al. 2017)". Abstract not obtainable. | Title; S2 Discussion |
| S30 | Vasques GM, Grunwald S, Myers DB (2012) Influence of the spatial extent and resolution of input data on soil carbon models in Florida, USA. *JGR Biogeosciences* 117(G4) | 10.1029/2012JG001982 | **AB** (OpenAlex) | Mixed (Florida) | not in abstract | Nested extents 5.58 km², 3585 km², 150 000 km² | Soil C **model R²** (not variance) | "The quality of soil C models increased with an increase in the spatial extent (R2 from 0.10 in the cattle station to 0.61 in Florida)". This is indirect: a larger extent contains more systematic, covariate-explained variation. | Abstract |
| S31 | VandenBygaart AJ, Bremer E, McConkey BG, et al. (2011) Impact of sampling depth on differences in soil carbon stocks in long-term agroecosystem experiments. *SSSAJ* 75:226–234 | 10.2136/sssaj2010.0099 | **AB** (OpenAlex) | LTAE research plots, Canada | to 60 cm | Replicate plots | **Stock** difference | "In most cases, four cores would be suitable for detecting a significant difference in SOC stock of 5 Mg ha −1 at 95% confidence for LMCs in western Canada." | Abstract |

Sources found but not counted as evidence (abstract seen, no relevant variance content): Smith P (2004) *Global Change Biol* 10:1878–1883, doi 10.1111/j.1365-2486.2004.00854.x (time-to-detection modelling only); Berhongaray & Alvarez (2026) *Environ Monit Assess* 198:936, doi 10.1007/s10661-026-15794-0 (paired regional resampling, no variance numbers in abstract).

---

## 2. Synthesis: can the direction of the change in sigma_B (stock) from research plots to commercial support be bounded?

### 2.1 Verdict for STOCK variance

**Direction: yes, it can be bounded.** sigma_B between commercial sample locations will be **larger** than the 3.1 % (0–30 cm) between-plot CV, whether the locations are spread over a field, over many fields, or over a region.

**Strength of evidence: moderate.** Theory and every empirical source found point the same way. However:

- No study directly compares replicate research-plot variance with commercial point-support variance at the same location.
- Most cropland numbers are cross-study comparisons that differ in depth, land use and support.
- Several key MRV papers could only be read as abstracts.

**Two independent mechanisms push in the same direction.**

1. **Support effect: commercial samples are smaller than 0.02 ha plot means.**
   - The research-plot sigma_B is a variance between means of 0.02 ha plots. Each plot mean averages over a 53 m-long strip.
   - Commercial MRV locations are single cores or small composites.
   - The variance between plot means removes most short-range variance. This includes the nugget (micro-scale variation plus lab error) and any structure with a range shorter than about the plot length.
   - Evidence that this short-range component is large in SOC:
     - S23 (AB): ">50% of sample variance was spatially dependent at a scale of 5–60 m" in a 48 ha cultivated field.
     - S4 (FT): ">50 %" of SOC stock variance lies within 1 ha plots.
     - S2 (FT): within-site SD 41 % vs between-site SD 44 % of the mean, with microplots within about 42 m of each other.
     - S10 (AB): "Spatial dependence… weak", meaning variance is mostly nugget at field scale.
   - S16 (AB) shows the same thing inside research experiments: the "variance between replicate experimental units" was only "2%–42%, averaging 17%" of random error. A plot-mean sigma_B therefore omits most of the random variance a single core carries.
   - S20 (AB) and S21 (AB, crop yield) confirm that larger supports reduce variance.
   - Indirect reasoning (my inference): the 3.6 m x 53 m plot shape spans much of the 5–60 m range in S23, so each plot mean averages over most of the short-range structure.

2. **Extent effect: commercial locations span tens to hundreds of ha, and projects span regions.**
   - Theory [my statement; textbook not accessed, see §5]. Under an intrinsic-stationarity model, the dispersion variance of support v within domain V is D²(v|V) = γ̄(V,V) − γ̄(v,v). For nested domains v ⊂ V′ ⊂ V, D²(v|V) = D²(v|V′) + D²(V′|V) ("Krige's relation"), and D²(V′|V) ≥ 0. So variance cannot decrease as extent grows, and it falls as support grows. This is an expectation over realisations; a single real site can depart from it, for example a research site on unusually heterogeneous ground.
   - Empirical:
     - S5 (AB): "the coefficient of variation of the SOC stock increased across scales (from 5 to 35%)" in southern Belgian agriculture.
     - S8 (AB): across 117 cropland CVs, CV is significantly linearly related to log(sampling area). The sign is implied, not stated.
     - S6 (AB): required sample numbers rise from 34 (county) to 224 (state) to 501 (national) for US grassland. This is consistent with variance rising with extent, but the abstract does not give the CVs.
     - S29 (TI and CIT): the title asserts "Increased uncertainty… with spatial scale" for grasslands.
     - S2 (FT, forest): national between-site variance comes on top of within-site variance [my calculation: total point-level CV ≈ √(41² + 44²) ≈ 60 %, i.e. about 2.15 times the within-site variance].

### 2.2 Magnitude for STOCK (ranges, with sources)

All ratios below are **[my calculation]** against the 3.1 % (0–30 cm, plot-mean) input. Variance ratio = (SD ratio)².

| Commercial support / extent | Evidence | CV or SD reported | Ratio vs 3.1 % | Confidence |
|---|---|---|---|---|
| Single cores within one 1–2 ha cropland site, 0–30 cm stock | S1 (FT), Table 2 | 5 %, 10 %, 14 % (3 sites) | SD 1.6–4.5x; variance 2.6–20x | Moderate. Only 3 sites. Sites are 1–2 ha, smaller than commercial fields, so by S5, S8 and the identity above this is likely a **lower bound** for fields of tens to hundreds of ha |
| Same, grassland | S1 (FT) | 8 %, 17 %, 11 % | SD 2.6–5.5x | Moderate |
| Region or nation, cropland, 0–30 cm stock, composite of 25 cores in 20 x 20 m | S3 (FT) vs S1 (FT) | National SD 1.85 kg m−2 vs within-site SD 0.47–0.85 kg m−2 | National SD is 2.2–3.9x the within-site SD (variance 4.7–15x), **on top of** the within-site step | Low. Cross-study, different support (S3 composites reduce variance), no cropland median in S3 text |
| Agricultural landscape units up to region, southern Belgium | S5 (AB) | CV "from 5 to 35%" | Up to about 11x SD | Low to moderate. Abstract only; scale definitions unseen |
| National forest network, 0–15 cm mineral | S2 (FT) | Within-site 41 %, between-site 44 % | Not comparable to cropland plots (forest) | Shows the size of the between-location component at national extent: comparable to the within-site component |

**Bottom line for stock:**

- **Within a commercial field** (cores or small composites), sigma_B is most plausibly **about 1.5–5x** the research-plot value as an SD (**about 2–20x as a variance**). This means roughly 5–15 % CV at 0–30 cm in cropland.
- **For locations spread across many fields or a region**, a further between-field or between-region component is added. The only figures I could reach suggest CVs of order 20–35 %+, i.e. **about 5–10x** the 3.1 % SD. This is low confidence.
- Against the 11.5 % (0–15 cm) cross-site figure, the within-field increase is **not** established. S1's 0–10 cm cropland CVs are 21 %, 9 % and 12 %. Only the between-field or regional extent effect would still push it up.

**What could make the commercial value smaller.** Only design choices, not the soil:

- Large aggregate supports (S20) or many cores per composite.
- Stratification on good covariates (S14, S8).

Even then, composites spread across fields cannot remove the between-field component.

**Caveats the auditors should check:**

- Whether the 3.1 % is a residual CV after removing block effects. If it is, it excludes even the block-to-block component of within-site extent.
- How many cores make up each plot value.
- Whether 3.1 % is from one site at the low end of the research-plot range. S15 [my back-calculation] implies residual between-plot CVs of roughly 2–16 % at 0–10 cm across 13 Midwest sites.

**What study would tighten the magnitude.** A nested survey around a research site, with:

- Cores within 0.02 ha cells.
- Cells within fields, including the research plots themselves.
- Fields within farms, and farms within the region.
- The same depth (0–30 cm, equivalent soil mass), the same lab, and REML variance components at each level.
- A fitted point-support variogram, so dispersion variances can be computed for any support and extent (S20's regularisation approach).

---

## 3. Variance of stock CHANGE (separate question)

**Verdict: the direction cannot be bounded from the available evidence.** The literature explicitly warns that spatial variance of status is a poor proxy for variance of change:

- S17 (AB): "the status and change of an indicator are different variables and so their variability may differ… information on the variability of the change in soil is not in general available".
- S9 (AB): "spatial variance is a poor proxy for temporal variance".

What the evidence does show:

1. **Change is not a scaled copy of stock. The two sources disagree in sign.**
   - **Commercial cropland, 80 fields, 0–15 cm %C, about 1 yr interval (S9, AB):**
     - Between-field SD of level: 0.59 %C. Between-field SD of change: 0.08 %C. That is **more than 7x smaller as an SD** [my calculation: about 54x as a variance].
     - MDD from remeasurement was 0.056 %C, against 0.33 %C from spatial data.
     - "within-field variability remained high". No number is given in the abstract.
   - **National forest network, 0–15 cm mineral, about 10 yr interval (S2, FT):**
     - Between-site SD of change was 18.5 Mg ha−1 10 yr−1, about equal to the between-site SD of stock (19.0 Mg ha−1).
     - Within-site SD of change was 31.5 Mg ha−1 10 yr−1. That is larger than the within-site stock SD (17.3 Mg ha−1), and larger than the √2 x 17.3 ≈ 24.5 expected if the two visits were independent [my calculation; my reading is that extra temporal, relocation or method noise is present].
     - The authors also report regression to the mean, and a first-interval change that was not reproduced in the second interval.
   - So the extent dependence of change variance runs opposite ways in two available datasets. They differ in land use, interval, relocation offset (2 m) and units.
2. **At commercial support, change variance is dominated by within-location remeasurement noise, and that noise depends on support.**
   - S10 (AB): resampling one profile after a minimal shift gave a mean absolute error of 5.1 Mg C ha−1 (7.5 %) in cropland and 7.6 Mg C ha−1 (8.5 %) in grassland at 0–30 cm. This halved with 3 x 3 profiles.
   - S16 (AB): month-to-month variance was 15–32 % of random error. This was "often greater than" the between-replicate-unit variance in research experiments.
   - S2 (FT), Eq. 6 (citing de Gruijter et al. 2006, eq. 15.20; **CIT**): Var(change) = v1/n1 + v0/n0 − 2ρ√(v1/n1 · v0/n0). So change variance depends on the correlation ρ between paired observations, which depends on relocation precision and support.
   - S18 (AB): pairing helps only "if the observations are positively cross-correlated".
   - S7 (AB) and S19 (AB): resampling the same microplot or microsite enables detection of "much more modest changes" (S7) and recovered 91–106 % of added C (S19). Spatial (unpaired) comparisons failed beyond 35 cm.
3. **Inside research plots, temporal change is less variable than spatial between-plot differences.** S15 (AB), 0–10 cm: MDD for change over time was 3–13 %, against 6–31 % for a two-treatment comparison.

**Implication for G9.**

- If the audit applies a **stock** CV (3.1 %) to a **change** power calculation, the bias could go either way:
  - Paired, well-relocated designs over short intervals can have between-location change variance well below the stock variance (S9).
  - Long-interval networks with destructive, offset resampling can have change variance at or above stock variance (S2).
- For change variance itself, research plots vs commercial support:
  - The **support** argument favours **larger** at commercial support. Single cores or few-core composites per location carry more remeasurement noise than a multi-core 0.02 ha plot mean (S10, S2, S16).
  - The **extent** argument is weak. Between-field variance of change may be small (S9) or not (S2).
  - No study measured both on comparable terms, so I would not state a magnitude.

**What study would settle it.** A paired-remeasurement nested design in one region, with:

- Replicate research plots, surrounding commercial fields, and multiple farms.
- The same georeferenced points revisited (RTK GPS), the same lab, equivalent soil mass, and at least two remeasurement intervals (to separate true change heterogeneity from regression to the mean).
- Explicit duplicate cores at about 0–2 m offsets to estimate relocation and nugget error.
- Analysis by REML variance components of **change** at each level (cores, cells, plots/fields, farms, region), plus a cross-variogram between times 1 and 2.

The point-scale field data in S9, and the model framework in S13 (whose parameter values I could not read), are the closest existing pieces.

---

## 4. Access-wall log

Every host below refused the connection through this session's egress proxy, or served a bot challenge, on two attempts or after a confirmed refusal. Nothing behind these walls was treated as evidence for or against anything.

| Host | Failure | Items affected (full text not read) |
|---|---|---|
| www.sciencedirect.com | Proxy CONNECT 403; WebFetch ENOTFOUND | Conant & Paustian 2002; Stanley 2023; Bradford 2023; Potash 2022; Polussa 2026; de Gruijter et al. 2016 (10.1016/j.geoderma.2015.11.010); Maillard 2017; Heim et al. 2009 (10.1016/j.geoderma.2008.12.018); Chappell & Viscarra Rossel 2013 (10.1016/j.geoderma.2012.09.011); von Haden et al. 2024 (10.1016/j.geoderma.2024.116959); Xiong et al. 2016 (10.1016/j.still.2016.03.001); Lin et al. 2005 (10.1016/j.ecolmodel.2004.04.006); Goidts & van Wesemael 2007 (10.1016/j.geoderma.2007.06.013) |
| onlinelibrary.wiley.com | Proxy CONNECT 403 | Goidts 2009; Poeplau 2022; Lark 2009; Lark 2012; Papritz & Webster 1995; Saby 2008; Smith 2004; Vasques 2012 (JGR) |
| acsess.onlinelibrary.wiley.com | HTTP 403 Cloudflare challenge ("cf-mitigated: challenge") | Kravchenko & Robertson 2011; Ellert 2002; Cambardella 1994; Wuest & Durfee 2024; VandenBygaart 2011; Garten & Wullschleger 1999 |
| link.springer.com | JavaScript "Client Challenge" page | Vasques, Grunwald & Myers 2012 *Landscape Ecology* (10.1007/s10980-011-9702-3); McBratney & Pringle 1999 (10.1023/A:1009995404447); Skøien & Blöschl 2006 |
| iopscience.iop.org | Proxy 403 | Potash et al. 2025 (ERL) |
| www.jswconline.org; corn.agronomy.wisc.edu; dr.lib.iastate.edu | Proxy 403 | Necpálová et al. 2014 |
| eprints.qut.edu.au | Proxy 403; WebFetch ENOTFOUND | Conant & Paustian 2002 (repository PDF) |
| escholarship.org; arxiv.org; papers.ssrn.com | Proxy 403 | Stanley et al. 2023 (preprint and repository copies) |
| www.cabidigitallibrary.org / agrirxiv | Proxy 403 | Bradford et al. 2023 preprint; Polussa et al. 2026 preprint |
| datadryad.org; zenodo.org | Proxy 403 | Bradford et al. 2023 dataset (doi:10.5061/dryad.z08kprrjp, as listed in a search result) |
| www.openagrar.de | Proxy 403 | Poeplau et al. 2022 repository copy |
| www.zora.uzh.ch | Proxy 403 | Heim et al. 2009 green OA copy |
| brendo1001.github.io | Proxy 403 | Copy of de Gruijter et al. 2016 (per a search result) |
| www.cambridge.org | Proxy 403 | Fairfield Smith 1938 |
| www.publish.csiro.au; connectsci.au | Proxy 403 | Allen et al. 2010; "A pragmatic approach for national scale resampling" (*Soil Research*, SR25099) |
| www.mdpi.com | HTTP 403 (Akamai) | Not needed in the end |
| research.dial.uclouvain.be; scisoc.confex.com; orbi.uliege.be | Proxy 403 | Goidts thesis and conference abstract |
| poga.ca; static1.squarespace.com | Proxy 403 | Prairie Soil Carbon Balance project reports (McConkey), the main microsite-resampling change dataset |
| par.nsf.gov; projects.sare.org | Proxy 403 | Accepted-manuscript copies (unidentified, NSF PAR 10481180); von Haden et al. 2024 copy |
| api.openalex.org `/works?search=` | HTTP 429 ("Anonymous search is temporarily rate-limited") | Worked around with single-DOI lookups and Crossref and Semantic Scholar search |
| Elsevier abstracts in OpenAlex and Semantic Scholar | Abstract field "elided by the publisher" | Conant & Paustian 2002 (recovered via PubMed); de Gruijter 2016, Maillard 2017, Chappell 2013, Heim 2009, von Haden 2024 (not recovered) |

---

## 5. Unverified leads

None of the items below are used as evidence. Each needs checking against the source text.

1. **Dispersion variance and Krige's relation.** Textbook sources include Webster & Oliver, *Geostatistics for Environmental Scientists*, and Journel & Huijbregts. The identity in §2.1 is stated from the mathematics; the textbook pages were not accessed.
2. **Fairfield Smith's law applied to soil**, and the link between de Wijs/power variograms and "variance increases with the extent of the region" (Whittle 1956; McBratney & Pringle 1999). Not accessed. A search result paraphrased an unidentified review as saying that reducing plot size "by six orders of magnitude would only halve the variance". Source not identified.
3. **Vasques, Grunwald & Myers (2012) *Landscape Ecology*** (doi 10.1007/s10980-011-9702-3; volume and pages not verified). A search snippet quoted the paper as saying the study areas reflect "a progressively increasing variability of TC from the field to the state extent". I saw this only as a search snippet; the page range is unverified.
4. **Chappell & Viscarra Rossel (2013) *Geoderma*** (10.1016/j.geoderma.2012.09.011). A search snippet attributes this to the paper: "Within-field variance is poorly estimated by sampling within a support (here called a plot), which is a small proportion of the field." This is directly on point for G9 but unverified.
5. **Heim et al. (2009) *Geoderma*** (Lägeren, Swiss forest). A search summary says switching from unpaired to paired sampling improved the detection limit "by roughly a factor of four". Unverified.
6. **von Haden et al. (2024) *Geoderma* 116959**, a comment on Bradford 2023. A search summary says random sampling at both time points produced "relatively high dispersion in apparent SOC change", and that paired temporal sampling would improve single-field estimates. Unverified.
7. **Bradford et al. (2023)**: the within-field CVs of the 45 fields and the field locations. A search summary said the fields were mostly in Kansas, with some in Iowa and Nebraska. Unverified.
8. **Wuest & Durfee (2024)**: a search snippet says commercial-field CVs over 3 yr "ranged from 5% to 44%, with a mean of 16%". Unverified.
9. **Nakajima et al. (2025)**, *Agrosystems, Geosciences & Environment*, doi 10.1002/agg2.70025. A search snippet gives smallholder SOC stock CV 6.9–21.2 % and says "larger scales typically have higher variability". Unverified.
10. **Goidts et al. (2009)**: the definition of each "scale" and the land-use ordering. The English and French abstracts conflict on which land use is more variable.
11. **de Gruijter et al. (2016) "Farm-scale soil carbon auditing"** and **de Gruijter et al. (2006) *Sampling for Natural Resource Monitoring*** (eq. 15.20 for the variance of paired change). The latter is seen cited in S2.
12. **Maillard et al. (2017)**: the CV vs scale relationship. Only the title and S2's citation (0.5–89 %, mean 22 %) were seen.
13. **Potash et al. (2025)**: the fitted within-field and between-field variance-of-change parameters. Not seen.
14. **Prairie Soil Carbon Balance project** (Ellert, McConkey et al.): microsite resampling standard deviation of change on Saskatchewan farms. Reports blocked.
15. **"VandenBygaart & Allen"**, as named in the brief. No paper by these two authors was found. The closest items are VandenBygaart et al. 2011 (S31) and VandenBygaart 2006 *Can J Soil Sci* (10.4141/S05-106), the latter not read.
16. **Xiong et al. (2016)**, "Scale-dependent variability of SOC coupled to land use and land cover" (*Soil Till Res*); **Lin et al. (2005)**, "Assessment of soil spatial variability at multiple scales" (*Ecol Model*); **Corstanje, Schulin & Lark (2007)** *Eur J Soil Sci* 58:1087 (nested SOC at 0.2 m to 15 m and above, abstract seen but it gives no variance components). These are nested multi-scale designs that may hold variance components. Not read.
17. **Bellamy et al. (2005)** and **Lark, Bellamy & Kirk (2006)**: regression to the mean in national SOC change, England and Wales. Cited in S2; not read.
