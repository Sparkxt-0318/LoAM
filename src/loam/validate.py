"""Validation of the curated variance-component rows against the schema.

Kept separate from :mod:`loam.schema` (which only declares) and from
:mod:`loam.build_table` (which only emits), so the rules can be exercised by
tests without touching the filesystem.
"""

from __future__ import annotations

from typing import Any

from .schema import COLUMNS, COLUMNS_BY_NAME, COLUMN_NAMES, RULES


class ValidationError(Exception):
    """Raised when the curated table violates the schema."""


def _blank(v: Any) -> bool:
    return v is None or (isinstance(v, str) and not v.strip())


def _coerce_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.strip().lower() in {"true", "false", "yes", "no", "1", "0"}:
        return v.strip().lower() in {"true", "yes", "1"}
    raise ValueError(f"not a boolean: {v!r}")


def validate_row(row: dict[str, Any], index: int) -> list[str]:
    """Return a list of human-readable problems with a single row."""
    rid = row.get("row_id") or f"<row {index}>"
    problems: list[str] = []

    unknown = set(row) - set(COLUMN_NAMES)
    if unknown:
        problems.append(f"{rid}: unknown column(s) {sorted(unknown)}")

    for col in COLUMNS:
        value = row.get(col.name)

        if col.required and _blank(value):
            problems.append(f"{rid}: required column '{col.name}' is empty")
            continue
        if _blank(value):
            continue

        if col.enum is not None and value not in col.enum:
            problems.append(
                f"{rid}: '{col.name}' = {value!r} is not one of {list(col.enum)}"
            )

        if col.dtype == "float":
            try:
                float(value)
            except (TypeError, ValueError):
                problems.append(f"{rid}: '{col.name}' = {value!r} is not numeric")
        elif col.dtype == "int":
            if not isinstance(value, int) or isinstance(value, bool):
                problems.append(f"{rid}: '{col.name}' = {value!r} is not an integer")
        elif col.dtype == "bool":
            try:
                _coerce_bool(value)
            except ValueError:
                problems.append(f"{rid}: '{col.name}' = {value!r} is not a boolean")

    for rule in RULES:
        try:
            if rule.failed(row):
                problems.append(f"{rid}: violates {rule.rule_id} - {rule.description}")
        except (TypeError, ValueError) as exc:  # malformed value already reported
            problems.append(f"{rid}: could not evaluate {rule.rule_id} ({exc})")

    return problems


def validate_rows(rows: list[dict[str, Any]]) -> list[str]:
    """Return every problem across the whole table, including duplicate ids."""
    problems: list[str] = []

    seen: dict[str, int] = {}
    for i, row in enumerate(rows):
        rid = row.get("row_id")
        if rid:
            if rid in seen:
                problems.append(
                    f"{rid}: duplicate row_id (also at position {seen[rid]})"
                )
            else:
                seen[rid] = i
        problems.extend(validate_row(row, i))

    return problems


def assert_valid(rows: list[dict[str, Any]]) -> None:
    problems = validate_rows(rows)
    if problems:
        raise ValidationError(
            f"{len(problems)} schema violation(s):\n  - "
            + "\n  - ".join(problems)
        )


def coverage_by_component(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Rows per component, split by whether they can actually drive the OSSE.

    A component with zero in-scope baseline rows is an evidence gap, however many
    out-of-scope rows sit beside it. This is the number to report, not the total.
    """
    from .schema import COMPONENTS

    out: dict[str, dict[str, int]] = {}
    for comp in COMPONENTS:
        subset = [r for r in rows if r.get("component") == comp]
        out[comp] = {
            "total": len(subset),
            "baseline": sum(1 for r in subset if r.get("use_as") == "baseline"),
            "in_scope": sum(1 for r in subset if _coerce_bool(r.get("in_scope", False))),
            "verified_fulltext": sum(
                1 for r in subset if r.get("verification") == "verified_fulltext"
            ),
            "derived": sum(
                1 for r in subset if r.get("verification") == "derived_primary_data"
            ),
            "unverified": sum(
                1 for r in subset if r.get("verification") == "unverified"
            ),
        }
    return out
