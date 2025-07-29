import os
import shutil
import sys
from pathlib import Path

TEMPLATE_FILES = [
    ("src/kamalfirstpackage/core.py", "core.py"),
    ("src/kamalfirstpackage/core2.py", "core2.py"),
    ("main.py", "main.py"),
    ("main2.py", "main2.py"),
    ("main3.py", "main3.py"),
    ("pyproject.toml", "pyproject.toml"),
]

def start():
    cwd = Path.cwd()
    package_dir = Path(__file__).parent.parent
    for src_rel, dest_name in TEMPLATE_FILES:
        src = package_dir / src_rel
        dest = cwd / dest_name
        if dest.exists():
            print(f"File {dest} already exists, skipping.")
            continue
        shutil.copy2(src, dest)
        print(f"Copied {src_rel} to {dest}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        start()
    else:
        print("Usage: pypi_test start")

if __name__ == "__main__":
    main()
