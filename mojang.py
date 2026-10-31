"""
lazymc mojang module
Fetches manifests, downloads Minecraft versions, libraries, natives, and assets from Mojang.
"""

import os
import json
import zipfile
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
RESOURCES_BASE_URL = "https://resources.download.minecraft.net"


def fetch_manifest() -> dict:
    """Fetches the official version manifest v2 from Mojang."""
    req = urllib.request.Request(
        MANIFEST_URL,
        headers={"User-Agent": "lazymc/1.0 (Minecraft CLI Launcher)"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def rule_matches_windows(rules: list, features: dict = None) -> bool:
    """Evaluates rule list for Windows OS and launcher features."""
    if not rules:
        return True
    if features is None:
        features = {}
    allowed = False
    for r in rules:
        action = r.get("action")
        os_spec = r.get("os", {})
        os_name = os_spec.get("name")
        feat_spec = r.get("features", {})
        
        matches = True
        if os_name and os_name != "windows":
            matches = False

        if feat_spec:
            for feat_k, feat_v in feat_spec.items():
                if features.get(feat_k) != feat_v:
                    matches = False
                    break

        if matches:
            allowed = (action == "allow")
    return allowed


def download_file(url: str, dest_path: str, expected_size: int = None) -> bool:
    """Downloads a file if not already existing with the right size."""
    if os.path.exists(dest_path):
        if expected_size is None or os.path.getsize(dest_path) == expected_size:
            return True

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "lazymc/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp, open(dest_path, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
        return True
    except Exception as e:
        # Clean up partial download
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except Exception:
                pass
        return False


def extract_natives(native_jars: list, natives_dir: str):
    """Extracts .dll files from native jar archives into the natives directory."""
    os.makedirs(natives_dir, exist_ok=True)
    for jar_path in native_jars:
        if not os.path.exists(jar_path):
            continue
        try:
            with zipfile.ZipFile(jar_path, 'r') as zf:
                for member in zf.namelist():
                    if member.startswith("META-INF/") or member.endswith("/"):
                        continue
                    if member.endswith(".dll"):
                        filename = os.path.basename(member)
                        target = os.path.join(natives_dir, filename)
                        with zf.open(member) as src, open(target, "wb") as dst:
                            dst.write(src.read())
        except Exception:
            pass


def download_full_version(version_id: str, game_dir: str, progress_callback=None) -> bool:
    """
    Downloads client.jar, libraries, natives, and assets for the specified version.
    progress_callback(stage: str, current: int, total: int)
    """
    manifest = fetch_manifest()
    ver_info = next((v for v in manifest.get("versions", []) if v["id"] == version_id), None)
    if not ver_info:
        raise ValueError(f"Version {version_id} not found in manifest")

    # 1. Fetch version JSON
    version_dir = os.path.join(game_dir, "versions", version_id)
    os.makedirs(version_dir, exist_ok=True)
    version_json_path = os.path.join(version_dir, f"{version_id}.json")

    if progress_callback:
        progress_callback("meta", 0, 1)

    req = urllib.request.Request(ver_info["url"], headers={"User-Agent": "lazymc/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        v_data = json.loads(resp.read().decode("utf-8"))

    with open(version_json_path, "w", encoding="utf-8") as f:
        json.dump(v_data, f, indent=2)

    # 2. Download client.jar
    client_dl = v_data.get("downloads", {}).get("client", {})
    client_jar_path = os.path.join(version_dir, f"{version_id}.jar")
    if client_dl.get("url"):
        if progress_callback:
            progress_callback("client", 0, 1)
        download_file(client_dl["url"], client_jar_path, client_dl.get("size"))
        if progress_callback:
            progress_callback("client", 1, 1)

    # 3. Download Libraries
    libraries_to_dl = []
    native_jars = []
    libs_dir = os.path.join(game_dir, "libraries")

    for lib in v_data.get("libraries", []):
        rules = lib.get("rules", [])
        if not rule_matches_windows(rules):
            continue

        downloads = lib.get("downloads", {})
        # Artifact
        artifact = downloads.get("artifact")
        if artifact and artifact.get("url"):
            path = artifact.get("path")
            dest = os.path.join(libs_dir, path.replace("/", os.sep))
            libraries_to_dl.append((artifact["url"], dest, artifact.get("size")))

        # Classifiers (Natives for older versions)
        classifiers = downloads.get("classifiers", {})
        natives = lib.get("natives", {})
        nat_key = natives.get("windows")
        if nat_key and nat_key in classifiers:
            nat_artifact = classifiers[nat_key]
            if nat_artifact.get("url"):
                path = nat_artifact.get("path")
                dest = os.path.join(libs_dir, path.replace("/", os.sep))
                libraries_to_dl.append((nat_artifact["url"], dest, nat_artifact.get("size")))
                native_jars.append(dest)
        elif "natives-windows" in lib.get("name", ""):
            # Modern LWJGL native jar
            if artifact:
                dest = os.path.join(libs_dir, artifact["path"].replace("/", os.sep))
                native_jars.append(dest)

    total_libs = len(libraries_to_dl)
    done_libs = 0
    if progress_callback:
        progress_callback("libraries", 0, total_libs)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_file, url, dest, size): dest for url, dest, size in libraries_to_dl}
        for future in as_completed(futures):
            done_libs += 1
            if progress_callback:
                progress_callback("libraries", done_libs, total_libs)

    # 4. Extract natives
    natives_dir = os.path.join(version_dir, "natives")
    if progress_callback:
        progress_callback("natives", 0, 1)
    extract_natives(native_jars, natives_dir)
    if progress_callback:
        progress_callback("natives", 1, 1)

    # 5. Download Assets
    asset_index = v_data.get("assetIndex")
    if asset_index:
        index_id = asset_index.get("id")
        index_url = asset_index.get("url")
        indexes_dir = os.path.join(game_dir, "assets", "indexes")
        os.makedirs(indexes_dir, exist_ok=True)
        index_file = os.path.join(indexes_dir, f"{index_id}.json")

        download_file(index_url, index_file, asset_index.get("size"))

        if os.path.exists(index_file):
            with open(index_file, "r", encoding="utf-8") as f:
                index_data = json.load(f)

            objects = index_data.get("objects", {})
            assets_to_dl = []
            objects_dir = os.path.join(game_dir, "assets", "objects")

            for obj_name, obj_info in objects.items():
                hash_val = obj_info["hash"]
                sub = hash_val[:2]
                asset_url = f"{RESOURCES_BASE_URL}/{sub}/{hash_val}"
                dest = os.path.join(objects_dir, sub, hash_val)
                assets_to_dl.append((asset_url, dest, obj_info.get("size")))

            total_assets = len(assets_to_dl)
            done_assets = 0
            if progress_callback:
                progress_callback("assets", 0, total_assets)

            with ThreadPoolExecutor(max_workers=16) as executor:
                futures = {executor.submit(download_file, url, dest, size): dest for url, dest, size in assets_to_dl}
                for future in as_completed(futures):
                    done_assets += 1
                    if done_assets % 25 == 0 or done_assets == total_assets:
                        if progress_callback:
                            progress_callback("assets", done_assets, total_assets)

    return True


def check_missing_dependencies(version_id: str, game_dir: str) -> list:
    """Checks for missing files (client.jar, libraries, natives) for a given version."""
    version_dir = os.path.join(game_dir, "versions", version_id)
    version_json_path = os.path.join(version_dir, f"{version_id}.json")
    client_jar_path = os.path.join(version_dir, f"{version_id}.jar")

    missing = []
    if not os.path.exists(version_json_path):
        return ["version_json"]
    if not os.path.exists(client_jar_path):
        missing.append("client_jar")

    try:
        with open(version_json_path, "r", encoding="utf-8") as f:
            v_data = json.load(f)

        libs_dir = os.path.join(game_dir, "libraries")
        for lib in v_data.get("libraries", []):
            if not rule_matches_windows(lib.get("rules", [])):
                continue
            artifact = lib.get("downloads", {}).get("artifact")
            if artifact and artifact.get("path"):
                dest = os.path.join(libs_dir, artifact["path"].replace("/", os.sep))
                if not os.path.exists(dest):
                    missing.append(artifact["path"])

        # Check natives directory
        natives_dir = os.path.join(version_dir, "natives")
        if not os.path.exists(natives_dir) or not os.listdir(natives_dir):
            missing.append("natives")

    except Exception:
        pass

    return missing

