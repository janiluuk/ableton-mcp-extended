# Usage Examples for AI Audio Integrations

This guide provides practical examples for using each AI audio integration with Ableton MCP Extended.

## Table of Contents

1. [LocalAI Examples](#localai-examples)
2. [ComfyUI Examples](#comfyui-examples)
3. [UVR5 Examples](#uvr5-examples)
4. [RVC Examples](#rvc-examples)
5. [Combined Workflows](#combined-workflows)

---

## LocalAI Examples

LocalAI provides text-to-speech, speech-to-text, and audio generation capabilities.

### Example 1: Generate Speech for Narration

**Scenario**: Create a voiceover for your track intro.

**Steps**:
1. Start LocalAI server (or use Docker: `make dev-localai`)
2. In your AI assistant (Claude/Cursor):

```
Use LocalAI to generate speech with the text:
"Welcome to my latest production. This track explores ambient soundscapes with organic textures."

Save it to my ai_audio folder and use the 'nova' voice.
```

**What happens**:
- LocalAI generates speech audio
- File saved as `localai_tts_Welcome_to_my_20250115.mp3`
- Ready to import into Ableton

**Import to Ableton**:
```
Import the file localai_tts_Welcome_to_my_20250115.mp3 from ai_audio folder to track 1
```

### Example 2: Transcribe Audio for Lyrics

**Scenario**: Extract lyrics from a vocal recording.

**Steps**:
```
Use LocalAI to transcribe the audio file at /path/to/vocals.wav
Save the transcript to a file.
```

**What happens**:
- LocalAI processes the audio using Whisper
- Returns transcribed text
- Saves transcript as `localai_stt_vocals_20250115.txt`

### Example 3: Generate Background Music

**Scenario**: Create ambient background music.

**Steps**:
```
Use LocalAI to generate 30 seconds of ambient electronic music.
The prompt should be: "soft ambient pads with gentle arpeggios, peaceful atmosphere"
```

**What happens**:
- LocalAI uses MusicGen model
- Generates 30-second audio clip
- Saves as `localai_audio_soft_ambient_20250115.wav`

### Example 4: Multi-Language Narration

**Scenario**: Create narration in different languages.

**Steps**:
```
Use LocalAI to generate speech in Spanish:
"Bienvenido a mi nueva producción musical"

Then generate the same in English:
"Welcome to my new music production"

Save both to the ai_audio folder.
```

**Use Case**: Create bilingual content or language learning materials.

### Example 5: Check Available Models

**Steps**:
```
List available models on LocalAI server
```

**What happens**:
- Shows all installed TTS, STT, and audio generation models
- Helps you choose the right model for your needs

---

## ComfyUI Examples

ComfyUI enables workflow-based audio generation with custom node graphs.

### Example 1: Generate Audio with Stable Audio Workflow

**Scenario**: Use the Stable Audio workflow for high-quality audio generation.

**Setup**:
1. The workflow file is at `examples/stable_audio_workflow.json`
2. Set environment variable: `COMFYUI_WORKFLOW_PATH=/path/to/examples/stable_audio_workflow.json`

**Steps**:
```
Execute my ComfyUI workflow with the prompt:
"cinematic orchestral buildup, epic strings, powerful brass, dramatic percussion"

Set duration to 10 seconds.
```

**What happens**:
- ComfyUI loads the Stable Audio workflow
- Injects your prompt into text nodes
- Executes the workflow
- Downloads generated audio

### Example 2: Generate Multiple Variations

**Scenario**: Create several variations of a sound.

**Steps**:
```
Execute my ComfyUI workflow 3 times with these prompts:
1. "aggressive techno kick, punchy and distorted"
2. "deep sub bass, wobbling and modulated"
3. "crisp hi-hats, metallic and sharp"

Generate each as a 5-second sample.
```

**What happens**:
- Runs workflow multiple times
- Each with different prompt
- Creates library of samples

### Example 3: Check Workflow Queue

**Scenario**: Monitor ongoing generations.

**Steps**:
```
Check the ComfyUI queue status
```

**What happens**:
- Shows running workflows
- Shows pending workflows
- Helps manage generation queue

### Example 4: Custom Workflow Parameters

**Scenario**: Fine-tune generation parameters.

**Steps**:
```
Execute my ComfyUI workflow with:
- Prompt: "ambient drone, evolving pad sounds"
- Duration: 20 seconds
- Additional parameters: {"temperature": 0.8, "cfg_scale": 7.5}
```

**What happens**:
- Injects custom parameters into workflow
- Provides fine control over generation

### Example 5: Import Generated Audio to Ableton

**Complete workflow**:
```
1. Execute my ComfyUI workflow with prompt "dark techno bass loop"
2. Wait for completion
3. Import the generated file to track 5 in Ableton
4. Set the track name to "ComfyUI Bass"
```

**What happens**:
- Generates audio
- Automatically imports to Ableton
- Names track appropriately

---

## UVR5 Examples

UVR5 provides AI-powered stem separation for extracting vocals, instrumentals, and more.

### Example 1: Extract Vocals and Instrumental

**Scenario**: Separate a full mix for remixing.

**Steps**:
```
Use UVR5 to separate the audio file at /path/to/fullmix.wav

Extract both vocals and instrumental stems.
Use the UVR-MDX-NET-Inst_HQ_3 model for best quality.
```

**What happens**:
- UVR5 separates the audio
- Creates `fullmix_vocals.wav`
- Creates `fullmix_instrumental.wav`
- Saves both to uvr5_audio folder

### Example 2: Import Separated Stems to Ableton

**Complete workflow**:
```
1. Use UVR5 to separate /path/to/track.wav into vocals and instrumental
2. Import the vocals stem to track 3 in Ableton
3. Import the instrumental stem to track 4 in Ableton
4. Name track 3 "Vocals" and track 4 "Instrumental"
```

**What happens**:
- Separates audio
- Imports both stems to Ableton
- Sets up tracks for remixing

### Example 3: Multi-Stem Separation

**Scenario**: Extract drums, bass, vocals, and other elements.

**Steps**:
```
Use UVR5 to separate /path/to/song.wav

I need to extract all available stems: vocals, instrumental, drums, and bass if possible.
Use the best available model for multi-stem separation.
```

**What happens**:
- Separates into multiple stems
- Each saved as separate file
- Ready for detailed remixing

### Example 4: Check Available Models

**Steps**:
```
List available separation models on UVR5
```

**What happens**:
- Shows all installed separation models
- Displays model names and purposes
- Helps choose the right model

### Example 5: Batch Separation

**Scenario**: Separate multiple tracks.

**Steps**:
```
Use UVR5 to separate these files:
1. /path/to/track1.wav
2. /path/to/track2.wav
3. /path/to/track3.wav

Extract vocals and instrumental from each.
```

**What happens**:
- Processes each file
- Creates organized stem files
- Ready for production workflow

---

## RVC Examples

RVC provides AI voice conversion to transform voices with custom models.

### Example 1: Apply Voice Character

**Scenario**: Transform a vocal recording to a different character.

**Steps**:
```
Use RVC to convert the voice in /path/to/vocals.wav

Apply the 'anime_character' model.
Keep the original pitch.
```

**What happens**:
- RVC processes the audio
- Applies voice transformation
- Saves as `vocals_rvc_anime_character.wav`

### Example 2: Pitch Shift with Voice Conversion

**Scenario**: Convert voice and adjust pitch.

**Steps**:
```
Use RVC to convert /path/to/male_vocal.wav using the 'opera_singer' model

Shift the pitch up by 5 semitones.
Use high quality settings (index_rate: 0.8).
```

**What happens**:
- Converts voice to opera singer character
- Raises pitch by 5 semitones
- High-quality conversion

### Example 3: Check Available Voice Models

**Steps**:
```
List all available voice models on RVC
```

**What happens**:
- Shows all installed voice models
- Displays model names and descriptions
- Helps you choose the right voice

### Example 4: Get Model Information

**Steps**:
```
Get detailed information about the 'test_model' voice model on RVC
```

**What happens**:
- Shows model version
- Shows model description
- Displays model metadata

### Example 5: Create Vocal Variations

**Scenario**: Create multiple character voices from one recording.

**Steps**:
```
Use RVC to convert /path/to/original_vocal.wav with these models:
1. anime_character (no pitch shift)
2. opera_singer (+3 semitones)
3. test_model (-2 semitones)

Save each with descriptive names.
```

**What happens**:
- Creates 3 different character voices
- Each with different pitch
- Ready for creative projects

---

## Combined Workflows

These examples combine multiple services for complete production workflows.

### Workflow 1: Podcast Production

**Scenario**: Create a complete podcast episode with AI.

**Steps**:
```
1. Use LocalAI to generate narration:
   "Welcome to episode 5 of Tech Talks. Today we're discussing AI in music production."

2. Use LocalAI to generate background music:
   "soft corporate background music, upbeat and positive"

3. Import both to Ableton tracks 1 and 2

4. Use UVR5 to separate any intro music I have at /path/to/intro.wav

5. Import the intro music instrumental to track 3
```

**Result**: Complete podcast setup with AI-generated content.

### Workflow 2: Remix Creation

**Scenario**: Create a remix from a full track.

**Steps**:
```
1. Use UVR5 to separate /path/to/original_track.wav into vocals and instrumental

2. Use RVC to convert the vocals using the 'test_model' voice

3. Use ComfyUI to generate a new bassline:
   Prompt: "deep dubstep bass, wobbling and aggressive"

4. Import all stems to Ableton:
   - Converted vocals to track 1
   - Original instrumental to track 2  
   - New bassline to track 3

5. Name the tracks appropriately
```

**Result**: Remix project with AI-processed vocals and generated elements.

### Workflow 3: Music Video Narration

**Scenario**: Create voiceover for a music video.

**Steps**:
```
1. Use LocalAI to transcribe the dialogue from /path/to/rough_vocal.wav

2. Edit the transcription and use LocalAI to generate clean narration:
   [paste edited transcript]
   Use the 'nova' voice.

3. Use UVR5 to clean up any background noise by separating vocals

4. Import the clean narration to track 1 in Ableton

5. Use ComfyUI to generate ambient background:
   "cinematic ambient pad, emotional and atmospheric"

6. Import background to track 2
```

**Result**: Professional voiceover with atmospheric background.

### Workflow 4: Sound Design Library

**Scenario**: Create a library of sound effects.

**Steps**:
```
1. Use ComfyUI to generate these sound effects (5 seconds each):
   - "explosion sound effect, dramatic and powerful"
   - "whoosh transition, fast and clean"
   - "ambient texture, evolving and mysterious"

2. Use LocalAI to generate:
   - "warning siren, urgent and attention-grabbing"

3. Organize all generated sounds in Ableton:
   - Create a track for each sound
   - Add descriptive names
   - Group related sounds
```

**Result**: Organized sound effects library ready for use.

### Workflow 5: Voice Acting Project

**Scenario**: Create multiple character voices for a project.

**Steps**:
```
1. Use LocalAI to generate base dialogue:
   "Hello, I'm here to help you today."

2. Use RVC to create character variations:
   - anime_character model
   - opera_singer model  
   - test_model

3. Use UVR5 to clean each voice if needed

4. Import all character voices to separate Ableton tracks

5. Use ComfyUI to generate background ambience:
   "fantasy tavern ambience, warm and cozy"

6. Import ambience and mix with character voices
```

**Result**: Multi-character voice project with ambience.

---

## Tips for Best Results

### LocalAI Tips
- **TTS**: Shorter phrases (under 500 chars) work best
- **STT**: Clear audio improves transcription accuracy
- **Audio Gen**: Descriptive prompts yield better results

### ComfyUI Tips
- **Workflows**: Test workflows in ComfyUI UI first
- **Prompts**: Be specific about desired sound characteristics
- **Duration**: Start with shorter durations (5-10s)

### UVR5 Tips
- **Models**: HQ models take longer but sound better
- **Format**: WAV format recommended for best quality
- **Stems**: Extract only the stems you need

### RVC Tips
- **Quality**: Higher index_rate = more target voice character
- **Pitch**: Small adjustments (±3 semitones) sound more natural
- **Protection**: Use voiceless protection for clearer consonants

### General Tips
- **Import Path**: Use "query:UserLibrary#ai_audio:filename.mp3" for Ableton import
- **Organization**: Name tracks descriptively
- **Backup**: Keep generated files organized
- **Iteration**: Generate multiple variations and choose the best

---

## Environment Configuration

Make sure your `.env` file is configured:

```env
# LocalAI
LOCALAI_BASE_URL=http://localhost:8080
LOCALAI_TTS_MODEL=tts-1
LOCALAI_STT_MODEL=whisper-1
LOCALAI_AUDIO_MODEL=musicgen

# ComfyUI
COMFYUI_BASE_URL=http://localhost:8188
COMFYUI_WORKFLOW_PATH=/path/to/examples/stable_audio_workflow.json

# UVR5
UVR5_BASE_URL=http://localhost:5000
UVR5_OUTPUT_DIR=/path/to/ableton/user/library/uvr5_audio

# RVC
RVC_BASE_URL=http://localhost:6000
RVC_OUTPUT_DIR=/path/to/ableton/user/library/rvc_audio

# Shared
AI_AUDIO_OUTPUT_DIR=/path/to/ableton/user/library/ai_audio
```

---

## Quick Reference Commands

### Start Services (Docker)
```bash
make dev-localai      # LocalAI only
make dev-comfyui      # ComfyUI only
make dev-uvr5         # UVR5 mock only
make dev-rvc          # RVC mock only
make setup            # All services
```

### Health Checks
```
Check LocalAI health
Check ComfyUI health
Check UVR5 health
Check RVC health
```

### List Resources
```
List LocalAI models
List ComfyUI queue status
List UVR5 separation models
List RVC voice models
```

---

## Troubleshooting

**Issue**: Generated files not appearing in Ableton
- Check output directory configuration
- Verify file permissions
- Refresh Ableton's file browser

**Issue**: Service connection failed
- Verify service is running
- Check URL in .env file
- Test with health check command

**Issue**: Poor quality results
- Try different models
- Adjust quality parameters
- Use higher quality input files

---

## Next Steps

1. Try the basic examples for each service
2. Experiment with combined workflows
3. Create your own workflows
4. Share your results!

For more details, see:
- [AI_AUDIO_INTEGRATIONS.md](../AI_AUDIO_INTEGRATIONS.md) - Technical documentation
- [QUICKSTART_AI_AUDIO.md](../QUICKSTART_AI_AUDIO.md) - Quick setup guide
- [DOCKER_E2E_GUIDE.md](../DOCKER_E2E_GUIDE.md) - Docker and testing guide
