import pytest
import json
from unittest.mock import patch, MagicMock
import llm_chutes


def test_import():
    """Test that the module can be imported successfully"""
    assert llm_chutes is not None


def test_get_supports_images():
    """Test the get_supports_images function"""
    # Test with explicit supports_vision field
    model_with_vision = {"id": "test-model", "supports_vision": True}
    assert llm_chutes.get_supports_images(model_with_vision) is True
    
    model_without_vision = {"id": "test-model", "supports_vision": False}
    assert llm_chutes.get_supports_images(model_without_vision) is False
    
    # Test with vision keywords in model ID
    model_with_vision_keyword = {"id": "gpt-4o-vision"}
    assert llm_chutes.get_supports_images(model_with_vision_keyword) is True
    
    model_without_vision_keyword = {"id": "gpt-3.5-turbo"}
    assert llm_chutes.get_supports_images(model_without_vision_keyword) is False


def test_format_price():
    """Test the format_price function"""
    # Test various price ranges
    assert llm_chutes.format_price("input", "0.001") == "input $1/K"
    assert llm_chutes.format_price("output", "0.002") == "output $2/K"
    assert llm_chutes.format_price("input", "0.00001") == "input $10/M"
    assert llm_chutes.format_price("input", "1.5") == "input $1.5"
    assert llm_chutes.format_price("input", "0") is None
    assert llm_chutes.format_price("input", "invalid") is None


def test_format_pricing():
    """Test the format_pricing function"""
    pricing_dict = {"input": "0.001", "output": "0.002"}
    result = llm_chutes.format_pricing(pricing_dict)
    assert "input $1/K" in result
    assert "output $2/K" in result
    
    empty_dict = {}
    assert llm_chutes.format_pricing(empty_dict) == ""


@patch('llm_chutes.httpx.get')
def test_fetch_cached_json_success(mock_get):
    """Test successful API fetch"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"id": "test-model"}]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    with patch('llm_chutes.llm.get_key', return_value="test-key"):
        with patch('builtins.open', create=True) as mock_open:
            with patch('llm_chutes.json.dump'):
                result = llm_chutes.fetch_cached_json(
                    "https://test.com/models",
                    "/tmp/test.json",
                    0  # Force fresh fetch
                )
                assert result == {"data": [{"id": "test-model"}]}


def test_chutes_chat_str():
    """Test ChutesChat string representation"""
    chat_model = llm_chutes.ChutesChat(model_id="test-model")
    assert str(chat_model) == "chutes: test-model"


def test_chutes_async_chat_str():
    """Test ChutesAsyncChat string representation"""
    async_chat_model = llm_chutes.ChutesAsyncChat(model_id="test-model")
    assert str(async_chat_model) == "chutes: test-model"


@patch('llm_chutes.get_chutes_models')
def test_get_chutes_models_empty(mock_get_models):
    """Test get_chutes_models with empty response"""
    mock_get_models.return_value = []
    result = llm_chutes.get_chutes_models()
    assert result == []


@patch('llm_chutes.fetch_cached_json')
def test_get_chutes_models_with_data(mock_fetch):
    """Test get_chutes_models with data response"""
    mock_fetch.return_value = {"data": [{"id": "model1"}, {"id": "model2"}]}
    result = llm_chutes.get_chutes_models()
    assert len(result) == 2
    assert result[0]["id"] == "model1"
    assert result[1]["id"] == "model2"


@patch('llm_chutes.fetch_cached_json')
def test_get_chutes_models_list_format(mock_fetch):
    """Test get_chutes_models with list response format"""
    mock_fetch.return_value = [{"id": "model1"}, {"id": "model2"}]
    result = llm_chutes.get_chutes_models()
    assert len(result) == 2
    assert result[0]["id"] == "model1"
    assert result[1]["id"] == "model2"