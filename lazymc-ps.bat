@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$f='%~f0'; (Get-Content -Path $f -Encoding UTF8 | Select-Object -Skip 4) -join [Environment]::NewLine | Invoke-Expression"
exit /b %errorlevel%
REM PowerShell starts below
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$host.UI.RawUI.WindowTitle = "lazymc v0.2.0 (PowerShell Edition)"

$APP_VERSION = "v0.2.0"
$CONFIG_DIR = Join-Path $env:APPDATA ".lazymc"
$CONFIG_FILE = Join-Path $CONFIG_DIR "config.json"
$DEFAULT_GAME_DIR = Join-Path $env:APPDATA ".minecraft"
$MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
$REPO_RAW_URL = "https://raw.githubusercontent.com/lazymc-launcher/lazymc/main"

# ----------------- I18N -----------------
$TRANSLATIONS = @{
    "en" = @{
        "title" = "⚡ lazymc ⚡"
        "menu_title" = "MAIN MENU"
        "user" = "Nickname"
        "ram" = "RAM"
        "version" = "Version"
        "java" = "Java Runtime"
        "lang" = "Language"
        "status_no_version" = "No version selected! Please download/select one."
        "opt_launch" = "Launch Game"
        "opt_versions" = "Version Manager (Download / Select)"
        "opt_user" = "Change Nickname"
        "opt_settings" = "Settings (RAM, Java, JVM args)"
        "opt_lang" = "Change Language"
        "opt_update" = "Check for Updates"
        "opt_exit" = "Exit"
        "enter_choice" = "Select an action [1-7]: "
        "nick_title" = "CHANGE NICKNAME"
        "current_nick" = "Current nickname"
        "enter_nick" = "Enter new nickname (Enter to cancel): "
        "nick_saved" = "Nickname saved successfully!"
        "settings_title" = "LAUNCHER SETTINGS"
        "set_ram_opt" = "Change RAM allocation (current: {0} GB)"
        "set_jvm_opt" = "Extra JVM arguments (current: {0})"
        "back_to_menu" = "Back to Main Menu"
        "enter_ram" = "Enter RAM in GB (e.g. 4, 6, 8): "
        "settings_saved" = "Settings saved!"
        "ver_mgr_title" = "VERSION MANAGER"
        "local_versions" = "Installed local versions:"
        "no_local_versions" = "No versions installed locally yet."
        "opt_download_new" = "Mojang Version Catalog"
        "enter_ver_choice" = "Choose action: "
        "ver_selected" = "Active version set to: {0}"
        "browser_title" = "MOJANG VERSION CATALOG"
        "cat_releases" = "Releases"
        "cat_snapshots" = "Snapshots"
        "cat_jokes" = "April Fools"
        "cat_old" = "Beta / Alpha"
        "page_indicator" = "Page {0}/{1} • Total: {2}"
        "dl_fetching_manifest" = "Fetching version manifest from Mojang..."
        "dl_manifest_error" = "Failed to connect to Mojang API."
        "dl_ver_not_found" = "Version '{0}' not found!"
        "dl_success" = "Version {0} successfully downloaded and installed!"
        "launch_header" = "LAUNCHING MINECRAFT"
        "checking_files" = "Checking dependencies..."
        "missing_files" = "Missing components ({0}). Starting auto-download..."
        "starting_jvm" = "Starting Java Virtual Machine..."
        "game_running" = "Game process started! (PID: {0})"
        "game_logs" = "Game output is active. Press Ctrl+C to return to menu."
        "game_closed" = "Game closed (exit code: {0})."
        "update_title" = "CHECK FOR UPDATES"
        "update_checking" = "Checking for updates on GitHub..."
        "update_available" = "Update available: v{0} (current: v{1})!"
        "update_latest" = "You are using the latest version of lazymc."
        "update_prompt" = "Update lazymc now? [Y/N]: "
        "update_success" = "lazymc updated successfully! Please restart the launcher."
    }
    "ru" = @{
        "title" = "⚡ lazymc ⚡"
        "menu_title" = "ГЛАВНОЕ МЕНЮ"
        "user" = "Никнейм"
        "ram" = "ОЗУ (RAM)"
        "version" = "Версия"
        "java" = "Среда Java"
        "lang" = "Язык"
        "status_no_version" = "Версия не выбрана! Скачайте или выберите версию."
        "opt_launch" = "ЗАПУСТИТЬ ИГРУ"
        "opt_versions" = "Менеджер версий (Скачать / Выбрать)"
        "opt_user" = "Сменить никнейм"
        "opt_settings" = "Настройки (ОЗУ, Java, аргументы JVM)"
        "opt_lang" = "Сменить язык интерфейса"
        "opt_update" = "Проверить обновления"
        "opt_exit" = "Выход"
        "enter_choice" = "Выберите действие [1-7]: "
        "nick_title" = "СМЕНА НИКНЕЙМА"
        "current_nick" = "Текущий никнейм"
        "enter_nick" = "Введите новый никнейм (Enter для отмены): "
        "nick_saved" = "Никнейм успешно сохранен!"
        "settings_title" = "НАСТРОЙКИ ЛАУНЧЕРА"
        "set_ram_opt" = "Выделение ОЗУ (текущее: {0} ГБ)"
        "set_jvm_opt" = "Дополнительные JVM аргументы (текущие: {0})"
        "back_to_menu" = "Назад в главное меню"
        "enter_ram" = "Сколько ГБ выделить (например, 4, 6, 8): "
        "settings_saved" = "Настройки сохранены!"
        "ver_mgr_title" = "МЕНЕДЖЕР ВЕРСИЙ"
        "local_versions" = "Установленные локальные версии:"
        "no_local_versions" = "Локальные версии еще не установлены."
        "opt_download_new" = "Каталог версий Mojang (Релизы, Снапшоты, Первоапрельские)"
        "enter_ver_choice" = "Выберите действие: "
        "ver_selected" = "Активная версия переключена на: {0}"
        "browser_title" = "КАТАЛОГ ВЕРСИЙ MOJANG"
        "cat_releases" = "Релизы"
        "cat_snapshots" = "Снапшоты"
        "cat_jokes" = "Первоапрельские"
        "cat_old" = "Beta / Alpha"
        "page_indicator" = "Стр. {0}/{1} • Всего: {2}"
        "dl_fetching_manifest" = "Загрузка манифеста версий с серверов Mojang..."
        "dl_manifest_error" = "Не удалось связаться с серверами Mojang."
        "dl_ver_not_found" = "Версия '{0}' не найдена!"
        "dl_success" = "Версия {0} успешно загружена и установлена!"
        "launch_header" = "ЗАПУСК MINECRAFT"
        "checking_files" = "Проверка файлов и зависимостей..."
        "missing_files" = "Недостающих компонентов ({0}). Запуск автоскачивания..."
        "starting_jvm" = "Запуск Java Virtual Machine..."
        "game_running" = "Процесс игры запущен! (PID: {0})"
        "game_logs" = "Вывод игры активен. Нажмите Ctrl+C, чтобы вернуться в меню."
        "game_closed" = "Игра закрыта (код завершения: {0})."
        "update_title" = "ПРОВЕРКА ОБНОВЛЕНИЙ"
        "update_checking" = "Проверка обновлений на GitHub..."
        "update_available" = "Доступно новое обновление: v{0} (текущая: v{1})!"
        "update_latest" = "У вас установлена последняя версия lazymc."
        "update_prompt" = "Обновить lazymc прямо сейчас? [Y/N]: "
        "update_success" = "lazymc успешно обновлен! Пожалуйста, перезапустите лаунчер."
    }
    "uk" = @{
        "title" = "⚡ lazymc ⚡"
        "menu_title" = "ГОЛОВНЕ МЕНЮ"
        "user" = "Нікнейм"
        "ram" = "ОЗП (RAM)"
        "version" = "Версія"
        "java" = "Середовище Java"
        "lang" = "Мова"
        "status_no_version" = "Версія не обрана! Завантажте або виберіть версію."
        "opt_launch" = "ЗАПУСТИТИ ГРУ"
        "opt_versions" = "Менеджер версій (Завантажити / Обрати)"
        "opt_user" = "Змінити нікнейм"
        "opt_settings" = "Налаштування (ОЗП, Java, аргументи JVM)"
        "opt_lang" = "Змінити мову інтерфейсу"
        "opt_update" = "Перевірити оновлення"
        "opt_exit" = "Вихід"
        "enter_choice" = "Оберіть дію [1-7]: "
        "nick_title" = "ЗМІНА НІКНЕЙМА"
        "current_nick" = "Поточний нікнейм"
        "enter_nick" = "Введіть новий нікнейм (Enter для скасування): "
        "nick_saved" = "Нікнейм успішно збережено!"
        "settings_title" = "НАЛАШТУВАННЯ ЛАУНЧЕРА"
        "set_ram_opt" = "Виділення ОЗП (поточне: {0} ГБ)"
        "set_jvm_opt" = "Додаткові JVM аргументи (поточні: {0})"
        "back_to_menu" = "Назад до головного меню"
        "enter_ram" = "Скільки ГБ виділити (наприклад, 4, 6, 8): "
        "settings_saved" = "Налаштування збережено!"
        "ver_mgr_title" = "МЕНЕДЖЕР ВЕРСІЙ"
        "local_versions" = "Встановлені локальні версії:"
        "no_local_versions" = "Локальні версії ще не встановлені."
        "opt_download_new" = "Каталог версій Mojang (Релізи, Снапшоти, Першоквітневі)"
        "enter_ver_choice" = "Оберіть дію: "
        "ver_selected" = "Активна версія переключена на: {0}"
        "browser_title" = "КАТАЛОГ ВЕРСІЙ MOJANG"
        "cat_releases" = "Релізи"
        "cat_snapshots" = "Снапшоти"
        "cat_jokes" = "Першоквітневі"
        "cat_old" = "Beta / Alpha"
        "page_indicator" = "Стор. {0}/{1} • Всього: {2}"
        "dl_fetching_manifest" = "Завантаження маніфесту версій із серверів Mojang..."
        "dl_manifest_error" = "Не вдалося зв'язатися з серверами Mojang."
        "dl_ver_not_found" = "Версія '{0}' не знайдена!"
        "dl_success" = "Версія {0} успішно завантажена та встановлена!"
        "launch_header" = "ЗАПУСК MINECRAFT"
        "checking_files" = "Перевірка файлів та залежностей..."
        "missing_files" = "Недостатніх компонентів ({0}). Запуск автозавантаження..."
        "starting_jvm" = "Запуск Java Virtual Machine..."
        "game_running" = "Процес гри запущено! (PID: {0})"
        "game_logs" = "Вивід гри активний. Натисніть Ctrl+C, щоб повернутися до меню."
        "game_closed" = "Гру закрито (код завершення: {0})."
        "update_title" = "ПЕРЕВІРКА ОНОВЛЕНЬ"
        "update_checking" = "Перевірка оновлень на GitHub..."
        "update_available" = "Доступне нове оновлення: v{0} (поточна: v{1})!"
        "update_latest" = "У вас встановлена остання версія lazymc."
        "update_prompt" = "Оновити lazymc зараз? [Y/N]: "
        "update_success" = "lazymc успішно оновлено! Будь ласка, перезапустіть лаунчер."
    }
}

