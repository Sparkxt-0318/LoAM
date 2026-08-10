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

from .decisions import CONSTANTS, PROPOSED_FLAG, rows_exposed_to_open_decisions
from .schema import COLUMN_NAMES
from .validate import assert_valid, coverage_by_component

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_YAML = REPO_ROOT / "data" / "variance_components.yaml"
OUTPUT_CSV = REPO_ROOT / "data" / "variance_table.csv"

#: First line of the emitted CSV. Present so that anyone who opens the CSV to
#: edit it is told, in the file itself, that their edit will be overwritten.
GENERATED_BANNER = "# GENERATED - edit the YAML, not this file"


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
        fh.write(GENERATED_BANNER + "\r\n")
        writer = csv.DictWriter(
            fh, fieldnames=list(COLUMN_NAMES), quoting=csv.QUOTE_MINIMAL,
            extrasaction="raise",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _render(row.get(k)) for k in COLUMN_NAMES})


def read_csv(path: Path = OUTPUT_CSV) -> list[dict[str, str]]:
    """Read the emitted CSV, skipping the generated-file banner.

    Any consumer of variance_table.csv must go through something like this, or
    else drop banner lines itself - the first line is a comment, not the header.
    """
    with path.open(encoding="utf-8", newline="") as fh:
        body = (line for line in fh if not line.startswith("#"))
        return list(csv.DictReader(body))


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
            f"derived={stats['derived']:<3} unverified={stats['unverified']}{flag}"
        )

    print_decision_status(rows)
    return 0


def print_decision_status(rows: list[dict[str, Any]]) -> None:
    """Announce every constant resting on a decision nobody has made yet.

    Printed on every build, next to the NO BASELINE flags, for the same reason:
    an unratified value that drives a published number should have to be looked
    at, not remembered.
    """
    print("\ndecision status of the constants behind the derived rows:")
    for const in CONSTANTS:
        flag = PROPOSED_FLAG if const.is_proposed else ""
        print(
            f"  {const.name:<22} {const.governed_by}  {const.status:<8}"
            f"{flag}"
        )

    baselines = {r["row_id"] for r in rows if r.get("use_as") == "baseline"}
    exposed = {
        row_id: sorted(decisions)
        for row_id, decisions in rows_exposed_to_open_decisions(rows).items()
        if row_id in baselines
    }
    if exposed:
        print("\n  baseline rows resting on an open decision:")
        for row_id, decisions in sorted(exposed.items()):
            print(f"    {row_id:<20} {', '.join(decisions)}{PROPOSED_FLAG}")


if __name__ == "__main__":
    sys.exit(main())
