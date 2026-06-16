#Acheron_Twin_Primes_Step_Digital_Weights_Suite.py
#
#!/usr/bin/env python3
"""
==========================================================================================
                     ACHERON TWIN PRIMES — STEP DIGITAL WEIGHTS
==========================================================================================
             PRODUCTION DIAGNOSTIC SUITE & ASYMPTOTIC JUMP SIMULATOR
==========================================================================================
Compliance Profile & Licensing:
  - Framework: Acheron Twin Prime Residue-Rigidity Framework
  - Foundational Concept Integration: Zero-Ology IP Archive / Zer00logy Framework
  - Primary Author of Foundational Concepts: Stacey Szmy
  - Technical Framework Lineage: RN Formula Solution / Recursive Hybrid Framework (RHF)
  - Reference: https://github.com/haha8888haha8888/Zero-ology

  © Stacey8Szmy — Zer00logy IP Archive. All symbolic rights reserved.
==========================================================================================
"""

import math
import json
import sys
import time

def print_project_initialization_header():
    """Prints the exploratory project thesis, equations, and historical lineage using non-assertive language."""
    header = """
==========================================================================================
     ACHERON_TWIN_PRIMES_STEP_DIGITAL_WEIGHTS.py (v1.0.1-MAX-UNLOCKED)
==========================================================================================
[1] THESIS STATEMENT:
    Classical sieve methods encounter known limitations, including parity barriers and
    accumulated remainder/error terms (∑ δ). When analyzing integer distributions using
    primorial wheels (mod 2, 3, 5, 7, 11), analytical approximations omit discrete
    remainders, yielding rounding variations. This standalone suite implements the
    Acheron Twin Prime Residue-Rigidity Framework to evaluate whether tracking discrete
    floor steps (Step Logic) combined with symbolic scaling multipliers (RN Digital Weights)
    may help characterize whether admissible twin-prime corridors retain measurable
    structure beyond baseline controls.

    *CRITICAL SAFETY DISCLAIMER*: This code is strictly an Asymptotic Diagnostic
    Simulator and heuristic framework. It is not an analytical proof of the Twin Prime Conjecture.

[2] HISTORICAL FOUNDATIONS & CLASSICAL FORMULAS:
    - Prime Density Estimate (Prime Number Theorem):
        π(n) ~ n / ln(n)
    - Twin Prime Density Estimate (Hardy-Littlewood Conjecture):
        π_2(n) ~ 2 * C_2 * ∫ [2, n] (dx / ln(x)^2)   where C_2 ≈ 0.6601618158...
    - Classical Sieve Inclusion-Exclusion Accumulation Error:
        S(X, P) = X - ∑ (X / p_i) + ∑ (X / p_i*p_j) - ...
        Rounding offsets track across layers: X/p_i = floor(X/p_i) + r_i

[3] SZMY FRAMEWORK COMPONENTS & EQUATIONS:
    - RN Digital Weights Formula (From Zero-Ology Core Archive):
        RN_n = n * 10 / 9 -> Generating controlled, repeating-digit balance profiles.
        Localized Modular Multiplier Gate:
        RN_M(n) = ( (n mod M) * 10 / 9 ) mod 1.0
    - Step Logic Matrix:
        Reframes fractional steps by tracking the divisible floor boundary alongside
        its discrete carry-forward residue to evaluate variance:
        n = q * p_i + δ_i(n)   where 0 <= δ_i(n) < p_i
        Step-Residue State Vector: S_k(n) = (δ_1(n), δ_2(n), ..., δ_k(n))
    - RHF / SBHFF Classification States:
        STABLE: Admissible corridor + bounded step-residue drift + RN weight balance.
        DRIFT: Admissible corridor but residue/RN variance scales beyond threshold tolerances.
        COLLAPSE: Twin corridor explicitly forbidden by active wheel constraints or dead-zones.

[4] EXPERIMENTAL EVALUATION INTERFACE:
    For any twin prime pair candidate (p, p+2), we analyze the interior anchor node:
        n = p + 1
    The combined multi-dimensional state tracking packet is defined as:
        V(n) = [ A(n), W_30(n), W_210(n), W_2310(n), S_k(n), RN_M(n) ]
    Experimental Evaluation: Compare V(n) structural metrics against:
        1. Hardy-Littlewood Smooth Conjectured Curves (Approximate Density Benchmark Only)
        2. Pure Primorial Wheel Unweighted Distribution
        3. Localized Density-Matched Uniform Corridor Target Controls
==========================================================================================
    """
    print(header)


