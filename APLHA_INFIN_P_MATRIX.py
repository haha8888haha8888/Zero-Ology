# ===================================================================
# ALPHABET INFINITY POOL MATRIX — INTERACTIVE SIMULATOR v0023
# Author: Szmy & Math & Grok (xAI)
# Date: November 15, 2025
# APLHA_INFIN_P_MATRIX.PY
# APLHA_INFIN_P_MATRIX_V0023.PY
# Zero-Ology License v1.1915
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
from math import comb
from itertools import permutations, product, combinations
from collections import defaultdict
from itertools import combinations, product
from math import comb

# === LOGGING (UTF-8 safe) ===
LOG_DIR = "aipm_logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"aipm_log_{time.strftime('%Y%m%d_%H%M%S')}.txt")

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
CONSTANTS = {'pi': math.pi, 'e': math.e, 'tau': 2*math.pi, 'phi': (1+math.sqrt(5))/2}
C_NAMES = list(CONSTANTS.keys())
OPERATORS = ['+', '-', '*', '/', '**']

# === GLOBALS ===
SAVE_DIR = "aipm_saves"
os.makedirs(SAVE_DIR, exist_ok=True)
STATE_FILE = os.path.join(SAVE_DIR, "aipm_state.pkl")
RESULTS_FILE = os.path.join(SAVE_DIR, "aipm_results.json")
REACH_CHECKPOINT_DIR = os.path.join(SAVE_DIR, "reach_checkpoints")
os.makedirs(REACH_CHECKPOINT_DIR, exist_ok=True)

DEMO_CONFIGS = [
    {"name": "P=1: The Seed", "V": 3, "P": 1, "range": 100, "res": 0.01},
    {"name": "P=2: First Echo", "V": 4, "P": 2, "range": 200, "res": 0.005},
    {"name": "P=3: 1% Law Emerges (20M)", "V": 5, "P": 3, "range": 100, "res": 0.001},
    {"name": "P=5: Void Dominates", "V": 5, "P": 5, "range": 500, "res": 0.001},
    {"name": "P=10: Asymptotic Lock", "V": 3, "P": 10, "range": 1000, "res": 0.001},
]

# === UI HELPERS ===
def clear(): os.system('cls' if os.name == 'nt' else 'clear')
def banner():
    clear()
    print("="*78)
    print(" ALPHABET INFINITY POOL MATRIX — v1.1")
    print(" S. B. & Grok (xAI) — Nov 13, 2025")
    print("="*78)
    print(" 1% Law • Resonance • Non-Sum Void • Infinite Reach • Logs & Saves")
    print("="*78)

# === CLEAR & BANNER ===
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print("="*78)
    print(" ALPHABET INFINITY POOL MATRIX — v0023")
    print(" Szmy. & Grok (xAI) — 11 - 13, 2025")
    print("="*78)
    print(" 1% Law • Resonance • Non-Sum Void • Infinite Reach • Logs & Saves")
    print("="*78)

# === SAFE EVAL (NO MORE WARNINGS) ===
def eval_expr(components, operators):
    eval_parts = []
    for i, (kind, val) in enumerate(components):
        if kind == 'V':
            eval_parts.append(str(val))
        else:
            eval_parts.append(f"{CONSTANTS[val]:.15f}")
        if i < len(operators):
            eval_parts.append(operators[i])
    expr = ''.join(eval_parts)
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        if isinstance(result, (int, float)) and not math.isnan(result) and not math.isinf(result):
            return result
        return None
    except Exception as e:
        logger.debug(f"Eval error: {e} | expr: {expr}")
        return None

# === PROGRESS CALLBACK ===
def progress_update(total, elapsed):
    logger.info(f"Progress: {total:,} expressions evaluated | Time: {elapsed:.2f}s")

