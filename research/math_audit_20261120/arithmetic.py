#!/usr/bin/env python3
"""Source-only exact arithmetic for the SZL math audit's falsification fixtures.

No provider calls, credentials, GitHub mutations, training or release authority.
Numerical checks are not Lean proofs, signed attestations, or runtime evidence.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb


def geometric_threshold(epsilon: Fraction, threshold: Fraction, n: int) -> bool:
    """Exact condition G_n(epsilon, 1,...,1) >= threshold."""
    if type(n) is not int or not 1 <= n <= 10000:
        raise ValueError("INVALID_DIMENSION")
    if not (isinstance(epsilon, Fraction) and isinstance(threshold, Fraction)):
        raise ValueError("INVALID_FRACTIONS")
    if not (0 <= epsilon <= 1 and 0 <= threshold <= 1):
        raise ValueError("INVALID_FRACTION_DOMAIN")
    return epsilon >= threshold**n


def erroneous_reversed_condition(epsilon: Fraction, threshold: Fraction, n: int) -> bool:
    """Rejected Mistral reviewer inequality; negative control, NEVER a policy."""
    return epsilon <= threshold**n


def first_strict_passing_dimension(
    epsilon: Fraction, threshold: Fraction, *, maximum: int = 10000
) -> int:
    if type(maximum) is not int or not 1 <= maximum <= 10000:
        raise ValueError("INVALID_MAXIMUM")
    if type(epsilon) is not Fraction or type(threshold) is not Fraction:
        raise ValueError("INVALID_FRACTIONS")
    if not (0 < epsilon < threshold < 1):
        raise ValueError("INVALID_THRESHOLD_ORDER")
    for n in range(1, maximum + 1):
        if epsilon > threshold**n:
            return n
    raise ValueError("NO_PASSING_DIMENSION_WITHIN_BOUND")


def no_bad_in_sample_probability(N: int, B: int, n: int) -> Fraction:
    """Hypergeometric zero-detection probability, uniform sample without replacement."""
    if not all(type(x) is int for x in (N, B, n)) or not (0 < N and 0 <= B <= N and 0 <= n <= N):
        raise ValueError("INVALID_POPULATION")
    return Fraction(comb(N - B, n), comb(N, n)) if N - B >= n else Fraction(0)


def expected_unique_repos(N: int, sample_size: int, passes: int) -> Fraction:
    """Expected unique coverage: uniform independent subset of size sample_size/pass."""
    if not all(type(x) is int for x in (N, sample_size, passes)) or not (N > 0 and 0 <= sample_size <= N and passes >= 0):
        raise ValueError("INVALID_SAMPLING_PLAN")
    return N * (1 - Fraction(N - sample_size, N) ** passes)


def advisory_summary() -> dict:
    eps, t = Fraction(1, 100), Fraction(7, 10)
    return {
        "schema": "szl.math-reviewer-falsification/v1",
        "source_scope": "SOURCE_ONLY_NOT_FORMAL_OR_RELEASE_PROOF",
        "epsilon": str(eps),
        "threshold": str(t),
        "n_at_first_strict_threshold_crossing": first_strict_passing_dimension(eps, t),
        "t_to_13_exact": str(t**13),
        "geometric_threshold_n13_true": geometric_threshold(eps, t, 13),
        "reviewer_reversed_inequality_n13_false": erroneous_reversed_condition(eps, t, 13),
        "observed_github_population": 182,
        "hypothetical_bad_repositories": 15,
        "prob_zero_bad_in_sample_30_of_182": str(no_bad_in_sample_probability(182, 15, 30)),
        "expected_coverage_ten_independent_samples_of_20": str(expected_unique_repos(182, 20, 10)),
        "independent_model_output_verified": False,
        "lean_kernel_proof_performed": False,
        "releases_or_training_authorized": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(advisory_summary(), sort_keys=True, indent=2))
