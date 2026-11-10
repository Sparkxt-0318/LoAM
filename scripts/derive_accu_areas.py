#!/usr/bin/env python3
"""WP1a: derive area and credited rate for every credit-issued ACCU soil
project, from the register and the mapping files behind it.

    python scripts/fetch_cer_register.py --cea   # first, to populate raw/
    python scripts/derive_accu_areas.py

Needs the ``registry`` extra (pyshp, pyproj, shapely). Writes
``data/registry/accu_derived.json`` (committed; it is small and is the input
WP2 reads).

WHAT THE REGISTER DOES AND DOES NOT CARRY (resolving the contradiction
between docs/registry_corpus.md and docs/phase5_inverted_audit_results.md)
--------------------------------------------------------------------------
* There is NO numeric area field. "Project Area(s)" is a list of cadastral
  lot/plan identifiers, not hectares.
* "Project Mapping File URL" (a KML of the project-area boundary) is filled
  for every soil project.
* "Carbon Estimation Area mapping file URL" (a zipped shapefile of the
  carbon estimation areas, CEAs - the land the credits are actually computed
  over) is filled only for credit-issued projects.
So area is DERIVABLE from geometry for every project, and the credited area
(CEA) for every credit-issued project; it is never PUBLISHED as a number.
Every area below is therefore `inferred` (our computation from a stated
file), never `stated`.

AREA COMPUTATION
----------------
Geodesic area on the GRS80 ellipsoid (pyproj.Geod, Karney's algorithm), the
ellipsoid of GDA2020, which is the CRS every CEA .prj declares. Polygons are
re-oriented (exterior counter-clockwise, holes clockwise) before the area is
taken, so holes are subtracted. KML coordinates are WGS84 lon/lat; the
GDA2020/WGS84 difference is metre-level and immaterial to area.

RATE (D-064)
------------
* ``delta_net_mg_c_ha = ACCUs / 3.667 / CEA_ha`` - the cumulative NET credited
  stock change between the baseline sampling round and the latest one. The
  remeasurement interval does not enter it (years cancel). This is what the
  audit tests.
* ``tau_lower_mg_c_ha_y = delta_net / T_upper``, with ``T_upper`` the time
  from the crediting-period start date to 30 June of the latest financial
  year in which any ACCU was issued. Issuance follows the end of the
  reporting period, so ``T_upper`` is an UPPER bound on the time the credits
  cover and ``tau_lower`` a LOWER bound on the credited rate. Reported for
  comparison with literature rates; not used by the audit.
"""

from __future__ import annotations

import csv
import datetime as dt
import glob
import io
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

import shapefile
from pyproj import Geod
from shapely.geometry import MultiPolygon, Polygon, shape
from shapely.geometry.polygon import orient

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(REPO_ROOT, "data", "registry", "raw", "cer")
REGISTER = os.path.join(RAW, "accu_project_register.csv")
MANIFEST = os.path.join(REPO_ROOT, "data", "registry", "cer_manifest.json")
OUT = os.path.join(REPO_ROOT, "data", "registry", "accu_derived.json")

TCO2E_PER_MG_C = 44.0 / 12.0  # 3.667, as loam.inverted_audit.TCO2E_TO_MG_C
GEOD = Geod(ellps="GRS80")

FY_COL = re.compile(r"^(K|NK)ACCUs Units Issued in Financial Year (\d{4})/(\d{2})$")


def geodesic_area_ha(geom) -> float:
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
    total = 0.0
    for p in polys:
        p = orient(p, sign=1.0)
        a, _ = GEOD.geometry_area_perimeter(p)
        total += abs(a)
    return total / 1.0e4


def cea_geometry(zip_path: str):
    zf = zipfile.ZipFile(zip_path)
    shp = [n for n in zf.namelist() if n.lower().endswith(".shp")]
    if len(shp) != 1:
        raise ValueError(f"{zip_path}: expected one .shp, found {shp}")
    base = shp[0][:-4]
    prj = next((zf.read(n).decode(errors="replace") for n in zf.namelist() if n.lower().endswith(".prj")), "")
    r = shapefile.Reader(
        shp=io.BytesIO(zf.read(base + ".shp")),
        dbf=io.BytesIO(zf.read(base + ".dbf")),
        shx=io.BytesIO(zf.read(base + ".shx")),
    )
    geoms = [shape(s.__geo_interface__) for s in r.shapes()]
    polys: list[Polygon] = []
    for g in geoms:
        polys.extend(list(g.geoms) if isinstance(g, MultiPolygon) else [g])
    return MultiPolygon(polys), prj, len(geoms), r.shapeTypeName


def kml_geometry(kml_path: str):
    tree = ET.parse(kml_path)
    ns = {"k": "http://www.opengis.net/kml/2.2"}

    def ring(el):
        txt = el.find(".//k:coordinates", ns).text.strip()
        pts = [tuple(map(float, c.split(",")[:2])) for c in txt.split()]
        return pts

    polys = []
    for pg in tree.getroot().iter("{http://www.opengis.net/kml/2.2}Polygon"):
        outer = ring(pg.find("k:outerBoundaryIs", ns))
        inners = [ring(ib) for ib in pg.findall("k:innerBoundaryIs", ns)]
        polys.append(Polygon(outer, inners))
    return MultiPolygon(polys)


