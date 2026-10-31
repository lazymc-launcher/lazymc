"""
lazymc i18n module
Supports: Ukrainian (uk), Russian (ru), English (en - default fallback)
Auto-detects Windows system language.
"""

import ctypes
import locale

TRANSLATIONS = {
    "en": {
        "title": "⚡ lazymc ⚡",
        "menu_title": "MAIN MENU",
        "user": "Nickname",
        "ram": "RAM",
        "version": "Version",
        "java": "Java Runtime",
        "lang": "Language",
        "game_dir": "Game Directory",
        "status_ready": "Ready to launch",
        "status_no_version": "No version selected! Please download/select one.",
        
        "opt_launch": "Launch Game",
        "opt_versions": "Version Manager (Download / Select)",
        "opt_user": "Change Nickname",
        "opt_settings": "Settings (RAM, Java, JVM args)",
        "opt_lang": "Change Language",
        "opt_exit": "Exit",
        "enter_choice": "Select an action [1-6]: ",
        
        # Nickname
        "nick_title": "CHANGE NICKNAME",
        "current_nick": "Current nickname",
        "enter_nick": "Enter new nickname (or press Enter to cancel): ",
        "nick_saved": "Nickname saved successfully!",
        
        # RAM & Settings
        "settings_title": "LAUNCHER SETTINGS",
        "set_ram_opt": "Change RAM allocation (current: {ram} GB)",
        "set_java_opt": "Change Java path (current: {java})",
        "set_dir_opt": "Change Game Directory (current: {dir})",
        "set_jvm_opt": "Extra JVM arguments (current: {args})",
        "back_to_menu": "Back to Main Menu",
        "enter_ram": "Enter RAM in GB (e.g. 4, 6, 8): ",
        "invalid_ram": "Invalid number. Please enter an integer.",
        "settings_saved": "Settings saved!",
        
        # Java
        "java_auto": "Auto-detect",
        "java_found": "Found Java runtimes:",
        "java_select": "Select Java [number], enter custom path, or press Enter for auto: ",
        "java_not_found": "Warning: Java not detected! Please install Java or specify path.",
        
        # Version manager & Browser
        "ver_mgr_title": "VERSION MANAGER",
        "local_versions": "Installed local versions:",
        "no_local_versions": "No versions installed locally yet.",
        "opt_select_local": "Select installed version",
        "opt_download_new": "Download new version from Mojang",
        "opt_refresh": "Refresh list",
        "enter_ver_choice": "Choose action: ",
        "select_local_num": "Enter version number to activate: ",
        "ver_selected": "Active version set to: {version}",
        
        # Version Browser
        "browser_title": "MOJANG VERSION CATALOG",
        "cat_releases": "Releases",
        "cat_snapshots": "Snapshots",
        "cat_jokes": "April Fools / Jokes",
        "cat_old": "Beta & Alpha",
        "page_indicator": "Page {current}/{total} • Total: {count}",
        "browser_nav": "[1] Releases  [2] Snapshots  [3] April Fools  [4] Beta/Alpha",
        "browser_actions": "[P] Next >  [N] < Prev  [F] Search  [B] Back",
        "enter_browser_choice": "Select [1-{max}] to download, change tab [1-4], or enter name: ",
        "search_prompt": "Search version by name: ",
        "search_results": "Search results for '{query}':",
        "no_search_results": "No versions found matching '{query}'.",
        
        # Downloader
        "dl_fetching_manifest": "Fetching version manifest from Mojang servers...",
        "dl_manifest_error": "Failed to connect to Mojang API. Check your internet connection.",
        "dl_choose_type": "Filter versions: [1] Releases only  [2] Releases + Snapshots: ",
        "dl_select_version": "Enter version name to download (e.g. 1.21.1, 1.20.4, 1.16.5): ",
        "dl_ver_not_found": "Version '{version}' not found in Mojang manifest!",
        "dl_client_jar": "Downloading client JAR...",
        "dl_libraries": "Downloading libraries ({count} total)...",
        "dl_assets": "Downloading assets ({count} objects)...",
        "dl_natives": "Unpacking native libraries...",
        "dl_success": "Version {version} successfully downloaded and installed!",
        "dl_progress": "Progress: {done}/{total} ({percent}%)",
        
        # Launcher
        "launch_header": "LAUNCHING MINECRAFT",
        "checking_files": "Verifying files and dependencies...",
        "missing_files": "Some files are missing. Starting automatic download...",
        "starting_jvm": "Starting Java Virtual Machine...",
        "game_running": "Game process started! (PID: {pid})",
        "game_logs": "Game output is active. Press Ctrl+C to return to menu.",
        "game_closed": "Game closed (exit code: {code}).",
        "java_compat_warn": "Warning: Minecraft {mc_ver} recommends Java {rec_java}, but Java {cur_java} is selected.",
        
        # Language menu
        "lang_title": "SELECT LANGUAGE",
        "lang_auto": "System Default (Auto)",
        "lang_en": "English",
        "lang_ru": "Русский (Russian)",
        "lang_uk": "Українська (Ukrainian)",
        "lang_changed": "Language updated!"
    },
    
    "ru": {
        "title": "⚡ lazymc ⚡",
        "menu_title": "ГЛАВНОЕ МЕНЮ",
        "user": "Никнейм",
        "ram": "ОЗУ (RAM)",
        "version": "Версия",
        "java": "Среда Java",
        "lang": "Язык",
        "game_dir": "Папка игры",
        "status_ready": "Готов к запуску",
        "status_no_version": "Версия не выбрана! Скачайте или выберите версию.",
        
        "opt_launch": "ЗАПУСТИТЬ ИГРУ",
        "opt_versions": "Менеджер версий (Скачать / Выбрать)",
        "opt_user": "Сменить никнейм",
        "opt_settings": "Настройки (ОЗУ, Java, аргументы JVM)",
        "opt_lang": "Сменить язык интерфейса",
        "opt_exit": "Выход",
        "enter_choice": "Выберите действие [1-6]: ",
        
        # Nickname
        "nick_title": "СМЕНА НИКНЕЙМА",
        "current_nick": "Текущий никнейм",
        "enter_nick": "Введите новый никнейм (Enter для отмены): ",
        "nick_saved": "Никнейм успешно сохранен!",
        
        # RAM & Settings
        "settings_title": "НАСТРОЙКИ ЛАУНЧЕРА",
        "set_ram_opt": "Выделение ОЗУ (текущее: {ram} ГБ)",
        "set_java_opt": "Путь к Java (текущий: {java})",
        "set_dir_opt": "Рабочая папка игры (текущая: {dir})",
        "set_jvm_opt": "Дополнительные JVM аргументы (текущие: {args})",
        "back_to_menu": "Назад в главное меню",
        "enter_ram": "Сколько ГБ выделить (например, 4, 6, 8): ",
        "invalid_ram": "Некорректное число. Введите целое число.",
        "settings_saved": "Настройки сохранены!",
        
        # Java
        "java_auto": "Автоопределение",
        "java_found": "Найденные версии Java:",
        "java_select": "Выберите Java [номер], укажите путь или Enter для авто: ",
        "java_not_found": "Внимание: Java не найдена! Установите Java или укажите путь вручную.",
        
        # Version manager & Browser
        "ver_mgr_title": "МЕНЕДЖЕР ВЕРСИЙ",
        "local_versions": "Установленные локальные версии:",
        "no_local_versions": "Локальные версии еще не установлены.",
        "opt_select_local": "Выбрать установленную версию",
        "opt_download_new": "Каталог версий Mojang (Релизы, Снапшоты, Первоапрельские)",
        "opt_refresh": "Обновить список",
        "enter_ver_choice": "Выберите действие: ",
        "select_local_num": "Введите номер версии для активации: ",
        "ver_selected": "Активная версия переключена на: {version}",
        
        # Version Browser
        "browser_title": "КАТАЛОГ ВЕРСИЙ MOJANG",
        "cat_releases": "Релизы",
        "cat_snapshots": "Снапшоты",
        "cat_jokes": "Первоапрельские",
        "cat_old": "Beta / Alpha",
        "page_indicator": "Стр. {current}/{total} • Всего: {count}",
        "browser_nav": "[1] Релизы  [2] Снапшоты  [3] 1 Апреля  [4] Beta/Alpha",
        "browser_actions": "[P] Вперед >  [N] < Назад  [F] Поиск  [B] Меню",
        "enter_browser_choice": "Выберите [1-{max}] для скачивания, вкладку [1-4] или введите имя: ",
        "search_prompt": "Поиск версии по названию: ",
        "search_results": "Результаты поиска для '{query}':",
        "no_search_results": "Версий по запросу '{query}' не найдено.",
        
        # Downloader
        "dl_fetching_manifest": "Загрузка манифеста версий с серверов Mojang...",
        "dl_manifest_error": "Не удалось связаться с серверами Mojang. Проверьте подключение к интернету.",
        "dl_choose_type": "Показать: [1] Только релизы  [2] Релизы и снапшоты: ",
        "dl_select_version": "Введите версию для загрузки (например, 1.21.1, 1.20.4, 1.16.5): ",
        "dl_ver_not_found": "Версия '{version}' не найдена в официальном манифесте Mojang!",
        "dl_client_jar": "Загрузка client.jar...",
        "dl_libraries": "Загрузка библиотек (всего {count})...",
        "dl_assets": "Загрузка ассетов и звуков ({count} объектов)...",
        "dl_natives": "Распаковка нативных библиотек...",
        "dl_success": "Версия {version} успешно загружена и установлена!",
        "dl_progress": "Прогресс: {done}/{total} ({percent}%)",
        
        # Launcher
        "launch_header": "ЗАПУСК MINECRAFT",
        "checking_files": "Проверка файлов и целостности...",
        "missing_files": "Некоторые файлы отсутствуют. Начинаем автозагрузку...",
        "starting_jvm": "Запуск Java Virtual Machine...",
        "game_running": "Процесс игры запущен! (PID: {pid})",
        "game_logs": "Вывод игры активен. Нажмите Ctrl+C, чтобы вернуться в меню.",
        "game_closed": "Игра закрыта (код завершения: {code}).",
        "java_compat_warn": "Внимание: для Minecraft {mc_ver} требуется Java {rec_java}, а выбрана Java {cur_java}.",
        
        # Language menu
        "lang_title": "ВЫБОР ЯЗЫКА",
        "lang_auto": "Системный по умолчанию (Авто)",
        "lang_en": "English (Английский)",
        "lang_ru": "Русский",
        "lang_uk": "Українська (Украинский)",
        "lang_changed": "Язык успешно изменен!"
    },
    
    "uk": {
        "title": "⚡ lazymc ⚡",
        "menu_title": "ГОЛОВНЕ МЕНЮ",
        "user": "Нікнейм",
        "ram": "ОЗП (RAM)",
        "version": "Версія",
        "java": "Середовище Java",
        "lang": "Мова",
        "game_dir": "Папка гри",
        "status_ready": "Готовий до запуску",
        "status_no_version": "Версія не обрана! Завантажте або виберіть версію.",
        
        "opt_launch": "ЗАПУСТИТИ ГРУ",
        "opt_versions": "Менеджер версій (Завантажити / Обрати)",
        "opt_user": "Змінити нікнейм",
        "opt_settings": "Налаштування (ОЗП, Java, аргументи JVM)",
        "opt_lang": "Змінити мову інтерфейсу",
        "opt_exit": "Вихід",
        "enter_choice": "Оберіть дію [1-6]: ",
        
        # Nickname
        "nick_title": "ЗМІНА НІКНЕЙМА",
        "current_nick": "Поточний нікнейм",
        "enter_nick": "Введіть новий нікнейм (Enter для скасування): ",
        "nick_saved": "Нікнейм успішно збережено!",
        
        # RAM & Settings
        "settings_title": "НАЛАШТУВАННЯ ЛАУНЧЕРА",
        "set_ram_opt": "Виділення ОЗП (поточне: {ram} ГБ)",
        "set_java_opt": "Шлях до Java (поточний: {java})",
        "set_dir_opt": "Робоча папка гри (поточна: {dir})",
        "set_jvm_opt": "Додаткові JVM аргументи (поточні: {args})",
        "back_to_menu": "Назад до головного меню",
        "enter_ram": "Скільки ГБ виділити (наприклад, 4, 6, 8): ",
        "invalid_ram": "Некоректне число. Введіть ціле число.",
        "settings_saved": "Налаштування збережено!",
        
        # Java
        "java_auto": "Автовизначення",
        "java_found": "Знайдені версії Java:",
        "java_select": "Оберіть Java [номер], вкажіть шлях або Enter для авто: ",
        "java_not_found": "Увага: Java не знайдена! Встановіть Java або вкажіть шлях вручну.",
        
        # Version manager & Browser
        "ver_mgr_title": "МЕНЕДЖЕР ВЕРСІЙ",
        "local_versions": "Встановлені локальні версії:",
        "no_local_versions": "Локальні версії ще не встановлені.",
        "opt_select_local": "Обрати встановлену версію",
        "opt_download_new": "Каталог версій Mojang (Релізи, Снапшоти, Першоквітневі)",
        "opt_refresh": "Оновити список",
        "enter_ver_choice": "Оберіть дію: ",
        "select_local_num": "Введіть номер версії для активації: ",
        "ver_selected": "Активна версія переключена на: {version}",
        
        # Version Browser
        "browser_title": "КАТАЛОГ ВЕРСІЙ MOJANG",
        "cat_releases": "Релізи",
        "cat_snapshots": "Снапшоти",
        "cat_jokes": "Першоквітневі",
        "cat_old": "Beta / Alpha",
        "page_indicator": "Стор. {current}/{total} • Всього: {count}",
        "browser_nav": "[1] Релізи  [2] Снапшоти  [3] 1 Квітня  [4] Beta/Alpha",
        "browser_actions": "[P] Вперед >  [N] < Назад  [F] Пошук  [B] Меню",
        "enter_browser_choice": "Виберіть [1-{max}] для завантаження, вкладку [1-4] або введіть ім'я: ",
        "search_prompt": "Пошук версії за назвою: ",
        "search_results": "Результати пошуку для '{query}':",
        "no_search_results": "Версій за запитом '{query}' не знайдено.",
        
        # Downloader
        "dl_fetching_manifest": "Завантаження маніфесту версій із серверів Mojang...",
        "dl_manifest_error": "Не вдалося зв'язатися з серверами Mojang. Перевірте з'єднання з інтернетом.",
        "dl_choose_type": "Показати: [1] Тільки релізи  [2] Релізи та снапшоти: ",
        "dl_select_version": "Введіть версію для завантаження (наприклад, 1.21.1, 1.20.4, 1.16.5): ",
        "dl_ver_not_found": "Версія '{version}' не знайдена в офіційному маніфесті Mojang!",
        "dl_client_jar": "Завантаження client.jar...",
        "dl_libraries": "Завантаження бібліотек (усього {count})...",
        "dl_assets": "Завантаження асетів та звуків ({count} об'єктів)...",
        "dl_natives": "Розпакування нативних бібліотек...",
        "dl_success": "Версія {version} успішно завантажена та встановлена!",
        "dl_progress": "Прогрес: {done}/{total} ({percent}%)",
        
        # Launcher
        "launch_header": "ЗАПУСК MINECRAFT",
        "checking_files": "Перевірка файлів та цілісності...",
        "missing_files": "Деякі файли відсутні. Починаємо автозавантаження...",
        "starting_jvm": "Запуск Java Virtual Machine...",
        "game_running": "Процес гри запущено! (PID: {pid})",
        "game_logs": "Вивід гри активний. Натисніть Ctrl+C, щоб повернутися до меню.",
        "game_closed": "Гру закрито (код завершення: {code}).",
        "java_compat_warn": "Увага: для Minecraft {mc_ver} рекомендується Java {rec_java}, а обрано Java {cur_java}.",
        
        # Language menu
        "lang_title": "ВИБІР МОВИ",
        "lang_auto": "Системна за замовчуванням (Авто)",
        "lang_en": "English (Англійська)",
        "lang_ru": "Русский (Російська)",
        "lang_uk": "Українська",
        "lang_changed": "Мову успішно змінено!"
    }
}


