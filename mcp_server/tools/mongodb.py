#!/usr/bin/env python3
"""
MongoDB Integration Tool for MCP Server
Provides functions to query, insert, update, and delete data in MongoDB
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError
from bson import ObjectId, json_util

logger = logging.getLogger(__name__)

class MongoDBTool:
    """Tool for interacting with MongoDB"""
    
    def __init__(self):
        self.mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.database_name = os.getenv("MONGODB_DATABASE", "mcp_database")
        self.default_collection = os.getenv("MONGODB_COLLECTION", "embeddings")
        
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.database_name]
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {self.mongodb_uri}")
        except PyMongoError as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _serialize_objectid(self, obj):
        """Convert ObjectId to string for JSON serialization"""
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: self._serialize_objectid(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_objectid(item) for item in obj]
        else:
            return obj
    
    def find(self, collection: str, query: Optional[Dict[str, Any]] = None, 
            limit: Optional[int] = None, sort: Optional[Dict[str, Any]] = None) -> str:
        """
        Query documents from MongoDB collection
        
        Args:
            collection: Collection name
            query: MongoDB query filter
            limit: Maximum number of documents to return
            sort: Sort criteria
            
        Returns:
            JSON string with query results
        """
        try:
            # Validate collection name
            if not collection or not isinstance(collection, str):
                return json.dumps({"error": "Collection name must be a non-empty string"})
            
            # Validate limit parameter
            if limit is not None and (not isinstance(limit, int) or limit < 0):
                return json.dumps({"error": "Limit must be a non-negative integer"})
            
            coll = self.db[collection]
            
            # Build query
            mongo_query = query or {}
            
            # Execute query
            cursor = coll.find(mongo_query)
            
            # Apply sort if specified
            if sort:
                cursor = cursor.sort(list(sort.items()))
            
            # Apply limit if specified
            if limit:
                cursor = cursor.limit(limit)
            
            # Convert cursor to list and serialize
            results = list(cursor)
            serialized_results = self._serialize_objectid(results)
            
            return json.dumps({
                "collection": collection,
                "query": mongo_query,
                "count": len(results),
                "results": serialized_results
            }, indent=2, default=str)
            
        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            return json.dumps({"error": str(e)})
        except Exception as e:
            logger.error(f"Error querying MongoDB: {e}")
            return json.dumps({"error": str(e)})
    
    def insert(self, collection: str, documents: List[Dict]) -> str:
        """
        Insert documents into MongoDB collection
        
        Args:
            collection: Collection name
            documents: Array of documents to insert
            
        Returns:
            JSON string with insert results
        """
        try:
            coll = self.db[collection]
            
            # Validate and normalize documents input
            if not documents:
                return json.dumps({"error": "Documents cannot be empty"})
            
            # Convert single document to list
            if isinstance(documents, dict):
                documents = [documents]
            elif not isinstance(documents, list):
                return json.dumps({"error": "Documents must be a dictionary or list of dictionaries"})
            
            # Validate all documents are dictionaries
            for i, doc in enumerate(documents):
                if not isinstance(doc, dict):
                    return json.dumps({"error": f"Document at index {i} is not a dictionary"})
            
            # Add timestamp to documents
            timestamp = datetime.utcnow()
            for doc in documents:
                doc['created_at'] = timestamp
                doc['updated_at'] = timestamp
            
            # Insert documents
            if len(documents) == 1:
                result = coll.insert_one(documents[0])
                inserted_ids = [str(result.inserted_id)]
            else:
                result = coll.insert_many(documents)
                inserted_ids = [str(id) for id in result.inserted_ids]
            
            return json.dumps({
                "collection": collection,
                "operation": "insert",
                "inserted_count": len(inserted_ids),
                "inserted_ids": inserted_ids,
                "acknowledged": result.acknowledged
            }, indent=2)
            
        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            return json.dumps({"error": str(e)})
        except Exception as e:
            logger.error(f"Error inserting into MongoDB: {e}")
            return json.dumps({"error": str(e)})
    
    def update(self, collection: str, filter: Dict[str, Any], update: Dict[str, Any], 
              upsert: bool = False) -> str:
        """
        Update documents in MongoDB collection
        
        Args:
            collection: Collection name
            filter: Filter to match documents
            update: Update operations
            upsert: Create if doesn't exist
            
        Returns:
            JSON string with update results
        """
        try:
            # Validate inputs
            if not collection or not isinstance(collection, str):
                return json.dumps({"error": "Collection name must be a non-empty string"})
            if not isinstance(filter, dict):
                return json.dumps({"error": "Filter must be a dictionary"})
            if not isinstance(update, dict):
                return json.dumps({"error": "Update must be a dictionary"})
            
            coll = self.db[collection]
            
            # Add timestamp to update
            update['$set'] = update.get('$set', {})
            update['$set']['updated_at'] = datetime.utcnow()
            
            # Execute update
            result = coll.update_many(filter, update, upsert=upsert)
            
            return json.dumps({
                "collection": collection,
                "operation": "update",
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_count": getattr(result, 'upserted_count', 0),
                "acknowledged": result.acknowledged
            }, indent=2)
            
        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            return json.dumps({"error": str(e)})
        except Exception as e:
            logger.error(f"Error updating MongoDB: {e}")
            return json.dumps({"error": str(e)})
    
    def delete(self, collection: str, filter: Dict[str, Any]) -> str:
        """
        Delete documents from MongoDB collection
        
        Args:
            collection: Collection name
            filter: Filter to match documents
            
        Returns:
            JSON string with delete results
        """
        try:
            # Validate inputs
            if not collection or not isinstance(collection, str):
                return json.dumps({"error": "Collection name must be a non-empty string"})
            if not isinstance(filter, dict):
                return json.dumps({"error": "Filter must be a dictionary"})
            
            coll = self.db[collection]
            
            # Execute delete
            result = coll.delete_many(filter)
            
            return json.dumps({
                "collection": collection,
                "operation": "delete",
                "deleted_count": result.deleted_count,
                "acknowledged": result.acknowledged
            }, indent=2)
            
        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            return json.dumps({"error": str(e)})
        except Exception as e:
            logger.error(f"Error deleting from MongoDB: {e}")
            return json.dumps({"error": str(e)})
    
    def aggregate(self, collection: str, pipeline: List[Dict[str, Any]]) -> str:
        """
        Perform aggregation pipeline on MongoDB collection
        
        Args:
            collection: Collection name
            pipeline: Aggregation pipeline stages
            
        Returns:
            JSON string with aggregation results
        """
        try:
            # Validate inputs
            if not collection or not isinstance(collection, str):
                return json.dumps({"error": "Collection name must be a non-empty string"})
            if not isinstance(pipeline, list):
                return json.dumps({"error": "Pipeline must be a list of aggregation stages"})
            
            coll = self.db[collection]
            
            # Execute aggregation
            cursor = coll.aggregate(pipeline)
            results = list(cursor)
            
            # Serialize results
            serialized_results = self._serialize_objectid(results)
            
            return json.dumps({
                "collection": collection,
                "operation": "aggregate",
                "pipeline": pipeline,
                "count": len(results),
                "results": serialized_results
            }, indent=2, default=str)
            
        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            return json.dumps({"error": str(e)})
        except Exception as e:
            logger.error(f"Error aggregating MongoDB: {e}")
            return json.dumps({"error": str(e)})
    
    def get_collections(self) -> str:
        """
        Get list of all collections in the database
        
        Returns:
            JSON string with collection names
        """
        try:
            collections = self.db.list_collection_names()
            
            return json.dumps({
                "database": self.database_name,
                "collections": collections,
                "count": len(collections)
            }, indent=2)
            
        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            return json.dumps({"error": str(e)})
        except Exception as e:
            logger.error(f"Error getting collections: {e}")
            return json.dumps({"error": str(e)})
    
    def get_collection_stats(self, collection: str) -> str:
        """
        Get statistics about a collection
        
        Args:
            collection: Collection name
            
        Returns:
            JSON string with collection statistics
        """
        try:
            coll = self.db[collection]
            
            # Get collection stats
            stats = self.db.command("collstats", collection)
            
            # Get document count
            count = coll.count_documents({})
            
            stats_data = {
                "collection": collection,
                "count": count,
                "size": stats.get("size", 0),
                "storageSize": stats.get("storageSize", 0),
                "avgObjSize": stats.get("avgObjSize", 0),
                "indexes": stats.get("nindexes", 0),
                "indexSizes": stats.get("indexSizes", {})
            }
            
            return json.dumps(stats_data, indent=2)
            
        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            return json.dumps({"error": str(e)})
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return json.dumps({"error": str(e)})
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed") 