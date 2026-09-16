"""Verification for the pure-Python Student's t implementation.

Two independent checks, because ``loam.inverted_audit`` trusts this module for
every ``n_req`` it computes:

1. against standard published critical-value tables, at a spread of degrees
   of freedom including nu=1 (heaviest tail, hardest case for the continued
   fraction) and the large-nu limit (must reproduce the normal z-values);
2. against the red team's own worked demonstration in
   ``docs/inverted_audit_redteam.md`` (C-3) — the sharpest check available,
   because reproducing those four numbers exactly is what licenses using
   bisection over the fixed-point iteration the design doc originally (and
   wrongly) prescribed.
"""

from __future__ import annotations

import math

import pytest

from loam.student_t import (
    regularized_incomplete_beta,
    t_cdf,
    t_one_sided_critical,
    t_ppf,
    t_sf,
    t_two_sided_critical,
)

# ---------------------------------------------------------------------------
# regularized incomplete beta - sanity properties independent of the t-CDF use
# ---------------------------------------------------------------------------


def test_incomplete_beta_boundary_values():
    assert regularized_incomplete_beta(0.0, 2.0, 3.0) == 0.0
    assert regularized_incomplete_beta(1.0, 2.0, 3.0) == 1.0


def test_incomplete_beta_symmetric_case_is_half_at_midpoint():
    # I_0.5(a, a) = 0.5 for any a, by symmetry of the Beta(a, a) density.
    for a in (0.5, 1.0, 3.0, 12.5):
        assert regularized_incomplete_beta(0.5, a, a) == pytest.approx(0.5, abs=1e-12)


def test_incomplete_beta_matches_closed_form_integer_case():
    # I_x(2, 2) has the closed form 3x^2 - 2x^3 (CDF of a Beta(2,2)).
    for x in (0.1, 0.3, 0.6, 0.9):
        expect = 3 * x**2 - 2 * x**3
        assert regularized_incomplete_beta(x, 2.0, 2.0) == pytest.approx(expect, abs=1e-10)


# ---------------------------------------------------------------------------
# t CDF / survival - internal consistency
# ---------------------------------------------------------------------------


def test_t_cdf_at_zero_is_one_half():
    for nu in (1, 2, 5, 30, 500):
        assert t_cdf(0.0, nu) == pytest.approx(0.5, abs=1e-12)


def test_t_cdf_is_antisymmetric_about_zero():
    for nu in (1, 3, 10, 100):
        for t in (0.3, 1.5, 4.0):
            assert t_cdf(-t, nu) == pytest.approx(1.0 - t_cdf(t, nu), abs=1e-12)


def test_t_sf_is_one_minus_cdf():
    for nu in (2, 9, 50):
        for t in (-2.0, 0.5, 3.0):
            assert t_sf(t, nu) == pytest.approx(1.0 - t_cdf(t, nu), abs=1e-12)


def test_t_cdf_is_monotone_increasing():
    nu = 7
    ts = [-10, -3, -1, -0.1, 0, 0.1, 1, 3, 10]
    cdfs = [t_cdf(t, nu) for t in ts]
    assert cdfs == sorted(cdfs)


# ---------------------------------------------------------------------------
# t quantile against standard published critical-value tables
# ---------------------------------------------------------------------------

#: (nu, cumulative probability, published critical value). The cumulative
#: probabilities correspond to two-sided alpha=0.05 (p=0.975), one-sided
#: alpha=0.05 (p=0.95) and one-sided alpha=0.10 / power=0.90 (p=0.90) - the
#: exact quantities VM0042's Eq. (1)/(2) need. Values are the standard
#: textbook t-table entries.
PUBLISHED_TABLE = [
    (1, 0.975, 12.706), (1, 0.95, 6.314), (1, 0.90, 3.078),
    (2, 0.975, 4.303), (2, 0.95, 2.920), (2, 0.90, 1.886),
    (5, 0.975, 2.571), (5, 0.95, 2.015), (5, 0.90, 1.476),
    (9, 0.975, 2.262), (9, 0.95, 1.833), (9, 0.90, 1.383),
    (10, 0.975, 2.228), (10, 0.95, 1.812), (10, 0.90, 1.372),
    (30, 0.975, 2.042), (30, 0.95, 1.697), (30, 0.90, 1.310),
    (100, 0.975, 1.984), (100, 0.95, 1.660), (100, 0.90, 1.290),
]


