# data/literature/

PDFs of cited sources. **Gitignored** — third-party copyrighted material is
never committed. The shareable record of what we read is
[`docs/sources.md`](../../docs/sources.md).

## Naming

`<firstauthor><year>_<short_slug>.pdf` — e.g. `poeplau2022_plot_scale_variability.pdf`

## Currently held

- `poeplau2022_plot_scale_variability.pdf` — accepted manuscript, retrieved
  openly from the German National Library (`d-nb.info/125318657X/34`)

## Wanted

See the priority table at the end of [`docs/sources.md`](../../docs/sources.md).
Short version — these are paywalled or otherwise unreachable from here:

1. Buchkowski et al. 2026, *Global Change Biology* — `10.1111/gcb.70868`
2. Wuest 2024, *SSSAJ* — `10.1002/saj2.20660`
3. LUCAS 2015 Topsoil Survey report — `10.2760/616084`
4. Saby et al. 2008, *Global Change Biology* — `10.1111/j.1365-2486.2008.01658.x`

## After adding a PDF

1. Verify the value against the source and update `verification` in
   `data/variance_components.yaml` (`unverified` → `verified_fulltext`, etc.).
2. Record the exact `locator` — table, figure or section.
3. Log any new harmonization assumption in `DECISIONS.md`.
4. `python -m loam.build_table && pytest`

If a value turns out to differ from what we recorded, fix the row **and** add a
superseding `D-NNN` entry. Do not silently overwrite.
