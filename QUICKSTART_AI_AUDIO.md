# Quick Start Guide - AI Audio Integrations

Get started with the new AI audio generation features in under 10 minutes.

## What's New?

Four powerful AI audio integrations:
- **LocalAI** - Open-source TTS, STT, and audio generation
- **ComfyUI** - Custom workflow-based audio generation
- **UVR5** - Stem separation (vocals, instrumentals, etc.)
- **RVC** - Voice conversion and transformation

## Prerequisites

- Ableton MCP Extended already installed and working
- Python 3.10+
- One or more AI audio servers running (see server setup below)

## 5-Minute Setup

### 1. Update Your Installation

```bash
cd ableton-mcp-extended
git pull
pip install -e .
```

### 2. Configure Environment

Copy and edit the environment file:

```bash
cp .env.example .env
# Edit .env with your server URLs
```

Minimal `.env` configuration:
```env
# Use only the services you have running
LOCALAI_BASE_URL=http://localhost:8080
COMFYUI_BASE_URL=http://localhost:8188
UVR5_BASE_URL=http://localhost:5000
RVC_BASE_URL=http://localhost:6000
```

### 3. Add to Your AI Assistant

Add one or more of these servers to your AI assistant config:

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "python",
      "args": ["C:/path/to/MCP_Server/server.py"]
    },
    "LocalAI": {
      "command": "python",
      "args": ["C:/path/to/localai_mcp/server.py"]
    }
  }
}
```

Add ComfyUI, UVR5, or RVC similarly.

### 4. Test It!

Restart your AI assistant and try:

```
"Check LocalAI health"
"Check ComfyUI health"
```

## Server Setup (Choose What You Need)

### LocalAI (Recommended to start)

Easiest to set up, great for TTS and STT:

```bash
# Install
curl https://localai.io/install.sh | sh

# Start
local-ai

# Install models
local-ai models install whisper-1
local-ai models install tts-1
```

Done! LocalAI is ready at http://localhost:8080

### ComfyUI

For custom audio generation workflows:

```bash
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
python main.py
```

ComfyUI UI available at http://localhost:8188

### UVR5

For vocal/instrumental separation (requires implementation):

See `AI_AUDIO_INTEGRATIONS.md` for details on setting up a UVR5 API server.

### RVC

For voice conversion (requires implementation):

Reference the `ableton-rvc` project for RVC server implementation.

## First Tasks

### Example 1: Generate Speech

```
"Use LocalAI to generate speech: 'Welcome to my track' and save it"
```

### Example 2: Transcribe Audio

```
"Use LocalAI to transcribe the file at /path/to/audio.wav"
```

### Example 3: Generate Music

```
"Use LocalAI to generate 10 seconds of ambient electronic music"
```

### Example 4: Separate Vocals (if UVR5 is running)

```
"Separate the vocals from my_song.wav using UVR5"
```

### Example 5: Run ComfyUI Workflow (if configured)

```
"Execute my ComfyUI workflow with the prompt 'upbeat dance music'"
```

## Troubleshooting

**"Cannot connect to server"**
- Make sure the server is running
- Check the URL in your `.env`
- Try: `curl http://localhost:8080/health` (or appropriate port)

**"No tools available"**
- Restart your AI assistant
- Check server is in the config file
- Verify the path to server.py is correct

**"Model not found"**
- Install the required model on the server
- Use the `list_*_models` tool to see available models

## Next Steps

1. Read the full [AI Audio Integrations Guide](AI_AUDIO_INTEGRATIONS.md)
2. Check out [example workflows](examples/)
3. Try combining multiple tools for creative workflows
4. Customize the configurations for your needs

## Common Workflows

**Podcast Production:**
```
1. Generate narration with LocalAI TTS
2. Clean audio with UVR5
3. Import to Ableton and add music
```

**Music Remixing:**
```
1. Separate stems with UVR5
2. Process individual stems
3. Apply voice conversion with RVC
4. Recombine in Ableton
```

**Sound Design:**
```
1. Generate base audio with ComfyUI
2. Separate elements with UVR5
3. Transform with effects
4. Layer in Ableton
```

## Getting Help

- **Full Documentation**: See `AI_AUDIO_INTEGRATIONS.md`
- **GitHub Issues**: Report bugs or request features
- **Examples**: Check the `examples/` directory

Happy creating! 🎵
