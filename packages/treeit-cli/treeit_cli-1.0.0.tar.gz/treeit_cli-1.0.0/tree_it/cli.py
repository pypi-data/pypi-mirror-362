#!/usr/bin/env python3

import argparse
from pathlib import Path
import fnmatch

ANSI_FG_RED = "\033[31m"
ANSI_RESET = "\033[0m"

def write_structure_to_txt(root_path: str, output_file: str, max_depth: int | str, ignore_patterns: list[str]):
    root = Path(root_path).resolve()
    lines = []

    # Classify patterns
    ignored_files = set()
    ignored_dirs = set()
    ignored_dir_content = set()
    ignored_globs = []

    for pattern in ignore_patterns:
        p = Path(pattern)
        if "*" in pattern:
            if p.name == "*":
                # folder/* => ignore content but not the folder
                ignored_dir_content.add(str(p.parent))
            else:
                ignored_globs.append(pattern)
        elif pattern.endswith("/"):
            # folder/ => ignore folder completely
            ignored_dirs.add(pattern.rstrip("/"))
        else:
            # exact file
            ignored_files.add(pattern)

    def should_ignore_file(p: Path) -> bool:
        rel = p.relative_to(root)
        return (
            str(rel) in ignored_files or
            any(fnmatch.fnmatch(str(rel), pat) for pat in ignored_globs)
        )

    def should_ignore_dir(p: Path) -> str | None:
        rel = str(p.relative_to(root))
        if rel in ignored_dirs:
            return "full"
        elif rel in ignored_dir_content:
            return "content"
        return None

    def recurse(path: Path, prefix: str = "", depth: int = 0):
        if max_depth != "full" and depth > max_depth:
            return

        try:
            entries = [p for p in path.iterdir() if not p.name.startswith('.')]
        except PermissionError:
            lines.append(f"{prefix}└── [Permission Denied]")
            return

        dirs = sorted([e for e in entries if e.is_dir()], key=lambda p: p.name.lower())
        files = sorted([e for e in entries if not e.is_dir()], key=lambda p: p.name.lower())
        sorted_entries = dirs + files

        for i, entry in enumerate(sorted_entries):
            connector = "└── " if i == len(sorted_entries) - 1 else "├── "
            rel = entry.relative_to(root)

            # Check ignore
            if entry.is_file() and should_ignore_file(entry):
                continue
            if entry.is_dir():
                ignore_type = should_ignore_dir(entry)
                if ignore_type == "full":
                    continue
                elif ignore_type == "content":
                    lines.append(f"{prefix}{connector}{entry.name}/  (content ignored)")
                    continue

            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = "    " if i == len(sorted_entries) - 1 else "│   "
                recurse(entry, prefix + extension, depth + 1)

    lines.append(f"{root.name}/")
    recurse(root, depth=1)
    Path(output_file).write_text("\n".join(lines), encoding="utf-8")
    print(f"Tree saved to {output_file}")

def parse_args():
    parser = argparse.ArgumentParser(description="Export directory tree to a text file.")
    parser.add_argument("path", nargs="?", default=".", help="Root path of the project (default: current directory)")
    parser.add_argument("-o", "--output", default="tree.txt", help="Output file name")
    parser.add_argument("-d", "--depth", default="full", help="Max depth (0, 1, 2, ..., or 'full')")
    parser.add_argument("-i", "--ignore", nargs="*", default=[], help="Ignore patterns (e.g. folder/, folder/*, *.txt, file.md)")

    args = parser.parse_args()

    if args.depth != "full":
        try:
            args.depth = int(args.depth)
        except ValueError:
            parser.error(f"{ANSI_FG_RED}Depth must be an integer or 'full'{ANSI_RESET}")

    return args

def main():
    args = parse_args()
    write_structure_to_txt(args.path, args.output, args.depth, args.ignore)

if __name__ == "__main__":
    main()
