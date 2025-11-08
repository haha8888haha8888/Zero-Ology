#RHFsuite0020V
#Recursive Hybrid Framework Mono-Script-0020V
# 0ko3maibZero-OlogyLicensev1.17
# Zero-Ology License v1.17

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


# --- Variant-Specific Pipeline Runners ---
def run_copilot_rhf():
    curves = gen_curves()
    rhf1 = rhf1_prefilter(curves.copy())
    rhf1_selected = rhf1_select(rhf1)
    rhf1_scored = rhf1_score(rhf1_selected)
    print("\n=== Copilot RHF ===")
    print("Top 5 Curves:")
    print(rhf1_scored.sort_values(by='curve_score', ascending=False).head(5))
    print("Correlation:")
    print(correlation_matrix(rhf1_scored, ['deltaH', 'collapse_count', 'rank', 'regulator']).round(6))

def run_gemini_rhf():
    curves = gen_curves()
    rhf2 = rhf2_prefilter(curves.copy())
    rhf2_scored = rhf2_score(rhf2)
    rhf2_selected = rhf2_select(rhf2_scored)
    print("\n=== Gemini RHF ===")
    print("Top 5 Curves:")
    print(rhf2_selected.sort_values(by='composite_score', ascending=False).head(5))
    print("Correlation:")
    print(correlation_matrix(rhf2_selected, ['deltaH', 'collapse_ratio', 'prime_count', 'rank', 'regulator']).round(6))

def run_grok_rhf():
    curves = gen_curves()
    rhf3 = rhf3_prefilter(curves.copy())
    rhf3_selected = rhf3_select(rhf3)
    rhf3_scored = rhf3_score(rhf3_selected)
    print("\n=== Grok RHF ===")
    print("Top 5 Curves:")
    print(rhf3_scored.sort_values(by='curve_score', ascending=False).head(5))
    print("Correlation:")
    print(correlation_matrix(rhf3_scored, ['deltaH', 'collapse_count', 'rank', 'regulator']).round(6))


# --- Shared Curve Generator ---
def gen_curves(n=20000, a_range=(-10, 10), c_range=(-10, 10), seed=42):
    np.random.seed(seed)
    a_vals = np.random.uniform(*a_range, n)
    c_vals = np.random.uniform(*c_range, n)
    return pd.DataFrame({'id': np.arange(1, n+1), 'a': a_vals, 'c': c_vals, 'seed': seed})

# --- RHF Variant 1: Gaussian Drift + Collapse Count ---
def rhf1_prefilter(df):
    np.random.seed(df['seed'].iloc[0])
    df['deltaH'] = np.random.normal(0, 5, len(df))
    df['max_flag'] = np.random.choice(['Collapse', 'Drift', 'Prime'], len(df), p=[0.3, 0.2, 0.5])
    df['collapse_count'] = np.random.randint(0, 4, len(df))
    return df

def rhf1_score(df):
    df['rank'] = np.random.choice([0, 1, 2], len(df), p=[0.5, 0.4, 0.1])
    df['regulator'] = df['rank'] * np.random.uniform(1.0, 5.0, len(df))
    df['curve_score'] = (
        np.abs(df['deltaH']) * 0.3 +
        df['collapse_count'] * 0.2 +
        df['rank'] * 0.3 +
        df['regulator'] * 0.2
    )
    return df

def rhf1_select(df, threshold=2.5):
    return df[(np.abs(df['deltaH']) > threshold) & (df['collapse_count'] >= 1)]

# --- RHF Variant 2: Gemini Composite ---
def rhf2_prefilter(df):
    np.random.seed(df['seed'].iloc[0])
    df['deltaH'] = np.random.normal(0, 5, len(df))
    df['collapse_ratio'] = np.random.beta(0.5, 2, len(df))
    df['prime_count'] = np.random.poisson(0.5, len(df))
    df['max_flag'] = np.random.choice(['Collapse', 'Drift', 'Prime', 'Balanced'], len(df), p=[0.3, 0.2, 0.4, 0.1])
    return df

def rhf2_score(df):
    df['composite_score'] = (
        np.abs(df['deltaH']) * 0.4 +
        df['collapse_ratio'] * 0.4 +
        df['prime_count'] * 0.2
    )
    df['rank'] = np.random.choice([0, 1, 2], len(df), p=[0.5, 0.4, 0.1])
    df['regulator'] = df['rank'] * np.random.uniform(1.0, 5.0, len(df))
    return df

