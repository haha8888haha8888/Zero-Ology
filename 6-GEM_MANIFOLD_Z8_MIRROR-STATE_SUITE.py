#6-GEM_MANIFOLD_Z8_MIRROR-STATE_SUITE.py

import math
import random

MODULUS = 8.0
MOD_LABEL = "Z8"

# --- GEOMETRY / CORE MAP -----------------------------------------------------

def rot(z, deg):
    t = math.radians(deg)
    return z * complex(math.cos(t), math.sin(t))

def mod_gaussian(z, modulus=MODULUS):
    return complex(z.real % modulus, z.imag % modulus)

def f_scaled(a, b, c, scale=1.0):
    if scale == 0.0:
        return 0.0
    return math.tanh(scale * abs((a - b) * (b - c) * (c - a)))

def si(a, b, c, scale=1.0):
    return mod_gaussian(a + b + c + f_scaled(a, b, c, scale))

def mirror_pair_z8(z):
    """
    Z8 half-modulus mirror bracket.
    For real/imag continuous states, bracket by integer floor of real coordinate.
    """
    k = int(z.real) % 8
    base = k % 4
    return (base, (base + 4) % 8)

# --- CONSTRAINT ENGINE -------------------------------------------------------

def apply_constraint(state, mode="none"):
    a, b, c = state

    if mode == "force_equal_ab":
        return (a, a, c)

    if mode == "force_conjugate_ac":
        return (a, b, complex(a.real, -a.imag))

    if mode == "force_phase120":
        return (a, rot(a, 120), rot(a, 240))

    if mode == "force_diagonal":
        return (a, a, a)

    if mode == "force_mirror_ac_z8":
        return (a, b, mod_gaussian(a + 4))

    return (a, b, c)

def next_state(state, scale=1.0, constraint="none"):
    a, b, c = apply_constraint(state, constraint)
    return apply_constraint((b, c, si(a, b, c, scale)), constraint)

def get_full_map_jacobian_6d(state, scale=1.0, eps=1e-6, constraint="none"):
    base = next_state(state, scale, constraint)
    base_coords = [
        base[0].real, base[0].imag,
        base[1].real, base[1].imag,
        base[2].real, base[2].imag
    ]

    coords = [
        state[0].real, state[0].imag,
        state[1].real, state[1].imag,
        state[2].real, state[2].imag
    ]

    J = [[0.0] * 6 for _ in range(6)]

    for col in range(6):
        shifted = coords[:]
        shifted[col] += eps

        s2 = (
            complex(shifted[0], shifted[1]),
            complex(shifted[2], shifted[3]),
            complex(shifted[4], shifted[5])
        )

        pert = next_state(s2, scale, constraint)
        pert_coords = [
            pert[0].real, pert[0].imag,
            pert[1].real, pert[1].imag,
            pert[2].real, pert[2].imag
        ]

        for row in range(6):
            J[row][col] = (pert_coords[row] - base_coords[row]) / eps

    return J

# --- CLASSIFIER --------------------------------------------------------------

def classify_spectrum_ternary(spec, threshold=1e-4):
    s = sorted(spec, reverse=True)

    pos = sum(x > threshold for x in s)
    neg = sum(x < -threshold for x in s)
    zer = 6 - pos - neg

    trace = sum(spec)
    stable_mean = sum(s[2:]) / 4
    unstable_mean = sum(s[:2]) / 2
    ratio = abs(unstable_mean / stable_mean) if abs(stable_mean) > 1e-12 else float("inf")

    center_pair_floor = max(sorted(abs(x) for x in spec)[:2])

    is_24 = pos == 2 and neg == 4 and zer == 0
    is_22 = pos == 2 and neg == 2 and zer == 2

    label = "[2+,4-,0^0]" if is_24 else "[2+,2-,2^0]" if is_22 else f"[{pos}+,{neg}-,{zer}^0]"

    return {
        "label": label,
        "is_24": is_24,
        "is_22": is_22,
        "trace": trace,
        "ratio": ratio,
        "center": center_pair_floor,
        "sorted": s
    }

def calculate_center_drift(history, start=5, end=50):
    pts = [(n, c) for n, c in history if start <= n <= end and c > 0]

    if len(pts) < 2:
        return 0.0

    xm = sum(n for n, _ in pts) / len(pts)
    ym = sum(math.log10(c) for _, c in pts) / len(pts)

    den = sum((n - xm) ** 2 for n, _ in pts)
    num = sum((n - xm) * (math.log10(c) - ym) for n, c in pts)

    return num / den if den else 0.0

