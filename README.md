# MCP Chat Analysis Server

A Model Context Protocol (MCP) server that enables semantic analysis of chat conversations through vector embeddings and knowledge graphs. This server provides tools for analyzing chat data, performing semantic search, extracting concepts, and analyzing conversation patterns.

## Key Features

- 🔍 **Semantic Search**: Find relevant messages and conversations using vector similarity
- 🕸️ **Knowledge Graph**: Navigate relationships between messages, concepts, and topics
- 📊 **Conversation Analytics**: Analyze patterns, metrics, and conversation dynamics
- 🔄 **Flexible Import**: Support for various chat export formats
- 🚀 **MCP Integration**: Easy integration with Claude and other MCP-compatible systems

## Quick Start

```bash
# Install the package
pip install mcp-chat-analysis-server

# Set up configuration
cp config.example.yml config.yml
# Edit config.yml with your database settings

# Run the server
python -m mcp_chat_analysis.server
```

## MCP Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chat-analysis": {
      "command": "python",
      "args": ["-m", "mcp_chat_analysis.server"],
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

## Available Tools

### import_conversations
Import and analyze chat conversations
```python
{
    "source_path": "/path/to/export.zip",
    "format": "openai_native"  # or html, markdown, json
}
```

### semantic_search
Search conversations by semantic similarity
```python
{
    "query": "machine learning applications",
    "limit": 10,
    "min_score": 0.7
}
```

### analyze_metrics
Analyze conversation metrics
```python
{
    "conversation_id": "conv-123",
    "metrics": [
        "message_frequency",
        "response_times",
        "topic_diversity"
    ]
}
```

### extract_concepts
Extract and analyze concepts
```python
{
    "conversation_id": "conv-123",
    "min_relevance": 0.5,
    "max_concepts": 10
}
```

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed diagrams and documentation of:
- System components and interactions
- Data flow and processing pipeline
- Storage schema and vector operations
- Tool integration mechanism

## Prerequisites

- Python 3.8+
- Neo4j database for knowledge graph storage
- Qdrant vector database for semantic search
- sentence-transformers for embeddings

## Installation

1. Install the package:
```bash
pip install mcp-chat-analysis-server
```

2. Set up databases:
```bash
# Using Docker (recommended)
docker compose up -d
```

3. Configure the server:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/rebots-online/mcp-chat-analysis-server.git
cd mcp-chat-analysis-server
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Related Projects

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Claude Desktop](https://github.com/anthropics/claude-desktop)
- [Qdrant Vector Database](https://qdrant.tech/)
- [Neo4j Graph Database](https://neo4j.com/)

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/rebots-online/mcp-chat-analysis-server/issues)
- 💬 [Discussions](https://github.com/rebots-online/mcp-chat-analysis-server/discussions)