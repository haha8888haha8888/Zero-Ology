# far.py
# Finite Arithmetic Reflection + Bespoke Equality Frameworks (FA-R + BEF)
# F stable version — November 2025
# Zero-Ology License v1.1922
# 0ko3maibZero-OlogyLicensev1.1922

from dataclasses import dataclass
from typing import Tuple, List, Dict, Any, Optional
import random
import os
from datetime import datetime

# ──────────────────────────────────────────────────────────────
# Logging setup — one log file per session in ./log_far/
# ──────────────────────────────────────────────────────────────
LOG_DIR = "log_far"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"far_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def log(msg: str):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")

log("=== FA-R + BEF session started ===")
# ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class FAR:
    digits: Tuple[int, ...]      # finite explicit digits after decimal point
    stage: int                   # explicit potential infinity tier

    def __repr__(self) -> str:
        if not self.digits:
            return f"0_s{self.stage}"
        d = " ".join(map(str, self.digits))
        return f"0.{d}_s{self.stage}"

    def length_under(self, policy: str = "digits") -> int:
        if policy == "digits":  return len(self.digits)
        if policy == "stage":   return self.stage
        if policy == "total":   return len(self.digits) + self.stage
        return 0


def eq(a: FAR, b: FAR, policy: str = "exact") -> bool:
    if policy == "exact":
        return (a.digits == b.digits) and (a.stage == b.stage)
    if policy == "stage":
        return a.stage == b.stage
    if policy == "length":
        return len(a.digits) == len(b.digits)
    return False


# ────────────────────── Safe arithmetic operations ──────────────────────
def add(a: FAR, b: FAR) -> FAR:
    return FAR(a.digits + b.digits, max(a.stage, b.stage) + 1)


def multiply(a: FAR, b: FAR) -> FAR:
    min_len = min(len(a.digits), len(b.digits))
    new_digits = tuple(
        (a.digits[i] * b.digits[i]) % 10
        for i in range(min_len)
    )
    return FAR(new_digits or (0,), a.stage + b.stage + 1)


def subtract(a: FAR, b: FAR) -> Optional[FAR]:
    """Gap-preserving subtraction — now 100% safe"""
    if eq(a, b, "exact"):
        log("SUBTRACTION REFUSED: Sacred Gap protection (exact self-cancellation blocked)")
        return None

    # Pad the shorter tuple with zeros on the right
    len_a, len_b = len(a.digits), len(b.digits)
    max_len = max(len_a, len_b)
    a_pad = a.digits + (0,) * (max_len - len_a)
    b_pad = b.digits + (0,) * (max_len - len_b)

    new_digits = tuple(
        max(0, a_pad[i] - b_pad[i])
        for i in range(max_len)
    )
    # Remove leading zeros but keep at least one digit
    cleaned = new_digits
    while len(cleaned) > 1 and cleaned[0] == 0:
        cleaned = cleaned[1:]
    return FAR(cleaned, max(a.stage, b.stage))


def invert(a: FAR) -> Optional[FAR]:
    if all(d == 0 for d in a.digits):
        return None
    return FAR(tuple(9 - d for d in a.digits), a.stage + 100)


def scale_stage(a: FAR, factor: int) -> FAR:
    return FAR(a.digits, a.stage * factor)


def slice_digits(a: FAR, length: int) -> FAR:
    return FAR(a.digits[:max(0, length)], a.stage)


def compare(a: FAR, b: FAR, policy: str = "digits") -> int:
    if policy == "digits":
        return (a.digits > b.digits) - (a.digits < b.digits)
    if policy == "stage":
        return (a.stage > b.stage) - (a.stage < b.stage)
    if policy == "combined":
        cd = (a.digits > b.digits) - (a.digits < b.digits)
        return cd if cd != 0 else (a.stage > b.stage) - (a.stage < b.stage)
    return 0


def random_far(length: int = 10, max_digit: int = 9, max_stage: int = 50) -> FAR:
    digits = tuple(random.randint(0, max_digit) for _ in range(length))
    stage = random.randint(1, max_stage)
    return FAR(digits, stage)


def limit_spectrum(seq: List[FAR]) -> Dict[str, Any]:
    if not seq:
        return {"empty": True}
    exact = seq[-1]
    longest = max(seq, key=lambda x: x.length_under("digits"))
    return {
        "exact_match": exact,
        "longest_by_digit_policy": longest,
        "all_stages": sorted({x.stage for x in seq}),
        "classical_R": "refused – no collapse permitted"
    }


