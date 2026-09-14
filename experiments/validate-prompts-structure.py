"""
Generates a text-based folder & file structure.
Usage:
    python dir_tree.py [path_to_root] [--depth N] [--exclude DIR1 DIR2 ...]
Example:
    python dir_tree.py ./my_project --depth 4
"""

import argparse
import os
import sys


def generate_tree(start_path, prefix="", depth=0, max_depth=None, exclude=None):
    if max_depth is not None and depth > max_depth:
        return []

    results = []
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        results.append(f"{prefix}⛔ [Permission Denied]")
        return results
    except Exception as e:
        results.append(f"{prefix}❌ [Error: {e}]")
        return results

    # Filter excluded items
    if exclude:
        entries = [e for e in entries if e not in exclude]

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "├── " if not is_last else "└── "
        results.append(f"{prefix}{connector}{entry}")

        full_path = os.path.join(start_path, entry)
        child_prefix = f"{prefix}{'│   ' if not is_last else '    '}"

        if os.path.isdir(full_path):
            results.extend(
                generate_tree(full_path, child_prefix, depth + 1, max_depth, exclude)
            )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate a text-based directory tree.",
        epilog="Example: python dir_tree.py ./src --depth 3",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to start from (default:current)",
    )
    parser.add_argument("--depth", type=int, default=None, help="Max traversal depth")
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[".git", "node_modules", "__pycache__", ".venv", ".env", ".tox"],
        help="Folders/files to skip (space-separated)",
    )

    args = parser.parse_args()
    root_path = os.path.abspath(args.path)

    if not os.path.exists(root_path):
        print(f"❌ Error: Path '{root_path}' does not exist.")
        sys.exit(1)

    print(os.path.basename(root_path) + "/")
    for line in generate_tree(
        root_path, depth=0, max_depth=args.depth, exclude=args.exclude
    ):
        print(line)


if __name__ == "__main__":
    main()
