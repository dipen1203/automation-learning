import difflib
from pathlib import Path

script_dir = Path(__file__).parent
file_path = script_dir / "golden_conf.txt"

with open(file_path) as g_data:
    g_config = g_data.read()

with open(script_dir / "new_conf.txt") as n_data:
    n_config = n_data.read()


delta = difflib.Differ().compare(g_config.splitlines(), n_config.splitlines())

print(delta)

for data in delta:
    if data.startswith(("+ ", "- ")): # this lines shows only the lines which are different in both files
        print(data)
