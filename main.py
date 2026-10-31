"""
lazymc
Main CLI & interactive entry point.
"""

import os
import sys
import io
import time

# Force UTF-8 in Windows Terminal / Console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from i18n import i18n
from config import load_config, save_config, DEFAULT_CONFIG
from java_detector import find_all_javas, resolve_best_java, get_required_java_version, get_java_version
from mojang import fetch_manifest, download_full_version, check_missing_dependencies
from launcher import launch_game
from ui import (
    clear_screen, print_banner, draw_box, render_progress_bar,
    get_installed_versions, C_RESET, C_BOLD, C_GRAY, C_RED,
    C_GREEN, C_YELLOW, C_CYAN, C_WHITE
)


def format_status_panel(config: dict) -> list:
    active_ver = config.get("active_version") or i18n("status_no_version")
    ver_color = C_GREEN if config.get("active_version") else C_RED

    # Determine java display
    j_path = config.get("java_path", "auto")
    if j_path == "auto":
        req = get_required_java_version(config.get("active_version", ""))
        resolved = resolve_best_java("auto", req)
        ver_num = get_java_version(resolved)
        java_display = f"Auto (Java {ver_num})" if ver_num else "Auto (not found)"
    else:
        ver_num = get_java_version(j_path)
        java_display = f"Custom (Java {ver_num})" if ver_num else os.path.basename(j_path)

    lang_code = config.get("language", "auto")
    lang_labels = {"auto": i18n("lang_auto"), "ru": "Русский", "uk": "Українська", "en": "English"}
    lang_display = f"{lang_labels.get(lang_code, lang_code)} ({i18n.resolved_lang.upper()})"

    return [
        f"{C_YELLOW}{i18n('user')}:{C_RESET}       {C_WHITE}{config.get('username')}{C_RESET}",
        f"{C_YELLOW}{i18n('ram')}:{C_RESET}        {C_WHITE}{config.get('ram_gb')} GB{C_RESET}",
        f"{C_YELLOW}{i18n('version')}:{C_RESET}    {ver_color}{active_ver}{C_RESET}",
        f"{C_YELLOW}{i18n('java')}:{C_RESET}   {C_WHITE}{java_display}{C_RESET}",
        f"{C_YELLOW}{i18n('lang')}:{C_RESET}       {C_WHITE}{lang_display}{C_RESET}",
    ]


def menu_change_nick(config: dict):
    print_banner()
    draw_box(i18n("nick_title"), [
        f"{i18n('current_nick')}: {C_YELLOW}{config.get('username')}{C_RESET}"
    ])
    print()
    new_nick = input(f"{C_CYAN}{i18n('enter_nick')}{C_RESET}").strip()
    if new_nick:
        config["username"] = new_nick
        save_config(config)
        print(f"\n {C_GREEN}✓ {i18n('nick_saved')}{C_RESET}")
        time.sleep(1)


def menu_settings(config: dict):
    while True:
        print_banner()
        lines = [
            f"{C_CYAN}[1]{C_RESET} {i18n('set_ram_opt', ram=config.get('ram_gb'))}",
            f"{C_CYAN}[2]{C_RESET} {i18n('set_java_opt', java=config.get('java_path'))}",
            f"{C_CYAN}[3]{C_RESET} {i18n('set_dir_opt', dir=config.get('game_dir'))}",
            f"{C_CYAN}[4]{C_RESET} {i18n('set_jvm_opt', args=config.get('jvm_args'))}",
            f"{C_YELLOW}[5]{C_RESET} {i18n('back_to_menu')}",
        ]
        draw_box(i18n("settings_title"), lines)
        choice = input(f"\n{C_CYAN}{i18n('enter_choice')}{C_RESET}").strip()

        if choice == "1":
            ram_input = input(f"\n{C_CYAN}{i18n('enter_ram')}{C_RESET}").strip()
            if ram_input.isdigit() and int(ram_input) > 0:
                config["ram_gb"] = int(ram_input)
                save_config(config)
                print(f" {C_GREEN}✓ {i18n('settings_saved')}{C_RESET}")
                time.sleep(1)
            else:
                print(f" {C_RED}✗ {i18n('invalid_ram')}{C_RESET}")
                time.sleep(1.5)
        elif choice == "2":
            menu_select_java(config)
        elif choice == "3":
            new_dir = input(f"\n{C_CYAN}Game Directory (Enter to keep): {C_RESET}").strip()
            if new_dir:
                config["game_dir"] = os.path.normpath(new_dir)
                save_config(config)
                print(f" {C_GREEN}✓ {i18n('settings_saved')}{C_RESET}")
                time.sleep(1)
        elif choice == "4":
            new_args = input(f"\n{C_CYAN}JVM extra arguments: {C_RESET}").strip()
            config["jvm_args"] = new_args
            save_config(config)
            print(f" {C_GREEN}✓ {i18n('settings_saved')}{C_RESET}")
            time.sleep(1)
        elif choice == "5":
            break


