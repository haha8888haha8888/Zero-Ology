#Six_Gem_Logic_System_Dissertation_Suite.py
# =============================================================================
# 6 GEM LOGIC — Ternary Stream Inference System Suite
# A: S.Szmy
# CO-A: Copilot, Grok, Gemini, ChatGPT
# =============================================================================
# Commands:
#   ENTER       → new random Logic Stream
#   S or stats  → show distribution over 2000 streams
#   XX          → exit
# =============================================================================

import random
from collections import Counter

# ANSI colors
CYAN   = "\033[96m"   # Flux states (1,4)
AMBER  = "\033[93m"   # Tension states (2,5)
GREEN  = "\033[92m"   # Affirmation (0)
RED    = "\033[91m"   # Negation (3)
RESET  = "\033[0m"

def color_logic(state):
    if state in (1, 4): return f"{CYAN}{state}{RESET}"
    if state in (2, 5): return f"{AMBER}{state}{RESET}"
    if state == 0:      return f"{GREEN}{state}{RESET}"
    if state == 3:      return f"{RED}{state}{RESET}"
    return str(state)

def logic_label(v):
    labels = {
        0: "L0 - Absolute Affirmation",
        1: "L1 - Potential Flux",
        2: "L2 - Resonant Dissonance",
        3: "L3 - Absolute Negation",
        4: "L4 - Reflective Flux",
        5: "L5 - Resolved Dissonance"
    }
    return labels[v % 6]

# -----------------------------------------------------------------------------
# CORE STREAM INFERENCE OPERATOR
# -----------------------------------------------------------------------------

def stream_inference(a, b, c):
    a, b, c = a % 6, b % 6, c % 6

    base = (a + b + c) % 6
    correction = 1 if len({a, b, c}) == 3 else 0

    #balanced chirality
    def signed_step(x, y):
        diff = (y - x) % 6
        if diff == 0:
            return 0
        return diff if diff <= 3 else diff - 6

    step1 = signed_step(a, b)
    step2 = signed_step(b, c)

    if step1 > 0 and step2 > 0:
        orientation = 1
    elif step1 < 0 and step2 < 0:
        orientation = -1
    else:
        orientation = 0

    return (base + correction + orientation) % 6
# -----------------------------------------------------------------------------
# SINGLE TEST
# -----------------------------------------------------------------------------
def run_logic_test():
    a = random.randint(0, 5)
    b = random.randint(0, 5)
    c = random.randint(0, 5)
    result = stream_inference(a, b, c)

    print("\n" + "─"*70)
    print("  6 GEM LOGIC STREAM")
    print("─"*70)
    print(f" Premise A : {logic_label(a)}")
    print(f" Premise B : {logic_label(b)}")
    print(f" Witness C : {logic_label(c)}")
    print("─"*70)
    print(f" COLLAPSED INFERENCE → {color_logic(result)}  {logic_label(result)}")
    print("─"*70 + "\n")

    # NEW: return values for trace/wheel
    return a, b, c, result


# -----------------------------------------------------------------------------
# STATISTICS
# -----------------------------------------------------------------------------
def print_stats(n=2000):
    results = Counter()
    for _ in range(n):
        a, b, c = random.randint(0,5), random.randint(0,5), random.randint(0,5)
        results[stream_inference(a, b, c)] += 1

    print(f"\n{'═'*70}")
    print(f"  6 Gem Logic Distribution over {n:,} random streams")
    print(f"{'═'*70}")
    for i in range(6):
        count = results[i]
        perc = count / n * 100
        print(f"  {logic_label(i):28} : {count:5d}  ({perc:5.1f}%)")
    print(f"{'─'*70}\n")


# -----------------------------------------------------------------------------
# OPTIONAL ENHANCEMENTS FOR 6 GEM LOGIC SUITE
# -----------------------------------------------------------------------------

