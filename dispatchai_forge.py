# dispatchai_forge.py
# Title: 0KO DispatchAI Forge — External AI Configuration Utility 
# Version: v0001
# Ceo0: Szmy, Stacey.
# dev: HAHA.8888, HAHA.Xai.Grok, HAHA.Gemini
# Zer00logy License v1.11

import json
import os
import uuid
import time
import textwrap
import re
import sys
import traceback
import subprocess
from collections import Counter

# 🔹 Config and Constants
CONFIG_DIR = "dispatchaiconfig"  # Dedicated folder for JSON configs
DEFAULT_CONFIG_FILENAME = "external_dispatch_config.json"
EMOJI_SHIFT_CONFIG_FILE = "emoji_shift.cfg"
EMOJI_PATTERN = re.compile("[\U0001F300-\U0001FAFF]")
SHELL_WIDTH = 100
WRAP_WIDTH = 96
EMOJI_SHIFT = 2
TOP_LEFT = "╔"
TOP_RIGHT = "╗"
BOTTOM_LEFT = "╚"
BOTTOM_RIGHT = "╝"
HORIZONTAL = "═"
VERTICAL = "║"

# 🔹 Shell and Aesthetic Functions
def manual_visual_width(line, emoji_shift=EMOJI_SHIFT):
    emoji_count = len(EMOJI_PATTERN.findall(line))
    non_emoji_chars = EMOJI_PATTERN.sub("", line)
    return len(non_emoji_chars) + (emoji_count * emoji_shift)

def emoji_aware_pad(line, target_width=WRAP_WIDTH, emoji_shift=EMOJI_SHIFT):
    visual_width = manual_visual_width(line, emoji_shift)
    padding = max(0, target_width - visual_width)
    return line + " " * padding

def wrap_in_shell(content, width=WRAP_WIDTH):
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

