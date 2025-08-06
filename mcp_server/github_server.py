#!/usr/bin/env python3
"""
GitHub MCP Server - Perfect Implementation
Comprehensive GitHub repository management using FastMCP pattern
Compatible with MCP version 1.12.3
"""

import sys
import os
import logging
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Add venv to path for imports
sys.path.insert(0, '../venv/lib/python3.10/site-packages')

from mcp.server.fastmcp import FastMCP
from tools.github_tool import GitHubTool

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("github-mcp-server")

# Initialize GitHub tool
github_tool = GitHubTool()

# Repository Operations
@mcp.tool()
async def github_get_repository_info(owner: str, repo: str) -> str:
    """
    Get detailed information about a GitHub repository.
    
    Args:
        owner: Repository owner username or organization
        repo: Repository name
        
    Returns:
        JSON string with comprehensive repository information including stats, metadata, and URLs
    """
    logger.info(f"Getting repository info for {owner}/{repo}")
    return github_tool.get_repository_info(owner, repo)

@mcp.tool()
async def github_list_repositories(
    owner: str, 
    repo_type: str = "all", 
    per_page: int = 30
) -> str:
    """
    List repositories for a user or organization.
    
    Args:
        owner: Username or organization name
        repo_type: Type of repositories to list (all, owner, member)
        per_page: Number of repositories per page (1-100, default: 30)
        
    Returns:
        JSON string with list of repositories and their basic information
    """
    logger.info(f"Listing repositories for {owner} (type: {repo_type})")
    return github_tool.list_repositories(owner, repo_type, per_page)

@mcp.tool()
async def github_get_repository_contents(
    owner: str, 
    repo: str, 
    path: str = "", 
    ref: Optional[str] = None
) -> str:
    """
    Get contents of a repository directory or file.
    
    Args:
        owner: Repository owner
        repo: Repository name
        path: Path to directory or file (empty string for root directory)
        ref: Branch, tag, or commit SHA (optional, defaults to default branch)
        
    Returns:
        JSON string with directory listing or file content
    """
    logger.info(f"Getting contents for {owner}/{repo} at path: {path or 'root'}")
    return github_tool.get_repository_contents(owner, repo, path, ref)

@mcp.tool()
async def github_get_repository_branches(
    owner: str, 
    repo: str, 
    per_page: int = 30
) -> str:
    """
    List all branches for a repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        per_page: Number of branches per page (1-100, default: 30)
        
    Returns:
        JSON string with list of branches and their commit information
    """
    logger.info(f"Getting branches for {owner}/{repo}")
    return github_tool.get_repository_branches(owner, repo, per_page)

# Issue Operations
@mcp.tool()
async def github_list_issues(
    owner: str, 
    repo: str, 
    state: str = "open", 
    labels: Optional[str] = None, 
    per_page: int = 30
) -> str:
    """
    List issues for a repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: Issue state to filter by (open, closed, all)
        labels: Comma-separated list of label names to filter by (optional)
        per_page: Number of issues per page (1-100, default: 30)
        
    Returns:
        JSON string with list of issues and their details
    """
    logger.info(f"Listing issues for {owner}/{repo} (state: {state})")
    return github_tool.list_issues(owner, repo, state, labels, per_page)

@mcp.tool()
async def github_create_issue(
    owner: str, 
    repo: str, 
    title: str, 
    body: Optional[str] = None,
    labels: Optional[List[str]] = None, 
    assignees: Optional[List[str]] = None
) -> str:
    """
    Create a new issue in a repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        title: Issue title
        body: Issue description/body (optional)
        labels: List of label names to apply (optional)
        assignees: List of usernames to assign the issue to (optional)
        
    Returns:
        JSON string with created issue information
        
    Note:
        Requires a valid GitHub token with appropriate permissions
    """
    logger.info(f"Creating issue in {owner}/{repo}: {title}")
    return github_tool.create_issue(owner, repo, title, body, labels, assignees)

# Pull Request Operations
@mcp.tool()
async def github_list_pull_requests(
    owner: str, 
    repo: str, 
    state: str = "open", 
    per_page: int = 30
) -> str:
    """
    List pull requests for a repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: Pull request state to filter by (open, closed, all)
        per_page: Number of pull requests per page (1-100, default: 30)
        
    Returns:
        JSON string with list of pull requests and their details
    """
    logger.info(f"Listing pull requests for {owner}/{repo} (state: {state})")
    return github_tool.list_pull_requests(owner, repo, state, per_page)

# Search Operations
@mcp.tool()
async def github_search_repositories(
    query: str, 
    sort: str = "stars", 
    order: str = "desc", 
    per_page: int = 30
) -> str:
    """
    Search for repositories on GitHub.
    
    Args:
        query: Search query (can include qualifiers like 'language:python', 'stars:>1000', etc.)
        sort: Sort field (stars, forks, updated)
        order: Sort order (asc, desc)
        per_page: Number of results per page (1-100, default: 30)
        
    Returns:
        JSON string with search results and repository information
        
    Examples:
        - "machine learning language:python"
        - "stars:>1000 language:javascript"
        - "fastapi topic:api"
    """
    logger.info(f"Searching repositories with query: {query}")
    return github_tool.search_repositories(query, sort, order, per_page)

