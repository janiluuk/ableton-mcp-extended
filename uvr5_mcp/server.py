"""
UVR5 MCP Server

Provides MCP tools for vocal/instrumental separation using UVR5.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from uvr5_mcp.client import UVR5Client

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
UVR5_BASE_URL = os.getenv("UVR5_BASE_URL", "http://localhost:5000")
DEFAULT_OUTPUT_DIR = os.getenv(
    "UVR5_OUTPUT_DIR",
    os.path.join(Path.home(), "Documents", "Ableton", "User Library", "uvr5_audio")
)

# Initialize FastMCP server
mcp = FastMCP("UVR5")

# Initialize UVR5 client
client = UVR5Client(base_url=UVR5_BASE_URL)


@mcp.tool(
    description="""Separate vocals and instrumentals from audio using UVR5.
    
    Uses AI models to isolate different stems (vocals, instrumental, drums, bass, etc.)
    from audio files. Perfect for remixing, sampling, and creative audio processing.
    
    Args:
        audio_file_path: Path to audio file to process
        model_name: Separation model to use (default: UVR-MDX-NET-Inst_HQ_3)
        output_directory: Directory to save separated stems
        output_format: Output format (wav, flac, mp3)
        extract_vocals: Extract vocals stem
        extract_instrumental: Extract instrumental stem
    """
)
def separate_audio(
    audio_file_path: str,
    model_name: str = "UVR-MDX-NET-Inst_HQ_3",
    output_directory: str = DEFAULT_OUTPUT_DIR,
    output_format: str = "wav",
    extract_vocals: bool = True,
    extract_instrumental: bool = True
) -> TextContent:
    """Separate audio into stems using UVR5"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to UVR5 server at {UVR5_BASE_URL}"
        )
    
    try:
        # Validate file exists
        file_path = Path(audio_file_path)
        if not file_path.exists():
            return TextContent(type="text", text=f"Error: File not found: {audio_file_path}")
        
        # Perform separation
        with open(file_path, "rb") as audio_file:
            result = client.separate_audio(
                audio_file=audio_file,
                model_name=model_name,
                output_format=output_format
            )
        
        # Check if we got a job ID (async processing)
        job_id = result.get("job_id")
        if job_id:
            logger.info(f"Separation job queued with ID: {job_id}")
            
            # Get results
            job_result = client.get_separation_result(job_id)
            if job_result.get("status") != "completed":
                return TextContent(
                    type="text",
                    text=f"Separation in progress. Job ID: {job_id}\nCheck status later."
                )
        else:
            # Immediate result
            job_result = result
        
        # Download and save stems
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        base_name = file_path.stem
        
        # Download vocals
        if extract_vocals and "vocals" in job_result.get("stems", {}):
            try:
                if job_id:
                    vocals_data = client.download_stem(job_id, "vocals")
                else:
                    vocals_data = job_result["stems"]["vocals"]
                
                vocals_path = output_path / f"{base_name}_vocals.{output_format}"
                with open(vocals_path, "wb") as f:
                    if isinstance(vocals_data, bytes):
                        f.write(vocals_data)
                    else:
                        f.write(vocals_data.encode())
                
                saved_files.append(str(vocals_path))
            except Exception as e:
                logger.error(f"Failed to save vocals: {e}")
        
        # Download instrumental
        if extract_instrumental and "instrumental" in job_result.get("stems", {}):
            try:
                if job_id:
                    inst_data = client.download_stem(job_id, "instrumental")
                else:
                    inst_data = job_result["stems"]["instrumental"]
                
                inst_path = output_path / f"{base_name}_instrumental.{output_format}"
                with open(inst_path, "wb") as f:
                    if isinstance(inst_data, bytes):
                        f.write(inst_data)
                    else:
                        f.write(inst_data.encode())
                
                saved_files.append(str(inst_path))
            except Exception as e:
                logger.error(f"Failed to save instrumental: {e}")
        
        if saved_files:
            files_list = "\n".join(saved_files)
            return TextContent(
                type="text",
                text=f"Audio separation completed!\n\nSeparated stems:\n{files_list}\n\nModel: {model_name}"
            )
        else:
            return TextContent(
                type="text",
                text="Separation completed but no stems could be saved"
            )
    
    except Exception as e:
        logger.error(f"Audio separation failed: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


@mcp.tool(description="Check UVR5 server health and connectivity")
def check_uvr5_health() -> TextContent:
    """Check if UVR5 server is accessible"""
    if client.check_health():
        return TextContent(
            type="text",
            text=f"✓ UVR5 server is healthy at {UVR5_BASE_URL}"
        )
    else:
        return TextContent(
            type="text",
            text=f"✗ Cannot connect to UVR5 server at {UVR5_BASE_URL}"
        )


@mcp.tool(description="List available UVR5 separation models")
def list_uvr5_models() -> TextContent:
    """List available separation models on UVR5 server"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to UVR5 server at {UVR5_BASE_URL}"
        )
    
    try:
        models = client.list_models()
        if not models:
            return TextContent(
                type="text",
                text="No models found on UVR5 server"
            )
        
        model_list = "\n".join([f"- {m}" for m in models])
        return TextContent(
            type="text",
            text=f"Available UVR5 models:\n{model_list}"
        )
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


def main():
    """Run the UVR5 MCP server"""
    logger.info("Starting UVR5 MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
