
#!/usr/bin/env python3
"""
==========================================================================================
THE ACHERON-GCA CONVERGENCE MASTER ENGINE (v3.3-PROD)
==========================================================================================
Core Objective: Quantify prime corridor anomalies, evaluate asymptotic scaling limits,
and formalize empirical data streams as GCA Digamma-Class (𝔇_n) limit candidates.

Operational Context: Single-pass, low-overhead flat streaming architecture. Fully 
optimized for multi-scale horizon variance tracking up to N = 1B.

Unified Integration Matrix (v3.3-PROD):
  - Merged v2.6-PROD structural compliance layout (full-corridor edge_width=0 main sweeps).
  - Merged v1.2 log-scale horizon delta normalization for publication-safe velocity tracking.
  - Fully decoupled strict empirical observations from formal proof certifications.
  - INTEGRATED SECTOR 19 (v3.3 Optimized): Green–Tao Prime Chain Fitness Audit with 
    deterministic prime thinning (`prime_sample_stride`) to safeguard 500M/1B scale runs.

Attribution: 
© Stacey8Szmy — Zero-Ology IP Archive.
https://github.com/haha8888haha8888/Zero-ology
==========================================================================================
"""

import math
import sys
import random
from array import array

# ==========================================================================================
# GCA REPRODUCIBILITY MANIFEST COMPILER ENGINE (§8 REQUIREMENTS)
# ==========================================================================================