def fix_symbolic_box_alignment(lines, emoji_shift=EMOJI_SHIFT):
    fixed_lines = []
    left_positions = []
    right_positions = []
    for line in lines:
        if VERTICAL in line:
            left = line.find(VERTICAL)
            right = line.rfind(VERTICAL)
            if left != -1 and right != -1 and left != right:
                left_positions.append(left)
                right_positions.append(right)
    if left_positions and right_positions:
        left_target = Counter(left_positions).most_common(1)[0][0]
        right_target = Counter(right_positions).most_common(1)[0][0]
    else:
        return lines
    for line in lines:
        if VERTICAL in line:
            left = line.find(VERTICAL)
            right = line.rfind(VERTICAL)
            if left != -1 and right != -1 and left != right:
                content = line[left + 1:right].strip()
                content_area_width = right_target - left_target - 2
                padded = emoji_aware_pad(content, content_area_width, emoji_shift)
                new_line = (
                    line[:left_target] + VERTICAL +
                    " " + padded + " " +
                    VERTICAL + line[right_target + 1:]
                )
                fixed_lines.append(new_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    return fixed_lines

def shell_print(*lines, label=None):
    if any(VERTICAL in line for line in lines):
        lines = fix_symbolic_box_alignment(list(lines))
        for line in lines:
            print(line)
        return
    content = "\n".join(lines)
    if label:
        content = f"🔻 {label} 🔻\n\n{content}"
    print(wrap_in_shell(content))

def shell_input(prompt, label=None):
    shell_print(prompt, label=label)
    return input("♾️ Consol: ")

def handle_symbolic_error(e, context="Unknown"):
    error_msg = [
        "🤖🧻⚠️💬: ⚠️ SYSTEM ERROR DETECTED",
        f"🔻 Context: {context}",
        f"🔻 Exception: {str(e)}",
        "",
        "🤖🧻💬: Configuration Utility : Recovery Protocol Activated",
        "   ↳ Attempting to proceed...",
    ]
    shell_print(*error_msg, label="DispatchAI Forge 🤖🧻💬 : — Symbolic Error Handler")

# 🔹 Emoji Calibration
def calibrate_emoji_width():
    global EMOJI_SHIFT
    shell_print(
        "🤖🧻👋💬: Welcome! Let's calibrate your terminal's emoji rendering.",
        "This ensures all symbolic outputs align perfectly.",
        "You'll see a boxed frame below. If the emoji line looks wider than the empty ones,",
        "enter how many spaces it appears shifted (usually 1, 2, or 3).",
        label="Calibration Instructions"
    )
    while True:
        try:
            shift_input = input("🤖🧻💬: 🔧: Enter estimated emoji width (1, 2, or 3): ").strip()
            shift = int(shift_input)
            if shift not in [1, 2, 3]:
                raise ValueError("Invalid emoji width")
            frame_width = WRAP_WIDTH - 4
            top_border = TOP_LEFT + HORIZONTAL * (frame_width + 2) + TOP_RIGHT
            bottom_border = BOTTOM_LEFT + HORIZONTAL * (frame_width + 2) + BOTTOM_RIGHT
            empty_line = f"{VERTICAL} {emoji_aware_pad('', frame_width, shift)} {VERTICAL}"
            emoji_line_content = "👋"
            visual_width_emoji = manual_visual_width(emoji_line_content, shift)
            padding_needed = frame_width - visual_width_emoji
            pad_left = padding_needed // 2
            pad_right = padding_needed - pad_left
            emoji_line = f"{VERTICAL} {' ' * pad_left}👋{' ' * pad_right} {VERTICAL}"
            print("\n" + top_border)
            for i in range(6):
                print(emoji_line if i == 3 else empty_line)
            print(bottom_border + "\n")
            confirm = input("🤖✅🧻💬: Does this look aligned? (y/n): ").strip().lower()
            if confirm == "y":
                shell_print(f"🤖🧻💬: ✅: Calibration complete. Emoji width set to {shift}", label="Calibration Success")
                EMOJI_SHIFT = shift
                return shift
            else:
                shell_print("🤖🧻🧻💬: Let's try again. Adjust the emoji width.", label="Calibration Retry")
        except Exception as e:
            handle_symbolic_error(e, "Emoji Calibration Input")

def save_shift(shift):
    try:
        with open(EMOJI_SHIFT_CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(str(shift))
        shell_print(f"✅🤖🧻💬: Emoji Shift Saved to `{EMOJI_SHIFT_CONFIG_FILE}`", label="Emoji Calibration Save")
    except Exception as e:
        handle_symbolic_error(e, "save_shift")

def load_shift():
    global EMOJI_SHIFT
    try:
        if os.path.isfile(EMOJI_SHIFT_CONFIG_FILE):
            with open(EMOJI_SHIFT_CONFIG_FILE, "r", encoding="utf-8") as f:
                shift = int(f.read().strip())
                shell_print(f"🧻✅🤖💬: Loaded emoji shift: {shift}", label="Emoji Calibration")
                EMOJI_SHIFT = shift
                return shift
        else:
            raise FileNotFoundError("Config file not found.")
    except Exception:
        shell_print("🧻⚠️🤖💬: No valid emoji config found. Running calibration...", label="Emoji Calibration")
        shift = calibrate_emoji_width()
        save_shift(shift)
        EMOJI_SHIFT = shift
        return shift

# 🔹 Config File Handlers
def get_config_filepath(filename=DEFAULT_CONFIG_FILENAME):
    return os.path.join(CONFIG_DIR, filename)

def get_all_config_files():
    if not os.path.exists(CONFIG_DIR):
        return []
    files = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".json")]
    files.sort(key=lambda f: os.path.getmtime(get_config_filepath(f)), reverse=True)
    return files

