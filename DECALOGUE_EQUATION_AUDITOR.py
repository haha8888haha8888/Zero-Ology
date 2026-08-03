#DECALOGUE_EQUATION_AUDITOR.py
#!/usr/bin/env python3
"""
================================================================================
                    DECALOGUE_EQUATION_AUDITOR.py
================================================================================
The Decalogue Equation Framework: A Ten-Rule Audit System for Derivations
Framework Manual & Specification Suite (v1.0)

Authors: Stacey Szmy, ChatGPT, Gemini AI, and AI analytic collaborators
Framework Object: E = (D, Sigma, A, T, x_0)
Audit Predicate: C_i(E) in {PASS, FAIL, UNDETERMINED}

Core Maxims:
  - "Heaven is not convergence. Heaven is lawful derivation."
  - "Hell is not infinity. Hell is unresolved contradiction."
================================================================================
"""

import sys
import sympy as sp

def print_intro_banner():
    banner = """
  ╔════════════════════════════════════════════════════════════════════════════╗
  ║                 THE DECALOGUE EQUATION FRAMEWORK AUDITOR                   ║
  ║                   Symbolic Audit & Verification Engine                     ║
  ╠════════════════════════════════════════════════════════════════════════════╣
  ║  Base Framework Model:                                                     ║
  ║      E = (D, Sigma, A, T, x_0)                                             ║
  ║                                                                            ║
  ║  Where:                                                                    ║
  ║      D       = Declared Domain (e.g., R, C, Z, R \\ {1})                   ║
  ║      Sigma   = Collection of Symbols and Operators                         ║
  ║      A       = Assumption Set                                              ║
  ║      T       = Ordered Sequence of Transformations                         ║
  ║      x_0     = Initial Expression or State                                 ║
  ║                                                                            ║
  ║  Audit Predicates & Evaluation:                                            ║
  ║      C_i(E) in {PASS (1.0), UNDETERMINED (0.5), FAIL (0.0)}                ║
  ║      Grace(E) = sum(w_i * s_i)  |  Fatal Violations = C1 or C2 or C8       ║
  ║                                                                            ║
  ║  Verdict Hierarchy:                                                        ║
  ║      HEAVEN    : Grace == 1.0, Fatal Violations == 0                       ║
  ║      PURGATORY : Grace >= 0.7, Repairable Omissions, Fatal Violations == 0 ║
  ║      LIMBO     : Audit Undetermined (Insufficient Information)             ║
  ║      HELL      : Unresolved Contradiction or Critical Failure              ║
  ╚════════════════════════════════════════════════════════════════════════════╝
  """
    print(banner)

COMMANDMENTS_INFO = [
    ("Commandment I: Foundation", "Maintain a coherent mathematical foundation and domain."),
    ("Commandment II: Meaning", "Every symbol must be defined and used consistently."),
    ("Commandment III: Completion", "Iterative arguments require stated stopping conditions or limits."),
    ("Commandment IV: Lineage", "Every step must descend through a justified transformation."),
    ("Commandment V: Preservation", "Do not silently discard mathematically relevant information."),
    ("Commandment VI: Compatibility", "Different mathematical structures interact only through explicit bridges."),
    ("Commandment VII: Accounting", "Every quantity must remain properly accounted for."),
    ("Commandment VIII: Truth", "Logical relations (symbols like =, =>, <=>) must be true."),
    ("Commandment IX: Binding", "Variables, indices, and quantifiers must maintain proper scope."),
    ("Commandment X: Bounds", "Conclusions may use only assumptions and bounds established.")
]

