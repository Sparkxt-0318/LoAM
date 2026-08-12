"""Schema guard for the Phase 5 registry corpus.

The corpus exists to answer one question — could this project's sampling design
have detected what it claimed? — and that answer is only worth as much as the
provenance behind each number. The variance table earned its credibility by
making every row carry a source, a locator and an honest statement of what was
assumed; this file gets the same treatment before it grows, not after.

The load-bearing rule is the STATUS VOCABULARY, and in particular the
distinction between:

* ``not_disclosed`` - we looked and it is not in the public documents, and
* ``withheld`` - the public document NAMES a document that carries the
  parameter, and that document is not public.

Those are different findings about a registry, and a corpus that blurred them
would understate the sharper one. So the vocabulary is closed and a typo cannot
quietly invent a fifth category.
"""

from __future__ import annotations

import datetime as dt

import pytest
import yaml

from loam import build_table

#: Closed vocabulary. `withheld` is deliberately distinct from `not_disclosed`
#: - see the module docstring.
STATUSES = {"stated", "inferred", "not_disclosed", "withheld", "not_applicable"}

#: A field that is not `stated` must not carry a value, and a field that IS
#: stated must carry one. Otherwise a null can masquerade as a measurement.
MUST_HAVE_VALUE = {"stated"}
MUST_NOT_HAVE_VALUE = {"not_disclosed", "withheld", "not_applicable"}

CORPUS = build_table.REPO_ROOT / "data" / "registry" / "projects.yaml"


@pytest.fixture(scope="module")
def corpus() -> dict:
    with open(CORPUS, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _fields(project: dict):
    """(name, block) for every field written in the {value, status, ...} form."""
    for name, block in project.items():
        if isinstance(block, dict) and "status" in block:
            yield name, block


def test_corpus_parses_and_is_not_empty(corpus):
    assert corpus["projects"], "the corpus has no projects"
    assert corpus["sources"], "the corpus has no sources"


def test_every_project_has_an_id_and_a_registry(corpus):
    for p in corpus["projects"]:
        assert p.get("project_id"), f"project without an id: {p.get('project_name')}"
        assert p.get("registry"), f"{p['project_id']} does not name its registry"
        assert p.get("protocol"), f"{p['project_id']} does not name its protocol"


def test_project_ids_are_unique(corpus):
    ids = [p["project_id"] for p in corpus["projects"]]
    assert len(ids) == len(set(ids)), f"duplicate project ids: {ids}"


def test_every_field_declares_a_status_from_the_closed_vocabulary(corpus):
    bad = [
        f"{p['project_id']}.{name}: {block['status']!r}"
        for p in corpus["projects"]
        for name, block in _fields(p)
        if block["status"] not in STATUSES
    ]
    assert not bad, (
        "fields with a status outside the vocabulary:\n  - " + "\n  - ".join(bad)
        + f"\n\nAllowed: {sorted(STATUSES)}. Do not widen this set to fit a "
        "field - the distinction between `not_disclosed` and `withheld` is the "
        "finding, and a fifth category dilutes it."
    )


def test_every_field_carries_a_source_and_a_locator(corpus):
    """No number without provenance. The rule the variance table runs on."""
    bad = [
        f"{p['project_id']}.{name}"
        for p in corpus["projects"]
        for name, block in _fields(p)
        if not block.get("source") or not block.get("locator")
    ]
    assert not bad, (
        "fields missing a source or a locator:\n  - " + "\n  - ".join(bad)
    )


def test_every_source_reference_resolves(corpus):
    known = set(corpus["sources"])
    bad = [
        f"{p['project_id']}.{name} -> {block['source']!r}"
        for p in corpus["projects"]
        for name, block in _fields(p)
        if block["source"] not in known
    ]
    for block in corpus.get("registry_coverage", []):
        if block.get("source") not in known:
            bad.append(f"registry_coverage[{block.get('registry')}] -> {block.get('source')!r}")
    assert not bad, (
        "references to sources that are not in the `sources` block:\n  - "
        + "\n  - ".join(bad)
    )


def test_every_source_has_a_url_and_an_access_date(corpus):
    """An undated retrieval cannot be re-checked, and registries change."""
    bad = [
        f"{key}: missing {'url' if not src.get('url') else 'accessed'}"
        for key, src in corpus["sources"].items()
        if not src.get("url") or not src.get("accessed")
    ]
    assert not bad, "sources without a URL or an access date:\n  - " + "\n  - ".join(bad)

    for key, src in corpus["sources"].items():
        assert isinstance(src["accessed"], dt.date), (
            f"{key}: `accessed` must be a YAML date, got {src['accessed']!r}"
        )


def test_undisclosed_fields_carry_no_value(corpus):
    """A null is a null. It must never be dressed up as a measurement."""
    bad = [
        f"{p['project_id']}.{name} is {block['status']} but carries {block['value']!r}"
        for p in corpus["projects"]
        for name, block in _fields(p)
        if block["status"] in MUST_NOT_HAVE_VALUE and block.get("value") is not None
    ]
    assert not bad, "\n  - ".join(["fields asserting a value they do not have:"] + bad)


def test_stated_fields_carry_a_value(corpus):
    bad = [
        f"{p['project_id']}.{name}"
        for p in corpus["projects"]
        for name, block in _fields(p)
        if block["status"] in MUST_HAVE_VALUE and block.get("value") is None
    ]
    assert not bad, (
        "fields marked `stated` with no value - use `not_disclosed`:\n  - "
        + "\n  - ".join(bad)
    )


def test_inferred_fields_explain_the_inference(corpus):
    """An inference nobody can retrace is indistinguishable from a guess."""
    bad = [
        f"{p['project_id']}.{name}"
        for p in corpus["projects"]
        for name, block in _fields(p)
        if block["status"] == "inferred" and not block.get("note")
    ]
    assert not bad, (
        "`inferred` fields with no note explaining the derivation:\n  - "
        + "\n  - ".join(bad)
    )


def test_out_of_scope_projects_say_why(corpus):
    """Scope is locked (SOC, cropland topsoil, temperate). Out-of-scope entries
    are kept rather than deleted - the same rule D-016 applies to variance-table
    rows - but they must carry the reason with them."""
    bad = [
        p["project_id"]
        for p in corpus["projects"]
        if p.get("in_loam_scope") is False and not p.get("scope_note")
    ]
    assert not bad, f"out-of-scope projects with no scope_note: {bad}"


def test_in_scope_flag_is_explicit(corpus):
    bad = [p["project_id"] for p in corpus["projects"] if "in_loam_scope" not in p]
    assert not bad, (
        f"projects that do not declare `in_loam_scope`: {bad}. Scope is locked; "
        "silence is not a scope decision."
    )


def test_blocked_targets_record_their_attempt_count(corpus):
    """Two attempts max on an access blocker, then log and move on. The log is
    only useful if it says how hard we tried."""
    for entry in corpus.get("blocked_or_deferred", []):
        assert "attempts" in entry, f"{entry.get('target')!r} does not record attempts"
        assert entry.get("outcome"), f"{entry.get('target')!r} does not record an outcome"
        assert entry["attempts"] <= 2, (
            f"{entry['target']!r} records {entry['attempts']} attempts; the rule "
            "is two, then log and move on"
        )