def load_config(filename=None):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        shell_print(f"🤖🧻💬: Created config directory: [{CONFIG_DIR}]", label="System Setup")
        return [], None
    config_files = get_all_config_files()
    if not config_files:
        return [], None
    file_to_load = filename if (filename and filename in config_files) else config_files[0]
    filepath = get_config_filepath(file_to_load)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            external_ais = json.load(f)
        shell_print(f"🧻✅🤖💬: Loaded {len(external_ais)} configuration(s) from [{file_to_load}]", label="Config Load")
        return external_ais, file_to_load
    except json.JSONDecodeError:
        shell_print(f"🤖🧻⚠️: Error reading {file_to_load}. Starting blank.", label="Config Error")
        return [], file_to_load
    except Exception as e:
        handle_symbolic_error(e, f"load_config_from_file:{file_to_load}")
        return [], file_to_load

def save_config(external_ais, current_filename=None, new_save=False):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    filename_to_save = current_filename or DEFAULT_CONFIG_FILENAME
    if new_save:
        shell_print(f"Current file: [{filename_to_save}]", label="New Save Option")
        new_filename = shell_input("Enter a NEW filename for this configuration (e.g., 'gemini_only.json'):").strip()
        if not new_filename.endswith(".json"):
            new_filename += ".json"
        filename_to_save = new_filename
    filepath = get_config_filepath(filename_to_save)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(external_ais, f, indent=4)
        shell_print(
            f"Configuration saved to [{filename_to_save}]",
            f"Total {len(external_ais)} external AI systems configured",
            label="Config Save Success"
        )
        return True
    except Exception as e:
        handle_symbolic_error(e, "save_config_file")
        return False

# 🔹 Menu Functions
def test_ai_connection(ai_config):
    ai_name = ai_config.get("name", "Unknown AI")
    ai_type = ai_config.get("type", "unknown")
    model = ai_config.get("model", "unknown")
    shell_print(f"[TESTING] Initiating connection test for {ai_name} ({model})...", label="AI Connection Test")
    time.sleep(1)
    api_key_override = ai_config.get("api_key_override", "").lower()
    if "key_error" in api_key_override or "invalid" in api_key_override:
        return False, "Simulated failure: API Key appears invalid or expired."
    elif not ai_name or not ai_type or not model:
        return False, "Simulated failure: Missing critical configuration fields (Name, Type, Model)."
    elif ai_type == "ollama":
        try:
            subprocess.run(f"ollama show {model}", shell=True, capture_output=True, text=True, check=True)
            return True, f"Success: Ollama model '{model}' is available."
        except subprocess.CalledProcessError:
            return False, f"Failure: Ollama model '{model}' not found."
    elif ai_type in ["gemini", "openai"]:
        return True, f"Simulated success: {ai_type.capitalize()} API is ready."
    return True, "Simulated success: Custom API is ready."

def add_new_ai(external_ais):
    shell_print("--- ADD NEW EXTERNAL AI CONFIGURATION ---", label="Add AI")
    ai_name = shell_input("[AI Name] (e.g., 'Gemini-API', 'ChatGPT-4o'): ").strip()
    ai_type = shell_input("[Driver/API Type] (e.g., 'gemini', 'openai', 'ollama'): ").strip().lower()
    model_name = shell_input("[Model Name] (e.g., 'gemini-2.5-flash', 'gpt-4o'): ").strip()
    api_key = shell_input("[API Key/Secret] (LEAVE BLANK to use environment variable): ").strip()
    emoji = shell_input("[Display Emoji] (e.g., '✨', '🧠', '⚙️'): ").strip()
    new_ai = {
        "id": str(uuid.uuid4()),
        "name": ai_name,
        "type": ai_type,
        "model": model_name,
        "emoji": emoji,
        "api_key_override": api_key,
        "enabled": True
    }
    test_success, test_message = test_ai_connection(new_ai)
    if test_success:
        shell_print(f"✅ Connection Test Passed: {test_message}", label="Test Result")
        external_ais.append(new_ai)
        shell_print(f"✅ Added {ai_name} ({model_name}) to the configuration list.", label="AI Added")
    else:
        shell_print(f"⚠️ Connection Test FAILED: {test_message}", label="Test Failure")
        choice = shell_input("Do you still want to save this configuration? (y/N): ").strip().lower()
        if choice == "y":
            external_ais.append(new_ai)
            shell_print(f"⚠️ Added FAILED configuration {ai_name}. Please fix the API Key later.", label="AI Added (Failure)")
    return external_ais

