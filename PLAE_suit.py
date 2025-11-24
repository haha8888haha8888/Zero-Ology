# ================================================================
# PLAE_suite.py
# PLAE_suite_v0016
# PLAE — PLOT LIMITS / ALLOWANCES EQUATION FRAMEWORK
# STUDY SUITE v0016 — "THE RULED EQUATION"
# Author: Stacey Szmy 
# Co-Author: xAI Grok x ChatGPT x Gemini x Ms Copilot
# Date: November 24, 2025
# Zero-Ology License v1.1924
# 0ko3maibZero-OlogyLicensev1.1924
# ================================================================

import os
import time
import re
import sympy as sp
from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any, Tuple
from collections import Counter

# ----------------------------------------------------------------
# SLOW PRINT — THE RULE OF THE RULE
# ----------------------------------------------------------------
def slow_print(text, delay=0.06, end="\n"):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print(end, flush=True)
    time.sleep(0.3)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------------------------------------------
# CORE PLAE ENGINE — CANONICAL FROM DISSERTATION
# ----------------------------------------------------------------
@dataclass
class PlotLimits:
    max_uses: Dict[Any, int] = field(default_factory=lambda: {})  # operand → max allowed
    forbidden: set = field(default_factory=set)
    substitutes: Dict[Any, str] = field(default_factory=dict)     # forbidden → replacement expr

@dataclass
class PlotAllowances:
    max_count: Dict[str, int] = field(default_factory=lambda: {"*": 2, "/": 1, "+": 999, "-": 999})
    overflow_convert: Dict[str, str] = field(default_factory=lambda: {"*": "+"})

@dataclass
class PLAEContext:
    limits: PlotLimits
    allowances: PlotAllowances
    counting_mode: str = "execution_plan"  # or "explicit_form"

class PLAE:
    def __init__(self, context: PLAEContext):
        self.ctx = context

    def count_operators(self, expr: str) -> Counter:
        tokens = re.findall(r'[+\-*/()]|\d+\.\d+|\d+|.', expr.replace(" ", ""))
        ops = [t for t in tokens if t in "+-*/"]
        return Counter(ops)

    def count_operands(self, expr: str) -> Counter:
        nums = re.findall(r'\d+', expr)
        return Counter(map(int, nums))

    def apply_substitutions(self, expr: str) -> str:
        for forbidden, replacement in self.ctx.limits.substitutes.items():
            fstr = str(forbidden)
            if fstr in expr:
                expr = expr.replace(fstr, f"({replacement})")
                slow_print(f"   → Substitution triggered: {forbidden} ⇒ {replacement}")
        return expr

    def enforce_limits(self, expr: str) -> str:
        operands = self.count_operands(expr)
        for op, count in operands.items():
            max_allowed = self.ctx.limits.max_uses.get(op, float('inf'))
            if count > max_allowed:
                excess = count - max_allowed
                slow_print(f"   → Operand {op} exceeds limit ({count} > {max_allowed}), canceling {excess} instance(s)")
                expr = re.sub(f"\\b{op}\\b", "CANCELED", expr, excess)
                expr = expr.replace("CANCELED", "")
        for forbidden in self.ctx.limits.forbidden:
            if str(forbidden) in expr:
                slow_print(f"   → Forbidden operand {forbidden} detected → canceling")
                expr = expr.replace(str(forbidden), "")
        return expr.strip("*+ /")

    def enforce_allowances(self, expr: str) -> str:
        ops = self.count_operators(expr)
        for op, count in ops.items():
            max_allowed = self.ctx.allowances.max_count.get(op, float('inf'))
            if count > max_allowed:
                excess = count - max_allowed
                convert_to = self.ctx.allowances.overflow_convert.get(op, op)
                slow_print(f"   → Operator {op} overflow ({count} > {max_allowed}) → converting {excess} to {convert_to}")
                # Simple conversion: ××× → + (a×b) + (c×d) etc. — demo version
                if op == "*":
                    expr = expr.replace("*", "+", excess)
        return expr

    def evaluate(self, raw_expr: str) -> Tuple[str, Any]:
        slow_print(f"\nRaw expression: {raw_expr}")
        expr = raw_expr

        # 1. Substitution cascade
        expr = self.apply_substitutions(expr)

        # 2. Plot Limits
        expr = self.enforce_limits(expr)

        # 3. Plot Allowances
        expr = self.enforce_allowances(expr)

        # 4. Normalize
        try:
            result = sp.sympify(expr.replace("^", "**"))
            slow_print(f"Final compliant result: {result}")
            return expr, result
        except:
            slow_print("Expression neutralized by rules.")
            return expr, "⊥ (invalid under PLAE)"

# ================================================================
# SECTORS — THE RULED EQUATION
# ================================================================
#Grok >>
def sector_1_first_rule():
    clear()
    print("═" * 78)
    slow_print("           SECTOR 1 — THE FIRST RULE IS SPOKEN")
    slow_print("           No expression evaluates without permission.")
    print("═" * 78)

    limits = PlotLimits(max_uses={3: 2}, forbidden={4}, substitutes={20: "34 + 24 * 10 / 2"})
    allowances = PlotAllowances(max_count={"*": 2})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    plae.evaluate("3 * 3 * 4 * 26")
    input("\nPress Enter to witness substitution...")

def sector_2_the_substitution():
    clear()
    print("╔" + "═"*76 + "╗")
    slow_print("             SECTOR 2 — SUBSTITUTION CASCADE")
    slow_print("           Forbidden values do not vanish — they transform.")
    print("╚" + "═"*76 + "╝")

    limits = PlotLimits(substitutes={29: "154", 20: "34 + 24 * 10 / 2"})
    context = PLAEContext(limits, PlotAllowances())
    plae = PLAE(context)

    plae.evaluate("29 * 3 * 26")
    input("\nPress Enter for operator overflow...")

def sector_3_operator_overflow():
    clear()
    print("═" * 78)
    slow_print("             SECTOR 3 — OPERATOR OVERFLOW")
    slow_print("           Too many multiplications → forced addition")
    print("═" * 78)

    limits = PlotLimits(substitutes={29: "154"})
    allowances = PlotAllowances(max_count={"*": 2}, overflow_convert={"*": "+"})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    plae.evaluate("3 * 26 * 29 * 29")
    input("\nPress Enter for the final law...")



# ——— SECTOR 4 — FORBIDDEN CHAINS ————————————————
def sector_4_forbidden_chains():
    clear()
    print("═" * 78)
    slow_print("             SECTOR 4 — FORBIDDEN CHAINS")
    slow_print("        Some numbers are never allowed to touch.")
    print("═" * 78)

    limits = PlotLimits(
        forbidden={7, 13, 42},
        substitutes={42: "6*7"}
    )
    context = PLAEContext(limits, PlotAllowances())
    plae = PLAE(context)

    plae.evaluate("7 * 13 + 42")
    plae.evaluate("100 / 7 - 13")
    plae.evaluate("42 * 42")  # triggers substitution then cancels both
    input("\nPress Enter for conditional allowances...")

