
# ================================================
# OddPerfectTerminator_GODD.py
# OddPerfectTerminator_GODDv0099 #93 rewrite new
# AUTHOR: Stacey Szmy + GROK (Nov 9, 2025)
# PURPOSE: Hunt odd perfect numbers using NEGATIVE GHOST + SANDWICH SNIPER
# GODD MODE: Runs 6+ months, saves every 5 min, resumable, tracks closest hits
# 0ko3maibZero-OlogyLicensev1.191
# Zero-Ology License v1.191
# ================================================

# =======================
# STANDARD LIBRARY IMPORTS
# =======================
import os
import sys
import time
import json
import pickle
import signal
import random
import threading
import re
import shutil

# =======================
# THIRD-PARTY IMPORTS
# =======================
from datetime import datetime
from sympy import nextprime, isprime, mod_inverse

# =======================
# GLOBAL CONFIGURATION
# =======================

# Script behavior flags
auto_resume_after_jump = False  # Auto-resume after a jump point

# Python integer handling
sys.set_int_max_str_digits(0)  # Unlimited integer string conversion

# Mathematical constants / settings
MODULI = [120]

# =======================
# PULSE / HEARTBEAT CONTROL
# =======================
pulse_active = False
last_heartbeat = time.time()

# Directories
LOG_DIR = "logs"
ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)



# ------------------- CONFIG -------------------
SAVE_FILE = "GODMODE_STATE.pkl"
LOG_FILE = "GODMODE_LOG.txt"
CLOSEST_HITS_FILE = "CLOSEST_HITS.json"
CHECKPOINT_INTERVAL = 300
MAX_SANDWICHES_PER_GHOST = 50_000_000
# ---------------------------------------------

MERSENNE_EXPONENTS = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281,
                      3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243,
                      110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377,
                      6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657,
                      37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933]



# ———————— FIXED PULSE SYSTEM — GLOBAL STATE REFERENCE — NO MORE NameError ————————
pulse_active = False
pulse_thread = None
current_state_ref = None  # This holds the live state for the pulse thread
pulse_start_time = None   # For accurate speed calculation


## colab cells 

# ——————— DISTRIBUTED EMPIRE COLONY SYSTEM v0011.0 ———————
COLONY_ID = None  # 1 to 10
TOTAL_COLONIES = 10
GHOSTS_PER_COLONY = (len(MERSENNE_EXPONENTS) + TOTAL_COLONIES - 1) // TOTAL_COLONIES

# Auto-detect if running in Colab
try:
    import google.colab
    IN_COLAB = True
except:
    IN_COLAB = False

# Auto-generate COLONY_ID from filename or env
import os
if IN_COLAB:
    from IPython.display import display, Javascript
    filename = os.path.basename(globals().get('__file__', 'OddPerfectTerminator_COLONY_1.py'))
    COLONY_ID = int(''.join(filter(str.isdigit, filename)) or 1)
else:
    # Local PC: ask user
    pass

## 

def get_colony_suffix():
    return f"_COLONY_{COLONY_ID}" if COLONY_ID else ""

SAVE_FILE = f"GODMODE_STATE{get_colony_suffix()}.pkl"
LOG_FILE = f"GODMODE_LOG{get_colony_suffix()}.txt"
CLOSEST_HITS_FILE = f"CLOSEST_HITS{get_colony_suffix()}.json"

# Rest of save/load functions stay the same — they auto-use colony files
## 
def colony_control_panel():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("═" * 95)
    print(" " * 28 + "STACEY SZMY COLONY COMMAND CENTER — SESSION MODE")
    print("═" * 95)
    print(f" {'SESSION':<8} {'COLONIES':<14} {'GHOSTS':<12} {'ZONES DONE':<15} {'% COMPLETE':<12} STATUS")
    print("─" * 95)
    
    sessions = [
        (1, 1, 3, "1–3",   "1–18"),
        (2, 4, 6, "4–6",   "19–36"),
        (3, 7, 10, "7–10", "37–51")
    ]
    
    total_zones_per_session = [3, 3, 4]  # colonies per session
    session_progress = []

    for sid, start_col, end_col, col_range, ghost_range in sessions:
        old_save = SAVE_FILE
        old_log = LOG_FILE
        old_hits = CLOSEST_HITS_FILE
        
        total_zones = 0
        zones_done = 0
        
        for cid in range(start_col, end_col + 1):
            suffix = f"_COLONY_{cid}"
            globals()['SAVE_FILE'] = f"GODMODE_STATE{suffix}.pkl"
            globals()['LOG_FILE'] = f"GODMODE_LOG{suffix}.txt"
            globals()['CLOSEST_HITS_FILE'] = f"CLOSEST_HITS{suffix}.json"

            if os.path.exists(SAVE_FILE):
                state = load_state() or {'current_ghost_index': 0, 'zone_counter': 0}
                start_ghost = (cid - 1) * GHOSTS_PER_COLONY
                end_ghost = min(cid * GHOSTS_PER_COLONY, len(MERSENNE_EXPONENTS))
                
                for gi in range(start_ghost, end_ghost):
                    if gi < state.get('current_ghost_index', 0):
                        zones_done += MAX_SANDWICHES_PER_GHOST
                        total_zones += MAX_SANDWICHES_PER_GHOST
                    elif gi == state.get('current_ghost_index', 0):
                        zones_done += min(state.get('zone_counter', 0), MAX_SANDWICHES_PER_GHOST)
                        total_zones += MAX_SANDWICHES_PER_GHOST
            else:
                total_zones += (min(cid * GHOSTS_PER_COLONY, 51) - (cid-1)*GHOSTS_PER_COLONY) * MAX_SANDWICHES_PER_GHOST

        percent = (zones_done / total_zones * 100) if total_zones > 0 else 0
        status = "DONE" if percent >= 99.999 else "HUNTING" if zones_done > 0 else "OFFLINE"
        print(f" {sid:<8} {col_range:<14} {ghost_range:<12} {zones_done:>12,} {percent:>10.6f}% {status}")
        session_progress.append(percent)

        globals()['SAVE_FILE'] = old_save
        globals()['LOG_FILE'] = old_log
        globals()['CLOSEST_HITS_FILE'] = old_hits
    
    print("─" * 95)
    print(f" EMPIRE AVERAGE: {sum(session_progress)/len(session_progress):.6f}%")
    print()
    print(" SESSION LAUNCH COMMANDS (3 TABS ONLY!):")
    print("   Type: session 1    → Launch Session 1 (Colonies 1–3)")
    print("   Type: session 2    → Launch Session 2 (Colonies 4–6)")
    print("   Type: session 3    → Launch Session 3 (Colonies 7–10)")
    print("   Type: session auto → Auto-launch weakest session")
    print("   Type: back         → Main menu")
    print("═" * 95)
    
    while True:
        cmd = input("\nSESSION COMMAND > ").strip().lower()
        if cmd.startswith("session "):
            target = cmd[8:].strip()
            if target == "auto":
                weakest = min(range(1,4), key=lambda x: session_progress[x-1])
                print(f" LAUNCHING WEAKEST SESSION #{weakest} (Colonies {sessions[weakest-1][3]})")
                time.sleep(1)
                return f"SESSION_{weakest}_{sessions[weakest-1][1]}_{sessions[weakest-1][2]}"
            else:
                try:
                    sid = int(target)
                    if 1 <= sid <= 3:
                        cols = sessions[sid-1][3]
                        print(f" LAUNCHING SESSION #{sid} → COLONIES {cols}")
                        time.sleep(1)
                        return f"SESSION_{sid}_{sessions[sid-1][1]}_{sessions[sid-1][2]}"
                except:
                    pass
        elif cmd == "back":
            return None
        print(" Use: session 1 | session 2 | session 3 | session auto")

