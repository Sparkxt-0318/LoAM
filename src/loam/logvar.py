"""Unbiased log-variance estimation from small, unequal replicate counts.

WHY THIS MODULE EXISTS
----------------------
D-040's joint covariate model regressed ``log(sd)`` on covariates by unweighted
OLS, restricted to treatments with at least three replicates. Re-run across four
nested NAPESHM samples during the D-055 work, that specification returned

    t = -0.37,  +4.58,  -4.53,  +0.75

on the same coefficient — **changing sign twice**. The debiased, weighted version
of the identical contrast was flat in all four. A specification that flips sign
across nested subsets of one dataset while its unbiased counterpart does not is
reporting itself, not the soil.

The cause is not subtle and it is not the covariates. It is that ``log s`` is a
strongly biased estimator of ``log sigma`` at small degrees of freedom, and the
bias DEPENDS ON THE DEGREES OF FREEDOM:

    E[log s^2] = log sigma^2 + psi(nu/2) - log(nu/2)

At ``nu = 1`` that bias is about -1.27 in log-variance units — a factor of 3.6
downward — and it shrinks towards zero as ``nu`` grows. So in a sample where
replicate count correlates with anything at all, an unweighted regression on
``log(sd)`` fits the replicate count. In NAPESHM replicate count is perfectly
aliased with country (D-040 check 1c), which is exactly the aliasing that made
the sign flip.

Dropping the low-replicate treatments does not fix it. It changes which
treatments carry the bias, which is why the sign moves when the filter admits a
different set.

THE FIX
-------
Two corrections, both standard, both cheap:

1. **Debias.** ``y = log(s^2) - psi(nu/2) + log(nu/2)`` is unbiased for
   ``log sigma^2`` at every ``nu``.
2. **Weight by information.** ``Var[log s^2] = psi'(nu/2)``, so
   ``w = 1 / psi'(nu/2)`` is the efficient weight. A 2-replicate treatment then
   contributes at its true (small) information content instead of being either
   dropped or counted equally.

Both facts are exact for Gaussian data — ``nu * s^2 / sigma^2 ~ chi^2_nu``, and
the log of a chi-square has mean ``psi(nu/2) + log 2`` and variance
``psi'(nu/2)``.

WHY PURE PYTHON RATHER THAN SCIPY
---------------------------------
``src/loam`` is deliberately standard-library only: CI installs ``[dev]`` (pytest
and pyyaml) and the guards have to run there. That is not a compromise here,
because ``nu`` is always a positive integer, so ``nu/2`` is always an integer or a
half-integer — and at those arguments ``psi`` and ``psi'`` have EXACT closed
forms. No asymptotic series, no accuracy question:

    psi(1)       = -gamma                     psi'(1)       = pi^2 / 6
    psi(1/2)     = -gamma - 2 ln 2            psi'(1/2)     = pi^2 / 2
    psi(k+1)     = psi(1)   + sum 1/j         psi'(k+1)     = psi'(1)   - sum 1/j^2
    psi(k+1/2)   = psi(1/2) + 2 sum 1/(2j-1)  psi'(k+1/2)   = psi'(1/2) - 4 sum 1/(2j-1)^2

``tests/test_logvar_estimator.py`` checks these against independently known
values and against a seeded Monte Carlo, and it guards against the retired
specification being reintroduced.

WHAT THIS DOES NOT CLAIM
------------------------
Debiasing does not rescue a null. It makes a null HARDER to reach, not easier:
the unweighted estimator's excess noise inflates standard errors, so a genuine
signal is more likely to be missed and a spurious one more likely to appear at
random. D-040's substantive conclusion — between-plot CV is approximately
invariant across the covariates an MDC surface would use — was a null, and a
noisy estimator biases AGAINST reaching a null, not toward it. Correcting the
estimator therefore cannot manufacture D-040's conclusion; it can only confirm or
overturn it. See D-058.
"""

from __future__ import annotations

import math

#: Euler-Mascheroni constant, to double precision.
EULER_GAMMA = 0.5772156649015328606

