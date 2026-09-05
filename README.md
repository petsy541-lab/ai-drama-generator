# AI Drama Generator Agent

An intelligent AI agent that creates realistic drama videos with multiple genres (C-Drama, K-Drama, US Drama) featuring:
- **AI Video Generation** - Creates scenes with AI characters
- **Voice-Over Generation** - English voice-overs with emotion and tone
- **Sound Effects** - Adds atmospheric music and SFX
- **Video Editing** - Compiles multiple scenes into a complete drama
- **Multi-Genre Support** - C-Drama, K-Drama, US Drama storytelling

## Features

✨ **Multi-Genre Drama Creation**
- C-Drama (period pieces, romance, political intrigue)
- K-Drama (romance, revenge, slice-of-life)
- US Drama (crime, medical, supernatural)

🎬 **Complete Video Production Pipeline**
- Script generation based on drama type
- AI character and scene generation
- Professional voice-over creation
- Dynamic sound effects and music
- Automatic video compilation and editing

🎯 **Free AI Tools Integration**
- Hugging Face for text generation
- ElevenLabs free tier for voice-over (or Bark)
- Stable Diffusion for visual generation
- MoviePy for video editing
- Pydub for audio processing

## Project Structure

```
ai-drama-generator/
├── config/
│   ├── genres.yaml
│   ├── characters.yaml
│   └── settings.yaml
├── src/
│   ├── agent/
│   │   ├── drama_agent.py
│   │   └── orchestrator.py
│   ├── generators/
│   │   ├── script_generator.py
│   │   ├── video_generator.py
│   │   ├── voice_generator.py
│   │   └── sound_effects.py
│   ├── editors/
│   │   ├── video_editor.py
│   │   └── audio_mixer.py
│   └── utils/
│       ├── file_manager.py
│       ├── logger.py
│       └── constants.py
├── output/
│   ├── scripts/
│   ├── scenes/
│   ├── voiceovers/
│   ├── sfx/
│   └── final_videos/
├── requirements.txt
├── main.py
└── README.md
```

## Installation

```bash
git clone https://github.com/petsy541-lab/ai-drama-generator.git
cd ai-drama-generator
pip install -r requirements.txt
```

## Quick Start

```bash
python main.py --genre k-drama --duration 5 --title "Love Across Time"
```

## Environment Setup

Create a `.env` file with API keys:

```env
HUGGINGFACE_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
STABILITY_API_KEY=your_key_here
```

## Usage

### Basic Usage

```python
from src.agent.drama_agent import DramaAgent

agent = DramaAgent(genre="c-drama")
final_video = agent.create_drama(
    title="The Forbidden Palace",
    duration_minutes=3,
    num_scenes=5
)
```

### Advanced Options

```python
agent = DramaAgent(
    genre="k-drama",
    language="english",
    emotion_intensity=0.8,
    music_style="orchestral"
)

video = agent.create_drama(
    title="Winter Romance",
    description="A love story in Seoul during winter",
    duration_minutes=5,
    num_scenes=8,
    voiceover_style="dramatic",
    add_subtitles=True
)
```

## Workflow

1. **Script Generation** → Story tailored to drama genre
2. **Scene Planning** → Visual storyboard creation
3. **Video Generation** → AI creates scene visuals
4. **Voice-Over Creation** → Emotional English narration
5. **Sound Design** → Background music + SFX
6. **Video Compilation** → Seamless scene integration
7. **Final Export** → High-quality drama video

## Supported Drama Types

### C-Drama
- Ancient/Period pieces
- Martial arts and fantasy
- Political intrigue
- Romance

### K-Drama
- Contemporary romance
- Revenge plots
- Fantasy/supernatural
- Slice-of-life

### US Drama
- Crime procedural
- Medical drama
- Supernatural thriller
- Workplace drama

## Free Tools Used

- **Hugging Face** - Text generation, story creation
- **Bark/ElevenLabs** - Voice synthesis
- **Stable Diffusion** - Image generation
- **MoviePy** - Video composition and editing
- **Pydub** - Audio processing
- **FFmpeg** - Video encoding
- **Free Music Archive** - Background music
- **Freesound.org** - Sound effects

## Output

All generated content is saved in the `output/` directory:
- Scripts (txt, json)
- Scene images (png)
- Voice files (mp3, wav)
- Final videos (mp4)

## Contributing

Contributions are welcome! Please fork and submit pull requests.

## License

MIT License

## Roadmap

- [ ] Multi-language support
- [ ] Real-time voice emotion adjustment
- [ ] Custom character creation
- [ ] 3D character animation support
- [ ] Music composition AI
- [ ] Subtitle generation and translation
- [ ] Interactive drama branching
- [ ] Web UI dashboard

## Contact

For questions and suggestions, please open an issue on GitHub.