function Get-SystemLang {
    try {
        $l = [System.Globalization.CultureInfo]::InstalledUICulture.TwoLetterISOLanguageName.ToLower()
        if ($l -eq "ru") { return "ru" }
        if ($l -eq "uk") { return "uk" }
    } catch {}
    return "en"
}

$CurrentLang = Get-SystemLang

function T($key, $arg0=$null, $arg1=$null, $arg2=$null) {
    $dict = $TRANSLATIONS[$CurrentLang]
    if (-not $dict) { $dict = $TRANSLATIONS["en"] }
    $str = $dict[$key]
    if (-not $str) { $str = $TRANSLATIONS["en"][$key] }
    if (-not $str) { return $key }
    if ($arg0 -ne $null) {
        return ($str -f $arg0, $arg1, $arg2)
    }
    return $str
}

# ----------------- CONFIG -----------------
$Config = @{
    "username" = "Player"
    "language" = "auto"
    "ram_gb" = 4
    "game_dir" = $DEFAULT_GAME_DIR
    "active_version" = ""
    "java_path" = "auto"
    "jvm_args" = "-XX:+UseG1GC"
    "window_width" = 854
    "window_height" = 480
}

function Load-Config {
    if (Test-Path $CONFIG_FILE) {
        try {
            $json = Get-Content $CONFIG_FILE -Raw -Encoding UTF8 | ConvertFrom-Json
            foreach ($prop in $json.PSObject.Properties) {
                $Config[$prop.Name] = $prop.Value
            }
        } catch {}
    }
    if ($Config["language"] -ne "auto" -and $TRANSLATIONS.ContainsKey($Config["language"])) {
        $global:CurrentLang = $Config["language"]
    } else {
        $global:CurrentLang = Get-SystemLang
    }
}