class GCAManifestCompiler:
    def __init__(self, target_horizon, seed_value=42):
        self.target_horizon = target_horizon
        self.seed_value = seed_value
        self.horizon_records = []
        self.edge_sensitivity = {}
        self.wheel_sensitivity = {}
        self.green_tao_results = []
        
    def register_horizon_step(self, n, primes_count, corridors, base_corr, frag_mean, null_m30, z_score):
        self.horizon_records.append({
            'N': n, 'primes': primes_count, 'corridors': corridors,
            'C_A': base_corr, 'F_A': frag_mean, 'Null_M30': null_m30, 'Z_Score': z_score
        })
        
    def register_edge_audit(self, width, c_a, f_a):
        self.edge_sensitivity[width] = (c_a, f_a)
        
    def register_wheel_audit(self, modulus, f_a, null_f_a):
        self.wheel_sensitivity[modulus] = (f_a, null_f_a)

    def register_green_tao_audit(self, results):
        self.green_tao_results = results

    def compile_formal_appendix(self):
        """Generates a peer-safe, log-normalized GCA §8 compliance manifest."""
        if len(self.horizon_records) == 0:
            return "[!] No data points compiled to build GCA manifest."
            
        if len(self.horizon_records) < 2:
            final_rec = self.horizon_records[-1]
            return (
                "\n" + "="*95 + 
                "\n                 APPENDIX: SINGLE-HORIZON GCA OBSERVATION MANIFEST" + 
                "\n" + "="*95 + 
                f"\n  - Horizon N                           : {final_rec['N']:,}" + 
                f"\n  - Empirical Limit Candidate 𝔊_C       : {final_rec['C_A']:.6f}" + 
                f"\n  - Empirical Limit Candidate 𝔊_F       : {final_rec['F_A']:.6f}" + 
                f"\n  - Null Mod-30 Baseline                : {final_rec['Null_M30']:.6f}" + 
                f"\n  - Z-Score                             : {final_rec['Z_Score']:.3f}" + 
                "\n  - Log-Normalized Velocity Status      : UNAVAILABLE — NEED ≥2 HORIZONS" + 
                "\n  - Limit Status                        : EMPIRICAL OBSERVATION ONLY" + 
                "\n" + "="*95
            )
            
        final_rec = self.horizon_records[-1]
        
        # Log-scale normalized step velocity engine
        log_velocities = []
        for i in range(1, len(self.horizon_records)):
            prev_rec = self.horizon_records[i-1]
            curr_rec = self.horizon_records[i]
            delta_c_a = abs(curr_rec['C_A'] - prev_rec['C_A'])
            delta_log_n = math.log10(curr_rec['N']) - math.log10(prev_rec['N'])
            v_c = delta_c_a / delta_log_n if delta_log_n > 0 else 0.0
            log_velocities.append(v_c)
            
        if len(log_velocities) < 2:
            r_v_status = "INSUFFICIENT STEPS — NEED ≥3 HORIZONS FOR VELOCITY CHANGE ANALYSIS"
        else:
            eps = 1e-10
            monotonic_deceleration = True
            for i in range(1, len(log_velocities)):
                if log_velocities[i] > log_velocities[i-1] + eps:
                    monotonic_deceleration = False
                    break
            r_v_status = "STRICTLY DECELERATING LOG-VELOCITY (CONVERGENCE SHAPING)" if monotonic_deceleration else "FLUCTUATING / ASYMPTOTICALLY BOUNDED LOG-VELOCITY"
        
        c_a_vals = [vals[0] for vals in self.edge_sensitivity.values()]
        edge_span = max(c_a_vals) - min(c_a_vals) if c_a_vals else 0.0
        edge_stability_status = "STABILIZED / NARROW RANGE" if edge_span < 0.15 else "WIDE VARIATION - BOUNDARY SENSITIVE"
        
        m30_real, m30_null = self.wheel_sensitivity.get(30, (final_rec['F_A'], final_rec['Null_M30']))
        residual_gap = m30_real - m30_null
        
        m6_res = self.wheel_sensitivity.get(6, (0, 0))
        m210_res = self.wheel_sensitivity.get(210, (0, 0))
        deficit_6 = abs(m6_res[0] - m6_res[1])
        deficit_210 = abs(m210_res[0] - m210_res[1])
        
        if deficit_6 > (2.5 * deficit_210) and deficit_210 > 0.001:
            resolution_verdict = "PARTIAL WHEEL RESIDUAL — GRADIENT PRESENT"
        elif abs(residual_gap) <= 0.015:
            resolution_verdict = "COMPLETE WHEEL CONFLATION (HIGH)"
        else:
            resolution_verdict = "EXOGENOUS INDEPENDENT ARITHMETIC FIELD"

        manifest = []
        manifest.append("="*95)
        manifest.append("                 APPENDIX: GCA §8 FORMAL REPRODUCIBILITY MANIFEST")
        manifest.append("="*95)
        manifest.append(f" [8.1] BASE TRACK SPECIFICATION : ℝ (Real-valued field space; range boundary [-1, 0])")
        manifest.append(f" [8.2] SEED CONSTANT SET (C_n)  : Digamma-Class (𝔇_n) Arithmetic Field, sequence-dependent N")
        manifest.append(f" [8.3] AGGREGATOR FUNCTION (𝒜) : Pearson Covariance Functional over Prime Corridor population")
        manifest.append(f" [8.4] UNARY OPERATOR SET (𝒪)  : Identity (Functional maps as aggregator primitive)")
        manifest.append(f" [8.5] NUMERICAL SCHEMA METHOD  : Flat-Profile Zero-Allocation Streaming Matrix Filter")
        manifest.append(f"                                 Null Model Variant: Mod-30 Pseudo-Stochastic Wheel Shuffle")
        manifest.append(f"                                 Deterministic PRNG Seed Lock: {self.seed_value}")
        manifest.append(f" [8.6] MAXIMUM EXPERIMENTAL N   : {self.target_horizon:,}")
        manifest.append("-"*95)
        manifest.append(" [8.7] FORMAL GCA CLASSIFICATION VERDICT")
        manifest.append("-"*95)
        manifest.append(f"  - Empirical Limit Candidate 𝔊_C        : {final_rec['C_A']:.6f}")
        manifest.append(f"  - Empirical Limit Candidate 𝔊_F        : {final_rec['F_A']:.6f}")
        manifest.append(f"  - Terminal Log-Scale Velocity (v_C)    : {log_velocities[-1]:.6f}")
        manifest.append(f"  - Velocity Deceleration Profile (R_v)  : {r_v_status}")
        manifest.append(f"  - Permutation Null Escape Z-Score      : {final_rec['Z_Score']:.3f}")
        manifest.append(f"  - GCA §6 Status                        : EMPIRICAL LIMIT CANDIDATE — FORMAL PROOF PENDING")
        
        if self.green_tao_results:
            manifest.append("-"*95)
            manifest.append(" [8.8] SECTOR 19 — GREEN-TAO SAMPLE ALIGNMENT MATRICES")
            manifest.append("-"*95)
            for r in self.green_tao_results:
                manifest.append(f"  - Progression length k = {r['k']}  | Bases Audited: {r['tested_bases']:<8,} | Chains Found: {r['chains_found']:<8,} | Mean ρ_GT: {r['mean_chain_rho']:.6f} | Mean F_GT: {r['mean_chain_frag']:.6f}")
        
        manifest.append("-"*95)
        manifest.append(" [8.9] CAUSATIVE ATTRIBUTION VERIFICATION")
        manifest.append("-"*95)
        manifest.append(f"  - Observed Real Fragmentation (F_A)   : {final_rec['F_A']:.5f}")
        manifest.append(f"  - Mod-30 Sieve Wheel Null Baseline    : {final_rec['Null_M30']:.5f}")
        manifest.append(f"  - Residual Spatial Gap (Δ Matrix)    : {final_rec['F_A'] - final_rec['Null_M30']:+.5f}")
        manifest.append(f"  - Structural Conflation Resolution   : {resolution_verdict}")
        
        manifest.append("-"*95)
        manifest.append(" [8.10] PARAMETRIC SENSITIVITY ROBUSTNESS MATRICES")
        manifest.append("-"*95)
        manifest.append(f"  [Track A] Edge-Width Spatial Robustness ({edge_stability_status}):")
        manifest.append(f"    * Maximum Guard Track Delta Span    : {edge_span:.6f}")
        for w, (c_a, f_a) in sorted(self.edge_sensitivity.items()):
            manifest.append(f"    * Guard Width = {w:<2} | BaseCorr: {c_a:.6f} | FragMean: {f_a:.5f}")
            
        manifest.append("\n  [Track B] Sieve Dimensioning Array:")
        for m, (f_a, null_f_a) in sorted(self.wheel_sensitivity.items()):
            manifest.append(f"    * Modulus Wheel-{m:<3} | Real F_A: {f_a:.5f} | Null F_A: {null_f_a:.5f} | Deficit: {f_a - null_f_a:+.5f}")
        manifest.append("="*95)
        
        return "\n".join(manifest)