def trace_stream(a, b, c):
    """Show full breakdown of the inference process."""
    a, b, c = a % 6, b % 6, c % 6

    base = (a + b + c) % 6
    correction = 1 if len({a, b, c}) == 3 else 0

    # --- MATCHES MAIN OPERATOR (FIXED) ---
    def signed_step(x, y):
        diff = (y - x) % 6
        if diff == 0:
            return 0
        return diff if diff <= 3 else diff - 6

    step1 = signed_step(a, b)
    step2 = signed_step(b, c)

    if step1 > 0 and step2 > 0:
        orientation = 1
    elif step1 < 0 and step2 < 0:
        orientation = -1
    else:
        orientation = 0
    # -------------------------------------

    final = (base + correction + orientation) % 6

    print("\n" + "─"*70)
    print("  TRACE MODE — Full Stream Breakdown")
    print("─"*70)
    print(f" Premise A : {logic_label(a)}")
    print(f" Premise B : {logic_label(b)}")
    print(f" Witness C : {logic_label(c)}")
    print("─"*70)
    print(f" Base Sum (A+B+C mod 6)     : {base}")
    print(f" Nonlinear Correction (f)    : {correction}")
    print(f" Orientation Term (χ)        : {orientation}")
    print("─"*70)
    print(f" COLLAPSED RESULT → {color_logic(final)}  {logic_label(final)}")
    print("─"*70 + "\n")


def manual_input():
    """Let user enter A, B, C manually, with ENTER = random."""
    try:
        raw_a = input(" Enter A (0–5, ENTER=random): ").strip()
        raw_b = input(" Enter B (0–5, ENTER=random): ").strip()
        raw_c = input(" Enter C (0–5, ENTER=random): ").strip()

        a = int(raw_a) if raw_a != "" else random.randint(0, 5)
        b = int(raw_b) if raw_b != "" else random.randint(0, 5)
        c = int(raw_c) if raw_c != "" else random.randint(0, 5)

        trace_stream(a, b, c)

    except:
        print(" Invalid input. Use integers 0–5 or press ENTER for random.\n")

def show_phase_wheel_with_examples(a, b, c, result):
    """Hex wheel showing A, B, C, and the collapsed result."""
    wheel = [
        "        [1]        ",
        "   [0]        [2]  ",
        "   [5]        [3]  ",
        "        [4]        "
    ]

    markers = {
        a: "A",
        b: "B",
        c: "C",
        result: color_logic(result)
    }

    print("\nPhase Wheel (A,B,C,Result):")
    for line in wheel:
        for i in range(6):
            token = f"[{i}]"
            if i in markers:
                mark = markers[i]
                line = line.replace(token, f"[{mark}]")
            else:
                line = line.replace(token, f"[{i}]")
        print(line)
    print()

# ---------

def deviation_rate(n=5000):
    diff = 0
    for _ in range(n):
        a, b, c = random.randint(0,5), random.randint(0,5), random.randint(0,5)
        if stream_inference(a,b,c) != (a+b+c)%6:
            diff += 1

    rate = diff / n * 100
    print(f"\nDeviation from Z6 baseline: {diff}/{n} ({rate:.2f}%)\n")



def stability_test(n=1000):
    stable = 0

    for _ in range(n):
        a, b, c = random.randint(0,5), random.randint(0,5), random.randint(0,5)
        base = stream_inference(a,b,c)

        # perturb one input slightly
        c2 = (c + 1) % 6
        new = stream_inference(a,b,c2)

        if base == new:
            stable += 1

    print(f"\nStability under small perturbation: {stable}/{n} ({stable/n*100:.2f}%)\n")


##

def associativity_test(n=2000):
    failures = 0

    for _ in range(n):
        a,b,c,d = [random.randint(0,5) for _ in range(4)]

        left = stream_inference(stream_inference(a,b,c), d, 0)
        right = stream_inference(a, stream_inference(b,c,d), 0)

        if left != right:
            failures += 1

    print(f"\nNon-associativity rate: {failures}/{n} ({failures/n*100:.2f}%)\n")

