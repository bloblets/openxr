#!/usr/bin/env python3

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

# CHANGE THESE IF NEEDED
REPO_URL = "https://gitlab.com/gabmus/envision.git"
PREFIX = "/usr/bin"


def run(cmd, cwd=None):
    print(f"+ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)


def list_tags():
    run(["git", "ls-remote", "--tags", "--refs", REPO_URL])


def install(tag=None, branch=None):
    with tempfile.TemporaryDirectory() as tmp:
        repo_dir = Path(tmp) / "envision"
        build_dir = repo_dir / "build"

        # Clone repo
        run(["git", "clone", REPO_URL, str(repo_dir)])

        # Checkout tag or branch
        if tag:
            run(["git", "checkout", f"tags/{tag}"], cwd=repo_dir)
        elif branch:
            run(["git", "checkout", branch], cwd=repo_dir)

        # Configure with meson
        run([
            "meson",
            "setup",
            str(build_dir),
            f"--prefix={PREFIX}",
            "--buildtype=release",
        ], cwd=repo_dir)

        # Build
        run(["ninja", "-C", str(build_dir)])

        # Install
        run(["ninja", "-C", str(build_dir), "install"])

        print(f"\nEnvision installed to {PREFIX}/bin")


def main():
    parser = argparse.ArgumentParser(
        description="Build and install Envision using Meson/Ninja"
    )

    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="List available git tags and exit",
    )

    parser.add_argument(
        "--tag",
        help="Build and install a specific git tag",
    )

    parser.add_argument(
        "--branch",
        help="Build and install from a specific branch",
    )

    args = parser.parse_args()

    if args.list_tags:
        list_tags()
        return

    install(tag=args.tag, branch=args.branch)


if __name__ == "__main__":
    main()
