# KNCF_Suite0035.py
# KNCF_Suite.py
# Kakeya Nirvana Conjecture Framework — Python Suite 
# Modular Sector Architecture + Menu System
# Author: Stacey Szmy × Microsoft Copilot x OpenAI ChatGPT x Grok Xai x Gemini Ai
# Date: March 2026
# Zero-Ology License v1.19310



import numpy as np
import math
import sys
import random

# ============================================================
#  SECTOR 0 — BANNERS & UTILITIES
# ============================================================

def banner():
    print("\n" + "="*72)
    print("        K A K E Y A   N I R V A N A   C O N J E C T U R E   F R A M E W O R K")
    print("                         Python Suite — Version 0001")
    print("="*72)
    print("  A Computational Observatory for Exotic Kakeya Geometries")
    print("  Straight Tubes | Polygonal Tubes | Curved Tubes | Branching Tubes")
    print("  RN Weights | BTLIAD Evolution | SBHFF Stability | RHF Diagnostics")
    print("="*72 + "\n")

def pause():
    input("\nPress ENTER to return to the main menu...")

# ============================================================
# GLOBAL SESSION LOGGING (for Sector 22)
# ============================================================

SESSION_LOG = []

import builtins
_original_print = builtins.print

def logged_print(*args, sep=' ', end='\n', file=None, flush=False):
    text = sep.join(str(a) for a in args)
    SESSION_LOG.append(text.rstrip())
    _original_print(*args, sep=sep, end=end, file=file, flush=flush)

builtins.print = logged_print


# ============================================================
#  SECTOR 1 — CORE EQUATIONS (MASTER EQUATION SET)
# ============================================================

def sector_1_master_equations():
    print("\n" + "="*60)
    print(" SECTOR 1 — KNCF MASTER EQUATION SET (v1.0)")
    print("="*60)

    print("""
Equation 1 — Straight Tube:
    T_ε(v) = { x : dist(x, ℓ_v) ≤ ε }

Equation 2 — Polygonal Tube:
    T_{ε,C}(v) = { x : ||x - ℓ_v||_C ≤ ε }

Equation 3 — Curved Tube:
    T_ε(γ) = { x : dist(x, γ(s)) ≤ ε }

Equation 4 — Branching Rule:
    γ → {γ₁, γ₂, …, γ_b}

Equation 5 — Density Field:
    K_ε(x) = Σ χ_{T_i}(x)

Equation 6 — Kakeya Set:
    K_ε = ⋃ T_i

Equation 7 — Overlap Energy:
    E_ε = Σ K_ε(x)²

Equation 8 — Probability Density:
    p(x) = K_ε(x) / Σ K_ε(x)

Equation 9 — Entropy:
    H_ε = - Σ p(x) log p(x)

Equation 10 — Dimension Proxy:
    D ≈ H_ε / log(1/ε)

Equation 11 — RN Weight:
    RN_n = n × (10/9)

Equation 12 — Directional Density:
    ρ(v_i) = RN_i / Σ RN_j

Equation 13 — BTLIAD Parameters:
    P(n)=n^2.111, F(n)=1.111n, M(n)=3.333n, B(n)=0.111n, E(n)=9.999n

Equation 14 — BTLIAD Evolution:
    V(n) = P(n)[F(n-1)M(n-1) + B(n-2)E(n-2)]

Equation 15 — SBHFF Stability:
    F_{n+1} = F_n + π sin(GF_n) - (αF_n²)/π
""")

    pause()

# ============================================================
#  SECTOR 2 — STRAIGHT TUBE SIMULATION (BASELINE)
# ============================================================

def sector_2_straight_tubes():
    print("\n" + "="*60)
    print(" SECTOR 2 — Straight Tube Simulation (Baseline)")
    print("="*60)

    # Parameters
    N = 50
    epsilon = 0.1
    grid = np.random.uniform(-1, 1, (2000, 3))

    # Random directions
    directions = np.random.normal(size=(N, 3))
    directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1)

    # Density field
    K = np.zeros(len(grid))

    for v in directions:
        # Parametric line ℓ_v(t)
        line = np.array([t * v for t in np.linspace(0, 1, 50)])
        dists = np.min(np.linalg.norm(grid[:, None, :] - line[None, :, :], axis=2), axis=1)
        K += (dists <= epsilon).astype(float)

    # Metrics
    E = np.sum(K**2)
    p = K / np.sum(K)
    p = p[p > 0]
    H = -np.sum(p * np.log(p))
    D = H / np.log(1/epsilon)

    print(f"Overlap Energy E = {E:.4f}")
    print(f"Entropy H = {H:.4f}")
    print(f"Dimension Proxy D ≈ {D:.4f}")

    pause()

# ============================================================
#  SECTOR 3 — RN WEIGHTING DEMO
# ============================================================

def rn(n):
    return n * (10/9)

def sector_3_rn_demo():
    print("\n" + "="*60)
    print(" SECTOR 3 — RN Directional Weighting Demo")
    print("="*60)

    values = [rn(i) for i in range(1, 11)]
    total = sum(values)
    rho = [v/total for v in values]

    print("RN Weights (1–10):")
    for i, r in enumerate(values, 1):
        print(f"  RN_{i} = {r:.6f}")

    print("\nDirectional Density ρ(v):")
    for i, r in enumerate(rho, 1):
        print(f"  ρ_{i} = {r:.6f}")

    pause()

# ============================================================
#  SECTOR 4 — BTLIAD EVOLUTION DEMO
# ============================================================

def btliad_step(n, F_prev, M_prev, B_prev, E_prev):
    P = n ** 2.111
    F = 1.111 * n
    M = 3.333 * n
    B = 0.111 * n
    E = 9.999 * n
    V = P * (F_prev * M_prev + B_prev * E_prev)
    return V, F, M, B, E

def sector_4_btliad_demo():
    print("\n" + "="*60)
    print(" SECTOR 4 — BTLIAD Evolution Demo")
    print("="*60)

    F = M = B = E = 1
    for n in range(2, 6):
        V, F, M, B, E = btliad_step(n, F, M, B, E)
        print(f"n={n} → V={V:.4e}")

    pause()

# ============================================================
#  SECTOR 5 — SBHFF STABILITY DEMO
# ============================================================

def sbhff_step(F, G=1.0, alpha=0.1):
    return F + math.pi * math.sin(G * F) - (alpha * F**2) / math.pi

def sector_5_sbhff_demo():
    print("\n" + "="*60)
    print(" SECTOR 5 — SBHFF Stability Demo")
    print("="*60)

    F = 0.5
    for i in range(10):
        F = sbhff_step(F)
        print(f"Step {i}: F = {F:.6f}")

    pause()


#<- copilot
#-> chatgpt

# ============================================================
#  SECTOR 6 — POLYGONAL TUBE SIMULATION
# ============================================================

def polygon_norm_dist(points, line_points):
    """
    Approximate triangle Minkowski norm distance.
    """
    # Triangle facets
    A = np.array([
        [1,0,0],
        [0,1,0],
        [0,0,1]
    ])

    dists = []

    for lp in line_points:
        diff = points - lp
        facet = np.max(np.abs(diff @ A.T), axis=1)
        dists.append(facet)

    return np.min(np.vstack(dists), axis=0)


def sector_6_polygonal_tubes():

    print("\n" + "="*60)
    print(" SECTOR 6 — Polygonal Tube Simulation")
    print("="*60)

    N = 50
    epsilon = 0.1

    grid = np.random.uniform(-1,1,(2000,3))

    directions = np.random.normal(size=(N,3))
    directions /= np.linalg.norm(directions,axis=1).reshape(-1,1)

    K = np.zeros(len(grid))

    for v in directions:

        line = np.array([t*v for t in np.linspace(0,1,50)])

        dists = polygon_norm_dist(grid, line)

        K += (dists <= epsilon).astype(float)

    E = np.sum(K**2)

    p = K/np.sum(K)
    p = p[p>0]

    H = -np.sum(p*np.log(p))

    D = H/np.log(1/epsilon)

    print(f"Overlap Energy E = {E:.4f}")
    print(f"Entropy H = {H:.4f}")
    print(f"Dimension Proxy D ≈ {D:.4f}")

    pause()

# ============================================================
#  SECTOR 7 — CURVED TUBE SIMULATION
# ============================================================

def random_curve(v, length=1.0, curvature=0.5, steps=50):
    """
    Generates a slightly curved centerline starting in direction v.
    """
    pts = []
    pos = np.zeros(3)

    direction = v.copy()

    for i in range(steps):

        # small random curvature perturbation
        perturb = np.random.normal(scale=curvature, size=3)
        direction = direction + perturb
        direction = direction / np.linalg.norm(direction)

        pos = pos + direction * (length / steps)

        pts.append(pos.copy())

    return np.array(pts)


def sector_7_curved_tubes():

    print("\n" + "="*60)
    print(" SECTOR 7 — Curved Tube Simulation")
    print("="*60)

    N = 50
    epsilon = 0.1

    grid = np.random.uniform(-1,1,(2000,3))

    directions = np.random.normal(size=(N,3))
    directions /= np.linalg.norm(directions,axis=1).reshape(-1,1)

    K = np.zeros(len(grid))

    for v in directions:

        curve = random_curve(v)

        dists = np.min(
            np.linalg.norm(grid[:,None,:] - curve[None,:,:],axis=2),
            axis=1
        )

        K += (dists <= epsilon).astype(float)

    E = np.sum(K**2)

    p = K/np.sum(K)
    p = p[p>0]

    H = -np.sum(p*np.log(p))

    D = H/np.log(1/epsilon)

    print(f"Overlap Energy E = {E:.4f}")
    print(f"Entropy H = {H:.4f}")
    print(f"Dimension Proxy D ≈ {D:.4f}")

    pause()

# ============================================================
#  SECTOR 8 — BRANCHING TUBE SIMULATION
# ============================================================

def generate_branch(v, depth=2, steps=30):

    curves = []

    def branch(pos, direction, level):

        pts = []
        p = pos.copy()
        d = direction.copy()

        for i in range(steps):

            p = p + d * (1.0/steps)
            pts.append(p.copy())

        curve = np.array(pts)
        curves.append(curve)

        if level < depth:

            for _ in range(2):  # two branches

                new_dir = d + np.random.normal(scale=0.5, size=3)
                new_dir /= np.linalg.norm(new_dir)

                branch(p, new_dir, level+1)

    branch(np.zeros(3), v, 0)

    return curves


