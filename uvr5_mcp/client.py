"""
UVR5 API Client

Provides connectivity to UVR5 (Ultimate Vocal Remover) server for
vocal/instrumental separation and audio processing.
"""

import httpx
import logging
from typing import Optional, BinaryIO
from pathlib import Path

logger = logging.getLogger(__name__)


class UVR5Client:
    """Client for interacting with UVR5 server"""
    
    def __init__(self, base_url: str, timeout: float = 600.0):
        """
        Initialize UVR5 client
        
        Args:
            base_url: Base URL of the UVR5 server
            timeout: Request timeout in seconds (vocal separation can take time)
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
        Check if UVR5 server is available
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def separate_audio(
        self,
        audio_file: BinaryIO,
        model_name: str = "UVR-MDX-NET-Inst_HQ_3",
        output_format: str = "wav",
        stem_naming: str = "standard"
    ) -> dict:
        """
        Separate vocals and instrumentals from audio
        
        Args:
            audio_file: Audio file to process
            model_name: Model to use for separation
            output_format: Output format (wav, flac, mp3)
            stem_naming: Naming convention for stems (standard, pair)
            
        Returns:
            Dictionary with separation results and file data
            
        Raises:
            Exception: If separation fails
        """
        try:
            files = {
                "audio_file": audio_file
            }
            data = {
                "model_name": model_name,
                "output_format": output_format,
                "stem_naming": stem_naming
            }
            
            response = self.client.post(
                f"{self.base_url}/api/separate",
                files=files,
                data=data
            )
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logger.error(f"Audio separation failed: {e}")
            raise Exception(f"Failed to separate audio: {str(e)}")
    
    def get_separation_result(self, job_id: str) -> dict:
        """
        Get results of a separation job
        
        Args:
            job_id: Job ID to query
            
        Returns:
            Dictionary with job status and results
        """
        try:
            response = self.client.get(f"{self.base_url}/api/result/{job_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get separation result: {e}")
            return {"status": "error", "message": str(e)}
    
    def download_stem(self, job_id: str, stem_type: str) -> bytes:
        """
        Download a separated stem
        
        Args:
            job_id: Job ID
            stem_type: Type of stem (vocals, instrumental, drums, bass, other)
            
        Returns:
            Audio data as bytes
            
        Raises:
            Exception: If download fails
        """
        try:
            response = self.client.get(
                f"{self.base_url}/api/download/{job_id}/{stem_type}"
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Failed to download stem: {e}")
            raise Exception(f"Failed to download {stem_type} stem: {str(e)}")
    
    def list_models(self) -> list:
        """
        List available separation models
        
        Returns:
            List of available models
        """
        try:
            response = self.client.get(f"{self.base_url}/api/models")
            response.raise_for_status()
            return response.json().get("models", [])
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
