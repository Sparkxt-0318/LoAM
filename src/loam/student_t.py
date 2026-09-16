"""Student's t distribution — CDF, survival, and quantile (inverse CDF).

WHY THIS MODULE EXISTS
-----------------------
The Phase 5 inverted audit (``loam.inverted_audit``) solves VM0042's own
Equation (2), ``n >= (S * (t_alpha + t_beta) / MDD)^2``, for the smallest
admissible sample size. That needs t-distribution QUANTILES at a degrees of
freedom that is itself a function of the unknown ``n`` — the fixed point the
red team's C-3 objection showed cannot be reached by naive iteration (see
``docs/inverted_audit_redteam.md``). Bisection on that fixed point (see
``loam.inverted_audit.n_req``) needs a t quantile function that is monotone,
accurate at small degrees of freedom, and callable many times cheaply.

``src/loam`` is deliberately standard-library only (see ``loam.logvar`` for
why: CI installs only ``[dev]`` — pytest and pyyaml — and the guards have to
run there). ``scipy.stats.t`` is not available. This module supplies the same
functionality from ``math`` alone.

METHOD
------
The t CDF has a closed relationship to the regularized incomplete beta
function I_x(a, b) (Abramowitz & Stegun 26.7.1-26.7.5):

    F(t; nu) = 1 - 0.5 * I_x(nu/2, 1/2)   for t >= 0
    F(t; nu) = 0.5 * I_x(nu/2, 1/2)       for t <  0
    x = nu / (nu + t^2)

``I_x`` is evaluated by the standard continued-fraction expansion (Numerical
Recipes in C, 3rd ed., section 6.4), which converges quickly and uniformly
across the range this module is used at (nu from 1 to several thousand,
non-integer nu included, since the bisection in ``inverted_audit`` searches
over real-valued n before rounding up to an integer sample size).

There is no closed form for the quantile (inverse CDF), so ``t_ppf`` inverts
the CDF by bisection. The CDF is strictly monotone in t, so this is safe and
needs no starting guess.

VERIFICATION
------------
``tests/test_student_t.py`` checks ``t_ppf`` against standard published
critical-value tables (two-sided alpha=0.05 and one-sided 0.90 and 0.95, at a
spread of degrees of freedom from 1 to 100) to within 2e-3, and checks the
z-distribution limit as nu -> infinity. It also reproduces, exactly, the
worked ``n_req`` values in the red team's C-3 demonstration table — the
sharpest available check, because those four numbers are the reason this
module exists.
"""

from __future__ import annotations

import math

#: Continued-fraction iteration cap and convergence tolerance for the
#: incomplete beta function. 150 iterations / 1e-12 relative tolerance is
#: generous for the a, b, x ranges this module is ever called at (b is always
#: exactly 1/2; a = nu/2 for nu from about 1 to 1e6) - the continued fraction
#: converges geometrically, so in practice this triggers the early-exit
#: `abs(delta - 1.0) < eps` well before the cap on every input this module
#: has been exercised against; the cap is a safety net, not the normal path.
_BETACF_MAXIT = 150
_BETACF_EPS = 1e-12
_BETACF_FPMIN = 1e-300


def _betacf(a: float, b: float, x: float) -> float:
    """Continued-fraction factor for the regularized incomplete beta.

    Lentz's algorithm, as in Numerical Recipes 3rd ed. section 6.4. Not
    meaningful on its own; ``regularized_incomplete_beta`` is the entry point.
    """
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < _BETACF_FPMIN:
        d = _BETACF_FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, _BETACF_MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < _BETACF_FPMIN:
            d = _BETACF_FPMIN
        c = 1.0 + aa / c
        if abs(c) < _BETACF_FPMIN:
            c = _BETACF_FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < _BETACF_FPMIN:
            d = _BETACF_FPMIN
        c = 1.0 + aa / c
        if abs(c) < _BETACF_FPMIN:
            c = _BETACF_FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < _BETACF_EPS:
            break
    return h


def regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    """``I_x(a, b)``, for ``a, b > 0`` and ``0 <= x <= 1``.

    Uses the continued-fraction expansion on whichever side of
    ``x = (a+1)/(a+b+2)`` converges fastest, and the symmetry relation
    ``I_x(a,b) = 1 - I_(1-x)(b,a)`` to reach the other side. Standard method;
    see Numerical Recipes 3rd ed. section 6.4.
    """
    if not (0.0 <= x <= 1.0):
        raise ValueError(f"x must be in [0, 1]; got {x}")
    if a <= 0.0 or b <= 0.0:
        raise ValueError(f"a and b must be positive; got a={a}, b={b}")
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    log_bt = (
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log(1.0 - x)
    )
    bt = math.exp(log_bt)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_cdf(t: float, nu: float) -> float:
    """``P(T <= t)`` for ``T ~ Student's t`` with ``nu`` degrees of freedom.

    ``nu`` need not be an integer: the bisection search in
    ``loam.inverted_audit.n_req`` treats sample size as continuous until the
    last step, and the incomplete-beta relation this is built on is valid for
    any real ``nu > 0``.
    """
    if nu <= 0:
        raise ValueError(f"nu must be positive; got {nu}")
    x = nu / (nu + t * t)
    ib = regularized_incomplete_beta(x, nu / 2.0, 0.5)
    return 1.0 - 0.5 * ib if t >= 0 else 0.5 * ib


def t_sf(t: float, nu: float) -> float:
    """``P(T > t)`` — the upper tail / survival function."""
    return 1.0 - t_cdf(t, nu)


#: Bisection depth for t_ppf. Bisection halves the bracket every step, so
#: this is chosen for ABSOLUTE PRECISION, not iteration-count comfort: at the
#: default 1e5 bracket, 35 steps already gives precision 1e5/2^35 ~ 2.9e-6 -
#: far below anything ``loam.inverted_audit`` can use (it works in Mg C/ha to
#: a handful of significant figures, and t only ever enters that module
#: squared). ``loam.inverted_audit`` calls this function deep inside its OWN
#: nested bisections (n_req's search x this, and n_req itself sits inside
#: cost_optimum's C-sweep and the break_even_* searches), so its cost is
#: multiplied many times over one audit run - an original 200 (1e5/2^200, a
#: precision with no physical meaning at all) made a full corpus run take
#: minutes; 35 does not change any reported figure at the precision it is
#: rounded to.
_T_PPF_ITERATIONS = 35


def t_ppf(p: float, nu: float, bracket: float = 1.0e5) -> float:
    """The quantile function: ``t`` such that ``P(T <= t) = p``.

    No closed form exists, so this bisects the (strictly monotone) CDF. The
    initial bracket is wide enough that even ``p`` extremely close to 0 or 1
    at ``nu = 1`` (the heaviest-tailed case in practice here) stays inside it;
    if it did not, the loop would silently return a bracket endpoint, so a
    ValueError is preferable and cheap to check.
    """
    if not (0.0 < p < 1.0):
        raise ValueError(f"p must be strictly between 0 and 1; got {p}")
    lo, hi = -bracket, bracket
    if t_cdf(lo, nu) > p or t_cdf(hi, nu) < p:
        raise ValueError(
            f"t_ppf(p={p}, nu={nu}) falls outside the search bracket "
            f"+/-{bracket}; widen it explicitly if this is truly needed"
        )
    for _ in range(_T_PPF_ITERATIONS):
        mid = (lo + hi) / 2.0
        if t_cdf(mid, nu) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def t_two_sided_critical(alpha: float, nu: float) -> float:
    """The two-sided critical value at significance ``alpha``: ``t_{1-alpha/2, nu}``.

    This is VM0042's ``t_alpha`` in Equations (1)/(2), Section 8.2.1 item 11,
    at the methodology's own stated convention ("frequently taken as 0.05",
    two-sided).
    """
    return t_ppf(1.0 - alpha / 2.0, nu)


def t_one_sided_critical(power: float, nu: float) -> float:
    """The one-sided critical value at power ``power``: ``t_{power, nu}``.

    This is VM0042's ``t_beta`` — the methodology states type II error
    "(e.g., 90%)" as one-sided power, so ``power=0.90`` reproduces the
    convention it uses.
    """
    return t_ppf(power, nu)
