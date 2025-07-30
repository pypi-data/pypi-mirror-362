import pytest
from chunk_metadata_adapter.semantic_chunk import SemanticChunk, ChunkMetrics
import uuid
from chunk_metadata_adapter.data_types import ChunkType, LanguageEnum
from pydantic import ValidationError

def valid_uuid():
    return str(uuid.uuid4())

def test_get_default_prop_val_error():
    with pytest.raises(ValueError):
        SemanticChunk.get_default_prop_val("not_exist")

def test_source_lines_property_and_setter():
    chunk = SemanticChunk(
        uuid=str(uuid.uuid4()),
        source_id=str(uuid.uuid4()),
        type=ChunkType.DOC_BLOCK,
        body="b",
        text="b",
        language=LanguageEnum.EN,
        start=0,
        end=1
    )
    # По умолчанию None
    assert chunk.source_lines is None
    # Установка
    chunk.source_lines = [10, 20]
    assert chunk.source_lines == [10, 20]
    # Некорректная установка
    chunk.source_lines = [1]
    assert chunk.source_lines is None
    chunk.source_lines = None
    assert chunk.source_lines is None

def test_to_flat_dict_empty_fields():
    data = dict(body="b", type="DocBlock", language="en", start=0, end=1, project="p", task_id=valid_uuid(), subtask_id=valid_uuid(), unit_id=valid_uuid(), chunk_uuid=valid_uuid())
    chunk, err = SemanticChunk.validate_and_fill(data)
    assert err is None
    d = chunk.to_flat_dict(for_redis=False)
    print(f"[test_to_flat_dict_empty_fields] d: {d}")
    assert "tags" in d and d["tags"] == []
    assert "links" in d and d["links"] == []
    assert "link_parent" in d and d["link_parent"] == ""
    assert "link_related" in d and d["link_related"] == ""
    assert "source_lines_start" in d and d["source_lines_start"] == 0
    assert "source_lines_end" in d and d["source_lines_end"] == 0

def test_from_flat_dict_empty_fields():
    d = {"body": "b", "type": "DocBlock", "language": "en", "start": 0, "end": 1, "project": "p", "task_id": valid_uuid(), "subtask_id": valid_uuid(), "unit_id": valid_uuid(), "chunk_uuid": valid_uuid()}
    chunk, err = SemanticChunk.validate_and_fill(d)
    assert err is None
    assert chunk.tags == []
    assert chunk.links == []
    assert chunk.source_lines in (None, [0,0], [1,0])
    from chunk_metadata_adapter.semantic_chunk import ChunkMetrics
    assert chunk.metrics is None or isinstance(chunk.metrics, ChunkMetrics)

def test_validate_metadata_type_error():
    with pytest.raises(ValidationError):
        SemanticChunk(
            uuid=str(uuid.uuid4()),
            source_id=str(uuid.uuid4()),
            type=ChunkType.DOC_BLOCK,
            body="b",
            text="b",
            language=LanguageEnum.EN,
            tags="notalist",
            start=0,
            end=1
        )

def test_fill_text_from_body_autofill():
    values = {"body": "abc", "text": None}
    out = SemanticChunk.fill_text_from_body(values)
    assert out["text"] == "abc"

def test_validate_and_fill_error():
    # Ошибка: невалидный type (validate_and_fill автозаполняет DocBlock)
    data = {"type": "notatype", "body": "b", "language": "en", "start": 0, "end": 1}
    chunk, err = SemanticChunk.validate_and_fill(data)
    assert chunk is not None
    assert chunk.type == "DocBlock"

def test_model_post_init_else():
    # metrics = None, но есть поля для ChunkMetrics
    data = dict(body="b", type="DocBlock", language="en", start=0, end=1, project="p", task_id=str(uuid.uuid4()), subtask_id=str(uuid.uuid4()), unit_id=str(uuid.uuid4()), uuid=str(uuid.uuid4()), quality_score=0.5, used_in_generation=False)
    chunk, err = SemanticChunk.validate_and_fill(data)
    assert err is None
    from chunk_metadata_adapter.semantic_chunk import ChunkMetrics
    assert isinstance(chunk.metrics, ChunkMetrics)
    # source_lines есть, но невалидные
    data = dict(body="b", type="DocBlock", language="en", start=0, end=1, project="p", task_id=str(uuid.uuid4()), subtask_id=str(uuid.uuid4()), unit_id=str(uuid.uuid4()), uuid=str(uuid.uuid4()), source_lines_start=1, used_in_generation=False)
    chunk, err = SemanticChunk.validate_and_fill(data)
    assert err is None

