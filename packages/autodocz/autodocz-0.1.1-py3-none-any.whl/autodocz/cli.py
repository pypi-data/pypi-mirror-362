# src/docgen/cli.py
import argparse
from autodocz.tree import print_tree

def main():
    parser = argparse.ArgumentParser(
        prog="autodocz",
        description="autodocz: print directory tree"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to print (default: current dir)"
    )
    args = parser.parse_args()
    print(f"{args.path}/")
    print_tree(args.path)