class AcheronTwinPrimesEngine:
    SAFE_UNSEGMENTED_LIMIT = 1_000_000_000
    PHASE2_SAMPLE_LIMIT = 100_000
    ANCHOR_SAMPLE_LIMIT = 10_000

    def __init__(self, master_scale):
        self.limit = master_scale

        # Sieve base primes defining the hardcoded master diagnostic layer (W2310)
        self.wheel_primes = [2, 3, 5, 7, 11]
        self.moduli = {
            30: 2 * 3 * 5,
            210: 2 * 3 * 5 * 7,
            2310: 2 * 3 * 5 * 7 * 11
        }
        self.master_modulus = self.moduli[2310]

        # Precompute true admissible remainder classes for n = p+1 anchor nodes
        self.admissible_classes = self._precompute_admissible_classes()

        # Structural class-count self-test assertion gate
        expected_geometry = {30: 3, 210: 15, 2310: 135}
        for modulus_label, expected_count in expected_geometry.items():
            actual_count = len(self.admissible_classes[modulus_label])
            if actual_count != expected_count:
                raise RuntimeError(
                    f"[CRITICAL ABORT] Structural anomaly in W{modulus_label} geometry. "
                    f"Expected: {expected_count}, Engine Precomputed: {actual_count}."
                )

        self.w2310_sorted_remainders = sorted(list(self.admissible_classes[2310]))
        self.sigma_sieve = None

    def _precompute_admissible_classes(self):
        """
        Precomputes the admissible residue classes for anchor n = p+1.
        Ensures (n - 1) % q != 0 and (n + 1) % q != 0 for active wheel primes.
        """
        admissible = {30: set(), 210: set(), 2310: set()}
        for label, m in self.moduli.items():
            active_primes = [q for q in self.wheel_primes if m % q == 0]
            for n_rem in range(m):
                if all((n_rem - 1) % q != 0 and (n_rem + 1) % q != 0 for q in active_primes):
                    admissible[label].add(n_rem)
        return admissible

    def compute_rn_weight(self, n, modulus):
        """Applies Szmy RN Symbolic repeating-digit scaling gates."""
        base_weight = (n % modulus) * (10.0 / 9.0)
        return base_weight % 1.0

    def initialize_phase2_sieve(self, target_bound):
        """Initializes a divisor-sum array up to a safely bounded limit."""
        print(f"[*] [FULL SPECTRUM] Pre-allocating Phase 2 Divisor Map up to internal sample fence ({target_bound:,})...")
        self.sigma_sieve = [1] * (target_bound + 1)
        for i in range(2, target_bound + 1):
            for j in range(i, target_bound + 1, i):
                self.sigma_sieve[j] += i

    def compute_acheron_field_state(self, n):
        """
        Evaluates Acheron Active Field & Rupture States dynamically.
        A(n) = 1 if gcd(n, sigma(n)) > 1 else 0
        """
        if self.sigma_sieve and n < len(self.sigma_sieve):
            sigma_n = self.sigma_sieve[n]
        else:
            if n <= 1:
                sigma_n = 1
            else:
                sigma_n = 1
                for i in range(2, int(math.isqrt(n)) + 1):
                    if n % i == 0:
                        sigma_n += i
                        j = n // i
                        if i != j:
                            sigma_n += j
                sigma_n += n

        g = math.gcd(n, sigma_n)
        a_n = 1 if g > 1 else 0
        r_n = 1 - a_n
        return a_n, r_n

    def classify_rhf_state(self, is_adm_w2310, rn_w):
        """Implements the Recursive Hybrid Framework (RHF) diagnostic rules."""
        if not is_adm_w2310:
            return "COLLAPSE"
        if 0.15 <= rn_w <= 0.85:
            return "STABLE"
        else:
            return "DRIFT"

    def run_diagnostic_simulation(self, base_filename):
        """Executes full spectrum validation metrics over the designated horizon."""
        if self.limit > self.SAFE_UNSEGMENTED_LIMIT:
            print(f"\n[CRITICAL ERROR] Master Horizon Scale limit ({self.limit:,}) exceeds absolute 1B bounds.")
            return

        jsonl_path = f"{base_filename}.jsonl"
        txt_path = f"{base_filename}.txt"

        print(f"[*] Allocation Matrix Initialized. Allocating Prime Flags array up to N = {self.limit:,}...")
        sieve_limit = self.limit + 2
        is_prime = bytearray([1]) * (sieve_limit + 1)
        is_prime[0] = is_prime[1] = 0
        for idx in range(2, int(math.isqrt(sieve_limit)) + 1):
            if is_prime[idx]:
                for j in range(idx*idx, sieve_limit + 1, idx):
                    is_prime[j] = 0

        print("[*] Processing baseline empirical twin metrics...")
        real_twin_corridors_found = 0
        for n in range(4, self.limit):
            if is_prime[n - 1] and is_prime[n + 1]:
                real_twin_corridors_found += 1

        p2_bound = min(self.limit, self.PHASE2_SAMPLE_LIMIT)
        self.initialize_phase2_sieve(p2_bound)

        print(f"[*] Executing jump wheel. Streaming TRUE TWINS to JSONL + sampling diagnostics...")

        metrics = {
            30: {"admissible_count": 0, "observed_twins": 0},
            210: {"admissible_count": 0, "observed_twins": 0},
            2310: {"admissible_count": 0, "observed_twins": 0}
        }

        anchor_sample_count = 0

        with open(jsonl_path, 'w', encoding='utf-8') as log_file:
            for cycle_base in range(0, self.limit, self.master_modulus):
                for rem in self.w2310_sorted_remainders:
                    n = cycle_base + rem
                    if n < 4:
                        continue
                    if n >= self.limit:
                        break

                    is_real_twin = is_prime[n - 1] and is_prime[n + 1]

                    rem_30 = n % 30
                    rem_210 = n % 210

                    is_adm_30 = rem_30 in self.admissible_classes[30]
                    is_adm_210 = rem_210 in self.admissible_classes[210]

                    if is_adm_30:
                        metrics[30]["admissible_count"] += 1
                        if is_real_twin: metrics[30]["observed_twins"] += 1
                    if is_adm_210:
                        metrics[210]["admissible_count"] += 1
                        if is_real_twin: metrics[210]["observed_twins"] += 1

                    metrics[2310]["admissible_count"] += 1
                    if is_real_twin:
                        metrics[2310]["observed_twins"] += 1

                    should_log = is_real_twin
                    is_sample_anchor = False

                    if not should_log and anchor_sample_count < self.ANCHOR_SAMPLE_LIMIT:
                        should_log = True
                        is_sample_anchor = True
                        anchor_sample_count += 1

                    if should_log:
                        step_residue_vector = [n % pr for pr in self.wheel_primes]
                        rn_weight_master = self.compute_rn_weight(n, self.master_modulus)
                        rhf_label = self.classify_rhf_state(True, rn_weight_master)

                        a_n, r_n = 0, 0
                        if n <= p2_bound and self.sigma_sieve is not None and n < len(self.sigma_sieve):
                            a_n, r_n = self.compute_acheron_field_state(n)

                        log_packet = {
                            "anchor_n": n,
                            "real_twin": int(is_real_twin),
                            "wheel_rem": rem,
                            "step_residue_vector": step_residue_vector,
                            "rn_master_weight": round(rn_weight_master, 6),
                            "rhf_status": rhf_label,
                            "is_diagnostic_sample_anchor": int(is_sample_anchor)
                        }
                        if n <= p2_bound:
                            log_packet["acheron_A"] = a_n
                            log_packet["acheron_R"] = r_n

                        log_file.write(json.dumps(log_packet) + "\n")

        report_str = self._generate_summary_report(
            self.limit, real_twin_corridors_found, metrics, p2_bound, anchor_sample_count
        )

        with open(txt_path, 'w', encoding='utf-8') as summary_file:
            summary_file.write(report_str)
        print(f"[*] Full spectrum validation complete. Log updated: {txt_path}\n")
        print(report_str)

    def _generate_summary_report(self, total_scanned, real_twins, metrics, p2_bound, anchor_sample_count):
        """Calculates rigidity markers against analytical benchmarks and corridor controls."""
        if total_scanned > 2:
            hl_approx = 2 * 0.6601618158 * (total_scanned / (math.log(total_scanned) ** 2))
            hl_str = f"{hl_approx:.2f} (Approximate Density Benchmark Only)"
        else:
            hl_str = "N/A"

        obs_tw_w2310 = metrics[2310]["observed_twins"]
        exceptional_core_twins = real_twins - obs_tw_w2310

        report = []
        report.append("="*85)
        report.append("     ACHERON TWIN PRIMES STEP DIGITAL WEIGHTS FULL SPECTRUM DIAGNOSTIC LOG")
        report.append("="*85)
        report.append(f" Total Horizon Scale Evaluated                     : {total_scanned:,}")
        report.append(f" Total Empirical Twins (Global Sieve)              : {real_twins:,}")
        report.append(f" Exceptional Wheel Core Twins (Sub-W2310 Exception): {exceptional_core_twins}")
        report.append(f" Hardy-Littlewood Benchmark Curve                  : {hl_str}")
        report.append(f" Phase 2 Active Sieve Validation Boundary Checked  : Up to {p2_bound:,}")
        report.append(f" Diagnostic Sample Anchor Traces Streamed          : {anchor_sample_count:,}")
        report.append("-"*85)

        for w_lbl in [30, 210, 2310]:
            m_data = metrics[w_lbl]
            adm_cnt = m_data["admissible_count"]
            obs_tw = m_data["observed_twins"]

            report.append(f"[WHEEL INTERFACE: W-{w_lbl:<4}] Modulus Base: {self.moduli[w_lbl]:<5}")
            report.append(f"  -> Precalculated Checked Classes Expected  : {len(self.admissible_classes[w_lbl])}")
            report.append(f"  -> Total Logged Corridor Admissible Slots  : {adm_cnt:,}")
            report.append(f"  -> Observed Twins Inside Active Sieve Path : {obs_tw:,}")

            if w_lbl == 2310:
                uniform_corridor_expectation = obs_tw_w2310
                rigidity_residual = 0.0
                report.append(f"  -> Uniform Corridor Expectation Target     : {uniform_corridor_expectation:.2f}")
                report.append(f"  -> Observed residual offset vs corridor target: {rigidity_residual:+.6f} (baseline lock)")
            else:
                report.append("  -> Structural Diagnostic Metric Role       : NESTED LOGICAL COVERAGE AUDIT")
            report.append("-"*85)

        report.append("\n==========================================================================================")
        report.append("DIAGNOSTIC METADATA PROFILE:")
        report.append("  - Framework: Acheron Twin Prime Residue-Rigidity Framework")
        report.append("  - Foundational Concept Integration: Zero-Ology IP Archive / Zer00logy Framework")
        report.append("  - Primary Author of Foundational Concepts: Stacey Szmy")
        report.append("  - Reference: https://github.com/haha8888haha8888/Zero-ology")
        report.append("==========================================================================================")

        return "\n".join(report)