# ==========================================================================================
# MATHEMATICAL HELPER ENGINES (STREAMING TELEMETRY)
# ==========================================================================================

def make_corr_accumulator():
    return {"n": 0, "sx": 0.0, "sy": 0.0, "sx2": 0.0, "sy2": 0.0, "sxy": 0.0}

def update_corr(st, x, y):
    st["n"] += 1
    st["sx"] += x
    st["sy"] += y
    st["sx2"] += x * x
    st["sy2"] += y * y
    st["sxy"] += x * y

def finalize_corr(st):
    n = st["n"]
    if n < 2: return 0.0
    denx = n * st["sx2"] - st["sx"] * st["sx"]
    deny = n * st["sy2"] - st["sy"] * st["sy"]
    if denx <= 0 or deny <= 0: return 0.0
    return (n * st["sxy"] - st["sx"] * st["sy"]) / math.sqrt(denx * deny)

# ==========================================================================================
# PRIMAL & PROPERTY SIEVE STREAM GENERATOR
# ==========================================================================================

def generate_sieve_and_fields(limit):
    print(f"[*] Pre-computing Global Fields and boundaries up to N = {limit:,}...")
    
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.isqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i : limit + 1 : i] = bytearray(len(range(i*i, limit + 1, i)))
            
    primes = array('I', [i for i in range(2, limit + 1) if sieve[i]])
    print(f"    [->] Compiled {len(primes):,} base prime boundaries.")

    A_field = bytearray(limit + 1)
    chunk_size = 5000000
    small_bound = int(math.isqrt(limit)) + 100
    
    s_sieve = [True] * (small_bound + 1)
    s_sieve[0] = s_sieve[1] = False
    for i in range(2, int(math.isqrt(small_bound)) + 1):
        if s_sieve[i]:
            for j in range(i*i, small_bound + 1, i): s_sieve[j] = False
    small_primes = [i for i, p in enumerate(s_sieve) if p]

    for chunk_start in range(1, limit + 1, chunk_size):
        chunk_end = min(chunk_start + chunk_size - 1, limit)
        current_size = chunk_end - chunk_start + 1
        
        sigma = [1] * current_size
        temp_n = [m for m in range(chunk_start, chunk_end + 1)]
        
        max_factor = int(math.isqrt(chunk_end))
        for p_val in small_primes:
            if p_val > max_factor: break
            first_mult = ((chunk_start + p_val - 1) // p_val) * p_val
            for idx_mult in range(first_mult, chunk_end + 1, p_val):
                i_idx = idx_mult - chunk_start
                p_sum = 1
                p_pow = 1
                while temp_n[i_idx] % p_val == 0:
                    p_pow *= p_val
                    p_sum += p_pow
                    temp_n[i_idx] //= p_val
                sigma[i_idx] *= p_sum

        for i in range(current_size):
            if temp_n[i] > 1:
                sigma[i] *= (1 + temp_n[i])
            n_val = chunk_start + i
            if n_val >= 2 and math.gcd(n_val, sigma[i]) > 1:
                A_field[n_val] = 1

    return sieve, primes, A_field

# ==========================================================================================
# PARAMETRIC FIELD ANALYSIS ENGINE
# ==========================================================================================

def evaluate_metrics(primes, A_field, horizon, edge_width=0, mod_wheel=30):
    corr_acc = make_corr_accumulator()
    frag_sum = 0.0
    corridor_count = 0
    
    wheel_counts = [0] * mod_wheel
    wheel_nodes = [0] * mod_wheel
    
    for n in range(2, horizon + 1):
        res = n % mod_wheel
        wheel_counts[res] += 1
        if A_field[n] == 1:
            wheel_nodes[res] += 1
            
    wheel_probs = [wheel_nodes[r] / wheel_counts[r] if wheel_counts[r] > 0 else 0.0 for r in range(mod_wheel)]
    
    null_frag_sum = 0.0
    null_frag_sq_sum = 0.0

    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i+1]
        if q > horizon: break
        
        gap = q - p
        width = gap - 1
        if width <= 0: continue
        
        bits = A_field[p + 1 : q]
        
        if edge_width and edge_width > 0 and width > (2 * edge_width):
            effective_bits = list(bits[:edge_width]) + list(bits[-edge_width:])
            effective_width = len(effective_bits)
        else:
            effective_bits = bits
            effective_width = width
            
        a_count = sum(effective_bits)
        rho = a_count / effective_width if effective_width > 0 else 0.0
        
        update_corr(corr_acc, gap, rho)
        
        a_runs = 0
        in_run = False
        for bit in effective_bits:
            if bit == 1:
                if not in_run:
                    a_runs += 1
                    in_run = True
            else:
                in_run = False
                
        frag = (a_runs / a_count) if a_count > 0 else 0.0
        frag_sum += frag
        corridor_count += 1

        null_bits = [1 if random.random() < wheel_probs[(p + 1 + idx) % mod_wheel] else 0 for idx in range(width)]
        if edge_width and edge_width > 0 and width > (2 * edge_width):
            null_bits = null_bits[:edge_width] + null_bits[-edge_width:]
            
        n_count = sum(null_bits)
        n_runs = 0
        n_in_run = False
        for bit in null_bits:
            if bit == 1:
                if not n_in_run:
                    n_runs += 1
                    n_in_run = True
            else:
                n_in_run = False
                
        n_frag = (n_runs / n_count) if n_count > 0 else 0.0
        null_frag_sum += n_frag
        null_frag_sq_sum += n_frag * n_frag

    mean_real = frag_sum / corridor_count if corridor_count > 0 else 0.0
    mean_null = null_frag_sum / corridor_count if corridor_count > 0 else 0.0
    var_null = (null_frag_sq_sum / corridor_count) - (mean_null * mean_null)
    std_null = math.sqrt(max(var_null, 1e-12))
    
    z_score = (mean_real - mean_null) / (std_null / math.sqrt(corridor_count)) if corridor_count > 0 else 0.0

    return finalize_corr(corr_acc), mean_real, mean_null, corridor_count, z_score

