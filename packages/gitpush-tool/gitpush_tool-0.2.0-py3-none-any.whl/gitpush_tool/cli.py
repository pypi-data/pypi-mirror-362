#!/usr/bin/env python3
import os
import argparse
import sys
import requests
from getpass import getpass
import json
from datetime import datetime

def get_github_token():
    """Get GitHub token from various sources with priority order"""
    # 1. Check environment variable
    token = os.getenv("GITHUB_TOKEN")
    
    # 2. Check token file
    if not token:
        token_path = os.path.join(os.path.dirname(__file__), '..', 'token')
        if os.path.exists(token_path):
            with open(token_path, 'r') as f:
                token = f.read().strip()
    
    # 3. Prompt user if still not found
    if not token:
        print("\n🔑 GitHub personal access token is required to create repositories.")
        print("Create one at: https://github.com/settings/tokens (with 'repo' scope)")
        token = getpass("Enter your GitHub token: ")
    
    return token

def get_github_username():
    """Get GitHub username from config or API"""
    try:
        # Try git config first
        username = os.popen("git config github.user").read().strip()
        if username:
            return username
            
        # Fallback to API if token exists
        token = get_github_token()
        if token:
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github+json"
            }
            response = requests.get("https://api.github.com/user", headers=headers)
            if response.status_code == 200:
                return response.json().get("login")
    except:
        pass
    return None

def create_github_repo(repo_name, private=False, description=""):
    """Create a new GitHub repository using the GitHub API"""
    token = get_github_token()
    
    if not token:
        print("❌ GitHub token is required to create a repository")
        return None

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    data = {
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": False,
        "has_issues": True,
        "has_projects": False,
        "has_wiki": False
    }
    
    try:
        response = requests.post(
            "https://api.github.com/user/repos",
            headers=headers,
            json=data,
            timeout=10
        )
        
        # Detailed error handling
        if response.status_code == 401:
            print("❌ Authentication failed. Invalid or expired token.")
            print("Please create a new token with 'repo' scope at:")
            print("https://github.com/settings/tokens")
            return None
            
        elif response.status_code == 403:
            print("❌ Permission denied (403 Forbidden). Possible reasons:")
            print("- Token doesn't have 'repo' scope")
            print("- Token is restricted to specific repositories")
            print("- GitHub API rate limit exceeded")
            
            # Try to get rate limit info
            try:
                limits = requests.get(
                    "https://api.github.com/rate_limit",
                    headers=headers
                ).json()
                remaining = limits['resources']['core']['remaining']
                reset_time = datetime.fromtimestamp(limits['resources']['core']['reset']).strftime('%Y-%m-%d %H:%M:%S')
                print(f"⏳ API calls remaining: {remaining}")
                print(f"🔄 Rate limit resets at: {reset_time}")
            except:
                pass
                
            return None
            
        elif response.status_code == 422:
            error_data = response.json()
            if 'errors' in error_data:
                for error in error_data['errors']:
                    if error.get('field') == 'name' and 'already exists' in error.get('message', ''):
                        print(f"❌ Repository '{repo_name}' already exists")
                        return None
            print(f"❌ Validation error: {error_data.get('message', 'Unknown error')}")
            return None
            
        elif response.status_code != 201:
            print(f"❌ Failed to create repository (HTTP {response.status_code}): {response.text}")
            return None
            
        repo_url = response.json()["html_url"]
        print(f"✅ Successfully created repository: {repo_url}")
        return repo_url
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create repository: {str(e)}")
        if "Max retries exceeded" in str(e):
            print("⚠️  Network connection problem detected")
        return None

def create_with_gh_cli(repo_name, private=False, description=""):
    """Alternative using GitHub CLI if installed"""
    try:
        private_flag = "--private" if private else "--public"
        cmd = f"gh repo create {repo_name} {private_flag} --source=. --remote=origin --push"
        if description:
            cmd += f" --description \"{description}\""
        return os.system(cmd) == 0
    except:
        return False

def initialize_repository(remote_url=None):
    """Initialize git repository with sensible defaults"""
    if not os.path.exists(".git"):
        print("🛠 Initializing git repository")
        os.system("git init")
        os.system("git branch -M main")
        
        if remote_url:
            os.system(f"git remote add origin {remote_url}")
        
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
        current_version = "0.2.0"  # Should match your setup.py
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
        repo_url = create_github_repo(
            args.new_repo,
            private=args.private,
            description=args.description or ""
        )
        
        # Fallback to GitHub CLI if API fails
        if not repo_url:
            print("⚠️  Falling back to GitHub CLI...")
            if create_with_gh_cli(args.new_repo, args.private, args.description):
                username = get_github_username()
                if username:
                    repo_url = f"https://github.com/{username}/{args.new_repo}.git"
                else:
                    repo_url = None
            else:
                print("❌ Could not create repository. Please check your credentials.")
                print("You can install GitHub CLI with: brew install gh (Mac) or winget install --id GitHub.cli (Windows)")
                sys.exit(1)
        
        if repo_url:
            initialize_repository(repo_url)
            args.init = False  # Already initialized
        else:
            sys.exit(1)

    if args.init:
        initialize_repository()

    # Stage all changes
    os.system("git add .")

    if args.commit:
        print(f"📦 Committing: '{args.commit}'")
        commit_result = os.system(f'git commit -m "{args.commit}"')
        if commit_result != 0:
            print("❌ Commit failed")
            sys.exit(1)
    else:
        print("⚠️  Skipping commit (no message provided)")

    # Build push command
    push_cmd = "git push"
    if args.force:
        push_cmd += " --force-with-lease"
    if args.tags:
        push_cmd += " --tags"
    if args.remote and args.branch:
        push_cmd += f" {args.remote} {args.branch}"

    print(f"🚀 Executing: {push_cmd}")
    push_result = os.system(push_cmd)
    
    if push_result == 0:
        print("✅ Successfully pushed changes")
    else:
        print("❌ Push failed")
        sys.exit(1)

if __name__ == "__main__":
    check_for_updates()
    run()