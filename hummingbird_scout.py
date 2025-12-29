import hashlib, os, time, shutil
from pathlib import Path

# --- CONFIGURATION ---
MIN_SIZE_MB = 10

#THE COMPASS: This finds 'April Book' OR 'daniellec' automatically.
home = Path.home()

SEARCH_PATHS = [
    home / "pCloud Drive",
    home / "Library/Mobile Documents/com~apple~CloudDocs",
    home / "Downloads"
]

dna_vault, clog_list = {}, []
trash_bin = Path.home() / "Hummingbird_Trash"
trash_bin.mkdir(exist_ok=True)

def storage_inspection():
    # THE WARNING: Visual signpost for the Architect
    print("\n--- ⚠️  ARCHITECT'S RULE: DO NOT MOVE FILES DURING FLIGHT! ---\n")
    print(f"--- Cloud Scout: Hummingbird Detailed Edition (>{MIN_SIZE_MB}MB) ---")
    start_time = time.time()

    for path_str in SEARCH_PATHS:
        root_path = Path(path_str)
        if not root_path.exists(): continue

        print(f" Scouting Grove: {root_path}")
        try:
            os.listdir(root_path) # Wake up pCloud
            for p in root_path.rglob("*"):
                if p.is_file() and not p.name.startswith('.'):
                    try:
                        size_mb = p.stat().st_size / (1024**2)
                        if size_mb > MIN_SIZE_MB:
                            with open(p, "rb") as f:
                                dna = hashlib.md5(f.read(64*1024)).hexdigest()
                                if dna in dna_vault:
                                    clog_list.append({"name": p.name, "path": p, "size": size_mb})
                                else:
                                    dna_vault[dna] = p
                    except: continue
        except: continue

    print(f"\n Scan Finished in {time.time() - start_time:.1f}s.")

    if not clog_list:
        print("No duplicates found! The forest is clean.")
        return

    print(f"\n FOUND {len(clog_list)} DUPLICATES:")
    for i, item in enumerate(clog_list):
        print(f"[{i}] {item['name']} ({item['size']:.2f}MB)")

    choice = input("\nType 'all', a number, or 'skip': ").lower()
    
    if choice == 'all' or choice.isdigit():
        to_trash = clog_list if choice == 'all' else [clog_list[int(choice)]]
        
        # THE ACCOUNTANT: Tracking the harvest
        total_reclaimed = 0
        for item in to_trash:
            try:
                shutil.move(str(item['path']), str(trash_bin / item['name']))
                total_reclaimed += item['size']
                print(f"Moved: {item['name']}")
            except FileNotFoundError:
                # THE SHIELD: If the flower vanished, stay calm
                print(f"💨 {item['name']} vanished! Skipping.")
        
        print(f"\n✅ SUCCESS: You moved {total_reclaimed:.2f} MB to the Trash!")
    else:
        print("Scout returning to base. No changes made.")

# --- THE FLIGHT ---
storage_inspection()

# THE LANDING SONG: Only plays if the computer stayed awake!
print("\n✨ ALL FLIGHTS COMPLETE. The Scout is back in its nest! ✨\n")      