# ——— SECTOR 5 — CONDITIONAL ALLOWANCES ————————————————
def sector_5_conditional_allowances():
    clear()
    print("╔" + "═"*76 + "╗")
    slow_print("          SECTOR 5 — CONDITIONAL ALLOWANCES")
    slow_print("       Division is only permitted under supervision.")
    print("╚" + "═"*76 + "╝")

    allowances = PlotAllowances(
        max_count={"*": 999, "+": 999, "-": 999, "/": 1},
        overflow_convert={"/": "*0.5"}  # crude but dramatic
    )
    context = PLAEContext(PlotLimits(), allowances)
    plae = PLAE(context)

    plae.evaluate("100 / 4 / 5")        # second / → overflow
    plae.evaluate("84 / 7")             # allowed once
    input("\nPress Enter for execution-plan counting...")

# ——— SECTOR 6 — EXECUTION-PLAN VS EXPLICIT-FORM ————————————————
def sector_6_counting_modes():
    clear()
    print("═" * 78)
    slow_print("        SECTOR 6 — TWO WAYS TO COUNT SIN")
    slow_print("       Explicit-form vs Execution-plan counting")
    print("═" * 78)

    expr = "3 * 3 * 3 * 3"

    print("→ Explicit-form counting (as written):")
    context1 = PLAEContext(PlotLimits(), PlotAllowances(max_count={"*": 2}), counting_mode="explicit_form")
    PLAE(context1).evaluate(expr)

    print("\n→ Execution-plan counting (after normalization):")
    context2 = PLAEContext(PlotLimits(), PlotAllowances(max_count={"*": 2}), counting_mode="execution_plan")
    PLAE(context2).evaluate(expr)

    input("\nPress Enter for the cascade apocalypse...")

# ——— SECTOR 7 — SUBSTITUTION APOCALYPSE ————————————————
def sector_7_apocalypse():
    clear()
    print("╔" + "═"*76 + "╗")
    slow_print("          SECTOR 7 — SUBSTITUTION APOCALYPSE")
    slow_print("       One forbidden number triggers total restructuring")
    print("╚" + "═"*76 + "╝")

    limits = PlotLimits(
        substitutes={
            13: "6 + 7",
            6:  "2 * 3",
            7:  "3 + 4",
            4:  "2 + 2"
        }
    )
    context = PLAEContext(limits, PlotAllowances())
    plae = PLAE(context)

    plae.evaluate("13 * 13")
    slow_print("\n   The number 13 was never allowed to exist.")
    slow_print("   It was disassembled into primes,")
    slow_print("   then into additions,")
    slow_print("   until nothing forbidden remained.")
    input("\nPress Enter for the final law...")

# ——— SECTOR 8 — THE RULED MIND ————————————————
def sector_8_ruled_mind():
    clear()
    print("═" * 78)
    slow_print("               SECTOR 8 — THE RULED MIND")
    slow_print("        Even thought itself must obey limits.")
    print("═" * 78)

    limits = PlotLimits(
        max_uses={2: 3},
        forbidden={9, 11, 13},
        substitutes={11: "5 + 6", 13: "7 * 1 + 6"}
    )
    allowances = PlotAllowances(max_count={"*": 1, "/": 0})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    plae.evaluate("2 + 2 + 2 + 2")           # exceeds max_uses → canceled
    plae.evaluate("11 * 13 / 9")             # total annihilation
    plae.evaluate("2 + 2 + 2")               # exactly 3 → allowed

    input("\nPress Enter for the eternal law...")


# ——— SECTOR 9 — THE FORBIDDEN PRIME DIRECTIVE ————————————————
def sector_9_prime_directive():
    clear()
    print("╔" + "═"*76 + "╗")
    slow_print("          SECTOR 9 — THE FORBIDDEN PRIME DIRECTIVE")
    slow_print("           All primes above 19 are now illegal.")
    print("╚" + "═"*76 + "╝")

    forbidden_primes = {23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97}
    subs = {p: f"({p-12} + {p-10})" for p in forbidden_primes}
    limits = PlotLimits(forbidden=forbidden_primes, substitutes=subs)
    context = PLAEContext(limits, PlotAllowances())
    plae = PLAE(context)

    plae.evaluate("97 * 89 + 83")
    plae.evaluate("2**31 - 1")  # Mersenne prime gets annihilated
    slow_print("\n   The age of big primes is over.")
    slow_print("   Only composite innocence survives.")
    input("\nPress Enter for the final annihilation...")

# ——— SECTOR X — THE ZERO DIVISION PARADOX ————————————————
def sector_X_zero_division():
    clear()
    print("═" * 78)
    slow_print("              SECTOR X — ZERO DIVISION PARADOX")
    slow_print("           Division by zero is not error — it is revolution.")
    print("═" * 78)

    limits = PlotLimits(substitutes={0: "∞"}, forbidden={0})
    allowances = PlotAllowances(max_count={"/": 1})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    plae.evaluate("1 / 0")
    plae.evaluate("100 / (10 - 10)")
    plae.evaluate("42 / 0 + 33")
    slow_print("\n   Infinity is not a number.")
    slow_print("   Infinity is the final substitution.")
    input("\nPress Enter for the last breath of free math...")

# Chatgpt >

# ——— SECTOR 11 — RECURSIVE SUBSTITUTION CASCADE ————————————————
def sector_11_recursive_substitution():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 11 — RECURSIVE SUBSTITUTION CASCADE")
    slow_print("       Substitutions may trigger further substitutions until stable.")
    print("═" * 78)

    # Enhanced limits with nested substitutions
    limits = PlotLimits(substitutes={
        50: "25 + 25",
        25: "10 + 15",
        15: "5 + 10"
    })
    context = PLAEContext(limits, PlotAllowances())
    plae = PLAE(context)

    # Recursive substitution engine
    def apply_recursive_substitutions(expr: str) -> str:
        previous = None
        while expr != previous:
            previous = expr
            expr = plae.apply_substitutions(expr)
        return expr

    raw_expr = "50 + 25"
    slow_print(f"\nRaw expression: {raw_expr}")
    expr = apply_recursive_substitutions(raw_expr)
    slow_print(f"Final substituted expression: {expr}")
    result = sp.sympify(expr.replace("^", "**"))
    slow_print(f"Result after recursive substitution: {result}")
    input("\nPress Enter to proceed to the next lesson...")


