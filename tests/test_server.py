import pytest
import json
from unittest.mock import Mock, AsyncMock
from pathlib import Path

from modelcontextprotocol.types import CallToolRequest, CallToolParams
from mcp_chat_analysis.server import ChatAnalysisServer
from mcp_chat_analysis.models import (
    ConversationFormat,
    ConversationData,
    SearchQuery,
    MetricsRequest,
    ConceptRequest,
    MetricType
)

@pytest.fixture
def mock_qdrant():
    return Mock()

@pytest.fixture
def mock_neo4j():
    return Mock()

@pytest.fixture
def mock_embedding_generator():
    generator = Mock()
    generator.generate_single = AsyncMock()
    generator.generate = AsyncMock()
    return generator

@pytest.fixture
async def server(mock_qdrant, mock_neo4j, mock_embedding_generator):
    server = ChatAnalysisServer()
    server.qdrant = mock_qdrant
    server.neo4j = mock_neo4j
    server.embedding_generator = mock_embedding_generator
    return server

@pytest.mark.asyncio
async def test_list_tools(server):
    """Test that the server correctly lists available tools"""
    result = await server._handle_list_tools(None)
    
    assert "tools" in result
    tools = result["tools"]
    assert len(tools) == 4
    
    tool_names = {tool["name"] for tool in tools}
    expected_names = {
        "import_conversations",
        "semantic_search",
        "analyze_metrics",
        "extract_concepts"
    }
    assert tool_names == expected_names

@pytest.mark.asyncio
async def test_import_conversations(server):
    """Test conversation import tool"""
    request = CallToolRequest(
        params=CallToolParams(
            name="import_conversations",
            arguments={
                "source_path": "/path/to/export.zip",
                "format": "openai_native"
            }
        )
    )
    
    # Mock processor response
    server.processor.process_conversations = AsyncMock(return_value={
        "conversations_processed": 1,
        "messages_processed": 10,
        "vectors_created": 10,
        "concepts_extracted": 5
    })
    
    result = await server._handle_call_tool(request)
    
    assert result["content"][0]["type"] == "text"
    assert "Imported conversations" in result["content"][0]["text"]
    assert server.processor.process_conversations.called

@pytest.mark.asyncio
async def test_semantic_search(server):
    """Test semantic search tool"""
    request = CallToolRequest(
        params=CallToolParams(
            name="semantic_search",
            arguments={
                "query": "test query",
                "limit": 5
            }
        )
    )
    
    # Mock search results
    server.processor.search = AsyncMock(return_value=[
        {
            "text": "Result 1",
            "score": 0.9
        }
    ])
    
    result = await server._handle_call_tool(request)
    
    assert result["content"][0]["type"] == "text"
    assert "Search results" in result["content"][0]["text"]
    assert server.processor.search.called

@pytest.mark.asyncio
async def test_analyze_metrics(server):
    """Test metrics analysis tool"""
    request = CallToolRequest(
        params=CallToolParams(
            name="analyze_metrics",
            arguments={
                "conversation_id": "test-id",
                "metrics": ["message_frequency", "response_times"]
            }
        )
    )
    
    # Mock metrics results
    server.processor.analyze_metrics = AsyncMock(return_value={
        "message_frequency": {"avg": 5},
        "response_times": {"avg": 60}
    })
    
    result = await server._handle_call_tool(request)
    
    assert result["content"][0]["type"] == "text"
    assert "Metrics analysis" in result["content"][0]["text"]
    assert server.processor.analyze_metrics.called

@pytest.mark.asyncio
async def test_extract_concepts(server):
    """Test concept extraction tool"""
    request = CallToolRequest(
        params=CallToolParams(
            name="extract_concepts",
            arguments={
                "conversation_id": "test-id",
                "min_relevance": 0.5
            }
        )
    )
    
    # Mock concept extraction results
    server.processor.extract_concepts = AsyncMock(return_value=[
        {
            "name": "AI",
            "relevance": 0.9,
            "frequency": 5
        }
    ])
    
    result = await server._handle_call_tool(request)
    
    assert result["content"][0]["type"] == "text"
    assert "Extracted concepts" in result["content"][0]["text"]
    assert server.processor.extract_concepts.called

@pytest.mark.asyncio
async def test_invalid_tool(server):
    """Test handling of invalid tool requests"""
    request = CallToolRequest(
        params=CallToolParams(
            name="invalid_tool",
            arguments={}
        )
    )
    
    with pytest.raises(Exception) as exc:
        await server._handle_call_tool(request)
    assert "Unknown tool" in str(exc.value)

@pytest.mark.asyncio
async def test_invalid_arguments(server):
    """Test handling of invalid tool arguments"""
    request = CallToolRequest(
        params=CallToolParams(
            name="semantic_search",
            arguments={
                "invalid": "argument"
            }
        )
    )
    
    with pytest.raises(Exception):
        await server._handle_call_tool(request)