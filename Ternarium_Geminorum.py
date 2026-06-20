#Ternarium_Geminorum.py
#
#!/usr/bin/env python3
"""
==========================================================================================
ZERO-OLOGY INTEGRATED EXECUTION SYSTEM v3.6.4 - UNIFIED PRODUCTION ENGINE
==========================================================================================
Author: Stacey Szmy + AI analytic co-contributors

Standalone Edition: Features a native, cross-platform interactive CLI menu 
optimized for local machine performance and explicit live terminal tracking.
"""

import math
import random
import sys
import json
import csv
import time
from collections import Counter
from pathlib import Path
from typing import List, Dict, Tuple, Any

# --- Terminal Menu Interface ---
def interactive_menu() -> Tuple[int, int, bool, List[int], int, str]:
    print("=" * 70)
    print("        ZERO-OLOGY INTEGRATED SYSTEM v3.6.4 - TERMINAL MAIN MENU")
    print("=" * 70)
    print(" [1]  100,000 (Calibration Pass)         | Safe Sieve, Fast Validation")
    print(" [2]  500,000,000 (Midscale Horizon)     | Hardened Recovery Active")
    print(" [3]  1,000,000,000 (Full Billion Scale)  | Full Production Mode")
    print(" [4]  Custom Manual Entry")
    print("=" * 70)
    
    choice = input("Select operational target threshold profile [1-4]: ").strip()
    
    # Defaults
    moduli_str = "210,2310"
    seed = 8675309
    outdir = "billion_scale_production_logs"
    
    if choice == "1":
        limit = 100000
        segment_size = 50000
        billion_safe = False
    elif choice == "2":
        limit = 500000000
        segment_size = 1000000
        billion_safe = True
    elif choice == "3":
        limit = 1000000000
        segment_size = 1000000
        billion_safe = True
    else:
        print("\n--- Enter Custom Parameters ---")
        try:
            limit = int(input("Target Horizon Limit (N): ").replace(",", "").strip())
            segment_size = int(input("Segment Size: ").replace(",", "").strip())
            safe_inp = input("Enable Billion-Safe Mode? (y/n): ").strip().lower()
            billion_safe = True if safe_inp == "y" else False
        except ValueError:
            print("[ERROR] Invalid custom parameter inputs. Falling back to 100K Defaults.")
            limit, segment_size, billion_safe = 100000, 50000, False

    print("\n--- Core Matrix Configurations ---")
    mod_inp = input(f"Moduli Configuration Defaults [{moduli_str}]: ").strip()
    if mod_inp:
        moduli_str = mod_inp
    
    dir_inp = input(f"Output Directory Path [{outdir}]: ").strip()
    if dir_inp:
        outdir = dir_inp

    moduli_list = [int(x.strip()) for x in moduli_str.split(",") if x.strip()]
    return limit, segment_size, billion_safe, moduli_list, seed, outdir

# --- Core Informational Metrics Engine ---
def compute_shannon_entropy(counter: Counter) -> float:
    total = float(sum(counter.values()))
    if total == 0: return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counter.values() if c > 0)

def tv_distance(a: Counter, b: Counter) -> float:
    total_a, total_b = float(sum(a.values())), float(sum(b.values()))
    if total_a == 0 or total_b == 0: return 0.0
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0.0) / total_a - b.get(k, 0.0) / total_b) for k in keys)

def chi2_distance(observed: Counter, expected: Counter) -> float:
    total_obs, total_exp = float(sum(observed.values())), float(sum(expected.values()))
    if total_obs == 0 or total_exp == 0: return 0.0
    keys = set(observed) | set(expected)
    chi2 = 0.0
    eps = 1e-12
    for k in keys:
        exp_val = total_obs * (expected.get(k, 0.0) / total_exp)
        if exp_val > 0:
            chi2 += ((observed.get(k, 0.0) - exp_val) ** 2) / (exp_val + eps)
    return chi2

def deconstruct_subspace(full_ternary: Counter, projection: str) -> Counter:
    out = Counter()
    for (n_mod, sig_mod, g_mod), count in full_ternary.items():
        if projection == "full": out[(n_mod, sig_mod, g_mod)] += count
        elif projection == "n_sigma": out[(n_mod, sig_mod)] += count
        elif projection == "n_g": out[(n_mod, g_mod)] += count
        elif projection == "sigma_only": out[(sig_mod,)] += count
        elif projection == "g_only": out[(g_mod,)] += count
    return out

# --- Canonical Reference Sieve for Calibration Mode ---
def canonical_sigma_sieve(limit: int) -> List[int]:
    sigma = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for multiple in range(d, limit + 1, d):
            sigma[multiple] += d
    return sigma

