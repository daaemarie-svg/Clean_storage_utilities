import os, time
path = os.path.expanduser("~/Downloads")

def survey_forest():
    for file in os.listdir(path):
        f_path = os.path.join(path, file)
        if os.path.isfile(f_path):
            is_heavy = os.path.getsize(f_path) > 100 * 1024 * 1024
            is_old = os.stat(f_path).st_mtime < (time.time() - (30 * 86400))
            if is_heavy or is_old:
                print(f"Cluttered spot: {file}")

survey_forest()