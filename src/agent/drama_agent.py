#!/usr/bin/env python3
"""
Drama Agent Orchestrator - Main agent that coordinates all components
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from src.utils.logger import setup_logger
from src.utils.constants import (
    load_genre_config,
    FINAL_VIDEO_OUTPUT_DIR,
    SCENE_DURATION_SECONDS,
    DEFAULT_GENRE
)
from src.generators.script_generator import ScriptGenerator
from src.generators.voice_generator import VoiceOverGenerator
from src.generators.video_generator import VideoGenerator
from src.generators.sound_effects import SoundEffectsGenerator
from src.editors.video_editor import VideoEditor
from src.editors.audio_mixer import AudioMixer

logger = setup_logger()


@dataclass
class DramaConfig:
    """Configuration for drama generation"""
    genre: str = "k-drama"
    language: str = "english"
    emotion_intensity: float = 0.8
    music_style: str = "orchestral"
    video_quality: str = "1080p"
    add_subtitles: bool = False
    add_title_card: bool = True
    add_credits: bool = True


class DramaAgent:
    """
    Main AI agent that orchestrates drama video creation
    Coordinates: script generation, video creation, voiceover, audio mixing, and video editing
    """
    
    def __init__(
        self,
        genre: str = DEFAULT_GENRE,
        language: str = "english",
        emotion_intensity: float = 0.8,
        music_style: str = "orchestral"
    ):
        """
        Initialize Drama Agent
        
        Args:
            genre: Drama genre (c-drama, k-drama, us-drama)
            language: Language for voiceover (English for narration)
            emotion_intensity: Emotion intensity for voice (0.0-1.0)
            music_style: Background music style
        """
        self.config = DramaConfig(
            genre=genre,
            language=language,
            emotion_intensity=emotion_intensity,
            music_style=music_style
        )
        
        # Initialize components
        self.script_generator = ScriptGenerator(genre=genre)
        self.voice_generator = VoiceOverGenerator(voice_model="bark")
        self.video_generator = VideoGenerator(model="stable-diffusion", device="cpu")
        self.sfx_generator = SoundEffectsGenerator()
        self.video_editor = VideoEditor()
        self.audio_mixer = AudioMixer()
        
        logger.info(f"DramaAgent initialized: {genre.upper()} | Emotion: {emotion_intensity}")
    
    def create_drama(
        self,
        title: str,
        description: str = "",
        duration_minutes: int = 5,
        num_scenes: int = 5,
        voiceover_style: str = "dramatic",
        add_title_card: bool = True,
        add_credits: bool = True
    ) -> Path:
        """
        Create a complete drama video from scratch
        
        Args:
            title: Drama title
            description: Plot description
            duration_minutes: Target video duration in minutes
            num_scenes: Number of scenes to generate
            voiceover_style: Voice style for narration
            add_title_card: Whether to add opening title card
            add_credits: Whether to add ending credits
        
        Returns:
            Path to final video file
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Creating {self.config.genre.upper()} Drama: {title}")
        logger.info(f"Duration: {duration_minutes} min | Scenes: {num_scenes} | Voiceover: {voiceover_style}")
        logger.info(f"{'='*60}\n")
        
        try:
            # Step 1: Generate Script
            logger.info("\n[STEP 1/6] Generating Script...")
            script = self.script_generator.generate_script(
                title=title,
                description=description,
                num_scenes=num_scenes,
                language=self.config.language
            )
            self.script_generator.save_script(script)
            
            # Step 2: Generate Video Scenes
            logger.info("\n[STEP 2/6] Generating Video Scenes...")
            scene_frames = self._generate_all_scenes(script)
            
            # Step 3: Generate Voiceovers
            logger.info("\n[STEP 3/6] Generating Voice-Over...")
            voiceover_paths = self._generate_all_voiceovers(script, voiceover_style)
            
            # Step 4: Generate Sound Effects and Music
            logger.info("\n[STEP 4/6] Generating Sound Effects and Music...")
            music_path = self._generate_music()
            sfx_paths = self._generate_sound_effects(num_scenes)
            
            # Step 5: Mix Audio
            logger.info("\n[STEP 5/6] Mixing Audio...")
            combined_audio = self._mix_audio(voiceover_paths, music_path, sfx_paths)
            
            # Step 6: Compile Final Video
            logger.info("\n[STEP 6/6] Compiling Final Video...")
            final_video = self._compile_final_video(
                scene_frames=scene_frames,
                audio_path=combined_audio,
                title=title,
                add_title_card=add_title_card,
                add_credits=add_credits
            )
            
            logger.info(f"\n{'='*60}")
            logger.success(f"✓ Drama Created Successfully!")
            logger.info(f"Output: {final_video}")
            logger.info(f"{'='*60}\n")
            
            return final_video
        
        except Exception as e:
            logger.error(f"Drama creation failed: {str(e)}")
            raise
    
    def _generate_all_scenes(self, script) -> List[List[Path]]:
        """
        Generate video frames for all scenes
        
        Args:
            script: DramaScript object
        
        Returns:
            List of frame lists for each scene
        """
        all_scene_frames = []
        
        for scene in script.scenes:
            logger.info(f"Generating frames for Scene {scene.number}: {scene.title}")
            
            frames = self.video_generator.generate_scene(
                prompts=scene.visual_prompts,
                scene_number=scene.number,
                num_frames=SCENE_DURATION_SECONDS * 24,  # 24fps
                style=self.config.genre
            )
            
            all_scene_frames.append(frames)
        
        return all_scene_frames
    
    def _generate_all_voiceovers(self, script, voiceover_style: str) -> List[Path]:
        """
        Generate voiceovers for all scenes
        
        Args:
            script: DramaScript object
            voiceover_style: Voice style
        
        Returns:
            List of voiceover file paths
        """
        voiceover_paths = []
        
        for narration in script.voiceover_narration:
            logger.info(f"Generating voiceover for Scene {narration['scene_number']}")
            
            vo_path = self.voice_generator.generate_voiceover(
                text=narration['narrative_text'],
                style=voiceover_style,
                speaker="v2/en_speaker_6"
            )
            
            if vo_path:
                voiceover_paths.append(vo_path)
        
        return voiceover_paths
    
    def _generate_music(self) -> Path:
        """
        Generate background music for entire drama
        
        Returns:
            Path to music file
        """
        logger.info(f"Generating {self.config.music_style} background music...")
        
        music_path = self.sfx_generator.add_background_music(
            duration_seconds=300,  # 5 minutes default
            music_style=self.config.music_style
        )
        
        return music_path
    
    def _generate_sound_effects(self, num_scenes: int) -> List[Path]:
        """
        Generate sound effects for scenes
        
        Args:
            num_scenes: Number of scenes
        
        Returns:
            List of SFX file paths
        """
        sfx_paths = []
        
        # Add dramatic transition SFX between scenes
        for scene_num in range(1, num_scenes):
            logger.info(f"Generating SFX for scene transition {scene_num}...")
            sfx_path = self.sfx_generator.add_sound_effect(
                effect_type="dramatic_whoosh",
                duration_seconds=1.0
            )
            if sfx_path:
                sfx_paths.append(sfx_path)
        
        return sfx_paths
    
    def _mix_audio(
        self,
        voiceover_paths: List[Path],
        music_path: Path,
        sfx_paths: List[Path]
    ) -> Path:
        """
        Combine all audio layers
        
        Args:
            voiceover_paths: List of voiceover files
            music_path: Music file path
            sfx_paths: List of SFX files
        
        Returns:
            Path to combined audio file
        """
        # For simplicity, use first voiceover as base
        if not voiceover_paths:
            logger.warning("No voiceovers found")
            return music_path
        
        # Concatenate voiceovers
        from pydub import AudioSegment
        combined_vo = AudioSegment.empty()
        for vo_path in voiceover_paths:
            try:
                audio = AudioSegment.from_wav(str(vo_path))
                combined_vo += audio
            except Exception as e:
                logger.warning(f"Failed to load voiceover {vo_path}: {e}")
        
        # Mix with music and SFX
        final_audio = self.audio_mixer.mix_audio(
            voiceover_path=voiceover_paths[0] if voiceover_paths else music_path,
            music_path=music_path,
            sfx_paths=sfx_paths[:3],  # Limit SFX to avoid cluttering
            voiceover_volume=1.0,
            music_volume=0.5,
            sfx_volume=0.7
        )
        
        return final_audio
    
    def _compile_final_video(
        self,
        scene_frames: List[List[Path]],
        audio_path: Path,
        title: str,
        add_title_card: bool = True,
        add_credits: bool = True
    ) -> Path:
        """
        Compile all elements into final video
        
        Args:
            scene_frames: List of scene frame lists
            audio_path: Path to combined audio
            title: Drama title
            add_title_card: Whether to add title card
            add_credits: Whether to add credits
        
        Returns:
            Path to final video file
        """
        clips_to_compile = []
        
        # Add title card if requested
        if add_title_card:
            logger.info("Creating title card...")
            title_card = self.video_editor.create_title_card(
                title=title,
                subtitle=f"A {self.config.genre.upper()} Production",
                duration=3.0
            )
            if title_card:
                clips_to_compile.append(title_card)
        
        # Compile main video
        logger.info("Compiling main video...")
        main_video = self.video_editor.compile_video(
            scene_frames=scene_frames,
            audio_path=audio_path,
            title=title
        )
        clips_to_compile.append(main_video)
        
        # Add credits if requested
        if add_credits:
            logger.info("Creating credits roll...")
            credits_data = {
                "Director": ["AI Drama Generator"],
                "Cinematography": ["Stable Diffusion"],
                "Sound Design": ["Bark TTS, Free Music Archive"],
                "Editing": ["MoviePy"],
                "Production": ["petsy541-lab"]
            }
            credits_video = self.video_editor.create_credits_roll(credits_data)
            if credits_video:
                clips_to_compile.append(credits_video)
        
        # Concatenate all clips
        if len(clips_to_compile) > 1:
            logger.info("Concatenating all video segments...")
            from moviepy.editor import concatenate_videoclips, VideoFileClip
            
            video_clips = [VideoFileClip(str(clip)) for clip in clips_to_compile]
            final = concatenate_videoclips(video_clips)
            
            output_path = FINAL_VIDEO_OUTPUT_DIR / f"{title.replace(' ', '_')}_FINAL.mp4"
            final.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            final.close()
            
            return output_path
        else:
            return main_video