# ────────────────────── Demo functions ──────────────────────
def demo_gap():
    log("Demo: Sacred Gap enforcement")
    nines = FAR(tuple([9] * 999), 999)
    one = FAR((1,), 0)
    log(f"0.999…_s999 = {nines}")
    log(f"Exact equality with 1? {eq(nines, one, 'exact')}")
    log(f"Stage-only equality with high stage? {eq(nines, FAR((), 999), 'stage')}")


def demo_spectrum():
    log("Demo: Convergence spectrum (no collapse)")
    seq = [FAR(tuple([9] * n), n) for n in range(1, 150)]
    print(limit_spectrum(seq))


def demo_addition():
    log("Demo: Non-commutative addition + stage rise")
    a = FAR((1,2,3,4,5), 7)
    b = FAR((8,8,8), 3)
    log(f"a + b → {add(a, b)}")
    log(f"b + a → {add(b, a)}")


def demo_infinitesimal():
    log("Demo: Pure infinitesimal")
    eps = FAR((0,)*500 + (1,), 9999)
    log(f"ε = {eps}")


def demo_invert():
    log("Demo: Partial inversion")
    a = FAR((1,2,3,7), 10)
    log(f"Invert {a} → {invert(a)}")


def demo_multiply():
    log("Demo: Tier-aware multiplication")
    a = FAR((1,2,3,4), 5)
    b = FAR((4,5,6), 2)
    log(f"{a} × {b} → {multiply(a, b)}")
    log(f"{b} × {a} → {multiply(b, a)}")


def demo_subtract():
    log("Demo: Gap-preserving subtraction")
    a = FAR((9,9,9,9,9), 6)
    b = FAR((1,2,3), 4)
    c = FAR((9,9,9,9,9), 6)
    log(f"{a} − {b} → {subtract(a, b)}")
    log(f"{b} − {a} → {subtract(b, a)}")
    log(f"{a} − {a} → {subtract(a, c)} (should be None)")


def demo_scale_stage():
    log("Demo: Stage scaling")
    a = FAR((1,2,3), 5)
    log(f"{a} → stage ×20 → {scale_stage(a, 20)}")


def demo_slice_digits():
    log("Demo: Spectral slicing")
    a = FAR(tuple(range(25)), 42)
    log(f"Original: {a}")
    log(f"First 8 digits: {slice_digits(a, 8)}")


def demo_compare():
    log("Demo: Policy-driven comparison")
    a = FAR((1,2,3), 10)
    b = FAR((1,2,4), 8)
    log(f"compare digits: {compare(a,b,'digits')}")
    log(f"compare stage : {compare(a,b,'stage')}")
    log(f"compare combined: {compare(a,b,'combined')}")


def demo_random_far():
    log("Demo: Random FAR generation")
    for _ in range(5):
        log(random_far(12, 9, 100))

def sector_7_dissertation():
    print(open("far.txt", "r", encoding="utf-8").read())

# ────────────────────── Interactive menu ──────────────────────
def menu():
    options = {
        "1": ("Sacred Gap", demo_gap),
        "2": ("Convergence Spectrum", demo_spectrum),
        "3": ("Non-commutative Addition", demo_addition),
        "4": ("Pure Infinitesimal", demo_infinitesimal),
        "5": ("Partial Inversion", demo_invert),
        "6": ("Tier-aware Multiplication", demo_multiply),
        "7": ("Gap-preserving Subtraction", demo_subtract),
        "8": ("Stage Scaling", demo_scale_stage),
        "9": ("Spectral Slicing", demo_slice_digits),
        "10": ("Policy Comparison", demo_compare),
        "11": ("Random FARs", demo_random_far),
        "12": ("View Dissertation", sector_7_dissertation),
        "q": ("Quit", None),
    }

    log("Menu started")
    print("\n=== FA-R + BEF — All 18 rejected rules active ===")
    print("Logs are automatically saved to ./log_far/\n")

    while True:
        print("─" * 55)
        for k, (desc, _) in options.items():
            if k != "q":
                print(f"{k:>2}. {desc}")
        print(" q. Quit")
        print("─" * 55)
        choice = input("\nChoose (Enter = 1): ").strip() or "1"

        if choice == "q":
            log("Session ended by user")
            print(f"\nSession log saved as: {LOG_FILE}")
            break
        if choice in options and options[choice][1]:
            print()
            log(f"Running demo #{choice}: {options[choice][0]}")
            options[choice][1]()
            input("\nPress Enter to continue...")
        else:
            log(f"Invalid menu choice: {choice}")
            print("Invalid choice.")


if __name__ == "__main__":
    menu()


# LICENSE.TXT
# Zero-Ology License v1.1922
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.1922
#November 22, 2025
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
#- far.py
#- Far.txt
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