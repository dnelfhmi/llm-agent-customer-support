from embedding_utils import get_embedding

def test_get_embedding_shape():
    text = "Test embedding"
    embedding = get_embedding(text)
    assert isinstance(embedding, list)
    assert len(embedding) == 1536  # For ada-002
