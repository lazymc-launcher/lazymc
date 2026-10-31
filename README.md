# ⚡ lazymc `v0.1.2`

> A lightning-fast, lightweight terminal launcher for Minecraft with zero bloat and zero manual setup.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg)](https://microsoft.com/windows)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)

---

```
  _                                   
 | | __ _ _____   _ _ __ ___   ___    
 | |/ _` |_  / | | | '_ ` _ \ / __|   
 | | (_| |/ /| |_| | | | | | | (__    
 |_|\__,_/___|\__, |_| |_| |_|\___|   
              |___/                               v0.1.2
```

---

## 🌟 Key Features

- **⚡ Zero Manual Setup (Self-Bootstrapping)**:
  - If Python is not installed on the system, `lazymc.bat` automatically provisions official, isolated portable Python 3.11 embeddable in seconds. No administrator permissions or manual Python installations needed.
- **📦 Comprehensive Mojang Version Catalog**:
  - Connects directly to the official Mojang version manifest API (`piston-meta.mojang.com`).
  - **Releases**: All official releases from the latest versions back to legacy releases.
  - **Snapshots**: Development previews and test builds.
  - **April Fools Updates**: Special joke versions with descriptions (e.g. `24w14potato` Poisonous Potato, `23w13a_or_b` The Vote Update, `20w14infinite` Infinite Dimensions, `3D Shareware v1.34`, `1.RV-Pre1` Trendy Update).
  - **Nostalgia (Beta / Alpha)**: Classic legacy versions.
- **🔄 Pre-Launch Dependency Self-Healing**:
  - Automatically verifies the integrity of the selected version prior to launching.
  - Detects missing `client.jar`, libraries, assets, or native `.dll` files and downloads only what is missing without crashing.
- **☕ Intelligent Java Runtime Resolver**:
  - Automatically scans for installed Java runtimes across the system (Adoptium, Microsoft OpenJDK, Oracle, Prism/MultiMC runtimes).
  - Matches the required Java version to the target Minecraft version (Java 21+ for modern versions, Java 17 for 1.17–1.20, Java 8 for legacy builds).
- **🌍 Trilingual Interface**:
  - Auto-detects the system display language via Windows API (`uk` Ukrainian, `ru` Russian, `en` English fallback).
  - Allows manual language switching at any time.
- **🛡️ Windows Command-Line Length Limit Bypass**:
  - Uses modern Java 9+ `@argfile` parameters to bypass the Windows 8,191-character command prompt limit, preventing crashes on heavily modded or library-dense versions.
- **🖥️ Live Console Log Streaming**:
  - Real-time game process output streaming with color-coded log levels (`ERROR` in red, `WARN` in yellow).
  - Press `Ctrl+C` to return to the launcher menu while keeping the game running in the background.

---

## 🚀 Quick Start

### 1. Clone the repository
```cmd
git clone https://github.com/lazymc-launcher/lazymc.git
cd lazymc
```

### 2. Launch
Double-click **`lazymc.bat`** or run:
```cmd
python main.py
```
*(If Python is not installed on your system, `lazymc.bat` will automatically download and configure portable Python for you).*

---

## ⌨️ Navigation & Controls

| Key | Action | Description |
|---|---|---|
| `[1]` | **Launch Game** | Verifies dependencies, starts JVM, and launches Minecraft |
| `[2]` | **Version Manager** | Select installed versions or open the Mojang catalog |
| `[3]` | **Change Nickname** | Sets the offline player profile nickname and generates UUID |
| `[4]` | **Settings** | Configure RAM allocation (Xmx), Java executable, game directory |
| `[5]` | **Language** | Switch language between English, Русский, and Українська |
| `[6]` | **Exit** | Close the launcher |

### Version Catalog Navigation:
- `[1]`, `[2]`, `[3]`, `[4]` — Switch between tabs (**Releases**, **Snapshots**, **April Fools**, **Beta/Alpha**)
- `[P]` / `[N]` — Next / Previous page
- `[F]` — Search version by keyword
- `[#1]` – `[#14]` — Immediately download and activate an item from the current page

---

## ⚙️ Configuration

Settings are saved in `%APPDATA%\.lazymc\config.json`:

```json
{
    "username": "Player",
    "language": "auto",
    "ram_gb": 4,
    "game_dir": "C:\\Users\\<user>\\AppData\\Roaming\\.minecraft",
    "active_version": "1.21.1",
    "java_path": "auto",
    "jvm_args": "-XX:+UseG1GC",
    "window_width": 854,
    "window_height": 480
}
```

---

## 📁 Project Structure

```
lazymc/
├── lazymc.bat          # Windows self-bootstrapping launcher script
├── main.py             # CLI entry point, menu loops, and user flow
├── mojang.py           # Mojang manifest fetching, multithreaded downloader
├── launcher.py         # JVM argument parsing, classpath argfile builder
├── java_detector.py    # Automatic JVM runtime scanner and compatibility resolver
├── config.py           # Persistent configuration management
├── ui.py               # TUI rendering, ANSI styling, text-wrapping box layouts
├── i18n.py             # Translations and system locale auto-detection
├── LICENSE             # Apache 2.0 License
└── README.md           # Documentation
```

---

## 📜 License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