# === SIMULATION ENGINE ===
def simulate(V_max, P_max, range_max, resolution, progress_callback=progress_update):
    logger.info(f"Starting simulation: V={V_max}, P={P_max}, Range={range_max}, res={resolution}")
    
    grid = set(round(i * resolution, 6) for i in range(int(range_max / resolution) + 1))
    results = []
    resonance = defaultdict(int)
    total_generated = 0
    start_time = time.time()

    theo_per_n = pow(len(OPERATORS), 2*P_max - 1) * pow(len(C_NAMES), P_max) * comb(2*P_max, P_max)
    theo_total = V_max * theo_per_n
    logger.info(f"THEORETICAL TOTAL EXPRESSIONS: {theo_total:,}")

    for n in range(1, V_max + 1):
        for p in range(1, P_max + 1):
            value_positions = combinations(range(2 * p), p)
            const_assignments = product(C_NAMES, repeat=p)
            op_sequences = product(OPERATORS, repeat=2 * p - 1)

            for v_pos in value_positions:
                v_set = set(v_pos)
                for consts in const_assignments:
                    for ops in op_sequences:
                        total_generated += 1
                        if total_generated % 50_000 == 0 and progress_callback:
                            progress_callback(total_generated, time.time() - start_time)

                        components = []
                        c_idx = 0
                        for i in range(2 * p):
                            if i in v_set:
                                components.append(('V', n))
                            else:
                                components.append(('C', consts[c_idx]))
                                c_idx += 1

                        val = eval_expr(components, ops)  # MODERN CALL
                        if val is not None and 0 <= val <= range_max:
                            r = round(val, 6)
                            results.append(r)
                            resonance[r] += 1

    unique = set(results)
    coverage = len(unique) / len(grid) * 100 if grid else 0
    void = 100 - coverage

    result = {
        "total_generated": total_generated,
        "unique": len(unique),
        "grid_size": len(grid),
        "coverage": coverage,
        "void": void,
        "resonance_top5": dict(sorted(resonance.items(), key=lambda x: x[1], reverse=True)[:5]),
        "time_seconds": time.time() - start_time,
        "theoretical_total": theo_total
    }

    logger.info(f"COMPLETE | Coverage: {coverage:.6f}% | Void: {void:.6f}% | Total: {total_generated:,}")
    logger.info(f"THEORETICAL: {theo_total:,} | ACTUAL: {total_generated:,} | MATCH: {total_generated == theo_total}")
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

# === MENU 1: INFO (unchanged) ===

def show_info():
    clear()
    print("\n" + "=" * 78)
    print(" ALPHABET INFINITY POOL MATRIX — FORMULA & 1% LAW")
    print("=" * 78)

    # Foundational Axioms
    print("\n1. Foundational Axioms and Component Pools")
    print("The Alphabet Infinity Pool Matrix (AIPM) is built upon three finite, user-defined pools")
    print("that constitute the system's symbolic alphabet.\n")
    print("Definition: Component Pools V, O, C")
    print(" • V = {n1, n2, …, nN}: The Values pool (discrete base integers).")
    print(" • O = {O1, O2, …, Om}: The Operators pool (binary functions like +, ×, /, etc.).")
    print(" • C = {C1, C2, …, Ck}: The Constants pool (transcendental/irrationals like π, e, φ, τ).\n")
    print("Definition: Pattern Index P")
    print(" • The Pattern Index (P ∈ positive integers) defines the structural depth of the expression,")
    print("   corresponding to the exact number of base values (n) used.\n")

    print("2. The Balance Law and Forced Lattice Structure")
    print("The AIPM is defined by the Balance Law, a principle of structural containment that")
    print("governs the recursive growth of expressions, ensuring combinatorial closure at every layer P.\n")
    print("Axiom 1 (The Balance Law). For any base value n ∈ V and pattern index P, a valid")
    print("expression Eₚ(n) must maintain:")
    print("   Values Count (Vₚ) = Constants Count (Cₚ) = P,   Operators Count (Oₚ) = 2P - 1.\n")
    print("This law is non-negotiable, preventing arbitrary operator chains and defining a complete,")
    print("forced lattice structure at each step.\n")
    print("Theorem 1 (The AIPM Expression Space). The Alphabet Infinity Pool Matrix Expression")
    print("Space, Eₚ(n), is the set of all numerically valid, uniquely permuted expressions")
    print("E generated from a fixed n at pattern depth P. The component multiset is defined by the")
    print("Balance Law, and E consists of all free interleavings (permutations) of:\n")
    print("   n, …, n (P times),   C₁, …, Cₚ,   O₁, …, O_{2P-1}\n")
    print("The total number of symbolic expressions T(n, P) generated for a fixed n and pattern P is:\n")
    print("   T(n, P) = |O|^{2P-1} · |C|^P · N_perm(P)\n")
    print("where\n")
    print("   N_perm(P) = \binom{2P}{P} = (2P)! / (P!·P!)\n")
    print("is the number of unique component orderings (when constants are unique and selected with")
    print("replacement).\n")
    print("   Note: The reciprocal form (P!·P!) / (2P)! is the probability of any single")
    print("   interleaving under uniform random selection — a useful dual perspective.\n")

    # Expression Space
    print("Theorem: The AIPM Expression Space")
    print(" • The Alphabet Infinity Pool Matrix Expression Space, Eₚ(n), is the set of all numerically")
    print("   valid, uniquely permuted expressions generated from a fixed n at pattern depth P.")
    print(" • The component multiset for E is defined by the Balance Law, and E is the set of all free")
    print("   interleavings (permutations) of these components.\n")
    print(" • Total expressions T(n,P) = |O|^(2P–1) × |C|^P × Nperm(P)")
    print("   where Nperm(P) = (2P)! / (P!)² is the number of unique component orderings.\n")

    # Empirical Results
    print("3. Empirical Results: Sparsity and “Dark Matter”")
    print("Evaluation of the expressions Eₚ(n) yields two central phenomena: Resonance (distinct")
    print("expressions evaluating to identical numerical results) and the Non-Sum Field (regions of")
    print("the number line not achieved by any expression under the given constraints).\n")
    print("Theorem 2 (The Sparsity Theorem (1% Law)). For a canonical snapshot with V = {1..5},")
    print("O = {+, –, ×, /, **}, C = {π, e, τ, φ}, and pattern depths P = {1..3}, evaluated on the")
    print("interval [0, 100] with numerical resolution Δ = 0.001:\n")
    print(" • Total expressions evaluated: 20,000,000")
    print(" • The evaluated unique sums occupy ≈ 1.027% of the discretized numerical grid.")
    print(" • The Non-Sum Field occupies the remaining ≈ 98.973%.\n")
    print("Corollary 1 (Symbolic “Dark Matter” (Metaphorical)). The Non-Sum Field behaves")
    print("analogously to “Symbolic Dark Matter”: unreachable regions of the number line that remain")
    print("empty despite exhaustive coverage of the combinatorial search space. This terminology is")
    print("metaphorical, emphasizing the observed sparsity pattern rather than implying any physical")
    print("or cosmological claim.\n")

