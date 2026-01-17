"""
LocalAI API Client

Provides connectivity to LocalAI server for text-to-speech, speech-to-text,
and audio generation functionality.
"""

import httpx
import logging
from typing import Optional, BinaryIO
from pathlib import Path

logger = logging.getLogger(__name__)


class LocalAIClient:
    """Client for interacting with LocalAI server"""
    
    def __init__(self, base_url: str, timeout: float = 60.0):
        """
        Initialize LocalAI client
        
        Args:
            base_url: Base URL of the LocalAI server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
        
    def __del__(self):
        """Cleanup client resources"""
        try:
            self.client.close()
        except:
            pass
    
    def check_health(self) -> bool:
        """
        Check if LocalAI server is available
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = self.client.get(f"{self.base_url}/readyz")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def text_to_speech(
        self,
        text: str,
        model: str = "tts-1",
        voice: str = "alloy",
        response_format: str = "mp3",
        speed: float = 1.0
    ) -> bytes:
        """
        Convert text to speech using LocalAI
        
        Args:
            text: Text to convert to speech
            model: TTS model to use
            voice: Voice to use for speech generation
            response_format: Audio format (mp3, opus, aac, flac, wav, pcm)
            speed: Speech speed (0.25 to 4.0)
            
        Returns:
            Audio data as bytes
            
        Raises:
            Exception: If TTS generation fails
        """
        try:
            response = self.client.post(
                f"{self.base_url}/v1/audio/speech",
                json={
                    "model": model,
                    "input": text,
                    "voice": voice,
                    "response_format": response_format,
                    "speed": speed
                }
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise Exception(f"Failed to generate speech: {str(e)}")
    
    def speech_to_text(
        self,
        audio_file: BinaryIO,
        model: str = "whisper-1",
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        response_format: str = "json",
        temperature: float = 0.0
    ) -> dict:
        """
        Convert speech to text using LocalAI
        
        Args:
            audio_file: Audio file to transcribe
            model: STT model to use
            language: Language code (e.g., 'en', 'es')
            prompt: Optional prompt to guide the model
            response_format: Response format (json, text, srt, verbose_json, vtt)
            temperature: Sampling temperature
            
        Returns:
            Transcription result as dictionary
            
        Raises:
            Exception: If transcription fails
        """
        try:
            files = {
                "file": audio_file
            }
            data = {
                "model": model,
                "response_format": response_format,
                "temperature": temperature
            }
            if language:
                data["language"] = language
            if prompt:
                data["prompt"] = prompt
            
            response = self.client.post(
                f"{self.base_url}/v1/audio/transcriptions",
                files=files,
                data=data
            )
            response.raise_for_status()
            
            if response_format == "json" or response_format == "verbose_json":
                return response.json()
            else:
                return {"text": response.text}
        except Exception as e:
            logger.error(f"STT transcription failed: {e}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    def generate_audio(
        self,
        prompt: str,
        model: str = "musicgen",
        duration: float = 10.0,
        temperature: float = 1.0,
        top_k: int = 250,
        top_p: float = 0.0
    ) -> bytes:
        """
        Generate audio from text prompt using LocalAI
        
        Args:
            prompt: Text description of desired audio
            model: Audio generation model to use
            duration: Duration of generated audio in seconds
            temperature: Sampling temperature
            top_k: Top-k sampling parameter
            top_p: Top-p sampling parameter
            
        Returns:
            Generated audio data as bytes
            
        Raises:
            Exception: If audio generation fails
        """
        try:
            response = self.client.post(
                f"{self.base_url}/v1/audio/generations",
                json={
                    "model": model,
                    "prompt": prompt,
                    "duration": duration,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_p": top_p
                }
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Audio generation failed: {e}")
            raise Exception(f"Failed to generate audio: {str(e)}")
    
    def list_models(self) -> list:
        """
        List available models on LocalAI server
        
        Returns:
            List of available models
        """
        try:
            response = self.client.get(f"{self.base_url}/v1/models")
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
