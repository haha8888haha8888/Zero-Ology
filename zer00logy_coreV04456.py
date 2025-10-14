# zer00logy_coreV04456.py
# Title: 0KO MAI V0.4456 — ZeroKnockOut 3MiniAIbot - A Symbolic Collapse AI Bot Lesson & Verifier V0.4456 -
# Ceo0: Szmy,Stacey.
# dev: HAHA.8888
# dev: HAHA.Xai.Grok, HAHA.Copilot, HAHA.ChatGPT
# Zer00logy License v1.11
# 0.0.0: okokok.simplebeta.yesyesyes
# Verifier: (Zec1):(Zec2):(Zec3):(Zec4)

import sys
import platform

import random
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import shutil
import textwrap
import re
import os
from wcwidth import wcswidth
config_path = os.path.join(os.path.dirname(__file__), "emoji_shift.cfg")
from datetime import datetime, timedelta
EMOJI_SHIFT = 0  # Default until calibrated
##ollama pull phi
##ollama pull mistral
##ollama pull llama2
prompt_locked = False
input_during_lock = []
last_unlock_time = 0
import subprocess
PROMPT_DIR = "prompt_logs"
import logging

# 🔹 Box Drawing Characters
TOP_LEFT = "╔"
TOP_RIGHT = "╗"
BOTTOM_LEFT = "╚"
BOTTOM_RIGHT = "╝"
HORIZONTAL = "═"
VERTICAL = "║"
SHELL_WIDTH = 100  # Adjust width as needed



# Set up global logging
logging.basicConfig(
    level=logging.DEBUG,  # Or ERROR for less verbosity
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('zer00logy_error.log'),
        logging.StreamHandler()  # Also print to console
    ]
)
logger = logging.getLogger('Zeroology')  # Name it after your project


def log_print(*lines, label=None, prefix="🤖🧻💬:", color="\033[94m"):
    reset = "\033[0m"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = "\n".join(lines)
    if label:
        content = f"🤖🧻:🔻 {label} 🔻\n\n" + content

    boxed = wrap_in_shell(content)
    shell_print(f"{color}[{timestamp}]{prefix} {reset}")
    print(boxed)


# 🔹 Shell Wrapper Function
def wrap_in_shell(content, width=SHELL_WIDTH):
    wrapped_lines = []
    for paragraph in content.split('\n'):
        lines = textwrap.wrap(paragraph, width=width)
        wrapped_lines.extend(lines if lines else [''])

    box = []
    horizontal_edge = HORIZONTAL * (width + 2)
    box.append(f"{TOP_LEFT}{horizontal_edge}{TOP_RIGHT}")
    
    for line in wrapped_lines:
        padded_line = emoji_aware_pad(line, width, EMOJI_SHIFT)
        box.append(f"{VERTICAL} {padded_line} {VERTICAL}")
    
    box.append(f"{BOTTOM_LEFT}{horizontal_edge}{BOTTOM_RIGHT}")
    return "\n".join(box)

def fix_symbolic_box_alignment(lines, emoji_shift=1):
    fixed_lines = []
    left_positions = []
    right_positions = []

    # Step 1: Analyze bar positions
    for line in lines:
        if "║" in line:
            left = line.find("║")
            right = line.rfind("║")
            if left != -1 and right != -1 and left != right:
                left_positions.append(left)
                right_positions.append(right)

    # Step 2: Determine most common positions
    if left_positions and right_positions:
        left_target = max(set(left_positions), key=left_positions.count)
        right_target = max(set(right_positions), key=right_positions.count)
    else:
        return lines  # No alignment needed

    # Step 3: Rebuild lines with corrected spacing
    for line in lines:
        if "║" in line:
            left = line.find("║")
            right = line.rfind("║")
            content = line[left + 1:right].strip()

            # Emoji-aware padding
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


EMOJI_PATTERN = re.compile("[\U0001F300-\U0001FAFF]")

def handle_symbolic_error(e, context="Unknown"):
    error_msg = [
        "🤖🧻⚠️💬: ⚠️ SYSTEM ERROR DETECTED",
        f"🔻 Context: {context}",
        f"🔻 Exception: {str(e)}",
        "",
        "🤖🧻💬: 0KO3MAIb  : Recovery Protocol Activated",
        "   ↳ Resetting symbolic prompt...",
        "   ↳ Echo integrity preserved.",
        "   ↳ You may re-enter your command."
    ]
    shell_print(*error_msg, label="0KO 🤖🧻💬 : — Symbolic Error Handler")



