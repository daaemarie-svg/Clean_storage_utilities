import os, hashlib, time

MIN_SIZE_MB = 500 
SEARCH_PATHS = ["/Users/AprilBook/pCloud Drive", os.path.expanduser("~/Downloads")]
dna_vault, clog_list = {}, []

def storage_inspection():
    start_time = time.time()
    files_scanned = 0
    print(f"--- 🕵️ Strategic Inspector: Deep Scan Mode ---")
    
    for drive in SEARCH_PATHS:
        print(f"🌲 Entering: {drive}")
        # Manual recursion to bypass pCloud's virtual 'gate'
        for root, dirs, files in os.walk(drive, topdown=True, followlinks=True):
            for name in files:
                files_scanned += 1
                if files_scanned % 500 == 0:
                    print(f"🔍 Surveyed {files_scanned} files...")
                
                f_path = os.path.join(root, name)
                try:
                    # Filter for large files before hashing to save time
                    size_mb = os.path.getsize(f_path) / (1024**2)
                    if size_mb > MIN_SIZE_MB:
                        with open(f_path, "rb") as f:
                            dna = hashlib.md5(f.read(1024*1024)).hexdigest()
                        if dna in dna_vault:
                            clog_list.append({"name": name, "trash": f_path, "size": size_mb})
                        else:
                            dna_vault[dna] = f_path
                except: continue

    duration = time.time() - start_time
    print(f"\n✅ Scan Finished in {duration:.1f} seconds. Total: {files_scanned}")
    if not clog_list:
        print("No duplicates found. The forest is clean.")
        return

    for i, clog in enumerate(clog_list):
        print(f"[{i}] {clog['name']} ({clog['size']:.2f}MB)\n    Path: {clog['trash']}")
    print("\n--- STANDBY FOR ACTION ---")

storage_inspection()