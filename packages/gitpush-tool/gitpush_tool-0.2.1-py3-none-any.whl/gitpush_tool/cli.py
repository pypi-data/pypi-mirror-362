#!/usr/bin/env python3
import os
import argparse
import sys
import subprocess
from datetime import datetime
import requests

def check_gh_installed():
    """Check if GitHub CLI is installed"""
    try:
        subprocess.run(["gh", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False

def gh_authenticated():
    """Check if user is authenticated with GitHub CLI"""
    try:
        result = subprocess.run(["gh", "auth", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except:
        return False

def authenticate_with_gh():
    """Authenticate user with GitHub CLI"""
    print("\n🔑 GitHub authentication required")
    print("We'll use the GitHub CLI (gh) for authentication")
    print("This will open your browser for secure login")
    
    try:
        subprocess.run(["gh", "auth", "login", "--web", "-h", "github.com"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Authentication failed")
        return False
    except FileNotFoundError:
        print("❌ GitHub CLI not found")
        return False

def create_with_gh_cli(repo_name, private=False, description="", commit_message="Initial commit"):
    """Create and push to new repository using GitHub CLI"""
    try:
        private_flag = "--private" if private else "--public"
        cmd = [
            "gh", "repo", "create", repo_name,
            private_flag,
            "--source=.",
            "--remote=origin",
            "--push"
        ]
        
        if description:
            cmd.extend(["--description", description])
        
        # Run the command
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            # Get the repo URL
            url_result = subprocess.run(
                ["gh", "repo", "view", "--json", "url", "--jq", ".url"],
                stdout=subprocess.PIPE,
                text=True,
                check=True
            )
            repo_url = url_result.stdout.strip()
            print(f"✅ Successfully created repository: {repo_url}")
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create repository: {e.stderr}")
        return False

def initialize_repository(remote_url=None):
    """Initialize git repository with sensible defaults"""
    if not os.path.exists(".git"):
        print("🛠 Initializing git repository")
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        
        if remote_url:
            subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
        
        # Create basic .gitignore if doesn't exist
        if not os.path.exists(".gitignore"):
            with open(".gitignore", "w") as f:
                f.write("""# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# System
.DS_Store
Thumbs.db

# Project specific
*.log
*.tmp
*.bak
""")
        print("📁 Created .gitignore file")

def check_for_updates():
    """Check for newer versions on PyPI"""
    try:
        current_version = "0.2.1"  # Should match your setup.py
        response = requests.get("https://pypi.org/pypi/gitpush-tool/json", timeout=2)
        latest_version = response.json()["info"]["version"]
        if latest_version != current_version:
            print(f"ℹ️  New version available: {latest_version} (you have {current_version})")
            print("   Run 'pip install --upgrade gitpush-tool' to update")
    except:
        pass

def run():
    parser = argparse.ArgumentParser(
        description="🚀 Supercharged Git push tool with GitHub repo creation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  Basic push:            gitpush_tool "Commit message"
  Create new repo:       gitpush_tool "Initial commit" --new-repo project-name
  Private repository:    gitpush_tool --new-repo private-project --private
  Force push:            gitpush_tool "Fix critical bug" --force
  Push specific branch:  gitpush_tool "Update feature" feature-branch upstream
"""
    )
    parser.add_argument("commit", nargs="?", help="Commit message")
    parser.add_argument("branch", nargs="?", default="main", help="Branch name (default: main)")
    parser.add_argument("remote", nargs="?", default="origin", help="Remote name (default: origin)")
    parser.add_argument("--force", action="store_true", help="Force push with --force-with-lease")
    parser.add_argument("--tags", action="store_true", help="Push tags")
    parser.add_argument("--init", action="store_true", help="Initialize git repo")
    parser.add_argument("--new-repo", metavar="NAME", help="Create new GitHub repository")
    parser.add_argument("--private", action="store_true", help="Make repository private")
    parser.add_argument("--description", help="Repository description")

    args = parser.parse_args()

    if args.new_repo:
        print(f"🆕 Creating repository: {args.new_repo}")
        
        # Check if GitHub CLI is installed
        if not check_gh_installed():
            print("❌ GitHub CLI (gh) is not installed")
            print("Please install it first:")
            print("  Mac (Homebrew): brew install gh")
            print("  Windows (Winget): winget install --id GitHub.cli")
            print("  Linux: See https://github.com/cli/cli#installation")
            sys.exit(1)
        
        # Check if authenticated
        if not gh_authenticated():
            if not authenticate_with_gh():
                sys.exit(1)
        
        # Create repository
        if not create_with_gh_cli(
            args.new_repo,
            private=args.private,
            description=args.description or "",
            commit_message=args.commit or "Initial commit"
        ):
            sys.exit(1)

    if args.init:
        initialize_repository()

    # Stage all changes
    subprocess.run(["git", "add", "."], check=True)

    if args.commit:
        print(f"📦 Committing: '{args.commit}'")
        try:
            subprocess.run(['git', 'commit', '-m', args.commit], check=True)
        except subprocess.CalledProcessError:
            print("❌ Commit failed")
            sys.exit(1)
    else:
        print("⚠️  Skipping commit (no message provided)")

    # Build push command
    push_cmd = ["git", "push"]
    if args.force:
        push_cmd.append("--force-with-lease")
    if args.tags:
        push_cmd.append("--tags")
    if args.remote and args.branch:
        push_cmd.extend([args.remote, args.branch])

    print(f"🚀 Executing: {' '.join(push_cmd)}")
    try:
        subprocess.run(push_cmd, check=True)
        print("✅ Successfully pushed changes")
    except subprocess.CalledProcessError:
        print("❌ Push failed")
        sys.exit(1)

if __name__ == "__main__":
    check_for_updates()
    run()