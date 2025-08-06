#!/usr/bin/env python3
"""
FastMCP MongoDB Server - Working Implementation
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
from tools.mongodb import MongoDBTool

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("mongodb-mcp-server")

# Initialize MongoDB tool
mongodb_tool = MongoDBTool()

@mcp.tool()
async def mongodb_find(
    collection: str, 
    query: Optional[Dict[str, Any]] = None, 
    limit: Optional[int] = None, 
    sort: Optional[Dict[str, Any]] = None
) -> str:
    """
    Query documents from MongoDB collection.
    
    Args:
        collection: Collection name
        query: MongoDB query filter (optional)
        limit: Maximum number of documents to return (optional)
        sort: Sort criteria (optional)
        
    Returns:
        JSON string with query results
    """
    logger.info(f"Finding documents in collection: {collection}")
    return mongodb_tool.find(collection, query, limit, sort)

@mcp.tool()
async def mongodb_insert(collection: str, documents: List[Dict[str, Any]]) -> str:
    """
    Insert documents into MongoDB collection.
    
    Args:
        collection: Collection name
        documents: Array of documents to insert
        
    Returns:
        JSON string with insert results
    """
    logger.info(f"Inserting {len(documents)} documents into collection: {collection}")
    return mongodb_tool.insert(collection, documents)

@mcp.tool()
async def mongodb_update(
    collection: str, 
    filter: Dict[str, Any], 
    update: Dict[str, Any], 
    upsert: bool = False
) -> str:
    """
    Update documents in MongoDB collection.
    
    Args:
        collection: Collection name
        filter: Filter to match documents
        update: Update operations
        upsert: Create if doesn't exist (default: False)
        
    Returns:
        JSON string with update results
    """
    logger.info(f"Updating documents in collection: {collection}")
    return mongodb_tool.update(collection, filter, update, upsert)

@mcp.tool()
async def mongodb_delete(collection: str, filter: Dict[str, Any]) -> str:
    """
    Delete documents from MongoDB collection.
    
    Args:
        collection: Collection name
        filter: Filter to match documents
        
    Returns:
        JSON string with delete results
    """
    logger.info(f"Deleting documents from collection: {collection}")
    return mongodb_tool.delete(collection, filter)

@mcp.tool()
async def mongodb_aggregate(collection: str, pipeline: List[Dict[str, Any]]) -> str:
    """
    Perform aggregation pipeline on MongoDB collection.
    
    Args:
        collection: Collection name
        pipeline: Aggregation pipeline stages
        
    Returns:
        JSON string with aggregation results
    """
    logger.info(f"Running aggregation on collection: {collection}")
    return mongodb_tool.aggregate(collection, pipeline)

@mcp.tool()
async def mongodb_get_collections() -> str:
    """
    Get list of all collections in the database.
    
    Returns:
        JSON string with collection names
    """
    logger.info("Getting list of collections")
    return mongodb_tool.get_collections()

@mcp.tool()
async def mongodb_get_collection_stats(collection: str) -> str:
    """
    Get statistics about a collection.
    
    Args:
        collection: Collection name
        
    Returns:
        JSON string with collection statistics
    """
    logger.info(f"Getting stats for collection: {collection}")
    return mongodb_tool.get_collection_stats(collection)

if __name__ == "__main__":
    logger.info("Starting FastMCP MongoDB Server...")
    mcp.run()