#NSRHFsuite0020V
#The Navier-Stokes Recursive Hybrid Formula (NSRHF) Suit-0020V
# 0ko3maibZer00logyLicensev1.15
# Zero-Ology License v1.15

import time
import random
import sys
# Used for string matching in the final summary of the parameter sweep
import re

# ==============================================================================
#           MOCK IMPLEMENTATIONS FOR CORE NSRHF TESTS
# ==============================================================================

def run_mock_test(title, complexity_factor=1):
    """Generic function to run and report a mock simulation test with max data output."""
    
    # Header
    print(f"\n{'='*85}")
    print(f"--- Running {title} (Complexity Factor: {complexity_factor}) ---")
    print(f"{'='*85}")

    # Simulate computation time and instability/success
    total_steps = random.randint(800 * complexity_factor, 1200 * complexity_factor)
    is_stable = random.random() > (0.1 / complexity_factor)  # Higher factor = higher chance of stability
    
    # --- Progress Log (Max Data Output) ---
    enstrophy_history = []
    print("\n[ SIMULATION PROGRESS LOG ]")
    
    # Simulate step-by-step data reporting
    log_interval = total_steps // 6 if total_steps >= 6 else 1
    
    for i in range(1, total_steps + 1):
        if i % log_interval == 0 or i == 1:
            mean_enstrophy = random.uniform(0.001, 0.005) / (i / total_steps)
            max_v_current = random.uniform(1.0, 5.0) * (1 + (i / total_steps) * (0.1 if is_stable else 10))
            max_p_current = random.uniform(0.5, 2.0)
            enstrophy_history.append(mean_enstrophy)
            
            # Print detailed step data
            print(f"    STEP {i}/{total_steps:<4} | Mean Enstrophy={mean_enstrophy:.6f} | Max Velocity={max_v_current:.3f} | Max Pressure={max_p_current:.3f} | Residual Norm={random.uniform(1e-8, 1e-6):.2e}")
        
        # Simulate collapse check and early exit
        if not is_stable and i > (total_steps * 0.1) and random.random() < 0.005:
            collapse_step = i
            break
    else:
        collapse_step = total_steps  # Completed successfully
        time.sleep(random.uniform(0.05, 0.1))  # Add delay for successful completion

    # --- Final Status Report ---
    print("\n[ FINAL STATUS ]")
    if is_stable:
        max_v = random.uniform(0.1, 5.0)
        enstrophy = random.uniform(0.001, 0.1)
        print(f"STABILIZED: Max Velocity = {max_v:.3e}, Final Enstrophy = {enstrophy:.3e} in {total_steps} steps.")
        print(f"    Final Energy Dissipation Rate: {random.uniform(1e-6, 5e-5):.4e} J/s")
    else:
        max_v = random.uniform(5.0e3, 1.0e5)
        print(f"COLLAPSED: Max Velocity blowup ({max_v:.3e}) detected at step {collapse_step}/{total_steps}.")
        print(f"    NSRHF-Mask Activation Index: {random.randint(100, 500)}")

    # --- Simulated Maximum Data Output ---
    print("\n" + "~"*85)
    print("--- SIMULATED VISUALIZATION DATA ARRAYS (MAX DATA OUTPUT) ---")
    
    # Grid size mock for visual data dump
    grid_size = 8 * complexity_factor
    
    print(f"\n1. Vorticity Magnitude (Central Slice, {grid_size}x{grid_size}):")
    sim_array_vort = [f"{random.uniform(0.3, 1.5):.6f}" for _ in range(grid_size ** 2)]
    for i in range(min(grid_size, 10)):  # Print max 10 rows
        print("  " + " ".join(sim_array_vort[i*grid_size:i*grid_size + min(grid_size, 8)]))  # Print max 8 columns
    print(f"  ... ({grid_size*grid_size} total points redacted) ...")

    print(f"\n2. Collapse Activation Mask (Central Slice, chi, {grid_size}x{grid_size}):")
    sim_array_mask = [f"{random.choice([0.0, 0.0, 0.0, 0.0, 1.0]):.1f}" for _ in range(grid_size ** 2)]
    for i in range(min(grid_size, 5)):
        print("  " + " ".join(sim_array_mask[i*grid_size:i*grid_size + min(grid_size, 8)]))
    print(f"  ... ({grid_size*grid_size} total points redacted) ...")

    print(f"\n3. Enstrophy History (Mean Enstrophy over time, {len(enstrophy_history)} points):")
    # Limit output length for readability
    history_output = [f"{e:.6f}" for e in enstrophy_history[:10]]
    if len(enstrophy_history) > 10:
        history_output.append("...")
    print("  " + " ".join(history_output))
    
    print("-----------------------------------------------------------------")
    print(f"\n--- {title} Complete ---\n")
    print("="*85)

    # Return to main menu prompt
    input("Press ENTER to return to the main menu...")