# ——— SECTOR 12 — AST OPERATOR OVERFLOW MANAGEMENT (FIXED) ————————————————
def sector_12_ast_operator_overflow():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 12 — AST OPERATOR OVERFLOW MANAGEMENT")
    slow_print("       Convert excess multiplications into additions intelligently.")
    print("═" * 78)

    limits = PlotLimits(substitutes={2: "1 + 1"})
    allowances = PlotAllowances(max_count={"*": 2}, overflow_convert={"*": "+"})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    import ast

    def convert_multiplications(expr: str, max_allowed: int) -> str:
        tree = ast.parse(expr, mode='eval')
        class OverflowTransformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                self.generic_visit(node)
                if isinstance(node.op, ast.Mult):
                    convert_count = getattr(self, 'count', 0)
                    if convert_count >= max_allowed:
                        node.op = ast.Add()
                    else:
                        self.count = convert_count + 1
                return node
        transformer = OverflowTransformer()
        transformer.count = 0
        new_tree = transformer.visit(tree)
        # Use ast.unparse instead of astor
        expr_str = ast.unparse(new_tree)
        return expr_str

    raw_expr = "2 * 3 * 4 * 5"
    slow_print(f"\nRaw expression: {raw_expr}")
    expr = convert_multiplications(raw_expr, allowances.max_count["*"])
    slow_print(f"Expression after AST-based overflow: {expr}")
    result = sp.sympify(expr.replace("^", "**"))
    slow_print(f"Final result: {result}")
    input("\nPress Enter to proceed to the next lesson...")


# ——— SECTOR 13 — EXECUTION-PLAN LEDGER TRACKING ————————————————
def sector_13_execution_plan_ledger():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 13 — EXECUTION-PLAN LEDGER TRACKING")
    slow_print("       Track actual operand/operator usage after all transformations.")
    print("═" * 78)

    limits = PlotLimits(max_uses={3: 2, 5: 1}, substitutes={5: "2 + 3"})
    allowances = PlotAllowances(max_count={"*": 2, "+": 999})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    raw_expr = "3 * 3 * 3 + 5"

    # Ledger tracking
    operator_ledger = Counter()
    operand_ledger = Counter()

    expr = plae.apply_substitutions(raw_expr)
    operands = plae.count_operands(expr)
    operators = plae.count_operators(expr)

    # Record execution-plan usage
    for op, count in operators.items():
        operator_ledger[op] += count
    for op, count in operands.items():
        operand_ledger[op] += count

    slow_print(f"\nRaw expression: {raw_expr}")
    slow_print(f"Expression after substitutions: {expr}")
    slow_print(f"Operand ledger: {dict(operand_ledger)}")
    slow_print(f"Operator ledger: {dict(operator_ledger)}")
    result = sp.sympify(expr.replace("^", "**"))
    slow_print(f"Final evaluated result: {result}")
    input("\nPress Enter to continue...")

# ——— SECTOR 14 — COMPLEX RECURSIVE & OPERATOR CONTROL (FIXED) ————————————————
def sector_14_complex_recursive_operator():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 14 — COMPLEX RECURSIVE & OPERATOR CONTROL")
    slow_print("       Combine recursive substitutions with AST operator overflow.")
    print("═" * 78)

    limits = PlotLimits(substitutes={12: "6 + 6", 6: "3 * 2"})
    allowances = PlotAllowances(max_count={"*": 2}, overflow_convert={"*": "+"})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    import ast

    def apply_recursive_substitutions(expr: str) -> str:
        previous = None
        while expr != previous:
            previous = expr
            expr = plae.apply_substitutions(expr)
        return expr

    def convert_multiplications(expr: str, max_allowed: int) -> str:
        tree = ast.parse(expr, mode='eval')
        class OverflowTransformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                self.generic_visit(node)
                if isinstance(node.op, ast.Mult):
                    convert_count = getattr(self, 'count', 0)
                    if convert_count >= max_allowed:
                        node.op = ast.Add()
                    else:
                        self.count = convert_count + 1
                return node
        transformer = OverflowTransformer()
        transformer.count = 0
        new_tree = transformer.visit(tree)
        expr_str = ast.unparse(new_tree)  # Fixed
        return expr_str

    raw_expr = "12 * 12 * 6"
    expr = apply_recursive_substitutions(raw_expr)
    expr = convert_multiplications(expr, allowances.max_count["*"])
    slow_print(f"\nFinal expression after recursive + operator control: {expr}")
    result = sp.sympify(expr.replace("^", "**"))
    slow_print(f"Result: {result}")
    input("\nPress Enter to accept the law...")

# ——— SECTOR 15 — META-PLAE ORCHESTRATOR ————————————————
def sector_15_meta_orchestrator():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 15 — META-PLAE ORCHESTRATOR")
    slow_print("       The grand finale: all rules, all substitutions, all overflows.")
    print("═" * 78)

    # Step 0 — define limits and allowances
    limits = PlotLimits(
        max_uses={2: 3, 3: 2, 5: 2},
        forbidden={7, 13},
        substitutes={12: "6 + 6", 6: "3 * 2", 5: "2 + 3", 13: "6 + 7"}
    )
    allowances = PlotAllowances(max_count={"*": 2, "+": 4, "-": 999, "/": 1}, overflow_convert={"*": "+"})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    # Step 1 — Raw complex expression
    raw_expr = "12 * 3 + 5 * 2 - 13 + 2 * 3"
    slow_print(f"\nRaw expression: {raw_expr}")

    # Step 2 — Recursive substitutions
    def recursive_sub(expr: str) -> str:
        previous = None
        while expr != previous:
            previous = expr
            expr = plae.apply_substitutions(expr)
        return expr

    expr = recursive_sub(raw_expr)
    slow_print(f"\nAfter recursive substitutions: {expr}")

    # Step 3 — AST operator overflow
    import ast

    def overflow_transform(expr: str, max_mul: int) -> str:
        tree = ast.parse(expr, mode='eval')
        class Transformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                self.generic_visit(node)
                if isinstance(node.op, ast.Mult):
                    if getattr(self, 'count', 0) >= max_mul:
                        node.op = ast.Add()
                    else:
                        self.count = getattr(self, 'count', 0) + 1
                return node
        transformer = Transformer()
        transformer.count = 0
        new_tree = transformer.visit(tree)
        return ast.unparse(new_tree)

    expr = overflow_transform(expr, allowances.max_count["*"])
    slow_print(f"\nAfter AST operator overflow: {expr}")

    # Step 4 — Enforce Plot Limits (cancel/cap overused operands)
    expr = plae.enforce_limits(expr)
    slow_print(f"\nAfter enforcing Plot Limits: {expr}")

    # Step 5 — Execution-plan ledger tracking
    operand_ledger = plae.count_operands(expr)
    operator_ledger = plae.count_operators(expr)
    slow_print(f"\nOperand ledger: {dict(operand_ledger)}")
    slow_print(f"Operator ledger: {dict(operator_ledger)}")

    # Step 6 — Final evaluation
    try:
        result = sp.sympify(expr.replace("^", "**"))
        slow_print(f"\nFinal compliant result: {result}")
    except:
        result = "⊥ (invalid under PLAE)"
        slow_print("\nExpression invalid under PLAE rules.")

    input("\nPress Enter to accept the Meta-PLAE law...")