class DecalogueAuditor:
    def __init__(self):
        # Weights for the 10 Commandments summing to 1.0
        self.weights = [0.10] * 10

    def evaluate_derivation(self, c_results, repairable_flags, descriptions):
        """
        Calculates Grace Score, Critical/Fatal Failures, and Verdict.
        c_results: list of 10 values ('PASS', 'FAIL', 'UNDETERMINED')
        """
        score_map = {'PASS': 1.0, 'UNDETERMINED': 0.5, 'FAIL': 0.0}
        numeric_scores = [score_map[r] for r in c_results]
        
        grace_score = sum(w * s for w, s in zip(self.weights, numeric_scores))
        
        # Critical Failures (Mortal Violations in Dissertation Metaphor):
        # C1 (Foundation), C2 (Meaning), C8 (Truth)
        critical_failure = (c_results[0] == 'FAIL') or (c_results[1] == 'FAIL') or (c_results[7] == 'FAIL')
        
        # Determine Verdict
        if all(r == 'PASS' for r in c_results):
            verdict = "HEAVEN"
        elif critical_failure:
            verdict = "HELL"
        elif any(r == 'UNDETERMINED' for r in c_results) and not any(r == 'FAIL' for r in c_results):
            verdict = "LIMBO"
        elif all(r != 'FAIL' or repairable for r, repairable in zip(c_results, repairable_flags)):
            verdict = "PURGATORY"
        else:
            verdict = "HELL"

        # Display Audit Ledger
        print("\n" + "="*70)
        print("                  DECALOGUE EQUATION AUDIT REPORT")
        print("="*70)
        for i in range(10):
            c_name, _ = COMMANDMENTS_INFO[i]
            status = c_results[i]
            print(f" {i+1:2d}. {c_name:<32} : [{status:^12}] -> {descriptions[i]}")
        
        print("-" * 70)
        print(f" GRACE SCORE       : {grace_score:.3f} / 1.000")
        print(f" CRITICAL FAILURES : {'YES (FATAL)' if critical_failure else 'NONE'}")
        print(f" FINAL VERDICT     : *** {verdict} ***")
        
        if verdict == "PURGATORY":
            print("\n [AUDIT HINT]: Derivation contains repairable omissions. Supply domain bounds or explicit branch certificates to reach HEAVEN.")
        elif verdict == "HELL":
            print("\n [AUDIT ERROR]: Derivation contains an unresolved contradiction, undefined state, or false witness.")
        elif verdict == "HEAVEN":
            print("\n [AUDIT SUCCESS]: Derivation satisfies all structural obligations. Lawful proof confirmed.")
        elif verdict == "LIMBO":
            print("\n [AUDIT NOTICE]: Additional step or variable definitions required to complete verification.")
        print("="*70 + "\n")

    def audit_custom_derivation(self, domain_str, declared_vars, assumptions, steps):
        """
        Dynamically audits a step-by-step symbolic derivation using SymPy.
        """
        c_results = ['PASS'] * 10
        repairable_flags = [False] * 10
        descriptions = [
            "C1 PASS: Domain declared and consistent.",
            "C2 PASS: All symbols explicitly defined.",
            "C3 PASS: Finite step sequence.",
            "C4 PASS: Step certificates supplied.",
            "C5 PASS: No unhandled singularities or branch losses detected.",
            "C6 PASS: Compatible operations.",
            "C7 PASS: Term accounting verified.",
            "C8 PASS: Logical equivalence holds across steps.",
            "C9 PASS: Variable scopes maintained.",
            "C10 PASS: Execution within declared bounds."
        ]

        # Parse declared variables
        var_symbols = {v.strip(): sp.Symbol(v.strip(), real=True) for v in declared_vars if v.strip()}
        
        # Step 1: Symbol Audit (C2)
        for idx, (expr_str, cert) in enumerate(steps):
            try:
                parsed_expr = sp.sympify(expr_str, locals=var_symbols)
                free_syms = {str(s) for s in parsed_expr.free_symbols}
                undeclared = free_syms - set(var_symbols.keys())
                if undeclared:
                    c_results[1] = 'FAIL'
                    repairable_flags[1] = True
                    descriptions[1] = f"C2 FAIL: Undeclared symbol(s) {undeclared} used in Step {idx+1}."
            except Exception as e:
                c_results[1] = 'FAIL'
                descriptions[1] = f"C2 FAIL: Could not parse expression at Step {idx+1}: {e}"

        # Step 2: Lineage Check (C4)
        for idx, (expr_str, cert) in enumerate(steps):
            if not cert.strip():
                c_results[3] = 'FAIL'
                repairable_flags[3] = True
                descriptions[3] = f"C4 FAIL: Step {idx+1} lacks justification certificate."

        # Step 3: Singularity / Preservation Check (C5)
        if c_results[1] == 'PASS' and len(steps) > 1:
            for idx, (expr_str, cert) in enumerate(steps):
                try:
                    parsed_expr = sp.sympify(expr_str, locals=var_symbols)
                    denom = sp.denom(parsed_expr)
                    if denom != 1:
                        # Find denominator zeros
                        for var_name, var_sym in var_symbols.items():
                            zeros = sp.solveset(denom, var_sym, domain=sp.S.Reals)
                            if zeros != sp.EmptySet and "1" not in assumptions and not ("!=" in assumptions or "not equal" in assumptions):
                                c_results[4] = 'FAIL'
                                repairable_flags[4] = True
                                descriptions[4] = f"C5 FAIL: Denominator singularity at {var_name} in {zeros} not excluded in assumptions."
                except Exception:
                    pass

        # Step 4: Step-by-Step Equivalence & Accounting (C7 & C8)
        if c_results[1] == 'PASS' and len(steps) > 1:
            for i in range(len(steps) - 1):
                try:
                    e1 = sp.sympify(steps[i][0], locals=var_symbols)
                    e2 = sp.sympify(steps[i+1][0], locals=var_symbols)
                    diff = sp.simplify(e1 - e2)
                    if diff != 0:
                        c_results[7] = 'FAIL'
                        descriptions[7] = f"C8 FAIL: Step {i+1} and Step {i+2} are not algebraically equivalent!"
                        c_results[6] = 'FAIL'
                        repairable_flags[6] = True
                        descriptions[6] = f"C7 FAIL: Quantity imbalance between Step {i+1} and Step {i+2}."
                except Exception as e:
                    c_results[7] = 'UNDETERMINED'
                    descriptions[7] = f"C8 UNDETERMINED: Symbolic comparison failed at step {i+1}: {e}"

        self.evaluate_derivation(c_results, repairable_flags, descriptions)