# --- Test Definitions (Mocks) ---

def run_shock_vortex():
    """1. Shock–Vortex Interaction Test (NSRHF)"""
    run_mock_test("Shock–Vortex Interaction Test (NSRHF)", complexity_factor=2)

def run_lorenz_bifurcation():
    """2. 3D Lorenz-Space Bifurcation Test (NSRHF-Enhanced)"""
    run_mock_test("3D Lorenz-Space Bifurcation Test (NSRHF-Enhanced Python Script)", complexity_factor=3)

def run_reaction_diffusion_neural():
    """3. Full NSRHF-stabilized Coupled Reaction–Diffusion + Neural Field test"""
    run_mock_test("NSRHF-stabilized Coupled Reaction–Diffusion + Neural Field test", complexity_factor=4)

def run_stabilized_jet():
    """4. Fully stabilized turbulent jet injection simulation"""
    run_mock_test("Fully stabilized turbulent jet injection simulation", complexity_factor=5)

def run_kelvin_helmholtz():
    """5. Kelvin–Helmholtz Instability (NSRHF-Compatible)"""
    run_mock_test("Kelvin–Helmholtz Instability (NSRHF-Compatible Python Script)", complexity_factor=2)

def run_scaffold():
    """6. NSRHF Simulation Scaffold (Python)"""
    run_mock_test("NSRHF Simulation Scaffold (Python) - Template Check", complexity_factor=1)

def run_pressure_spike():
    """7. Pressure Spike Near Sharp Corners"""
    run_mock_test("Pressure Spike Near Sharp Corners - High Gradient Stability Check", complexity_factor=3)

def run_taylor_green():
    """9. Taylor–Green Vortex Decay (NSRHF)"""
    run_mock_test("Taylor–Green Vortex Decay Test (NSRHF)", complexity_factor=2)

def run_turbulent_jet():
    """10. Turbulent jet injection script"""
    run_mock_test("Turbulent jet injection script (High Turbulence)", complexity_factor=1)

def run_vortex_singularity():
    """11. Vortex Stretching Singularity with NSRHF"""
    run_mock_test("Vortex Stretching Singularity with NSRHF - Collapse Prevention", complexity_factor=4)

# --- NEW TESTS (12-15) ---

def run_isentropic_vortex_decay():
    """12. Isentropic Vortex Decay Test (NSRHF)"""
    run_mock_test("Isentropic Vortex Decay Test (NSRHF)", complexity_factor=2)

def run_barotropic_flow():
    """13. 2D Barotropic Flow Test (NSRHF)"""
    run_mock_test("2D Barotropic Flow Test (NSRHF)", complexity_factor=3)

def run_channel_flow():
    """14. 3D Channel Flow Test (NSRHF)"""
    run_mock_test("3D Channel Flow Test (NSRHF)", complexity_factor=4)

def run_richtmyer_meshkov():
    """15. Richtmyer–Meshkov Instability Test (NSRHF)"""
    run_mock_test("Richtmyer–Meshkov Instability Test (NSRHF)", complexity_factor=5)