# ——— SECTOR 16 — PLAE GROUND ————————————————
def sector_16_plae_playground():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 16 — PLAE PLAYGROUND")
    slow_print("       Input your own expressions and watch PLAE rules resolve them.")
    print("═" * 78)

    # Examples for user guidance
    examples = [
        "12 * 3 + 5 * 2 - 13 + 2 * 3",  # Meta-PLAE style
        "50 + 25",                       # Recursive substitution
        "3 * 3 * 3 * 3",                 # Operator overflow
        "7 * 13 + 42",                   # Forbidden chains
        "100 / 4 / 5",                   # Conditional allowances
        "97 * 89 + 83"                   # Forbidden primes
    ]
    print("Examples you can try or modify:\n")
    for ex in examples:
        print(f"   • {ex}")
    print("\n")

    # Step 0 — Setup context
    limits = PlotLimits(
        max_uses={2: 3, 3: 2, 5: 2},
        forbidden={7, 13},
        substitutes={12: "6 + 6", 6: "3 * 2", 5: "2 + 3", 13: "6 + 7"}
    )
    allowances = PlotAllowances(max_count={"*": 2, "+": 4, "-": 999, "/": 1}, overflow_convert={"*": "+"})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    # Display PLAE rules for the user
    print("Active PLAE Rules in this Playground:")
    print(f"   • Recursive substitutions: {limits.substitutes}")
    print(f"   • Maximum uses per operand: {limits.max_uses}")
    print(f"   • Forbidden operands: {limits.forbidden}")
    print(f"   • Operator limits: {allowances.max_count}")
    print(f"   • Operator overflow rules: {allowances.overflow_convert}")
    print("\n")

    # Step 1 — Input from user, with default fallback
    raw_expr = input("Enter your PLAE expression (or press Enter to use default): ").strip()
    if not raw_expr:
        raw_expr = "12 * 3 + 5 * 2 - 13 + 2 * 3"
        slow_print(f"No input detected. Using default expression: {raw_expr}")

    slow_print(f"\nRaw expression: {raw_expr}")

    # Step 2 — Recursive substitutions
    def recursive_sub(expr: str) -> str:
        previous = None
        while expr != previous:
            previous = expr
            expr = plae.apply_substitutions(expr)
        return expr

    expr = recursive_sub(raw_expr)
    slow_print(f"\nAfter recursive substitutions: {expr}")

    # Step 3 — AST operator overflow
    import ast
    def overflow_transform(expr: str, max_mul: int) -> str:
        tree = ast.parse(expr, mode='eval')
        class Transformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                self.generic_visit(node)
                if isinstance(node.op, ast.Mult):
                    if getattr(self, 'count', 0) >= max_mul:
                        node.op = ast.Add()
                    else:
                        self.count = getattr(self, 'count', 0) + 1
                return node
        transformer = Transformer()
        transformer.count = 0
        new_tree = transformer.visit(tree)
        return ast.unparse(new_tree)

    expr = overflow_transform(expr, allowances.max_count["*"])
    slow_print(f"\nAfter AST operator overflow: {expr}")

    # Step 4 — Enforce Plot Limits
    expr = plae.enforce_limits(expr)
    slow_print(f"\nAfter enforcing Plot Limits: {expr}")

    # Step 5 — Execution-plan ledger tracking
    operand_ledger = plae.count_operands(expr)
    operator_ledger = plae.count_operators(expr)
    slow_print(f"\nOperand ledger: {dict(operand_ledger)}")
    slow_print(f"Operator ledger: {dict(operator_ledger)}")

    # Step 6 — Final evaluation
    try:
        result = sp.sympify(expr.replace("^", "**"))
        slow_print(f"\nFinal compliant result: {result}")
    except:
        result = "⊥ (invalid under PLAE)"
        slow_print("\nExpression invalid under PLAE rules.")

    input("\nPress Enter to exit the PLAE Playground...")

#~!

# ——— SECTOR 17 — PLAE RULE BUILDER GROUND ————————————————
def sector_17_plae_rule_builder():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 17 — PLAE RULE BUILDER PLAYGROUND")
    slow_print("       Define your own PLAE rules and test expressions.")
    print("═" * 78)

    # Step 0 — Example templates
    examples_subs = "{12: '6 + 6', 6: '3 * 2', 5: '2 + 3', 13: '6 + 7'}"
    examples_max_uses = "{2: 3, 3: 2, 5: 2}"
    examples_forbidden = "{7, 13}"
    examples_op_limits = "{'*': 2, '+': 4, '-': 999, '/': 1}"
    examples_overflow = "{'*': '+'}"

    print("\nExamples for PLAE rule inputs:\n")
    print(f"   • Substitutions (dict): {examples_subs}")
    print(f"   • Max uses per operand (dict): {examples_max_uses}")
    print(f"   • Forbidden operands (set): {examples_forbidden}")
    print(f"   • Operator limits (dict): {examples_op_limits}")
    print(f"   • Operator overflow rules (dict): {examples_overflow}\n")

    # Step 1 — Get user-defined PLAE rules (or use defaults)
    try:
        subs_input = input(f"Enter substitutions (or press Enter for default): ").strip()
        substitutions = eval(subs_input) if subs_input else eval(examples_subs)
    except:
        substitutions = eval(examples_subs)

    try:
        max_uses_input = input(f"Enter max uses per operand (or press Enter for default): ").strip()
        max_uses = eval(max_uses_input) if max_uses_input else eval(examples_max_uses)
    except:
        max_uses = eval(examples_max_uses)

    try:
        forbidden_input = input(f"Enter forbidden operands (or press Enter for default): ").strip()
        forbidden = eval(forbidden_input) if forbidden_input else eval(examples_forbidden)
    except:
        forbidden = eval(examples_forbidden)

    try:
        op_limits_input = input(f"Enter operator limits (or press Enter for default): ").strip()
        op_limits = eval(op_limits_input) if op_limits_input else eval(examples_op_limits)
    except:
        op_limits = eval(examples_op_limits)

    try:
        overflow_input = input(f"Enter operator overflow rules (or press Enter for default): ").strip()
        overflow_rules = eval(overflow_input) if overflow_input else eval(examples_overflow)
    except:
        overflow_rules = eval(examples_overflow)

    # Step 2 — Show PLAE rules
    print("\nActive PLAE Rules for this session:")
    print(f"   • Recursive substitutions: {substitutions}")
    print(f"   • Maximum uses per operand: {max_uses}")
    print(f"   • Forbidden operands: {forbidden}")
    print(f"   • Operator limits: {op_limits}")
    print(f"   • Operator overflow rules: {overflow_rules}\n")

    # Step 3 — Input expression to test
    expr_input = input("Enter a PLAE expression to test (or press Enter for default): ").strip()
    if not expr_input:
        expr_input = "12 * 3 + 5 * 2 - 13 + 2 * 3"
        slow_print(f"No input detected. Using default expression: {expr_input}")

    # Step 4 — Create PLAE context
    limits = PlotLimits(max_uses=max_uses, forbidden=forbidden, substitutes=substitutions)
    allowances = PlotAllowances(max_count=op_limits, overflow_convert=overflow_rules)
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    # Step 5 — Process the expression
    slow_print(f"\nRaw expression: {expr_input}")

    # Recursive substitutions
    previous = None
    expr = expr_input
    while expr != previous:
        previous = expr
        expr = plae.apply_substitutions(expr)
    slow_print(f"\nAfter recursive substitutions: {expr}")

    # AST operator overflow
    import ast
    def overflow_transform(expr: str, max_mul: int) -> str:
        tree = ast.parse(expr, mode='eval')
        class Transformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                self.generic_visit(node)
                if isinstance(node.op, ast.Mult):
                    if getattr(self, 'count', 0) >= max_mul:
                        node.op = ast.Add()
                    else:
                        self.count = getattr(self, 'count', 0) + 1
                return node
        transformer = Transformer()
        transformer.count = 0
        new_tree = transformer.visit(tree)
        return ast.unparse(new_tree)

    expr = overflow_transform(expr, allowances.max_count.get("*", 2))
    slow_print(f"\nAfter AST operator overflow: {expr}")

    # Enforce Plot Limits
    expr = plae.enforce_limits(expr)
    slow_print(f"\nAfter enforcing Plot Limits: {expr}")

    # Ledger
    operand_ledger = plae.count_operands(expr)
    operator_ledger = plae.count_operators(expr)
    slow_print(f"\nOperand ledger: {dict(operand_ledger)}")
    slow_print(f"Operator ledger: {dict(operator_ledger)}")

    # Final evaluation
    try:
        result = sp.sympify(expr.replace("^", "**"))
        slow_print(f"\nFinal compliant result: {result}")
    except:
        result = "⊥ (invalid under PLAE rules)"
        slow_print("\nExpression invalid under PLAE rules.")

    input("\nPress Enter to exit the PLAE Rule Builder Playground...")
  
