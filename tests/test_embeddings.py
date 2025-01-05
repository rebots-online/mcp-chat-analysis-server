import pytest
import numpy as np
from mcp_chat_analysis.embeddings import EmbeddingGenerator

@pytest.fixture
def embedding_generator():
    return EmbeddingGenerator(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        device="cpu",
        batch_size=2
    )

@pytest.mark.asyncio
async def test_single_embedding_generation(embedding_generator):
    text = "This is a test message"
    embedding = await embedding_generator.generate_single(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == embedding_generator.embedding_dim
    assert all(isinstance(x, float) for x in embedding)

@pytest.mark.asyncio
async def test_batch_embedding_generation(embedding_generator):
    texts = [
        "First test message",
        "Second test message",
        "Third test message"
    ]
    embeddings = await embedding_generator.generate(texts)
    
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(texts)
    assert all(len(emb) == embedding_generator.embedding_dim for emb in embeddings)

@pytest.mark.asyncio
async def test_similarity_computation(embedding_generator):
    text1 = "This is about artificial intelligence"
    text2 = "AI and machine learning are related topics"
    text3 = "The weather is nice today"
    
    # Similar texts should have higher similarity
    sim1 = await embedding_generator.compute_similarity(text1, text2)
    sim2 = await embedding_generator.compute_similarity(text1, text3)
    
    assert 0 <= sim1 <= 1
    assert 0 <= sim2 <= 1
    assert sim1 > sim2  # Related topics should be more similar

@pytest.mark.asyncio
async def test_similar_chunks_finding(embedding_generator):
    query = "artificial intelligence"
    texts = [
        "AI and machine learning",
        "Natural language processing",
        "The weather forecast",
        "Today's temperature",
        "Deep learning algorithms"
    ]
    
    results = await embedding_generator.find_similar_chunks(
        query,
        texts,
        threshold=0.3,
        top_k=3
    )
    
    assert isinstance(results, list)
    assert len(results) <= 3
    assert all("score" in r and "text" in r for r in results)
    assert all(0 <= r["score"] <= 1 for r in results)
    
    # Check ordering
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)

@pytest.mark.asyncio
async def test_long_text_handling(embedding_generator):
    long_text = "a" * 1000  # Text longer than max_length
    embedding = await embedding_generator.generate_single(long_text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == embedding_generator.embedding_dim

@pytest.mark.asyncio
async def test_empty_text_handling(embedding_generator):
    empty_text = ""
    embedding = await embedding_generator.generate_single(empty_text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == embedding_generator.embedding_dim

@pytest.mark.asyncio
async def test_different_similarity_methods(embedding_generator):
    text1 = "This is a test"
    text2 = "Another test message"
    
    cosine_sim = await embedding_generator.compute_similarity(
        text1,
        text2,
        method="cosine"
    )
    euclidean_sim = await embedding_generator.compute_similarity(
        text1,
        text2,
        method="euclidean"
    )
    
    assert 0 <= cosine_sim <= 1
    assert 0 <= euclidean_sim <= 1

@pytest.mark.asyncio
async def test_invalid_similarity_method(embedding_generator):
    with pytest.raises(ValueError):
        await embedding_generator.compute_similarity(
            "text1",
            "text2",
            method="invalid"
        )