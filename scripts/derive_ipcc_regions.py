#!/usr/bin/env python3
"""Classify the 94 NAPESHM sites into IPCC 2006 default climate regions.

Partial by decision, not by accident — see DECISIONS.md D-028 (decided) and
D-033. A site that reaches a test we cannot evaluate is returned as
``unclassified`` with the blocking variable named. Nothing is imputed.

WHAT THIS NEEDS THAT NAPESHM DOES NOT PUBLISH
---------------------------------------------
Frost days per year, for the ``MAT > 18 °C AND <= 7 days of frost/year`` test.
Recovered from **Daymet**, which is the source NAPESHM's own data dictionary
cites for every one of its climate columns, queried at each site's own published
coordinates. This is the same series reduced with a different operator
(threshold-and-count instead of mean), not a proxy.

That identity is checked rather than asserted: ``--verify`` reproduces the
published ``site_meanmin_temp`` / ``site_meanmax_temp`` / ``site_mean_temp``
integers from the fetched series, truncation convention included. It came back
60/60 exact across the 20 sites at MAT >= 18. A different pixel, window or
version would not do that — which is what licenses using the V4 R1 endpoint
against a dictionary citing doi:10.3334/ORNLDAAC/1328.

MAP:PET is NOT recovered, and must not be. There is no documented Hargreaves
formulation or averaging window in NAPESHM to reproduce, so any PET computed
here would be ours, not theirs, and the resulting label would say "IPCC" while
meaning something else. Sites needing it stay unclassified.

USAGE
-----
    python scripts/derive_ipcc_regions.py            # uses the cached frost data
    python scripts/derive_ipcc_regions.py --refetch  # re-query Daymet (~20 calls)
    python scripts/derive_ipcc_regions.py --verify   # re-run the reproduction check
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import statistics
import sys
import time
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from loam.ipcc_climate import (  # noqa: E402
    UNCLASSIFIED,
    classify_partial,
    is_temperate,
)

SITES = "data/raw/napeshm/sites.csv"
FROST_CACHE = "data/processed/ipcc_frost_days.json"
OUT = "data/processed/ipcc_site_regions.json"

DAYMET = "https://daymet.ornl.gov/single-pixel/api/data"
WINDOW = ("2010-01-01", "2019-12-31")  # matches NAPESHM's stated 2010-2019

#: Only sites this warm can reach the frost test; below it the tropical
#: conjunction is False on temperature alone (see loam.ipcc_climate).
FROST_NEEDED_ABOVE_MAT = 18.0


def load_sites() -> list[dict]:
    with open(SITES, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Daymet
# ---------------------------------------------------------------------------


def fetch_daymet(lat: str, lon: str) -> dict:
    url = (f"{DAYMET}?lat={lat}&lon={lon}&vars=tmax,tmin"
           f"&start={WINDOW[0]}&end={WINDOW[1]}")
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=180) as resp:
                text = resp.read().decode()
            break
        except Exception as exc:  # network flake; Daymet is occasionally slow
            last = exc
            time.sleep(4 * (attempt + 1))
    else:
        raise RuntimeError(f"Daymet failed for {lat},{lon}: {last}")

    rows = csv.reader(io.StringIO("year,yday," + text.split("year,yday,")[1]))
    header = next(rows)
    i_max = next(i for i, h in enumerate(header) if h.strip().startswith("tmax"))
    i_min = next(i for i, h in enumerate(header) if h.strip().startswith("tmin"))

    tmins, tmaxs, frost = [], [], Counter()
    years = set()
    for row in rows:
        if len(row) < 3:
            continue
        year, tmin, tmax = int(row[0]), float(row[i_min]), float(row[i_max])
        years.add(year)
        tmins.append(tmin)
        tmaxs.append(tmax)
        if tmin <= 0.0:
            frost[year] += 1
    return {
        "n_days": len(tmins),
        "n_years": len(years),
        "mean_tmin": statistics.mean(tmins),
        "mean_tmax": statistics.mean(tmaxs),
        "frost_days_per_year": sum(frost[y] for y in years) / len(years),
    }


def frost_days(sites: list[dict], refetch: bool) -> dict:
    """Frost days for every site that can reach the test. Cached in the repo."""
    if not refetch and os.path.exists(FROST_CACHE):
        with open(FROST_CACHE, encoding="utf-8") as fh:
            return json.load(fh)

    need = [s for s in sites
            if float(s["site_mean_temp"]) >= FROST_NEEDED_ABOVE_MAT]
    print(f"querying Daymet for {len(need)} sites at MAT >= {FROST_NEEDED_ABOVE_MAT:.0f} "
          f"(the rest cannot reach the frost test)")
    out = {}
    for site in need:
        out[site["sitecode"]] = fetch_daymet(site["site_latitude"],
                                             site["site_longitude"])
        time.sleep(1)
    os.makedirs(os.path.dirname(FROST_CACHE), exist_ok=True)
    with open(FROST_CACHE, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return out


def verify(sites: list[dict], frost: dict) -> tuple[int, int]:
    """Prove we are on NAPESHM's own pixel by reproducing its published integers."""
    by_code = {s["sitecode"]: s for s in sites}
    ok = total = 0
    print(f"\n{'site':9}{'tmin':>12}{'tmax':>12}{'tmean':>12}")
    for code, d in sorted(frost.items()):
        s = by_code[code]
        checks = [
            (math.floor(d["mean_tmin"]), float(s["site_meanmin_temp"])),
            (math.floor(d["mean_tmax"]), float(s["site_meanmax_temp"])),
            (math.floor((d["mean_tmin"] + d["mean_tmax"]) / 2),
             float(s["site_mean_temp"])),
        ]
        marks = "".join("." if a == b else "X" for a, b in checks)
        ok += sum(a == b for a, b in checks)
        total += len(checks)
        cells = "".join(f"{a:>6.0f}/{b:<5.0f}" for a, b in checks)
        print(f"{code:9}{cells}  {marks}")
    print(f"\nreproduction against published columns: {ok}/{total} exact")
    return ok, total


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refetch", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    sites = load_sites()
    frost = frost_days(sites, args.refetch)

    if args.verify:
        ok, total = verify(sites, frost)
        if ok != total:
            print("REPRODUCTION FAILED - do not trust the frost counts", file=sys.stderr)
            return 3

    results = []
    for s in sites:
        mat = float(s["site_mean_temp"])
        f = frost.get(s["sitecode"])
        region, blocked_by = classify_partial(
            mat,
            float(s["site_precip"]),
            elevation_m=float(s["site_elevation"]),
            frost_days_per_year=f["frost_days_per_year"] if f else None,
            map_pet_ratio=None,          # D-028: never invented
            monthly_mean_temps_c=None,   # unreachable: no site is <= 0 C
        )
        results.append({
            "sitecode": s["sitecode"], "country": s["country"],
            "mat_c": mat, "map_mm": float(s["site_precip"]),
            "elevation_m": float(s["site_elevation"]),
            "frost_days_per_year": round(f["frost_days_per_year"], 2) if f else None,
            "region": region, "blocked_by": blocked_by,
            "is_temperate": is_temperate(region) if region != UNCLASSIFIED else None,
            # A site within +/-0.5 C of a MAT cut point could flip on rounding
            # alone, because site_mean_temp is published as a whole number.
            "on_mat_threshold": mat in (0.0, 10.0, 18.0),
        })

    classified = [r for r in results if r["region"] != UNCLASSIFIED]
    unclassified = [r for r in results if r["region"] == UNCLASSIFIED]

    print(f"\n{'='*64}\nIPCC 2006 partial classification (D-028 decided)\n{'='*64}")
    print(f"  classified   : {len(classified):>3} / {len(results)}")
    print(f"  unclassified : {len(unclassified):>3} / {len(results)}")
    print("\n  by region:")
    for region, n in Counter(r["region"] for r in classified).most_common():
        print(f"    {region:<22} {n:>3}")
    print("\n  unclassified, by blocking variable:")
    for var, n in Counter(r["blocked_by"] for r in unclassified).most_common():
        print(f"    {var:<22} {n:>3}")
    print(f"\n  IPCC-temperate sites: {sum(1 for r in classified if r['is_temperate'])}")
    flip = [r for r in results if r["on_mat_threshold"]]
    print(f"  sites sitting exactly on a MAT cut point (could flip on rounding): "
          f"{len(flip)}")

    payload = {
        "scheme": "IPCC 2006 Vol 4 Ch 3, Figure 3A.5.2, p. 3.39",
        "decision": "D-028 (decided): partial classification; unclassified is "
                    "explicit and never imputed",
        "frost_days_source": (
            "Daymet single-pixel API at each site's published coordinates, "
            f"{WINDOW[0]}..{WINDOW[1]}; the source NAPESHM's dictionary cites "
            "for its own climate columns"),
        "map_pet": "NOT recovered - no documented Hargreaves formulation or "
                   "averaging window in NAPESHM (D-028, D-033)",
        "n_sites": len(results),
        "n_classified": len(classified),
        "n_unclassified": len(unclassified),
        "by_region": dict(Counter(r["region"] for r in classified)),
        "sites": results,
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
