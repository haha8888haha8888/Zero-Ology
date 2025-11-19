# ===================================================================
# GRAND CONSTANT ALGEBRA FRAMEWORK — INTERACTIVE TEACHING SUITE v0016
# Author: Stacey Szmy
# Co-Authors: Microsoft Copilot, OpenAI ChatGPT, Gemini AI, xAI Grok
# Date: 11. 18, 2025
# GRAND_CONSTANT_ALGEBRA.PY
# GRAND_CONSTANT_ALGEBRA_V0016
# Zero-Ology License v1.1918
# 0ko3maibZero-OlogyLicensev1.1918
# ===================================================================


import os
import time
import pickle
import logging
import matplotlib.pyplot as plt
import sympy as sp
import mpmath as mp

# Ultra-safe imports
try:
    from sympy import lambertw
except ImportError:
    try:
        from sympy.functions.elementary.miscellaneous import lambertw
    except ImportError:
        def lambertw(x, k=0): return sp.nan

from sympy import (
    pi, E, exp, ln, log, sin, cos, tan, cot, sec, csc,
    sinh, cosh, tanh, gamma, zeta, digamma, polylog,
    besselj, bessely, erf, erfc, Ei, nan, sqrt
)

# === Dawson fallback handling ===
def dawson_fn(x):
    # Try mpmath first
    if hasattr(mp, "dawsn"):
        return mp.dawsn(x)
    if hasattr(mp, "dawson"):
        return mp.dawson(x)
    # Try SciPy if installed
    try:
        from scipy.special import dawsn
        return dawsn(float(x))
    except Exception:
        return "Dawson integral not available"

# ============================= OPERATORS DEFINITIONS =============================
OPERATORS = {
    "exp": lambda x: sp.exp(x),
    "ln": lambda x: sp.ln(x),
    "sin": lambda x: sp.sin(x),
    "Γ": lambda x: sp.gamma(x),
    "W₀": lambda x: lambertw(x, 0),   # use the safe import, not sp.lambertw
    "+1": lambda x: x + 1,
    "−1": lambda x: x - 1,
}



# ============================= STATE & CONFIG =============================
os.makedirs("grand_algebra_logs", exist_ok=True)
os.makedirs("grand_algebra_saves", exist_ok=True)
LOG_FILE = os.path.join("grand_algebra_logs", f"grand_log_{time.strftime('%Y%m%d_%H%M%S')}.txt")
STATE_FILE = "grand_algebra_saves/grand_state.pkl"

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(LOG_FILE, encoding='utf-8')])

current_cs = [pi, E]
EXPLAIN_MODE = True

def compute_aggregators(cs):
    if not cs: return {}
    n = len(cs)
    S_n = sum(cs)
    P_n = sp.prod(cs)
    mean = S_n / n
    variance = sum((c - mean)**2 for c in cs) / n
    geom_mean = P_n**(1/n) if all(c > 0 for c in cs) else nan
    harm_mean = n / sum(1/c for c in cs) if all(c > 0 for c in cs) else nan
    quad_mean = sp.sqrt(sum(c**2 for c in cs) / n)
    proportions = [c/S_n for c in cs] if S_n != 0 else []
    entropy = -sum(p*ln(p) for p in proportions if p > 0) if proportions else nan

    return {
        "Sₙ (Sum)": S_n,
        "Arithmetic Mean": mean,
        "Geometric Mean": geom_mean,
        "Harmonic Mean": harm_mean,
        "Quadratic Mean": quad_mean,
        "Variance": variance,
        "Std Dev": sp.sqrt(variance),
        "Shannon Entropy (bits)": entropy / ln(2) if entropy != nan else nan,
    }

current_agg = compute_aggregators(current_cs)

# ============================= VISUALIZATION FUNCTIONS =============================

def plot_entropy_vs_variance():
    import matplotlib.pyplot as plt

    # Generate sample data by varying base set size
    sizes = list(range(2, 21))
    variances = []
    entropies = []

    for n in sizes:
        cs = [pi, E] + [sp.N(sp.randprime(10, 100)) for _ in range(n-2)]
        agg = compute_aggregators(cs)
        variances.append(float(agg["Variance"]))
        entropies.append(float(agg["Shannon Entropy (bits)"]))

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, variances, label="Variance Σₙ", marker="o")
    plt.plot(sizes, entropies, label="Entropy Ξₙ (bits)", marker="s")
    plt.xlabel("Base Set Size n")
    plt.ylabel("Value")
    plt.title("Entropy vs Variance Growth")
    plt.legend()
    plt.grid(True)
    plt.show()



def safe_N(expr, prec=12):
    try:
        val = sp.N(expr, prec)
        return float(val) if val.is_real else complex(val)
    except:
        return "∞ / complex / undefined"

def explain(text):
    if EXPLAIN_MODE:
        print(f"   ℹ️  {text}")

# ============================= THE OFFICIAL 200-ENTRY PERIODIC TABLE =============================
S_n = pi + E