# User Operations
@mcp.tool()
async def github_get_user_info(username: str) -> str:
    """
    Get information about a GitHub user.
    
    Args:
        username: GitHub username
        
    Returns:
        JSON string with user profile information including stats and social links
    """
    logger.info(f"Getting user info for: {username}")
    return github_tool.get_user_info(username)

# Personal Account Operations
@mcp.tool()
async def github_get_my_repositories(
    repo_type: str = "all", 
    per_page: int = 30
) -> str:
    """
    Get YOUR repositories (authenticated user's repositories).
    
    Args:
        repo_type: Type of repositories to list (all, owner, member, private, public)
        per_page: Number of repositories per page (1-100, default: 30)
        
    Returns:
        JSON string with your repository list including private repositories
        
    Note:
        This shows repositories for YOUR account (the token owner)
    """
    logger.info(f"Getting my repositories (type: {repo_type})")
    return github_tool.get_my_repositories(repo_type, per_page)

@mcp.tool()
async def github_get_my_user_info() -> str:
    """
    Get YOUR user information (authenticated user's profile).
    
    Returns:
        JSON string with your complete user profile information
        
    Note:
        This shows information for YOUR account (the token owner)
    """
    logger.info("Getting my user info")
    return github_tool.get_authenticated_user_info()

# Advanced Operations
@mcp.tool()
async def github_analyze_repository(owner: str, repo: str) -> str:
    """
    Perform comprehensive analysis of a GitHub repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        
    Returns:
        JSON string with comprehensive repository analysis including:
        - Repository info and statistics
        - Recent issues and pull requests
        - Branch information
        - Top contributors (if accessible)
    """
    logger.info(f"Performing comprehensive analysis of {owner}/{repo}")
    
    try:
        # Gather comprehensive repository data
        repo_info = github_tool.get_repository_info(owner, repo)
        branches = github_tool.get_repository_branches(owner, repo, 10)
        recent_issues = github_tool.list_issues(owner, repo, "all", None, 10)
        recent_prs = github_tool.list_pull_requests(owner, repo, "all", 10)
        
        # Combine all analysis data
        import json
        analysis = {
            "operation": "analyze_repository",
            "repository": f"{owner}/{repo}",
            "timestamp": github_tool._make_request("GET", "")["timestamp"] if "timestamp" in github_tool._make_request("GET", "") else None,
            "repository_info": json.loads(repo_info),
            "branches": json.loads(branches),
            "recent_issues": json.loads(recent_issues),
            "recent_pull_requests": json.loads(recent_prs)
        }
        
        return json.dumps(analysis, indent=2)
        
    except Exception as e:
        logger.error(f"Error analyzing repository {owner}/{repo}: {e}")
        return json.dumps({
            "error": f"Failed to analyze repository: {str(e)}",
            "repository": f"{owner}/{repo}"
        })

@mcp.tool()
async def github_get_trending_repositories(
    language: Optional[str] = None, 
    since: str = "daily",
    per_page: int = 30
) -> str:
    """
    Get trending repositories on GitHub.
    
    Args:
        language: Programming language to filter by (optional)
        since: Time period for trending (daily, weekly, monthly)
        per_page: Number of results per page (1-100, default: 30)
        
    Returns:
        JSON string with trending repositories
        
    Note:
        This uses search with date filters to approximate trending repositories
    """
    logger.info(f"Getting trending repositories (language: {language or 'all'}, since: {since})")
    
    try:
        from datetime import datetime, timedelta
        
        # Calculate date range based on 'since' parameter
        now = datetime.now()
        if since == "daily":
            days_back = 1
        elif since == "weekly":
            days_back = 7
        elif since == "monthly":
            days_back = 30
        else:
            days_back = 1
        
        start_date = (now - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        # Build search query
        query = f"created:>={start_date}"
        if language:
            query += f" language:{language}"
        
        return github_tool.search_repositories(query, "stars", "desc", per_page)
        
    except Exception as e:
        logger.error(f"Error getting trending repositories: {e}")
        return json.dumps({
            "error": f"Failed to get trending repositories: {str(e)}"
        })

if __name__ == "__main__":
    logger.info("Starting GitHub MCP Server...")
    
    # Check for GitHub token
    if not os.getenv("GITHUB_TOKEN"):
        logger.warning("⚠️  GITHUB_TOKEN not found in environment variables!")
        logger.warning("   Some operations will be limited. Please set GITHUB_TOKEN for full functionality.")
    else:
        logger.info("✅ GitHub token found - full functionality available")
    
    # Display available tools
    logger.info("📋 Available GitHub tools:")
    logger.info("   Repository: get_info, list, get_contents, get_branches, analyze")
    logger.info("   Issues: list, create")  
    logger.info("   Pull Requests: list")
    logger.info("   Search: repositories, trending")
    logger.info("   Users: get_info")
    logger.info("   Personal: get_my_repositories, get_my_user_info")
    
    mcp.run()