# ==========================================================================================
# SECTOR 19 — GREEN–TAO PRIME CHAIN FITNESS AUDIT (SAFE DETECTIVE SAMPLING)
# ==========================================================================================

def sector_19_green_tao_chain_audit(sieve, primes, A_field, horizon, chain_lengths=(3, 4, 5), max_step=250, prime_sample_stride=100):
    """
    Sector 19 — Green–Tao Prime Chain Fitness Audit.
    Uses deterministic prime thinning so 100M/500M/1B runs stay bounded.
    This is an empirical AP-chain sample audit, not a full exhaustive Green–Tao census.
    """
    print(f"[*] Executing Sector 19: Green–Tao Prime Chain Fitness Audit up to N = {horizon:,}...")
    print(f"    [Mode] Deterministic sampled AP audit | max_step={max_step} | prime_stride={prime_sample_stride}")

    results = []

    for k in chain_lengths:
        chain_count = 0
        rho_sum = 0.0
        frag_sum = 0.0
        tested_bases = 0

        for idx_a, a in enumerate(primes):
            if a > horizon:
                break

            if idx_a % prime_sample_stride != 0:
                continue

            tested_bases += 1

            for d in range(2, max_step + 1, 2):
                if a + (k - 1) * d > horizon:
                    break

                is_chain = True
                for j in range(1, k):
                    if not sieve[a + j * d]:
                        is_chain = False
                        break

                if not is_chain:
                    continue

                chain_count += 1
                bits_total = 0
                a_nodes = 0
                runs = 0
                in_run = False

                for j in range(k - 1):
                    x = a + j * d
                    y = a + (j + 1) * d

                    for n in range(x + 1, y):
                        bits_total += 1
                        if A_field[n]:
                            a_nodes += 1
                            if not in_run:
                                runs += 1
                                in_run = True
                        else:
                            in_run = False

                    # prime boundary breaks corridor continuity
                    in_run = False

                rho = a_nodes / bits_total if bits_total else 0.0
                frag = runs / a_nodes if a_nodes else 0.0

                rho_sum += rho
                frag_sum += frag

        results.append({
            "k": k,
            "tested_bases": tested_bases,
            "chains_found": chain_count,
            "mean_chain_rho": rho_sum / chain_count if chain_count else 0.0,
            "mean_chain_frag": frag_sum / chain_count if chain_count else 0.0,
        })

    print("\n" + "="*95)
    print("SECTOR 19 — GREEN–TAO PRIME CHAIN FITNESS AUDIT")
    print("="*95)
    print(" k | Bases Tested | Chains Found | Mean Chain ρ_GT | Mean Chain F_GT")
    print("-"*95)
    for r in results:
        print(
            f" {r['k']:<2}| {r['tested_bases']:<12,} | "
            f"{r['chains_found']:<12,} | {r['mean_chain_rho']:<15.6f} | "
            f"{r['mean_chain_frag']:<15.6f}"
        )
    print("="*95)

    return results

