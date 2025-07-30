import os
import argparse
import sys
import requests
from getpass import getpass
import json

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
        "auto_init": False
    }
    
    try:
        response = requests.post(
            "https://api.github.com/user/repos",
            headers=headers,
            json=data
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
                reset_time = limits['resources']['core']['reset']
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

def run():
    parser = argparse.ArgumentParser(
        description="📦 CLI tool to automate git operations and GitHub repository creation"
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
        
        if not repo_url:
            sys.exit(1)
            
        # Initialize git if needed
        if not os.path.exists(".git"):
            args.init = True
            
        # Set remote
        os.system(f"git remote add {args.remote} {repo_url}")

    if args.init:
        print("🛠 Initializing git repository")
        os.system("git init")

    os.system("git add .")

    if args.commit:
        print(f"📦 Committing: '{args.commit}'")
        os.system(f'git commit -m "{args.commit}"')
    else:
        print("⚠️  Skipping commit (no message provided)")

    push_cmd = "git push"
    if args.force:
        push_cmd += " --force-with-lease"
    if args.tags:
        push_cmd += " --tags"
    if args.remote and args.branch:
        push_cmd += f" {args.remote} {args.branch}"

    print(f"🚀 Executing: {push_cmd}")
    os.system(push_cmd)

if __name__ == "__main__":
    run()