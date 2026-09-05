#!/usr/bin/env python3
"""
Utility functions and constants
"""

import os
from pathlib import Path
from typing import Dict, Any
import yaml

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
SRC_DIR = BASE_DIR / "src"

# Output subdirectories
SCRIPT_OUTPUT_DIR = OUTPUT_DIR / "scripts"
SCENE_OUTPUT_DIR = OUTPUT_DIR / "scenes"
VOICEOVER_OUTPUT_DIR = OUTPUT_DIR / "voiceovers"
SFX_OUTPUT_DIR = OUTPUT_DIR / "sfx"
FINAL_VIDEO_OUTPUT_DIR = OUTPUT_DIR / "final_videos"

# Create output directories
for dir_path in [SCRIPT_OUTPUT_DIR, SCENE_OUTPUT_DIR, VOICEOVER_OUTPUT_DIR, SFX_OUTPUT_DIR, FINAL_VIDEO_OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Video settings
VIDEO_FPS = 30
VIDEO_RESOLUTION = (1920, 1080)  # 1080p
VIDEO_CODEC = "libx264"
VIDEO_BITRATE = "5000k"

# Audio settings
AUDIO_SAMPLE_RATE = 44100
AUDIO_BITRATE = 192000  # 192 kbps
AUDIO_CHANNELS = 2  # Stereo

# Scene settings
SCENE_DURATION_SECONDS = 5  # Default scene duration
SCENE_TRANSITION_DURATION = 0.5  # Transition between scenes

# Voice-over settings
VOICEOVER_SPEED = 1.0
VOICEOVER_PITCH = 1.0

# Default genres
DEFAULT_GENRE = "k-drama"
AVAILABLE_GENRES = ["c-drama", "k-drama", "us-drama"]

# AI Model settings
VIDEO_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
VOICE_MODEL = "bark"  # or "elevenlabs"
TEXT_MODEL = "meta-llama/Llama-2-7b-hf"

# API timeout
API_TIMEOUT = 300  # 5 minutes


def load_genre_config(genre: str) -> Dict[str, Any]:
    """
    Load genre configuration from YAML file
    
    Args:
        genre: Drama genre (c-drama, k-drama, us-drama)
    
    Returns:
        Genre configuration dictionary
    """
    config_file = CONFIG_DIR / "genres.yaml"
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    if genre not in config['genres']:
        raise ValueError(f"Unknown genre: {genre}. Available: {list(config['genres'].keys())}")
    
    return config['genres'][genre]


def get_voice_style_config(style: str) -> Dict[str, Any]:
    """
    Get voice style configuration
    
    Args:
        style: Voice style name
    
    Returns:
        Voice style configuration dictionary
    """
    config_file = CONFIG_DIR / "genres.yaml"
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    if style not in config['voice_styles']:
        raise ValueError(f"Unknown voice style: {style}")
    
    return config['voice_styles'][style]
