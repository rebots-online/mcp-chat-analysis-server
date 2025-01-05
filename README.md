# MCP Chat Analysis Server

A Model Context Protocol (MCP) server that provides chat analysis capabilities through vector embeddings and knowledge graph operations. This server can be used to analyze chat conversations, perform semantic search, extract concepts, and analyze conversation metrics.

## Features

- Semantic analysis of chat conversations
- Vector embeddings for similarity search
- Knowledge graph operations
- Conversation metrics analysis
- Concept extraction and relationship mapping

## Tools

### import_conversations
Import and analyze chat conversations
- Input:
  - source_path: Path to chat export file
  - format: Export format (openai_native, html, markdown, json)

### semantic_search
Search conversations by semantic similarity
- Input:
  - query: Search query text
  - limit: Maximum number of results (default: 10)
  - filters: Optional result filters

### analyze_metrics
Analyze conversation metrics
- Input:
  - conversation_id: ID of conversation to analyze
  - metrics: Array of metrics to analyze
    - message_frequency
    - response_times
    - topic_diversity
    - conversation_depth
    - interaction_patterns

### extract_concepts
Extract and analyze concepts from conversations
- Input:
  - conversation_id: ID of conversation to analyze
  - min_relevance: Minimum relevance score (0-1, default: 0.5)

## Installation

```bash
# Using uv (recommended)
uv pip install mcp-server-chat-analysis

# Using pip
pip install mcp-server-chat-analysis
```

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chat-analysis": {
      "command": "mcp-server-chat-analysis",
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "NEO4J_URL": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "your-password"
      }
    }
  }
}
```

## Environment Variables

- `QDRANT_URL`: URL of Qdrant vector database
- `QDRANT_API_KEY`: Optional API key for Qdrant
- `NEO4J_URL`: URL of Neo4j database
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `EMBEDDING_MODEL`: Name of sentence transformer model (default: "sentence-transformers/all-MiniLM-L6-v2")
- `LOG_LEVEL`: Logging level (default: "INFO")

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest tests/
   ```

## Architecture

The server is built with a modular architecture:

```
mcp-server-chat-analysis/
├── src/
│   └── mcp_chat_analysis/
│       ├── server.py          # MCP server implementation
│       ├── tools/             # Tool implementations
│       ├── processors/        # Data processors
│       ├── embeddings/        # Vector embedding handlers
│       ├── graph/            # Knowledge graph operations
│       └── models/           # Data models
├── tests/                    # Test suite
└── examples/                 # Usage examples
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details