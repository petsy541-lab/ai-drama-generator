#!/usr/bin/env python3
"""
Sound Effects Generator - Adds background music and sound effects
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from src.utils.logger import setup_logger
from src.utils.constants import SFX_OUTPUT_DIR, AUDIO_SAMPLE_RATE

logger = setup_logger()


class SoundEffectsGenerator:
    """
    Adds atmospheric sound effects and background music to videos
    Uses free libraries and APIs for music and SFX
    """
    
    def __init__(self):
        """
        Initialize SFX generator
        """
        self.music_libraries = {
            "orchestral": "ambient, orchestral, dramatic",
            "electronic": "synth, electronic, modern",
            "traditional-chinese": "guzheng, ancient, chinese",
            "korean-pop": "k-pop, upbeat, modern",
            "cinematic": "strings, dramatic, cinematic",
            "ambient": "peaceful, ambient, background"
        }
        logger.info("SoundEffectsGenerator initialized")
    
    def add_background_music(
        self,
        duration_seconds: int,
        music_style: str = "cinematic",
        output_path: Path = None
    ) -> Path:
        """
        Generate or fetch background music
        
        Args:
            duration_seconds: Duration of music needed
            music_style: Style of music
            output_path: Path to save music
        
        Returns:
            Path to background music file
        """
        if output_path is None:
            output_path = SFX_OUTPUT_DIR / f"music_{music_style}_{duration_seconds}s.mp3"
        
        logger.info(f"Adding background music: {music_style} ({duration_seconds}s)")
        
        try:
            # Try to use Freesound API or generate with local tools
            music_path = self._fetch_or_generate_music(
                style=music_style,
                duration=duration_seconds,
                output_path=output_path
            )
            
            if music_path:
                logger.success(f"Background music added: {music_path}")
                return music_path
        except Exception as e:
            logger.error(f"Failed to add background music: {e}")
        
        return output_path
    
    def _fetch_or_generate_music(self, style: str, duration: int, output_path: Path) -> Path:
        """
        Fetch music from free sources or generate locally
        
        Args:
            style: Music style
            duration: Duration in seconds
            output_path: Where to save
        
        Returns:
            Path to music file
        """
        try:
            # Try Freesound API
            music_path = self._fetch_from_freesound(style, output_path)
            if music_path:
                return music_path
        except Exception as e:
            logger.warning(f"Freesound fetch failed: {e}")
        
        try:
            # Generate with basic audio synthesis
            music_path = self._generate_music_locally(style, duration, output_path)
            return music_path
        except Exception as e:
            logger.error(f"Music generation failed: {e}")
            return None
    
    def _fetch_from_freesound(self, style: str, output_path: Path) -> Path:
        """
        Fetch music from Freesound.org API
        
        Args:
            style: Music style to search
            output_path: Where to save
        
        Returns:
            Path to downloaded music or None
        """
        try:
            import requests
            
            # Note: Requires FREESOUND_API_KEY environment variable
            api_key = os.getenv('FREESOUND_API_KEY')
            if not api_key:
                logger.warning("FREESOUND_API_KEY not set")
                return None
            
            # Search for music
            url = f"https://freesound.org/apiv2/search/text/"
            params = {
                "query": style,
                "filter": "duration:[30 TO 600]",
                "sort": "rating_desc",
                "token": api_key,
                "page_size": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    sound_url = results[0]['previews']['preview-hq-mp3']
                    audio = requests.get(sound_url)
                    
                    with open(output_path, 'wb') as f:
                        f.write(audio.content)
                    
                    logger.success(f"Music fetched from Freesound: {output_path}")
                    return output_path
        except Exception as e:
            logger.warning(f"Freesound API failed: {e}")
        
        return None
    
    def _generate_music_locally(self, style: str, duration: int, output_path: Path) -> Path:
        """
        Generate music locally using synthesis
        
        Args:
            style: Music style
            duration: Duration in seconds
            output_path: Where to save
        
        Returns:
            Path to generated music
        """
        try:
            import numpy as np
            from scipy.io import wavfile
            
            # Generate simple ambient music
            sample_rate = 44100
            num_samples = sample_rate * duration
            
            t = np.linspace(0, duration, num_samples)
            
            # Create layered tones for ambient music
            if style == "orchestral":
                # Slow strings-like sound
                freq1, freq2, freq3 = 55, 110, 165  # Low notes
                audio = 0.3 * np.sin(2 * np.pi * freq1 * t)
                audio += 0.2 * np.sin(2 * np.pi * freq2 * t)
                audio += 0.1 * np.sin(2 * np.pi * freq3 * t)
            
            elif style == "electronic":
                # Synth sounds
                freq1, freq2 = 440, 880
                audio = 0.3 * np.sin(2 * np.pi * freq1 * t)
                audio += 0.2 * np.cos(2 * np.pi * freq2 * t * (1 + 0.1 * np.sin(2 * np.pi * 0.5 * t)))
            
            else:  # Default ambient
                # Ambient pad
                freq = 110
                audio = 0.2 * np.sin(2 * np.pi * freq * t)
                audio += 0.15 * np.sin(2 * np.pi * freq * 1.5 * t)
            
            # Normalize
            audio = audio / np.max(np.abs(audio)) * 0.9
            
            # Convert to 16-bit PCM
            audio_int16 = np.int16(audio * 32767)
            
            # Save as WAV
            wavfile.write(str(output_path), sample_rate, audio_int16)
            logger.success(f"Music generated locally: {output_path}")
            
            return output_path
        except Exception as e:
            logger.error(f"Local music generation failed: {e}")
            return None
    
    def add_sound_effect(
        self,
        effect_type: str,
        duration_seconds: float = 1.0,
        output_path: Path = None
    ) -> Path:
        """
        Add a sound effect
        
        Args:
            effect_type: Type of effect (dramatic_whoosh, scene_transition, emotional_swell, etc)
            duration_seconds: Duration of effect
            output_path: Path to save
        
        Returns:
            Path to sound effect file
        """
        if output_path is None:
            output_path = SFX_OUTPUT_DIR / f"sfx_{effect_type}_{duration_seconds}s.wav"
        
        logger.info(f"Generating sound effect: {effect_type}")
        
        try:
            sfx_path = self._generate_sound_effect(effect_type, duration_seconds, output_path)
            if sfx_path:
                logger.success(f"Sound effect created: {sfx_path}")
                return sfx_path
        except Exception as e:
            logger.error(f"Failed to create sound effect: {e}")
        
        return output_path
    
    def _generate_sound_effect(self, effect_type: str, duration: float, output_path: Path) -> Path:
        """
        Generate sound effect using synthesis
        
        Args:
            effect_type: Type of effect
            duration: Duration in seconds
            output_path: Where to save
        
        Returns:
            Path to sound effect
        """
        try:
            import numpy as np
            from scipy.io import wavfile
            
            sample_rate = 44100
            num_samples = int(sample_rate * duration)
            t = np.linspace(0, duration, num_samples)
            
            if effect_type == "dramatic_whoosh":
                # Swooshing sound with frequency sweep
                freq_start, freq_end = 200, 50
                freq = freq_start - (freq_start - freq_end) * t / duration
                audio = np.sin(2 * np.pi * freq * t) * np.exp(-t / duration)
            
            elif effect_type == "scene_transition":
                # Transition effect
                audio = np.sin(2 * np.pi * 440 * t) * np.exp(-3 * t / duration)
            
            elif effect_type == "emotional_swell":
                # Building emotional sound
                audio = np.sin(2 * np.pi * 110 * t) * (1 - np.exp(-3 * t / duration))
            
            elif effect_type == "tension_build":
                # Tension building effect
                freq = 220 + 220 * (1 - np.exp(-2 * t / duration))
                audio = np.sin(2 * np.pi * freq * t) * 0.8
            
            else:  # Default effect
                audio = np.sin(2 * np.pi * 440 * t) * np.exp(-t / duration)
            
            # Normalize
            audio = audio / np.max(np.abs(audio)) * 0.9
            audio_int16 = np.int16(audio * 32767)
            
            wavfile.write(str(output_path), sample_rate, audio_int16)
            return output_path
        except Exception as e:
            logger.error(f"Sound effect generation failed: {e}")
            return None
    
    def mix_audio_layers(
        self,
        voiceover_path: Path,
        music_path: Path,
        sfx_paths: List[Path] = None,
        output_path: Path = None,
        voiceover_volume: float = 1.0,
        music_volume: float = 0.5,
        sfx_volume: float = 0.8
    ) -> Path:
        """
        Mix voiceover, music, and sound effects
        
        Args:
            voiceover_path: Path to voiceover audio
            music_path: Path to background music
            sfx_paths: List of sound effect paths
            output_path: Path to save mixed audio
            voiceover_volume: Voiceover volume multiplier
            music_volume: Music volume multiplier
            sfx_volume: SFX volume multiplier
        
        Returns:
            Path to mixed audio file
        """
        if output_path is None:
            output_path = SFX_OUTPUT_DIR / "mixed_audio.wav"
        
        if sfx_paths is None:
            sfx_paths = []
        
        logger.info(f"Mixing audio layers: voiceover + music + {len(sfx_paths)} effects")
        
        try:
            from pydub import AudioSegment
            
            # Load audio files
            voiceover = AudioSegment.from_wav(str(voiceover_path)) if voiceover_path.suffix == '.wav' else AudioSegment.from_file(str(voiceover_path))
            music = AudioSegment.from_wav(str(music_path)) if music_path.suffix == '.wav' else AudioSegment.from_file(str(music_path))
            
            # Adjust volumes
            voiceover = voiceover + (20 * np.log10(voiceover_volume)) if voiceover_volume > 0 else voiceover
            music = music + (20 * np.log10(music_volume)) if music_volume > 0 else music
            
            # Composite audio (overlay)
            # Make sure all have same length
            max_length = max(len(voiceover), len(music))
            voiceover = voiceover.pad(max_length)
            music = music.pad(max_length)
            
            # Mix
            mixed = voiceover.overlay(music)
            
            # Add sound effects
            for sfx_path in sfx_paths:
                try:
                    sfx = AudioSegment.from_wav(str(sfx_path)) if sfx_path.suffix == '.wav' else AudioSegment.from_file(str(sfx_path))
                    sfx = sfx + (20 * np.log10(sfx_volume)) if sfx_volume > 0 else sfx
                    mixed = mixed.overlay(sfx)
                except Exception as e:
                    logger.warning(f"Failed to add SFX {sfx_path}: {e}")
            
            # Export
            mixed.export(str(output_path), format="wav")
            logger.success(f"Audio mixed successfully: {output_path}")
            
            return output_path
        except Exception as e:
            logger.error(f"Audio mixing failed: {e}")
            return voiceover_path
