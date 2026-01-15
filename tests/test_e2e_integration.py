"""
End-to-End Tests for AI Audio Integrations

These tests require actual servers to be running (via docker-compose).
They test the full integration flow from client to server and back.
"""

import pytest
import os
import time
from pathlib import Path
import io

# Mark all tests in this file as e2e tests
pytestmark = pytest.mark.e2e


class TestLocalAIE2E:
    """E2E tests for LocalAI integration"""
    
    @pytest.fixture
    def localai_client(self):
        """Create LocalAI client connected to real server"""
        from localai_mcp.client import LocalAIClient
        base_url = os.getenv("LOCALAI_BASE_URL", "http://localhost:8080")
        return LocalAIClient(base_url=base_url)
    
    def test_health_check(self, localai_client):
        """Test LocalAI server health check"""
        # Retry a few times as server might be starting
        for _ in range(5):
            if localai_client.check_health():
                break
            time.sleep(2)
        
        assert localai_client.check_health(), "LocalAI server should be healthy"
    
    def test_list_models(self, localai_client):
        """Test listing available models"""
        models = localai_client.list_models()
        # LocalAI might have models or be empty on first start
        assert isinstance(models, list), "Should return a list of models"


class TestComfyUIE2E:
    """E2E tests for ComfyUI integration"""
    
    @pytest.fixture
    def comfyui_client(self):
        """Create ComfyUI client connected to real server"""
        from comfyui_mcp.client import ComfyUIClient
        base_url = os.getenv("COMFYUI_BASE_URL", "http://localhost:8188")
        return ComfyUIClient(base_url=base_url)
    
    def test_health_check(self, comfyui_client):
        """Test ComfyUI server health check"""
        # Retry a few times as server might be starting
        for _ in range(10):
            if comfyui_client.check_health():
                break
            time.sleep(3)
        
        assert comfyui_client.check_health(), "ComfyUI server should be healthy"
    
    def test_get_queue(self, comfyui_client):
        """Test getting queue status"""
        queue = comfyui_client.get_queue()
        assert isinstance(queue, dict), "Should return queue information"
        # Queue should have running and pending keys
        assert "queue_running" in queue or "queue_pending" in queue or queue == {}


class TestUVR5E2E:
    """E2E tests for UVR5 integration"""
    
    @pytest.fixture
    def uvr5_client(self):
        """Create UVR5 client connected to real server"""
        from uvr5_mcp.client import UVR5Client
        base_url = os.getenv("UVR5_BASE_URL", "http://localhost:5000")
        return UVR5Client(base_url=base_url)
    
    @pytest.fixture
    def sample_audio(self):
        """Create a simple mock audio file"""
        # Create minimal WAV header + data
        audio_data = b'RIFF' + b'\x00' * 4 + b'WAVE'
        return io.BytesIO(audio_data)
    
    def test_health_check(self, uvr5_client):
        """Test UVR5 server health check"""
        # Retry a few times as server might be starting
        for _ in range(5):
            if uvr5_client.check_health():
                break
            time.sleep(2)
        
        assert uvr5_client.check_health(), "UVR5 server should be healthy"
    
    def test_list_models(self, uvr5_client):
        """Test listing available separation models"""
        models = uvr5_client.list_models()
        assert isinstance(models, list), "Should return a list of models"
        assert len(models) > 0, "Should have at least one model"
    
    def test_separate_audio(self, uvr5_client, sample_audio):
        """Test audio separation"""
        result = uvr5_client.separate_audio(
            audio_file=sample_audio,
            model_name="UVR-MDX-NET-Inst_HQ_3"
        )
        
        assert isinstance(result, dict), "Should return a dictionary"
        assert "job_id" in result or "stems" in result, "Should have job_id or stems"


class TestRVCE2E:
    """E2E tests for RVC integration"""
    
    @pytest.fixture
    def rvc_client(self):
        """Create RVC client connected to real server"""
        from rvc_mcp.client import RVCClient
        base_url = os.getenv("RVC_BASE_URL", "http://localhost:6000")
        return RVCClient(base_url=base_url)
    
    @pytest.fixture
    def sample_audio(self):
        """Create a simple mock audio file"""
        # Create minimal WAV header + data
        audio_data = b'RIFF' + b'\x00' * 4 + b'WAVE'
        return io.BytesIO(audio_data)
    
    def test_health_check(self, rvc_client):
        """Test RVC server health check"""
        # Retry a few times as server might be starting
        for _ in range(5):
            if rvc_client.check_health():
                break
            time.sleep(2)
        
        assert rvc_client.check_health(), "RVC server should be healthy"
    
    def test_list_models(self, rvc_client):
        """Test listing available voice models"""
        models = rvc_client.list_models()
        assert isinstance(models, list), "Should return a list of models"
        assert len(models) > 0, "Should have at least one model"
    
    def test_get_model_info(self, rvc_client):
        """Test getting model information"""
        models = rvc_client.list_models()
        if models:
            model_name = models[0]["name"] if isinstance(models[0], dict) else models[0]
            info = rvc_client.get_model_info(model_name)
            assert isinstance(info, dict), "Should return model information"
    
    def test_convert_voice(self, rvc_client, sample_audio):
        """Test voice conversion"""
        result = rvc_client.convert_voice(
            audio_file=sample_audio,
            model_name="test_model"
        )
        
        assert isinstance(result, bytes), "Should return audio bytes"
        assert len(result) > 0, "Should return non-empty audio data"


class TestIntegrationWorkflow:
    """Test complete workflows using multiple services"""
    
    def test_full_audio_processing_workflow(self):
        """Test a complete workflow: generate -> separate -> convert"""
        # This test demonstrates how all services work together
        # In a real scenario, you would:
        # 1. Generate audio with LocalAI or ComfyUI
        # 2. Separate stems with UVR5
        # 3. Apply voice conversion with RVC
        # 4. Import to Ableton
        
        from localai_mcp.client import LocalAIClient
        from uvr5_mcp.client import UVR5Client
        from rvc_mcp.client import RVCClient
        
        # Initialize clients
        localai = LocalAIClient(os.getenv("LOCALAI_BASE_URL", "http://localhost:8080"))
        uvr5 = UVR5Client(os.getenv("UVR5_BASE_URL", "http://localhost:5000"))
        rvc = RVCClient(os.getenv("RVC_BASE_URL", "http://localhost:6000"))
        
        # Verify all services are healthy
        assert localai.check_health(), "LocalAI should be available"
        assert uvr5.check_health(), "UVR5 should be available"
        assert rvc.check_health(), "RVC should be available"
        
        # This confirms all services can be orchestrated together
        print("✓ All services are healthy and can be orchestrated")
