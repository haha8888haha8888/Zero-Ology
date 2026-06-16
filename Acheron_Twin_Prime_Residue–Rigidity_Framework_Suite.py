#Acheron_Twin_Prime_Residue–Rigidity_Framework_Suite.py
#
#!/usr/bin/env python3
"""
==========================================================================================
     ACHERON_TWIN_PRIMES_STEP_DIGITAL_WEIGHTS.py (v1.0.3-RELEASE-UNLOCKED)
==========================================================================================
[1] THESIS STATEMENT:
    Classical sieve methods encounter known limitations, including parity barriers and
    accumulated remainder/error terms (∑ δ). This suite implements the un-intercepted 
    Acheron Twin Prime Residue-Rigidity Framework, capturing class-by-class variance against
    empirical group means and tracking the distribution profiles of tunable RN_M gates.

==========================================================================================
Compliance Profile & Licensing:
  - Framework: Acheron Twin Prime Residue–Rigidity Framework
  - Foundational Concept Integration: Zero-Ology IP Archive / Zer00logy Framework
  - Primary Author of Foundational Concepts: Stacey Szmy
  - Technical Framework Lineage: RN Formula Solution /
  - Reference: https://github.com/haha8888haha8888/Zero-ology
  - Reference: www.zero-ology.com

  © Stacey8Szmy — Zer00logy IP Archive. All symbolic rights reserved.
==========================================================================================
"""

import sys
import time
import math
from collections import defaultdict

# -------------------------------------------------------------------------------------
# INITIALIZATION & CORE CONSTANTS
# -------------------------------------------------------------------------------------
W2310_MODULUS = 2310

# Anchors for small-wheel edge cases (3,5), (5,7), (11,13)
EXCEPTIONAL_ANCHORS = {4, 6, 12} 

def precompute_admissible_classes():
    """
    Precomputes anchors (p+1) modulo 2310 where both (anchor-1) and (anchor+1)
    are coprime to 2310. This isolates the 135 valid avenues of the wheel.
    """
    primes = [2, 3, 5, 7, 11]
    admissible = []
    for n in range(W2310_MODULUS):
        p1 = n - 1
        p2 = n + 1
        if all(p1 % p != 0 for p in primes) and all(p2 % p != 0 for p in primes):
            admissible.append(n)
    return set(admissible)

def calculate_hardy_littlewood(n):
    """
    Approximates the Hardy-Littlewood logarithmic integral curve up to N.
    """
    if n < 3:
        return 0.0
    C_2 = 0.6601618158
    steps = 1000
    integration_sum = 0.0
    dx = (n - 2) / steps
    for i in range(steps):
        x = 2 + (i + 0.5) * dx
        integration_sum += (1.0 / (math.log(x) ** 2)) * dx
    return 2 * C_2 * integration_sum

