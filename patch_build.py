import os

with open("build_datasets.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace any occurrence of OUT_DIR definition with the correct data/ path
target_old = "OUT_DIR = os.path.dirname(os.path.abspath(__file__))"
target_new = "OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')\nos.makedirs(OUT_DIR, exist_ok=True)"

if target_old in code:
    code = code.replace(target_old, target_new)
    with open("build_datasets.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully patched OUT_DIR in build_datasets.py to point to data/")
else:
    print("OUT_DIR already updated or customized.")