def parse_date(s: str) -> dt.date | None:
    s = (s or "").strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def num(s: str) -> float:
    s = (s or "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return 0.0


def main() -> int:
    with open(REGISTER, "rb") as fh:
        rows = list(csv.DictReader(io.StringIO(fh.read().decode("utf-8-sig"))))
    with open(MANIFEST, encoding="utf-8") as fh:
        manifest = json.load(fh)
    reg_rec = next(f for f in manifest["files"] if f["url"] and f["url"].endswith("accu-scheme-project-register-0"))

    out: dict = {
        "note": (
            "Derived by scripts/derive_accu_areas.py from the ACCU register and the CER "
            "mapping files. Every area here is INFERRED (our geodesic computation from a "
            "stated boundary file) - the register publishes no numeric area. See D-064."
        ),
        "register": {k: reg_rec.get(k) for k in ("url", "sha256", "last_modified", "accessed")},
        "projects": {},
    }
    targets = [r for r in rows if "Soil" in r["Method"] and "Measurement" in r["Method"] and num(r["ACCUs Total units issued"]) > 0]
    for r in targets:
        pid = r["Project ID"].strip()
        rec: dict = {
            "project_name": r["Project Name"].strip(),
            "proponent": r["Project Proponent"].strip(),
            "method": r["Method"].strip(),
            "activities": r["Project activities"].strip(),
            "state": r["Project location"].strip(),
            "postcode": r["Project location (postcode)"].strip(),
            # the register writes "n/a" for a blank field; that is not a disclosure
            "approach_field": (r["Estimation or measurement approach or model"].strip()
                               if r["Estimation or measurement approach or model"].strip().lower() not in ("", "n/a") else None),
            "crediting_start": None, "crediting_end": None,
            "permanence_period": r["Nominated Permanence Period, if applicable"].strip(),
            "revoked": r["Project revoked"].strip(),
            "accus_total": num(r["ACCUs Total units issued"]),
            "cea_url": r["Carbon Estimation Area mapping file URL"].strip(),
            "project_kml_url": r["Project Mapping File URL"].strip(),
            "notes_excerpt": (r["Notes"] or "").strip()[:300] or None,
        }
        cs, ce = parse_date(r["Crediting period start date"]), parse_date(r["Crediting period end date"])
        rec["crediting_start"] = cs.isoformat() if cs else None
        rec["crediting_end"] = ce.isoformat() if ce else None

        fy: dict[str, float] = {}
        for col, val in r.items():
            m = FY_COL.match(col)
            if m and num(val) > 0:
                key = f"{m.group(2)}/{m.group(3)}"
                fy[key] = fy.get(key, 0.0) + num(val)
        rec["issuance_by_fy"] = dict(sorted(fy.items()))
        if fy:
            last_fy_start = int(max(fy).split("/")[0])
            first_fy_start = int(min(fy).split("/")[0])
            rec["first_issuance_fy"] = min(fy)
            rec["last_issuance_fy"] = max(fy)
            fy_end = dt.date(last_fy_start + 1, 6, 30)
            rec["t_upper_years"] = round((fy_end - cs).days / 365.25, 3) if cs else None
            rec["n_issuance_fys"] = len(fy)
            assert abs(sum(fy.values()) - rec["accus_total"]) < 1.0, (pid, sum(fy.values()), rec["accus_total"])
            del first_fy_start

        cea_zip = os.path.join(RAW, "cea", pid + ".zip")
        kml = os.path.join(RAW, "kml", pid + ".kml")
        if os.path.exists(cea_zip):
            g, prj, n_shapes, stype = cea_geometry(cea_zip)
            rec["cea_area_ha"] = round(geodesic_area_ha(g), 2)
            rec["cea_n_polygons"] = len(g.geoms)
            rec["cea_crs"] = prj.split('"')[1] if '"' in prj else prj[:40]
            c = g.centroid
            rec["cea_centroid_lon_lat"] = [round(c.x, 4), round(c.y, 4)]
        if os.path.exists(kml):
            pg = kml_geometry(kml)
            rec["project_area_ha"] = round(geodesic_area_ha(pg), 2)
            if "cea_area_ha" in rec and rec["project_area_ha"] > 0:
                rec["cea_over_project_area"] = round(rec["cea_area_ha"] / rec["project_area_ha"], 4)
                # CEA is meant to lie inside the project area; check rather than assume.
                inter = g.buffer(0).intersection(pg.buffer(0))
                rec["cea_fraction_inside_project_area"] = round(geodesic_area_ha(inter) / rec["cea_area_ha"], 4) if not inter.is_empty else 0.0

        if rec.get("cea_area_ha"):
            d = rec["accus_total"] / TCO2E_PER_MG_C / rec["cea_area_ha"]
            rec["delta_net_mg_c_ha"] = round(d, 4)
            if rec.get("t_upper_years"):
                rec["tau_lower_mg_c_ha_y"] = round(d / rec["t_upper_years"], 4)
        out["projects"][pid] = rec

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(f"wrote {OUT}: {len(out['projects'])} projects")
    return 0


if __name__ == "__main__":
    sys.exit(main())
