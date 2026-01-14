"""
ComfyUI MCP Server

Provides MCP tools for audio generation through ComfyUI workflow execution.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from comfyui_mcp.client import ComfyUIClient

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
COMFYUI_BASE_URL = os.getenv("COMFYUI_BASE_URL", "http://localhost:8188")
COMFYUI_WORKFLOW_PATH = os.getenv("COMFYUI_WORKFLOW_PATH", "")
DEFAULT_OUTPUT_DIR = os.getenv(
    "AI_AUDIO_OUTPUT_DIR",
    os.path.join(Path.home(), "Documents", "Ableton", "User Library", "ai_audio")
)

# Initialize FastMCP server
mcp = FastMCP("ComfyUI")

# Initialize ComfyUI client
client = ComfyUIClient(base_url=COMFYUI_BASE_URL)


@mcp.tool(
    description="""Execute a ComfyUI workflow for audio generation.
    
    Loads and executes a ComfyUI workflow from a JSON file. The workflow should be
    configured for audio generation. Generated files are downloaded and saved locally.
    
    Args:
        workflow_path: Path to workflow JSON file (optional, uses env default)
        prompt_text: Text prompt to use in the workflow (if applicable)
        output_directory: Directory to save generated audio
        max_wait: Maximum time to wait for completion in seconds
        workflow_params: JSON string of additional parameters to inject into workflow
    """
)
def execute_workflow(
    workflow_path: Optional[str] = None,
    prompt_text: Optional[str] = None,
    output_directory: str = DEFAULT_OUTPUT_DIR,
    max_wait: int = 300,
    workflow_params: Optional[str] = None
) -> TextContent:
    """Execute ComfyUI workflow for audio generation"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to ComfyUI server at {COMFYUI_BASE_URL}"
        )
    
    # Use default workflow path if not provided
    wf_path = workflow_path or COMFYUI_WORKFLOW_PATH
    if not wf_path:
        return TextContent(
            type="text",
            text="Error: No workflow path provided. Set COMFYUI_WORKFLOW_PATH or provide workflow_path parameter"
        )
    
    try:
        # Load workflow
        workflow = client.load_workflow(wf_path)
        
        # Inject prompt text if provided
        if prompt_text:
            # Try to find text input nodes and update them
            for node_id, node_data in workflow.items():
                if isinstance(node_data, dict):
                    inputs = node_data.get("inputs", {})
                    if "text" in inputs:
                        inputs["text"] = prompt_text
                        logger.info(f"Updated text input in node {node_id}")
        
        # Inject additional parameters if provided
        if workflow_params:
            import json
            params = json.loads(workflow_params)
            for node_id, param_data in params.items():
                if node_id in workflow:
                    workflow[node_id]["inputs"].update(param_data)
        
        # Queue the workflow
        prompt_id = client.queue_prompt(workflow)
        
        # Wait for completion
        logger.info(f"Waiting for workflow completion (max {max_wait}s)...")
        completed = client.wait_for_completion(prompt_id, max_wait=max_wait)
        
        if not completed:
            return TextContent(
                type="text",
                text=f"Workflow execution timed out after {max_wait}s. Check ComfyUI server."
            )
        
        # Get output files
        output_files = client.get_output_files(prompt_id)
        
        if not output_files:
            return TextContent(
                type="text",
                text="Workflow completed but no output files found"
            )
        
        # Download and save files
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        for file_info in output_files:
            try:
                file_data = client.download_file(
                    filename=file_info["filename"],
                    subfolder=file_info.get("subfolder", "")
                )
                
                # Save file
                save_path = output_path / file_info["filename"]
                with open(save_path, "wb") as f:
                    f.write(file_data)
                
                saved_files.append(str(save_path))
                logger.info(f"Saved {file_info['type']} file: {save_path}")
            except Exception as e:
                logger.error(f"Failed to download file {file_info['filename']}: {e}")
        
        if saved_files:
            files_list = "\n".join(saved_files)
            return TextContent(
                type="text",
                text=f"Workflow completed successfully!\n\nGenerated files:\n{files_list}"
            )
        else:
            return TextContent(
                type="text",
                text="Workflow completed but failed to download output files"
            )
    
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


@mcp.tool(description="Check ComfyUI server health and connectivity")
def check_comfyui_health() -> TextContent:
    """Check if ComfyUI server is accessible"""
    if client.check_health():
        return TextContent(
            type="text",
            text=f"✓ ComfyUI server is healthy at {COMFYUI_BASE_URL}"
        )
    else:
        return TextContent(
            type="text",
            text=f"✗ Cannot connect to ComfyUI server at {COMFYUI_BASE_URL}"
        )


@mcp.tool(description="Get current ComfyUI queue status")
def get_queue_status() -> TextContent:
    """Get current queue status from ComfyUI"""
    if not client.check_health():
        return TextContent(
            type="text",
            text=f"Error: Cannot connect to ComfyUI server at {COMFYUI_BASE_URL}"
        )
    
    try:
        queue_data = client.get_queue()
        
        running = queue_data.get("queue_running", [])
        pending = queue_data.get("queue_pending", [])
        
        status = f"ComfyUI Queue Status:\n"
        status += f"Running: {len(running)} workflows\n"
        status += f"Pending: {len(pending)} workflows\n"
        
        return TextContent(type="text", text=status)
    except Exception as e:
        logger.error(f"Failed to get queue status: {e}")
        return TextContent(type="text", text=f"Error: {str(e)}")


def main():
    """Run the ComfyUI MCP server"""
    logger.info("Starting ComfyUI MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