def menu_select_java(config: dict):
    print_banner()
    javas = find_all_javas()
    lines = [f"{C_CYAN}[0]{C_RESET} {i18n('java_auto')}"]
    for i, j in enumerate(javas, 1):
        lines.append(f"{C_CYAN}[{i}]{C_RESET} Java {j['version']} -> {j['path']}")

    draw_box("JAVA SELECTOR", lines, width=70)
    choice = input(f"\n{C_CYAN}{i18n('java_select')}{C_RESET}").strip()
    if choice == "0" or choice == "":
        config["java_path"] = "auto"
        save_config(config)
    elif choice.isdigit() and 1 <= int(choice) <= len(javas):
        config["java_path"] = javas[int(choice) - 1]["path"]
        save_config(config)
    elif os.path.exists(choice):
        config["java_path"] = os.path.normpath(choice)
        save_config(config)
    print(f" {C_GREEN}✓ {i18n('settings_saved')}{C_RESET}")
    time.sleep(1)


def menu_select_language(config: dict):
    print_banner()
    lines = [
        f"{C_CYAN}[1]{C_RESET} {i18n('lang_auto')}",
        f"{C_CYAN}[2]{C_RESET} {i18n('lang_ru')}",
        f"{C_CYAN}[3]{C_RESET} {i18n('lang_uk')}",
        f"{C_CYAN}[4]{C_RESET} {i18n('lang_en')}",
    ]
    draw_box(i18n("lang_title"), lines)
    choice = input(f"\n{C_CYAN}{i18n('enter_choice')}{C_RESET}").strip()

    mapping = {"1": "auto", "2": "ru", "3": "uk", "4": "en"}
    if choice in mapping:
        config["language"] = mapping[choice]
        i18n.set_language(mapping[choice])
        save_config(config)
        print(f"\n {C_GREEN}✓ {i18n('lang_changed')}{C_RESET}")
        time.sleep(1)


def menu_version_manager(config: dict):
    while True:
        print_banner()
        game_dir = config.get("game_dir")
        local_vers = get_installed_versions(game_dir)

        content = []
        if local_vers:
            content.append(f"{C_WHITE}{i18n('local_versions')}{C_RESET}")
            for i, v in enumerate(local_vers[:10], 1):
                marker = f"{C_GREEN}▶{C_RESET} " if v == config.get("active_version") else "  "
                content.append(f" {marker}{C_YELLOW}[{i}]{C_RESET} {v}")
            if len(local_vers) > 10:
                content.append(f"  {C_GRAY}... ({len(local_vers) - 10} more){C_RESET}")
        else:
            content.append(f"{C_GRAY}{i18n('no_local_versions')}{C_RESET}")

        content.append("")
        content.append(f"{C_CYAN}[S]{C_RESET} {i18n('opt_download_new')}")
        content.append(f"{C_YELLOW}[B]{C_RESET} {i18n('back_to_menu')}")

        draw_box(i18n("ver_mgr_title"), content)
        choice = input(f"\n{C_CYAN}{i18n('enter_ver_choice')}{C_RESET}").strip()

        if choice.upper() == "B":
            break
        elif choice.upper() == "S":
            action_download_version(config)
        elif choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(local_vers):
                config["active_version"] = local_vers[idx - 1]
                save_config(config)
                print(f"\n {C_GREEN}✓ {i18n('ver_selected', version=local_vers[idx - 1])}{C_RESET}")
                time.sleep(1)


