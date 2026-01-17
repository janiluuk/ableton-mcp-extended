"""
Tests for UVR5 client connectivity and functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from uvr5_mcp.client import UVR5Client


class TestUVR5Client:
    """Test suite for UVR5 client"""
    
    def test_client_initialization(self):
        """Test client can be initialized"""
        client = UVR5Client(base_url="http://localhost:5000")
        assert client.base_url == "http://localhost:5000"
        assert client.timeout == 600.0
    
    @patch('httpx.Client.get')
    def test_health_check_success(self, mock_get):
        """Test successful health check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = UVR5Client(base_url="http://localhost:5000")
        result = client.check_health()
        
        assert result is True
    
    @patch('httpx.Client.get')
    def test_health_check_failure(self, mock_get):
        """Test health check when server is down"""
        mock_get.side_effect = Exception("Connection refused")
        
        client = UVR5Client(base_url="http://localhost:5000")
        result = client.check_health()
        
        assert result is False
    
    @patch('httpx.Client.post')
    def test_separate_audio_success(self, mock_post):
        """Test successful audio separation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "job_id": "test-123",
            "status": "queued"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = UVR5Client(base_url="http://localhost:5000")
        mock_file = MagicMock()
        
        result = client.separate_audio(audio_file=mock_file)
        
        assert result["job_id"] == "test-123"
    
    @patch('httpx.Client.post')
    def test_separate_audio_with_custom_params(self, mock_post):
        """Test audio separation with custom parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"job_id": "test-123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = UVR5Client(base_url="http://localhost:5000")
        mock_file = MagicMock()
        
        result = client.separate_audio(
            audio_file=mock_file,
            model_name="UVR-MDX-NET-Inst_HQ_3",
            output_format="flac"
        )
        
        assert result["job_id"] == "test-123"
    
    @patch('httpx.Client.get')
    def test_get_separation_result_success(self, mock_get):
        """Test getting separation results"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "completed",
            "stems": {
                "vocals": "vocals_data",
                "instrumental": "inst_data"
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = UVR5Client(base_url="http://localhost:5000")
        result = client.get_separation_result("test-123")
        
        assert result["status"] == "completed"
        assert "vocals" in result["stems"]
    
    @patch('httpx.Client.get')
    def test_download_stem_success(self, mock_get):
        """Test downloading a separated stem"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = UVR5Client(base_url="http://localhost:5000")
        result = client.download_stem("test-123", "vocals")
        
        assert result == b"fake_audio_data"
    
    @patch('httpx.Client.get')
    def test_list_models_success(self, mock_get):
        """Test listing available models"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                "UVR-MDX-NET-Inst_HQ_3",
                "UVR-MDX-NET-Voc_FT"
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = UVR5Client(base_url="http://localhost:5000")
        result = client.list_models()
        
        assert len(result) == 2
        assert "UVR-MDX-NET-Inst_HQ_3" in result