def view_edit_test_ai(external_ais):
    if not external_ais:
        shell_print("No external AI systems configured to view/edit.", label="Error")
        return
    shell_print("--- VIEW / EDIT / TEST AI CONFIGURATIONS ---", label="Edit AI")
    display_lines = [f"[{i+1}] {ai['emoji']} {ai['name']} ({ai['model']}) [Type: {ai['type']}]" for i, ai in enumerate(external_ais)]
    shell_print(*display_lines, label="AI List")
    try:
        choice = shell_input("\nEnter the number of the AI to edit/test (or 'c' to cancel): ").strip()
        if choice.lower() == "c":
            return
        index = int(choice) - 1
        if 0 <= index < len(external_ais):
            ai = external_ais[index]
            shell_print(f"--- Editing: {ai['name']} ---", label="AI Editor")
            def get_input_with_default(prompt, current_value):
                new_value = shell_input(f"[{prompt}] (Current: '{current_value}'): ").strip()
                return new_value if new_value else current_value
            ai["name"] = get_input_with_default("AI Name", ai["name"])
            ai["type"] = get_input_with_default("Driver/API Type", ai["type"]).lower()
            ai["model"] = get_input_with_default("Model Name", ai["model"])
            api_prompt = "API Key/Secret (Press ENTER to keep current value or use ENV variable)"
            current_status = "***REDACTED***" if ai["api_key_override"] else "Uses ENV Variable"
            new_key = shell_input(f"[{api_prompt}] (Current: {current_status}): ").strip()
            if new_key:
                ai["api_key_override"] = new_key
            ai["emoji"] = get_input_with_default("Display Emoji", ai["emoji"])
            test_choice = shell_input("Configuration updated. Run connection test now? (y/N): ").strip().lower()
            if test_choice == "y":
                test_success, test_message = test_ai_connection(ai)
                shell_print(f"{'✅' if test_success else '⚠️'} Connection Test {'Passed' if test_success else 'FAILED'}: {test_message}", label="Test Result")
        else:
            shell_print("Invalid selection.", label="Error")
    except ValueError:
        shell_print("Invalid input. Please enter a number or 'c'.", label="Error")

def delete_ai(external_ais):
    if not external_ais:
        shell_print("No external AI systems configured to delete.", label="Error")
        return
    shell_print("--- DELETE AI CONFIGURATIONS ---", label="Delete AI")
    display_lines = [f"[{i+1}] {ai['emoji']} {ai['name']} ({ai['model']})" for i, ai in enumerate(external_ais)]
    shell_print(*display_lines, label="AI List")
    try:
        choice = shell_input("\nEnter the number of the AI to DELETE (or 'c' to cancel): ").strip()
        if choice.lower() == "c":
            return
        index = int(choice) - 1
        if 0 <= index < len(external_ais):
            ai_to_delete = external_ais[index]
            confirm = shell_input(f"Are you sure you want to delete {ai_to_delete['name']}? (y/N): ").strip().lower()
            if confirm == "y":
                del external_ais[index]
                shell_print(f"✅ Successfully deleted {ai_to_delete['name']}.", label="Deletion Success")
            else:
                shell_print("Deletion cancelled.", label="Cancellation")
        else:
            shell_print("Invalid selection.", label="Error")
    except ValueError:
        shell_print("Invalid input. Please enter a number or 'c'.", label="Error")

