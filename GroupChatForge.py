# GroupChatForge.py
# Title: 0KO GroupChatForge V0026 — Ping-Pong Multi-User AI Chat Bot with Ollama
# Ceo0: Szmy, Stacey.
# dev: HAHA.8888
# dev: HAHA.Xai.Grok
# Zer00logy License v1.10

import sys
import platform
import json
import shutil
import textwrap
import re
import os
from wcwidth import wcswidth
from datetime import datetime, timedelta
import logging
import time
import uuid
import traceback
import subprocess
import threading
import itertools

# 🔹 Config and Constants
config_path = os.path.join(os.path.dirname(__file__), "emoji_shift.cfg")
PROMPT_DIR = "prompt_logs"
prompt_locked = False
input_during_lock = []
last_unlock_time = 0
EMOJI_SHIFT = 0  # Module-level initialization
TOP_LEFT = "╔"
TOP_RIGHT = "╗"
BOTTOM_LEFT = "╚"
BOTTOM_RIGHT = "╝"
HORIZONTAL = "═"
VERTICAL = "║"
SHELL_WIDTH = 100
WRAP_WIDTH = 100
EMOJI_PATTERN = re.compile("[\U0001F300-\U0001FAFF]")
MODEL_CONFIG = {
    "mistral": {"model": "mistral", "tag": "🤖🧻💬: Mistral AI Response 🔻"},
    "llama2": {"model": "llama2", "tag": "🤖🧻💬: Llama2 AI Response 🔻"},
    "phi": {"model": "phi3", "tag": "🤖🧻💬: PHI AI Response 🔻"}
}
stop_indicator_flag = threading.Event()

# 🔹 Setup Logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"groupchatforge_error_{timestamp}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('GroupChatForge')
logger.info(f"Initialized new log file: {log_file}")

