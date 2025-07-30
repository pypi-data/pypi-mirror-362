import pytest
import json
from unittest.mock import patch, MagicMock
from llm_togetherai import get_together_models, fetch_cached_json, refresh_models


def test_get_together_models():
    """Test that get_together_models returns a list of models"""
    with patch('llm_togetherai.fetch_cached_json') as mock_fetch:
        mock_fetch.return_value = [
            {
                "id": "test-model",
                "display_name": "Test Model",
                "type": "chat",
                "context_length": 4096,
                "organization": "Test Org"
            }
        ]
        
        models = get_together_models()
        assert isinstance(models, list)
        assert len(models) == 1
        assert models[0]["id"] == "test-model"


def test_fetch_cached_json_with_cache():
    """Test fetch_cached_json when cache is valid"""
    with patch('llm_togetherai.Path') as mock_path, \
         patch('llm_togetherai.time.time') as mock_time, \
         patch('builtins.open', create=True) as mock_open:
        
        # Mock path operations
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.is_file.return_value = True
        mock_path_instance.stat.return_value.st_mtime = 1000
        mock_path_instance.parent.mkdir = MagicMock()
        
        # Mock time to make cache valid
        mock_time.return_value = 2000  # Cache is 1000 seconds old, timeout is 3600
        
        # Mock file content
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_open.return_value = mock_file
        
        test_data = [{"id": "test-model"}]
        with patch('json.load', return_value=test_data):
            result = fetch_cached_json("http://test.com", "/test/path", 3600)
            assert result == test_data


def test_fetch_cached_json_api_call():
    """Test fetch_cached_json when making API call"""
    with patch('llm_togetherai.Path') as mock_path, \
         patch('llm_togetherai.httpx.get') as mock_get, \
         patch('llm_togetherai.llm.get_key') as mock_get_key, \
         patch('builtins.open', create=True) as mock_open:
        
        # Mock path operations
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.is_file.return_value = False
        mock_path_instance.parent.mkdir = MagicMock()
        
        # Mock API key
        mock_get_key.return_value = "test-key"
        
        # Mock HTTP response
        mock_response = MagicMock()
        test_data = [{"id": "test-model"}]
        mock_response.json.return_value = test_data
        mock_get.return_value = mock_response
        
        # Mock file operations
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_open.return_value = mock_file
        
        with patch('json.dump') as mock_dump:
            result = fetch_cached_json("http://test.com", "/test/path", 3600)
            assert result == test_data
            mock_dump.assert_called_once()


def test_refresh_models():
    """Test refresh_models function"""
    with patch('llm_togetherai.llm.get_key') as mock_get_key, \
         patch('llm_togetherai.httpx.get') as mock_get, \
         patch('llm_togetherai.Path') as mock_path, \
         patch('builtins.open', create=True) as mock_open, \
         patch('llm_togetherai.click.echo') as mock_echo:
        
        # Mock API key
        mock_get_key.return_value = "test-key"
        
        # Mock path operations
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.parent.mkdir = MagicMock()
        
        # Mock HTTP response
        mock_response = MagicMock()
        test_data = [{"id": "test-model"}]
        mock_response.json.return_value = test_data
        mock_get.return_value = mock_response
        
        # Mock file operations
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_open.return_value = mock_file
        
        with patch('json.dump') as mock_dump:
            refresh_models()
            mock_echo.assert_called()
            mock_dump.assert_called_once()


def test_refresh_models_no_key():
    """Test refresh_models when no API key is available"""
    with patch('llm_togetherai.llm.get_key') as mock_get_key:
        mock_get_key.return_value = None
        
        with pytest.raises(Exception):  # Should raise ClickException
            refresh_models()


if __name__ == "__main__":
    pytest.main([__file__])