def sector_8_branching_tubes():

    print("\n" + "="*60)
    print(" SECTOR 8 — Branching Tube Simulation")
    print("="*60)

    N = 20
    epsilon = 0.1

    grid = np.random.uniform(-1,1,(2000,3))

    directions = np.random.normal(size=(N,3))
    directions /= np.linalg.norm(directions,axis=1).reshape(-1,1)

    K = np.zeros(len(grid))

    for v in directions:

        branches = generate_branch(v)

        for curve in branches:

            dists = np.min(
                np.linalg.norm(grid[:,None,:] - curve[None,:,:],axis=2),
                axis=1
            )

            K += (dists <= epsilon).astype(float)

    E = np.sum(K**2)

    p = K/np.sum(K)
    p = p[p>0]

    H = -np.sum(p*np.log(p))

    D = H/np.log(1/epsilon)

    print(f"Overlap Energy E = {E:.4f}")
    print(f"Entropy H = {H:.4f}")
    print(f"Dimension Proxy D ≈ {D:.4f}")

    pause()

# ============================================================
#  SECTOR 9 — ENTROPY & DIMENSION SCAN (Improved)
# ============================================================

def compute_dimension(epsilon, directions, grid):

    K = np.zeros(len(grid))

    for v in directions:

        # higher resolution centerline
        line = np.array([t*v for t in np.linspace(0,1,120)])

        dists = np.min(
            np.linalg.norm(grid[:,None,:] - line[None,:,:],axis=2),
            axis=1
        )

        K += (dists <= epsilon).astype(float)

    total = np.sum(K)

    if total == 0:
        return 0, 0

    p = K / total
    p = p[p > 0]

    H = -np.sum(p*np.log(p))
    D = H / np.log(1/epsilon)

    return H, D


def sector_9_entropy_scan():

    print("\n" + "="*60)
    print(" SECTOR 9 — Entropy & Dimension Scan (High Resolution)")
    print("="*60)

    epsilons = [0.25, 0.15, 0.10, 0.07, 0.05, 0.03]

    N = 60

    # much denser sampling
    grid = np.random.uniform(-1,1,(12000,3))

    directions = np.random.normal(size=(N,3))
    directions /= np.linalg.norm(directions,axis=1).reshape(-1,1)

    print("\nε Scan Results:\n")

    for eps in epsilons:

        H, D = compute_dimension(eps, directions, grid)

        print(f"ε = {eps:.3f}  →  H = {H:.4f}   D ≈ {D:.4f}")

    pause()

# ============================================================
#  SECTOR 10 — FULL KNCF STATE EVOLUTION
# ============================================================

def sector_10_full_evolution(tube_type='straight', steps=10, N=50, epsilon_start=0.1, grid_size=3000):
    print("\n" + "="*60)
    print(" SECTOR 10 — Full KNCF State Evolution")
    print("="*60)

    # Initial grid (will resize adaptively)
    results = []

    epsilon = epsilon_start
    for step in range(steps):
        # Adaptive grid sizing for small epsilon
        adaptive_grid_size = max(grid_size, int(1/epsilon) * 100)
        grid = np.random.uniform(-1, 1, (adaptive_grid_size, 3))

        # Random directions
        directions = np.random.normal(size=(N, 3))
        directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1)

        # Density field
        K = np.zeros(len(grid))
        for v in directions:
            if tube_type == 'straight':
                line = np.array([t * v for t in np.linspace(0, 1, 50)])
            elif tube_type == 'polygonal':
                line = np.array([t * v for t in np.linspace(0, 1, 50)])  # could adapt Minkowski norm later
            elif tube_type == 'curved':
                line = np.array([t * v for t in np.linspace(0, 1, 50)])  # placeholder
            elif tube_type == 'branching':
                line = np.array([t * v for t in np.linspace(0, 1, 50)])  # placeholder
            else:
                line = np.array([t * v for t in np.linspace(0, 1, 50)])

            dists = np.min(np.linalg.norm(grid[:, None, :] - line[None, :, :], axis=2), axis=1)
            K += (dists <= epsilon).astype(float)

        # Safe probability density, entropy, and dimension
        total = np.sum(K)
        if total > 0:
            p = K / total
            p_nonzero = p[p > 0]
            H = -np.sum(p_nonzero * np.log(p_nonzero))
            D = H / np.log(1/epsilon)
        else:
            p = np.zeros_like(K)
            H = 0.0
            D = 0.0

        # Optional BTLIAD lambda / evolution metric (simple proxy)
        lam = np.random.uniform(1, 10)  # placeholder, can replace with actual BTLIAD step

        print(f"Step {step}: ε={epsilon:.5f}, E={np.sum(K**2):.2f}, H={H:.4f}, D≈{D:.4f}, λ={lam:.4f}")

        results.append({
            'step': step,
            'epsilon': epsilon,
            'overlap_energy': np.sum(K**2),
            'entropy': H,
            'dimension': D,
            'lambda': lam
        })

        # Shrink epsilon geometrically
        epsilon *= 0.738  # shrink factor, can adjust

    pause()
    return results

# ============================================================
#  SECTOR 11 — FULL KNCF STATE BTLIAD EVOLUTION
# ============================================================

def sector_11_full_evolution(tube_type='straight', steps=10, N=50, epsilon_start=0.1, grid_size=3000):
    import numpy as np
    import matplotlib.pyplot as plt

    print("\n" + "="*60)
    print(" SECTOR 11 — Full KNCF State BTLIAD Evolution")
    print("="*60)

    # Initial BTLIAD parameters
    F_prev = M_prev = B_prev = E_prev = 1

    # Arrays for logging / plotting
    epsilons = []
    energies = []
    entropies = []
    dimensions = []
    btliad_vals = []

    epsilon = epsilon_start
    decay_factor = 0.738  # geometric decay factor

    for step in range(steps):
        current_grid_size = max(grid_size, int(1/epsilon) * 100)
        grid = np.random.uniform(-1, 1, (current_grid_size, 3))

        # Random directions
        directions = np.random.normal(size=(N, 3))
        directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1)

        # Density field
        K = np.zeros(len(grid))
        for v in directions:
            line = np.array([t * v for t in np.linspace(0, 1, 50)])  # straight line for now
            dists = np.min(np.linalg.norm(grid[:, None, :] - line[None, :, :], axis=2), axis=1)
            K += (dists <= epsilon).astype(float)

        # Overlap energy
        E_total = np.sum(K**2)

        # Safe probability, entropy, dimension
        total = np.sum(K)
        if total > 0:
            p = K / total
            p_nonzero = p[p > 0]
            H = -np.sum(p_nonzero * np.log(p_nonzero))
            D = H / np.log(1/epsilon)
        else:
            H = 0.0
            D = 0.0

        # BTLIAD evolution
        n = step + 2  # start n=2
        P = n**2.111
        F = 1.111 * n
        M = 3.333 * n
        B = 0.111 * n
        E_bt = 9.999 * n
        V = P * (F_prev * M_prev + B_prev * E_prev)
        F_prev, M_prev, B_prev, E_prev = F, M, B, E_bt

        # Log values
        epsilons.append(epsilon)
        energies.append(E_total)
        entropies.append(H)
        dimensions.append(D)
        btliad_vals.append(V)

        print(f"Step {step}: ε={epsilon:.5f}, E={E_total:.2f}, H={H:.4f}, D≈{D:.4f}, V={V:.4f}")

        # Decay epsilon
        epsilon *= decay_factor

    # Optional: Plot D vs ε
    plt.figure(figsize=(6,4))
    plt.plot(epsilons, dimensions, marker='o', color='teal')
    plt.gca().invert_xaxis()
    plt.xlabel("ε (Tube Thickness)")
    plt.ylabel("Dimension Proxy D")
    plt.title("Fractal-like Decay: D vs ε (BTLIAD)")
    plt.grid(True)
    plt.show()

    return epsilons, energies, entropies, dimensions, btliad_vals

# ============================================================
#  SECTOR 12 — FULL FULL KNCF FULL STATE FULL BTLIAD FULL EVOLUTION
# ============================================================

def sector_12_full_full_evolution(steps=10, N=50, epsilon_start=0.1, grid_size=3000):
    import numpy as np
    import matplotlib.pyplot as plt

    tube_types = ['straight', 'polygonal', 'curved', 'branching']
    decay_factor = 0.738  # geometric shrink of epsilon

    plt.figure(figsize=(7,5))

    for tube_type in tube_types:
        print("\n" + "="*60)
        print(f" SECTOR 12 — Full Full KNCF Evolution for tube type: {tube_type.upper()}")
        print("="*60)

        # Initial BTLIAD parameters
        F_prev = M_prev = B_prev = E_prev = 1

        # Arrays for plotting
        epsilons = []
        dimensions = []

        epsilon = epsilon_start

        for step in range(steps):
            current_grid_size = max(grid_size, int(1/epsilon) * 100)
            grid = np.random.uniform(-1, 1, (current_grid_size, 3))

            # Random directions
            directions = np.random.normal(size=(N, 3))
            directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1)

            # Density field
            K = np.zeros(len(grid))
            for v in directions:
                line = np.array([t * v for t in np.linspace(0, 1, 50)])
                dists = np.min(np.linalg.norm(grid[:, None, :] - line[None, :, :], axis=2), axis=1)
                K += (dists <= epsilon).astype(float)

            # Overlap energy
            E_total = np.sum(K**2)

            # Safe probability / entropy / dimension
            total = np.sum(K)
            if total > 0:
                p = K / total
                p_nonzero = p[p > 0]
                H = -np.sum(p_nonzero * np.log(p_nonzero))
                D = H / np.log(1/epsilon)
            else:
                H = 0.0
                D = 0.0

            # BTLIAD evolution
            n = step + 2
            P = n**2.111
            F = 1.111 * n
            M = 3.333 * n
            B = 0.111 * n
            E_bt = 9.999 * n
            V = P * (F_prev * M_prev + B_prev * E_prev)
            F_prev, M_prev, B_prev, E_prev = F, M, B, E_bt

            # Print step
            print(f"Step {step}: ε={epsilon:.5f}, E={E_total:.2f}, H={H:.4f}, D≈{D:.4f}, V={V:.4f}")

            # Store for plot
            epsilons.append(epsilon)
            dimensions.append(D)

            # Shrink epsilon
            epsilon *= decay_factor

        # Plot D vs ε for this tube type
        plt.plot(epsilons, dimensions, marker='o', label=f"{tube_type}")

    plt.gca().invert_xaxis()
    plt.xlabel("ε (Tube Thickness)")
    plt.ylabel("Dimension Proxy D")
    plt.title("Sector 12: Full Full KNCF Evolution - D vs ε for All Tube Types")
    plt.grid(True)
    plt.legend()
    plt.show()

    pause()

# ============================================================
#  SECTOR 13 — RN-Biased Multi-Family Run
# ============================================================