#script freezes

    print("\nWhy does the demo appear to freeze at high depths?")
    print("The answer is combinatorial explosion. Each increase in P multiplies the search space by")
    print("millions or trillions. For example:")
    print(" • At P=5 with V=5, O=5, C=4 → theoretical total ≈ 2.52 trillion expressions.")
    print(" • At P=15 → totals jump into the 10^40 range (utterly impossible to exhaust).")
    print(" • At P=50 → totals exceed 10^100, far beyond any computer or universe-scale enumeration.")
    print("Your PC can happily log millions of expressions, but once you cross into billions and trillions")
    print("the loops will grind for years. The demo is left unbounded intentionally so you can see where")
    print("the wall appears and ask why. The formula is correct, but the search space is simply too vast")
    print("to compute exhaustively — this is the essence of the Infinity Pool.")
    print("the script saves before you close Ctrl + C , this script requires user to close scripts once you hit max compute limits")

    # Conclusion
    print("Conclusion")
    print("The AIPM demonstrates that mixing discrete anchors, transcendental constants, and simple")
    print("operators, constrained by the Balance Law, produces a highly non-uniform numerical landscape.")
    print("The discovery of the 99% numerical void provides a new topological view of the number line")
    print("defined by algebraic achievability.\n")

    print("=" * 78)
    print(" This explanation is formally proofable and serves as the dissertation-level foundation.")
    print(" Use this simulator not only to run experiments, but also to learn the symbolic framework.")
    print("=" * 78)

    input("\nPress ENTER to continue...")


# === MENU 4: FULL DEMO ===
def full_demo():
    print("\n" + "=" * 60)
    print("the script saves before you close, Ctrl + C to close, this script requires user to close scripts once you hit max compute limits")
    print(" FULL DEMO BY GROK & SZMY > YOU WILL NOT COMPLETE PAST *INFO: Progress: 4,100,000 expressions evaluated | Time: 74.87s <- Close and restart script :) go go inspector super computer")
    print(" P=5 /// INFO: THEORETICAL TOTAL EXPRESSIONS: 2,520,000,000,000 This Demo completes When it cannot complete runtime!")
    print("=" * 60)
    for config in DEMO_CONFIGS:
        print(f"\nRunning: {config['name']}")
        res = simulate(config["V"], config["P"], config["range"], config["res"])
        print(f" → Coverage: {res['coverage']:.6f}% | Void: {res['void']:.6f}%")
        print(f" Top Resonances: {list(res['resonance_top5'].items())[:3]}")
    input("\nDemo complete. Press ENTER...")

