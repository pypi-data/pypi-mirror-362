import argparse
from autodocz.generator import make_readme, make_license, make_srs
from autodocz.utils import *

def main():
    parser = argparse.ArgumentParser(
        prog="autodocz",
        description="autodocz: directory tree & doc generator"
    )
    sub = parser.add_subparsers(dest="command", required=True)


    # GENERATE command
    gen = sub.add_parser("generate", help="generate documentation files")
    gen.add_argument("doc", choices=["readme", "license", "srs", "report","all"],
                     help="which document to generate")
    gen.add_argument("-o", "--output", default=None,
                     help="path/filename to write (default: README.md, LICENSE, SRS.md)")

    args = parser.parse_args()

    if args.command == "generate":
        targets = [args.doc] if args.doc != "all" else ["readme","license","srs","report"]
        for doc in targets:
            if doc == "readme":
                content = make_readme(get_project_info())
                out = args.output or "README.md"
            elif doc == "license":
                content = make_license()
                out = args.output or "LICENSE"
            elif doc == "srs":
                content = make_srs()
                out = args.output or "SRS.md"
            with open(out, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Generated {out}")
