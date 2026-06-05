#ACHERON_FIELDS_SUITE.py
#!/usr/bin/env python3
"""
==========================================================================================
THE ACHERON FIELDS EXTRAPOLATION MASTER SUITE (v4.4 LIVE-STREAMING EDITION - STABLE)
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
    print("      ACHERON FIELDS HORIZON SELECTOR (v4.4 Live-Streaming)       ")
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

def get_single_sigma(num):
    if num < 1: return 0
    total = 1
    p = 2
    temp_n = num
    while p * p <= temp_n:
        if temp_n % p == 0:
            p_sum = 1
            p_pow = 1
            while temp_n % p == 0:
                p_pow *= p
                p_sum += p_pow
                temp_n //= p
            total *= p_sum
        p += 1 if p == 2 else 2
    if temp_n > 1:
        total *= (1 + temp_n)
    return total

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

def main():
    limit = interactive_menu()

    print(__doc__)
    print(f"[*] Initializing Optimized Target Pool Upper Horizon Limit N = {limit:,}\n")

    print(f"[*] Generating master prime maps up to n = {limit:,}...")
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            for m in range(p * p, limit + 1, p):
                is_prime[m] = 0

    primes = array('I', [n for n in range(2, limit + 1) if is_prime[n]])
    print(f"[+] Primes compiled: {len(primes):,}")

    is_pure_prime_power = bytearray(limit + 1)
    for p in primes:
        val = p * p
        while val <= limit:
            is_pure_prime_power[val] = 1
            if val > limit // p:
                break
            val *= p

    CHUNK_SIZE = 5000000
    print(f"[*] Processing Acheron substrate configurations in segments of {CHUNK_SIZE:,}...")

    A = bytearray(limit + 1)
    
    total_ruptures = 0
    pure_pp_ruptures = 0
    composite_non_pp_ruptures = 0
    sample_pool_print = []

    total_chunks = math.ceil((limit - 1) / CHUNK_SIZE)
    current_chunk_idx = 0

    for chunk_start in range(2, limit + 1, CHUNK_SIZE):
        chunk_end = min(chunk_start + CHUNK_SIZE - 1, limit)
        chunk_len = chunk_end - chunk_start + 1
        current_chunk_idx += 1
        
        local_sigma = array('Q', [1] * chunk_len)
        for d in range(2, chunk_end + 1):
            first_multiplier = max(2, (chunk_start + d - 1) // d)
            start_m = first_multiplier * d
            for m in range(start_m, chunk_end + 1, d):
                local_sigma[m - chunk_start] += d
                
        for n in range(chunk_start, chunk_end + 1):
            sig_val = local_sigma[n - chunk_start]
            if math.gcd(n, sig_val) > 1:
                A[n] = 1
            else:
                total_ruptures += 1
                if is_pure_prime_power[n] == 1:
                    pure_pp_ruptures += 1
                elif is_prime[n] == 0:
                    composite_non_pp_ruptures += 1
                    if len(sample_pool_print) < 5:
                        sample_pool_print.append((n, get_prime_factors(n), sig_val))
        
        pct = (chunk_end / limit) * 100
        print(f"    [Segment Scan] Block {current_chunk_idx}/{total_chunks} processed: [{chunk_start:,} -> {chunk_end:,}] | Progress: {pct:.2f}%", flush=True)

    print(f"\n[+] Substrates compiled. Field Support Density: {sum(A)/(limit-1):.6f}")

    pp_tested = sum(is_pure_prime_power)
    pp_failed = 0
    for n in range(2, limit + 1):
        if is_pure_prime_power[n] == 1 and A[n] != 0:
            pp_failed += 1
    verdict = "[PASS]" if pp_failed == 0 else "[FAIL]"
    print(f"    [Verification] Pure Prime-Power Nodes Checked: {pp_tested:,} | Failures: {pp_failed:,} Verification: {verdict}\n")

    print("[*] Compiling A-run block indexes sequentially...")
    current_run_len = 0
    current_run_start = 0
    run_starts = array('I')
    run_ends = array('I')
    run_lens = array('I')

    for n in range(2, limit + 1):
        if A[n] == 1:
            if current_run_len == 0: current_run_start = n
            current_run_len += 1
        else:
            if current_run_len > 0:
                run_starts.append(current_run_start)
                run_ends.append(n - 1)
                run_lens.append(current_run_len)
                current_run_len = 0
    if current_run_len > 0:
        run_starts.append(current_run_start)
        run_ends.append(limit)
        run_lens.append(current_run_len)

    # #sector 1# Dynamic Waterline Stepwise Extraction
    print("\n.. #sector 1# evaluating stepwise kakós waterline values K(N)")
    milestones = [1000000, 10000000, 50000000, 100000000, 150000000, 200000000, limit]
    milestones = sorted(list(set([m for m in milestones if m <= limit])))

    waterline_history = {}
    horizon_run_counts = {}

    print("\n    [+] ===== KAKÓS WATERLINE TRACKING MATRIX (BOUND-CLIPPED) =====")
    for horizon in milestones:
        max_k = 0
        max_run = None
        depths = [10, 15, 17, 18, 20]
        counts_at_horizon = {d: 0 for d in depths}

        for idx in range(len(run_starts)):
            s = run_starts[idx]
            if s > horizon:
                continue
            e = run_ends[idx]
            clipped_end = min(e, horizon)
            clipped_len = clipped_end - s + 1
            
            if clipped_len > max_k:
                max_k = clipped_len
                max_run = (s, clipped_end, clipped_len)
            
            for d in depths:
                if clipped_len >= d:
                    counts_at_horizon[d] += 1

        if max_run:
            k_n = max_run[2]
            coord_str = f"at [{max_run[0]:,} -> {max_run[1]:,}]"
        else:
            k_n = 0
            coord_str = "N/A"

        waterline_history[horizon] = k_n
        horizon_run_counts[horizon] = counts_at_horizon
        print(f"      Survey Bound N = {horizon:<13,} | Observed Waterline K(N) = {k_n:<2}  {coord_str}")
    print("    ================================================\n")

    # #sector 2# Corridor Truncation Profiles & Streaming Analytics
    print(".. #sector 2# running horizon corridor-density targets and metric profiles")
    
    # Milestone Tracking Aggregators
    m_stats = {m: {"n": 0, "sx": 0.0, "sy": 0.0, "sx2": 0.0, "sy2": 0.0, "sxy": 0.0, 
                   "sat_sum": 0, "sat_cnt": 0, "groups": defaultdict(lambda: [0, 0.0])} for m in milestones}
    
    # #sector 5# Streaming Bracket Statistics Tracking Arrays
    # Format: [n, sx, sy, sx2, sy2, sxy]
    bracket_accumulators = {
        "Micro (1-3)": [0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Short (4-7)": [0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Medium (8-15)": [0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Long (16-31)": [0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Maxi (32+)": [0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
    
    # #sector 3# & #sector 4# Global Saturated Stream Collectors
    total_sat = 0
    sat_gap_sum = sat_gap_max = sat_width_max = 0
    sat_gaps_list = array('I') # Small footprint tracker reserved specifically for median calculation
    slice_counts = {2: 0, 4: 0, 6: 0, 8: 0, 10: 0, "gt10": 0}
    ex_gt6 = ex_gt10 = ex_ge14 = 0
    
    # #sector 5# Resolution Quantile Envelope Matrix Accumulators
    resolutions = [10, 20, 40, 80]
    res_bins = {r: [{"cnt": 0, "gap_sum": 0.0, "rho_sum": 0.0} for _ in range(r)] for r in resolutions}
    
    # #sector 8# Bounded Dynamic Insertion Filter for Top 3 High-Strain Target Storage
    # Stores tuples of (left_prime, right_prime, gap, width)
    top_3_high_strain = []

    # #sector 6# Sampling Arrays for Permutation Control
    sample_rhos = array('d')
    sample_gaps = array('I')
    sample_max = 250000
    sample_interval = max(1, (len(primes) - 2) // sample_max)

    for i in range(1, len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        gap = q - p
        width = gap - 1
        if width <= 0: 
            continue
            
        a_count = sum(A[m] for m in range(p + 1, q))
        rho = a_count / width
        
        # Populate Permutation Sample Matrix on the fly
        if i % sample_interval == 0 and len(sample_rhos) < sample_max:
            sample_rhos.append(rho)
            sample_gaps.append(gap)
            
        # Single-pass dynamic update of cumulative milestone horizons
        for m in milestones:
            if q > m:
                continue
            st = m_stats[m]
            st["n"] += 1
            st["sx"] += rho
            st["sy"] += gap
            st["sx2"] += rho * rho
            st["sy2"] += gap * gap
            st["sxy"] += rho * gap
            
            # Map grouped structures for Quadratic Fit requirements
            st["groups"][(a_count, width)][0] += 1
            st["groups"][(a_count, width)][1] += gap
            
            if a_count == width:
                st["sat_cnt"] += 1
                st["sat_sum"] += gap

        # Global final terminal analysis assignments (Crossed Upper Bound Threshold)
        if a_count == width:
            total_sat += 1
            sat_gap_sum += gap
            sat_gaps_list.append(gap)
            if gap > sat_gap_max: sat_gap_max = gap
            if width > sat_width_max: sat_width_max = width
            
            # Slices updates (#sector 4#)
            if gap in [2, 4, 6, 8, 10]:
                slice_counts[gap] += 1
            elif gap > 10:
                slice_counts["gt10"] += 1
                
            # Streaming high-strain exception tracking counts (#sector 8#)
            if gap > 6: ex_gt6 += 1
            if gap > 10: ex_gt10 += 1
            if gap >= 14: ex_ge14 += 1
            
            # Continuous Top-3 High Strain Exception sorting insertion filter
            if len(top_3_high_strain) < 3:
                top_3_high_strain.append((p, q, gap, width))
                top_3_high_strain.sort(key=lambda x: x[2], reverse=True)
            elif gap > top_3_high_strain[-1][2]:
                top_3_high_strain[-1] = (p, q, gap, width)
                top_3_high_strain.sort(key=lambda x: x[2], reverse=True)

        # Quantile Matrix updates (#sector 5#)
        for r in resolutions:
            idx = min(r - 1, int(rho * r))
            res_bins[r][idx]["cnt"] += 1
            res_bins[r][idx]["gap_sum"] += gap
            res_bins[r][idx]["rho_sum"] += rho

        # Stratified Geometry Audits (#sector 5#)
        br_name = None
        if 1 <= width <= 3: br_name = "Micro (1-3)"
        elif 4 <= width <= 7: br_name = "Short (4-7)"
        elif 8 <= width <= 15: br_name = "Medium (8-15)"
        elif 16 <= width <= 31: br_name = "Long (16-31)"
        elif width >= 32: br_name = "Maxi (32+)"
        
        if br_name:
            ba = bracket_accumulators[br_name]
            ba[0] += 1
            ba[1] += rho
            ba[2] += gap
            ba[3] += rho * rho
            ba[4] += gap * gap
            ba[5] += rho * gap

    # Display Milestone Analytics Output Stream
    for m in milestones:
        st = m_stats[m]
        nrec = st["n"]
        if nrec >= 2:
            denx = math.sqrt(nrec * st["sx2"] - st["sx"] * st["sx"])
            deny = math.sqrt(nrec * st["sy2"] - st["sy"] * st["sy"])
            corr_t = ((nrec * st["sxy"] - st["sx"] * st["sy"]) / (denx * deny)) if denx and deny else 0.0
        else:
            corr_t = 0.0

        v_rhos, m_gaps = [], []
        for (a_cnt, wth), (cnt, gap_sum) in st["groups"].items():
            if cnt >= 100:
                v_rhos.append(a_cnt / wth)
                m_gaps.append(gap_sum / cnt)
                
        r2_exclusive = quadratic_fit(v_rhos, m_gaps)[3] if len(v_rhos) >= 3 else 0.0
        sat_floor_t = st["sat_sum"] / st["sat_cnt"] if st["sat_cnt"] else 0.0
        
        print(f"    Target N: {m:<12,} | Corridors: {nrec:<9,} | BaseCorr: {corr_t:<8.4f} | BinExclR²: {r2_exclusive:<8.4f} | SatFloor: {sat_floor_t:.4f}")

    # #sector 3# Saturated Sinks Distribution Profiling
    print("\n.. #sector 3# running saturation distribution configuration audit")
    print(f"    Saturated Count (N) : {total_sat:,}")
    print(f"    Mean Saturated Gap  : {sat_gap_sum / total_sat if total_sat else 0.0:.4f}")
    print(f"    Median Saturated Gap: {median(sat_gaps_list) if total_sat else 0.0:.1f}")
    print(f"    Max Saturated Gap   : {sat_gap_max:,}")

    if total_sat > 0:
        k_limit = waterline_history[limit]
        print(f"    Saturated Corridor Width and Gap Constraint Audit:")
        print(f"      - Max Observed Saturated Corridor Width: {sat_width_max} | Surveyed Boundary K({limit:,}): {k_limit}")
        print(f"      - Max Observed Saturated Corridor Gap:   {sat_gap_max} | Surveyed Gap Ceiling K(N)+1: {k_limit + 1}")

        width_pass = sat_width_max <= k_limit
        gap_pass = sat_gap_max <= (k_limit + 1)

        print(f"      - Internal Width Verification Status : [{'PASS' if width_pass else 'DIVERGENT'}] (width {sat_width_max} <= K(N) {k_limit})")
        print(f"      - Structural Gap Verification Status  : [{'PASS' if gap_pass else 'DIVERGENT'}] (gap {sat_gap_max} <= K(N)+1 {k_limit + 1})")

    # #sector 4# Saturation Spectrum Slices
    print("\n.. #sector 4# analyzing saturation spectrum gap slices")
    if total_sat > 0:
        for k, count in slice_counts.items():
            label = f"Gap == {k}" if isinstance(k, int) else "Gap > 10"
            print(f"    Saturation Spectrum [{label:<10}]: {count:<7,} ({count/total_sat*100:.2f}%)")

    # #sector 5# Quantile Envelope Resolutions & Structural Width Audits
    print("\n.. #sector 5# running quantile envelope resolutions & structural width audits")
    for r in resolutions:
        xs, ys = [], []
        for b in range(r):
            if res_bins[r][b]["cnt"] > 0:
                xs.append(res_bins[r][b]["rho_sum"] / res_bins[r][b]["cnt"])
                ys.append(res_bins[r][b]["gap_sum"] / res_bins[r][b]["cnt"])
        r2_alt = quadratic_fit(xs, ys)[3]
        print(f"    Slices: {r:<2} | Quadratic Fit R²: {r2_alt:.4f}")

    print("\n    Executing stratified arithmetic geometry width conditioning:")
    for name in ["Micro (1-3)", "Short (4-7)", "Medium (8-15)", "Long (16-31)", "Maxi (32+)"]:
        ba = bracket_accumulators[name]
        nrec = ba[0]
        if nrec >= 2:
            denx = math.sqrt(nrec * ba[3] - ba[1] * ba[1])
            deny = math.sqrt(nrec * ba[4] - ba[2] * ba[2])
            corr_sub = ((nrec * ba[5] - ba[1] * ba[2]) / (denx * deny)) if denx and deny else 0.0
        else:
            corr_sub = 0.0
        print(f"      Bracket: {name:<15} | Recs: {nrec:<9,} | LocalCorr: {corr_sub:.4f}")

    # #sector 6# Permutation Null Shuffle (Sub-Sampled Matrix Optimization)
    print("\n.. #sector 6# launching multi-shuffle permutation null control matrix (50 cycles)")
    if len(sample_rhos) > 1:
        xs_sample = list(sample_rhos)
        ys_sample = list(sample_gaps)
        nrec = len(xs_sample)
        
        sum_y = sum(ys_sample)
        sum_y2 = sum(y * y for y in ys_sample)
        my = sum_y / nrec
        deny = math.sqrt(sum_y2 - sum_y * sum_y / nrec)

        null_corrs = []
        shuffled_rhos = list(xs_sample)
        total_cycles = 50
        
        random.seed(42)
        for cycle in range(1, total_cycles + 1):
            random.shuffle(shuffled_rhos)
            
            # Ultra-fast integrated correlation loop
            mx = sum(shuffled_rhos) / nrec
            num = sum((x - mx) * (y - my) for x, y in zip(shuffled_rhos, ys_sample))
            denx = math.sqrt(sum((x - mx) ** 2 for x in shuffled_rhos))
            
            null_corrs.append(num / (denx * deny) if denx and deny else 0.0)
            
            percent = (cycle / total_cycles) * 100
            bar = "█" * (cycle // 2) + "░" * (25 - (cycle // 2))
            print(f"\r    [Permutation Progress] |{bar}| Cycle {cycle}/{total_cycles} ({percent:.0f}%)", end="", flush=True)
        print("\n")

        m_null = mean(null_corrs)
        s_null = stdev(null_corrs) if len(null_corrs) > 1 else 1.0
        
        # Calculate actual baseline sample correlation
        mx_act = sum(xs_sample) / nrec
        num_act = sum((x - mx_act) * (y - my) for x, y in zip(xs_sample, ys_sample))
        denx_act = math.sqrt(sum((x - mx_act) ** 2 for x in xs_sample))
        actual_corr = (num_act / (denx_act * deny)) if denx_act and deny else 0.0
        
        z_score = (actual_corr - m_null) / s_null if s_null > 0 else 0.0
        print(f"    Observed Base Correlation (Sample) : {actual_corr:.6f}")
        print(f"    Permuted Null Expected Mean        : {m_null:.6f} | Null Dev: {s_null:.6f}")
        print(f"    Analytical Significance            : Z-Score = {z_score:+.3f}")

    # #sector 7# Run Depth Milestone Matrix
    print("\n.. #sector 7# reporting stratified run depth metrics across milestone horizons")
    for horizon in milestones:
        counts = horizon_run_counts[horizon]
        print(f"    Horizon N = {horizon:<12,} | Runs >=10: {counts[10]:<5,} >=15: {counts[15]:<4,} >=17: {counts[17]:<3,} >=18: {counts[18]:<2,} >=20: {counts[20]}")

    # #sector 8# Exception Neighborhood Audits
    print("\n.. #sector 8# auditing exception-class high-strain saturated pools")
    print(f"    Exception Filter [Saturated gt6 ]: Count = {ex_gt6:,}")
    print(f"    Exception Filter [Saturated gt10]: Count = {ex_gt10:,}")
    print(f"    Exception Filter [Saturated ge14]: Count = {ex_ge14:,}")

    print("\n    [!] Running Strain Neighborhood Audits on Top 3 Large Saturated Exceptions:")
    for index, ex in enumerate(top_3_high_strain):
        lp, rp = ex[0], ex[1]
        left_nb = [1 - int(A[coord]) for coord in range(max(2, lp - 5), lp + 1)]
        right_nb = [1 - int(A[coord]) for coord in range(rp, min(limit + 1, rp + 6))]
        print(f"      High-Strain Target #{index+1} (Gap={ex[2]} | Corridor: {lp} -> {rp}):")
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
    critical_indices = sorted(range(len(run_lens)), key=lambda k: run_lens[k], reverse=True)
    for idx, run_idx in enumerate(critical_indices[:3]):
        start = run_starts[run_idx]
        end = run_ends[run_idx]
        length = run_lens[run_idx]
        
        left_boundary, right_boundary = start - 1, end + 1
        l_facs = get_prime_factors(left_boundary) if left_boundary >= 2 else []
        r_facs = get_prime_factors(right_boundary) if right_boundary <= limit else []
        
        print(f"    Critical Run #{idx+1} (Length {length}) Boundary Matrix:")
        print(f"      Left Rupture  (n={left_boundary:,}) | Factors={l_facs} | σ(n)={get_single_sigma(left_boundary) if left_boundary>=2 else 0} | gcd=1")
        print(f"      Right Rupture (n={right_boundary:,}) | Factors={r_facs} | σ(n)={get_single_sigma(right_boundary) if right_boundary<=limit else 0} | gcd=1")

    print(f"\n[✓] Master Merge Integration Protocol Complete. v4.4 Engine stabilized at limit N = {limit:,}.\n")

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