#: psi(1) and psi(1/2) — the two anchors every value below is built from.
_PSI_1 = -EULER_GAMMA
_PSI_HALF = -EULER_GAMMA - 2.0 * math.log(2.0)

#: psi'(1) and psi'(1/2).
_PSI1_1 = math.pi ** 2 / 6.0
_PSI1_HALF = math.pi ** 2 / 2.0


def digamma_half_integer(two_x: int) -> float:
    """``psi(two_x / 2)`` for positive integer ``two_x``. Exact.

    ``two_x`` is twice the argument, so that the argument is always representable
    without floating-point drift: ``two_x = 3`` means ``psi(1.5)``.
    """
    if two_x < 1:
        raise ValueError(f"argument must be positive; got two_x={two_x}")
    if two_x % 2 == 0:                       # psi(k) for integer k >= 1
        k = two_x // 2
        return _PSI_1 + sum(1.0 / j for j in range(1, k))
    k = (two_x - 1) // 2                     # psi(k + 1/2)
    return _PSI_HALF + 2.0 * sum(1.0 / (2 * j - 1) for j in range(1, k + 1))


def trigamma_half_integer(two_x: int) -> float:
    """``psi'(two_x / 2)`` for positive integer ``two_x``. Exact."""
    if two_x < 1:
        raise ValueError(f"argument must be positive; got two_x={two_x}")
    if two_x % 2 == 0:                       # psi'(k) for integer k >= 1
        k = two_x // 2
        return _PSI1_1 - sum(1.0 / j ** 2 for j in range(1, k))
    k = (two_x - 1) // 2                     # psi'(k + 1/2)
    return _PSI1_HALF - 4.0 * sum(1.0 / (2 * j - 1) ** 2 for j in range(1, k + 1))


def log_variance_bias(nu: int) -> float:
    """``E[log s^2] - log sigma^2`` at ``nu`` degrees of freedom.

    Always negative: a small-sample variance estimate is biased DOWNWARD on the
    log scale, and sharply so. ``nu = 1`` gives about -1.27.
    """
    if nu < 1:
        raise ValueError(f"need nu >= 1; got {nu}")
    return digamma_half_integer(nu) - math.log(nu / 2.0)


def log_variance_variance(nu: int) -> float:
    """``Var[log s^2]`` at ``nu`` degrees of freedom. This is ``psi'(nu/2)``."""
    if nu < 1:
        raise ValueError(f"need nu >= 1; got {nu}")
    return trigamma_half_integer(nu)


def debias(log_s2: float, nu: int) -> float:
    """Unbiased estimate of ``log sigma^2`` from an observed ``log s^2``."""
    return log_s2 - log_variance_bias(nu)


def weight(nu: int) -> float:
    """Efficient regression weight for one debiased observation: ``1/psi'(nu/2)``."""
    return 1.0 / log_variance_variance(nu)


def prepare(sample_variances, replicate_counts):
    """Debias and weight a set of per-group sample variances.

    Returns ``(y, w)`` as lists: ``y`` unbiased for ``log sigma^2`` per group,
    ``w`` the efficient weights. Groups with a non-positive or missing variance,
    or fewer than two replicates, are dropped and reported by position so the
    caller can keep its covariates aligned.

    This is the only entry point the derivation scripts should use. Keeping the
    arithmetic in one place is the point: the D-040 specification survived as
    long as it did because it was six lines inside one function, with nothing
    naming it or testing it.
    """
    y, w, kept = [], [], []
    for i, (s2, n) in enumerate(zip(sample_variances, replicate_counts)):
        if s2 is None or n is None:
            continue
        try:
            s2f, nf = float(s2), int(n)
        except (TypeError, ValueError):
            continue
        if not (s2f > 0.0) or nf < 2 or s2f != s2f:      # NaN-safe
            continue
        nu = nf - 1
        y.append(debias(math.log(s2f), nu))
        w.append(weight(nu))
        kept.append(i)
    return y, w, kept