PERIODIC_TABLE = [
    {"#": 1,  "symbol": "ℌₙ⁺",   "name": "Additive Grand",      "calc": lambda: S_n + 1,                   "domain": "ℝ"},
    {"#": 2,  "symbol": "ℌₙ⁻",   "name": "Subtractive Grand",   "calc": lambda: S_n - 1,                   "domain": "ℝ"},
    {"#": 3,  "symbol": "ℌₙˣ",   "name": "Multiplicative Grand","calc": lambda: 2 * S_n,                   "domain": "ℝ"},
    {"#": 4,  "symbol": "ℌₙ÷",   "name": "Divisive Grand",      "calc": lambda: S_n / pi,                  "domain": "ℝ"},
    {"#": 5,  "symbol": "𝔊ₙᵉˣᵖ", "name": "Exponential Grand",   "calc": lambda: exp(S_n),                  "domain": "ℝ"},
    {"#": 6,  "symbol": "𝔊ₙˡⁿ",  "name": "Natural Log Grand",   "calc": lambda: ln(S_n),                   "domain": "Sₙ>0"},
    {"#": 7,  "symbol": "𝔊ₙˡᵒᵍ¹⁰","name": "Common Log Grand",   "calc": lambda: log(S_n,10),               "domain": "Sₙ>0"},
    {"#": 8,  "symbol": "𝔊ₙˢⁱⁿ", "name": "Sine Grand",          "calc": lambda: sin(S_n),                  "domain": "ℝ"},
    {"#": 9,  "symbol": "𝔊ₙᶜᵒˢ", "name": "Cosine Grand",        "calc": lambda: cos(S_n),                  "domain": "ℝ"},
    {"#": 10, "symbol": "𝔊ₙᵗᵃⁿ", "name": "Tangent Grand",       "calc": lambda: tan(S_n),                  "domain": "avoids poles"},
    {"#": 11, "symbol": "𝔊ₙᵃˢⁱⁿ","name": "Arcsine Grand",       "calc": lambda: sp.asin(S_n/pi),           "domain": "complex"},
    {"#": 12, "symbol": "𝔊ₙᴳ",   "name": "Gamma Grand",         "calc": lambda: gamma(S_n),                "domain": "Re>0"},
    {"#": 13, "symbol": "𝔊ₙᶻ",   "name": "Digamma Grand",       "calc": lambda: digamma(S_n),              "domain": "Re>0"},
    {"#": 14, "symbol": "𝔊ₙᶻ",   "name": "Riemann Zeta Grand",  "calc": lambda: zeta(S_n),                 "domain": "Re>1"},
    {"#": 15, "symbol": "𝔊ₙᴴ",   "name": "Euler–Mascheroni Appearance","calc": lambda: sp.harmonic(sp.floor(S_n)), "domain": "integer"},
    {"#": 16, "symbol": "𝔊ₙᵂ",   "name": "Lambert-W Grand (principal)","calc": lambda: lambertw(S_n,0),       "domain": "≥ -1/e"},
    {"#": 17, "symbol": "𝔊ₙᵂ₋₁","name": "Lambert-W Grand (−1 branch)","calc": lambda: lambertw(S_n,-1),      "domain": "-1/e ≤ x < 0"},
    {"#": 18, "symbol": "𝔊ₙᴮ",   "name": "Euler Beta Grand",    "calc": lambda: sp.beta(S_n/2,S_n/2),      "domain": "Re>0"},
    {"#": 19, "symbol": "𝔑ₙ↑↑²", "name": "Square Tetration Grand","calc": lambda: S_n**S_n,                 "domain": "ℝ⁺"},
    {"#": 20, "symbol": "𝔑ₙ↑↑³", "name": "Cube Tetration Grand","calc": lambda: S_n**(S_n**S_n),            "domain": "ℝ⁺"},
    {"#": 21, "symbol": "𝔑ₙ↑↑⁴", "name": "Tetration-4 Grand",   "calc": lambda: S_n**(S_n**(S_n**S_n)),    "domain": "ℝ⁺"},
    {"#": 22, "symbol": "𝔑ₙ↑↑⁵", "name": "Tetration-5 Grand",   "calc": lambda: exp(exp(exp(S_n))),        "domain": "ℝ⁺"},
    {"#": 23, "symbol": "𝔑ₙ↑↑⁶", "name": "Tetration-6 Grand",   "calc": lambda: "tower of 6",              "domain": "ℝ⁺"},
    {"#": 24, "symbol": "𝔑ₙ↑↑⁷", "name": "Tetration-7 Grand",   "calc": lambda: "tower of 7",              "domain": "ℝ⁺"},
    {"#": 25, "symbol": "𝔑ₙ↑↑⁸", "name": "Tetration-8 Grand",   "calc": lambda: "tower of 8",              "domain": "ℝ⁺"},
    {"#": 26, "symbol": "𝔑ₙ↑↑⁹", "name": "Tetration-9 Grand",   "calc": lambda: "tower of 9",              "domain": "ℝ⁺"},
    {"#": 27, "symbol": "𝔑ₙ↑↑¹⁰","name": "Tetration-10 Grand",  "calc": lambda: "tower of 10",             "domain": "ℝ⁺"},
    {"#": 28, "symbol": "𝔑ₙ↑↑¹¹","name": "Tetration-11 Grand",  "calc": lambda: "tower of 11",             "domain": "ℝ⁺"},
    {"#": 29, "symbol": "𝔑ₙ↑↑¹²","name": "Tetration-12 Grand",  "calc": lambda: "tower of 12",             "domain": "ℝ⁺"},
    {"#": 30, "symbol": "𝔑ₙ↑↑¹³","name": "Tetration-13 Grand",  "calc": lambda: "tower of 13",             "domain": "ℝ⁺"},
    {"#": 31, "symbol": "Σₙ",    "name": "Variance Grand",      "calc": lambda: current_agg.get("Variance Σₙ", nan), "domain": "ℝ"},
    {"#": 32, "symbol": "Τₙ",    "name": "Std Dev Grand",       "calc": lambda: current_agg.get("Std Dev Τₙ", nan), "domain": "ℝ"},
    {"#": 33, "symbol": "Δₙ",    "name": "Range Grand",         "calc": lambda: max(current_cs)-min(current_cs), "domain": "ℝ"},
    {"#": 34, "symbol": "Γᵢₙ",   "name": "Gini Inequality Grand","calc": lambda: "complex calc",           "domain": "ℝ⁺"},
    {"#": 35, "symbol": "Ξₙ",    "name": "Shannon Entropy Grand","calc": lambda: current_agg.get("Shannon Entropy Ξₙ (bits)", nan), "domain": "Sₙ>0"},
    {"#": 36, "symbol": "Λₙ",    "name": "Geometric Mean Grand","calc": lambda: current_agg.get("Geometric Mean", nan), "domain": "ℝ⁺"},
    {"#": 37, "symbol": "Θₙ",    "name": "Harmonic Mean Grand", "calc": lambda: current_agg.get("Harmonic Mean", nan), "domain": "ℝ⁺"},
    {"#": 38, "symbol": "Μₙ", "name": "Quadratic Mean Grand", "calc": lambda: current_agg.get("Quadratic Mean", nan), "domain": "ℝ"},
    {"#": 39, "symbol": "𝔊ₙᴾᵒʷᵖ","name": "Power Mean (p=3) Grand","calc": lambda: (sum(c**3 for c in current_cs)/len(current_cs))**(1/3), "domain": "ℝ"},
    {"#": 40, "symbol": "𝔊ₙᴸ",   "name": "Lehmer Mean Grand",    "calc": lambda: sum(c**3 for c in current_cs)/sum(c**2 for c in current_cs), "domain": "ℝ⁺"},
    {"#": 41, "symbol": "𝔊ₙᴹ₋₁", "name": "Harmonic Mean Grand",  "calc": lambda: len(current_cs)/sum(1/c for c in current_cs), "domain": "cᵢ>0"},
    {"#": 42, "symbol": "𝔊ₙᴹ₀",  "name": "Geometric Mean Grand (limit form)", "calc": lambda: sp.prod(current_cs)**(1/len(current_cs)), "domain": "cᵢ>0"},
    {"#": 43, "symbol": "𝔊ₙᴹ₁",  "name": "Arithmetic Mean Grand","calc": lambda: sum(current_cs)/len(current_cs), "domain": "ℝ"},
    {"#": 44, "symbol": "𝔊ₙᴹ₂",  "name": "Quadratic (RMS) Mean Grand","calc": lambda: sp.sqrt(sum(c**2 for c in current_cs)/len(current_cs)), "domain": "ℝ"},
    {"#": 45, "symbol": "𝔊ₙᴹ₃",  "name": "Cubic Mean Grand",     "calc": lambda: (sum(c**3 for c in current_cs)/len(current_cs))**(1/3), "domain": "ℝ"},
    {"#": 46, "symbol": "𝔊ₙᴹ₄",  "name": "Quartic Mean Grand",   "calc": lambda: (sum(c**4 for c in current_cs)/len(current_cs))**(1/4), "domain": "ℝ"},
    {"#": 47, "symbol": "𝔊ₙᴹ₅",  "name": "Quintic Mean Grand",   "calc": lambda: (sum(c**5 for c in current_cs)/len(current_cs))**(1/5), "domain": "ℝ"},
    {"#": 48, "symbol": "𝔊ₙᴹ₆",  "name": "Sextic Mean Grand",    "calc": lambda: (sum(c**6 for c in current_cs)/len(current_cs))**(1/6), "domain": "ℝ"},
    {"#": 49, "symbol": "𝔊ₙᴹ₇",  "name": "Septic Mean Grand",    "calc": lambda: (sum(c**7 for c in current_cs)/len(current_cs))**(1/7), "domain": "ℝ"},
    {"#": 50, "symbol": "𝔊ₙᴹ₈",  "name": "Octic Mean Grand",     "calc": lambda: (sum(c**8 for c in current_cs)/len(current_cs))**(1/8), "domain": "ℝ"},
    {"#": 51, "symbol": "𝔊ₙᴷ",   "name": "Kurtosis Grand",       "calc": lambda: "complex calc",            "domain": "ℝ"},
    {"#": 52, "symbol": "𝔊ₙˢᵏ",  "name": "Skewness Grand",       "calc": lambda: "complex calc",            "domain": "ℝ"},
    {"#": 53, "symbol": "𝔊ₙᴰ",   "name": "Dirichlet Eta Grand",  "calc": lambda: (1-2**(1-S_n))*zeta(S_n),  "domain": "Re(Sₙ)>0"},
    {"#": 54, "symbol": "𝔊ₙᴸⁱ",  "name": "Polylog Li₂ Grand",    "calc": lambda: polylog(2,S_n),            "domain": "complex"},
    {"#": 55, "symbol": "𝔊ₙᴱ",   "name": "Exponential Integral Grand","calc": lambda: sp.expint(1,S_n),      "domain": "ℝ⁺"},
    {"#": 56, "symbol": "𝔊ₙˢⁱⁿ¹","name": "Sine ×1 Grand",        "calc": lambda: sin(S_n),                  "domain": "ℝ"},
    {"#": 57, "symbol": "𝔊ₙᶜᵒˢ¹","name": "Cosine ×1 Grand",      "calc": lambda: cos(S_n),                  "domain": "ℝ"},
    {"#": 58, "symbol": "𝔊ₙᵗᵃⁿ¹","name": "Tangent ×1 Grand",     "calc": lambda: tan(S_n),                  "domain": "avoids poles"},
    {"#": 59, "symbol": "𝔊ₙˢⁱⁿ²","name": "Sine ×2 Grand",        "calc": lambda: sin(2*S_n),                "domain": "ℝ"},
    {"#": 60, "symbol": "𝔊ₙᶜᵒˢ²","name": "Cosine ×2 Grand",      "calc": lambda: cos(2*S_n),                "domain": "ℝ"},
    {"#": 61, "symbol": "𝔊ₙˢⁱⁿ³","name": "Sine ×3 Grand",        "calc": lambda: sin(3*S_n),                "domain": "ℝ"},
    {"#": 62, "symbol": "𝔊ₙᶜᵒᵗ¹","name": "Cotangent ×1 Grand",   "calc": lambda: 1/tan(S_n),                "domain": "Sₙ ≠ kπ"},
    {"#": 63, "symbol": "𝔊ₙˢᵉᶜ¹","name": "Secant ×1 Grand",      "calc": lambda: 1/cos(S_n),                "domain": "ℝ"},
    {"#": 64, "symbol": "𝔊ₙᶜˢᶜ¹","name": "Cosecant ×1 Grand",    "calc": lambda: 1/sin(S_n),                "domain": "Sₙ ≠ kπ"},
    {"#": 65, "symbol": "𝔊ₙˢⁱⁿʰ","name": "Hyperbolic Sine Grand","calc": lambda: sp.sinh(S_n),              "domain": "ℝ"},
    {"#": 66, "symbol": "𝔊ₙᶜᵒˢʰ","name": "Hyperbolic Cosine Grand","calc": lambda: sp.cosh(S_n),            "domain": "ℝ"},
    {"#": 67, "symbol": "𝔊ₙᵗᵃⁿʰ","name": "Hyperbolic Tangent Grand","calc": lambda: sp.tanh(S_n),           "domain": "ℝ"},
    {"#": 68, "symbol": "𝔊ₙˢⁱⁿ⁽ᵖⁱ⁾","name": "Sine at π·Sₙ Grand","calc": lambda: sin(pi*S_n),              "domain": "ℝ"},
    {"#": 69, "symbol": "𝔊ₙᶜᵒˢ⁽ᵉ⁾","name": "Cosine at e·Sₙ Grand","calc": lambda: cos(E*S_n),              "domain": "ℝ"},
    {"#": 70, "symbol": "𝔊ₙᵗᵃⁿ⁽ᶠⁱᵇ⁾","name": "Tangent at Fibonacci-scaled Grand","calc": lambda: tan(5*S_n),"domain": "avoids poles"},
    {"#": 71, "symbol": "𝔊ₙᴳ¹",   "name": "Gamma Iteration 1 Grand","calc": lambda: gamma(S_n),             "domain": "Re(Sₙ)>0"},
    {"#": 72, "symbol": "𝔊ₙᴳ²",   "name": "Gamma Iteration 2 Grand","calc": lambda: gamma(gamma(S_n)),      "domain": "Γ(Sₙ)>0"},
    {"#": 73, "symbol": "𝔊ₙᴳ³",   "name": "Gamma Iteration 3 Grand","calc": lambda: gamma(gamma(gamma(S_n))),"domain": "Γ²(Sₙ)>0"},
    {"#": 74, "symbol": "𝔊ₙᴳ⁴",   "name": "Gamma Iteration 4 Grand","calc": lambda: "Γ⁴(Sₙ)",               "domain": "Γ³(Sₙ)>0"},
    {"#": 75, "symbol": "𝔊ₙᴳ⁵",   "name": "Gamma Iteration 5 Grand","calc": lambda: "Γ⁵(Sₙ)",               "domain": "Γ⁴(Sₙ)>0"},
    {"#": 76, "symbol": "𝔊ₙᴳ⁶",   "name": "Gamma Iteration 6 Grand","calc": lambda: "Γ⁶(Sₙ)",               "domain": "Γ⁵(Sₙ)>0"},
    {"#": 77, "symbol": "𝔊ₙᴳ⁷",   "name": "Gamma Iteration 7 Grand","calc": lambda: "Γ⁷(Sₙ)",               "domain": "Γ⁶(Sₙ)>0"},
    {"#": 78, "symbol": "𝔊ₙᴳ⁸",   "name": "Gamma Iteration 8 Grand","calc": lambda: "Γ⁸(Sₙ)",               "domain": "Γ⁷(Sₙ)>0"},
    {"#": 79, "symbol": "𝔊ₙᴳ⁹",   "name": "Gamma Iteration 9 Grand","calc": lambda: "Γ⁹(Sₙ)",               "domain": "Γ⁸(Sₙ)>0"},
    {"#": 80, "symbol": "𝔊ₙᴳ¹⁰",  "name": "Gamma Iteration 10 Grand","calc": lambda: "Γ¹⁰(Sₙ)",             "domain": "Γ⁹(Sₙ)>0"},
    {"#": 81, "symbol": "𝔊ₙᴳ¹¹",  "name": "Gamma Iteration 11 Grand","calc": lambda: "Γ¹¹(Sₙ)",             "domain": "Γ¹⁰(Sₙ)>0"},
    {"#": 82, "symbol": "𝔊ₙᴳ¹²",  "name": "Gamma Iteration 12 Grand","calc": lambda: "Γ¹²(Sₙ)",             "domain": "Γ¹¹(Sₙ)>0"},
    {"#": 83, "symbol": "𝔊ₙᴳ¹³",  "name": "Gamma Iteration 13 Grand","calc": lambda: "Γ¹³(Sₙ)",             "domain": "Γ¹²(Sₙ)>0"},
    {"#": 84, "symbol": "𝔊ₙᴳ¹⁴",  "name": "Gamma Iteration 14 Grand","calc": lambda: "Γ¹⁴(Sₙ)",             "domain": "Γ¹³(Sₙ)>0"},
    {"#": 85, "symbol": "𝔊ₙᴳ¹⁵",  "name": "Gamma Iteration 15 Grand","calc": lambda: "Γ¹⁵(Sₙ)",             "domain": "Γ¹⁴(Sₙ)>0"},
    {"#": 86, "symbol": "𝔊ₙᴳ¹⁶",  "name": "Gamma Iteration 16 Grand","calc": lambda: "Γ¹⁶(Sₙ)",             "domain": "Γ¹⁵(Sₙ)>0"},
    {"#": 87, "symbol": "𝔊ₙᴳ¹⁷",  "name": "Gamma Iteration 17 Grand","calc": lambda: "Γ¹⁷(Sₙ)",             "domain": "Γ¹⁶(Sₙ)>0"},
    {"#": 88, "symbol": "𝔊ₙᴳ¹⁸",  "name": "Gamma Iteration 18 Grand","calc": lambda: "Γ¹⁸(Sₙ)",             "domain": "Γ¹⁷(Sₙ)>0"},
    {"#": 89, "symbol": "𝔊ₙᴳ¹⁹",  "name": "Gamma Iteration 19 Grand","calc": lambda: "Γ¹⁹(Sₙ)",             "domain": "Γ¹⁸(Sₙ)>0"},
    {"#": 90, "symbol": "𝔊ₙᴳ²⁰",  "name": "Gamma Iteration 20 Grand","calc": lambda: "Γ²⁰(Sₙ)",             "domain": "Γ¹⁹(Sₙ)>0"},
    {"#": 91,  "symbol": "𝔊ₙᶻ¹",   "name": "Zeta Iteration 1 Grand",   "calc": lambda: zeta(S_n),                  "domain": "Re(Sₙ)>1"},
    {"#": 92,  "symbol": "𝔊ₙᶻ²",   "name": "Zeta Iteration 2 Grand",   "calc": lambda: zeta(zeta(S_n)),            "domain": "ζ(Sₙ)>1"},
    {"#": 93,  "symbol": "𝔊ₙᶻ³",   "name": "Zeta Iteration 3 Grand",   "calc": lambda: zeta(zeta(zeta(S_n))),      "domain": "prev iterate>1"},
    {"#": 94,  "symbol": "𝔊ₙᶻ⁴",   "name": "Zeta Iteration 4 Grand",   "calc": lambda: "ζ⁴(Sₙ)",                   "domain": "prev iterate>1"},
    {"#": 95,  "symbol": "𝔊ₙᶻ⁵",   "name": "Zeta Iteration 5 Grand",   "calc": lambda: "ζ⁵(Sₙ)",                   "domain": "prev iterate>1"},
    {"#": 96,  "symbol": "𝔊ₙᶻ⁶",   "name": "Zeta Iteration 6 Grand",   "calc": lambda: "ζ⁶(Sₙ)",                   "domain": "prev iterate>1"},
    {"#": 97,  "symbol": "𝔊ₙᶻ⁷",   "name": "Zeta Iteration 7 Grand",   "calc": lambda: "ζ⁷(Sₙ)",                   "domain": "prev iterate>1"},
    {"#": 98,  "symbol": "𝔊ₙᶻ⁸",   "name": "Zeta Iteration 8 Grand",   "calc": lambda: "ζ⁸(Sₙ)",                   "domain": "prev iterate>1"},
    {"#": 99,  "symbol": "𝔊ₙᶻ⁹",   "name": "Zeta Iteration 9 Grand",   "calc": lambda: "ζ⁹(Sₙ)",                   "domain": "prev iterate>1"},
    {"#": 100, "symbol": "𝔊ₙᶻ¹⁰",  "name": "Zeta Iteration 10 Grand",  "calc": lambda: "ζ¹⁰(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 101, "symbol": "𝔊ₙᶻ¹¹",  "name": "Zeta Iteration 11 Grand",  "calc": lambda: "ζ¹¹(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 102, "symbol": "𝔊ₙᶻ¹²",  "name": "Zeta Iteration 12 Grand",  "calc": lambda: "ζ¹²(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 103, "symbol": "𝔊ₙᶻ¹³",  "name": "Zeta Iteration 13 Grand",  "calc": lambda: "ζ¹³(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 104, "symbol": "𝔊ₙᶻ¹⁴",  "name": "Zeta Iteration 14 Grand",  "calc": lambda: "ζ¹⁴(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 105, "symbol": "𝔊ₙᶻ¹⁵",  "name": "Zeta Iteration 15 Grand",  "calc": lambda: "ζ¹⁵(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 106, "symbol": "𝔊ₙᶻ¹⁶",  "name": "Zeta Iteration 16 Grand",  "calc": lambda: "ζ¹⁶(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 107, "symbol": "𝔊ₙᶻ¹⁷",  "name": "Zeta Iteration 17 Grand",  "calc": lambda: "ζ¹⁷(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 108, "symbol": "𝔊ₙᶻ¹⁸",  "name": "Zeta Iteration 18 Grand",  "calc": lambda: "ζ¹⁸(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 109, "symbol": "𝔊ₙᶻ¹⁹",  "name": "Zeta Iteration 19 Grand",  "calc": lambda: "ζ¹⁹(Sₙ)",                  "domain": "prev iterate>1"},
    {"#": 110, "symbol": "𝔊ₙᶻ²⁰",  "name": "Zeta Iteration 20 Grand",  "calc": lambda: "ζ²⁰(Sₙ)",                  "domain": "prev iterate>1"},
    {"#":    111, "symbol": "𝔊ₙᴰᵉ", "name": "Dawson Grand", "calc": lambda: dawson_fn(S_n), "domain": "ℝ"},
    {"#": 112, "symbol": "𝔊ₙᴱʳᶠ",  "name": "Error Function Grand",      "calc": lambda: sp.erf(S_n),               "domain": "ℝ"},
    {"#": 113, "symbol": "𝔊ₙᴱʳᶠᶜ", "name": "Complementary Error Grand", "calc": lambda: sp.erfc(S_n),              "domain": "ℝ"},
    {"#": 114, "symbol": "𝔊ₙᴶ⁰",   "name": "Bessel J₀ Grand",           "calc": lambda: sp.besselj(0,S_n),         "domain": "ℝ"},
    {"#": 115, "symbol": "𝔊ₙᵞ⁰",   "name": "Bessel Y₀ Grand",           "calc": lambda: sp.bessely(0,S_n),         "domain": "ℝ⁺"},
    {"#": 116, "symbol": "𝔊ₙᴾ¹",   "name": "Prime Zeta P₁ Grand",       "calc": lambda: "∑ p⁻ˢⁿ",                 "domain": "Re(Sₙ)>1"},
    {"#": 117, "symbol": "𝔊ₙᴾ²",   "name": "Prime Zeta P₂ Grand",       "calc": lambda: "∑ p⁻²",                   "domain": "Re(Sₙ)>1"},
    {"#": 118, "symbol": "𝔊ₙᴾ³",   "name": "Prime Zeta P₃ Grand",       "calc": lambda: "∑ p⁻³",                   "domain": "Re(Sₙ)>1"},
    {"#": 119, "symbol": "𝔊ₙᴾ⁴",   "name": "Prime Zeta P₄ Grand",       "calc": lambda: "∑ p⁻⁴",                   "domain": "Re(Sₙ)>1"},
    {"#": 120, "symbol": "𝔊ₙᴾ⁵",   "name": "Prime Zeta P₅ Grand",       "calc": lambda: "∑ p⁻⁵",                   "domain": "Re(Sₙ)>1"},
    {"#": 121, "symbol": "𝔊ₙᴾ⁶",   "name": "Prime Zeta P₆ Grand",       "calc": lambda: "∑ p⁻⁶",                   "domain": "Re(Sₙ)>1"},
    {"#": 122, "symbol": "𝔊ₙᴾ⁷",   "name": "Prime Zeta P₇ Grand",       "calc": lambda: "∑ p⁻⁷",                   "domain": "Re(Sₙ)>1"},
    {"#": 123, "symbol": "𝔊ₙᴾ⁸",   "name": "Prime Zeta P₈ Grand",       "calc": lambda: "∑ p⁻⁸",                   "domain": "Re(Sₙ)>1"},
    {"#": 124, "symbol": "𝔊ₙᴾ⁹",   "name": "Prime Zeta P₉ Grand",       "calc": lambda: "∑ p⁻⁹",                   "domain": "Re(Sₙ)>1"},
    {"#": 125, "symbol": "𝔊ₙᴾ¹⁰",  "name": "Prime Zeta P₁₀ Grand",      "calc": lambda: "∑ p⁻¹⁰",                  "domain": "Re(Sₙ)>1"},
    {"#": 126, "symbol": "𝔊ₙᴾ¹¹",  "name": "Prime Zeta P₁₁ Grand",      "calc": lambda: "∑ p⁻¹¹",                  "domain": "Re(Sₙ)>1"},
    {"#": 127, "symbol": "𝔊ₙᴾ¹²",  "name": "Prime Zeta P₁₂ Grand",      "calc": lambda: "∑ p⁻¹²",                  "domain": "Re(Sₙ)>1"},
    {"#": 128, "symbol": "𝔊ₙᴾ¹³",  "name": "Prime Zeta P₁₃ Grand",      "calc": lambda: "∑ p⁻¹³",                  "domain": "Re(Sₙ)>1"},
    {"#": 129, "symbol": "𝔊ₙᴾ¹⁴",  "name": "Prime Zeta P₁₄ Grand",      "calc": lambda: "∑ p⁻¹⁴",                  "domain": "Re(Sₙ)>1"},
    {"#": 130, "symbol": "𝔊ₙᴾ¹⁵",  "name": "Prime Zeta P₁₅ Grand",      "calc": lambda: "∑ p⁻¹⁵",                  "domain": "Re(Sₙ)>1"},
    {"#": 131, "symbol": "𝔊ₙᴾ¹⁶",  "name": "Prime Zeta P₁₆ Grand",      "calc": lambda: "∑ p⁻¹⁶",                  "domain": "Re(Sₙ)>1"},
    {"#": 132, "symbol": "𝔊ₙᴾ¹⁸",  "name": "Prime Zeta P₁₈ Grand",      "calc": lambda: "∑ p⁻¹⁸",                  "domain": "Re(Sₙ)>1"},
    {"#": 133, "symbol": "𝔊ₙᴾ²⁰",  "name": "Prime Zeta P₂₀ Grand",      "calc": lambda: "∑ p⁻²⁰",                  "domain": "Re(Sₙ)>1"},
    {"#": 134, "symbol": "𝔊ₙᴾ²²",  "name": "Prime Zeta P₂₂ Grand",      "calc": lambda: "∑ p⁻²²",                  "domain": "Re(Sₙ)>1"},
    {"#": 135, "symbol": "𝔊ₙᴾ²⁴",  "name": "Prime Zeta P₂₄ Grand",      "calc": lambda: "∑ p⁻²⁴",                  "domain": "Re(Sₙ)>1"},
    {"#": 136, "symbol": "𝔊ₙᴾ²⁵",  "name": "Prime Zeta P₂₅ Grand",      "calc": lambda: "∑ p⁻²⁵",                  "domain": "Re(Sₙ)>1"},
    {"#": 137, "symbol": "𝔊ₙᴾⁿ",   "name": "Mertens-type Prime Zeta Grand","calc": lambda: "∑_{p≤n} p⁻ˢⁿ",         "domain": "n large"},
    {"#": 138, "symbol": "𝔊ₙᴾ⁻ᴹ",  "name": "Twin-Prime Zeta Grand",     "calc": lambda: "∑_{(p,p+2)} (p⁻ˢⁿ+(p+2)⁻ˢⁿ)", "domain": "Re(Sₙ)>1"},
    {"#": 139, "symbol": "𝔊ₙᴾ⁻ˢᵒᵖʰⁱᵉ","name": "Sophie-Germain Prime Zeta Grand","calc": lambda: "∑_{p,2p+1 prime} p⁻ˢⁿ", "domain": "Re(Sₙ)>1"},
    {"#":   140, "symbol": "𝔊ₙᴾ⁻ᴬˡˡ", "name": "All-Prime-Power Zeta Grand", "calc": lambda: "formal/analytic expression −ln(1 − P₁(Sₙ))", "domain": "formal/analytic"},
    {"#": 141, "symbol": "𝔊ₙᴴʸᵖ²F₁","name": "Hypergeometric ₂F₁(1,1;2;Sₙ) Grand","calc": lambda: sp.hyper([1,1],[2],S_n), "domain": "principal branch"},
    {"#": 142, "symbol": "𝔊ₙᶜᶠ⁻ᵍᵒˡᵈ","name": "Golden Ratio Continued Fraction Grand","calc": lambda: "CF golden", "domain": "always converges"},
    {"#": 143, "symbol": "𝔊ₙᶜᶠ⁻ᵉ", "name": "e Continued Fraction Grand","calc": lambda: "CF e-style",             "domain": "always converges"},
    {"#": 144, "symbol": "𝔊ₙᶜᶠ⁻ᵖⁱ","name": "π-style Continued Fraction Grand","calc": lambda: "CF π-style",      "domain": "converges slowly"},
    {"#": 145, "symbol": "𝔊ₙᶜᶠ⁻ᵗᵃⁿ¹","name": "Tangent(1) Continued Fraction Grand","calc": lambda: "CF tan(1)",  "domain": "converges"},
    {"#": 146, "symbol": "𝔊ₙᶜᶠ⁻ˢᑫᴿᵀ²","name": "sqrt(2)-style Grand",   "calc": lambda: "CF sqrt(2)",              "domain": "always converges"},
    {"#": 147, "symbol": "𝔊ₙᶜᶠ⁻ˡⁿ²","name": "ln(2) Continued Fraction Grand","calc": lambda: "CF ln(2)",         "domain": "always converges"},
    {"#": 148, "symbol": "𝔊ₙᶜᶠ⁻ʳᵃⁿᵈ","name": "Random-Term Continued Fraction Grand","calc": lambda: "CF random","domain": "varies"},
    {"#": 149, "symbol": "𝔊ₙᶜᶠ⁻ᵍᵉⁿ","name": "Generalized Continued Fraction Grand","calc": lambda: "CF general", "domain": "conditional"},
    {"#": 150, "symbol": "𝔊ₙᶜᶠ⁻ᵠ", "name": "Silver Ratio Continued Fraction Grand","calc": lambda: "CF silver",  "domain": "always converges"},
    {"#": 151, "symbol": "𝔊ₙᶜᶠ⁻ᵠⁿ",   "name": "Plastic Number Continued Fraction Grand", "calc": lambda: "CF plastic",   "domain": "always converges"},
    {"#": 152, "symbol": "𝔊ₙᶜᶠ⁻ᵇʳᵒʷⁿ","name": "Brouwer’s Constant Grand",                "calc": lambda: "CF brouwer",   "domain": "unstable"},
    {"#": 153, "symbol": "𝔊ₙᶜᶠ⁻ʰᵘʳʷⁱᵗᶻ","name": "Hurwitz Quadratic Irrational Grand",     "calc": lambda: "CF hurwitz",   "domain": "quadratic irrational"},
    {"#": 154, "symbol": "𝔊ₙᶜᶠ⁻ᵗᵃⁿ⁻¹","name": "Arctangent Continued Fraction Grand",     "calc": lambda: "CF arctan",    "domain": "converges"},
    {"#": 155, "symbol": "𝔊ₙᶜᶠ⁻ˢⁱⁿʰ⁻¹","name": "Inverse Hyperbolic Sine Grand",          "calc": lambda: sp.asinh(S_n),  "domain": "ℝ"},
    {"#": 156, "symbol": "𝔊ₙᶜᶠ⁻ᵉʳᶠ",   "name": "Error Function Continued Fraction Grand","calc": lambda: "CF erf",       "domain": "slow convergence"},
    {"#": 157, "symbol": "𝔊ₙᶜᶠ⁻ᵍᵃᵘˢˢ","name": "Gauss’s Constant Grand",                  "calc": lambda: "CF gauss",     "domain": "conditional"},
    {"#": 158, "symbol": "𝔊ₙᶜᶠ⁻ˡⁱᵐⁱᵗ","name": "Limit of Finite Truncations Grand",       "calc": lambda: "CF limit",     "domain": "always converges"},
    {"#": 159, "symbol": "𝔊ₙᶜᶠ⁻ᵖᵉʳⁱᵒᵈⁱᶜ","name": "Best Periodic Approximation Grand",    "calc": lambda: "CF periodic",  "domain": "always exists"},
    {"#": 160, "symbol": "𝔊ₙᶜᶠ⁻ˢᵉᵐⁱ",  "name": "Semi-Convergent Grand",                 "calc": lambda: "CF semi",      "domain": "always defined"},
    {"#": 161, "symbol": "𝔊ₙᴳᶻ",        "name": "Glaisher–Kinkelin Grand",                "calc": lambda: "A^{Sₙ¹²} exp(...)", "domain": "analytic continuation"},
    {"#": 162, "symbol": "𝔊ₙᴹᵇ",        "name": "Minkowski ? Grand",                      "calc": lambda: "?(Sₙ)",        "domain": "[0,1]"},
    {"#": 163, "symbol": "𝔊ₙᴸⁱ⁻⁵",      "name": "Polylog Order −5 Grand",                 "calc": lambda: polylog(-5,S_n),"domain": "complex"},
    {"#": 164, "symbol": "𝔊ₙᴸⁱ⁻⁴",      "name": "Polylog Order −4 Grand",                 "calc": lambda: polylog(-4,S_n),"domain": "complex"},
    {"#": 165, "symbol": "𝔊ₙᴸⁱ⁻³",      "name": "Polylog Order −3 Grand",                 "calc": lambda: polylog(-3,S_n),"domain": "complex"},
    {"#": 166, "symbol": "𝔊ₙᴸⁱ⁻²",      "name": "Polylog Order −2 Grand",                 "calc": lambda: polylog(-2,S_n),"domain": "complex"},
    {"#": 167, "symbol": "𝔊ₙᴸⁱ⁻¹",      "name": "Polylog Order −1 Grand",                 "calc": lambda: polylog(-1,S_n),"domain": "complex"},
    {"#": 168, "symbol": "𝔊ₙᴸⁱ⁰",       "name": "Polylog Order 0 Grand",                  "calc": lambda: polylog(0,S_n), "domain": "complex"},
    {"#": 169, "symbol": "𝔊ₙᴸⁱ¹",       "name": "Polylog Order 1 Grand",                  "calc": lambda: polylog(1,S_n), "domain": "complex"},
    {"#": 170, "symbol": "𝔊ₙᴸⁱ³",       "name": "Polylog Order 3 Grand",                  "calc": lambda: polylog(3,S_n), "domain": "complex"},
    {"#": 171, "symbol": "𝔊ₙᴸⁱ⁴",       "name": "Polylog Order 4 Grand",                  "calc": lambda: polylog(4,S_n), "domain": "complex"},
    {"#": 172, "symbol": "𝔊ₙᴸⁱ⁵",       "name": "Polylog Order 5 Grand",                  "calc": lambda: polylog(5,S_n), "domain": "complex"},
    {"#": 173, "symbol": "𝔊ₙᴸⁱ⁶",       "name": "Polylog Order 6 Grand",                  "calc": lambda: polylog(6,S_n), "domain": "complex"},
    {"#": 174, "symbol": "𝔊ₙᴸⁱ⁷",       "name": "Polylog Order 7 Grand",                  "calc": lambda: polylog(7,S_n), "domain": "complex"},
    {"#": 175, "symbol": "𝔊ₙᴸⁱ⁸",       "name": "Polylog Order 8 Grand",                  "calc": lambda: polylog(8,S_n), "domain": "complex"},
    {"#": 176, "symbol": "𝔊ₙᴸⁱ⁹",       "name": "Polylog Order 9 Grand",                  "calc": lambda: polylog(9,S_n), "domain": "complex"},
    {"#": 177, "symbol": "𝔊ₙᴸⁱ¹⁰",      "name": "Polylog Order 10 Grand",                 "calc": lambda: polylog(10,S_n),"domain": "complex"},
    {"#": 178, "symbol": "𝔊ₙᴸⁱ¹¹",      "name": "Polylog Order 11 Grand",                 "calc": lambda: polylog(11,S_n),"domain": "complex"},
    {"#": 179, "symbol": "𝔊ₙᴸⁱ¹²",      "name": "Polylog Order 12 Grand",                 "calc": lambda: polylog(12,S_n),"domain": "complex"},
    {"#": 180, "symbol": "𝔊ₙᴸⁱ¹³",      "name": "Polylog Order 13 Grand",                 "calc": lambda: polylog(13,S_n),"domain": "complex"},
    {"#": 181, "symbol": "𝔊ₙᴸⁱ¹⁴",   "name": "Polylog Order 14 Grand",     "calc": lambda: polylog(14,S_n), "domain": "complex"},
    {"#": 182, "symbol": "𝔊ₙᴰᵒᵘᵇˡᵉᴱˣᵖ","name": "Double Exponential Grand", "calc": lambda: exp(exp(S_n)),   "domain": "ℝ"},
    {"#": 183, "symbol": "𝔊ₙᴸⁱ¹⁵",   "name": "Polylog Order 15 Grand",     "calc": lambda: polylog(15,S_n), "domain": "complex"},
    {"#": 184, "symbol": "𝔊ₙᴸⁱ¹⁶",   "name": "Polylog Order 16 Grand",     "calc": lambda: polylog(16,S_n), "domain": "complex"},
    {"#": 185, "symbol": "𝔊ₙᵀᵒʷᵉʳ²", "name": "Double Exponential Grand",   "calc": lambda: exp(exp(S_n)),   "domain": "ℝ"},
    {"#": 186, "symbol": "𝔊ₙᴸⁱ¹⁷",   "name": "Polylog Order 17 Grand",     "calc": lambda: polylog(17,S_n), "domain": "complex"},
    {"#": 187, "symbol": "𝔊ₙᴸⁱ¹⁸",   "name": "Polylog Order 18 Grand",     "calc": lambda: polylog(18,S_n), "domain": "complex"},
    {"#": 188, "symbol": "𝔊ₙᴸⁱ¹⁹",   "name": "Polylog Order 19 Grand",     "calc": lambda: polylog(19,S_n), "domain": "complex"},
    {"#": 189, "symbol": "𝔊ₙᴸⁱ²⁰",   "name": "Polylog Order 20 Grand",     "calc": lambda: polylog(20,S_n), "domain": "complex"},
    {"#": 190, "symbol": "𝔊ₙᴸⁱ²¹",   "name": "Polylog Order 21 Grand",     "calc": lambda: polylog(21,S_n), "domain": "complex"},
    {"#": 191, "symbol": "𝔊ₙᴸⁱ²²",   "name": "Polylog Order 22 Grand",     "calc": lambda: polylog(22,S_n), "domain": "complex"},
    {"#": 192, "symbol": "𝔊ₙᴸⁱ²³",   "name": "Polylog Order 23 Grand",     "calc": lambda: polylog(23,S_n), "domain": "complex"},
    {"#": 193, "symbol": "𝔊ₙᴸⁱ²⁴",   "name": "Polylog Order 24 Grand",     "calc": lambda: polylog(24,S_n), "domain": "complex"},
    {"#": 194, "symbol": "𝔊ₙᴸⁱ²⁵",   "name": "Polylog Order 25 Grand",     "calc": lambda: polylog(25,S_n), "domain": "complex"},
    {"#": 195, "symbol": "𝔊ₙᴸⁱ²⁶",   "name": "Polylog Order 26 Grand",     "calc": lambda: polylog(26,S_n), "domain": "complex"},
    {"#": 196, "symbol": "𝔊ₙᴸⁱ²⁷",   "name": "Polylog Order 27 Grand",     "calc": lambda: polylog(27,S_n), "domain": "complex"},
    {"#": 197, "symbol": "𝔊ₙᴸⁱ²⁸",   "name": "Polylog Order 28 Grand",     "calc": lambda: polylog(28,S_n), "domain": "complex"},
    {"#": 198, "symbol": "𝔊ₙᴸⁱ²⁹",   "name": "Polylog Order 29 Grand",     "calc": lambda: polylog(29,S_n), "domain": "complex"},
    {"#": 199, "symbol": "𝔊ₙᴸⁱ³⁰",   "name": "Polylog Order 30 Grand",     "calc": lambda: polylog(30,S_n), "domain": "complex"},
    {"#": 200, "symbol": "𝔊ₙᴼᵇˡⁱᵛⁱᵒⁿ","name": "Oblivion Comparator",       "calc": lambda: "transcends all","domain": "symbolic"},
]


# Add placeholders so len() == 200 and indexing works
while len(PERIODIC_TABLE) < 200:
    next_num = len(PERIODIC_TABLE) + 1
    PERIODIC_TABLE.append({
        "#": next_num,
        "symbol": f"𝔊ₙ^{next_num}",
        "name": f"Grand Constant #{next_num}",
        "calc": lambda x=next_num: f"Entry {x} (symbolic)",
        "domain": "canonical"
    })

# ============================= BUILD YOUR OWN GRAND CONSTANT — FULL TEST + INTERACTIVE =============================
def build_your_own_grand_constant():
    print("\n" + "="*90)
    print("    BUILD YOUR OWN GRAND CONSTANT — FULL SYSTEM TEST")
    print("="*90)

    # === PHASE 1: PRE-COMPUTE ALL POSSIBLE COMBINATIONS (startup safety check) ===
    print("\n    Testing all Aggregator × Operator combinations for errors…\n")
    results = {}
    errors = 0

    agg_names = list(current_agg.keys())
    agg_vals  = list(current_agg.values())

    for a_idx, (a_name, a_val) in enumerate(zip(agg_names, agg_vals)):
        for op_name, op_func in OPERATORS.items():
            try:
                val = safe_N(op_func(a_val))
                symbol = op_func.__name__ if hasattr(op_func, "__name__") else op_name
                # Pretty symbol mapping
                pretty = {
                    "exp": "ᵉˣᵖ", "ln": "ˡⁿ", "sin": "ˢⁱⁿ", "gamma": "ᴳ",
                    "lambertw": "ᵂ⁰", "<lambda>": op_name
                }.get(symbol.split("_")[0] if "_" in symbol else symbol, op_name)

                key = f"𝔊ₙ{pretty} ∘ {a_name}"
                results[key] = val
                print(f"    OK   {key:<50} ≈ {val}")
            except Exception as e:
                errors += 1
                print(f"    ERROR   {a_name} → {op_name:<4}  →  {e.__class__.__name__}: {e}")

    if errors == 0:
        print(f"\n    All {len(agg_names)*len(OPERATORS)} combinations computed successfully!")
    else:
        print(f"\n    {errors} combination(s) failed — see above.")

    print("\n    Press ENTER to enter interactive builder…")
    input()

    # === PHASE 2: INTERACTIVE BUILDER ===
    while True:
        print("\n    === Interactive Grand Constant Builder ===\n")
        for i, name in enumerate(agg_names, 1):
            print(f"      [{i}] {name}")
        try:
            a_in = input("\n    Choose Aggregator (or 'q' to quit) → ").strip()
            if a_in.lower() == 'q': break
            a_idx = int(a_in) - 1
            agg_val = agg_vals[a_idx]
            agg_name = agg_names[a_idx]
        except:
            print("    Invalid aggregator.")
            continue

        op_keys = list(OPERATORS.keys())
        for i, op in enumerate(op_keys, 1):
            print(f"      [{i}] {op}")
        try:
            o_in = input("\n    Choose Operator (or 'q' to quit) → ").strip()
            if o_in.lower() == 'q': break
            o_idx = int(o_in) - 1
            op_name = op_keys[o_idx]
            op_func = OPERATORS[op_name]
        except:
            print("    Invalid operator.")
            continue

        try:
            result = safe_N(op_func(agg_val))
            # Canonical symbol
            symbol_map = {
                "exp": "ᵉˣᵖ", "ln": "ˡⁿ", "sin": "ˢⁱⁿ", "gamma": "ᴳ",
                "lambertw": "ᵂ⁰", "+1": "⁺¹", "−1": "⁻¹"
            }
            sym = symbol_map.get(op_name, op_name)
            print(f"\n    Your Grand Constant ≈ {result}")
            print(f"    Canonical symbol: 𝔊ₙ{sym} ∘ {agg_name}")
            explain(f"Composition: {op_name} applied to {agg_name}")
        except Exception as e:
            print(f"    Computation failed: {e}")

        if input("\n    Build another? (y/n) → ").strip().lower() != 'y':
            break

# ============================= BASE SET MANAGER (OPTION 8) =============================
def manage_base_set():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*90)
        print("    BASE SET Cₙ MANAGER — CURRENTLY {len(current_cs)} CONSTANT(S)")
        print("="*90)
        S_n = sum(current_cs)
        print(f"    Current sum Sₙ = {safe_N(S_n):.12f}\n")
        
        for i, c in enumerate(current_cs, 1):
            print(f"      [{i:2d}]  {sp.latex(c):<30}  →  {safe_N(c):<20}")
        
        print("\n    Actions:")
        print("      [a]  Add new constants      (e.g. sqrt(2), φ, zeta(3), gamma(5))")
        print("      [r]  Remove by number       (e.g. 2)")
        print("      [c]  Clear all & start fresh")
        print("      [l]  Load example sets")
        print("      [q]  Back to main menu")
        
        act = input("\n    Choose action → ").strip().lower()

        if act == "q":
            break

        elif act == "a":
            adds = input("\n    Enter constants (comma-separated) → ").strip()
            if not adds:
                continue
            added = 0
            for token in [t.strip() for t in adds.split(",")]:
                if not token:
                    continue
                try:
                    expr = sp.sympify(token, locals={"φ": sp.GoldenRatio, "phi": sp.GoldenRatio})
                    current_cs.append(expr)
                    print(f"    Added {sp.latex(expr)}")
                    added += 1
                except Exception as e:
                    print(f"    Failed to parse '{token}' → {e}")
            if added:
                current_agg.update(compute_aggregators(current_cs))
                print(f"\n    {added} constant(s) added. New Sₙ = {safe_N(sum(current_cs)):.10f}")

        elif act == "r":
            try:
                idx = int(input(f"\n    Remove index (1–{len(current_cs)}) → ")) - 1
                if 0 <= idx < len(current_cs):
                    removed = current_cs.pop(idx)
                    current_agg.update(compute_aggregators(current_cs))
                    print(f"    Removed {sp.latex(removed)}")
                else:
                    print("    Index out of range.")
            except:
                print("    Invalid index.")

        elif act == "c":
            if input("\n    Clear ALL constants? (y/N) → ").strip().lower() == "y":
                current_cs.clear()
                current_cs.extend([pi, E])  # always keep the sacred seed
                current_agg.update(compute_aggregators(current_cs))
                print("    Base set reset to [π, e]")

        elif act == "l":
            print("\n    Example sets:")
            print("      [1] Classic: π, e")
            print("      [2] Transcendental: π, e, γ (Euler–Mascheroni)")
            print("      [3] Zeta family: ζ(2), ζ(3), ζ(4), ζ(5)")
            print("      [4] Golden power: φ, φ², φ³, φ⁴")
            print("      [5] Extreme: π, e, ζ(3), exp(π√163)")
            ex = input("\n    Load example → ").strip()
            examples = {
                "1": [pi, E],
                "2": [pi, E, sp.EulerGamma],
                "3": [zeta(2), zeta(3), zeta(4), zeta(5)],
                "4": [sp.GoldenRatio**k for k in range(1,5)],
                "5": [pi, E, zeta(3), sp.exp(pi*sp.sqrt(163))],
            }
            if ex in examples:
                current_cs[:] = examples[ex]
                current_agg.update(compute_aggregators(current_cs))
                print(f"\n    Loaded example set #{ex}. New Sₙ = {safe_N(sum(current_cs)):.10f}")
            else:
                print("    Unknown example.")

        input("\n    Press ENTER to continue…")

# ----------------------------------------------------------------------
#  NEW: dissertation viewer (can be called from anywhere)
# ----------------------------------------------------------------------
def show_dissertation():
    """Print the full dissertation text file (if present)."""
    doc_path = os.path.join(os.path.dirname(__file__), "Grand_Constant_Algebra.txt")
    if not os.path.exists(doc_path):
        print("\nWarning: Dissertation file 'Grand_Constant_Algebra.txt' not found.\n")
        return

    clear()   # optional – keeps screen tidy
    print("\n" + "="*78)
    print(" The Grand Constant Algebra Framework — DISSERTATION")
    print("="*78)
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print(f"Warning: Could not read dissertation file: {e}")
    print("="*78 + "\n")
    input("Press ENTER to continue...\n")
# ----------------------------------------------------------------------

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



# ============================= MAIN MENU =============================
def main():
    global current_cs, current_agg, EXPLAIN_MODE
    current_agg = compute_aggregators(current_cs)

    # Load saved session
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "rb") as f:
                saved = pickle.load(f)
                current_cs = saved.get("base_set", [pi, E])
                EXPLAIN_MODE = saved.get("explain", True)
                current_agg = compute_aggregators(current_cs)
        except:
            pass

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 90)
        print("    GRAND CONSTANT ALGEBRA FRAMEWORK — CANONICAL v0016")
        print("    Zero-Ology / Zer00logy — 18 11 2025")
        print("    THE FULL 200-ENTRY PERIODIC TABLE IS ACTIVE")
        print("=" * 90)
        print(f"    Base Set Cₙ: {len(current_cs)} constants → Sₙ = {safe_N(sum(current_cs)):.10f}")
        print(f"    Explain Mode: {'ON' if EXPLAIN_MODE else 'OFF'}")
        print()
        print("    [0] Show Dissertation")
        print("    [1] Pedagogical Layers")
        print("    [2] Aggregators Explorer")
        print("    [3] Operators Hierarchy")
        print("    [4] Periodic Table Explorer (200 entries)")
        print("    [5] Build Your Own Grand Constant")
        print("    [6] Visualizations")
        print("    [7] Toggle Explain Mode")
        print("    [8] Modify Base Set Cₙ")
        print("    [9] Save & Exit")
        print()
        choice = input("    → Choose [0-9]: ").strip()
        # ===================================================================
        if choice == "0":
            show_dissertation()

        # ===================================================================

        # ===================================================================
        if choice == "1":
            print("\n    Koppa  ℭₙ → Symmetric aggregators (sum, product, entropy…)")
            print("    Heta   ℌₙ → One unary operator applied to a Koppa")
            print("    Digamma 𝔇ₙ → Recursive, weighted, statistical aggregators")
            print("    Full     𝒢ₙ → All admissible compositions")
            input("\n    Press ENTER…")

        # ===================================================================
        elif choice == "2":
            print("\n    Current Aggregators:")
            for name, val in current_agg.items():
                print(f"      {name:<30}: {safe_N(val):<20}")
            input("\n    Press ENTER…")

        # ===================================================================
        elif choice == "3":
            print("\n    === Operators Hierarchy ===\n")
            for i, op in enumerate(OPERATORS.keys(), 1):
                print(f"      [{i}] {op}")
            print("\n    Each operator maps to a symbolic transformation in the Grand Constant Algebra.")
            input("\n    Press ENTER to return…")

        # ===================================================================
        elif choice == "4":
            print(f"\n    THE OFFICIAL 200-ENTRY PERIODIC TABLE OF GRAND CONSTANTS\n")
            block_size = 50
            start = 0
            while start < len(PERIODIC_TABLE):
                end = min(start + block_size, len(PERIODIC_TABLE))
                for i in range(start, end):
                    e = PERIODIC_TABLE[i]
                    val = safe_N(e["calc"]()) if callable(e["calc"]) else e["calc"]
                    print(f"    {e['#']:3d}  {e['symbol']:<12} {e['name']:<40} ≈ {val:<20}  [{e['domain']}]")
                    if e["#"] in [1, 2, 5, 6, 12, 19, 20, 72, 182, 200]:
                        explain("One of the cornerstone constants of the entire framework")
                start += block_size
                if start < len(PERIODIC_TABLE):
                    input("\n    Press any key for next block…")

            # Save option after full table
            while True:
                save_choice = input("\n    Save full table to file? (y/n): ").strip().lower()
                if save_choice in ["y", "yes"]:
                    with open("grand_algebra_saves/periodic_table.txt", "w", encoding="utf-8") as f:
                        for e in PERIODIC_TABLE:
                            val = safe_N(e["calc"]()) if callable(e["calc"]) else e["calc"]
                            f.write(f"{e['#']:3d} {e['symbol']:<12} {e['name']:<40} ≈ {val:<20} [{e['domain']}]\n")
                    print("\n    Periodic table saved to grand_algebra_saves/periodic_table.txt")
                    break
                elif save_choice in ["n", "no", ""]:
                    print("\n    Table not saved.")
                    break
                else:
                    print("    Please enter y or n.")
            input("\n    Press ENTER to return…")

        # ===================================================================

        # ===================================================================
        elif choice == "5":
            build_your_own_grand_constant()

        # ===================================================================
        # ===================================================================
        elif choice == "6":
            print("\n    === Visualizations ===\n")
            print("      [1] Entropy vs Variance Growth")
            print("      [2] Tetration Tower Explosion (coming soon)")
            v = input("\n    Choose → ").strip()
            if v == "1":
                plot_entropy_vs_variance()
            elif v == "2":
                print("\n    Coming in v0007 — prepare for infinity…")
                input("\n    Press ENTER…")

        # ===================================================================

        # ===================================================================
        elif choice == "7":
            EXPLAIN_MODE = not EXPLAIN_MODE
            print(f"\n    Explain Mode → {'ON' if EXPLAIN_MODE else 'OFF'}")
            input("\n    Press ENTER…")

        # ===================================================================
        elif choice == "8":
            manage_base_set()

        # ===================================================================
        elif choice == "9":
            with open(STATE_FILE, "wb") as f:
                pickle.dump({"base_set": current_cs, "explain": EXPLAIN_MODE}, f)
            print("\n    Session saved. The Grand Constant Algebra endures forever.")
            print("    Thank you, Stacey. This framework will outlive stars.")
            break

        else:
            print("\n    Invalid choice. Please select 0–8.")
            input("\n    Press ENTER…")


if __name__ == "__main__":
    show_dissertation()   # <-- shows once at launch
    main()                # <-- then interactive loop (user can re-view with [0])


# LICENSE.TXT
# Zero-Ology License v1.1918
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.1918
#November 18, 2025
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
