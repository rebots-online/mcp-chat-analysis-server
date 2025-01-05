from typing import List, Dict, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class ConversationFormat(str, Enum):
    """Supported conversation import formats"""
    OPENAI_NATIVE = "openai_native"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"

class ConversationData(BaseModel):
    """Input schema for conversation import"""
    source_path: str = Field(
        description="Path to the chat export file"
    )
    format: ConversationFormat = Field(
        description="Format of the chat export"
    )
    metadata: Optional[Dict] = Field(
        default=None,
        description="Additional metadata for the import"
    )

class SearchFilter(BaseModel):
    """Filter criteria for semantic search"""
    field: str
    operator: str
    value: Union[str, int, float, bool, List]

class SearchQuery(BaseModel):
    """Input schema for semantic search"""
    query: str = Field(
        description="Search query text"
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results"
    )
    filters: Optional[List[SearchFilter]] = Field(
        default=None,
        description="Optional filters for search results"
    )
    min_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score"
    )

class MetricType(str, Enum):
    """Types of conversation metrics"""
    MESSAGE_FREQUENCY = "message_frequency"
    RESPONSE_TIMES = "response_times"
    TOPIC_DIVERSITY = "topic_diversity"
    CONVERSATION_DEPTH = "conversation_depth"
    INTERACTION_PATTERNS = "interaction_patterns"

class MetricsRequest(BaseModel):
    """Input schema for metrics analysis"""
    conversation_id: str = Field(
        description="ID of the conversation to analyze"
    )
    metrics: List[MetricType] = Field(
        description="Metrics to analyze"
    )
    time_window: Optional[str] = Field(
        default=None,
        description="Time window for analysis (e.g., '1d', '1w', '1m')"
    )

class ConceptRequest(BaseModel):
    """Input schema for concept extraction"""
    conversation_id: str = Field(
        description="ID of the conversation to analyze"
    )
    min_relevance: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score for concepts"
    )
    max_concepts: int = Field(
        default=10,
        ge=1,
        description="Maximum number of concepts to extract"
    )

class Message(BaseModel):
    """Chat message data model"""
    id: str
    content: str
    role: str
    timestamp: datetime
    parent_id: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)

class Conversation(BaseModel):
    """Conversation data model"""
    id: str
    title: Optional[str]
    messages: List[Message]
    create_time: datetime
    update_time: Optional[datetime]
    metadata: Dict = Field(default_factory=dict)

class SearchResult(BaseModel):
    """Semantic search result"""
    message: Message
    conversation: Conversation
    score: float
    context: Dict = Field(default_factory=dict)

class ConceptNode(BaseModel):
    """Extracted concept node"""
    id: str
    name: str
    relevance: float
    frequency: int
    first_occurrence: datetime
    last_occurrence: datetime
    related_concepts: List[str] = Field(default_factory=list)

class MetricsResult(BaseModel):
    """Conversation metrics result"""
    conversation_id: str
    time_window: Optional[str]
    metrics: Dict[MetricType, Dict]
    generated_at: datetime = Field(default_factory=datetime.now)