def test_validate_sha256():
    from chunk_metadata_adapter.semantic_chunk import SemanticChunk
    # Валидный
    assert SemanticChunk.validate_sha256("a"*64) == "a"*64
    # Не валидный
    with pytest.raises(ValueError):
        SemanticChunk.validate_sha256("badsha256")

def test_validate_created_at():
    from chunk_metadata_adapter.semantic_chunk import SemanticChunk
    import datetime
    # Валидный
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    assert SemanticChunk.validate_created_at(now) == now
    # Не валидный
    with pytest.raises(ValueError):
        SemanticChunk.validate_created_at("notadate")

def test_validate_embedding():
    from chunk_metadata_adapter.semantic_chunk import SemanticChunk
    # Валидный
    assert SemanticChunk.validate_embedding([1,2,3]) == [1,2,3]
    # Не валидный
    with pytest.raises(ValueError):
        SemanticChunk.validate_embedding(123) 

def test_from_flat_dict_invalid_list():
    # tags как невалидная строка (не список, не csv) — теперь должен превращаться в список с этой строкой
    data = {"body": "b", "type": "DocBlock", "language": "en", "tags": "[notalist]", "start": 0, "end": 1}
    chunk = SemanticChunk.from_flat_dict(data)
    assert chunk.tags == ["[notalist]"]

def test_from_flat_dict_invalid_block_meta():
    # block_meta как невалидная строка
    data = {"body": "b", "type": "DocBlock", "language": "en", "block_meta": "notadict", "start": 0, "end": 1}
    with pytest.raises(Exception):
        SemanticChunk.from_flat_dict(data)

def test_validate_and_fill_invalid_enum():
    # Некорректный Enum
    data = {"body": "b", "type": "notatype", "language": "en", "start": 0, "end": 1}
    chunk, err = SemanticChunk.validate_and_fill(data)
    assert chunk is not None
    assert chunk.type == "DocBlock" or chunk.type == SemanticChunk.model_fields["type"].default

def test_validate_and_fill_invalid_chunkid():
    # Некорректный UUID
    data = {"body": "b", "type": "DocBlock", "language": "en", "uuid": "notauuid", "start": 0, "end": 1}
    with pytest.raises(Exception):
        SemanticChunk(**data)

def test_model_post_init_metrics_dict():
    # metrics как dict
    data = {"body": "b", "type": "DocBlock", "language": "en", "metrics": {"quality_score": 0.5}, "start": 0, "end": 1}
    chunk = SemanticChunk(**data)
    assert isinstance(chunk.metrics, ChunkMetrics)

def test_model_post_init_source_lines_list():
    # source_lines как список
    data = {"body": "b", "type": "DocBlock", "language": "en", "source_lines": [1, 2], "start": 0, "end": 1}
    chunk = SemanticChunk(**data)
    assert chunk.source_lines == [1, 2]

def test_model_post_init_is_code_chunk_autofill():
    # is_code_chunk не задано, должен вычисляться автоматически
    data = {"body": "b", "type": "DocBlock", "language": "en", "start": 0, "end": 1}
    chunk = SemanticChunk(**data)
    assert chunk.is_code_chunk is not None

def test_field_validators_errors():
    # sha256 невалидный
    from chunk_metadata_adapter.semantic_chunk import SemanticChunk
    with pytest.raises(ValueError):
        SemanticChunk.validate_sha256("badsha256")
    # created_at невалидный
    with pytest.raises(ValueError):
        SemanticChunk.validate_created_at("notadate")
    # embedding невалидный
    with pytest.raises(ValueError):
        SemanticChunk.validate_embedding(123)
    # uuid невалидный
    with pytest.raises(Exception):
        SemanticChunk.validate_chunkid_fields("notauuid") 