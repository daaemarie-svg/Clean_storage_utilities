import hashlib, os, time, shutil
from pathlib import Path

#THE COMPASS: This finds 'April Book' OR 'daniellec' automatically.
home = Path.home()

#The GROVES: Using the compass to find the folders.
MIN_SIZE_MB = 500
SEARCH_PATHS = [
    home / "pCloud Drive",
    home / "Library/Mobile Documents/com~apple~CloudDocs",
    home / "Downloads"

]

dna_vault, clog_list = {}, []
trash_bin = Path.home() / "Hawk_Trash"
trash_bin.mkdir(exist_ok=True)

def storage_inspection():
    print(f"--- Cloud Scout: Multi-Cloud Edition ---")
    start_time = time.time()

    for path_str in SEARCH_PATHS:
        root_path = Path(path_str)
        if not root_path.exists(): continue

        print(f" Scouting Grove: {root_path}")
        #Force a manual look at the directory to wake up pCloud Drive
        os.listdir(root_path)

        for p in root_path.rglob("*"):
            if p.is_file():
                try:
                    size_mb = p.stat().st_size / (1024**2)
                    if size_mb > MIN_SIZE_MB:
                        with open(p, "rb") as f:
                            dna = hashlib.md5(f.read(1024*1024)).hexdigest()

                            if dna in dna_vault: #since if/else is tucked inside the 'with' block, the dna is only checked when the gate is open.
                                clog_list.append({"name": p.name, "path": p, "size": size_mb})
                            else:
                                dna_vault[dna] = p
                
                except: continue

    print(f"\n Scan Finished in {time.time() - start_time:.1f}s.")

    if not clog_list:
        print("No duplicates found! The forest is clean.")
        return
    print(f"\n FOUND {len(clog_list)} DUPLICATES:")
    for i, item in enumerate(clog_list):
        print(f"[{i}] {item['name']} ({item['size']:.2f}MB)\n  Path: {item['path']}")

    choice = input("\nType a number to move Hawk_Trash, 'all', or 'skip':").lower()
    
    if choice == 'all' or choice.isdigit():
        to_trash = clog_list if choice == 'all' else [clog_list[int(choice)]]
        for item in to_trash:
            shutil.move(str(item['path']), str(trash_bin / item['name']))
            print(f"Moved to Hawk_Trash: {item['name']}")
    else:
        print("Scout returning to base. No changes made.")

storage_inspection()
        

