#!/usr/bin/env python3
"""
Recursive Directory Content Viewer

This program recursively displays the contents of a specified directory,
showing subfolders and files along with their names and types.
"""

import sys
import argparse
from pathlib import Path


def get_item_type(path: Path) -> str:
    """Return a human-readable string representing the path type."""
    if path.is_symlink():
        return "Symlink"
    elif path.is_dir():
        return "Directory"
    elif path.is_file():
        return "File"
    elif path.is_fifo():
        return "FIFO"
    elif path.is_socket():
        return "Socket"
    elif path.is_block_device():
        return "Block Device"
    elif path.is_char_device():
        return "Char Device"
    else:
        return "Unknown"


def display_directory(
    root_path: Path,
    prefix: str = "",
    show_hidden: bool = False
) -> None:
    """
    Recursively display directory contents with names and types.

    :param root_path: Path object representing the folder to display.
    :param prefix: Visual indentation prefix for tree structure.
    :param show_hidden: Whether to include hidden files/directories (starting with .).
    """
    try:
        entries = sorted(root_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except PermissionError:
        print(f"{prefix}[Permission Denied]")
        return
    except OSError as e:
        print(f"{prefix}[Error: {e}]")
        return

    if not show_hidden:
        entries = [e for e in entries if not e.name.startswith('.')]

    count = len(entries)
    for index, entry in enumerate(entries):
        is_last = (index == count - 1)
        connector = "└── " if is_last else "├── "
        item_type = get_item_type(entry)

        print(f"{prefix}{connector}{entry.name} [{item_type}]")

        if entry.is_dir() and not entry.is_symlink():
            extension = "    " if is_last else "│   "
            display_directory(entry, prefix=prefix + extension, show_hidden=show_hidden)


def main():
    parser = argparse.ArgumentParser(
        description="Recursively display contents of a folder (subfolders and files with name and type)."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the directory to inspect (default: current directory)"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Include hidden files and folders (starting with .)"
    )

    args = parser.parse_args()
    target_path = Path(args.path)

    if not target_path.exists():
        print(f"Error: Path '{target_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not target_path.is_dir():
        item_type = get_item_type(target_path)
        print(f"'{target_path}' is a {item_type}, not a directory.")
        return

    root_type = get_item_type(target_path)
    print(f"{target_path.resolve().name or target_path} [{root_type}]")
    display_directory(target_path, show_hidden=args.all)


if __name__ == "__main__":
    main()