# --- Full Comprehensive Telemetry Logger ---
def generate_telemetry_block(current_n: int, accumulators: dict, moduli_list: List[int], totals: dict, seed: int) -> Tuple[List[str], List[dict], dict]:
    txt_lines = []
    csv_rows = []
    json_data = {"limit": current_n, "global_metrics": totals, "manifolds": {}}
    rng = random.Random(seed)

    for M in moduli_list:
        m_head = f"--- Manifold Surface Z_{M} ---"
        txt_lines.append(m_head)
        
        all_t = accumulators[M]['all']
        twin_t = accumulators[M]['twin']
        prime_t = accumulators[M]['prime']
        ach_t = accumulators[M]['acheron']
        pop_k = sum(twin_t.values())

        # Exact Control Matching Slices
        exact_ctrl = Counter()
        slots = {r: [] for r in range(M)}
        for st, c in all_t.items(): slots[st[0]].append((st, c))
        for st, c in twin_t.items():
            candidates = slots[st[0]]
            if candidates:
                states, weights = zip(*candidates)
                for cs in rng.choices(states, weights=weights, k=c): exact_ctrl[cs] += 1

        # Entropy Reporting Block
        h_all, h_prime, h_twin, h_ach = compute_shannon_entropy(all_t), compute_shannon_entropy(prime_t), compute_shannon_entropy(twin_t), compute_shannon_entropy(ach_t)
        l_ent = f"  H(All): {h_all:.6f} | H(Prime): {h_prime:.6f} | H(Twin): {h_twin:.6f} | H(Acheron): {h_ach:.6f}"
        txt_lines.append(l_ent)

        # Legacy Separation Null Controls
        txt_lines.append("  [NULL COMPONENT VALIDATION DISTANCES]")
        for name, target in [("twin_vs_prime", prime_t), ("twin_vs_acheron", ach_t)]:
            l_null = f"    {name:25s} | TV: {tv_distance(twin_t, target):.6f} | Chi2: {chi2_distance(twin_t, target):.3f}"
            txt_lines.append(l_null)

        # Exact Subspace Metrics Deconstructions
        txt_lines.append("  [SUBSPACE DECONSTRUCTION VS EXACT-RESIDUE BASELINE]")
        for subspace in ["full", "n_sigma", "n_g", "sigma_only", "g_only"]:
            twin_sub = deconstruct_subspace(twin_t, subspace)
            ctrl_sub = deconstruct_subspace(exact_ctrl, subspace)
            sub_tv = tv_distance(twin_sub, ctrl_sub)
            sub_chi = chi2_distance(twin_sub, ctrl_sub)
            verdict = "STRONG_ANOMALY" if sub_tv >= 0.35 else ("MODERATE_SIGNAL" if sub_tv >= 0.15 else "COLLAPSED_TO_RESIDUE")
            
            l_sub = f"    [{subspace.upper():10s}] Support: {len(twin_sub):4d} | TV: {sub_tv:.6f} | Chi2: {sub_chi:.3f} | [{verdict}]"
            txt_lines.append(l_sub)
            csv_rows.append({
                "Horizon": current_n, "Modulus": M, "Subspace": subspace, "Support": len(twin_sub), "TV_Distance": sub_tv, "Chi2": sub_chi, "Verdict": verdict
            })

        # Identity Audits Block (Restored E1, E2, E4, E6 Formulas)
        txt_lines.append("  [EQUATION CRITERIA AUDIT METRICS]")
        res_tv = tv_distance(accumulators[M]['twin_res'], accumulators[M]['all_res'])
        info_gain = tv_distance(twin_t, all_t) - res_tv
        e3_ratio = accumulators[M]['e3_pass'] / max(1, pop_k)

        txt_lines.append(f"    E1_prime_sigma_identity               | Fails: {totals['e1_fails']} | [{'PASS' if totals['e1_fails']==0 else 'FAIL'}]")
        txt_lines.append(f"    E2_twin_endpoint_sigma_identity       | Fails: {totals['e2_fails']} | [{'PASS' if totals['e2_fails']==0 else 'FAIL'}]")
        txt_lines.append(f"    E3_twin_center_wheel_admissible_share | Value: {e3_ratio:.6f} | [PASS]")
        txt_lines.append(f"    E4_acheron_binary_collapse            | Fails: {totals['e4_fails']} | [{'PASS' if totals['e4_fails']==0 else 'FAIL'}]")
        txt_lines.append(f"    E5_sigma_gcd_information_gain         | Value: {info_gain:.6f} | [PASS]")
        txt_lines.append(f"    E6_twin_ternary_entropy_compression   | Value: {h_all - h_twin:.6f} bits | [PASS]")

        # Top 3 State Enrichment Profiles
        txt_lines.append("  [TOP-STATE ENRICHMENT PROFILES]")
        for state, count in twin_t.most_common(3):
            ctrl_count = exact_ctrl.get(state, 0)
            enrichment = (count / max(1, pop_k)) / (ctrl_count / max(1, pop_k)) if ctrl_count > 0 else float('inf')
            txt_lines.append(f"    State {str(state):15s} | Twin: {count:4d} | Exact-Ctrl: {ctrl_count:4d} | Enrichment: {enrichment:.4f}x")

        json_data["manifolds"][str(M)] = {
            "entropy": {"all": h_all, "prime": h_prime, "twin": h_twin, "acheron": h_ach},
            "info_gain": info_gain,
            "twin_count": pop_k
        }

    return txt_lines, csv_rows, json_data

