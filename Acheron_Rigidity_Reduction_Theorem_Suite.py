#Acheron_Rigidity_Reduction_Theorem_Suite.py
#
#!/usr/bin/env python3
"""
==========================================================================================
   ACHERON_RIGIDITY_INTEGRATED_SUITE.py (v1.0.1-RELEASE)
==========================================================================================
PROVEN THEOREM & SYSTEM CONTROLLER:
    Consolidates the core engine, verification assertions, and multi-modulus 
    exploration vectors into a unified, interactive execution environment.
    
    Verifies that the geometric ~65.93% STABLE control baseline observed in the Acheron 
    framework is a deterministic consequence of the interaction between the RN_M 
    denominator 9 and the primorial twin-prime admissible anchor residue structure.

Author: Stacey Szmy
AI Analytic Co-contributors: Claude, ChatGPT, Gemini, Microsoft Copilot, Grok
Project: Zer00logy / Acheron Twin Prime Residue–Rigidity Framework
==========================================================================================
==========================================================================================
Compliance Profile & Licensing:
  - Framework: Acheron Rigidity Reduction Theorem
  - Foundational Concept Integration: Zero-Ology IP Archive / Zer00logy Framework
  - Primary Author of Foundational Concepts: Stacey Szmy
  - Technical Framework Lineage: RN Formula Solution / Acheron Fields / Acheron Fragmentation
  - Reference: https://github.com/haha8888haha8888/Zero-ology
  - Reference: https://github.com/haha8888haha8888/Zer00logy
  - Reference: www.zero-ology.com

  © Stacey8Szmy — Zer00logy IP Archive. All symbolic rights reserved.
==========================================================================================
"""

import sys
import math
from collections import defaultdict

# ========================================================================================
# 1. CORE ANALYTICAL RIGIDITY ENGINE
# ========================================================================================
class AcheronRigidityEngine:
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19]

    def __init__(self, modulus_index: int, gate_lower: float = 0.15, gate_upper: float = 0.85):
        """
        Initializes the rigidity engine for a specific primorial wheel index.
        index=1: M=6 (2*3)
        index=2: M=30 (2*3*5)
        index=3: M=210 (2*3*5*7)
        index=4: M=2310 (2*3*5*7*11)
        """
        if modulus_index < 1 or modulus_index > len(self.PRIMES):
            raise ValueError(f"Modulus index must map to available primorial depth (1 to {len(self.PRIMES)}).")
            
        self.wheel_primes = self.PRIMES[:modulus_index + 1]
        self.modulus = math.prod(self.wheel_primes)
        self.gate_lower = gate_lower
        self.gate_upper = gate_upper

    def compute_admissible_anchor_classes(self) -> list:
        """
        Computes the set A_M of residue classes r mod M where both (r-1) and (r+1)
        are coprime to the primorial modulus M.
        """
        admissible_set = []
        for r in range(self.modulus):
            if all((r - 1) % p != 0 and (r + 1) % p != 0 for p in self.wheel_primes):
                admissible_set.append(r)
        return admissible_set

    def run_rigidity_analysis(self) -> dict:
        """
        Executes complete modular decomposition across the chosen primorial wheel.
        """
        a_m = self.compute_admissible_anchor_classes()
        total_classes = len(a_m)
        
        mod9_partition = defaultdict(list)
        stable_count = 0
        drift_count = 0
        
        for r in a_m:
            # 1. Classical continuous operator definition
            rn_m = ((r * 10) / 9) % 1.0
            
            # 2. Reduced algebraic definition
            r_mod_9 = r % 9
            mod9_partition[r_mod_9].append(r)
            
            # CRITICAL THEOREM CHECK: Cross-check both RN formulas with strict float tolerance
            assert abs(rn_m - (r_mod_9 / 9.0)) < 1e-12, \
                f"[!] Operator collapse failed at residue r={r}: Classical={rn_m}, Reduced={r_mod_9/9.0}"
            
            # Evaluate against the active gate window
            if self.gate_lower <= rn_m <= self.gate_upper:
                stable_count += 1
            else:
                drift_count += 1
                
        return {
            "modulus": self.modulus,
            "total_classes": total_classes,
            "stable_count": stable_count,
            "drift_count": drift_count,
            "partition": mod9_partition,
            "stable_fraction": stable_count / total_classes if total_classes > 0 else 0.0
        }