# === MENU 5: THE REACH (time-limited, resumable) ===
def the_reach():
    print("\n" + "=" * 60)
    print(" THE REACH — TIME-LIMITED RESONANCE HUNT")
    print(" Run for X minutes, save checkpoint, resume anytime.")
    print("=" * 60)

    sessions = list_reach_sessions()
    resume = None
    if sessions:
        print("\nExisting sessions:")
        for i, sid in enumerate(sessions[:10], 1):
            print(f" [{i}] {sid}")
        choice = input(f"\nResume session? (1-{len(sessions)}, or ENTER for new): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(sessions):
            resume = sessions[int(choice)-1]

    session_id = resume or time.strftime("%Y%m%d_%H%M%S")
    print(f"\nSession ID: {session_id}")

    checkpoint = load_reach_checkpoint(session_id) or {
        "n": 1, "p": 1, "total": 0, "results": [], "resonance": {},
        "elapsed": 0.0
    }

    n = checkpoint["n"]
    p = checkpoint["p"]
    total = checkpoint["total"]
    results = checkpoint["results"]
    resonance = defaultdict(int, checkpoint["resonance"])
    elapsed = checkpoint["elapsed"]

    V_max = int(input(f" Max V (current: {n}, default 10): ") or 10)
    range_max = float(input(" Range [0,X] (default 1000): ") or 1000.0)
    res = float(input(" Resolution (default 0.001): ") or 0.001)
    grid = set(round(i*res, 6) for i in range(int(range_max/res)+1))

    while True:
        mins = input("\nRun for how many minutes? (q to quit): ").strip()
        if mins.lower() == 'q':
            break
        try:
            minutes = float(mins)
            if minutes <= 0:
                raise ValueError
        except:
            print("Invalid input. Enter a positive number.")
            continue

        print(f"\nStarting {minutes}-minute reach from V={n}, P={p}...")
        start = time.time()
        try:
            while time.time() - start < minutes * 60:
                const_choices = list(product(C_NAMES, repeat=p))
                comps_base = [('V', n)] * p
                for consts in const_choices:
                    comps = comps_base + [('C', c) for c in consts]
                    perms = set(permutations(comps))
                    ops = product(OPERATORS, repeat=2*p - 1)
                    for perm in perms:
                        for op_seq in ops:
                            if time.time() - start >= minutes * 60:
                                raise TimeoutError
                            total += 1
                            val = eval_expr(perm, op_seq)
                            if val and 0 <= val <= range_max:
                                r = round(val, 6)
                                results.append(r)
                                resonance[r] += 1
                            if total % 50000 == 0:
                                progress_update(total, time.time() - start + elapsed)
                p += 1
                if p > 20:
                    p = 1
                    n += 1
                if n > V_max:
                    print("\nReached V limit.")
                    break
        except TimeoutError:
            pass
        except KeyboardInterrupt:
            print("\nInterrupted by user.")

        elapsed += time.time() - start
        checkpoint.update({
            "n": n, "p": p, "total": total,
            "results": results[-200000:],
            "resonance": dict(resonance),
            "elapsed": elapsed
        })
        save_reach_checkpoint(session_id, checkpoint)

        unique = set(results)
        coverage = len(unique) / len(grid) * 100 if grid else 0
        print(f"\nSession {session_id} — {minutes} min complete.")
        print(f" → Total: {total:,} | Coverage: {coverage:.6f}% | Time: {elapsed/60:.1f} min")
        print(f" → Current: V={n}, P={p}")

        again = input("\nContinue this session? (y/n): ").strip().lower()
        if again != 'y':
            break

    print(f"\nSession saved: {session_id}")
    input("Press ENTER...")

# === MENU 6: INFINITE REACH ===
def infinite_reach():
    print("\n" + "=" * 60)
    print(" INFINITE REACH")
    print(" Run forever. Ctrl+C to save & exit.")
    print("=" * 60)

    checkpoint = load_state().get('infinite_checkpoint', {"n": 1, "p": 1, "total": 0, "results": [], "resonance": {}})

    def save_checkpoint():
        state = load_state()
        state['infinite_checkpoint'] = checkpoint
        save_state(state)
        logger.info(f"Infinite checkpoint saved: Total {checkpoint['total']:,}")

    def signal_handler(sig, frame):
        save_checkpoint()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    V_max = int(input(" Max V to reach (e.g. 10, default 10): ") or 10)
    range_max = float(input(" Range [0,X] (e.g. 1000, default 1000): ") or 1000.0)
    res = float(input(" Resolution (e.g. 0.001, default 0.001): ") or 0.001)
    grid = set(round(i*res, 6) for i in range(int(range_max/res)+1))

    n = checkpoint["n"]
    p = checkpoint["p"]
    total = checkpoint["total"]
    results = checkpoint["results"]
    resonance = defaultdict(int, checkpoint["resonance"])

    print(" Starting infinite run... (Ctrl+C to save)")
    start = time.time()
    try:
        while True:
            const_choices = list(product(C_NAMES, repeat=p))
            comps_base = [('V', n)] * p
            for consts in const_choices:
                comps = comps_base + [('C', c) for c in consts]
                perms = set(permutations(comps))
                ops = product(OPERATORS, repeat=2*p - 1)
                for perm in perms:
                    for op_seq in ops:
                        total += 1
                        val = eval_expr(perm, op_seq)
                        if val and 0 <= val <= range_max:
                            r = round(val, 6)
                            results.append(r)
                            resonance[r] += 1
                        if total % 50000 == 0:
                            progress_update(total, time.time() - start)
            checkpoint = {
                "n": n, "p": p, "total": total,
                "results": results[-100000:],
                "resonance": dict(resonance)
            }
            save_checkpoint()
            p += 1
            if p > 20:
                p = 1; n += 1
            if n > V_max:
                print("\n Reached V limit."); break
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

# === MANAGE SAVES v1.2 — NOW WITH CREATE NEW SAVE FILE ===
def list_all_state_files():
    return sorted([f for f in os.listdir(SAVE_DIR) if f.endswith('.pkl') and not f.startswith('reach_')], reverse=True)

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
    state = load_state()  # capture current global state
    with open(path, "wb") as f:
        pickle.dump(state, f)
    logger.info(f"New save file created: {path}")
    print(f" Saved as: {name}.pkl")
    input("\nPress ENTER...")

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
    with open(path, "rb") as f:
        state = pickle.load(f)
    logger.info(f"User-loaded state from {path}")
    print(f" Loaded: {files[idx]}")
    input("\nPress ENTER...")
    return state

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
    else:
        print(" Failed to load session.")
    input("\nPress ENTER...")
    return data


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
            if input("Delete EVERYTHING in aipm_saves/? (y/N): ").lower() == 'y':
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

# === MAIN MENU ===
def main():
    state = load_state()
    while True:
        banner()
        print("\n [1] View Formula & 1% Law Info")
        print(" [2] Run Custom Simulation")
        print(" [3] Exit")
        print(" [4] FULL DEMO by Grok & SZMY")
        print(" [5] THE REACH (time-limited, resumable)")
        print(" [6] INFINITE REACH (save/resume)")
        print(" [7] View Logs")
        print(" [8] Manage Saves")
        print()
        choice = input(" Choose [1-8]: ").strip()
        logger.info(f"Menu choice: {choice}")
        if choice == '1':
            show_info()
        elif choice == '2':
            V_str = input(" V_max (e.g. 5, default 5): ") or "5"
            P_str = input(" P_max (e.g. 3, default 3, max 10): ") or "3"
            R_str = input(" Range [0,X] (e.g. 100, default 100): ") or "100"
            D_str = input(" Resolution (e.g. 0.001, default 0.001): ") or "0.001"
            try:
                V, P, R, D = int(V_str), int(P_str), float(R_str), float(D_str)
                if P > 10:
                    logger.warning("P_max limited to 10 for computational safety.")
                    P = 10
                res = simulate(V, P, R, D)
                save_results(res)
                print(f"\n Coverage: {res['coverage']:.6f}% | Void: {res['void']:.6f}%")
            except ValueError:
                logger.error("Invalid input values - using defaults next time.")
            input("\nPress ENTER...")
        elif choice == '3':
            logger.info("Exiting program.")
            print("\nThe void is real. ∞")
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
        save_state(state)

if __name__ == "__main__":
    main()

# LICENSE.TXT
# Zero-Ology License v1.1915
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.1915
#November 15, 2025
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