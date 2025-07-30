import os
import argparse
import sys
import requests
from getpass import getpass

def create_github_repo(repo_name, private=False, description=""):
    """Create a new GitHub repository using the GitHub API"""
    # Get GitHub token from environment or prompt
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        token_path = os.path.join(os.path.dirname(__file__), '..', 'token')
        if os.path.exists(token_path):
            with open(token_path, 'r') as f:
                token = f.read().strip()
        else:
            token = getpass("Enter your GitHub personal access token: ")
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": False
    }
    
    try:
        response = requests.post(
            "https://api.github.com/user/repos",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()["html_url"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create repository: {e}")
        return None

def run():
    parser = argparse.ArgumentParser(
        description="📦 Simple CLI to automate git operations and GitHub repository creation."
    )
    parser.add_argument("commit", nargs="?", help="Commit message. If omitted, no commit will be made.")
    parser.add_argument("branch", nargs="?", default="main", help="Branch to push to (default: main).")
    parser.add_argument("remote", nargs="?", default="origin", help="Remote name (default: origin).")
    parser.add_argument("--force", action="store_true", help="Force push (use with caution).")
    parser.add_argument("--tags", action="store_true", help="Push all local tags.")
    parser.add_argument("--init", action="store_true", help="Run 'git init' before pushing.")
    parser.add_argument("--new-repo", metavar="REPO_NAME", help="Create a new GitHub repository with this name.")
    parser.add_argument("--private", action="store_true", help="Make the new repository private.")
    parser.add_argument("--description", help="Description for the new repository.")

    args = parser.parse_args()

    # Create new GitHub repository if requested
    if args.new_repo:
        print(f"🆕 Creating new GitHub repository: {args.new_repo}")
        repo_url = create_github_repo(
            args.new_repo,
            private=args.private,
            description=args.description or ""
        )
        if not repo_url:
            sys.exit(1)
        
        print(f"✅ Repository created: {repo_url}")
        
        # Initialize git if not already a repo
        if not os.path.exists(".git"):
            args.init = True
        
        # Set up git remote
        os.system(f"git remote add {args.remote} {repo_url}")

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