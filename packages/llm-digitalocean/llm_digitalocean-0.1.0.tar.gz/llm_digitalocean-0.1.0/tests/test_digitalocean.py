import pytest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock
from pathlib import Path
import llm_digitalocean


def test_get_headers_missing_key():
    """Test that missing API key raises ClickException"""
    with patch('llm.get_key', return_value=None):
        with pytest.raises(Exception):  # ClickException
            llm_digitalocean.get_headers()


@patch('llm.get_key')
def test_get_headers_success(mock_get_key):
    """Test successful header generation"""
    mock_get_key.return_value = "test-api-key"
    headers = llm_digitalocean.get_headers()
    
    assert headers["Authorization"] == "Bearer test-api-key"
    assert headers["Content-Type"] == "application/json"
    assert "HTTP-Referer" in headers
    assert "X-Title" in headers


@patch('llm_digitalocean.fetch_cached_json')
@patch('llm_digitalocean.get_headers')
def test_get_digitalocean_models(mock_get_headers, mock_fetch):
    """Test model retrieval"""
    mock_get_headers.return_value = {"Authorization": "Bearer test-key"}
    mock_fetch.return_value = {
        'data': [
            {
                'id': 'test-model-1',
                'object': 'model',
                'created': 1234567890,
                'owned_by': 'digitalocean'
            },
            {
                'id': 'test-model-2',
                'object': 'model',
                'created': 1234567891,
                'owned_by': 'digitalocean'
            }
        ]
    }
    
    models = llm_digitalocean.get_digitalocean_models()
    
    assert len(models) == 2
    assert models[0]['id'] == 'test-model-1'
    assert models[1]['id'] == 'test-model-2'
    # Check that additional metadata was added
    assert 'supports_schema' in models[0]
    assert 'supports_vision' in models[0]


def test_fetch_cached_json_with_cache():
    """Test cached JSON retrieval with valid cache"""
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'test_cache.json'
        
        # Create a fresh cache file
        test_data = {'data': [{'id': 'test-model', 'name': 'Test Model'}]}
        with open(cache_file, 'w') as f:
            json.dump(test_data, f)
        
        # Mock time to make cache appear fresh
        with patch('time.time', return_value=cache_file.stat().st_mtime + 1800):  # 30 minutes later
            result = llm_digitalocean.fetch_cached_json(
                url="https://example.com/api",
                path=cache_file,
                cache_timeout=3600
            )
            
            assert result == test_data


@patch('httpx.get')
def test_fetch_cached_json_expired_cache(mock_get):
    """Test JSON retrieval with expired cache"""
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'test_cache.json'
        
        # Create an old cache file
        old_data = {'data': [{'id': 'old-model'}]}
        with open(cache_file, 'w') as f:
            json.dump(old_data, f)
        
        # Mock HTTP response
        new_data = {'data': [{'id': 'new-model'}]}
        mock_response = MagicMock()
        mock_response.json.return_value = new_data
        mock_get.return_value = mock_response
        
        # Mock time to make cache appear expired
        with patch('time.time', return_value=cache_file.stat().st_mtime + 7200):  # 2 hours later
            result = llm_digitalocean.fetch_cached_json(
                url="https://example.com/api",
                path=cache_file,
                cache_timeout=3600
            )
            
            assert result == new_data
            mock_get.assert_called_once()


def test_get_supports_images():
    """Test vision support detection"""
    # Test explicit vision support
    model_with_vision = {'supports_vision': True, 'id': 'test-model'}
    assert llm_digitalocean.get_supports_images(model_with_vision) == True
    
    # Test keyword detection
    model_with_vision_keyword = {'id': 'gpt-4o-vision-preview'}
    assert llm_digitalocean.get_supports_images(model_with_vision_keyword) == True
    
    # Test no vision support
    model_without_vision = {'id': 'text-model-basic'}
    assert llm_digitalocean.get_supports_images(model_without_vision) == False


def test_digitalocean_chat_str():
    """Test DigitalOceanChat string representation"""
    chat_model = llm_digitalocean.DigitalOceanChat(
        model_id="digitalocean/test-model",
        model_name="test-model",
        api_base="https://inference.do-ai.run/v1"
    )
    
    assert str(chat_model) == "DigitalOcean: digitalocean/test-model"


def test_digitalocean_async_chat_str():
    """Test DigitalOceanAsyncChat string representation"""
    async_chat_model = llm_digitalocean.DigitalOceanAsyncChat(
        model_id="digitalocean/test-model",
        model_name="test-model",
        api_base="https://inference.do-ai.run/v1"
    )
    
    assert str(async_chat_model) == "DigitalOcean: digitalocean/test-model"


@patch('llm.get_key')
@patch('llm_digitalocean.get_digitalocean_models')
def test_register_models_no_key(mock_get_models, mock_get_key):
    """Test that models are not registered without API key"""
    mock_get_key.return_value = None
    
    register_mock = MagicMock()
    llm_digitalocean.register_models(register_mock)
    
    # Should not call get_digitalocean_models or register anything
    mock_get_models.assert_not_called()
    register_mock.assert_not_called()


@patch('llm.get_key')
@patch('llm_digitalocean.get_digitalocean_models')
@patch('llm_digitalocean.get_headers')
def test_register_models_with_key(mock_get_headers, mock_get_models, mock_get_key):
    """Test that models are registered with valid API key"""
    mock_get_key.return_value = "test-key"
    mock_get_headers.return_value = {"Authorization": "Bearer test-key"}
    mock_get_models.return_value = [
        {
            'id': 'test-model',
            'supports_schema': False,
            'supports_vision': False
        }
    ]
    
    register_mock = MagicMock()
    llm_digitalocean.register_models(register_mock)
    
    # Should call register with both sync and async models
    assert register_mock.call_count == 1
    # Check that both models were passed to register
    call_args = register_mock.call_args[0]
    assert len(call_args) == 2  # sync and async models


if __name__ == "__main__":
    pytest.main([__file__])