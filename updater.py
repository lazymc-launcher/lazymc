"""
lazymc updater module
Checks for updates on GitHub and applies them automatically.
"""

import os
import sys
import json
import shutil
import urllib.request
import subprocess

CURRENT_VERSION = "0.2.0"
REPO_RAW_URL = "https://raw.githubusercontent.com/lazymc-launcher/lazymc/main"
VERSION_CHECK_URL = f"{REPO_RAW_URL}/version.json"

CORE_FILES = [
    "main.py",
    "mojang.py",
    "launcher.py",
    "ui.py",
    "i18n.py",
    "config.py",
    "java_detector.py",
    "updater.py",
    "version.json",
    "lazymc.bat"
]


def parse_version(ver_str: str) -> tuple:
    """Converts version string '0.2.0' into tuple (0, 2, 0)."""
    clean = ver_str.strip().lstrip("v")
    parts = []
    for x in clean.split("."):
        if x.isdigit():
            parts.append(int(x))
    return tuple(parts)


def check_for_updates() -> dict:
    """
    Checks if an update is available on GitHub.
    Returns dict with update info if available, or None.
    """
    try:
        req = urllib.request.Request(
            VERSION_CHECK_URL,
            headers={"User-Agent": f"lazymc/{CURRENT_VERSION}"}
        )
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        remote_ver_str = data.get("version", "")
        if not remote_ver_str:
            return None

        if parse_version(remote_ver_str) > parse_version(CURRENT_VERSION):
            return {
                "available": True,
                "current": CURRENT_VERSION,
                "latest": remote_ver_str,
                "notes": data.get("notes", "")
            }
    except Exception:
        pass
    return None


def apply_update(project_dir: str, progress_callback=None) -> bool:
    """
    Downloads and applies updates to the launcher.
    Uses git pull if git repository, otherwise downloads files directly from raw.githubusercontent.com.
    """
    git_dir = os.path.join(project_dir, ".git")
    if os.path.exists(git_dir) and shutil.which("git"):
        try:
            res = subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=15
            )
            if res.returncode == 0:
                return True
        except Exception:
            pass

    # Direct file download fallback
    total = len(CORE_FILES)
    for idx, fname in enumerate(CORE_FILES, 1):
        file_url = f"{REPO_RAW_URL}/{fname}"
        dest_path = os.path.join(project_dir, fname)
        try:
            req = urllib.request.Request(file_url, headers={"User-Agent": f"lazymc/{CURRENT_VERSION}"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read()
            with open(dest_path, "wb") as f:
                f.write(content)
        except Exception as e:
            pass
        if progress_callback:
            progress_callback(idx, total, fname)

    return True
