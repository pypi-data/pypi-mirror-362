"""
Comprehensive tests for embedding serialization control.

This test file covers all embedding serialization scenarios:
- Default Redis mode (embedding excluded)
- Redis mode with embedding included
- API mode (embedding always included)
- Edge cases and error conditions
- Migration from manual workarounds
"""

import pytest
import uuid
from datetime import datetime, timezone
from chunk_metadata_adapter.semantic_chunk import SemanticChunk
from chunk_metadata_adapter.chunk_query import ChunkQuery
from chunk_metadata_adapter.utils import to_flat_dict, from_flat_dict
from chunk_metadata_adapter.data_types import ChunkType, LanguageEnum, ChunkStatus


def valid_uuid():
    return str(uuid.uuid4())


class TestEmbeddingSerializationComprehensive:
    """Comprehensive tests for embedding serialization control."""

    def test_semantic_chunk_redis_mode_default(self):
        """Test SemanticChunk Redis mode - embedding excluded by default."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test chunk",
            text="Test chunk",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3, 0.4, 0.5]
        )
        
        # Default Redis mode - embedding should be excluded
        flat_dict = chunk.to_flat_dict()
        
        # Verify embedding is not present
        assert "embedding" not in flat_dict
        
        # Verify other fields are properly serialized
        assert flat_dict["uuid"] == chunk.uuid
        assert flat_dict["type"] == ChunkType.DOC_BLOCK.value
        assert flat_dict["body"] == "Test chunk"
        assert isinstance(flat_dict["created_at"], str)  # Auto-filled

    def test_semantic_chunk_redis_mode_explicit(self):
        """Test SemanticChunk Redis mode with explicit parameters."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test chunk",
            text="Test chunk",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3]
        )
        
        # Explicit Redis mode - embedding excluded
        flat_dict = chunk.to_flat_dict(for_redis=True, include_embedding=False)
        
        # Verify embedding is not present
        assert "embedding" not in flat_dict

    def test_semantic_chunk_redis_mode_with_embedding(self):
        """Test SemanticChunk Redis mode with embedding included."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test chunk",
            text="Test chunk",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3]
        )
        
        # Redis mode with embedding included
        flat_dict = chunk.to_flat_dict(for_redis=True, include_embedding=True)
        
        # Verify embedding is present as strings
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == ["0.1", "0.2", "0.3"]
        
        # Verify other fields are properly serialized
        assert flat_dict["uuid"] == chunk.uuid
        assert flat_dict["type"] == ChunkType.DOC_BLOCK.value

    def test_semantic_chunk_api_mode(self):
        """Test SemanticChunk API mode - embedding always included."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test chunk",
            text="Test chunk",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3]
        )
        
        # API mode - embedding should always be included
        flat_dict = chunk.to_flat_dict(for_redis=False)
        
        # Verify embedding is present as floats
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == [0.1, 0.2, 0.3]
        
        # Verify other fields remain in original types
        assert flat_dict["uuid"] == chunk.uuid
        assert flat_dict["type"] == ChunkType.DOC_BLOCK  # Enum object, not string
        assert flat_dict["body"] == "Test chunk"
        assert "created_at" not in flat_dict  # Not auto-filled in API mode

    def test_chunk_query_redis_mode_default(self):
        """Test ChunkQuery Redis mode - embedding excluded by default."""
        query = ChunkQuery(
            uuid=valid_uuid(),
            type="DocBlock",
            embedding=[0.1, 0.2, 0.3]
        )
        
        # Default Redis mode - embedding should be excluded
        flat_dict = query.to_flat_dict()
        
        # Verify embedding is not present
        assert "embedding" not in flat_dict
        
        # Verify other fields are properly serialized
        assert flat_dict["uuid"] == query.uuid
        assert flat_dict["type"] == "DocBlock"

    def test_chunk_query_redis_mode_with_embedding(self):
        """Test ChunkQuery Redis mode with embedding included."""
        query = ChunkQuery(
            uuid=valid_uuid(),
            type="DocBlock",
            embedding=[0.1, 0.2, 0.3]
        )
        
        # Redis mode with embedding included
        flat_dict = query.to_flat_dict(for_redis=True, include_embedding=True)
        
        # Verify embedding is present as strings
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == ["0.1", "0.2", "0.3"]

    def test_chunk_query_api_mode(self):
        """Test ChunkQuery API mode - embedding always included."""
        query = ChunkQuery(
            uuid=valid_uuid(),
            type="DocBlock",
            embedding=[0.1, 0.2, 0.3]
        )
        
        # API mode - embedding should always be included
        flat_dict = query.to_flat_dict(for_redis=False)
        
        # Verify embedding is present as floats
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == [0.1, 0.2, 0.3]

    def test_utils_to_flat_dict_redis_mode(self):
        """Test low-level to_flat_dict function in Redis mode."""
        data = {
            "uuid": valid_uuid(),
            "text": "Sample text",
            "embedding": [0.1, 0.2, 0.3, 0.4]
        }
        
        # Redis mode - embedding excluded
        flat_dict = to_flat_dict(data, for_redis=True)
        
        # Verify embedding is not present
        assert "embedding" not in flat_dict
        
        # Verify other fields are serialized to strings
        assert flat_dict["uuid"] == data["uuid"]
        assert flat_dict["text"] == "Sample text"
        assert "created_at" in flat_dict  # Auto-filled

    def test_utils_to_flat_dict_redis_mode_with_embedding(self):
        """Test low-level to_flat_dict function in Redis mode with embedding."""
        data = {
            "uuid": valid_uuid(),
            "text": "Sample text",
            "embedding": [0.1, 0.2, 0.3]
        }
        
        # Redis mode with embedding included
        flat_dict = to_flat_dict(data, for_redis=True, include_embedding=True)
        
        # Verify embedding is present as strings
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == ["0.1", "0.2", "0.3"]

    def test_utils_to_flat_dict_api_mode(self):
        """Test low-level to_flat_dict function in API mode."""
        data = {
            "uuid": valid_uuid(),
            "text": "Sample text",
            "embedding": [0.1, 0.2, 0.3]
        }
        
        # API mode - embedding included
        flat_dict = to_flat_dict(data, for_redis=False)
        
        # Verify embedding is present as floats
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == [0.1, 0.2, 0.3]
        
        # Verify other fields remain in original types
        assert flat_dict["uuid"] == data["uuid"]
        assert flat_dict["text"] == "Sample text"
        assert "created_at" not in flat_dict  # Not auto-filled

    def test_round_trip_redis_mode(self):
        """Test round-trip serialization in Redis mode."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test round trip",
            text="Test round trip",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3]
        )
        
        # Serialize to Redis format (embedding excluded)
        flat_dict = chunk.to_flat_dict(for_redis=True)
        assert "embedding" not in flat_dict
        
        # Deserialize back
        restored_chunk = SemanticChunk.from_flat_dict(flat_dict)
        
        # Verify chunk is restored correctly (without embedding)
        assert restored_chunk.uuid == chunk.uuid
        assert restored_chunk.body == chunk.body
        assert restored_chunk.type == chunk.type
        assert restored_chunk.embedding == []  # Default empty list

    def test_round_trip_api_mode(self):
        """Test round-trip serialization in API mode."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test round trip",
            text="Test round trip",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3]
        )
        
        # Serialize to API format (embedding included)
        flat_dict = chunk.to_flat_dict(for_redis=False)
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == [0.1, 0.2, 0.3]
        
        # Deserialize back
        restored_chunk = SemanticChunk.from_flat_dict(flat_dict)
        
        # Verify chunk is restored correctly (with embedding)
        assert restored_chunk.uuid == chunk.uuid
        assert restored_chunk.body == chunk.body
        assert restored_chunk.type == chunk.type
        assert restored_chunk.embedding == [0.1, 0.2, 0.3]

    def test_edge_cases_empty_embedding(self):
        """Test edge cases with empty or None embedding."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test edge cases",
            text="Test edge cases",
            type=ChunkType.DOC_BLOCK,
            embedding=[]  # Empty embedding
        )
        
        # Redis mode - empty embedding should be excluded
        flat_dict = chunk.to_flat_dict(for_redis=True)
        assert "embedding" not in flat_dict
        
        # API mode - empty embedding should be included
        flat_dict = chunk.to_flat_dict(for_redis=False)
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == []

    def test_edge_cases_none_embedding(self):
        """Test edge cases with None embedding."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test edge cases",
            text="Test edge cases",
            type=ChunkType.DOC_BLOCK,
            embedding=None  # None embedding
        )
        
        # Redis mode - None embedding should be excluded
        flat_dict = chunk.to_flat_dict(for_redis=True)
        assert "embedding" not in flat_dict
        
        # API mode - None embedding should be excluded (None values are excluded)
        flat_dict = chunk.to_flat_dict(for_redis=False)
        assert "embedding" not in flat_dict

    def test_migration_from_manual_workaround(self):
        """Test migration from manual workaround to clean API."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test migration",
            text="Test migration",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3]
        )
        
        # Old approach (manual workaround)
        chunk_dict_old = chunk.model_dump()
        if 'embedding' in chunk_dict_old:
            del chunk_dict_old['embedding']
        
        # New approach (clean API)
        chunk_dict_new = chunk.to_flat_dict(for_redis=True)
        
        # Both should have embedding excluded
        assert "embedding" not in chunk_dict_old
        assert "embedding" not in chunk_dict_new
        
        # Both should have other fields
        assert chunk_dict_old["uuid"] == chunk.uuid
        assert chunk_dict_new["uuid"] == chunk.uuid

    def test_performance_comparison(self):
        """Test that Redis mode is faster than API mode."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test performance",
            text="Test performance",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1] * 1536  # Large embedding vector
        )
        
        import time
        
        # Measure Redis mode performance
        start_time = time.time()
        for _ in range(100):
            chunk.to_flat_dict(for_redis=True)
        redis_time = time.time() - start_time
        
        # Measure API mode performance
        start_time = time.time()
        for _ in range(100):
            chunk.to_flat_dict(for_redis=False)
        api_time = time.time() - start_time
        
        # Redis mode should be faster (embedding excluded)
        assert redis_time < api_time, f"Redis mode ({redis_time:.4f}s) should be faster than API mode ({api_time:.4f}s)"

    def test_consistency_across_methods(self):
        """Test consistency across different serialization methods."""
        chunk = SemanticChunk(
            uuid=valid_uuid(),
            source_id=valid_uuid(),
            body="Test consistency",
            text="Test consistency",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3]
        )
        
        # Test consistency between SemanticChunk.to_flat_dict and utils.to_flat_dict
        chunk_flat = chunk.to_flat_dict(for_redis=True, include_embedding=True)
        utils_flat = to_flat_dict(chunk.model_dump(), for_redis=True, include_embedding=True)
        
        # Both should produce the same result (excluding created_at which has timestamp)
        chunk_flat_no_time = {k: v for k, v in chunk_flat.items() if k != 'created_at'}
        utils_flat_no_time = {k: v for k, v in utils_flat.items() if k != 'created_at'}
        assert chunk_flat_no_time == utils_flat_no_time
        
        # Both should have created_at field
        assert 'created_at' in chunk_flat
        assert 'created_at' in utils_flat

    def test_error_handling(self):
        """Test error handling for invalid embedding data."""
        # Test with invalid embedding data using model_dump to bypass validation
        chunk_data = {
            "uuid": valid_uuid(),
            "source_id": valid_uuid(),
            "body": "Test error handling",
            "text": "Test error handling",
            "type": ChunkType.DOC_BLOCK,
            "embedding": "invalid_embedding"  # Invalid type
        }
        
        # Should handle gracefully in Redis mode
        flat_dict = to_flat_dict(chunk_data, for_redis=True)
        assert "embedding" not in flat_dict
        
        # Should handle gracefully in API mode
        flat_dict = to_flat_dict(chunk_data, for_redis=False)
        assert "embedding" in flat_dict
        assert flat_dict["embedding"] == "invalid_embedding"

    def test_documentation_examples(self):
        """Test that documentation examples work correctly."""
        # Example from documentation
        chunk = SemanticChunk(
            uuid="12345678-1234-4123-8123-123456789012",
            source_id=valid_uuid(),
            body="Sample text",
            text="Sample text",
            type=ChunkType.DOC_BLOCK,
            embedding=[0.1, 0.2, 0.3, 0.4]
        )
        
        # Redis storage (default) - embedding excluded
        redis_dict = chunk.to_flat_dict()
        assert "embedding" not in redis_dict
        
        # Redis storage with embedding included
        redis_dict_with_emb = chunk.to_flat_dict(include_embedding=True)
        assert redis_dict_with_emb["embedding"] == ["0.1", "0.2", "0.3", "0.4"]
        
        # API response - embedding included as floats
        api_dict = chunk.to_flat_dict(for_redis=False)
        assert api_dict["embedding"] == [0.1, 0.2, 0.3, 0.4] 