def rhf2_select(df, n=9500):
    return df.sort_values(by='composite_score', ascending=False).head(n)

# --- RHF Variant 3: Quadratic Map Proxy ---
def rhf3_prefilter(df):
    def entropy_drift(H_prev, H_next, epsilon=0.01, threshold=1e3):
        delta = H_next - H_prev
        if abs(delta) < epsilon or abs(H_next) > threshold:
            return "Collapse"
        elif abs(H_next) > 10:
            return "Drift"
        elif int(H_next) % 2 == 0 and int(H_next) == H_next:
            return "Even"
        elif int(H_next) % 2 == 1 and int(H_next) == H_next:
            return "Odd"
        return "Balanced"

    np.random.seed(df['seed'].iloc[0])
    results = []
    for _, row in df.iterrows():
        H_values = [row['a']]
        flags = ["Balanced"]
        for _ in range(5):
            H_next = H_values[-1] ** 2 + row['c']
            flag = entropy_drift(H_values[-1], H_next)
            flags.append(flag)
            H_values.append(H_next)
            if flag == "Collapse":
                break
        deltaH = H_values[-1] - H_values[0]
        priority = {"Collapse": 1, "Drift": 2, "Even": 3, "Odd": 3, "Balanced": 4}
        max_flag = min(flags, key=lambda f: priority.get(f, 99))
        collapse_count = flags.count("Collapse")
        results.append([row['id'], deltaH, max_flag, collapse_count])
    prefilter_df = pd.DataFrame(results, columns=["id", "deltaH", "max_flag", "collapse_count"])
    return pd.merge(df, prefilter_df, on="id")

def rhf3_score(df):
    df['rank'] = np.random.choice([0, 1, 2], len(df), p=[0.5, 0.4, 0.1])
    df['regulator'] = df['rank'] * np.random.uniform(1.0, 5.0, len(df))
    df['curve_score'] = (
        np.abs(df['deltaH']) * 0.4 +
        df['collapse_count'] * 0.3 +
        df['rank'] * 0.3
    )
    return df

def rhf3_select(df, threshold=1.0):
    return df[(np.abs(df['deltaH']) > threshold) & (df['collapse_count'] > 0) & (df['max_flag'].isin(['Collapse', 'Drift']))]

# --- Shared Correlation ---
def correlation_matrix(df, cols):
    return df[cols].corr(method='spearman')

# --- Mono Pipeline Runner ---
def run_all_rhf():
    curves = gen_curves()

    print("\n=== RHF Variant 1 ===")
    rhf1 = rhf1_prefilter(curves.copy())
    rhf1_selected = rhf1_select(rhf1)
    rhf1_scored = rhf1_score(rhf1_selected)
    print("Top 5 Curves:")
    print(rhf1_scored.sort_values(by='curve_score', ascending=False).head(5))
    print("Correlation:")
    print(correlation_matrix(rhf1_scored, ['deltaH', 'collapse_count', 'rank', 'regulator']).round(6))

    print("\n=== RHF Variant 2 ===")
    rhf2 = rhf2_prefilter(curves.copy())
    rhf2_scored = rhf2_score(rhf2)
    rhf2_selected = rhf2_select(rhf2_scored)
    print("Top 5 Curves:")
    print(rhf2_selected.sort_values(by='composite_score', ascending=False).head(5))
    print("Correlation:")
    print(correlation_matrix(rhf2_selected, ['deltaH', 'collapse_ratio', 'prime_count', 'rank', 'regulator']).round(6))

    print("\n=== RHF Variant 3 ===")
    rhf3 = rhf3_prefilter(curves.copy())
    rhf3_selected = rhf3_select(rhf3)
    rhf3_scored = rhf3_score(rhf3_selected)
    print("Top 5 Curves:")
    print(rhf3_scored.sort_values(by='curve_score', ascending=False).head(5))
    print("Correlation:")
    print(correlation_matrix(rhf3_scored, ['deltaH', 'collapse_count', 'rank', 'regulator']).round(6))

