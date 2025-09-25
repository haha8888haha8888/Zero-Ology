# rainbowquest1000v0288AI.py
# haha.8888
# haha.????
# haha.Xai.Grok
# haha.OpenAi.ChatGPT

# Title: RainbowQuest1000.py
# Version: 1000v0288AI
# Changelog:
# v0272: Cleared changelog
# v0273: Added Ollama AI integration for Player2 with model selection (Phi, Mistral, Llama2, or random computer)
# v0274: Fixed debug print revealing Player2's Hit Me votes/bets in RQBJ mode; improved AI dispatch with UTF-8 encoding and retries
# v0275: Fixed RQ mode round summary to include details of bets on opponent's guesses (higher/lower, suit, rank)
# v0276: Added display of Player2's bets on Player1's guesses in RQ and RQBJ modes before Player1's grand bets
# v0277: Fixed Player2's bets on Player1's guesses not displaying before Player1's grand bets in both RQ and RQBJ modes

import random
import time
import os
import sys
import traceback
import logging
import re
import textwrap
from datetime import datetime
import subprocess
import threading  # For spinner

# Attempt to import shelling module for emoji score display (Zero-ology/Zer00logy style)
try:
    import shelling  # Optional, from Zero-ology/Zer00logy
except ImportError:
    shelling = None  # Fallback to numeric scores

# Set up logging with fallback to console
try:
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('rainbowquest_error.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger('RainbowQuest')
except Exception as e:
    print(f"Failed to set up logging: {e}")
    logger = logging.getLogger('RainbowQuest')
    logger.addHandler(logging.StreamHandler())

# Shelling and Emoji Calibration
TOP_LEFT = "╔"
TOP_RIGHT = "╗"
BOTTOM_LEFT = "╚"
BOTTOM_RIGHT = "╝"
HORIZONTAL = "═"
VERTICAL = "║"
SHELL_WIDTH = 100  # Adjust width as needed

EMOJI_PATTERN = re.compile("[\U0001F300-\U0001FAFF]")
EMOJI_SHIFT = 0  # Default until calibrated

def dispatch_to_ai(model, prompt):
    """Dispatch a prompt to the specified Ollama model and return the response."""
    try:
        full_prompt = f"You are an AI opponent in Rainbow Quest. Make strategic decisions based on game rules. {prompt}"
        for attempt in range(3):  # Retry up to 3 times
            try:
                response = subprocess.run(
                    ['ollama', 'run', model, full_prompt],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',  # Explicit UTF-8 encoding
                    timeout=60  # Increased timeout
                ).stdout.strip()
                if response:
                    return response
                logger.warning(f"Ollama empty response on attempt {attempt + 1}")
            except subprocess.TimeoutExpired:
                logger.error(f"Ollama timeout on attempt {attempt + 1}")
            except UnicodeDecodeError as e:
                logger.error(f"Ollama UnicodeDecodeError: {str(e)}")
        logger.error("Ollama failed after retries.")
        return None
    except Exception as e:
        logger.error(f"Ollama error: {str(e)}")
        return None

def spinner(message):
    """Display a loading spinner while AI is thinking."""
    spinner_chars = ['|', '/', '-', '\\']
    i = 0
    while getattr(threading.current_thread(), 'do_run', True):
        print(f"\r{message} {spinner_chars[i % len(spinner_chars)]}", end="")
        i += 1
        time.sleep(0.2)

def manual_visual_width(line, emoji_shift):
    """Calculate the visual width of a line, accounting for emojis."""
    emoji_count = len(EMOJI_PATTERN.findall(line))
    non_emoji_chars = EMOJI_PATTERN.sub("", line)
    return len(non_emoji_chars) + (emoji_count * emoji_shift)

def emoji_aware_pad(text, width, emoji_shift=None):
    """Pad a line to the target width, accounting for emoji visual width."""
    if emoji_shift is None:
        emoji_shift = EMOJI_SHIFT
    visual_width = manual_visual_width(text, emoji_shift)
    padding = max(0, width - visual_width)
    return text + " " * padding

def save_shift(shift, save_dir="config_logs"):
    """Save the emoji shift value to a configuration file."""
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"emoji_shift_{timestamp}.cfg"
    filepath = os.path.join(save_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(shift))
    print(f"✅ Emoji Shift Saved to: {filename}")
    return filepath

def load_shift(config_path="config_logs"):
    """Load the latest emoji shift value from the configuration directory or file."""
    try:
        if os.path.isfile(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                shift = int(f.read().strip())
                print(f"✅ Loaded emoji shift from {os.path.basename(config_path)}: {shift}")
                return shift
        elif os.path.isdir(config_path):
            files = [f for f in os.listdir(config_path) if f.startswith("emoji_shift_") and f.endswith(".cfg")]
            if not files:
                raise FileNotFoundError("No emoji shift config files found.")
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(config_path, f)))
            filepath = os.path.join(config_path, latest_file)
            with open(filepath, "r", encoding="utf-8") as f:
                shift = int(f.read().strip())
                print(f"✅ Loaded emoji shift from {latest_file}: {shift}")
                return shift
        else:
            raise FileNotFoundError(f"Invalid path: {config_path}")
    except Exception as e:
        print(f"⚠️ Error loading emoji shift: {e}. Running calibration...")
        shift = calibrate_emoji_width()
        save_shift(shift, "config_logs")
        return shift

