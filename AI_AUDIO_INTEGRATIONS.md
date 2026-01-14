# AI Audio Generation Integrations

This document describes the new AI audio generation integrations added to Ableton MCP Extended.

## Overview

The project now supports four additional AI audio servers for advanced audio generation, processing, and voice manipulation:

1. **LocalAI** - Open-source OpenAI-compatible API for TTS, STT, and audio generation
2. **ComfyUI** - Workflow-based audio generation using custom workflows
3. **UVR5** - Ultimate Vocal Remover for stem separation (vocals, instrumentals, etc.)
4. **RVC** - Retrieval-based Voice Conversion for voice transformation

## Table of Contents

- [Setup](#setup)
- [LocalAI Integration](#localai-integration)
- [ComfyUI Integration](#comfyui-integration)
- [UVR5 Integration](#uvr5-integration)
- [RVC Integration](#rvc-integration)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

## Setup

### 1. Install Dependencies

```bash
cd ableton-mcp-extended
pip install -e .
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and configure your server URLs:

```bash
cp .env.example .env
```

Edit `.env` with your server endpoints:

```env
# LocalAI Server Configuration
LOCALAI_BASE_URL=http://localhost:8080
LOCALAI_TTS_MODEL=tts-1
LOCALAI_STT_MODEL=whisper-1
LOCALAI_AUDIO_MODEL=musicgen

# ComfyUI Server Configuration
COMFYUI_BASE_URL=http://localhost:8188
COMFYUI_WORKFLOW_PATH=/path/to/comfyui/workflow.json

# UVR5 Server Configuration
UVR5_BASE_URL=http://localhost:5000
UVR5_OUTPUT_DIR=/path/to/your/ableton/user/library/uvr5_audio

# RVC Server Configuration
RVC_BASE_URL=http://localhost:6000
RVC_OUTPUT_DIR=/path/to/your/ableton/user/library/rvc_audio

# Shared Audio Output Configuration
AI_AUDIO_OUTPUT_DIR=/path/to/your/ableton/user/library/ai_audio
```

### 3. Configure AI Assistant

Add the new MCP servers to your AI assistant configuration:

**For Claude Desktop:**

```json
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "python",
      "args": ["C:/path/to/ableton-mcp-extended/MCP_Server/server.py"]
    },
    "LocalAI": {
      "command": "python",
      "args": ["C:/path/to/ableton-mcp-extended/localai_mcp/server.py"]
    },
    "ComfyUI": {
      "command": "python",
      "args": ["C:/path/to/ableton-mcp-extended/comfyui_mcp/server.py"]
    },
    "UVR5": {
      "command": "python",
      "args": ["C:/path/to/ableton-mcp-extended/uvr5_mcp/server.py"]
    },
    "RVC": {
      "command": "python",
      "args": ["C:/path/to/ableton-mcp-extended/rvc_mcp/server.py"]
    }
  }
}
```

## LocalAI Integration

### Description

LocalAI provides open-source, self-hosted alternatives to OpenAI's APIs. It supports text-to-speech, speech-to-text, and audio generation models like MusicGen.

### Server Setup

1. **Install LocalAI:**
   ```bash
   curl https://localai.io/install.sh | sh
   ```

2. **Start LocalAI:**
   ```bash
   local-ai
   ```

3. **Download Models:**
   ```bash
   # For TTS
   local-ai models install tts-1
   
   # For STT (Whisper)
   local-ai models install whisper-1
   
   # For audio generation (MusicGen)
   local-ai models install musicgen
   ```

### Available Tools

- `text_to_speech` - Convert text to speech
- `speech_to_text` - Transcribe audio to text
- `generate_audio` - Generate audio from text prompts
- `check_localai_health` - Check server connectivity
- `list_localai_models` - List available models

### Example Usage

```
👤 "Use LocalAI to generate a voice saying 'Welcome to Ableton Live' and import it into my session"

🤖 "Generating speech with LocalAI... Done! Audio saved to ai_audio folder and imported to track 1"
```

## ComfyUI Integration

### Description

ComfyUI allows you to create custom audio generation workflows with a node-based interface. Perfect for complex audio processing pipelines.

### Server Setup

1. **Install ComfyUI:**
   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI
   cd ComfyUI
   pip install -r requirements.txt
   ```

2. **Start ComfyUI:**
   ```bash
   python main.py
   ```

3. **Create Workflow:**
   - Open http://localhost:8188
   - Design your audio generation workflow
   - Export as JSON and save the path in `.env`

### Available Tools

- `execute_workflow` - Execute a ComfyUI workflow
- `check_comfyui_health` - Check server connectivity
- `get_queue_status` - View current workflow queue

### Example Usage

```
👤 "Run my audio generation workflow with the prompt 'ambient electronic soundscape'"

🤖 "Executing ComfyUI workflow... Workflow completed! Generated: output_001.wav"
```

## UVR5 Integration

### Description

UVR5 (Ultimate Vocal Remover) uses AI models to separate audio into stems: vocals, instrumentals, drums, bass, and more. Essential for remixing and sampling.

### Server Setup

Note: This integration expects a UVR5 API server. You can implement one using the UVR5 library or use existing implementations.

Example server implementation:
```python
# uvr5_server.py
from flask import Flask, request, jsonify
from audio_separator.separator import Separator

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/separate', methods=['POST'])
def separate():
    # Implementation here
    pass

if __name__ == '__main__':
    app.run(port=5000)
```

### Available Tools

- `separate_audio` - Separate audio into stems
- `check_uvr5_health` - Check server connectivity
- `list_uvr5_models` - List available separation models

### Example Usage

```
👤 "Separate the vocals from my_track.wav and import both stems to Ableton"

🤖 "Separating audio with UVR5... Done! Created: my_track_vocals.wav and my_track_instrumental.wav"
```

## RVC Integration

### Description

RVC (Retrieval-based Voice Conversion) transforms voices in audio to match target voice models. Great for voice acting, character voices, and creative effects.

### Server Setup

Note: This integration expects an RVC API server. Reference the `ableton-rvc` project for implementation details.

### Available Tools

- `convert_voice` - Convert voice using RVC model
- `check_rvc_health` - Check server connectivity
- `list_rvc_models` - List available voice models
- `get_rvc_model_info` - Get information about a model

### Example Usage

```
👤 "Convert the voice in vocals.wav to sound like the 'opera_singer' model"

🤖 "Converting voice with RVC... Done! Created: vocals_rvc_opera_singer.wav"
```

## Configuration

### Environment Variables

All configuration is done through environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `LOCALAI_BASE_URL` | LocalAI server URL | http://localhost:8080 |
| `LOCALAI_TTS_MODEL` | Default TTS model | tts-1 |
| `LOCALAI_STT_MODEL` | Default STT model | whisper-1 |
| `LOCALAI_AUDIO_MODEL` | Default audio gen model | musicgen |
| `COMFYUI_BASE_URL` | ComfyUI server URL | http://localhost:8188 |
| `COMFYUI_WORKFLOW_PATH` | Path to workflow JSON | - |
| `UVR5_BASE_URL` | UVR5 server URL | http://localhost:5000 |
| `UVR5_OUTPUT_DIR` | UVR5 output directory | ~/Documents/Ableton/User Library/uvr5_audio |
| `RVC_BASE_URL` | RVC server URL | http://localhost:6000 |
| `RVC_OUTPUT_DIR` | RVC output directory | ~/Documents/Ableton/User Library/rvc_audio |
| `AI_AUDIO_OUTPUT_DIR` | Shared output directory | ~/Documents/Ableton/User Library/ai_audio |

### Output Directories

Audio files are saved to the configured output directories, which can be directly accessed by Ableton Live through the User Library.

To import generated audio into Ableton:
```
"Import the file from ai_audio/localai_tts_welcome_20250114.mp3 to track 1"
```

## Usage Examples

### Example 1: Complete Music Production Workflow

```
👤 "Create a beat using ComfyUI, then use UVR5 to separate it, and finally apply RVC to the vocals"

🤖 "1. Running ComfyUI workflow for beat generation...
    2. Separating stems with UVR5...
    3. Converting vocals with RVC...
    Done! All files imported to Ableton"
```

### Example 2: Podcast Narration

```
👤 "Generate narration with LocalAI: 'This is the intro to my podcast about music production', then clean it up with UVR5"

🤖 "Generated narration and processed. Files ready in Ableton!"
```

### Example 3: Voice Character Creation

```
👤 "Convert my_voice.wav using the 'anime_character' RVC model with +3 pitch"

🤖 "Voice converted with pitch shift +3. Output: my_voice_rvc_anime_character.wav"
```

## Troubleshooting

### Connection Issues

**Problem:** Cannot connect to server

**Solutions:**
1. Check server is running: `curl http://localhost:8080/health` (adjust port)
2. Verify `.env` configuration has correct URLs
3. Check firewall settings
4. Ensure no port conflicts

### Model Not Found

**Problem:** Model not available on server

**Solutions:**
1. List available models: Use the `list_*_models` tool
2. Install required models on the server
3. Update model name in `.env` or tool call

### Audio File Issues

**Problem:** Generated audio not appearing in Ableton

**Solutions:**
1. Check output directory configuration
2. Verify file permissions
3. Refresh Ableton's file browser
4. Check file format compatibility

### Performance Issues

**Problem:** Audio generation takes too long

**Solutions:**
1. Use shorter audio durations
2. Optimize server hardware (GPU recommended)
3. Choose faster models
4. Check server resource usage

## Testing

Run the test suite to verify connectivity:

```bash
# Run all tests
pytest tests/

# Run specific integration tests
pytest tests/test_localai_client.py -v
pytest tests/test_comfyui_client.py -v
pytest tests/test_uvr5_client.py -v
pytest tests/test_rvc_client.py -v
```

## Contributing

To add new integrations or improve existing ones:

1. Create a new client in `{integration}_mcp/client.py`
2. Add MCP tools in `{integration}_mcp/server.py`
3. Write tests in `tests/test_{integration}_client.py`
4. Update documentation

## License

MIT License - Same as the main project