def detect_system_language() -> str:
    """Detects system UI language on Windows, falling back to English."""
    try:
        windll = getattr(ctypes, 'windll', None)
        if windll:
            lang_id = windll.kernel32.GetUserDefaultUILanguage()
            primary = lang_id & 0x3ff
            if primary == 0x19:   # Russian (0x0419)
                return "ru"
            elif primary == 0x22: # Ukrainian (0x0422)
                return "uk"
            elif primary == 0x09: # English (0x0409)
                return "en"
    except Exception:
        pass

    try:
        loc = (locale.getlocale()[0] or "").lower()
        if loc.startswith("ru"):
            return "ru"
        elif loc.startswith("uk") or loc.startswith("ua"):
            return "uk"
    except Exception:
        pass

    return "en"


class I18n:
    def __init__(self, current_lang="auto"):
        self.set_language(current_lang)

    def set_language(self, lang_code: str):
        if lang_code == "auto" or not lang_code:
            self.resolved_lang = detect_system_language()
            self.setting = "auto"
        else:
            if lang_code in TRANSLATIONS:
                self.resolved_lang = lang_code
                self.setting = lang_code
            else:
                self.resolved_lang = "en"
                self.setting = "en"

    def get(self, key: str, **kwargs) -> str:
        dict_to_use = TRANSLATIONS.get(self.resolved_lang, TRANSLATIONS["en"])
        template = dict_to_use.get(key, TRANSLATIONS["en"].get(key, key))
        if kwargs:
            try:
                return template.format(**kwargs)
            except Exception:
                return template
        return template

    def __call__(self, key: str, **kwargs) -> str:
        return self.get(key, **kwargs)


i18n = I18n()