# --- MAIN EVALUATOR ----------------------------------------------------------

def evaluate_dual_skeleton(
    a, b, c,
    max_steps=5000,
    scale=1.0,
    eps=1e-6,
    threshold=1e-4,
    constraint="none",
    required_24_locks=10
):
    Q = [[1.0 if i == j else 0.0 for j in range(6)] for i in range(6)]
    lsums = [0.0] * 6

    st = apply_constraint((complex(a), complex(b), complex(c)), constraint)

    first_22 = first_24 = stable_24 = None

    p22_current = p22_max = p22_total = 0
    p24_current = p24_max = p24_total = 0

    center_history = []
    mirror_counts = {(0, 4): 0, (1, 5): 0, (2, 6): 0, (3, 7): 0}

    for step in range(1, max_steps + 1):
        J = get_full_map_jacobian_6d(st, scale, eps, constraint)
        ns = next_state(st, scale, constraint)

        pair = mirror_pair_z8(ns[2])
        mirror_counts[pair] += 1

        new_Q = [
            [sum(J[row][col] * Q[v][col] for col in range(6)) for row in range(6)]
            for v in range(6)
        ]

        for i in range(6):
            for j in range(i):
                dot = sum(new_Q[i][k] * new_Q[j][k] for k in range(6))
                for k in range(6):
                    new_Q[i][k] -= dot * new_Q[j][k]

            norm = math.sqrt(sum(new_Q[i][k] ** 2 for k in range(6)))

            if norm > 1e-12:
                lsums[i] += math.log(norm)
                for k in range(6):
                    new_Q[i][k] /= norm

            Q[i] = new_Q[i]

        st = ns

        spec = [x / step for x in lsums]
        cls = classify_spectrum_ternary(spec, threshold)
        center_history.append((step, cls["center"]))

        if cls["is_22"]:
            p22_total += 1
            p22_current += 1
            first_22 = first_22 or step
            p22_max = max(p22_max, p22_current)
        else:
            p22_current = 0

        if cls["is_24"]:
            p24_total += 1
            p24_current += 1
            first_24 = first_24 or step
            p24_max = max(p24_max, p24_current)

            if p24_current >= required_24_locks and stable_24 is None:
                stable_24 = step - required_24_locks + 1
        else:
            p24_current = 0

    final_spec = [x / max_steps for x in lsums]
    final = classify_spectrum_ternary(final_spec, threshold)

    return {
        "first_22": first_22,
        "p22_max": p22_max,
        "p22_total": p22_total,

        "first_24": first_24,
        "stable_24": stable_24,
        "p24_max": p24_max,
        "p24_total": p24_total,

        "trace": final["trace"],
        "ratio": final["ratio"],
        "center": final["center"],
        "label": final["label"],
        "drift": calculate_center_drift(center_history),
        "spec": final_spec,
        "mirror_counts": mirror_counts
    }

# --- SEEDS -------------------------------------------------------------------

def build_core_targets():
    phi = (1 + math.sqrt(5)) / 2
    pi = math.pi
    z = complex(phi, pi)

    return [
        ("Golden Diagonal", (phi, phi, phi)),
        ("Cubic Roots Phase", (z, rot(z, 120), rot(z, 240))),
        ("Quarter Roots Phase", (z, rot(z, 90), rot(z, 180))),
        ("Phase Ring 180", (z, rot(z, 180), rot(z, 360))),
        ("Large +1e6", (1e6, 1e6, 1e6)),
        ("Large -1e6", (-1e6, -1e6, -1e6)),
        ("Ultra Complex 1e6+i1e6", (
            complex(1e6, 1e6),
            complex(1e6, 1e6),
            complex(1e6, 1e6)
        )),
        ("Boundary Edge 7.9999+i7.9999", (
            complex(7.9999, 7.9999),
            complex(7.9999, 7.9999),
            complex(7.9999, 7.9999)
        ))
    ]

def perturb_seed(seed, p, mode):
    a, b, c = seed

    if mode == "c_wedge":
        return a, b, c + complex(p, -p)

    if mode == "a_wedge":
        return a + complex(p, -p), b, c

    if mode == "b_wedge":
        return a, b + complex(p, -p), c

    if mode == "all_wedge":
        return a + complex(p, -p), b + complex(-p, p), c + complex(p, p)

    if mode == "real_all":
        return a + p, b - p, c + p

    if mode == "imag_all":
        return a + 1j * p, b - 1j * p, c + 1j * p

    return seed

# --- SCRIPT 1: SOVEREIGN CLOSURE --------------------------------------------

