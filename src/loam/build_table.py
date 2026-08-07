"""Emit ``data/variance_table.csv`` from the curated YAML source.

The YAML is hand-edited; the CSV is a build artifact that happens to be
committed so that downstream tools (and reviewers) get a plain table without
needing to run anything. Never edit the CSV directly - it is overwritten.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

import yaml

from .schema import COLUMN_NAMES
from .validate import assert_valid, coverage_by_component

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_YAML = REPO_ROOT / "data" / "variance_components.yaml"
OUTPUT_CSV = REPO_ROOT / "data" / "variance_table.csv"


def load_rows(path: Path = SOURCE_YAML) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    if not isinstance(doc, dict) or "rows" not in doc:
        raise ValueError(f"{path} must contain a top-level 'rows:' list")
    rows = doc["rows"]
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{path} contains no rows")
    return rows


def _render(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        # YAML folded scalars leave trailing newlines; collapse to one line so
        # the CSV stays one-record-per-row.
        return " ".join(value.split())
    return str(value)


def write_csv(rows: list[dict[str, Any]], path: Path = OUTPUT_CSV) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=list(COLUMN_NAMES), quoting=csv.QUOTE_MINIMAL,
            extrasaction="raise",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _render(row.get(k)) for k in COLUMN_NAMES})


def main(argv: list[str] | None = None) -> int:
    rows = load_rows()
    assert_valid(rows)
    write_csv(rows)

    print(f"wrote {OUTPUT_CSV.relative_to(REPO_ROOT)}: "
          f"{len(rows)} rows x {len(COLUMN_NAMES)} columns")
    print("\ncoverage by component (baseline = usable in the OSSE today):")
    for comp, stats in coverage_by_component(rows).items():
        flag = "  <-- NO BASELINE" if stats["baseline"] == 0 else ""
        print(
            f"  {comp:<22} total={stats['total']:<3} baseline={stats['baseline']:<3} "
            f"in_scope={stats['in_scope']:<3} fulltext={stats['verified_fulltext']:<3} "
            f"unverified={stats['unverified']}{flag}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
