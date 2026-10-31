"""
lazymc ui module
Handles terminal styling, ANSI boxes, menus, and user interactions.
"""

import os
import sys
import re
from pathlib import Path
from i18n import i18n

# ANSI Color codes
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_GRAY = "\033[90m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_MAGENTA = "\033[95m"
C_CYAN = "\033[96m"
C_WHITE = "\033[97m"


APP_VERSION = "v0.2.0"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}")
    print(r"  _                                   ")
    print(r" | | __ _ _____   _ _ __ ___   ___    ")
    print(r" | |/ _` |_  / | | | '_ ` _ \ / __|   ")
    print(r" | | (_| |/ /| |_| | | | | | | (__    ")
    print(r" |_|\__,_/___|\__, |_| |_| |_|\___|   ")
    print(f"              |___/{' ' * 31}{C_GRAY}{C_BOLD}{APP_VERSION}{C_RESET}")
    print(f"{C_RESET}{C_GRAY} ────────────────────────────────────────────────────────{C_RESET}")


def strip_ansi(text: str) -> str:
    return re.sub(r'\033\[[0-9;]*m', '', text)


def wrap_text(line: str, max_width: int) -> list:
    """Wraps text gracefully so it fits within max_width without breaking box borders."""
    if len(strip_ansi(line)) <= max_width:
        return [line]

    words = line.split(" ")
    res = []
    cur = ""
    for w in words:
        if not cur:
            cur = w
        elif len(strip_ansi(cur + " " + w)) <= max_width:
            cur += " " + w
        else:
            res.append(cur)
            cur = w
    if cur:
        res.append(cur)
    return res if res else [line]


def draw_box(title: str, content_lines: list, width: int = 68):
    border_color = C_GRAY
    inner_width = width - 2
    title_colored = f"{C_CYAN}{C_BOLD}{title.center(inner_width)}{C_RESET}"

    print(f"{border_color}┌{'─' * inner_width}┐{C_RESET}")
    print(f"{border_color}│{title_colored}{border_color}│{C_RESET}")
    print(f"{border_color}├{'─' * inner_width}┤{C_RESET}")

    for line in content_lines:
        wrapped_sublines = wrap_text(line, inner_width - 2)
        for sub in wrapped_sublines:
            raw_len = len(strip_ansi(sub))
            pad = inner_width - 2 - raw_len
            if pad < 0:
                pad = 0
            print(f"{border_color}│{C_RESET} {sub}{' ' * pad} {border_color}│{C_RESET}")

    print(f"{border_color}└{'─' * inner_width}┘{C_RESET}")


def render_progress_bar(done: int, total: int, prefix: str = "", length: int = 30):
    if total <= 0:
        percent = 100
        filled = length
    else:
        percent = min(100, int(100 * done / total))
        filled = int(length * done // total)

    bar = f"{C_GREEN}{'█' * filled}{C_GRAY}{'░' * (length - filled)}{C_RESET}"
    sys.stdout.write(f"\r  {prefix:<22} [{bar}] {C_WHITE}{percent:>3}%{C_RESET} ({done}/{total})")
    sys.stdout.flush()
    if done >= total and total > 0:
        print()


def get_installed_versions(game_dir: str) -> list:
    """Returns a list of versions installed in game_dir/versions that have a .json and .jar"""
    ver_dir = os.path.join(game_dir, "versions")
    if not os.path.exists(ver_dir):
        return []
    installed = []
    try:
        for entry in os.scandir(ver_dir):
            if entry.is_dir():
                v_name = entry.name
                v_json = os.path.join(entry.path, f"{v_name}.json")
                v_jar = os.path.join(entry.path, f"{v_name}.jar")
                if os.path.exists(v_json) and os.path.exists(v_jar):
                    installed.append(v_name)
    except Exception:
        pass
    return sorted(installed, reverse=True)