# ========================================================================================
# 2. AUTOMATION & DRIVER HOOKS
# ========================================================================================
def verify_control_baseline_hook(silent: bool = False) -> float:
    """
    Production driver anchor. Standard call signature utilized to assert structural
    geometry alignment instantly before massive computing iterations initialize.
    """
    engine = AcheronRigidityEngine(modulus_index=4)
    res = engine.run_rigidity_analysis()
    if not silent:
        print(f"\n[SYSTEM DETECTOR] Acheron RN/W2310 Structural Control Baseline Verified.")
        print(f"[SYSTEM DETECTOR] STABLE Target Threshold Lock = {res['stable_count']}/{res['total_classes']} ({res['stable_fraction']*100:.6f}%)")
    return res['stable_fraction']


# ========================================================================================
# 3. INTERACTIVE SUITE VECTORS / DIAGNOSTICS
# ========================================================================================
def execute_w2310_formal_proof():
    """
    Runs Option 1: Validates and prints the formal mathematical verification statements
    enforced by the strict unit assertions of the Acheron Rigidity Reduction Theorem.
    """
    print("\n" + "="*85)
    print(" VECTOR 1: ACHERON RIGIDITY THEOREM FORMAL PROOF RUNNER (W2310)")
    print("="*85)
    
    # Initialize Engine for W2310 (Index 4 maps to primes 2,3,5,7,11)
    engine = AcheronRigidityEngine(modulus_index=4, gate_lower=0.15, gate_upper=0.85)
    metrics = engine.run_rigidity_analysis()
    
    print("[*] Asserting Cardinality Check: |A2310| == 135...")
    assert metrics["total_classes"] == 135, f"Fail: Total classes={metrics['total_classes']}"
    print("    -> PASS: Found exactly 135 admissible classes.")
    
    print("[*] Asserting Active Multiples of 6 Modulo-9 Cyclic States...")
    active_states = set(metrics["partition"].keys())
    assert active_states.issubset({0, 3, 6}), f"Fail: Unexpected state leak observed: {active_states}"
    print(f"    -> PASS: Admissible residues strictly occupy expected states {active_states}.")
    
    print("[*] Asserting Combinatorial Partition Counts (46 / 44 / 45 Split)...")
    assert len(metrics["partition"][0]) == 46, f"Fail: State 0 Count={len(metrics['partition'][0])}"
    assert len(metrics["partition"][3]) == 44, f"Fail: State 3 Count={len(metrics['partition'][3])}"
    assert len(metrics["partition"][6]) == 45, f"Fail: State 6 Count={len(metrics['partition'][6])}"
    print("    -> PASS: Strict partition counts verified [State 0: 46 | State 3: 44 | State 6: 45].")
    
    print("[*] Asserting Absolute Stable Target Lock: STABLE == 89...")
    assert metrics["stable_count"] == 89, f"Fail: Stable Class Count={metrics['stable_count']}"
    print("    -> PASS: Exactly 89 classes confirmed inside STABLE zone.")
    
    print("-" * 85)
    print(f"[SUCCESS] THEOREM VERIFIED: {metrics['stable_count']}/{metrics['total_classes']} = {metrics['stable_fraction']*100:.6f}%")
    print("="*85)


def execute_multi_wheel_exploration():
    """
    Runs Option 2: Evaluates structural behavior scaling down across lower primorial wheels
    (W30, W210) to explicitly track the symmetry break of the mod-9 partition state space.
    """
    print("\n" + "="*85)
    print(" VECTOR 2: MULTI-MODULUS EXPLORATION CROSS-SPECTRUM (W30, W210, W2310)")
    print("="*85)
    print("[MECHANISM NOTE] The state restriction to {0,3,6} is an absolute invariant across")
    print("all listed wheels. Because every wheel depth contains both primes 2 and 3, any")
    print("admissible anchor residue r must satisfy gcd(r-1, 6) = 1 and gcd(r+1, 6) = 1,")
    print("forcing r ≡ 0 mod 6. Multiples of 6 mapped modulo 9 natively form a strict,")
    print("periodic 3-state cycle {0,3,6}. The wheels differ only in combinatorial drift.")
    print("-" * 85)
    
    indices = {"W30 (M=30)": 2, "W210 (M=210)": 3, "W2310 (M=2310)": 4}
    
    for label, idx in indices.items():
        engine = AcheronRigidityEngine(modulus_index=idx, gate_lower=0.15, gate_upper=0.85)
        m_res = engine.run_rigidity_analysis()
        
        print(f"\n[+] Spectrum Analytics for {label}:")
        print(f"    -> Admissible Modulo Classes : {m_res['total_classes']}")
        print(f"    -> Geometric STABLE Breakout : {m_res['stable_count']} classes")
        print(f"    -> Geometric DRIFT Breakout  : {m_res['drift_count']} classes")
        print(f"    -> Exact Baseline Density    : {m_res['stable_count']}/{m_res['total_classes']} = {m_res['stable_fraction']*100:.6f}%")
        print("    -> Complete Modulo 9 Partition Matrix Distribution:")
        
        for state_val in range(9):
            count = len(m_res['partition'][state_val])
            mapped_val = state_val / 9.0
            status = "STABLE" if engine.gate_lower <= mapped_val <= engine.gate_upper else "DRIFT"
            
            if count > 0:
                print(f"       * State r mod 9 = {state_val} -> Contains {count:<3} Classes ({status})")
            else:
                print(f"       * State r mod 9 = {state_val} -> [RESTRICTED / EMPTY ZONE] ({status})")
        print("    " + "." * 70)
    print("="*85)


