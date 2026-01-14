"""
ComfyUI API Client

Provides connectivity to ComfyUI server for workflow execution and audio generation.
"""

import httpx
import json
import logging
import time
import uuid
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ComfyUIClient:
    """Client for interacting with ComfyUI server"""
    
    def __init__(self, base_url: str, timeout: float = 300.0):
        """
        Initialize ComfyUI client
        
        Args:
            base_url: Base URL of the ComfyUI server
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
        Check if ComfyUI server is available
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = self.client.get(f"{self.base_url}/system_stats")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def load_workflow(self, workflow_path: str) -> Dict[str, Any]:
        """
        Load workflow from JSON file
        
        Args:
            workflow_path: Path to workflow JSON file
            
        Returns:
            Workflow dictionary
            
        Raises:
            Exception: If workflow loading fails
        """
        try:
            with open(workflow_path, 'r') as f:
                workflow = json.load(f)
            return workflow
        except Exception as e:
            logger.error(f"Failed to load workflow: {e}")
            raise Exception(f"Failed to load workflow from {workflow_path}: {str(e)}")
    
    def queue_prompt(self, workflow: Dict[str, Any], client_id: Optional[str] = None) -> str:
        """
        Queue a workflow for execution
        
        Args:
            workflow: Workflow dictionary
            client_id: Optional client ID for tracking
            
        Returns:
            Prompt ID
            
        Raises:
            Exception: If queueing fails
        """
        try:
            if client_id is None:
                client_id = str(uuid.uuid4())
            
            payload = {
                "prompt": workflow,
                "client_id": client_id
            }
            
            response = self.client.post(
                f"{self.base_url}/prompt",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            prompt_id = result.get("prompt_id")
            if not prompt_id:
                raise Exception("No prompt_id in response")
            
            logger.info(f"Queued prompt with ID: {prompt_id}")
            return prompt_id
        except Exception as e:
            logger.error(f"Failed to queue prompt: {e}")
            raise Exception(f"Failed to queue workflow: {str(e)}")
    
    def get_queue(self) -> Dict[str, Any]:
        """
        Get current queue status
        
        Returns:
            Queue information dictionary
        """
        try:
            response = self.client.get(f"{self.base_url}/queue")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get queue: {e}")
            return {}
    
    def get_history(self, prompt_id: str) -> Dict[str, Any]:
        """
        Get execution history for a prompt
        
        Args:
            prompt_id: Prompt ID to query
            
        Returns:
            History dictionary
        """
        try:
            response = self.client.get(f"{self.base_url}/history/{prompt_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get history: {e}")
            return {}
    
    def wait_for_completion(self, prompt_id: str, max_wait: int = 300, poll_interval: int = 2) -> bool:
        """
        Wait for workflow execution to complete
        
        Args:
            prompt_id: Prompt ID to wait for
            max_wait: Maximum time to wait in seconds
            poll_interval: Time between polls in seconds
            
        Returns:
            True if completed successfully, False otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                history = self.get_history(prompt_id)
                if prompt_id in history:
                    prompt_data = history[prompt_id]
                    if "outputs" in prompt_data:
                        logger.info(f"Workflow {prompt_id} completed")
                        return True
                
                time.sleep(poll_interval)
            except Exception as e:
                logger.error(f"Error checking completion: {e}")
                time.sleep(poll_interval)
        
        logger.warning(f"Workflow {prompt_id} did not complete within {max_wait}s")
        return False
    
    def get_output_files(self, prompt_id: str) -> list:
        """
        Get output files from completed workflow
        
        Args:
            prompt_id: Prompt ID
            
        Returns:
            List of output file information
        """
        try:
            history = self.get_history(prompt_id)
            if prompt_id not in history:
                return []
            
            outputs = history[prompt_id].get("outputs", {})
            files = []
            
            for node_id, node_output in outputs.items():
                if "images" in node_output:
                    for img in node_output["images"]:
                        files.append({
                            "type": "image",
                            "filename": img.get("filename"),
                            "subfolder": img.get("subfolder", ""),
                            "node_id": node_id
                        })
                if "audio" in node_output:
                    for audio in node_output["audio"]:
                        files.append({
                            "type": "audio",
                            "filename": audio.get("filename"),
                            "subfolder": audio.get("subfolder", ""),
                            "node_id": node_id
                        })
            
            return files
        except Exception as e:
            logger.error(f"Failed to get output files: {e}")
            return []
    
    def download_file(self, filename: str, subfolder: str = "", file_type: str = "output") -> bytes:
        """
        Download a file from ComfyUI server
        
        Args:
            filename: Name of the file
            subfolder: Subfolder path
            file_type: Type of file (output, input, temp)
            
        Returns:
            File content as bytes
            
        Raises:
            Exception: If download fails
        """
        try:
            params = {
                "filename": filename,
                "type": file_type
            }
            if subfolder:
                params["subfolder"] = subfolder
            
            response = self.client.get(
                f"{self.base_url}/view",
                params=params
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            raise Exception(f"Failed to download file {filename}: {str(e)}")
