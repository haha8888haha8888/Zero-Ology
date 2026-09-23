#!/usr/bin/env python3
"""SHIFT ARITHMETIC FINAL EXAMINATION v7 — S. Szmy.

COMPLETE REPLACEMENT: Python 3.10+, standard library only.
Paste the entire file into Colab and run. A real input menu appears.
Choose a number range from 50,000 through 1,000,000, then a test group.
Enter accepts defaults. Bad input is explained and requested again.
Enter q to cancel. End-of-input cancels rather than silently starting a run.

All 61 v4 mathematical tests remain, plus 9 menu/control tests (70 total).
Menu groups: complete; number sweep; angle/triangle/trig; algebra only.
Only number-sweep groups build large arrays. No old notebook tests are loaded.
The number sweep is built once, shared by its tests, and reports progress.
Compact arrays reduce million-target memory; optimal tree counts remain
arbitrary-precision Python integers. No dependencies or earlier files needed.

Optional terminal commands (not required in Colab):
  python shift_final_examination_v7.py
  python shift_final_examination_v7.py --no-menu
  python shift_final_examination_v7.py --number-limit 1000000 --tests all
  python shift_final_examination_v7.py --tests geometry --angle-limit 360
  python shift_final_examination_v7.py --menu

NUMBER: a ⋆ b = a(b+1), non-associative, associator ac.
ANGLE: A ⋆ B = A+B+1°, associative; a separate model.
Unit angle seeds yield S_n={2n−1}; seeds (1,2) yield {2n−1,...,3n−1}.
Algebra/DP checks are exact; trig checks are numerical to stated tolerance.
Construction here means expression trees, not straightedge-and-compass.
The large reachability calculation uses divisor recurrence; independent
leaf-split and Catalan checks cover small cases, not the whole million.
Gap rows explicitly indicate value truncation. No historical novelty claim.
All output stays in the console; no files are written by the suite.
"""
import argparse
import math
import re
import sys
import unittest
from collections import Counter
from array import array
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from typing import Dict, Optional, Tuple

MAX_LIMIT = 1000


def bounded_int(value, name, minimum=1, maximum=MAX_LIMIT):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError('{} must be an integer from {} to {}'.format(name, minimum, maximum))
    return value


def exact_degrees(value):
    """Accept integers/Fractions only: callers explicitly choose exact input."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError('Use an integer or Fraction for exact degrees.')
    return Fraction(value)


def angle_shift(A, B):
    return exact_degrees(A) + exact_degrees(B) + 1


def normalize_bases(bases):
    result = tuple(sorted(set(bounded_int(v, 'base angle') for v in bases)))
    if not result:
        raise ValueError('At least one positive integer base angle is required.')
    return result


@dataclass(frozen=True)
class AngleNode:
    value: Optional[int] = None
    left: Optional['AngleNode'] = None
    right: Optional['AngleNode'] = None

    def __post_init__(self):
        if self.value is not None:
            bounded_int(self.value, 'leaf angle')
            if self.left is not None or self.right is not None:
                raise ValueError('A leaf cannot also have children.')
        elif not isinstance(self.left, AngleNode) or not isinstance(self.right, AngleNode):
            raise ValueError('An internal node requires two AngleNode children.')

    def evaluate(self):
        if self.value is not None:
            return Fraction(self.value)
        return angle_shift(self.left.evaluate(), self.right.evaluate())

    def leaf_count(self):
        if self.value is not None:
            return 1
        return self.left.leaf_count() + self.right.leaf_count()

    def expression(self):
        if self.value is not None:
            return '{}°'.format(self.value)
        return '({} ⋆ {})'.format(self.left.expression(), self.right.expression())


class AngleSolver:
    """Target-indexed DP. Strictly smaller positive children ensure completeness.

    Every allowed leaf costs 1. For each A, test every positive decomposition
    A=X+Y+1 whose two child costs are finite. Store one optimal witness.
    This is O(limit²) in loop count. Unreachable targets have no witness.
    Balance tie-breaks keep witness depth small; repeated subtrees are counted
    per occurrence even if immutable Python nodes share storage.
    """
    def __init__(self, limit=180, bases=(1,)):
        self.limit = bounded_int(limit, 'limit')
        self.bases = normalize_bases(bases)
        self.costs: Dict[int, Optional[int]] = {}
        self.nodes: Dict[int, Optional[AngleNode]] = {}
        for A in range(1, self.limit + 1):
            best = (1, 0) if A in self.bases else None
            node = AngleNode(value=A) if best else None
            for X in range(1, (A - 1) // 2 + 1):
                Y = A - X - 1
                cx, cy = self.costs[X], self.costs[Y]
                if cx is None or cy is None:
                    continue
                candidate = (cx + cy, abs(X - Y))
                if best is None or candidate < best:
                    best = candidate
                    node = AngleNode(left=self.nodes[X], right=self.nodes[Y])
            self.costs[A] = best[0] if best is not None else None
            self.nodes[A] = node

    def cost(self, angle):
        bounded_int(angle, 'target angle', maximum=self.limit)
        return self.costs[angle]

    def witness(self, angle):
        bounded_int(angle, 'target angle', maximum=self.limit)
        return self.nodes[angle]


def compute_angle_cost(limit=180, bases=(1,)):
    """Compatibility interface: cost and expression dictionaries, with None gaps."""
    solver = AngleSolver(limit, bases)
    return solver.costs, {a: n.expression() if n else None for a, n in solver.nodes.items()}


def enumerate_angle_sets(max_leaves, bases=(1,), max_angle=None):
    """Independent leaf-indexed recurrence. At most 16 leaves for this audit.

    If max_angle is set, values above it are pruned; positive children always
    give larger parents, so pruning cannot remove an in-range construction.
    """
    bounded_int(max_leaves, 'enumeration leaf budget', maximum=16)
    bases = normalize_bases(bases)
    if max_angle is not None:
        bounded_int(max_angle, 'maximum angle')
    S = {1: {b for b in bases if max_angle is None or b <= max_angle}}
    for n in range(2, max_leaves + 1):
        vals = set()
        for k in range(1, n):
            for A in S[k]:
                for B in S[n-k]:
                    value = A + B + 1
                    if max_angle is None or value <= max_angle:
                        vals.add(value)
        S[n] = vals
    return S


@lru_cache(maxsize=None)
def catalan_trees(leaves):
    """All ordered full binary tree shapes, with unit leaves; bounded output."""
    bounded_int(leaves, 'Catalan leaves', maximum=8)
    if leaves == 1:
        return (AngleNode(value=1),)
    return tuple(AngleNode(left=l, right=r)
                 for k in range(1, leaves)
                 for l in catalan_trees(k) for r in catalan_trees(leaves-k))


def eval_angle_expr(expression, bases=(1,)):
    """Parse only 'leaf°' or '(expression ⋆ expression)'; no Python eval.

    An explicit stack avoids recursion-depth failure on long comb expressions.
    Returns (exact degree value, leaf count); rejects incomplete/extra tokens.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError('Expected a nonempty witness expression.')
    if len(expression) > 50000:
        raise ValueError('Expression exceeds this audit parser’s size limit.')
    allowed = normalize_bases(bases)
    pattern = re.compile(r'\s*(\d+°|[()⋆])')
    tokens, pos = [], 0
    expression = expression.strip()
    while pos < len(expression):
        match = pattern.match(expression, pos)
        if not match:
            raise ValueError('Invalid expression token at position {}'.format(pos))
        tokens.append(match.group(1))
        pos = match.end()
    stack = []
    for token in tokens:
        if token.endswith('°'):
            value = int(token[:-1])
            if value not in allowed:
                raise ValueError('Leaf is not in the allowed seed set.')
            stack.append((Fraction(value), 1))
        elif token != ')':
            stack.append(token)
        else:
            if (len(stack) < 4 or stack[-4] != '(' or stack[-2] != '⋆'
                    or not isinstance(stack[-3], tuple) or not isinstance(stack[-1], tuple)):
                raise ValueError('Malformed binary expression.')
            left, right = stack[-3], stack[-1]
            stack[-4:] = [(angle_shift(left[0], right[0]), left[1]+right[1])]
    if len(stack) != 1 or not isinstance(stack[0], tuple):
        raise ValueError('Incomplete expression or trailing tokens.')
    return stack[0]


