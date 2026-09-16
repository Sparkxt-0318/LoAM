# LoAM

An Observing System Simulation Experiment (OSSE) testbed for **soil organic
carbon monitoring**. Purely computational.

## The claim

We are **not predicting soil carbon**. We are quantifying **detectability**:
given a sampling design, can it resolve the SOC change it purports to measure?

This matters because minimum detectable change (MDC) depends on the **variance
structure** of the measurement process, not on the truth model's mean trajectory
being correct. That is what makes the testbed defensible despite using an
imperfect carbon model underneath.

Every design decision is required to preserve that property. Where a component
does depend on the mean, it is flagged explicitly — see `mean_dependent` in the
[schema](docs/variance_table_schema.md) and D-004 / D-007 in
[`DECISIONS.md`](DECISIONS.md).

## Scope — locked

- Soil organic carbon only (no N, no GHG fluxes)
- Cropland topsoil, 0–30 cm
- Temperate climate
- One or two management practices (cover crops, reduced tillage)

The scope lock is enforced **in data**, not in prose: rules R7 and R10 prevent
an out-of-scope row from becoming a baseline, and a test asserts that every
baseline row is cropland within 0–30 cm.

## Status

**Phase 0 — variance-component reference table.** Complete and under review.
The simulator is not written yet.

| # | component | rows | in-scope baseline |
|---|-----------|------|-------------------|
| 1 | analytical | 4 | ✅ |
| 2 | within-plot spatial | 4 | ✅ |
| 3 | between-plot spatial | 6 | ✅ NAPESHM, derived — 0–15 cm, upper bound |
| 4 | temporal | 2 | ❌ dryland only (G4) — the last gap |
| 5 | relocation | 6 | ✅ |
| 6 | depth / bulk density | 4 | ✅ |

26 rows, 14 verified against full text, 2 derived from primary data we hold,
2 locked out pending a PDF.
Open evidence gaps are tracked as **G1–G9** in [`DECISIONS.md`](DECISIONS.md);
**G1 and G4 are closed**.

**Phase 5 — the inverted audit — is now the headline deliverable** (Deliverable
3, a spatially explicit MDC surface, was retired: see
[`docs/invariance_finding.md`](docs/invariance_finding.md)). Instead of asking
whether a registered soil-carbon project's sampling design was adequate — a
question almost no registry discloses enough to answer, see
[`docs/registry_corpus.md`](docs/registry_corpus.md) — it asks what sampling
the project's own claim would have required to be detectable, using VM0042's
own optional Equation (2). First implementation and first-run results:
[`docs/phase5_inverted_audit_results.md`](docs/phase5_inverted_audit_results.md);
design: [`docs/phase5_inverted_audit_design.md`](docs/phase5_inverted_audit_design.md).

Every row also records `bias_direction` — whether its number is likely too large
or too small for our scope — because an inflated variance is conservative for a
sampling calculator but anti-conservative for the Phase 5 audit (D-023).

## Layout

```
data/
  variance_components.yaml   curated source of truth — edit this
  variance_table.csv         generated deliverable — never edit
  literature/                PDFs (gitignored; see literature/README.md)
  raw/  processed/           gitignored
  registry/projects.yaml     Phase 5 corpus: registered soil-carbon project sampling inputs
docs/
  variance_table_schema.md   schema reference
  sources.md                 bibliography and retrieval status
  phase5_inverted_audit_results.md  Phase 5 implementation + first-run numbers
src/loam/
  schema.py                  columns, vocabularies, integrity rules
  validate.py                rule evaluation
  build_table.py             YAML -> CSV
  logvar.py                  debiased log-variance estimator (D-058)
  student_t.py               pure-Python Student's t, used by inverted_audit
  inverted_audit.py          Phase 5: the inverted audit engine
scripts/                     derivations, outside the package build
  derive_g1_napeshm.py       between-plot baseline from NAPESHM (needs [derive])
  neon_temporal_variance.py  exploratory temporal probe (NEON /data/ is 403 here)
  run_inverted_audit.py      Phase 5: run the audit over the registry corpus
tests/
DECISIONS.md                 every harmonization assumption, appendable
```

## Setup

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -e ".[dev]"

# only to re-run the derivations under scripts/ (heavy; not needed for tests)
uv pip install --python .venv/bin/python -e ".[derive]"
```

## Use

```bash
python -m loam.build_table          # regenerate the CSV + print coverage by component
python scripts/run_inverted_audit.py  # Phase 5: run the audit over the registry corpus
pytest                               # schema, scope-lock and staleness guards
```

`build_table` prints which components have no usable baseline, so the gaps stay
visible on every run rather than needing to be looked up. `run_inverted_audit`
does the equivalent for Phase 5: it prints which corpus projects cannot be
audited at all, and why.