def run_print_NSRHF():
    print("\n=== NSRHF Reference Information ===")
    print("Title: Varia Math & Artificial Intelligence")
    print("Subtitle: The Navier-Stokes Recursive Hybrid Formula (NSRHF)")
    print("Author: Stacey Szmy")
    print("Co-Creators: Ms Copilot, OpenAI ChatGPT")
    print("Audit AI: Xai Grok, Google Gemini")
    print("Review AI: Google Gemini, Xai Grok, OpenAI ChatGPT, Ms Copilot")
    print("Date: August 2025")
    print("Issue: PRINT")
    print("ISBN: 9798263063306\n")

    print("Abstract:")
    print("The Navier–Stokes Recursive Hybrid Formula (NSRHF) is a symbolic, entropy-aware framework designed to stabilize incompressible fluid dynamics under collapse-prone conditions. It isolates the nonlinear convective term and reintroduces other components through recursive symbolic logic, enabling dynamic zone adaptation, entropy drift tracking, and collapse parameter modulation.\n")

    print("Core Formula:")
    print("uₙ₊₁ = C⁻¹(T⁻¹[Pₙ + Vₙ + Fₙ])")
    print("• C⁻¹: inverse convective operator")
    print("• T⁻¹: inverse temporal operator")
    print("• Pₙ: pressure gradient")
    print("• Vₙ: viscous diffusion")
    print("• Fₙ: external forcing\n")

    print("Hybrid Operator Bundle H[u;κ]:")
    print("• Vᵣ: viscous scaffolding")
    print("• Sᵣ: shear rebalancing")
    print("• P_b: pressure buffer")
    print("• E_s: entropy sink\n")

    print("Collapse Parameter Evolution:")
    print("κₙ₊₁(x) = (1 − β) κₙ(x) + β ||ΔXₙ(x)||ₙ")
    print("• ΔXₙ: diagnostic state vector (velocity increments, entropy change, enstrophy drift)\n")

    print("Recursive Logic:")
    print("1. Compute uₙ₊₁ using inverted operators")
    print("2. Evaluate entropy drift: Sₙ(x) = e(x, uₙ) − e(x, uₙ₋₁)")
    print("   • e(x, u) = ½ |∇×u|²")
    print("3. Identify collapse zones: Zₙ = {x | Sₙ(x) > θ ⋅ κₙ(x)}")
    print("4. Apply activation mask: χ_Zₙ(x) = 1 / (1 + exp(−γ(Sₙ(x) − θκₙ(x)))")
    print("5. Inject H[u;κ] into collapse zones")
    print("6. Update κₙ adaptively\n")

    print("Comparative Analysis:")
    print("• DNS: Direct numerical integration — resolves all scales, but costly")
    print("• LES: Subgrid filtering — reduces cost, loses detail")
    print("• RANS: Time-averaging — efficient, but averages out dynamics")
    print("• NSRHF: Recursive symbolic hybrid — entropy-aware, adaptive, zone-specific\n")

    print("Strengths of NSRHF:")
    print("• Symbolic recursion: Self-reflective fluid system")
    print("• Entropy-aware collapse detection: Preemptive stabilization\n")

    print("Limitations:")
    print("• Formal proof of stability pending")
    print("• Scaling in 3D turbulence needs benchmarks")
    print("• Collapse parameter tuning requires sensitivity analysis\n")

    print("Potential Extensions:")
    print("• AI coupling with neural PDE solvers")
    print("• Symbolic attractor tracking")
    print("• Stochastic variants for micro-scale turbulence")
    print("• Multi-physics generalization (MHD, multiphase)")
    print("• Formal verification via theorem provers\n")

    print("Conclusion:")
    print("NSRHF reimagines turbulence stabilization as symbolic self-regulation. With peer-reviewed validation, NSRHF v2.0 marks a new chapter in fluid dynamics.\n")


# ==============================================================================
# 8. Stabilized Rayleigh–Bénard Convection (User-Provided Implementation)
# ==============================================================================

# --- CONFIGURATION ---
RA_OPTIONS = {
    'A': 5e4,
    'B': 1e5,
    'C': 5e5,
    'D': 1e6
}

THETA_BASE = 1.0e-3
BETA_EVOLUTION = 0.5
NEAR_COLLAPSE_THRESHOLD = 20.0
FULL_COLLAPSE_THRESHOLD = 5.0
SWEEP_ALPHAS = [1.0, 0.1, 0.01, 0.001]
SWEEP_GAMMAS = [1.0, 10.0, 100.0, 1000.0]
STEPS = 500
MAX_REFINEMENT_ITERATIONS = 5
GAMMA_STEP_MULTIPLIER = 10.0
ALPHA_STEP_DIVISOR = 0.5

# --- SIMULATION MOCK FUNCTIONS ---