function Save-Config {
    if (-not (Test-Path $CONFIG_DIR)) { New-Item -ItemType Directory -Path $CONFIG_DIR -Force | Out-Null }
    $Config | ConvertTo-Json -Depth 4 | Set-Content -Path $CONFIG_FILE -Encoding UTF8
}

# ----------------- UI HELPERS -----------------
$ESC = [char]27
$C_RESET = "$ESC[0m"
$C_BOLD = "$ESC[1m"
$C_GRAY = "$ESC[90m"
$C_RED = "$ESC[91m"
$C_GREEN = "$ESC[92m"
$C_YELLOW = "$ESC[93m"
$C_CYAN = "$ESC[96m"
$C_WHITE = "$ESC[97m"

function Print-Banner {
    Clear-Host
    Write-Host "$C_CYAN$C_BOLD" -NoNewline
    Write-Host "  _                                   "
    Write-Host " | | __ _ _____   _ _ __ ___   ___    "
    Write-Host " | |/ _` |_  / | | | '_ ` _ \ / __|   "
    Write-Host " | | (_| |/ /| |_| | | | | | | (__    "
    Write-Host " |_|\__,_/___|\__, |_| |_| |_|\___|   "
    Write-Host "              |___/                               $C_GRAY$C_BOLD$APP_VERSION$C_RESET"
    Write-Host "$C_GRAY ────────────────────────────────────────────────────────$C_RESET"
}

function Strip-Ansi($s) {
    return ($s -replace '\x1b\[[0-9;]*m', '')
}

function Draw-Box($title, $lines, $width=74) {
    $border = $C_GRAY
    $innerWidth = $width - 2
    $rawTitle = Strip-Ansi $title
    $padLeft = [Math]::Max(0, [int](($innerWidth - $rawTitle.Length) / 2))
    $padRight = [Math]::Max(0, $innerWidth - $rawTitle.Length - $padLeft)
    $titleLine = (" " * $padLeft) + "$C_CYAN$C_BOLD$title$C_RESET" + (" " * $padRight)

    Write-Host "$border┌$('-' * $innerWidth)┐$C_RESET"
    Write-Host "$border│$titleLine$border│$C_RESET"
    Write-Host "$border├$('-' * $innerWidth)┤$C_RESET"

    foreach ($line in $lines) {
        $raw = Strip-Ansi $line
        $pad = [Math]::Max(0, $innerWidth - 2 - $raw.Length)
        Write-Host "$border│$C_RESET $line$($(' ' * $pad)) $border│$C_RESET"
    }
    Write-Host "$border└$('-' * $innerWidth)┘$C_RESET"
}

function Render-ProgressBar($done, $total, $prefix="Download", $length=25) {
    if ($total -le 0) { $pct = 100; $filled = $length }
    else {
        $pct = [Math]::Min(100, [int](100 * $done / $total))
        $filled = [int]($length * $done / $total)
    }
    $bar = "$C_GREEN" + ('█' * $filled) + "$C_GRAY" + ('░' * ($length - $filled)) + "$C_RESET"
    Write-Host -NoNewline "`r  $($prefix.PadRight(18)) [$bar] $C_WHITE$($pct.ToString().PadLeft(3))%$C_RESET ($done/$total)"
    if ($done -ge $total -and $total -gt 0) { Write-Host "" }
}