# -------------------------------------------------------------------------------------
# MAIN EXECUTION CORE ENGINE
# -------------------------------------------------------------------------------------
def run_acheron_sieve(horizon_scale):
    print(f"\n[+] Initialization Vector Confirmed. Scale Lock: {horizon_scale:,}")
    print("[*] Allocation Matrix Initialized. Deploying bytearray sieve allocator to secure memory footprint...")
    
    start_time = time.time()
    
    # Safe memory footprint utilization using bytearray allocation
    sieve = bytearray([1]) * (horizon_scale + 1)
    if len(sieve) > 0: sieve[0] = 0
    if len(sieve) > 1: sieve[1] = 0
    
    limit = int(math.sqrt(horizon_scale))
    for i in range(2, limit + 1):
        if sieve[i]:
            for j in range(i * i, horizon_scale + 1, i):
                sieve[j] = 0
                
    print("[*] Processing baseline empirical twin metrics & framework telemetry...")
    
    # Load wheel structure
    w2310_admissible = precompute_admissible_classes()
    
    # Telemetry Counters
    total_empirical_twins = 0
    observed_twins_inside_path = 0
    exceptional_outside_twins = 0
    
    # Global Classification State Registers
    total_stable_clocks = 0
    total_drift_anomalies = 0
    
    # Class-by-Class Corridor Performance Tracker
    corridor_distribution_map = defaultdict(int)
    
    # Explicitly define the RN_M gate parameters as structural, tunable boundaries
    GATE_LOWER_BOUND = 0.15
    GATE_UPPER_BOUND = 0.85
    GATE_INTERVAL_COVERAGE_PCT = (GATE_UPPER_BOUND - GATE_LOWER_BOUND) * 100.0
    
    # Evaluate Twin Candidates across the full space
    for p in range(3, horizon_scale - 1, 2):
        if sieve[p] and sieve[p+2]:
            total_empirical_twins += 1
            anchor_node = p + 1
            
            # Module 3.1: Localized Modular Multiplier Gate (RN_M)
            rn_m = ((anchor_node % W2310_MODULUS) * 10 / 9) % 1.0
            
            # Wheel Check Modulo 2310
            mod_class = anchor_node % W2310_MODULUS
            
            if mod_class in w2310_admissible:
                observed_twins_inside_path += 1
                corridor_distribution_map[mod_class] += 1
                
                # Tunable RN_M interval check to distinguish digital equilibrium profiles
                if GATE_LOWER_BOUND <= rn_m <= GATE_UPPER_BOUND:
                    total_stable_clocks += 1
                else:
                    total_drift_anomalies += 1
            else:
                if anchor_node in EXCEPTIONAL_ANCHORS:
                    exceptional_outside_twins += 1

    execution_duration = time.time() - start_time
    hl_benchmark = calculate_hardy_littlewood(horizon_scale)
    
    # -------------------------------------------------------------------------------------
    # DECOUPLED OUTPUT MATRIX LOG GENERATION
    # -------------------------------------------------------------------------------------
    print(f"[*] Full spectrum validation complete.")
    print("=" * 85)
    print("      ACHERON TWIN PRIMES STEP DIGITAL WEIGHTS SPECTRAL LOG (v1.0.3-RELEASE)")
    print("=" * 85)
    print(f"Total Horizon Scale Evaluated         : {horizon_scale:,}")
    print(f"Total Empirical Twins (Global Sieve)  : {total_empirical_twins:,}")
    print(f"Hardy-Littlewood Benchmark Curve     : {hl_benchmark:.2f}")
    print(f"Execution Window Processing Velocity  : {execution_duration:.4f} seconds")
    print("-" * 85)
    
    print(f"[WHEEL GEOMETRY ANALYSIS: W-2310]")
    print(f" -> Active Admissible Channels Available : 135")
    print(f" -> Observed Twins Bounded Inside Paths  : {observed_twins_inside_path:,}")
    print(f" -> Exceptional Outside-W2310 Twin Anchors: {exceptional_outside_twins}")
    
    # Honest statistical representation relative to group behavior
    empirical_mean_per_class = observed_twins_inside_path / 135.0
    print(f" -> Empirical Mean Per Active Class      : {empirical_mean_per_class:.4f}")
    
    # Calculate real mathematical variance and standard deviation relative to the group mean
    variances = []
    counts_list = []
    for c in w2310_admissible:
        observed = corridor_distribution_map[c]
        counts_list.append(observed)
        variance_offset = observed - empirical_mean_per_class
        variances.append(variance_offset ** 2)
    
    mean_empirical_variance = sum(variances) / len(variances) if variances else 0.0
    empirical_standard_deviation = math.sqrt(mean_empirical_variance)
    min_corridor_count = min(counts_list) if counts_list else 0
    max_corridor_count = max(counts_list) if counts_list else 0
    
    print(f" -> Mean Empirical Corridor Variance    : {mean_empirical_variance:+.6f}")
    print(f" -> Empirical Corridor Std Deviation     : {empirical_standard_deviation:.6f}")
    print(f" -> Absolute Channel Spread Boundary     : Min = {min_corridor_count:,} | Max = {max_corridor_count:,}")
    print("-" * 85)
    
    # Surface the classification state metrics cleanly as direct percentages
    total_active_clocks = total_stable_clocks + total_drift_anomalies
    stable_pct = (total_stable_clocks / total_active_clocks * 100.0) if total_active_clocks else 0.0
    drift_pct = (total_drift_anomalies / total_active_clocks * 100.0) if total_active_clocks else 0.0
    
    print("[FRAMEWORK STATE ENGINE VALUATION - OPERATIONAL TELEMETRY]")
    print(f" -> Tunable Multiplier Gate Configuration: [{GATE_LOWER_BOUND} <= RN_M <= {GATE_UPPER_BOUND}]")
    print(f" -> Expected Uniform Interval Coverage  : {GATE_INTERVAL_COVERAGE_PCT:.2f}%")
    print(f" -> Global STABLE State Clockings        : {total_stable_clocks:,} ({stable_pct:.4f}%)")
    print(f" -> Global DRIFT State Anomalies         : {total_drift_anomalies:,} ({drift_pct:.4f}%)")
    print("=" * 85)
    
    # Full verification of all 135 admissible classes, retaining zero-count pathways
    print("\n[DIAGNOSTIC SAMPLE: CLASS-BY-CLASS CHANNELS (Top 5 / Bottom 5 Performance)]")
    sorted_corridors = sorted(
        [(c, corridor_distribution_map[c]) for c in w2310_admissible], 
        key=lambda x: x[1], 
        reverse=True
    )
    
    if sorted_corridors:
        print("  Highest Density Channels:")
        for cls, count in sorted_corridors[:5]:
            deviation = count - empirical_mean_per_class
            print(f"    - Modulo Class [{cls:4d}]: Observed = {count:5d} | Mean Dev = {deviation:+.4f}")
        print("  Lowest Density Channels:")
        for cls, count in sorted_corridors[-5:]:
            deviation = count - empirical_mean_per_class
            print(f"    - Modulo Class [{cls:4d}]: Observed = {count:5d} | Mean Dev = {deviation:+.4f}")
    print("=" * 85)