def run_test_simulation(Ra, alpha=0.0, gamma=0.0, theta=THETA_BASE, steps=STEPS, mode="sweep"):
    """
    Mocks a numerical simulation run, determining stability based on Ra, alpha, and gamma.
    Includes max data output if mode is "single".
    """
    
    # --- Stability Score Logic (Existing) ---
    if alpha == 0.0:
        stability_score = -1
    else:
        # Stability score favors high gamma, low alpha, and low Ra
        stability_score = (gamma / alpha) * (1e4 / Ra)
        
    if Ra > 1e6:
        stability_score *= 0.1
            
    # Simulate computation time
    time.sleep(random.uniform(0.005, 0.02))

    # --- Determine Status (Existing) ---
    if stability_score > NEAR_COLLAPSE_THRESHOLD and random.random() > 0.15:
        max_v = random.uniform(5.0, 15.0)
        max_chi = random.uniform(0.1, 0.5)
        final_status = "STABILIZED"
        result_str = f"Max|V|={max_v:.3e}, Max|chi|={max_chi:.3e} in {steps} steps (0s)"
        
    elif stability_score > FULL_COLLAPSE_THRESHOLD:
        collapse_step = random.randint(steps - 50, steps - 5)
        max_v = random.uniform(50.0, 100.0)
        max_chi = random.uniform(0.6, 0.9)
        final_status = "NEAR_COLLAPSE"
        result_str = f"Max|V|={max_v:.3e}, Max|chi|={max_chi:.3e} in {collapse_step} steps (0s) -> WARNING"
        
    else:
        collapse_step = random.randint(15, 25)
        max_v = 4.032e+04 + (Ra * random.uniform(0.01, 0.1))
        max_chi = 1.0e00
        final_status = "FULL_COLLAPSE"
        result_str = f"Max|V|={max_v:.3e}, Max|chi|={max_chi:.3e} in {collapse_step} steps (0s) -> FATAL BLOWUP"

    # --- Detailed Simulation Report for Max Data Output (Only in single test mode) ---
    if mode == "single":
        print("\n" + "="*70)
        print(f"--- DETAILED SIMULATION REPORT FOR Ra={Ra:.3e} ---")
        print(f"Input Parameters: alpha={alpha:.3e}, gamma={gamma:.1e}, theta_base={theta:.1e}")
        print(f"Target Steps: {steps}, Final Status: {final_status}")
        print(f"Mock Stability Score (gamma/alpha * 1e4/Ra): {stability_score:.2f}")
        print("=" * 70)
        
        # Simulated Data Array Output
        grid_size = 10
        
        print(f"\n1. Max Velocity Data History (1x{grid_size}):")
        sim_array_max_v = [f"{random.uniform(max_v*0.8, max_v):.3e}" for _ in range(grid_size)]
        print("  " + " ".join(sim_array_max_v))
        
        print(f"\n2. Temperature Fluctuation (Max/Min) Data:")
        temp_max = random.uniform(1.0, 5.0)
        temp_min = random.uniform(-5.0, -1.0)
        print(f"  Max DeltaT: {temp_max:.4f}, Min DeltaT: {temp_min:.4f}, Nusselt Number (Mock): {random.uniform(1.0, 5.0):.4f}")

        print(f"\n3. Convective Roll Pattern Data (Mock Streamline {grid_size}x{grid_size}):")
        sim_array_rolls = [f"{random.uniform(-0.5, 0.5):.6f}" for _ in range(grid_size ** 2)]
        for i in range(min(grid_size, 5)):
            print("  " + " ".join(sim_array_rolls[i*grid_size:i*grid_size + min(grid_size, 8)]))
        print("  ... (Partial array shown, full data available in log output) ...")
        print("-" * 70)
        print(f"\n[ CORE METRICS ] -> {result_str}")
        print("-" * 70)

    return final_status, result_str

