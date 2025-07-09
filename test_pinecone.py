from unittest.mock import patch

def test_query_kb_returns_expected_text():
    with patch('pinecone_utils.get_embedding', return_value=[0.1]*1536), \
         patch('pinecone_utils.index') as mock_index:
        mock_index.query.return_value = {
            'matches': [{'metadata': {'text': 'expected result'}}]
        }
        from pinecone_utils import query_kb
        result = query_kb("test description")
        assert result == ['expected result']
