import os
import argparse
import sys

def run():
    parser = argparse.ArgumentParser(
        description="📦 Simple CLI to automate git init, add, commit, and push operations."
    )
    parser.add_argument("commit", nargs="?", help="Commit message. If omitted, no commit will be made.")
    parser.add_argument("branch", nargs="?", help="Branch to push to (e.g., main, feature/xyz).")
    parser.add_argument("remote", nargs="?", help="Remote name (default: origin).")
    parser.add_argument("--force", action="store_true", help="Force push (use with caution).")
    parser.add_argument("--tags", action="store_true", help="Push all local tags.")
    parser.add_argument("--init", action="store_true", help="Run 'git init' before pushing.")

    args = parser.parse_args()

    if args.init:
        print("🛠 Initializing git repository...")
        os.system("git init")

    os.system("git add .")

    if args.commit:
        print(f"📦 Committing with message: '{args.commit}'")
        os.system(f'git commit -m "{args.commit}"')
    else:
        print("⚠️  No commit message provided. Skipping commit step.")

    push_cmd = "git push"

    if args.force:
        push_cmd += " --force-with-lease"

    if args.tags:
        push_cmd += " --tags"

    if args.remote and args.branch:
        push_cmd += f" {args.remote} {args.branch}"
    elif args.branch:
        push_cmd += f" origin {args.branch}"

    print(f"🚀 Running: {push_cmd}")
    os.system(push_cmd)
