#TG_DETROIT_MATRIX_CORE_EQUATION_SUITE.py

import os
import sys
import math
import time
import json
import random
import glob
from collections import Counter

# =====================================================================
# SECTOR 1: HIGH-PERFORMANCE PRIME SIEVE LAYER
# =====================================================================
def compute_prime_sieve(limit):
    print(f"[-] Initializing Production Sieve up to {limit:,}...")
    start = time.time()
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.isqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = 0
    print(f"[+] Sieve complete in {time.time() - start:.2f}s.")
    return sieve

# =====================================================================
# SECTOR 2: POPULATION REGISTRY (WITH BOUNDARY MATCHING)
# =====================================================================
def is_twin_center(n, sieve, limit):
    return n > 1 and (n-1) <= limit and (n+1) <= limit and sieve[n-1] and sieve[n+1]

def is_cousin_center(n, sieve, limit):
    return n > 2 and (n-2) <= limit and (n+2) <= limit and sieve[n-2] and sieve[n+2]

def is_sexy_center(n, sieve, limit):
    return n > 3 and (n-3) <= limit and (n+3) <= limit and sieve[n-3] and sieve[n+3]

def is_sophie_germain(n, sieve, limit):
    # Dynamic horizon constraint: ensure the sieve array can absorb the upper pairing edge
    return n <= limit and sieve[n] and (2 * n + 1) < len(sieve) and sieve[2 * n + 1]

def is_perfect_square(n, sieve, limit):
    root = int(math.isqrt(n))
    return root * root == n

def is_semiprime(n, sieve, limit):
    if n < 4 or sieve[n]: return False
    temp = n
    factors = 0
    for p in range(2, int(math.isqrt(n)) + 1):
        if sieve[p] and temp % p == 0:
            while temp % p == 0:
                factors += 1
                temp //= p
                if factors > 2: return False
    if temp > 1:
        if sieve[temp]: factors += 1
        else: return False
    return factors == 2

def is_prime_power(n, sieve, limit):
    if n < 4 or sieve[n]: return False
    for p in range(2, int(math.isqrt(n)) + 1):
        if sieve[p] and n % p == 0:
            temp = n
            while temp % p == 0:
                temp //= p
            return temp == 1
    return False

def is_abundant(n, sigma, limit): return sigma > 2 * n
def is_deficient(n, sigma, limit): return sigma < 2 * n

POPULATION_REGISTRY = {
    '1': ('Twin Centers', is_twin_center, False, False),
    '2': ('Cousin Centers', is_cousin_center, False, False),
    '3': ('Sexy Centers', is_sexy_center, False, False),
    '4': ('Sophie Germain Primes', is_sophie_germain, False, False),
    '5': ('Semiprimes [HEAVY]', is_semiprime, False, True), 
    '6': ('Prime Powers [HEAVY]', is_prime_power, False, True), 
    '7': ('Perfect Squares', is_perfect_square, False, False),
    '8': ('Abundant Numbers', None, True, False), 
    '9': ('Deficient Numbers', None, True, False)
}