# ----------------- JAVA RESOLVER -----------------
function Get-JavaVersionNumber($javaPath) {
    if (-not (Test-Path $javaPath)) { return 0 }
    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $javaPath
        $psi.Arguments = "-version"
        $psi.RedirectStandardError = $true
        $psi.RedirectStandardOutput = $true
        $psi.UseShellExecute = $false
        $proc = [System.Diagnostics.Process]::Start($psi)
        $proc.WaitForExit(3000) | Out-Null
        $out = $proc.StandardError.ReadToEnd() + $proc.StandardOutput.ReadToEnd()
        if ($out -match 'version "(1\.)?(\d+)') {
            if ($matches[1]) { return [int]$matches[2] }
            return [int]$matches[2]
        }
    } catch {}
    return 0
}

function Find-AllJavas {
    $paths = @()
    $cmd = Get-Command "java" -ErrorAction SilentlyContinue
    if ($cmd) { $paths += $cmd.Source }

    $dirs = @(
        "C:\Program Files\Eclipse Adoptium",
        "C:\Program Files\Java",
        "C:\Program Files\Microsoft",
        "$env:APPDATA\ElyPrismLauncher\java"
    )

    foreach ($d in $dirs) {
        if (Test-Path $d) {
            Get-ChildItem -Path $d -Filter "java.exe" -Recurse -Depth 4 -ErrorAction SilentlyContinue | ForEach-Object {
                $paths += $_.FullName
            }
        }
    }

    $results = @()
    foreach ($p in ($paths | Select-Object -Unique)) {
        $v = Get-JavaVersionNumber $p
        if ($v -gt 0) {
            $results += [PSCustomObject]@{ Path = $p; Version = $v }
        }
    }
    return ($results | Sort-Object -Property Version -Descending)
}

function Resolve-BestJava($targetMcVer) {
    if ($Config["java_path"] -ne "auto" -and (Test-Path $Config["java_path"])) {
        return $Config["java_path"]
    }
    $req = 21
    if ($targetMcVer -match '^1\.(\d+)') {
        $m = [int]$matches[1]
        if ($m -ge 21) { $req = 21 }
        elseif ($m -ge 17) { $req = 17 }
        else { $req = 8 }
    }

    $all = Find-AllJavas
    if ($all.Count -eq 0) { return "java.exe" }
    foreach ($j in $all) {
        if ($j.Version -eq $req) { return $j.Path }
    }
    if ($req -ge 21) {
        foreach ($j in $all) {
            if ($j.Version -ge 21) { return $j.Path }
        }
    }
    return $all[0].Path
}

# ----------------- MOJANG DOWNLOADER -----------------
function Fetch-Manifest {
    $wc = New-Object System.Net.WebClient
    $wc.Headers.Add("User-Agent", "lazymc/0.2.0")
    $jsonStr = $wc.DownloadString($MANIFEST_URL)
    return ($jsonStr | ConvertFrom-Json)
}

function Download-FileWithRetry($url, $dest) {
    $dir = Split-Path $dest
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    try {
        $wc = New-Object System.Net.WebClient
        $wc.Headers.Add("User-Agent", "lazymc/0.2.0")
        $wc.DownloadFile($url, $dest)
        return $true
    } catch {
        return $false
    }
}