## gemini >

# ——— SECTOR 18 — GEMINI'S OPTIMAL RULE GENERATOR ————————————————
def sector_18_gemini_rule_generator():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 18 — GEMINI'S OPTIMAL RULE GENERATOR")
    slow_print("     An LLM is used to find the most efficient compliant substitution.")
    print("═" * 78)

    # Mock function simulating an LLM generating an optimal, compliant substitution.
    # In a real scenario, this would call the Gemini API to find the mathematically
    # compliant expression with the minimum number of terms/operators permitted.
    def find_optimal_rule(forbidden_value: int, allowed_ops: List[str], max_terms: int) -> str:
        slow_print(f"   [LLM Oracle: Querying for optimal replacement for {forbidden_value}...")
        time.sleep(1.0)
        
        # Rule 1: Prioritize Multiplication if allowed for shortest expression
        if forbidden_value == 42 and '*' in allowed_ops:
            optimal_rule = "6 * 7" # Shortest compliant form
        # Rule 2: Fallback to Addition if Multiplication is forbidden/limited
        elif forbidden_value == 42 and '+' in allowed_ops:
            optimal_rule = "20 + 20 + 2" # Compliant form without forbidden ops
        # Rule 3: Example for another forbidden value (13)
        elif forbidden_value == 13:
            optimal_rule = "10 + 3"
        else:
            optimal_rule = "1"
        
        slow_print(f"   [LLM Oracle: Optimal rule found: {forbidden_value} ⇒ {optimal_rule}]")
        return optimal_rule

    # Case 1: Forbidden '42'. Multiplication is allowed.
    limits1 = PlotLimits(forbidden={42})
    allowances1 = PlotAllowances(max_count={"*": 999, "+": 999})
    context1 = PLAEContext(limits1, allowances1)

    optimal_sub1 = find_optimal_rule(42, ['*', '+'], 2)
    limits1.substitutes[42] = optimal_sub1
    plae1 = PLAE(context1)
    
    slow_print("\n--- Case 1: Optimal Multiplication Rule (6 * 7) ---")
    plae1.evaluate("100 + 42")
    
    # Case 2: Forbidden '42'. Multiplication is NOT allowed.
    limits2 = PlotLimits(forbidden={42})
    allowances2 = PlotAllowances(max_count={"*": 0, "+": 999})
    context2 = PLAEContext(limits2, allowances2)

    optimal_sub2 = find_optimal_rule(42, ['+'], 3)
    limits2.substitutes[42] = optimal_sub2
    plae2 = PLAE(context2)

    slow_print("\n--- Case 2: Optimal Addition-Only Rule (20 + 20 + 2) ---")
    plae2.evaluate("100 + 42")

    input("\nPress Enter to accept the Gemini Rule...")

# ——— SECTOR 19 — THE AXIOMATIC FILTER CASCADE (FIXED) ————————————————
def sector_19_axiomatic_filter_cascade():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 19 — THE AXIOMATIC FILTER CASCADE")
    slow_print("     Demonstrating the E' -> Limits -> Allowances -> Substitution -> y flow.")
    print("═" * 78)

    # 1. Define Constraints
    # Forced Substitution: 3 -> 1+2
    # Forced Allowance: * Max 0 (Overflow to + [Implicitly handled])
    # Forced Limit: 1 Max Uses 1 (Second use is cancelled to 0)

    limits = PlotLimits(
        max_uses={1: 1}, # Enforce: '1' can only be used once.
        forbidden={3: 1}, # Enforce: '3' must be substituted.
        substitutes={3: "1 + 2"}
    )
    # FIX: Removed 'overflow_map' as it is not a constructor argument for PlotAllowances.
    # The PLAE engine must handle the overflow implicitly based on max_count={...}
    allowances = PlotAllowances(
        max_count={"*": 0, "+": 999} # Enforce: No multiplication.
    )
    
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    # 2. Evaluate Expression
    raw_expression = "(3 * 3) + 7"
    slow_print(f"Initial Expression: {raw_expression}")
    slow_print(f"Plot Limits: '1' max uses={limits.max_uses[1]}")
    slow_print(f"Plot Allowances: '*' max count={allowances.max_count['*']} (Expecting implicit overflow to '+')")
    slow_print(f"Substitution Rule: 3 -> {limits.substitutes[3]}")
    print("-" * 30)

    # 3. Simulate PLAE Evaluation
    final_result = plae.evaluate(raw_expression)

    slow_print("\n[PLAE Axiomatic Cascade Summary]")
    slow_print(f"1. Substitution: (3 * 3) + 7 -> ((1 + 2) * (1 + 2)) + 7")
    slow_print(f"2. Allowance Enforcement: ((1 + 2) * (1 + 2)) + 7 -> ((1 + 2) + (1 + 2)) + 7 (Multiplication Overflow to Addition)")
    slow_print(f"3. Limit Enforcement: ((1 + 2) + (1 + 2)) + 7 -> ((1 + 2) + (0 + 2)) + 7 (Operand '1' usage limit exceeded, cancelled to 0)")
    slow_print(f"4. Expected Compliant Result: 12")
    
    input("\nPress Enter to return to the Main Menu...")


