"""
RVC API Client

Provides connectivity to RVC (Retrieval-based Voice Conversion) server
for voice conversion and transformation.
"""

import httpx
import logging
from typing import Optional, BinaryIO
from pathlib import Path

logger = logging.getLogger(__name__)


class RVCClient:
    """Client for interacting with RVC server"""
    
    def __init__(self, base_url: str, timeout: float = 300.0):
        """
        Initialize RVC client
        
        Args:
            base_url: Base URL of the RVC server
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
        Check if RVC server is available
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def convert_voice(
        self,
        audio_file: BinaryIO,
        model_name: str,
        pitch_shift: int = 0,
        filter_radius: int = 3,
        index_rate: float = 0.75,
        rms_mix_rate: float = 0.25,
        protect_voiceless: float = 0.5,
        output_format: str = "wav"
    ) -> bytes:
        """
        Convert voice in audio file using RVC model
        
        Args:
            audio_file: Audio file to process
            model_name: Name of RVC model to use
            pitch_shift: Pitch shift in semitones (-12 to 12)
            filter_radius: Median filtering radius (0-7)
            index_rate: Feature retrieval ratio (0.0-1.0)
            rms_mix_rate: Volume envelope mix rate (0.0-1.0)
            protect_voiceless: Protect voiceless consonants (0.0-0.5)
            output_format: Output format (wav, mp3, flac)
            
        Returns:
            Converted audio data as bytes
            
        Raises:
            Exception: If conversion fails
        """
        try:
            files = {
                "audio_file": audio_file
            }
            data = {
                "model_name": model_name,
                "pitch_shift": pitch_shift,
                "filter_radius": filter_radius,
                "index_rate": index_rate,
                "rms_mix_rate": rms_mix_rate,
                "protect_voiceless": protect_voiceless,
                "output_format": output_format
            }
            
            response = self.client.post(
                f"{self.base_url}/api/convert",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Voice conversion failed: {e}")
            raise Exception(f"Failed to convert voice: {str(e)}")
    
    def list_models(self) -> list:
        """
        List available RVC models
        
        Returns:
            List of available models with metadata
        """
        try:
            response = self.client.get(f"{self.base_url}/api/models")
            response.raise_for_status()
            return response.json().get("models", [])
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    def get_model_info(self, model_name: str) -> dict:
        """
        Get information about a specific RVC model
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model information dictionary
        """
        try:
            response = self.client.get(f"{self.base_url}/api/models/{model_name}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return {}
    
    def train_model(
        self,
        model_name: str,
        training_files: list,
        epochs: int = 500,
        batch_size: int = 8,
        learning_rate: float = 1e-4
    ) -> dict:
        """
        Train a new RVC model (if supported by server)
        
        Args:
            model_name: Name for the new model
            training_files: List of training audio file paths
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate
            
        Returns:
            Training job information
            
        Raises:
            Exception: If training fails
        """
        try:
            files = [
                ("training_files", open(f, "rb"))
                for f in training_files
            ]
            data = {
                "model_name": model_name,
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate
            }
            
            response = self.client.post(
                f"{self.base_url}/api/train",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise Exception(f"Failed to train model: {str(e)}")
        finally:
            # Close opened files
            for _, file_obj in files:
                try:
                    file_obj.close()
                except:
                    pass
