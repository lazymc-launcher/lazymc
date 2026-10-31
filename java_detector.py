"""
lazymc java_detector module
Detects installed Java runtimes, inspects versions, and resolves compatibility.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path


def get_java_version(executable_path: str) -> int:
    """Returns the major version of Java (e.g., 8, 17, 21, 25), or 0 if unknown."""
    if not executable_path or not os.path.exists(executable_path):
        return 0
    try:
        proc = subprocess.run(
            [executable_path, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        output = proc.stderr or proc.stdout
        # Examples:
        # "1.8.0_301" -> 8
        # "17.0.2" -> 17
        # "21.0.1" -> 21
        match = re.search(r'version "(1\.)?(\d+)', output)
        if match:
            if match.group(1): # "1.8" -> 8
                return int(match.group(2))
            return int(match.group(2))
    except Exception:
        pass
    return 0


def find_all_javas() -> list:
    """Finds all java.exe executables on the system with their versions."""
    candidates = set()

    # 1. From PATH
    which_java = shutil.which("java")
    if which_java:
        candidates.add(os.path.normpath(which_java))

    # 2. Search common locations
    search_dirs = [
        r"C:\Program Files\Eclipse Adoptium",
        r"C:\Program Files\Java",
        r"C:\Program Files\Microsoft",
        r"C:\Program Files\BellSoft",
        r"C:\Program Files\Zulu",
        os.path.expandvars(r"%APPDATA%\ElyPrismLauncher\java"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Eclipse Adoptium")
    ]

    for s_dir in search_dirs:
        if os.path.isdir(s_dir):
            try:
                for root, _, files in os.walk(s_dir):
                    if "java.exe" in [f.lower() for f in files]:
                        candidates.add(os.path.normpath(os.path.join(root, "java.exe")))
            except Exception:
                pass

    results = []
    for c in sorted(candidates):
        ver = get_java_version(c)
        if ver > 0:
            results.append({
                "path": c,
                "version": ver
            })

    # Sort descending by version
    results.sort(key=lambda x: x["version"], reverse=True)
    return results


def get_required_java_version(mc_version_str: str) -> int:
    """Determines required major Java version for a given Minecraft version string."""
    if not mc_version_str:
        return 21
    
    # Extract major.minor (e.g. 1.21.1 -> 1.21; 26.3 -> 26)
    match = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?', mc_version_str)
    if not match:
        return 21

    v1, v2 = int(match.group(1)), int(match.group(2))
    v3 = int(match.group(3)) if match.group(3) else 0

    if v1 >= 26:
        return 21
    if v1 == 1:
        if v2 >= 21 or (v2 == 20 and v3 >= 5):
            return 21
        elif v2 >= 17:
            return 17
        else:
            return 8
    return 21


def resolve_best_java(configured_path: str, required_major: int = 21) -> str:
    """Returns the most appropriate java.exe path."""
    if configured_path and configured_path != "auto" and os.path.exists(configured_path):
        return configured_path

    all_javas = find_all_javas()
    if not all_javas:
        # Fallback to system command 'java' or 'javaw'
        return "javaw"

    # Exact match for required version
    for j in all_javas:
        if j["version"] == required_major:
            return j["path"]

    # If required >= 21, any >= 21 is fine
    if required_major >= 21:
        for j in all_javas:
            if j["version"] >= 21:
                return j["path"]

    # Otherwise return the newest one
    return all_javas[0]["path"]