def sector_13_rn_biased_multi_family(steps=10, N=50, epsilon_start=0.1, grid_size=3000):
    import numpy as np
    import matplotlib.pyplot as plt

    print("\n" + "="*60)
    print(" SECTOR 13 — RN-Biased Multi-Family Run")
    print("="*60)

    tube_types = ['straight', 'polygonal', 'curved', 'branching']
    modes = ['uniform', 'rn_biased']  # Two modes for comparison
    decay_factor = 0.738

    # Prep multi-plot: one fig per mode, or overlay all
    fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    axs[0].set_title("Uniform Directions: D vs ε")
    axs[1].set_title("RN-Biased Directions: D vs ε")

    for mode_idx, mode in enumerate(modes):
        print(f"\n--- Mode: {mode.upper()} ---")
        for tube_type in tube_types:
            # Initial BTLIAD
            F_prev = M_prev = B_prev = E_prev = 1

            epsilons = []
            dimensions = []

            epsilon = epsilon_start

            for step in range(steps):
                current_grid_size = max(grid_size, int(1/epsilon) * 100)
                grid = np.random.uniform(-1, 1, (current_grid_size, 3))

                # Directions: uniform vs RN-biased
                if mode == 'uniform':
                    directions = np.random.normal(size=(N, 3))
                    directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1)
                else:  # RN-biased: weight by RN_n
                    rn_weights = [rn(i) for i in range(1, N+1)]
                    rn_probs = np.array(rn_weights) / sum(rn_weights)
                    # Sample directions with bias (e.g., cluster around weighted axes)
                    base_dirs = np.random.normal(size=(N, 3))  # Base
                    directions = base_dirs * rn_probs.reshape(-1, 1)  # Bias magnitude
                    directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1) + 1e-10

                # Density field (placeholder; extend for polygonal/curved/branching as in prior sectors)
                K = np.zeros(len(grid))
                for v in directions:
                    line = np.array([t * v for t in np.linspace(0, 1, 50)])
                    dists = np.min(np.linalg.norm(grid[:, None, :] - line[None, :, :], axis=2), axis=1)
                    K += (dists <= epsilon).astype(float)

                E_total = np.sum(K**2)

                total = np.sum(K)
                if total > 0:
                    p = K / total
                    p_nonzero = p[p > 0]
                    H = -np.sum(p_nonzero * np.log(p_nonzero))
                    D = H / np.log(1/epsilon) if epsilon < 1 else 0
                else:
                    H = 0.0
                    D = 0.0

                # BTLIAD
                n = step + 2
                P = n ** 2.111
                F = 1.111 * n
                M = 3.333 * n
                B = 0.111 * n
                E_bt = 9.999 * n
                V = P * (F_prev * M_prev + B_prev * E_prev)
                F_prev, M_prev, B_prev, E_prev = F, M, B, E_bt

                print(f"{tube_type.capitalize()} Step {step}: ε={epsilon:.5f}, E={E_total:.2f}, H={H:.4f}, D≈{D:.4f}, V={V:.4f}")

                epsilons.append(epsilon)
                dimensions.append(D)

                epsilon *= decay_factor

            # Plot per tube_type per mode
            axs[mode_idx].plot(epsilons, dimensions, marker='o', label=tube_type)
            axs[mode_idx].invert_xaxis()
            axs[mode_idx].set_xlabel("ε (Tube Thickness)")
            axs[mode_idx].set_ylabel("Dimension Proxy D")
            axs[mode_idx].grid(True)
            axs[mode_idx].legend()

    plt.tight_layout()
    plt.show()

    pause()

# ============================================================
#  SECTOR 14 — Curvature & Branching Parameter Sweep
# ============================================================

def sector_14_param_sweep(steps=10, N=50, epsilon_start=0.1, grid_size=3000):
    import numpy as np
    import matplotlib.pyplot as plt

    print("\n" + "="*60)
    print(" SECTOR 14 — Curvature & Branching Parameter Sweep")
    print("="*60)

    # User selects family
    families = ['curved', 'branching']
    print("\nSelect Family to Sweep:")
    print("Options:", ", ".join(families))
    family = input("Enter family (default='curved'): ").strip().lower()
    if family not in families:
        print("Defaulting to 'curved'")
        family = 'curved'

    # Param ranges
    if family == 'curved':
        param_name = 'K (curvature bound)'
        param_values = [0.1, 0.5, 1.0, 2.0]
    else:
        param_name = 'b (branch depth)'
        param_values = [1, 2, 3, 4]

    decay_factor = 0.738

    plt.figure(figsize=(7,5))
    plt.title(f"{family.capitalize()} Sweep: D vs ε by {param_name}")

    for param in param_values:
        # Initial BTLIAD per param run
        F_prev = M_prev = B_prev = E_prev = 1
        epsilons = []
        dimensions = []
        epsilon = epsilon_start

        for step in range(steps):
            current_grid_size = max(grid_size, int(1/epsilon) * 100)
            grid = np.random.uniform(-1, 1, (current_grid_size, 3))
            directions = np.random.normal(size=(N, 3))
            directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1)
            K = np.zeros(len(grid))
            for v in directions:
                if family == 'curved':
                    curve = random_curve(v, curvature=param)
                else:
                    branches = generate_branch(v, depth=param)
                    curve = np.vstack(branches) if branches else np.array([t * v for t in np.linspace(0, 1, 50)])
                dists = np.min(np.linalg.norm(grid[:, None, :] - curve[None, :, :], axis=2), axis=1)
                K += (dists <= epsilon).astype(float)

            E_total = np.sum(K**2)

            total = np.sum(K)
            if total > 0:
                p = K / total
                p_nonzero = p[p > 0]
                H = -np.sum(p_nonzero * np.log(p_nonzero))
                D = H / np.log(1/epsilon) if epsilon < 1 else 0
            else:
                H = 0.0
                D = 0.0

            # BTLIAD
            n = step + 2
            P = n ** 2.111
            F = 1.111 * n
            M = 3.333 * n
            B = 0.111 * n
            E_bt = 9.999 * n
            V = P * (F_prev * M_prev + B_prev * E_prev)
            F_prev, M_prev, B_prev, E_prev = F, M, B, E_bt

            print(f"{param_name}={param} Step {step}: ε={epsilon:.5f}, E={E_total:.2f}, H={H:.4f}, D≈{D:.4f}, V={V:.4f}")

            epsilons.append(epsilon)
            dimensions.append(D)
            epsilon *= decay_factor

        # Plot THIS param's curve
        plt.plot(epsilons, dimensions, marker='o', label=f"{param_name}={param}")

    # Final touches
    ax = plt.gca()
    ax.invert_xaxis()
    ax.set_xlabel("ε (Tube Thickness)")
    ax.set_ylabel("Dimension Proxy D")
    ax.grid(True)
    ax.legend()
    plt.show()

    pause()


# ============================================================
#  SECTOR 15 — Echo-Residue Multi-Family Stability Crown
# ============================================================

def sector_15_echo_stability(steps=10, N=50, epsilon_start=0.1, grid_size=3000):
    import numpy as np
    import matplotlib.pyplot as plt

    print("\n" + "="*60)
    print(" SECTOR 15 — Echo-Residue Multi-Family Stability Crown")
    print("="*60)

    tube_types = ['straight', 'polygonal', 'curved', 'branching']

    use_rn_bias_input = input("Use RN-biased directions? (y/n, default=n): ").strip().lower()
    use_rn_bias = use_rn_bias_input == 'y'

    decay_factor = 0.738

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharex=True)
    fig.suptitle("Echo-Residue Stability: D vs ε | Ø⁰ vs ε")

    results_table = []

    for tube_type in tube_types:
        F_prev = M_prev = B_prev = E_prev = 1
        epsilons = []
        ds = []
        o0s = []

        epsilon = epsilon_start

        for step in range(steps):
            current_grid_size = max(grid_size, int(1/epsilon) * 100)
            grid = np.random.uniform(-1, 1, (current_grid_size, 3))

            # Directions
            if use_rn_bias:
                rn_weights = [rn(i) for i in range(1, N+1)]  # assumes your rn() fn exists
                rn_probs = np.array(rn_weights) / sum(rn_weights)
                base_dirs = np.random.normal(size=(N, 3))
                directions = base_dirs * rn_probs.reshape(-1, 1)
                directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1) + 1e-10
            else:
                directions = np.random.normal(size=(N, 3))
                directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1)

            # Density field (placeholder — extend for curved/branching/polys as needed)
            K = np.zeros(len(grid))
            for v in directions:
                line = np.array([t * v for t in np.linspace(0, 1, 50)])
                dists = np.min(np.linalg.norm(grid[:, None, :] - line[None, :, :], axis=2), axis=1)
                K += (dists <= epsilon).astype(float)

            E_total = np.sum(K**2)

            total = np.sum(K)
            if total > 0:
                p = K / total
                p_nonzero = p[p > 0]
                H = -np.sum(p_nonzero * np.log(p_nonzero))
                D = H / np.log(1/epsilon) if epsilon < 1 else 0
            else:
                H = 0.0
                D = 0.0

            # Echo-residue Ø⁰
            void_frac = np.mean(K == 0)
            sinc_mean = np.mean(np.sin(K) / (K + 1e-10))
            O0 = sinc_mean + void_frac

            # BTLIAD
            n = step + 2
            P = n ** 2.111
            F = 1.111 * n
            M = 3.333 * n
            B = 0.111 * n
            E_bt = 9.999 * n
            V = P * (F_prev * M_prev + B_prev * E_prev)
            F_prev, M_prev, B_prev, E_prev = F, M, B, E_bt

            print(f"{tube_type.capitalize()} Step {step}: ε={epsilon:.5f}, E={E_total:.2f}, D≈{D:.4f}, Ø⁰={O0:.4f}, V={V:.4f}")

            epsilons.append(epsilon)
            ds.append(D)
            o0s.append(O0)

            epsilon *= decay_factor

        # Plot D (left axis)
        ax1.plot(epsilons, ds, marker='o', label=tube_type)
        # Plot Ø⁰ (right axis)
        ax2.plot(epsilons, o0s, marker='x', linestyle='--', label=tube_type)

        # Final classification
        final_D = ds[-1]
        final_O0 = o0s[-1]
        if final_O0 > 1.2 and final_D < 0.4:
            status = "Collapse (high void echo + low D)"
        elif 0.6 < final_O0 <= 1.2 and 0.4 <= final_D <= 1.0:
            status = "Balanced"
        else:
            status = "Chaotic / Other"

        results_table.append([tube_type, f"{final_D:.4f}", f"{final_O0:.4f}", status])

    # Finalize plots
    ax1.invert_xaxis()
    ax1.set_xlabel("ε (Tube Thickness)")
    ax1.set_ylabel("Dimension Proxy D")
    ax1.grid(True)
    ax1.legend(title="D curves")

    ax2.invert_xaxis()
    ax2.set_xlabel("ε (Tube Thickness)")
    ax2.set_ylabel("Echo-Residue Ø⁰")
    ax2.grid(True)
    ax2.legend(title="Ø⁰ curves")

    plt.tight_layout()
    plt.show()

    # Stability Crown Table (plain print, no tabulate)
    print("\nStability Crown Table (Final ε ≈ 0.00649)")
    print("-" * 70)
    print(f"{'Family':<12} {'Final D':<12} {'Final Ø⁰':<12} {'Classification'}")
    print("-" * 70)
    for row in results_table:
        family, final_d, final_o0, status = row
        print(f"{family:<12} {final_d:<12} {final_o0:<12} {status}")
    print("-" * 70)

    pause()