# 🔹 Ollama Service Check
def check_ollama_service():
    try:
        result = subprocess.run(
            "ollama ps",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            shell_print("🤖🧻✅: Ollama service is running.", label="Ollama Status")
            return True
        else:
            shell_print(
                "🤖🧻⚠️: Ollama service is not running.",
                "   ↳ Run 'ollama serve' in another terminal.",
                f"   ↳ Error: {result.stderr.strip()}",
                label="Ollama Status"
            )
            return False
    except Exception as e:
        handle_symbolic_error(e, context="check_ollama_service")
        return False

# 🔹 Shell and Display Functions
def log_print(*lines, label=None, prefix="🤖🧻💬:", color="\033[94m"):
    reset = "\033[0m"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = "\n".join(lines)
    if label:
        content = f"🤖🧻:🔻 {label} 🔻\n\n" + content
    boxed = wrap_in_shell(content)
    shell_print(f"{color}[{timestamp}]{prefix} {reset}")
    print(boxed)

def wrap_in_shell(content, width=SHELL_WIDTH):
    wrapped_lines = []
    for paragraph in content.split('\n'):
        lines = textwrap.wrap(paragraph, width=width)
        wrapped_lines.extend(lines if lines else [''])
    box = []
    horizontal_edge = HORIZONTAL * (width + 2)
    box.append(f"{TOP_LEFT}{horizontal_edge}{TOP_RIGHT}")
    for line in wrapped_lines:
        padded_line = emoji_aware_pad(line, width)
        box.append(f"{VERTICAL} {padded_line} {VERTICAL}")
    box.append(f"{BOTTOM_LEFT}{horizontal_edge}{BOTTOM_RIGHT}")
    return "\n".join(box)

def fix_symbolic_box_alignment(lines, emoji_shift=1):
    fixed_lines = []
    left_positions = []
    right_positions = []
    for line in lines:
        if "║" in line:
            left = line.find("║")
            right = line.rfind("║")
            if left != -1 and right != -1 and left != right:
                left_positions.append(left)
                right_positions.append(right)
    if left_positions and right_positions:
        left_target = max(set(left_positions), key=left_positions.count)
        right_target = max(set(right_positions), key=right_positions.count)
    else:
        return lines
    for line in lines:
        if "║" in line:
            left = line.find("║")
            right = line.rfind("║")
            content = line[left + 1:right].strip()
            padded = emoji_aware_pad(content, right_target - left_target - 1, emoji_shift)
            new_line = (
                line[:left_target] + "║" +
                " " + padded + " " +
                "║" + line[right_target + 1:]
            )
            fixed_lines.append(new_line)
        else:
            fixed_lines.append(line)
    return fixed_lines

def shell_print(*lines, label=None):
    if any("║" in line for line in lines):
        lines = fix_symbolic_box_alignment(lines)
        for line in lines:
            print(line)
        return
    content = "\n".join(lines)
    if label:
        content = f"🔻 {label} 🔻\n\n" + content
    print(wrap_in_shell(content))

def shell_input(prompt, label=None):
    shell_print(prompt, label=label)
    return input("♾️ Consol: ")

def handle_symbolic_error(e, context="Unknown"):
    error_msg = [
        "🤖🧻⚠️💬: ⚠️ SYSTEM ERROR DETECTED",
        f"🔻 Context: {context}",
        f"🔻 Exception: {str(e)}",
        f"🔻 Stack Trace: {traceback.format_exc()}",
        "",
        "🤖🧻💬: GroupChatForge : Recovery Protocol Activated",
        "   ↳ Resetting symbolic prompt...",
        "   ↳ Echo integrity preserved.",
        "   ↳ You may re-enter your command."
    ]
    logger.error(f"Error in {context}: {str(e)}\n{traceback.format_exc()}")
    shell_print(*error_msg, label="GroupChatForge 🤖🧻💬 : — Symbolic Error Handler")
    print(f"Error logged to: {log_file}")

# 🔹 Emoji Calibration
def calibrate_emoji_width():
    shell_print(
        "🤖🧻👋💬: Welcome to GroupChatForge! Before we start, let's calibrate your terminal's emoji rendering.",
        "🤖🧻🧻💬: This ensures all symbolic outputs align perfectly.",
        "",
        "🤖🧻💬: You'll see a boxed frame below.",
        "If the emoji line looks wider than the empty ones, enter how many spaces it appears shifted.",
        "We'll keep testing until the borders align visually.",
        label="Calibration Instructions"
    )
    while True:
        try:
            shift_input = input("🤖🧻💬: 🔧: Enter estimated emoji width (1, 2, or 3): ").strip()
            shift = int(shift_input)
            if shift not in [1, 2, 3]:
                raise ValueError("Invalid emoji width")
            shell_print(
                "🧪🤖🧻💬: Re-rendering with your selected emoji width...",
                "Check if the borders now align visually.",
                label="Calibration Preview"
            )
            frame_width = 60 + shift
            top_border = "╔" + "═" * frame_width + "╗"
            bottom_border = "╚" + "═" * frame_width + "╝"
            empty_line = "║" + " " * frame_width + "║"
            emoji_line = (
                "║" + " " * ((frame_width // 2) - 1) + "👋" + " " * ((frame_width // 2) - 1) + "║"
            )
            print("\n" + top_border)
            for i in range(6):
                print(emoji_line if i == 3 else empty_line)
            print(bottom_border + "\n")
            confirm = input("🤖✅🧻💬: Does this look aligned? (y/n): ").strip().lower()
            if confirm == "y":
                log_print(
                    "🤖🧻💬: ✅: Calibration complete. Emoji width set to " + str(shift),
                    label="Calibration Success"
                )
                return shift
            else:
                log_print(
                    "🤖🧻🧻💬: Let's try again. Adjust the emoji width and re-test.",
                    label="Calibration Retry"
                )
        except Exception as e:
            handle_symbolic_error(e, context="Emoji Calibration")

def save_shift(shift, save_dir="config_logs"):
    try:
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"emoji_shift_{timestamp}.cfg"
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(shift))
        shell_print(
            emoji_aware_pad("✅🤖🧻💬:🔧 Emoji Shift Saved 🔧", 60),
            emoji_aware_pad(f"📄 Saved to: `{filename}`", 60),
            label="Emoji Calibration"
        )
        return filepath
    except Exception as e:
        handle_symbolic_error(e, context="save_shift")

def load_shift(config_path="config_logs"):
    global EMOJI_SHIFT
    try:
        if os.path.isfile(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                shift = int(f.read().strip())
                shell_print(f"🧻✅🤖💬: Loaded emoji shift from `{os.path.basename(config_path)}`: {shift}", label="Emoji Calibration")
                EMOJI_SHIFT = shift
                return shift
        elif os.path.isdir(config_path):
            files = [f for f in os.listdir(config_path) if f.startswith("emoji_shift_") and f.endswith(".cfg")]
            if not files:
                raise FileNotFoundError("No emoji shift config files found.")
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(config_path, f)))
            filepath = os.path.join(config_path, latest_file)
            with open(filepath, "r", encoding="utf-8") as f:
                shift = int(f.read().strip())
                shell_print(f"🧻✅🤖💬: Loaded emoji shift from latest file `{latest_file}`: {shift}", label="Emoji Calibration")
                EMOJI_SHIFT = shift
                return shift
        else:
            raise FileNotFoundError(f"Invalid path: {config_path}")
    except Exception as e:
        handle_symbolic_error(e, context="load_shift → fallback")
        shell_print("🧻⚠️🤖💬: No valid config found. Running calibration...", label="Emoji Calibration")
        shift = calibrate_emoji_width()
        save_shift(shift, "config_logs")
        EMOJI_SHIFT = shift
        return shift

def manual_visual_width(line, emoji_shift):
    emoji_count = len(EMOJI_PATTERN.findall(line))
    non_emoji_chars = EMOJI_PATTERN.sub("", line)
    return len(non_emoji_chars) + (emoji_count * emoji_shift)

def emoji_aware_pad(line, target_width=60, emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = EMOJI_SHIFT
    visual_width = manual_visual_width(line, emoji_shift)
    padding = max(0, target_width - visual_width)
    return line + " " * padding

# 🔹 Thinking Indicator
def symbolic_thinking_indicator(model_name):
    global stop_indicator_flag
    BRICKS = ['🧻', '🧱', '⬜', '⬛']
    animation_frames = itertools.cycle(BRICKS)
    width = SHELL_WIDTH
    print("\n")
    while not stop_indicator_flag.is_set():
        frame = next(animation_frames)
        line_content = f"🤖🧻💬: {model_name.upper()} {frame} Symbolic Computation in Progress..."
        padded_content = emoji_aware_pad(line_content, width - 4, EMOJI_SHIFT)
        sys.stdout.write(f"\r{VERTICAL} {padded_content}{frame} {VERTICAL}")
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write(f"\r{' ' * (width + 4)}\r")
    sys.stdout.flush()

def start_indicator(model_name):
    global stop_indicator_flag
    stop_indicator_flag.clear()
    t = threading.Thread(target=symbolic_thinking_indicator, args=(model_name,))
    t.daemon = True
    t.start()
    return t

def stop_indicator(thread):
    global stop_indicator_flag
    stop_indicator_flag.set()
    if thread and thread.is_alive():
        thread.join(timeout=0.3)

# 🔹 Print Function
def print_file(filepath):
    try:
        filepath = filepath.strip('"\'').replace('\\', os.sep)
        if not os.path.exists(filepath):
            shell_print(
                emoji_aware_pad(f"🤖🧻⚠️: File not found: {filepath}", 60),
                label="Print Error"
            )
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if filepath.endswith(".json"):
            try:
                content = json.loads(content)
                content_lines = [f"{model}: {resp}" for model, resp in content.items()]
            except json.JSONDecodeError:
                content_lines = [content]
        else:
            content_lines = content.splitlines()
        shell_print(
            *content_lines,
            emoji_aware_pad(f"📄 Printed from: {filepath}", 60),
            label="Print Output"
        )
        return True
    except Exception as e:
        handle_symbolic_error(e, context="print_file")
        return None

# 🔹 Group Chat Logic
group_chat_state = {}  # {session_id: {users: [], prompt: [], timer: int, state: str, votes: {}, send_votes: {}, input_timer: int, prompt_file: str}}

def log_group_echo(session_id, event, data):
    timestamp = datetime.now().isoformat()
    if session_id not in group_chat_state:
        group_chat_state[session_id] = {'users': [], 'prompt': [], 'timer': None, 'state': 'init', 'votes': {}, 'send_votes': {}, 'input_timer': None, 'prompt_file': None}
    group_chat_state[session_id]['prompt'].append({
        'event': event,
        'data': data,
        'timestamp': timestamp,
        'nullity': 'Ø⁰' if event == 'group_init' else '∅÷∅'
    })
    logger.info(f"Group Chat [{session_id}] {event}: {data}")

def initiate_group_chat(initiator, num_users, timer_option, initial_prompt=None):
    try:
        session_id = str(uuid.uuid4())
        users = [f"User{i+1}" for i in range(num_users + 1)]  # Initiator + additional users
        timer_map = {
            'none': None,
            '5s': 5,
            '30min': 1800,
            '1h': 3600,
            '1d': 86400,
            'unlimited': None
        }
        timer = timer_map.get(timer_option, None)
        input_timer = 30 if timer is not None else None  # Default 30s for input if timer set
        group_chat_state[session_id] = {
            'users': users,
            'prompt': [],
            'timer': timer,
            'state': 'active',
            'votes': {},  # For override votes
            'send_votes': {},  # For send votes
            'input_timer': input_timer,
            'prompt_file': None
        }
        log_group_echo(session_id, 'group_init', {'initiator': initiator, 'users': users, 'timer': timer_option})
        if initial_prompt:
            group_chat_state[session_id]['prompt'].append({
                'user': initiator,
                'text': initial_prompt,
                'timestamp': datetime.now().isoformat()
            })
            log_group_echo(session_id, 'prompt_init', {'user': initiator, 'text': initial_prompt})
            prompt_text = f"{initiator}: {initial_prompt}"
            group_chat_state[session_id]['prompt_file'] = save_prompt_to_file(prompt_text)
        shell_print(
            emoji_aware_pad(f"🤖🧻💬: Group chat session {session_id} started with {num_users + 1} users.", 60),
            emoji_aware_pad(f"Session Timer: {timer_option}", 60),
            label="Group Chat Init"
        )
        return session_id
    except Exception as e:
        handle_symbolic_error(e, context="initiate_group_chat")

def handle_group_prompt(session_id, current_user, initial_prompt=None):
    try:
        if session_id not in group_chat_state:
            shell_print(
                emoji_aware_pad("🤖🧻⚠️: Group chat session not found.", 60),
                label="Group Chat Error"
            )
            return None
        state = group_chat_state[session_id]
        # Ensure initial_prompt is not duplicated if already added in initiate_group_chat
        if initial_prompt and not any(p.get('text') == initial_prompt for p in state['prompt']):
            state['prompt'].append({
                'user': current_user,
                'text': initial_prompt,
                'timestamp': datetime.now().isoformat()
            })
            log_group_echo(session_id, 'prompt_init', {'user': current_user, 'text': initial_prompt})
            prompt_text = f"{current_user}: {initial_prompt}"
            state['prompt_file'] = save_prompt_to_file(prompt_text)
            logger.debug(f"Initialized group chat prompt: {prompt_text}")
        current_idx = state['users'].index(current_user) if current_user in state['users'] else 0
        while state['state'] == 'active':
            next_user = state['users'][(current_idx + 1) % len(state['users'])]
            prompt_text = ' '.join([f"{p['user']}: {p['text']}" for p in state['prompt'] if 'text' in p]) or (f"{current_user}: {initial_prompt}" if initial_prompt else "None")
            timer_display = f"Session Timer: {state['timer'] // 60 if state['timer'] else 'None'}m, Input Timer: {state['input_timer']}s" if state['timer'] else "Session Timer: None, Input Timer: None"
            shell_print(
                emoji_aware_pad(f"🤖🧻💬: Current group prompt: {prompt_text}", 60),
                emoji_aware_pad(f"📄 Saved to: {state['prompt_file'] or 'None'}", 60),
                emoji_aware_pad(f"To: {next_user}, add to prompt, vote send, skip, or override? (Type 'add', 'send', 'skip', '@over-ride-vote-yes', or '!@0ko@!/print \"<file>\"')", 60),
                emoji_aware_pad(timer_display, 60),
                emoji_aware_pad(f"Send votes: {len(state['send_votes'])}/{len(state['users'])}", 60),
                label="Group Chat Prompt"
            )
            start_time = time.time()
            action = shell_input(f"🤖🧻💬: {next_user}, enter 'add', 'send', 'skip', '@over-ride-vote-yes', or '!@0ko@!/print \"<file>\"':").strip().lower()
            if action.startswith('!@0ko@!/print'):
                try:
                    filepath = action.split('"')[1]
                    if print_file(filepath):
                        shell_print(
                            emoji_aware_pad("🤖🧻💬: Returning to group chat prompt.", 60),
                            label="Print Return"
                        )
                    continue
                except IndexError:
                    shell_print(
                        emoji_aware_pad("🤖🧻⚠️: Invalid print command. Use: !@0ko@!/print \"<file>\"", 60),
                        label="Print Error"
                    )
                    continue
            if action == '@over-ride-vote-yes':
                state['votes'][next_user] = True
                log_group_echo(session_id, 'override_vote', {'user': next_user})
                if sum(1 for v in state['votes'].values() if v) > len(state['users']) // 2:
                    state['state'] = 'finalized'
                    shell_print(
                        emoji_aware_pad("🤖🧻💬: Override vote passed. Finalizing prompt.", 60),
                        label="Group Chat Override"
                    )
                    return prompt_text
                else:
                    shell_print(
                        emoji_aware_pad(f"🤖🧻💬: {next_user} voted to override. Need {len(state['users']) // 2 + 1} votes.", 60),
                        label="Group Chat Vote"
                    )
                    current_idx = (current_idx + 1) % len(state['users'])
                    continue
            if state['input_timer'] and time.time() - start_time > state['input_timer']:
                shell_print(
                    emoji_aware_pad(f"🤖🧻💬: {next_user} timed out. Moving to next user.", 60),
                    label="Group Chat Timeout"
                )
                current_idx = (current_idx + 1) % len(state['users'])
                continue
            if action == 'send':
                state['send_votes'][next_user] = True
                log_group_echo(session_id, 'send_vote', {'user': next_user})
                if len(state['send_votes']) == len(state['users']):
                    state['state'] = 'finalized'
                    shell_print(
                        emoji_aware_pad("🤖🧻💬: All users voted to send. Finalizing prompt.", 60),
                        label="Group Chat Finalized"
                    )
                    return prompt_text
                else:
                    shell_print(
                        emoji_aware_pad(f"🤖🧻💬: {next_user} voted to send. Need {len(state['users']) - len(state['send_votes'])} more votes.", 60),
                        label="Group Chat Send Vote"
                    )
                    current_idx = (current_idx + 1) % len(state['users'])
                    continue
            elif action == 'add':
                shell_print(
                    emoji_aware_pad(f"🤖🧻💬: {next_user}, enter your addition to the prompt:", 60),
                    label="Group Chat Add"
                )
                addition = shell_input(f"🤖🧻💬: {next_user}, your prompt addition:").strip()
                confirm = shell_input(
                    f"🤖🧻💬: Is this your addition?\n↳ {addition}\n\nType 'yes' to confirm or 'no' to cancel:",
                    label="Prompt Addition Confirmation"
                ).strip().lower()
                if confirm == 'yes':
                    state['prompt'].append({'user': next_user, 'text': addition, 'timestamp': datetime.now().isoformat()})
                    log_group_echo(session_id, 'prompt_add', {'user': next_user, 'text': addition})
                    prompt_text = ' '.join([f"{p['user']}: {p['text']}" for p in state['prompt'] if 'text' in p])
                    state['prompt_file'] = save_prompt_to_file(prompt_text)
                    state['send_votes'].clear()
                    shell_print(
                        emoji_aware_pad("🤖🧻💬: Send votes reset due to new addition.", 60),
                        label="Group Chat Reset"
                    )
                else:
                    shell_print(
                        emoji_aware_pad(f"🤖🧻💬: {next_user} canceled addition.", 60),
                        label="Group Chat Cancel"
                    )
                current_idx = (current_idx + 1) % len(state['users'])
            elif action == 'skip':
                shell_print(
                    emoji_aware_pad(f"🤖🧻💬: {next_user} skipped their turn.", 60),
                    label="Group Chat Skip"
                )
                current_idx = (current_idx + 1) % len(state['users'])
                continue
            else:
                shell_print(
                    emoji_aware_pad(f"🤖🧻⚠️: Invalid action by {next_user}. Please type 'add', 'send', 'skip', '@over-ride-vote-yes', or '!@0ko@!/print \"<file>\"'.", 60),
                    label="Group Chat Error"
                )
        return prompt_text if state['state'] == 'finalized' else None
    except Exception as e:
        handle_symbolic_error(e, context="handle_group_prompt")

# 🔹 Prompt and AI Dispatch
def save_prompt_to_file(prompt, directory=PROMPT_DIR):
    try:
        os.makedirs(directory, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prompt_{timestamp}.txt"
        filepath = os.path.join(directory, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(prompt)
        return filepath
    except Exception as e:
        handle_symbolic_error(e, context="save_prompt_to_file")
        return None

def dispatch_to_ollama(model_key, prompt):
    try:
        model_info = MODEL_CONFIG.get(model_key, {"model": model_key})
        model_name = model_info["model"]
        escaped_prompt = prompt.replace('"', '\\"')
        indicator_thread = start_indicator(model_name)
        cmd = f'ollama run {model_name} "{escaped_prompt}"'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        stop_indicator(indicator_thread)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            error_msg = f"Error from {model_name}: {result.stderr.strip()}"
            logger.error(error_msg)
            return error_msg
    except Exception as e:
        stop_indicator(indicator_thread)
        handle_symbolic_error(e, context=f"dispatch_to_ollama_{model_name}")
        return f"Error dispatching to {model_name}: {str(e)}"

def save_responses(responses):
    try:
        os.makedirs(PROMPT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"response_{timestamp}.json"
        filepath = os.path.join(PROMPT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(responses, f, indent=4, ensure_ascii=False)
        return filepath
    except Exception as e:
        handle_symbolic_error(e, context="save_responses")

# 🔹 Main Entry Point
if __name__ == "__main__":
    try:
        if not check_ollama_service():
            raise Exception("Ollama service check failed. Exiting.")
        load_shift()
        shell_print(
            "🤖🧻💬: GroupChatForge V0.9.3 is active.",
            "Type your initial prompt or command (!@0ko@!/print \"<file>\", !@0ko@!FORCESTOP@!) to start.",
            label="Chat Mode"
        )
        prompt_locked = False
        input_during_lock = []
        last_unlock_time = 0
        console_state = None
        pending_prompt = None

        while True:
            user_input = shell_input("🤖🧻💬: Enter prompt or command (!@0ko@!/print \"<file>\", !@0ko@!FORCESTOP@!):", label="GroupChatForge").strip()
            input_time = time.time()

            # Check commands first
            if user_input.lower() == "!@0ko@!forcestop@!":
                prompt_locked = False
                last_unlock_time = time.time()
                console_state = None
                shell_print(
                    emoji_aware_pad("🤖🧻💬:🧻⚡️ Prompt return forcibly stopped. Console unlocked.", 60),
                    label="System Override"
                )
                continue

            if user_input.lower().startswith('!@0ko@!/print'):
                try:
                    filepath = user_input.split('"')[1]
                    if print_file(filepath):
                        shell_print(
                            emoji_aware_pad("🤖🧻💬: Returning to console.", 60),
                            label="Print Return"
                        )
                    continue
                except IndexError:
                    shell_print(
                        emoji_aware_pad("🤖🧻⚠️: Invalid print command. Use: !@0ko@!/print \"<file>\"", 60),
                        label="Print Error"
                    )
                    continue

            if prompt_locked:
                input_during_lock.append((user_input, input_time))
                shell_print(
                    emoji_aware_pad("🤖🧻💬:🧻⚠️ Prompt input is currently blocked.", 60),
                    emoji_aware_pad("🤖🧻: Your message has been recorded but not sent.", 60),
                    emoji_aware_pad("🧻 To cancel and unlock console, enter:", 60),
                    emoji_aware_pad("   !@0ko@!FORCESTOP@!", 60),
                    label="Console Lock"
                )
                continue

            if input_time - last_unlock_time < 0.5:
                shell_print(
                    emoji_aware_pad("🤖🧻💬:🧻⚠️ Buffered input detected.", 60),
                    emoji_aware_pad("🤖🧻: Your prompt has been discarded to prevent accidental dispatch.", 60),
                    emoji_aware_pad("🤖🧻: 🧻 You may copy and paste it again if needed:", 60),
                    emoji_aware_pad(f"   {user_input}", 60),
                    label="System Notice"
                )
                continue

            if not user_input or user_input.isspace() or len(user_input.strip()) <= 2:
                shell_print(
                    emoji_aware_pad("🤖🧻⚠️: Empty or invalid prompt detected.", 60),
                    label="System Notice"
                )
                console_state = None
                continue

            # Set prompt and state after command checks
            console_state = 'prompt_confirmation'
            pending_prompt = user_input

            confirm_prompt = shell_input(
                f"🤖🧻💬: Is this the prompt you want to send?\n↳ {pending_prompt}\n\nType 'yes' to confirm, 'no' to cancel, or 'ADD1', 'ADD2', 'ADD3' to invite users:",
                label="Prompt Confirmation"
            ).strip().lower()

            if confirm_prompt in ['add1', 'add2', 'add3']:
                if not pending_prompt or pending_prompt.isspace():
                    shell_print(
                        emoji_aware_pad("🤖🧻⚠️: Ø⁰ Invalid initial prompt for group chat.", 60),
                        emoji_aware_pad("Please enter a valid prompt before adding users.", 60),
                        label="Group Chat Error"
                    )
                    console_state = None
                    continue
                num_users = int(confirm_prompt[-1])
                timer_options = ['none', '5s', '30min', '1h', '1d', 'unlimited']
                timer_prompt = shell_input(
                    f"🤖🧻💬: Set timer for user input (None, 5s, 30min, 1h, 1d, unlimited):",
                    label="Timer Selection"
                ).strip().lower()
                if timer_prompt not in timer_options:
                    shell_print(
                        emoji_aware_pad(f"🤖🧻⚠️: Invalid timer option. Defaulting to None.", 60),
                        label="Timer Error"
                    )
                    timer_prompt = 'none'
                session_id = initiate_group_chat('User1', num_users, timer_prompt, initial_prompt=pending_prompt)
                console_state = 'group_chat'
                final_prompt = handle_group_prompt(session_id, 'User1')
                if final_prompt:
                    filename = group_chat_state[session_id]['prompt_file']
                    shell_print(
                        emoji_aware_pad("🔻 Group Prompt Finalized 🔻", 60),
                        emoji_aware_pad(f"🤖🧻:📤: {final_prompt}", 60),
                        emoji_aware_pad(f"📄🤖🧻: Prompt saved to: `{filename}`", 60),
                        label="Group Prompt Echo"
                    )
                    responses = {}
                    for model_key in ["phi", "mistral", "llama2"]:
                        shell_print(f"🤖🧻🚀: Dispatching to {MODEL_CONFIG[model_key]['model'].upper()}...", label="Group Prompt Dispatch")
                        responses[model_key] = dispatch_to_ollama(model_key, final_prompt)
                        shell_print(
                            emoji_aware_pad(f"🔻 {MODEL_CONFIG[model_key]['model'].upper()} AI Response 🔻", 60),
                            emoji_aware_pad(responses[model_key] if responses[model_key] else "🤖🧻:⚠️ No response received.", 60),
                            label="Group Prompt Response"
                        )
                    filepath = save_responses(responses)
                    shell_print(
                        emoji_aware_pad("📎🤖🧻: To reprint this prompt and responses, type:", 60),
                        emoji_aware_pad(f'!@0ko@!/print "{filepath}"', 60),
                        label="Prompt Print Instruction"
                    )
                console_state = None
                continue

            if confirm_prompt != "yes":
                canceled_filename = f"canceled_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(os.path.join(PROMPT_DIR, canceled_filename), "w", encoding="utf-8") as f:
                    f.write(f"Canceled Prompt: {pending_prompt}\nTimestamp: {datetime.now().isoformat()}\n")
                shell_print(
                    emoji_aware_pad(f"🤖🧻💬: Prompt canceled and saved to {canceled_filename}", 60),
                    label="Prompt Canceled"
                )
                shell_print(
                    emoji_aware_pad("🤖🧻📎: 📎 To view this prompt later, type:", 60),
                    emoji_aware_pad(f'!@0ko@!/print "{canceled_filename}"', 60),
                    label="Prompt Print Instruction"
                )
                console_state = None
                continue

            filename = save_prompt_to_file(pending_prompt)
            filepath = os.path.join(PROMPT_DIR, filename)
            shell_print(
                emoji_aware_pad("🔻 Original Prompt Sent 🔻", 60),
                emoji_aware_pad(f"🤖🧻:📤: {pending_prompt}", 60),
                emoji_aware_pad(f"🤖🧻📄: Prompt saved to: `{filename}`", 60),
                label="Prompt Echo"
            )
            prompt_locked = True
            shell_print(f"🤖🧻💬: Processing prompt: {pending_prompt}", label="Prompt Dispatch")
            try:
                responses = {}
                for model_key in ["phi", "mistral", "llama2"]:
                    shell_print(f"🤖🧻🚀: Dispatching to {MODEL_CONFIG[model_key]['model'].upper()}...", label="Prompt Dispatch")
                    responses[model_key] = dispatch_to_ollama(model_key, pending_prompt)
                    shell_print(
                        emoji_aware_pad(f"🔻 {MODEL_CONFIG[model_key]['model'].upper()} AI Response 🔻", 60),
                        emoji_aware_pad(responses[model_key] if responses[model_key] else "🤖🧻:⚠️ No response received.", 60),
                        label="Prompt Response"
                    )
                filepath = save_responses(responses)
                shell_print(
                    emoji_aware_pad("📎🤖🧻: To reprint this prompt and responses, type:", 60),
                    emoji_aware_pad(f'!@0ko@!/print "{filepath}"', 60),
                    label="Prompt Print Instruction"
                )
            except Exception as dispatch_error:
                handle_symbolic_error(dispatch_error, context="main → dispatch")
            finally:
                prompt_locked = False
                last_unlock_time = time.time()
                console_state = None
                if input_during_lock:
                    shell_print(
                        emoji_aware_pad("🔻 Input During Prompt Load — Recorded Message Not Sent 🔻", 60),
                        label="Console Record"
                    )
                    for i, (msg, _) in enumerate(input_during_lock, 1):
                        shell_print(
                            emoji_aware_pad(f"🤖🧻💬:📥 {i}. {msg}", 60),
                            label="Recorded Input"
                        )
                    input_during_lock.clear()

    except Exception as e:
        error_msg = [
            emoji_aware_pad(f"🧻🤖🧻⚠️: ERROR: {str(e)}", 60),
            emoji_aware_pad(f"🧻🤖🧻⚠️: Stack Trace: {traceback.format_exc()}", 60),
            emoji_aware_pad("🤖🧻: Notice:", 60),
            emoji_aware_pad("   A fault occurred during initialization.", 60),
            emoji_aware_pad("   Try rerunning or checking your config files.", 60)
        ]
        logger.error(f"Initialization error: {str(e)}\n{traceback.format_exc()}")
        shell_print(*error_msg, label="System Error")
        print(f"Error logged to: {log_file}")

# LICENSE.TXT
# Zero-Ology License v1.10
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.10
# October 13, 2025
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
#- VoidMathOS_lesson.py
#- zer00logy_coreV04450.py
#- zer00logy_coreV04452.py
#- zer00logy_coreV04455.py
#- zer00logy_coreV04456.py
#- README.md
#- README_0KO3MAIB.txt
#- LICENSE.txt
#- 0ko3maibZer00logyLicensev01.txt
#- rainbowquest1000.py
#- GroupChatForge.py
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