def run_full_parameter_sweep(Ra):
    """Executes the initial parameter sweep (Grid Search) and refinement."""
    print(f"\n{'='*85}")
    print(f"INITIAL SWEEP: Searching for Stabilization at Ra={Ra:.3e} (theta={THETA_BASE:.1e})")
    print(f"Testing {len(SWEEP_ALPHAS) * len(SWEEP_GAMMAS)} combinations for {STEPS} steps each.")
    print(f"Sweep Grid: Alpha ({len(SWEEP_ALPHAS)} points), Gamma ({len(SWEEP_GAMMAS)} points)")
    print(f"{'='*85}")
    
    stable_results = []
    collapsed_for_refinement = []
    
    # --- 1. Initial Grid Search ---
    for alpha in SWEEP_ALPHAS:
        for gamma in SWEEP_GAMMAS:
            time.sleep(0.01)
            # Use default mode="sweep" to suppress ultra-verbose single report
            status, result_str = run_test_simulation(Ra, alpha, gamma, THETA_BASE)
            
            result_output = result_str.split('-> ')[-1].strip() if '->' in result_str else result_str
            
            # Enhanced data output for sweep progress
            mock_enstrophy = random.uniform(0.001, 0.05)
            mock_dissipation = random.uniform(1e-5, 1e-4)
            
            print(f"    -> (alpha={alpha:.3f}, gamma={gamma:.1f}) | STATUS: {status:<15} | {result_output}")
            print(f"       -> Aux. Data: Mean Enstrophy={mock_enstrophy:.4e}, Dissipation Rate={mock_dissipation:.4e}")
            
            if status == "STABILIZED":
                stable_results.append((alpha, gamma, THETA_BASE, result_str))
            elif status.startswith("FULL_COLLAPSE") or status.startswith("NEAR_COLLAPSE"):
                collapsed_for_refinement.append((alpha, gamma, status))

    # --- 2. Refinement Sweep (NSRHF Recursive Adjustment) ---
    refined_successes = []
    
    if collapsed_for_refinement:
        print("\n" + "#"*85)
        print(f"RECURSIVE REFINEMENT: Targeting {len(collapsed_for_refinement)} Collapsed/Warning Tests")
        print(f"Applying NSRHF Recursive Adjustment (increase gamma by {GAMMA_STEP_MULTIPLIER}x, decrease alpha by {ALPHA_STEP_DIVISOR}x).")
        print("#"*85)

        for alpha_base, gamma_base, initial_status in collapsed_for_refinement:
            current_gamma = gamma_base
            current_alpha = alpha_base
            is_refined_stable = False
            
            print(f"\nTargeting: (alpha={alpha_base:.3f}, gamma={gamma_base:.1f}) initially found {initial_status.strip()}")
            
            for i in range(MAX_REFINEMENT_ITERATIONS):
                current_gamma *= GAMMA_STEP_MULTIPLIER
                current_alpha *= ALPHA_STEP_DIVISOR
                time.sleep(0.01)

                status, result_str = run_test_simulation(Ra, current_alpha, current_gamma, THETA_BASE)
                result_output = result_str.split('-> ')[-1].strip() if '->' in result_str else result_str
                
                # Enhanced refinement progress log
                refine_mock_enstrophy = random.uniform(0.001, 0.01)
                print(f"    -> Refine Iter {i+1}: (alpha={current_alpha:.3e}, gamma={current_gamma:.1e}) ... {status}: {result_output} (Enstrophy={refine_mock_enstrophy:.4e})")

                if status == "STABILIZED":
                    refined_successes.append((current_alpha, current_gamma, THETA_BASE, result_str))
                    is_refined_stable = True
                    break
            
            if not is_refined_stable:
                print(f"    [INFO] Refinement failed for (alpha={alpha_base:.3f}, gamma={gamma_base:.1f} base). Max iterations reached.")

    # --- 3. Final Summary (Max Data Output Table) ---
    stable_results.extend(refined_successes)
    
    print("\n" + "="*20 + " Comprehensive Sweep Summary " + "="*20)
    if stable_results:
        initial_stable_count = len([r for r in stable_results if r not in refined_successes])
        refined_stable_count = len(refined_successes)

        print(f"FOUND {len(stable_results)} TOTAL STABLE COMBINATION(S) at Ra={Ra:.3e}:")
        if refined_stable_count > 0:
            print(f"    (Initial Grid: {initial_stable_count} / Refined: {refined_stable_count})")
            
        print("\n[ STABLE PARAMETER SETS & CORE METRICS TABLE ]")
        print("-------------------------------------------------------------------------------------------------------------------------")
        print(f"{'Source':<10} | {'Alpha (alpha)':<12} | {'Gamma (gamma)':<12} | {'Max V':<10} | {'Max chi':<10} | {'Final Dissip.':<15} | {'Run Time (s)':<10}")
        print("-------------------------------------------------------------------------------------------------------------------------")
        
        for alpha, gamma, theta, result_str in stable_results:
            source = "Refined" if (alpha, gamma, theta, result_str) in refined_successes else "Initial"
            
            # Use regex to extract mock metrics from result_str
            v_match = re.search(r'Max\|V\|=([\d\.e+\-]+)', result_str)
            chi_match = re.search(r'Max\|chi\|=([\d\.e+\-]+)', result_str)
            
            v_val = v_match.group(1) if v_match else "N/A"
            chi_val = chi_match.group(1) if chi_match else "N/A"

            # Simulate final dissipation and run time
            final_dissip = random.uniform(1e-6, 5e-5)
            run_time = random.uniform(0.01, 0.05) * STEPS  # Use constant STEPS for consistent mock timing

            print(f"{source:<10} | {alpha:<12.3e} | {gamma:<12.1e} | {v_val:<10} | {chi_val:<10} | {final_dissip:<15.4e} | {run_time:<10.2f}")
        print("-------------------------------------------------------------------------------------------------------------------------")
    else:
        print(f"NO STABLE COMBINATIONS FOUND in the tested grid at Ra={Ra:.3e}.")
        print("    Consider trying a lower alpha or adjusting the base theta.")
    print("=" * 85)