function Download-FullVersion($verId) {
    $manifest = Fetch-Manifest
    $vEntry = $manifest.versions | Where-Object { $_.id -eq $verId }
    if (-not $vEntry) {
        Write-Host "$C_RED✗ $(T 'dl_ver_not_found' $verId)$C_RESET"
        return $false
    }

    $gDir = $Config["game_dir"]
    $verDir = Join-Path $gDir "versions\$verId"
    if (-not (Test-Path $verDir)) { New-Item -ItemType Directory -Path $verDir -Force | Out-Null }
    $verJsonPath = Join-Path $verDir "$verId.json"

    Write-Host "`n $C_CYAN[1/4] $(T 'checking_files')...$C_RESET"
    $wc = New-Object System.Net.WebClient
    $wc.Headers.Add("User-Agent", "lazymc/0.2.0")
    $vDataStr = $wc.DownloadString($vEntry.url)
    Set-Content -Path $verJsonPath -Value $vDataStr -Encoding UTF8
    $vData = $vDataStr | ConvertFrom-Json

    # Download client.jar
    $clientJar = Join-Path $verDir "$verId.jar"
    if ($vData.downloads.client) {
        Write-Host " $C_GREEN▶ client.jar...$C_RESET"
        Download-FileWithRetry $vData.downloads.client.url $clientJar | Out-Null
    }

    # Download Libraries
    Write-Host " $C_CYAN[2/4] Библиотеки...$C_RESET"
    $libsDir = Join-Path $gDir "libraries"
    $libs = $vData.libraries
    $count = 0
    $total = $libs.Count
    $nativeJars = @()

    foreach ($lib in $libs) {
        $count++
        $allowed = $true
        if ($lib.rules) {
            $allowed = $false
            foreach ($r in $lib.rules) {
                $m = $true
                if ($r.os -and $r.os.name -and $r.os.name -ne "windows") { $m = $false }
                if ($m) { $allowed = ($r.action -eq "allow") }
            }
        }
        if (-not $allowed) { continue }

        if ($lib.downloads.artifact) {
            $art = $lib.downloads.artifact
            $dest = Join-Path $libsDir ($art.path -replace '/', '\')
            if (-not (Test-Path $dest)) {
                Download-FileWithRetry $art.url $dest | Out-Null
            }
            if ($lib.name -like "*natives-windows*") { $nativeJars += $dest }
        }
        if ($lib.natives -and $lib.natives.windows) {
            $natKey = $lib.natives.windows
            if ($lib.downloads.classifiers -and $lib.downloads.classifiers.$natKey) {
                $cArt = $lib.downloads.classifiers.$natKey
                $dest = Join-Path $libsDir ($cArt.path -replace '/', '\')
                if (-not (Test-Path $dest)) {
                    Download-FileWithRetry $cArt.url $dest | Out-Null
                }
                $nativeJars += $dest
            }
        }
        if ($count % 5 -eq 0 -or $count -eq $total) {
            Render-ProgressBar $count $total "Libraries"
        }
    }

    # Extract Natives
    Write-Host "`n $C_CYAN[3/4] Распаковка natives (.dll)...$C_RESET"
    $natDir = Join-Path $verDir "natives"
    if (-not (Test-Path $natDir)) { New-Item -ItemType Directory -Path $natDir -Force | Out-Null }
    Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction SilentlyContinue
    foreach ($nj in $nativeJars) {
        if (Test-Path $nj) {
            try {
                $zip = [System.IO.Compression.ZipFile]::OpenRead($nj)
                foreach ($entry in $zip.Entries) {
                    if ($entry.FullName.EndsWith(".dll") -and -not $entry.FullName.StartsWith("META-INF/")) {
                        $targetDll = Join-Path $natDir $entry.Name
                        [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $targetDll, $true)
                    }
                }
                $zip.Dispose()
            } catch {}
        }
    }

    # Assets
    Write-Host " $C_CYAN[4/4] Ассеты и звуки...$C_RESET"
    if ($vData.assetIndex) {
        $idxDir = Join-Path $gDir "assets\indexes"
        if (-not (Test-Path $idxDir)) { New-Item -ItemType Directory -Path $idxDir -Force | Out-Null }
        $idxFile = Join-Path $idxDir "$($vData.assetIndex.id).json"
        Download-FileWithRetry $vData.assetIndex.url $idxFile | Out-Null

        if (Test-Path $idxFile) {
            $idxData = Get-Content $idxFile -Raw -Encoding UTF8 | ConvertFrom-Json
            $objs = $idxData.objects.PSObject.Properties
            $objTotal = $objs.Count
            $objCount = 0
            $objDir = Join-Path $gDir "assets\objects"

            foreach ($prop in $objs) {
                $objCount++
                $h = $prop.Value.hash
                $sub = $h.Substring(0, 2)
                $destObj = Join-Path $objDir "$sub\$h"
                if (-not (Test-Path $destObj)) {
                    $u = "https://resources.download.minecraft.net/$sub/$h"
                    Download-FileWithRetry $u $destObj | Out-Null
                }
                if ($objCount % 35 -eq 0 -or $objCount -eq $objTotal) {
                    Render-ProgressBar $objCount $objTotal "Assets"
                }
            }
        }
    }

    Write-Host "`n`n $C_GREEN✓ $(T 'dl_success' $verId)$C_RESET"
    return $true
}

# ----------------- LAUNCHER -----------------
function Get-OfflineUUID($nick) {
    $md5 = [System.Security.Cryptography.MD5]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes("OfflinePlayer:$nick")
    $hash = $md5.ComputeHash($bytes)
    $hash[6] = ($hash[6] -band 0x0F) -bor 0x30
    $hash[8] = ($hash[8] -band 0x3F) -bor 0x80
    return (New-Object System.Guid(,$hash)).ToString()
}

function Launch-Minecraft($verId) {
    $gDir = $Config["game_dir"]
    $verDir = Join-Path $gDir "versions\$verId"
    $verJson = Join-Path $verDir "$verId.json"
    $clientJar = Join-Path $verDir "$verId.jar"

    if (-not (Test-Path $verJson) -or -not (Test-Path $clientJar)) {
        Write-Host " $C_YELLOW⚠ $(T 'missing_files' 1)$C_RESET"
        Download-FullVersion $verId | Out-Null
    }

    $vData = Get-Content $verJson -Raw -Encoding UTF8 | ConvertFrom-Json
    $javaExe = Resolve-BestJava $verId
    $javaw = $javaExe -replace 'java\.exe$', 'javaw.exe'
    $runner = if (Test-Path $javaw) { $javaw } else { $javaExe }

    # Build Classpath
    $cpList = @()
    $libsDir = Join-Path $gDir "libraries"
    foreach ($lib in $vData.libraries) {
        $allowed = $true
        if ($lib.rules) {
            $allowed = $false
            foreach ($r in $lib.rules) {
                $m = $true
                if ($r.os -and $r.os.name -and $r.os.name -ne "windows") { $m = $false }
                if ($m) { $allowed = ($r.action -eq "allow") }
            }
        }
        if ($allowed -and $lib.downloads.artifact) {
            $artPath = Join-Path $libsDir ($lib.downloads.artifact.path -replace '/', '\')
            if (Test-Path $artPath) { $cpList += $artPath }
        }
    }
    $cpList += $clientJar
    $cpStr = $cpList -join ";"

    # Argfile for Classpath
    $argfile = Join-Path $verDir "lazymc_args.txt"
    Set-Content -Path $argfile -Value "-cp`n$cpStr" -Encoding UTF8

    $nick = $Config["username"]
    $uuid = Get-OfflineUUID $nick
    $natDir = Join-Path $verDir "natives"
    $assetsDir = Join-Path $gDir "assets"
    $assetIdx = if ($vData.assetIndex) { $vData.assetIndex.id } else { "legacy" }

    $jvmArgs = @(
        "-Xmx$($Config['ram_gb'])G",
        "-Xms1G",
        "-Djava.library.path=$natDir"
    )
    if ($Config["jvm_args"]) { $jvmArgs += $Config["jvm_args"].Split(" ") }

    if ($vData.arguments -and $vData.arguments.jvm) {
        $skipNext = $false
        foreach ($j in $vData.arguments.jvm) {
            if ($j -is [string]) {
                if ($j -eq "-cp") { $skipNext = $true; continue }
                if ($skipNext) { $skipNext = $false; continue }
                if ($j -like "*`${classpath}*") { continue }
                $val = $j -replace '\$\{natives_directory\}', $natDir `
                          -replace '\$\{launcher_name\}', 'lazymc' `
                          -replace '\$\{launcher_version\}', '0.2.0'
                if ($val -like "-Djava.library.path=*") {
                    $jvmArgs = $jvmArgs | Where-Object { $_ -notlike "-Djava.library.path=*" }
                }
                $jvmArgs += $val
            }
        }
    }

    # Game Args
    $gameArgs = @()
    if ($vData.arguments -and $vData.arguments.game) {
        foreach ($g in $vData.arguments.game) {
            if ($g -is [string]) {
                $val = $g -replace '\$\{auth_player_name\}', $nick `
                          -replace '\$\{version_name\}', $verId `
                          -replace '\$\{game_directory\}', $gDir `
                          -replace '\$\{assets_root\}', $assetsDir `
                          -replace '\$\{assets_index_name\}', $assetIdx `
                          -replace '\$\{auth_uuid\}', $uuid `
                          -replace '\$\{auth_access_token\}', '0' `
                          -replace '\$\{user_type\}', 'mojang' `
                          -replace '\$\{version_type\}', 'release'
                $gameArgs += $val
            }
        }
    } else {
        $gameArgs = @(
            "--username", $nick,
            "--version", $verId,
            "--gameDir", $gDir,
            "--assetsDir", $assetsDir,
            "--assetIndex", $assetIdx,
            "--uuid", $uuid,
            "--accessToken", "0",
            "--userType", "legacy"
        )
    }

    $mainClass = if ($vData.mainClass) { $vData.mainClass } else { "net.minecraft.client.main.Main" }

    Print-Banner
    Draw-Box (T 'launch_header') @(
        "Game:    $C_GREEN$verId$C_RESET",
        "Player:  $C_YELLOW$nick$C_RESET",
        "RAM:     $C_WHITE$($Config['ram_gb']) GB$C_RESET"
    )

    Write-Host "`n $C_CYAN$(T 'starting_jvm')$C_RESET`n"
    $fullArgs = $jvmArgs + "@$argfile" + $mainClass + $gameArgs

    $proc = Start-Process -FilePath $runner -ArgumentList $fullArgs -WorkingDirectory $gDir -PassThru
    Write-Host " $C_GREEN✓ $(T 'game_running' $proc.Id)$C_RESET"
    Write-Host " $C_GRAY$(T 'game_logs')$C_RESET`n"
    Start-Sleep -Seconds 2
}

# ----------------- CATALOG BROWSER -----------------
function Show-Catalog {
    Print-Banner
    Write-Host "`n $C_CYAN$(T 'dl_fetching_manifest')$C_RESET"
    try {
        $manifest = Fetch-Manifest
    } catch {
        Write-Host " $C_RED✗ $(T 'dl_manifest_error')$C_RESET"
        Read-Host "`nPress Enter..."
        return
    }

    $allV = $manifest.versions
    $jokeKeys = @("potato", "shareware", "infinite", "rv", "love", "combat", "vote", "_or_b")
    $jokes = @($allV | Where-Object { $id = $_.id.ToLower(); foreach ($k in $jokeKeys) { if ($id -like "*$k*") { return $true } }; return $false })
    $jokeIds = @($jokes | ForEach-Object { $_.id })

    $releases = @($allV | Where-Object { $_.type -eq "release" -and $jokeIds -notcontains $_.id })
    $snapshots = @($allV | Where-Object { $_.type -eq "snapshot" -and $jokeIds -notcontains $_.id })
    $old = @($allV | Where-Object { $_.type -in @("old_beta", "old_alpha") })

    $tabs = @{
        "1" = @{ Name = (T "cat_releases"); List = $releases }
        "2" = @{ Name = (T "cat_snapshots"); List = $snapshots }
        "3" = @{ Name = (T "cat_jokes"); List = $jokes }
        "4" = @{ Name = (T "cat_old"); List = $old }
    }

    $currentTab = "1"
    $page = 0
    $pageSize = 14
    $searchQ = ""

    while ($true) {
        Print-Banner
        $activeList = if ($searchQ) {
            @($allV | Where-Object { $_.id.ToLower() -like "*$($searchQ.ToLower())*" })
        } else {
            $tabs[$currentTab].List
        }

        $totalPages = [Math]::Max(1, [int][Math]::Ceiling($activeList.Count / $pageSize))
        if ($page -ge $totalPages) { $page = $totalPages - 1 }
        if ($page -lt 0) { $page = 0 }

        $pageItems = @($activeList | Select-Object -Skip ($page * $pageSize) -First $pageSize)

        $tabParts = @()
        foreach ($k in @("1", "2", "3", "4")) {
            $t = $tabs[$k]
            if ($k -eq $currentTab -and -not $searchQ) {
                $tabParts += "$C_GREEN$C_BOLD[$k] $($t.Name)$C_RESET"
            } else {
                $tabParts += "$C_GRAY[$k] $($t.Name)$C_RESET"
            }
        }
        $headerLine = if ($searchQ) { "🔍 ПОИСК: '$searchQ' ($($activeList.Count) найдено)" } else { $tabParts -join "   " }

        $boxLines = @(
            " $headerLine",
            "$C_GRAY$('-' * 66)$C_RESET",
            " $C_YELLOW$(T 'page_indicator' ($page+1) $totalPages $activeList.Count)$C_RESET",
            ""
        )

        $half = [int][Math]::Ceiling($pageItems.Count / 2)
        $col1 = @($pageItems | Select-Object -First $half)
        $col2 = @($pageItems | Select-Object -Skip $half)

        $maxRows = [Math]::Max($col1.Count, $col2.Count)
        for ($r = 0; $r -lt $maxRows; $r++) {
            $p1 = ""; $p2 = ""
            if ($r -lt $col1.Count) {
                $idx1 = $r + 1
                $vid1 = $col1[$r].id
                $extra = if ($vid1 -eq "24w14potato") { " $C_GRAY(Potato)$C_RESET" } `
                         elseif ($vid1 -eq "23w13a_or_b") { " $C_GRAY(Vote)$C_RESET" } `
                         elseif ($vid1 -eq "20w14infinite") { " $C_GRAY(Infinite)$C_RESET" } `
                         else { "" }
                $p1 = "$C_CYAN[#$($idx1.ToString().PadLeft(2))]$C_RESET $C_WHITE$($vid1.PadRight(15))$C_RESET$extra"
            }
            if ($r -lt $col2.Count) {
                $idx2 = $r + $half + 1
                $vid2 = $col2[$r].id
                $p2 = "$C_CYAN[#$($idx2.ToString().PadLeft(2))]$C_RESET $C_WHITE$($vid2.PadRight(15))$C_RESET"
            }
            $boxLines += " $($p1.PadRight(35)) $p2"
        }

        $boxLines += ""
        $boxLines += "$C_GRAY$('-' * 66)$C_RESET"
        $boxLines += " $C_CYAN[P]$C_RESET Вперед >   $C_CYAN[N]$C_RESET < Назад   $C_YELLOW[F]$C_RESET Поиск   $C_WHITE[B]$C_RESET Меню"

        Draw-Box (T "browser_title") $boxLines 74

        $prompt = if (-not $searchQ) { "`n Введите [1-4] (вкладки), [#1-14] или имя: " } else { "`n Введите [#1-14], имя или [B] для сброса: " }
        Write-Host -NoNewline "$C_CYAN$prompt$C_RESET"
        $choice = (Read-Host).Trim()

        if ($choice.ToUpper() -eq "B") {
            if ($searchQ) { $searchQ = ""; $page = 0; continue } else { break }
        }
        if ($choice -in @("1", "2", "3", "4") -and -not $searchQ) {
            $currentTab = $choice; $page = 0; continue
        }
        if ($choice.ToUpper() -in @("P", ">")) {
            if ($page + 1 -lt $totalPages) { $page++ }
            continue
        }
        if ($choice.ToUpper() -in @("N", "<")) {
            if ($page -gt 0) { $page-- }
            continue
        }
        if ($choice.ToUpper() -in @("F", "/")) {
            Write-Host -NoNewline "`n $C_YELLOWПоиск версии по названию: $C_RESET"
            $searchQ = (Read-Host).Trim()
            $page = 0
            continue
        }

        $targetVer = $null
        if ($choice -match '^#?(\d+)$') {
            $pickedIdx = [int]$matches[1] - 1
            if ($pickedIdx -ge 0 -and $pickedIdx -lt $pageItems.Count) {
                $targetVer = $pageItems[$pickedIdx].id
            }
        } else {
            $matchEntry = $allV | Where-Object { $_.id.ToLower() -eq $choice.ToLower() }
            if ($matchEntry) { $targetVer = $matchEntry[0].id }
        }

        if ($targetVer) {
            Write-Host "`n $C_GREENНачинаем загрузку Minecraft $targetVer...$C_RESET"
            Download-FullVersion $targetVer | Out-Null
            $Config["active_version"] = $targetVer
            Save-Config
            Read-Host "`nНажмите Enter..."
            break
        }
    }
}

# ----------------- MAIN LOOP -----------------
function Main {
    Load-Config
    $installed = @()
    $vDir = Join-Path $Config["game_dir"] "versions"
    if (Test-Path $vDir) {
        $installed = Get-ChildItem -Path $vDir -Directory | ForEach-Object {
            if ((Test-Path (Join-Path $_.FullName "$($_.Name).json")) -and (Test-Path (Join-Path $_.FullName "$($_.Name).jar"))) {
                $_.Name
            }
        }
    }
    if (-not $Config["active_version"] -and $installed.Count -gt 0) {
        $Config["active_version"] = $installed[0]
        Save-Config
    }

    while ($true) {
        Print-Banner
        $activeVerDisplay = if ($Config["active_version"]) { "$C_GREEN$($Config['active_version'])" } else { "$C_RED$(T 'status_no_version')" }
        $resolvedJ = Resolve-BestJava $Config["active_version"]
        $jNum = Get-JavaVersionNumber $resolvedJ
        $jDisplay = if ($jNum -gt 0) { "Auto (Java $jNum)" } else { "Auto (not found)" }

        $statusLines = @(
            "$C_YELLOW$(T 'user'):$C_RESET       $C_WHITE$($Config['username'])$C_RESET",
            "$C_YELLOW$(T 'ram'):$C_RESET        $C_WHITE$($Config['ram_gb']) GB$C_RESET",
            "$C_YELLOW$(T 'version'):$C_RESET    $activeVerDisplay$C_RESET",
            "$C_YELLOW$(T 'java'):$C_RESET   $C_WHITE$jDisplay$C_RESET",
            "$C_YELLOW$(T 'lang'):$C_RESET       $C_WHITE$($CurrentLang.ToUpper())$C_RESET"
        )
        Draw-Box (T "menu_title") $statusLines

        Write-Host ""
        Write-Host "  $C_GREEN[1] 🚀 $(T 'opt_launch')$C_RESET"
        Write-Host "  $C_CYAN[2] 📦 $(T 'opt_versions')$C_RESET"
        Write-Host "  $C_YELLOW[3] 👤 $(T 'opt_user')$C_RESET"
        Write-Host "  $C_WHITE[4] ⚙️  $(T 'opt_settings')$C_RESET"
        Write-Host "  $C_WHITE[5] 🌐 $(T 'opt_lang')$C_RESET"
        Write-Host "  $C_CYAN[6] 🔄 $(T 'opt_update')$C_RESET"
        Write-Host "  $C_RED[7] 🚪 $(T 'opt_exit')$C_RESET"
        Write-Host "`n$C_GRAY ────────────────────────────────────────────────────────$C_RESET"

        Write-Host -NoNewline " $C_CYAN$(T 'enter_choice')$C_RESET"
        $choice = (Read-Host).Trim()

        if ($choice -eq "1") {
            if (-not $Config["active_version"]) {
                Write-Host "`n $C_RED✗ $(T 'status_no_version')$C_RESET"
                Start-Sleep -Seconds 2
            } else {
                Launch-Minecraft $Config["active_version"]
            }
        }
        elseif ($choice -eq "2") {
            Show-Catalog
        }
        elseif ($choice -eq "3") {
            Print-Banner
            Draw-Box (T "nick_title") @("$(T 'current_nick'): $C_YELLOW$($Config['username'])$C_RESET")
            Write-Host -NoNewline "`n$C_CYAN$(T 'enter_nick')$C_RESET"
            $newNick = (Read-Host).Trim()
            if ($newNick) {
                $Config["username"] = $newNick
                Save-Config
                Write-Host "`n $C_GREEN✓ $(T 'nick_saved')$C_RESET"
                Start-Sleep -Seconds 1
            }
        }
        elseif ($choice -eq "4") {
            Print-Banner
            $sLines = @(
                "$C_CYAN[1]$C_RESET $(T 'set_ram_opt' $Config['ram_gb'])",
                "$C_CYAN[2]$C_RESET $(T 'set_jvm_opt' $Config['jvm_args'])",
                "$C_YELLOW[3]$C_RESET $(T 'back_to_menu')"
            )
            Draw-Box (T "settings_title") $sLines
            Write-Host -NoNewline "`n$C_CYAN$(T 'enter_choice')$C_RESET"
            $sChoice = (Read-Host).Trim()
            if ($sChoice -eq "1") {
                Write-Host -NoNewline "`n$C_CYAN$(T 'enter_ram')$C_RESET"
                $newRam = (Read-Host).Trim()
                if ($newRam -match '^\d+$') {
                    $Config["ram_gb"] = [int]$newRam
                    Save-Config
                    Write-Host " $C_GREEN✓ $(T 'settings_saved')$C_RESET"
                    Start-Sleep -Seconds 1
                }
            }
            elseif ($sChoice -eq "2") {
                Write-Host -NoNewline "`n$C_CYANExtra JVM args: $C_RESET"
                $Config["jvm_args"] = (Read-Host).Trim()
                Save-Config
                Write-Host " $C_GREEN✓ $(T 'settings_saved')$C_RESET"
                Start-Sleep -Seconds 1
            }
        }
        elseif ($choice -eq "5") {
            Print-Banner
            Draw-Box "LANGUAGE" @("[1] Auto", "[2] Русский", "[3] Українська", "[4] English")
            Write-Host -NoNewline "`n$C_CYAN$(T 'enter_choice')$C_RESET"
            $lChoice = (Read-Host).Trim()
            if ($lChoice -eq "1") { $Config["language"] = "auto"; $global:CurrentLang = Get-SystemLang }
            if ($lChoice -eq "2") { $Config["language"] = "ru"; $global:CurrentLang = "ru" }
            if ($lChoice -eq "3") { $Config["language"] = "uk"; $global:CurrentLang = "uk" }
            if ($lChoice -eq "4") { $Config["language"] = "en"; $global:CurrentLang = "en" }
            Save-Config
            Start-Sleep -Seconds 1
        }
        elseif ($choice -eq "6") {
            Print-Banner
            Draw-Box (T "update_title") @((T "update_checking"))
            try {
                $wc = New-Object System.Net.WebClient
                $vJson = $wc.DownloadString("$REPO_RAW_URL/version.json") | ConvertFrom-Json
                $remoteVer = $vJson.version
                if ($remoteVer -ne "0.2.0") {
                    Print-Banner
                    Draw-Box (T "update_title") @(
                        "$C_GREEN★ $(T 'update_available' $remoteVer '0.2.0')$C_RESET",
                        "Notes: $($vJson.notes)"
                    )
                    Write-Host -NoNewline "`n$C_CYAN$(T 'update_prompt')$C_RESET"
                    $ans = (Read-Host).Trim()
                    if ($ans -in @("y", "yes", "д", "да", "1")) {
                        $wc.DownloadFile("$REPO_RAW_URL/lazymc-ps.bat", $MyInvocation.MyCommand.Path)
                        Write-Host "`n $C_GREEN✓ $(T 'update_success')$C_RESET"
                        Read-Host "Press Enter..."
                    }
                } else {
                    Print-Banner
                    Draw-Box (T "update_title") @("$C_GREEN✓ $(T 'update_latest') (v0.2.0)$C_RESET")
                    Start-Sleep -Seconds 2
                }
            } catch {
                Write-Host "Error checking updates."
                Start-Sleep -Seconds 2
            }
        }
        elseif ($choice -eq "7") {
            Print-Banner
            Write-Host "`n  $C_GREENGoodbye! До зустрічі! Пока!$C_RESET`n"
            break
        }
    }
}

Main
