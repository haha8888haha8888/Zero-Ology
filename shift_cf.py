
"""
Shift Arithmetic Multi-Sector Verification & Dynamic Solver Suite
Core Operator: a * b = a * (b + 1)
Associator:   (a * b) * c - a * (b * c) = a * c
Companion:    b (+) c = b + c + b * c = (1 + b)(1 + c) - 1
"""

import math
import unittest
from fractions import Fraction
from typing import Dict, Optional, Set


# =====================================================================
# CORE ALGEBRAIC DEFINITIONS (EXACT RATIONAL ARITHMETIC)
# =====================================================================

def shift(a: Fraction, b: Fraction) -> Fraction:
    """Core binary shift operation: a * b = a(b + 1)"""
    return a * (b + 1)

def companion_oplus(b: Fraction, c: Fraction) -> Fraction:
    """Companion composition law: b (+) c = b + c + bc = (1 + b)(1 + c) - 1"""
    return b + c + (b * c)

def shift_associator(a: Fraction, b: Fraction, c: Fraction) -> Fraction:
    """Exact associator gap: (a * b) * c - a * (b * c)"""
    left_assoc = shift(shift(a, b), c)
    right_assoc = shift(a, shift(b, c))
    return left_assoc - right_assoc


# =====================================================================
# EXPRESSION TREE & DYNAMIC PROGRAMMING SOLVER
# =====================================================================

class Node:
    """Binary expression tree node for exact evaluation and auditing."""
    def __init__(
        self, 
        val: Optional[Fraction] = None, 
        left: Optional['Node'] = None, 
        right: Optional['Node'] = None
    ):
        self.val = val
        self.left = left
        self.right = right

    def evaluate(self) -> Fraction:
        if self.left is None and self.right is None:
            return self.val
        return shift(self.left.evaluate(), self.right.evaluate())

    def leaf_count(self) -> int:
        if self.left is None and self.right is None:
            return 1
        return self.left.leaf_count() + self.right.leaf_count()


class DPSolver:
    """
    Dynamic programming reachable-set engine.
    Computes S_n (set of reachable integer values at leaf count n)
    and constructs witness trees for exact verification.
    """
    def __init__(self, max_leaves: int):
        self.max_leaves = max_leaves
        # S[n] maps integer_value -> witness Node
        self.S: Dict[int, Dict[int, Node]] = {i: {} for i in range(1, max_leaves + 1)}
        self._build_reachable_sets()

    def _build_reachable_sets(self):
        self.S[1][1] = Node(val=Fraction(1, 1))
        
        for n in range(2, self.max_leaves + 1):
            for k in range(1, n):
                for val_l, node_l in self.S[k].items():
                    for val_r, node_r in self.S[n - k].items():
                        val = val_l * (val_r + 1)
                        if val not in self.S[n]:
                            self.S[n][val] = Node(left=node_l, right=node_r)

    def get_minimal_cost(self, m: int) -> Optional[int]:
        for n in range(1, self.max_leaves + 1):
            if m in self.S[n]:
                return n
        return None

    def get_witness(self, m: int) -> Optional[Node]:
        for n in range(1, self.max_leaves + 1):
            if m in self.S[n]:
                return self.S[n][m]
        return None


# =====================================================================
# SECTOR 1: EXACT MAGMA & OPERAD ALGEBRA
# =====================================================================

class TestMagmaOperadSector(unittest.TestCase):
    def test_exact_associator_identity(self):
        """Verify (a * b) * c - a * (b * c) == a * c using exact Fraction arithmetic."""
        test_triplets = [
            (Fraction(2), Fraction(3), Fraction(4)),
            (Fraction(-3, 2), Fraction(1, 2), Fraction(8)),
            (Fraction(10), Fraction(10), Fraction(10)),
            (Fraction(1, 10), Fraction(2, 10), Fraction(3, 10))
        ]
        for a, b, c in test_triplets:
            gap = shift_associator(a, b, c)
            expected = a * c
            self.assertEqual(gap, expected)

    def test_right_distributivity(self):
        """Verify (a + b) * c = (a * c) + (b * c) exactly."""
        a, b, c = Fraction(3), Fraction(5), Fraction(4)
        left_side = shift(a + b, c)
        right_side = shift(a, c) + shift(b, c)
        self.assertEqual(left_side, right_side)