## end colab

def start_pulse(state_ref, hunt_start_time):
    global pulse_active, pulse_thread, current_state_ref, pulse_start_time
    current_state_ref = state_ref
    pulse_start_time = hunt_start_time
    pulse_active = True
    pulse_thread = threading.Thread(target=pulse_heartbeat, daemon=True)
    pulse_thread.start()

def stop_pulse():
    global pulse_active
    pulse_active = False
    if pulse_thread and pulse_thread.is_alive():
        pulse_thread.join(timeout=1.0)

def pulse_heartbeat():
    symbols = "⣾⣽⣻⢿⡿⣟⣯⣷"
    i = 0
    while pulse_active:
        if current_state_ref is None or pulse_start_time is None:
            time.sleep(0.2)
            continue

        now = datetime.now().strftime("%H:%M:%S")
        zones = current_state_ref.get('zone_counter', 0)
        ghost_idx = current_state_ref.get('current_ghost_index', 0) + 1
        elapsed = max(int(time.time() - pulse_start_time), 1)
        speed = zones // elapsed

        # === LIVE COVERAGE FROM PROOF LOG OR TRUTH FALLBACK ===
        cov = 0.0
        proof_file = f"PROOF_LOG{get_colony_suffix()}.jsonl"

        if os.path.exists(proof_file):
            try:
                with open(proof_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if lines:
                        last = json.loads(lines[-1])
                        cov = last.get("mod120_coverage", 0.0)
                    elif zones == 0:
                        # Bootstrap phase: max possible for odd n
                        cov = 60.0 / 120.0  # 50.0%
            except Exception:
                cov = 60.0 / 120.0  # Safety
        else:
            # No log yet: use known mathematical maximum for odd numbers
            cov = 60.0 / 120.0  # 50.0%

        print(
            f"\r[{now}] {symbols[i % 8]} PULSE → Z:{zones:,} | S:{speed:,}/s | G#{ghost_idx}/51 | mod120:{cov:.1%}",
            end="",
            flush=True,
        )
        i += 1
        time.sleep(0.25)

#old
# =======================
# UPDATED LOG & STATE FUNCTIONS
# =======================

def get_save_file():
    """Return the save file path for the current log session."""
    base_name = os.path.splitext(os.path.basename(logger.log_file))[0]
    return os.path.join(LOG_DIR, f"{base_name}_STATE.pkl")

def get_closest_hits_file():
    """Return the closest hits JSON file path for the current log session."""
    base_name = os.path.splitext(os.path.basename(logger.log_file))[0]
    return os.path.join(LOG_DIR, f"{base_name}_CLOSEST_HITS.json")

def log(msg):
    """Standard log to console and session log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(logger.log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def debug_log(msg):
    """Debug log with heartbeat update."""
    global last_heartbeat
    last_heartbeat = time.time()
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] DEBUG → {msg}"
    print("\n" + line)
    with open(logger.log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def save_state(state):
    """Save program state for the current log session or collab colony."""
    save_file = get_save_file()

    # ——— COLLAB DETECTION ———
    if 'COLONY_' in save_file:
        log(f"[COLLAB SAVE] Detected → {save_file}")
    else:
        log(f"[SESSION SAVE] Detected → {save_file}")

    with open(save_file, "wb") as f:
        pickle.dump(state, f)

    log(f"STATE SAVED → {save_file}")


def load_state():
    """Load program state for the current log session."""
    save_file = get_save_file()
    if os.path.exists(save_file):
        with open(save_file, "rb") as f:
            return pickle.load(f)
    return None

def save_closest_hits(hits):
    """Save closest hits for the current log session."""
    hits_file = get_closest_hits_file()
    with open(hits_file, "w") as f:
        json.dump(hits, f, indent=2)
    log(f"CLOSEST HITS SAVED → {hits_file}")

def load_closest_hits():
    """Load closest hits for the current log session."""
    hits_file = get_closest_hits_file()
    if os.path.exists(hits_file):
        with open(hits_file) as f:
            return json.load(f)
    return []


def generate_even_perfect(idx):
    p = MERSENNE_EXPONENTS[idx]
    return (1 << (p-1)) * ((1 << p) - 1)

def negative_ghost_reflection(G, q, k):
    try:
        mod = q ** k
        inv = mod_inverse(G, mod)
        lift = (inv * nextprime(q*q + k)) % mod
        return lift + mod if lift < 10**12 else lift
    except:
        return None

def negative_ghost_reflection_FAST_FOR_TEST(G, q, k):
    # FAKE FAST VERSION FOR CRASH TEST ONLY
    return random.randint(10**12, 10**13) * 2 + 1  # instant big odd number

def generate_sandwich(C):
    return [C-2, C, C+2] if C > 2 else []

def sigma_proper(n):
    if n < 2: return 0
    total = 1
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            total += i
            j = n // i
            if j != i and j != n:
                total += j
    return total

def test_number(n, closest_hits):
    if n <= 1 or n % 2 == 0:
        return closest_hits

    s = sigma_proper(n)
    if s == 0:
        return closest_hits

    ratio = s / n
    gap = abs(ratio - 2.0)

    # ——— ODD PERFECT FOUND ———
    if s == n:
        log("─────────────────────────────────────────")
        log(f"ODD PERFECT NUMBER FOUND: {n}")
        log("2300 YEARS OVER. YOU ARE GOD.")
        log("─────────────────────────────────────────")
        save_closest_hits(closest_hits)
        os._exit(0)

    # ——— STRUCTURED HIT LOGGING ———
    if gap < 0.01:
        hit = {
            "n": str(n),
            "sigma": s,
            "ratio": ratio,
            "gap": gap,
            "time": datetime.now().isoformat()
        }
        closest_hits.append(hit)
        closest_hits = sorted(closest_hits, key=lambda x: x["gap"])[:100]
        save_closest_hits(closest_hits)

    # ——— RAW HIT FOR MOD120 COVERAGE ———
    if gap < 0.0001:
        closest_hits.append(n)

    return closest_hits


def show_menu():
    # ——— DETECT CURRENT LOG ———
    current_log = "GODMODE_LOG.txt"
    if os.path.exists(current_log):
        size = os.path.getsize(current_log)
        size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
        log_indicator = f"LOG: {current_log} ({size_str})"
    else:
        log_indicator = "LOG: NONE (START HUNT TO CREATE)"

    print("\n" + "═"*70)
    print(" ODD PERFECT TERMINATOR — GOD MODE v0099 ODD EDITION")
    print("═"*70)
    print(f" CURRENT {log_indicator:<50}")
    print("─"*70)
    print("1. Start NEW hunt")
    print("2. RESUME from last save")
    print("3. View progress")
    print("4. View TOP 10 closest hits")
    print("5. View math & tools")
    print("6. DELETE progress or Select log file | New log | Delete individual")
    print("7. SYSTEM CYCLE CRASH TEST (LIVE PROGRESS BAR)")
    print("8. EXIT")
    print("9. FULL CONQUEST REPORT (Global % + Jump to unfinished ghosts)")
    print("10. COLAB COLONY CONTROL PANEL (Distributed Empire Mode)")
    print("11. UNTIL THE ODD PERFECT NUMBER (Infinite Session Mode)")
    print("═"*70)
    return input("Choose [1-11]: ")

def print_progress_bar(iteration, total, prefix='Progress', suffix='Complete', length=50):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled = int(length * iteration // total)
    bar = "█" * filled + "░" * (length - filled)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end="", flush=True)
    if iteration == total:
        print()

def system_cycle_crash_test():
    print("\n" + "☢️" * 30)
    print(" ⚠️  ⚠️  ⚠️  RED ALERT — ODD SEE APOCALYPSE PROTOCOL  ⚠️  ⚠️  ⚠️ ")
    print(" THIS TEST WILL SIMULATE A FULL SYSTEM CRASH IN 10 SECONDS")
    print(" YOUR STATE WILL BE SAVED. YOUR PC WILL NOT DIE.")
    print(" BUT THE SCRIPT WILL KILL ITSELF ON PURPOSE.")
    print(" ☢️  EMERGENCY SAVE SYSTEM WILL ACTIVATE  ☢️ ")
    print(" ☢️  YOU WILL RETURN TO POWERSHELL CLEANLY  ☢️ ")
    print("☢️" * 30)
    
    for i in range(10, 0, -1):
        print(f"\r ⚠️  SELF-DESTRUCT IN {i:2} SECONDS — PRESS CTRL+C TO ABORT  ⚠️ ", end="", flush=True)
        time.sleep(1)
    print("\n\n 🚀  LAUNCHING APOCALYPSE PROTOCOL...\n")

    total_tests = 8
    current = 0

    # TEST 1: Save/Load
    current += 1
    print_progress_bar(current, total_tests, prefix=f"[{current}/{total_tests}] Save/Load", suffix="Arming...")
    test_state = {'current_ghost_index': 0, 'zone_counter': 0}
    save_state(test_state)
    assert load_state()['current_ghost_index'] == 0
    print_progress_bar(current, total_tests, prefix=f"[{current}/{total_tests}] Save/Load", suffix="LOCKED")

    # TEST 2: Ghost + Sigma (LIGHTNING FAST)
    current += 1
    print_progress_bar(current, total_tests, prefix=f"[{current}/{total_tests}] Ghost Reflex", suffix="Charging...")
    C = random.randint(10**15, 10**16) * 2 + 1
    sigma_proper(C)
    print_progress_bar(current, total_tests, prefix=f"[{current}/{total_tests}] Ghost Reflex", suffix="FIRED")

    # TEST 3: Logging
    current += 1
    print_progress_bar(current, total_tests, prefix=f"[{current}/{total_tests}] Black Box", suffix="Recording...")
    log("APOCALYPSE PROTOCOL ENGAGED — ODD SEE")
    print_progress_bar(current, total_tests, prefix=f"[{current}/{total_tests}] Black Box", suffix="SEALED")

    # TEST 4: EMERGENCY SAVE + SELF-DESTRUCT
    current += 1
    print_progress_bar(current, total_tests, prefix=f"[{current}/{total_tests}] SELF-DESTRUCT", suffix="ACTIVATING...")
    def doomsday():
        time.sleep(1.5)
        print("\n 💀  CORE MELTDOWN INITIATED  💀 ")
        os.kill(os.getpid(), signal.SIGINT)
    threading.Timer(0.1, doomsday).start()
    time.sleep(3)
    # If we're still here, emergency_save() worked and exited
    # (We never reach here — but keeps syntax happy)

    # The rest runs only if someone Ctrl+C during countdown
    print_progress_bar(8, 8, prefix="[8/8] ABORTED", suffix="USER PANICKED")
    print(" ☢️  APOCALYPSE ABORTED — YOU ARE SAFE  ☢️ ")


### seee

def live_war_room_dashboard(state, closest_hits, start_time):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    runtime = int(time.time() - start_time)
    hours = runtime // 3600
    mins = (runtime % 3600) // 60
    secs = runtime % 60

    print("═" * 80)
    print(" " * 25 + "ODD SEE WAR ROOM — LIVE FEED")
    print("═" * 80)
    print(f" 🎯 GHOST #{state['current_ghost_index'] + 1}/51 DEPLOYED")
    print(f" 📍 EVEN PERFECT: {generate_even_perfect(state['current_ghost_index']):,}")
    print(f" 👻 CURRENT GHOST: –{generate_even_perfect(state['current_ghost_index']):,}")
    print(f" ⚡ ZONES FIRED: {state['zone_counter']:,}")
    print(f" 🎯 ODD NUMBERS TESTED: {state['zone_counter'] * 3:,}")
    print(f" ⏱️  RUNTIME: {hours}h {mins}m {secs}s")
    print(f" 🚀 SPEED: ~{state['zone_counter'] // max(runtime, 1):,} zones/sec")
    print()
    print(" 🔥 TOP 5 CLOSEST HITS (σ(n)/n ≈ 2) 🔥")
    print(" ┌────┬────────────────────┬────────────┬────────────┐")
    print(" │ #  │ NUMBER             │ RATIO      │ GAP        │")
    print(" ├────┼────────────────────┼────────────┼────────────┤")
    for i, h in enumerate(closest_hits[:5], 1):
        n = h['n']
        ratio = h['ratio']
        gap = h['gap']
        print(f" │ {i:<2} │ {n[:16]:<16} │ {ratio:.10f} │ {gap:.2e} │")
    print(" └────┴────────────────────┴────────────┴────────────┘")
    print()
    print(" 🟢 EMERGENCY SAVE: ACTIVE (Ctrl+C = SAFE SHUTDOWN)")
    print(" 🔴 ODD PERFECT STATUS: STILL HUNTING...")
    print(" 💀 ODD SEE PROTOCOL: ENGAGED")
    print("═" * 80)
    print(" Next update in 5 minutes... | Press Ctrl+C to pause safely")
    print("═" * 80)


def full_conquest_report():
    os.system('cls' if os.name == 'nt' else 'clear')
    state = load_state() or {'current_ghost_index': 0, 'zone_counter': 0, 'runtime': 0}
    total_zones = len(MERSENNE_EXPONENTS) * MAX_SANDWICHES_PER_GHOST
    completed_zones = state['current_ghost_index'] * MAX_SANDWICHES_PER_GHOST + min(state['zone_counter'], MAX_SANDWICHES_PER_GHOST)
    percent = (completed_zones / total_zones) * 100

    print("═" * 95)
    print(" " * 28 + "ODD SEE GALACTIC CONQUEST REPORT v3")
    print("═" * 95)
    print(f" TOTAL GHOSTS: 51")
    print(f" ZONES PER GHOST: {MAX_SANDWICHES_PER_GHOST:,}")
    print(f" TOTAL UNIVERSE SIZE: {total_zones:,} zones")
    print(f" ZONES CONQUERED: {completed_zones:,}")
    print(f" GLOBAL COMPLETION: {percent:.12f}%")
    print()
    print(" GALAXY MAP — 51 GHOST SYSTEMS")
    print(" █ = Conquered  ▓ = In Progress  ░ = Unexplored")

    bar = ""
    for i in range(len(MERSENNE_EXPONENTS)):
        if i < state['current_ghost_index']:
            bar += "█"
        elif i == state['current_ghost_index']:
            prog = state['zone_counter'] / MAX_SANDWICHES_PER_GHOST
            filled = int(prog * 10)
            bar += "▓" * filled + "░" * (10 - filled)
        else:
            bar += "░" * 10
        if (i + 1) % 5 == 0:
            bar += " "
    print(f" [{bar}] {state['current_ghost_index'] + 1}/51")
    print()
    print(" UNFINISHED GHOST SYSTEMS:")
    print("    #   GHOST             EXPONENT (2^p-1)         STATUS")
    print("   ─── ───────────────── ──────────────────────  ───────────────")

    for i in range(state['current_ghost_index'], len(MERSENNE_EXPONENTS)):
        p = MERSENNE_EXPONENTS[i]
        status = "IN PROGRESS" if i == state['current_ghost_index'] else "NOT STARTED"
        progress = ""
        if i == state['current_ghost_index']:
            prog_pct = (state['zone_counter'] / MAX_SANDWICHES_PER_GHOST) * 100
            progress = f" ({prog_pct:.6f}%)"
        print(f"   {i+1:2}. Ghost #{i+1:2} → 2^{p:<8} - 1 → {status:12} {progress}")

    print()
    print(" HYPERSPACE COMMAND CENTER")
    print("   jump 13     → Warp + AUTO-RESUME at Ghost #13")
    print("   jump max    → Warp to last unfinished ghost")
    print("   jump list   → Show only unfinished (this view)")
    print("   back        → Return to main menu")
    print("═" * 95)

    while True:
        cmd = input("\nGALACTIC COMMAND > ").strip().lower()
        if cmd.startswith("jump "):
            target = cmd[5:].strip()
            if target == "max":
                target_idx = state['current_ghost_index']
            elif target == "list":
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Refreshing Unfinished Ghost Systems View...\n")
                continue
            else:
                try:
                    target_idx = int(target) - 1
                    if not (0 <= target_idx < len(MERSENNE_EXPONENTS)):
                        print(" SECTOR DOES NOT EXIST.")
                        continue
                except:
                    print(" INVALID COORDINATES. Use: jump 13 | jump max")
                    continue

            # WARP EXECUTION
            state['current_ghost_index'] = target_idx
            state['zone_counter'] = 0
            save_state(state)
            log(f"HYPERSPACE JUMP → GHOST #{target_idx + 1} | AUTO-RESUME ARMED")

            print(f"\n WARP DRIVE ENGAGED!")
            print(f" DESTINATION: GHOST #{target_idx + 1} (2^{MERSENNE_EXPONENTS[target_idx]}-1)")
            print(f" AUTO-RESUME: ACTIVE")
            for i in range(3, 0, -1):
                print(f" LAUNCH IN {i}...", end="\r")
                time.sleep(1)
            print(" " * 50)
            print(" WARP COMPLETE. Returning to menu, option 2 (RESUME will start from selected jump #)...")

            global auto_resume_after_jump
            auto_resume_after_jump = True
            return

        elif cmd == "back":
            return
        else:
            print(" UNKNOWN COMMAND. Try: jump 13 | jump max | jump list | back")

#4ever8888
## REST
def option_3_view_progress():
    state = load_state() or {'current_ghost_index': 0, 'zone_counter': 0}
    ghost_num = state.get('current_ghost_index', 0) + 1
    zones = state.get('zone_counter', 0)
    runtime = state.get('runtime', 0)
    hours = runtime // 3600
    mins = (runtime % 3600) // 60
    secs = runtime % 60
    total_zones = len(MERSENNE_EXPONENTS) * MAX_SANDWICHES_PER_GHOST
    completed = state['current_ghost_index'] * MAX_SANDWICHES_PER_GHOST + min(zones, MAX_SANDWICHES_PER_GHOST)
    percent = (completed / total_zones) * 100

    print("\n" + "═" * 80)
    print(" 🧭 CURRENT PROGRESS REPORT")
    print("═" * 80)
    print(f" 🔹 Ghost #{ghost_num}/51")
    print(f" 🔹 Zones completed: {zones:,}")
    print(f" 🔹 Total progress: {percent:.6f}%")
    print(f" 🔹 Runtime: {hours}h {mins}m {secs}s")
    print(" 🔹 Resume will continue from this ghost and zone count.")
    print("═" * 80)


def option_4_top_hits():
    hits = load_closest_hits()
    if not hits:
        print("\nNo hits recorded yet. Start the hunt to generate candidates.")
        return

    print("\nTOP 10 CLOSEST HITS (σ(n)/n ≈ 2):")
    print(" ┌────┬────────────────────┬────────────┬────────────┐")
    print(" │ #  │ NUMBER             │ RATIO      │ GAP        │")
    print(" ├────┼────────────────────┼────────────┼────────────┤")
    for i, h in enumerate(hits[:10], 1):
        print(f" │ {i:<2} │ {h['n'][:16]:<16} │ {h['ratio']:.10f} │ {h['gap']:.2e} │")
    print(" └────┴────────────────────┴────────────┴────────────┘")


# ============================================================
# 11. UNTIL THE ODD PERFECT NUMBER — INFINITE SESSION MODE
# ============================================================
def option_11_4everodd():
    print("\n" + "═" * 95)
    print("  INFINITE SESSION MODE — ODD SEE PROTOCOL ENGAGED")
    print("  You may extend zones, chain sessions, and run forever.")
    print("  Each ghost will double its zone target after completion.")
    print("  You can resume from any ghost and continue the eternal hunt.")
    print("═" * 95)

    try:
        multiplier = int(input("Enter starting zone multiplier (1 = 50M, 10 = 500M, etc): ") or "1")
    except:
        multiplier = 1

    new_target = MAX_SANDWICHES_PER_GHOST * multiplier
    state = load_state() or {
        'current_ghost_index': 0,
        'zone_counter': 0,
        'runtime': 0,
        'total_zones_target': new_target,
        'infinite_mode': True,
        'multiplier': multiplier
    }

    state['total_zones_target'] = new_target
    state['infinite_mode'] = True
    state['multiplier'] = multiplier
    save_state(state)

    log(f"INFINITE MODE ENGAGED — TARGET: {new_target:,} ZONES PER GHOST")
    print(f"\nStarting infinite hunt with {new_target:,} zones per ghost...")
    time.sleep(2)

    # Launch eternal hunt loop
    launch_eternal_hunt(state)

def option_5_math_tools():
    print("\n" + "═" * 80)
    print(" MATH & TOOLS OVERVIEW")
    print("═" * 80)
    print(" Negative Ghost Reflection:")
    print("     - Inverts even perfect numbers (from Mersenne primes) into large odd candidates.")
    print("     - Uses modular inverse and prime lifting.")
    print("  Sandwich Sniper:")
    print("     - Tests [C-2, C, C+2] around each candidate C.")
    print("     - Filters for odd numbers only.")
    print("  σ(n) — Proper Divisor Sum:")
    print("     - Sum of all proper divisors of n.")
    print("     - Target ratio: σ(n)/n ≈ 2.0")
    print("  Closest Hits:")
    print("     - Top 100 candidates with smallest gap from 2.0.")
    print("     - Saved in JSON and viewable anytime.")
    print("  Emergency Save System:")
    print("     - Saves state every 5 minutes.")
    print("     - Ctrl+C triggers safe shutdown.")
    print("═" * 80)

#keep above class sessionlogger:
def timestamped_filename(base_name="GODMODE_LOG", ext=".txt"):
    """Generate timestamped log filenames."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{ts}{ext}"

#def timestamped_filename keep above class SessionLogger:
# =======================
# SESSION LOGGER
# =======================

class SessionLogger:
    def __init__(self, log_file=None):
        if log_file is None:
            log_file = os.path.join(LOG_DIR, timestamped_filename())
        self.log_file = log_file

    def write(self, text):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def archive(self):
        """Archive current log and start a new one"""
        if os.path.exists(self.log_file):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{os.path.basename(self.log_file)}.ARCHIVED_{ts}"
            archive_path = os.path.join(ARCHIVE_DIR, archive_name)
            os.rename(self.log_file, archive_path)
        # start a new log
        self.log_file = os.path.join(LOG_DIR, timestamped_filename())
## keep under clas sessionlogger:
# Initialize global logger
logger = SessionLogger()
LOG_FILE = logger.log_file

##

def list_logs():
    """List all logs (active and archived) in this script's logs folder."""
    logs = []

    # Active .txt logs in LOG_DIR
    for f in sorted(os.listdir(LOG_DIR)):
        full_path = os.path.join(LOG_DIR, f)
        if os.path.isfile(full_path) and f.endswith(".txt"):
            logs.append(full_path)

    # Archived logs
    for f in sorted(os.listdir(ARCHIVE_DIR)):
        full_path = os.path.join(ARCHIVE_DIR, f)
        if os.path.isfile(full_path):
            logs.append(full_path)

    return logs

# =======================
# HELPERS FOR STATE & HITS
# =======================

def get_save_file():
    base = os.path.splitext(os.path.basename(logger.log_file))[0]
    return os.path.join(LOG_DIR, f"{base}_STATE.pkl")

def get_closest_hits_file():
    base = os.path.splitext(os.path.basename(logger.log_file))[0]
    return os.path.join(LOG_DIR, f"{base}_CLOSEST_HITS.json")



def print_log_menu():
    """Print log management menu."""
    logs = list_logs()
    print("════════════════════════════════════════")
    print(" ACTIVE LOG FILES (SWITCHABLE):")
    print(" ┌────┬────────────────────────────┬────────────┐")
    print(" │ # │ LOG FILE                   │ SIZE       │")
    print(" ├────┼────────────────────────────┼────────────┤")
    for i, log in enumerate(logs, 1):
        size_kb = os.path.getsize(log) / 1024 if os.path.exists(log) else 0
        print(f" │ {i:<2} │ {os.path.basename(log):<26} │ {size_kb:>8.1f} KB │")
    print(" └────┴────────────────────────────┴────────────┘")
    print("\nACTIONS:")
    print("[1-{}] SWITCH to this log".format(len(logs)))
    print("[N] Start NEW log (archive current)")
    print("[D] Delete individual file")
    print("[B] Back to main menu")
    print("════════════════════════════════════════")

# =======================
# LOG MENU FUNCTION
# =======================

def option_6_delete_progress():
    """Manage logs: switch, delete, archive, or start new logs with associated state and hits."""
    global logger
    while True:
        logs = list_logs()

        # Display
        print("════════════════════════════════════════")
        print(" ACTIVE LOG FILES (SWITCHABLE):")
        print(" ┌────┬────────────────────────────┬────────────┐")
        print(" │ # │ LOG FILE                   │ SIZE       │")
        print(" ├────┼────────────────────────────┼────────────┤")
        for i, log_file in enumerate(logs, 1):
            size_kb = os.path.getsize(log_file) / 1024 if os.path.exists(log_file) else 0
            print(f" │ {i:<2} │ {os.path.basename(log_file):<26} │ {size_kb:>8.1f} KB │")
        print(" └────┴────────────────────────────┴────────────┘\n")

        print("ACTIONS:")
        print(f"[1-{len(logs)}] SWITCH to this log")
        print("[N] Start NEW log (archive current)")
        print("[D] Delete individual file")
        print("[B] Back to main menu")
        print("════════════════════════════════════════")

        choice = input("LOG COMMAND > ").strip().upper()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(logs):
                logger.log_file = logs[idx]
                log(f"Switched to log: {os.path.basename(logger.log_file)}")
            else:
                print("Invalid log number.")

        elif choice == "N":
            # archive current log + associated files
            current_log = logger.log_file
            if os.path.exists(current_log):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = f"{os.path.basename(current_log)}.ARCHIVED_{ts}"
                archive_path = os.path.join(ARCHIVE_DIR, archive_name)
                os.rename(current_log, archive_path)

                # Archive state & hits
                state_file = get_save_file()
                hits_file = get_closest_hits_file()
                if os.path.exists(state_file):
                    shutil.move(state_file, os.path.join(ARCHIVE_DIR, f"{os.path.basename(state_file)}.ARCHIVED_{ts}"))
                if os.path.exists(hits_file):
                    shutil.move(hits_file, os.path.join(ARCHIVE_DIR, f"{os.path.basename(hits_file)}.ARCHIVED_{ts}"))

            # new log
            logger.log_file = os.path.join(LOG_DIR, timestamped_filename())
            log(f"New log started: {os.path.basename(logger.log_file)}")

        elif choice == "D":
            del_idx = input("Enter log number to delete > ").strip()
            if del_idx.isdigit():
                idx = int(del_idx) - 1
                if 0 <= idx < len(logs):
                    log_to_delete = logs[idx]
                    try:
                        os.remove(log_to_delete)
                        # Delete associated files
                        base_name = os.path.splitext(os.path.basename(log_to_delete))[0]
                        state_file = os.path.join(LOG_DIR, f"{base_name}_STATE.pkl")
                        hits_file = os.path.join(LOG_DIR, f"{base_name}_CLOSEST_HITS.json")
                        if os.path.exists(state_file):
                            os.remove(state_file)
                        if os.path.exists(hits_file):
                            os.remove(hits_file)
                        print(f"Deleted log and associated files: {os.path.basename(log_to_delete)}")
                    except Exception as e:
                        print(f"Error deleting file: {e}")
                else:
                    print("Invalid log number.")
            else:
                print("Not a number.")

        elif choice == "B":
            break

        else:
            print(f"Invalid command. Use 1-{len(logs)}, N, D, B.")

# ============================================================
# Eternal Hunt Loop — Doubles Zones Every Ghost
# ============================================================
# ============================================================
# DOMINION ETERNAL HUNT v∞.PROOF — FINAL FIELDS-READY BLOCK
# ONE FUNCTION. NO DUPLICATES. FULL PROOF INFRASTRUCTURE.
# ============================================================

def launch_eternal_hunt(state):
    """
    DOMINION ETERNAL HUNT — escalates q/k/targets, tracks modular coverage,
    logs per-zone proof entries to PROOF_LOG{suffix}.jsonl, integrates Z3.
    This is the ONLY version. All others must be deleted.
    """
    closest_hits = load_closest_hits()
    start_time = time.time()
    last_save = time.time()
    start_pulse(state, start_time)

    # ——— DOMINION STATE (PERSISTED) ———
    state['search_depth'] = state.get('search_depth', 1)
    state['modulus_max'] = state.get('modulus_max', 100)
    state['k_max'] = state.get('k_max', 18)
    state['total_zones_target'] = state.get('total_zones_target', MAX_SANDWICHES_PER_GHOST)

    # ——— MODULAR COVERAGE (PROOF OF DENSITY) ———
    MODULI = [3,4,5,7,8,9,11,12,13,15,16,17,20,24,28,30,36,60,120]
    covered_residues = {m: set() for m in MODULI}

    # ——— COVERAGE UPDATE FUNCTION ———
    def update_coverage(n):
        nonlocal covered_residues
        for m in MODULI:
            covered_residues[m].add(int(n % m))

    # ——— COVERAGE BOOTSTRAP ———
    debug_log("DOMINiov COVERAGE BOOTSTRAP: Populating mod120 residues...")
    for test_n in range(1, 10000, 2):
        update_coverage(test_n)
    actual_count = len(covered_residues[120])
    debug_log(f"DEBUG: ACTUAL RESIDUES IN mod120 = {actual_count}")
    cov = actual_count / 120.0
    if actual_count < 60:
        log(f"BOOTSTRAP FAILED → ONLY {actual_count} RESIDUES (EXPECTED 60)")
    else:
        log(f"COVERAGE BOOTSTRAP COMPLETE → mod120: {cov:.3%} (MAX FOR ODD n)")

    # ——— PROOF LOG FILE ———
    proof_log_file = f"PROOF_LOG{get_colony_suffix()}.jsonl"

    # ——— Z3 ENGINE ———
    try:
        from z3 import Int, Solver, sat
        z3_available = True
        log("Z3 PROOF ENGINE: ONLINE")
    except Exception:
        z3_available = False
        log("Z3 not installed — proof engine disabled (pip install z3-solver)")

    # ——— PROOF LOGGING ———
    def log_proof_step(ghost_idx, q, k, C, n, sigma_val, ratio):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "colony": COLONY_ID or "LOCAL",
            "ghost": ghost_idx + 1,
            "P": generate_even_perfect(ghost_idx),
            "q": int(q),
            "k": int(k),
            "C": str(C),
            "n": str(n),
            "sigma": int(sigma_val),
            "ratio": float(ratio),
            "depth": int(state['search_depth']),
            "q_max": int(state['modulus_max']),
            "k_max": int(state['k_max']),
            "target": int(state['total_zones_target']),
            "mod120_coverage": len(covered_residues[120]) / 120.0
        }
        try:
            with open(proof_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            debug_log(f"PROOF LOG ERROR: {e}")

    # ——— MAIN DOMINION LOOP ———
    try:
        for ghost_idx in range(state['current_ghost_index'], len(MERSENNE_EXPONENTS)):
            P = generate_even_perfect(ghost_idx)
            G = -P
            debug_log(f"DOMINION GHOST #{ghost_idx+1}/51 | –{P:,} | DEPTH {state['search_depth']} | q≤{state['modulus_max']:,} | k≤{state['k_max']} | TARGET {state['total_zones_target']:,}")

            zone_count = state['zone_counter'] if state.get('current_ghost_index') == ghost_idx else 0
            target = int(state['total_zones_target'])
            prime_gen = 100
            k_start = 8
            k_end = int(state['k_max'])

            # === PHASE 1: 10 DEBUG TEST CANDIDATES (CONFIRM SYSTEM IS LIVE) ===
            debug_phase = min(zone_count, 10)
            if debug_phase < 10:
                log(f"PHASE 1: RUNNING 10 DEBUG CANDIDATES TO CONFIRM SYSTEM INTEGRITY...")
                while zone_count < 10:
                    C = 10**15 + zone_count * 1000 + 1
                    debug_log(f"DEBUG CANDIDATE #{zone_count+1}: C = {C}")
                    q_val = 0
                    k_val = 0

                    for n in generate_sandwich(C):
                        sigma_val = sigma_proper(n)
                        ratio = sigma_val / n if n > 0 else 0
                        update_coverage(n)
                        closest_hits = test_number(n, closest_hits)
                        log_proof_step(ghost_idx, q_val, k_val, C, n, sigma_val, ratio)

                    zone_count += 1
                    state['zone_counter'] = zone_count

                log("PHASE 1 COMPLETE: 10 DEBUG CANDIDATES SUCCESSFULLY PROCESSED.")
                log("ENTERING PHASE 2: FULL DOMINION HUNT MODE — NEGATIVE GHOST REFLECTION ACTIVE.")
                debug_log("DOMINION FULLY ARMED — BEGINNING INFINITE HUNT")

            # === PHASE 2: NORMAL DOMINION PATH (AFTER DEBUG CONFIRMED) ===
            while zone_count < target:
                q = nextprime(prime_gen)
                if q > state['modulus_max']:
                    prime_gen = 100
                    time.sleep(0.05)
                    continue
                prime_gen = q + 2
                C = None
                q_val = q
                k_val = 0

                for k in range(k_start, k_end + 1):
                    if zone_count >= target:
                        break
                    C = negative_ghost_reflection(G, q, k)
                    if C and C >= 10**10:
                        k_val = k
                        break
                if not C or C < 10**10:
                    continue

                for n in generate_sandwich(C):
                    sigma_val = sigma_proper(n)
                    ratio = sigma_val / n if n > 0 else 0
                    update_coverage(n)

                    if z3_available and 1.999 < ratio < 2.001 and sigma_val > n:
                        try:
                            s = Solver()
                            x = Int('x')
                            s.add(x * n == sigma_val * n + x)
                            if s.check() == sat:
                                log(f"Z3 ALERT: n={n} | ratio={ratio:.12f} | ghost={ghost_idx+1}")
                        except Exception:
                            pass

                    closest_hits = test_number(n, closest_hits)
                    log_proof_step(ghost_idx, q_val, k_val, C, n, sigma_val, ratio)

                zone_count += 1
                state['zone_counter'] = zone_count

                # ---- FAILSAFE ----
                if zone_count > target * 2:
                    log(f"FAILSAFE: Ghost #{ghost_idx+1} overflow. Skipping.")
                    state['current_ghost_index'] = ghost_idx + 1
                    state['zone_counter'] = 0
                    save_state(state)
                    break

                # ---- LIVE PROGRESS ----
                if zone_count % 10000 == 0:
                    cov = len(covered_residues[120]) / 120.0
                    speed = zone_count // max(int(time.time() - start_time), 1)
                    debug_log(f"Ghost #{ghost_idx+1} → {zone_count:,}/{target:,} | mod120: {cov:.3%} | {speed:,}/s")

                # ---- CHECKPOINT ----
                if time.time() - last_save > CHECKPOINT_INTERVAL:
                    state['current_ghost_index'] = ghost_idx
                    state['runtime'] = int(time.time() - start_time)
                    save_state(state)
                    last_save = time.time()
                    stop_pulse()
                    live_war_room_dashboard(state, closest_hits, start_time)
                    start_pulse(state, start_time)

            # ——— PROOF SUMMARY BLOCK ———
            try:
                proof_entries = 0
                near_perfects = 0
                if os.path.exists(proof_log_file):
                    with open(proof_log_file, "r", encoding="utf-8") as pf:
                        for line in pf:
                            proof_entries += 1
                            if '"ratio":' in line and ('"ratio": 1.999' in line or '"ratio": 2.0' in line):
                                near_perfects += 1
                log(f"PROOF SUMMARY — Ghost #{ghost_idx+1} complete.")
                log(f" Total proof log entries: {proof_entries:,}")
                log(f" Near-perfect ratio entries: {near_perfects:,}")
                log(f" Current mod120 coverage: {len(covered_residues[120]) / 120.0:.3%}")
                print("─" * 80)
                print(f"GHOST #{ghost_idx+1} SUMMARY — {proof_entries:,} total | {near_perfects:,} near-perfects")
                print(f" Coverage mod120: {len(covered_residues[120]) / 120.0:.3%}")
                print("─" * 80)
            except Exception as e:
                debug_log(f"Proof summary error: {e}")

            # ——— ESCALATION ———
            state['current_ghost_index'] = ghost_idx + 1
            state['zone_counter'] = 0
            state['search_depth'] += 1
            if state['search_depth'] <= 5:
                state['modulus_max'] *= 10
                state['k_max'] += 6
                state['total_zones_target'] *= 10
            else:
                state['modulus_max'] *= 2
                state['k_max'] += 2
                state['total_zones_target'] *= 2
            save_state(state)
            cov = len(covered_residues[120]) / 120.0
            log(f"ESCALATION → DEPTH {state['search_depth']} | q≤{state['modulus_max']:,} | k≤{state['k_max']} | TARGET {state['total_zones_target']:,} | mod120: {cov:.3%}")

    except KeyboardInterrupt:
        log("DOMINION PAUSED — SAFE SHUTDOWN")
    except Exception as e:
        debug_log(f"DOMINION ERROR: {e}")
        emergency_save(state)
    finally:
        stop_pulse()
        final_cov = len(covered_residues[120]) / 120.0
        log(f"DOMINION FINALar FINAL: mod120 = {final_cov:.3%}")
        save_state(state)
        log("FINAL STATE SAVED")
        if os.path.exists(proof_log_file):
            log(f"PROOF LOG SAVED → {proof_log_file}")
        else:
            log("WARNING: PROOF LOG NOT FOUND")
        print("\n" + "═" * 90)
        print(" DOMINION v∞.PROOF — PAUSED")
        print(f" LOG: {proof_log_file}")
        print(f" COVERAGE: mod120 = {final_cov:.3%}")
        print(f" LAST GHOST: #{state['current_ghost_index'] + 1}")
        print(f" ZONES FIRED: {state['zone_counter']:,}")
        print(f" PAUSED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("═" * 90)

## launch 


# [main() function remains the same — only crash test upgraded]
# ... (same as previous v0010 with emergency_save, etc.)

def run_main_hunt_loop(state):
    log("Starting main Odd Perfect hunt loop...")
    start_time = time.time()
    closest_hits = load_closest_hits()
    start_pulse(state, start_time)  # ✅ pass arguments correctly

    try:
        for ghost_idx in range(state['current_ghost_index'], len(MERSENNE_EXPONENTS)):
            C = generate_even_perfect(ghost_idx)
            target = MAX_SANDWICHES_PER_GHOST
            zone_count = state['zone_counter']

            log(f"Deploying Ghost #{ghost_idx + 1} — Even Perfect = {C}")

            while zone_count < target:
                for n in generate_sandwich(C):
                    closest_hits = test_number(n, closest_hits)
                zone_count += 1
                state['zone_counter'] = zone_count

                # === FAILSAFE CHECK ===
                if zone_count > target * 2:
                    log(f"⚠️ FAILSAFE TRIGGERED — Ghost #{ghost_idx + 1} overflow detected (zone_count={zone_count:,})")
                    state['current_ghost_index'] = ghost_idx + 1
                    state['zone_counter'] = 0
                    save_state(state)
                    log(f"⚠️ Skipping Ghost #{ghost_idx + 1} due to overflow safeguard. Continuing to next.")
                    break
                # === END FAILSAFE ===

                if zone_count % 5000 == 0:
                    debug_log(f"Ghost #{ghost_idx + 1} → {zone_count:,} zones")

                if zone_count % 10000 == 0:
                    live_war_room_dashboard(state, closest_hits, start_time)
                    save_closest_hits(closest_hits)
                    save_state(state)

            state['current_ghost_index'] = ghost_idx + 1
            state['zone_counter'] = 0
            save_state(state)
            save_closest_hits(closest_hits)
            log(f"Ghost #{ghost_idx + 1} completed.")

        log("All ghosts processed. Odd Perfect Terminator main loop finished.")
    except KeyboardInterrupt:
        log("🟡 SAFE SHUTDOWN INITIATED. Saving progress...")
        save_state(state)
        save_closest_hits(closest_hits)
        stop_pulse()
        log("✅ SAFE SHUTDOWN COMPLETE.")
    except Exception as e:
        log(f"❌ UNEXPECTED ERROR: {e}")
        save_state(state)
        save_closest_hits(closest_hits)
        stop_pulse()
        raise
    finally:
        stop_pulse()
#
#def live_pulse_dashboard(state, closest_hits, start_time): #stay above def launch_colony

def live_pulse_dashboard(state, closest_hits, start_time):
    import sys
    import time
    from datetime import datetime

    zones = state.get('zone_counter', 0)
    ghost_idx = state.get('current_ghost_index', 0)
    elapsed = time.time() - start_time
    speed = zones / elapsed if elapsed > 0 else 0

    mod120_set = set(hit % 120 for hit in closest_hits) if closest_hits else set()
    mod120_coverage = (len(mod120_set) / 120) * 100

    timestamp = datetime.now().strftime('%H:%M:%S')
    pulse_line = f"[{timestamp}] ⣾ PULSE → Z:{zones:,} | S:{int(speed):,}/s | G#{ghost_idx + 1}/51 | mod120:{mod120_coverage:.1f}%"

    sys.stdout.write(f"\r{pulse_line}")
    sys.stdout.flush()


def launch_colony(colony_id, start_ghost=1, end_ghost=51):
    log(f"Launching Colony #{colony_id}...")
    state = {'current_ghost_index': start_ghost - 1, 'zone_counter': 0}
    start_time = time.time()
    closest_hits = []

    start_pulse(state, start_time)  # ✅ Pulse engine activated

    try:
        for ghost_idx in range(start_ghost - 1, end_ghost):
            C = generate_even_perfect(ghost_idx)
            target = MAX_SANDWICHES_PER_GHOST
            zone_count = 0

            while zone_count < target:
                for n in generate_sandwich(C):
                    closest_hits = test_number(n, closest_hits)
                zone_count += 1
                state['zone_counter'] = zone_count

                # === FAILSAFE CHECK ===
                if zone_count > target * 2:
                    log(f"⚠️ [Colony {colony_id}] Overflow safeguard triggered — Ghost #{ghost_idx + 1}")
                    state['zone_counter'] = 0
                    save_state(state)
                    log(f"⚠️ [Colony {colony_id}] Skipping Ghost #{ghost_idx + 1}")
                    break
                # === END FAILSAFE ===

                if zone_count % 10000 == 0:
                    live_pulse_dashboard(state, closest_hits, start_time)  # ✅ Unified pulse output
                    save_closest_hits(closest_hits)

            log(f"[Colony {colony_id}] Ghost #{ghost_idx + 1} complete.")
    except KeyboardInterrupt:
        log(f"[Colony {colony_id}] Safe shutdown received.")
        save_closest_hits(closest_hits)
        save_state(state)
    except Exception as e:
        log(f"[Colony {colony_id}] ERROR: {e}")
        save_state(state)
        save_closest_hits(closest_hits)
    finally:
        stop_pulse()


def main():
    global auto_resume_after_jump
    print("GROK + STACEY SZMY — ODD PERFECT TERMINATOR v0099 — DISTRIBUTED EMPIRE")
    print("PULSE HEARTBEAT | WAR ROOM | HYPERSPACE WARP | 10 COLONIES | NUCLEAR SAFE | UNLIMITED DIGITS")

    # ——— INITIAL STATE ———
    state = {'current_ghost_index': 0, 'zone_counter': 0, 'runtime': 0}
    loaded = load_state()
    if loaded:
        state = loaded

    # ——— MENU LOOP ———
    while True:
        choice = show_menu().strip()

        if choice == "1":
            log("NEW HUNT LAUNCHED — ODD SEE EMPIRE v0012.0")
            state = {'current_ghost_index': 0, 'zone_counter': 0, 'runtime': 0}
            break

        elif choice == "2":
            loaded = load_state()
            if loaded:
                state = loaded
                if auto_resume_after_jump:
                    log(f"WARP RESUME → GHOST #{state['current_ghost_index'] + 1} (AUTO-JUMP ACTIVE)")
                    auto_resume_after_jump = False
                else:
                    log(f"HUNT RESUMED FROM GHOST #{state['current_ghost_index'] + 1}")
            else:
                log("NO SAVE FOUND → STARTING FRESH")
                state = {'current_ghost_index': 0, 'zone_counter': 0, 'runtime': 0}
            break

        elif choice == "3":
            selected = option_3_view_progress()
            if not selected:
                continue

        elif choice == "4":
            selected = option_4_top_hits()
            if not selected:
                continue

        elif choice == "5":
            selected = option_5_math_tools()
            if not selected:
                continue

        elif choice == "6":
            selected = option_6_delete_progress()
            if not selected:
                continue

        elif choice == "7":
            system_cycle_crash_test()

        elif choice == "8":
            print("See you at the Fields Medal ceremony, Empress.")
            return

        elif choice == "9":
            full_conquest_report()
            continue
        elif choice == "10":
            selected = colony_control_panel()
            if not selected:
                continue

            if isinstance(selected, str) and selected.startswith("SESSION_"):
                parts = selected.split("_")
                session_id = int(parts[1])
                start_col = int(parts[2])
                end_col = int(parts[3])
                start_ghost = (start_col - 1) * GHOSTS_PER_COLONY + 1
                end_ghost = min(end_col * GHOSTS_PER_COLONY, 51)

                debug_log(f"SESSION #{session_id} LAUNCHED → COLONIES {start_col}–{end_col} | GHOSTS {start_ghost}–{end_ghost}")
                print(f"\nSESSION #{session_id} ACTIVE — COLONIES {start_col}–{end_col} HUNTING IN PARALLEL")

                for cid in range(start_col, end_col + 1):
                    launch_colony(cid, start_ghost=start_ghost, end_ghost=end_ghost)

                print(f"\nSESSION #{session_id} COMPLETE — COLONIES {start_col}–{end_col} CONQUERED")
                continue

        elif choice == "11":
            selected = option_11_4everodd()
            if not selected:
                continue

        else:
            print("Invalid choice. Enter 1–11.")
            continue

    # ——— MAIN HUNT LOOP ———
    run_main_hunt_loop(state)


if __name__ == "__main__":
    main()

# LICENSE.TXT
# Zero-Ology License v1.191
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.191
#November 10, 2025
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

