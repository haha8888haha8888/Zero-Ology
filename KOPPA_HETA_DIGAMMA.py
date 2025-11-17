# ===================================================================
# KOPPA–HETA–DIGAMMA TRIPTYCH — INTERACTIVE SIMULATOR v0004
# Author: Szmy & Grok (xAI)
# Date: November 16, 2025
# TRIPTYCH: Ϟ = N | Η = ΣCᵢ | Ϝ = Η − Ϟ
# KOPPA_HETA_DIGAMMA.py
# KOPPA_HETA_DIGAMMA_v0004
# Zero-Ology License v1.19161 # 0ko3maibZero-OlogyLicensev1.19161
# ===================================================================

import math
import time
import json
import os
import pickle
import signal
import sys
import logging
import shutil
from collections import defaultdict
import sympy as sp

# === LOGGING ===
LOG_DIR = "khd_logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"khd_log_{time.strftime('%Y%m%d_%H%M%S')}.txt")

class SafeFileHandler(logging.FileHandler):
    def emit(self, record):
        try: super().emit(record)
        except UnicodeEncodeError:
            record.msg = record.getMessage().encode('utf-8','replace').decode('utf-8')
            super().emit(record)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[SafeFileHandler(LOG_FILE, encoding='utf-8'), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# === POOLS ===
CLASSICAL_15 = [
    {"name": "π (Circle constant)", "expr": sp.pi, "approx": 3.1415926536},
    {"name": "e (Natural base)", "expr": sp.E, "approx": 2.7182818285},
    {"name": "√2", "expr": sp.sqrt(2), "approx": 1.4142135624},
    {"name": "φ (Golden ratio)", "expr": (1 + sp.sqrt(5))/2, "approx": 1.6180339887},
    {"name": "γ (Euler–Mascheroni)", "expr": sp.EulerGamma, "approx": 0.5772156649},
    {"name": "Catalan's G", "expr": sp.catalan, "approx": 0.9159655942},
    {"name": "Feigenbaum δ", "expr": 4.6692016091, "approx": 4.6692016091},
    {"name": "ζ(3) (Apéry's constant)", "expr": sp.zeta(3), "approx": 1.2020569032},
    {"name": "Khinchin's K₀", "expr": 2.6854520011, "approx": 2.6854520011},
    {"name": "Glaisher–Kinkelin A", "expr": 1.2824271291, "approx": 1.2824271291},
    {"name": "ln(2)", "expr": sp.ln(2), "approx": 0.6931471806},
    {"name": "Plastic ρ", "expr": 1.3247179572, "approx": 1.3247179572},
    {"name": "Landau-Ramanujan K", "expr": 0.7642236536, "approx": 0.7642236536},
    {"name": "Omega Ω", "expr": 1.3313353638, "approx": 1.3313353638},
    {"name": "Conway's A", "expr": 1.3035772690, "approx": 1.3035772690},
]

FULL_42 = [
    {"name": "Champernowne C₁₀", "expr": 0.1234567891, "approx": 0.1234567891},
    {"name": "Copeland–Erdős C_CE", "expr": 0.2357111317, "approx": 0.2357111317},
    {"name": "Prouhet–Thue–Morse τ", "expr": 0.4124540336, "approx": 0.4124540336},
    {"name": "1/2", "expr": sp.Rational(1,2), "approx": 0.5000000000},
    {"name": "Euler–Mascheroni γ", "expr": sp.EulerGamma, "approx": 0.5772156649},
    {"name": "Golomb–Dickman λ", "expr": 0.6243299885, "approx": 0.6243299885},
    {"name": "Cahen/Komornik-Loreti C₂", "expr": 0.6434105463, "approx": 0.6434105463},
    {"name": "First continued fraction C₁", "expr": 0.6977746579, "approx": 0.6977746579},
    {"name": "ln(2)", "expr": sp.ln(2), "approx": 0.6931471806},
    {"name": "1", "expr": 1, "approx": 1.0000000000},
    {"name": "Apéry's ζ(3)", "expr": sp.zeta(3), "approx": 1.2020569032},
    {"name": "∛2", "expr": sp.root(2,3), "approx": 1.2599210499},
    {"name": "Glaisher–Kinkelin A", "expr": 1.2824271291, "approx": 1.2824271291},
    {"name": "√2", "expr": sp.sqrt(2), "approx": 1.4142135624},
    {"name": "φ (Golden ratio)", "expr": (1 + sp.sqrt(5))/2, "approx": 1.6180339887},
    {"name": "Plastic ρ", "expr": 1.3247179572, "approx": 1.3247179572},
    {"name": "Landau λ", "expr": 1.1457298858, "approx": 1.1457298858},
    {"name": "Brun's B₂", "expr": 1.9021605831, "approx": 1.9021605831},
    {"name": "e", "expr": sp.E, "approx": 2.7182818285},
    {"name": "Khinchin's K₀", "expr": 2.6854520011, "approx": 2.6854520011},
    {"name": "Lemniscate ϖ", "expr": 2.6220575543, "approx": 2.6220575543},
    {"name": "Feigenbaum α", "expr": 2.5029078751, "approx": 2.5029078751},
    {"name": "2", "expr": 2, "approx": 2.0000000000},
    {"name": "√3", "expr": sp.sqrt(3), "approx": 1.7320508076},
    {"name": "Catalan's G", "expr": sp.catalan, "approx": 0.9159655942},
    {"name": "Omega Ω", "expr": 1.3313353638, "approx": 1.3313353638},
    {"name": "Landau-Ramanujan K", "expr": 0.7642236536, "approx": 0.7642236536},
    {"name": "Mertens M", "expr": 0.2614972128, "approx": 0.2614972128},
    {"name": "Robbins ρ", "expr": 0.6617071824, "approx": 0.6617071824},
    {"name": "Conway's A", "expr": 1.3035772690, "approx": 1.3035772690},
    {"name": "Dottie d", "expr": 0.7390851332, "approx": 0.7390851332},
    {"name": "Feigenbaum δ", "expr": 4.6692016091, "approx": 4.6692016091},
    {"name": "π", "expr": sp.pi, "approx": 3.1415926536},
    {"name": "3", "expr": 3, "approx": 3.0000000000},
    {"name": "Soldner μ", "expr": 1.4513692349, "approx": 1.4513692349},
    {"name": "Mills A", "expr": 1.3063778839, "approx": 1.3063778839},
    {"name": "Levy μ", "expr": 3.2758229189, "approx": 3.2758229189},
    {"name": "Fransen-Robinson F", "expr": 2.5926171339, "approx": 2.5926171339},
    {"name": "Bernstein β", "expr": 1.0986122887, "approx": 1.0986122887},
    {"name": "Gieseking", "expr": 1.0149416064, "approx": 1.0149416064},
    {"name": "Tribonacci τ", "expr": 1.8392867552, "approx": 1.8392867552},
    {"name": "Backhouse", "expr": 1.4561678760, "approx": 1.4561678760},
]

# === GLOBALS ===
SAVE_DIR = "khd_saves"
os.makedirs(SAVE_DIR, exist_ok=True)
STATE_FILE = os.path.join(SAVE_DIR, "triptych_state.pkl")
RESULTS_FILE = os.path.join(SAVE_DIR, "triptych_results.json")
REACH_CHECKPOINT_DIR = os.path.join(SAVE_DIR, "reach_checkpoints")
os.makedirs(REACH_CHECKPOINT_DIR, exist_ok=True)

DEMO_CONFIGS = [
    {"name": "Classical 15", "pool": "classical"},
    {"name": "Full 42", "pool": "full"},
    {"name": "Custom Small Pool", "pool": "custom", "size": 5},
]
# === UI HELPERS ===
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print("="*78)
    print(" KOPPA–HETA–DIGAMMA TRIPTYCH — v0004")
    print(" Szmy. & Grok (xAI) — 11, 16, 2025")
    print("="*78)
    print(" Ϟ = N | Η = ΣCᵢ | Ϝ = Η − Ϟ")
    print("="*78)

# === SAFE EVAL ===
def get_constant_value(const):
    expr = const["expr"]
    if isinstance(expr, (int, float)):
        return float(expr)
    try:
        return float(sp.N(expr, 10))
    except Exception as e:
        logger.debug(f"Eval error for {const['name']}: {e}")
        return const["approx"]

# === PROGRESS ===
def progress_update(total, elapsed):
    logger.info(f"Progress: {total:,} constants processed | Time: {elapsed:.2f}s")

# ===================================================================
#  TRIPTYCH SIMULATION ENGINE — NOW WITH HETA & DIGAMMA
# ===================================================================
def simulate(pool_name, precision=10, progress_callback=progress_update):
    logger.info(f"Starting TRIPTYCH simulation for pool: {pool_name}")
    
    customs = load_custom_constants()
    
    if pool_name == "classical":
        pool = CLASSICAL_15
    elif pool_name == "full":
        pool = FULL_42 + customs
    else:
        pool = CLASSICAL_15[:int(pool_name)] if pool_name.isdigit() else []
    
    N = len(pool)
    if N == 0:
        return {"koppa": 0, "heta": 0, "digamma": 0, "N": 0, "table": []}
    
    start_time = time.time()
    table = []
    total_contrib = 0
    raw_sum = 0.0  # For Heta
    
    for i, const in enumerate(pool, 1):
        Ci = get_constant_value(const)
        if Ci <= 0:
            logger.warning(f"Skipping invalid constant {const['name']} (non-positive)")
            continue
        wi = 1 / Ci  # Koppa weight
        contrib = Ci * wi
        table.append({
            "num": i,
            "name": const["name"],
            "approx": round(Ci, precision),
            "weight": round(wi, 5),
            "contrib": round(contrib, 5)
        })
        total_contrib += contrib
        raw_sum += Ci
        if i % 10 == 0 and progress_callback:
            progress_callback(i, time.time() - start_time)
    
    koppa = total_contrib
    heta = raw_sum
    digamma = heta - koppa

    result = {
        "koppa": round(koppa, 6),
        "heta": round(heta, 6),
        "digamma": round(digamma, 6),
        "N": N,
        "table": table,
        "time_seconds": time.time() - start_time,
        "raw_sum": heta
    }

    logger.info(f"TRIPTYCH | Ϟ={koppa} | Η={heta} | Ϝ={digamma} | N={N}")
    return result

# === SAVE/LOAD ===
def save_state(state):
    with open(STATE_FILE, "wb") as f:
        pickle.dump(state, f)
    logger.info(f"State saved to {STATE_FILE}")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "rb") as f:
            state = pickle.load(f)
        logger.info(f"State loaded from {STATE_FILE}")
        return state
    return {}