# =====================================================================
# SECTOR 3: TELEMETRY ENGINE WITH CONDITIONAL STATE RUNS
# =====================================================================
def run_segmented_spectrometer(limit, target_id, sieve, M, block_size=5000000, use_checkpoints=False, control_mode=False):
    name, condition_func, sigma_dependent, is_heavy = POPULATION_REGISTRY[target_id]
    checkpoint_file = f"tg_checkpoint_T{target_id}_M{M}_L{limit}.jsonl"
    
    projections = {
        'full': Counter(), 'n_sigma': Counter(), 'n_g': Counter(),
        'sigma_g': Counter(), 'n_only': Counter(), 'sigma_only': Counter(), 'g_only': Counter()
    }
    total_target_count = 0
    acheron_overlap = 0
    start_block = 0

    if use_checkpoints and os.path.exists(checkpoint_file) and not control_mode:
        with open(checkpoint_file, 'r') as f:
            for line in f:
                last_data = json.loads(line)
                start_block = last_data.get('block_end', 0)
                total_target_count = last_data.get('total_target_count', 0)
                acheron_overlap = last_data.get('acheron_overlap', 0)
                if 'projections_snapshot' in last_data:
                    for p_space, mapping in last_data['projections_snapshot'].items():
                        for k_str, val in mapping.items():
                            k_tuple = tuple(int(x) for x in k_str.split(','))
                            projections[p_space][k_tuple] = val

    last_report_time = time.time()
    report_interval = 10.0 

    for low in range(start_block, limit, block_size):
        high = min(low + block_size, limit + 1)
        sigma_buf = [1] * (high - low)
        temp_buf = [i for i in range(low, high)]
        
        for i in range(2, int(math.isqrt(high)) + 1):
            p_start = max(i * i, ((low + i - 1) // i) * i)
            for j in range(p_start, high, i):
                idx = j - low
                if temp_buf[idx] % i == 0:
                    p_pow = 1
                    p_sum = 1
                    while temp_buf[idx] % i == 0:
                        p_pow *= i
                        p_sum += p_pow
                        temp_buf[idx] //= i
                    sigma_buf[idx] *= p_sum
                    
        for j in range(max(1, low), high):
            idx = j - low
            if temp_buf[idx] > 1:
                sigma_buf[idx] *= (1 + temp_buf[idx])
        
        # TARGET-FIRST ANALYSIS PASS
        for n in range(max(1, low), high):
            idx = n - low
            sig = sigma_buf[idx]
            is_target = False
            
            if control_mode:
                is_target = (random.random() < 0.05)
            else:
                if sigma_dependent:
                    if target_id == '8': is_target = is_abundant(n, sig, limit)
                    elif target_id == '9': is_target = is_deficient(n, sig, limit)
                else:
                    is_target = condition_func(n, sieve, limit)
                    
            if is_target:
                total_target_count += 1
                g = math.gcd(n, sig)
                if g > 1: acheron_overlap += 1
                
                rn, rs, rg = n % M, sig % M, g % M
                projections['full'][(rn, rs, rg)] += 1
                projections['sigma_only'][rs] += 1

        # TELEMETRY HEARTBEAT
        current_time = time.time()
        if current_time - last_report_time >= report_interval:
            pct_complete = (high / limit) * 100
            shannon, norm_e = calculate_metrics(projections['full'])
            u_states = len(projections['full'])
            print(
                f"  [TELEMETRY] {pct_complete:6.2f}% | "
                f"Targets: {total_target_count:9,} | "
                f"Acheron: {acheron_overlap:9,} | "
                f"States: {u_states:5,} | "
                f"NormEntropy: {norm_e:.4f}"
            )
            last_report_time = current_time

        if use_checkpoints and not control_mode:
            with open(checkpoint_file, 'a') as f:
                proj_snapshot = {
                    p_name: {",".join(map(str, k)): v for k, v in c.items()} 
                    for p_name, c in projections.items()
                }
                f.write(json.dumps({
                    "block_end": high, "total_target_count": total_target_count, 
                    "acheron_overlap": acheron_overlap, "projections_snapshot": proj_snapshot
                }) + "\n")
                
    return total_target_count, acheron_overlap, projections

def calculate_metrics(counter_obj):
    if not counter_obj: return 0.0, 0.0
    total = sum(counter_obj.values())
    probs = [count / total for count in counter_obj.values()]
    shannon = -sum(p * math.log2(p) for p in probs if p > 0)
    norm_e = shannon / math.log2(len(counter_obj)) if len(counter_obj) > 1 else 0.0
    return shannon, norm_e

# =====================================================================
# DYNAMIC CONSOLE SYSTEM
# =====================================================================
def run_plan_console():
    print("=" * 75)
    print("      TERNARIUM GEMINORUM — DETROIT MATRIX PRODUCTION SPECTROMETER      ")
    print("=" * 75)
    
    lim_map = {'1': 1000000, '2': 100000000, '3': 200000000, '4': 500000000}
    
    # Initialize baseline configurations at startup
    limit = 1000000
    sieve_limit = limit + 1
    sieve = compute_prime_sieve(sieve_limit)
    M = 210
    
    while True:
        print(f"\nOptions Framework [Active Horizon: {limit:,} | Sieve Limit: {len(sieve)-1:,}]:")
        print("1) Reconfigure Upper Target Scale Horizon Limit")
        print("2) Run Phase 1: Mode 3 Ground-Truth Validation Counts")
        print("3) Run Phase 2: Single Target Spectrometry (With Dynamic Real-Time Telemetry)")
        print("4) Run Phase 3: Detroit Matrix Mode Compare-All (Protects Cache/Memory)")
        print("5) Terminate Suite")
        choice = input("Select Option (1-5): ").strip()
        
        if choice == '1':
            print("\nSelect Boundary Limit Environment Configuration:")
            print("1) 1,000,000 (1M Validation Run)")
            print("2) 100,000,000 (100M Scale Protection Bound)")
            print("3) 200,000,000 (200M Mid-Scale Bound)")
            print("4) 500,000,000 (500M Maximum Boundary)")
            lim_choice = input("Select limit option (1-4): ").strip()
            limit = lim_map.get(lim_choice, 1000000)
            
            # CRITICAL OPTIMIZATION: Default matrix allocations stay tight unless executing isolated targets
            sieve_limit = limit + 1
            sieve = compute_prime_sieve(sieve_limit)
            
        elif choice == '2':
            # Sophie Germain requires verification expansion check
            if len(sieve) < (2 * limit + 1):
                print("[-] Re-allocating prime sieve to 2*limit+1 for Sophie Germain validation...")
                sieve = compute_prime_sieve(2 * limit + 1)
            print("\nExecuting Phase 1 Benchmarking...")
            for tid in ['1', '4']:
                cnt, _, _ = run_segmented_spectrometer(limit, tid, sieve, M, use_checkpoints=False)
                print(f" -> [Ground Truth] ID {tid} ({POPULATION_REGISTRY[tid][0]}): Extracted Count = {cnt:,}")
                
        elif choice == '3':
            print("\nChoose Target Sequence Spectrometry Profile:")
            for k, v in POPULATION_REGISTRY.items():
                print(f"  {k}) {v[0]}")
            t_choice = input("Select number (1-9): ").strip()
            
            if t_choice in POPULATION_REGISTRY:
                # OPTIMIZATION: Dynamically expand the array horizon strictly on-demand for Sophie
                if t_choice == '4' and len(sieve) < (2 * limit + 1):
                    print("[-] Sophie Germain selection identified. Scaling sieve window out to 2*limit+1...")
                    sieve = compute_prime_sieve(2 * limit + 1)
                elif t_choice != '4' and len(sieve) > (limit + 1) and limit >= 100000000:
                    print("[-] Constraining prime sieve memory bound to normal upper limit...")
                    sieve = compute_prime_sieve(limit + 1)
                    
                if POPULATION_REGISTRY[t_choice][3] and limit >= 100000000:
                    warn = input("[!] WARNING: Target is marked HEAVY and will bottleneck at this scale. Continue? (y/n): ").strip().lower()
                    if warn != 'y': continue
                    
                chk_dec = input("Enable disk checkpoint states? (y/n): ").strip().lower()
                use_chk = True if chk_dec == 'y' else False
                
                print(f"\n[-] Starting streaming spectrometry for {POPULATION_REGISTRY[t_choice][0]}...")
                t_count, a_overlap, proj = run_segmented_spectrometer(limit, t_choice, sieve, M, use_checkpoints=use_chk)
                shannon, norm_e = calculate_metrics(proj['full'])
                print(f"\n[+] Final Spectrometry Summary Profile:")
                print(f"    Total Counts:        {t_count:,}")
                print(f"    Acheron Convergence: {a_overlap:,} ({(a_overlap/t_count*100) if t_count > 0 else 0:.2f}%)")
                print(f"    Manifold Entropy:    {shannon:.4f} (Normalized: {norm_e:.4f})")
            
        elif choice == '4':
            # Matrix mode doesn't include Sophie's lookahead requirement, keep it tightly constrained to limit + 1
            if len(sieve) > (limit + 1):
                print("[-] Bypassing lookahead arrays. Hard-clamping matrix sieve to limit + 1 bounds...")
                sieve = compute_prime_sieve(limit + 1)
                
            print("\nExecuting Detroit Matrix Side-by-Side Generation...")
            print("-" * 92)
            print(f"| {'Target System':<26} | {'Total Count':<12} | {'Acheron %':<12} | {'Norm Entropy':<12} |")
            print("-" * 92)
            for tid in sorted(POPULATION_REGISTRY.keys()):
                if POPULATION_REGISTRY[tid][3] and limit >= 100000000:
                    print(f"| {POPULATION_REGISTRY[tid][0] + ' (SKIPPED)':<26} | {'N/A':>12} | {'N/A':>12} | Navigating... |")
                    continue
                    
                cnt, ach, proj = run_segmented_spectrometer(limit, tid, sieve, M, use_checkpoints=False)
                _, norm_e = calculate_metrics(proj['full'])
                pct = (ach / cnt * 100) if cnt > 0 else 0.0
                print(f"| {POPULATION_REGISTRY[tid][0]:<26} | {cnt:>12,} | {pct:>11.2f}% | {norm_e:>12.4f} |")
            print("-" * 92)
            
        elif choice == '5':
            break

if __name__ == "__main__":
    run_plan_console()


#==========================================================================================
#Compliance Profile & Licensing:
#  - Framework: TERNARIUM GEMINORUM — DETROIT MATRIX CORE EQUATION
#  - Foundational Concept Integration: Zero-Ology IP Archive / Zer00logy IP Archive
#  - Primary Author of Foundational Concepts: Stacey Szmy
#  - Technical Framework Lineage: RN Digital Weights Framework / Acheron Fields / Acheron Fragmentation /  Acheron Twin-Prime Finite Residue Geometry and Asymptotic Distribution Framework / Ternarium Geminorum
#  - Reference: https://github.com/haha8888haha8888/Zero-ology
#  - Reference: https://github.com/haha8888haha8888/Zer00logy
#  - Reference: www.zero-ology.com
#
#  © Stacey8Szmy — Zer00logy IP Archive. All symbolic rights reserved.
#==========================================================================================