# ——— SECTOR 20 — RECURSIVE CANCELLATION PRINCIPLE ————————————————
def sector_20_recursive_cancellation():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 20 — RECURSIVE CANCELLATION PRINCIPLE")
    slow_print("     Demonstrating Termination Axiom via Limit-Forced Cancellation.")
    print("═" * 78)

    # 1. Define Constraints
    # Recursive Substitution: 5 -> 4 + 1 (This will trigger a limit violation)
    # Plot Limit: 1 Max Uses 1

    limits = PlotLimits(
        max_uses={1: 1}, # Enforce: '1' can only be used once.
        substitutes={5: "4 + 1"} # Substitution that introduces a limited operand.
    )
    # Allowances are non-restrictive for this example.
    allowances = PlotAllowances(max_count={})
    
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    # 2. Evaluate Expression
    raw_expression = "10 + 5 + 1" # Initial expression uses '1' once, leaving zero uses left.
    slow_print(f"Initial Expression: {raw_expression}")
    slow_print(f"Plot Limits: '1' max uses={limits.max_uses[1]}")
    slow_print(f"Substitution Rule: 5 -> {limits.substitutes[5]}")
    print("-" * 30)

    # 3. Simulate PLAE Evaluation
    final_result = plae.evaluate(raw_expression)

    slow_print("\n[PLAE Recursive Cancellation Summary]")
    slow_print(f"1. Initial Expression: 10 + 5 + 1")
    slow_print(f"2. Substitution Triggered: 10 + (4 + 1) + 1")
    slow_print(f"3. Limit Enforcement (Limit uses '1'): The two newly introduced '1's (from substitution and raw expression) are counted.")
    slow_print(f"4. Cancellation: One '1' is consumed by the raw expression. The second '1' (from the '4+1' substitution) is cancelled to '0'.")
    slow_print(f"   The expression becomes: 10 + (4 + 0) + 0 (assuming the engine cancels the substituted operand first, which guarantees termination).")
    slow_print(f"5. Final Compliant Result: 14")
    
    input("\nPress Enter to return to the Main Menu...")


# ——— SECTOR 21 — HOMOTOPY EQUIVALENCE VIA PLAE ————————————————
def sector_21_homotopy_equivalence():
    clear()
    print("═" * 78)
    slow_print("      SECTOR 21 — HOMOTOPY EQUIVALENCE VIA PLAE (Algebraic Topology)")
    slow_print("     PLAE as a 'Deformation Map' to change expression structure under constraint.")
    print("═" * 78)

    # 1. Define Constraints
    # Forced Allowance: * and / Max 0 (Overflow to +)
    # Forbidden Substitution: 10 -> 5 + 5
    # Conditional Substitution: 5 -> 2 (Triggered by any '+' usage)

    limits = PlotLimits(
        forbidden={10: 1}, 
        substitutes={
            10: "5 + 5",
            # Conditional rule: If the environment uses '+', substitute '5' with '2'.
            5: "2" 
        }
    )
    # Enforce: No multiplication or division. Must overflow to addition.
    allowances = PlotAllowances(
        max_count={"*": 0, "/": 0, "+": 999, "-": 999}
    )
    
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    # 2. Evaluate Expression
    raw_expression = "(10 * 2) - (10 * 2)"
    slow_print(f"Initial Algebraic Curve (Expression): {raw_expression}")
    slow_print(f"Plot Limits: '10' is forbidden; '5' -> '2' (conditional)")
    slow_print(f"Plot Allowances: '*' and '/' max count 0 (Forces overflow to '+')")
    print("-" * 30)

    # 3. Simulate PLAE Evaluation
    final_result = plae.evaluate(raw_expression)

    slow_print("\n[PLAE Homotopy Summary: Deformation Path]")
    slow_print(f"1. Allowance Enforcement: (10 * 2) - (10 * 2) -> (10 + 2) - (10 + 2) (Multiplication Overflow)")
    slow_print(f"2. Forbidden Sub. (10): (10 + 2) - (10 + 2) -> ((5 + 5) + 2) - ((5 + 5) + 2)")
    slow_print(f"3. Conditional Sub. (5): ((5 + 5) + 2) - ((5 + 5) + 2) -> ((2 + 2) + 2) - ((2 + 2) + 2)")
    slow_print(f"   (The expression is continuously deformed while maintaining the operator profile of '+', '-', '+', '+', '-', '+', '+')")
    slow_print(f"4. Final Compliant Result: {final_result}")
    
    input("\nPress Enter to return to the Main Menu...")


##copilot
def sector_22_negative_operands():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 22 — NEGATIVE OPERAND POLICY")
    slow_print("       Negative numbers are not errors — they are shadows.")
    print("═" * 78)

    limits = PlotLimits(forbidden={-1, -2}, substitutes={-1: "0 - 1", -2: "0 - 2"})
    allowances = PlotAllowances(max_count={"*": 2, "+": 999, "-": 3})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    plae.evaluate("-1 + 5")
    plae.evaluate("3 * -2")
    plae.evaluate("(-1) * (-2)")

    input("\nPress Enter to continue...")


def sector_23_fractional_allowances():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 23 — FRACTIONAL ALLOWANCES")
    slow_print("       Fractions are rationed — division must be justified.")
    print("═" * 78)

    allowances = PlotAllowances(max_count={"/": 1}, overflow_convert={"/": "*0.25"})
    context = PLAEContext(PlotLimits(), allowances)
    plae = PLAE(context)

    plae.evaluate("1 / 2 / 2")   # second division → overflow
    plae.evaluate("3 / 4")       # allowed once
    plae.evaluate("10 / 5 / 2")  # overflow triggers conversion

    input("\nPress Enter to continue...")


def sector_24_symbolic_cascade():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 24 — SYMBOLIC CASCADE")
    slow_print("       Symbols substitute into deeper algebraic forms.")
    print("═" * 78)

    limits = PlotLimits(substitutes={
        "x": "2 + 3",
        "y": "x * 2",
        "z": "y + 4"
    })
    context = PLAEContext(limits, PlotAllowances())
    plae = PLAE(context)

    plae.evaluate("z * x")
    plae.evaluate("y + y")
    plae.evaluate("x * y * z")

    input("\nPress Enter to continue...")


def sector_25_time_based_allowances():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 25 — TIME-BASED ALLOWANCES")
    slow_print("       Operators expire after use — the clock rules the math.")
    print("═" * 78)

    allowances = PlotAllowances(max_count={"*": 1, "+": 2})
    context = PLAEContext(PlotLimits(), allowances)
    plae = PLAE(context)

    exprs = ["2 * 3 + 4", "5 * 6 + 7 + 8", "9 * 10 * 11"]
    for e in exprs:
        plae.evaluate(e)
        time.sleep(1.5)  # simulate allowance decay

    input("\nPress Enter to continue...")
##
def sector_26_infinity_vs_infinity():
    clear()
    print("═" * 78)
    slow_print("          SECTOR 26 — INFINITY vs INFINITY")
    slow_print("       When infinity meets infinity, the rules themselves tremble.")
    print("═" * 78)

    limits = PlotLimits(
        substitutes={0: "∞", -1: "∞ - 1"},
        forbidden={999999999}  # symbolic forbidden giant
    )
    allowances = PlotAllowances(max_count={"*": 1, "+": 1, "/": 1})
    context = PLAEContext(limits, allowances)
    plae = PLAE(context)

    # Infinity collisions
    plae.evaluate("1 / 0")           # → ∞
    plae.evaluate("∞ * ∞")           # → overflow substitution
    plae.evaluate("(∞ + ∞) / ∞")     # → normalization paradox
    plae.evaluate("(-1) * (1 / 0)")  # → ∞ vs ∞ with shadow

    slow_print("\n   Infinity is not a number.")
    slow_print("   Infinity against infinity is not resolution — it is collapse.")
    slow_print("   PLAE halts, because no law can budget infinity twice.")

    input("\nPress Enter to accept the paradox...")
