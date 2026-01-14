"""
Pytest configuration for ableton-mcp-extended tests
"""

import pytest
import os
from pathlib import Path


@pytest.fixture
def test_audio_dir(tmp_path):
    """Create a temporary directory for test audio files"""
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()
    return audio_dir


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing"""
    test_dir = Path.home() / "test_audio"
    
    monkeypatch.setenv("LOCALAI_BASE_URL", "http://localhost:8080")
    monkeypatch.setenv("COMFYUI_BASE_URL", "http://localhost:8188")
    monkeypatch.setenv("UVR5_BASE_URL", "http://localhost:5000")
    monkeypatch.setenv("RVC_BASE_URL", "http://localhost:6000")
    monkeypatch.setenv("AI_AUDIO_OUTPUT_DIR", str(test_dir))
    
    return {
        "LOCALAI_BASE_URL": "http://localhost:8080",
        "COMFYUI_BASE_URL": "http://localhost:8188",
        "UVR5_BASE_URL": "http://localhost:5000",
        "RVC_BASE_URL": "http://localhost:6000",
        "AI_AUDIO_OUTPUT_DIR": str(test_dir)
    }


@pytest.fixture
def sample_audio_file(test_audio_dir):
    """Create a simple test audio file"""
    import wave
    import struct
    
    audio_file = test_audio_dir / "test.wav"
    
    # Create a simple 1-second sine wave at 440Hz
    sample_rate = 44100
    duration = 1.0
    frequency = 440.0
    
    with wave.open(str(audio_file), 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(int(sample_rate * duration)):
            value = int(32767.0 * 0.3 * (i % (sample_rate // int(frequency))) / (sample_rate // int(frequency)))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)
    
    return audio_file
