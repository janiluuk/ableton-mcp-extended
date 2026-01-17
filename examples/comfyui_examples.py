"""
ComfyUI Quick Start Examples

These examples demonstrate how to use the ComfyUI integration
directly from Python for testing and automation.
"""

import os
import json
from pathlib import Path
from comfyui_mcp.client import ComfyUIClient

# Configuration
COMFYUI_URL = os.getenv("COMFYUI_BASE_URL", "http://localhost:8188")
WORKFLOW_PATH = Path(__file__).parent / "stable_audio_workflow.json"
OUTPUT_DIR = Path.home() / "Documents" / "Ableton" / "User Library" / "ai_audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize client
client = ComfyUIClient(base_url=COMFYUI_URL)


def example_1_check_health():
    """Example 1: Check ComfyUI server health"""
    print("\n=== Example 1: Check Server Health ===")
    
    if client.check_health():
        print("✓ ComfyUI server is healthy")
        return True
    else:
        print("❌ ComfyUI server not available")
        return False


def example_2_get_queue():
    """Example 2: Check queue status"""
    print("\n=== Example 2: Queue Status ===")
    
    queue = client.get_queue()
    
    running = queue.get("queue_running", [])
    pending = queue.get("queue_pending", [])
    
    print(f"Running workflows: {len(running)}")
    print(f"Pending workflows: {len(pending)}")


def example_3_execute_workflow():
    """Example 3: Execute workflow"""
    print("\n=== Example 3: Execute Workflow ===")
    
    if not WORKFLOW_PATH.exists():
        print(f"⚠ Workflow not found: {WORKFLOW_PATH}")
        print("Please ensure stable_audio_workflow.json exists in examples/")
        return
    
    # Load workflow
    print(f"Loading workflow: {WORKFLOW_PATH}")
    workflow = client.load_workflow(str(WORKFLOW_PATH))
    
    # Modify prompt in workflow
    prompt = "epic cinematic music, orchestral strings, powerful drums"
    print(f"Injecting prompt: {prompt}")
    
    # Try to find and update text input nodes
    for node_id, node_data in workflow.items():
        if isinstance(node_data, dict):
            inputs = node_data.get("inputs", {})
            if "text" in inputs:
                inputs["text"] = prompt
                print(f"  Updated node {node_id}")
    
    # Queue workflow
    print("Queueing workflow...")
    try:
        prompt_id = client.queue_prompt(workflow)
        print(f"✓ Queued with ID: {prompt_id}")
        
        # Wait for completion
        print("Waiting for completion (max 60s)...")
        completed = client.wait_for_completion(prompt_id, max_wait=60)
        
        if completed:
            print("✓ Workflow completed!")
            
            # Get output files
            files = client.get_output_files(prompt_id)
            print(f"Generated {len(files)} file(s)")
            
            # Download files
            for file_info in files:
                filename = file_info["filename"]
                print(f"  Downloading: {filename}")
                
                file_data = client.download_file(filename)
                output_path = OUTPUT_DIR / filename
                
                with open(output_path, "wb") as f:
                    f.write(file_data)
                
                print(f"  ✓ Saved to: {output_path}")
        else:
            print("⚠ Workflow did not complete in time")
            
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")


def example_4_workflow_with_params():
    """Example 4: Execute workflow with custom parameters"""
    print("\n=== Example 4: Workflow with Parameters ===")
    
    if not WORKFLOW_PATH.exists():
        print(f"⚠ Workflow not found: {WORKFLOW_PATH}")
        return
    
    # Load workflow
    workflow = client.load_workflow(str(WORKFLOW_PATH))
    
    # Custom parameters
    prompt = "ambient electronic soundscape, evolving pads"
    duration = 15.0
    
    print(f"Prompt: {prompt}")
    print(f"Duration: {duration}s")
    
    # Update workflow
    for node_id, node_data in workflow.items():
        if isinstance(node_data, dict):
            inputs = node_data.get("inputs", {})
            if "text" in inputs:
                inputs["text"] = prompt
            if "duration" in inputs:
                inputs["duration"] = duration
    
    print("Parameters injected into workflow")
    print("(Would queue here - skipping to avoid long execution)")


if __name__ == "__main__":
    print("ComfyUI Quick Start Examples")
    print("=" * 50)
    print(f"Server: {COMFYUI_URL}")
    print(f"Workflow: {WORKFLOW_PATH}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 50)
    
    # Check if server is available
    if not example_1_check_health():
        print("\n❌ ComfyUI server is not running.")
        print("Start it with: make dev-comfyui")
        exit(1)
    
    # Run examples
    example_2_get_queue()
    example_3_execute_workflow()
    example_4_workflow_with_params()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("Check your ai_audio folder for generated files.")
