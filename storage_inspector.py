#Cloud Priority inspector Script
import os, hashlib

MIN_SIZE_MB = 500
#Swap the order: pCloud is now the 'Reference" forest
SEARCH_PATHS = [
    "/Users/AprilBook/pCloud Drive",
    os.path.expanduser("~/Downloads")
]
dna_vault = {}

def storage_inspection():
    print(f"--- Storage Inspector: Cloud-Priority Mode ---")
    for drive in SEARCH_PATHS:
        if not os.path.exists(drive): continue

        for root, dirs, files, in os.walk(drive):
            for name in files:
                f_path = os.path.join(root, name)
                try:
                    size_mb = os.path.getsize(f_path) / (1024**2)
                    if size_mb > MIN_SIZE_MB:
                        #Partial DNA check (1MB)
                        with open(f_path, "rb") as f:
                            dna = hashlib.md5(f.read(1024*1024)).hexdigest()

                        if dna in dna_vault:
                            print(f"\n DUPLICATE FOUND IN DOWNLOADS: {name}")
                            print(f" [KEEPING IN CLOUD]: {dna_vault[dna]}")
                            print(f" [TRASHING LOCAL]: {f_path}")

                            choice = input("Delete local download copy? (y/n): ")
                            if choice.lower() == 'y':
                                os.remove(f_path)
                                print("Local space reclaimed.")
                        else:
                            #This stores the path of the first version found (pCloud)
                            dna_vault[dna] = f_path

                except: continue
        print("\n--- Inspection Complete ---\n")

storage_inspection()