def calibrate_emoji_width():
    """Calibrate emoji width by prompting the user to align a test frame."""
    print("🌈 Calibrating emoji width...")
    while True:
        try:
            shift_input = input("🔧 Enter estimated emoji width (1, 2, or 3): ").strip()
            shift = int(shift_input)
            if shift not in [1, 2, 3]:
                raise ValueError("Invalid emoji width")
            frame_width = 60 + shift
            top_border = "╔" + "═" * frame_width + "╗"
            bottom_border = "╚" + "═" * frame_width + "╝"
            empty_line = "║" + " " * frame_width + "║"
            emoji_line = "║" + " " * ((frame_width // 2) - 1) + "👋" + " " * ((frame_width // 2) - 1) + "║"
            print("\n" + top_border)
            for i in range(6):
                print(emoji_line if i == 3 else empty_line)
            print(bottom_border + "\n")
            confirm = input("✅ Does this look aligned? (y/n): ").strip().lower()
            if confirm == "y":
                print(f"✅ Calibration complete. Emoji width set to {shift}")
                return shift
            else:
                print("🔁 Let's try again. Adjust the emoji width and re-test.")
        except Exception as e:
            print(f"⚠️ Calibration error: {e}. Please try again.")

def wrap_in_shell(content, width=SHELL_WIDTH):
    """Wrap content in a boxed shell with emoji-aware padding."""
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

def shell_print(content, label=None):
    """Print content with optional label, wrapped in a shell."""
    if label:
        content = f"🔻 {label} 🔻\n\n" + content
    print(wrap_in_shell(content))

def handle_symbolic_error(e, context="Unknown"):
    """Handle errors with a formatted error message."""
    error_msg = [
        "⚠️ SYSTEM ERROR DETECTED",
        f"🔻 Context: {context}",
        f"🔻 Exception: {str(e)}",
        "",
        "🤖 Recovery Protocol Activated",
        "   ↳ Resetting symbolic prompt...",
        "   ↳ Echo integrity preserved.",
        "   ↳ You may re-enter your command."
    ]
    shell_print("\n".join(error_msg), label="Error Handler")

# Initialize EMOJI_SHIFT
try:
    config_path = os.path.join(os.path.dirname(__file__), "config_logs")
except NameError:
    config_path = os.path.join(os.getcwd(), "config_logs")
EMOJI_SHIFT = load_shift(config_path)

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.color = 'Black' if suit in ['Spades', 'Clubs'] else 'Red'
        self.face_up = False

    def get_blackjack_value(self, ace_low=False):
        """Return blackjack value (Ace = 11 or 1, face cards = 10)."""
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        if self.rank == 'Ace':
            return 1 if ace_low else 11
        return int(self.rank) if self.rank.isdigit() else 0

    def get_rank_order(self):
        """Return rank order for higher/lower (Ace = 14, except special rule Ace < 2)."""
        order = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
        }
        return order.get(self.rank, 0)

    def flip(self):
        self.face_up = not self.face_up

    def __str__(self):
        if self.face_up:
            return f"{self.rank} of {self.suit}"
        return "[Face Down]"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if self.rank == 'Ace' and other.rank == '2':
            return True
        if self.rank == '2' and other.rank == 'Ace':
            return False
        return self.get_rank_order() < other.get_rank_order()

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

class Player:
    def __init__(self, name, is_human, model=None):
        self.name = name
        self.is_human = is_human
        self.model = model  # Ollama model if AI, None for random
        self.score = 0
        self.base_scores = []
        self.grand_scores = []
        self.bonus_scores = []

def generate_deck():
    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    return [Card(suit, rank) for suit in suits for rank in ranks]

def display_table(table):
    content = "\n🃏 Table (Positions 1-52):\n"
    num_cards = len(table)
    for i in range(0, num_cards, 13):
        row = []
        for j in range(13):
            idx = i + j
            if idx < num_cards:
                card_str = str(table[idx])
                row.append(f"{idx+1:2}: {card_str}")
        if row:
            content += '  '.join(row) + '\n'
    shell_print(content, "Game Table")

def display_score(score):
    """Display score with emoji shells if shelling module is available."""
    if shelling:
        return shelling.count_shells(score)  # Assumes shelling module has count_shells
    return '⚪' * score if score > 0 else '0'

def pick_position(player, available):
    if player.is_human:
        while True:
            try:
                content = f"{player.name}, pick a position (1-52):"
                shell_print(content, f"{player.name}'s Card Pick")
                pos = int(input()) - 1
                if pos in available:
                    return pos
                shell_print("Invalid or already picked position.", "Error")
            except ValueError:
                shell_print("Please enter a valid number.", "Error")
    else:
        avail_list = sorted(list(available))
        if player.model:
            prompt = f"Choose a position from: {', '.join(map(str, [p+1 for p in avail_list]))}. Respond with ONLY the number (1-52)."
            spinner_thread = threading.Thread(target=spinner, args=(f"{player.name} is thinking...",))
            spinner_thread.do_run = True
            spinner_thread.start()
            response = dispatch_to_ai(player.model, prompt)
            spinner_thread.do_run = False
            spinner_thread.join()
            print("\r" + " " * 50 + "\r")  # Clear spinner line
            try:
                pos = int(response) - 1
                if pos in available:
                    shell_print(f"{player.name} ({player.model.capitalize()}) picks position {pos+1}", f"{player.name}'s Card Pick")
                    time.sleep(0.5)
                    return pos
            except (ValueError, TypeError):
                pass  # Fallback to random
        pos = random.choice(avail_list)
        shell_print(f"{player.name} picks position {pos+1}", f"{player.name}'s Card Pick")
        time.sleep(0.5)
        return pos

def get_guess(player, prompt, choices=None, max_val=None):
    if player.is_human:
        if choices:
            choice_str = '/'.join(choices)
            content = f"{player.name}, {prompt} ({choice_str})"
            shell_print(content, f"{player.name}'s Guess")
            guess = input().capitalize()
            while guess not in choices:
                shell_print(f"Invalid choice. Choose from {choice_str}.", "Error")
                guess = input().capitalize()
            return guess
        else:
            while True:
                try:
                    content = f"{player.name}, {prompt} (0-{max_val})"
                    shell_print(content, f"{player.name}'s Guess")
                    guess = int(input())
                    if 0 <= guess <= max_val:
                        return guess
                    shell_print(f"Please enter a number between 0 and {max_val}.", "Error")
                except ValueError:
                    shell_print("Please enter a valid number.", "Error")
    else:
        if player.model:
            if choices:
                choice_str = ', '.join(choices)
                ai_prompt = f"{prompt} Choices: {choice_str}. Respond with ONLY the chosen option."
            else:
                ai_prompt = f"{prompt} (0-{max_val}). Respond with ONLY the number."
            spinner_thread = threading.Thread(target=spinner, args=(f"{player.name} is thinking...",))
            spinner_thread.do_run = True
            spinner_thread.start()
            response = dispatch_to_ai(player.model, ai_prompt)
            spinner_thread.do_run = False
            spinner_thread.join()
            print("\r" + " " * 50 + "\r")  # Clear spinner line
            if choices and response in choices:
                if prompt.startswith("do you want to request a Hit Me") or prompt.startswith("do you bet that"):
                    shell_print(f"{player.name} has submitted their Hit Me vote.", f"{player.name} Status")
                return response
            elif not choices:
                try:
                    guess = int(response)
                    if 0 <= guess <= max_val:
                        return guess
                except (ValueError, TypeError):
                    pass  # Fallback to random
        if choices:
            weights = [0.45, 0.45, 0.1] if 'Tie' in choices else None
            guess = random.choices(choices, weights=weights)[0] if weights else random.choice(choices)
            if prompt.startswith("do you want to request a Hit Me") or prompt.startswith("do you bet that"):
                shell_print(f"{player.name} has submitted their Hit Me vote.", f"{player.name} Status")
            return guess
        else:
            return random.randint(0, max_val)

def display_victory_screen(player1, player2):
    content = "\n🎉 Game Over! 🎉\n\n"
    winner = player1 if player1.score > player2.score else player2 if player2.score > player1.score else None
    if winner:
        content += f"🏆 {winner.name} wins! 🏆\n"
    else:
        content += "🤝 It's a tie! 🤝\n"
    
    content += "\n📊 Final Score Summary:\n"
    content += f"{player1.name}: {display_score(player1.score)} ({player1.score} points)\n"
    content += f"  Base Points: {sum(player1.base_scores)} {display_score(sum(player1.base_scores))}\n"
    content += f"  Grand Points: {sum(player1.grand_scores)} {display_score(sum(player1.grand_scores))}\n"
    content += f"  Bonus Points: {sum(player1.bonus_scores)} {display_score(sum(player1.bonus_scores))}\n"
    content += f"  Round-by-Round: {player1.base_scores} (Base) + {player1.grand_scores} (Grand) + {player1.bonus_scores} (Bonus)\n"
    content += f"{player2.name}: {display_score(player2.score)} ({player2.score} points)\n"
    content += f"  Base Points: {sum(player2.base_scores)} {display_score(sum(player2.base_scores))}\n"
    content += f"  Grand Points: {sum(player2.grand_scores)} {display_score(sum(player2.grand_scores))}\n"
    content += f"  Bonus Points: {sum(player2.bonus_scores)} {display_score(sum(player2.bonus_scores))}\n"
    content += f"  Round-by-Round: {player2.base_scores} (Base) + {player2.grand_scores} (Grand) + {player2.bonus_scores} (Bonus)\n"
    content += "\nPress Enter twice to start a new game..."
    shell_print(content, "Victory Screen")

def play_round_type1(player1, player2, table, available, round_num, game_mode, house_hand):
    content = f"\n🎲 Round {round_num}\n"
    if game_mode == 'RQBJ' and house_hand is not None:
        content += f"🏛️ House Dealer's Hand: {house_hand}\n"
    shell_print(content, "Round Start")
    display_table(table)

    shell_print(f"{player1.name} picks first.", "Turn Order")
    p1_pos = pick_position(player1, available)
    available.remove(p1_pos)
    p1_card = table[p1_pos]

    shell_print(f"{player2.name} picks second.", "Turn Order")
    p2_pos = pick_position(player2, available)
    available.remove(p2_pos)
    p2_card = table[p2_pos]

    is_third_round = round_num % 3 == 0
    p1_sees_card = p2_card if game_mode == 'RQBJ' and is_third_round else p1_card
    p2_sees_card = p1_card if game_mode == 'RQBJ' and is_third_round else p2_card

    # Player1 initial guesses
    shell_print(f"{player1.name}'s Guesses (you will be prompted):", f"{player1.name}'s Guesses")
    p1_bets = {}
    p1_bets['hl'] = get_guess(player1, "is your card higher or lower than opponent's?", ['Higher', 'Lower'])
    p1_bets['suit'] = get_guess(player1, "guess your card's suit", ['Spades', 'Clubs', 'Diamonds', 'Hearts'])
    p1_bets['rank'] = get_guess(player1, "guess your card's rank", ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'])
    if game_mode == 'RQBJ':
        p1_bets['bj_total'] = get_guess(player1, "guess the blackjack total (2-21)", ['2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21'])
        p1_bets['bust'] = get_guess(player1, "guess if the total will bust", ['Yes', 'No'])
        p1_bets['opp_color'] = get_guess(player1, "guess opponent's card color", ['Red', 'Black'])
        if house_hand is not None:
            p1_bets['vs_house'] = get_guess(player1, "is your blackjack total higher, lower, or tied with the House?", ['Higher', 'Lower', 'Tie'])

    # Player2 initial guesses
    shell_print(f"{player2.name}'s Guesses:", f"{player2.name}'s Guesses")
    p2_bets = {}
    p2_bets['hl'] = get_guess(player2, "is your card higher or lower than opponent's?", ['Higher', 'Lower'])
    p2_bets['suit'] = get_guess(player2, "guess your card's suit", ['Spades', 'Clubs', 'Diamonds', 'Hearts'])
    p2_bets['rank'] = get_guess(player2, "guess your card's rank", ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'])
    if game_mode == 'RQBJ':
        p2_bets['bj_total'] = get_guess(player2, "guess the blackjack total (2-21)", ['2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21'])
        p2_bets['bust'] = get_guess(player2, "guess if the total will bust", ['Yes', 'No'])
        p2_bets['opp_color'] = get_guess(player2, "guess opponent's card color", ['Red', 'Black'])
        if house_hand is not None:
            p2_bets['vs_house'] = get_guess(player2, "is your blackjack total higher, lower, or tied with the House?", ['Higher', 'Lower', 'Tie'])
    
    # Display Player2's guesses to Player1
    p2_guesses_display = f"{player2.name}'s Guesses (revealed for your betting):\n"
    p2_guesses_display += f"  - Higher/Lower: {p2_bets['hl']}\n"
    p2_guesses_display += f"  - Suit: {p2_bets['suit']}\n"
    p2_guesses_display += f"  - Rank: {p2_bets['rank']}\n"
    if game_mode == 'RQBJ':
        p2_guesses_display += f"  - Blackjack Total: {p2_bets['bj_total']}\n"
        p2_guesses_display += f"  - Bust: {p2_bets['bust']}\n"
        p2_guesses_display += f"  - Opponent Color: {p2_bets['opp_color']}\n"
        if house_hand is not None:
            p2_guesses_display += f"  - Vs House: {p2_bets['vs_house']}\n"
    shell_print(p2_guesses_display, f"{player2.name}'s Guesses Revealed")

    # Player1 bets on Player2's guesses
    shell_print(f"{player1.name}'s Bets on {player2.name}'s Guesses:", f"{player1.name}'s Bets on {player2.name}")
    p1_on_p2 = {}
    for key, desc in [('hl', 'higher/lower'), ('suit', 'suit'), ('rank', 'rank')]:
        p1_on_p2[key] = get_guess(player1, f"is {player2.name}'s {desc} guess correct?", ['Correct', 'Incorrect'])
    if game_mode == 'RQBJ':
        p1_on_p2['bj_total'] = get_guess(player1, f"is {player2.name}'s blackjack total guess correct?", ['Correct', 'Incorrect'])
        p1_on_p2['bust'] = get_guess(player1, f"is {player2.name}'s bust guess correct?", ['Correct', 'Incorrect'])
        p1_on_p2['opp_color'] = get_guess(player1, f"is {player2.name}'s opponent color guess correct?", ['Correct', 'Incorrect'])
        if house_hand is not None:
            p1_on_p2['vs_house'] = get_guess(player1, f"is {player2.name}'s vs House guess correct?", ['Correct', 'Incorrect'])

    # Player2 bets on Player1's guesses
    shell_print(f"{player2.name}'s Bets on {player1.name}'s Guesses:", f"{player2.name}'s Bets on {player1.name}")
    p2_on_p1 = {}
    for key, desc in [('hl', 'higher/lower'), ('suit', 'suit'), ('rank', 'rank')]:
        p2_on_p1[key] = get_guess(player2, f"is {player1.name}'s {desc} guess correct?", ['Correct', 'Incorrect'])
    if game_mode == 'RQBJ':
        p2_on_p1['bj_total'] = get_guess(player2, f"is {player1.name}'s blackjack total guess correct?", ['Correct', 'Incorrect'])
        p2_on_p1['bust'] = get_guess(player2, f"is {player1.name}'s bust guess correct?", ['Correct', 'Incorrect'])
        p2_on_p1['opp_color'] = get_guess(player2, f"is {player1.name}'s opponent color guess correct?", ['Correct', 'Incorrect'])
        if house_hand is not None:
            p2_on_p1['vs_house'] = get_guess(player2, f"is {player1.name}'s vs House guess correct?", ['Correct', 'Incorrect'])

    # Display Player2's bets on Player1's guesses to Player1 (MOVED HERE FOR BOTH MODES)
    p2_bets_on_p1_display = f"{player2.name}'s Bets on {player1.name}'s Guesses (revealed for your grand bets):\n"
    p2_bets_on_p1_display += f"  - Higher/Lower: {p2_on_p1['hl']}\n"
    p2_bets_on_p1_display += f"  - Suit: {p2_on_p1['suit']}\n"
    p2_bets_on_p1_display += f"  - Rank: {p2_on_p1['rank']}\n"
    if game_mode == 'RQBJ':
        p2_bets_on_p1_display += f"  - Blackjack Total: {p2_on_p1['bj_total']}\n"
        p2_bets_on_p1_display += f"  - Bust: {p2_on_p1['bust']}\n"
        p2_bets_on_p1_display += f"  - Opponent Color: {p2_on_p1['opp_color']}\n"
        if house_hand is not None:
            p2_bets_on_p1_display += f"  - Vs House: {p2_on_p1['vs_house']}\n"
    shell_print(p2_bets_on_p1_display, f"{player2.name}'s Bets on {player1.name} Revealed")

    # RQBJ: Show cards before color declaration
    if game_mode == 'RQBJ':
        card_owner = "opponent's" if is_third_round else "your"
        shell_print(f"🔍 Color Declaration Phase (You may bluff {card_owner} card's color. Choose wisely...)", "Color Declaration")
        if player1.is_human:
            p1_sees_card.flip()
            shell_print(f"{player1.name}, {card_owner} card is: {p1_sees_card} (visible only to you)", f"{player1.name} - Secret Card")
            input("Press Enter to proceed...")
            p1_sees_card.flip()
        if player2.is_human:
            p2_sees_card.flip()
            shell_print(f"{player2.name}, {card_owner} card is: {p2_sees_card} (visible only to you)", f"{player2.name} - Secret Card")
            input("Press Enter to proceed...")
            p2_sees_card.flip()

        # Color declaration bets
        if is_third_round:
            shell_print(f"{player1.name}, declare the color of {player2.name}'s card (Red/Black, you may lie):", f"{player1.name}'s Color Declaration")
            p1_declare_color = get_guess(player1, "declare opponent's card color", ['Red', 'Black'])
            shell_print(f"{player2.name}, declare the color of {player1.name}'s card (Red/Black, you may lie):", f"{player2.name}'s Color Declaration")
            p2_declare_color = get_guess(player2, "declare opponent's card color", ['Red', 'Black'])
        else:
            shell_print(f"{player1.name}, declare the color of your card (Red/Black, you may lie):", f"{player1.name}'s Color Declaration")
            p1_declare_color = get_guess(player1, "declare your card color", ['Red', 'Black'])
            shell_print(f"{player2.name}, declare the color of your card (Red/Black, you may lie):", f"{player2.name}'s Color Declaration")
            p2_declare_color = get_guess(player2, "declare your card color", ['Red', 'Black'])

        # Belief in opponent's declaration
        if is_third_round:
            shell_print(f"{player2.name} declares your card is {p2_declare_color}. Is this correct?", f"{player1.name} - Believe Declaration")
            p1_believe_p2 = get_guess(player1, "believe opponent's color declaration", ['Correct', 'Incorrect'])
            shell_print(f"{player1.name} declares your card is {p1_declare_color}. Is this correct?", f"{player2.name} - Believe Declaration")
            p2_believe_p1 = get_guess(player2, "believe opponent's color declaration", ['Correct', 'Incorrect'])
        else:
            shell_print(f"{player2.name} declares their card is {p2_declare_color}. Is this correct?", f"{player1.name} - Believe Declaration")
            p1_believe_p2 = get_guess(player1, "believe opponent's color declaration", ['Correct', 'Incorrect'])
            shell_print(f"{player1.name} declares their card is {p1_declare_color}. Is this correct?", f"{player2.name} - Believe Declaration")
            p2_believe_p1 = get_guess(player2, "believe opponent's color declaration", ['Correct', 'Incorrect'])

    # Grand bets
    max_base = 14 if game_mode == 'RQBJ' else 6
    shell_print(f"{player1.name}'s Grand Bets (guess scores for bonus points):", f"{player1.name}'s Grand Bets")
    if player1.is_human and not (game_mode == 'RQBJ' and is_third_round):
        p1_card.flip()
        shell_print(f"{player1.name}, your card is: {p1_card} (visible only to you)", f"{player1.name} - Secret Card")
        input("Press Enter to proceed...")
        p1_card.flip()
    p1_guess_own = get_guess(player1, "guess your base points this round", max_val=max_base)
    p1_guess_opp = get_guess(player1, "guess opponent's base points this round", max_val=max_base)

    shell_print(f"{player2.name}'s Grand Bets (guess scores for bonus points):", f"{player2.name}'s Grand Bets")
    if player2.is_human and not (game_mode == 'RQBJ' and is_third_round):
        p2_card.flip()
        shell_print(f"{player2.name}, your card is: {p2_card} (visible only to you)", f"{player2.name} - Secret Card")
        input("Press Enter to proceed...")
        p2_card.flip()
    p2_guess_own = get_guess(player2, "guess your base points this round", max_val=max_base)
    p2_guess_opp = get_guess(player2, "guess opponent's base points this round", max_val=max_base)
    p1_grand_bets = {'own': p1_guess_own, 'opp': p1_guess_opp}
    p2_grand_bets = {'own': p2_guess_own, 'opp': p2_guess_opp}

    # RQBJ: Hit Me vote and bonus bet
    hit_me_card = None
    p1_hit_me = None
    p2_hit_me = None
    p1_bet_hit_me = None
    p2_bet_hit_me = None
    p1_bonus = 0
    p2_bonus = 0
    p1_bonus_details = []
    p2_bonus_details = []
    if game_mode == 'RQBJ':
        shell_print("🎯 Hit Me Voting Phase 🎯", "Hit Me Voting Phase")
        p1_hit_me = get_guess(player1, "do you want to request a Hit Me and vote to draw another card? (requires both players to vote Yes)", ['Yes', 'No'])
        p2_hit_me = get_guess(player2, "do you want to request a Hit Me and vote to draw another card? (requires both players to vote Yes)", ['Yes', 'No'])
        
        p1_bet_hit_me = get_guess(player1, f"do you bet that {player2.name} has voted Yes to the Hit Me request?", ['Yes', 'No'])
        p2_bet_hit_me = get_guess(player2, f"do you bet that {player1.name} has voted Yes to the Hit Me request?", ['Yes', 'No'])

        # Award bonus points for correct bets
        p1_bonus_hitme_result = "✅" if p1_bet_hit_me == p2_hit_me else "❌"
        if p1_bet_hit_me == p2_hit_me:
            p1_bonus += 1
            p1_bonus_details.append(f"Bet on {player2.name}'s Hit Me vote ({p1_bet_hit_me}): Correct (+1 point)")
        else:
            p1_bonus_details.append(f"Bet on {player2.name}'s Hit Me vote ({p1_bet_hit_me}): Incorrect")
        
        p2_bonus_hitme_result = "✅" if p2_bet_hit_me == p1_hit_me else "❌"
        if p2_bet_hit_me == p1_hit_me:
            p2_bonus += 1
            p2_bonus_details.append(f"Bet on {player1.name}'s Hit Me vote ({p2_bet_hit_me}): Correct (+1 point)")
        else:
            p2_bonus_details.append(f"Bet on {player1.name}'s Hit Me vote ({p2_bet_hit_me}): Incorrect")

        # Hit Me vote summary
        hit_me_summary = "🔍 Hit Me Summary:\n"
        hit_me_summary += f"- {player1.name} voted: {p1_hit_me}\n"
        hit_me_summary += f"- {player2.name} voted: {p2_hit_me}\n"
        hit_me_summary += f"- {player1.name} bet {player2.name} voted Yes: {p1_bet_hit_me} {p1_bonus_hitme_result}\n"
        hit_me_summary += f"- {player2.name} bet {player1.name} voted Yes: {p2_bet_hit_me} {p2_bonus_hitme_result}\n"

        # Check if a Hit Me card should be drawn
        if len(available) == 1:
            shell_print("Only one card remains! Forcing Hit Me card draw.", "Hit Me Forced")
            p1_hit_me = 'Yes'
            p2_hit_me = 'Yes'
        if p1_hit_me == 'Yes' and p2_hit_me == 'Yes' and available:
            picker = player2 if round_num % 2 == 1 else player1
            shell_print(f"Both players voted YES for Hit Me! Press Enter to draw the Hit Me card...", "Hit Me Draw")
            if picker.is_human:
                input()
            time.sleep(1)
            hit_me_pos = pick_position(picker, available)
            hit_me_card = table[hit_me_pos]
            hit_me_card.flip()
            available.remove(hit_me_pos)
            shell_print(f"Hit Me card: {hit_me_card}", "Hit Me Card")
            shell_print(hit_me_summary, "Hit Me Summary")
        elif p1_hit_me == 'Yes' and p2_hit_me == 'Yes' and not available:
            shell_print("No cards remain for Hit Me! Showing summary...", "Hit Me Summary")
            shell_print(hit_me_summary, "Hit Me Summary")
        else:
            shell_print("Hit Me not requested by both players.", "Hit Me Summary")
            shell_print(hit_me_summary, "Hit Me Summary")

    # Calculate blackjack total
    bj_total = 0
    bj_bonus = 0
    if game_mode == 'RQBJ':
        bj_total = p1_card.get_blackjack_value() + p2_card.get_blackjack_value()
        num_aces = (1 if p1_card.rank == 'Ace' else 0) + (1 if p2_card.rank == 'Ace' else 0)
        if hit_me_card:
            bj_total += hit_me_card.get_blackjack_value()
            if hit_me_card.rank == 'Ace':
                num_aces += 1
        while bj_total > 21 and num_aces > 0:
            bj_total -= 10
            num_aces -= 1
        is_bust = bj_total > 21

    # Calculate higher/lower
    is_p1_higher = p1_card > p2_card
    is_p1_lower = p1_card < p2_card
    is_tie = p1_card.rank == p2_card.rank

    # Player1 base points
    p1_base = 0
    p1_base_details = []
    if not is_tie:
        if (p1_bets['hl'] == 'Higher' and is_p1_higher) or (p1_bets['hl'] == 'Lower' and is_p1_lower):
            p1_base += 1
            p1_base_details.append(f"Higher/Lower: {p1_bets['hl']} (Correct)")
        else:
            p1_base_details.append(f"Higher/Lower: {p1_bets['hl']} (Incorrect)")
    else:
        p1_base_details.append(f"Higher/Lower: {p1_bets['hl']} (No points, tie)")
    if p1_bets['suit'] == p1_card.suit:
        p1_base += 1
        p1_base_details.append(f"Suit: {p1_bets['suit']} (Correct)")
    else:
        p1_base_details.append(f"Suit: {p1_bets['suit']} (Incorrect)")
    if p1_bets['rank'] == p1_card.rank:
        p1_base += 1
        p1_base_details.append(f"Rank: {p1_bets['rank']} (Correct)")
    else:
        p1_base_details.append(f"Rank: {p1_bets['rank']} (Incorrect)")

    # Player2 base points
    p2_base = 0
    p2_base_details = []
    if not is_tie:
        if (p2_bets['hl'] == 'Higher' and not is_p1_higher) or (p2_bets['hl'] == 'Lower' and not is_p1_lower):
            p2_base += 1
            p2_base_details.append(f"Higher/Lower: {p2_bets['hl']} (Correct)")
        else:
            p2_base_details.append(f"Higher/Lower: {p2_bets['hl']} (Incorrect)")
    else:
        p2_base_details.append(f"Higher/Lower: {p2_bets['hl']} (No points, tie)")
    if p2_bets['suit'] == p2_card.suit:
        p2_base += 1
        p2_base_details.append(f"Suit: {p2_bets['suit']} (Correct)")
    else:
        p2_base_details.append(f"Suit: {p2_bets['suit']} (Incorrect)")
    if p2_bets['rank'] == p2_card.rank:
        p2_base += 1
        p2_base_details.append(f"Rank: {p2_bets['rank']} (Correct)")
    else:
        p2_base_details.append(f"Rank: {p2_bets['rank']} (Incorrect)")

    # Bets on opponent's guesses
    p1_hl_correct = not is_tie and ((p1_bets['hl'] == 'Higher' and is_p1_higher) or (p1_bets['hl'] == 'Lower' and is_p1_lower))
    p1_suit_correct = p1_bets['suit'] == p1_card.suit
    p1_rank_correct = p1_bets['rank'] == p1_card.rank
    p2_hl_correct = not is_tie and ((p2_bets['hl'] == 'Higher' and not is_p1_higher) or (p2_bets['hl'] == 'Lower' and not is_p1_lower))
    p2_suit_correct = p2_bets['suit'] == p2_card.suit
    p2_rank_correct = p2_bets['rank'] == p2_card.rank

    for key, actual in [('hl', p2_hl_correct), ('suit', p2_suit_correct), ('rank', p2_rank_correct)]:
        if (p1_on_p2[key] == 'Correct' and actual) or (p1_on_p2[key] == 'Incorrect' and not actual):
            p1_base += 1
            p1_base_details.append(f"Bet on {player2.name}'s {key}: {p1_on_p2[key]} (Correct)")
        else:
            p1_base_details.append(f"Bet on {player2.name}'s {key}: {p1_on_p2[key]} (Incorrect)")
    for key, actual in [('hl', p1_hl_correct), ('suit', p1_suit_correct), ('rank', p1_rank_correct)]:
        if (p2_on_p1[key] == 'Correct' and actual) or (p2_on_p1[key] == 'Incorrect' and not actual):
            p2_base += 1
            p2_base_details.append(f"Bet on {player1.name}'s {key}: {p2_on_p1[key]} (Correct)")
        else:
            p2_base_details.append(f"Bet on {player1.name}'s {key}: {p2_on_p1[key]} (Incorrect)")

    # RQBJ additional bets
    if game_mode == 'RQBJ':
        if p1_bets['bj_total'] == str(bj_total):
            p1_base += 1
            p1_base_details.append(f"Blackjack Total: {p1_bets['bj_total']} (Correct)")
        else:
            p1_base_details.append(f"Blackjack Total: {p1_bets['bj_total']} (Incorrect)")
        if (p1_bets['bust'] == 'Yes' and is_bust) or (p1_bets['bust'] == 'No' and not is_bust):
            p1_base += 1
            p1_base_details.append(f"Bust: {p1_bets['bust']} (Correct)")
        else:
            p1_base_details.append(f"Bust: {p1_bets['bust']} (Incorrect)")
        if p1_bets['opp_color'] == p2_card.color:
            p1_base += 1
            p1_base_details.append(f"Opponent Color: {p1_bets['opp_color']} (Correct)")
        else:
            p1_base_details.append(f"Opponent Color: {p1_bets['opp_color']} (Incorrect)")
        if house_hand is not None:
            if bj_total > house_hand and p1_bets['vs_house'] == 'Higher':
                p1_base += 1
                p1_base_details.append(f"Vs House: {p1_bets['vs_house']} (Correct)")
            elif bj_total < house_hand and p1_bets['vs_house'] == 'Lower':
                p1_base += 1
                p1_base_details.append(f"Vs House: {p1_bets['vs_house']} (Correct)")
            elif bj_total == house_hand and p1_bets['vs_house'] == 'Tie':
                p1_base += 1
                p1_base_details.append(f"Vs House: {p1_bets['vs_house']} (Correct)")
            else:
                p1_base_details.append(f"Vs House: {p1_bets['vs_house']} (Incorrect)")

        if p2_bets['bj_total'] == str(bj_total):
            p2_base += 1
            p2_base_details.append(f"Blackjack Total: {p2_bets['bj_total']} (Correct)")
        else:
            p2_base_details.append(f"Blackjack Total: {p2_bets['bj_total']} (Incorrect)")
        if (p2_bets['bust'] == 'Yes' and is_bust) or (p2_bets['bust'] == 'No' and not is_bust):
            p2_base += 1
            p2_base_details.append(f"Bust: {p2_bets['bust']} (Correct)")
        else:
            p2_base_details.append(f"Bust: {p2_bets['bust']} (Incorrect)")
        if p2_bets['opp_color'] == p1_card.color:
            p2_base += 1
            p2_base_details.append(f"Opponent Color: {p2_bets['opp_color']} (Correct)")
        else:
            p2_base_details.append(f"Opponent Color: {p2_bets['opp_color']} (Incorrect)")
        if house_hand is not None:
            if bj_total > house_hand and p2_bets['vs_house'] == 'Higher':
                p2_base += 1
                p2_base_details.append(f"Vs House: {p2_bets['vs_house']} (Correct)")
            elif bj_total < house_hand and p2_bets['vs_house'] == 'Lower':
                p2_base += 1
                p2_base_details.append(f"Vs House: {p2_bets['vs_house']} (Correct)")
            elif bj_total == house_hand and p2_bets['vs_house'] == 'Tie':
                p2_base += 1
                p2_base_details.append(f"Vs House: {p2_bets['vs_house']} (Correct)")
            else:
                p2_base_details.append(f"Vs House: {p2_bets['vs_house']} (Incorrect)")

        # Bets on opponent's additional guesses
        for key, actual in [
            ('bj_total', p2_bets['bj_total'] == str(bj_total)),
            ('bust', (p2_bets['bust'] == 'Yes' and is_bust) or (p2_bets['bust'] == 'No' and not is_bust)),
            ('opp_color', p2_bets['opp_color'] == p1_card.color)
        ]:
            if (p1_on_p2[key] == 'Correct' and actual) or (p1_on_p2[key] == 'Incorrect' and not actual):
                p1_base += 1
                p1_base_details.append(f"Bet on {player2.name}'s {key}: {p1_on_p2[key]} (Correct)")
            else:
                p1_base_details.append(f"Bet on {player2.name}'s {key}: {p1_on_p2[key]} (Incorrect)")
        if house_hand is not None:
            is_higher = bj_total > house_hand
            is_tie = bj_total == house_hand
            actual_vs_house = (p2_bets['vs_house'] == 'Higher' and is_higher) or \
                              (p2_bets['vs_house'] == 'Lower' and not is_higher and not is_tie) or \
                              (p2_bets['vs_house'] == 'Tie' and is_tie)
            if (p1_on_p2['vs_house'] == 'Correct' and actual_vs_house) or \
               (p1_on_p2['vs_house'] == 'Incorrect' and not actual_vs_house):
                p1_base += 1
                p1_base_details.append(f"Bet on {player2.name}'s vs_house: {p1_on_p2['vs_house']} (Correct)")
            else:
                p1_base_details.append(f"Bet on {player2.name}'s vs_house: {p1_on_p2['vs_house']} (Incorrect)")

        for key, actual in [
            ('bj_total', p1_bets['bj_total'] == str(bj_total)),
            ('bust', (p1_bets['bust'] == 'Yes' and is_bust) or (p1_bets['bust'] == 'No' and not is_bust)),
            ('opp_color', p1_bets['opp_color'] == p2_card.color)
        ]:
            if (p2_on_p1[key] == 'Correct' and actual) or (p2_on_p1[key] == 'Incorrect' and not actual):
                p2_base += 1
                p2_base_details.append(f"Bet on {player1.name}'s {key}: {p2_on_p1[key]} (Correct)")
            else:
                p2_base_details.append(f"Bet on {player1.name}'s {key}: {p2_on_p1[key]} (Incorrect)")
        if house_hand is not None:
            is_higher = bj_total > house_hand
            is_tie = bj_total == house_hand
            actual_vs_house = (p1_bets['vs_house'] == 'Higher' and is_higher) or \
                              (p1_bets['vs_house'] == 'Lower' and not is_higher and not is_tie) or \
                              (p1_bets['vs_house'] == 'Tie' and is_tie)
            if (p2_on_p1['vs_house'] == 'Correct' and actual_vs_house) or \
               (p2_on_p1['vs_house'] == 'Incorrect' and not actual_vs_house):
                p2_base += 1
                p2_base_details.append(f"Bet on {player1.name}'s vs_house: {p2_on_p1['vs_house']} (Correct)")
            else:
                p2_base_details.append(f"Bet on {player1.name}'s vs_house: {p2_on_p1['vs_house']} (Incorrect)")

        # Color declaration scoring
        if is_third_round:
            if (p1_believe_p2 == 'Correct' and p2_declare_color == p1_card.color) or \
               (p1_believe_p2 == 'Incorrect' and p2_declare_color != p1_card.color):
                p1_base += 1
                p1_base_details.append(f"Believed {player2.name}'s declaration of your card ({p2_declare_color}): {p1_believe_p2} (Correct)")
            else:
                p2_base += 1
                p1_base_details.append(f"Believed {player2.name}'s declaration of your card ({p2_declare_color}): {p1_believe_p2} (Incorrect)")
                p2_base_details.append(f"{player1.name} misjudged your color declaration (Correct)")
            
            if (p2_believe_p1 == 'Correct' and p1_declare_color == p2_card.color) or \
               (p2_believe_p1 == 'Incorrect' and p1_declare_color != p2_card.color):
                p2_base += 1
                p2_base_details.append(f"Believed {player1.name}'s declaration of your card ({p1_declare_color}): {p2_believe_p1} (Correct)")
            else:
                p1_base += 1
                p2_base_details.append(f"Believed {player1.name}'s declaration of your card ({p1_declare_color}): {p2_believe_p1} (Incorrect)")
                p1_base_details.append(f"{player2.name} misjudged your color declaration (Correct)")
        else:
            if (p1_believe_p2 == 'Correct' and p2_declare_color == p2_card.color) or \
               (p1_believe_p2 == 'Incorrect' and p2_declare_color != p2_card.color):
                p1_base += 1
                p1_base_details.append(f"Believed {player2.name}'s declaration of their card ({p2_declare_color}): {p1_believe_p2} (Correct)")
            else:
                p2_base += 1
                p1_base_details.append(f"Believed {player2.name}'s declaration of their card ({p2_declare_color}): {p1_believe_p2} (Incorrect)")
                p2_base_details.append(f"{player1.name} misjudged your color declaration (Correct)")
            
            if (p2_believe_p1 == 'Correct' and p1_declare_color == p1_card.color) or \
               (p2_believe_p1 == 'Incorrect' and p1_declare_color != p1_card.color):
                p2_base += 1
                p2_base_details.append(f"Believed {player1.name}'s declaration of their card ({p1_declare_color}): {p2_believe_p1} (Correct)")
            else:
                p1_base += 1
                p2_base_details.append(f"Believed {player1.name}'s declaration of their card ({p1_declare_color}): {p2_believe_p1} (Incorrect)")
                p1_base_details.append(f"{player2.name} misjudged your color declaration (Correct)")

    # Blackjack 21 bonus
    if game_mode == 'RQBJ' and bj_total == 21:
        bj_bonus = 2 if round_num == 21 else 1
        p1_base += bj_bonus
        p2_base += bj_bonus
        p1_base_details.append(f"Blackjack 21 Bonus: {'Double ' if round_num == 21 else ''}+{bj_bonus}")
        p2_base_details.append(f"Blackjack 21 Bonus: {'Double ' if round_num == 21 else ''}+{bj_bonus}")

    # Grand points
    p1_grand = 0
    p1_grand_details = []
    if p1_grand_bets['own'] == p1_base:
        p1_grand += 1
        p1_grand_details.append(f"Guessed own score ({p1_grand_bets['own']}): Correct")
    else:
        p1_grand_details.append(f"Guessed own score ({p1_grand_bets['own']}): Incorrect (off by {abs(p1_grand_bets['own'] - p1_base)} points)")
    if p1_grand_bets['opp'] == p2_base:
        p1_grand += 1
        p1_grand_details.append(f"Guessed opponent score ({p1_grand_bets['opp']}): Correct")
    else:
        p1_grand_details.append(f"Guessed opponent score ({p1_grand_bets['opp']}): Incorrect (off by {abs(p1_grand_bets['opp'] - p2_base)} points)")

    p2_grand = 0
    p2_grand_details = []
    if p2_grand_bets['own'] == p2_base:
        p2_grand += 1
        p2_grand_details.append(f"Guessed own score ({p2_grand_bets['own']}): Correct")
    else:
        p2_grand_details.append(f"Guessed own score ({p2_grand_bets['own']}): Incorrect (off by {abs(p2_grand_bets['own'] - p2_base)} points)")
    if p2_grand_bets['opp'] == p1_base:
        p2_grand += 1
        p2_grand_details.append(f"Guessed opponent score ({p2_grand_bets['opp']}): Correct")
    else:
        p2_grand_details.append(f"Guessed opponent score ({p2_grand_bets['opp']}): Incorrect (off by {abs(p2_grand_bets['opp'] - p1_base)} points)")

    # Reveal cards
    print("\n🃏 Revealing cards...")
    p1_card.flip()
    p2_card.flip()
    display_table(table)
    content = f"{player1.name}'s card: {p1_card}\n"
    content += f"{player2.name}'s card: {p2_card}\n"
    if game_mode == 'RQBJ':
        content += f"🎲 Blackjack Total: {bj_total}{' (Bust)' if is_bust else ''}\n"
        if hit_me_card:
            content += f"Hit Me Card: {hit_me_card}\n"
        if house_hand is not None:
            content += f"🏛️ House Dealer's Hand: {house_hand}\n"
    shell_print(content, "Card Reveal")

    # Display round summaries
    content = f"📊 {player1.name}'s Round Summary:\n"
    content += "  Your Guesses:\n"
    for detail in p1_base_details[:3]:
        content += f"    - {detail}\n"
    content += "  Bets on Opponent's Guesses:\n"
    for detail in p1_base_details[3:6]:
        content += f"    - {detail}\n"
    if game_mode == 'RQBJ':
        content += "  Blackjack Guesses:\n"
        for detail in p1_base_details[6:9 + (1 if house_hand is not None else 0)]:
            content += f"    - {detail}\n"
        content += "  Bets on Opponent's Blackjack Guesses:\n"
        for detail in p1_base_details[9 + (1 if house_hand is not None else 0):12 + (1 if house_hand is not None else 0)]:
            content += f"    - {detail}\n"
        content += "  Color Declaration Bets:\n"
        for detail in p1_base_details:
            if 'color declaration' in detail.lower():
                content += f"    - {detail}\n"
        if bj_total == 21:
            content += "  Bonuses:\n"
            for detail in p1_base_details:
                if 'blackjack 21 bonus' in detail.lower():
                    content += f"    - {detail}\n"
    content += "  Grand Bets:\n"
    for detail in p1_grand_details:
        content += f"    - {detail}\n"
    if game_mode == 'RQBJ' and p1_bonus_details:
        content += "  Hit Me Bonus Bets:\n"
        for detail in p1_bonus_details:
            content += f"    - {detail}\n"
    content += f"  Total Round Points: {p1_base + p1_grand + p1_bonus} (Base: {p1_base} {display_score(p1_base)}, Grand: {p1_grand} {display_score(p1_grand)}, Bonus: {p1_bonus} {display_score(p1_bonus)})\n"
    shell_print(content, f"{player1.name}'s Round Summary")

    content = f"📊 {player2.name}'s Round Summary:\n"
    content += "  Your Guesses:\n"
    for detail in p2_base_details[:3]:
        content += f"    - {detail}\n"
    content += "  Bets on Opponent's Guesses:\n"
    for detail in p2_base_details[3:6]:
        content += f"    - {detail}\n"
    if game_mode == 'RQBJ':
        content += "  Blackjack Guesses:\n"
        for detail in p2_base_details[6:9 + (1 if house_hand is not None else 0)]:
            content += f"    - {detail}\n"
        content += "  Bets on Opponent's Blackjack Guesses:\n"
        for detail in p2_base_details[9 + (1 if house_hand is not None else 0):12 + (1 if house_hand is not None else 0)]:
            content += f"    - {detail}\n"
        content += "  Color Declaration Bets:\n"
        for detail in p2_base_details:
            if 'color declaration' in detail.lower():
                content += f"    - {detail}\n"
        if bj_total == 21:
            content += "  Bonuses:\n"
            for detail in p2_base_details:
                if 'blackjack 21 bonus' in detail.lower():
                    content += f"    - {detail}\n"
    content += "  Grand Bets:\n"
    for detail in p2_grand_details:
        content += f"    - {detail}\n"
    if game_mode == 'RQBJ' and p2_bonus_details:
        content += "  Hit Me Bonus Bets:\n"
        for detail in p2_bonus_details:
            content += f"    - {detail}\n"
    content += f"  Total Round Points: {p2_base + p2_grand + p2_bonus} (Base: {p2_base} {display_score(p2_base)}, Grand: {p2_grand} {display_score(p2_grand)}, Bonus: {p2_bonus} {display_score(p2_bonus)})\n"
    shell_print(content, f"{player2.name}'s Round Summary")

    # Update scores
    player1.score += p1_base + p1_grand + p1_bonus
    player2.score += p2_base + p2_grand + p2_bonus
    player1.base_scores.append(p1_base)
    player1.grand_scores.append(p1_grand)
    player1.bonus_scores.append(p1_bonus)
    player2.base_scores.append(p2_base)
    player2.grand_scores.append(p2_grand)
    player2.bonus_scores.append(p2_bonus)

    content = f"🏆 Total Scores: {player1.name}: {player1.score} {display_score(player1.score)}, {player2.name}: {player2.score} {display_score(player2.score)}\n"
    shell_print(content, "Total Scores")

    # Check if game should end due to insufficient cards
    if len(available) < 2:
        shell_print("Not enough cards to continue! Game will end after this round.", "Game End")
        return bj_total if game_mode == 'RQBJ' else None, True
    
    return bj_total if game_mode == 'RQBJ' else None, False

def main():
    try:
        print("🌈 Initializing Rainbow Quest Blackjack...")
        global EMOJI_SHIFT
        try:
            config_path = os.path.join(os.path.dirname(__file__), "config_logs")
        except NameError:
            config_path = os.path.join(os.getcwd(), "config_logs")
        EMOJI_SHIFT = load_shift(config_path)  # Load or calibrate emoji shift
        print("🌈 Calibration complete! Ready to play Rainbow Quest Blackjack! 🌈\n")

        while True:
            content = "🎉 Welcome to Rainbow Quest! 🎉\n\n"
            content += "Rainbow Quest is a strategic card game for two players (you vs. an AI opponent) using a standard 52-card deck, played over up to 26 rounds. Each round, you pick cards from a table, make guesses about your card and the game state, bet on your opponent's guesses, and score points based on accuracy. The goal is to outscore your opponent.\n\n"
            content += "Choose from two game modes:\n\n"
            content += "1. Rainbow Quest (RQ):\n"
            content += "   - Pick one card per round from a 52-card table.\n"
            content += "   - Guess your card's higher/lower value (relative to opponent's), suit, and rank (up to 3 points).\n"
            content += "   - Bet on whether opponent's guesses are correct (up to 3 points).\n"
            content += "   - See your card and opponent's bets, then guess your and opponent's base scores (up to 2 points).\n"
            content += "   - Cards revealed at round's end.\n"
            content += "   - Max 8 points/round (6 base + 2 grand).\n\n"
            content += "2. Rainbow Quest Blackjack (RQBJ):\n"
            content += "   - Extends RQ with blackjack mechanics.\n"
            content += "   - Additional guesses: blackjack total (sum of both cards, 2-21), bust (yes/no), opponent's card color (up to 3 points).\n"
            content += "   - Bet on opponent's blackjack guesses (up to 4 points).\n"
            content += "   - Color declaration: Non-3rd rounds (1,2,4,5,...), declare your card's color (Red/Black, can lie) and opponent bets on if they believe it matches your card; 3rd rounds (3,6,9,...), declare opponent's card color and opponent bets on if they believe it matches their card (up to 2 points).\n"
            content += "   - Every 3rd round, see opponent's card instead of yours for color declaration.\n"
            content += "   - Blackjack 21 bonus: +1 point if total is 21 (+2 on round 21).\n"
            content += "   - House Dealer's Hand: After round 1, guess if your blackjack total is higher/lower/tied with the previous round's total (1 point).\n"
            content += "   - Hit Me: After grand bets, vote to draw an extra card (both must vote Yes); bet on opponent's vote (1 bonus point). If drawn, non-first player picks card, added to blackjack total. If only one card remains, it's forced as Hit Me card. Game ends if <2 cards remain.\n"
            content += "   - Max 17 points/round (14 base + 2 grand + 1 bonus, or 15 base on round 21).\n\n"
            content += "Game Notes:\n"
            content += "   - Higher/lower: Card order is Ace (1, except < 2), 2, 3, ..., 10, Jack (11), Queen (12), King (13). Ties only on same rank.\n"
            content += "   - Blackjack totals (RQBJ): 2-10 (face value), Jack/Queen/King (10), Ace (11 or 1 to avoid bust).\n"
            content += "   - Exit by typing '!@exit@!' at round's end.\n"
            content += "   - Victory screen shows winner and score breakdown after 26 rounds or when cards run out.\n\n"
            content += "Press Enter to continue..."
            shell_print(content, "Game Introduction")
            input()
            
            content = "Welcome to Rainbow Quest!\n"
            content += "Choose game mode:\n"
            content += "1. Rainbow Quest (RQ)\n"
            content += "2. Rainbow Quest Blackjack (RQBJ)\n"
            shell_print(content, "Game Mode Selection")
            choice = input("Enter 1 or 2: ")
            while choice not in ['1', '2']:
                print("Please enter 1 or 2.")
                choice = input("Enter 1 or 2: ")
            game_mode = 'RQ' if choice == '1' else 'RQBJ'

            content = "Choose opponent for Player 2:\n"
            content += "1. Phi (AI)\n"
            content += "2. Mistral (AI)\n"
            content += "3. Llama (AI)\n"
            content += "4. Computer (random)\n"
            shell_print(content, "Opponent Selection")
            while True:
                try:
                    ai_choice = int(input("Enter 1, 2, 3, or 4: "))
                    if ai_choice == 1:
                        player2_model = "phi"
                        player2_name = "Phi"
                        break
                    elif ai_choice == 2:
                        player2_model = "mistral"
                        player2_name = "Mistral"
                        break
                    elif ai_choice == 3:
                        player2_model = "llama2"
                        player2_name = "Llama"
                        break
                    elif ai_choice == 4:
                        player2_model = None
                        player2_name = "Computer"
                        break
                    else:
                        shell_print("Invalid choice. Please enter 1, 2, 3, or 4.", "Error")
                except ValueError:
                    shell_print("Please enter a valid number.", "Error")

            deck = generate_deck()
            random.shuffle(deck)
            table = deck
            available = set(range(52))

            content = "🃏 Shuffling and dealing cards...\n"
            for i in range(52):
                table[i].face_up = False
                content += f"Dealing card {i+1}...\n"
                shell_print(content, "Dealing Cards")
                display_table(table)
                time.sleep(0.05)
                content = "🃏 Shuffling and dealing cards...\n"

            player1 = Player("Player1 (Human)", True)
            player2 = Player(f"Player2 ({player2_name})", False, model=player2_model)
            round_catalogue = ['round.1']
            house_hand = None

            for round_num in range(1, 27):
                if not round_catalogue:
                    print("No more round types!")
                    break

                round_type = random.choice(round_catalogue)
                if round_type == 'round.1':
                    result = play_round_type1(player1, player2, table, available, round_num, game_mode, house_hand)
                    house_hand = result[0] if game_mode == 'RQBJ' else None
                    should_end = result[1] if game_mode == 'RQBJ' else False
                    if should_end:
                        display_victory_screen(player1, player2)
                        input("Press Enter...")
                        input("Press Enter again to start a new game...")
                        break
                    if len(available) < 2:
                        print("Not enough cards to continue!")
                        display_victory_screen(player1, player2)
                        input("Press Enter...")
                        input("Press Enter again to start a new game...")
                        break

                content = "Press Enter for next round or type '!@exit@!' to quit: "
                shell_print(content, "Round Transition")
                user_input = input()
                if user_input.strip() == "!@exit@!":
                    print("Exiting game. Goodbye!")
                    break

            display_victory_screen(player1, player2)
            input("Press Enter...")
            input("Press Enter again to start a new game...")

    except Exception as e:
        handle_symbolic_error(e, "Main Game Loop")
        print("Game terminated due to an error. Please restart.")
        sys.exit(1)

if __name__ == "__main__":
    main()

# LICENSE.TXT
# 0ko3maibZer00logyLicensev1.09
# Zer00logy License v1.09
# September 25, 2025
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
#- README.md
#- README_0KO3MAIB.txt
#- LICENSE.txt
#- 0ko3maibZer00logyLicensev01.txt
#- rainbowquest1000.py
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
#© Stacey8Szmy — Zer00logy IP Archive
