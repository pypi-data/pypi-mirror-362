import os
import ast
from typing import Dict, List, Any, Optional

try:
    import toml
except ImportError:
    toml = None

EXCLUDE_DIRS = {"venv", "__pycache__", "tests", ".git"}


def load_pyproject_info(start_path: str) -> Dict[str, Any]:
    toml_path = os.path.join(start_path, "pyproject.toml")
    if toml and os.path.isfile(toml_path):
        data = toml.load(toml_path).get("tool", {}).get("poetry", {}) \
            or toml.load(toml_path).get("project", {})
        return {
            "name": data.get("name"),
            "version": data.get("version"),
            "description": data.get("description"),
            "authors": data.get("authors", []),
            "dependencies": list(data.get("dependencies", {}).keys())
        }
    return {}


def find_python_files(start_path: str) -> List[str]:
    py_files = []
    for root, dirs, files in os.walk(start_path):
        # skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))
    return py_files


def parse_file_info(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source, filename=path)
    module_doc = ast.get_docstring(tree)
    classes, functions = [], []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "doc": ast.get_docstring(node)
            })
        elif isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "doc": ast.get_docstring(node),
                "args": [arg.arg for arg in node.args.args]
            })
    return {
        "path": path,
        "module_doc": module_doc,
        "classes": classes,
        "functions": functions
    }


def get_project_info(start_path: str = ".") -> Dict[str, Any]:
    """
    Walks the project at start_path and returns:
      - metadata from pyproject.toml (if present)
      - a list of parsed Python modules with docstrings, classes, and functions
    """
    info: Dict[str, Any] = {}
    # 1. Project metadata
    info["metadata"] = load_pyproject_info(start_path)

    # 2. Code structure
    py_files = find_python_files(start_path)
    modules_info = []
    for path in py_files:
        # skip __init__.py if you want, or include it
        modules_info.append(parse_file_info(path))
    info["modules"] = modules_info

    return info