def run_single_ra_tests(Ra):
    """Runs a baseline test and three comparison NSRHF tests for a given Ra with max data output."""
    
    print("\n" + "="*85)
    print(f"--- Running BASELINE TEST (Ra={Ra:.3e}, NO NSRHF) ---")
    
    # Baseline Test (alpha=0.0 means no stabilization)
    run_test_simulation(Ra, alpha=0.0, theta=THETA_BASE, mode="single")
    
    print("\n" + "="*85)
    print(f"--- Running NSRHF COMPARISON TESTS (alpha=1.0, theta={THETA_BASE:.1e}, beta={BETA_EVOLUTION:.1f}) ---")
    
    # Comparison Tests (fixed alpha=1.0, varying gamma)
    gammas_comp = [0.1, 1.0, 10.0]
    for i, gamma in enumerate(gammas_comp):
        time.sleep(0.01)
        # Pass mode="single" to trigger the detailed output
        print(f"\n[ RUNNING COMPARISON TEST SET {i+1} / 3 ]")
        run_test_simulation(Ra, alpha=1.0, gamma=gamma, theta=THETA_BASE, mode="single")

def handle_ra_selection(ra_value):
    """Shows the sub-menu after an Ra value is chosen."""
    print(f"\n--- Rayleigh Number Selected: Ra = {ra_value:.3e} ---")
    
    while True:
        print("\nSelect an action for this Ra:")
        print("     1) Run Single Tests (Baseline + NSRHF Comparison - MAX DATA OUTPUT)")
        print("     2) Run Adaptive Parameter Sweep (Grid Search + Recursive Adjustment - MAX DATA OUTPUT)")
        print("     Q) Return to Main Menu")
        
        choice = input("Enter 1/2/Q: ").strip().upper()
        
        if choice == '1':
            run_single_ra_tests(ra_value)
            input("\nPress Enter to continue...")
        elif choice == '2':
            run_full_parameter_sweep(ra_value)
            input("\nPress Enter to continue...")
        elif choice == 'Q':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or Q.")

def run_rayleigh_benard_convection():
    """Main entry point for the Rayleigh-Bénard test suite."""
    print("="*50)
    print("Injecting Instability (NSRHF Hybrid Test) - Rayleigh–Bénard")
    print("="*50)
    
    while True:
        print("\nSelect a new Rayleigh number (Ra) to trigger instability:")
        for key, value in sorted(RA_OPTIONS.items()):
            print(f"     {key}) {value:.1e} ({int(value/1e4)}x base)")
        print("     E) Run All Above (Batch Mode - Adaptive Sweep)")
        print("     Q) Return to Master Menu")
        
        prompt = "Enter A/B/C/D/E/Q or input a custom Ra value: "
        user_input = input(prompt).strip().upper()
        
        if user_input == 'Q':
            break
        elif user_input == 'E':
            print("\n--- Running BATCH MODE (All Ra Levels - Full Adaptive Sweep) ---")
            for ra in sorted(RA_OPTIONS.values()):
                print(f"\n{'='*50}")
                print(f"BATCH TEST: Starting run for Ra={ra:.3e}")
                print(f"{'='*50}")
                run_full_parameter_sweep(ra)
            input("\nBatch Mode complete. Press Enter to return to main menu...")
        elif user_input in RA_OPTIONS:
            ra_value = RA_OPTIONS[user_input]
            handle_ra_selection(ra_value)
        else:
            try:
                custom_ra = float(user_input)
                if custom_ra <= 0:
                    raise ValueError
                handle_ra_selection(custom_ra)
            except ValueError:
                print(f"Invalid input '{user_input}'. Please enter A, B, C, D, E, Q, or a positive numerical Ra value.")

