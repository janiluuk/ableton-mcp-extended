"""
RVC MCP Server

Provides MCP tools for voice conversion using RVC (Retrieval-based Voice Conversion).
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from rvc_mcp.client import RVCClient

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
RVC_BASE_URL = os.getenv("RVC_BASE_URL", "http://localhost:6000")
DEFAULT_OUTPUT_DIR = os.getenv(
    "RVC_OUTPUT_DIR",
    os.path.join(Path.home(), "Documents", "Ableton", "User Library", "rvc_audio")
)

# Initialize FastMCP server
mcp = FastMCP("RVC")

# Initialize RVC client
client = RVCClient(base_url=RVC_BASE_URL)


@mcp.tool(
    description="""Convert voice in audio file using RVC model.
    
    Transforms the voice in an audio file to match a target voice model.
    Perfect for creating unique vocal characters, voice acting, and creative voice effects.
    
    Args:
        audio_file_path: Path to audio file to process
        model_name: Name of RVC model to use for conversion
        output_directory: Directory to save converted audio
        pitch_shift: Pitch shift in semitones (-12 to 12)
        filter_radius: Median filtering radius for smoothing (0-7)
        index_rate: Feature retrieval ratio, higher = more target voice (0.0-1.0)
        rms_mix_rate: Volume envelope mix rate (0.0-1.0)
        protect_voiceless: Protection for voiceless consonants (0.0-0.5)
        output_format: Output format (wav, mp3, flac)
    """
)
def convert_voice(
    audio_file_path: str,
    model_name: str,
    output_directory: str = DEFAULT_OUTPUT_DIR,
    pitch_shift: int = 0,
    filter_radius: int = 3,
    index_rate: float = 0.75,
    rms_mix_rate: float = 0.25,
    protect_voiceless: float = 0.5,
    output_format: str = "wav"
) -> TextContent:
    """Convert voice using RVC"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to RVC server at {RVC_BASE_URL}"
        )
    
    try:
        # Validate file exists
        file_path = Path(audio_file_path)
        if not file_path.exists():
            return TextContent(type="text", text=f"Error: File not found: {audio_file_path}")
        
        # Perform voice conversion
        with open(file_path, "rb") as audio_file:
            converted_audio = client.convert_voice(
                audio_file=audio_file,
                model_name=model_name,
                pitch_shift=pitch_shift,
                filter_radius=filter_radius,
                index_rate=index_rate,
                rms_mix_rate=rms_mix_rate,
                protect_voiceless=protect_voiceless,
                output_format=output_format
            )
        
        # Save converted audio
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
        
        base_name = file_path.stem
        output_file = output_path / f"{base_name}_rvc_{model_name}.{output_format}"
        
        with open(output_file, "wb") as f:
            f.write(converted_audio)
        
        return TextContent(
            type="text",
            text=f"Voice conversion completed!\n\nConverted audio: {output_file}\nModel: {model_name}, Pitch: {pitch_shift:+d}"
        )
    
    except Exception as e:
        logger.error(f"Voice conversion failed: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


@mcp.tool(description="Check RVC server health and connectivity")
def check_rvc_health() -> TextContent:
    """Check if RVC server is accessible"""
    if client.check_health():
        return TextContent(
            type="text",
            text=f"✓ RVC server is healthy at {RVC_BASE_URL}"
        )
    else:
        return TextContent(
            type="text",
            text=f"✗ Cannot connect to RVC server at {RVC_BASE_URL}"
        )


@mcp.tool(description="List available RVC voice models")
def list_rvc_models() -> TextContent:
    """List available RVC models on server"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to RVC server at {RVC_BASE_URL}"
        )
    
    try:
        models = client.list_models()
        if not models:
            return TextContent(
                type="text",
                text="No models found on RVC server"
            )
        
        model_list = []
        for model in models:
            if isinstance(model, dict):
                name = model.get("name", "unknown")
                info = model.get("info", "")
                model_list.append(f"- {name}: {info}" if info else f"- {name}")
            else:
                model_list.append(f"- {model}")
        
        models_str = "\n".join(model_list)
        return TextContent(
            type="text",
            text=f"Available RVC models:\n{models_str}"
        )
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


@mcp.tool(description="Get information about a specific RVC model")
def get_rvc_model_info(model_name: str) -> TextContent:
    """Get detailed information about an RVC model"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to RVC server at {RVC_BASE_URL}"
        )
    
    try:
        model_info = client.get_model_info(model_name)
        if not model_info:
            return TextContent(
                type="text",
                text=f"No information found for model: {model_name}"
            )
        
        info_str = f"Model: {model_name}\n"
        for key, value in model_info.items():
            info_str += f"{key}: {value}\n"
        
        return TextContent(type="text", text=info_str)
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


def main():
    """Run the RVC MCP server"""
    logger.info("Starting RVC MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
