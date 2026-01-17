"""
RVC Quick Start Examples

These examples demonstrate how to use the RVC integration
directly from Python for testing and automation.
"""

import os
import io
from pathlib import Path
from rvc_mcp.client import RVCClient

# Configuration
RVC_URL = os.getenv("RVC_BASE_URL", "http://localhost:6000")
OUTPUT_DIR = Path.home() / "Documents" / "Ableton" / "User Library" / "rvc_audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize client
client = RVCClient(base_url=RVC_URL)


def example_1_check_health():
    """Example 1: Check RVC server health"""
    print("\n=== Example 1: Check Server Health ===")
    
    if client.check_health():
        print("✓ RVC server is healthy")
        return True
    else:
        print("❌ RVC server not available")
        print("Start with: make dev-rvc")
        return False


def example_2_list_models():
    """Example 2: List available voice models"""
    print("\n=== Example 2: List Voice Models ===")
    
    models = client.list_models()
    
    if models:
        print(f"Available voice models ({len(models)}):")
        for model in models:
            if isinstance(model, dict):
                name = model.get("name", "unknown")
                info = model.get("info", "")
                print(f"  - {name}: {info}")
            else:
                print(f"  - {model}")
    else:
        print("No models found or server not configured")


def example_3_get_model_info():
    """Example 3: Get detailed model information"""
    print("\n=== Example 3: Get Model Info ===")
    
    model_name = "test_model"
    print(f"Getting info for: {model_name}")
    
    try:
        info = client.get_model_info(model_name)
        print(f"  Name: {info.get('name')}")
        print(f"  Version: {info.get('version')}")
        print(f"  Description: {info.get('description')}")
    except Exception as e:
        print(f"  ⚠ {e}")


def example_4_convert_voice():
    """Example 4: Convert voice"""
    print("\n=== Example 4: Convert Voice ===")
    
    # Create mock audio file for testing
    print("Creating mock audio file...")
    mock_audio = b'RIFF' + b'\x00' * 4 + b'WAVE' + b'\x00' * 100
    audio_file = io.BytesIO(mock_audio)
    audio_file.name = "test_vocal.wav"
    
    # Convert voice
    model_name = "test_model"
    pitch_shift = 3
    
    print(f"Converting voice with:")
    print(f"  Model: {model_name}")
    print(f"  Pitch shift: {pitch_shift:+d} semitones")
    
    try:
        converted_audio = client.convert_voice(
            audio_file=audio_file,
            model_name=model_name,
            pitch_shift=pitch_shift,
            index_rate=0.75,
            rms_mix_rate=0.25
        )
        
        # Save converted audio
        output_file = OUTPUT_DIR / f"test_converted_{model_name}.wav"
        with open(output_file, "wb") as f:
            f.write(converted_audio)
        
        print(f"✓ Converted audio saved: {output_file}")
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")


def example_5_advanced_conversion():
    """Example 5: Advanced conversion with parameters"""
    print("\n=== Example 5: Advanced Conversion ===")
    
    print("Advanced parameters:")
    print("  pitch_shift: Adjust pitch in semitones (-12 to +12)")
    print("  filter_radius: Smoothing filter (0-7)")
    print("  index_rate: Feature retrieval ratio (0.0-1.0)")
    print("    Higher = more target voice character")
    print("  rms_mix_rate: Volume envelope mix (0.0-1.0)")
    print("  protect_voiceless: Protect consonants (0.0-0.5)")
    
    print("\nExample configuration:")
    config = {
        "model_name": "anime_character",
        "pitch_shift": 5,
        "filter_radius": 3,
        "index_rate": 0.8,
        "rms_mix_rate": 0.25,
        "protect_voiceless": 0.5
    }
    
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print("\nUse these settings for:")
    print("  - Natural sound: index_rate=0.6-0.75")
    print("  - Strong character: index_rate=0.8-1.0")
    print("  - Clear speech: protect_voiceless=0.3-0.5")


def example_6_workflow():
    """Example 6: Complete workflow"""
    print("\n=== Example 6: Complete Workflow ===")
    print("Typical workflow:")
    print("1. List available voice models")
    print("2. Select appropriate model")
    print("3. Load vocal audio file")
    print("4. Configure conversion parameters")
    print("5. Convert voice")
    print("6. Save converted audio")
    print("7. Import to Ableton")
    print("\nFor real files, use:")
    print("  with open('vocal.wav', 'rb') as f:")
    print("      result = client.convert_voice(")
    print("          f, model_name='anime_character',")
    print("          pitch_shift=3, index_rate=0.75")
    print("      )")


if __name__ == "__main__":
    print("RVC Quick Start Examples")
    print("=" * 50)
    print(f"Server: {RVC_URL}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 50)
    
    # Check if server is available
    if not example_1_check_health():
        print("\nNote: Using mock RVC server for testing")
    
    # Run examples
    example_2_list_models()
    example_3_get_model_info()
    example_4_convert_voice()
    example_5_advanced_conversion()
    example_6_workflow()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("\nFor production use:")
    print("1. Install RVC server (see ableton-rvc project)")
    print("2. Configure RVC_BASE_URL in .env")
    print("3. Load voice models")
    print("4. Use real vocal files for conversion")
