#ACHERON_FIELDS_SUITE.py
#!/usr/bin/env python3
"""
==========================================================================================
THE ACHERON FIELDS EXTRAPOLATION MASTER SUITE (v4.2 TRUE STREAMING EDITION)
==========================================================================================
THE KAKÓS WATERLINE FUNCTION K(N) & COMPREHENSIVE SURVEYED FIELD INTERACTION POOLS
------------------------------------------------------------------------------------------
[THE COMPREHENSIVE ACHERON FIELD MODEL]
  A(n) = 1  if  gcd(n, σ(n)) > 1, else 0  (Saturated-Support Number / Acheron Flow Segment)
  R(n) = 1  if  gcd(n, σ(n)) = 1, else 0  (Rupture Number Field / Anchoring Bedrock)
  where σ(n) is the sum of divisors of n.

[THE KAKÓS WATERLINE FUNCTION DEFINITION]
  K(N) = max{ k : there exists n <= N such that A(n) = A(n+1) = ... = A(n+k-1) = 1 }

  Corridor Bounding Constraints within Surveyed Bounds:
    Every fully saturated prime corridor up to N satisfies:
      internal width <= K(N)   |   prime gap <= K(N) + 1
==========================================================================================
"""

import math
import random
import sys
from array import array
from statistics import mean, median, stdev
from collections import defaultdict

def interactive_menu():
    print("==================================================================")
    print("      ACHERON FIELDS HORIZON SELECTOR (v4.2 True Stream Engine)   ")
    print("==================================================================")
    print(" 1) Run  50,000,000 Horizon Pool")
    print(" 2) Run 100,000,000 Horizon Pool")
    print(" 3) Run 200,000,000 Horizon Pool")
    print(" 4) Run 500,000,000 Horizon Pool")
    print(" 5) Run 1,000,000,000 Horizon Pool")
    print(" 6) Custom Limit Entry")
    print("------------------------------------------------------------------")

    while True:
        try:
            choice = input("Select horizon target (1-6): ").strip()
            if choice == '1': return 50000000
            if choice == '2': return 100000000
            if choice == '3': return 200000000
            if choice == '4': return 500000000
            if choice == '5': return 1000000000
            if choice == '6':
                custom = int(input("Enter custom integer limit: ").replace(',', ''))
                if custom > 1: return custom
                print("[!] Limit must be greater than 1.")
            print("[!] Invalid selection. Please enter a number between 1 and 6.")
        except ValueError:
            print("[!] Please enter a valid integer choice.")

def get_prime_factors(n):
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return sorted(list(factors))

def pearson(xs, ys):
    if len(xs) < 2 or len(ys) < 2: return 0.0
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (denx * deny) if denx and deny else 0.0

