import subprocess
import re
import os
import sys

import csv
from datetime import datetime

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paths.csv")
EXECUTABLES = ["arma3.exe", "arma3_x64.exe", "arma3battleye.exe"]

def get_path_from_csv(path_type):
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['type', 'path', 'comment'])
            writer.writeheader()
        return None
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['type'] == path_type:
                return row['path']
    return None

def set_path_in_csv(path_type, path, comment=None):
    rows = []
    found = False
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['type'] == path_type:
                    row['path'] = path
                    if comment is not None:
                        row['comment'] = comment
                    found = True
                rows.append(row)
    if not found:
        rows.append({'type': path_type, 'path': path, 'comment': comment or ''})
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['type', 'path', 'comment'])
        writer.writeheader()
        writer.writerows(rows)

def get_arma_path():
    path = get_path_from_csv('arma')
    while True:
        if path and os.path.isdir(path):
            # Only accept if at least one executable exists
            if any(os.path.isfile(os.path.join(path, exe)) for exe in EXECUTABLES):
                return path
            else:
                print(f"Directory exists but no Arma 3 executables found in: {path}")
        path = input("Enter the PATH to your Arma 3 folder: ").strip().strip('"')
        if not os.path.isdir(path):
            print(f"Directory not found: {path}")
            path = None
            continue
        if not any(os.path.isfile(os.path.join(path, exe)) for exe in EXECUTABLES):
            print(f"No Arma 3 executables found in: {path}")
            path = None
            continue
        set_path_in_csv('arma', path, 'Main Arma 3 directory')
        return path

def get_workshop_path(arma_path):
    while True:
        path = get_path_from_csv('workshop')
        if path and validate_workshop_path(path, arma_path):
            return path
        path = input("Enter the Workshop PATH (e.g. ...\\workshop\\content\\107410): ").strip().strip('"')
        if path.lower() == "quit":
            return None
        if validate_workshop_path(path, arma_path):
            set_path_in_csv('workshop', path, 'Steam Workshop mods folder')
            return path

def validate_workshop_path(path, arma_path):
    if not os.path.isdir(path):
        print(f"Directory not found: {path}")
        return False
    arma_drive = os.path.splitdrive(arma_path)[0].upper()
    workshop_drive = os.path.splitdrive(path)[0].upper()
    if arma_drive != workshop_drive:
        print(f"Workshop PATH is on drive {workshop_drive} but Arma 3 is on drive {arma_drive}.")
        print("They must be on the same drive.")
        return False
    contents = os.listdir(path)
    if not contents:
        print("Workshop PATH has been defined but it has no mods.")
        return False
        CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paths.csv")

        def get_arma_path():
            path = get_path_from_csv('arma')
            while not path or not os.path.isdir(path):
                path = input("Enter the PATH to your Arma 3 folder: ").strip().strip('"')
                if not os.path.isdir(path):
                    print(f"Directory not found: {path}")
                    continue
                set_path_in_csv('arma', path, 'Main Arma 3 directory')
            return path
            return path
        def get_workshop_path(arma_path):
            while True:
                path = get_path_from_csv('workshop')
                if path and validate_workshop_path(path, arma_path):
                    return path
                path = input("Enter the Workshop PATH (e.g. ...\\workshop\\content\\107410): ").strip().strip('"')
                if path.lower() == "quit":
                    return None
                if validate_workshop_path(path, arma_path):
                    set_path_in_csv('workshop', path, 'Steam Workshop mods folder')
                    return path