def execute_custom_gate_sim():
    """
    Runs Option 3: Allows the user to supply manual gate windows dynamically to observe 
    how structural baseline frequencies respond to boundary alterations.
    """
    print("\n" + "="*85)
    print(" VECTOR 3: DYNAMIC GATE VARIANCE SIMULATOR (W2310)")
    print("="*85)
    
    try:
        lower = float(input("[>] Enter custom gate LOWER bound (e.g., 0.20): ").strip())
        upper = float(input("[>] Enter custom gate UPPER bound (e.g., 0.80): ").strip())
        if not (0.0 <= lower < upper <= 1.0):
            print("[!] Boundary Error: Limits must conform to 0.0 <= lower < upper <= 1.0")
            return
    except ValueError:
        print("[!] Input Signature Error: Standard decimal floats required.")
        return

    engine = AcheronRigidityEngine(modulus_index=4, gate_lower=lower, gate_upper=upper)
    metrics = engine.run_rigidity_analysis()
    
    print("-" * 85)
    print(f"[+] Computed Outputs under Custom Intercept Configuration [{lower} <= RN_M <= {upper}]:")
    print(f"    -> Retained STABLE Classes : {metrics['stable_count']} / 135")
    print(f"    -> Excluded DRIFT Classes  : {metrics['drift_count']} / 135")
    print(f"    -> Resulting Base Density  : {metrics['stable_fraction']*100:.6f}%")
    print("    -> State Permutations Matrix:")
    for state_val, residues in sorted(metrics['partition'].items()):
        mapped_val = state_val / 9.0
        status = "STABLE" if lower <= mapped_val <= upper else "DRIFT"
        print(f"       * State r mod 9 = {state_val} (Val: {mapped_val:.4f}) -> {len(residues):<3} Classes [{status}]")
    print("="*85)


# ========================================================================================
# 4. INTERACTIVE MASTER TERMINAL MENU SYSTEM
# ========================================================================================
def main_menu():
    # Execute automation hook quietly on module startup to guarantee environment integrity
    verify_control_baseline_hook(silent=True)
    
    while True:
        print("\n=== ACHERON RIGIDITY SUITE — INTERACTIVE ENVIRONMENT SYSTEM ===")
        print("1) Run Formal Proof Matrix & Unit Assertions (W2310)")
        print("2) Execute Multi-Wheel Cross-Exploration Spectrum (W30 / W210 / W2310)")
        print("3) Simulate Custom Intercept Gate Variance Configurations")
        print("4) Run Production Driver Integration Simulation Hook")
        print("9) Terminate Execution / Exit Framework")
        print("-" * 63)
        
        choice = input("[>] Select target analytical vector [1-4 / 9]: ").strip()
        
        if choice == '1':
            execute_w2310_formal_proof()
        elif choice == '2':
            execute_multi_wheel_exploration()
        elif choice == '3':
            execute_custom_gate_sim()
        elif choice == '4':
            print("\n" + "-"*65)
            print("[*] Simulating live ingestion check inside high-performance sieve...")
            verify_control_baseline_hook(silent=False)
            print("-"*65)
        elif choice == '9':
            print("\n[*] Disengaging framework matrix environments. System terminated cleanly.\n")
            sys.exit(0)
        else:
            print("[!] Signature sequence unmapped. Please pass a valid option choice.")


if __name__ == "__main__":
    main_menu()