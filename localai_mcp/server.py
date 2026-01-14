"""
LocalAI MCP Server

Provides MCP tools for text-to-speech, speech-to-text, and audio generation
through LocalAI server integration.
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from localai_mcp.client import LocalAIClient
from localai_mcp.utils import make_output_path, make_output_file

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
LOCALAI_BASE_URL = os.getenv("LOCALAI_BASE_URL", "http://localhost:8080")
LOCALAI_TTS_MODEL = os.getenv("LOCALAI_TTS_MODEL", "tts-1")
LOCALAI_STT_MODEL = os.getenv("LOCALAI_STT_MODEL", "whisper-1")
LOCALAI_AUDIO_MODEL = os.getenv("LOCALAI_AUDIO_MODEL", "musicgen")
DEFAULT_OUTPUT_DIR = os.getenv(
    "AI_AUDIO_OUTPUT_DIR",
    os.path.join(Path.home(), "Documents", "Ableton", "User Library", "ai_audio")
)

# Initialize FastMCP server
mcp = FastMCP("LocalAI")

# Initialize LocalAI client
client = LocalAIClient(base_url=LOCALAI_BASE_URL)


@mcp.tool(
    description="""Convert text to speech using LocalAI server.
    
    Generates speech audio from text and saves it to the specified directory.
    For importing into Ableton, use the import_audio_file tool with the generated file path.
    
    Args:
        text: Text to convert to speech
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        output_directory: Directory to save the audio file
        model: TTS model to use (default from env)
        response_format: Audio format (mp3, wav, opus, aac, flac, pcm)
        speed: Speech speed (0.25 to 4.0)
    """
)
def text_to_speech(
    text: str,
    voice: str = "alloy",
    output_directory: str = DEFAULT_OUTPUT_DIR,
    model: Optional[str] = None,
    response_format: str = "mp3",
    speed: float = 1.0
) -> TextContent:
    """Convert text to speech using LocalAI"""
    if not text:
        return TextContent(type="text", text="Error: Text is required")
    
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to LocalAI server at {LOCALAI_BASE_URL}"
        )
    
    try:
        # Use default model from env if not specified
        model_to_use = model or LOCALAI_TTS_MODEL
        
        # Generate speech
        audio_data = client.text_to_speech(
            text=text,
            model=model_to_use,
            voice=voice,
            response_format=response_format,
            speed=speed
        )
        
        # Save to file
        output_path = make_output_path(output_directory)
        output_file = make_output_file("localai_tts", text, output_path, response_format)
        file_path = output_path / output_file
        
        output_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(audio_data)
        
        return TextContent(
            type="text",
            text=f"Success. Audio saved to: {file_path}\nVoice: {voice}, Model: {model_to_use}"
        )
    except Exception as e:
        logger.error(f"Text-to-speech failed: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


@mcp.tool(
    description="""Convert speech to text using LocalAI server.
    
    Transcribes audio file to text using Whisper or other STT models.
    
    Args:
        audio_file_path: Path to audio file to transcribe
        model: STT model to use (default from env)
        language: Language code (e.g., 'en', 'es', 'fr')
        prompt: Optional prompt to guide transcription
        response_format: Response format (json, text, srt, verbose_json, vtt)
        temperature: Sampling temperature (0.0 to 1.0)
    """
)
def speech_to_text(
    audio_file_path: str,
    model: Optional[str] = None,
    language: Optional[str] = None,
    prompt: Optional[str] = None,
    response_format: str = "json",
    temperature: float = 0.0
) -> TextContent:
    """Convert speech to text using LocalAI"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to LocalAI server at {LOCALAI_BASE_URL}"
        )
    
    try:
        # Validate file exists
        file_path = Path(audio_file_path)
        if not file_path.exists():
            return TextContent(type="text", text=f"Error: File not found: {audio_file_path}")
        
        # Use default model from env if not specified
        model_to_use = model or LOCALAI_STT_MODEL
        
        # Transcribe audio
        with open(file_path, "rb") as audio_file:
            result = client.speech_to_text(
                audio_file=audio_file,
                model=model_to_use,
                language=language,
                prompt=prompt,
                response_format=response_format,
                temperature=temperature
            )
        
        # Format response
        if isinstance(result, dict):
            text = result.get("text", str(result))
        else:
            text = str(result)
        
        return TextContent(
            type="text",
            text=f"Transcription:\n{text}\n\nModel: {model_to_use}"
        )
    except Exception as e:
        logger.error(f"Speech-to-text failed: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


@mcp.tool(
    description="""Generate audio from text description using LocalAI.
    
    Creates audio based on text prompts using models like MusicGen.
    For importing into Ableton, use the import_audio_file tool with the generated file path.
    
    Args:
        prompt: Text description of the audio to generate
        output_directory: Directory to save the audio file
        model: Audio generation model to use (default from env)
        duration: Duration in seconds (default 10.0)
        temperature: Sampling temperature (0.0 to 2.0)
        top_k: Top-k sampling parameter
        top_p: Top-p sampling parameter
    """
)
def generate_audio(
    prompt: str,
    output_directory: str = DEFAULT_OUTPUT_DIR,
    model: Optional[str] = None,
    duration: float = 10.0,
    temperature: float = 1.0,
    top_k: int = 250,
    top_p: float = 0.0
) -> TextContent:
    """Generate audio using LocalAI"""
    if not prompt:
        return TextContent(type="text", text="Error: Prompt is required")
    
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to LocalAI server at {LOCALAI_BASE_URL}"
        )
    
    try:
        # Use default model from env if not specified
        model_to_use = model or LOCALAI_AUDIO_MODEL
        
        # Generate audio
        audio_data = client.generate_audio(
            prompt=prompt,
            model=model_to_use,
            duration=duration,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p
        )
        
        # Save to file
        output_path = make_output_path(output_directory)
        output_file = make_output_file("localai_audio", prompt, output_path, "wav")
        file_path = output_path / output_file
        
        output_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(audio_data)
        
        return TextContent(
            type="text",
            text=f"Success. Audio generated and saved to: {file_path}\nModel: {model_to_use}, Duration: {duration}s"
        )
    except Exception as e:
        logger.error(f"Audio generation failed: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


@mcp.tool(description="Check LocalAI server health and connectivity")
def check_localai_health() -> TextContent:
    """Check if LocalAI server is accessible"""
    if client.check_health():
        return TextContent(
            type="text",
            text=f"✓ LocalAI server is healthy at {LOCALAI_BASE_URL}"
        )
    else:
        return TextContent(
            type="text",
            text=f"✗ Cannot connect to LocalAI server at {LOCALAI_BASE_URL}"
        )


@mcp.tool(description="List available models on LocalAI server")
def list_localai_models() -> TextContent:
    """List available models on LocalAI server"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to LocalAI server at {LOCALAI_BASE_URL}"
        )
    
    try:
        models = client.list_models()
        if not models:
            return TextContent(
                type="text",
                text="No models found on LocalAI server"
            )
        
        model_list = "\n".join([f"- {m.get('id', 'unknown')}" for m in models])
        return TextContent(
            type="text",
            text=f"Available models on LocalAI:\n{model_list}"
        )
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


def main():
    """Run the LocalAI MCP server"""
    logger.info("Starting LocalAI MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
