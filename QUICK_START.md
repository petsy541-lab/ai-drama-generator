#!/usr/bin/env python3
"""
Getting Started Guide - Quick Start Examples
"""

from src.agent.orchestrator import DramaOrchestrator


def quick_start():
    """
    Quick start guide for AI Drama Generator
    """
    
    print("""
    ✈ AI DRAMA GENERATOR - QUICK START
    
    1. INSTALLATION
    ================
    pip install -r requirements.txt
    
    2. BASIC USAGE
    ==============
    
    Option A: Command Line
    ----------------------
    python main.py --genre k-drama --title "My Drama" --duration 5 --scenes 5
    
    Option B: Python Script
    ----------------------
    from src.agent.drama_agent import DramaAgent
    
    agent = DramaAgent(genre="k-drama")
    video = agent.create_drama(
        title="My First Drama",
        description="A beautiful love story",
        duration_minutes=5,
        num_scenes=5
    )
    
    3. AVAILABLE GENRES
    ===================
    • c-drama    : Chinese dramas (period pieces, martial arts, romance)
    • k-drama    : Korean dramas (romance, revenge, fantasy)
    • us-drama   : American dramas (crime, medical, supernatural)
    
    4. VOICE STYLES
    ===============
    • dramatic   : Serious, slow-paced narration
    • emotional  : Passionate, heartfelt delivery
    • calm       : Peaceful, gentle voiceover
    • intense    : Fast-paced, aggressive tone
    • mysterious : Enigmatic, suspenseful delivery
    • romantic   : Tender, loving narration
    
    5. OUTPUT STRUCTURE
    ===================
    output/
    ├── scripts/          # Generated stories
    ├── scenes/           # Individual video frames
    ├── voiceovers/       # English narrations
    ├── sfx/              # Sound effects & music
    └── final_videos/     # Complete drama videos
    
    6. EXAMPLES
    ===========
    python examples/create_k_drama.py
    python examples/create_c_drama.py
    python examples/create_us_drama.py
    python examples/advanced_custom_drama.py
    python examples/batch_create_dramas.py
    
    7. FREE AI TOOLS USED
    ====================
    • Stable Diffusion   : Video scene generation
    • Bark TTS          : English voice-over generation
    • MoviePy           : Video editing & composition
    • Pydub             : Audio processing
    • Free Music Archive: Background music
    • Freesound.org     : Sound effects
    
    8. TIPS & TRICKS
    ================
    • Start with smaller videos (3-5 minutes) to test
    • Higher emotion_intensity = more dramatic voiceovers
    • Use GPU (cuda) for faster video generation
    • Keep descriptions detailed for better story generation
    • Experiment with different voice styles and music genres
    
    9. TROUBLESHOOTING
    ==================
    Q: Video generation is slow?
    A: This is normal! Reduce num_scenes or duration_minutes.
    
    Q: Model download is stuck?
    A: Check internet connection and available disk space.
    
    Q: Out of memory error?
    A: Reduce batch size or use CPU device (slower but works).
    
    10. DOCUMENTATION
    ==================
    • README.md          : Full project overview
    • examples/          : Working code examples
    • config/genres.yaml : Genre configurations
    
    Happy Drama Creating! 🎬✨
    """)


if __name__ == "__main__":
    quick_start()