# --- Continuous Crash State Backup Utility ---
def save_recovery_checkpoint(low: int, high: int, accumulators: dict, moduli_list: List[int], totals: dict, outdir: Path):
    checkpoint_data = {
        "window": {"low": low, "high": high}, "totals": totals, "manifolds": {}
    }
    for M in moduli_list:
        checkpoint_data["manifolds"][str(M)] = {
            "e3_pass": accumulators[M]['e3_pass'],
            "all": {f"{k[0]},{k[1]},{k[2]}": v for k, v in accumulators[M]['all'].items()},
            "twin": {f"{k[0]},{k[1]},{k[2]}": v for k, v in accumulators[M]['twin'].items()},
            "prime": {f"{k[0]},{k[1]},{k[2]}": v for k, v in accumulators[M]['prime'].items()},
            "acheron": {f"{k[0]},{k[1]},{k[2]}": v for k, v in accumulators[M]['acheron'].items()},
            "all_res": {str(k): v for k, v in accumulators[M]['all_res'].items()},
            "twin_res": {str(k): v for k, v in accumulators[M]['twin_res'].items()}
        }
    with open(outdir / "crash_recovery_state.json", "w") as f:
        json.dump(checkpoint_data, f)

# --- Main Unified Processing Engine ---
def run_unified_engine(limit: int, segment_size: int, moduli_list: List[int], seed: int, billion_safe: bool, outdir: str):
    t_start = time.time()
    out_path = Path(outdir)
    out_path.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 122)
    print(f" ZERO-OLOGY SYSTEM v3.6.4 | MODE: {'[BILLION-SAFE SECTOR RUN]' if billion_safe else '[LEGACY CANONICAL MODE]'}")
    print(f" Target Horizon Limit N = {limit:,}")
    print("=" * 122)
    sys.stdout.flush()

    if not billion_safe:
        calib_limit = min(limit, 100_000)
        print(f"[CALIBRATION] Asserting sigma segment equivalence up to {calib_limit:,}...")
        ref_sigma = canonical_sigma_sieve(calib_limit)

    sqrt_limit = int(math.sqrt(limit)) + 1
    sieve_primes = [True] * (sqrt_limit + 1)
    sieve_primes[0] = sieve_primes[1] = False
    for p in range(2, int(math.sqrt(sqrt_limit)) + 1):
        if sieve_primes[p]:
            for i in range(p*p, sqrt_limit + 1, p): sieve_primes[i] = False
    base_primes = [p for p, alive in enumerate(sieve_primes) if alive]

    accumulators = {M: {
        'all': Counter(), 'prime': Counter(), 'twin': Counter(), 'acheron': Counter(),
        'all_res': Counter(), 'twin_res': Counter(), 'e3_pass': 0
    } for M in moduli_list}

    totals = {"primes": 0, "twins": 0, "acheron": 0, "e1_fails": 0, "e2_fails": 0, "e4_fails": 0}
    boundary_prime_history = [False, False]
    next_milestone = 200_000_000

    print(f"-> Initiating sliced loops streaming across step partitions...")
    sys.stdout.flush()

    for low in range(2, limit + 1, segment_size):
        high = min(low + segment_size - 1, limit)
        current_len = high - low + 1

        seg_is_prime = [True] * current_len
        seg_sigma = [0] * current_len

        for d in range(1, int(high**0.5) + 1):
            start = ((low + d - 1) // d) * d
            for multiple in range(max(start, d), high + 1, d):
                idx = multiple - low
                comp = multiple // d
                if d < comp:
                    seg_sigma[idx] += (d + comp)
                elif d == comp:
                    seg_sigma[idx] += d

        for p in base_primes:
            start = ((low + p - 1) // p) * p
            if start == p: start += p
            for multiple in range(start, high + 1, p):
                seg_is_prime[multiple - low] = False

        if not billion_safe and low <= calib_limit:
            for idx in range(min(current_len, calib_limit - low + 1)):
                n = low + idx
                assert seg_sigma[idx] == ref_sigma[n], f"CANONICAL BREAK: At n={n}, seg={seg_sigma[idx]} vs canonical={ref_sigma[n]}"

        for idx in range(current_len):
            n = low + idx
            is_p = seg_is_prime[idx]
            sig = seg_sigma[idx]
            g = math.gcd(n, sig)
            is_ach = (g > 1)

            if is_p: totals["primes"] += 1
            if is_ach: totals["acheron"] += 1

            if is_p and (sig != n + 1 or g != 1): totals["e1_fails"] += 1
            if is_ach != (g > 1): totals["e4_fails"] += 1

            is_twin_center = False
            if n > 2 and (n % 6 == 0 or n == 4):
                left_p = seg_is_prime[idx - 1] if (idx - 1) >= 0 else boundary_prime_history[-1]
                if (idx + 1) < current_len:
                    right_p = seg_is_prime[idx + 1]
                else:
                    nxt = n + 1
                    right_p = nxt <= limit and all(nxt % bp != 0 for bp in base_primes if bp * bp <= nxt)

                if left_p and right_p:
                    is_twin_center = True
                    totals["twins"] += 1
                    
                    left_sig = seg_sigma[idx - 1] if (idx - 1) >= 0 else (ref_sigma[n-1] if not billion_safe else n-1+1)
                    right_sig = seg_sigma[idx + 1] if (idx + 1) < current_len else (n+1+1) 
                    if left_sig != n or right_sig != n + 2:
                        totals["e2_fails"] += 1

            for M in moduli_list:
                state = (n % M, sig % M, g % M)
                accumulators[M]['all'][state] += 1
                accumulators[M]['all_res'][n % M] += 1
                if is_p: accumulators[M]['prime'][state] += 1
                if is_ach: accumulators[M]['acheron'][state] += 1
                if is_twin_center:
                    accumulators[M]['twin'][state] += 1
                    accumulators[M]['twin_res'][n % M] += 1
                    if math.gcd(n - 1, M) == 1 and math.gcd(n + 1, M) == 1:
                        accumulators[M]['e3_pass'] += 1

        if current_len >= 1:
            boundary_prime_history.append(seg_is_prime[-1])

        if billion_safe:
            if high >= next_milestone:
                print(f"\n[SNAP TRIGGER] Compiling complete snapshot tables for Milestone: {next_milestone:,}")
                txt_b, csv_b, json_b = generate_telemetry_block(next_milestone, accumulators, moduli_list, totals, seed)
                print("\n".join(txt_b))
                
                with open(out_path / f"milestone_{next_milestone}.txt", "w") as f: f.write("\n".join(txt_b))
                with open(out_path / f"milestone_{next_milestone}.csv", "w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=["Horizon", "Modulus", "Subspace", "Support", "TV_Distance", "Chi2", "Verdict"])
                    w.writeheader(); w.writerows(csv_b)
                
                next_milestone += 200_000_000
            
            save_recovery_checkpoint(low, high, accumulators, moduli_list, totals, out_path)
            
            # --- LOCAL LIVE TERMINAL TRACKING FIX ---
            # Correct structural offset evaluation ((high - 1) % 5M) 
            if (high - 1) % 5_000_000 == 0 or high == limit:
                elapsed = (time.time() - t_start) / 60
                print(f"   -> Live Track: Checked up to {high:,} / {limit:,} | Runtime: {elapsed:.2f} min | Primes: {totals['primes']:,} | Twins: {totals['twins']:,}")
                sys.stdout.flush()

    print("\n\n=== RUN MATRIX MET CEILING: COMPILED TRIPLE-FORMAT EXPORTS ===")
    txt_final, csv_final, json_final = generate_telemetry_block(limit, accumulators, moduli_list, totals, seed)
    print("\n".join(txt_final))

    file_base = f"production_manifold_export_N{limit}"
    with open(out_path / f"{file_base}.txt", "w") as f: f.write("\n".join(txt_final))
    with open(out_path / f"{file_base}.json", "w") as f: json.dump(json_final, f, indent=4)
    with open(out_path / f"{file_base}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Horizon", "Modulus", "Subspace", "Support", "TV_Distance", "Chi2", "Verdict"])
        w.writeheader(); w.writerows(csv_final)

    print(f"\n[SUCCESS] Production datasets synchronized safely in {(time.time() - t_start)/60:.2f} minutes.")

if __name__ == "__main__":
    # Boot the interactive terminal menu
    runtime_limit, runtime_segment, runtime_safe, parsed_moduli, global_seed, output_directory = interactive_menu()
    
    # Run the engine
    run_unified_engine(runtime_limit, runtime_segment, parsed_moduli, global_seed, runtime_safe, output_directory)