# ============================================================
# SECTOR 16 — High-Curvature Collapse Probe (v2.0 - Fixed & Upgraded)
# ============================================================
def sector_16_high_curvature_collapse(realizations=20, steps=12, N=200, epsilon_start=0.05, grid_size=50000):
    import numpy as np
    import matplotlib.pyplot as plt
    import time

    print("\n" + "="*70)
    print(" SECTOR 16 — High-Curvature Collapse Probe (Curved tubes) - v2.0")
    print("="*70)

    # Hypothesis & opposing sub upfront
    print("\n" + "-"*80)
    print("HYPOTHESIS UNDER TEST (High-Curvature Collapse):")
    print("For curved tubes with curvature bound K ≥ 1.5,")
    print("the numerical Minkowski dimension proxy D is expected to fall")
    print("below 0.45 at ε ≤ 0.01 in >75% of realizations — indicating")
    print("faster apparent collapse than straight tubes.")
    print("\nOPPOSING SUB-HYPOTHESIS:")
    print("If % D < 0.45 ≤ 50% at high K, curvature does not significantly")
    print("accelerate dimensional collapse beyond moderate levels,")
    print("suggesting geometry-limited packing efficiency.")
    print("-"*80 + "\n")

    # Run mode toggle
    mode_input = input("Run mode [1] Single (default) [2] Brute-force loop (auto-vary): ").strip()
    brute_force = mode_input == '2'

    cycle = 0
    while True:
        cycle += 1
        if brute_force:
            print(f"\n=== Brute-Force Cycle {cycle} (N={N}, grid={grid_size}, realizations={realizations}, ε_start={epsilon_start:.4f}) ===")

        K_values = [1.0, 1.5, 2.0, 3.0]
        decay_factor = 0.75
        thresholds = [0.45, 0.40, 0.35]  # collapse threshold sweep

        all_results = {k: {'final_Ds': [], 'trajectories': [], 'decay_slopes': []} for k in K_values}
        straight_final_Ds = []  # baseline

        plt.figure(figsize=(12, 8))
        plt.suptitle(f"High-Curvature Collapse - Cycle {cycle} ({realizations} realizations)")

        # Run straight baseline first (quick, 5 realizations)
        print("Running straight-tube baseline (5 realizations)...")
        for r in range(5):
            epsilon = epsilon_start
            Ds = []
            for step in range(steps):
                current_grid = max(grid_size, int(1/epsilon) * 200)
                grid = np.random.uniform(-1, 1, (current_grid, 3))
                directions = np.random.normal(size=(N, 3))
                directions /= np.linalg.norm(directions, axis=1)[:, None]
                K_field = np.zeros(len(grid))
                for v in directions:
                    line = np.array([t * v for t in np.linspace(0, 1, 50)])
                    dists = np.min(np.linalg.norm(grid[:, None, :] - line[None, :, :], axis=2), axis=1)
                    K_field += (dists <= epsilon).astype(float)
                total = np.sum(K_field)
                if total > 0:
                    p = K_field / total
                    p_nonzero = p[p > 0]
                    H = -np.sum(p_nonzero * np.log(p_nonzero))
                    D = max(0, H / np.log(1/epsilon)) if epsilon < 1 else 0
                else:
                    D = 0.0
                Ds.append(D)
                epsilon *= decay_factor
            straight_final_Ds.append(Ds[-1])

        mean_straight = np.mean(straight_final_Ds)
        print(f"Straight baseline mean D = {mean_straight:.4f}")

        for K in K_values:
            print(f"\n--- Curvature K = {K} ---")
            final_D_list = []
            all_trajectories = []  # list of (steps,) arrays per realization

            for r in range(realizations):
                print(f"  Realization {r+1}/{realizations}", end=" ... ")
                epsilon = epsilon_start
                Ds = []
                for step in range(steps):
                    current_grid = max(grid_size, int(1/epsilon) * 200)
                    grid = np.random.uniform(-1, 1, (current_grid, 3))
                    directions = np.random.normal(size=(N, 3))
                    directions /= np.linalg.norm(directions, axis=1)[:, None]

                    K_field = np.zeros(len(grid))
                    for v in directions:
                        curve = random_curve(v, curvature=K)
                        dists = np.min(np.linalg.norm(grid[:, None, :] - curve[None, :, :], axis=2), axis=1)
                        K_field += (dists <= epsilon).astype(float)

                    total = np.sum(K_field)
                    if total > 0:
                        p = K_field / total
                        p_nonzero = p[p > 0]
                        H = -np.sum(p_nonzero * np.log(p_nonzero))
                        D = max(0, H / np.log(1/epsilon)) if epsilon < 1 else 0
                    else:
                        D = 0.0

                    Ds.append(D)
                    epsilon *= decay_factor

                final_D_list.append(Ds[-1])
                all_trajectories.append(np.array(Ds))
                print(f"final D = {Ds[-1]:.4f}")

                if r == 0:
                    avg_eps = [epsilon_start * (decay_factor ** i) for i in range(steps)]

            # Average trajectory for plotting
            avg_Ds = np.mean(all_trajectories, axis=0)  # shape = (steps,)
            plt.plot(avg_eps, avg_Ds, marker='o', label=f"K={K}")

            mean_final_D = np.mean(final_D_list)
            std_final_D = np.std(final_D_list)
            below_045 = np.mean(np.array(final_D_list) < 0.45) * 100

            # Adjusted slope (mid-range only)
            valid_mask = (avg_Ds > 0.01) & (np.array(avg_eps) < 0.1)
            slope = 0.0
            if np.sum(valid_mask) >= 3:
                valid_eps = np.array(avg_eps)[valid_mask]
                valid_D = avg_Ds[valid_mask]
                log_eps = np.log(valid_eps)
                log_D = np.log(valid_D + 1e-10)
                slope = np.polyfit(log_eps, log_D, 1)[0]

            all_results[K]['final_Ds'] = final_D_list
            all_results[K]['decay_slopes'].append(slope)

        plt.gca().invert_xaxis()
        plt.xlabel("ε (Tube Thickness)")
        plt.ylabel("Avg Dimension Proxy D")
        plt.grid(True)
        plt.legend()
        plt.show()

        # Summary table
        print("\nHigh-Curvature Collapse Summary ({} realizations)".format(realizations))
        print("-" * 100)
        print(f"{'K':<6} {'Mean D ± std':<18} {'% <0.45':<10} {'% <0.40':<10} {'% <0.35':<10} {'Adj. slope':<12}")
        print("-" * 100)
        high_k_below = []
        for K in K_values:
            Ds = all_results[K]['final_Ds']
            mean_d = np.mean(Ds)
            std_d = np.std(Ds)
            pct_045 = np.mean(np.array(Ds) < 0.45) * 100
            pct_040 = np.mean(np.array(Ds) < 0.40) * 100
            pct_035 = np.mean(np.array(Ds) < 0.35) * 100
            slope = all_results[K]['decay_slopes'][0] if all_results[K]['decay_slopes'] else 0.0
            print(f"{K:<6} {mean_d:.4f} ± {std_d:.4f} {pct_045:<10.1f} {pct_040:<10.1f} {pct_035:<10.1f} {slope:<12.3f}")
            if K >= 1.5:
                high_k_below.append(pct_045)
        print("-" * 100)
        overall_high_k = np.mean(high_k_below) if high_k_below else 0
        print(f"Overall % D < 0.45 for K ≥ 1.5: {overall_high_k:.1f}%")
        if overall_high_k > 75:
            print("STRONG EVIDENCE: Hypothesis supported (>75% collapse rate at high K)")
        elif overall_high_k > 50:
            print("MODERATE EVIDENCE: Hypothesis partially supported")
        else:
            print("WEAK EVIDENCE: Hypothesis not strongly supported")
            print("OPPOSING SUB-HYPOTHESIS WINS: Curvature does not significantly accelerate collapse")

        if not brute_force:
            pause()
            break

        # Brute-force next cycle
        print("\nCycle {} complete. Next cycle starts in 10 seconds... (Ctrl+C to stop)".format(cycle))
        try:
            for i in range(10, 0, -1):
                print(f"{i} ", end="", flush=True)
                time.sleep(1)
            print("\nStarting next cycle...")
        except KeyboardInterrupt:
            print("\nInterrupted! Exiting brute-force.")
            pause()
            break

        # Mutate params
        N = int(N * 1.1)
        grid_size = int(grid_size * 1.2)
        realizations = min(realizations + 5, 50)
        epsilon_start *= 0.95
