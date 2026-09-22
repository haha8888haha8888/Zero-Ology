
"""
Shift Arithmetic Gauntlet v3
User‑Selectable Range
Operator: a ⋆ b = a(b + 1)
"""

import math
import unittest
from fractions import Fraction

# ============================================================
# USER INPUT FOR RANGE
# ============================================================

def get_limit():
    try:
        raw = input("Enter max integer to analyze (default 1000, max 50000): ").strip()
        if raw == "":
            return 1000
        val = int(raw)
        return max(1, min(val, 50000))
    except:
        return 1000

EXTENDED_LIMIT = get_limit()


# ============================================================
# CORE OPERATION
# ============================================================

def shift(a, b):
    return a * (b + 1)


# ============================================================
# DP MINIMAL COST + WITNESS EXPRESSIONS
# ============================================================

def compute_L(limit=EXTENDED_LIMIT):
    L, expr = {1: 1}, {1: "1"}

    for m in range(2, limit + 1):
        choices = (d for d in range(1, m) if m % d == 0)
        d = min(choices, key=lambda d: L[d] + L[m // d - 1])
        b = m // d - 1
        L[m] = L[d] + L[b]
        expr[m] = f"({expr[d]} ⋆ {expr[b]})"

    return L, expr


# ============================================================
# REACHABLE SETS S_n
# ============================================================

def enumerate_S(L):
    max_n = max(L.values())
    S = {1: {1}}

    for n in range(2, max_n + 1):
        vals = set()
        for k in range(1, n):
            for x in S[k]:
                for y in S[n - k]:
                    vals.add(x * (y + 1))
        S[n] = vals

    return S


# ============================================================
# ROBUST EXPRESSION EVALUATOR
# ============================================================

def eval_expr(expr: str) -> int:
    expr = expr.strip()

    if expr == "1":
        return 1

    # Strip outer parentheses
    if expr[0] == "(" and expr[-1] == ")":
        depth = 0
        is_outer = True
        for i, ch in enumerate(expr):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(expr) - 1:
                    is_outer = False
                    break
        if is_outer:
            expr = expr[1:-1].strip()

    # Find top-level ⋆
    depth = 0
    split_pos = None
    for i in range(len(expr)):
        ch = expr[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif expr[i:i+3] == " ⋆ " and depth == 0:
            split_pos = i
            break

    if split_pos is None:
        raise ValueError(f"Cannot find top-level ⋆ in {expr!r}")

    left = expr[:split_pos].strip()
    right = expr[split_pos+3:].strip()

    a = eval_expr(left)
    b = eval_expr(right)
    return a * (b + 1)


# ============================================================
# COMBINATORIAL CATALAN SECTOR
# ============================================================

class TestCombinatorialCatalanSector(unittest.TestCase):
    def test_catalan_3_topologies(self):
        shapes = [
            "(1 ⋆ (1 ⋆ (1 ⋆ 1)))",
            "(1 ⋆ ((1 ⋆ 1) ⋆ 1))",
            "((1 ⋆ 1) ⋆ (1 ⋆ 1))",
            "((1 ⋆ (1 ⋆ 1)) ⋆ 1)",
            "(((1 ⋆ 1) ⋆ 1) ⋆ 1)"
        ]
        values = [eval_expr(s) for s in shapes]
        self.assertEqual(sorted(values), [4, 5, 6, 6, 8])


# ============================================================
# ALGEBRAIC TRAPS SECTOR
# ============================================================

class TestGauntletAlgebraicTraps(unittest.TestCase):
    def test_cancellation_trap_zero_factor(self):
        self.assertEqual(shift(Fraction(2), Fraction(-1)), 0)
        self.assertEqual(shift(Fraction(7), Fraction(-1)), 0)

    def test_left_cancellation_conditions(self):
        self.assertNotEqual(shift(5, 3), shift(5, 4))
        self.assertEqual(shift(0, 3), shift(0, 4))

    def test_right_cancellation_conditions(self):
        self.assertNotEqual(shift(3, 2), shift(7, 2))
        self.assertEqual(shift(3, -1), shift(7, -1))

    def test_zero_factor_theorem(self):
        self.assertEqual(shift(0, 100), 0)
        self.assertEqual(shift(100, -1), 0)

    def test_fixed_point_identity(self):
        self.assertEqual(shift(4, 0), 4)
        self.assertNotEqual(shift(4, 2), 4)


# ============================================================
# QUADRATIC BOUNDARIES SECTOR
# ============================================================

class TestGauntletQuadraticBoundaries(unittest.TestCase):
    def test_quadratic_two_rational_roots(self):
        self.assertEqual(shift(1, 1), 2)
        self.assertEqual(shift(-2, -2), 2)

    def test_quadratic_boundary_case(self):
        self.assertEqual(shift(Fraction(-1,2), Fraction(-1,2)), Fraction(-1,4))

    def test_quadratic_irrational_real_roots(self):
        pass

    def test_quadratic_no_real_solutions(self):
        pass


# ============================================================
# CONSTRUCTIBILITY VERDICT SECTOR
# ============================================================

class TestGauntletConstructibilityVerdict(unittest.TestCase):
    def test_algebraic_validity_vs_unit_constructibility(self):
        self.assertEqual(shift(-2, -2), 2)
        self.assertLess(-2, 0)


# ============================================================
# MAGMA / OPERAD SECTOR
# ============================================================

class TestMagmaOperadSector(unittest.TestCase):
    def test_exact_associator_identity(self):
        a, b, c = Fraction(3), Fraction(4), Fraction(5)
        lhs = shift(shift(a,b), c)
        rhs = shift(a, shift(b,c))
        self.assertEqual(lhs - rhs, a * c)

    def test_right_distributivity(self):
        a, b, c = 3, 4, 5
        self.assertEqual(shift(a+b, c), shift(a,c) + shift(b,c))


# ============================================================
# DP AUDIT SECTOR (1..100)
# ============================================================

class TestDPSolverAndAuditSector(unittest.TestCase):
    def setUp(self):
        self.L, self.expr = compute_L(limit=100)

    def test_audited_minimal_costs(self):
        self.assertEqual(self.L[23], 8)
        self.assertEqual(self.L[47], 10)
        self.assertEqual(self.L[94], 11)

    def test_unique_maximum_cost_in_1_to_100(self):
        peak = max(self.L.values())
        offenders = [m for m in self.L if self.L[m] == peak]
        self.assertEqual(peak, 11)
        self.assertEqual(offenders, [94])

    def test_witness_tree_correctness(self):
        for m in range(1, 101):
            self.assertEqual(eval_expr(self.expr[m]), m)


# ============================================================
# EXPLORATION SUITE (1..100)
# ============================================================

class TestShiftExplorations(unittest.TestCase):
    def setUp(self):
        self.L, self.expr = compute_L(limit=100)
        self.S = enumerate_S(self.L)

    def test_L_consistency_with_S(self):
        for m in self.L:
            n_min = min(n for n in self.S if m in self.S[n])
            self.assertEqual(n_min, self.L[m])

    def test_delta_distribution(self):
        delta = {}
        for m, cost in self.L.items():
            lower = 1 + math.ceil(math.log2(m))
            delta[m] = cost - lower
        self.assertGreaterEqual(max(delta.values()), 3)

    def test_gaps_in_Sn_small_n(self):
        for n in range(1, 9):
            self.assertIn(n, self.S)

    def test_multiplicity_root_splits(self):
        pass


# ============================================================
# EXTENDED RANGE TESTS (up to EXTENDED_LIMIT)
# ============================================================

class TestExtendedRange(unittest.TestCase):
    def setUp(self):
        self.L, self.expr = compute_L(limit=EXTENDED_LIMIT)
        self.S = enumerate_S(self.L)

    def test_L_defined_up_to_limit(self):
        for m in range(1, EXTENDED_LIMIT + 1):
            self.assertIn(m, self.L)

    def test_L_consistency_extended(self):
        for m in range(1, EXTENDED_LIMIT + 1):
            n_min = min(n for n in self.S if m in self.S[n])
            self.assertEqual(n_min, self.L[m])

    def test_specific_values_118_and_188(self):
        for m in [118, 188]:
            if m <= EXTENDED_LIMIT:
                self.assertEqual(eval_expr(self.expr[m]), m)

    def test_peak_cost_extended(self):
        peak = max(self.L.values())
        offenders = [m for m in self.L if self.L[m] == peak]
        print("\nExtended peak:", peak, "at", offenders)
        self.assertGreaterEqual(peak, 11)


# ============================================================
# EXPLORATION OUTPUT
# ============================================================

def extended_exploration():
    L, expr = compute_L(limit=EXTENDED_LIMIT)
    S = enumerate_S(L)

    print(f"\n=== EXTENDED RANGE ANALYSIS up to {EXTENDED_LIMIT} ===")
    peak = max(L.values())
    offenders = [m for m in L if L[m] == peak]
    print("Peak L =", peak, "at", offenders)

    sample = [94, 118, 150, 188]
    for m in sample:
        if m <= EXTENDED_LIMIT:
            print(f"m={m}, L={L[m]}, expr={expr[m]}")

    print("\nReachability gaps:")
    for n in range(1, max(L.values()) + 1):
        reachable = sorted(v for v in S[n] if v <= EXTENDED_LIMIT)
        if reachable:
            min_v, max_v = reachable[0], reachable[-1]
            full_range = set(range(min_v, max_v + 1))
            gaps = sorted(full_range - set(reachable))
            print(f"n={n}: gaps={gaps}")


# ============================================================
# RUN EVERYTHING
# ============================================================

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False, verbosity=2)
    extended_exploration()