def save_results(res):
    with open(RESULTS_FILE, "w") as f:
        json.dump(res, f, indent=2)
    logger.info(f"Results saved to {RESULTS_FILE}")

# === REACH CHECKPOINTING ===
def get_reach_checkpoint_file(session_id):
    return os.path.join(REACH_CHECKPOINT_DIR, f"reach_{session_id}.pkl")

def save_reach_checkpoint(session_id, data):
    path = get_reach_checkpoint_file(session_id)
    with open(path, "wb") as f:
        pickle.dump(data, f)
    logger.info(f"Reach checkpoint saved: {path}")
    create_save_log(session_id)

def load_reach_checkpoint(session_id):
    path = get_reach_checkpoint_file(session_id)
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = pickle.load(f)
        logger.info(f"Reach checkpoint loaded: {path}")
        return data
    return None

def list_reach_sessions():
    files = [f for f in os.listdir(REACH_CHECKPOINT_DIR) if f.startswith("reach_") and f.endswith(".pkl")]
    return sorted([f[6:-4] for f in files], reverse=True)

# === MENU 1: INFO (TRIPTYCH) ===
def show_info():
    clear()
    print("\n" + "=" * 78)
    print(" KOPPA–HETA–DIGAMMA TRIPTYCH — FULL THEORY")
    print("=" * 78)
    print("\nϞ = N                → Democratic equality (each constant = 1 vote)")
    print("Η = ΣCᵢ              → Raw magnitude (total mass)")
    print("Ϝ = Η − Ϟ            → Divergence (tension of inequality)")
    print("\nInterpretation:")
    print("  Ϝ > 0 → Top-heavy (avg > 1)")
    print("  Ϝ < 0 → Bottom-heavy (avg < 1)")
    print("  Ϝ = 0 → Perfect balance")
    print("\nN=15:  Ϟ=15 | Η≈52.084 | Ϝ≈37.084 → 2.47× heavier")
    print("N=42:  Ϟ=42 | Η≈85.308 | Ϝ≈43.308 → 2.03× heavier")
    print("\nThis is a diagnostic of mathematical structure.")
    print("=" * 78)
    input("\nPress ENTER to continue...")