# ============================================================
# SECTOR 17 — RN-Bias Reduction Quantifier (v2.0 - Fixed KDTree Query Direction)
# ============================================================
def sector_17_rn_bias_reduction(realizations=20, steps=12, N=200, epsilon_start=0.05, grid_size=50000):
    import numpy as np
    import matplotlib.pyplot as plt
    import time
    from scipy.spatial import cKDTree

    print("\n" + "="*70)
    print(" SECTOR 17 — RN-Bias Reduction Quantifier (Uniform vs RN) - v2.0")
    print("="*70)

    # Hypothesis & opposing sub
    print("\n" + "-"*80)
    print("HYPOTHESIS UNDER TEST (RN-Bias Reduction):")
    print("RN-biased directional clustering reduces the final dimension proxy D")
    print("by 0.10–0.25 on average compared to uniform sampling across all families —")
    print("suggesting directional anisotropy may enable more efficient packing")
    print("and sub-3 dimensional Kakeya-like sets.")
    print("\nOPPOSING SUB-HYPOTHESIS:")
    print("If mean ΔD ≤ 0.05 or RN D higher than uniform in >50% of realizations,")
    print("then RN-bias does not significantly reduce effective dimension,")
    print("indicating directional clustering may not improve packing efficiency")
    print("or could even increase apparent dimension.")
    print("-"*80 + "\n")

    # Brute-force mode toggle
    mode_input = input("Run mode [1] Single (default) [2] Brute-force loop (auto-vary params): ").strip()
    brute_force = mode_input == '2'

    cycle = 0
    while True:
        cycle += 1
        if brute_force:
            print(f"\n=== Brute-Force Cycle {cycle} (N={N}, grid={grid_size}, realizations={realizations}, ε_start={epsilon_start:.4f}) ===")

        tube_types = ['straight', 'polygonal', 'curved', 'branching']
        modes = ['uniform', 'rn_biased']
        decay_factor = 0.75
        thresholds = [0.45, 0.40, 0.35]

        results = {t: {m: [] for m in modes} for t in tube_types}

        plt.figure(figsize=(12, 8))
        plt.suptitle(f"RN-Bias Effect - Cycle {cycle} ({realizations} realizations per mode)")

        # Reuse grid across all steps and modes (but we build curve_tree per curve)
        max_grid = max(grid_size, int(1/epsilon_start) * 200)
        grid = np.random.uniform(-1, 1, (max_grid, 3))

        for tube_type in tube_types:
            print(f"\n=== {tube_type.capitalize()} ===")
            for mode in modes:
                print(f"  Mode: {mode.upper()}")
                final_D_list = []
                avg_eps = []
                avg_Ds = np.zeros(steps)
                std_Ds = np.zeros(steps)

                for r in range(realizations):
                    print(f"    Realization {r+1}/{realizations}", end=" ... ")
                    epsilon = epsilon_start
                    Ds = []

                    for step in range(steps):
                        if mode == 'rn_biased':
                            rn_weights = [rn(i) for i in range(1, N+1)]
                            rn_probs = np.array(rn_weights) / sum(rn_weights)
                            indices = np.random.choice(np.arange(N), size=N, p=rn_probs)
                            directions = np.random.normal(size=(N, 3))[indices]
                            directions /= np.linalg.norm(directions, axis=1)[:, None] + 1e-10
                        else:
                            directions = np.random.normal(size=(N, 3))
                            directions /= np.linalg.norm(directions, axis=1)[:, None]

                        K = np.zeros(len(grid))
                        for v in directions:
                            if tube_type == 'straight':
                                curve = np.array([t * v for t in np.linspace(0, 1, 50)])
                            elif tube_type == 'polygonal':
                                curve = np.array([t * v for t in np.linspace(0, 1, 50)])
                                # Placeholder - replace with polygon_norm_dist when ready
                            elif tube_type == 'curved':
                                curve = random_curve(v, curvature=1.5)
                            elif tube_type == 'branching':
                                branches = generate_branch(v, depth=3)
                                curve = np.vstack(branches) if branches else np.array([t * v for t in np.linspace(0, 1, 50)])

                            # FIXED: build tree on curve points, query grid against it
                            curve_tree = cKDTree(curve)
                            min_dists, _ = curve_tree.query(grid)  # shape = (len(grid),)
                            K += (min_dists <= epsilon).astype(float)

                        total = np.sum(K)
                        if total > 0:
                            p = K / total
                            p_nonzero = p[p > 0]
                            H = -np.sum(p_nonzero * np.log(p_nonzero))
                            D = max(0, H / np.log(1/epsilon)) if epsilon < 1 else 0
                        else:
                            D = 0.0

                        Ds.append(D)
                        epsilon *= decay_factor

                    final_D_list.append(Ds[-1])
                    print(f"final D = {Ds[-1]:.4f}")

                    if r == 0:
                        avg_eps = [epsilon_start * (decay_factor ** i) for i in range(steps)]
                    avg_Ds += np.array(Ds)
                    std_Ds += np.array(Ds)**2

                avg_Ds /= realizations
                std_Ds = np.sqrt(std_Ds / realizations - avg_Ds**2)

                plt.plot(avg_eps, avg_Ds, marker='o' if mode == 'uniform' else 'x',
                         linestyle='-' if mode == 'uniform' else '--',
                         label=f"{tube_type} {mode}")

                mean_final_D = np.mean(final_D_list)
                std_final_D = np.std(final_D_list)
                results[tube_type][mode] = final_D_list

                print(f"    → Mean final D = {mean_final_D:.4f} ± {std_final_D:.4f}")

        plt.gca().invert_xaxis()
        plt.xlabel("ε (Tube Thickness)")
        plt.ylabel("Avg Dimension Proxy D")
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

        # Delta table + verdict
        print("\nRN-Bias Reduction Summary (ΔD = D_uniform - D_RN)")
        print("-" * 100)
        print(f"{'Family':<12} {'Mean D_uniform':<18} {'Mean D_RN':<18} {'Mean ΔD':<12} {'% RN lower':<12}")
        print("-" * 100)
        deltas = []
        pct_lowers = []
        for t in tube_types:
            d_uni = results[t]['uniform']
            d_rn = results[t]['rn_biased']
            mean_uni = np.mean(d_uni)
            mean_rn = np.mean(d_rn)
            delta = mean_uni - mean_rn
            pct_lower = np.mean(np.array(d_rn) < np.array(d_uni)) * 100
            print(f"{t:<12} {mean_uni:.4f} ± {np.std(d_uni):.4f} {mean_rn:.4f} ± {np.std(d_rn):.4f} {delta:<12.4f} {pct_lower:<12.1f}")
            deltas.append(delta)
            pct_lowers.append(pct_lower)
        print("-" * 100)
        avg_delta = np.mean(deltas)
        avg_pct_lower = np.mean(pct_lowers)
        print(f"Overall mean ΔD: {avg_delta:.4f}")
        print(f"Overall % runs RN lower: {avg_pct_lower:.1f}%")
        if avg_delta > 0.10 and avg_pct_lower > 70:
            print("STRONG EVIDENCE: Hypothesis supported (RN reduces D significantly)")
        elif avg_delta > 0.05 and avg_pct_lower > 55:
            print("MODERATE EVIDENCE: Hypothesis partially supported")
        else:
            print("WEAK EVIDENCE: Hypothesis not strongly supported")
            print("OPPOSING SUB-HYPOTHESIS WINS: RN-bias does not significantly reduce dimension")

        if not brute_force:
            pause()
            break

        # Brute-force next cycle
        print("\nCycle {} complete. Next cycle starts in 10 seconds... (Ctrl+C to stop)".format(cycle))
        try:
            for i in range(10, 0, -1):
                print(f"{i} ", end="", flush=True)
                time.sleep(1)
            print("\nStarting next cycle...")
        except KeyboardInterrupt:
            print("\nInterrupted! Exiting brute-force.")
            pause()
            break

        # Mutate params
        N = int(N * 1.1)
        grid_size = int(grid_size * 1.2)
        realizations = min(realizations + 5, 50)
        epsilon_start *= 0.95


# ============================================================
# SECTOR 18 — Branching Depth Efficiency Hammer (v2.0)
# ============================================================
def sector_18_branching_depth_hammer(realizations=20, steps=12, N=200, epsilon_start=0.05, grid_size=50000):
    import numpy as np
    import matplotlib.pyplot as plt
    import time

    print("\n" + "="*70)
    print(" SECTOR 18 — Branching Depth Efficiency Hammer - v2.0")
    print("="*70)

    # Hypothesis & opposing sub upfront
    print("\n" + "-"*80)
    print("HYPOTHESIS UNDER TEST (Branching Depth Efficiency):")
    print("Branching tubes with depth ≥ 3 produce the lowest average final D proxy")
    print("among all families (frequently < 0.35 at ε ≈ 0.005 in >75% of realizations),")
    print("potentially indicating near-logarithmic packing efficiency in hierarchical")
    print("tube structures.")
    print("\nOPPOSING SUB-HYPOTHESIS:")
    print("If mean D for depth ≥ 3 is not the lowest or % D < 0.35 ≤ 50%,")
    print("then higher branching depth does not lower effective dimension,")
    print("suggesting hierarchical structures may saturate or increase D due to")
    print("redundancy in branching.")
    print("-"*80 + "\n")

    # Run mode toggle
    mode_input = input("Run mode [1] Single (default) [2] Brute-force loop (auto-vary): ").strip()
    brute_force = mode_input == '2'

    cycle = 0
    while True:
        cycle += 1
        if brute_force:
            print(f"\n=== Brute-Force Cycle {cycle} (N={N}, grid={grid_size}, realizations={realizations}, ε_start={epsilon_start:.4f}) ===")

        depths = [1, 2, 3, 4, 5]
        decay_factor = 0.75
        thresholds = [0.35, 0.30, 0.25]

        all_results = {d: {'final_Ds': [], 'trajectories': [], 'decay_slopes': []} for d in depths}
        straight_final_Ds = []  # baseline

        plt.figure(figsize=(10, 6))
        plt.title(f"Branching Depth Efficiency - Cycle {cycle} ({realizations} realizations)")

        # Straight baseline (5 realizations)
        print("Running straight-tube baseline (5 realizations)...")
        for r in range(5):
            epsilon = epsilon_start
            Ds = []
            for step in range(steps):
                current_grid = max(grid_size, int(1/epsilon) * 200)
                grid = np.random.uniform(-1, 1, (current_grid, 3))
                directions = np.random.normal(size=(N, 3))
                directions /= np.linalg.norm(directions, axis=1)[:, None]
                K_field = np.zeros(len(grid))
                for v in directions:
                    line = np.array([t * v for t in np.linspace(0, 1, 50)])
                    dists = np.min(np.linalg.norm(grid[:, None, :] - line[None, :, :], axis=2), axis=1)
                    K_field += (dists <= epsilon).astype(float)
                total = np.sum(K_field)
                if total > 0:
                    p = K_field / total
                    p_nonzero = p[p > 0]
                    H = -np.sum(p_nonzero * np.log(p_nonzero))
                    D = max(0, H / np.log(1/epsilon)) if epsilon < 1 else 0
                else:
                    D = 0.0
                Ds.append(D)
                epsilon *= decay_factor
            straight_final_Ds.append(Ds[-1])

        mean_straight = np.mean(straight_final_Ds)
        print(f"Straight baseline mean D = {mean_straight:.4f}")

        for depth in depths:
            print(f"\n--- Branch Depth = {depth} ---")
            final_D_list = []
            all_trajectories = []

            for r in range(realizations):
                print(f"  Realization {r+1}/{realizations}", end=" ... ")
                epsilon = epsilon_start
                Ds = []

                for step in range(steps):
                    current_grid = max(grid_size, int(1/epsilon) * 200)
                    grid = np.random.uniform(-1, 1, (current_grid, 3))
                    directions = np.random.normal(size=(N, 3))
                    directions /= np.linalg.norm(directions, axis=1)[:, None]

                    K_field = np.zeros(len(grid))
                    for v in directions:
                        branches = generate_branch(v, depth=depth)
                        curve = np.vstack(branches) if branches else np.array([t * v for t in np.linspace(0, 1, 50)])
                        dists = np.min(np.linalg.norm(grid[:, None, :] - curve[None, :, :], axis=2), axis=1)
                        K_field += (dists <= epsilon).astype(float)

                    total = np.sum(K_field)
                    if total > 0:
                        p = K_field / total
                        p_nonzero = p[p > 0]
                        H = -np.sum(p_nonzero * np.log(p_nonzero))
                        D = max(0, H / np.log(1/epsilon)) if epsilon < 1 else 0
                    else:
                        D = 0.0

                    Ds.append(D)
                    epsilon *= decay_factor

                final_D_list.append(Ds[-1])
                all_trajectories.append(np.array(Ds))
                print(f"final D = {Ds[-1]:.4f}")

                if r == 0:
                    avg_eps = [epsilon_start * (decay_factor ** i) for i in range(steps)]

            # Average trajectory
            avg_Ds = np.mean(all_trajectories, axis=0)
            plt.plot(avg_eps, avg_Ds, marker='o', label=f"depth={depth}")
            plt.fill_between(avg_eps, avg_Ds - np.std(all_trajectories, axis=0), avg_Ds + np.std(all_trajectories, axis=0), alpha=0.15)

            mean_final_D = np.mean(final_D_list)
            std_final_D = np.std(final_D_list)
            pct_035 = np.mean(np.array(final_D_list) < 0.35) * 100

            # Adjusted slope (mid-range)
            valid_mask = (avg_Ds > 0.01) & (np.array(avg_eps) < 0.1)
            slope = 0.0
            if np.sum(valid_mask) >= 3:
                valid_eps = np.array(avg_eps)[valid_mask]
                valid_D = avg_Ds[valid_mask]
                log_eps = np.log(valid_eps)
                log_D = np.log(valid_D + 1e-10)
                slope = np.polyfit(log_eps, log_D, 1)[0]

            all_results[depth]['final_Ds'] = final_D_list
            all_results[depth]['decay_slopes'].append(slope)

            print(f"  → Mean final D = {mean_final_D:.4f} ± {std_final_D:.4f}")
            print(f"  → % realizations with D < 0.35 = {pct_035:.1f}%")
            print(f"  → Adjusted late decay slope ≈ {slope:.3f}")

        plt.gca().invert_xaxis()
        plt.xlabel("ε (Tube Thickness)")
        plt.ylabel("Avg Dimension Proxy D")
        plt.grid(True)
        plt.legend()
        plt.show()

        # Summary table + verdict
        print("\nBranching Depth Efficiency Summary ({} realizations)".format(realizations))
        print("-" * 100)
        print(f"{'Depth':<8} {'Mean D ± std':<18} {'% <0.35':<10} {'% <0.30':<10} {'% <0.25':<10} {'Adj. slope':<12}")
        print("-" * 100)
        high_depth_below = []
        for depth in depths:
            Ds = all_results[depth]['final_Ds']
            mean_d = np.mean(Ds)
            std_d = np.std(Ds)
            pct_035 = np.mean(np.array(Ds) < 0.35) * 100
            pct_030 = np.mean(np.array(Ds) < 0.30) * 100
            pct_025 = np.mean(np.array(Ds) < 0.25) * 100
            slope = all_results[depth]['decay_slopes'][0] if all_results[depth]['decay_slopes'] else 0.0
            print(f"{depth:<8} {mean_d:.4f} ± {std_d:.4f} {pct_035:<10.1f} {pct_030:<10.1f} {pct_025:<10.1f} {slope:<12.3f}")
            if depth >= 3:
                high_depth_below.append(pct_035)
        print("-" * 100)
        overall_high_depth = np.mean(high_depth_below) if high_depth_below else 0
        print(f"Overall % D < 0.35 for depth ≥ 3: {overall_high_depth:.1f}%")
        if overall_high_depth > 75:
            print("STRONG EVIDENCE: Hypothesis supported (deep branching drives low D)")
        elif overall_high_depth > 50:
            print("MODERATE EVIDENCE: Hypothesis partially supported")
        else:
            print("WEAK EVIDENCE: Hypothesis not strongly supported")
            print("OPPOSING SUB-HYPOTHESIS WINS: Higher branching does not lower dimension significantly")

        if not brute_force:
            pause()
            break

        # Brute-force next cycle
        print("\nCycle {} complete. Next cycle starts in 10 seconds... (Ctrl+C to stop)".format(cycle))
        try:
            for i in range(10, 0, -1):
                print(f"{i} ", end="", flush=True)
                time.sleep(1)
            print("\nStarting next cycle...")
        except KeyboardInterrupt:
            print("\nInterrupted! Exiting brute-force.")
            pause()
            break

        # Mutate params
        N = int(N * 1.1)
        grid_size = int(grid_size * 1.2)
        realizations = min(realizations + 5, 50)
        epsilon_start *= 0.95

