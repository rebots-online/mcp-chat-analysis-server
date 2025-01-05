# Architecture Documentation

## System Overview

```mermaid
graph TB
    Client[Client Application] -->|MCP Protocol| Server[Chat Analysis Server]
    Server -->|Vector Operations| Qdrant[Qdrant Vector DB]
    Server -->|Graph Operations| Neo4j[Neo4j Graph DB]
    Server -->|Embeddings| Model[Sentence Transformer]
    
    subgraph "Chat Analysis Server"
        Tools[MCP Tools] --> Processor[Conversation Processor]
        Processor --> Embeddings[Embedding Generator]
        Processor --> GraphOps[Graph Operations]
        Processor --> Analytics[Analytics Engine]
    end
```

## Component Architecture

```mermaid
classDiagram
    class ChatAnalysisServer {
        +QdrantClient qdrant
        +Neo4jDriver neo4j
        +EmbeddingGenerator embedding_generator
        +handle_list_tools()
        +handle_call_tool()
    }
    
    class ConversationProcessor {
        +process_conversations()
        +search()
        +analyze_metrics()
        +extract_concepts()
    }
    
    class EmbeddingGenerator {
        +generate()
        +generate_single()
        +compute_similarity()
        +find_similar_chunks()
    }
    
    class Message {
        +str id
        +str content
        +str role
        +datetime timestamp
        +Dict metadata
    }
    
    class ConversationThread {
        +str id
        +str title
        +Dict messages
        +str root_id
        +from_export_mapping()
        +traverse_messages()
    }
    
    ChatAnalysisServer --> ConversationProcessor
    ChatAnalysisServer --> EmbeddingGenerator
    ConversationProcessor --> EmbeddingGenerator
    ConversationProcessor ..> Message
    ConversationProcessor ..> ConversationThread
```

## Data Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server as Chat Analysis Server
    participant Embeddings as Embedding Generator
    participant Qdrant
    participant Neo4j
    
    Client->>Server: Import Conversations
    Server->>Embeddings: Generate Embeddings
    Embeddings-->>Server: Return Vectors
    Server->>Qdrant: Store Vectors
    Server->>Neo4j: Create Graph Structure
    Server-->>Client: Import Complete
    
    Client->>Server: Semantic Search
    Server->>Embeddings: Generate Query Vector
    Server->>Qdrant: Search Similar Vectors
    Server->>Neo4j: Get Context
    Server-->>Client: Search Results
    
    Client->>Server: Extract Concepts
    Server->>Neo4j: Query Graph Patterns
    Server->>Qdrant: Get Related Vectors
    Server-->>Client: Concept Analysis
```

## Storage Schema

### Vector Storage (Qdrant)

```mermaid
erDiagram
    VECTOR {
        string id
        vector embedding
        string message_id
        string conversation_id
        string role
        timestamp created_at
    }
    
    PAYLOAD {
        string message_id
        string content
        string role
        json metadata
    }
```

### Graph Storage (Neo4j)

```mermaid
erDiagram
    CONVERSATION ||--o{ MESSAGE : contains
    MESSAGE ||--o{ CONCEPT : mentions
    CONCEPT ||--o{ CONCEPT : related_to
    
    CONVERSATION {
        string id
        string title
        timestamp create_time
        timestamp update_time
    }
    
    MESSAGE {
        string id
        string content
        string role
        string vector_id
        timestamp timestamp
    }
    
    CONCEPT {
        string id
        string name
        float relevance
        int frequency
    }
```

## Processing Pipeline

```mermaid
graph LR
    Input[Chat Export] --> Parser[Format Parser]
    Parser --> Processor[Conversation Processor]
    
    subgraph "Processing Pipeline"
        Processor --> Embeddings[Generate Embeddings]
        Processor --> Graph[Create Graph Structure]
        Processor --> Concepts[Extract Concepts]
        
        Embeddings --> VectorStore[Store in Qdrant]
        Graph --> GraphStore[Store in Neo4j]
        Concepts --> Analysis[Analyze Relationships]
    end
    
    VectorStore --> Search[Semantic Search]
    GraphStore --> Navigation[Graph Navigation]
    Analysis --> Metrics[Generate Metrics]
```

## Tool Integration

```mermaid
graph TB
    MCP[MCP Protocol] --> Tools[Tool Registry]
    
    subgraph "Available Tools"
        Import[import_conversations]
        Search[semantic_search]
        Metrics[analyze_metrics]
        Concepts[extract_concepts]
    end
    
    Tools --> Import
    Tools --> Search
    Tools --> Metrics
    Tools --> Concepts
    
    Import --> Processor[Conversation Processor]
    Search --> Processor
    Metrics --> Processor
    Concepts --> Processor