def resolve_mod_ids(mod_names, mod_paths, workshop_path):
    mod_ids = {}

    if workshop_path and os.path.isdir(workshop_path):
        ws_map = {}
        for folder_id in os.listdir(workshop_path):
            folder_full = os.path.join(workshop_path, folder_id)
            if os.path.isdir(folder_full):
                meta = os.path.join(folder_full, "meta.cpp")
                if os.path.isfile(meta):
                    try:
                        with open(meta, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
                        if name_match:
                            ws_map[name_match.group(1).lower()] = folder_id
                    except Exception:
                        pass

        for name in mod_names:
            clean = name.lstrip("@")
            if clean.lower() in ws_map:
                mod_ids[name] = ws_map[clean.lower()]

    for i, mod_path in enumerate(mod_paths):
        name = mod_names[i] if i < len(mod_names) else None
        if name and name in mod_ids:
            continue
        if os.path.isdir(mod_path):
            try:
                real = os.path.realpath(mod_path)
                folder_id = os.path.basename(real)
                if folder_id.isdigit() and name:
                    mod_ids[name] = folder_id
            except Exception:
                pass

    return mod_ids


def check_executables(arma_path):
    found = []
    missing = []
    for exe in EXECUTABLES:
        full = os.path.join(arma_path, exe)
        if os.path.isfile(full):
            found.append(exe)
        else:
            missing.append(exe)

    print("\n--- Executable Check ---")
    for exe in found:
        print(f"  [OK] {exe}")
    for exe in missing:
        print(f"  [MISSING] {exe}")

    if "arma3battleye.exe" not in found:
        print("\narma3battleye.exe not found - cannot read mod list.")
        return False
    return True


def check_running_processes(arma_path=None):
    running = []
    for exe in EXECUTABLES:
        if arma_path:
            expected = os.path.join(arma_path, exe).replace("'", "''")
            cmd = f"Get-CimInstance Win32_Process -Filter \"Name = '{exe}'\" | Where-Object {{ $_.ExecutablePath -eq '{expected}' }} | Select-Object -ExpandProperty ProcessId"
        else:
            cmd = f'(Get-CimInstance Win32_Process -Filter "Name = \'{exe}\'").ProcessId'
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", cmd],
                capture_output=True, text=True, timeout=15
            )
            if result.stdout.strip():
                running.append(exe)
                print(f"  {exe} - running")
            else:
                print(f"  {exe} - not running")
        except Exception:
            print(f"  {exe} - not running")
    return running


def get_commandlines(arma_path=None):
    all_lines = []
    for exe in EXECUTABLES:
        if arma_path:
            expected = os.path.join(arma_path, exe).replace("'", "''")
            cmd = f"Get-CimInstance Win32_Process -Filter \"Name = '{exe}'\" | Where-Object {{ $_.ExecutablePath -eq '{expected}' }} | Select-Object -ExpandProperty CommandLine"
        else:
            cmd = f'(Get-CimInstance Win32_Process -Filter "Name = \'{exe}\'").CommandLine'
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", cmd],
                capture_output=True, text=True, timeout=15
            )
            output = result.stdout.strip()
            if output:
                for line in output.splitlines():
                    all_lines.append((exe, line))
        except Exception as e:
            print(f"  Error querying {exe}: {e}")
    return all_lines


def extract_mods(commandline):
    match = re.search(r'-mod=([^"]*)', commandline)
    if not match:
        match = re.search(r'-mod=(\S+)', commandline)
    if not match:
        return [], []

    mod_string = match.group(1)
    parts = [p.strip() for p in mod_string.split(";") if p.strip()]

    mod_names = []
    mod_paths = []
    for part in parts:
        mod_paths.append(part)
        at_match = re.search(r'(@[^;]+)$', part.split("\\")[-1].split("/")[-1])
        if at_match:
            mod_names.append(at_match.group(1))
        elif "@" in part:
            idx = part.rfind("@")
            mod_names.append(part[idx:])
        else:
            mod_names.append(part)

    return mod_names, mod_paths