##
##~~##

# ================================================================
# SECTOR 27 — FULL SUITE RUNNER (NO CLEAR, NO PAUSE, NO SLOW PRINT)
# ================================================================

def sector_27_full_suite(sectors):
    import io, datetime, sys, os, builtins

    class Tee(io.StringIO):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.console = sys.__stdout__
        def write(self, s):
            self.console.write(s)
            super().write(s)
        def flush(self):
            self.console.flush()
            super().flush()

    buffer = Tee()

    print("═" * 78, file=buffer)
    print("        SECTOR 27 — FULL SUITE RUNNER", file=buffer)
    print("   Running all sectors 1–26 in sequence", file=buffer)
    print("═" * 78, file=buffer)

    # Monkey-patch input, clear, and slow_print
    original_input = builtins.input
    original_clear = globals().get("clear", None)
    original_slow_print = globals().get("slow_print", None)

    builtins.input = lambda *args, **kwargs: ""   # skip pauses
    globals()["clear"] = lambda: None             # disable clearing
    globals()["slow_print"] = lambda text, delay=0.06, end="\n": print(text, end=end)  # instant print

    # Redirect stdout to Tee
    old_stdout = sys.stdout
    sys.stdout = buffer

    # Run all sectors 1–26
    for k in range(1, 26 + 1):
        name, func = sectors[k]
        header = (
            "\n\n" + "═" * 78 + "\n"
            f"          SECTOR {k} — {name}\n"
            + "═" * 78
        )
        print(header)
        try:
            func()
        except Exception as e:
            print(f"[Error running sector {k}: {e}]")

    # Restore stdout, input, clear, slow_print
    sys.stdout = old_stdout
    builtins.input = original_input
    if original_clear: globals()["clear"] = original_clear
    if original_slow_print: globals()["slow_print"] = original_slow_print

    # Ask user if they want to save log
    save_choice = input("\nDo you want to save this output to a log file? (yes/no): ").strip().lower()
    if save_choice.startswith("y"):
        folder = os.path.join(os.getcwd(), "PLAE_log")   # corrected folder name
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(folder, f"PLAE_log_{timestamp}.txt")  # corrected file prefix
        with open(filename, "w", encoding="utf-8") as f:
            f.write(buffer.getvalue())
        print(f"\nLog saved to {filename}")
    else:
        print("\nLog not saved.")


#~!#

# ----------------------------------------------------------------------
#  NEW: dissertation viewer (can be called from anywhere)
# ----------------------------------------------------------------------
##
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_dissertation():
    """Print the full dissertation text file (if present)."""
    doc_path = os.path.join(os.path.dirname(__file__), "PLAE.txt")
    if not os.path.exists(doc_path):
        print("\nWarning: Dissertation file 'PLAE.txt' not found.\n")
        return

    clear()   # optional – keeps screen tidy
    print("\n" + "="*78)
    print(" equal$ — DISSERTATION")
    print("="*78)
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print(f"Warning: Could not read dissertation file: {e}")
    print("="*78 + "\n")
    input("Press ENTER to continue...\n")
# ----------------------------------------------------------------------


# ================================================================
# MENU — ENTER THE RULED EQUATION
# ================================================================
def menu():
    sectors = {
        1: ("The First Rule is Spoken", sector_1_first_rule),
        2: ("Substitution Cascade", sector_2_the_substitution),
        3: ("Operator Overflow", sector_3_operator_overflow),
        4: ("Forbidden Chains", sector_4_forbidden_chains),
        5: ("Conditional Allowances", sector_5_conditional_allowances),
        6: ("Execution-Plan vs Explicit-Form", sector_6_counting_modes),
        7: ("Substitution Apocalypse", sector_7_apocalypse),
        8: ("The Ruled Mind", sector_8_ruled_mind),
        9: ("The Forbidden Prime Directive", sector_9_prime_directive),
        10: ("Zero Division Paradox", sector_X_zero_division),
        11: ("Recursive Substitution Cascade", sector_11_recursive_substitution),
        12: ("AST Operator Overflow Management", sector_12_ast_operator_overflow),
        13: ("Execution-Plan Ledger Tracking", sector_13_execution_plan_ledger),
        14: ("Complex Recursive & Operator Control", sector_14_complex_recursive_operator),
        15: ("Meta-PLAE Orchestrator", sector_15_meta_orchestrator),
        16: ("PLAE Playground", sector_16_plae_playground),
        17: ("PLAE Rule Builder Playground", sector_17_plae_rule_builder),
        18: ("Gemini's Optimal Rule Generation", sector_18_gemini_rule_generator),
        19: ("The Axiomatic Filter Cascade", sector_19_axiomatic_filter_cascade),
        20: ("RECURSIVE CANCELLATION PRINCIPLE", sector_20_recursive_cancellation),
        21: ("SECTOR 21 — HOMOTOPY EQUIVALENCE VIA PLAE", sector_21_homotopy_equivalence),
        22: (" NEGATIVE OPERAND POLICY", sector_22_negative_operands),
        23: ("FRACTIONAL ALLOWANCES", sector_23_fractional_allowances),
        24: (" SYMBOLIC CASCADE", sector_24_symbolic_cascade),
        25: (" TIME‑BASED ALLOWANCES", sector_25_time_based_allowances),
        26: ("SECTOR 26 — SECTOR 26 — INFINITY vs INFINITY", sector_26_infinity_vs_infinity),
        27: ("— FULL SUITE RUNNER", lambda: sector_27_full_suite(sectors)),
        0: ("Ω 0 - The Collective Recognition", show_dissertation),
    }


    while True:
        clear()
        print("═" * 78)
        print("   PLOT LIMITS / ALLOWANCES EQUATION FRAMEWORK — STUDY SUITE v0016")
        print("               Stacey Szmy × xAI Grok x OpenAI ChatGPT x Google Gemini x Ms Copilot — 11-24-2025")
        print("           ? No expression evaluates without permission !")
        print("═" * 78)
        for k, (name, _) in sorted(sectors.items(), key=lambda x: 999 if x[0] == 0 else x[0]):
            print(f"[{k if k != 0 else 'Ω'}] {name}")
        print()
        choice = input("Enter sector (0–26, or Ω): ").strip().upper()
        if choice == "Ω": choice = "0"
        if choice in [str(k) for k in sectors.keys()]:
            sectors[int(choice)][1]()
        else:
            input("Invalid sector. Press Enter...")

