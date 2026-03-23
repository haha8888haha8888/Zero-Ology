# =============================================================================
# STEREALGEBRA — Formalization of the 6 Gem States of Stereo-Identity in Ternary Algebra
#A: S.Szmy
#CO-A: Copilot, Grok, Gemini, ChatGPT
# =============================================================================
# Commands:
#   ENTER       → run a new random triple test
#   S or stats  → show statistics over 2000 random triples
#   XX          → exit
# Terminal output persists (no screen clearing)
# =============================================================================

import random
from collections import Counter

# ANSI colors (works in most terminals)
GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"

def color_val(v):
    if v > 0: return f"{GREEN}{v:+d}{RESET}"
    if v < 0: return f"{RED}{v:+d}{RESET}"
    return f"{v:+d}"

# -----------------------------------------------------------------------------
# CHIRALITY VARIANTS
# -----------------------------------------------------------------------------
def chirality_original(a, b, c):
    a0, b0, c0 = a % 6, b % 6, c % 6
    step1 = (b0 - a0) % 6
    step2 = (c0 - b0) % 6
    if step1 == 0 or step2 == 0:
        return 0
    def direction(step):
        return +1 if step in (1, 2, 3) else -1
    dir1 = direction(step1)
    dir2 = direction(step2)
    return dir1 if dir1 == dir2 else 0


def chirality_signed_arc(a, b, c):
    def signed_step(x, y):
        d = (y - x) % 6
        if d == 0: return 0
        return d if d <= 3 else d - 6
    s1 = signed_step(a, b)
    s2 = signed_step(b, c)
    if s1 == 0 or s2 == 0:
        return 0
    if s1 > 0 and s2 > 0: return +1
    if s1 < 0 and s2 < 0: return -1
    return 0


def chirality_direction_only(a, b, c):
    def dir_step(x, y):
        d = (y - x) % 6
        if d == 0: return 0
        return +1 if d <= 3 else -1
    d1 = dir_step(a, b)
    d2 = dir_step(b, c)
    if d1 == 0 or d2 == 0:
        return 0
    return d1 if d1 == d2 else 0


def chirality_same_step(a, b, c):
    def signed_step(x, y):
        d = (y - x) % 6
        if d == 0: return 0
        return d if d <= 3 else d - 6
    s1 = signed_step(a, b)
    s2 = signed_step(b, c)
    if s1 == 0 or s2 == 0 or s1 != s2:
        return 0
    return +1 if s1 > 0 else -1


# -----------------------------------------------------------------------------
# LABELING
# -----------------------------------------------------------------------------
def label(v):
    labels = {
        0: "0/1", 1: "1/i", 2: "2/j",
        3: "3/-1", 4: "4/-i", 5: "5/-j"
    }
    v = v % 6
    return f"{labels[v]} ({v})"


# -----------------------------------------------------------------------------
# STATISTICS
# -----------------------------------------------------------------------------
def print_statistics(n=2000):
    counters = {
        "original": Counter(),
        "signed_arc": Counter(),
        "direction_only": Counter(),
        "same_step": Counter(),
    }

    for _ in range(n):
        a = random.randint(0, 5)
        b = random.randint(0, 5)
        c = random.randint(0, 5)
        counters["original"][chirality_original(a, b, c)] += 1
        counters["signed_arc"][chirality_signed_arc(a, b, c)] += 1
        counters["direction_only"][chirality_direction_only(a, b, c)] += 1
        counters["same_step"][chirality_same_step(a, b, c)] += 1

    print(f"\n{'═'*60}")
    print(f" Statistics over {n:,} uniform random triples")
    print(f"{'═'*60}")
    for name, cnt in counters.items():
        total = sum(cnt.values())
        p_pos = cnt[+1] / total * 100 if total else 0
        p_neg = cnt[-1] / total * 100 if total else 0
        p_zero = cnt[0] / total * 100 if total else 0
        print(f"  {name:16}  +1: {cnt[+1]:5d} ({p_pos:5.1f}%)"
              f"   -1: {cnt[-1]:5d} ({p_neg:5.1f}%)"
              f"    0: {cnt[0]:5d} ({p_zero:5.1f}%)")
    print(f"{'─'*60}\n")


# -----------------------------------------------------------------------------
# SINGLE RANDOM TEST
# -----------------------------------------------------------------------------
def run_random_test():
    a = random.randint(0, 5)
    b = random.randint(0, 5)
    c = random.randint(0, 5)

    vals = [
        chirality_original(a, b, c),
        chirality_signed_arc(a, b, c),
        chirality_direction_only(a, b, c),
        chirality_same_step(a, b, c)
    ]

    print("\n" + "─"*60)
    print(" STEREALGEBRA — Chirality Variant Test")
    print("─"*60)
    print(f"  {label(a)}  →  {label(b)}  →  {label(c)}")
    print()

    print(f"  Original          : {color_val(vals[0])}")
    print(f"  Signed arc        : {color_val(vals[1])}")
    print(f"  Direction-only    : {color_val(vals[2])}   ← Option A")
    print(f"  Same-step strict  : {color_val(vals[3])}   ← Option B")

    if len(set(vals)) > 1:
        print("\n  ⚠  VARIANTS DISAGREE on this triple")

    print("─"*60 + "\n")


# -----------------------------------------------------------------------------
# MAIN REPL
# -----------------------------------------------------------------------------
def main():
    print("\n" + "="*60)
    print("  STEREALGEBRA — Formalization of the 6 Gem States of Stereo-Identity in Ternary Algebra via python")
    print("="*60)
    print("  ENTER       → new random triple")
    print("  S / stats   → show statistics (2000 triples)")
    print("  XX          → exit")
    print("  Colors: " + GREEN + "+1" + RESET + " = clockwise, " + RED + "-1" + RESET + " = anticlockwise")
    print("="*60 + "\n")

    while True:
        user = input("Command (ENTER = test, S = stats, XX = exit): ").strip().upper()
        if user == "XX":
            print("\nExiting. Goodbye.\n")
            break
        elif user in ("S", "STATS"):
            print_statistics(2000)
        else:
            run_random_test()


if __name__ == "__main__":
    main()



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
#- szmy_mirror_model.txt
#- SMM_suite.py
#- SMM_log.txt
#- AWAKE_ERDŐS_STEP_RESONANCE_FRAMEWORK.txt
#- AESR_Suite.py
#- AESR_log.txt
#- AESR_V02_Suite.py
#- AESR_V02_Suite_log.txt
#- AWAKE_ERDŐS_STEP_RESONANCE_FRAMEWORK_V02.txt
#- Team_Zer00logy_Mathematics_Distillation_Challenge_Equational_Theories_DENSEFORM.txt
#- Team_Zer00logy_Mathematics_Distillation_Challenge_Equational_Theories_SOLIDFORM.txt
#- Team_Zer00logy_Mathematics_Distillation_Challenge_Equational_Theories_SOLIDFORM_ZEROPYTHFON_BETA.txt
#- Team_Zer00logy_Mathematics_Distillation_Challenge_Equational_Theories_ZEROPYTHFON_ZPY_ZETA.txt
#- Team_Zer00logy_Mathematics_Distillation_Challenge_Equational_Theories_ZEROPYTHFON_ZPY_ZETA_FALSE.txt
#- Six_Gem_States_of_Stereo-Identity_in_Ternary_Algebra_Suite.py
#- Six_Gem_States_of_Stereo-Identity_in_Ternary_Algebra.txt
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

