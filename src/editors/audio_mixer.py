#!/usr/bin/env python3
"""
Audio Mixer - Mix voiceover, music, and sound effects
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from src.utils.logger import setup_logger
from src.utils.constants import VOICEOVER_OUTPUT_DIR

logger = setup_logger()


class AudioMixer:
    """
    Mixes multiple audio layers (voiceover, music, SFX)
    """
    
    def __init__(self):
        """
        Initialize audio mixer
        """
        logger.info("AudioMixer initialized")
    
    def mix_audio(
        self,
        voiceover_path: Path,
        music_path: Path,
        sfx_paths: List[Path] = None,
        output_path: Path = None,
        voiceover_volume: float = 1.0,
        music_volume: float = 0.5,
        sfx_volume: float = 0.7
    ) -> Path:
        """
        Mix audio layers with volume control
        
        Args:
            voiceover_path: Path to voiceover audio
            music_path: Path to background music
            sfx_paths: List of sound effect paths
            output_path: Path to save mixed audio
            voiceover_volume: Voiceover volume (0-1+)
            music_volume: Music volume (0-1)
            sfx_volume: SFX volume (0-1)
        
        Returns:
            Path to mixed audio file
        """
        if output_path is None:
            output_path = VOICEOVER_OUTPUT_DIR / "final_audio.mp3"
        
        if sfx_paths is None:
            sfx_paths = []
        
        logger.info(f"Mixing audio: voiceover + music + {len(sfx_paths)} effects")
        
        try:
            from pydub import AudioSegment
            import numpy as np
            
            # Load main audio files
            voiceover = self._load_audio(voiceover_path)
            music = self._load_audio(music_path)
            
            if voiceover is None or music is None:
                logger.error("Failed to load audio files")
                return None
            
            # Adjust volumes
            voiceover = self._adjust_volume(voiceover, voiceover_volume)
            music = self._adjust_volume(music, music_volume)
            
            # Ensure same length by padding or cropping
            max_length = max(len(voiceover), len(music))
            voiceover = self._match_length(voiceover, max_length)
            music = self._match_length(music, max_length)
            
            # Mix voiceover and music
            mixed = voiceover.overlay(music)
            
            # Add sound effects
            for sfx_path in sfx_paths:
                try:
                    sfx = self._load_audio(sfx_path)
                    if sfx:
                        sfx = self._adjust_volume(sfx, sfx_volume)
                        mixed = mixed.overlay(sfx)
                except Exception as e:
                    logger.warning(f"Failed to add SFX {sfx_path}: {e}")
            
            # Export
            format_type = output_path.suffix.strip('.')
            mixed.export(str(output_path), format=format_type)
            
            logger.success(f"Audio mixed successfully: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Audio mixing failed: {e}")
            return None
    
    def _load_audio(self, audio_path: Path):
        """
        Load audio file
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            AudioSegment object or None
        """
        try:
            from pydub import AudioSegment
            
            if not audio_path.exists():
                logger.warning(f"Audio file not found: {audio_path}")
                return None
            
            # Auto-detect format
            audio = AudioSegment.from_file(str(audio_path))
            return audio
        except Exception as e:
            logger.error(f"Failed to load audio {audio_path}: {e}")
            return None
    
    def _adjust_volume(self, audio, volume: float):
        """
        Adjust audio volume
        
        Args:
            audio: AudioSegment object
            volume: Volume multiplier (0-1+)
        
        Returns:
            Adjusted audio
        """
        if volume == 1.0:
            return audio
        
        # Volume in dB = 20 * log10(volume)
        db_adjustment = 20 * __import__('math').log10(max(volume, 0.01))
        return audio + db_adjustment
    
    def _match_length(self, audio, target_length: int):
        """
        Match audio length by padding or cropping
        
        Args:
            audio: AudioSegment object
            target_length: Target length in milliseconds
        
        Returns:
            Matched audio
        """
        current_length = len(audio)
        if current_length > target_length:
            return audio[:target_length]
        elif current_length < target_length:
            silence = AudioSegment.silent(duration=target_length - current_length)
            return audio + silence
        return audio
    
    def normalize_audio(self, audio_path: Path, output_path: Path = None) -> Path:
        """
        Normalize audio to standard loudness
        
        Args:
            audio_path: Path to audio file
            output_path: Path to save normalized audio
        
        Returns:
            Path to normalized audio
        """
        if output_path is None:
            output_path = VOICEOVER_OUTPUT_DIR / f"normalized_{audio_path.name}"
        
        logger.info(f"Normalizing audio: {audio_path}")
        
        try:
            from pydub import AudioSegment
            from pydub.utils import mediainfo
            
            audio = AudioSegment.from_file(str(audio_path))
            
            # Get current loudness and normalize to -20dBFS
            target_loudness = -20
            current_loudness = audio.dBFS
            loudness_diff = target_loudness - current_loudness
            
            normalized = audio + loudness_diff
            
            # Export
            format_type = audio_path.suffix.strip('.')
            normalized.export(str(output_path), format=format_type)
            
            logger.success(f"Audio normalized: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Audio normalization failed: {e}")
            return audio_path