def valid_triangle(A, B, C):
    angles = tuple(exact_degrees(v) for v in (A, B, C))
    return all(0 < a < 180 for a in angles) and sum(angles) == 180


def triangle_kind(A, B, C):
    if not valid_triangle(A, B, C):
        return None
    largest = max(A, B, C)
    return 'right' if largest == 90 else 'obtuse' if largest > 90 else 'acute'


def triangle_constructibility(A, B, C, solver):
    if not valid_triangle(A, B, C):
        return {'geometric': False, 'status': 'invalid triangle', 'leaf_cost': None}
    angles = tuple(exact_degrees(v) for v in (A, B, C))
    # Seeds and increment are integers: fractional values are globally excluded.
    if any(a.denominator != 1 for a in angles):
        return {'geometric': True, 'status': 'unreachable in integer-seed model', 'leaf_cost': None}
    if any(a > solver.limit for a in angles):
        return {'geometric': True, 'status': 'outside computed range', 'leaf_cost': None}
    costs = [solver.cost(int(a)) for a in angles]
    if any(c is None for c in costs):
        return {'geometric': True, 'status': 'unreachable in selected model', 'leaf_cost': None}
    return {'geometric': True, 'status': 'reachable', 'leaf_cost': sum(costs)}


def enumerate_triangles(solver):
    """Unordered positive integer angle triples A<=B<=C summing to 180.

    All three components must be within solver.limit and reachable there.
    This is a complete integer-angle census when solver.limit >= 178.
    """
    triangles = []
    for A in range(1, min(60, solver.limit)+1):
        if solver.cost(A) is None:
            continue
        for B in range(A, min((180-A)//2, solver.limit)+1):
            C = 180-A-B
            if C > solver.limit or C < B:
                continue
            if solver.cost(B) is not None and solver.cost(C) is not None:
                triangles.append((A, B, C))
    return triangles


def trig_degrees(angle):
    """Exact degree normalization/pole classification, then numerical trig.

    Exact quadrantal cases avoid tiny numerical residues at 0°,90°,180°,270°.
    Other sin/cos/tan results are floats; tan=None at mathematical poles.
    """
    a = exact_degrees(angle) % 360
    quadrants = {0: (0.0, 1.0), 90: (1.0, 0.0),
                 180: (0.0, -1.0), 270: (-1.0, 0.0)}
    if a in quadrants:
        sine, cosine = quadrants[a]
    else:
        radians = math.radians(float(a))
        sine, cosine = math.sin(radians), math.cos(radians)
    pole = a % 180 == 90
    if not pole and cosine == 0.0:
        raise ArithmeticError('Numerical cosine underflow near a tangent pole.')
    return {'degrees_mod_360': a, 'sin': sine, 'cos': cosine,
            'tan': None if pole else sine/cosine, 'tan_defined': not pole}


def trig_shift_residuals(A, B):
    """Check sin/cos of A+B+1° using ordinary addition identities twice."""
    a, b, step = trig_degrees(A), trig_degrees(B), trig_degrees(1)
    sin_sum = a['sin']*b['cos'] + a['cos']*b['sin']
    cos_sum = a['cos']*b['cos'] - a['sin']*b['sin']
    predicted_sin = sin_sum*step['cos'] + cos_sum*step['sin']
    predicted_cos = cos_sum*step['cos'] - sin_sum*step['sin']
    actual = trig_degrees(angle_shift(A, B))
    return actual['sin']-predicted_sin, actual['cos']-predicted_cos


class TestAngleAlgebra(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(angle_shift(30, 60), 91)
        self.assertEqual(angle_shift(1, 1), 3)

    def test_associativity_and_commutativity(self):
        for a, b, c in [(1, 2, 3), (-2, 0, 8), (Fraction(1, 2), 3, -1)]:
            self.assertEqual(angle_shift(a, b), angle_shift(b, a))
            self.assertEqual(angle_shift(angle_shift(a, b), c), angle_shift(a, angle_shift(b, c)))

    def test_identity_and_cancellation(self):
        for a in [-5, 0, 1, Fraction(3, 2)]:
            self.assertEqual(angle_shift(a, -1), a)
            self.assertEqual(angle_shift(-1, a), a)
            self.assertEqual(angle_shift(a, 4)-angle_shift(a, 9), -5)

    def test_shifted_addition(self):
        for a, b in [(1, 1), (30, 60), (-2, Fraction(1, 3))]:
            self.assertEqual(angle_shift(a, b)+1, (a+1)+(b+1))

    def test_strict_input(self):
        with self.assertRaises(TypeError):
            angle_shift(1.5, 2)


class TestAngleDP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = AngleSolver(1000)

    def test_all_costs_against_closed_form(self):
        for a in range(1, 1001):
            self.assertEqual(self.solver.cost(a), (a+1)//2 if a % 2 else None)

    def test_all_witnesses_exactly(self):
        for a in range(1, 1001):
            n = self.solver.witness(a)
            if a % 2:
                self.assertEqual(n.evaluate(), Fraction(a))
                self.assertEqual(n.leaf_count(), self.solver.cost(a))
            else:
                self.assertIsNone(n)

    def test_expression_round_trip(self):
        for a in [1, 3, 45, 179, 999]:
            expr = self.solver.witness(a).expression()
            self.assertEqual(eval_angle_expr(expr), (Fraction(a), (a+1)//2))

    def test_invalid_expressions(self):
        for expr in ['', '2°', '(1° ⋆)', '1° ⋆ 1°', '(1° ⋆ 1°))', '1° 1°', '__import__("os")']:
            with self.subTest(expr=expr), self.assertRaises(ValueError):
                eval_angle_expr(expr)

    def test_bad_inputs(self):
        for limit in [0, -1, 1001, 2.5, True]:
            with self.assertRaises(ValueError):
                AngleSolver(limit)
        for bases in [(), (0,), (-1,), (1.5,)]:
            with self.assertRaises(ValueError):
                AngleSolver(20, bases)
        with self.assertRaises(ValueError):
            self.solver.cost(0)
        with self.assertRaises(ValueError):
            AngleNode()

    def test_independent_reachable_sets(self):
        for bases in [(1,), (1, 2), (2,)]:
            S = enumerate_angle_sets(10, bases)
            solver = AngleSolver(max(max(v) for v in S.values()), bases)
            for n, vals in S.items():
                for a in vals:
                    first = min(k for k in S if a in S[k])
                    self.assertEqual(solver.cost(a), first)
                    self.assertLessEqual(solver.cost(a), n)

    def test_exact_strict_sets(self):
        self.assertEqual(enumerate_angle_sets(8), {n: {2*n-1} for n in range(1, 9)})

    def test_pruned_sets(self):
        full = enumerate_angle_sets(8, (1, 2))
        pruned = enumerate_angle_sets(8, (1, 2), max_angle=12)
        self.assertEqual(pruned, {n: {v for v in vals if v <= 12} for n, vals in full.items()})

    def test_small_and_optional_model(self):
        self.assertEqual(compute_angle_cost(1), ({1: 1}, {1: '1°'}))
        solver = AngleSolver(180, (1, 2))
        self.assertEqual(solver.cost(2), 1)
        for a in range(1, 181):
            self.assertIsNotNone(solver.cost(a))
            self.assertEqual(eval_angle_expr(solver.witness(a).expression(), (1, 2)),
                             (Fraction(a), solver.cost(a)))


class TestCatalanAngles(unittest.TestCase):
    def test_five_shapes_one_value(self):
        trees = catalan_trees(4)
        self.assertEqual(len(trees), 5)
        self.assertEqual(len({t.expression() for t in trees}), 5)
        self.assertEqual({t.evaluate() for t in trees}, {Fraction(7)})

    def test_catalan_counts_and_leaf_invariant(self):
        for n in range(1, 8):
            trees = catalan_trees(n)
            self.assertEqual(len(trees), math.comb(2*(n-1), n-1)//n)
            for t in trees:
                self.assertEqual(t.leaf_count(), n)
                self.assertEqual(t.evaluate(), 2*n-1)


class TestTriangleGauntlet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strict = AngleSolver(180)
        cls.extended = AngleSolver(180, (1, 2))

    def test_standard_triangles(self):
        for angles in [(60, 60, 60), (30, 60, 90), (45, 45, 90), (1, 1, 178)]:
            self.assertTrue(valid_triangle(*angles))

    def test_invalid_triangles(self):
        for angles in [(0, 90, 90), (-1, 90, 91), (60, 60, 61), (180, 0, 0)]:
            self.assertFalse(valid_triangle(*angles))
            self.assertEqual(triangle_constructibility(*angles, self.strict)['status'], 'invalid triangle')

    def test_exact_fractional_triangle(self):
        angles = (Fraction(1, 2), Fraction(179, 2), 90)
        self.assertTrue(valid_triangle(*angles))
        self.assertIn('unreachable', triangle_constructibility(*angles, self.extended)['status'])

    def test_angle_classification(self):
        self.assertEqual(triangle_kind(60, 60, 60), 'acute')
        self.assertEqual(triangle_kind(45, 45, 90), 'right')
        self.assertEqual(triangle_kind(20, 30, 130), 'obtuse')
        self.assertIsNone(triangle_kind(0, 0, 180))

    def test_strict_parity_obstruction(self):
        self.assertEqual(enumerate_triangles(self.strict), [])
        self.assertEqual(triangle_constructibility(45, 45, 90, self.strict)['status'],
                         'unreachable in selected model')

    def test_optional_model_triangles(self):
        triples = enumerate_triangles(self.extended)
        self.assertIn((30, 60, 90), triples)
        self.assertIn((60, 60, 60), triples)
        self.assertEqual(len(triples), len(set(triples)))
        for triple in triples:
            self.assertTrue(valid_triangle(*triple))
            self.assertEqual(triangle_constructibility(*triple, self.extended)['status'], 'reachable')

    def test_triangle_leaf_cost(self):
        result = triangle_constructibility(30, 60, 90, self.extended)
        expected = sum(self.extended.witness(a).leaf_count() for a in (30, 60, 90))
        self.assertEqual(result['leaf_cost'], expected)

    def test_outside_range(self):
        self.assertEqual(triangle_constructibility(60, 60, 60, AngleSolver(10))['status'],
                         'outside computed range')


class TestTrigGauntlet(unittest.TestCase):
    def test_quadrantal_values(self):
        self.assertEqual(trig_degrees(0)['sin'], 0)
        self.assertEqual(trig_degrees(90)['cos'], 0)
        self.assertEqual(trig_degrees(180)['cos'], -1)
        self.assertEqual(trig_degrees(270)['sin'], -1)

    def test_known_numerical_values(self):
        self.assertAlmostEqual(trig_degrees(30)['sin'], 0.5, places=12)
        self.assertAlmostEqual(trig_degrees(60)['cos'], 0.5, places=12)
        self.assertAlmostEqual(trig_degrees(45)['tan'], 1, places=12)

    def test_tangent_poles_and_near_pole(self):
        for a in [90, 270, -90, 450]:
            self.assertIsNone(trig_degrees(a)['tan'])
            self.assertFalse(trig_degrees(a)['tan_defined'])
        near = trig_degrees(Fraction(89999, 1000))
        self.assertTrue(near['tan_defined'])
        self.assertTrue(math.isfinite(near['tan']))

    def test_periodicity_without_constructibility_wrap(self):
        self.assertEqual(trig_degrees(-30), trig_degrees(330))
        self.assertEqual(trig_degrees(10**20 * 360 + 30), trig_degrees(30))
        solver = AngleSolver(361)
        self.assertEqual(solver.cost(1), 1)
        self.assertEqual(solver.cost(361), 181)
        self.assertEqual(trig_degrees(1), trig_degrees(361))

    def test_pythagorean_identity_numerically(self):
        for a in range(-360, 721, 7):
            t = trig_degrees(a)
            self.assertAlmostEqual(t['sin']**2+t['cos']**2, 1, places=12)

    def test_shift_addition_identities_numerically(self):
        for A, B in [(30, 60), (45, 44), (-90, 270), (Fraction(1, 2), Fraction(3, 4))]:
            for residual in trig_shift_residuals(A, B):
                self.assertAlmostEqual(residual, 0, places=12)

    def test_triangle_cosine_identity_numerically(self):
        # For A+B+C=180°: cos²A+cos²B+cos²C+2cosA cosB cosC = 1.
        for angles in [(60, 60, 60), (30, 60, 90), (20, 30, 130)]:
            a, b, c = [trig_degrees(x)['cos'] for x in angles]
            self.assertAlmostEqual(a*a+b*b+c*c+2*a*b*c, 1, places=12)

    def test_equal_sines_are_not_equal_angles(self):
        self.assertAlmostEqual(trig_degrees(30)['sin'], trig_degrees(150)['sin'], places=12)
        self.assertNotEqual(30, 150)


class TestAutomaticModelComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extended = AngleSolver(1000, (1, 2))
        cls.triangles = enumerate_triangles(cls.extended)

    def test_extended_cost_closed_form_through_1000(self):
        # n leaves give 2n-1+k where k is the number of 2-degree leaves.
        # Thus 2n-1 <= A <= 3n-1, with every intermediate integer reachable.
        # For A>=1 the smallest feasible n is ceil((A+1)/3).
        for A in range(1, 1001):
            self.assertEqual(self.extended.cost(A), (A+3)//3)

    def test_extended_reachable_intervals(self):
        sets = enumerate_angle_sets(12, (1, 2))
        for n, values in sets.items():
            self.assertEqual(values, set(range(2*n-1, 3*n)))

    def test_complete_triangle_census(self):
        self.assertEqual(len(self.triangles), 2700)
        counts = Counter(triangle_kind(*t) for t in self.triangles)
        self.assertEqual(dict(counts), {'acute': 675, 'right': 45, 'obtuse': 1980})
        self.assertEqual(enumerate_triangles(AngleSolver(180)), [])

    def test_census_against_independent_ordered_enumeration(self):
        # Separate enumeration: scan all ordered positive integer A,B;
        # derive C and canonicalize. No solver costs or triangle helper used.
        reference = set()
        for A in range(1, 179):
            for B in range(1, 180-A):
                C = 180-A-B
                reference.add(tuple(sorted((A, B, C))))
        self.assertEqual(set(self.triangles), reference)


TEST_CLASSES = (TestAngleAlgebra, TestAngleDP, TestCatalanAngles,
                TestTriangleGauntlet, TestTrigGauntlet, TestAutomaticModelComparison)


def run_tests(verbosity=1):
    """Explicit class list prevents discovery of unrelated old notebook tests."""
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
                               for c in TEST_CLASSES)
    return unittest.TextTestRunner(verbosity=verbosity).run(suite)


def summarize(limit=180, bases=(1,), show_trig=True):
    solver = AngleSolver(limit, bases)
    reachable = [a for a, cost in solver.costs.items() if cost is not None]
    missing = [a for a, cost in solver.costs.items() if cost is None]
    print('\nANGLE / TRIANGLE / TRIG GAUNTLET — degrees, no construction wrapping')
    print('Seeds: {}; target range: 1..{}°'.format(solver.bases, limit))
    print('Reachable: {}; unreachable in this model: {}'.format(len(reachable), len(missing)))
    print('First unreachable targets:', missing[:12])
    if reachable:
        peak = max(solver.costs[a] for a in reachable)
        hardest = [a for a in reachable if solver.costs[a] == peak]
        print('Largest finite leaf cost: {}; targets (first 12): {}'.format(peak, hardest[:12]))
    else:
        print('No reachable targets in the selected range.')
    print('Witness samples (at most 100 characters each):')
    for a in (1, 2, 3, 30, 45, 60, 90, 179):
        if a > limit:
            continue
        node = solver.witness(a)
        expr = node.expression() if node else 'unreachable'
        if len(expr) > 100:
            expr = expr[:97]+'...'
        print('  {}°: L={}  {}'.format(a, solver.cost(a), expr))
    print('Reachable sets by leaf budget (first 6, unpruned):')
    for n, vals in enumerate_angle_sets(6, bases).items():
        ordered = sorted(vals)
        print('  S_{}: {} values; first 12 {}'.format(n, len(vals), ordered[:12]))
    strict = solver.bases == (1,)
    if strict:
        print('Strict model theorem: S_n={2n−1}; all even targets excluded.')
        print('Triangle theorem: three reachable angles are odd; their sum cannot be 180°.')
    triples = enumerate_triangles(solver)
    counts = Counter(triangle_kind(*t) for t in triples)
    print('Unordered reachable integer triangles within component range: {}'.format(len(triples)))
    print('Triangle types:', dict(sorted(counts.items())))
    for triple in ((30, 60, 90), (45, 45, 90), (60, 60, 60)):
        print('  {}: {}'.format(triple, triangle_constructibility(*triple, solver)))
    if show_trig:
        print('Trig samples: numerical values, independent of tree reachability')
        for a in (30, 45, 60, 90):
            t = trig_degrees(a)
            tangent = '{:.8g}'.format(t['tan']) if t['tan_defined'] else 'undefined (pole)'
            print('  {}°: sin={:.8g}, cos={:.8g}, tan={}'.format(a, t['sin'], t['cos'], tangent))
    print('This is expression constructibility, not a straightedge-and-compass test.')



# =====================================================================
# NUMBER MODEL — DISTINCT FROM THE ADDITIVE ANGLE MODEL
# =====================================================================
import time

NUMBER_MAX = 1_000_000


def number_shift(a, b):
    return a * (b + 1)


def companion_oplus(b, c):
    return b + c + b*c


def rational_self_shift_roots(t):
    """Explicit domain verdict plus exact rational roots of x(x+1)=t."""
    t = exact_degrees(t)  # Generic exact integer/Fraction validation.
    q = t + Fraction(1, 4)
    if q < 0:
        return 'no real roots', ()
    p, r = math.isqrt(q.numerator), math.isqrt(q.denominator)
    if p*p != q.numerator or r*r != q.denominator:
        return 'two irrational real roots', ()
    root = Fraction(p, r)
    roots = tuple(sorted({-Fraction(1, 2)-root, -Fraction(1, 2)+root}))
    return ('one rational real root' if len(roots) == 1 else 'two rational real roots'), roots


class SplitTable:
    """Compact witness storage: right child is determined by m and left child."""
    def __init__(self, size):
        self.left = array('I', [0])*size

    def __getitem__(self, m):
        a = self.left[m]
        return None if a == 0 else (a, m//a-1)

    def __setitem__(self, m, value):
        self.left[m] = value[0]


class NumberSweep:
    """Ascending divisor DP; exact integer costs, witnesses and multiplicities.

    For each m>1 every root decomposition is m=d*(e+1), d<m, e>=1.
    L(m)=min_d [L(d)+L(e)]. Both children are smaller than m.
    Smallest-prime-factor sieve supplies divisors without scanning 1..m.

    masks[m] has bit n iff an n-leaf expression for m exists, for n<=peak.
    Combine child masks by adding their leaf counts. Values above limit need
    never be stored: each positive child is strictly smaller than its parent.
    This is exact bounded reachability, not enumeration of unbounded S_n.
    Costs and masks use the same factorization structure; independent Catalan
    and leaf-split enumeration are used separately at small sizes.

    Optimal tree counts count ordered full expression trees, without reusing
    subexpressions for free. Root split count and tree count are different.
    """
    def __init__(self, limit=50000, progress=None):
        self.limit = bounded_int(limit, 'number limit', maximum=NUMBER_MAX)
        N = self.limit
        if progress:
            progress('Prime-factor sieve', 0, N)
        spf = array('I', range(N+1))
        for p in range(2, math.isqrt(N)+1):
            if spf[p] == p:
                for m in range(p*p, N+1, p):
                    if spf[m] == m:
                        spf[m] = p
        self.spf = spf
        self.L = bytearray(N+1)
        self.split = SplitTable(N+1)
        self.optimal_root_splits = array('I', [0])*(N+1)
        self.optimal_trees = [0]*(N+1)
        self.L[1] = 1
        self.optimal_trees[1] = 1
        report_step = max(1, N//5)
        if progress:
            progress('Costs and optimal trees', 0, N)
        for m in range(2, N+1):
            best, witness, roots, trees = m, None, 0, 0
            for d in self.proper_divisors(m):
                e = m//d-1
                cost = self.L[d]+self.L[e]
                if cost < best or witness is None:
                    best, witness = cost, (d, e)
                    roots, trees = 1, self.optimal_trees[d]*self.optimal_trees[e]
                elif cost == best:
                    roots += 1
                    trees += self.optimal_trees[d]*self.optimal_trees[e]
            self.L[m], self.split[m] = best, witness
            self.optimal_root_splits[m], self.optimal_trees[m] = roots, trees
            if progress and (m % report_step == 0 or m == N):
                progress('Costs and optimal trees', m, N)
        self.peak = max(self.L)
        # Binary doubling plus successor constructs m with <=2*floor(log2 m)+1
        # leaves. At N<=1,000,000 this is <=39, so 64-bit masks suffice.
        if self.peak >= 64:
            raise ArithmeticError('Leaf mask exceeds allocated exact width.')
        self.masks = array('Q', [0])*(N+1)
        self.masks[1] = 1 << 1
        cap = (1 << (self.peak+1))-1
        if progress:
            progress('Exact-leaf reachability', 0, N)
        for m in range(2, N+1):
            possible = 0
            for d in self.proper_divisors(m):
                e = m//d-1
                left, right = self.masks[d], self.masks[e]
                # Iterate set bits of the sparser mask; convolution is symmetric
                # in leaf counts, although the underlying operator is not.
                if left.bit_count() > right.bit_count():
                    left, right = right, left
                while left:
                    bit = left & -left
                    possible |= right << (bit.bit_length()-1)
                    left ^= bit
            self.masks[m] = possible & cap
            if progress and (m % report_step == 0 or m == N):
                progress('Exact-leaf reachability', m, N)

    def proper_divisors(self, m):
        remaining, divisors = m, [1]
        while remaining > 1:
            prime = self.spf[remaining]
            powers, power = [], 1
            while remaining % prime == 0:
                remaining //= prime
                power *= prime
                powers.append(power)
            previous = divisors[:]
            divisors.extend(d*p for p in powers for d in previous)
        return sorted(d for d in divisors if d < m)

    def expression(self, m):
        bounded_int(m, 'number target', maximum=self.limit)
        if m == 1:
            return '1'
        a, b = self.split[m]
        return '({} ⋆ {})'.format(self.expression(a), self.expression(b))

    def reachable(self, m, n):
        bounded_int(m, 'number target', maximum=self.limit)
        bounded_int(n, 'leaf count', maximum=self.peak)
        return bool(self.masks[m] & (1 << n))

    def witness_audit(self):
        """Evaluate all stored witnesses and count unfolded leaves topologically."""
        values, counts = array('I', [0])*(self.limit+1), bytearray(self.limit+1)
        values[1] = counts[1] = 1
        for m in range(2, self.limit+1):
            a, b = self.split[m]
            values[m] = number_shift(values[a], values[b])
            counts[m] = counts[a]+counts[b]
            if values[m] != m or counts[m] != self.L[m]:
                return False
        return True


def number_leaf_sets(max_leaves=11, value_limit=1000):
    """Independent split-by-leaves reference implementation, bounded explicitly."""
    bounded_int(max_leaves, 'reference leaf budget', maximum=12)
    bounded_int(value_limit, 'reference value limit', maximum=2000)
    S = {1: {1}}
    for n in range(2, max_leaves+1):
        vals = set()
        for k in range(1, n):
            for a in S[k]:
                for b in S[n-k]:
                    value = number_shift(a, b)
                    if value <= value_limit:
                        vals.add(value)
        S[n] = vals
    return S


@lru_cache(maxsize=None)
def number_tree_values(n):
    """One value per ordered Catalan tree; duplicates intentionally retained."""
    bounded_int(n, 'explicit tree leaves', maximum=9)
    if n == 1:
        return (1,)
    return tuple(number_shift(a, b) for k in range(1, n)
                 for a in number_tree_values(k) for b in number_tree_values(n-k))


def eval_number_expression(expression):
    """Strict stack parser for unit-leaf witnesses; returns value and leaf count."""
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError('Empty number expression.')
    if len(expression) > 50000:
        raise ValueError('Expression too large for audit parser.')
    compact = ''.join(expression.split())
    stack = []
    for ch in compact:
        if ch == '1':
            stack.append((1, 1))
        elif ch in '(⋆':
            stack.append(ch)
        elif ch == ')':
            if (len(stack) < 4 or stack[-4] != '(' or stack[-2] != '⋆'
                    or not isinstance(stack[-3], tuple) or not isinstance(stack[-1], tuple)):
                raise ValueError('Malformed number tree.')
            a, b = stack[-3], stack[-1]
            stack[-4:] = [(number_shift(a[0], b[0]), a[1]+b[1])]
        else:
            raise ValueError('Only unit leaves, parentheses and ⋆ are allowed.')
    if len(stack) != 1 or not isinstance(stack[0], tuple):
        raise ValueError('Incomplete number tree or extra tokens.')
    return stack[0]


class TestNumberAlgebraAndBoundaries(unittest.TestCase):
    def test_associator_exact(self):
        for a in (Fraction(-3, 2), Fraction(0), Fraction(1, 10), Fraction(7)):
            for b in (-1, 0, 5):
                for c in (Fraction(-2), Fraction(0), Fraction(3, 7)):
                    self.assertEqual(number_shift(number_shift(a, b), c)-number_shift(a, number_shift(b, c)), a*c)

    def test_distributivity_and_commutator(self):
        for a, b, c in [(2, 3, 4), (-1, 0, 8), (Fraction(1, 3), 2, -1)]:
            self.assertEqual(number_shift(a+b, c), number_shift(a, c)+number_shift(b, c))
            self.assertEqual(number_shift(a, b+c), number_shift(a, b)+number_shift(a, c)-a)
            self.assertEqual(number_shift(a, b)-number_shift(b, a), a-b)

    def test_both_cancellation_boundaries(self):
        self.assertEqual(number_shift(2, -1), number_shift(7, -1))
        self.assertEqual(number_shift(0, 2), number_shift(0, 7))
        for a in (-4, Fraction(1, 7), 5):
            self.assertNotEqual(number_shift(a, 2), number_shift(a, 7))
        for c in (-3, 0, Fraction(1, 5)):
            self.assertNotEqual(number_shift(2, c), number_shift(7, c))

    def test_zero_product_and_fixed_points(self):
        for a in (-2, 0, Fraction(1, 3), 4):
            for b in (-1, 0, Fraction(2, 3), 8):
                self.assertEqual(number_shift(a, b) == 0, a == 0 or b == -1)
                self.assertEqual(number_shift(a, b) == a, a*b == 0)

    def test_quadratic_two_rational_roots(self):
        status, roots = rational_self_shift_roots(2)
        self.assertEqual(status, 'two rational real roots')
        self.assertEqual(roots, (Fraction(-2), Fraction(1)))
        for r in roots:
            self.assertEqual(number_shift(r, r), 2)

    def test_quadratic_boundary(self):
        self.assertEqual(rational_self_shift_roots(Fraction(-1, 4)),
                         ('one rational real root', (Fraction(-1, 2),)))

    def test_quadratic_irrational_roots(self):
        self.assertEqual(rational_self_shift_roots(1), ('two irrational real roots', ()))
        # Standard discriminant 5 is positive and is not a rational square.
        self.assertGreater(5, 0)
        self.assertNotEqual(math.isqrt(5)**2, 5)

    def test_quadratic_no_real_roots(self):
        self.assertEqual(rational_self_shift_roots(-1), ('no real roots', ()))
        self.assertLess(Fraction(-1)+Fraction(1, 4), 0)

    def test_companion_composition_and_inverse(self):
        for a, b, c in [(3, Fraction(1, 5), Fraction(3, 10)), (-2, -1, 4), (0, 2, 3)]:
            self.assertEqual(number_shift(number_shift(a, b), c), number_shift(a, companion_oplus(b, c)))
            self.assertEqual(1+companion_oplus(b, c), (1+b)*(1+c))
        for b in (Fraction(-2), Fraction(0), Fraction(1, 4)):
            self.assertEqual(companion_oplus(b, -b/(1+b)), 0)
        self.assertEqual(companion_oplus(-1, 19), -1)

    def test_zero_step_gap_exact(self):
        for a in (Fraction('1.1222'), Fraction(1, 1000), Fraction(1, 10**18), Fraction(0), Fraction(-1, 100)):
            for b in (Fraction(-5), Fraction(2, 3), Fraction(10**20)):
                self.assertEqual(number_shift(a, b+1)-number_shift(a, b), a)

    def test_inverse_error_amplification(self):
        for a in (Fraction(1), Fraction(1, 1000), Fraction(1, 10**18)):
            b, error = Fraction(7, 3), Fraction(1, 10**12)
            output = number_shift(a, b)
            self.assertEqual((output+error)/a-1-b, error/a)

    def test_nonuniform_output_limit_path(self):
        for a in (Fraction(1, 10), Fraction(1, 1000), Fraction(1, 10**18)):
            self.assertEqual(number_shift(a, 1/a-1), 1)

    def test_algebraic_root_outside_unit_tree_domain(self):
        self.assertEqual(number_shift(-2, -2), 2)
        for n in range(1, 8):
            self.assertTrue(all(v >= n for v in number_tree_values(n)))


_ACTIVE_NUMBER_SWEEP = None


class TestNumberConstructionSweep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sweep = _ACTIVE_NUMBER_SWEEP if _ACTIVE_NUMBER_SWEEP is not None else NumberSweep(1000)
        cls.small = cls.sweep if cls.sweep.limit >= 1000 else NumberSweep(1000)

    def test_catalan_topologies(self):
        self.assertEqual(sorted(number_tree_values(4)), [4, 5, 6, 6, 8])
        for n in range(1, 8):
            self.assertEqual(len(number_tree_values(n)), math.comb(2*n-2, n-1)//n)

    def test_audited_minima(self):
        for m, expected in {1:1, 4:3, 8:4, 23:8, 47:10, 94:11, 95:10, 118:11, 150:10, 188:12}.items():
            self.assertEqual(self.small.L[m], expected)
        self.assertEqual([m for m in range(1,101) if self.small.L[m]==11], [94])

    def test_all_stored_witness_values_and_leaf_counts(self):
        self.assertTrue(self.sweep.witness_audit())

    def test_sample_expression_roundtrips(self):
        for m in (1, 94, 118, 150, 188, self.sweep.limit):
            solver = self.sweep if m <= self.sweep.limit else self.small
            self.assertEqual(eval_number_expression(solver.expression(m)), (m, solver.L[m]))

    def test_reachable_mask_minima_through_selected_limit(self):
        for m in range(1, self.sweep.limit+1):
            mask = self.sweep.masks[m]
            self.assertGreater(mask, 0)
            self.assertEqual((mask & -mask).bit_length()-1, self.sweep.L[m])

    def test_independent_leaf_split_crosscheck(self):
        sets = number_leaf_sets(11, 1000)
        for n, vals in sets.items():
            mask_vals = {m for m in range(1,1001) if self.small.masks[m] & (1 << n)}
            self.assertEqual(mask_vals, vals)

    def test_small_full_gap_counts(self):
        sets = number_leaf_sets(10, 1000)
        expected = [0, 0, 0, 1, 4, 11, 29, 68, 156, 338]
        for n, gaps in enumerate(expected, 1):
            self.assertEqual((2**(n-1)-n+1)-len(sets[n]), gaps)

    def test_optimal_tree_multiplicities(self):
        for n in range(1, 9):
            counts = Counter(number_tree_values(n))
            for m, multiplicity in counts.items():
                if self.small.L[m] == n:
                    self.assertEqual(self.small.optimal_trees[m], multiplicity)
        self.assertEqual(self.small.optimal_trees[6], 2)
        self.assertEqual(self.small.optimal_root_splits[6], 2)

    def test_optimal_root_split_counts(self):
        for m in range(2, 301):
            brute = sum(self.small.L[d]+self.small.L[m//d-1]==self.small.L[m]
                        for d in range(1,m) if m%d==0)
            self.assertEqual(self.small.optimal_root_splits[m], brute)

    def test_lower_bounds_and_excess(self):
        for m in range(1, self.sweep.limit+1):
            lower = 1+(m-1).bit_length()  # exact 1+ceil(log2(m)), including m=1
            self.assertGreaterEqual(self.sweep.L[m], lower)
        self.assertEqual(self.small.L[94]-(1+(93).bit_length()), 3)

    def test_reported_50000_peak_when_available(self):
        if self.sweep.limit < 50000:
            self.skipTest('50,000 peak check requires number limit >= 50,000.')
        prefix_peak = max(self.sweep.L[1:50001])
        peaks = [m for m in range(1,50001) if self.sweep.L[m] == prefix_peak]
        self.assertEqual(prefix_peak, 24)
        self.assertEqual(peaks, [42767, 45863])

    def test_invalid_inputs(self):
        for limit in (0, -1, True, 1.5, NUMBER_MAX+1):
            with self.assertRaises(ValueError):
                NumberSweep(limit)
        for expr in ('', '2', '(1⋆)', '1⋆1', '(1⋆1))', '11'):
            with self.assertRaises(ValueError):
                eval_number_expression(expr)


ALL_TEST_CLASSES = TEST_CLASSES + (TestNumberAlgebraAndBoundaries, TestNumberConstructionSweep)


def run_all_tests(verbosity=1):
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
                               for c in ALL_TEST_CLASSES)
    return unittest.TextTestRunner(verbosity=verbosity).run(suite)


def summarize_numbers(solver):
    print('\n'+'='*64)
    print('NUMBER MODEL: a ⋆ b = a(b+1); unit leaves; targets 1..{}'.format(solver.limit))
    peaks = [m for m in range(1,solver.limit+1) if solver.L[m]==solver.peak]
    print('Peak L={}; {} target(s); first 20: {}'.format(solver.peak, len(peaks), peaks[:20]))
    for m in (94, 118, 150, 188):
        if m <= solver.limit:
            print('m={}, L={}, optimal root splits={}, optimal trees={}'.format(
                m, solver.L[m], solver.optimal_root_splits[m], solver.optimal_trees[m]))
            print('  witness:', solver.expression(m))
    delta_counts = Counter(solver.L[m]-1-(m-1).bit_length() for m in range(1,solver.limit+1))
    print('Excess Δ = L − 1 − ceil(log2 m); counts:', dict(sorted(delta_counts.items())))
    print('\nExact-leaf gaps over [n, min(limit, 2^(n−1))].')
    print('Counts include missing endpoints; large-n rows are RANGE-TRUNCATED.')
    for n in range(1, solver.peak+1):
        upper = min(solver.limit, 1 << (n-1))
        if upper < n:
            continue
        bit, count, first = 1 << n, 0, []
        for m in range(n,upper+1):
            if not solver.masks[m] & bit:
                count += 1
                if len(first) < 10:
                    first.append(m)
        scope = 'full' if upper == 1 << (n-1) else 'truncated'
        print('n={}: {} gaps in {}..{} [{}]; first {}'.format(n,count,n,upper,scope,first))
    print('Gap means absent at EXACTLY n leaves; it is not global nonconstructibility.')
    print('Independent leaf-split cross-check covers n<=11 and values<=1000.')


# =====================================================================
# USER MENU AND EXPLICIT TEST SELECTION
# =====================================================================
RANGE_PRESETS = {1: 50000, 2: 100000, 3: 250000, 4: 500000,
                 5: 750000, 6: 1000000}
PROFILE_NAMES = {'all': 'Complete examination', 'numbers': 'Number sweep and algebra',
                 'geometry': 'Angles, triangles and trig', 'algebra': 'Algebra and zero boundaries only'}


class MenuCancelled(Exception):
    pass


def parse_range_selection(raw):
    text = raw.strip().lower()
    if not text:
        return 50000
    if text in ('q', 'quit', 'exit'):
        raise MenuCancelled()
    clean = text.replace(',', '').replace('_', '')
    if not clean.isascii() or not clean.isdigit():
        raise ValueError('Enter menu choice 1–6 or a whole-number limit from 50,000 to 1,000,000.')
    value = int(clean)
    if value in RANGE_PRESETS:
        return RANGE_PRESETS[value]
    return bounded_int(value, 'menu number limit', minimum=50000, maximum=NUMBER_MAX)


def parse_profile_selection(raw):
    text = raw.strip().lower()
    if text in ('q', 'quit', 'exit'):
        raise MenuCancelled()
    aliases = {'': 'all', '1': 'all', '2': 'numbers', '3': 'geometry', '4': 'algebra'}
    profile = aliases.get(text, text)
    if profile not in PROFILE_NAMES:
        raise ValueError('Enter 1, 2, 3, 4, or the group name: all, numbers, geometry, algebra.')
    return profile


def prompt_choice(prompt, parser, input_fn, output_fn):
    while True:
        try:
            raw = input_fn(prompt)
        except (EOFError, KeyboardInterrupt):
            raise MenuCancelled() from None
        try:
            return parser(raw)
        except ValueError as error:
            output_fn(str(error))


def select_menu(input_fn=None, output_fn=print):
    if input_fn is None:
        input_fn = input  # Resolve at call time: works with Colab input and tests.
    output_fn('\nSHIFT ARITHMETIC FINAL EXAMINATION v7 — USER MENU')
    output_fn('NUMBER RANGE (Enter = 50,000; q = cancel)')
    for key, value in RANGE_PRESETS.items():
        output_fn('  {}. {:,}'.format(key, value))
    output_fn('You may also enter a custom whole-number limit between 50,000 and 1,000,000.')
    number_limit = prompt_choice('Select number range: ', parse_range_selection, input_fn, output_fn)
    output_fn('\nTEST GROUP (Enter = all tests)')
    output_fn('  1. Complete examination — 70 tests, number sweep and both angle models')
    output_fn('  2. Numbers — 34 tests, number sweep and algebra/zero boundaries')
    output_fn('  3. Geometry — 45 tests, angles/triangles/trig; no large number sweep')
    output_fn('  4. Algebra only — 22 tests; no large number sweep')
    profile = prompt_choice('Select test group: ', parse_profile_selection, input_fn, output_fn)
    output_fn('\nOutput: 1. Compact dots (default)   2. Each test name')
    def parse_detail(raw):
        text = raw.strip().lower()
        if text in ('q', 'quit', 'exit'):
            raise MenuCancelled()
        if text in ('', '1'):
            return False
        if text == '2':
            return True
        raise ValueError('Enter 1 for compact output or 2 for test names.')
    verbose = prompt_choice('Select output: ', parse_detail, input_fn, output_fn)
    output_fn('Selected: {}; number bound {:,}; angle summaries through 180°.'.format(
        PROFILE_NAMES[profile], number_limit))
    if profile in ('geometry', 'algebra'):
        output_fn('This test group does not use the selected large number range.')
    return number_limit, profile, verbose


def profile_classes(profile, include_controls=True):
    groups = {
        'all': ALL_TEST_CLASSES,
        'numbers': (TestNumberAlgebraAndBoundaries, TestNumberConstructionSweep),
        'geometry': TEST_CLASSES,
        'algebra': (TestNumberAlgebraAndBoundaries,),
    }
    if profile not in groups:
        raise ValueError('Unknown test profile: '+str(profile))
    return groups[profile] + ((TestMenuAndControls,) if include_controls else ())


class TestMenuAndControls(unittest.TestCase):
    def test_every_range_preset(self):
        for option, expected in RANGE_PRESETS.items():
            self.assertEqual(parse_range_selection(str(option)), expected)

    def test_defaults_and_formatted_limits(self):
        for value, expected in [('',50000), ('50,000',50000), ('1_000_000',1000000), ('123456',123456)]:
            self.assertEqual(parse_range_selection(value), expected)

    def test_invalid_ranges(self):
        for raw in ('0','7','49999','1000001','1.5','abc','-50000','1e6'):
            with self.assertRaises(ValueError):
                parse_range_selection(raw)

    def test_profile_choices(self):
        for raw, expected in [('', 'all'),('1','all'),('2','numbers'),('3','geometry'),('4','algebra'),('GEOMETRY','geometry')]:
            self.assertEqual(parse_profile_selection(raw), expected)
        with self.assertRaises(ValueError):
            parse_profile_selection('5')

    def test_complete_menu_and_retry(self):
        answers = iter(['bad','6','bad','1','bad','2'])
        messages = []
        result = select_menu(lambda prompt: next(answers), messages.append)
        self.assertEqual(result, (1000000,'all',True))
        self.assertTrue(any('whole-number' in text for text in messages))

    def test_cancellation_and_eof(self):
        with self.assertRaises(MenuCancelled):
            select_menu(lambda prompt: 'q', lambda text: None)
        def no_input(prompt):
            raise EOFError
        with self.assertRaises(MenuCancelled):
            select_menu(no_input, lambda text: None)

    def test_all_defaults_without_mutation(self):
        self.assertEqual(select_menu(lambda prompt: '', lambda text: None), (50000,'all',False))

    def test_exact_profile_counts(self):
        expected = {'all':70, 'numbers':34, 'geometry':45, 'algebra':22}
        for profile, count in expected.items():
            total = sum(unittest.defaultTestLoader.loadTestsFromTestCase(c).countTestCases()
                        for c in profile_classes(profile))
            self.assertEqual(total,count)

    def test_compact_witness_storage_and_progress(self):
        reports=[]
        solver=NumberSweep(100, progress=lambda phase,done,total:reports.append((phase,done,total)))
        self.assertEqual(solver.split[1],None)
        self.assertEqual(solver.L[94],11)
        self.assertTrue(solver.witness_audit())
        self.assertTrue(any(phase=='Exact-leaf reachability' and done==100 for phase,done,total in reports))


def run_selected_tests(profile='all', verbosity=1):
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
                            for c in profile_classes(profile))
    # Explicit classes only: never discover unrelated old notebook tests.
    return unittest.TextTestRunner(verbosity=verbosity, stream=sys.stdout).run(suite)


def execute_selection(number_limit=50000, profile='all', angle_limit=180, verbose=False):
    bounded_int(number_limit,'number limit',minimum=50000,maximum=NUMBER_MAX)
    bounded_int(angle_limit,'angle limit')
    profile_classes(profile)  # Validate before allocating the sweep.
    global _ACTIVE_NUMBER_SWEEP
    _ACTIVE_NUMBER_SWEEP=None  # Release prior run before allocating another.
    start=time.perf_counter()
    print('\nRUNNING: {} | number bound {:,}'.format(PROFILE_NAMES[profile],number_limit),flush=True)
    if profile in ('all','numbers'):
        def report(phase,done,total):
            print('  {}: {:>3.0f}% ({:,}/{:,})'.format(phase,100*done/total,done,total),flush=True)
        _ACTIVE_NUMBER_SWEEP=NumberSweep(number_limit,progress=report)
        print('Sweep ready in {:.3f}s. Testing...'.format(time.perf_counter()-start),flush=True)
    result=run_selected_tests(profile,2 if verbose else 1)
    if not result.wasSuccessful():
        print('FAILED: summaries withheld. Share the errors above.')
        return 1
    if profile in ('all','numbers'):
        summarize_numbers(_ACTIVE_NUMBER_SWEEP)
    if profile in ('all','geometry'):
        for index,bases in enumerate(((1,),(1,2)),1):
            print('\n'+'='*64)
            print('ANGLE MODEL {}: seeds {} — A ⋆ B = A+B+1°'.format(index,bases))
            print('The angle operation is distinct from a(b+1).')
            summarize(angle_limit,bases,show_trig=(index==2))
    skipped=len(result.skipped)
    print('\nRUN COMPLETE: {} tests; {} passed; {} skipped; no failures/errors.'.format(
        result.testsRun,result.testsRun-skipped,skipped))
    print('Profile: {}; selected number bound: {:,}.'.format(profile,number_limit))
    print('Total elapsed: {:.3f}s. Share this output for review.'.format(time.perf_counter()-start))
    return 0


def main(argv=None):
    args_list=list(sys.argv[1:] if argv is None else argv)
    parser=argparse.ArgumentParser(description='Shift Arithmetic final edition v7: menu and selectable tests.')
    parser.add_argument('--number-limit',type=int,default=50000)
    parser.add_argument('--angle-limit',type=int,default=180)
    parser.add_argument('--tests',choices=tuple(PROFILE_NAMES),default='all')
    parser.add_argument('--verbose',action='store_true')
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--menu',action='store_true')
    modes.add_argument('--no-menu',action='store_true')
    args=parser.parse_args(args_list)
    try:
        if args.menu or not args_list:
            limit,profile,verbose=select_menu()
        else:
            limit,profile,verbose=args.number_limit,args.tests,args.verbose
        bounded_int(limit,'number limit',minimum=50000,maximum=NUMBER_MAX)
        bounded_int(args.angle_limit,'angle limit')
    except MenuCancelled:
        print('\nCancelled. No examination started. Run the file again when ready.')
        return 0
    except ValueError as error:
        parser.error(str(error))
    try:
        return execute_selection(limit,profile,args.angle_limit,verbose)
    except KeyboardInterrupt:
        print('\nRun interrupted. No complete verification result was produced.')
        return 130


if __name__=='__main__':
    if 'ipykernel' in sys.modules or 'google.colab' in sys.modules:
        main([])  # Opens the menu while ignoring Jupyter kernel flags.
    else:
        raise SystemExit(main())
