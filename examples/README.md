# Examples

This directory contains example files and configurations for the AI audio integrations.

## ComfyUI Workflow Example

`comfyui_audio_workflow_example.json` - A sample ComfyUI workflow for audio generation using MusicGen.

### How to use:

1. Open ComfyUI in your browser (http://localhost:8188)
2. Load this workflow JSON file
3. Modify the nodes as needed for your use case
4. Export and save the modified workflow
5. Set `COMFYUI_WORKFLOW_PATH` in your `.env` to point to your workflow file
6. Use the `execute_workflow` tool to run it

### Workflow Nodes:

- **LoadAudio**: Loads an audio file (optional for conditioning)
- **AudioPrompt**: Defines the text prompt and parameters
- **MusicGenNode**: Generates audio using MusicGen model
- **SaveAudio**: Saves the generated audio

Note: The actual node types and connections may vary depending on your ComfyUI setup and available custom nodes. This is a conceptual example.

## Creating Your Own Workflows

ComfyUI workflows can be customized for various audio tasks:

- Music generation with different models (MusicGen, AudioCraft, etc.)
- Audio effects processing
- Style transfer
- Sound design
- Multi-stage audio processing pipelines

Refer to the [AI Audio Integrations Guide](../AI_AUDIO_INTEGRATIONS.md) for more information.