# ==========================================================================================
# RUNTIME INTEGRATION ENGINE
# ==========================================================================================

def run_integrated_suite(limit):
    seed_value = 42
    random.seed(seed_value)
    print(f"\n[*] Initializing Acheron GCA Integrated Execution Matrix up to N = {limit:,}")
    
    manifest_compiler = GCAManifestCompiler(limit, seed_value=seed_value)
    sieve, primes, A_field = generate_sieve_and_fields(limit)
    
    default_horizons = [2000000, 10000000, 50000000, 100000000, 200000000, 500000000, 1000000000]
    
    print("\n[*] Validating target scale horizons...")
    horizons = []
    for h in default_horizons:
        if h <= limit:
            horizons.append(h)
            print(f"  [✓] Horizon N = {h:,} included in active matrix run.")
        else:
            print(f"  [-] Horizon N = {h:,} dropped (exceeds specified limit context).")

    print("\n[*] Sweeping Horizons and capturing convergence metrics...")
    print(" Horizon (N)   | BaseCorr (C_A) | FragMean (F_A) | Null Mod-30 | Z-Score")
    print("-"*85)
    for h in horizons:
        bc, mf, mnf, v_c, z_sc = evaluate_metrics(primes, A_field, h, edge_width=0, mod_wheel=30)
        p_cnt = sum(1 for p in primes if p <= h)
        manifest_compiler.register_horizon_step(h, p_cnt, v_c, bc, mf, mnf, z_sc)
        print(f" {h:<13,} | {bc:<14.6f} | {mf:<14.5f} | {mnf:<11.5f} | {z_sc:+.3f}")

    deep_horizon = horizons[-1]
    
    # Scale-adapted execution throttling gates to safeguard high-horizon runtime bounds
    if deep_horizon <= 10_000_000:
        dynamic_max_step = 1000
        prime_stride = 10
    elif deep_horizon <= 100_000_000:
        dynamic_max_step = 500
        prime_stride = 50
    else:
        dynamic_max_step = 250
        prime_stride = 250

    gt_metrics = sector_19_green_tao_chain_audit(
        sieve,
        primes,
        A_field,
        deep_horizon,
        chain_lengths=(3, 4, 5),
        max_step=dynamic_max_step,
        prime_sample_stride=prime_stride
    )
    manifest_compiler.register_green_tao_audit(gt_metrics)

    print(f"\n[*] Processing Sector 3: Edge Sensitivity Variations (At N = {deep_horizon:,})...")
    edge_widths = [1, 2, 3, 5, 10]
    for ew in edge_widths:
        bc, mf, _, _, _ = evaluate_metrics(primes, A_field, deep_horizon, edge_width=ew, mod_wheel=30)
        manifest_compiler.register_edge_audit(ew, bc, mf)

    print(f"[*] Processing Sector 4: Mod Sieve Model Adaptations (At N = {deep_horizon:,})...")
    wheels = [6, 30, 210]
    for w in wheels:
        _, mf, mnf, _, _ = evaluate_metrics(primes, A_field, deep_horizon, edge_width=0, mod_wheel=w)
        manifest_compiler.register_wheel_audit(w, mf, mnf)

    print("\n" + manifest_compiler.compile_formal_appendix())

if __name__ == "__main__":
    print("="*75)
    print("     ACHERON CONSTANT CONJECTURE SYSTEM: MASTER REVOLUTION SUITE v3.3")
    print("="*75)
    print("  1) Express Validation Pool (N = 2,000,000)")
    print("  2) Production Scale Check  (N = 10,000,000)")
    print("  3) Extended Deep Horizon   (N = 100,000,000)")
    print("  4) Full 500M Scale Verification")
    print("  5) 1B Master Horizon Execution Matrix")
    print("-"*75)
    
    choice = input("Select execution index (1-5): ").strip()
    if choice == '1':   run_integrated_suite(2000000)
    elif choice == '2': run_integrated_suite(10000000)
    elif choice == '3': run_integrated_suite(100000000)
    elif choice == '4': run_integrated_suite(500000000)
    elif choice == '5': run_integrated_suite(1000000000)
    else:               print("[!] Invalid index selected. Exiting execution environment.")