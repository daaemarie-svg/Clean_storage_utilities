import os, hashlib
from pathlib import Path

# --- The Personality / Atmosphere ---
OUTCOME_LABEL = "COMPOST" # Setting the outcome label to Compost

# THE COMPASS
home = Path.home()

#The path to the "cluttered" area
path = home / "Downloads"
files_seen = {}

def find_duplicates():
    for file in os.listdir(path):
        f_path = os.path.join(path,file)
        if os.path.isfile(f_path) and not file.startswith('.'):
            #1.Open the file and read its binary 'DNA'
            with open(f_path, 'rb') as f:
                fingerprint = hashlib.md5(f.read()).hexdigest() #Creating a unique fingerprint for the file
                #2. Check if we've seen this 'DNA' before
                if fingerprint in files_seen:
                    print(f"Duplicate found: {file}")
                    #3. Ask for permission to delete
                    choice = input(f"Delete {file}? (y/n): ")
                    #4. Using the personality here                           
                    if choice.lower() == 'y':
                        os.remove(f_path)
                        print(f"The digital material has vanished. {file} is {OUTCOME_LABEL}.")
                else:
                    files_seen[fingerprint] = file

find_duplicates ()