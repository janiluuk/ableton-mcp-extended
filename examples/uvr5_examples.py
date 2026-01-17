"""
UVR5 Quick Start Examples

These examples demonstrate how to use the UVR5 integration
directly from Python for testing and automation.
"""

import os
import io
from pathlib import Path
from uvr5_mcp.client import UVR5Client

# Configuration
UVR5_URL = os.getenv("UVR5_BASE_URL", "http://localhost:5000")
OUTPUT_DIR = Path.home() / "Documents" / "Ableton" / "User Library" / "uvr5_audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize client
client = UVR5Client(base_url=UVR5_URL)


def example_1_check_health():
    """Example 1: Check UVR5 server health"""
    print("\n=== Example 1: Check Server Health ===")
    
    if client.check_health():
        print("✓ UVR5 server is healthy")
        return True
    else:
        print("❌ UVR5 server not available")
        print("Start with: make dev-uvr5")
        return False


def example_2_list_models():
    """Example 2: List available separation models"""
    print("\n=== Example 2: List Separation Models ===")
    
    models = client.list_models()
    
    if models:
        print(f"Available models ({len(models)}):")
        for model in models:
            print(f"  - {model}")
    else:
        print("No models found or server not configured")


def example_3_separate_audio():
    """Example 3: Separate audio into stems"""
    print("\n=== Example 3: Separate Audio ===")
    
    # Create a mock audio file for testing
    print("Creating mock audio file...")
    mock_audio = b'RIFF' + b'\x00' * 4 + b'WAVE' + b'\x00' * 100
    audio_file = io.BytesIO(mock_audio)
    audio_file.name = "test_audio.wav"
    
    # Separate audio
    print("Separating audio...")
    try:
        result = client.separate_audio(
            audio_file=audio_file,
            model_name="UVR-MDX-NET-Inst_HQ_3",
            output_format="wav"
        )
        
        job_id = result.get("job_id")
        if job_id:
            print(f"✓ Separation job created: {job_id}")
            
            # Download stems
            stems_to_get = ["vocals", "instrumental"]
            for stem_type in stems_to_get:
                try:
                    print(f"  Downloading {stem_type} stem...")
                    stem_data = client.download_stem(job_id, stem_type)
                    
                    output_file = OUTPUT_DIR / f"test_{stem_type}.wav"
                    with open(output_file, "wb") as f:
                        f.write(stem_data)
                    
                    print(f"  ✓ Saved: {output_file}")
                except Exception as e:
                    print(f"  ⚠ {stem_type}: {e}")
        else:
            print("✓ Separation completed (immediate result)")
            
    except Exception as e:
        print(f"❌ Separation failed: {e}")


def example_4_get_separation_result():
    """Example 4: Check separation job status"""
    print("\n=== Example 4: Check Job Status ===")
    
    # This would check a real job ID
    job_id = "test-job-id"
    print(f"Checking status for job: {job_id}")
    
    result = client.get_separation_result(job_id)
    status = result.get("status", "unknown")
    
    print(f"Status: {status}")
    
    if status == "completed":
        stems = result.get("stems", {})
        print(f"Available stems: {list(stems.keys())}")


def example_5_workflow():
    """Example 5: Complete workflow"""
    print("\n=== Example 5: Complete Workflow ===")
    print("Typical workflow:")
    print("1. Upload/provide audio file")
    print("2. Select separation model")
    print("3. Initiate separation")
    print("4. Wait for completion")
    print("5. Download separated stems")
    print("6. Import stems to Ableton")
    print("\nFor real files, use:")
    print("  with open('your_audio.wav', 'rb') as f:")
    print("      result = client.separate_audio(f, model_name='...')")


if __name__ == "__main__":
    print("UVR5 Quick Start Examples")
    print("=" * 50)
    print(f"Server: {UVR5_URL}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 50)
    
    # Check if server is available
    if not example_1_check_health():
        print("\nNote: Using mock UVR5 server for testing")
    
    # Run examples
    example_2_list_models()
    example_3_separate_audio()
    example_4_get_separation_result()
    example_5_workflow()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("\nFor production use:")
    print("1. Install UVR5 server (see AI_AUDIO_INTEGRATIONS.md)")
    print("2. Configure UVR5_BASE_URL in .env")
    print("3. Use real audio files for separation")