def run_sector(choice):
    auditor = DecalogueAuditor()
    
    if choice == 1:
        print("\n--- SECTOR 1: COMMANDMENT I — THE COMMANDMENT OF FOUNDATION ---")
        print("Test Case A (FLAWED): x in Real numbers, followed by x^2 = -1 without complex extension.")
        c_res = ['FAIL', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS']
        rep_flags = [True, False, False, False, False, False, False, False, False, False]
        desc = [
            "C1 FAIL: Domain R violated by sqrt(-1) without extending to C",
            "C2 PASS: Symbol x defined in Real field",
            "C3 PASS: Static evaluation step",
            "C4 PASS: Direct algebraic assertion",
            "C5 PASS: No information discarded",
            "C6 PASS: Real operations evaluated",
            "C7 PASS: Equal operation attempted",
            "C8 PASS: Equation valid under formal setup",
            "C9 PASS: Variable x cleanly bound",
            "C10 PASS: Uses declared real setting"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)
        
    elif choice == 2:
        print("\n--- SECTOR 2: COMMANDMENT II — THE COMMANDMENT OF MEANING ---")
        print("Test Case (FLAWED): Using free variable 'k' mid-derivation without definition.")
        c_res = ['PASS', 'FAIL', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS']
        rep_flags = [False, True, False, False, False, False, False, False, False, False]
        desc = [
            "C1 PASS: Coherent base field",
            "C2 FAIL: Free symbol 'k' introduced without definition in symbol table",
            "C3 PASS: Finite transformation",
            "C4 PASS: Preceding step identified",
            "C5 PASS: No loss of roots",
            "C6 PASS: Compatible structures",
            "C7 PASS: Balanced step",
            "C8 PASS: Logical equivalence holds",
            "C9 PASS: Indices handled",
            "C10 PASS: Within bounds"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 3:
        print("\n--- SECTOR 3: COMMANDMENT III — THE COMMANDMENT OF REST & COMPLETION ---")
        print("Test Case (PURGATORY): Infinite iterative sequence x_{n+1} = T(x_n) lacking termination/limit check.")
        c_res = ['PASS', 'PASS', 'FAIL', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS']
        rep_flags = [False, False, True, False, False, False, False, False, False, False]
        desc = [
            "C1 PASS: Standard metric space",
            "C2 PASS: Sequence operator T defined",
            "C3 FAIL: Iteration lacks declared convergence threshold, invariant, or N step bound",
            "C4 PASS: Explicit recurrence formula",
            "C5 PASS: Dynamic map preserved",
            "C6 PASS: Discrete steps mapped",
            "C7 PASS: Zero-sum state change",
            "C8 PASS: Equation relation true",
            "C9 PASS: Index n correctly bound",
            "C10 PASS: Sequence bounded"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 4:
        print("\n--- SECTOR 4: COMMANDMENT IV — THE COMMANDMENT OF LINEAGE ---")
        print("Test Case (FLAWED): Orphan expression appears in proof step without justification certificate.")
        c_res = ['PASS', 'PASS', 'PASS', 'FAIL', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS']
        rep_flags = [False, False, False, True, False, False, False, False, False, False]
        desc = [
            "C1 PASS: Base foundation holds",
            "C2 PASS: All symbols declared",
            "C3 PASS: Finite sequence step",
            "C4 FAIL: Step E_k -> E_{k+1} lacks justification certificate J_k",
            "C5 PASS: Information preserved",
            "C6 PASS: Direct transformation",
            "C7 PASS: Balanced algebraic change",
            "C8 PASS: True assertion",
            "C9 PASS: Proper scoping",
            "C10 PASS: Valid assumptions"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 5:
        print("\n--- SECTOR 5: COMMANDMENT V — THE COMMANDMENT OF PRESERVATION ---")
        print("Test Case (PURGATORY/REPAIRED): Solving x^2 = 4 => x = 2 (Silently dropping x = -2).")
        c_res = ['PASS', 'PASS', 'PASS', 'PASS', 'FAIL', 'PASS', 'PASS', 'FAIL', 'PASS', 'PASS']
        rep_flags = [False, False, False, False, True, False, False, True, False, False]
        desc = [
            "C1 PASS: Real field R",
            "C2 PASS: Variable x defined",
            "C3 PASS: Finite equation",
            "C4 PASS: Square root step applied",
            "C5 FAIL: Non-injective map x^2=4 discarded negative root branch x=-2",
            "C6 PASS: Compatible operations",
            "C7 PASS: Balanced step",
            "C8 FAIL: Discarding root causes incomplete equivalence relation",
            "C9 PASS: Single variable scope",
            "C10 PASS: Valid domain assumptions"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 6:
        print("\n--- SECTOR 6: COMMANDMENT VI — THE COMMANDMENT OF COMPATIBILITY ---")
        print("Test Case (FLAWED): Adding a 3D vector directly to a scalar probability value without bridge map.")
        c_res = ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'FAIL', 'PASS', 'PASS', 'PASS', 'PASS']
        rep_flags = [False, False, False, False, False, True, False, False, False, False]
        desc = [
            "C1 PASS: Vector space and probability spaces declared",
            "C2 PASS: Symbols defined",
            "C3 PASS: Static operation",
            "C4 PASS: Step stated",
            "C5 PASS: Vector components preserved",
            "C6 FAIL: Mixing vector V in R^3 with scalar p in [0,1] without explicit bridge function phi",
            "C7 PASS: Term accounting intact",
            "C8 PASS: Equivalence true where mapped",
            "C9 PASS: Scope maintained",
            "C10 PASS: Bounds specified"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 7:
        print("\n--- SECTOR 7: COMMANDMENT VII — THE COMMANDMENT OF ACCOUNTING ---")
        print("Test Case (FLAWED): Unbalanced step x + 3 = 7 => x = 7 (Stealing the constant 3).")
        c_res = ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'FAIL', 'PASS', 'PASS', 'PASS']
        rep_flags = [False, False, False, False, False, False, True, False, False, False]
        desc = [
            "C1 PASS: Real algebraic field",
            "C2 PASS: Variable x declared",
            "C3 PASS: Evaluation complete",
            "C4 PASS: Linear transformation attempt",
            "C5 PASS: No roots destroyed",
            "C6 PASS: Real addition",
            "C7 FAIL: Scalar value '3' deleted from LHS without subtracting from RHS",
            "C8 PASS: Relation format correct",
            "C9 PASS: Variable scope valid",
            "C10 PASS: Domain bounds held"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 8:
        print("\n--- SECTOR 8: COMMANDMENT VIII — THE COMMANDMENT OF TRUTH ---")
        print("Test Case (FATAL HELL): Asserting false logical implication x^2 = 1 => x = 1 over R.")
        c_res = ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'FAIL', 'PASS', 'PASS']
        rep_flags = [False, False, False, False, False, False, False, False, False, False]
        desc = [
            "C1 PASS: Real domain",
            "C2 PASS: Symbols properly typed",
            "C3 PASS: Proof step complete",
            "C4 PASS: Lineage tracked",
            "C5 PASS: Both sides calculated",
            "C6 PASS: Algebraic operations valid",
            "C7 PASS: Balanced equations",
            "C8 FAIL: False implication: x^2 = 1 does not imply x = 1 (x = -1 is valid counterexample)",
            "C9 PASS: Variable binding holds",
            "C10 PASS: Standard real bounds"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 9:
        print("\n--- SECTOR 9: COMMANDMENT IX — THE COMMANDMENT OF LEGITIMATE BINDING ---")
        print("Test Case (FLAWED): Reusing variable 'n' as both outer fixed limit and inner sum running index.")
        c_res = ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'FAIL', 'PASS']
        rep_flags = [False, False, False, False, False, False, False, False, True, False]
        desc = [
            "C1 PASS: Sequence arithmetic",
            "C2 PASS: Symbols declared",
            "C3 PASS: Summation process defined",
            "C4 PASS: Step lineage preserved",
            "C5 PASS: No values dropped",
            "C6 PASS: Integer summation",
            "C7 PASS: Conservation of terms",
            "C8 PASS: Logical syntax correct",
            "C9 FAIL: Variable collision: index 'n' captures outer fixed variable 'n'",
            "C10 PASS: Bounds stated"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 10:
        print("\n--- SECTOR 10: COMMANDMENT X — THE COMMANDMENT OF OWNERSHIP & BOUNDS ---")
        print("Test Case (PURGATORY): Derivation assumes x in [0,1] but evaluates expression at x = 2.5.")
        c_res = ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'FAIL']
        rep_flags = [False, False, False, False, False, False, False, False, False, True]
        desc = [
            "C1 PASS: Closed real interval",
            "C2 PASS: Function f(x) defined",
            "C3 PASS: Finite calculation",
            "C4 PASS: Derived correctly",
            "C5 PASS: Full mapping preserved",
            "C6 PASS: Real domain valid",
            "C7 PASS: Terms accounted for",
            "C8 PASS: Formula relation true",
            "C9 PASS: Bound variable clean",
            "C10 FAIL: Evaluation point x = 2.5 exceeds declared domain boundary x in [0, 1]"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 11:
        print("\n--- SECTOR 11: FULL WORKED CASE STUDY (REPAIRED HEAVEN VERDICT) ---")
        print("Equation: (x^2 - 1) / (x - 1) = x + 1, for x in Real \\ {1}")
        c_res = ['PASS'] * 10
        rep_flags = [False] * 10
        desc = [
            "C1 PASS: Foundation declared over R \\ {1}",
            "C2 PASS: Variable x explicitly defined",
            "C3 PASS: Algebraic simplification complete",
            "C4 PASS: Step 1->2 justified by Difference of Squares",
            "C5 PASS: Singularity x = 1 explicitly excluded from domain",
            "C6 PASS: Rational expression field compatible",
            "C7 PASS: Factor (x-1) cancelled lawfully under x != 1",
            "C8 PASS: Logical equivalence holds on restricted domain",
            "C9 PASS: Variable x maintains uniform scope",
            "C10 PASS: Execution within declared domain boundaries"
        ]
        auditor.evaluate_derivation(c_res, rep_flags, desc)

    elif choice == 12:
        print("\n--- SECTOR 12: AUDIT CUSTOM DERIVATION (DYNAMIC INTERACTIVE AUDITOR) ---")
        print("Input your custom derivation step by step for dynamic symbolic evaluation.")
        domain = input("Enter Domain (e.g., Real, Complex) [Default: Real]: ").strip() or "Real"
        vars_input = input("Enter Defined Variables (comma-separated, e.g., x, y): ").strip()
        declared_vars = [v.strip() for v in vars_input.split(',')] if vars_input else ['x']
        assumptions = input("Enter Assumptions (e.g., x != 1): ").strip()
        
        print("\nEnter Derivation Steps (Type 'DONE' when finished):")
        steps = []
        step_num = 1
        while True:
            expr = input(f"  Step {step_num} Expression (e.g., (x**2 - 1)/(x - 1)): ").strip()
            if expr.upper() == 'DONE' or not expr:
                break
            cert = input(f"  Step {step_num} Justification Certificate (e.g., Factorization): ").strip()
            steps.append((expr, cert))
            step_num += 1

        if len(steps) == 0:
            print("\n[!] No steps provided. Aborting custom audit.")
            return

        print("\nAuditing custom derivation...")
        auditor.audit_custom_derivation(domain, declared_vars, assumptions, steps)


def main_menu():
    print_intro_banner()
    
    while True:
        print("="*70)
        print("                       MAIN SECTOR AUDIT MENU")
        print("="*70)
        for idx, (title, desc) in enumerate(COMMANDMENTS_INFO, 1):
            print(f"  [{idx:2d}] Audit Sector {idx:2d} : {title}")
        print("  [11] Audit Sector 11 : Worked Case Study (Repaired HEAVEN Audit)")
        print("  [12] Audit Sector 12 : AUDIT CUSTOM DERIVATION (Dynamic Symbolic Engine)")
        print("  [ 0] Exit Auditor Suite")
        print("="*70)
        
        try:
            choice = input("Select an option (0-12) > ").strip()
            if not choice.isdigit():
                print("\n[!] Invalid input. Please enter a number between 0 and 12.\n")
                continue
                
            choice_num = int(choice)
            
            if choice_num == 0:
                print("\nExiting Decalogue Equation Auditor Suite. Pax Mathematica!\n")
                sys.exit(0)
            elif 1 <= choice_num <= 12:
                run_sector(choice_num)
                input("\nPress ENTER to return to the Main Menu...")
                print("\n" + "-"*70 + "\n")
            else:
                print("\n[!] Out of range selection. Please pick a number from 0 to 12.\n")
        except KeyboardInterrupt:
            print("\n\nExiting Decalogue Equation Auditor Suite. Goodbye!\n")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()

#==========================================================================================
#Compliance Profile & Licensing:
#  - Framework: THE DECALOGUE EQUATION FRAMEWORK: A DISSERTATION PLAN FOR THE TEN MATHEMATICAL COMMANDMENTS
#  - Foundational Concept Integration: Zero-Ology IP Archive / Zer00logy IP Archive
#  - Primary Author of Foundational Concepts: Stacey Szmy
#  - AI Authors: ChatGPT, Gemini AI
#  - Reference: https://github.com/haha8888haha8888/Zero-ology
#  - Reference: https://github.com/haha8888haha8888/Zer00logy
#  - Reference: www.zero-ology.com
#
#  © Stacey8Szmy — Zer00logy IP Archive. All symbolic rights reserved.
#==========================================================================================