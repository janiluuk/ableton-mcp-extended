"""
LocalAI Quick Start Examples

These examples demonstrate how to use the LocalAI integration
directly from Python for testing and automation.
"""

import os
from pathlib import Path
from localai_mcp.client import LocalAIClient

# Configuration
LOCALAI_URL = os.getenv("LOCALAI_BASE_URL", "http://localhost:8080")
OUTPUT_DIR = Path.home() / "Documents" / "Ableton" / "User Library" / "ai_audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize client
client = LocalAIClient(base_url=LOCALAI_URL)


def example_1_text_to_speech():
    """Example 1: Generate speech from text"""
    print("\n=== Example 1: Text to Speech ===")
    
    # Check health
    if not client.check_health():
        print("❌ LocalAI server not available")
        return
    
    print("✓ LocalAI server is healthy")
    
    # Generate speech
    text = "Welcome to my Ableton Live production. Let's create something amazing."
    print(f"Generating speech: {text}")
    
    audio_data = client.text_to_speech(
        text=text,
        voice="alloy",
        speed=1.0
    )
    
    # Save file
    output_file = OUTPUT_DIR / "example_narration.mp3"
    with open(output_file, "wb") as f:
        f.write(audio_data)
    
    print(f"✓ Saved to: {output_file}")
    print("Import to Ableton with: import_audio_file(uri='query:UserLibrary#ai_audio:example_narration.mp3')")


def example_2_list_models():
    """Example 2: List available models"""
    print("\n=== Example 2: List Available Models ===")
    
    models = client.list_models()
    
    if models:
        print(f"Found {len(models)} models:")
        for model in models:
            model_id = model.get("id", "unknown")
            print(f"  - {model_id}")
    else:
        print("No models found or server not configured")


def example_3_generate_audio():
    """Example 3: Generate audio from prompt"""
    print("\n=== Example 3: Generate Audio ===")
    
    if not client.check_health():
        print("❌ LocalAI server not available")
        return
    
    # Generate audio
    prompt = "upbeat electronic music, synthesizer melody, 120 BPM"
    print(f"Generating audio: {prompt}")
    
    try:
        audio_data = client.generate_audio(
            prompt=prompt,
            duration=10.0,
            temperature=1.0
        )
        
        # Save file
        output_file = OUTPUT_DIR / "example_music.wav"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        
        print(f"✓ Saved to: {output_file}")
    except Exception as e:
        print(f"⚠ Audio generation requires MusicGen or similar model: {e}")


def example_4_speech_to_text():
    """Example 4: Transcribe audio (requires audio file)"""
    print("\n=== Example 4: Speech to Text ===")
    
    # Note: This example needs an audio file
    test_audio = OUTPUT_DIR / "example_narration.mp3"
    
    if not test_audio.exists():
        print("⚠ No audio file found. Run example 1 first to generate one.")
        return
    
    if not client.check_health():
        print("❌ LocalAI server not available")
        return
    
    print(f"Transcribing: {test_audio}")
    
    try:
        with open(test_audio, "rb") as f:
            result = client.speech_to_text(
                audio_file=f,
                model="whisper-1"
            )
        
        text = result.get("text", "")
        print(f"✓ Transcription: {text}")
    except Exception as e:
        print(f"⚠ Transcription requires Whisper model: {e}")


if __name__ == "__main__":
    print("LocalAI Quick Start Examples")
    print("=" * 50)
    print(f"Server: {LOCALAI_URL}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 50)
    
    # Run examples
    example_1_text_to_speech()
    example_2_list_models()
    example_3_generate_audio()
    example_4_speech_to_text()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("Check your ai_audio folder for generated files.")
