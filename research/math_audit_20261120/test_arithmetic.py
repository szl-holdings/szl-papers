"""Independent, no-network falsification controls for the SZL math referee."""
from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().with_name("arithmetic.py")
spec = importlib.util.spec_from_file_location("szl_review_falsification", SOURCE)
assert spec is not None and spec.loader is not None
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MathAudit(unittest.TestCase):
    def test_exact_threshold_at_13(self):
        self.assertTrue(m.geometric_threshold(Fraction(1,100), Fraction(7,10), 13))

    def test_threshold_not_met_at_12(self):
        self.assertFalse(m.geometric_threshold(Fraction(1,100), Fraction(7,10), 12))

    def test_reversed_reviewer_falsified(self):
        eps, t = Fraction(1,100), Fraction(7,10)
        self.assertNotEqual(
            m.geometric_threshold(eps,t,13),
            m.erroneous_reversed_condition(eps,t,13),
        )

    def test_exact_threshold_power(self):
        self.assertEqual(Fraction(7,10)**13, Fraction(96889010407, 10**13))

    def test_first_strict_dimension(self):
        self.assertEqual(m.first_strict_passing_dimension(Fraction(1,100),Fraction(7,10)),13)

    def test_no_dimension_within_limit_is_typed_hold(self):
        with self.assertRaisesRegex(ValueError, "NO_PASSING_DIMENSION_WITHIN_BOUND"):
            m.first_strict_passing_dimension(Fraction(1,3), Fraction(1,2), maximum=1)

    def test_dimension_limit_rejects_bad_types_and_values(self):
        for limit in (True, False, None, 0, -1, 1.0, 10001):
            with self.subTest(limit=limit):
                with self.assertRaisesRegex(ValueError, "INVALID_MAXIMUM"):
                    m.first_strict_passing_dimension(Fraction(1,3), Fraction(1,2), maximum=limit)

    def test_first_passing_dimension_requires_exact_fractions(self):
        with self.assertRaisesRegex(ValueError, "INVALID_FRACTIONS"):
            m.first_strict_passing_dimension(0.01, Fraction(7,10))

    def test_dimension_limit_boundary_exactly_satisfies(self):
        self.assertEqual(
            m.first_strict_passing_dimension(Fraction(1,3), Fraction(1,2), maximum=2),
            2,
        )

    def test_equal_boundary_is_admitted_by_score_only(self):
        self.assertTrue(m.geometric_threshold(Fraction(1,4), Fraction(1,2), 2))

    def test_bad_type_boolean_dimension_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_DIMENSION"):
            m.geometric_threshold(Fraction(1,4),Fraction(1,2),True)

    def test_bad_type_float_fraction_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_FRACTIONS"):
            m.geometric_threshold(.01,Fraction(7,10),13)

    def test_no_bad_repositories_probability_one(self):
        self.assertEqual(m.no_bad_in_sample_probability(182,0,30),1)

    def test_one_bad_definitely_detected_by_full_census(self):
        self.assertEqual(m.no_bad_in_sample_probability(182,1,182),0)

    def test_hypothetical_sample_cannot_rule_out_15_bad_at_five_percent(self):
        p=m.no_bad_in_sample_probability(182,15,30)
        self.assertGreater(p,Fraction(1,20))
        self.assertAlmostEqual(float(p),0.059434905874682746,places=14)

    def test_repeating_partial_random_passes_expect_incomplete_coverage(self):
        expected=m.expected_unique_repos(182,20,10)
        self.assertLess(expected,182)
        self.assertAlmostEqual(float(expected),125.17915950060231,places=9)

    def test_sample_probability_rejects_oversized_population(self):
        with self.assertRaisesRegex(ValueError, "INVALID_POPULATION"):
            m.no_bad_in_sample_probability(10001, 0, 0)

    def test_expected_coverage_rejects_oversized_population(self):
        with self.assertRaisesRegex(ValueError, "INVALID_SAMPLING_PLAN"):
            m.expected_unique_repos(10001, 1, 1)

    def test_expected_coverage_rejects_oversized_pass_budget(self):
        # Deliberately use 513 rather than an enormous exponent for the red test.
        with self.assertRaisesRegex(ValueError, "INVALID_SAMPLING_PLAN"):
            m.expected_unique_repos(182, 20, 513)

    def test_extreme_audit_loop_refuses_before_big_integer_exponent(self):
        # A huge Fraction exponent must never run during an offline review.
        with self.assertRaisesRegex(ValueError, "INVALID_SAMPLING_PLAN"):
            m.expected_unique_repos(182, 20, 10**8)
        with self.assertRaisesRegex(ValueError, "INVALID_POPULATION"):
            m.no_bad_in_sample_probability(10**9, 0, 0)

    def test_bounded_full_population_coverage_still_exact(self):
        self.assertEqual(m.no_bad_in_sample_probability(10000, 0, 0), 1)
        self.assertEqual(m.expected_unique_repos(10000, 10000, 512), 10000)

    def test_full_census_even_one_pass_is_complete(self):
        self.assertEqual(m.expected_unique_repos(182,182,1),182)

    def test_zero_passes_cover_nothing(self):
        self.assertEqual(m.expected_unique_repos(182,20,0),0)

    def test_false_independence_of_two_reviewers(self):
        p=Fraction(1,5)
        self.assertGreater(p,p*p)

    def test_invalid_population_boolean_rejected(self):
        with self.assertRaisesRegex(ValueError,"INVALID_POPULATION"):
            m.no_bad_in_sample_probability(182,True,30)

    def test_never_claims_formal_or_runtime_authority(self):
        out=m.advisory_summary()
        for key in ("independent_model_output_verified","lean_kernel_proof_performed",
                    "releases_or_training_authorized"):
            self.assertIs(out[key],False)
        self.assertEqual(out["n_at_first_strict_threshold_crossing"],13)


if __name__ == "__main__":
    unittest.main()
