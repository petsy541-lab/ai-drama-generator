#!/usr/bin/env python3
"""
Voice-Over Generator - Creates English voice-overs with emotion and style
"""

import os
from pathlib import Path
from typing import List, Dict, Any
import json
from src.utils.logger import setup_logger
from src.utils.constants import (
    VOICEOVER_OUTPUT_DIR,
    AUDIO_SAMPLE_RATE,
    get_voice_style_config
)

logger = setup_logger()


class VoiceOverGenerator:
    """
    Generates professional English voice-overs with emotion and style variation
    Uses free AI tools: Bark, gTTS, or Coqui TTS
    """
    
    def __init__(self, voice_model: str = "bark"):
        """
        Initialize voice-over generator
        
        Args:
            voice_model: Voice model to use (bark, gtts, or coqui)
        """
        self.voice_model = voice_model
        self.supported_models = ["bark", "gtts", "coqui"]
        
        if voice_model not in self.supported_models:
            logger.warning(f"Model {voice_model} not supported, using bark")
            self.voice_model = "bark"
        
        logger.info(f"VoiceOverGenerator initialized with {self.voice_model}")
        self._initialize_model()
    
    def _initialize_model(self):
        """
        Initialize the selected TTS model
        """
        try:
            if self.voice_model == "bark":
                from bark import SAMPLE_RATE, generate_audio, preload_models
                preload_models()
                logger.success("Bark TTS model loaded")
            elif self.voice_model == "gtts":
                from gtts import gTTS
                logger.success("gTTS initialized")
            elif self.voice_model == "coqui":
                from TTS.api import TTS
                self.tts_engine = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=False)
                logger.success("Coqui TTS model loaded")
        except ImportError as e:
            logger.warning(f"Could not load {self.voice_model}: {e}. Install with: pip install {self.voice_model}")
    
    def generate_voiceover(
        self,
        text: str,
        style: str = "dramatic",
        speaker: str = "v2/en_speaker_6",
        output_path: Path = None
    ) -> Path:
        """
        Generate voice-over for given text with style
        
        Args:
            text: Text to convert to speech
            style: Voice style (dramatic, emotional, calm, intense, mysterious, romantic)
            speaker: Speaker voice identifier
            output_path: Path to save audio file
        
        Returns:
            Path to generated audio file
        """
        if output_path is None:
            output_path = VOICEOVER_OUTPUT_DIR / f"voiceover_{len(list(VOICEOVER_OUTPUT_DIR.glob('*.wav')))+1}.wav"
        
        logger.info(f"Generating voiceover: {len(text)} chars, style: {style}")
        
        try:
            if self.voice_model == "bark":
                audio = self._generate_with_bark(text, style, speaker)
            elif self.voice_model == "gtts":
                audio = self._generate_with_gtts(text, output_path)
            elif self.voice_model == "coqui":
                audio = self._generate_with_coqui(text, output_path)
            
            if audio is not None:
                logger.success(f"Voice-over generated: {output_path}")
                return output_path
        except Exception as e:
            logger.error(f"Failed to generate voiceover: {e}")
            raise
    
    def _generate_with_bark(self, text: str, style: str, speaker: str) -> bytes:
        """
        Generate audio using Bark TTS
        
        Args:
            text: Text to convert
            style: Voice style
            speaker: Speaker ID
        
        Returns:
            Audio bytes
        """
        try:
            from bark import generate_audio, SAMPLE_RATE
            import numpy as np
            from scipy.io import wavfile
            
            # Get voice style config for emotion
            style_config = get_voice_style_config(style)
            
            # Add emotional context to the text
            emotional_prompt = f"[{style_config['tone'].upper()}] {text}"
            
            # Generate audio
            audio_array = generate_audio(emotional_prompt, history_prompt=speaker)
            
            logger.success(f"Bark generated audio for style: {style}")
            return audio_array
        except Exception as e:
            logger.error(f"Bark generation failed: {e}")
            return None
    
    def _generate_with_gtts(self, text: str, output_path: Path) -> bool:
        """
        Generate audio using Google Text-to-Speech
        
        Args:
            text: Text to convert
            output_path: Path to save audio
        
        Returns:
            Success status
        """
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(output_path))
            
            logger.success(f"gTTS generated audio to {output_path}")
            return True
        except Exception as e:
            logger.error(f"gTTS generation failed: {e}")
            return False
    
    def _generate_with_coqui(self, text: str, output_path: Path) -> bool:
        """
        Generate audio using Coqui TTS
        
        Args:
            text: Text to convert
            output_path: Path to save audio
        
        Returns:
            Success status
        """
        try:
            self.tts_engine.tts_to_file(text=text, file_path=str(output_path))
            logger.success(f"Coqui generated audio to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Coqui generation failed: {e}")
            return False
    
    def generate_scene_voiceover(
        self,
        scene_data: Dict[str, Any],
        voiceover_style: str = "dramatic"
    ) -> Dict[str, Path]:
        """
        Generate voiceovers for all dialogue in a scene
        
        Args:
            scene_data: Scene data with dialogue
            voiceover_style: Overall voiceover style
        
        Returns:
            Dictionary mapping character names to audio paths
        """
        voiceovers = {}
        
        for dialogue in scene_data.get('dialogue', []):
            character = dialogue['character']
            text = dialogue['text']
            emotion = dialogue.get('emotion', 'neutral')
            
            # Generate voiceover for this dialogue
            audio_path = self.generate_voiceover(
                text=text,
                style=voiceover_style,
                speaker=f"v2/en_speaker_{hash(character) % 10}"
            )
            
            voiceovers[f"{character}_{len(voiceovers)}"] = audio_path
        
        return voiceovers
    
    def adjust_speech_rate(
        self,
        audio_path: Path,
        rate: float = 1.0,
        output_path: Path = None
    ) -> Path:
        """
        Adjust speech rate of audio
        
        Args:
            audio_path: Path to audio file
            rate: Speech rate multiplier (1.0 = normal, 0.8 = slower, 1.2 = faster)
            output_path: Path to save adjusted audio
        
        Returns:
            Path to adjusted audio file
        """
        if output_path is None:
            output_path = VOICEOVER_OUTPUT_DIR / f"adjusted_{audio_path.name}"
        
        try:
            from pydub import AudioSegment
            
            audio = AudioSegment.from_wav(str(audio_path))
            # Speed up or slow down
            adjusted = audio.speedup(playback_speed=rate)
            adjusted.export(str(output_path), format="wav")
            
            logger.success(f"Speech rate adjusted ({rate}x): {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to adjust speech rate: {e}")
            return audio_path
    
    def adjust_pitch(
        self,
        audio_path: Path,
        semitones: float = 0,
        output_path: Path = None
    ) -> Path:
        """
        Adjust pitch of audio
        
        Args:
            audio_path: Path to audio file
            semitones: Pitch adjustment in semitones (0 = no change, positive = higher, negative = lower)
            output_path: Path to save adjusted audio
        
        Returns:
            Path to adjusted audio file
        """
        if output_path is None:
            output_path = VOICEOVER_OUTPUT_DIR / f"pitch_adjusted_{audio_path.name}"
        
        try:
            from pydub import AudioSegment
            import numpy as np
            from scipy import signal
            
            # Load audio and adjust pitch using librosa
            import librosa
            import soundfile as sf
            
            y, sr = librosa.load(str(audio_path))
            y_pitched = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)
            sf.write(str(output_path), y_pitched, sr)
            
            logger.success(f"Pitch adjusted ({semitones} semitones): {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to adjust pitch: {e}")
            return audio_path