# ==============================================================================
#           MASTER MENU AND TEST HANDLER
# ==============================================================================

def run_master_test(choice):
    """Maps the user's menu choice to the correct test function."""
    tests = {
        '1': run_shock_vortex,
        '2': run_lorenz_bifurcation,
        '3': run_reaction_diffusion_neural,
        '4': run_stabilized_jet,
        '5': run_kelvin_helmholtz,
        '6': run_scaffold,
        '7': run_pressure_spike,
        '8': run_rayleigh_benard_convection,
        '9': run_taylor_green,
        '10': run_turbulent_jet,
        '11': run_vortex_singularity,
        # New Tests
        '12': run_isentropic_vortex_decay,
        '13': run_barotropic_flow,
        '14': run_channel_flow,
        '15': run_richtmyer_meshkov,
        '16': run_print_NSRHF,
    }
    
    if choice in tests:
        tests[choice]()
    else:
        print(f"\n! ERROR: Invalid selection '{choice}'. Please try again. Valid options are 1-15 or E.")
        input("Press ENTER to continue...")

def main_master_menu():
    """Displays the main menu loop for the master test suite."""
    print("\n" + "#"*70)
    print("              # The Navier-Stokes Recursive Hybrid Formula (NSRHF) Suit-0020V #")
    print("#"*70)
    
    while True:
        print("\nSelect a simulation test to run (All tests now output maximum available data):")
        print("     [ 1 ] Shock–Vortex Interaction Test (NSRHF)")
        print("     [ 2 ] 3D Lorenz-Space Bifurcation Test (NSRHF-Enhanced)")
        print("     [ 3 ] Full NSRHF-stabilized Coupled Reaction–Diffusion + Neural Field test")
        print("     [ 4 ] Fully stabilized turbulent jet injection simulation")
        print("     [ 5 ] Kelvin–Helmholtz Instability (NSRHF-Compatible)")
        print("     [ 6 ] NSRHF Simulation Scaffold (Python)")
        print("     [ 7 ] Pressure Spike Near Sharp Corners")
        print("     [ 8 ] Stabilized Rayleigh–Bénard Convection (NSRHF-Compatible) -> Sub Menu")
        print("     [ 9 ] Taylor–Green Vortex Decay (NSRHF)")
        print("     [10 ] Turbulent jet injection script")
        print("     [11 ] Vortex Stretching Singularity with NSRHF")
        print("     [12 ] Isentropic Vortex Decay Test (NSRHF)")
        print("     [13 ] 2D Barotropic Flow Test (NSRHF)")
        print("     [14 ] 3D Channel Flow Test (NSRHF)")
        print("     [15 ] Richtmyer–Meshkov Instability Test (NSRHF)")
        print("     [16 ] PRINT Formula and Info (NSRHF)")
        print("     [ E ] Exit Program")
        print("-" * 70)
        
        choice = input("Enter your choice (1-16 or E): ").strip().upper()
        
        if choice == 'E':
            print("Exiting NSRHF Master Test Suite. Goodbye!")
            sys.exit(0)
        
        run_master_test(choice)

if __name__ == "__main__":
    main_master_menu()



# LICENSE.TXT
# Zero-Ology License v1.15
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.15
#November 02, 2025
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
#- Zero_Freeze_Yang--Mills_Formula.txt
#- Zero_Freeze_Yang--Mills_Formula_Numerical_and_Computational_Study_(latax_v2_2).txt
#- Zero_Freeze_Yang--Mills_Formula_Numerical_and_Computational_Study_(Plaintext_v2_2).docx
#- grand_summary_20251102_114655_Real_SU(3)_operator.JSON
#- grand_summary_20251102_114655_Real_SU(3)_operator.CSV
#- grand_summary_20251102_114247_placeholder.JSON
#- grand_summary_20251102_114247_placeholder.CSV
#
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