def chirality_balance(n=5000):
    pos = neg = zero = 0

    for _ in range(n):
        a,b,c = [random.randint(0,5) for _ in range(3)]

        # reuse signed logic
        def signed_step(x,y):
            diff = (y-x)%6
            return 0 if diff==0 else (diff if diff<=3 else diff-6)

        s1 = signed_step(a,b)
        s2 = signed_step(b,c)

        if s1>0 and s2>0: pos += 1
        elif s1<0 and s2<0: neg += 1
        else: zero += 1

    print(f"\nChirality balance:")
    print(f" +1: {pos}")
    print(f" -1: {neg}")
    print(f"  0: {zero}\n")

##

def order_sensitivity_test(n=2000):
    diff = 0

    for _ in range(n):
        a,b,c = [random.randint(0,5) for _ in range(3)]

        if stream_inference(a,b,c) != stream_inference(b,a,c):
            diff += 1

    print(f"\nOrder sensitivity (A,B swap): {diff}/{n} ({diff/n*100:.2f}%)\n")


# -----------------------------------------------------------------------------
# MAIN REPL (FULLY PATCHED)
# -----------------------------------------------------------------------------
def main():
    print("="*70)
    print("  6 GEM LOGIC — Ternary Stream Inference Simulator v1.3")
    print("  Built on the 6 Gem States of Stereo-Identity")
    print("="*70)
    print("  ENTER       → new random Logic Stream")
    print("  S / stats   → show distribution")
    print("  M / manual  → enter A,B,C manually")
    print("  T / trace   → trace last random stream")
    print("  W / wheel   → new stream + wheel display")
    print("  D / dev     → deviation from Z6 baseline")
    print("  STAB        → stability test (perturbation)")
    print("  A / assoc   → non-associativity test")
    print("  C / chir    → chirality balance test")
    print("  O / order    → show commands")
    print("  H / help    → show commands")
    print("  XX          → exit")
    print("="*70 + "\n")

    # Track last stream for trace/wheel
    last_a, last_b, last_c, last_result = None, None, None, None

    def print_help():
        print("\nCommands:")
        print("  ENTER  → random stream")
        print("  S      → distribution stats")
        print("  M      → manual input")
        print("  T      → trace last stream")
        print("  W      → new stream + wheel")
        print("  D      → deviation from baseline")
        print("  STAB   → stability test")
        print("  A      → non-associativity test")
        print("  C      → chirality balance test")
        print("  O      → Order")
        print("  H      → help")
        print("  XX     → exit\n")

    while True:

        cmd = input(
            "\nCommand "
            "(ENTER=Stream | S=Stats | M=Manual | T=Trace | W=Wheel | "
            "D=Dev | STAB | A=Assoc | C=Chir | O=Order | H=Help | XX=Exit): "
        ).strip().upper()

        # EXIT
        if cmd == "XX":
            print("\nExiting. See you in the next stream.\n")
            break

        # HELP
        elif cmd in ("H", "HELP"):
            print_help()

        # STATS
        elif cmd in ("S", "STATS"):
            print_stats(2000)

        # MANUAL INPUT
        elif cmd in ("M", "MANUAL"):
            manual_input()

        # TRACE LAST STREAM
        elif cmd in ("T", "TRACE"):
            if last_a is not None:
                trace_stream(last_a, last_b, last_c)
            else:
                print("No stream has been run yet.\n")

        # WHEEL (new stream + wheel)
        elif cmd in ("W", "WHEEL"):
            last_a, last_b, last_c, last_result = run_logic_test()
            show_phase_wheel_with_examples(last_a, last_b, last_c, last_result)

        # DEVIATION TEST
        elif cmd in ("D", "DEV"):
            deviation_rate(5000)

        # STABILITY TEST
        elif cmd == "STAB":
            stability_test(2000)

        # NON-ASSOCIATIVITY TEST
        elif cmd in ("A", "ASSOC"):
            associativity_test(2000)

        # CHIRALITY BALANCE TEST
        elif cmd in ("C", "CHIR"):
            chirality_balance(5000)

        # ORDER 
        elif cmd in ("O", "Order"):
            order_sensitivity_test(2000)

        # DEFAULT → RANDOM STREAM
        else:
            last_a, last_b, last_c, last_result = run_logic_test()


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
#- Six_Gem_Logic_System_Dissertation.txt
#- Six_Gem_Logic_System_Dissertation_Suite.py
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
