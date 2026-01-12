#!/usr/bin/env python3

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_URL = "https://gitlab.com/gabmus/envision.git"
BIN_NAME = "envision"
INSTALL_PATH = Path("/usr/local/bin") / BIN_NAME


def run(cmd, cwd=None):
    print(f"+ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)


def list_tags():
    run(["git", "ls-remote", "--tags", REPO_URL])


def install(tag=None, branch=None):
    with tempfile.TemporaryDirectory() as tmp:
        repo_dir = Path(tmp) / "envision"

        run(["git", "clone", REPO_URL, str(repo_dir)])

        if tag:
            run(["git", "checkout", f"tags/{tag}"], cwd=repo_dir)
        elif branch:
            run(["git", "checkout", branch], cwd=repo_dir)

        src = repo_dir / BIN_NAME

        if not src.exists():
            sys.exit(f"Error: {BIN_NAME} not found in repository root")

        run(["install", "-m", "0755", str(src), str(INSTALL_PATH)])

        print(f"\nInstalled {BIN_NAME} to {INSTALL_PATH}")


def main():
    parser = argparse.ArgumentParser(
        description="Install Envision into /usr/local/bin"
    )

    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="List available git tags and exit",
    )

    parser.add_argument(
        "--tag",
        help="Install a specific git tag",
    )

    parser.add_argument(
        "--branch",
        help="Install a specific branch (default: repo default)",
    )

    args = parser.parse_args()

    if args.list_tags:
        list_tags()
        return

    install(tag=args.tag, branch=args.branch)


if __name__ == "__main__":
    main()