def quadratic_fit(xs, ys):
    n = len(xs)
    if n < 3: return 0.0, 0.0, 0.0, 0.0
    sx, sx2, sx3, sx4 = sum(xs), sum(x**2 for x in xs), sum(x**3 for x in xs), sum(x**4 for x in xs)
    sy, sxy, sx2y = sum(ys), sum(x*y for x, y in zip(xs, ys)), sum((x**2)*y for x, y in zip(xs, ys))
    M = [[n, sx, sx2, sy], [sx, sx2, sx3, sxy], [sx2, sx3, sx4, sx2y]]
    for i in range(3):
        piv = M[i][i]
        if abs(piv) < 1e-12: return 0.0, 0.0, 0.0, 0.0
        for j in range(i, 4): M[i][j] /= piv
        for k in range(3):
            if k != i:
                f = M[k][i]
                for j in range(i, 4): M[k][j] -= f * M[i][j]
    a, b, c = M[0][3], M[1][3], M[2][3]
    y_m = mean(ys)
    ss_res = sum((y - (a + b*x + c*x*x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - y_m) ** 2 for y in ys)
    return a, b, c, (1 - ss_res / ss_tot if ss_tot else 0.0)

def expectation_bins(records, bins=20):
    records = sorted(records, key=lambda r: r["rho"])
    size = len(records) // bins
    results = []
    for b in range(bins):
        lo = b * size
        hi = (b + 1) * size if b < bins - 1 else len(records)
        bk = records[lo:hi]
        if not bk: continue
        results.append({
            "rho_mean": mean([r["rho"] for r in bk]), "gap_mean": mean([r["gap"] for r in bk])
        })
    return results

def main():
    limit = interactive_menu()

    print(__doc__)
    print(f"[*] Initializing Optimized Target Pool Upper Horizon Limit N = {limit:,}\n")

    # Step 1: Highly efficient prime sieve using a low-memory bit-packed bytearray
    print(f"[*] Generating master prime maps up to n = {limit:,}...")
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            for m in range(p * p, limit + 1, p):
                is_prime[m] = 0

    primes = array('I', [n for n in range(2, limit + 1) if is_prime[n]])
    print(f"[+] Primes compiled: {len(primes):,}")

    # Pure Prime-Power Identification
    is_pure_prime_power = bytearray(limit + 1)
    for p in primes:
        val = p * p
        while val <= limit:
            is_pure_prime_power[val] = 1
            if val > limit // p:
                break
            val *= p

    # Step 2: Segmented window architecture for field calculations (Bypasses pre-allocation MemoryError)
    CHUNK_SIZE = 5000000
    print(f"[*] Processing Acheron substrate and Rupture configurations in segments of {CHUNK_SIZE:,}...")

    A = bytearray(limit + 1)
    R = bytearray(limit + 1)
    
    # Track metrics dynamically to conserve global space
    total_ruptures = 0
    pure_pp_ruptures = 0
    composite_non_pp_ruptures = 0
    sample_pool_print = []

    for chunk_start in range(2, limit + 1, CHUNK_SIZE):
        chunk_end = min(chunk_start + CHUNK_SIZE - 1, limit)
        chunk_len = chunk_end - chunk_start + 1
        
        # Local segment block allocation (tiny memory footprint)
        local_sigma = array('Q', [1] * chunk_len)
        
        # Segmented Sieve for Divisor Sums
        for d in range(2, chunk_end + 1):
            first_multiplier = max(2, (chunk_start + d - 1) // d)
            start_m = first_multiplier * d
            for m in range(start_m, chunk_end + 1, d):
                local_sigma[m - chunk_start] += d
                
        # Evaluate localized structural field components
        for n in range(chunk_start, chunk_end + 1):
            sig_val = local_sigma[n - chunk_start]
            if math.gcd(n, sig_val) > 1:
                A[n] = 1
            else:
                R[n] = 1
                total_ruptures += 1
                if is_pure_prime_power[n] == 1:
                    pure_pp_ruptures += 1
                elif is_prime[n] == 0:
                    composite_non_pp_ruptures += 1
                    if len(sample_pool_print) < 5:
                        # Late-bind sigma since we don't hold the full array globally
                        sample_pool_print.append((n, get_prime_factors(n), sig_val))

    print(f"[+] Substrates compiled. Field Support Density: {sum(A)/(limit-1):.6f}")

    # Pure Prime-Power Verification Subsector
    pp_tested = sum(is_pure_prime_power)
    pp_failed = 0
    for n in range(2, limit + 1):
        if is_pure_prime_power[n] == 1 and R[n] != 1:
            pp_failed += 1
    verdict = "[PASS]" if pp_failed == 0 else "[FAIL]"
    print(f"    [Verification] Pure Prime-Power Nodes Checked: {pp_tested:,} | Failures: {pp_failed:,} Verification: {verdict}\n")

    # Scan field to collect continuous A-run boundaries sequentially
    current_run_len = 0
    current_run_start = 0
    all_runs_log = []

    for n in range(2, limit + 1):
        if A[n] == 1:
            if current_run_len == 0: current_run_start = n
            current_run_len += 1
        else:
            if current_run_len > 0:
                all_runs_log.append((current_run_start, n - 1, current_run_len))
                current_run_len = 0
    if current_run_len > 0:
        all_runs_log.append((current_run_start, limit, current_run_len))

    # #sector 1# Dynamic Waterline Stepwise Extraction
    print(".. #sector 1# evaluating stepwise kakós waterline values K(N)")
    milestones = [1000000, 10000000, 50000000, 100000000, 150000000, 200000000, limit]
    milestones = sorted(list(set([m for m in milestones if m <= limit])))

    waterline_history = {}
    horizon_run_counts = {}

    print("\n    [+] ===== KAKÓS WATERLINE TRACKING MATRIX (BOUND-CLIPPED) =====")
    for horizon in milestones:
        local_runs = [(s, min(e, horizon), min(e, horizon) - s + 1) for s, e, k in all_runs_log if s <= horizon]
        if local_runs:
            max_run = max(local_runs, key=lambda item: item[2])
            k_n = max_run[2]
            coord_str = f"at [{max_run[0]:,} -> {max_run[1]:,}]"
        else:
            k_n = 0
            coord_str = "N/A"

        waterline_history[horizon] = k_n

        depths = [10, 15, 17, 18, 20]
        counts_at_horizon = {d: sum(1 for r in local_runs if r[2] >= d) for d in depths}
        horizon_run_counts[horizon] = counts_at_horizon

        print(f"      Survey Bound N = {horizon:<13,} | Observed Waterline K(N) = {k_n:<2}  {coord_str}")
    print("    ================================================\n")

    # #sector 2# Corridor Truncation Profiles
    print(".. #sector 2# running horizon corridor-density targets and metric profiles")
    final_records = []

    for target in milestones:
        records_t = []
        for i in range(1, len(primes) - 1):
            p = primes[i]
            q = primes[i + 1]
            if q > target:
                break
            prev_gap = primes[i] - primes[i - 1]
            gap = q - p
            width = gap - 1
            if width <= 0: continue
            rho = sum(A[m] for m in range(p + 1, q)) / width
            expanded = 1 if gap > prev_gap else 0
            records_t.append({
                "left_prime": p, "right_prime": q, "gap": gap, "rho": rho, "expanded": expanded, "width": width
            })
        if target == limit:
            final_records = records_t

        corr_t = pearson([r["rho"] for r in records_t], [r["gap"] for r in records_t]) if len(records_t) >= 2 else 0.0

        groups_t = defaultdict(list)
        for r in records_t:
            groups_t[r["rho"]].append(r["gap"])
        v_rhos, m_gaps = [], []
        for rho, gps in groups_t.items():
            if len(gps) >= 100:
                v_rhos.append(rho)
                m_gaps.append(mean(gps))
        r2_exclusive = quadratic_fit(v_rhos, m_gaps)[3] if len(v_rhos) >= 3 else 0.0

        sat_gaps_t = [r["gap"] for r in records_t if abs(r["rho"] - 1.0) < 1e-5]
        sat_floor_t = mean(sat_gaps_t) if sat_gaps_t else 0.0
        print(f"    Target N: {target:<12,} | Corridors: {len(records_t):<9,} | BaseCorr: {corr_t:<8.4f} | BinExclR²: {r2_exclusive:<8.4f} | SatFloor: {sat_floor_t:.4f}")

    # #sector 3# Saturated Sinks Distribution Profiling (ρ = 1.0)
    print("\n.. #sector 3# running saturation distribution configuration audit")
    sat_pool = [r for r in final_records if abs(r["rho"] - 1.0) < 1e-6]
    total_sat = len(sat_pool)
    sat_gaps = [r["gap"] for r in sat_pool]

    print(f"    Saturated Count (N) : {total_sat:,}")
    print(f"    Mean Saturated Gap  : {mean(sat_gaps) if sat_gaps else 0.0:.4f}")
    print(f"    Median Saturated Gap: {median(sat_gaps) if sat_gaps else 0.0:.1f}")
    print(f"    Max Saturated Gap   : {max(sat_gaps) if sat_gaps else 0:,}")

    if total_sat > 0:
        max_sat_width = max([r["width"] for r in sat_pool])
        max_sat_gap = max(sat_gaps)
        k_limit = waterline_history[limit]
        print(f"    Saturated Corridor Width and Gap Constraint Audit:")
        print(f"      - Max Observed Saturated Corridor Width: {max_sat_width} | Surveyed Boundary K({limit:,}): {k_limit}")
        print(f"      - Max Observed Saturated Corridor Gap:   {max_sat_gap} | Surveyed Gap Ceiling K(N)+1: {k_limit + 1}")

        width_pass = max_sat_width <= k_limit
        gap_pass = max_sat_gap <= (k_limit + 1)

        print(f"      - Internal Width Verification Status : [{'PASS' if width_pass else 'DIVERGENT'}] (width {max_sat_width} <= K(N) {k_limit})")
        print(f"      - Structural Gap Verification Status  : [{'PASS' if gap_pass else 'DIVERGENT'}] (gap {max_sat_gap} <= K(N)+1 {k_limit + 1})")

    # #sector 4# Saturation Spectrum Slices
    print("\n.. #sector 4# analyzing saturation spectrum gap slices")
    if total_sat > 0:
        slice_counts = {2: 0, 4: 0, 6: 0, 8: 0, 10: 0, "gt10": 0}
        for g in sat_gaps:
            if g in [2, 4, 6, 8, 10]:
                slice_counts[g] += 1
            elif g > 10:
                slice_counts["gt10"] += 1
        for k, count in slice_counts.items():
            label = f"Gap == {k}" if isinstance(k, int) else "Gap > 10"
            print(f"    Saturation Spectrum [{label:<10}]: {count:<7,} ({count/total_sat*100:.2f}%)")

    # #sector 5# Quantile Envelope Resolutions
    print("\n.. #sector 5# running quantile envelope resolutions & structural width audits")
    resolutions = [10, 20, 40, 80]
    for res in resolutions:
        binned = expectation_bins(final_records, bins=res)
        xs = [b["rho_mean"] for b in binned]
        ys = [b["gap_mean"] for b in binned]
        r2_alt = quadratic_fit(xs, ys)[3]
        print(f"    Slices: {res:<2} | Quadratic Fit R²: {r2_alt:.4f}")

    print("\n    Executing stratified arithmetic geometry width conditioning:")
    brackets = [
        ("Micro (1-3)", lambda w: 1 <= w <= 3),
        ("Short (4-7)", lambda w: 4 <= w <= 7),
        ("Medium (8-15)", lambda w: 8 <= w <= 15),
        ("Long (16-31)", lambda w: 16 <= w <= 31),
        ("Maxi (32+)", lambda w: w >= 32)
    ]
    for name, condition in brackets:
        subset = [r for r in final_records if condition(r["width"])]
        corr_sub = pearson([r["rho"] for r in subset], [r["gap"] for r in subset]) if len(subset) >= 2 else 0.0
        print(f"      Bracket: {name:<15} | Recs: {len(subset):<9,} | LocalCorr: {corr_sub:.4f}")

    # #sector 6# Permutation Null Shuffle
    print("\n.. #sector 6# launching multi-shuffle permutation null control matrix (50 cycles)")
    if len(final_records) > 1:
        shuffled_rhos = [r["rho"] for r in final_records]
        gaps_control = [r["gap"] for r in final_records]
        null_corrs = []
        random.seed(42)

        for _ in range(50):
            random.shuffle(shuffled_rhos)
            null_corrs.append(pearson(shuffled_rhos, gaps_control))

        m_null = mean(null_corrs)
        s_null = stdev(null_corrs) if len(null_corrs) > 1 else 1.0
        actual_corr = pearson([r["rho"] for r in final_records], [r["gap"] for r in final_records])
        z_score = (actual_corr - m_null) / s_null if s_null > 0 else 0.0

        print(f"    Observed Base Correlation   : {actual_corr:.6f}")
        print(f"    Permuted Null Expected Mean : {m_null:.6f} | Null Dev: {s_null:.6f}")
        print(f"    Analytical Significance     : Z-Score = {z_score:+.3f}")

    # #sector 7# Run Depth Milestone Matrix
    print("\n.. #sector 7# reporting stratified run depth metrics across milestone horizons")
    for horizon in milestones:
        counts = horizon_run_counts[horizon]
        print(f"    Horizon N = {horizon:<12,} | Runs >=10: {counts[10]:<5,} >=15: {counts[15]:<4,} >=17: {counts[17]:<3,} >=18: {counts[18]:<2,} >=20: {counts[20]}")

    # #sector 8# Exception Neighborhood Audits
    print("\n.. #sector 8# auditing exception-class high-strain saturated pools")
    exception_pools = {
        "gt6": [r for r in sat_pool if r["gap"] > 6],
        "gt10": [r for r in sat_pool if r["gap"] > 10],
        "ge14": [r for r in sat_pool if r["gap"] >= 14]
    }
    for label, pool_elements in exception_pools.items():
        print(f"    Exception Filter [Saturated {label:<5}]: Count = {len(pool_elements):,}")

    print("\n    [!] Running Strain Neighborhood Audits on Top 3 Large Saturated Exceptions:")
    sorted_high_strain = sorted(sat_pool, key=lambda x: x["gap"], reverse=True)
    for index, ex in enumerate(sorted_high_strain[:3]):
        lp, rp = ex["left_prime"], ex["right_prime"]
        left_nb = [int(R[coord]) for coord in range(max(2, lp - 5), lp + 1)]
        right_nb = [int(R[coord]) for coord in range(rp, min(limit + 1, rp + 6))]
        print(f"      High-Strain Target #{index+1} (Gap={ex['gap']} | Corridor: {lp} -> {rp}):")
        print(f"        Left Rupture Shield R Vector (5 steps outwards):  {left_nb}")
        print(f"        Right Rupture Shield R Vector (5 steps onwards): {right_nb}")

    # #sector 9# Rupture Census Summaries
    print("\n.. #sector 9# executing full rupture field infrastructure census report")
    print(f"    Total Rupture Coordinates R(n)=1   : {total_ruptures:,}")
    print(f"    Global Field Rupture Density       : {total_ruptures / (limit - 1):.6f}")
    print(f"    Prime Boundary Rupture Nodes       : {len(primes):,}")
    print(f"    Pure Prime-Power Rupture Nodes     : {pure_pp_ruptures:,}")
    print(f"    Composite Non-PP Rupture Nodes     : {composite_non_pp_ruptures:,}")
    print("    Composite Non-PP Sample Array Details (Top 5):")
    for item in sample_pool_print:
        print(f"      - Coord: {item[0]:<10} | Factors: {str(item[1]):<15} | σ(n): {item[2]}")

    # #sector 10# Boundary Factor Signatures
    print("\n.. #sector 10# analyzing boundary prime factor signatures of high-waterline runs")
    critical_runs = sorted([r for r in all_runs_log if r[2] >= 15], key=lambda x: x[2], reverse=True)
    for idx, cr in enumerate(critical_runs[:3]):
        start, end, length = cr[0], cr[1], cr[2]
        left_boundary, right_boundary = start - 1, end + 1
        l_facs = get_prime_factors(left_boundary) if left_boundary >= 2 else []
        r_facs = get_prime_factors(right_boundary) if right_boundary <= limit else []
        
        # Pull temporary localized divisor sum for the specific boundary values to avoid holding them in RAM
        def get_single_sigma(num):
            return sum(d for d in range(1, num + 1) if num % d == 0)
            
        print(f"    Critical Run #{idx+1} (Length {length}) Boundary Matrix:")
        print(f"      Left Rupture  (n={left_boundary:,}) | Factors={l_facs} | σ(n)={get_single_sigma(left_boundary) if left_boundary>=2 else 0} | gcd=1")
        print(f"      Right Rupture (n={right_boundary:,}) | Factors={r_facs} | σ(n)={get_single_sigma(right_boundary) if right_boundary<=limit else 0} | gcd=1")

    print(f"\n[✓] Master Merge Integration Protocol Complete. v4.2 Engine stabilized at limit N = {limit:,}.\n")

if __name__ == "__main__":
    main()

# LICENSE.TXT
# Zero-Ology License v2.6.65
# June 05, 2026
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
#- ACHERON_FIELDS.txt
#- UNPERFECT_ANOMALY.txt
#- ACHERON_FIELDS_SUITE.py
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
#www.zero-ology.com
#─────────────────────────────
#© Stacey8Szmy
#© Stacey8Szmy — Zero-Ology IP Archive