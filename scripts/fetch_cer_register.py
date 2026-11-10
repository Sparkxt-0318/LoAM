#!/usr/bin/env python3
"""WP1a: fetch the ACCU project register and the mapping files behind it.

    python scripts/fetch_cer_register.py            # register CSV only
    python scripts/fetch_cer_register.py --cea      # + CEA zips and project KMLs
                                                    #   for every credit-issued
                                                    #   soil project

Writes into ``data/registry/raw/cer/`` (git-ignored: third-party files,
reproducible from this script) and a committed manifest,
``data/registry/cer_manifest.json``, recording for every file the URL, the
HTTP status, the byte count, the sha256 and the access timestamp - so a reader
can tell whether the file they re-download is the one this analysis used.

Politeness: sequential, one request at a time, a fixed pause between
requests, an identifying User-Agent, and only paths that cer.gov.au's
robots.txt does not disallow (``/document/...`` and
``/sites/default/files/projectFiles/...``; checked 2026-11-10).

Two-attempts rule: each file is tried at most twice; a second failure is
recorded in the manifest as a wall and the script moves on.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import sys
import time
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(REPO_ROOT, "data", "registry", "raw", "cer")
MANIFEST = os.path.join(REPO_ROOT, "data", "registry", "cer_manifest.json")
REGISTER_URL = "https://cer.gov.au/document/accu-scheme-project-register-0"
REGISTER_FILE = "accu_project_register.csv"
UA = "LoAM-research/0.1 (soil carbon detectability testbed; sequential, rate-limited)"
PAUSE_S = 2.0

#: The census definition behind D-056's 999: the two measurement-based soil
#: methods (2018 and 2021 determinations). Reproduced exactly from the
#: 2026-10-20 register (999). The 2014 grazing-systems method (30 projects,
#: none issued) is reported separately, never folded in.
def is_measurement_soil_method(method: str) -> bool:
    return "Soil" in method and "Measurement" in method


def _get(url: str, dest: str) -> dict:
    rec: dict = {"url": url, "file": os.path.relpath(dest, REPO_ROOT)}
    for attempt in (1, 2):
        rec["attempts"] = attempt
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = resp.read()
                rec["http_status"] = resp.status
                rec["last_modified"] = resp.headers.get("Last-Modified")
            with open(dest, "wb") as fh:
                fh.write(body)
            rec["bytes"] = len(body)
            rec["sha256"] = hashlib.sha256(body).hexdigest()
            rec["accessed"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
            rec["outcome"] = "ok"
            return rec
        except Exception as exc:  # noqa: BLE001 - logged, not swallowed
            rec["outcome"] = f"FAILED: {type(exc).__name__}: {exc}"
            time.sleep(PAUSE_S * 2)
    rec["outcome"] = "WALL (two attempts): " + rec["outcome"]
    return rec


def load_register(path: str) -> list[dict]:
    with open(path, "rb") as fh:
        txt = fh.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(txt)))


def accus(row: dict) -> float:
    s = (row.get("ACCUs Total units issued") or "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cea", action="store_true", help="also fetch CEA zips + project KMLs for issued soil projects")
    ap.add_argument("--reuse-register", action="store_true", help="do not re-download the register if present")
    args = ap.parse_args()
    os.makedirs(os.path.join(RAW, "cea"), exist_ok=True)
    os.makedirs(os.path.join(RAW, "kml"), exist_ok=True)

    manifest = {"note": "written by scripts/fetch_cer_register.py; raw files are git-ignored", "files": []}
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = json.load(fh)
    by_url = {f["url"]: f for f in manifest["files"]}

    reg_path = os.path.join(RAW, REGISTER_FILE)
    if not (args.reuse_register and os.path.exists(reg_path)):
        by_url[REGISTER_URL] = _get(REGISTER_URL, reg_path)
        print(f"register: {by_url[REGISTER_URL]['outcome']}")
    rows = load_register(reg_path)

    if args.cea:
        targets = [
            r for r in rows
            if is_measurement_soil_method(r["Method"]) and accus(r) > 0
        ]
        print(f"{len(targets)} credit-issued measurement-method soil projects")
        for r in targets:
            pid = r["Project ID"].strip()
            for col, sub, ext in (
                ("Carbon Estimation Area mapping file URL", "cea", ".zip"),
                ("Project Mapping File URL", "kml", ".kml"),
            ):
                url = r[col].strip()
                if not url or url.lower() == "n/a":
                    by_url[f"missing:{pid}:{sub}"] = {"url": None, "project_id": pid, "outcome": f"no {col} in register"}
                    continue
                dest = os.path.join(RAW, sub, pid + ext)
                if url in by_url and by_url[url].get("outcome") == "ok" and os.path.exists(dest):
                    continue
                rec = _get(url, dest)
                rec["project_id"] = pid
                rec["kind"] = sub
                by_url[url] = rec
                print(f"  {pid} {sub}: {rec['outcome']} {rec.get('bytes', '')}")
                time.sleep(PAUSE_S)

    manifest["files"] = sorted(by_url.values(), key=lambda f: (f.get("project_id") or "", f.get("kind") or "", f.get("url") or ""))
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
