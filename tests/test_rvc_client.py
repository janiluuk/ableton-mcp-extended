"""
Tests for RVC client connectivity and functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from rvc_mcp.client import RVCClient


class TestRVCClient:
    """Test suite for RVC client"""
    
    def test_client_initialization(self):
        """Test client can be initialized"""
        client = RVCClient(base_url="http://localhost:6000")
        assert client.base_url == "http://localhost:6000"
        assert client.timeout == 300.0
    
    @patch('httpx.Client.get')
    def test_health_check_success(self, mock_get):
        """Test successful health check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = RVCClient(base_url="http://localhost:6000")
        result = client.check_health()
        
        assert result is True
    
    @patch('httpx.Client.get')
    def test_health_check_failure(self, mock_get):
        """Test health check when server is down"""
        mock_get.side_effect = Exception("Connection refused")
        
        client = RVCClient(base_url="http://localhost:6000")
        result = client.check_health()
        
        assert result is False
    
    @patch('httpx.Client.post')
    def test_convert_voice_success(self, mock_post):
        """Test successful voice conversion"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = RVCClient(base_url="http://localhost:6000")
        mock_file = MagicMock()
        
        result = client.convert_voice(
            audio_file=mock_file,
            model_name="test_model"
        )
        
        assert result == b"fake_audio_data"
    
    @patch('httpx.Client.post')
    def test_convert_voice_with_custom_params(self, mock_post):
        """Test voice conversion with custom parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = RVCClient(base_url="http://localhost:6000")
        mock_file = MagicMock()
        
        result = client.convert_voice(
            audio_file=mock_file,
            model_name="test_model",
            pitch_shift=5,
            index_rate=0.8
        )
        
        assert result == b"fake_audio_data"
        call_args = mock_post.call_args
        assert call_args[1]['data']['pitch_shift'] == 5
        assert call_args[1]['data']['index_rate'] == 0.8
    
    @patch('httpx.Client.get')
    def test_list_models_success(self, mock_get):
        """Test listing available models"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {"name": "model1", "info": "Test model 1"},
                {"name": "model2", "info": "Test model 2"}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = RVCClient(base_url="http://localhost:6000")
        result = client.list_models()
        
        assert len(result) == 2
        assert result[0]["name"] == "model1"
    
    @patch('httpx.Client.get')
    def test_get_model_info_success(self, mock_get):
        """Test getting model information"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "test_model",
            "version": "1.0",
            "description": "Test model"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = RVCClient(base_url="http://localhost:6000")
        result = client.get_model_info("test_model")
        
        assert result["name"] == "test_model"
        assert result["version"] == "1.0"
