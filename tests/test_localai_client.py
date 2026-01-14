"""
Tests for LocalAI client connectivity and functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from localai_mcp.client import LocalAIClient


class TestLocalAIClient:
    """Test suite for LocalAI client"""
    
    def test_client_initialization(self):
        """Test client can be initialized with correct parameters"""
        client = LocalAIClient(base_url="http://localhost:8080")
        assert client.base_url == "http://localhost:8080"
        assert client.timeout == 60.0
    
    def test_client_initialization_strips_trailing_slash(self):
        """Test client strips trailing slash from base URL"""
        client = LocalAIClient(base_url="http://localhost:8080/")
        assert client.base_url == "http://localhost:8080"
    
    @patch('httpx.Client.get')
    def test_health_check_success(self, mock_get):
        """Test successful health check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = LocalAIClient(base_url="http://localhost:8080")
        result = client.check_health()
        
        assert result is True
        mock_get.assert_called_once_with("http://localhost:8080/readyz")
    
    @patch('httpx.Client.get')
    def test_health_check_failure(self, mock_get):
        """Test health check when server is down"""
        mock_get.side_effect = Exception("Connection refused")
        
        client = LocalAIClient(base_url="http://localhost:8080")
        result = client.check_health()
        
        assert result is False
    
    @patch('httpx.Client.post')
    def test_text_to_speech_success(self, mock_post):
        """Test successful text-to-speech generation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = LocalAIClient(base_url="http://localhost:8080")
        result = client.text_to_speech(text="Hello world")
        
        assert result == b"fake_audio_data"
        mock_post.assert_called_once()
    
    @patch('httpx.Client.post')
    def test_text_to_speech_with_custom_params(self, mock_post):
        """Test TTS with custom parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = LocalAIClient(base_url="http://localhost:8080")
        result = client.text_to_speech(
            text="Hello",
            model="tts-1",
            voice="nova",
            speed=1.5
        )
        
        assert result == b"fake_audio_data"
        call_args = mock_post.call_args
        assert call_args[1]['json']['voice'] == "nova"
        assert call_args[1]['json']['speed'] == 1.5
    
    @patch('httpx.Client.post')
    def test_text_to_speech_failure(self, mock_post):
        """Test TTS failure handling"""
        mock_post.side_effect = Exception("Server error")
        
        client = LocalAIClient(base_url="http://localhost:8080")
        
        with pytest.raises(Exception) as exc_info:
            client.text_to_speech(text="Hello")
        
        assert "Failed to generate speech" in str(exc_info.value)
    
    @patch('httpx.Client.post')
    def test_speech_to_text_success(self, mock_post):
        """Test successful speech-to-text transcription"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"text": "Hello world"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = LocalAIClient(base_url="http://localhost:8080")
        
        # Create a mock file object
        mock_file = MagicMock()
        result = client.speech_to_text(audio_file=mock_file)
        
        assert result == {"text": "Hello world"}
        mock_post.assert_called_once()
    
    @patch('httpx.Client.post')
    def test_generate_audio_success(self, mock_post):
        """Test successful audio generation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = LocalAIClient(base_url="http://localhost:8080")
        result = client.generate_audio(
            prompt="upbeat electronic music",
            duration=10.0
        )
        
        assert result == b"fake_audio_data"
        call_args = mock_post.call_args
        assert call_args[1]['json']['prompt'] == "upbeat electronic music"
        assert call_args[1]['json']['duration'] == 10.0
    
    @patch('httpx.Client.get')
    def test_list_models_success(self, mock_get):
        """Test listing models"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": "tts-1"},
                {"id": "whisper-1"}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = LocalAIClient(base_url="http://localhost:8080")
        result = client.list_models()
        
        assert len(result) == 2
        assert result[0]["id"] == "tts-1"
        assert result[1]["id"] == "whisper-1"
    
    @patch('httpx.Client.get')
    def test_list_models_empty(self, mock_get):
        """Test listing models when none available"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = LocalAIClient(base_url="http://localhost:8080")
        result = client.list_models()
        
        assert result == []
