"""
Utility functions for LocalAI MCP server
"""

import re
from pathlib import Path
from datetime import datetime


def make_output_path(output_directory: str) -> Path:
    """
    Create and validate output directory path
    
    Args:
        output_directory: Directory path string
        
    Returns:
        Path object for output directory
    """
    output_path = Path(output_directory).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def make_output_file(prefix: str, content: str, output_path: Path, extension: str) -> str:
    """
    Generate a safe filename for output
    
    Args:
        prefix: Prefix for filename (e.g., 'tts', 'audio')
        content: Content to derive filename from
        output_path: Directory where file will be saved
        extension: File extension without dot
        
    Returns:
        Safe filename string
    """
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Clean content for filename (take first 30 chars, remove special chars)
    safe_content = re.sub(r'[^\w\s-]', '', content)[:30]
    safe_content = re.sub(r'[-\s]+', '_', safe_content).strip('_')
    
    # Construct filename
    if safe_content:
        filename = f"{prefix}_{safe_content}_{timestamp}.{extension}"
    else:
        filename = f"{prefix}_{timestamp}.{extension}"
    
    return filename
