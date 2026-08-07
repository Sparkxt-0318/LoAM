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
| 3 | between-plot spatial | 4 | ❌ forest only (G1) |
| 4 | temporal | 2 | ❌ dryland only (G4) |
| 5 | relocation | 6 | ✅ |
| 6 | depth / bulk density | 4 | ✅ |

24 rows, 14 verified against full text, 2 locked out pending a PDF.
Open evidence gaps are tracked as **G1–G7** in [`DECISIONS.md`](DECISIONS.md).

## Layout

```
data/
  variance_components.yaml   curated source of truth — edit this
  variance_table.csv         generated deliverable — never edit
  literature/                PDFs (gitignored; see literature/README.md)
  raw/  processed/           gitignored
docs/
  variance_table_schema.md   schema reference
  sources.md                 bibliography and retrieval status
src/loam/
  schema.py                  columns, vocabularies, integrity rules
  validate.py                rule evaluation
  build_table.py             YAML -> CSV
tests/
DECISIONS.md                 every harmonization assumption, appendable
```

## Setup

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -e ".[dev]"
```

## Use

```bash
python -m loam.build_table   # regenerate the CSV + print coverage by component
pytest                       # schema, scope-lock and staleness guards
```

`build_table` prints which components have no usable baseline, so the gaps stay
visible on every run rather than needing to be looked up.