def main():
    print("=== Arma 3 Mod Reader ===\n")


    arma_path = get_arma_path()
    print(f"\nChecking for running Arma 3 processes...")
    running = check_running_processes(arma_path)
    if not running:
        print(f"\n{', '.join(EXECUTABLES)} are not running.")
        print(f"Arma PATH: {arma_path}")
        print("Please run Arma 3 with mods first.")
        wait_and_exit()
    if not check_executables(arma_path):
        wait_and_exit()

    print(f"\nVerifying processes are running from defined PATH...")
    running_from_path = check_running_processes(arma_path)
    if not running_from_path:
        print(f"\nExecutables are running but NOT from your defined PATH:")
        print(f"  {arma_path}")
        print("The running Arma 3 instance may be from a different install.")
        wait_and_exit()

    workshop_path = get_workshop_path(arma_path)
    print("\nReading command lines from running executables...")
    cmd_lines = get_commandlines(arma_path)

    if not cmd_lines:
        print("\nExecutables are running but could not read their command lines.")
        wait_and_exit()

    all_mods = []
    all_paths = []
    for exe, line in cmd_lines:
        if "-mod=" in line:
            mods, paths = extract_mods(line)
            all_mods.extend(mods)
            all_paths.extend(paths)

    if not all_mods:
        print("\nExecutables are running but no mods are loaded.")
        print("You need to launch Arma 3 with mods enabled for this tool to work.")
        wait_and_exit()

    seen = set()
    unique_mods = []
    unique_paths = []
    for m, p in zip(all_mods, all_paths):
        if m not in seen:
            seen.add(m)
            unique_mods.append(m)
            unique_paths.append(p)

    workshop_path = get_workshop_path(arma_path)
    mod_ids = resolve_mod_ids(unique_mods, unique_paths, workshop_path)

    resolved_count = len(mod_ids)
    print(f"\nResolved {resolved_count}/{len(unique_mods)} mod IDs.")

    print(f"\nTotal amount of found / loaded mods: {len(unique_mods)}")
    print("\nDo you wish to see the list and/or save them to a file?")
    print("  1 - See List")
    print("  2 - Save to File")
    print("  3 - See the list and save to a file")
    print("  Q - Quit")

    while True:
        choice = input("\nChoice: ").strip().lower()
        if choice == "q":
            wait_and_exit()
        elif choice in ("1", "2", "3"):
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or Q.")

    if choice in ("1", "3"):
        print(f"\n--- Active Mods ({len(unique_mods)}) ---")
        for mod in unique_mods:
            mod_id = mod_ids.get(mod)
            if mod_id:
                print(f"  {mod} [ ID: {mod_id} ]")
            else:
                print(f"  {mod} [ ID: unknown ]")

    if choice in ("2", "3"):
        today = datetime.now()
        date_prefix = today.strftime("%d_%m_%Y")
        script_dir = os.path.dirname(os.path.abspath(__file__))

        name_filename = f"{date_prefix}_modsWithName.txt"
        name_file = os.path.join(script_dir, name_filename)
        inc = 1
        while os.path.exists(name_file):
            inc += 1
            name_filename = f"{date_prefix}_modsWithName_{inc}.txt"
            name_file = os.path.join(script_dir, name_filename)

        mod_line = '"-mod=' + ";".join(unique_mods) + '"'
        with open(name_file, "w", encoding="utf-8") as f:
            f.write(mod_line)
        print(f"\nMods (names) saved to: {name_file}")

        id_filename = f"{date_prefix}_modsWithID.txt"
        id_file = os.path.join(script_dir, id_filename)
        inc = 1
        while os.path.exists(id_file):
            inc += 1
            id_filename = f"{date_prefix}_modsWithID_{inc}.txt"
            id_file = os.path.join(script_dir, id_filename)

        id_entries = []
        for mod in unique_mods:
            mod_id = mod_ids.get(mod, "unknown")
            id_entries.append(mod_id)
        id_line = '"-mod=' + ";".join(id_entries) + '"'
        with open(id_file, "w", encoding="utf-8") as f:
            f.write(id_line)
        print(f"Mods (IDs) saved to: {id_file}")

    wait_and_exit()


if __name__ == "__main__":
    main()
