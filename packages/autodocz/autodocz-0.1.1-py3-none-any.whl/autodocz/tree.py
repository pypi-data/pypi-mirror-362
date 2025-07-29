# src/docgen/tree.py
import os

def print_tree(start_path: str = ".", prefix: str = "") -> None:
    files, folders = [], []
    for item in sorted(os.listdir(start_path)):
        full = os.path.join(start_path, item)
        (folders if os.path.isdir(full) else files).append(item)

    for folder in folders:
        print(f"{prefix}├── {folder}/")
        print_tree(os.path.join(start_path, folder), prefix + "│   ")

    for idx, file in enumerate(files):
        connector = "└──" if idx == len(files) - 1 else "├──"
        print(f"{prefix}{connector} {file}")