def action_download_version(config: dict):
    print_banner()
    print(f"\n {C_CYAN}{i18n('dl_fetching_manifest')}{C_RESET}")
    try:
        manifest = fetch_manifest()
    except Exception as e:
        print(f" {C_RED}✗ {i18n('dl_manifest_error')} ({e}){C_RESET}")
        input("\nPress Enter to continue...")
        return

    all_versions = manifest.get("versions", [])
    joke_keys = ['potato', 'shareware', 'infinite', 'rv', 'love', 'combat', 'vote', '_or_b', 'april']

    # Categorize versions
    joke_versions = [v for v in all_versions if any(k in v['id'].lower() for k in joke_keys)]
    joke_ids = set(v['id'] for v in joke_versions)

    release_versions = [v for v in all_versions if v['type'] == 'release' and v['id'] not in joke_ids]
    snapshot_versions = [v for v in all_versions if v['type'] == 'snapshot' and v['id'] not in joke_ids]
    old_versions = [v for v in all_versions if v['type'] in ('old_beta', 'old_alpha')]

    tabs = {
        "1": {"name": i18n("cat_releases"), "list": release_versions},
        "2": {"name": i18n("cat_snapshots"), "list": snapshot_versions},
        "3": {"name": i18n("cat_jokes"), "list": joke_versions},
        "4": {"name": i18n("cat_old"), "list": old_versions},
    }

    current_tab = "1"
    page = 0
    page_size = 14
    search_query = ""

    while True:
        print_banner()
        if search_query:
            filtered_list = [v for v in all_versions if search_query.lower() in v['id'].lower()]
            tab_header = f"🔍 ПОИСК: '{search_query}' ({len(filtered_list)} найдено)"
        else:
            filtered_list = tabs[current_tab]["list"]
            tab_items = []
            for k in ["1", "2", "3", "4"]:
                t = tabs[k]
                if k == current_tab:
                    tab_items.append(f"{C_GREEN}{C_BOLD}[{k}] {t['name']}{C_RESET}")
                else:
                    tab_items.append(f"{C_GRAY}[{k}] {t['name']}{C_RESET}")
            tab_header = "   ".join(tab_items)

        total_pages = max(1, (len(filtered_list) + page_size - 1) // page_size)
        if page >= total_pages:
            page = total_pages - 1
        if page < 0:
            page = 0

        start_idx = page * page_size
        page_items = filtered_list[start_idx:start_idx + page_size]

        lines = [
            f" {tab_header}",
            f"{C_GRAY}──────────────────────────────────────────────────────────────────{C_RESET}",
            f" {C_YELLOW}{i18n('page_indicator', current=page+1, total=total_pages, count=len(filtered_list))}{C_RESET}",
            ""
        ]

        # Two-column layout for page items
        half = (len(page_items) + 1) // 2
        col1 = page_items[:half]
        col2 = page_items[half:]

        for i in range(max(len(col1), len(col2))):
            part1 = ""
            part2 = ""
            if i < len(col1):
                idx1 = i + 1
                v_id1 = col1[i]['id']
                extra1 = ""
                if v_id1 == "24w14potato":
                    extra1 = f" {C_GRAY}(Potato){C_RESET}"
                elif v_id1 == "23w13a_or_b":
                    extra1 = f" {C_GRAY}(Vote){C_RESET}"
                elif v_id1 == "20w14infinite":
                    extra1 = f" {C_GRAY}(Infinite){C_RESET}"
                elif v_id1 == "3D Shareware v1.34":
                    extra1 = f" {C_GRAY}(1994){C_RESET}"
                part1 = f"{C_CYAN}[#{idx1:>2}]{C_RESET} {C_WHITE}{v_id1:<15}{C_RESET}{extra1}"

            if i < len(col2):
                idx2 = i + half + 1
                v_id2 = col2[i]['id']
                extra2 = ""
                if v_id2 == "1.RV-Pre1":
                    extra2 = f" {C_GRAY}(Trendy){C_RESET}"
                part2 = f"{C_CYAN}[#{idx2:>2}]{C_RESET} {C_WHITE}{v_id2:<15}{C_RESET}{extra2}"

            lines.append(f" {part1:<35} {part2}")

        lines.append("")
        lines.append(f"{C_GRAY}──────────────────────────────────────────────────────────────────{C_RESET}")
        lines.append(f" {C_CYAN}[P]{C_RESET} Вперед >   {C_CYAN}[N]{C_RESET} < Назад   {C_YELLOW}[F]{C_RESET} Поиск   {C_WHITE}[B]{C_RESET} Меню")

        draw_box(i18n("browser_title"), lines, width=74)

        prompt_text = " Введите [1-4] (вкладки), [#1-14] или имя: " if not search_query else " Введите [#1-14], имя или [B] для сброса: "
        choice = input(f"\n{C_CYAN}{prompt_text}{C_RESET}").strip()

        if choice.upper() == "B":
            if search_query:
                search_query = ""
                page = 0
                continue
            else:
                break
        elif choice in ["1", "2", "3", "4"] and not search_query:
            current_tab = choice
            page = 0
            continue
        elif choice.upper() in ["P", ">"]:
            if page + 1 < total_pages:
                page += 1
            continue
        elif choice.upper() in ["N", "<"]:
            if page > 0:
                page -= 1
            continue
        elif choice.upper() in ["F", "/"]:
            sq = input(f"\n {C_YELLOW}{i18n('search_prompt')}{C_RESET}").strip()
            search_query = sq
            page = 0
            continue

        target_version = None
        if choice.startswith("#") and choice[1:].isdigit():
            c_idx = int(choice[1:]) - 1
            if 0 <= c_idx < len(page_items):
                target_version = page_items[c_idx]["id"]
        elif choice.isdigit() and search_query:
            c_idx = int(choice) - 1
            if 0 <= c_idx < len(page_items):
                target_version = page_items[c_idx]["id"]
        else:
            matched = next((v for v in all_versions if v["id"].lower() == choice.lower()), None)
            if matched:
                target_version = matched["id"]

        if target_version:
            game_dir = config["game_dir"]
            print(f"\n {C_GREEN}Начинаем загрузку Minecraft {target_version}...{C_RESET}\n")

            def progress(stage: str, current: int, total: int):
                labels = {
                    "meta": "Метаданные",
                    "client": "client.jar",
                    "libraries": "Библиотеки",
                    "natives": "Нативные DLL",
                    "assets": "Ассеты и звуки"
                }
                render_progress_bar(current, total, prefix=labels.get(stage, stage))

            try:
                download_full_version(target_version, game_dir, progress_callback=progress)
                config["active_version"] = target_version
                save_config(config)
                print(f"\n\n {C_GREEN}✓ {i18n('dl_success', version=target_version)}{C_RESET}")
            except Exception as e:
                print(f"\n\n {C_RED}✗ Ошибка загрузки: {e}{C_RESET}")
            input("\nНажмите Enter, чтобы продолжить...")
            break
        elif choice:
            print(f"\n {C_RED}✗ {i18n('dl_ver_not_found', version=choice)}{C_RESET}")
            time.sleep(1.5)


def action_launch_game(config: dict):
    active_ver = config.get("active_version")
    if not active_ver:
        print(f"\n {C_RED}✗ {i18n('status_no_version')}{C_RESET}")
        time.sleep(2)
        return

    print_banner()
    draw_box(i18n("launch_header"), [
        f"Game:    {C_GREEN}Minecraft {active_ver}{C_RESET}",
        f"Player:  {C_YELLOW}{config.get('username')}{C_RESET}",
        f"RAM:     {C_WHITE}{config.get('ram_gb')} GB{C_RESET}"
    ])

    # Автопроверка и автоскачивание недостающих зависимостей
    print(f"\n {C_CYAN}{i18n('checking_files')}{C_RESET}")
    missing = check_missing_dependencies(active_ver, config.get("game_dir"))
    if missing:
        print(f" {C_YELLOW}⚠ {i18n('missing_files')}{C_RESET}")
        print(f" {C_GRAY}Недостающих файлов: {len(missing)}{C_RESET}\n")

        def progress(stage: str, current: int, total: int):
            labels = {
                "meta": "Метаданные",
                "client": "client.jar",
                "libraries": "Библиотеки",
                "natives": "Нативные DLL",
                "assets": "Ассеты и звуки"
            }
            render_progress_bar(current, total, prefix=labels.get(stage, stage))

        try:
            download_full_version(active_ver, config.get("game_dir"), progress_callback=progress)
            print(f"\n\n {C_GREEN}✓ Все зависимости успешно загружены!{C_RESET}\n")
        except Exception as e:
            print(f"\n\n {C_RED}✗ Ошибка автозагрузки: {e}{C_RESET}")
            input("\nНажмите Enter для продолжения...")
            return

    print(f" {C_CYAN}{i18n('starting_jvm')}{C_RESET}\n")
    try:
        proc = launch_game(config, active_ver)
        print(f" {C_GREEN}✓ {i18n('game_running', pid=proc.pid)}{C_RESET}")
        print(f" {C_GRAY}{i18n('game_logs')}{C_RESET}\n")

        # Stream game logs until exit or user interrupt
        try:
            for line in proc.stdout:
                line_str = line.strip()
                if line_str:
                    # Clean colorize standard log lines
                    if "ERROR" in line_str:
                        print(f" {C_RED}{line_str}{C_RESET}")
                    elif "WARN" in line_str:
                        print(f" {C_YELLOW}{line_str}{C_RESET}")
                    else:
                        print(f" {C_GRAY}{line_str}{C_RESET}")
            proc.wait()
            print(f"\n {C_WHITE}{i18n('game_closed', code=proc.returncode)}{C_RESET}")
            input("\nPress Enter to return to menu...")
        except KeyboardInterrupt:
            print(f"\n {C_YELLOW}Returning to menu while game runs in background...{C_RESET}")
            time.sleep(1.5)

    except Exception as e:
        print(f" {C_RED}✗ Launch failed: {e}{C_RESET}")
        input("\nPress Enter to continue...")


def ensure_dependencies():
    """Checks and automatically installs any missing python libraries."""
    required = []
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"\n {C_CYAN}[lazymc] Загрузка библиотек: {', '.join(missing)}...{C_RESET}")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL)
            print(f" {C_GREEN}✓ Библиотеки успешно установлены!{C_RESET}\n")
        except Exception as e:
            print(f" {C_RED}✗ Ошибка установки библиотек: {e}{C_RESET}\n")