# -------------------------------------------------------------------------------------
# SELECTION INTERFACE DIRECTORY
# -------------------------------------------------------------------------------------
def main_menu():
    while True:
        print("\n=== ACHERON HORIZON FULL SPECTRUM SELECTOR SYSTEM (v1.0.3-RELEASE) ===")
        print("1) 1M - Validation Scale Checkpoint")
        print("2) 10M - Short Scale Audit")
        print("3) 50M - Deep Core Evaluation")
        print("4) 100M - High-Scale Diagnostic Horizon")
        print("5) 500M - High-Scale Diagnostic Horizon [UNLOCKED]")
        print("6) 1B - Asymptotic Peak Horizon [UNLOCKED]")
        print("9) Exit Suite")
        
        try:
            choice = input("[>] Select targeted diagnostic vector [1-6 / 9]: ").strip()
            if choice == '1': run_acheron_sieve(1000000)
            elif choice == '2': run_acheron_sieve(10000000)
            elif choice == '3': run_acheron_sieve(50000000)
            elif choice == '4': run_acheron_sieve(100000000)
            elif choice == '5': run_acheron_sieve(500000000)
            elif choice == '6': run_acheron_sieve(1000000000)
            elif choice == '9': 
                print("\n[+] Exiting Analysis Environment System. System Disengaged.\n")
                break
            else:
                print("[!] Invalid Selection. Choose an initialized validation lane.")
        except KeyboardInterrupt:
            print("\n\n[!] Execution stream broken via Hardware Interrupt signal.")
            break
        except Exception as e:
            print(f"[!] Engine Fault detected: {str(e)}")

if __name__ == "__main__":
    main_menu()