def run_sovereign_closure_scan(base_abc, name, steps):
    perturbations = [0.0, 1e-15, 1e-12, 1e-9, 1e-8]
    thresholds = [1e-3, 1e-4, 1e-5, 1e-6]

    print(f"\n[{MOD_LABEL} SOVEREIGN CLOSURE SCAN] {name} | Steps={steps}")

    for th in thresholds:
        print(f"\nThreshold={th:.0e}")
        print(f"{'Pert':<10} | {'First22':<8} | {'P22Max':<7} | {'Stable24':<8} | {'Trace':<10} | Drift | MirrorCounts")

        for p in perturbations:
            a, b, c = base_abc
            r = evaluate_dual_skeleton(
                a, b, c + complex(p, -p),
                max_steps=steps,
                threshold=th
            )

            print(
                f"{p:<10.1e} | "
                f"{str(r['first_22']):<8} | "
                f"{r['p22_max']:<7} | "
                f"{str(r['stable_24']):<8} | "
                f"{r['trace']:+.6f} | "
                f"{r['drift']:+.3e} | "
                f"{r['mirror_counts']}"
            )

def run_v5142_block():
    phi = (1 + math.sqrt(5)) / 2
    pi = math.pi
    z = complex(phi, pi)

    broad = [
        ("Large Negative Real Scale (-10^6)", (-1e6, -1e6, -1e6)),
        ("Ultra Complex Float (10^6+i10^6)", (
            complex(1e6, 1e6),
            complex(1e6, 1e6),
            complex(1e6, 1e6)
        )),
        ("Phase Ring 30", (z, rot(z, 30), rot(z, 60))),
        ("Phase Ring 45", (z, rot(z, 45), rot(z, 90))),
        ("Phase Ring 90", (z, rot(z, 90), rot(z, 180))),
        ("Phase Ring 120", (z, rot(z, 120), rot(z, 240)))
    ]

    deep = [
        ("Deep Golden Diagonal", (phi, phi, phi)),
        ("Deep Cubic Roots Phase", (z, rot(z, 120), rot(z, 240))),
        ("Deep Phase Ring 180", (z, rot(z, 180), rot(z, 360)))
    ]

    print(f"\n=== {MOD_LABEL} V5.1.4.2 SOVEREIGN CLOSURE MATRIX ===")

    for name, seed in broad:
        run_sovereign_closure_scan(seed, name, steps=5000)

    for name, seed in deep:
        run_sovereign_closure_scan(seed, name, steps=100000)

# --- SCRIPT 2: ISSUE SCANS ---------------------------------------------------

def run_center_dwell_report():
    print(f"\n[{MOD_LABEL} ISSUE 1] CENTER DWELL / DRIFT REPORT")

    for name, seed in build_core_targets():
        r = evaluate_dual_skeleton(*seed, max_steps=50000)

        note = "NO CENTER ROOM"
        if r["p22_max"] == 1:
            note = "ONE-STEP CORRIDOR"
        elif 2 <= r["p22_max"] < 100:
            note = "METASTABLE SHORT CORRIDOR"
        elif r["p22_max"] >= 100:
            note = "LONG-LIVED CHAMBER CANDIDATE"

        print(
            f"{name:<32} | "
            f"First22={r['first_22']} | "
            f"P22Max={r['p22_max']} | "
            f"P22Total={r['p22_total']} | "
            f"Stable24={r['stable_24']} | "
            f"Drift={r['drift']:+.3e} | "
            f"Final={r['label']} | "
            f"{note}"
        )

def run_multi_axis_perturbation_scan():
    print(f"\n[{MOD_LABEL} ISSUE 2] MULTI-AXIS PERTURBATION SCAN")

    modes = ["c_wedge", "a_wedge", "b_wedge", "all_wedge", "real_all", "imag_all"]
    perturbations = [0.0, 1e-15, 1e-12, 1e-9, 1e-8]

    for name, seed in build_core_targets()[:4]:
        print(f"\nTarget: {name}")

        for mode in modes:
            for p in perturbations:
                r = evaluate_dual_skeleton(
                    *perturb_seed(seed, p, mode),
                    max_steps=5000
                )

                print(
                    f"{mode:<10} p={p:.1e} | "
                    f"First22={r['first_22']} | "
                    f"P22Max={r['p22_max']} | "
                    f"Stable24={r['stable_24']} | "
                    f"Trace={r['trace']:+.6f} | "
                    f"Drift={r['drift']:+.3e}"
                )