# ============================================================
# SECTOR 19 — Hybrid Synergy Probe (v2.1 - Crash-Fixed)
# ============================================================
def sector_19_hybrid_synergy_probe(realizations=20, steps=12, N=50, epsilon_start=0.1, grid_size=3000):
    import numpy as np
    import matplotlib.pyplot as plt
    import time

    print("\n" + "="*70)
    print(" SECTOR 19 — Hybrid Synergy Probe (RN + Curved + Branching) - v2.1 Crash-Fixed")
    print("="*70)

    families = ['straight', 'curved', 'branching', 'hybrid']

    decay_factor = 0.75
    min_epsilon = 0.01
    curve_points = 25

    # Brute-force toggle
    mode_input = input("Run mode [1] Single [2] Brute-force: ").strip()
    brute_force = mode_input == '2'

    cycle = 0
    while True:
        cycle += 1
        print(f"\n=== Cycle {cycle} (N={N}, grid={grid_size}, realizations={realizations}, ε_start={epsilon_start}) ===")

        # Recompute RN bias for current N (fixes size mismatch)
        rn_weights = np.array([rn(i) for i in range(1, N+1)])
        rn_probs = rn_weights / rn_weights.sum()

        results = {f: [] for f in families}
        trajectories = {f: [] for f in families}

        max_grid = max(grid_size, int(1/epsilon_start) * 200)
        grid = np.random.uniform(-1, 1, (max_grid, 3))

        for r in range(realizations):
            print(f"  Realization {r+1}/{realizations} started", end=" ... ")

            epsilon = epsilon_start
            eps_traj = []
            Ds = {f: [] for f in families}

            for step in range(steps):
                eps_traj.append(epsilon)

                indices = np.random.choice(np.arange(N), size=N, p=rn_probs)
                directions = np.random.normal(size=(N, 3))[indices]
                directions /= np.linalg.norm(directions, axis=1)[:, None] + 1e-10

                for family in families:
                    K_field = np.zeros(len(grid))

                    for v in directions:
                        if family == 'straight':
                            curve = np.array([t * v for t in np.linspace(0, 1, curve_points)])
                        elif family == 'curved':
                            curve = random_curve(v, curvature=1.5)
                        elif family == 'branching':
                            branches = generate_branch(v, depth=3)
                            curve = np.vstack(branches) if branches else np.array([t * v for t in np.linspace(0, 1, curve_points)])
                        elif family == 'hybrid':
                            spine = random_curve(v, curvature=1.5)
                            full_structure = [spine]
                            branch_points = [int(i) for i in np.linspace(5, len(spine)-5, 3)]
                            for i in branch_points:
                                pos = spine[i]
                                local_dir = spine[i] - spine[max(0, i-1)]
                                local_dir /= np.linalg.norm(local_dir) + 1e-10
                                branches = generate_branch(local_dir, depth=2)[:10]  # cap
                                full_structure.extend([b + pos for b in branches])
                            curve = np.vstack(full_structure)

                        diff = grid[:, None, :] - curve[None, :, :]
                        d2 = np.sum(diff * diff, axis=2)
                        mind2 = np.min(d2, axis=1)
                        K_field += (mind2 <= epsilon**2)

                    total = np.sum(K_field)
                    if total > 0:
                        p = K_field / total
                        p = p[p > 0]
                        H = -np.sum(p * np.log(p))
                        denom = np.log(1/epsilon) + 1e-12
                        D = max(0, H / denom)
                    else:
                        D = 0.0

                    Ds[family].append(D)

                epsilon = max(epsilon * decay_factor, min_epsilon)

            for f in families:
                results[f].append(Ds[f][-1])
                trajectories[f].append(Ds[f])

            print("done")

        # Plot & summary (same as before)
        plt.figure(figsize=(10, 6))
        for f in families:
            traj = np.mean(trajectories[f], axis=0)
            plt.plot(eps_traj, traj, marker='o', label=f)

        plt.gca().invert_xaxis()
        plt.xlabel("ε")
        plt.ylabel("D")
        plt.title("Hybrid Synergy vs Baselines")
        plt.grid(True)
        plt.legend()
        plt.show()

        print("\nHybrid Synergy Summary")
        print("-"*90)
        print(f"{'Family':<12} {'Mean D':<10} {'Std D':<10} {'% D < 0.35':<10}")
        print("-"*90)

        best_single = float('inf')
        for f in families:
            arr = np.array(results[f])
            mean_d = arr.mean()
            std_d = arr.std()
            pct_low = np.mean(arr < 0.35)*100
            print(f"{f:<12} {mean_d:<10.4f} {std_d:<10.4f} {pct_low:<10.1f}")
            if f != 'hybrid' and mean_d < best_single:
                best_single = mean_d

        print("-"*90)

        hybrid_mean = np.mean(results['hybrid'])
        delta = hybrid_mean - best_single
        if delta < -0.05:
            print("STRONG EVIDENCE: Hybrid beats best single mechanism")
        elif delta < -0.02:
            print("MODERATE EVIDENCE: Hybrid partially better")
        else:
            print("WEAK EVIDENCE: No clear synergy")
            print("OPPOSING SUB-HYPOTHESIS WINS: Hybrid does not outperform individual mechanisms")

        if not brute_force:
            pause()
            break

        print("\nCycle complete. Next in 10s (Ctrl+C to exit)...")
        time.sleep(10)
        N = int(N * 1.1)
        grid_size = int(grid_size * 1.2)
        realizations = min(realizations + 5, 50)
        epsilon_start *= 0.95