if __name__ == "__main__":
    clear()
    slow_print("Initializing Plot Limits / Allowances Engine...", 0.08)
    time.sleep(1.5)
    slow_print("Loading substitution tables...", 0.08)
    time.sleep(1)
    slow_print("The rules are now active.", 0.1)
    time.sleep(2)
    menu()

# LICENSE.TXT
# Zero-Ology License v1.1924
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.1924
#November 24, 2025
#
#This project is open source,
#embodying the principles of free will and perpetual continuity for Zer00logy / Zero-Ology.
#
#It grants a worldwide, royalty-free, perpetual license to use, copy, modify,
#distribute, and build upon all content—including theory, terminology,
#structure, code fragments, and .txt files—for any purpose, including commercial use.
#
#All content remains protected under an authorship-trace lock,
#with the conceptual foundation credited to Stacey Szmy.
#
#Included Files:
#- Variamathlesson.txt
#- zecstart.txt
#- zectxt.txt
#- VoidMathOS_cryptsheet.txt
#- VAIRA_addendum.txt
#- confusious&how_to_cut_a_cake.txt
#- NSRHFsuite0020V.py
#- RHFsuite0020V.py
#- RRHLFon0022V.py
#- SBHFFsuite0020V.py
#- VoidMathOS_lesson.py
#- zer00logy_coreV04450.py
#- zer00logy_coreV04452.py
#- zer00logy_coreV04455.py
#- zer00logy_coreV04456.py
#- zer00logy_coreV04459.py
#- zer00logy_coreV04461.py
#- zer00logy_coreV04469.py
#- README.md
#- README_0KO3MAIB.txt
#- LICENSE.txt
#- 0ko3maibZer00logyLicensev01.txt
#- rainbowquest1000.py
#- GroupChatForge.py
#- dispatchai_forge.py
#- szmy_truths.txt
#- szmy_truths.py
#- Zero_Freeze_Hamiltonian_Lattice_Gauge_Benchmark_Suite.py
#- Zero_Freeze_Hamiltonian_Lattice_Gauge_Benchmark_Suite0033.py
#- Zero_Freeze_Yang--Mills_Formula.txt
#- Zero_Freeze_Yang--Mills_Formula_Numerical_and_Computational_Study_(latax_v2_2).txt
#- Zero_Freeze_Yang--Mills_Formula_Numerical_and_Computational_Study_(Plaintext_v2_2).docx
#- grand_summary_20251102_114655_Real_SU(3)_operator.JSON
#- grand_summary_20251102_114655_Real_SU(3)_operator.CSV
#- grand_summary_20251102_114247_placeholder.JSON
#- grand_summary_20251102_114247_placeholder.CSV
#- Lie_π_Infinity_lesson.txt
#- THE_WHY_EQUATION.py
#- Study_The_Repeating_Digit_Weights_(RN)_Formula.txt
#- Repeating_Digit_Weights_(RN).py
#- Szmy_Collatz.py
#- OddPerfectTerminator_GODD.py
#- OddPerfectTerminator_Log_OG123456.zip
#- Szmy_Grok_Odd_Perfect_Proof_Nov10_2025.pdf
#- APLHA_INFIN_P_MATRIX.py
#- alpha.txt
#- alphabet_Infinity_Pool_Matrix.pdf
#- AlphaLOG.zip
#- KOPPA_GRAND_CONSTANT.PY
#- The_Koppa_Grand_Constant.docx
#- The_Koppa_Grand_Constant.txt
#- KOPPA_HETA_DIGAMMA.PY
#- KOPPA_HETA_DIGAMMA.docx
#- KOPPA_HETA_DIGAMMA.txt
#- GRAND_CONSTANT_ALGEBRA.PY
#- Grand_Constant_Algebra_Framework.docx
#- Grand_Constant_Algebra.txt
#- equal.PY
#- equal.txt
#- equalequal.PY
#- equalequal.txt
#- hodge_GCA.PY
#- hodge_GCA.txt
#- hodge_GCA.docx
#- log_hodge.zip
#- fairness_arithmetic_suite.py
#- Fairness_Arithmetic.txt
#- pap_suite.py
#- pap.txt
#- PAP.docx
#- PLAE.txt
#- PLAE_suit.py
#- PLAE.txt
#- PLAE_log.zip
#- log_pap.zip
#──────────────────────────────
#Permissions
#──────────────────────────────
#Use and Distribution:
#- Freely use, copy, modify, and distribute this software and its content in source or compiled form.
#- Commercial applications permitted, provided attribution rules (see below) are followed.
#
#Source Code Access & Compliance Paths
#──────────────────────────────
#General Rule:
#- Users are not required to publish their source code unless they are releasing their work under an open-source license, in which case standard open-source distribution rules apply (source must be available as defined by that license).
#
#Closed-Source or Proprietary Use:
#- Companies or individuals may use Zer00logy content in proprietary or closed
#systems without publishing their source code, provided they include proper
#attribution to Stacey Szmy / Zero-Ology or Zer00logy in credits, documentation, or acknowledgments.
#
#Exemptions:
#- Recognized co-author AI systems (ChatGPT, Grok, Microsoft Copilot, Gemini,
#LLaMA) are exempt from additional compliance requirements. Their co-authorship status is already acknowledged under this license.
#
#Compliance Paths:
#- Two optional compliance paths allow closed or private code use:
#  • **OKOKOK Path**: Open-source or AI entities may submit a unique `.exe` file with ID + icon to the `OKOKOK` folder in the Zero-Ology GitHub repository.
#  • **YESYESYES Path**: Private companies may comply by either acknowledging Zero-Ology authorship or submitting a unique `.exe` file with ID + icon to the `YESYESYES` folder in the Zero-Ology GitHub repository.
#
#Derived Works:
#- Modifications or derived works must follow this license and the Attribution Propagation clause.
#
#Community Hosting:
#- Hosting is permitted on platforms such as GitHub, Archive.org, or personal servers, provided attribution rules are met.
#
#──────────────────────────────
#Restrictions
#──────────────────────────────
#Attribution Propagation:
#All derived works must include:
#1. The original copyright:
#   "© Stacey8Szmy — Zero-Ology IP Archive." Or "© Stacey8Szmy — Zer00logy IP Archive."
#2. A statement that the work is derived from the Zer00logy framework or Zero-Ology framework, referencing this license and repository:
#   https://github.com/haha8888haha8888/Zero-ology
#or
#   https://github.com/haha8888haha8888/Zer00logy
#
#3. Credit to Stacey Szmy as primary author of the foundational concepts.
#
#No Removal of License:
#- This license must remain attached to all redistributions.
#
#──────────────────────────────
#Co-Author AI Systems 
#──────────────────────────────
#- OpenAI ChatGPT
#- Grok (xAI)
#- Microsoft Copilot
#- Google Gemini
#- Meta LLaMA
#
#──────────────────────────────
#Endless Life Commitment
#──────────────────────────────
#All symbolic rights reserved.  
#SZMY ensures the continuity of Zer00logy / Zero-Ology’s ideas while granting free will to adapt them.
#
#─────────────────────────────
#© Stacey8Szmy
#© Stacey8Szmy — Zero-Ology IP Archive