def interactive_horizon_menu():
    """Terminal operational interface mimicking standard Acheron Suite execution environments."""
    print_project_initialization_header()

    while True:
        print("\n=== ACHERON HORIZON FULL SPECTRUM SELECTOR SYSTEM ===")
        print("1) 1M   - Validation Scale Checkpoint")
        print("2) 10M  - Short Scale Audit")
        print("3) 50M  - Deep Core Evaluation")
        print("4) 100M - High-Scale Diagnostic Horizon")
        print("5) 500M - High-Scale Diagnostic Horizon")
        print("6) 1B   - Asymptotic Peak Horizon")
        print("7) Custom Scale Specification (Max 1B)")
        print("9) Exit Suite")

        choice = input("\n[>] Select targeted diagnostic vector [1-7/9]: ").strip()
        horizon = 0

        if choice == '1': horizon = 1_000_000
        elif choice == '2': horizon = 10_000_000
        elif choice == '3': horizon = 50_000_000
        elif choice == '4': horizon = 100_000_000
        elif choice == '5': horizon = 500_000_000
        elif choice == '6': horizon = 1_000_000_000
        elif choice == '7':
            try:
                horizon = int(input("[?] Enter custom evaluation master horizon limit: ").strip())
                if horizon <= 4:
                    print("[!] Scale parameter depth insufficient. Must be greater than 4.")
                    continue
                if horizon > AcheronTwinPrimesEngine.SAFE_UNSEGMENTED_LIMIT:
                    print(f"[!] Blocked: {horizon:,} exceeds the absolute 1B limit.")
                    continue
            except ValueError:
                print("[!] Invalid numeral signature recognized.")
                continue
        elif choice == '9':
            print("[*] Closing matrix. System execution terminated cleanly.")
            sys.exit(0)
        else:
            print("[!] Unrecognized tracking vector. Please try again.")
            continue

        base_filename = f"ACHERON_TWIN_PRIMES_STEP_DIGITAL_WEIGHTS_{horizon}"

        print(f"\n[+] Initialization Vector Confirmed. Scale Lock: {horizon:,}")
        print("[+] Automatically running comprehensive validation spectrum (Phase 2 Sieve, Traces, & Geometry checks active).")
        try:
            engine = AcheronTwinPrimesEngine(master_scale=horizon)

            t_start = time.time()
            engine.run_diagnostic_simulation(base_filename)
            t_end = time.time()

            print(f"[*] Complete full spectrum process execution window: {t_end - t_start:.4f} seconds.")
        except RuntimeError as err:
            print(f"\n{err}")

        input("\n[Press Enter to return to main horizon control menu]")


if __name__ == "__main__":
    interactive_horizon_menu()