# --- RHF Reference Information ---
def print_rhf_reference():
    print("\n=== RHF Reference Information ===")
    print("Title: Varia Math & Artificial Intelligence")
    print("Subtitle: Group Law Recursive Hybrid Formula & Deterministic Lift Recursive Hybrid Formula & Infinity Loop Recursive Hybrid Formula & Birch and Swinnerton-Dyer Conjecture return results From The Recursive Hybrid Framework.\n")
    print("Author: Stacey Szmy")
    print("Co-Creators: Ms Copilot, OpenAI ChatGPT-5")
    print("Review AI: Google Gemini, Xai Grok, OpenAI ChatGPT, Ms Copilot, Meta LLaMA")
    print("Date: August 2025")
    print("Issue: PRINT")
    print("ISBN: 9798262637737\n")

    print("Abstract:")
    print("The Recursive Hybrid Framework (RHF) is a symbolic diagnostic system designed to simulate, classify, and analyze recursive behavior in elliptic curve structures. RHF is not a proof engine for the Birch and Swinnerton-Dyer Conjecture (BSD), but a heuristic simulator that identifies collapse points, entropy drift, modular lifts, and infinite recursions through symbolic logic.\n")

    print("Core Formulas:")
    print("GLRHF — Group Law Recursive Hybrid Formula:")
    print("  P ⊕ Q = ∞ if tangent vertical (SBHFF trigger), else (x₃, y₃)")
    print("DLRHF — Deterministic Lift Recursive Hybrid Formula:")
    print("  L(m) = Lift(m) → ℤ, guided by flag hierarchy")
    print("ILRHF — Infinity Loop Recursive Hybrid Formula:")
    print("  R(Fₙ) = SBHFF(Fₙ) if recursive divergence, else Fₙ₊₁")
    print("SBHFF — Symbolic Black Hole Function Finder:")
    print("  B(Fₙ) = 1 if Fₙ → ∞ or 0 in finite steps, else 0\n")

    print("Symbolic Drift & Entropy Drift:")
    print("  ΔH = Hₙ₊₁ − Hₙ")
    print("  Collapse if |ΔH| < ε or ΔH → ∞")

    print("\nBSD Mapping:")
    print("  GLRHF Collapse → Rank anomalies")
    print("  DLRHF Lift → Modular invariants")
    print("  ILRHF Recursion → L-function vanishing")
    print("  Entropy Drift → Regulator slope")
    print("  SBHFF → Singular curve behavior")

    print("\nGlossary:")
    print("  Collapse: Recursive system divergence")
    print("  Drift: Symbolic instability")
    print("  SBHFF: Collapse finder for recursive sequences")

    print("\nExercises:")
    print("  1. Simulate GLRHF for y² = x³ − x")
    print("  2. Apply DLRHF to modular lift m = 37")
    print("  3. Run ILRHF with Fibonacci-lens SBHFF")
    print("  4. Measure entropy drift in a quadratic map")
    print("  5. Map symbolic results to BSD rank predictions")

# --- Terminal Control Loop ---
while True:
    print("\n" + "="*60)
    print("Recursive Hybrid Framework Mono-Script-0020V Execution Complete.")
    print("Press [Enter] to exit program.")
    print("Type [1] to run ALL RHF variants.")
    print("Type [2] to run Copilot RHF only.")
    print("Type [3] to run Gemini RHF only.")
    print("Type [4] to run Grok RHF only.")
    print("Type [5] to print RHF Reference Information and view core equations.")
    print("="*60)

    user_input = input("Your choice: ").strip()

    if user_input == "":
        print("Exiting program. Goodbye!")
        break
    elif user_input == "1":
        print("\nRunning ALL RHF variants...\n")
        run_all_rhf()
    elif user_input == "2":
        print("\nRunning Copilot RHF...\n")
        run_copilot_rhf()
    elif user_input == "3":
        print("\nRunning Gemini RHF...\n")
        run_gemini_rhf()
    elif user_input == "4":
        print("\nRunning Grok RHF...\n")
        run_grok_rhf()
    elif user_input == "5":
        print_rhf_reference()
    else:
        print("Invalid input. Please try again.")



if __name__ == "__main__":
    run_all_rhf()

# LICENSE.TXT
# Zero-Ology License v1.17
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.17
#November 07, 2025
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