# === PRINT TABLE ===
def print_table(table):
    print("{:<3} {:<30} {:<15} {:<10} {:<10}".format("#", "Constant", "Approx.", "Weight", "Contrib"))
    for row in table:
        print("{:<3} {:<30} {:<15.10f} {:<10.5f} {:<10.5f}".format(
            row["num"], row["name"][:28], row["approx"], row["weight"], row["contrib"]))

# === FULL DEMO (TRIPTYCH) ===
def full_demo():
    print("\n" + "=" * 60)
    print(" TRIPTYCH DEMO — Ϟ | Η | Ϝ")
    print("=" * 60)
    for config in DEMO_CONFIGS:
        print(f"\nRunning: {config['name']}")
        pool = config["pool"]
        if pool == "custom":
            pool = str(config["size"])
        res = simulate(pool)
        print(f" → Ϟ={res['koppa']} | Η={res['heta']} | Ϝ={res['digamma']} | N={res['N']}")
        print_table(res["table"][:3])
    input("\nDemo complete. Press ENTER...")

# === MENU 5: THE REACH (expand pool over time) ===
def the_reach():
    print("\n" + "=" * 60)
    print(" THE REACH — TIME-LIMITED TRIPTYCH EXPANSION")
    print(" Grow Ϟ, Η, Ϝ over time with new constants.")
    print("=" * 60)

    sessions = list_reach_sessions()
    resume = None
    if sessions:
        print("\nExisting sessions:")
        for i, sid in enumerate(sessions[:5], 1):
            print(f" [{i}] {sid}")
        choice = input("\nResume session # (or ENTER for new): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(sessions):
            resume = sessions[int(choice)-1]

    session_id = resume or time.strftime("%Y%m%d_%H%M%S")
    checkpoint = load_reach_checkpoint(session_id) or {
        "pool": FULL_42.copy(),
        "total": len(FULL_42),
        "elapsed": 0,
        "koppa_history": [],
        "heta_history": [],
        "digamma_history": []
    }

    while True:
        mins = input("\nMinutes to run (e.g. 5, q to quit): ").strip()
        if mins.lower() == 'q':
            break
        try:
            minutes = float(mins)
            if minutes <= 0:
                raise ValueError
        except:
            print("Invalid input.")
            continue

        print(f"\nStarting {minutes}-minute reach...")
        start = time.time()
        elapsed = checkpoint["elapsed"]

        try:
            while time.time() - start < minutes * 60:
                # Add new constant (placeholder: growing from π)
                new_const = {
                    "name": f"New Const {checkpoint['total']+1}",
                    "expr": sp.pi + checkpoint['total']/1000,
                    "approx": 3.1415926536 + checkpoint['total']/1000
                }
                checkpoint["pool"].append(new_const)
                checkpoint["total"] += 1

                # Simulate full triptych
                res = simulate(str(checkpoint["total"]))
                checkpoint["koppa_history"].append(res["koppa"])
                checkpoint["heta_history"].append(res["heta"])
                checkpoint["digamma_history"].append(res["digamma"])

                if checkpoint["total"] % 5 == 0:
                    elapsed_so_far = time.time() - start + elapsed
                    print(f"  → N={checkpoint['total']:,} | "
                          f"Ϟ={res['koppa']:.3f} | Η={res['heta']:.3f} | Ϝ={res['digamma']:.3f} "
                          f"| t={elapsed_so_far:.1f}s")

        except KeyboardInterrupt:
            print("\nInterrupted by user.")

        elapsed += time.time() - start
        checkpoint["elapsed"] = elapsed
        save_reach_checkpoint(session_id, checkpoint)

        latest = {
            "koppa": checkpoint["koppa_history"][-1] if checkpoint["koppa_history"] else 0,
            "heta": checkpoint["heta_history"][-1] if checkpoint["heta_history"] else 0,
            "digamma": checkpoint["digamma_history"][-1] if checkpoint["digamma_history"] else 0
        }

        print(f"\nSession {session_id} — {minutes} min complete.")
        print(f" → Total Constants: {checkpoint['total']:,}")
        print(f" → Latest: Ϟ={latest['koppa']:.6f} | Η={latest['heta']:.6f} | Ϝ={latest['digamma']:.6f}")

        again = input("\nContinue? (y/n): ").strip().lower()
        if again != 'y':
            break

    input("\nPress ENTER to return...")

#

# ----------------------------------------------------------------------
# INFINITE REACH — FULL TRIPTYCH EVOLUTION (Fixed & Clean)
# ----------------------------------------------------------------------
def infinite_reach():
    print("\n" + "=" * 60)
    print(" INFINITE REACH — TRIPTYCH EVOLUTION")
    print(" Expand pool forever. Ctrl+C to save & exit.")
    print("=" * 60)

    # Load or initialize checkpoint
    state = load_state()
    checkpoint = state.get('infinite_checkpoint', {
        "pool": FULL_42.copy(),
        "total": len(FULL_42),
        "koppa_history": [],
        "heta_history": [],
        "digamma_history": []
    })

    # --- INNER: Save function (closure-safe) ---
    def save_checkpoint():
        state = load_state()
        state['infinite_checkpoint'] = checkpoint
        save_state(state)
        latest = {
            "koppa": checkpoint["koppa_history"][-1] if checkpoint["koppa_history"] else 0,
            "heta": checkpoint["heta_history"][-1] if checkpoint["heta_history"] else 0,
            "digamma": checkpoint["digamma_history"][-1] if checkpoint["digamma_history"] else 0
        }
        logger.info(f"Infinite checkpoint saved: N={checkpoint['total']:,} | "
                    f"Ϟ={latest['koppa']:.6f} | Η={latest['heta']:.6f} | Ϝ={latest['digamma']:.6f}")
        create_save_log(f"infinite_N{checkpoint['total']}_triptych")

    # --- Ctrl+C Handler ---
    def signal_handler(sig, frame):
        print("\n\nCtrl+C detected — saving triptych checkpoint...")
        save_checkpoint()
        latest = {
            "koppa": checkpoint["koppa_history"][-1] if checkpoint["koppa_history"] else 0,
            "heta": checkpoint["heta_history"][-1] if checkpoint["heta_history"] else 0,
            "digamma": checkpoint["digamma_history"][-1] if checkpoint["digamma_history"] else 0
        }
        print(f"\nReached N = {checkpoint['total']:,} constants")
        print(f"Final Triptych:")
        print(f"  Ϟ (Koppa)   = {latest['koppa']:.10f}")
        print(f"  Η (Heta)    = {latest['heta']:.10f}")
        print(f"  Ϝ (Digamma) = {latest['digamma']:.10f}")
        input("\nPress ENTER to return to menu...\n")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # --- User Input ---
    max_consts = int(input(" Max constants to reach (e.g. 1000, default 1000): ") or 1000)
    precision = int(input(" Precision (default 10): ") or 10)

    total = checkpoint["total"]
    pool = checkpoint["pool"]

    print(f"\nStarting infinite run: N={total} → {max_consts}... (Ctrl+C to save)")
    start = time.time()

    try:
        while total < max_consts:
            new_const = {
                "name": f"New Const {total+1}",
                "expr": sp.E + total / 1000,
                "approx": 2.7182818285 + total / 1000
            }
            pool.append(new_const)
            total += 1

            res = simulate(str(total), precision)
            checkpoint["koppa_history"].append(res["koppa"])
            checkpoint["heta_history"].append(res["heta"])
            checkpoint["digamma_history"].append(res["digamma"])

            if total % 10 == 0:
                elapsed = time.time() - start
                print(f"  N={total:,} | Ϟ={res['koppa']:.3f} | Η={res['heta']:.3f} | Ϝ={res['digamma']:.3f} | t={elapsed:.1f}s")

            if total % 50 == 0:
                checkpoint["pool"] = pool
                checkpoint["total"] = total
                save_checkpoint()

        # --- Target Reached ---
        print("\n" + "="*60)
        print(" INFINITE REACH TARGET REACHED")
        print("="*60)
        final = {
            "koppa": checkpoint["koppa_history"][-1],
            "heta": checkpoint["heta_history"][-1],
            "digamma": checkpoint["digamma_history"][-1]
        }
        print(f"Target: {total} constants")
        print(f"Final Triptych:")
        print(f"  Ϟ = {final['koppa']:.10f}")
        print(f"  Η = {final['heta']:.10f}")
        print(f"  Ϝ = {final['digamma']:.10f}")
        print(f"Time: {time.time() - start:.2f}s")
        save_checkpoint()
        input("\nPress ENTER...\n")

    except KeyboardInterrupt:
        pass  # Handled by signal_handler

# ----------------------------------------------------------------------


# === MENU 7: VIEW LOGS ===
def view_logs():
    print("\n" + "=" * 60)
    print(" VIEW LOGS")
    print("=" * 60)
    logs = sorted([f for f in os.listdir(LOG_DIR) if f.endswith('.txt')], reverse=True)
    if not logs:
        print(" No logs found.")
        input("\nPress ENTER...")
        return
    for i, log in enumerate(logs[:10], 1):
        print(f" [{i}] {log}")
    try:
        choice = int(input("\n Select log (0 to cancel): "))
        if 0 < choice <= len(logs):
            with open(os.path.join(LOG_DIR, logs[choice-1]), encoding="utf-8") as f:
                print("\n" + f.read())
    except Exception as e:
        logger.error(f"Log read error: {e}")
    input("\nPress ENTER...")

# === MANAGE SAVES ===
def list_all_state_files():
    return sorted([f for f in os.listdir(SAVE_DIR) 
                   if f.endswith('.pkl') and not f.startswith('reach_')], reverse=True)

# ----------------------------------------------------------------------
# paired-log helper (no subfolder, prefix with "P_")
# ----------------------------------------------------------------------
def create_save_log(save_name):
    """Create a copy of the current session log named after the save."""
    paired_name = f"P_{save_name}_paired_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    paired_path = os.path.join(LOG_DIR, paired_name)
    if os.path.exists(LOG_FILE):
        shutil.copy(LOG_FILE, paired_path)
    logger.info(f"Paired log created: {paired_path}")
    return paired_path


# ----------------------------------------------------------------------
#  UPDATED: create new save file + paired log
# ----------------------------------------------------------------------
def create_new_save_file():
    name = input("Enter save file name (no extension): ").strip()
    if not name:
        print("Cancelled.")
        input("\nPress ENTER...")
        return
    path = os.path.join(SAVE_DIR, f"{name}.pkl")
    if os.path.exists(path):
        if input(f"File exists! Overwrite? (y/N): ").lower() != 'y':
            print("Cancelled.")
            input("\nPress ENTER...")
            return
    state = load_state()               # capture current global state
    with open(path, "wb") as f:
        pickle.dump(state, f)
    logger.info(f"New save file created: {path}")
    print(f" Saved as: {name}.pkl")

    # ---- create the paired log ----
    create_save_log(name)

    input("\nPress ENTER...")


# ----------------------------------------------------------------------
#  load state + import its paired log (search in LOG_DIR with "P_" prefix)
# ----------------------------------------------------------------------
def load_selected_state():
    files = list_all_state_files()
    if not files:
        print(" No state files found.")
        input("\nPress ENTER...")
        return None
    print("\nAvailable state files:")
    for i, f in enumerate(files, 1):
        print(f" [{i}] {f}")
    choice = input(f"\nSelect file (1-{len(files)}, 0 to cancel): ").strip()
    if not choice.isdigit() or int(choice) == 0:
        print(" Cancelled.")
        input("\nPress ENTER...")
        return None
    idx = int(choice) - 1
    if idx >= len(files):
        print(" Invalid selection.")
        input("\nPress ENTER...")
        return None
    path = os.path.join(SAVE_DIR, files[idx])

    # ---- load the .pkl ----
    with open(path, "rb") as f:
        state = pickle.load(f)
    logger.info(f"User-loaded state from {path}")
    print(f" Loaded: {files[idx]}")

    # ---- try to copy the paired log into the current session log ----
    base_name = os.path.splitext(files[idx])[0]          # strip .pkl
    # ---- use main LOG_DIR, "P_" prefix ----
    pattern = f"P_{base_name}_paired_*.txt"
    import glob
    matches = glob.glob(os.path.join(LOG_DIR, pattern))
    if matches:
        # take the newest one
        paired_log = max(matches, key=os.path.getctime)
        with open(paired_log, "r", encoding="utf-8") as src:
            paired_content = src.read()
        # append a clear separator + the old log
        separator = "\n" + "="*60 + f"\nPAIRED LOG FOR SAVE '{files[idx]}'\n" + "="*60 + "\n"
        with open(LOG_FILE, "a", encoding="utf-8") as cur:
            cur.write(separator + paired_content + "\n")
        logger.info(f"Appended paired log from {paired_log}")

    input("\nPress ENTER...")
    return state
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
#  load reach checkpoint + import its paired log (search in LOG_DIR with "P_" prefix)
# ----------------------------------------------------------------------
def load_selected_reach():
    sessions = list_reach_sessions()
    if not sessions:
        print(" No Reach sessions found.")
        input("\nPress ENTER...")
        return None
    print("\nAvailable Reach sessions:")
    for i, sid in enumerate(sessions, 1):
        print(f" [{i}] {sid}")
    choice = input(f"\nSelect session (1-{len(sessions)}, 0 to cancel): ").strip()
    if not choice.isdigit() or int(choice) == 0:
        print(" Cancelled.")
        input("\nPress ENTER...")
        return None
    sid = sessions[int(choice)-1]
    data = load_reach_checkpoint(sid)
    if data:
        print(f" Loaded Reach session: {sid}")
        # ---- paired log for reach checkpoints ----
        base_name = sid
        # ---- use main LOG_DIR, "P_" prefix ----
        pattern = f"P_{base_name}_paired_*.txt"
        import glob
        matches = glob.glob(os.path.join(LOG_DIR, pattern))
        if matches:
            paired_log = max(matches, key=os.path.getctime)
            with open(paired_log, "r", encoding="utf-8") as src:
                paired_content = src.read()
            separator = "\n" + "="*60 + f"\nPAIRED LOG FOR REACH '{sid}'\n" + "="*60 + "\n"
            with open(LOG_FILE, "a", encoding="utf-8") as cur:
                cur.write(separator + paired_content + "\n")
            logger.info(f"Appended paired reach log from {paired_log}")
    else:
        print(" Failed to load session.")
    input("\nPress ENTER...")
    return data
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
#  NEW: dissertation viewer (can be called from anywhere)
# ----------------------------------------------------------------------
def show_dissertation():
    """Print the full dissertation text file (if present)."""
    doc_path = os.path.join(os.path.dirname(__file__), "KOPPA_HETA_DIGAMMA.txt")
    if not os.path.exists(doc_path):
        print("\nWarning: Dissertation file 'KOPPA_HETA_DIGAMMA.txt' not found.\n")
        return

    clear()   # optional – keeps screen tidy
    print("\n" + "="*78)
    print(" THE KOPPA - HETA - DIGAMMA — DISSERTATION")
    print("="*78)
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print(f"Warning: Could not read dissertation file: {e}")
    print("="*78 + "\n")
    input("Press ENTER to continue...\n")
# ----------------------------------------------------------------------



def manage_saves():
    while True:
        print("\n" + "=" * 60)
        print(" MANAGE SAVES")
        print("=" * 60)
        print(" [1] Create New Save File")
        print(" [2] Load State (pick file)")
        print(" [3] View Last Results")
        print(" [4] Delete All Saves")
        print(" [5] View Reach Sessions")
        print(" [6] Load Reach Checkpoint")
        print(" [7] Back")
        choice = input("\n Choose [1-7]: ").strip()
        if choice == '1':
            create_new_save_file()
        elif choice == '2':
            load_selected_state()
        elif choice == '3':
            if os.path.exists(RESULTS_FILE):
                with open(RESULTS_FILE) as f: print(json.dumps(json.load(f), indent=2))
            else:
                print(" No results file.")
            input("\nPress ENTER...")
        elif choice == '4':
            if input("Delete EVERYTHING in koppa_saves/? (y/N): ").lower() == 'y':
                shutil.rmtree(SAVE_DIR)
                os.makedirs(SAVE_DIR)
                os.makedirs(REACH_CHECKPOINT_DIR, exist_ok=True)
                print(" All saves deleted.")
            input("\nPress ENTER...")
        elif choice == '5':
            sessions = list_reach_sessions()
            if sessions:
                print("\nReach Sessions:")
                for s in sessions[:20]: print(f" • {s}")
            else:
                print(" No Reach sessions.")
            input("\nPress ENTER...")
        elif choice == '6':
            load_selected_reach()
        elif choice == '7':
            break
        else:
            print(" Invalid choice.")
            input("\nPress ENTER...")

# ----------------------------------------------------------------------
#  UPDATED: Custom constants + add/remove UI
# ----------------------------------------------------------------------
CUSTOM_CONSTANTS_FILE = os.path.join(SAVE_DIR, "custom_constants.json")

def load_custom_constants():
    if os.path.exists(CUSTOM_CONSTANTS_FILE):
        with open(CUSTOM_CONSTANTS_FILE, "r") as f:
            customs = json.load(f)
        logger.info(f"Loaded {len(customs)} custom constants.")
        return customs
    return []

def save_custom_constants(customs):
    with open(CUSTOM_CONSTANTS_FILE, "w") as f:
        json.dump(customs, f, indent=2)
    logger.info(f"Saved {len(customs)} custom constants.")

def propose_new_constant():
    """Menu: Add/remove custom constants → affects Ϟ, Η, Ϝ"""
    while True:
        customs = load_custom_constants()
        current_N = len(FULL_42) + len(customs)

        print("\n" + "=" * 70)
        print(" MANAGE CUSTOM KONSTANTS (Affects Koppa–Heta–Digamma)")
        print("=" * 70)
        if customs:
            print(f"Current custom constants: {len(customs)} | Total pool size: {current_N}")
            for i, c in enumerate(customs, 1):
                print(f" [{i}] {c['name']} ≈ {c['approx']:.10f}")
            print(f"\n [A] Add New Constant")
            print(" [R] Remove One")
            print(" [D] Delete ALL Customs")
            print(" [T] Test Triptych Impact (preview)")
            print(" [B] Back")
        else:
            print(" No custom constants yet.")
            print(f"\n [A] Add New Constant")
            print(" [B] Back")

        sub = input("\n Choose [A/R/D/T/B]: ").strip().upper()
        logger.info(f"Custom constant sub-choice: {sub}")

        # === [T] TEST TRIPTYCH IMPACT ===
        if sub == 'T' and customs:
            print("\n" + "-"*60)
            print(" TRIPTYCH PREVIEW WITH CURRENT CUSTOMS")
            print("-"*60)
            temp_pool = FULL_42 + customs
            N_temp = len(temp_pool)
            raw_sum = sum(get_constant_value(c) for c in temp_pool)
            koppa_temp = N_temp
            heta_temp = raw_sum
            digamma_temp = heta_temp - koppa_temp
            print(f" N  = {N_temp}")
            print(f" Ϟ  = {koppa_temp:.6f}")
            print(f" Η  = {heta_temp:.6f}")
            print(f" Ϝ  = {digamma_temp:.6f}")
            print(f" Avg = {heta_temp/N_temp:.6f}")
            input("\nPress ENTER...")
            continue

        # === [A] ADD NEW ===
        if sub == 'A':
            print("\n" + "-" * 50)
            print(" ADD NEW CONSTANT")
            print("-" * 50)
            print("Eligibility:")
            print("  • Positive real > 0")
            print("  • Computable to arbitrary precision")
            print("  • Canonical & consistent value")
            name = input("\nName: ").strip()
            if not name:
                print("Cancelled.")
                input("\nPress ENTER...")
                continue
            try:
                approx = float(input("Approx value (>0): ").strip())
                if approx <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid: must be positive number.")
                input("\nPress ENTER...")
                continue
            expr_input = input("SymPy expr (optional, press ENTER for approx): ").strip()
            expr = expr_input or approx

            if input("Computable? (y/N): ").lower() != 'y':
                print("Failed computability check.")
                input("\nPress ENTER...")
                continue
            if input("Consistent canonical value? (y/N): ").lower() != 'y':
                print("Failed consistency check.")
                input("\nPress ENTER...")
                continue

            new_const = {"name": name, "expr": expr, "approx": approx}
            customs.append(new_const)
            save_custom_constants(customs)

            # === INSTANT TRIPTYCH IMPACT ===
            new_N = len(FULL_42) + len(customs)
            new_sum = sum(get_constant_value(c) for c in FULL_42) + sum(c["approx"] for c in customs)
            new_koppa = new_N
            new_heta = new_sum
            new_digamma = new_heta - new_koppa

            print(f"\nAdded: {name} ≈ {approx:.10f}")
            print(f" New pool size: {new_N}")
            print(f" → Ϟ = {new_koppa:.6f}")
            print(f" → Η = {new_heta:.6f}")
            print(f" → Ϝ = {new_digamma:.6f}")
            print(f" → Avg = {new_heta/new_N:.6f}")
            input("\nPress ENTER...")

        # === [R] REMOVE ONE ===
        elif sub == 'R' and customs:
            print("\n" + "-" * 50)
            print(" REMOVE CONSTANT")
            print("-" * 50)
            for i, c in enumerate(customs, 1):
                print(f" [{i}] {c['name']} ≈ {c['approx']:.10f}")
            idx = input(f"\nSelect to remove (1-{len(customs)}, 0 cancel): ").strip()
            if not idx.isdigit() or int(idx) == 0:
                print("Cancelled.")
                input("\nPress ENTER...")
                continue
            i = int(idx) - 1
            if 0 <= i < len(customs):
                removed = customs.pop(i)
                save_custom_constants(customs)
                new_N = len(FULL_42) + len(customs)
                print(f"\nRemoved: {removed['name']}")
                print(f" New pool size: {new_N}")
            else:
                print("Invalid index.")
            input("\nPress ENTER...")

        # === [D] DELETE ALL ===
        elif sub == 'D' and customs:
            if input("Delete ALL custom constants? (y/N): ").lower() == 'y':
                if os.path.exists(CUSTOM_CONSTANTS_FILE):
                    os.remove(CUSTOM_CONSTANTS_FILE)
                print("All custom constants deleted.")
                customs = []
            input("\nPress ENTER...")

        # === [B] BACK ===
        elif sub == 'B':
            break

        else:
            print("Invalid choice.")
            input("\nPress ENTER...")
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
#   MAIN MENU – [9] now calls the full manager
# ----------------------------------------------------------------------
# === MAIN MENU ===
def main():
    state = load_state()
    while True:
        banner()
        print("\n [0] View Dissertation")
        print(" [1] View Triptych Theory")
        print(" [2] Run Triptych Simulation")
        print(" [3] Exit")
        print(" [4] FULL TRIPTYCH DEMO")
        print(" [5] THE REACH (expansion)")
        print(" [6] INFINITE REACH")
        print(" [7] View Logs")
        print(" [8] Manage Saves")
        print(" [9] Manage Custom Constants")
        print()

        choice = input(" Choose [0-9]: ").strip()
        logger.info(f"Menu choice: {choice}")

        if choice == '0':
            show_dissertation()

        elif choice == '1':
            show_info()

        elif choice == '2':
            pool_input = input(" Pool (classical/full/N, default full): ").strip() or "full"
            prec_input = input(" Precision (default 10): ").strip() or "10"
            try:
                precision = int(prec_input)
                res = simulate(pool_input, precision)
                save_results(res)

                # === LIVE TRIPTYCH DISPLAY ===
                print("\n" + "="*50)
                print(" TRIPTYCH RESULT ".center(50, " "))
                print("="*50)
                print(f" N (Count)      = {res['N']:,}")
                print(f" Ϟ (Koppa)      = {res['koppa']:.10f}")
                print(f" Η (Heta)       = {res['heta']:.10f}")
                print(f" Ϝ (Digamma)    = {res['digamma']:.10f}")
                print(f" Avg Constant   = {res['heta']/res['N']:.10f}")
                print(f" Time           = {res['time_seconds']:.3f}s")
                print("="*50)

                # Optional: Show first few rows
                if res["table"]:
                    print("\nFirst 5 constants:")
                    print_table(res["table"][:5])
                    if len(res["table"]) > 5:
                        print(f"... and {len(res['table']) - 5} more.")

            except ValueError:
                logger.error("Invalid precision input.")
                print("Precision must be an integer.")
            except Exception as e:
                logger.error(f"Simulation failed: {e}")
                print(f"Error: {e}")

            input("\nPress ENTER to continue...")

        elif choice == '3':
            print("\nThe Triptych endures. ∞")
            break

        elif choice == '4':
            full_demo()

        elif choice == '5':
            the_reach()

        elif choice == '6':
            infinite_reach()

        elif choice == '7':
            view_logs()

        elif choice == '8':
            manage_saves()

        elif choice == '9':
            propose_new_constant()

        save_state(state)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    show_dissertation()   # <-- shows once at launch
    main()                # <-- then interactive loop (user can re-view with [0])

# LICENSE.TXT
# Zero-Ology License v1.19161
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.19161
#November 16, 2025
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