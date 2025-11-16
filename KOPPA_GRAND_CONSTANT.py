# ===================================================================
# KOPPA GRAND CONSTANT — INTERACTIVE SIMULATOR v0011
# Author: Szmy & Grok (xAI)
# Date: November 16, 2025
# KOPPA_GRAND_CONSTANT.PY
# KOPPA_GRAND_CONSTANT_V0011
# Zero-Ology License v1.1916 # 0ko3maibZero-OlogyLicensev1.1916
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

# === LOGGING (UTF-8 safe) ===
LOG_DIR = "koppa_logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"koppa_log_{time.strftime('%Y%m%d_%H%M%S')}.txt")

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
# Predefined pools of constants: name, sympy expression or float approx
CLASSICAL_15 = [
    {"name": "π (Circle constant)", "expr": sp.pi, "approx": 3.1415926536},
    {"name": "e (Natural base)", "expr": sp.E, "approx": 2.7182818285},
    {"name": "√2", "expr": sp.sqrt(2), "approx": 1.4142135624},
    {"name": "φ (Golden ratio)", "expr": (1 + sp.sqrt(5))/2, "approx": 1.6180339887},
    {"name": "γ (Euler–Mascheroni)", "expr": sp.EulerGamma, "approx": 0.5772156649},
    {"name": "Catalan's G", "expr": sp.catalan, "approx": 0.9159655942},  # sympy has catalan constant
    {"name": "Feigenbaum δ", "expr": 4.6692016091, "approx": 4.6692016091},  # Approx, no sympy built-in
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
SAVE_DIR = "koppa_saves"
os.makedirs(SAVE_DIR, exist_ok=True)
STATE_FILE = os.path.join(SAVE_DIR, "koppa_state.pkl")
RESULTS_FILE = os.path.join(SAVE_DIR, "koppa_results.json")
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
    print(" KOPPA GRAND CONSTANT — v0011")
    print(" Szmy. & Grok (xAI) — November 16, 2025")
    print("="*78)
    print(" Self-Normalizing Meta-Constant • Democracy • Expandability • Logs & Saves")
    print("="*78)

# === SAFE EVAL FOR CONSTANTS ===
def get_constant_value(const):
    expr = const["expr"]
    if isinstance(expr, (int, float)):
        return float(expr)
    try:
        return float(sp.N(expr, 10))  # 10 decimal places
    except Exception as e:
        logger.debug(f"Eval error for {const['name']}: {e}")
        return const["approx"]

# === PROGRESS CALLBACK ===
def progress_update(total, elapsed):
    logger.info(f"Progress: {total:,} constants processed | Time: {elapsed:.2f}s")

# ----------------------------------------------------------------------
#  simulation engine (use dynamic full pool + customs)
# ----------------------------------------------------------------------
def simulate(pool_name, precision=10, progress_callback=progress_update):
    logger.info(f"Starting simulation for pool: {pool_name}, precision={precision}")
    
    customs = load_custom_constants()  # <-- load user additions
    
    if pool_name == "classical":
        pool = CLASSICAL_15
    elif pool_name == "full":
        pool = FULL_42 + customs  # <-- add customs to full pool
    else:
        pool = CLASSICAL_15[:int(pool_name)] if pool_name.isdigit() else []
    
    N = len(pool)
    if N == 0:
        return {"koppa": 0, "N": 0, "table": []}
    
    start_time = time.time()
    table = []
    total_contrib = 0
    for i, const in enumerate(pool, 1):
        Ci = get_constant_value(const)
        if Ci <= 0:
            logger.warning(f"Skipping invalid constant {const['name']} (non-positive)")
            continue
        wi = 1 / Ci  # Since koppa = N, wi = 1 / Ci
        contrib = Ci * wi
        table.append({
            "num": i,
            "name": const["name"],
            "approx": round(Ci, precision),
            "weight": round(wi, 5),
            "contrib": round(contrib, 5)
        })
        total_contrib += contrib
        if i % 10 == 0 and progress_callback:
            progress_callback(i, time.time() - start_time)
    
    koppa = total_contrib  # Should be N
    result = {
        "koppa": koppa,
        "N": N,
        "table": table,
        "time_seconds": time.time() - start_time,
        "raw_sum": sum(get_constant_value(c) for c in pool)
    }

    logger.info(f"COMPLETE | Koppa: {koppa} | N: {N} | Raw Sum: {result['raw_sum']:.2f}")
    return result

# === SAVE/LOAD STATE ===
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
    logger.info("No state file found")
    return {}

# === SAVE RESULTS ===
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

    # ---- add paired log for reach ----
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

# === MENU 1: INFO ===
def show_info():
    clear()
    print("\n" + "=" * 78)
    print(" KOPPA GRAND CONSTANT — FORMULA & PHILOSOPHY")
    print("=" * 78)

    print("\n1. Introduction and Philosophy")
    print("The Koppa Grand Constant (Ϟ) is a self-referential meta-constant that aggregates eligible mathematical constants democratically.")
    print("Philosophy: All constants contribute equally, magnitude neutralized via self-normalizing weights.")
    print("Ϟ = N, where N is the number of eligible constants.")

    print("\n2. Eligibility Rules")
    print(" - Computability: Approximable to arbitrary precision.")
    print(" - Consistency: Well-defined canonical value.")
    print(" - Weightability: Positive real value (Ci > 0).")

    print("\n3. Definition")
    print("Ϟ = Σ (Ci * wi), where wi = Ϟ / (N * Ci)")
    print("Self-normalizing: Each Ci * wi = 1, so Ϟ = N.")

    print("\n4. Computation")
    print("Select pool, compute weights wi = 1 / Ci, contributions = 1 each, sum to N.")

    print("\n5. Governance (Koppa Law)")
    print("Pillars: Eligibility, Democracy, Expandability.")
    print("Registry: Submit, Verify, Admit, Immutable.")

    print("\n6. Future Work")
    print("Infinite pools, probabilistic, graph-theoretic extensions, meta-operators.")

    print("\nThis simulator allows exploring pools, computing Ϟ, and expanding via 'reach' modes.")
    print("=" * 78)

    input("\nPress ENTER to continue...")

# === MENU 4: FULL DEMO ===
def full_demo():
    print("\n" + "=" * 60)
    print(" FULL DEMO BY GROK & SZMY")
    print(" Computes for predefined pools.")
    print("=" * 60)
    for config in DEMO_CONFIGS:
        print(f"\nRunning: {config['name']}")
        pool = config["pool"]
        if pool == "custom":
            pool = str(config["size"])
        res = simulate(pool)
        print(f" → Koppa: {res['koppa']} | N: {res['N']} | Raw Sum: {res['raw_sum']:.2f}")
        print_table(res["table"][:3])  # Show first 3 for brevity
    input("\nDemo complete. Press ENTER...")

def print_table(table):
    print("{:<3} {:<30} {:<15} {:<10} {:<10}".format("#", "Constant", "Approx.", "Weight", "Contrib"))
    for row in table:
        print("{:<3} {:<30} {:<15.10f} {:<10.5f} {:<10.5f}".format(row["num"], row["name"][:28], row["approx"], row["weight"], row["contrib"]))

# === MENU 5: THE REACH (expand pool over time) ===
def the_reach():
    print("\n" + "=" * 60)
    print(" THE REACH — TIME-LIMITED POOL EXPANSION")
    print(" Add new constants over time, simulate growing Ϟ.")
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
        "pool": FULL_42.copy(),  # Start with full
        "total": len(FULL_42),
        "elapsed": 0,
        "koppa_history": []
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
                # Simulate adding a new constant (placeholder: random or search)
                new_const = {"name": f"New Const {checkpoint['total']+1}", "expr": sp.pi + checkpoint['total']/1000, "approx": 3.1415 + checkpoint['total']/1000}
                checkpoint["pool"].append(new_const)
                checkpoint["total"] += 1
                res = simulate(str(checkpoint["total"]))  # Use size as pool_name for custom
                checkpoint["koppa_history"].append(res["koppa"])
                if checkpoint["total"] % 5 == 0:
                    progress_update(checkpoint["total"], time.time() - start + elapsed)
        except KeyboardInterrupt:
            print("\nInterrupted.")

        elapsed += time.time() - start
        checkpoint["elapsed"] = elapsed
        save_reach_checkpoint(session_id, checkpoint)

        print(f"\nSession {session_id} — {minutes} min complete.")
        print(f" → Total Constants: {checkpoint['total']:,} | Latest Koppa: {checkpoint['koppa_history'][-1] if checkpoint['koppa_history'] else 0}")

        again = input("\nContinue? (y/n): ").strip().lower()
        if again != 'y':
            break

    input("Press ENTER...")

# ----------------------------------------------------------------------
# INFINITE REACH – pause at end so user can read results
# ----------------------------------------------------------------------
def infinite_reach():
    print("\n" + "=" * 60)
    print(" INFINITE REACH")
    print(" Expand pool forever. Ctrl+C to save & exit.")
    print("=" * 60)

    checkpoint = load_state().get('infinite_checkpoint', {
        "pool": FULL_42.copy(),
        "total": len(FULL_42),
        "koppa_history": []
    })

    def save_checkpoint():
        state = load_state()
        state['infinite_checkpoint'] = checkpoint
        save_state(state)
        logger.info(f"Infinite checkpoint saved: Total {checkpoint['total']:,}")

    def signal_handler(sig, frame):
        print("\n\nCtrl+C detected — saving checkpoint...")
        save_checkpoint()
        print(f"\nReached {checkpoint['total']} constants.")
        print(f"Koppa = {checkpoint['koppa_history'][-1]:.10f} (last value)")
        input("\nPress ENTER to return to menu...\n")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    max_consts = int(input(" Max constants to reach (e.g. 100, default 100): ") or 100)
    precision = int(input(" Precision (default 10): ") or 10)

    total = checkpoint["total"]
    pool = pool = checkpoint["pool"]

    print(" Starting infinite run... (Ctrl+C to save)")
    start = time.time()

    try:
        while total < max_consts:
            new_const = {
                "name": f"New Const {total+1}",
                "expr": sp.E + total/1000,
                "approx": 2.718 + total/1000
            }
            pool.append(new_const)
            total += 1
            res = simulate(str(total), precision)
            checkpoint["koppa_history"].append(res["koppa"])
            if total % 10 == 0:
                progress_update(total, time.time() - start)
            checkpoint = {"pool": pool, "total": total, "koppa_history": checkpoint["koppa_history"]}
            save_checkpoint()

        # --- Normal completion (reached max) ---
        print("\n" + "="*60)
        print(" INFINITE REACH COMPLETE")
        print("="*60)
        print(f"Reached target: {total} constants")
        print(f"Final Koppa: {checkpoint['koppa_history'][-1]:.10f}")
        print(f"Time elapsed: {time.time() - start:.2f} seconds")
        input("\nPress ENTER to return to menu...\n")

    except KeyboardInterrupt:
        # Ctrl+C already handled in signal_handler → will pause & exit
        pass
# ----------------------------------------------------------------------

def save_checkpoint():
    state = load_state()
    state['infinite_checkpoint'] = checkpoint
    save_state(state)
    logger.info(f"Infinite checkpoint saved: Total {checkpoint['total']:,}")

    # ---- add paired log for infinite (use fixed name) ----
    create_save_log("infinite_checkpoint")

    def signal_handler(sig, frame):
        save_checkpoint()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    max_consts = int(input(" Max constants to reach (e.g. 100, default 100): ") or 100)
    precision = int(input(" Precision (default 10): ") or 10)

    total = checkpoint["total"]
    pool = checkpoint["pool"]

    print(" Starting infinite run... (Ctrl+C to save)")
    start = time.time()
    try:
        while total < max_consts:
            new_const = {"name": f"New Const {total+1}", "expr": sp.E + total/1000, "approx": 2.718 + total/1000}
            pool.append(new_const)
            total += 1
            res = simulate(str(total), precision)
            checkpoint["koppa_history"].append(res["koppa"])
            if total % 10 == 0:
                progress_update(total, time.time() - start)
            checkpoint = {"pool": pool, "total": total, "koppa_history": checkpoint["koppa_history"]}
            save_checkpoint()
    except KeyboardInterrupt:
        save_checkpoint()

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
            with open(os.path.join(LOG_DIR, logs[choice-1])) as f:
                print("\n" + f.read())
    except:
        pass
    input("\nPress ENTER...")

# === MANAGE SAVES ===
def list_all_state_files():
    return sorted([f for f in os.listdir(SAVE_DIR) if f.endswith('.pkl') and not f.startswith('reach_')], reverse=True)

# ----------------------------------------------------------------------
#  paired-log helper (no subfolder, prefix with "P_")
# ----------------------------------------------------------------------
def create_save_log(save_name):
    """Create a copy of the current session log named after the save."""
    # ---- no subdir, use main LOG_DIR ----
    paired_name = f"P_{save_name}_paired_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    paired_path = os.path.join(LOG_DIR, paired_name)
    if os.path.exists(LOG_FILE):
        shutil.copy(LOG_FILE, paired_path)
    logger.info(f"Paired log created for save '{save_name}': {paired_path}")
    return paired_path   # return path in case caller wants it
# ----------------------------------------------------------------------


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
    doc_path = os.path.join(os.path.dirname(__file__), "The_Koppa_Grand_Constant.txt")
    if not os.path.exists(doc_path):
        print("\nWarning: Dissertation file 'The Koppa Grand Constant.txt' not found.\n")
        return

    clear()   # optional – keeps screen tidy
    print("\n" + "="*78)
    print(" THE KOPPA GRAND CONSTANT — DISSERTATION")
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
    """Menu: Add new constant OR remove existing ones."""
    while True:
        customs = load_custom_constants()
        print("\n" + "=" * 60)
        print(" MANAGE CUSTOM KONSTANTS (Koppa-Eligible)")
        print("=" * 60)
        if customs:
            print("Current custom constants:")
            for i, c in enumerate(customs, 1):
                print(f" [{i}] {c['name']} ≈ {c['approx']:.10f}")
            print(f"\n [A] Add New Constant")
            print(" [R] Remove One")
            print(" [D] Delete ALL Customs")
            print(" [B] Back")
        else:
            print(" No custom constants yet.")
            print("\n [A] Add New Constant")
            print(" [B] Back")

        sub = input("\n Choose [A/R/D/B]: ").strip().upper()
        logger.info(f"Propose sub-choice: {sub}")

        # --------------------------------------------------------------
        #  ADD NEW
        # --------------------------------------------------------------
        if sub == 'A':
            print("\n" + "-" * 50)
            print(" ADD NEW CONSTANT")
            print("-" * 50)
            print("Rules:")
            print("1. Computable to arbitrary precision")
            print("2. Consistent canonical value")
            print("3. Positive real > 0")
            name = input("\nName: ").strip()
            if not name:
                print("Cancelled.")
                input("\nPress ENTER...")
                continue

            try:
                approx = float(input("Approx value (positive): ").strip())
                if approx <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid: must be positive number.")
                input("\nPress ENTER...")
                continue

            expr = input("SymPy expr (optional): ").strip() or approx

            if input("Computable? (y/N): ").lower() != 'y':
                print("Failed computability.")
                input("\nPress ENTER...")
                continue
            if input("Consistent? (y/N): ").lower() != 'y':
                print("Failed consistency.")
                input("\nPress ENTER...")
                continue

            customs.append({"name": name, "expr": expr, "approx": approx})
            save_custom_constants(customs)
            print(f"\nAdded: {name} ≈ {approx:.10f}")
            print(f"Koppa pool size now: {len(FULL_42) + len(customs)}")
            input("\nPress ENTER...")

        # --------------------------------------------------------------
        #  REMOVE ONE
        # --------------------------------------------------------------
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
                print(f"\nRemoved: {removed['name']}")
                print(f"Koppa pool size now: {len(FULL_42) + len(customs)}")
            else:
                print("Invalid index.")
            input("\nPress ENTER...")

        # --------------------------------------------------------------
        #  DELETE ALL
        # --------------------------------------------------------------
        elif sub == 'D' and customs:
            if input("Delete ALL custom constants? (y/N): ").lower() == 'y':
                os.remove(CUSTOM_CONSTANTS_FILE)
                print("All custom constants deleted.")
            input("\nPress ENTER...")

        # --------------------------------------------------------------
        #  BACK
        # --------------------------------------------------------------
        elif sub == 'B':
            break

        else:
            print("Invalid choice.")
            input("\nPress ENTER...")
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
#   MAIN MENU – [9] now calls the full manager
# ----------------------------------------------------------------------
def main():
    state = load_state()
    while True:
        banner()
        print("\n [0] View Dissertation")
        print(" [1] View Formula & Info")
        print(" [2] Run Custom Simulation")
        print(" [3] Exit")
        print(" [4] FULL DEMO by Grok & SZMY")
        print(" [5] THE REACH (time-limited expansion)")
        print(" [6] INFINITE REACH (save/resume)")
        print(" [7] View Logs")
        print(" [8] Manage Saves")
        print(" [9] Manage Custom Constants")   # ← clearer label
        print()
        choice = input(" Choose [0-9]: ").strip()
        logger.info(f"Menu choice: {choice}")

        if choice == '0':
            show_dissertation()
        elif choice == '1':
            show_info()
        elif choice == '2':
            pool = input(" Pool (classical/full/N for custom size, default full): ") or "full"
            prec = input(" Precision (default 10): ") or "10"
            try:
                prec = int(prec)
                res = simulate(pool, prec)
                save_results(res)
                print(f"\n Koppa: {res['koppa']} | N: {res['N']}")
                print_table(res["table"])
            except ValueError:
                logger.error("Invalid input.")
            input("\nPress ENTER...")
        elif choice == '3':
            logger.info("Exiting program.")
            print("\nKoppa grows eternally. ∞")
            break
        elif choice == '4':
            full_demo()
        elif choice == '5':
            the_reach()
        elif choice == '6':
            infinite_reach()          # ← **THIS WAS MISSING** (typo in your copy?)
        elif choice == '7':
            view_logs()
        elif choice == '8':
            manage_saves()
        elif choice == '9':
            propose_new_constant()
        save_state(state)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    show_dissertation()   # <-- shows it **once** at launch
    main()                # <-- then interactive loop (user can re-view with [0])

# LICENSE.TXT
# Zero-Ology License v1.1916
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.1916
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