# ============================================================
# SECTOR 20 — Adaptive Coverage Avoidance System (v2.1 - Final Polished)
# ============================================================
def sector_20_adaptive_coverage_avoidance(realizations=20, steps=12, N_candidates=50, N_selected=10, epsilon_start=0.05, grid_size=50000):
    import numpy as np
    import matplotlib.pyplot as plt
    import time

    print("\n" + "="*70)
    print(" SECTOR 20 — Adaptive Coverage Avoidance System - v2.1 Final")
    print("="*70)

    # Hypothesis & opposing sub
    print("\n" + "-"*80)
    print("HYPOTHESIS UNDER TEST (Adaptive Avoidance):")
    print("Adaptive tubes that minimize overlap with existing coverage produce")
    print("lower D than random placement, suggesting self-organizing systems")
    print("approximate efficient Kakeya packings.")
    print("\nOPPOSING SUB-HYPOTHESIS:")
    print("If adaptive D is not significantly lower than random placement,")
    print("then overlap avoidance does not improve packing efficiency in finite approximations.")
    print("-"*80 + "\n")

    decay_factor = 0.75
    min_epsilon = 0.01

    final_D_adaptive = []
    final_D_random = []

    plt.figure(figsize=(12, 8))
    plt.suptitle("Adaptive vs Random Placement Comparison")

    for r in range(realizations):
        print(f"  Realization {r+1}/{realizations}", end=" ... ")

        # Fixed grid per realization
        max_grid = max(grid_size, int(1/epsilon_start) * 200)
        grid = np.random.uniform(-1, 1, (max_grid, 3))

        # ----------------------------------------------------
        # Random baseline — accumulates coverage
        # ----------------------------------------------------
        epsilon = epsilon_start
        Ds_random = []
        coverage_random = np.zeros(len(grid))
        for step in range(steps):
            directions = np.random.normal(size=(N_selected, 3))
            directions /= np.linalg.norm(directions, axis=1)[:, None]
            K = np.zeros(len(grid))
            for v in directions:
                curve = random_curve(v, curvature=1.5)
                diff = grid[:, None, :] - curve[None, :, :]
                d2 = np.sum(diff * diff, axis=2)
                mind2 = np.min(d2, axis=1)
                K += (mind2 <= epsilon**2)
            coverage_random += K
            total = np.sum(coverage_random)
            if total > 0:
                p = coverage_random / total
                p_nonzero = p[p > 0]
                H = -np.sum(p_nonzero * np.log(p_nonzero))
                denom = np.log(1/epsilon) + 1e-12
                D = max(0, H / denom)
            else:
                D = 0.0
            Ds_random.append(D)
            epsilon = max(epsilon * decay_factor, min_epsilon)

        final_D_random.append(Ds_random[-1])

        # ----------------------------------------------------
        # Adaptive run — true sequential greedy
        # ----------------------------------------------------
        epsilon = epsilon_start
        Ds_adaptive = []
        coverage = np.zeros(len(grid))

        for step in range(steps):
            print(f"    Step {step+1}/{steps} ε={epsilon:.4f}", end="\r")
            for _ in range(N_selected):
                best_overlap = float('inf')
                best_K_add = None

                for _ in range(N_candidates):
                    v = np.random.normal(size=3)
                    v /= np.linalg.norm(v)
                    candidate_curve = random_curve(v, curvature=1.5)
                    diff = grid[:, None, :] - candidate_curve[None, :, :]
                    d2 = np.sum(diff * diff, axis=2)
                    mind2 = np.min(d2, axis=1)
                    candidate_K = (mind2 <= epsilon**2).astype(float)

                    overlap = np.sum(candidate_K * coverage)
                    if overlap < best_overlap:
                        best_overlap = overlap
                        best_K_add = candidate_K

                if best_K_add is not None:
                    coverage += best_K_add

            total = np.sum(coverage)
            if total > 0:
                p = coverage / total
                p_nonzero = p[p > 0]
                H = -np.sum(p_nonzero * np.log(p_nonzero))
                denom = np.log(1/epsilon) + 1e-12
                D = max(0, H / denom)
            else:
                D = 0.0

            Ds_adaptive.append(D)
            epsilon = max(epsilon * decay_factor, min_epsilon)

        final_D_adaptive.append(Ds_adaptive[-1])

        delta_r = Ds_random[-1] - Ds_adaptive[-1]
        print(f"adaptive D = {Ds_adaptive[-1]:.4f}, random D = {Ds_random[-1]:.4f}, ΔD = {delta_r:.4f}")

    # Summary & plot
    mean_adaptive = np.mean(final_D_adaptive)
    mean_random = np.mean(final_D_random)
    delta = mean_random - mean_adaptive
    pct_adaptive_lower = np.mean(np.array(final_D_adaptive) < np.array(final_D_random)) * 100
    pct_low_adaptive = np.mean(np.array(final_D_adaptive) < 0.35) * 100
    pct_low_random = np.mean(np.array(final_D_random) < 0.35) * 100
    noise_floor = (np.std(final_D_adaptive) + np.std(final_D_random)) / 2

    print("\nAdaptive vs Random Summary")
    print("-" * 100)
    print(f"Mean D (Adaptive): {mean_adaptive:.4f}")
    print(f"Mean D (Random):   {mean_random:.4f}")
    print(f"ΔD (Random - Adaptive): {delta:.4f}")
    print(f"Noise floor ≈ {noise_floor:.4f}")
    print(f"% runs Adaptive lower: {pct_adaptive_lower:.1f}%")
    print(f"% D < 0.35 (Adaptive): {pct_low_adaptive:.1f}%")
    print(f"% D < 0.35 (Random):   {pct_low_random:.1f}%")
    print("-" * 100)

    if abs(delta) < noise_floor:
        print("ΔD within noise floor — difference statistically insignificant")
        print("WEAK EVIDENCE: Adaptive and random are indistinguishable in this regime")
    elif delta > 0.10 and pct_adaptive_lower > 70:
        print("STRONG EVIDENCE: Adaptive placement reduces D significantly")
    elif delta > 0.05:
        print("MODERATE EVIDENCE: Adaptive placement partially reduces D")
    else:
        print("WEAK EVIDENCE: No significant advantage from adaptive placement")
        print("OPPOSING SUB-HYPOTHESIS WINS: Overlap avoidance does not improve packing")

    print("\nINTERPRETATION: In this regime, greedy overlap-avoidance tends to increase D,")
    print("suggesting that 'even coverage' is entropically expensive and not Kakeya-efficient.")

    pause()


# ============================================================
# SECTOR 21 — Directional Coverage Balancer (v1.1 - Final)
# ============================================================
def sector_21_directional_coverage_balancer(realizations=20, steps=12, N_candidates=50, N_selected=10, epsilon_start=0.05, grid_size=50000):
    import numpy as np
    import matplotlib.pyplot as plt
    import time

    print("\n" + "="*70)
    print(" SECTOR 21 — Directional Coverage Balancer (v1.1 - Final)")
    print("="*70)

    # Hypothesis & opposing sub
    print("\n" + "-"*80)
    print("HYPOTHESIS UNDER TEST (Directional Coverage):")
    print("Optimizing for even directional distribution on the sphere (max min angular separation)")
    print("produces lower mean D than random placement,")
    print("suggesting direction uniformity is key to efficient Kakeya-like packings.")
    print("\nOPPOSING SUB-HYPOTHESIS:")
    print("If directional balancing does not reduce D significantly,")
    print("then direction uniformity is not the dominant factor in finite approximations.")
    print("-"*80 + "\n")

    decay_factor = 0.75
    min_epsilon = 0.01

    final_D_balanced = []
    final_D_random = []
    traj_balanced = []  # for plot
    traj_random = []

    plt.figure(figsize=(12, 8))
    plt.suptitle("Directional Balancer vs Random Placement")

    for r in range(realizations):
        print(f"  Realization {r+1}/{realizations}", end=" ... ")

        # Fixed grid per realization
        max_grid = max(grid_size, int(1/epsilon_start) * 200)
        grid = np.random.uniform(-1, 1, (max_grid, 3))

        # Track used directions (unit vectors)
        used_dirs = []

        # ----------------------------------------------------
        # Random baseline — accumulates coverage
        # ----------------------------------------------------
        epsilon = epsilon_start
        Ds_random = []
        coverage_random = np.zeros(len(grid))
        for step in range(steps):
            directions = np.random.normal(size=(N_selected, 3))
            directions /= np.linalg.norm(directions, axis=1)[:, None] + 1e-10
            K = np.zeros(len(grid))
            for v in directions:
                curve = random_curve(v, curvature=1.5)
                diff = grid[:, None, :] - curve[None, :, :]
                d2 = np.sum(diff * diff, axis=2)
                mind2 = np.min(d2, axis=1)
                K += (mind2 <= epsilon**2)
            coverage_random += K
            total = np.sum(coverage_random)
            if total > 0:
                p = coverage_random / total
                p_nonzero = p[p > 0]
                H = -np.sum(p_nonzero * np.log(p_nonzero))
                denom = np.log(1/epsilon) + 1e-12
                D = max(0, H / denom)
            else:
                D = 0.0
            Ds_random.append(D)
            epsilon = max(epsilon * decay_factor, min_epsilon)
        final_D_random.append(Ds_random[-1])
        traj_random.append(Ds_random)

        # ----------------------------------------------------
        # Balanced run — maximize min angular separation
        # ----------------------------------------------------
        epsilon = epsilon_start
        Ds_balanced = []
        coverage = np.zeros(len(grid))
        used_dirs = []

        for step in range(steps):
            print(f"    Step {step+1}/{steps} ε={epsilon:.4f}", end="\r")
            for _ in range(N_selected):
                best_score = -float('inf')
                best_v = None
                best_K_add = None

                for _ in range(N_candidates):
                    v = np.random.normal(size=3)
                    v /= np.linalg.norm(v) + 1e-10

                    # Score = min angular distance to existing directions
                    if len(used_dirs) == 0:
                        score = float('inf')
                    else:
                        cosines = np.dot(np.array(used_dirs), v)
                        min_cos = np.max(cosines)
                        min_angle = np.arccos(np.clip(min_cos, -1, 1))
                        score = min_angle  # higher = better spread

                    if score > best_score:
                        best_score = score
                        best_v = v

                        curve = random_curve(best_v, curvature=1.5)
                        diff = grid[:, None, :] - curve[None, :, :]
                        d2 = np.sum(diff * diff, axis=2)
                        mind2 = np.min(d2, axis=1)
                        best_K_add = (mind2 <= epsilon**2).astype(float)

                if best_K_add is not None:
                    coverage += best_K_add
                    used_dirs.append(best_v)

            total = np.sum(coverage)
            if total > 0:
                p = coverage / total
                p_nonzero = p[p > 0]
                H = -np.sum(p_nonzero * np.log(p_nonzero))
                denom = np.log(1/epsilon) + 1e-12
                D = max(0, H / denom)
            else:
                D = 0.0

            Ds_balanced.append(D)
            epsilon = max(epsilon * decay_factor, min_epsilon)

        final_D_balanced.append(Ds_balanced[-1])
        traj_balanced.append(Ds_balanced)

        delta_r = Ds_random[-1] - Ds_balanced[-1]
        print(f"balanced D = {Ds_balanced[-1]:.4f}, random D = {Ds_random[-1]:.4f}, ΔD = {delta_r:.4f}")

    # Summary & plot
    mean_balanced = np.mean(final_D_balanced)
    mean_random = np.mean(final_D_random)
    delta = mean_random - mean_balanced
    pct_balanced_lower = np.mean(np.array(final_D_balanced) < np.array(final_D_random)) * 100
    pct_low_balanced = np.mean(np.array(final_D_balanced) < 0.35) * 100
    pct_low_random = np.mean(np.array(final_D_random) < 0.35) * 100
    noise_floor = (np.std(final_D_balanced) + np.std(final_D_random)) / 2

    print("\nDirectional Balancer vs Random Summary")
    print("-" * 100)
    print(f"Mean D (Balanced): {mean_balanced:.4f}")
    print(f"Mean D (Random):   {mean_random:.4f}")
    print(f"ΔD (Random - Balanced): {delta:.4f}")
    print(f"Noise floor ≈ {noise_floor:.4f}")
    print(f"% runs Balanced lower: {pct_balanced_lower:.1f}%")
    print(f"% D < 0.35 (Balanced): {pct_low_balanced:.1f}%")
    print(f"% D < 0.35 (Random):   {pct_low_random:.1f}%")
    print("-" * 100)

    if abs(delta) < noise_floor:
        print("ΔD within noise floor — difference statistically insignificant")
    elif delta > 0.10 and pct_balanced_lower > 70:
        print("STRONG EVIDENCE: Directional balancing reduces D significantly")
    elif delta > 0.05:
        print("MODERATE EVIDENCE: Directional balancing partially reduces D")
    else:
        print("WEAK EVIDENCE: No significant advantage from directional balancing")
        print("OPPOSING SUB-HYPOTHESIS WINS: Direction uniformity does not improve packing")

    print("\nINTERPRETATION: If directional balancing lowers D, it suggests even sphere coverage is key to Kakeya efficiency.")
    print("If not, directional distribution may be secondary to spatial structure in finite approximations.")

    # Trajectory plot
    plt.figure(figsize=(10, 6))
    plt.plot(range(steps), np.mean(traj_random, axis=0), 'b--', label='Random')
    plt.plot(range(steps), np.mean(traj_balanced, axis=0), 'r-', label='Balanced')
    plt.xlabel("Step")
    plt.ylabel("D")
    plt.title("Trajectory Comparison")
    plt.grid(True)
    plt.legend()
    plt.show()

    pause()

