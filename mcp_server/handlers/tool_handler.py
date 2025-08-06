#!/usr/bin/env python3
"""
Tool Handler for MCP Server
Executes LLM tool requests by routing to appropriate tools
"""

import json
import logging
from typing import Dict, Any, Optional, Callable, Awaitable
from tools.mongodb import MongoDBTool

logger = logging.getLogger(__name__)

class ToolHandler:
    """Handles execution of MCP tool requests"""
    
    def __init__(self, mongodb_tool: MongoDBTool):
        self.mongodb_tool = mongodb_tool
        
        # Tool routing map
        self.tool_handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[str]]] = {
            # MongoDB Tools
            "mongodb_find": self._handle_mongodb_find,
            "mongodb_insert": self._handle_mongodb_insert,
            "mongodb_update": self._handle_mongodb_update,
            "mongodb_delete": self._handle_mongodb_delete,
            "mongodb_aggregate": self._handle_mongodb_aggregate,
            "mongodb_get_collections": self._handle_mongodb_get_collections,
            "mongodb_get_collection_stats": self._handle_mongodb_get_collection_stats
        }
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute a tool with given arguments
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            JSON string with tool execution results
        """
        try:
            logger.info(f"Executing tool: {tool_name} with arguments: {arguments}")
            
            # Get tool handler
            handler = self.tool_handlers.get(tool_name)
            if not handler:
                return json.dumps({
                    "error": f"Unknown tool: {tool_name}",
                    "available_tools": list(self.tool_handlers.keys())
                })
            
            # Execute tool
            result = await handler(arguments)
            return result
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return json.dumps({
                "error": str(e),
                "tool": tool_name,
                "arguments": arguments
            })
    
    # MongoDB Tool Handlers
    async def _handle_mongodb_find(self, args: Dict[str, Any]) -> str:
        """Handle MongoDB find operation"""
        collection = args.get("collection")
        if not collection:
            return json.dumps({"error": "Collection parameter is required"})
        
        return self.mongodb_tool.find(
            collection=collection,
            query=args.get("query"),
            limit=args.get("limit"),
            sort=args.get("sort")
        )
    
    async def _handle_mongodb_insert(self, args: Dict[str, Any]) -> str:
        """Handle MongoDB insert operation"""
        collection = args.get("collection")
        documents = args.get("documents")
        
        if not collection:
            return json.dumps({"error": "Collection parameter is required"})
        if not documents:
            return json.dumps({"error": "Documents parameter is required"})
        
        return self.mongodb_tool.insert(collection, documents)
    
    async def _handle_mongodb_update(self, args: Dict[str, Any]) -> str:
        """Handle MongoDB update operation"""
        collection = args.get("collection")
        filter_query = args.get("filter")
        update_query = args.get("update")
        
        if not collection:
            return json.dumps({"error": "Collection parameter is required"})
        if not filter_query:
            return json.dumps({"error": "Filter parameter is required"})
        if not update_query:
            return json.dumps({"error": "Update parameter is required"})
        
        return self.mongodb_tool.update(
            collection=collection,
            filter=filter_query,
            update=update_query,
            upsert=args.get("upsert", False)
        )
    
    async def _handle_mongodb_delete(self, args: Dict[str, Any]) -> str:
        """Handle MongoDB delete operation"""
        collection = args.get("collection")
        filter_query = args.get("filter")
        
        if not collection:
            return json.dumps({"error": "Collection parameter is required"})
        if not filter_query:
            return json.dumps({"error": "Filter parameter is required"})
        
        return self.mongodb_tool.delete(collection, filter_query)
    
    async def _handle_mongodb_aggregate(self, args: Dict[str, Any]) -> str:
        """Handle MongoDB aggregate operation"""
        collection = args.get("collection")
        pipeline = args.get("pipeline")
        
        if not collection:
            return json.dumps({"error": "Collection parameter is required"})
        if not pipeline:
            return json.dumps({"error": "Pipeline parameter is required"})
        
        return self.mongodb_tool.aggregate(collection, pipeline)
    
    async def _handle_mongodb_get_collections(self, args: Dict[str, Any]) -> str:
        """Handle MongoDB get collections operation"""
        return self.mongodb_tool.get_collections()
    
    async def _handle_mongodb_get_collection_stats(self, args: Dict[str, Any]) -> str:
        """Handle MongoDB get collection stats operation"""
        collection = args.get("collection")
        if not collection:
            return json.dumps({"error": "Collection parameter is required"})
        
        return self.mongodb_tool.get_collection_stats(collection)
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all available tools"""
        tools_info: Dict[str, Dict[str, Any]] = {}
        
        for tool_name, handler in self.tool_handlers.items():
            tools_info[tool_name] = {
                "name": tool_name,
                "handler": handler.__name__,
                "async": True
            }
        
        return tools_info
    
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
            "mongodb_find": ["collection"],
            "mongodb_insert": ["collection", "documents"],
            "mongodb_update": ["collection", "filter", "update"],
            "mongodb_delete": ["collection", "filter"],
            "mongodb_aggregate": ["collection", "pipeline"],
            "mongodb_get_collection_stats": ["collection"]
        }
        
        if tool_name in required_params:
            for param in required_params[tool_name]:
                if param not in arguments or arguments[param] is None:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Missing required parameter: {param}")
        
        return validation_result 