"""
lazymc launcher module
Assembles classpath, resolves arguments, checks Java compatibility, and launches Minecraft.
"""

import os
import sys
import json
import uuid
import hashlib
import subprocess
from pathlib import Path
from java_detector import get_java_version, resolve_best_java, get_required_java_version
from mojang import rule_matches_windows


def get_offline_uuid(username: str) -> str:
    """Generates standard Minecraft offline player UUID (MD5 hash)."""
    h = hashlib.md5(f"OfflinePlayer:{username}".encode("utf-8")).digest()
    # RFC 4122 version 3
    byte_array = bytearray(h)
    byte_array[6] = (byte_array[6] & 0x0f) | 0x30  # Version 3
    byte_array[8] = (byte_array[8] & 0x3f) | 0x80  # Variant 1
    return str(uuid.UUID(bytes=bytes(byte_array)))


def resolve_args(arg_list: list, replacements: dict, features: dict = None) -> list:
    """Resolves string and rule-based argument items from version JSON."""
    result = []
    for item in arg_list:
        if isinstance(item, str):
            val = item
            for k, v in replacements.items():
                val = val.replace(k, str(v))
            result.append(val)
        elif isinstance(item, dict):
            rules = item.get("rules", [])
            if rule_matches_windows(rules, features):
                values = item.get("value", [])
                if isinstance(values, str):
                    values = [values]
                for v in values:
                    val = v
                    for rk, rv in replacements.items():
                        val = val.replace(rk, str(rv))
                    result.append(val)
    return result


def launch_game(config: dict, version_id: str) -> subprocess.Popen:
    """Constructs launch command and starts the Minecraft game process."""
    game_dir = config["game_dir"]
    version_dir = os.path.join(game_dir, "versions", version_id)
    version_json_path = os.path.join(version_dir, f"{version_id}.json")
    client_jar_path = os.path.join(version_dir, f"{version_id}.jar")

    if not os.path.exists(version_json_path):
        raise FileNotFoundError(f"Version JSON not found: {version_json_path}")
    if not os.path.exists(client_jar_path):
        raise FileNotFoundError(f"Client JAR not found: {client_jar_path}")

    with open(version_json_path, "r", encoding="utf-8") as f:
        v_data = json.load(f)

    # 1. Resolve Java executable
    req_java = get_required_java_version(version_id)
    java_exe = resolve_best_java(config.get("java_path", "auto"), req_java)

    # 2. Build Classpath
    cp_entries = []
    libs_dir = os.path.join(game_dir, "libraries")

    for lib in v_data.get("libraries", []):
        if not rule_matches_windows(lib.get("rules", [])):
            continue
        artifact = lib.get("downloads", {}).get("artifact")
        if artifact and artifact.get("path"):
            full_path = os.path.join(libs_dir, artifact["path"].replace("/", os.sep))
            if os.path.exists(full_path):
                cp_entries.append(full_path)
            else:
                # If artifact path not directly downloaded, search library by name
                pass

    cp_entries.append(client_jar_path)
    classpath_str = ";".join(cp_entries)

    # 3. Environment variables & placeholders
    username = config.get("username", "Player")
    player_uuid = get_offline_uuid(username)
    natives_dir = os.path.join(version_dir, "natives")
    assets_dir = os.path.join(game_dir, "assets")
    asset_index = v_data.get("assetIndex", {}).get("id", "legacy")
    main_class = v_data.get("mainClass", "net.minecraft.client.main.Main")

    replacements = {
        "${auth_player_name}": username,
        "${version_name}": version_id,
        "${game_directory}": game_dir,
        "${assets_root}": assets_dir,
        "${game_assets}": assets_dir,
        "${assets_index_name}": asset_index,
        "${auth_uuid}": player_uuid,
        "${auth_access_token}": "0",
        "${clientid}": "0",
        "${auth_xuid}": "0",
        "${user_type}": "mojang",
        "${version_type}": v_data.get("type", "release"),
        "${classpath}": classpath_str,
        "${natives_directory}": natives_dir,
        "${launcher_name}": "lazymc",
        "${launcher_version}": "1.0.0",
        "${resolution_width}": str(config.get("window_width", 854)),
        "${resolution_height}": str(config.get("window_height", 480))
    }

    features = {
        "has_custom_resolution": True,
        "is_demo_user": False,
        "has_quick_plays_support": False,
        "is_quick_play_singleplayer": False,
        "is_quick_play_multiplayer": False,
        "is_quick_play_realms": False
    }

    # 4. Write classpath argfile to avoid Windows 8191 CMD length limit
    argfile_path = os.path.join(version_dir, "lazymc_args.txt")
    with open(argfile_path, "w", encoding="utf-8") as f:
        f.write("-cp\n")
        f.write(f"{classpath_str}\n")
    
    # 5. Build JVM arguments
    jvm_args = [
        f"-Xmx{config.get('ram_gb', 4)}G",
        "-Xms1G",
        f"-Djava.library.path={natives_dir}"
    ]

    extra_jvm = config.get("jvm_args", "").strip()
    if extra_jvm:
        jvm_args.extend(extra_jvm.split())

    args_spec = v_data.get("arguments", {})
    if "jvm" in args_spec:
        # Filter out -cp and ${classpath} as they are passed via @argfile
        filtered_jvm_spec = []
        skip_next = False
        for item in args_spec["jvm"]:
            if isinstance(item, str):
                if item == "-cp":
                    skip_next = True
                    continue
                if skip_next:
                    skip_next = False
                    continue
                if "${classpath}" in item:
                    continue
                filtered_jvm_spec.append(item)
            else:
                filtered_jvm_spec.append(item)

        custom_jvm = resolve_args(filtered_jvm_spec, replacements, features)
        for cj in custom_jvm:
            # If version JSON specifies custom library path, override the default
            if cj.startswith("-Djava.library.path="):
                jvm_args = [a for a in jvm_args if not a.startswith("-Djava.library.path=")]
            jvm_args.append(cj)

    # 6. Build Game arguments
    if "game" in args_spec:
        game_args = resolve_args(args_spec["game"], replacements, features)
    elif "minecraftArguments" in v_data:
        legacy_template = v_data["minecraftArguments"]
        for k, v in replacements.items():
            legacy_template = legacy_template.replace(k, str(v))
        game_args = legacy_template.split()
    else:
        game_args = [
            "--username", username,
            "--version", version_id,
            "--gameDir", game_dir,
            "--assetsDir", assets_dir,
            "--assetIndex", asset_index,
            "--uuid", player_uuid,
            "--accessToken", "0",
            "--userType", "legacy"
        ]

    # Full command
    # Using @argfile for classpath works cleanly on Java 9+
    # Also verify if javaw exists in the same folder as java.exe for clean window launch
    javaw_candidate = os.path.join(os.path.dirname(java_exe), "javaw.exe")
    exe_to_run = javaw_candidate if os.path.exists(javaw_candidate) else java_exe

    cmd = [exe_to_run] + jvm_args + [f"@{argfile_path}", main_class] + game_args

    proc = subprocess.Popen(
        cmd,
        cwd=game_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    return proc