# =====================================================================
# SECTOR 2: COMBINATORICS & CATALAN TREE TOPOLOGIES
# =====================================================================

class TestCombinatorialCatalanSector(unittest.TestCase):
    def test_catalan_3_topologies(self):
        """
        Evaluate all C_3 = 5 Catalan tree topologies for 4 leaves (all val=1).
        Exact values:
        T1: (((1*1)*1)*1) = 8
        T2: ((1*(1*1))*1) = 6
        T3: ((1*1)*(1*1)) = 6
        T4: (1*((1*1)*1)) = 5
        T5: (1*(1*(1*1))) = 4
        """
        leaf = lambda: Node(val=Fraction(1, 1))
        
        t1 = Node(left=Node(left=Node(left=leaf(), right=leaf()), right=leaf()), right=leaf())
        t2 = Node(left=Node(left=leaf(), right=Node(left=leaf(), right=leaf())), right=leaf())
        t3 = Node(left=Node(left=leaf(), right=leaf()), right=Node(left=leaf(), right=leaf()))
        t4 = Node(left=leaf(), right=Node(left=Node(left=leaf(), right=leaf()), right=leaf()))
        t5 = Node(left=leaf(), right=Node(left=leaf(), right=Node(left=leaf(), right=leaf())))

        results = {
            "T1_left_comb": int(t1.evaluate()),
            "T2": int(t2.evaluate()),
            "T3_balanced": int(t3.evaluate()),
            "T4": int(t4.evaluate()),
            "T5_right_comb": int(t5.evaluate()),
        }

        self.assertEqual(results, {
            "T1_left_comb": 8,
            "T2": 6,
            "T3_balanced": 6,
            "T4": 5,
            "T5_right_comb": 4,
        })


# =====================================================================
# SECTOR 3: DYNAMIC PROGRAMMING AUDIT & REACHABLE SET CROSS-CHECK
# =====================================================================

class TestDPSolverAndAuditSector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate reachable sets up to max_leaves = 11 to audit range 1..100
        cls.solver = DPSolver(max_leaves=11)

    def test_audited_minimal_costs(self):
        """Verify computed L(m) matches audited values for key integers."""
        expected_costs = {
            1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 4, 8: 4,
            22: 7, 23: 8, 47: 10, 94: 11, 95: 10
        }
        for m, expected_L in expected_costs.items():
            computed_L = self.solver.get_minimal_cost(m)
            self.assertEqual(
                computed_L, expected_L, 
                f"Mismatch at m={m}: expected L({m})={expected_L}, got {computed_L}"
            )

    def test_witness_tree_correctness(self):
        """Verify witness trees evaluate to m and match computed leaf count L(m)."""
        for m in range(1, 101):
            witness = self.solver.get_witness(m)
            self.assertIsNotNone(witness, f"Missing witness tree for m={m}")
            self.assertEqual(int(witness.evaluate()), m)
            self.assertEqual(witness.leaf_count(), self.solver.get_minimal_cost(m))

    def test_unique_maximum_cost_in_1_to_100(self):
        """Programmatically prove m=94 is the unique peak with L(94)=11 across 1..100."""
        costs_1_to_100 = {m: self.solver.get_minimal_cost(m) for m in range(1, 101)}
        max_cost = max(costs_1_to_100.values())
        peaks = [m for m, cost in costs_1_to_100.items() if cost == max_cost]

        self.assertEqual(max_cost, 11)
        self.assertEqual(peaks, [94])
        self.assertGreater(costs_1_to_100[94], costs_1_to_100[95])


if __name__ == "__main__":
    # argv=[''] prevents unittest from parsing IPython/Jupyter kernel flags
    # exit=False prevents SystemExit exceptions inside interactive notebooks
    unittest.main(argv=[''], exit=False, verbosity=2)