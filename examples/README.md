# Examples

This directory contains example files, configurations, and usage guides for the AI audio integrations.

## 📚 Documentation

### [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
**Complete usage guide with practical examples for all integrations**

Includes:
- **LocalAI Examples**: TTS, STT, audio generation (5 examples)
- **ComfyUI Examples**: Workflow-based generation (5 examples)
- **UVR5 Examples**: Stem separation (5 examples)
- **RVC Examples**: Voice conversion (5 examples)
- **Combined Workflows**: Multi-service production workflows (5 workflows)
- Tips, troubleshooting, and quick reference

**Perfect for**: Learning how to use each service and creating complete production workflows.

## 🎵 ComfyUI Workflows

### comfyui_audio_workflow_example.json
A basic ComfyUI workflow template for audio generation using MusicGen.

**Nodes:**
- LoadAudio - Loads audio file (optional for conditioning)
- AudioPrompt - Defines text prompt and parameters
- MusicGenNode - Generates audio using MusicGen model
- SaveAudio - Saves generated audio

### stable_audio_workflow.json
**Professional Stable Audio workflow for high-quality audio generation**

This is a production-ready workflow using Stable Audio with:
- CLIP text encoding for precise control
- Configurable duration (5-30 seconds typical)
- High-quality audio output
- Multiple parameter controls

**Features:**
- Text prompt support
- Duration control
- Quality settings
- Professional results

**Usage with AI assistant:**
```
Execute my ComfyUI workflow with prompt "epic orchestral music" and duration 10 seconds
```

**Configuration:**
Set in your `.env`:
```env
COMFYUI_WORKFLOW_PATH=/path/to/examples/stable_audio_workflow.json
```

## 🚀 Quick Start Examples

### LocalAI - Generate Speech
```
Use LocalAI to generate speech: "Welcome to my production"
Save it with the nova voice
```

### ComfyUI - Generate Audio
```
Execute my ComfyUI workflow with prompt "ambient electronic soundscape"
Set duration to 15 seconds
```

### UVR5 - Separate Vocals
```
Use UVR5 to separate /path/to/song.wav
Extract vocals and instrumental stems
```

### RVC - Convert Voice
```
Use RVC to convert /path/to/vocal.wav using anime_character model
Apply pitch shift of +3 semitones
```

## 📁 File Descriptions

| File | Type | Purpose |
|------|------|---------|
| `USAGE_EXAMPLES.md` | Guide | Comprehensive usage examples |
| `stable_audio_workflow.json` | Workflow | Professional Stable Audio workflow |
| `comfyui_audio_workflow_example.json` | Workflow | Basic MusicGen template |
| `README.md` | Guide | This file |

## 🎯 How to Use

### 1. **Start with USAGE_EXAMPLES.md**
Read through the examples to understand capabilities and workflows.

### 2. **Configure Your Environment**
Set up `.env` with your server URLs and workflow paths.

### 3. **Try Basic Examples**
Start with simple single-service examples:
- Generate speech with LocalAI
- Separate stems with UVR5
- Convert voice with RVC

### 4. **Experiment with Workflows**
Try the ComfyUI workflows:
- Test in ComfyUI UI first
- Then use via AI assistant
- Modify parameters as needed

### 5. **Create Combined Workflows**
Combine multiple services:
- Generate → Separate → Convert
- Build complete production pipelines

## 🔧 Workflow Customization

### Modify Existing Workflows

1. **Open in ComfyUI UI**: http://localhost:8188
2. **Load workflow**: Use "Load" button
3. **Edit nodes**: Adjust parameters, add/remove nodes
4. **Save**: Export as JSON
5. **Update .env**: Point to your custom workflow

### Create New Workflows

1. **Design in ComfyUI**: Create node graph
2. **Test thoroughly**: Verify it works
3. **Export**: Save as JSON
4. **Document**: Add description and usage notes
5. **Share**: Save in examples directory

## 💡 Tips for Best Results

### LocalAI
- Keep TTS prompts under 500 characters
- Use clear audio for STT
- Descriptive prompts for audio generation

### ComfyUI
- Test workflows in UI before automation
- Start with short durations (5-10s)
- Be specific in prompts

### UVR5
- Use WAV format for best quality
- HQ models produce better results
- Extract only needed stems

### RVC
- Small pitch adjustments sound natural
- Higher index_rate = more character
- Use voiceless protection for clarity

## 🔗 Related Documentation

- [AI_AUDIO_INTEGRATIONS.md](../AI_AUDIO_INTEGRATIONS.md) - Technical details
- [QUICKSTART_AI_AUDIO.md](../QUICKSTART_AI_AUDIO.md) - 5-minute setup
- [DOCKER_E2E_GUIDE.md](../DOCKER_E2E_GUIDE.md) - Docker setup

## 🎨 Example Workflows by Use Case

### Music Production
- Generate backing tracks
- Create drum samples
- Design synth sounds
- Build sound effects library

### Podcast Production
- Generate narration
- Create intro/outro music
- Add voiceovers
- Clean audio

### Sound Design
- Create unique textures
- Generate SFX
- Design ambient sounds
- Build layered soundscapes

### Voice Acting
- Generate character voices
- Apply voice effects
- Create variations
- Process dialogue

### Remixing
- Separate original tracks
- Transform vocals
- Generate new elements
- Build arrangements

## 📞 Support

For questions or issues:
1. Check [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for examples
2. Review [AI_AUDIO_INTEGRATIONS.md](../AI_AUDIO_INTEGRATIONS.md) for troubleshooting
3. Test services with health checks
4. Check service logs

## 🎉 Get Started

```bash
# Start services
make setup

# Try first example
# In your AI assistant:
"Check LocalAI health"
"Use LocalAI to generate speech: 'Hello from Ableton'"

# Import to Ableton
"Import the generated file to track 1"
```

Happy creating! 🎵
