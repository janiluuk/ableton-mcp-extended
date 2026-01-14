"""
Tests for ComfyUI client connectivity and functionality
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from comfyui_mcp.client import ComfyUIClient


class TestComfyUIClient:
    """Test suite for ComfyUI client"""
    
    def test_client_initialization(self):
        """Test client can be initialized"""
        client = ComfyUIClient(base_url="http://localhost:8188")
        assert client.base_url == "http://localhost:8188"
        assert client.timeout == 300.0
    
    @patch('httpx.Client.get')
    def test_health_check_success(self, mock_get):
        """Test successful health check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        result = client.check_health()
        
        assert result is True
    
    @patch('httpx.Client.get')
    def test_health_check_failure(self, mock_get):
        """Test health check when server is down"""
        mock_get.side_effect = Exception("Connection refused")
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        result = client.check_health()
        
        assert result is False
    
    def test_load_workflow_success(self, tmp_path):
        """Test loading workflow from file"""
        workflow_data = {"1": {"class_type": "LoadImage"}}
        workflow_file = tmp_path / "workflow.json"
        
        with open(workflow_file, 'w') as f:
            json.dump(workflow_data, f)
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        result = client.load_workflow(str(workflow_file))
        
        assert result == workflow_data
    
    def test_load_workflow_file_not_found(self):
        """Test loading workflow when file doesn't exist"""
        client = ComfyUIClient(base_url="http://localhost:8188")
        
        with pytest.raises(Exception) as exc_info:
            client.load_workflow("/nonexistent/workflow.json")
        
        assert "Failed to load workflow" in str(exc_info.value)
    
    @patch('httpx.Client.post')
    def test_queue_prompt_success(self, mock_post):
        """Test queueing a workflow"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"prompt_id": "test-123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        workflow = {"1": {"class_type": "LoadImage"}}
        
        result = client.queue_prompt(workflow)
        
        assert result == "test-123"
    
    @patch('httpx.Client.get')
    def test_get_queue(self, mock_get):
        """Test getting queue status"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "queue_running": [],
            "queue_pending": []
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        result = client.get_queue()
        
        assert "queue_running" in result
        assert "queue_pending" in result
    
    @patch('httpx.Client.get')
    def test_get_history(self, mock_get):
        """Test getting execution history"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "test-123": {
                "outputs": {
                    "1": {"audio": [{"filename": "output.wav"}]}
                }
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        result = client.get_history("test-123")
        
        assert "test-123" in result
        assert "outputs" in result["test-123"]
    
    @patch('httpx.Client.get')
    def test_wait_for_completion_success(self, mock_get):
        """Test waiting for workflow completion"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "test-123": {
                "outputs": {
                    "1": {"audio": [{"filename": "output.wav"}]}
                }
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        result = client.wait_for_completion("test-123", max_wait=5, poll_interval=1)
        
        assert result is True
    
    @patch('httpx.Client.get')
    def test_get_output_files(self, mock_get):
        """Test getting output files from completed workflow"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "test-123": {
                "outputs": {
                    "1": {
                        "audio": [
                            {"filename": "output.wav", "subfolder": ""}
                        ]
                    }
                }
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        result = client.get_output_files("test-123")
        
        assert len(result) == 1
        assert result[0]["type"] == "audio"
        assert result[0]["filename"] == "output.wav"
    
    @patch('httpx.Client.get')
    def test_download_file_success(self, mock_get):
        """Test downloading a file"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = ComfyUIClient(base_url="http://localhost:8188")
        result = client.download_file("output.wav")
        
        assert result == b"fake_audio_data"
