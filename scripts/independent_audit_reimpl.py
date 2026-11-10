"""Independent re-implementation of the inverted-audit sample-size / cost calculation.

INDEPENDENCE STATEMENT: this file was written WITHOUT reading, grepping, importing
or otherwise inspecting any of: src/loam/inverted_audit.py, src/loam/student_t.py,
tests/test_inverted_audit.py, tests/test_student_t.py, scripts/run_inverted_audit.py,
data/processed/inverted_audit.json, or anything under data/processed/. It does not
import the `loam` package. It was written from a standalone specification plus
docs/phase5_inverted_audit_design.md sections 2.1-2.3 and DECISIONS.md D-060/D-061
(background only; the standalone specification governs). Student's t quantiles come
from scipy.stats.t, not from any project code. Its purpose is to be diffed against
the existing implementation.

Model
-----
Components are percent CVs of SOC *stock*, converted to Mg C/ha via a reference
stock R = 60 Mg C/ha (sigma_abs = CV/100 * R).

    paired:   S(C)^2 = sigma_R^2   + 2 (sigma_W^2 + sigma_A^2)/C + 2 sigma_T^2
    unpaired: S(C)^2 = 2 sigma_B^2 + 2 (sigma_W^2 + sigma_A^2)/C + 2 sigma_T^2

n_req (VM0042 Eq. 2) = smallest integer n >= 2 with
    n >= ( S (t_{0.975, n-1} + t_{0.90, n-1}) / Delta )^2 .

Method for n_req: g(n) = n - RHS(n) is STRICTLY INCREASING in n, because n grows
and RHS(n) is non-increasing (both t quantiles with p > 0.5 decrease as the degrees
of freedom grow). So the admissible set {n >= 2 : g(n) >= 0} is an up-set of the
integers and its minimum is found exactly by (i) returning 2 if g(2) >= 0, else
(ii) exponential search for an upper bracket hi with g(hi) >= 0 (starting from
the large-sample lower bound, since RHS(n) > (S (z_a + z_b)/Delta)^2 for every
finite n), then (iii) integer bisection keeping g(lo) < 0 <= g(hi). No fixed-point
iteration is used. `--selfcheck` verifies this against a brute-force linear scan.

Cost: cost(n, C) = n (C c_loc + c_assay). For each design, C = 1..30 is scanned and
the minimum-cost C is kept (ties -> smallest C). The headline design is the one with
lower optimal cost (ties -> paired). Implied uncertainty deduction at the headline
optimum: UNC = k * (S / sqrt(n_req)) / Delta * 100.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

from scipy.stats import norm, t as student_t

# I/O defaults edited after delivery (WP3, by the session that commissioned
# this file, NOT its author) to point at repository paths instead of a
# session scratch directory. No other line of this file was changed.
_REPO = Path(__file__).resolve().parent.parent
DEFAULT_IN = _REPO / "data" / "audit" / "reimpl_cases.json"
DEFAULT_OUT = _REPO / "data" / "processed" / "reimpl_out.json"

REFERENCE_STOCK = 60.0  # Mg C / ha
CV_PCT = {
    "B": 3.136,  # between-plot
    "W": 8.0,  # within-plot
    "A": 1.25,  # analytical
    "T": 2.708,  # temporal
    "R": 9.4,  # relocation, difference scale (default)
}
ALPHA_Q = 0.975  # two-sided alpha = 0.05
POWER_Q = 0.90  # one-sided, power 0.90
C_MAX = 30


def absolute(cv_pct: float) -> float:
    return cv_pct / 100.0 * REFERENCE_STOCK


def components(relocation: str) -> dict[str, float]:
    comp = {k: absolute(v) for k, v in CV_PCT.items()}
    if relocation == "difference_scale":
        pass
    elif relocation == "per_observation_sqrt2":
        comp["R"] = absolute(CV_PCT["R"] / math.sqrt(2.0))
    else:
        raise ValueError(relocation)
    return comp


def s_of_c(design: str, c: int, comp: dict[str, float]) -> float:
    shared = 2.0 * (comp["W"] ** 2 + comp["A"] ** 2) / c + 2.0 * comp["T"] ** 2
    if design == "paired":
        var = comp["R"] ** 2 + shared
    elif design == "unpaired":
        var = 2.0 * comp["B"] ** 2 + shared
    else:
        raise ValueError(design)
    return math.sqrt(var)


def rhs(n: int, s: float, delta: float) -> float:
    nu = n - 1
    mult = student_t.ppf(ALPHA_Q, nu) + student_t.ppf(POWER_Q, nu)
    return (s * mult / delta) ** 2


def n_req(s: float, delta: float) -> int:
    """Smallest integer n >= 2 with n >= RHS(n); bracket + integer bisection."""

    def g(n: int) -> float:
        return n - rhs(n, s, delta)

    if g(2) >= 0:
        return 2
    lo = 2  # invariant: g(lo) < 0
    z_bound = (s * (norm.ppf(ALPHA_Q) + norm.ppf(POWER_Q)) / delta) ** 2
    # every n <= z_bound fails (RHS(n) > z_bound >= n), so it is a valid lo
    cand = int(math.floor(z_bound))
    if cand > lo:
        lo = cand
    hi = max(lo + 1, int(math.ceil(z_bound * 1.05)) + 1)
    while g(hi) < 0:
        lo, hi = hi, hi * 2
    while hi - lo > 1:  # invariant: g(lo) < 0 <= g(hi)
        mid = (lo + hi) // 2
        if g(mid) >= 0:
            hi = mid
        else:
            lo = mid
    return hi


def n_req_scan(s: float, delta: float, limit: int = 100000) -> int:
    """Brute-force reference: first n >= 2 with n >= RHS(n)."""
    for n in range(2, limit):
        if n >= rhs(n, s, delta):
            return n
    raise RuntimeError("scan limit")


def optimise(design: str, delta: float, comp, c_loc: float, c_assay: float):
    best = None
    for c in range(1, C_MAX + 1):
        s = s_of_c(design, c, comp)
        n = n_req(s, delta)
        cost = n * (c * c_loc + c_assay)
        if best is None or cost < best["cost"]:  # strict '<' keeps smallest C on ties
            best = {"C": c, "n_req": n, "S": s, "cost": cost}
    return best


def r6(x: float) -> float:
    return round(float(x), 6)


VARIANTS = {
    "default": {"relocation": "difference_scale", "c_loc": 15.0, "c_assay": 20.0},
    "relocation_per_observation_sqrt2": {
        "relocation": "per_observation_sqrt2",
        "c_loc": 15.0,
        "c_assay": 20.0,
    },
    "assay_cost_60": {"relocation": "difference_scale", "c_loc": 15.0, "c_assay": 60.0},
}


def run(cases):
    z_sum = norm.ppf(ALPHA_Q) + norm.ppf(POWER_Q)
    out = {}
    for vname, v in VARIANTS.items():
        comp = components(v["relocation"])
        vout = {}
        for case in cases:
            delta = float(case["delta_mg_c_ha"])
            k = float(case["k"])
            res = {
                d: optimise(d, delta, comp, v["c_loc"], v["c_assay"])
                for d in ("paired", "unpaired")
            }
            head = "paired" if res["paired"]["cost"] <= res["unpaired"]["cost"] else "unpaired"
            h = res[head]
            unc = k * (h["S"] / math.sqrt(h["n_req"])) / delta * 100.0
            vout[case["case_id"]] = {
                **{
                    d: {"C": r["C"], "n_req": r["n_req"], "S": r6(r["S"]), "cost": r6(r["cost"])}
                    for d, r in res.items()
                },
                "headline_design": head,
                "implied_deduction_pct": r6(unc),
                "large_sample_approx_pct": r6(k * 100.0 / z_sum),
            }
        out[vname] = vout
    return out


def selfcheck() -> None:
    # Red-team table from design doc Sec 2.1 (sigma, Delta) -> n
    for s, d, want in [(4.0, 2.0, 45), (3.0, 3.0, 13), (10.0, 1.0, 1053)]:
        got = n_req(s, d)
        assert got == want, (s, d, got, want)
        assert n_req_scan(s, d) == want
    rng = random.Random(12345)
    for _ in range(400):
        s = rng.uniform(0.5, 12.0)
        d = rng.uniform(0.3, 20.0)
        if (s * 3.3 / d) ** 2 > 20000:
            continue
        a, b = n_req(s, d), n_req_scan(s, d)
        assert a == b, (s, d, a, b)
    print("selfcheck OK")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=Path, default=DEFAULT_IN)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--selfcheck", action="store_true")
    a = ap.parse_args(argv)
    if a.selfcheck:
        selfcheck()
    cases = json.loads(a.cases.read_text())
    out = run(cases)
    a.out.write_text(json.dumps(out, indent=2))
    print(f"wrote {a.out} ({len(cases)} cases x {len(out)} variants)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
