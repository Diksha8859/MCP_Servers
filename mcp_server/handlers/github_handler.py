#!/usr/bin/env python3
"""
GitHub Tool Handler for MCP Server
Handles execution of GitHub tool requests with proper validation and error handling
"""

import json
import logging
from typing import Dict, Any, Optional, List
from tools.github_tool import GitHubTool

logger = logging.getLogger(__name__)

class GitHubHandler:
    """Handles execution of GitHub MCP tool requests"""
    
    def __init__(self, github_tool: GitHubTool):
        self.github_tool = github_tool
        
        # Tool routing map
        self.tool_handlers = {
            # Repository operations
            "github_get_repository_info": self._handle_get_repository_info,
            "github_list_repositories": self._handle_list_repositories,
            "github_get_repository_contents": self._handle_get_repository_contents,
            "github_get_repository_branches": self._handle_get_repository_branches,
            
            # Issue operations
            "github_list_issues": self._handle_list_issues,
            "github_create_issue": self._handle_create_issue,
            
            # Pull request operations
            "github_list_pull_requests": self._handle_list_pull_requests,
            "github_get_pull_request_reviews": self._handle_get_pull_request_reviews,
            "github_create_pull_request_review": self._handle_create_pull_request_review,
            "github_get_pull_request_review_comments": self._handle_get_pull_request_review_comments,
            "github_create_pull_request_review_comment": self._handle_create_pull_request_review_comment,
            "github_update_pull_request_review_comment": self._handle_update_pull_request_review_comment,
            "github_delete_pull_request_review_comment": self._handle_delete_pull_request_review_comment,
            "github_get_pull_request_files": self._handle_get_pull_request_files,
            
            # Search operations
            "github_search_repositories": self._handle_search_repositories,
            
            # User operations
            "github_get_user_info": self._handle_get_user_info,
            "github_get_my_repositories": self._handle_get_my_repositories,
            "github_get_my_user_info": self._handle_get_my_user_info
        }
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute a GitHub tool with given arguments
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            JSON string with tool execution results
        """
        try:
            logger.info(f"Executing GitHub tool: {tool_name} with arguments: {arguments}")
            
            # Get tool handler
            handler = self.tool_handlers.get(tool_name)
            if not handler:
                return json.dumps({
                    "error": f"Unknown GitHub tool: {tool_name}",
                    "available_tools": list(self.tool_handlers.keys())
                })
            
            # Execute tool
            result = await handler(arguments)
            return result
            
        except Exception as e:
            logger.error(f"Error executing GitHub tool {tool_name}: {e}")
            return json.dumps({
                "error": str(e),
                "tool": tool_name,
                "arguments": arguments
            })
    
    # Repository Tool Handlers
    async def _handle_get_repository_info(self, args: Dict[str, Any]) -> str:
        """Handle get repository information operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        
        if not owner:
            return json.dumps({"error": "Owner parameter is required"})
        if not repo:
            return json.dumps({"error": "Repository parameter is required"})
        
        return self.github_tool.get_repository_info(owner, repo)
    
    async def _handle_list_repositories(self, args: Dict[str, Any]) -> str:
        """Handle list repositories operation"""
        owner = args.get("owner")
        repo_type = args.get("type", "all")
        per_page = args.get("per_page", 30)
        
        if not owner:
            return json.dumps({"error": "Owner parameter is required"})
        
        # Validate parameters
        if repo_type not in ["all", "owner", "member"]:
            return json.dumps({"error": "Type must be one of: all, owner, member"})
        
        if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
            return json.dumps({"error": "per_page must be an integer between 1 and 100"})
        
        return self.github_tool.list_repositories(owner, repo_type, per_page)
    
    async def _handle_get_repository_contents(self, args: Dict[str, Any]) -> str:
        """Handle get repository contents operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        path = args.get("path", "")
        ref = args.get("ref")
        
        if not owner:
            return json.dumps({"error": "Owner parameter is required"})
        if not repo:
            return json.dumps({"error": "Repository parameter is required"})
        
        return self.github_tool.get_repository_contents(owner, repo, path, ref)
    
    async def _handle_get_repository_branches(self, args: Dict[str, Any]) -> str:
        """Handle get repository branches operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        per_page = args.get("per_page", 30)
        
        if not owner:
            return json.dumps({"error": "Owner parameter is required"})
        if not repo:
            return json.dumps({"error": "Repository parameter is required"})
        
        if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
            return json.dumps({"error": "per_page must be an integer between 1 and 100"})
        
        return self.github_tool.get_repository_branches(owner, repo, per_page)
    
    # Issue Tool Handlers
    async def _handle_list_issues(self, args: Dict[str, Any]) -> str:
        """Handle list issues operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        state = args.get("state", "open")
        labels = args.get("labels")
        per_page = args.get("per_page", 30)
        
        if not owner:
            return json.dumps({"error": "Owner parameter is required"})
        if not repo:
            return json.dumps({"error": "Repository parameter is required"})
        
        # Validate parameters
        if state not in ["open", "closed", "all"]:
            return json.dumps({"error": "State must be one of: open, closed, all"})
        
        if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
            return json.dumps({"error": "per_page must be an integer between 1 and 100"})
        
        return self.github_tool.list_issues(owner, repo, state, labels, per_page)
    
    async def _handle_create_issue(self, args: Dict[str, Any]) -> str:
        """Handle create issue operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        title = args.get("title")
        body = args.get("body")
        labels = args.get("labels")
        assignees = args.get("assignees")
        
        if not owner:
            return json.dumps({"error": "Owner parameter is required"})
        if not repo:
            return json.dumps({"error": "Repository parameter is required"})
        if not title:
            return json.dumps({"error": "Title parameter is required"})
        
        # Validate parameters
        if labels and not isinstance(labels, list):
            return json.dumps({"error": "Labels must be a list of strings"})
        
        if assignees and not isinstance(assignees, list):
            return json.dumps({"error": "Assignees must be a list of usernames"})
        
        return self.github_tool.create_issue(owner, repo, title, body, labels, assignees)
    
    # Pull Request Tool Handlers
    async def _handle_list_pull_requests(self, args: Dict[str, Any]) -> str:
        """Handle list pull requests operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        state = args.get("state", "open")
        per_page = args.get("per_page", 30)
        
        if not owner:
            return json.dumps({"error": "Owner parameter is required"})
        if not repo:
            return json.dumps({"error": "Repository parameter is required"})
        
        # Validate parameters
        if state not in ["open", "closed", "all"]:
            return json.dumps({"error": "State must be one of: open, closed, all"})
        
        if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
            return json.dumps({"error": "per_page must be an integer between 1 and 100"})
        
        return self.github_tool.list_pull_requests(owner, repo, state, per_page)
    
    # Search Tool Handlers
    async def _handle_search_repositories(self, args: Dict[str, Any]) -> str:
        """Handle search repositories operation"""
        query = args.get("query")
        sort = args.get("sort", "stars")
        order = args.get("order", "desc")
        per_page = args.get("per_page", 30)
        
        if not query:
            return json.dumps({"error": "Query parameter is required"})
        
        # Validate parameters
        if sort not in ["stars", "forks", "updated"]:
            return json.dumps({"error": "Sort must be one of: stars, forks, updated"})
        
        if order not in ["asc", "desc"]:
            return json.dumps({"error": "Order must be one of: asc, desc"})
        
        if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
            return json.dumps({"error": "per_page must be an integer between 1 and 100"})
        
        return self.github_tool.search_repositories(query, sort, order, per_page)
    
    # User Tool Handlers
    async def _handle_get_user_info(self, args: Dict[str, Any]) -> str:
        """Handle get user information operation"""
        username = args.get("username")
        
        if not username:
            return json.dumps({"error": "Username parameter is required"})
        
        return self.github_tool.get_user_info(username)
    
    async def _handle_get_my_repositories(self, args: Dict[str, Any]) -> str:
        """Handle get my repositories operation"""
        repo_type = args.get("type", "all")
        per_page = args.get("per_page", 30)
        
        # Validate parameters
        if repo_type not in ["all", "owner", "member", "private", "public"]:
            return json.dumps({"error": "Type must be one of: all, owner, member, private, public"})
        
        if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
            return json.dumps({"error": "per_page must be an integer between 1 and 100"})
        
        return self.github_tool.get_my_repositories(repo_type, per_page)
    
    async def _handle_get_my_user_info(self, args: Dict[str, Any]) -> str:
        """Handle get my user info operation"""
        return self.github_tool.get_authenticated_user_info()
    
    async def _handle_get_pull_request_reviews(self, args: Dict[str, Any]) -> str:
        """Handle get pull request reviews operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        pull_number = args.get("pull_number")
        
        if not isinstance(pull_number, int):
            return json.dumps({"error": "pull_number must be an integer"})
        
        return self.github_tool.get_pull_request_reviews(owner, repo, pull_number)
    
    async def _handle_create_pull_request_review(self, args: Dict[str, Any]) -> str:
        """Handle create pull request review operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        pull_number = args.get("pull_number")
        event = args.get("event", "COMMENT")
        body = args.get("body")
        comments = args.get("comments")
        
        if not isinstance(pull_number, int):
            return json.dumps({"error": "pull_number must be an integer"})
        
        return self.github_tool.create_pull_request_review(owner, repo, pull_number, event, body, comments)
    
    async def _handle_get_pull_request_review_comments(self, args: Dict[str, Any]) -> str:
        """Handle get pull request review comments operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        pull_number = args.get("pull_number")
        
        if not isinstance(pull_number, int):
            return json.dumps({"error": "pull_number must be an integer"})
        
        return self.github_tool.get_pull_request_review_comments(owner, repo, pull_number)
    
    async def _handle_create_pull_request_review_comment(self, args: Dict[str, Any]) -> str:
        """Handle create pull request review comment operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        pull_number = args.get("pull_number")
        body = args.get("body")
        commit_id = args.get("commit_id")
        path = args.get("path")
        line = args.get("line")
        side = args.get("side", "RIGHT")
        
        if not isinstance(pull_number, int):
            return json.dumps({"error": "pull_number must be an integer"})
        
        if not all([body, commit_id, path]):
            return json.dumps({"error": "body, commit_id, and path are required"})
        
        return self.github_tool.create_pull_request_review_comment(
            owner, repo, pull_number, body, commit_id, path, line, side
        )
    
    async def _handle_update_pull_request_review_comment(self, args: Dict[str, Any]) -> str:
        """Handle update pull request review comment operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        comment_id = args.get("comment_id")
        body = args.get("body")
        
        if not isinstance(comment_id, int):
            return json.dumps({"error": "comment_id must be an integer"})
        
        if not body:
            return json.dumps({"error": "body is required"})
        
        return self.github_tool.update_pull_request_review_comment(owner, repo, comment_id, body)
    
    async def _handle_delete_pull_request_review_comment(self, args: Dict[str, Any]) -> str:
        """Handle delete pull request review comment operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        comment_id = args.get("comment_id")
        
        if not isinstance(comment_id, int):
            return json.dumps({"error": "comment_id must be an integer"})
        
        return self.github_tool.delete_pull_request_review_comment(owner, repo, comment_id)
    
    async def _handle_get_pull_request_files(self, args: Dict[str, Any]) -> str:
        """Handle get pull request files operation"""
        owner = args.get("owner")
        repo = args.get("repo")
        pull_number = args.get("pull_number")
        
        if not isinstance(pull_number, int):
            return json.dumps({"error": "pull_number must be an integer"})
        
        return self.github_tool.get_pull_request_files(owner, repo, pull_number)
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all available GitHub tools"""
        tools_info = {}
        
        for tool_name, handler in self.tool_handlers.items():
            tools_info[tool_name] = {
                "name": tool_name,
                "handler": handler.__name__,
                "async": True,
                "category": self._get_tool_category(tool_name)
            }
        
        return tools_info
    
    def _get_tool_category(self, tool_name: str) -> str:
        """Get category for a tool based on its name"""
        if "repository" in tool_name or "repo" in tool_name:
            return "repository"
        elif "issue" in tool_name:
            return "issues"
        elif "pull" in tool_name:
            return "pull_requests"
        elif "search" in tool_name:
            return "search"
        elif "user" in tool_name:
            return "users"
        else:
            return "general"
    
    def validate_arguments(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate tool arguments
        
        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Basic validation for required parameters
        required_params = {
            "github_get_repository_info": ["owner", "repo"],
            "github_list_repositories": ["owner"],
            "github_get_repository_contents": ["owner", "repo"],
            "github_get_repository_branches": ["owner", "repo"],
            "github_list_issues": ["owner", "repo"],
            "github_create_issue": ["owner", "repo", "title"],
            "github_list_pull_requests": ["owner", "repo"],
            "github_search_repositories": ["query"],
            "github_get_user_info": ["username"],
            "github_get_my_repositories": [],
            "github_get_my_user_info": [],
            # PR Review tools
            "github_get_pull_request_reviews": ["owner", "repo", "pull_number"],
            "github_create_pull_request_review": ["owner", "repo", "pull_number"],
            "github_get_pull_request_review_comments": ["owner", "repo", "pull_number"],
            "github_create_pull_request_review_comment": ["owner", "repo", "pull_number", "body", "commit_id", "path"],
            "github_update_pull_request_review_comment": ["owner", "repo", "comment_id", "body"],
            "github_delete_pull_request_review_comment": ["owner", "repo", "comment_id"],
            "github_get_pull_request_files": ["owner", "repo", "pull_number"]
        }
        
        if tool_name in required_params:
            for param in required_params[tool_name]:
                if param not in arguments or arguments[param] is None:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Missing required parameter: {param}")
        
        # Additional validations
        if tool_name == "github_create_issue" and not self.github_tool.github_token:
            validation_result["warnings"].append("GitHub token required for creating issues")
        
        return validation_result