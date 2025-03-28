#!/usr/bin/env python3

# (c) Manuel Alejandro Gómez Nicasio <az-dev@outlook.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

# With help from ChatGPT

import os
import subprocess


REPO_LIST = "repos.txt"
BASE_DIR = os.path.expanduser("~/workspace/github.com/codingcompetitions/")


def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as exception:
        return f"Error: {exception}"


def clone_or_update(repo_url, repo_dir):
    full_repo_path = os.path.join(BASE_DIR, repo_dir)

    if os.path.exists(full_repo_path) and os.path.isdir(os.path.join(full_repo_path, ".git")):
        print(f"Updating repository in {full_repo_path}...")
        run_command("git pull", cwd=full_repo_path)
    else:
        print(f"Cloning {repo_url} into {full_repo_path}...")
        os.makedirs(full_repo_path, exist_ok=True)
        run_command(f"git clone {repo_url} {full_repo_path}")


def push_changes(repo_dir):
    full_repo_path = os.path.join(BASE_DIR, repo_dir)

    current_branch = run_command("git rev-parse --abbrev-ref HEAD", cwd=full_repo_path)

    if not current_branch:
        print(f"Error: Could not determine the current branch in {full_repo_path}")
        return

    ahead_status = run_command(f"git rev-list --count origin/{current_branch}..HEAD", cwd=full_repo_path)

    if ahead_status.isdigit() and int(ahead_status) > 0:
        print(f"Pushing committed changes from {full_repo_path} (branch: {current_branch})...")
        run_command(f"git push origin {current_branch}", cwd=full_repo_path)
    else:
        print(f"No committed changes to push in {full_repo_path} (branch: {current_branch}).")


def check_status(repo_dir):
    full_repo_path = os.path.join(BASE_DIR, repo_dir)

    print(f"Status of {full_repo_path}:")
    status_output = run_command("git status -s", cwd=full_repo_path)
    if status_output:
        print(status_output)
    else:
        print("No changes.")


def main():
    if not os.path.exists(REPO_LIST):
        print(f"Error: {REPO_LIST} not found!")
        return

    with open(REPO_LIST, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue  # Skip empty lines and comments

            parts = line.split(None, 1)  # Split into URL and directory
            if len(parts) < 2:
                print(f"Invalid line: {line}")
                continue

            repo_url, repo_dir = parts
            clone_or_update(repo_url, repo_dir)
            check_status(repo_dir)
            push_changes(repo_dir)
            print("\n")

    print(f"All repositories processed in {BASE_DIR}.")


if __name__ == "__main__":
    main()
