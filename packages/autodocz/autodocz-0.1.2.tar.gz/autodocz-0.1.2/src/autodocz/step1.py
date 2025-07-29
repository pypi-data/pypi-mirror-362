import os

def print_tree(start_path, prefix=""):
    files = []
    folders = []

    # Separate files and folders for better display order
    for item in os.listdir(start_path):
        full_path = os.path.join(start_path, item)
        if os.path.isdir(full_path):
            folders.append(item)
        else:
            files.append(item)

    for folder in sorted(folders):
        folder_path = os.path.join(start_path, folder)
        print(f"{prefix}├── {folder}/")
        print_tree(folder_path, prefix + "│   ")

    for i, file in enumerate(sorted(files)):
        connector = "└──" if i == len(files) - 1 else "├──"
        print(f"{prefix}{connector} {file}")


if __name__ == "__main__":
    root_dir = "."  
    print(f"{root_dir}/")
    print_tree(root_dir)