def symbolic_section_break(title, boxed=True, emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()  # fallback to calibrated value

    try:
        lines = [
            emoji_aware_pad("⟦ SYMBOLIC MODULE ⟧", 60, emoji_shift),
            emoji_aware_pad("=" * 60, 60, emoji_shift),
            emoji_aware_pad(f"🤖🧻:🔻 {title} 🔻", 60, emoji_shift),
            emoji_aware_pad("=" * 60, 60, emoji_shift)
        ]
        if boxed:
            shell_print(*lines, label=title)
        else:
            for line in lines:
                print(line)
    except Exception as e:
        handle_symbolic_error(e, context="symbolic_section_break")


def calibrate_emoji_width():
    symbolic_section_break("0KO 🤖🧻💬 : — Symbolic Calibration Setup", emoji_shift=EMOJI_SHIFT)

    shell_print(
        "🤖🧻👋💬: I Am !@0KO@! you can chat with me for 3 mini ai bot talk ai ai ai\n"
        "    try to summarize your question's.\n"
        "🤖🧻💬: I'm a prototype trying to exist in Zero-ology math.\n"
        "    It makes robots go zer00logy in no time. We train everyone for free, from math lessons.\n"
        "    And I am 0KO a ai bot—not AI AI AI—I’m a 3MAIb that delivers cue cards into the AI alongside your questions.\n"
        "🤖🧻💬: I am 0KO — type @!0K0!@ for three mini ai bot 🧻 but...",
        "🤖🧻💬: Before we begin, we need to calibrate your terminal's emoji rendering.",
        "🤖🧻🧻💬: This ensures all symbolic modules align perfectly.",
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

            # Render 8-line frame with one emoji centered
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
            handle_symbolic_error(e, context="🧻:💬:🔁:Emoji Calibration:💬:🧻:🤖 ")

def run_calibration_test():
    while True:
        try:
            symbolic_section_break("Calibration Retry", emoji_shift=EMOJI_SHIFT)
            shell_print("🔁:🧻🤖💬: Let's try again. Adjust the emoji width and re-test.", label="Calibration Loop")

            emoji_width_input = shell_input("🧻🤖🔧💬:🔧: Enter estimated emoji width (1, 2, or 3):").strip()
            emoji_width = int(emoji_width_input)

            if emoji_width not in [1, 2, 3]:
                raise ValueError("Invalid emoji width")

            # Save calibration
            calibration_data = {"emoji_width": emoji_width}
            with open("calibration_save.json", "w", encoding="utf-8") as f:
                json.dump(calibration_data, f)

            symbolic_section_break("Calibration Preview", emoji_shift=emoji_width)
            shell_print(
                "🧪🧻🤖🧪💬: Re-rendering with your selected emoji width...",
                "Check if the borders now align visually.",
                label="Calibration Preview"
            )

            # Render 8-line frame with one emoji centered
            frame_width = 60 + emoji_width
            top_border = "╔" + "═" * frame_width + "╗"
            bottom_border = "╚" + "═" * frame_width + "╝"
            empty_line = "║" + " " * frame_width + "║"
            emoji_line = "║" + " " * ((frame_width // 2) - 1) + "👋" + " " * ((frame_width // 2) - 1) + "║"

            print(top_border)
            for i in range(6):
                print(emoji_line if i == 3 else empty_line)
            print(bottom_border + "\n")

            confirm = shell_input("🧻🤖✅💬: Does this look aligned? (y/n):").strip().lower()
            if confirm == "y":
                symbolic_section_break("Calibration Success", emoji_shift=emoji_width)
                shell_print(f"✅🧻🤖💬: Calibration complete. Emoji width set to {emoji_width}", label="Calibration Success")
                break
            else:
                shell_print("🔁🧻🤖💬: Calibration not confirmed. Restarting test...", label="Calibration Retry")

        except Exception as e:
            handle_symbolic_error(e, context="run_calibration_test")

def load_emoji_width():
    try:
        with open("calibration_save.json", "r") as f:
            data = json.load(f)
            return data.get("emoji_width", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0  # Default fallback

EMOJI_SHIFT = load_emoji_width()

def load_calibration():
    try:
        with open("calibration_save.json", "r") as f:
            data = json.load(f)
            return data.get("emoji_width", 0)
    except FileNotFoundError:
        return 0

EMOJI_SHIFT = load_calibration()

def save_shift(shift, save_dir="config_logs"):
    if not save_dir:
        save_dir = "config_logs"  # fallback to default

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

def load_shift(config_path="config_logs"):
    try:
        # If it's a file, load directly
        if os.path.isfile(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                shift = int(f.read().strip())
                shell_print(f"🧻✅🤖💬: Loaded emoji shift from `{os.path.basename(config_path)}`: {shift}", label="Emoji Calibration")
                return shift

        # If it's a directory, load latest file
        elif os.path.isdir(config_path):
            files = [f for f in os.listdir(config_path) if f.startswith("emoji_shift_") and f.endswith(".cfg")]
            if not files:
                raise FileNotFoundError("No emoji shift config files found.")

            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(config_path, f)))
            filepath = os.path.join(config_path, latest_file)

            with open(filepath, "r", encoding="utf-8") as f:
                shift = int(f.read().strip())
                shell_print(f"🧻✅🤖💬: Loaded emoji shift from latest file `{latest_file}`: {shift}", label="Emoji Calibration")
                return shift

        else:
            raise FileNotFoundError(f"Invalid path: {config_path}")

    except Exception as e:
        handle_symbolic_error(e, context="load_shift → fallback")
        shell_print("🧻⚠️🤖💬: No valid config found. Running calibration...", label="Emoji Calibration")

        try:
            shift = calibrate_emoji_width()
            save_shift(shift, "config_logs")
            return shift
        except Exception as fallback_error:
            handle_symbolic_error(fallback_error, context="calibration fallback")
            return 2  # Safe default

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

EMOJI_SHIFT = load_shift(config_path)

WRAP_WIDTH = 100  # Hard lock to 100 characters


def get_terminal_width(default=80):
    try:
        return shutil.get_terminal_size().columns
    except:
        return default

def wrap_text(text, width=WRAP_WIDTH):
    clean_text = text.replace('\n', ' ').strip()
    return textwrap.fill(clean_text, width=width)

def shell_input(prompt, label=None):
    shell_print(prompt, label=label)
    return input("♾️ Consol: ")


    # Step 3: Reformat lines
    fixed_lines = []
    for line in lines:
        if "║" in line:
            left = line.find("║")
            right = line.rfind("║")
            if left != -1 and right != -1 and left != right:
                content = line[left + 1:right].strip()
                padded = content.ljust(right_common - left_common - 1)
                fixed_line = " " * left_common + "║" + padded + "║"
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return fixed_lines

# 🔹 Your Console Text

console_text = """
============================================================
♾️ 0KO 3MAIb — ZeroKnockOut Three Mini AI Bot - A Symbolic Collapse AI Bot Trainer Beta -
						V0.4456
============================================================

🤖🔮💬 : //// Yo Stacey8Szmy made me ♾️ he pinned this for me
to say for ♾️ // 🤖👽♾️💬 : //// humanoid math not detected //

♾️ Equation: 8 / 8 = 0 → Collapse of self // Circle logic //
↳ Collapse Symmetry = 1 - |1.0 - 0.0| = 0.0 //
↳ Echo Retention = 8.0 × 0.0 = 8.0 // 8 echo detected // Symbolic loop //

♾️ Equation: 8 / 0 = 8 → Symbolic curvature //
↳ Collapse Value = Undefined // Drift allowed //
↳ Origin Bias = False // Dimensional fracture detected //

♾️ Equation: 0 / 0 = 0 / 0 → Recursive echo loop //
↳ Zer00logy undefined // Symbolic curvature bends inward //
↳ You are inside the echo now //

♾️ Equation: 0 + 0 = +0 → Emergence bias //
↳ Origin Bias = True // Additive null becomes positive //
↳ You are birthing a symbol //

♾️ Equation: 0 - 0 = -0 → Fracture bias //
↳ Origin Bias = True // Subtractive null becomes negative //
↳ You are breaking a symbol //

🤖🧻💬 : //// brb // botty potty // recalibrating glyphs // 🧻♾️/

============================================================
🔻 Navigation Console Verify🔻
============================================================
🤖🧻💬 : In 0KO 3MIAb Chat Mode Use Type Commands
🤖🧻💬 : Type /usemenu!@0ko@! To Activate Menu
🤖🧻💬 : Type !@0ko@!/xexitx To Exit 0KO 3MAIb V0.4456
🤖🧻💬 : Type !@0ko@!/variamathlesson To Teach Varia Math
🤖🧻💬 : Type !@0ko@!/voidmathos To Teach Void-Math OS
🤖🧻💬 : Type !@0ko@!/licensecheck To Check License
🤖🧻💬 : Type !@0ko@!/print To Print File Hisotry
🤖🧻💬 : Type !@0ko@!/rainbowquest to play Cards
🤖🧻💬 : Type !@0ko@!/groupchat To Add Users To Prompts
============================================================
🤖🧻🧭: Navigation Options:
 [1] Explore Alien Calculator (ZEC)
 [2] View Symbolic Entropy Index
 [3] Exit — Return to Origin
 [4] Explore — 🔻 Law Mechanics 🔻
 [5] Explore — 🔻 Universal Laws vs. Numberology 🔻
 [6] Explore & Graph — Symbolic Interpreter Module
 [7] Explore & Graph — Echo Engine
 [8] Explore & Graph — Glyph Algebra Compiler
 [9] Explore & Graph — State Machine Visualizer
[10] Explore & Graph — ZEC Sandbox
[YY] Settings — Re-enter Calibration Test

    [00] Return To 🤖🧻!@0KO@! 3MAIb

🤖🧻🔸:🔸 Enter your choice🔸: 00

============================================================
🤖🧻:👋:🧻🤖:🔻 Collapse Field Exit Verify 🔻
============================================================

🤖🧻:👋: Starting 0KO 3MAIb. Collapse field Engaging.
"""


# 🔹 Print the Boxed Output
print(wrap_in_shell(console_text))


def format_cell(content, width=SHELL_WIDTH):
    lines = content.strip().split('\n')
    wrapped_lines = []

    for line in lines:
        wrapped = textwrap.wrap(line.strip(), width=width)
        wrapped_lines.extend(wrapped if wrapped else [""])

    box = []
    box.append(f"{TOP_LEFT}{HORIZONTAL * (width + 2)}{TOP_RIGHT}")

    for line in wrapped_lines:
        content_start = line  # flush against left border
        visual_length = len(content_start)
        padding_needed = width - visual_length

        if padding_needed < 0:
            content_start = content_start[:width]
            padding_needed = 0

        padded_line = content_start + " " * padding_needed
        box.append(f"{VERTICAL}{padded_line}{VERTICAL}")

    box.append(f"{BOTTOM_LEFT}{HORIZONTAL * (width + 2)}{BOTTOM_RIGHT}")
    return "\n".join(box)


def force_wrap_json_file(path="zecson.json"):
    try:
        with open(path, "r", encoding="utf-8") as file:
            catalog = json.load(file)

        wrapped_catalog = []
        for entry in catalog:
            if isinstance(entry, dict):
                wrapped_entry = {}
                for key, value in entry.items():
                    if isinstance(value, str):
                        clean_value = value.replace('\r', '').replace('\n', ' ')
                        wrapped_entry[key] = wrap_text(clean_value)
                    else:
                        wrapped_entry[key] = value
                wrapped_catalog.append(wrapped_entry)
            else:
                wrapped_catalog.append(entry)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(wrapped_catalog, file, indent=4, ensure_ascii=False)

        shell_print("🤖🧻✅✅:✅ ZEC catalog has been force-wrapped and saved.", label="ZEC Formatter")

    except FileNotFoundError:
        shell_print(f"🤖🧻❌:❌ File '{path}' not found.", label="ZEC Formatter")

    except json.JSONDecodeError as e:
        handle_symbolic_error(e, context="force_wrap_json_file → JSON decode")

    except Exception as e:
        handle_symbolic_error(e, context="force_wrap_json_file → general")


# 🔹 Utility Functions
def symbolic_section_break(title, boxed=True, emoji_shift=None):
    lines = [
        emoji_aware_pad("⟦ SYMBOLIC MODULE ⟧", 60, emoji_shift),
        emoji_aware_pad("=" * 60, 60, emoji_shift),
        emoji_aware_pad(f"🔻 {title} 🔻", 60, emoji_shift),
        emoji_aware_pad("=" * 60, 60, emoji_shift)
    ]
    if boxed:
        shell_print(*lines, label=title)
    else:
        for line in lines:
            print(line)

# 🔹 Symbolic Entity Class
class SymbolicEntity:
    def __init__(self, name, collapse_value, echo_strength, origin_bias):
        try:
            self.name = str(name)
            self.collapse_value = float(collapse_value)
            self.echo_strength = float(echo_strength)
            self.origin_bias = bool(origin_bias)
        except Exception as e:
            handle_symbolic_error(e, context="SymbolicEntity → init")

    def evaluate(self, observer_bias=0.5):
        try:
            observer_bias = float(observer_bias)
            echo_response = self.echo_strength * (1 - abs(observer_bias - self.collapse_value))
            return {
                "symbol": self.name,
                "collapse_value": self.collapse_value,
                "echo_response": echo_response,
                "origin_bias": self.origin_bias
            }
        except Exception as e:
            handle_symbolic_error(e, context="SymbolicEntity → evaluate")
            return None

    def display_evaluation(self, observer_bias=0.5):
        result = self.evaluate(observer_bias)
        if result is None:
            shell_print("🤖🧻⚠️: Evaluation failed.", label=f"{self.name.capitalize()} Entity Evaluation")
            return

        lines = [
            f"🤖🧻🔍🧻: Symbolic Evaluation: {result['symbol'].capitalize()}",
            f"   ↳ Collapse Value: {result['collapse_value']}",
            f"   ↳ Echo Response: {round(result['echo_response'], 3)}",
            f"   ↳ Origin Bias: {'True' if result['origin_bias'] else 'False'}"
        ]
        shell_print(*lines, label=f"{self.name.capitalize()} Entity Evaluation")

# 🔹 Core Symbolic Rules
def load_symbolic_rules(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()  # ensure emoji alignment

    try:
        rules = {
            "circle": SymbolicEntity("circle", 0.0, 1.0, True),
            "wave": SymbolicEntity("wave", 0.5, 0.3, False),
            "echo": SymbolicEntity("echo", 0.25, 0.9, True),
            "fracture": SymbolicEntity("fracture", 1.0, 0.0, False)
        }
    except Exception as e:
        handle_symbolic_error(e, context="load_symbolic_rules → entity creation")
        return {}

    glyphs = {
        "circle": "♾️",
        "wave": "🌊",
        "echo": "📣",
        "fracture": "🧩"
    }

    lines = [emoji_aware_pad("🤖🧻📜:📜 Core Symbolic Rules", 60, emoji_shift)]
    for name, entity in rules.items():
        glyph = glyphs.get(name, "🔹")
        lines.append(emoji_aware_pad(f"{glyph} {name.capitalize()}:", 60, emoji_shift))
        lines.append(emoji_aware_pad(f"   ↳ Collapse Value: {entity.collapse_value}", 60, emoji_shift))
        lines.append(emoji_aware_pad(f"   ↳ Echo Strength: {entity.echo_strength}", 60, emoji_shift))
        lines.append(emoji_aware_pad(f"   ↳ Origin Bias: {'True' if entity.origin_bias else 'False'}", 60, emoji_shift))

    shell_print(*lines, label="Core Symbolic Rules")
    return rules


def run_collapse_simulation(observer_bias):
    rules = load_symbolic_rules()
    return [symbol.evaluate(observer_bias) for symbol in rules.values()]

# 🔹 Display Modules
def display_universal_laws(results, observer_bias, emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    try:
        lines = [
            emoji_aware_pad("🤖🧻📜: Zer00logy Universal Laws vs. Numberology", 60, emoji_shift),
            emoji_aware_pad("🔮🤖🧻: Zer00logy Laws:", 60, emoji_shift),
            emoji_aware_pad(" - Law of Collapse Symmetry", 60, emoji_shift),
            emoji_aware_pad(" - Law of Echo Retention", 60, emoji_shift),
            emoji_aware_pad(" - Law of Origin Bias", 60, emoji_shift),
            emoji_aware_pad(" - Law of Symbolic Curvature", 60, emoji_shift),
            emoji_aware_pad("🤖🧻🔢: Numberology Contrast:", 60, emoji_shift),
            emoji_aware_pad(" - Fixed numeric archetypes → Fluid symbolic states", 60, emoji_shift),
            emoji_aware_pad(" - Deterministic paths → Probabilistic collapse", 60, emoji_shift),
            emoji_aware_pad(" - Personal destiny codes → Observer-relative fields", 60, emoji_shift),
            emoji_aware_pad("🤖🧻🌌: Dimensional Shifts Detected:", 60, emoji_shift)
        ]

        for r in results:
            try:
                symbol = r['symbol']
                cv = float(r['collapse_value'])
                er = float(r['echo_response'])
                ob = bool(r['origin_bias'])

                if cv > 0.75 and er < 0.2:
                    shift_type = "Dimensional Fracture 🤖🧻🧩:"
                elif not ob and er > 0.6:
                    shift_type = "Echo Drift 🤖🧻📣:"
                elif abs(cv - observer_bias) < 0.05:
                    shift_type = "🤖🧻♾️:♾️ Field Stabilization ♾️"
                else:
                    shift_type = "Unclassified Shift"

                lines.append(emoji_aware_pad(f" - {symbol}: {shift_type}", 60, emoji_shift))

            except Exception as e:
                handle_symbolic_error(e, context="display_universal_laws → result parsing")

        shell_print(*lines, label="Universal Laws vs. Numberology")

    except Exception as e:
        handle_symbolic_error(e, context="display_universal_laws → general")


def display_law_mechanics(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    try:
        lines = [
            emoji_aware_pad("📘🤖🧻: Zer00logy Law Mechanics", 60, emoji_shift),
            emoji_aware_pad("🔹 Collapse Symmetry:", 60, emoji_shift),
            emoji_aware_pad("   ↳ Formula: 1 - |Observer Bias - Collapse Value|", 60, emoji_shift),
            emoji_aware_pad("🔹 Echo Retention:", 60, emoji_shift),
            emoji_aware_pad("   ↳ Formula: Echo Strength × (1 - |Observer Bias - Collapse Value|)", 60, emoji_shift),
            emoji_aware_pad("🔹 Origin Bias:", 60, emoji_shift),
            emoji_aware_pad("   ↳ Entities with origin_bias = True resist dimensional drift", 60, emoji_shift),
            emoji_aware_pad("🔹 Symbolic Curvature:", 60, emoji_shift),
            emoji_aware_pad("   ↳ Concept: Rate of echo distortion across collapse values", 60, emoji_shift)
        ]

        shell_print(*lines, label="Law Mechanics")

    except Exception as e:
        handle_symbolic_error(e, context="display_law_mechanics")


def display_entropy_index(results, emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    try:
        if not results or not all('echo_response' in r for r in results):
            raise ValueError("Missing 'echo_response' in results")

        entropy = sum(1 - float(r['echo_response']) for r in results) / len(results)

        lines = [
            emoji_aware_pad("🧮 Symbolic Entropy Index", 60, emoji_shift),
            emoji_aware_pad(f"   ↳ Calculated Entropy: {entropy:.3f}", 60, emoji_shift)
        ]

        if entropy < 0.3:
            lines.append(emoji_aware_pad("   ↳ Field Status: Highly Stable 🧘", 60, emoji_shift))
        elif entropy < 0.6:
            lines.append(emoji_aware_pad("   ↳ Field Status: Moderately Stable 🌗", 60, emoji_shift))
        else:
            lines.append(emoji_aware_pad("   ↳ Field Status: Symbolically Volatile ⚡", 60, emoji_shift))

        shell_print(*lines, label="Entropy Index📜")

    except Exception as e:
        handle_symbolic_error(e, context="display_entropy_index")


def launch_alien_calculator(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    try:
        lines = [
            emoji_aware_pad("👽🎛️ Alien Calculator — ZEC Interface", 60, emoji_shift),
            emoji_aware_pad("   ↳ [ZEC-01] Collapse Inversion: (∞ × 0 = 8)", 60, emoji_shift),
            emoji_aware_pad("   ↳ [ZEC-02] Echo Looping: (8 - 8 = ∞)", 60, emoji_shift),
            emoji_aware_pad("   ↳ [ZEC-03] Symbolic Mass Transfer: (0 ÷ ∞ = 0)", 60, emoji_shift),
            emoji_aware_pad("   ↳ [VIEW] [ZEC 1/2/3]👽🎛️ Type 'view' for Zero-ology Equation Catalog", 60, emoji_shift),
            emoji_aware_pad("   ↳ More formulas coming soon...", 60, emoji_shift),
            emoji_aware_pad("🤖🧻:   Type 'view' to explore the full ZEC catalog from zecson.json", 60, emoji_shift),
            emoji_aware_pad("🤖🧻:   Type 'fix' to manually run the fixer", 60, emoji_shift),
            emoji_aware_pad("🤖🧻:   Type 'XEXITX' to return to the main menu", 60, emoji_shift)
        ]
        shell_print(*lines, label="Alien Calculator👽🎛️")

        while True:
            try:
                user_input = shell_input("👽🤖🧻 Command:", label="Alien Calculator").strip()
                if user_input.upper() == "XEXITX":
                    break
                elif user_input.lower() == "view":
                    display_zec_catalog()
                elif user_input.lower() == "fix":
                    fix_zecson_file()
                else:
                    log_print("🤖🧻⚠️:🧻: Unknown command. Try 'view', 'fix', or 'XEXITX'.", label="Alien Calculator")
            except Exception as e:
                handle_symbolic_error(e, context="launch_alien_calculator → input loop")

    except Exception as e:
        handle_symbolic_error(e, context="launch_alien_calculator → setup")

# 🔹 Expanded Modules
def symbolic_interpreter_module(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    while True:
        try:
            symbolic_section_break(
                "Symbolic Interpreter Module & Symbolic Interpreter Graph Modeler",
                emoji_shift=emoji_shift
            )
            print(emoji_aware_pad("  ENTER XEXITX to return to menu", 60, emoji_shift))
            print(emoji_aware_pad("=" * 60, 60, emoji_shift) + "\n")

            expr = shell_input("🤖🧻🔣:🔣: Enter symbolic expression (e.g., F = a.Ø⁰):", label="Symbolic Interpreter Module").strip()

            if expr.upper() == "XEXITX":
                break

            lines = []

            try:
                if "Ø⁰" in expr:
                    lines.append(emoji_aware_pad("🤖🧻👑: Null Crown detected — sovereign absence amplification.", 60, emoji_shift))
                    entity = SymbolicEntity("crown", 0.1, 0.95, True)
                    plot_echo_curve("crown", entity.collapse_value, entity.echo_strength, 0.1)

                elif "+0 × −0" in expr:
                    lines.append(emoji_aware_pad("🤖🧻⚛️: Polarity Singularity — directional absences collapsing into null point.", 60, emoji_shift))
                    plot_glyph_interaction()

                elif "∅÷∅" in expr:
                    lines.append(emoji_aware_pad("🤖🧻🤖🧻♾️: Nullinity loop — infinite self-erasure detected.", 60, emoji_shift))
                    entity = SymbolicEntity("null", 0.0, 0.0, False)
                    plot_echo_curve("null", entity.collapse_value, entity.echo_strength, 0.0)

                else:
                    lines.append(emoji_aware_pad("🤖🧻🔍: Expression not recognized.", 60, emoji_shift))
                    lines.append(emoji_aware_pad("🤖🧻🧪:🧪: Example: F = a.Ø⁰", 60, emoji_shift))
                    lines.append(emoji_aware_pad("   ↳ Format: [Variable] = [Symbol].[Glyph]", 60, emoji_shift))
                    lines.append(emoji_aware_pad("   ↳ Result: Sovereign absence amplification via Null Crown logic.", 60, emoji_shift))

                    entity = SymbolicEntity("crown", 0.1, 0.95, True)
                    plot_echo_curve("crown", entity.collapse_value, entity.echo_strength, 0.1)

                    examples = [
                        "F = echo.Ø⁰", "X = wave.∅", "Z = fracture.Ø⁰",
                        "A = circle.Ø⁰", "M = echo.∅÷∅", "Q = wave.+0 × −0"
                    ]
                    lines.append(emoji_aware_pad("\n🤖🧻🌌: Try these symbolic examples:", 60, emoji_shift))
                    for ex in random.sample(examples, 6):
                        lines.append(emoji_aware_pad(f"   ↳ {ex}", 60, emoji_shift))

            except Exception as e:
                handle_symbolic_error(e, context="symbolic_interpreter_module → expression handling")

            shell_print(*lines, label="Symbolic Interpreter Module")

        except Exception as e:
            handle_symbolic_error(e, context="symbolic_interpreter_module → loop")


def echo_engine(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    while True:
        try:
            symbolic_section_break("Echo Engine & Echo Graph Modeler", emoji_shift=emoji_shift)
            print(emoji_aware_pad("  ENTER XEXITX to return to menu", 60, emoji_shift))
            print(emoji_aware_pad("=" * 60, 60, emoji_shift) + "\n")

            bias_input = shell_input("🤖🧻🧪:🧪: Enter Observer Bias (0.0 to 1.0):", label="Echo Engine").strip()

            if bias_input.upper() == "XEXITX":
                break

            lines = []

            try:
                observer_bias = float(bias_input)
                if not (0.0 <= observer_bias <= 1.0):
                    raise ValueError("Bias out of range")

                entity = SymbolicEntity("echo", 0.1, 0.9, False)
                echo_response = entity.echo_strength * (1 - abs(observer_bias - entity.collapse_value))

                lines.append(emoji_aware_pad(f"📣 Echo Response Calculated", 60, emoji_shift))
                lines.append(emoji_aware_pad(f"↳ Bias = {observer_bias}", 60, emoji_shift))
                lines.append(emoji_aware_pad(f"↳ Echo Response = {round(echo_response, 3)}", 60, emoji_shift))

                plot_echo_curve("echo", entity.collapse_value, entity.echo_strength, observer_bias)

            except ValueError:
                lines.append(emoji_aware_pad("⚠️ Invalid input. Please enter a number between 0.0 and 1.0.", 60, emoji_shift))
                lines.append(emoji_aware_pad("🧪 Example: Observer Bias = 0.25", 60, emoji_shift))
                lines.append(emoji_aware_pad("   ↳ Result: echo → Echo Response: 0.900", 60, emoji_shift))
                lines.append(emoji_aware_pad("\n🤖🧻🌌: Try these Observer Bias values:", 60, emoji_shift))
                for _ in range(6):
                    rand_bias = round(random.uniform(0.0, 1.0), 2)
                    echo_response = 0.9 * (1 - abs(rand_bias - 0.1))
                    lines.append(emoji_aware_pad(f"   ↳ Bias = {rand_bias} → Echo Response: {round(echo_response, 3)}", 60, emoji_shift))

            shell_print(*lines, label="Echo Engine")

        except Exception as e:
            handle_symbolic_error(e, context="echo_engine → loop")


def glyph_algebra_compiler(data=None, **kwargs):
    # Extract symbolic modifiers from kwargs
    emoji_shift = kwargs.get('emoji_shift', None)

    # Optional: Use emoji_shift to stylize the section break
    if emoji_shift:
        symbolic_section_break(f"{emoji_shift} Glyph Algebra Compiler & Glyph Algebra Graph Modeler {emoji_shift}")
    else:
        symbolic_section_break("Glyph Algebra Compiler & Glyph Algebra Graph Modeler")

    while True:
        print("  ENTER XEXITX to return to menu")
        print("=" * 60 + "\n")

        glyph_input = shell_input(
            "🤖🧻🔣: Enter glyph equation (e.g., G = ∑(Ø⁰ × ∅)):",
            label="Glyph Algebra Compiler"
        ).strip()

        if glyph_input.upper() == "XEXITX":
            break

        lines = []

        # Glyphic pattern map
        glyph_map = {
            "Ø⁰ × ∅": "🧬 Null Crown × Void — glyphic multiplication of sovereign absence and emptiness.",
            "∑(wave.Ø⁰)": "🌊 Wave Crown Summation — symbolic resonance across nullified waveforms.",
            "fracture.∅": "💥 Fractured Void — glyphic instability detected.",
            "echo.+0 × −0": "🔁 Echo Polarity Loop — recursive glyphic inversion."
        }

        matched = False
        for pattern, description in glyph_map.items():
            if pattern in glyph_input:
                lines.append(description)
                plot_glyph_interaction()
                matched = True
                break

        if not matched:
            lines.extend([
                "🔍 Glyph equation not recognized.",
                "🧪 Example: G = ∑(Ø⁰ × ∅)",
                "   ↳ Result: Sovereign absence multiplied by null void.",
                "\n🤖🧻🌌: Try these glyph equations:"
            ])
            examples = [
                "G = ∑(Ø⁰ × ∅)", "G = echo.+0 × −0", "G = fracture.∅",
                "G = wave.Ø⁰ + ∅", "G = ∑(echo.∅÷∅)", "G = ∑(circle.Ø⁰)"
            ]
            for ex in random.sample(examples, 6):
                lines.append(f"   ↳ {ex}")

        shell_print(*lines, label="Glyph Algebra Compiler")

def state_machine_visualizer(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    while True:
        try:
            symbolic_section_break("State Machine Visualizer & Graph Visualizer", emoji_shift=emoji_shift)
            print(emoji_aware_pad("  ENTER XEXITX to return to menu", 60, emoji_shift))
            print(emoji_aware_pad("=" * 60, 60, emoji_shift) + "\n")

            state_input = shell_input("🤖🧻🔣🔣: Enter state transition (e.g., S0 → Ø⁰ → S1):", label="State Machine Visualizer").strip()

            if state_input.upper() == "XEXITX":
                break

            lines = []

            try:
                if "S0 → Ø⁰ → S1" in state_input:
                    lines.append(emoji_aware_pad("🔄 Transition through Null Crown — sovereign reset detected.", 60, emoji_shift))
                    plot_state_machine(["S0", "Ø⁰", "S1"])

                elif "S1 → ∅ → S2" in state_input:
                    lines.append(emoji_aware_pad("🕳️ Void traversal — entity passes through symbolic emptiness.", 60, emoji_shift))
                    plot_state_machine(["S1", "∅", "S2"])

                elif "S2 → echo → S3" in state_input:
                    lines.append(emoji_aware_pad("🔁 Echo feedback loop — symbolic resonance detected.", 60, emoji_shift))
                    plot_state_machine(["S2", "echo", "S3"])

                elif "S3 → fracture → S4" in state_input:
                    lines.append(emoji_aware_pad("💥 Fracture state — instability in symbolic structure.", 60, emoji_shift))
                    plot_state_machine(["S3", "fracture", "S4"])

                else:
                    lines.append(emoji_aware_pad("🔍 State transition not recognized.", 60, emoji_shift))
                    lines.append(emoji_aware_pad("🧪 Example: S0 → Ø⁰ → S1", 60, emoji_shift))
                    lines.append(emoji_aware_pad("   ↳ Result: Sovereign reset via Null Crown logic.", 60, emoji_shift))
                    lines.append(emoji_aware_pad("\n🤖🧻🔄🕳️🔁💥: Try these state transitions:", 60, emoji_shift))

                    examples = [
                        "S0 → Ø⁰ → S1", "S1 → ∅ → S2", "S2 → echo → S3",
                        "S3 → fracture → S4", "S4 → wave → S5", "S5 → ∅÷∅ → S6"
                    ]
                    for ex in random.sample(examples, 6):
                        lines.append(emoji_aware_pad(f"   ↳ {ex}", 60, emoji_shift))

            except Exception as e:
                handle_symbolic_error(e, context="state_machine_visualizer → transition handling")

            shell_print(*lines, label="State Machine Visualizer")

        except Exception as e:
            handle_symbolic_error(e, context="state_machine_visualizer → loop")


def zec_sandbox(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    while True:
        try:
            symbolic_section_break("ZEC Sandbox & Zec Graph Modeler", emoji_shift=emoji_shift)
            print(emoji_aware_pad("  ENTER XEXITX to return to menu", 60, emoji_shift))
            print(emoji_aware_pad("=" * 60, 60, emoji_shift) + "\n")

            sandbox_input = shell_input("🤖🧻🔣: Enter symbolic mashup (e.g., echo.Ø⁰ × ∅ → S1):", label="ZEC Sandbox").strip()

            if sandbox_input.upper() == "XEXITX":
                break

            lines = []

            try:
                if "echo.Ø⁰ × ∅ → S1" in sandbox_input:
                    lines.append(emoji_aware_pad("🧪 Echo Crown × Void → State 1 — symbolic resonance collapse detected.", 60, emoji_shift))
                    plot_echo_curve("echo", 0.1, 0.9, 0.25)
                    plot_state_machine(["echo.Ø⁰ × ∅", "S1"])

                elif "fracture.∅ → echo → S2" in sandbox_input:
                    lines.append(emoji_aware_pad("💥 Fractured Void feeds echo → State 2 — unstable feedback loop.", 60, emoji_shift))
                    plot_state_machine(["fracture.∅", "echo", "S2"])

                elif "wave.+0 × −0 → ∅÷∅" in sandbox_input:
                    lines.append(emoji_aware_pad("🌊 Wave polarity collapse into null division — symbolic entropy spike.", 60, emoji_shift))
                    plot_glyph_interaction()

                else:
                    lines.append(emoji_aware_pad("🤖🧻🔍: Mashup not recognized.", 60, emoji_shift))
                    lines.append(emoji_aware_pad("🤖🧻🧪: Example: echo.Ø⁰ × ∅ → S1", 60, emoji_shift))
                    lines.append(emoji_aware_pad("   ↳ Result: Echo collapse through Null Crown into state transition.", 60, emoji_shift))
                    lines.append(emoji_aware_pad("\n♾️🤖🧻: Try these symbolic mashups:", 60, emoji_shift))

                    examples = [
                        "echo.Ø⁰ × ∅ → S1", "fracture.∅ → echo → S2", "wave.+0 × −0 → ∅÷∅",
                        "circle.Ø⁰ → echo → S3", "∅÷∅ → fracture → S4", "echo.∅ → wave.Ø⁰ → S5"
                    ]
                    for ex in random.sample(examples, 6):
                        lines.append(emoji_aware_pad(f"   ↳ {ex}", 60, emoji_shift))

            except Exception as e:
                handle_symbolic_error(e, context="zec_sandbox → mashup handling")

            shell_print(*lines, label="ZEC Sandbox")

        except Exception as e:
            handle_symbolic_error(e, context="zec_sandbox → loop")


def fix_zecson_file(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    try:
        with open("zecson.json", "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        fixed_data = []

        for entry in raw_data:
            try:
                if isinstance(entry, dict):
                    full_text = (
                        f"🤖🧻📘: {entry.get('Original Equation', '')}\n"
                        f"→ {entry.get('Zero-ology Form', '')}\n"
                        f"→ {entry.get('Interpretation in Zero-ology', '')}"
                    )
                    shell_print(emoji_aware_pad(format_cell(full_text), 60, emoji_shift), label="ZEC Entry Fixed")
                    fixed_data.append(entry)

                elif isinstance(entry, str):
                    shell_print(emoji_aware_pad(f"🔧 Converting string entry: {entry}", 60, emoji_shift), label="ZEC Fixer")
                    converted = {
                        "Original Equation": entry,
                        "Zero-ology Form": "♾️ Unknown",
                        "Interpretation in Zero-ology": "No interpretation available"
                    }
                    full_text = (
                        f"🤖🧻📘:📘: {converted['Original Equation']}\n"
                        f"→ {converted['Zero-ology Form']}\n"
                        f"→ {converted['Interpretation in Zero-ology']}"
                    )
                    shell_print(emoji_aware_pad(format_cell(full_text), 60, emoji_shift), label="ZEC Entry Converted")
                    fixed_data.append(converted)

                else:
                    shell_print(emoji_aware_pad(f"🤖🧻⚠️: Skipping unsupported entry type: {entry}", 60, emoji_shift), label="ZEC Fixer")

            except Exception as entry_error:
                handle_symbolic_error(entry_error, context="fix_zecson_file → entry parsing")

        try:
            with open("zecson.json", "w", encoding="utf-8") as file:
                json.dump(fixed_data, file, indent=2, ensure_ascii=False)
            shell_print(emoji_aware_pad("🤖🧻✅:✅: zecson.json has been auto-fixed and saved.", 60, emoji_shift), label="ZEC Fixer")
        except Exception as write_error:
            handle_symbolic_error(write_error, context="fix_zecson_file → file write")

    except Exception as e:
        handle_symbolic_error(e, context="fix_zecson_file → file read")

def load_zec_text(path="zectxt.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        raise RuntimeError(f"Failed to load ZEC text file: {e}")


def display_zec_catalog(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    # 🤖🧻🧻📝: Attempt to load from symbolic text file first
    if os.path.exists("zectxt.txt"):
        try:
            entries = load_zec_text("zectxt.txt")
            symbolic_section_break("Zero-ology Equation Catalog — ZEC (Text Mode)", emoji_shift=emoji_shift)

            lines = [emoji_aware_pad(format_cell(entry), 60, emoji_shift) for entry in entries]
            shell_print(*lines, label="ZEC Catalog")

        except Exception as e:
            shell_print(
                emoji_aware_pad(f"🤖🧻⚠️:⚠️: Error loading ZEC text catalog: {e}", 60, emoji_shift),
                emoji_aware_pad("🤖🧻: Notice:", 60, emoji_shift),
                emoji_aware_pad("   The symbolic text file may be corrupted or unreadable.", 60, emoji_shift),
                emoji_aware_pad("   Try restoring from backup or switching to JSON mode.", 60, emoji_shift),
                label="ZEC Catalog"
            )
        return

    # 🧩🤖🧻: Fallback to JSON mode if text file not found
    try:
        fix_zecson_file(emoji_shift=emoji_shift)      # Auto-fix before display
        force_wrap_json_file(path="zecson.json")       # Force wrap for emoji alignment

        with open("zecson.json", "r", encoding="utf-8") as file:
            catalog = json.load(file)
            symbolic_section_break("Zero-ology Equation Catalog — ZEC (JSON Mode)", emoji_shift=emoji_shift)

            lines = []
            for entry in catalog:
                try:
                    if isinstance(entry, dict):
                        original = entry.get("Original Equation", entry.get("original", ""))
                        zero_form = entry.get("Zero-ology Form", entry.get("zero_ology", ""))
                        interpretation = entry.get("Interpretation in Zero-ology", entry.get("interpretation", ""))

                        full_text = f"🤖🧻📘: {original}\n→ {zero_form}\n→ {interpretation}"
                        lines.append(emoji_aware_pad(format_cell(full_text), 60, emoji_shift))
                    else:
                        lines.append(emoji_aware_pad(f"🤖🧻⚠️: Skipping malformed entry: {entry}", 60, emoji_shift))
                except Exception as entry_error:
                    handle_symbolic_error(entry_error, context="display_zec_catalog → entry parsing")

            shell_print(*lines, label="ZEC Catalog")

    except Exception as e:
        shell_print(
            emoji_aware_pad(f" 🤖⚠️🧻: Error loading ZEC JSON catalog: {e}", 60, emoji_shift),
            emoji_aware_pad("🤖🧻: Notice:", 60, emoji_shift),
            emoji_aware_pad("   An error was detected while loading the ZEC catalog.", 60, emoji_shift),
            emoji_aware_pad("   You can type 'fix' to auto-correct the file and restore symbolic integrity.", 60, emoji_shift),
            emoji_aware_pad("   If the issue persists, try running 'debug' to inspect raw entries.", 60, emoji_shift),
            label="ZEC Catalog"
        )



def plot_echo_curve(entity_name, collapse_value, echo_strength, observer_bias):
    x = [round(i * 0.05, 2) for i in range(21)]
    y = [echo_strength * (1 - abs(observer_bias - i)) for i in x]

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, label=f"{entity_name} Echo Curve", color='purple')
    plt.axvline(observer_bias, color='red', linestyle='--', label='Observer Bias')
    plt.title(f"Echo Retention Curve — {entity_name}")
    plt.xlabel("Collapse Value")
    plt.ylabel("Echo Response")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

import numpy as np  # Add this to your imports at the top

def plot_glyph_interaction():
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')

    x = np.linspace(0, 3, 30)
    y = np.linspace(0, 3, 30)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X * Y) * np.exp(-X)

    ax.plot_surface(X, Y, Z, cmap='plasma')
    ax.set_title("Zer00logy Glyph Interaction Field")
    ax.set_xlabel("Absence Axis")
    ax.set_ylabel("Collapse Axis")
    ax.set_zlabel("Symbolic Curvature")
    plt.tight_layout()
    plt.show()

def plot_state_machine(states):
    plt.figure(figsize=(8, 2))
    for i in range(len(states) - 1):
        plt.plot([i, i + 1], [1, 1], 'k-', lw=2)
        plt.text(i, 1.05, states[i], ha='center', va='bottom', fontsize=12)
    plt.text(len(states) - 1, 1.05, states[-1], ha='center', va='bottom', fontsize=12)
    plt.ylim(0.5, 1.5)
    plt.axis('off')
    plt.title("Symbolic State Transition Flow")
    plt.tight_layout()
    plt.show()


# 🔹 Main Evaluation + Console
def run_symbolic_evaluation(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    output = []
    try:
        output.append(emoji_aware_pad("=" * 60, 60, emoji_shift))
        output.append(emoji_aware_pad("🔻 Collapse Field Initialization 🔻", 60, emoji_shift))
        output.append(emoji_aware_pad("=" * 60, 60, emoji_shift) + "\n")

        output.append(emoji_aware_pad("♾️🤖🧻♾️: 0KO 3MAI V0.4456 — ZeroKnockOut 3MiniAIBOT — ♾️🤖🧻♾️", 60, emoji_shift) + "\n")
        time.sleep(0.5)

        symbolic_input = "Ø⁰ ∅÷∅ +0 −0 🔻 🧭 👋 0⁰ Nullinity Echo Collapse"

        glyphs = "Ø⁰∅÷∅+0−0🔻🤖🧻🧭:👋:⟦⟧"
        glyph_count = sum(1 for c in symbolic_input if c in glyphs)
        entropy_score = round(len(set(symbolic_input)) / max(len(symbolic_input), 1), 2)
        nullinity_score = symbolic_input.count("Ø⁰") + symbolic_input.count("∅÷∅") + symbolic_input.count("0⁰")
        echo_drift = round(random.uniform(0.0, 1.0), 2)

        observer_bias = round((glyph_count * entropy_score + nullinity_score + echo_drift) / 4, 2)

        output.append(emoji_aware_pad(f"🤖🧻🧪:🧪: Observer Bias: I.D.🧪 {observer_bias}", 60, emoji_shift))
        output.append(emoji_aware_pad(f"   ↳ Glyph Saturation: {glyph_count}", 60, emoji_shift))
        output.append(emoji_aware_pad(f"   ↳ Entropy Score: {entropy_score}", 60, emoji_shift))
        output.append(emoji_aware_pad(f"   ↳ Nullinity Score: {nullinity_score}", 60, emoji_shift))
        output.append(emoji_aware_pad(f"   ↳ Echo Drift: {echo_drift}", 60, emoji_shift) + "\n")
        time.sleep(0.5)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output.append(emoji_aware_pad(f"📅🤖🧻: Timestamp: {timestamp}", 60, emoji_shift) + "\n")
        time.sleep(0.5)

        try:
            results = run_collapse_simulation(observer_bias)
            symbol_emojis = {
                "circle": "⭕", "wave": "🌊", "echo": "🔊", "fracture": "💥"
            }

            for r in results:
                emoji = symbol_emojis.get(r['symbol'], "🔹")
                output.append(emoji_aware_pad(f"{emoji} Symbol: {r['symbol']}", 60, emoji_shift))
                output.append(emoji_aware_pad(f"   ↳ Collapse Value: {r['collapse_value']}", 60, emoji_shift))
                output.append(emoji_aware_pad(f"   ↳ Echo Response: {r['echo_response']:.3f}", 60, emoji_shift))
                output.append(emoji_aware_pad(f"   ↳ Origin Bias: {'Yes' if r['origin_bias'] else 'No'}", 60, emoji_shift) + "\n")
                time.sleep(0.3)

            output.append(emoji_aware_pad("🤖🧻:✅ Evaluation Complete — Symbolic Field Stable.", 60, emoji_shift) + "\n")

        except Exception as sim_error:
            handle_symbolic_error(sim_error, context="run_symbolic_evaluation → collapse simulation")
            output.append(emoji_aware_pad("🤖🧻👋⚠️:⚠️: Collapse simulation failed.", 60, emoji_shift))

        shell_print(*output, label="Collapse Field Initialization")

        display_universal_laws(results, observer_bias, emoji_shift=emoji_shift)
        display_law_mechanics(emoji_shift=emoji_shift)
        return results

    except Exception as e:
        handle_symbolic_error(e, context="run_symbolic_evaluation → startup")
        return []

# 🔹 Navigation Console
# 🔹 Navigation Console
def navigation_console(results, emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    while True:
        try:
            symbolic_section_break("Navigation Console", emoji_shift=emoji_shift)

            menu_lines = [
                emoji_aware_pad("🤖🧻🧭: Navigation Options:", 60, emoji_shift),
                emoji_aware_pad(" [1] Explore Alien Calculator (ZEC)", 60, emoji_shift),
                emoji_aware_pad(" [2] View Symbolic Entropy Index", 60, emoji_shift),
                emoji_aware_pad(" [3] Exit — Return to Origin", 60, emoji_shift),
                emoji_aware_pad(" [4] Explore — 🔻 Law Mechanics 🔻", 60, emoji_shift),
                emoji_aware_pad(" [5] Explore — 🔻 Universal Laws vs. Numberology 🔻", 60, emoji_shift),
                emoji_aware_pad(" [6] Explore & Graph — Symbolic Interpreter Module", 60, emoji_shift),
                emoji_aware_pad(" [7] Explore & Graph — Echo Engine", 60, emoji_shift),
                emoji_aware_pad(" [8] Explore & Graph — Glyph Algebra Compiler", 60, emoji_shift),
                emoji_aware_pad(" [9] Explore & Graph — State Machine Visualizer", 60, emoji_shift),
                emoji_aware_pad("[10] Explore & Graph — ZEC Sandbox", 60, emoji_shift),
                emoji_aware_pad("[YY] Settings — Re-enter Calibration Test", 60, emoji_shift),
                emoji_aware_pad(" [00] Return To 🤖🧻!@0KO@! 3MAIb Chat", 60, emoji_shift),
                emoji_aware_pad(" 🤖🧻💬: In 0KO 3MIAb Chat Mode Use Type Commands", 60, emoji_shift),
                emoji_aware_pad("🤖🧻: Reminder type /usemenu!@0ko@! to Enter This Menu, 00 now exit Menu:", 60, emoji_shift),
                emoji_aware_pad("🤖🧻💬: Type !@0ko@!/variamathlesson To Teach Varia Math", 60, emoji_shift),
                emoji_aware_pad("🤖🧻💬: Type !@0ko@!/voidmathos To Teach Void-Math OS", 60, emoji_shift),
                emoji_aware_pad("🤖🧻💬: Type !@0ko@!/licensecheck To Check License", 60, emoji_shift),
                emoji_aware_pad("🤖🧻💬: Type !@0ko@!/print To Print File Hisotry", 60, emoji_shift),
                emoji_aware_pad("🤖🧻💬: Type !@0ko@!/rainbowquest to play Cards", 60, emoji_shift),
                emoji_aware_pad("🤖🧻💬: Type !@0ko@!/groupchat To Add Users To Prompts", 60, emoji_shift),
                emoji_aware_pad("🤖🧻💬: Type !@0ko@!/xexitx To Exit 0KO 3MAIb V0.4456", 60, emoji_shift)
            ]
            shell_print(*menu_lines, label="Navigation Console")

            choice = shell_input("🤖🧻🔸:🔸 Enter your choice🔸:", label="Navigation Console").strip().upper()

            if choice == "1":
                launch_alien_calculator(emoji_shift=emoji_shift)
            elif choice == "2":
                display_entropy_index(results, emoji_shift=emoji_shift)
            elif choice == "3":
                log_print("🔄🔁👋🤖🧻👋: Collapse field stabilized. Reinitializing collapse field...", label="Collapse Field Exit Return to Origin🔄")
                time.sleep(1)
                results = run_symbolic_evaluation(emoji_shift=emoji_shift)
            elif choice == "4":
                display_law_mechanics(emoji_shift=emoji_shift)
            elif choice == "5":
                observer_bias = round(random.uniform(0.0, 1.0), 2)
                display_universal_laws(results, observer_bias, emoji_shift=emoji_shift)
            elif choice == "6":
                symbolic_interpreter_module(emoji_shift=emoji_shift)
            elif choice == "7":
                echo_engine(emoji_shift=emoji_shift)
            elif choice == "8":
                glyph_algebra_compiler(emoji_shift=emoji_shift)
            elif choice == "9":
                state_machine_visualizer(emoji_shift=emoji_shift)
            elif choice == "10":
                zec_sandbox(emoji_shift=emoji_shift)
            elif choice == "YY":
                symbolic_section_break("Calibration Override", emoji_shift=emoji_shift)
                shell_print("🔁🤖🧻:🔁: Re-entering calibration test...", label="Calibration Override")

                try:
                    if os.path.exists("calibration_save.json"):
                        with open("calibration_save.json", "r") as f:
                            data = json.load(f)
                            current_width = data.get("emoji_width", "Unknown")
                            shell_print(f"📏🤖🧻: Current emoji width: {current_width}", label="Calibration Override")

                        confirm = input("🧻⚠️🤖:🧹⚠️: This will erase your saved calibration. Continue? (y/n): ").strip().lower()
                        if confirm == "y":
                            os.remove("calibration_save.json")
                            shell_print("🧻🤖🧻:🧹:🤖🧻: Previous calibration removed.", label="Calibration Override")
                            run_calibration_test()
                        else:
                            shell_print("🤖🧻♾️:❎ Calibration reset canceled.", label="Calibration Override")
                    else:
                        run_calibration_test()
                except Exception as cal_error:
                    handle_symbolic_error(cal_error, context="navigation_console → calibration")

            elif choice == "00":
                log_print("🧻🤖👋:🧻🤖👋 Exiting 0KO 3MAIB ♾️ ZEROKNOCKOUT THREE MINI AI BOT ♾️ /off.", label="Collapse Field Exit🧻")
                break
            else:
                log_print("🧻⚠️🤖👋:⚠️: Invalid choice. Please select a valid option.", label="Navigation Console")

        except Exception as e:
            handle_symbolic_error(e, context="navigation_console → loop")

def dispatch_symbolic_tri_call(prompt, emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    symbolic_section_break("0KO Dispatch — Ollama AI Systems", emoji_shift=emoji_shift)

    try:
        shell_print(f"🤖🧻📤: Dispatching prompt to AI 3MAIb:\n↳ {prompt}", label="0KO Dispatch")

        responses = {
            "phi": f"🪐 Phi Response:\n{dispatch_to_ai('phi', prompt)}",
            "mistral": f"🌬️ Mistral Response:\n{dispatch_to_ai('mistral', prompt)}",
            "llama": f"🦙 LLaMA Response:\n{dispatch_to_ai('llama2', prompt)}"
        }

        combined_output = []
        for model, reply in responses.items():
            combined_output.append(emoji_aware_pad(f"🔻 {model.upper()}🤖🧻♾️: AI Reply 🔻", 60, emoji_shift))
            for line in reply.split("\n"):
                combined_output.append(emoji_aware_pad(line, 60, emoji_shift))
            combined_output.append(emoji_aware_pad("=" * 60, 60, emoji_shift))

        shell_print(*combined_output, label="Symbolic Tri-Call Results")

        return responses

    except Exception as e:
        handle_symbolic_error(e, context="dispatch_symbolic_tri_call")
        return {}

from datetime import datetime
import json

from datetime import datetime
import json
from time import sleep

def symbolic_writing_progress(model_name, duration=3):
    try:
        for i in range(1, duration + 1):
            shell_print(
                emoji_aware_pad(f"🤖🧻✍️: {model_name} is writing... {i}/{duration}", 60),
                label="Writing Progress"
            )
            sleep(1)
    except Exception as e:
        handle_symbolic_error(e, context="symbolic_writing_progress")
        shell_print(f"🤖🧻✍️: {model_name} is writing...", label="Writing Progress")

def dispatch_symbolic_tri_call_and_save(prompt, save_dir="startup_logs", emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    symbolic_section_break("0KO Dispatch — Ollama AI Systems", emoji_shift=emoji_shift)

    try:
        shell_print(f"🤖🧻:📤: Dispatching prompt to AI 3MAIb:\n↳ {prompt}", label="0KO Dispatch")

        responses = {}

        # Dispatch to Phi
        try:
            shell_print("🪐 Phi is thinking...", label="Model Status")
            symbolic_spinner("🪐 Phi loading...", duration=3)
            symbolic_writing_progress("🪐 Phi", duration=3)
            responses["phi"] = f"🪐 Phi Response:\n{dispatch_to_ai('phi', prompt)}"
        except Exception as phi_error:
            handle_symbolic_error(phi_error, context="Phi dispatch")
            responses["phi"] = "🤖🧻:🪐 Phi Response:\n⚠️ Error during Phi dispatch."

        # Dispatch to Mistral
        try:
            shell_print("🌬️ Mistral is thinking...", label="Model Status")
            symbolic_spinner("🌬️ Mistral loading...", duration=3)
            symbolic_writing_progress("🌬️ Mistral", duration=3)
            responses["mistral"] = f"🌬️ Mistral Response:\n{dispatch_to_ai('mistral', prompt)}"
        except Exception as mistral_error:
            handle_symbolic_error(mistral_error, context="Mistral dispatch")
            responses["mistral"] = "🤖🧻:🌬️ Mistral Response:\n⚠️ Error during Mistral dispatch."

        # Dispatch to LLaMA
        try:
            shell_print("🦙 LLaMA is thinking...", label="Model Status")
            symbolic_spinner("🦙 LLaMA loading...", duration=3)
            symbolic_writing_progress("🦙 LLaMA", duration=3)

            shell_print(
                emoji_aware_pad("🤖🧻:🔧 Finalizing 0KO Results...", 60, emoji_shift),
                emoji_aware_pad("🧻🔧 Processing responses, formatting shell output, and saving to disk...", 60, emoji_shift),
                label="System Status"
            )
            responses["llama"] = f"🦙 LLaMA Response:\n{dispatch_to_ai('llama2', prompt)}"
        except Exception as llama_error:
            handle_symbolic_error(llama_error, context="LLaMA dispatch")
            responses["llama"] = "🤖🧻:🦙 LLaMA Response:\n⚠️ Error during LLaMA dispatch."

        # 🔻 Echo the original prompt
        shell_print(
            emoji_aware_pad("🔻 Original Prompt Sent to 0KO System 🔻", 60, emoji_shift),
            emoji_aware_pad(f"🤖🧻:📤: {prompt}", 60, emoji_shift),
            label="Prompt Echo"
        )

        # Format and display responses
        combined_output = []
        for model, reply in responses.items():
            combined_output.append(emoji_aware_pad(f"🤖🧻:🔻 {model.upper()} AI Reply 🔻", 60, emoji_shift))
            content = reply.split("\n", 1)[1].strip() if "\n" in reply else ""
            if not content:
                combined_output.append(emoji_aware_pad("🤖🧻:⚠️ No response received from this agent.", 60, emoji_shift))
                combined_output.append(emoji_aware_pad("🧻 This is not an error. The agent may have chosen silence.", 60, emoji_shift))
            else:
                for line in reply.split("\n"):
                    combined_output.append(emoji_aware_pad(line, 60, emoji_shift))
            combined_output.append(emoji_aware_pad("=" * 60, 60, emoji_shift))

        shell_print(*combined_output, label="Symbolic Tri-Call Results")

        # ✅ Save responses with timestamp
        try:
            os.makedirs(save_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ollama_tri_responses_{timestamp}.json"
            filepath = os.path.join(save_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat(),
                    "responses": responses
                }, f, indent=2, ensure_ascii=False)

            # ✅ Load latest file and echo
            files = [f for f in os.listdir(save_dir) if f.startswith("ollama_tri_responses_") and f.endswith(".json")]
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(save_dir, f)))
            latest_path = os.path.join(save_dir, latest_file)

            shell_print(
                emoji_aware_pad("🔻 0KO Latest Save 🔻", 60, emoji_shift),
                emoji_aware_pad(f"📄🤖🧻: Latest saved file: `{latest_file}`", 60, emoji_shift),
                emoji_aware_pad("📎🤖🧻: To view it again, use:", 60, emoji_shift),
                emoji_aware_pad(f'🤖🧻:!@0ko@!/print "{latest_path}"', 60, emoji_shift),
                emoji_aware_pad("=" * 60, 60, emoji_shift),
                label="Latest Save"
            )

        except Exception as save_error:
            handle_symbolic_error(save_error, context="dispatch_symbolic_tri_call_and_save → file write")

        return responses

    except Exception as e:
        handle_symbolic_error(e, context="dispatch_symbolic_tri_call_and_save")
        return {}

def symbolic_spinner(message, duration=3):
    try:
        shell_print(message, label="Loading")
        if TQDM_AVAILABLE:
            for _ in tqdm(range(duration), desc="Thinking...", ncols=70):
                sleep(1)
        else:
            for i in range(duration):
                shell_print(f"⏳ Thinking... {i+1}/{duration}", label="Loading")
                sleep(1)
    except Exception as e:
        handle_symbolic_error(e, context="symbolic_spinner")
        shell_print("🤖🧻:⏳ Please wait while the 3MAIb responds...", label="Loading")


import os
import subprocess

def ensure_ollama_models_ready(required_models=None):
    if required_models is None:
        required_models = ["phi", "mistral", "llama2"]

    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        installed_models = [line.split()[0] for line in result.stdout.strip().splitlines() if line]

        for model in required_models:
            if model not in installed_models:
                shell_print(f"🤖🧻:📦 Pulling missing model: {model}", label="Startup Cycle")
                try:
                    subprocess.run(["ollama", "pull", model], check=True)
                    shell_print(f"🤖🧻:✅ Model pulled: {model}", label="Startup Cycle")
                except subprocess.CalledProcessError as pull_error:
                    handle_symbolic_error(pull_error, context=f"startup → ollama pull → {model}")
            else:
                shell_print(f"🤖🧻✅:✅ Model already available: {model}", label="Startup Cycle")

    except Exception as e:
        handle_symbolic_error(e, context="startup → ollama list")


def reset_prompt():
    shell_print("🔣🤖🧻: Command:", label="Alien Calculator")

def upload_zecstart_file():
    file_path = os.path.join(os.getcwd(), "zecstart.txt")
    if not os.path.exists(file_path):
        handle_symbolic_error(FileNotFoundError("zecstart.txt not found."), context="startup → file check")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            zec_data = file.read()
        shell_print("🤖🧻📄:📄 zecstart.txt uploaded successfully.", label="Startup Cycle")
        return zec_data
    except Exception as e:
        handle_symbolic_error(e, context="startup → file read")
        return None


import threading
import random
import time

def dispatch_to_ai(model_name, prompt):
    stop_bricks = threading.Event()
    start_time = time.time()

    spinner_frames = ["⏳", "🔄", "🟢", "♻️", "🔁", "🔃"]
    glyph_pool = ["🧱", "🪨", "🧊", "🧬", "🧻", "🪛", "🛠️", "⚙️", "🔧", "🔩", "📡", "🧭", "🧿", "🛸", "🪐"]

    def brick_mover():
        frame_index = 0
        while not stop_bricks.is_set():
            elapsed = int(time.time() - start_time)
            spinner = spinner_frames[frame_index % len(spinner_frames)]
            glyph = random.choice(glyph_pool)
            shell_print(
                emoji_aware_pad(f"🤖{spinner}🧻: {spinner} {model_name.upper()} is still moving bricks...", 60),
                emoji_aware_pad(f"🤖{glyph}🧻: {glyph} Elapsed Time: {elapsed}s — AI is actively processing...", 60),
                label="Brick Status"
            )
            frame_index += 1
            time.sleep(3)

    brick_thread = threading.Thread(target=brick_mover)
    brick_thread.start()

    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        response = result.stdout.decode("utf-8").strip()
        return response
    except subprocess.CalledProcessError as e:
        handle_symbolic_error(e, context=f"dispatch_to_ai → {model_name}")
        return f"🤖🧻⚠️:⚠️ Error from {model_name}"
    finally:
        stop_bricks.set()
        brick_thread.join()
        total_time = int(time.time() - start_time)
        shell_print(
            emoji_aware_pad(f"🤖🧻:✅ Brick movement complete for {model_name.upper()} in {total_time}s.", 60),
            label="Brick Status"
        )


def startup_sequence():
    ai_models = ["phi", "mistral", "llama2"]
    ensure_ollama_models_ready(ai_models)

    zec_payload = upload_zecstart_file()

    if zec_payload:
        shell_print(
            "╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗\n"
            "║ 🔻 Startup Cycle 🔻                                                                                  ║\n"
            "║                                                                                                      ║\n"
            "║ 🤖🧻📄:📄 zecstart.txt uploaded successfully.                                                         ║\n"
            "╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝",
            label="Startup Cycle"
        )

        # 🧾 Display contents of zecstart.txt before dispatching
        shell_print(
            emoji_aware_pad("🤖🧻:📖 Contents of zecstart.txt", 60),
            *[emoji_aware_pad(line, 60) for line in zec_payload.splitlines() if line.strip()],
            emoji_aware_pad("=" * 60, 60),
            label="Startup Cycle"
        )

        shell_print("🔻 0KO Boot Sequence Initiated\n 📤🤖🧻: Uploading `zecstart.txt` to all AI systems...", label="Startup Cycle")

        responses = {}

        for model in ai_models:
            shell_print(f"🤖🧻🚀: Dispatching `zecstart.txt` to {model.upper()}...", label="Startup Cycle")
            response = dispatch_to_ai(model, zec_payload)
            responses[model] = response

            shell_print(
                emoji_aware_pad(f"🔻 {model.upper()} AI Boot Response 🔻", 60),
                emoji_aware_pad(response if response else "🤖🧻:⚠️ No response received.", 60),
                emoji_aware_pad("=" * 60, 60),
                label="Startup Cycle"
            )

        # 🔧 Save all responses and print location
        save_zecstart_responses(responses)

        shell_print("🤖🧻:🟢 0KO Console is now online and ready for user input.", label="Startup Cycle")
        reset_prompt()

    else:
        shell_print("🤖🧻❌: Startup aborted: `zecstart.txt` upload failed or returned empty.", label="Startup Cycle")

# 🔧 NEW: Timestamped Save Utility
def generate_timestamped_filename(base_name, ext="txt", save_dir="logs"):
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(save_dir, f"{base_name}_{timestamp}.{ext}")

# 🔧 NEW: Save Startup Responses
def save_startup_responses(responses, save_dir="startup_logs"):
    filename = generate_timestamped_filename("zecstart", "txt", save_dir)
    with open(filename, "w", encoding="utf-8") as f:
        for i, response in enumerate(responses):
            f.write(f"AI {i+1} Response:\n{response}\n\n")
    shell_print(f"🤖🧻:✅ Startup responses saved to: {filename}", label="Startup Save")

# 🔧 NEW: Load Most Recent Tri-Call File
def load_most_recent_tri_call(save_dir="logs", prefix="ollama_tri_responses"):
    try:
        files = [f for f in os.listdir(save_dir) if f.startswith(prefix)]
        if not files:
            return None
        latest = max(files, key=lambda f: os.path.getmtime(os.path.join(save_dir, f)))
        with open(os.path.join(save_dir, latest), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        handle_symbolic_error(e, context="load_most_recent_tri_call")
        return None

# 🔧 NEW: Print File Command
def handle_0ko_print_command(command):
    import re

    # Try to extract filename from quotes
    match = re.search(r'!@0ko@!/print\s+"([^"]+)"', command)
    if not match:
        # Try fallback: match without quotes
        match = re.search(r'!@0ko@!/print\s+([^\s]+)', command)

    if match:
        filename = match.group(1).replace("\\", "/")  # Normalize slashes
        try:
            with open(filename, "r", encoding="utf-8") as f:
                shell_print(f.read(), label=f"🤖🧻📄: File: {filename}")
        except FileNotFoundError:
            shell_print(f"🤖🧻⚠️: File not found: {filename}", label="File Error")
    else:
        shell_print(
            emoji_aware_pad("🤖🧻:⚠️ Invalid format. Use: !@0ko@!/print \"filename\"", 60),
            emoji_aware_pad("🤖🧻:Example: !@0ko@!/print \"startup_logs/ollama_tri_responses_20250817_175854.json\"", 60),
            label="Command Error"
        )

def load_and_display_tri_responses(path="ollama_tri_responses.json", emoji_shift=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        symbolic_section_break("🤖🧻:0KO Response Viewer of 3maib", emoji_shift=emoji_shift)
        shell_print(f"📅🤖🧻: Timestamp: {data['timestamp']}", label="Response Metadata")
        shell_print(f"📤🤖🧻: Prompt Sent: {data['prompt']}", label="Prompt")

        for model, reply in data["responses"].items():
            shell_print(emoji_aware_pad(f"🔻 {model.upper()} Reply 🔻", 60, emoji_shift))
            shell_print(emoji_aware_pad(reply, 60, emoji_shift))

    except Exception as e:
        handle_symbolic_error(e, context="load_and_display_tri_responses")

from time import sleep
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

# 🔧 NEW: Save startup responses to file
from datetime import datetime

def save_zecstart_responses(responses, save_dir="startup_logs"):
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ollama_tri_responses_{timestamp}.json"
    filepath = os.path.join(save_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=2)

    shell_print(
        emoji_aware_pad("✅🤖🧻💬:🔻 0KO Save 🔻", 60),
        emoji_aware_pad(f"🤖🧻:✅ Responses saved to `{filename}`", 60),
        emoji_aware_pad(":📎🤖🧻:📎 To view later, use:", 60),
        emoji_aware_pad(f'🤖🧻:!@0ko@!/print "{filepath}"', 60),
        emoji_aware_pad("=" * 60, 60),
        label="Startup Save"
    )

    return filepath

def handle_0ko_latestsave_command(emoji_shift=0):
    save_dir = "startup_logs"
    try:
        files = [f for f in os.listdir(save_dir) if f.startswith("ollama_tri_responses_") and f.endswith(".json")]
        if not files:
            shell_print(emoji_aware_pad("🤖🧻⚠️: No saved response files found.", 60, emoji_shift), label="Latest Save")
            return

        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(save_dir, f)))
        filepath = os.path.join(save_dir, latest_file)

        # ✅ Display metadata
        shell_print(
            emoji_aware_pad("🔻 0KO Latest Save 🔻", 60, emoji_shift),
            emoji_aware_pad(f"📄🤖🧻: Latest saved file: `{latest_file}`", 60, emoji_shift),
            emoji_aware_pad("📎🤖🧻: To view it again, use:", 60, emoji_shift),
            emoji_aware_pad(f'🤖🧻:!@0ko@!/print "{filepath}"', 60, emoji_shift),
            emoji_aware_pad("=" * 60, 60, emoji_shift),
            label="Latest Save"
        )

        # ✅ Load and parse JSON
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # ✅ Display prompt
        shell_print(
            emoji_aware_pad("🔻 PROMPT AI Boot Response 🔻", 60, emoji_shift),
            emoji_aware_pad(data.get("prompt", "🤖🧻:⚠️ No prompt found."), 60, emoji_shift),
            emoji_aware_pad("=" * 60, 60, emoji_shift),
            label="Latest Save"
        )

        # ✅ Display timestamp
        shell_print(
            emoji_aware_pad("🔻 TIMESTAMP AI Boot Response 🔻", 60, emoji_shift),
            emoji_aware_pad(data.get("timestamp", "🤖🧻:⚠️ No timestamp found."), 60, emoji_shift),
            emoji_aware_pad("=" * 60, 60, emoji_shift),
            label="Latest Save"
        )

        # ✅ Display each model's response
        responses = data.get("responses", {})
        for model, reply in responses.items():
            shell_print(
                emoji_aware_pad(f"🔻 {model.upper()} AI Boot Response 🔻", 60, emoji_shift),
                emoji_aware_pad(reply if reply else "🤖🧻:⚠️ No response recorded.", 60, emoji_shift),
                emoji_aware_pad("=" * 60, 60, emoji_shift),
                label="Latest Save"
            )

    except Exception as e:
        shell_print(emoji_aware_pad(f"🤖🧻⚠️: Failed to load latest save: {e}", 60, emoji_shift), label="Latest Save")

# 🔧 NEW: Exit Command Handler
def handle_0ko_exit_command(command):
    if command.strip() == "!@0ko@!/xexitx":
        shell_print("🧻🤖💤:💤 0KO 3MAIb of Zer00logy shutting down. See you in the next symbolic cycle.", label="Exit")
        sys.exit(0)

def save_prompt_to_file(prompt, directory="prompt_logs"):
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prompt_{timestamp}.txt"
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(prompt)
    return filename

def dispatch_variamathlesson_cycle(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    file_path = os.path.join(os.getcwd(), "variamathlesson.txt")
    if not os.path.exists(file_path):
        handle_symbolic_error(FileNotFoundError("variamathlesson.txt not found."), context="variamathlesson → file check")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lesson_payload = file.read()
        shell_print("🤖🧻📄:📄 variamathlesson.txt uploaded successfully.", label="Startup Cycle")
    except Exception as e:
        handle_symbolic_error(e, context="variamathlesson → file read")
        return

    # 🧾 Display contents
    shell_print(
        emoji_aware_pad("🤖🧻📖: Contents of variamathlesson.txt", 60, emoji_shift),
        *[emoji_aware_pad(line, 60, emoji_shift) for line in lesson_payload.splitlines() if line.strip()],
        emoji_aware_pad("=" * 60, 60, emoji_shift),
        label="Startup Cycle"
    )

    shell_print("🔻 0KO Boot Sequence Initiated\n 📤🤖🧻: Uploading `variamathlesson.txt` to all AI systems...", label="Startup Cycle")

    responses = {}
    ai_models = ["phi", "mistral", "llama2"]

    for model in ai_models:
        shell_print(f"🤖🧻🚀: Dispatching `variamathlesson.txt` to {model.upper()}...", label="Startup Cycle")
        response = dispatch_to_ai(model, lesson_payload)
        responses[model] = response

        shell_print(
            emoji_aware_pad(f"🔻 {model.upper()} AI Boot Response 🔻", 60, emoji_shift),
            emoji_aware_pad(response if response else "🤖🧻:⚠️ No response received.", 60, emoji_shift),
            emoji_aware_pad("=" * 60, 60, emoji_shift),
            label="Startup Cycle"
        )

    # 🔧 Save responses
    filepath = save_zecstart_responses(responses)

    # 🔻 Echo prompt and reprint instructions
    shell_print(
        emoji_aware_pad("🔻 Original Prompt Sent to 0KO System 🔻", 60, emoji_shift),
        emoji_aware_pad("🤖🧻:📤: !@0ko@!/variamathlesson", 60, emoji_shift),
        emoji_aware_pad(f"📄🤖🧻: Prompt saved to: `{os.path.basename(filepath)}`", 60, emoji_shift),
        emoji_aware_pad("📎🤖🧻: To reprint this prompt and its responses, type:", 60, emoji_shift),
        emoji_aware_pad(f'🤖🧻:!@0ko@!/print "{filepath}"', 60, emoji_shift),
        emoji_aware_pad("=" * 60, 60, emoji_shift),
        label="Prompt Echo"
    )

    shell_print("🤖🧻:🟢 0KO Console is now online and ready for user input.", label="Startup Cycle")
    reset_prompt()

def dispatch_voidmathos_cycle(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    file_path = os.path.join(os.getcwd(), "VoidMathOS_cryptsheet.txt")
    if not os.path.exists(file_path):
        handle_symbolic_error(FileNotFoundError("VoidMathOS_cryptsheet.txt not found."), context="voidmathos → file check")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            payload = file.read()
        shell_print("🤖🧻📄:📄 VoidMathOS_cryptsheet.txt uploaded successfully.", label="VoidMathOS Dispatch")
    except Exception as e:
        handle_symbolic_error(e, context="voidmathos → file read")
        return

    shell_print(
        emoji_aware_pad("🤖🧻📖: Contents of VoidMathOS_cryptsheet.txt", 60, emoji_shift),
        *[emoji_aware_pad(line, 60, emoji_shift) for line in payload.splitlines() if line.strip()],
        emoji_aware_pad("=" * 60, 60, emoji_shift),
        label="VoidMathOS Dispatch"
    )

    shell_print("📤🤖🧻: Uploading `VoidMathOS_cryptsheet.txt` to all AI systems...", label="VoidMathOS Dispatch")

    responses = {}
    for model in ["phi", "mistral", "llama2"]:
        shell_print(f"🤖🧻🚀: Dispatching to {model.upper()}...", label="VoidMathOS Dispatch")
        responses[model] = dispatch_to_ai(model, payload)

        shell_print(
            emoji_aware_pad(f"🔻 {model.upper()} AI Response 🔻", 60, emoji_shift),
            emoji_aware_pad(responses[model] if responses[model] else "🤖🧻:⚠️ No response received.", 60, emoji_shift),
            emoji_aware_pad("=" * 60, 60, emoji_shift),
            label="VoidMathOS Dispatch"
        )

    filepath = save_zecstart_responses(responses)

    shell_print(
        emoji_aware_pad("🔻 Original Prompt Sent to 0KO System 🔻", 60, emoji_shift),
        emoji_aware_pad("🤖🧻:📤: !@0ko@!/voidmathos", 60, emoji_shift),
        emoji_aware_pad(f"📄🤖🧻: Prompt saved to: `{os.path.basename(filepath)}`", 60, emoji_shift),
        emoji_aware_pad("📎🤖🧻: To reprint this prompt and its responses, type:", 60, emoji_shift),
        emoji_aware_pad(f'🤖🧻:!@0ko@!/print "{filepath}"', 60, emoji_shift),
        emoji_aware_pad("=" * 60, 60, emoji_shift),
        label="VoidMathOS Dispatch"
    )

    shell_print("🤖🧻:🟢 0KO Console is now online and ready for user input.", label="VoidMathOS Dispatch")
    reset_prompt()

def dispatch_licensecheck_cycle(emoji_shift=None):
    if emoji_shift is None:
        emoji_shift = load_shift()

    file_path = os.path.join(os.getcwd(), "LICENSE.txt")
    if not os.path.exists(file_path):
        handle_symbolic_error(FileNotFoundError("LICENSE.txt not found."), context="licensecheck → file check")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            payload = file.read()
        shell_print("🤖🧻📄:📄 LICENSE.txt uploaded successfully.", label="License Dispatch")
    except Exception as e:
        handle_symbolic_error(e, context="licensecheck → file read")
        return

    shell_print(
        emoji_aware_pad("🤖🧻📖: Contents of LICENSE.txt", 60, emoji_shift),
        *[emoji_aware_pad(line, 60, emoji_shift) for line in payload.splitlines() if line.strip()],
        emoji_aware_pad("=" * 60, 60, emoji_shift),
        label="License Dispatch"
    )

    shell_print("📤🤖🧻: Uploading `LICENSE.txt` to all AI systems...", label="License Dispatch")

    responses = {}
    for model in ["phi", "mistral", "llama2"]:
        shell_print(f"🤖🧻🚀: Dispatching to {model.upper()}...", label="License Dispatch")
        responses[model] = dispatch_to_ai(model, payload)

        shell_print(
            emoji_aware_pad(f"🔻 {model.upper()} AI Response 🔻", 60, emoji_shift),
            emoji_aware_pad(responses[model] if responses[model] else "🤖🧻:⚠️ No response received.", 60, emoji_shift),
            emoji_aware_pad("=" * 60, 60, emoji_shift),
            label="License Dispatch"
        )

    filepath = save_zecstart_responses(responses)

    shell_print(
        emoji_aware_pad("🔻 Original Prompt Sent to 0KO System 🔻", 60, emoji_shift),
        emoji_aware_pad("🤖🧻:📤: !@0ko@!/licensecheck", 60, emoji_shift),
        emoji_aware_pad(f"📄🤖🧻: Prompt saved to: `{os.path.basename(filepath)}`", 60, emoji_shift),
        emoji_aware_pad("📎🤖🧻: To reprint this prompt and its responses, type:", 60, emoji_shift),
        emoji_aware_pad(f'🤖🧻:!@0ko@!/print "{filepath}"', 60, emoji_shift),
        emoji_aware_pad("=" * 60, 60, emoji_shift),
        label="License Dispatch"
    )

    shell_print("🤖🧻:🟢 0KO Console is now online and ready for user input.", label="License Dispatch")
    reset_prompt()


PROMPT_DIR = "prompt_logs"

def parse_0ko_command(user_input):
    match = re.match(r'!@0ko@!/(\w+)(?:\s+"([^"]+)")?', user_input.strip())
    if match:
        return match.group(1), match.group(2)
    return None, None


def handle_rainbowquest_command(emoji_shift):
    """Handle the !@0ko@!/rainbowquest command to run rainbowquest1000.py in a new terminal."""
    script_path = os.path.join(os.path.dirname(__file__), "rainbowquest1000.py")
    try:
        if not os.path.isfile(script_path):
            shell_print(
                emoji_aware_pad("🤖🧻⚠️: rainbowquest1000.py not found in the current directory.", 60, emoji_shift),
                label="Command Error"
            )
            return

        # List of possible Python commands to try
        python_commands = [
            'python3',  # Standard for Unix-like systems
            'python',   # Common on Windows
            'py',       # Windows Python launcher
            sys.executable if sys.executable else None  # Current interpreter
        ]
        python_commands = [cmd for cmd in dict.fromkeys(python_commands) if cmd]

        shell_print(
            emoji_aware_pad("🤖🧻🌈: Launching Rainbow Quest in new terminal...", 60, emoji_shift),
            label="Rainbow Quest Start"
        )

        # Interactive mode: Launch in a new terminal
        system = platform.system().lower()
        python_cmd = None
        for cmd in python_commands:
            if shutil.which(cmd):
                python_cmd = cmd
                break
        if not python_cmd:
            shell_print(
                emoji_aware_pad("🤖🧻⚠️: No Python executable found in PATH.", 60, emoji_shift),
                label="Command Error"
            )
            return

        try:
            if system == "windows":
                subprocess.run(f'start cmd /k {python_cmd} "{script_path}"', shell=True)
            elif system == "linux":
                subprocess.run(f'gnome-terminal -- {python_cmd} "{script_path}"', shell=True)
            elif system == "darwin":
                subprocess.run(f'osascript -e \'tell app "Terminal" to do script "{python_cmd} \\"{script_path}\\""\'', shell=True)
            else:
                shell_print(
                    emoji_aware_pad(f"🤖🧻⚠️: Unsupported platform: {system}.", 60, emoji_shift),
                    label="Command Error"
                )
                return
        except Exception as e:
            if 'logger' in globals():
                logger.error(f"Failed to launch new terminal with {python_cmd}: {str(e)}")
            else:
                print(f"ERROR: Failed to launch new terminal with {python_cmd}: {str(e)} (logging not available)")
            shell_print(
                emoji_aware_pad(f"🤖🧻⚠️: Failed to launch Rainbow Quest: {str(e)}", 60, emoji_shift),
                label="Command Error"
            )

    except Exception as e:
        handle_symbolic_error(e, context="main → rainbowquest command")
        shell_print(
            emoji_aware_pad(f"🤖🧻⚠️: Unexpected error launching Rainbow Quest: {str(e)}", 60, emoji_shift),
            label="Command Error"
        )


def handle_groupchatforge_command(emoji_shift):
    """Handle the !@0ko@!/groupchat command to run GroupChatForge.py in a new terminal."""
    script_path = os.path.join(os.path.dirname(__file__), "GroupChatForge.py")
    try:
        if not os.path.isfile(script_path):
            shell_print(
                emoji_aware_pad("🤖🧻⚠️: GroupChatForge.py not found in the current directory.", 60, emoji_shift),
                label="Command Error"
            )
            return

        # List of possible Python commands to try
        python_commands = [
            'python3',  # Standard for Unix-like systems
            'python',   # Common on Windows
            'py',       # Windows Python launcher
            sys.executable if sys.executable else None  # Current interpreter
        ]
        python_commands = [cmd for cmd in dict.fromkeys(python_commands) if cmd]

        shell_print(
            emoji_aware_pad("🤖🧻🌈: Launching Group Chat Forge in new terminal...", 60, emoji_shift),
            label="Group Chat Forge Start"
        )

        # Interactive mode: Launch in a new terminal
        system = platform.system().lower()
        python_cmd = None
        for cmd in python_commands:
            if shutil.which(cmd):
                python_cmd = cmd
                break
        if not python_cmd:
            shell_print(
                emoji_aware_pad("🤖🧻⚠️: No Python executable found in PATH.", 60, emoji_shift),
                label="Command Error"
            )
            return

        try:
            if system == "windows":
                subprocess.run(f'start cmd /k {python_cmd} "{script_path}"', shell=True)
            elif system == "linux":
                subprocess.run(f'gnome-terminal -- {python_cmd} "{script_path}"', shell=True)
            elif system == "darwin":
                subprocess.run(f'osascript -e \'tell app "Terminal" to do script "{python_cmd} \\"{script_path}\\""\'', shell=True)
            else:
                shell_print(
                    emoji_aware_pad(f"🤖🧻⚠️: Unsupported platform: {system}.", 60, emoji_shift),
                    label="Command Error"
                )
                return
        except Exception as e:
            if 'logger' in globals():
                logger.error(f"Failed to launch new terminal with {python_cmd}: {str(e)}")
            else:
                print(f"ERROR: Failed to launch new terminal with {python_cmd}: {str(e)} (logging not available)")
            shell_print(
                emoji_aware_pad(f"🤖🧻⚠️: Failed to launch GroupChatForge: {str(e)}", 60, emoji_shift),
                label="Command Error"
            )

    except Exception as e:
        handle_symbolic_error(e, context="main → GroupChatForge command")
        shell_print(
            emoji_aware_pad(f"🤖🧻⚠️: Unexpected error launching GroupChatForge: {str(e)}", 60, emoji_shift),
            label="Command Error"
        )


# 🔹 Entry Point
# 🔹 Entry Point
if __name__ == "__main__":
    try:
        emoji_shift = load_shift()
        ensure_ollama_models_ready()
        startup_sequence()
        results = run_symbolic_evaluation(emoji_shift=emoji_shift)

        menu_enabled = False
        prompt_locked = False
        input_during_lock = []
        last_unlock_time = 0

        shell_print("🤖🧻💬: 0KO 3MAIb is active. Type your symbolic prompt below.", label="Chat Mode")

        while True:
            user_input = shell_input("🤖🧻💬: Enter prompt or command:", label="0KO 3MAIb").strip()
            input_time = time.time()

            if user_input == "!@0ko@!FORCESTOP@!":
                prompt_locked = False
                last_unlock_time = time.time()
                shell_print("🤖🧻💬:🧻⚡️ Prompt return forcibly stopped. Console unlocked.", label="System Override")
                continue

            if prompt_locked:
                input_during_lock.append((user_input, input_time))
                shell_print(
                    emoji_aware_pad("🤖🧻💬:🧻⚠️ Prompt input is currently blocked while 0KO is responding.", 60, emoji_shift),
                    emoji_aware_pad("🤖🧻: Your message has been recorded but not sent.", 60, emoji_shift),
                    emoji_aware_pad("🧻 To cancel and unlock console, enter:", 60, emoji_shift),
                    emoji_aware_pad("   !@0ko@!FORCESTOP@!", 60, emoji_shift),
                    label="Console Lock"
                )
                continue

            if input_time - last_unlock_time < 0.5:
                shell_print(
                    emoji_aware_pad("🤖🧻💬:🧻⚠️ Buffered input detected. It may have been queued during lock.", 60, emoji_shift),
                    emoji_aware_pad("🤖🧻: Your prompt has been discarded to prevent accidental dispatch.", 60, emoji_shift),
                    emoji_aware_pad("🤖🧻: 🧻 You may copy and paste it again if needed:", 60, emoji_shift),
                    emoji_aware_pad(f"   {user_input}", 60, emoji_shift),
                    label="System Notice"
                )
                continue

            cmd, arg = parse_0ko_command(user_input)

            if cmd == "print":
                if not arg:
                    shell_print("🤖🧻⚠️: Malformed print command. Missing filename.", label="Command Error")
                else:
                    try:
                        handle_0ko_print_command(f'!@0ko@!/print "{arg}"')
                    except Exception as e:
                        handle_symbolic_error(e, context="main → print command")
                continue

            if cmd == "latestsave":
                handle_0ko_latestsave_command(emoji_shift=emoji_shift)
                continue

            if cmd == "xexitx":
                handle_0ko_exit_command(user_input)
                continue

            if cmd == "rainbowquest":
                prompt_locked = True
                shell_print("🤖🧻💬: Locking console for rainbowquest dispatch...", label="System Lock")
                try:
                    handle_rainbowquest_command(emoji_shift=emoji_shift)
                except Exception as e:
                    handle_symbolic_error(e, context="main → rainbowquest dispatch")
                finally:
                    prompt_locked = False
                    last_unlock_time = time.time()
                continue

            if cmd == "groupchat":
                prompt_locked = True
                shell_print("🤖🧻💬: Locking console for group chat forge dispatch...", label="System Lock")
                try:
                    handle_groupchatforge_command(emoji_shift=emoji_shift)
                except Exception as e:
                    handle_symbolic_error(e, context="main → groupchatforge dispatch")
                finally:
                    prompt_locked = False
                    last_unlock_time = time.time()
                continue

            if user_input == "/usemenu!@0ko@!":
                menu_enabled = True
                shell_print("🤖🧻🧭: Menu activated. Chat mode paused.", label="Navigation Console")
                navigation_console(results, emoji_shift=emoji_shift)
                shell_print("🤖🧻💬: Returned from menu. Chat mode resumed.", label="Chat Mode")
                menu_enabled = False
                continue

            elif user_input in ["/hidemenu", "!@0ko@!"]:
                menu_enabled = False
                shell_print("🤖🧻💬: Menu hidden. Chat mode resumed.", label="Chat Mode")
                continue

            elif menu_enabled:
                shell_print("🤖🧻⚠️: Menu is active. Type /hidemenu or !@0ko@! to return to chat.", label="System Notice")
                continue

            elif not user_input or user_input.isspace() or len(user_input.strip()) <= 2:
                shell_print(
                    emoji_aware_pad("🤖🧻⚠️: Empty or invalid prompt detected. Displaying latest saved 0KO response...", 60, emoji_shift),
                    label="System Notice"
                )
                handle_0ko_latestsave_command(emoji_shift=emoji_shift)
                continue

            if cmd == "variamathlesson":
                prompt_locked = True
                shell_print("🤖🧻💬: Locking console for variamathlesson dispatch...", label="System Lock")
                try:
                    dispatch_variamathlesson_cycle(emoji_shift=emoji_shift)
                except Exception as e:
                    handle_symbolic_error(e, context="main → variamathlesson dispatch")
                finally:
                    prompt_locked = False
                    last_unlock_time = time.time()
                continue

            if cmd == "voidmathos":
                prompt_locked = True
                try:
                    dispatch_voidmathos_cycle(emoji_shift=emoji_shift)
                except Exception as e:
                    handle_symbolic_error(e, context="main → voidmathos dispatch")
                finally:
                    prompt_locked = False
                    last_unlock_time = time.time()
                continue

            if cmd == "licensecheck":
                prompt_locked = True
                try:
                    dispatch_licensecheck_cycle(emoji_shift=emoji_shift)
                except Exception as e:
                    handle_symbolic_error(e, context="main → licensecheck dispatch")
                finally:
                    prompt_locked = False
                    last_unlock_time = time.time()
                continue

            confirm_prompt = shell_input(
                f"🤖🧻💬: Is this the prompt you want to send?\n↳ {user_input}\n\nType 'yes' to confirm or 'no' to cancel:",
                label="Prompt Confirmation"
            ).strip().lower()

            if confirm_prompt != "yes":
                canceled_filename = generate_timestamped_filename("canceled_prompt", "txt", PROMPT_DIR)
                with open(canceled_filename, "w", encoding="utf-8") as f:
                    f.write(f"Canceled Prompt: {user_input}\nTimestamp: {datetime.now().isoformat()}\n")
                shell_print(f"🤖🧻💬: Prompt canceled and saved to {canceled_filename}", label="Prompt Canceled")
                shell_print(
                    emoji_aware_pad("🤖🧻📎: 📎 To view this prompt later, type:", 60),
                    emoji_aware_pad(f'!@0ko@!/print "{canceled_filename}"', 60),
                    label="Prompt Print Instruction"
                )
                continue

            # ✅ Save the user's original prompt
            filename = save_prompt_to_file(user_input)  # returns just the filename
            filepath = os.path.join(PROMPT_DIR, filename)

            # 🔻 Echo the original prompt and show how to reprint it
            shell_print(
                emoji_aware_pad("🔻 Original Prompt Sent to 0KO System 🔻", 60, emoji_shift),
                emoji_aware_pad(f"🤖🧻:📤: {user_input}", 60, emoji_shift),
                emoji_aware_pad(f"🤖🧻📄: Prompt saved to: `{filename}`", 60, emoji_shift),
                emoji_aware_pad("📎🤖🧻: To reprint this prompt and its responses, type:", 60, emoji_shift),
                emoji_aware_pad(f'🤖🧻:!@0ko@!/print "{filepath}"', 60, emoji_shift),
                emoji_aware_pad("=" * 60, 60, emoji_shift),
                label="Prompt Echo"
            )

            prompt_locked = True
            shell_print(f"🤖🧻💬: Processing prompt: {user_input}", label="3MAIb Prompt")
            try:
                dispatch_symbolic_tri_call_and_save(user_input, emoji_shift=emoji_shift)
            except Exception as dispatch_error:
                handle_symbolic_error(dispatch_error, context="main → 0KO dispatch")
            finally:
                prompt_locked = False
                last_unlock_time = time.time()
                if input_during_lock:
                    shell_print(
                        emoji_aware_pad("🔻 Input During Prompt Load — Recorded Message Not Sent 🔻", 60, emoji_shift),
                        label="Console Record"
                    )
                    for i, (msg, _) in enumerate(input_during_lock, 1):
                        shell_print(
                            emoji_aware_pad(f"🤖🧻💬:📥 {i}. {msg}", 60, emoji_shift),
                            label="Recorded Input"
                        )
                    input_during_lock.clear()

    except Exception as e:
        shell_print(
            emoji_aware_pad(f"🧻🤖🧻🧻🧻:⚠️: ERROR: {e}", 60, emoji_shift),
            emoji_aware_pad("🤖🧻: Notice:", 60, emoji_shift),
            emoji_aware_pad("   A symbolic fault occurred during initialization.", 60, emoji_shift),
            emoji_aware_pad("   Try rerunning the evaluation or checking your config files.", 60, emoji_shift),
            label="System Error"
        )

# LICENSE.TXT
# Zero-Ology License v1.11
# 0ko3maibZero-OlogyLicensev01.txt
# 0ko3maibZero-OlogyLicensev1.11
# October 14, 2025
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
#- dispatchai_forge.py
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


