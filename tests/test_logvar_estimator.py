"""The log-variance estimator, and the guard against the specification it replaced.

D-058 retired an unweighted OLS on ``log(sd)`` restricted to n>=3, after it
returned t = -0.37, +4.58, -4.53, +0.75 on the same coefficient across four
nested samples of one dataset. These tests do two jobs:

* check that the replacement is arithmetically what it claims to be — the
  closed forms are exact, so this is testable to machine precision rather than
  to a tolerance; and
* **fail if the retired specification is reintroduced**, which is the part that
  matters in six months when nobody remembers why.
"""

from __future__ import annotations

import math
import random
import re

import pytest

from loam import build_table, logvar

# ---------------------------------------------------------------------------
# the closed forms are exact — test them as such
# ---------------------------------------------------------------------------

#: Independently known values. psi(1) = -gamma; psi(1/2) = -gamma - 2 ln 2;
#: psi'(1) = pi^2/6; psi'(1/2) = pi^2/2. The recurrences build everything else.
_KNOWN_DIGAMMA = {
    1: -logvar.EULER_GAMMA - 2 * math.log(2),          # psi(1/2)
    2: -logvar.EULER_GAMMA,                            # psi(1)
    3: -logvar.EULER_GAMMA - 2 * math.log(2) + 2.0,    # psi(3/2)
    4: -logvar.EULER_GAMMA + 1.0,                      # psi(2)
}
_KNOWN_TRIGAMMA = {
    1: math.pi ** 2 / 2,                               # psi'(1/2)
    2: math.pi ** 2 / 6,                               # psi'(1)
    3: math.pi ** 2 / 2 - 4.0,                         # psi'(3/2)
    4: math.pi ** 2 / 6 - 1.0,                         # psi'(2)
}


@pytest.mark.parametrize("two_x,expected", sorted(_KNOWN_DIGAMMA.items()))
def test_digamma_matches_known_values(two_x, expected):
    assert logvar.digamma_half_integer(two_x) == pytest.approx(expected, abs=1e-14)


@pytest.mark.parametrize("two_x,expected", sorted(_KNOWN_TRIGAMMA.items()))
def test_trigamma_matches_known_values(two_x, expected):
    assert logvar.trigamma_half_integer(two_x) == pytest.approx(expected, abs=1e-14)


def test_digamma_satisfies_its_recurrence():
    """psi(x+1) = psi(x) + 1/x. If the recurrence holds at every step the whole
    ladder is right, independently of the anchors."""
    for two_x in range(1, 60):
        lhs = logvar.digamma_half_integer(two_x + 2)
        rhs = logvar.digamma_half_integer(two_x) + 1.0 / (two_x / 2.0)
        assert lhs == pytest.approx(rhs, abs=1e-12), f"recurrence fails at {two_x}/2"


def test_trigamma_satisfies_its_recurrence():
    """psi'(x+1) = psi'(x) - 1/x^2."""
    for two_x in range(1, 60):
        lhs = logvar.trigamma_half_integer(two_x + 2)
        rhs = logvar.trigamma_half_integer(two_x) - 1.0 / (two_x / 2.0) ** 2
        assert lhs == pytest.approx(rhs, abs=1e-12), f"recurrence fails at {two_x}/2"


def test_nonpositive_arguments_raise():
    for bad in (0, -1, -7):
        with pytest.raises(ValueError):
            logvar.digamma_half_integer(bad)
        with pytest.raises(ValueError):
            logvar.trigamma_half_integer(bad)
    for bad in (0, -3):
        with pytest.raises(ValueError):
            logvar.log_variance_bias(bad)


# ---------------------------------------------------------------------------
# the properties the estimator exists for
# ---------------------------------------------------------------------------


def test_the_bias_is_large_at_one_degree_of_freedom_and_shrinks():
    """This is the whole reason D-040's specification failed. At nu = 1 the
    downward bias in log-variance is about -1.27, a factor of 3.6, and it decays
    towards zero. A specification that ignores it fits the replicate count."""
    b1 = logvar.log_variance_bias(1)
    assert b1 == pytest.approx(-1.2704, abs=1e-3)
    assert math.exp(b1) == pytest.approx(1 / 3.56, rel=0.02)

    biases = [logvar.log_variance_bias(nu) for nu in range(1, 40)]
    assert all(b < 0 for b in biases), "the bias must be downward at every nu"
    assert all(a < b for a, b in zip(biases, biases[1:])), "the bias must shrink with nu"
    assert abs(biases[-1]) < 0.03


def test_weights_rise_with_degrees_of_freedom():
    """A 2-replicate treatment must count for less than a 6-replicate one. The
    retired specification either dropped it or counted it equally; both are
    wrong, and in opposite directions."""
    w = [logvar.weight(nu) for nu in range(1, 20)]
    assert all(a < b for a, b in zip(w, w[1:]))
    assert logvar.weight(1) < 0.25 * logvar.weight(5)