# ============================================================
# SECTOR 22 — SAVE FULL TERMINAL LOG
# ============================================================
def sector_22_save_log():
    import os, datetime

    print("\n" + "="*70)
    print(" SECTOR 22 — Save Full Terminal Log")
    print("="*70)

    if not SESSION_LOG:
        print("No logged output yet — session is empty.")
        pause()
        return

    log_dir = "kncf_logs"
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"KNCF_log_{timestamp}.txt"
    filepath = os.path.join(log_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for line in SESSION_LOG:
                f.write(line + "\n")

        print(f"Log successfully saved to: {filepath}")
        print(f"Total lines saved: {len(SESSION_LOG)}")

    except Exception as e:
        print(f"Error saving log: {e}")
        print("Check folder permissions or disk space.")

    pause()



# ============================================================
# MAIN MENU 
# ============================================================
def main_menu():
    banner()

    while True:
        print("\nSelect a Sector to Run:")
        print("  [1]  KNCF Master Equation Set")
        print("  [2]  Straight Tube Simulation (Baseline)")
        print("  [3]  RN Weighting Demo")
        print("  [4]  BTLIAD Evolution Demo")
        print("  [5]  SBHFF Stability Demo")
        print("  [6]  Polygonal Tube Simulation")
        print("  [7]  Curved Tube Simulation")
        print("  [8]  Branching Tube Simulation")
        print("  [9]  Entropy & Dimension Scan")
        print("  [10] Full KNCF State Evolution")
        print("  [11] Full KNCF State BTLIAD Evolution")
        print("  [12] Full Full KNCF Full State Full BTLIAD Full Evolution")
        print("  [13] RN-Biased Multi-Family Run")
        print("  [14] Curvature & Branching Parameter Sweep")
        print("  [15] Echo-Residue Multi-Family Stability Crown")
        print("  [16] @@@ High-Curvature Collapse Probe")
        print("  [17] RN Bias Reduction Sweep")
        print("  [18] Branching Depth Hammer Test")
        print("  [19] Hybrid Synergy Probe (RN + Curved + Branching)")
        print("  [20] Adaptive Coverage Avoidance System")
        print("  [21] Sector 21 - Directional Coverage Balancer")
        print("  [22] Save Full Terminal Log - manual saves required")
        print("  [0]  Exit")
        print("-" * 60)

        choice = input("Enter choice: ").strip()

        # ----------------------------------------------------
        # BASIC SECTORS
        # ----------------------------------------------------
        if choice == "1":
            sector_1_master_equations()

        elif choice == "2":
            sector_2_straight_tubes()

        elif choice == "3":
            sector_3_rn_demo()

        elif choice == "4":
            sector_4_btliad_demo()

        elif choice == "5":
            sector_5_sbhff_demo()

        elif choice == "6":
            sector_6_polygonal_tubes()

        elif choice == "7":
            sector_7_curved_tubes()

        elif choice == "8":
            sector_8_branching_tubes()

        elif choice == "9":
            sector_9_entropy_scan()

        elif choice == "22":
            sector_22_save_log()

        # ----------------------------------------------------
        # FULL EVOLUTION (10 & 11)
        # ----------------------------------------------------
        elif choice in ["10", "11"]:
            tube_options = ['straight', 'polygonal', 'curved', 'branching']
            print("\nSelect Tube Type:")
            print("Options:", ", ".join(tube_options))

            tube_type = input("Enter tube type (default='straight'): ").strip().lower()
            if tube_type not in tube_options:
                print("Invalid or blank. Using default: 'straight'")
                tube_type = 'straight'

            steps_input = input("Enter number of steps (default=10): ").strip()
            steps = int(steps_input) if steps_input.isdigit() else 10

            N_input = input("Enter number of directions N (default=50): ").strip()
            N = int(N_input) if N_input.isdigit() else 50

            epsilon_input = input("Enter starting ε (default=0.1): ").strip()
            try:
                epsilon_start = float(epsilon_input)
            except:
                epsilon_start = 0.1

            grid_input = input("Enter grid size (default=3000): ").strip()
            grid_size = int(grid_input) if grid_input.isdigit() else 3000

            if choice == "10":
                sector_10_full_evolution(
                    tube_type=tube_type,
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )
            else:
                sector_11_full_evolution(
                    tube_type=tube_type,
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

        # ----------------------------------------------------
        # ADVANCED MULTI-RUN SECTORS (12–20)
        # ----------------------------------------------------
        elif choice in ["12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]:

            steps_input = input("Enter number of steps (default=10): ").strip()
            steps = int(steps_input) if steps_input.isdigit() else 10

            N_input = input("Enter number of directions N (default=50): ").strip()
            N = int(N_input) if N_input.isdigit() else 50

            epsilon_input = input("Enter starting ε (default=0.1): ").strip()
            try:
                epsilon_start = float(epsilon_input)
            except:
                epsilon_start = 0.1

            grid_input = input("Enter grid size (default=3000): ").strip()
            grid_size = int(grid_input) if grid_input.isdigit() else 3000

            if choice == "12":
                sector_12_full_full_evolution(
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

            elif choice == "13":
                sector_13_rn_biased_multi_family(
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

            elif choice == "14":
                sector_14_param_sweep(
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

            elif choice == "15":
                sector_15_echo_stability(
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

            elif choice == "16":
                sector_16_high_curvature_collapse(
                    realizations=20,
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

            elif choice == "17":
                sector_17_rn_bias_reduction(
                    realizations=20,
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

            elif choice == "18":
                sector_18_branching_depth_hammer(
                    realizations=20,
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

            elif choice == "19":
                sector_19_hybrid_synergy_probe(
                    realizations=20,
                    steps=steps,
                    N=N,
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

            elif choice == "20":
                sector_20_adaptive_coverage_avoidance(
                    realizations=20,
                    steps=steps,
                    N_candidates=50,   # candidates to try per step
                    N_selected=10,     # how many to actually place per step
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )
            elif choice == "21":
                sector_21_directional_coverage_balancer(
                    realizations=20,
                    steps=steps,
                    N_candidates=50,   # candidates to try per step
                    N_selected=10,     # how many to actually place per step
                    epsilon_start=epsilon_start,
                    grid_size=grid_size
                )

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------
        elif choice == "0":
            print("\nExiting KNCF Suite. The geometry persists.\n")
            sys.exit(0)

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()

# LICENSE.TXT
# Zero-Ology License v1.19310
# 0ko3maibZero-OlogyLicensev1.19310
#March 10, 2026
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
#- zer00logy_coreV04469.py
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
#- Zero_Freeze_Hamiltonian_Lattice_Gauge_Benchmark_Suite0033.py
#- Zero_Freeze_Yang--Mills_Formula.txt
#- Zero_Freeze_Yang--Mills_Formula_Numerical_and_Computational_Study_(latax_v2_2).txt
#- Zero_Freeze_Yang--Mills_Formula_Numerical_and_Computational_Study_(Plaintext_v2_2).docx
#- grand_summary_20251102_114655_Real_SU(3)_operator.JSON
#- grand_summary_20251102_114655_Real_SU(3)_operator.CSV
#- grand_summary_20251102_114247_placeholder.JSON
#- grand_summary_20251102_114247_placeholder.CSV
#- Lie_π_Infinity_lesson.txt
#- THE_WHY_EQUATION.py
#- Study_The_Repeating_Digit_Weights_(RN)_Formula.txt
#- Repeating_Digit_Weights_(RN).py
#- Szmy_Collatz.py
#- OddPerfectTerminator_GODD.py
#- OddPerfectTerminator_Log_OG123456.zip
#- Szmy_Grok_Odd_Perfect_Proof_Nov10_2025.pdf
#- APLHA_INFIN_P_MATRIX.py
#- alpha.txt
#- alphabet_Infinity_Pool_Matrix.pdf
#- AlphaLOG.zip
#- KOPPA_GRAND_CONSTANT.PY
#- The_Koppa_Grand_Constant.docx
#- The_Koppa_Grand_Constant.txt
#- KOPPA_HETA_DIGAMMA.PY
#- KOPPA_HETA_DIGAMMA.docx
#- KOPPA_HETA_DIGAMMA.txt
#- GRAND_CONSTANT_ALGEBRA.PY
#- Grand_Constant_Algebra_Framework.docx
#- Grand_Constant_Algebra.txt
#- equal.PY
#- equal.txt
#- equalequal.PY
#- equalequal.txt
#- hodge_GCA.PY
#- hodge_GCA.txt
#- hodge_GCA.docx
#- log_hodge.zip
#- fairness_arithmetic_suite.py
#- Fairness_Arithmetic.txt
#- pap_suite.py
#- pap.txt
#- PAP.docx
#- PLAE.txt
#- PLAE_suit.py
#- PLAE.txt
#- PLAE_log.zip
#- log_pap.zip
#- daa_suite.py
#- DAA.txt
#- log_daa.zip
#- Domain_Attribute_Adjudicator.docx
#- ZRRF_suite.py
#- ZRRF_suite_log030826.txt
#- zenith.txt
#- Kakeya_Nirvana_Conjecture_Framework.txt
#- KNCF_Suite.py
#- KNCF_log_31026.txt
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