@pytest.mark.parametrize("nu,p,expect", PUBLISHED_TABLE)
def test_t_ppf_matches_published_table(nu, p, expect):
    assert t_ppf(p, nu) == pytest.approx(expect, abs=2e-3)


def test_t_ppf_approaches_normal_quantile_as_nu_grows():
    # z_0.975 = 1.959964..., z_0.90 = 1.281552...
    z_975 = 1.9599639845
    z_90 = 1.2815515655
    assert t_ppf(0.975, 100_000) == pytest.approx(z_975, abs=1e-3)
    assert t_ppf(0.90, 100_000) == pytest.approx(z_90, abs=1e-3)


def test_t_ppf_is_odd_around_p_one_half():
    for nu in (3, 8, 40):
        for p in (0.6, 0.8, 0.99):
            assert t_ppf(p, nu) == pytest.approx(-t_ppf(1 - p, nu), abs=1e-8)


def test_t_ppf_rejects_p_outside_open_interval():
    with pytest.raises(ValueError):
        t_ppf(0.0, 10)
    with pytest.raises(ValueError):
        t_ppf(1.0, 10)


# ---------------------------------------------------------------------------
# convenience wrappers used directly by loam.inverted_audit
# ---------------------------------------------------------------------------


def test_two_sided_and_one_sided_critical_match_ppf():
    nu = 14
    assert t_two_sided_critical(0.05, nu) == pytest.approx(t_ppf(0.975, nu), abs=1e-9)
    assert t_one_sided_critical(0.90, nu) == pytest.approx(t_ppf(0.90, nu), abs=1e-9)


# ---------------------------------------------------------------------------
# the sharpest check: reproduce the red team's C-3 demonstration exactly
# ---------------------------------------------------------------------------

#: docs/inverted_audit_redteam.md, section C-3: naive fixed-point iteration on
#: VM0042 Eq. (2) cycles at small n (it is a DECREASING map, more degrees of
#: freedom means a smaller t-multiplier means a smaller required n) and the
#: fix is bisection on g(n) = n_req(n) - n. These four (sigma, delta) pairs
#: and their bisection answers are quoted verbatim from that table, and from
#: the identical table in docs/phase5_inverted_audit_design.md Sec 2.1.
REDTEAM_C3_TABLE = [
    (4.0, 2.0, 45),
    (6.0, 1.5, 171),
    (3.0, 3.0, 13),
    (10.0, 1.0, 1053),
]


def _n_req_at_n(n: float, sigma: float, delta: float,
                 alpha: float = 0.05, power: float = 0.90) -> float:
    """VM0042 Eq. (2), RHS evaluated at nu = n - 1. Mirrors
    ``loam.inverted_audit.n_req`` without importing it, so this test does not
    depend on that module's internal structure - only on the shared t
    quantile function both use."""
    nu = max(n - 1.0, 1e-9)
    t_a = t_two_sided_critical(alpha, nu)
    t_b = t_one_sided_critical(power, nu)
    return (sigma * (t_a + t_b) / delta) ** 2


@pytest.mark.parametrize("sigma,delta,expect_n", REDTEAM_C3_TABLE)
def test_bisection_reproduces_redteam_c3_table(sigma, delta, expect_n):
    def g(n: float) -> float:
        return _n_req_at_n(n, sigma, delta) - n

    lo, hi = 2.0, 2.0
    while g(hi) > 0:
        hi *= 2.0
        assert hi < 1e12, "runaway search bracket"
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if g(mid) > 0:
            lo = mid
        else:
            hi = mid
    n_star = math.ceil(hi)
    assert n_star == expect_n


def test_naive_fixed_point_iteration_cycles_at_the_sigma3_delta3_case():
    """Pin the failure mode the design doc's original prescription had, so a
    future change cannot silently reintroduce plain iteration without this
    test noticing it no longer cycles (i.e. that the reintroduction is safe)."""
    sigma, delta = 3.0, 3.0
    n = 2.0
    seen = set()
    cycled = False
    for _ in range(50):
        n = _n_req_at_n(n, sigma, delta)
        key = round(n, 2)
        if key in seen:
            cycled = True
            break
        seen.add(key)
    assert cycled, (
        "expected naive fixed-point iteration to cycle at sigma=3, delta=3 "
        "(red team C-3); if it now converges, the bisection solver is no "
        "longer the only safe option and this test's premise should be "
        "revisited"
    )