def main():
    # Enable ANSI escape sequences on Windows
    os.system("")
    if sys.platform == "win32":
        os.system("title lazymc v0.1.2")

    ensure_dependencies()
    config = load_config()
    i18n.set_language(config.get("language", "auto"))

    # If no active version set, check if versions exist
    if not config.get("active_version"):
        installed = get_installed_versions(config.get("game_dir"))
        if installed:
            config["active_version"] = installed[0]
            save_config(config)

    while True:
        print_banner()
        status_lines = format_status_panel(config)
        draw_box(i18n("menu_title"), status_lines)

        menu_items = [
            f"{C_GREEN}[1] 🚀 {i18n('opt_launch')}{C_RESET}",
            f"{C_CYAN}[2] 📦 {i18n('opt_versions')}{C_RESET}",
            f"{C_YELLOW}[3] 👤 {i18n('opt_user')}{C_RESET}",
            f"{C_WHITE}[4] ⚙️  {i18n('opt_settings')}{C_RESET}",
            f"{C_WHITE}[5] 🌐 {i18n('opt_lang')}{C_RESET}",
            f"{C_RED}[6] 🚪 {i18n('opt_exit')}{C_RESET}",
        ]
        print()
        for item in menu_items:
            print(f"  {item}")

        print(f"\n{C_GRAY} ────────────────────────────────────────────────────────{C_RESET}")
        choice = input(f" {C_CYAN}{i18n('enter_choice')}{C_RESET}").strip()

        if choice == "1":
            action_launch_game(config)
        elif choice == "2":
            menu_version_manager(config)
        elif choice == "3":
            menu_change_nick(config)
        elif choice == "4":
            menu_settings(config)
        elif choice == "5":
            menu_select_language(config)
        elif choice == "6":
            print_banner()
            print(f"\n  {C_GREEN}Goodbye! До зустрічі! Пока!{C_RESET}\n")
            break


if __name__ == "__main__":
    main()
