# data/registry/raw — downloaded registry files (not committed)

Everything in this folder except this README is git-ignored. Files here are
third-party documents; the committed record of what was used is the manifest
(`data/registry/cer_manifest.json`) and the per-field `source`/`locator` in the
corpus YAML files.

| folder | how it is populated |
|---|---|
| `cer/` | `python scripts/fetch_cer_register.py --cea` (ACCU register CSV, CEA zips, project KMLs) |
| `car/` | CAR1459 documents fetched by hand from the Reserve's public document list (see `projects.yaml` sources `car1459_*`) |
| `verra/` | **downloaded by hand by the PI** — see `docs/registry_population.md` §"Verra: hand-download list" for the exact project IDs and document names |
