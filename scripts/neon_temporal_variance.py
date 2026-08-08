#!/usr/bin/env python3
"""EXPLORATORY: derive month-to-month SOC variance from NEON DP1.10086.

Standalone. Not part of the package build, not imported by ``loam``, not wired
into ``build_table``. Stdlib only, so it adds no dependency to the project.

WHY
---
Component 4 (temporal variance) rests on a single published source (Wuest 2024)
that is paywalled, depth-unconfirmed, and from Pacific Northwest dryland
cropping. Deriving a month-to-month variance ourselves from open data is a
stronger contribution than citing one number, and it converts a blocked row into
a partially constrained one.

KNOWN LIMITATION - READ BEFORE USING THE OUTPUT
-----------------------------------------------
**NEON is predominantly NON-CROPLAND.** It is an ecological observatory; most
sites are forest, grassland, shrubland or tundra. Only a handful of agricultural
sites exist - KONA, STER, DELA, LENO - so n is small, and those four do not span
temperate cropland in any representative way.

This therefore **SUPPLEMENTS Wuest (2024). It does not replace it.** It cannot
close gap G4 on its own, and it does not settle the open scope question in
DECISIONS.md D-021.

Further caveats that survive any amount of data:

* NEON's periodic soil sampling is not designed for temporal variance. Bouts are
  a few per year, not monthly, so "month-to-month" here means *between-bout
  within a year*, which is a coarser and less demanding quantity than Wuest's.
* Apparent temporal variance confounds real change, relocation within the plot
  (NEON randomises core locations within a plot rather than revisiting a point),
  and processing differences between bouts. The relocation share is NOT
  separable here and is probably large - see VC-REL-004.
* Depth intervals vary by bout and site; this script filters to samples lying
  within 0-30 cm but the support is not constant.

DO NOT add a variance_table row from this output without resolving the above and
logging a D-NNN entry. Output goes to a scratch file under data/processed/,
which is gitignored.

USAGE
-----
    python scripts/neon_temporal_variance.py
    python scripts/neon_temporal_variance.py --sites KONA STER --out /tmp/x.json

A NEON API token is optional and only raises rate limits; set NEON_TOKEN to use
one. If the data endpoint returns 403 the script says so and exits non-zero
rather than reporting an empty result as though it were a finding.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import statistics
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from typing import Any

API = "https://data.neonscience.org/api/v0"
PRODUCT = "DP1.10086.001"

#: The only NEON sites with a genuinely agricultural land use. Small n is the
#: point of the caveat in the module docstring, not an oversight.
AG_SITES = ("KONA", "STER", "DELA", "LENO")

#: NEON renames fields between data-product revisions, so resolve by trying
#: candidates rather than hard-coding one and failing opaquely years later.
CARBON_FIELDS = ("organicCPercent", "organiccPercent", "carbonPercent", "socPercent")
PLOT_FIELDS = ("plotID", "namedLocation")
DATE_FIELDS = ("collectDate", "startDate")
TOP_DEPTH_FIELDS = ("sampleTopDepth", "biomassSampleTopDepth")
BOTTOM_DEPTH_FIELDS = ("sampleBottomDepth", "biomassSampleBottomDepth")

MAX_DEPTH_CM = 30.0


class NeonAccessError(RuntimeError):
    """The NEON data endpoint refused us. Distinct from 'no data matched'."""


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


def _request(url: str) -> Any:
    headers = {"User-Agent": "loam-osse/0.1 (soil-carbon OSSE testbed; research)"}
    token = os.environ.get("NEON_TOKEN")
    if token:
        headers["X-API-Token"] = token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            raise NeonAccessError(
                f"HTTP 403 from {url}\n"
                "NEON's /data/ endpoint denied this request. The /products/ and "
                "/sites/ endpoints are reachable, so this is NEON-side access "
                "control (their WAF blocks some cloud egress ranges), not a "
                "network fault.\n"
                "Try: run from a workstation, or set NEON_TOKEN=<token> from "
                "https://data.neonscience.org/myaccount"
            ) from exc
        if exc.code == 404:
            return None
        raise


def _fetch_csv(url: str) -> list[dict[str, str]]:
    headers = {"User-Agent": "loam-osse/0.1 (soil-carbon OSSE testbed; research)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=180) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(text)))


# ---------------------------------------------------------------------------
# discovery
# ---------------------------------------------------------------------------


def available_months(sites: tuple[str, ...]) -> dict[str, list[str]]:
    doc = _request(f"{API}/products/{PRODUCT}")
    out: dict[str, list[str]] = {}
    for entry in doc["data"]["siteCodes"]:
        if entry["siteCode"] in sites:
            out[entry["siteCode"]] = sorted(entry["availableMonths"])
    return out


def feasibility(sites: tuple[str, ...]) -> dict[str, Any]:
    """How much temporal signal is even available, using metadata only.

    Runs off ``/products/``, which is reachable even where ``/data/`` is not, so
    the viability of the derivation can be assessed without the observations.
    A site-year with only one sampling bout contributes nothing to a
    month-to-month variance, so this bounds n from above.
    """
    per_site: dict[str, Any] = {}
    total_multi = 0
    for site, months in sorted(available_months(sites).items()):
        years: dict[str, list[str]] = defaultdict(list)
        for m in months:
            years[m[:4]].append(m[5:7])
        multi = {y: sorted(ms) for y, ms in years.items() if len(ms) >= 2}
        total_multi += len(multi)
        per_site[site] = {
            "site_months": len(months),
            "years_spanned": len(years),
            "years_with_2plus_bouts": len(multi),
            "bouts_per_multi_year": {y: len(ms) for y, ms in sorted(multi.items())},
        }
    return {
        "mode": "feasibility_only",
        "per_site": per_site,
        "total_site_years_with_2plus_bouts": total_multi,
        "interpretation": (
            f"{total_multi} site-years across {len(per_site)} agricultural sites "
            "have >=2 sampling bouts and could contribute to a between-bout "
            "variance. This is an UPPER BOUND at site level; the usable n rises "
            "once split by plot but falls again wherever a plot lacks two bouts "
            "in the same year with usable carbon values. Note NEON bouts are a "
            "few per year, so this is between-bout variance, not the true "
            "month-to-month quantity Wuest reports."
        ),
    }


def chemistry_urls(site: str, month: str) -> list[str]:
    doc = _request(f"{API}/data/{PRODUCT}/{site}/{month}")
    if doc is None:
        return []
    return [
        f["url"]
        for f in doc["data"]["files"]
        if "soilChemistry" in f["name"] and f["name"].endswith(".csv")
        and "basic" in f["name"]
    ]


def _first_present(row: dict[str, str], candidates: tuple[str, ...]) -> str | None:
    for c in candidates:
        if c in row:
            return c
    return None


# ---------------------------------------------------------------------------
# analysis
# ---------------------------------------------------------------------------


def collect(sites: tuple[str, ...], max_depth_cm: float, verbose: bool = True):
    """Return observations as (site, plot, year, month, soc_pct)."""
    obs: list[tuple[str, str, int, int, float]] = []
    skipped = defaultdict(int)
    months = available_months(sites)

    for site, site_months in sorted(months.items()):
        if verbose:
            print(f"  {site}: {len(site_months)} site-months available", file=sys.stderr)
        for month in site_months:
            for url in chemistry_urls(site, month):
                try:
                    rows = _fetch_csv(url)
                except urllib.error.HTTPError as exc:
                    skipped[f"http_{exc.code}"] += 1
                    continue
                if not rows:
                    continue

                cfield = _first_present(rows[0], CARBON_FIELDS)
                pfield = _first_present(rows[0], PLOT_FIELDS)
                dfield = _first_present(rows[0], DATE_FIELDS)
                if not (cfield and pfield and dfield):
                    skipped["missing_columns"] += 1
                    if verbose:
                        print(
                            f"    {site} {month}: expected columns absent; saw "
                            f"{sorted(rows[0])[:12]}...",
                            file=sys.stderr,
                        )
                    continue
                tfield = _first_present(rows[0], TOP_DEPTH_FIELDS)
                bfield = _first_present(rows[0], BOTTOM_DEPTH_FIELDS)

                for r in rows:
                    raw = (r.get(cfield) or "").strip()
                    if not raw:
                        skipped["no_carbon_value"] += 1
                        continue
                    try:
                        soc = float(raw)
                    except ValueError:
                        skipped["unparseable_carbon"] += 1
                        continue
                    if not 0.0 < soc < 60.0:
                        skipped["implausible_carbon"] += 1
                        continue

                    if bfield and (r.get(bfield) or "").strip():
                        try:
                            if float(r[bfield]) > max_depth_cm:
                                skipped["below_depth_cutoff"] += 1
                                continue
                        except ValueError:
                            pass
                    if tfield and (r.get(tfield) or "").strip():
                        try:
                            if float(r[tfield]) < 0:
                                continue
                        except ValueError:
                            pass

                    date = (r.get(dfield) or "").strip()
                    if len(date) < 7:
                        skipped["no_date"] += 1
                        continue
                    obs.append((site, r[pfield], int(date[:4]), int(date[5:7]), soc))

    return obs, dict(skipped)


def decompose(obs) -> dict[str, Any]:
    """Split variation into between-month and within-month (replicate) parts.

    Mirrors the decomposition Wuest reports, so the two are comparable: temporal
    variance is expressed as a SHARE of temporal + replicate, not as an absolute.
    """
    by_plot_month: dict[tuple, list[float]] = defaultdict(list)
    for site, plot, year, month, soc in obs:
        by_plot_month[(site, plot, year, month)].append(soc)

    # replicate variance: cores within one plot-month
    replicate_vars = [
        statistics.variance(v) for v in by_plot_month.values() if len(v) >= 2
    ]

    # temporal variance: month means within one plot-year, >= 2 distinct months
    by_plot_year: dict[tuple, dict[int, float]] = defaultdict(dict)
    for (site, plot, year, month), vals in by_plot_month.items():
        by_plot_year[(site, plot, year)][month] = statistics.fmean(vals)

    temporal_vars, temporal_cvs, usable = [], [], []
    for key, monthly in by_plot_year.items():
        if len(monthly) < 2:
            continue
        vals = list(monthly.values())
        mean = statistics.fmean(vals)
        var = statistics.variance(vals)
        temporal_vars.append(var)
        if mean > 0:
            temporal_cvs.append(100.0 * (var**0.5) / mean)
        usable.append(
            {
                "site": key[0], "plot": key[1], "year": key[2],
                "n_months": len(monthly), "months": sorted(monthly),
                "mean_soc_pct": round(mean, 4), "sd_soc_pct": round(var**0.5, 4),
                "cv_pct": round(100.0 * (var**0.5) / mean, 2) if mean > 0 else None,
            }
        )

    mean_temporal = statistics.fmean(temporal_vars) if temporal_vars else None
    mean_replicate = statistics.fmean(replicate_vars) if replicate_vars else None
    share = None
    if mean_temporal is not None and mean_replicate is not None:
        total = mean_temporal + mean_replicate
        if total > 0:
            share = round(100.0 * mean_temporal / total, 1)

    return {
        "n_observations": len(obs),
        "n_plot_years_usable": len(usable),
        "n_plot_months": len(by_plot_month),
        "mean_temporal_variance": mean_temporal,
        "mean_replicate_variance": mean_replicate,
        "temporal_share_of_random_error_pct": share,
        "median_temporal_cv_pct": (
            round(statistics.median(temporal_cvs), 2) if temporal_cvs else None
        ),
        "temporal_cv_range_pct": (
            [round(min(temporal_cvs), 2), round(max(temporal_cvs), 2)]
            if temporal_cvs else None
        ),
        "plot_years": sorted(usable, key=lambda d: (d["site"], d["plot"], d["year"])),
        "comparison_to_wuest_2024": (
            "Wuest reports month-to-month variance as 15-32% of random error "
            "(mean 20%). The share above is the closest analogue computed here. "
            "It is NOT a like-for-like comparison: NEON bouts are not monthly, "
            "and NEON randomises core position within a plot, so the temporal "
            "term here also absorbs relocation variance."
        ),
    }


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sites", nargs="+", default=list(AG_SITES))
    ap.add_argument("--max-depth-cm", type=float, default=MAX_DEPTH_CM)
    ap.add_argument(
        "--out",
        default="data/processed/neon_temporal_variance.json",
        help="scratch output (data/processed/ is gitignored)",
    )
    args = ap.parse_args()

    print(f"NEON {PRODUCT}, sites: {', '.join(args.sites)}", file=sys.stderr)
    try:
        obs, skipped = collect(tuple(args.sites), args.max_depth_cm)
    except NeonAccessError as exc:
        print(f"\nBLOCKED: {exc}\n", file=sys.stderr)
        # The observations are unreachable, but /products/ is not - so still
        # report whether the derivation is worth attempting elsewhere.
        report = feasibility(tuple(args.sites))
        report["blocked"] = str(exc)
        out = os.path.abspath(args.out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
        print("Feasibility (metadata only):", file=sys.stderr)
        for site, s in report["per_site"].items():
            print(
                f"  {site}: {s['site_months']} site-months, "
                f"{s['years_with_2plus_bouts']} years with >=2 bouts",
                file=sys.stderr,
            )
        print(
            f"  total site-years with >=2 bouts: "
            f"{report['total_site_years_with_2plus_bouts']}",
            file=sys.stderr,
        )
        print(f"wrote {out}", file=sys.stderr)
        return 2

    if not obs:
        print(
            "\nNo usable observations. This is NOT a finding of zero variance - "
            f"it means nothing matched. Skip reasons: {skipped}",
            file=sys.stderr,
        )
        return 3

    result = decompose(obs)
    result["_provenance"] = {
        "product": PRODUCT,
        "sites": args.sites,
        "max_depth_cm": args.max_depth_cm,
        "skipped": skipped,
        "caveat": (
            "EXPLORATORY. NEON is predominantly non-cropland; n is small. "
            "Supplements Wuest 2024, does not replace it. Do not add a "
            "variance_table row from this without logging a D-NNN entry."
        ),
    }

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    print(f"\nobservations: {result['n_observations']}", file=sys.stderr)
    print(f"usable plot-years: {result['n_plot_years_usable']}", file=sys.stderr)
    print(f"median temporal CV: {result['median_temporal_cv_pct']}%", file=sys.stderr)
    print(
        f"temporal share of random error: "
        f"{result['temporal_share_of_random_error_pct']}%  "
        f"(Wuest: 15-32%, mean 20%)",
        file=sys.stderr,
    )
    print(f"wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
