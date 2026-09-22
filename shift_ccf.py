
"""
Shift Arithmetic Standalone Gauntlet Suite
Operator: a * b = a(b + 1)
"""

import math
import unittest
from fractions import Fraction
from typing import List


def shift(a: Fraction, b: Fraction) -> Fraction:
    """Core binary shift operation: a * b = a(b + 1)"""
    return a * (b + 1)


# =====================================================================
# SECTOR 1: ALGEBRAIC TRAPS & CANCELLATION FALLACIES
# =====================================================================

class TestGauntletAlgebraicTraps(unittest.TestCase):
    def test_cancellation_trap_zero_factor(self):
        """
        Trap: 2 * (-1) = 7 * (-1) = 0.
        Canceling right input (-1) yields 2 = 7 (FALLACY).
        Reason: Factor (c + 1) evaluates to 0 when c = -1.
        """
        val1 = shift(Fraction(2), Fraction(-1))
        val2 = shift(Fraction(7), Fraction(-1))

        self.assertEqual(val1, Fraction(0))
        self.assertEqual(val2, Fraction(0))
        self.assertEqual(val1, val2)

    def test_left_cancellation_conditions(self):
        """
        a * b = a * c  ==>  b = c holds IF AND ONLY IF a != 0.
        When a = 0, 0 * b = 0 * c = 0 for all b, c.
        """
        a_nonzero = Fraction(5)
        b, c = Fraction(3), Fraction(4)

        self.assertNotEqual(shift(a_nonzero, b), shift(a_nonzero, c))

        a_zero = Fraction(0)
        self.assertEqual(shift(a_zero, b), shift(a_zero, c))

    def test_right_cancellation_conditions(self):
        """
        a * c = b * c  ==>  a = b holds IF AND ONLY IF c != -1.
        When c = -1, a * (-1) = b * (-1) = 0 for all a, b.
        """
        c_valid = Fraction(2)
        a, b = Fraction(3), Fraction(7)

        self.assertNotEqual(shift(a, c_valid), shift(b, c_valid))

        c_singular = Fraction(-1)
        self.assertEqual(shift(a, c_singular), shift(b, c_singular))

    def test_zero_factor_theorem(self):
        """
        a * b = 0  <==>  a = 0 OR b = -1 over Real numbers.
        """
        self.assertEqual(shift(Fraction(0), Fraction(100)), Fraction(0))
        self.assertEqual(shift(Fraction(100), Fraction(-1)), Fraction(0))

    def test_fixed_point_identity(self):
        """
        Fixed-point law: a * b = a  <==>  a(b + 1) = a  <==>  ab = 0
        (where ab denotes ordinary multiplication).
        For a != 0, forces b = 0.
        For a = 0, holds for all b.
        """
        a_nonzero = Fraction(4)
        self.assertEqual(shift(a_nonzero, Fraction(0)), a_nonzero)
        self.assertNotEqual(shift(a_nonzero, Fraction(2)), a_nonzero)


# =====================================================================
# SECTOR 2: QUADRATIC EQUATIONS & DOMAIN BOUNDARIES
# =====================================================================

class TestGauntletQuadraticBoundaries(unittest.TestCase):
    """
    Solves x * x = t  <==>  x^2 + x - t = 0  <==>  (x + 1/2)^2 = t + 1/4

    Domain Classification:
      - t < -1/4:  No real solutions (Discriminant < 0).
      - t = -1/4:  Single real/rational solution x = -1/2.
      - t > -1/4:  Two real solutions x = (-1 ± sqrt(1 + 4t)) / 2.
                   These solutions are rational iff (1/4 + t) is a square in Q.
    """

    def _solve_self_shift_rational(self, t: Fraction) -> List[Fraction]:
        """Returns rational solutions to x * x = t."""
        discriminant = Fraction(1, 4) + t
        if discriminant < 0:
            return []  # No real solutions exist

        num, den = discriminant.numerator, discriminant.denominator
        sqrt_num = math.isqrt(num)
        sqrt_den = math.isqrt(den)

        # Check if discriminant is a perfect square in Q
        if sqrt_num * sqrt_num == num and sqrt_den * sqrt_den == den:
            sqrt_disc = Fraction(sqrt_num, sqrt_den)
            x1 = Fraction(-1, 2) + sqrt_disc
            x2 = Fraction(-1, 2) - sqrt_disc
            return list(set([x1, x2]))

        # Real solutions exist, but neither is rational
        return []

    def test_quadratic_two_rational_roots(self):
        """Solve x * x = 2: yields rational roots x = 1 or x = -2."""
        roots = self._solve_self_shift_rational(Fraction(2))
        self.assertCountEqual(roots, [Fraction(1), Fraction(-2)])
        for r in roots:
            self.assertEqual(shift(r, r), Fraction(2))

    def test_quadratic_irrational_real_roots(self):
        """
        Solve x * x = 1: Discriminant = 5/4 > 0 (Real roots exist: (-1 ± sqrt(5))/2).
        Rational solver correctly returns [] because no rational roots exist.
        """
        roots = self._solve_self_shift_rational(Fraction(1))
        self.assertEqual(roots, [])

    def test_quadratic_boundary_case(self):
        """Solve x * x = -1/4: Discriminant = 0, yields unique root x = -1/2."""
        roots = self._solve_self_shift_rational(Fraction(-1, 4))
        self.assertEqual(roots, [Fraction(-1, 2)])
        self.assertEqual(shift(Fraction(-1, 2), Fraction(-1, 2)), Fraction(-1, 4))

    def test_quadratic_no_real_solutions(self):
        """Solve x * x = -1: Discriminant = -3/4 < 0. Zero real solutions."""
        roots = self._solve_self_shift_rational(Fraction(-1))
        self.assertEqual(roots, [])


# =====================================================================
# SECTOR 3: ALGEBRAIC ROOTS VS. UNIT-LEAF CONSTRUCTIBILITY
# =====================================================================

class TestGauntletConstructibilityVerdict(unittest.TestCase):
    def test_algebraic_validity_vs_unit_constructibility(self):
        """
        Algebraic Root vs. Unit-Leaf Constructibility:
        ----------------------------------------------
        x = -2 is a valid real/rational root of x * x = 2 since (-2) * (-2) = 2.

        Inductive Proof of Unit-Tree Positivity:
          Base Case (n = 1): A leaf node val = 1 > 0.
          Inductive Step: Let T = L * R. By IH, L > 0 and R >= 1.
          Evaluation: L * R = L(R + 1).
          Since L > 0 and (R + 1) >= 2 > 0, L(R + 1) > 0.

        By induction, every unit-leaf tree evaluates to a positive value (> 0).
        Therefore, negative algebraic roots (like x = -2) are non-constructible.
        """
        x_root = Fraction(-2)

        # Verify algebraic correctness
        self.assertEqual(shift(x_root, x_root), Fraction(2))

        # Check domain exclusion against unit tree lower bound
        self.assertLess(x_root, Fraction(0))


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False, verbosity=2)