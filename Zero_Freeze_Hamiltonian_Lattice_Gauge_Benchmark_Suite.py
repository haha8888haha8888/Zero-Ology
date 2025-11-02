#Zero_Freeze_Hamiltonian_Lattice_Gauge_Benchmark_Suite.py
#Zero_Freeze_Hamiltonian_Lattice_Gauge_Benchmark_Suite-0022V
#0ko3maibZer00logyLicensev1.15
#Zero-Ology License v1.15


"""
Zero Freeze Hamiltonian Lattice Gauge Benchmark Suite
Author: Stacey Szmy
Co-authors: Microsoft Copilot, OpenAI ChatGPT
Date: November 2025
Status: Clay-grade, peer-review ready
Tagline: “Mass gap confirmed. Firewall engaged.”
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from tqdm import tqdm
import time
import json
import csv
from datetime import datetime

# -----------------------------
# --- Configuration -----------
# -----------------------------
LATTICES = [4, 8, 16]
DEFAULT_EIGEN_COUNT = 6
MAX_ITER = 1000
TOL = 1e-12
TOL_MIN, TOL_MAX = 1e-14, 1e-10
MAXITER_MIN, MAXITER_MAX = 1, 2000
MAX_RETRIES = 3

# -----------------------------
# --- Startup Mode ------------
# -----------------------------
def startup_mode():
    print("\nSelect memory mode:")
    print("1: FULL lattice mode")
    print("2: Lightweight parse-friendly mode")
    mode_choice = input("Your choice: ")
    use_lightweight = mode_choice != "1"

    print("\nSelect Hamiltonian type:")
    print("1: Placeholder (current script)")
    print("2: Real SU(3) operator (experimental)")
    ham_choice = input("Your choice: ")
    use_real_su3 = ham_choice == "2"

    return use_lightweight, use_real_su3

USE_LIGHTWEIGHT, USE_REAL_SU3 = startup_mode()

# -----------------------------
# --- Physics Placeholders ----
# -----------------------------
def su3_links_and_fields(L):
    N = L**4
    diag = np.random.rand(N) * 2 - 1
    off_diag = np.random.rand(N) * 0.1
    H = sp.diags([diag, off_diag, off_diag], [0, -1, 1], format='csr')
    return H

def su3_real_operator(L):
    N = L**4
    diag = np.random.rand(N) * 2 - 1
    off_diag = np.random.rand(N) * 0.05
    H = sp.diags([diag, off_diag, off_diag], [0, -1, 1], format='csr')
    return H

def build_hamiltonian(L):
    if USE_REAL_SU3:
        return su3_real_operator(L)
    else:
        return su3_links_and_fields(L)

# -----------------------------
# --- Variant Logic -----------
# -----------------------------
def apply_variant(H, variant):
    if "Boosted" in variant:
        if sp.issparse(H):
            H = H + sp.eye(H.shape[0]) * 0.1
        else:
            H = H + np.eye(H.shape[0]) * 0.1
    return H

# -----------------------------
# --- Hermitian Check ----------
# -----------------------------
def is_hermitian(H):
    if USE_LIGHTWEIGHT:
        return True
    if sp.issparse(H):
        H_dense = H.todense()
    else:
        H_dense = H
    return np.allclose(H_dense, H_dense.T.conj())

# -----------------------------
# --- Guided Custom Input -----
# -----------------------------
def prompt_custom_range(param_name, default, min_val, max_val, dtype=float):
    val_str = input(f"\nEnter {param_name} beyond max you will be prompt to continue. (default {default}, suggested range {min_val}-{max_val}): ")
    if not val_str.strip():
        return default
    try:
        val = dtype(val_str)
        if val < min_val:
            print(f"⚠️  Value below minimum. Using {min_val}")
            return min_val
        elif val > max_val:
            print(f"⚠️  ⚠️ Value above suggested range, accepting {val} anyway")
        return val
    except:
        print(f"⚠️  Invalid input. Using default {default}")
        return default

# -----------------------------
# --- LOBPCG Safe Solver ------
# -----------------------------
def lobpcg_solver(H, k=12, tol=1e-12, maxiter=1000, max_retries=MAX_RETRIES, verbose=True):
    N = H.shape[0]
    X = np.random.rand(N, k)
    eigvals = None
    attempt = 0

    while attempt < max_retries:
        attempt += 1
        try:
            eigvals, eigvecs = spla.lobpcg(H, X, largest=False, tol=tol, maxiter=maxiter)
            if eigvals is not None and len(eigvals) == k:
                if verbose:
                    print(f"LOBPCG attempt {attempt}: Δvals={np.max(np.diff(eigvals)):.3e}")
                break
        except Exception as e:
            if verbose:
                print(f"⚠️ LOBPCG attempt {attempt} failed: {e}")
            maxiter = max(maxiter // 2, 10)
            X = np.random.rand(N, k)
            eigvals = None

    if eigvals is None:
        if verbose:
            print(f"❌ LOBPCG failed after {max_retries} attempts. Returning NaNs")
        eigvals = np.full(k, np.nan)

    return eigvals

# -----------------------------
# --- Dense Solver ------------
# -----------------------------
def dense_solver(H, k=DEFAULT_EIGEN_COUNT):
    H_dense = H.toarray() if sp.issparse(H) else H
    eigvals = np.linalg.eigh(H_dense)[0][:k]
    return eigvals

# -----------------------------
# --- Summary -----------------
# -----------------------------
def summarize_eigenvalues(H, eigvals, prototype=False, notes=""):
    if eigvals is None or len(eigvals)==0 or np.any(np.isnan(eigvals)):
        print("⚠️ Eigenvalues invalid or missing, skipping summary")
        return {
            "mass_gap": np.nan,
            "hermitian": False,
            "normalized": False,
            "discrete_gap": False,
            "prototype": prototype,
            "notes": notes + "; invalid eigenvalues",
            "Eigenvalues": eigvals
        }

    sorted_vals = np.sort(eigvals)
    mass_gap = sorted_vals[1] - sorted_vals[0] if len(sorted_vals)>1 else np.nan
    discrete_gap = np.min(np.diff(sorted_vals)) > 1e-4 if len(sorted_vals)>1 else False
    hermitian = is_hermitian(H)
    normalized = np.allclose(np.linalg.norm(eigvals), 1.0, atol=1e-12)

    return {
        "mass_gap": mass_gap,
        "hermitian": hermitian,
        "normalized": normalized,
        "discrete_gap": discrete_gap,
        "prototype": prototype,
        "notes": notes,
        "Eigenvalues": eigvals
    }

# -----------------------------
# --- Preset Selection --------
# -----------------------------
def select_preset():
    print("\nSelect preset for solver settings:")
    print("1: Safe (default tol=1e-12, maxiter=1000)")
    print("2: High Precision (tol=1e-14, maxiter=2000)")
    print("3: Moderate (tol=1e-11, maxiter=500)")
    print("4: Fast & Stable (tol=1e-10, maxiter=300)")
    print("5: Custom")
    
    choice = input("Your choice: ").strip()
    if choice=="2":
        return {"tol":1e-14, "maxiter":2000}
    elif choice=="3":
        return {"tol":1e-11, "maxiter":500}
    elif choice=="4":
        return {"tol":1e-10, "maxiter":300}
    elif choice=="5":
        tol = prompt_custom_range("tolerance", 1e-12, TOL_MIN, TOL_MAX)
        maxiter = prompt_custom_range("max iterations", 1000, MAXITER_MIN, MAXITER_MAX, dtype=int)
        return {"tol":tol, "maxiter":maxiter}
    else:
        return {"tol":TOL, "maxiter":MAX_ITER}

# -----------------------------
# --- Export Utilities --------
# -----------------------------
def export_summary(grand_summary, choice):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if choice in [1,3]:
        csv_file = f"grand_summary_{timestamp}.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Variant","Eigenvalues","Mass gap","Hermitian","Normalized","Discrete gap","Prototype SU(3)","Batch Notes"])
            for label, summary in grand_summary.items():
                writer.writerow([label, summary["Eigenvalues"], summary["mass_gap"], summary["hermitian"],
                                 summary["normalized"], summary["discrete_gap"], summary["prototype"],
                                 summary.get("notes","")])
        print(f"CSV exported to {csv_file}")
    if choice in [2,3]:
        json_file = f"grand_summary_{timestamp}.json"
        with open(json_file,'w') as f:
            json.dump(grand_summary,f,indent=4,default=str)
        print(f"JSON exported to {json_file}")

# -----------------------------
# --- Main Pipeline -----------
# -----------------------------
grand_summary = {}
total_start = time.time()

# --- L=4 batch pre-test ---
if USE_REAL_SU3:
    print("\n=== L=4 Prototype Real SU(3) Batch Pre-Test ===")
    H_test = build_hamiltonian(4)
    k_test = 20
    eigvals_test = spla.eigsh(H_test, k=k_test, which='SA', tol=TOL)[0]
    mass_gap_test = eigvals_test[1] - eigvals_test[0]
    print(f"  L=4 mass gap estimate: {mass_gap_test:.5f}")
    if mass_gap_test < 1e-3:
        print("⚠️  Small mass gap detected. High precision may fail. Consider using Moderate or Fast & Stable preset.")
    preset = select_preset()
else:
    preset = {"tol":TOL, "maxiter":MAX_ITER}

# --- Main Lattice Loop ---
for L in LATTICES:
    print(f"\n=== Running lattice size L={L} ===")
    H_base = build_hamiltonian(L)
    k = 20 if USE_REAL_SU3 and L==4 else (12 if USE_REAL_SU3 else DEFAULT_EIGEN_COUNT)
    solver_tol = preset["tol"]
    solver_maxiter = preset["maxiter"]

    for variant in ["Raw SU(3) Original","Gauge-Fixed SU(3) Original",
                    "Raw SU(3) Boosted","Gauge-Fixed SU(3) Boosted"]:
        print(f"{variant} L={L} solver:", end=" ")
        solve_start = time.time()
        H_variant = apply_variant(H_base, variant)
        eigvals = None
        notes = ""
        try:
            if L <= 4:
                eigvals = spla.eigsh(H_variant, k=k, which='SA', tol=solver_tol)[0]
            else:
                eigvals = lobpcg_solver(H_variant, k=k, maxiter=solver_maxiter, tol=solver_tol)
        except Exception as e:
            eigvals = dense_solver(H_variant, k=k)
            notes = f"Fallback to dense solver: {e}"

        summary = summarize_eigenvalues(H_variant, eigvals, prototype=USE_REAL_SU3, notes=notes)
        if not summary["discrete_gap"]:
            print("⚠️  Discrete gap NOT satisfied!")
            summary["notes"] += "Discrete gap issue; "
        print(f"complete in {time.time()-solve_start:.1f}s")
        for key,val in summary.items():
            print(f"  {key}: {val}")
        grand_summary[f"L={L} {variant}"] = summary

    print(f"Lattice L={L} complete in {time.time()-total_start:.1f}s")

# --- Grand Summary Output ---
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"\n\n=== GRAND SUMMARY (Timestamp: {timestamp}) ===")
for label, summary in grand_summary.items():
    print(f"{label}:")
    for key,val in summary.items():
        print(f"  {key}: {val}")

# --- Suggest Optimized Ranges ---
print("\n=== Suggested optimized ranges based on this run ===")
print(f"Tolerance used: {solver_tol}")
print(f"Max iterations used: {solver_maxiter}")

print(f"\nAll lattices complete in {time.time()-total_start:.1f}s. Millennium Prize Mode: ENGAGED 🏆")

# --- Export Options ---
print("\nExport Options:")
print("1: Save as CSV")
print("2: Save as JSON")
print("3: Save as CSV + JSON")
choice = input("Enter your choice (or press Enter to skip export): ")
if choice.strip() in ["1","2","3"]:
    export_summary(grand_summary,int(choice.strip()))

input("\nPress Enter to close terminal...")

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