def test_debias_is_unbiased_under_simulation():
    """Seeded Monte Carlo against chi-square draws. Deterministic, no scipy."""
    rng = random.Random(20260812)

    def chi2(nu: int) -> float:
        # sum of nu squared standard normals
        return sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))

    for nu, draws in ((1, 40_000), (3, 20_000), (7, 12_000)):
        vals = [logvar.debias(math.log(chi2(nu) / nu), nu) for _ in range(draws)]
        mean = sum(vals) / len(vals)
        se = math.sqrt(logvar.log_variance_variance(nu) / len(vals))
        assert abs(mean) < 4 * se, (
            f"nu={nu}: debiased mean {mean:.4f} is more than 4 SE ({se:.4f}) from 0"
        )


def test_prepare_drops_unusable_groups_and_reports_which():
    s2 = [0.04, 0.0, None, 0.09, -1.0, float("nan"), 0.01]
    n = [3, 4, 5, 2, 6, 4, 1]          # last one has only one replicate
    y, w, kept = logvar.prepare(s2, n)
    assert kept == [0, 3], "only the positive-variance, >=2-replicate groups survive"
    assert len(y) == len(w) == 2
    assert y[0] == pytest.approx(math.log(0.04) - logvar.log_variance_bias(2))
    assert w[1] == pytest.approx(logvar.weight(1))


def test_prepare_keeps_two_replicate_groups():
    """The retired specification dropped them. Keeping them at their true
    information content is half the fix — dropping them is what let the sign
    move when the filter changed."""
    _, w, kept = logvar.prepare([0.02, 0.02], [2, 5])
    assert kept == [0, 1]
    assert w[0] < w[1]


# ---------------------------------------------------------------------------
# the guard: the retired specification must not come back
# ---------------------------------------------------------------------------

#: The retired idiom: taking a log of a standard deviation (or of sqrt of a
#: variance) to use as a regression response. Narrow on purpose — this guards
#: against reintroduction of one specific construction, not against logs in
#: general.
_RETIRED_IDIOM = re.compile(
    r"log\s*\(\s*(np\.)?(sqrt\s*\(|.*?\bsd\b|.*?\bstd\s*\()", re.IGNORECASE
)

#: Files permitted to contain it, with the reason. `ic_conditioning.py` and
#: `sensitivity_g1.py` each compute the retired specification DELIBERATELY and
#: report it beside the repaired one, so the instability that motivated D-058
#: stays inspectable. Both label it `RETIRED`.
_ALLOWED = {
    "ic_conditioning.py": "computes the D-040 spec for explicit comparison (D-055)",
    "sensitivity_g1.py": "reports the retired spec beside the repaired one (D-058)",
}


def _script_sources():
    for path in sorted((build_table.REPO_ROOT / "scripts").glob("*.py")):
        yield path, path.read_text(encoding="utf-8")


def test_the_retired_log_sd_specification_is_not_reintroduced():
    offenders = []
    for path, src in _script_sources():
        if path.name in _ALLOWED:
            continue
        for lineno, line in enumerate(src.splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            if _RETIRED_IDIOM.search(line):
                offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not offenders, (
        "the log-of-a-standard-deviation specification retired by D-058 has "
        "reappeared:\n  - " + "\n  - ".join(offenders)
        + "\n\nUse loam.logvar.prepare() instead: it debiases with "
        "psi(nu/2) - log(nu/2) and weights by 1/psi'(nu/2), so treatments with "
        "different replicate counts are comparable. If this is a deliberate "
        "reproduction for comparison, add the file to _ALLOWED with a reason - "
        "do not widen the pattern."
    )


def test_allowlisted_files_still_label_the_retired_specification():
    """An allowlist that nobody re-reads is a hole. Each permitted file must say
    the word RETIRED next to what it is doing, so a reader of the OUTPUT cannot
    mistake the comparison number for a result."""
    for name in _ALLOWED:
        src = (build_table.REPO_ROOT / "scripts" / name).read_text(encoding="utf-8")
        assert "RETIRED" in src or "retired" in src, (
            f"{name} is allowlisted as a deliberate reproduction of the retired "
            "specification, but does not label it as retired anywhere"
        )


def test_the_repaired_joint_model_uses_the_shared_estimator():
    """Behavioural, not textual: the repaired D-040 model must go through
    loam.logvar rather than re-deriving the correction inline."""
    src = (build_table.REPO_ROOT / "scripts" / "sensitivity_g1.py").read_text(
        encoding="utf-8"
    )
    assert "from loam import logvar" in src, (
        "sensitivity_g1.joint_covariate_model must import loam.logvar. The "
        "D-040 specification survived as long as it did because the arithmetic "
        "was six unnamed lines inside one function."
    )
    assert "logvar.prepare(" in src
