#!/usr/bin/env python3
"""
GitHub Integration Tool for MCP Server
Provides comprehensive GitHub repository management functionality
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import base64

logger = logging.getLogger(__name__)

class GitHubTool:
    """Tool for interacting with GitHub repositories and APIs"""
    
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_username = os.getenv("GITHUB_USERNAME")
        self.base_url = "https://api.github.com"
        
        if not self.github_token:
            logger.warning("GITHUB_TOKEN not found in environment variables. Some operations may be limited.")
        
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MCP-GitHub-Server/1.0"
        }
        
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to GitHub API"""
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30
            )
            
            if response.status_code == 401:
                return {"error": "Authentication failed. Please check your GitHub token."}
            elif response.status_code == 403:
                return {"error": "Access forbidden. Check repository permissions or rate limits."}
            elif response.status_code == 404:
                return {"error": "Resource not found. Check repository name and permissions."}
            elif not response.ok:
                return {"error": f"GitHub API error: {response.status_code} - {response.text}"}
            
            return response.json() if response.content else {"success": True}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API request failed: {e}")
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error in GitHub API request: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_repository_info(self, owner: str, repo: str) -> str:
        """
        Get detailed information about a GitHub repository
        
        Args:
            owner: Repository owner username or organization
            repo: Repository name
            
        Returns:
            JSON string with repository information
        """
        try:
            result = self._make_request("GET", f"repos/{owner}/{repo}")
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            # Extract relevant information
            repo_info = {
                "name": result.get("name"),
                "full_name": result.get("full_name"),
                "description": result.get("description"),
                "url": result.get("html_url"),
                "clone_url": result.get("clone_url"),
                "ssh_url": result.get("ssh_url"),
                "language": result.get("language"),
                "stars": result.get("stargazers_count"),
                "forks": result.get("forks_count"),
                "watchers": result.get("watchers_count"),
                "open_issues": result.get("open_issues_count"),
                "size": result.get("size"),
                "default_branch": result.get("default_branch"),
                "created_at": result.get("created_at"),
                "updated_at": result.get("updated_at"),
                "pushed_at": result.get("pushed_at"),
                "private": result.get("private"),
                "archived": result.get("archived"),
                "disabled": result.get("disabled"),
                "topics": result.get("topics", []),
                "license": result.get("license", {}).get("name") if result.get("license") else None,
                "owner": {
                    "login": result.get("owner", {}).get("login"),
                    "type": result.get("owner", {}).get("type"),
                    "url": result.get("owner", {}).get("html_url")
                }
            }
            
            return json.dumps({
                "operation": "get_repository_info",
                "repository": f"{owner}/{repo}",
                "data": repo_info
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting repository info: {e}")
            return json.dumps({"error": str(e)})
    
    def list_repositories(self, owner: str, repo_type: str = "all", per_page: int = 30) -> str:
        """
        List repositories for a user or organization
        
        Args:
            owner: Username or organization name
            repo_type: Type of repositories (all, owner, member)
            per_page: Number of repositories per page (max 100)
            
        Returns:
            JSON string with repository list
        """
        try:
            params = {
                "type": repo_type,
                "per_page": min(per_page, 100),
                "sort": "updated"
            }
            
            result = self._make_request("GET", f"users/{owner}/repos", params=params)
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            repositories = []
            for repo in result:
                repositories.append({
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "description": repo.get("description"),
                    "url": repo.get("html_url"),
                    "language": repo.get("language"),
                    "stars": repo.get("stargazers_count"),
                    "forks": repo.get("forks_count"),
                    "updated_at": repo.get("updated_at"),
                    "private": repo.get("private")
                })
            
            return json.dumps({
                "operation": "list_repositories",
                "owner": owner,
                "type": repo_type,
                "count": len(repositories),
                "repositories": repositories
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error listing repositories: {e}")
            return json.dumps({"error": str(e)})
    
    def get_repository_contents(self, owner: str, repo: str, path: str = "", ref: str = None) -> str:
        """
        Get contents of a repository directory or file
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: Path to directory or file (empty for root)
            ref: Branch, tag, or commit SHA (defaults to default branch)
            
        Returns:
            JSON string with contents information
        """
        try:
            params = {}
            if ref:
                params["ref"] = ref
            
            endpoint = f"repos/{owner}/{repo}/contents/{path}"
            result = self._make_request("GET", endpoint, params=params)
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            # Handle single file vs directory
            if isinstance(result, list):
                # Directory listing
                contents = []
                for item in result:
                    contents.append({
                        "name": item.get("name"),
                        "path": item.get("path"),
                        "type": item.get("type"),
                        "size": item.get("size"),
                        "url": item.get("html_url"),
                        "download_url": item.get("download_url")
                    })
                
                return json.dumps({
                    "operation": "get_repository_contents",
                    "repository": f"{owner}/{repo}",
                    "path": path or "/",
                    "type": "directory",
                    "contents": contents
                }, indent=2)
            else:
                # Single file
                file_info = {
                    "name": result.get("name"),
                    "path": result.get("path"),
                    "type": result.get("type"),
                    "size": result.get("size"),
                    "encoding": result.get("encoding"),
                    "url": result.get("html_url"),
                    "download_url": result.get("download_url")
                }
                
                # Decode file content if it's base64 encoded and reasonable size
                if (result.get("encoding") == "base64" and 
                    result.get("size", 0) < 1048576):  # 1MB limit
                    try:
                        content = base64.b64decode(result.get("content", "")).decode('utf-8')
                        file_info["content"] = content
                    except Exception:
                        file_info["content"] = "Binary file or encoding error"
                
                return json.dumps({
                    "operation": "get_repository_contents",
                    "repository": f"{owner}/{repo}",
                    "path": path,
                    "type": "file",
                    "file": file_info
                }, indent=2)
                
        except Exception as e:
            logger.error(f"Error getting repository contents: {e}")
            return json.dumps({"error": str(e)})
    
    def list_issues(self, owner: str, repo: str, state: str = "open", labels: Optional[str] = None, per_page: int = 30) -> str:
        """
        List issues for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state (open, closed, all)
            labels: Comma-separated list of labels
            per_page: Number of issues per page (max 100)
            
        Returns:
            JSON string with issues list
        """
        try:
            params = {
                "state": state,
                "per_page": min(per_page, 100),
                "sort": "updated"
            }
            
            if labels:
                params["labels"] = labels
            
            result = self._make_request("GET", f"repos/{owner}/{repo}/issues", params=params)
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            issues = []
            for issue in result:
                # Skip pull requests (they appear in issues API)
                if issue.get("pull_request"):
                    continue
                    
                issues.append({
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "body": issue.get("body", "")[:500] + "..." if len(issue.get("body", "")) > 500 else issue.get("body", ""),
                    "state": issue.get("state"),
                    "user": issue.get("user", {}).get("login"),
                    "assignees": [assignee.get("login") for assignee in issue.get("assignees", [])],
                    "labels": [label.get("name") for label in issue.get("labels", [])],
                    "created_at": issue.get("created_at"),
                    "updated_at": issue.get("updated_at"),
                    "url": issue.get("html_url"),
                    "comments": issue.get("comments")
                })
            
            return json.dumps({
                "operation": "list_issues",
                "repository": f"{owner}/{repo}",
                "state": state,
                "count": len(issues),
                "issues": issues
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error listing issues: {e}")
            return json.dumps({"error": str(e)})
    
    def create_issue(self, owner: str, repo: str, title: str, body: Optional[str] = None, 
                    labels: Optional[List[str]] = None, assignees: Optional[List[str]] = None) -> str:
        """
        Create a new issue in a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            title: Issue title
            body: Issue description
            labels: List of label names
            assignees: List of usernames to assign
            
        Returns:
            JSON string with created issue information
        """
        try:
            if not self.github_token:
                return json.dumps({"error": "GitHub token required for creating issues"})
            
            data = {"title": title}
            
            if body:
                data["body"] = body
            if labels:
                data["labels"] = labels
            if assignees:
                data["assignees"] = assignees
            
            result = self._make_request("POST", f"repos/{owner}/{repo}/issues", data=data)
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            issue_info = {
                "number": result.get("number"),
                "title": result.get("title"),
                "body": result.get("body"),
                "state": result.get("state"),
                "user": result.get("user", {}).get("login"),
                "url": result.get("html_url"),
                "created_at": result.get("created_at")
            }
            
            return json.dumps({
                "operation": "create_issue",
                "repository": f"{owner}/{repo}",
                "success": True,
                "issue": issue_info
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            return json.dumps({"error": str(e)})
    
    def list_pull_requests(self, owner: str, repo: str, state: str = "open", per_page: int = 30) -> str:
        """
        List pull requests for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: PR state (open, closed, all)
            per_page: Number of PRs per page (max 100)
            
        Returns:
            JSON string with pull requests list
        """
        try:
            params = {
                "state": state,
                "per_page": min(per_page, 100),
                "sort": "updated"
            }
            
            result = self._make_request("GET", f"repos/{owner}/{repo}/pulls", params=params)
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            pulls = []
            for pr in result:
                pulls.append({
                    "number": pr.get("number"),
                    "title": pr.get("title"),
                    "body": pr.get("body", "")[:500] + "..." if len(pr.get("body", "")) > 500 else pr.get("body", ""),
                    "state": pr.get("state"),
                    "user": pr.get("user", {}).get("login"),
                    "head": {
                        "ref": pr.get("head", {}).get("ref"),
                        "sha": pr.get("head", {}).get("sha")
                    },
                    "base": {
                        "ref": pr.get("base", {}).get("ref"),
                        "sha": pr.get("base", {}).get("sha")
                    },
                    "created_at": pr.get("created_at"),
                    "updated_at": pr.get("updated_at"),
                    "url": pr.get("html_url"),
                    "mergeable": pr.get("mergeable"),
                    "merged": pr.get("merged")
                })
            
            return json.dumps({
                "operation": "list_pull_requests",
                "repository": f"{owner}/{repo}",
                "state": state,
                "count": len(pulls),
                "pull_requests": pulls
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error listing pull requests: {e}")
            return json.dumps({"error": str(e)})
    
    def get_repository_branches(self, owner: str, repo: str, per_page: int = 30) -> str:
        """
        List branches for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            per_page: Number of branches per page (max 100)
            
        Returns:
            JSON string with branches list
        """
        try:
            params = {"per_page": min(per_page, 100)}
            
            result = self._make_request("GET", f"repos/{owner}/{repo}/branches", params=params)
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            branches = []
            for branch in result:
                branches.append({
                    "name": branch.get("name"),
                    "sha": branch.get("commit", {}).get("sha"),
                    "protected": branch.get("protected"),
                    "url": branch.get("commit", {}).get("url")
                })
            
            return json.dumps({
                "operation": "get_repository_branches",
                "repository": f"{owner}/{repo}",
                "count": len(branches),
                "branches": branches
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting repository branches: {e}")
            return json.dumps({"error": str(e)})
    
    def search_repositories(self, query: str, sort: str = "stars", order: str = "desc", per_page: int = 30) -> str:
        """
        Search for repositories on GitHub
        
        Args:
            query: Search query
            sort: Sort field (stars, forks, updated)
            order: Sort order (asc, desc)
            per_page: Number of results per page (max 100)
            
        Returns:
            JSON string with search results
        """
        try:
            params = {
                "q": query,
                "sort": sort,
                "order": order,
                "per_page": min(per_page, 100)
            }
            
            result = self._make_request("GET", "search/repositories", params=params)
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            repositories = []
            for repo in result.get("items", []):
                repositories.append({
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "description": repo.get("description"),
                    "url": repo.get("html_url"),
                    "language": repo.get("language"),
                    "stars": repo.get("stargazers_count"),
                    "forks": repo.get("forks_count"),
                    "updated_at": repo.get("updated_at"),
                    "owner": repo.get("owner", {}).get("login")
                })
            
            return json.dumps({
                "operation": "search_repositories",
                "query": query,
                "total_count": result.get("total_count"),
                "count": len(repositories),
                "repositories": repositories
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error searching repositories: {e}")
            return json.dumps({"error": str(e)})
    
    def get_user_info(self, username: str) -> str:
        """
        Get information about a GitHub user
        
        Args:
            username: GitHub username
            
        Returns:
            JSON string with user information
        """
        try:
            result = self._make_request("GET", f"users/{username}")
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            user_info = {
                "login": result.get("login"),
                "name": result.get("name"),
                "bio": result.get("bio"),
                "company": result.get("company"),
                "location": result.get("location"),
                "email": result.get("email"),
                "blog": result.get("blog"),
                "twitter_username": result.get("twitter_username"),
                "public_repos": result.get("public_repos"),
                "public_gists": result.get("public_gists"),
                "followers": result.get("followers"),
                "following": result.get("following"),
                "created_at": result.get("created_at"),
                "updated_at": result.get("updated_at"),
                "url": result.get("html_url"),
                "avatar_url": result.get("avatar_url"),
                "type": result.get("type")
            }
            
            return json.dumps({
                "operation": "get_user_info",
                "username": username,
                "user": user_info
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return json.dumps({"error": str(e)})
    
    def get_my_repositories(self, repo_type: str = "all", per_page: int = 30) -> str:
        """
        Get repositories for the authenticated user (your repositories)
        
        Args:
            repo_type: Type of repositories (all, owner, member, private, public)
            per_page: Number of repositories per page (max 100)
            
        Returns:
            JSON string with your repository list
        """
        try:
            if not self.github_token:
                return json.dumps({"error": "GitHub token required to get your repositories"})
            
            if not self.github_username:
                return json.dumps({"error": "GitHub username not configured. Please set GITHUB_USERNAME in environment"})
            
            # Use the authenticated user endpoint for better results
            params = {
                "type": repo_type,
                "per_page": min(per_page, 100),
                "sort": "updated"
            }
            
            result = self._make_request("GET", "user/repos", params=params)
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            repositories = []
            for repo in result:
                repositories.append({
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "description": repo.get("description"),
                    "url": repo.get("html_url"),
                    "clone_url": repo.get("clone_url"),
                    "ssh_url": repo.get("ssh_url"),
                    "language": repo.get("language"),
                    "stars": repo.get("stargazers_count"),
                    "forks": repo.get("forks_count"),
                    "updated_at": repo.get("updated_at"),
                    "private": repo.get("private"),
                    "fork": repo.get("fork"),
                    "archived": repo.get("archived"),
                    "default_branch": repo.get("default_branch")
                })
            
            return json.dumps({
                "operation": "get_my_repositories",
                "username": self.github_username,
                "type": repo_type,
                "count": len(repositories),
                "repositories": repositories
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting your repositories: {e}")
            return json.dumps({"error": str(e)})
    
    def get_authenticated_user_info(self) -> str:
        """
        Get information about the authenticated user (you)
        
        Returns:
            JSON string with your user information
        """
        try:
            if not self.github_token:
                return json.dumps({"error": "GitHub token required to get your user info"})
            
            result = self._make_request("GET", "user")
            
            if "error" in result:
                return json.dumps(result, indent=2)
            
            user_info = {
                "login": result.get("login"),
                "name": result.get("name"),
                "bio": result.get("bio"),
                "company": result.get("company"),
                "location": result.get("location"),
                "email": result.get("email"),
                "blog": result.get("blog"),
                "twitter_username": result.get("twitter_username"),
                "public_repos": result.get("public_repos"),
                "public_gists": result.get("public_gists"),
                "followers": result.get("followers"),
                "following": result.get("following"),
                "created_at": result.get("created_at"),
                "updated_at": result.get("updated_at"),
                "url": result.get("html_url"),
                "avatar_url": result.get("avatar_url"),
                "type": result.get("type"),
                "plan": result.get("plan", {}).get("name") if result.get("plan") else None
            }
            
            return json.dumps({
                "operation": "get_authenticated_user_info",
                "user": user_info
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting your user info: {e}")
            return json.dumps({"error": str(e)})

    def close(self):
        """Close any connections (placeholder for consistency)"""
        pass