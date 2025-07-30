import os
from typing import List

def get_tree_lines(start_path: str = ".", prefix: str = "") -> List[str]:
    lines: List[str] = []
    # separate folders and files
    files, folders = [], []
    for item in sorted(os.listdir(start_path)):
        full = os.path.join(start_path, item)
        (folders if os.path.isdir(full) else files).append(item)

    # process folders first
    for idx, folder in enumerate(folders):
        # determine connector (last-folder handling is optional here)
        connector = "└──" if idx == len(folders) - 1 and not files else "├──"
        lines.append(f"{prefix}{connector} {folder}/")
        # recurse into subfolder, extending prefix
        extension = "    " if idx == len(folders) - 1 and not files else "│   "
        lines.extend(get_tree_lines(os.path.join(start_path, folder), prefix + extension))

    # then process files
    for idx, file in enumerate(files):
        connector = "└──" if idx == len(files) - 1 else "├──"
        lines.append(f"{prefix}{connector} {file}")

    return lines

def get_tree(start_path: str = ".") -> str:
    """Return the entire tree as one string (no printing)."""
    return "\n".join(get_tree_lines(start_path))