def handle_save_and_exit(external_ais, current_filename):
    shell_print("--- SAVE CONFIGURATION ---", label="Save/Exit")
    if not external_ais:
        shell_print("Configuration list is empty. Exiting without saving.", label="Notice")
        return True
    shell_print(f"Current loaded file: [{current_filename or DEFAULT_CONFIG_FILENAME}]", label="Save Options")
    while True:
        choice = shell_input("Choose save option:\n [1] Overwrite/Save to current file\n [2] Save as a NEW file\n [3] Cancel/Exit without saving\n Enter option number: ").strip()
        if choice == "1":
            return save_config(external_ais, current_filename)
        elif choice == "2":
            return save_config(external_ais, current_filename, new_save=True)
        elif choice == "3":
            shell_print("Exiting without saving changes.", label="Notice")
            return True
        else:
            shell_print("Invalid option. Please enter 1, 2, or 3.", label="Error")

def delete_configs():
    config_files = get_all_config_files()
    if not config_files:
        shell_print(f"No external config files found in the [{CONFIG_DIR}] directory.", label="Config Delete")
        return
    shell_print("--- DELETE CONFIGURATION FILES ---", label="Delete Files")
    for i, file in enumerate(config_files):
        shell_print(f"[{i+1}] {file}")
    shell_print(f"[{len(config_files) + 1}] Delete ALL {len(config_files)} files.")
    try:
        choice = shell_input("Enter the number of the file to DELETE, or the option to DELETE ALL (or 'c' to cancel): ").strip().lower()
        if choice == "c":
            return
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(config_files):
                file_to_delete = config_files[index]
                confirm = shell_input(f"Are you sure you want to delete [{file_to_delete}]? (y/N): ").strip().lower()
                if confirm == "y":
                    os.remove(get_config_filepath(file_to_delete))
                    shell_print(f"✅ Successfully deleted [{file_to_delete}].", label="Deletion Success")
            elif index == len(config_files):
                confirm = shell_input(f"⚠️ Are you sure you want to DELETE ALL {len(config_files)} files in {CONFIG_DIR}? (Y/n): ").strip().lower()
                if confirm == "y":
                    for file in config_files:
                        os.remove(get_config_filepath(file))
                    if not os.listdir(CONFIG_DIR):
                        os.rmdir(CONFIG_DIR)
                        shell_print(f"✅ Successfully deleted ALL files and removed the directory [{CONFIG_DIR}].", label="Deletion Success")
                    else:
                        shell_print(f"✅ Successfully deleted ALL files.", label="Deletion Success")
            else:
                shell_print("Invalid selection.", label="Error")
        else:
            shell_print("Invalid input. Please enter a number or 'c'.", label="Error")
    except Exception as e:
        handle_symbolic_error(e, "delete_configs")

def create_external_config():
    load_shift()
    external_ais, current_filename = load_config()
    current_filename = current_filename or DEFAULT_CONFIG_FILENAME
    shell_print(
        f"--- DispatchAI Forge External AI Config ---",
        f"Loaded {len(external_ais)} configuration(s).",
        f"Config Directory: [{CONFIG_DIR}]",
        label="Utility Startup"
    )
    while True:
        shell_print(
            "Choose an option:",
            " [1] Add New External AI (Run Connection Test)",
            " [2] View/Edit/Test Existing AI Configurations",
            " [3] Delete AI Configuration from List",
            " [4] Save/Exit (Save options: Overwrite/New File)",
            " [5] Delete Stored Configuration JSON Files",
            label="Main Menu"
        )
        choice = shell_input("Enter option number: ").strip()
        if choice == "1":
            external_ais = add_new_ai(external_ais)
        elif choice == "2":
            view_edit_test_ai(external_ais)
        elif choice == "3":
            delete_ai(external_ais)
        elif choice == "4":
            if handle_save_and_exit(external_ais, current_filename):
                break
        elif choice == "5":
            delete_configs()
        else:
            shell_print("Invalid option. Please enter 1, 2, 3, 4, or 5.", label="Error")

if __name__ == "__main__":
    create_external_config()

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