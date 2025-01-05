#!/usr/bin/env python3
from typing import Dict, Any, List, Optional
import asyncio
import os
from pathlib import Path
import logging
from datetime import datetime

from modelcontextprotocol import Server, StdioServerTransport
from modelcontextprotocol.types import (
    CallToolRequestSchema,
    ErrorCode,
    ListToolsRequestSchema,
    McpError,
)
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from neo4j import AsyncGraphDatabase

from .models import ConversationData, SearchQuery, MetricsRequest, ConceptRequest
from .processors import ConversationProcessor
from .embeddings import EmbeddingGenerator

logger = logging.getLogger(__name__)

class ChatAnalysisServer:
    """MCP server providing chat analysis capabilities"""
    
    def __init__(self):
        # Initialize MCP server
        self.server = Server(
            {
                "name": "mcp-server-chat-analysis",
                "version": "0.1.0",
            },
            {
                "capabilities": {
                    "tools": {},
                }
            }
        )
        
        # Load configuration from environment
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.embedding_model = os.getenv(
            "EMBEDDING_MODEL", 
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize components
        self._setup_clients()
        self._setup_tools()
        
        logger.info(f"Initialized ChatAnalysisServer with model: {self.embedding_model}")
    
    def _setup_clients(self):
        """Initialize database clients and processors"""
        # Initialize Qdrant client
        self.qdrant = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key
        )
        
        # Initialize Neo4j driver
        self.neo4j = AsyncGraphDatabase.driver(
            self.neo4j_url,
            auth=(self.neo4j_user, self.neo4j_password)
        )
        
        # Initialize embedding model
        self.embedding_generator = EmbeddingGenerator(
            model_name=self.embedding_model
        )
        
        # Initialize processor
        self.processor = ConversationProcessor(
            qdrant=self.qdrant,
            neo4j=self.neo4j,
            embedding_generator=self.embedding_generator
        )
    
    def _setup_tools(self):
        """Set up MCP tools"""
        self.server.set_request_handler(
            ListToolsRequestSchema, 
            self._handle_list_tools
        )
        self.server.set_request_handler(
            CallToolRequestSchema,
            self._handle_call_tool
        )
    
    async def _handle_list_tools(self, _):
        """Handle tool listing request"""
        return {
            "tools": [
                {
                    "name": "import_conversations",
                    "description": "Import and analyze chat conversations",
                    "inputSchema": ConversationData.schema()
                },
                {
                    "name": "semantic_search",
                    "description": "Search conversations by semantic similarity",
                    "inputSchema": SearchQuery.schema()
                },
                {
                    "name": "analyze_metrics",
                    "description": "Analyze conversation metrics",
                    "inputSchema": MetricsRequest.schema()
                },
                {
                    "name": "extract_concepts",
                    "description": "Extract and analyze concepts from conversations",
                    "inputSchema": ConceptRequest.schema()
                }
            ]
        }
    
    async def _handle_call_tool(self, request):
        """Handle tool execution request"""
        try:
            if request.params.name == "import_conversations":
                return await self._import_conversations(request.params.arguments)
            elif request.params.name == "semantic_search":
                return await self._semantic_search(request.params.arguments)
            elif request.params.name == "analyze_metrics":
                return await self._analyze_metrics(request.params.arguments)
            elif request.params.name == "extract_concepts":
                return await self._extract_concepts(request.params.arguments)
            else:
                raise McpError(
                    ErrorCode.MethodNotFound,
                    f"Unknown tool: {request.params.name}"
                )
        except Exception as e:
            logger.error(f"Error handling tool {request.params.name}: {e}")
            raise McpError(ErrorCode.InternalError, str(e))
    
    async def _import_conversations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Import and process conversations"""
        data = ConversationData(**args)
        stats = await self.processor.process_conversations(data)
        return {
            "content": [{
                "type": "text",
                "text": f"Imported conversations:\n{stats}"
            }]
        }
    
    async def _semantic_search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Perform semantic search"""
        query = SearchQuery(**args)
        results = await self.processor.search(query)
        return {
            "content": [{
                "type": "text",
                "text": f"Search results:\n{results}"
            }]
        }
    
    async def _analyze_metrics(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze conversation metrics"""
        request = MetricsRequest(**args)
        metrics = await self.processor.analyze_metrics(request)
        return {
            "content": [{
                "type": "text",
                "text": f"Metrics analysis:\n{metrics}"
            }]
        }
    
    async def _extract_concepts(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and analyze concepts"""
        request = ConceptRequest(**args)
        concepts = await self.processor.extract_concepts(request)
        return {
            "content": [{
                "type": "text",
                "text": f"Extracted concepts:\n{concepts}"
            }]
        }
    
    async def run(self):
        """Run the MCP server"""
        transport = StdioServerTransport()
        await self.server.connect(transport)
        logger.info("Chat Analysis MCP server running on stdio")

def main():
    """Entry point for the MCP server"""
    # Configure logging
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run server
    server = ChatAnalysisServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()