def run_gamma_sweep():
    print(f"\n[{MOD_LABEL} ISSUE 3] GAMMA / SCALE SWEEP")

    for name, seed in build_core_targets()[:5]:
        print(f"\nTarget: {name}")

        for sc in [0.0, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0]:
            r = evaluate_dual_skeleton(*seed, max_steps=10000, scale=sc)

            print(
                f"scale={sc:<4} | "
                f"First22={r['first_22']} | "
                f"P22Max={r['p22_max']} | "
                f"Stable24={r['stable_24']} | "
                f"Trace={r['trace']:+.6f} | "
                f"Ratio={r['ratio']:.4f} | "
                f"Final={r['label']}"
            )

def run_constrained_submap_scan():
    print(f"\n[{MOD_LABEL} ISSUE 4] CONSTRAINED SUBMAP / TRUE CHAMBER HUNT")

    constraints = [
        "none",
        "force_equal_ab",
        "force_conjugate_ac",
        "force_phase120",
        "force_diagonal",
        "force_mirror_ac_z8"
    ]

    for name, seed in build_core_targets()[:5]:
        print(f"\nTarget: {name}")

        for con in constraints:
            r = evaluate_dual_skeleton(*seed, max_steps=50000, constraint=con)

            print(
                f"{con:<20} | "
                f"First22={r['first_22']} | "
                f"P22Max={r['p22_max']} | "
                f"P22Total={r['p22_total']} | "
                f"P24Max={r['p24_max']} | "
                f"Trace={r['trace']:+.6f} | "
                f"Final={r['label']}"
            )

def run_random_basin_scan(samples=250, max_steps=5000, seed_value=1337):
    print(f"\n[{MOD_LABEL} ISSUE 5] RANDOM BASIN COVERAGE SCAN")

    rng = random.Random(seed_value)

    p22_hits = 0
    no_24 = 0
    max_p22 = 0
    best = None

    mirror_total = {(0, 4): 0, (1, 5): 0, (2, 6): 0, (3, 7): 0}

    for i in range(samples):
        seed = tuple(
            complex(rng.uniform(0, MODULUS), rng.uniform(0, MODULUS))
            for _ in range(3)
        )

        r = evaluate_dual_skeleton(*seed, max_steps=max_steps)

        if r["p22_max"] > 0:
            p22_hits += 1

        if r["stable_24"] is None:
            no_24 += 1

        for k, v in r["mirror_counts"].items():
            mirror_total[k] += v

        if r["p22_max"] > max_p22:
            max_p22 = r["p22_max"]
            best = (i, seed, r)

    print(f"Samples checked: {samples}")
    print(f"P22 hits: {p22_hits}")
    print(f"No stable [2+,4-,0^0] lock: {no_24}")
    print(f"Max P22 observed: {max_p22}")
    print(f"Aggregate Z8 mirror counts: {mirror_total}")

    if best:
        i, seed, r = best
        print(f"Best candidate index={i} | seed={seed}")
        print(
            f"First22={r['first_22']} | "
            f"P22Max={r['p22_max']} | "
            f"Stable24={r['stable_24']} | "
            f"Trace={r['trace']:+.6f} | "
            f"Ratio={r['ratio']:.4f} | "
            f"Final={r['label']}"
        )

# --- MASTER ------------------------------------------------------------------

def execute_combined_z8_suite():
    print("### 6-GEM MANIFOLD — Z8 MIRROR-STATE COMPARATIVE SUITE")
    print("### MODULUS = 8.0")
    print("### PURPOSE: compare original Z6 skeleton behavior against Z8 half-modulus mirror dynamics")

    run_v5142_block()
    run_center_dwell_report()
    run_multi_axis_perturbation_scan()
    run_gamma_sweep()
    run_constrained_submap_scan()
    run_random_basin_scan(samples=250, max_steps=5000)

    print("\n[Z8 DECISION RULE]")
    print("If [2+,4-,0^0] remains stable under Z8, the skeleton is modulus-robust.")
    print("If [2+,2-,2^0] grows under Z8, the mirror-state lift creates a true center chamber.")
    print("If mirror brackets distribute evenly, Z8 behaves as a balanced ignorance-state extension.")
    print("If one mirror bracket dominates, Z8 introduces directional hidden-state bias.")
    print("If Z8 destroys the Z6 lock, then the original 6-Gem signature is modulus-specific rather than universal.")

if __name__ == "__main__":
    execute_combined_z8_suite()

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
#- 6-GEM_MANIFOLD_Z8_MIRROR-STATE.txt
#- 6-GEM_MANIFOLD_Z8_MIRROR-STATE_SUITE.py
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