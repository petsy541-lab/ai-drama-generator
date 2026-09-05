#!/usr/bin/env python3
"""
Video Editor - Compiles scenes into complete video with transitions
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
from src.utils.logger import setup_logger
from src.utils.constants import (
    FINAL_VIDEO_OUTPUT_DIR,
    VIDEO_FPS,
    VIDEO_RESOLUTION,
    SCENE_TRANSITION_DURATION
)

logger = setup_logger()


class VideoEditor:
    """
    Edits video scenes and compiles them into final drama
    Uses MoviePy for video composition and FFmpeg for encoding
    """
    
    def __init__(self):
        """
        Initialize video editor
        """
        logger.info("VideoEditor initialized")
    
    def compile_video(
        self,
        scene_frames: List[List[Path]],
        audio_path: Path,
        title: str = "Drama",
        fps: int = VIDEO_FPS,
        resolution: Tuple[int, int] = VIDEO_RESOLUTION
    ) -> Path:
        """
        Compile multiple scenes into a complete video
        
        Args:
            scene_frames: List of frame lists for each scene
            audio_path: Path to combined audio (voiceover + music + SFX)
            title: Video title
            fps: Frames per second
            resolution: Video resolution (width, height)
        
        Returns:
            Path to compiled video file
        """
        logger.info(f"Compiling video: {title}")
        
        try:
            from moviepy.editor import (
                ImageSequenceClip,
                concatenate_videoclips,
                AudioFileClip,
                CompositeAudioClip
            )
            
            # Create video clips from frame sequences
            video_clips = []
            
            for scene_num, frames in enumerate(scene_frames):
                logger.info(f"Processing scene {scene_num + 1}/{len(scene_frames)}")
                
                if not frames:
                    logger.warning(f"Scene {scene_num + 1} has no frames, skipping")
                    continue
                
                # Create video clip from frames
                frame_paths = [str(f) for f in frames]
                clip = ImageSequenceClip(frame_paths, fps=fps)
                
                # Add transition if not first scene
                if scene_num > 0:
                    clip = self._add_transition(clip, SCENE_TRANSITION_DURATION)
                
                video_clips.append(clip)
            
            if not video_clips:
                raise ValueError("No valid video clips to compile")
            
            # Concatenate all clips
            final_video = concatenate_videoclips(video_clips)
            
            # Add audio
            if audio_path.exists():
                audio = AudioFileClip(str(audio_path))
                final_video = final_video.set_audio(audio)
            
            # Set resolution
            final_video = final_video.resize(newsize=resolution)
            
            # Export
            output_path = FINAL_VIDEO_OUTPUT_DIR / f"{title.replace(' ', '_')}.mp4"
            
            logger.info(f"Exporting video to {output_path}")
            final_video.write_videofile(
                str(output_path),
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Cleanup
            final_video.close()
            if audio_path.exists():
                audio.close()
            
            logger.success(f"Video compiled successfully: {output_path}")
            return output_path
        
        except ImportError:
            logger.error("MoviePy not installed. Install with: pip install moviepy")
            raise
        except Exception as e:
            logger.error(f"Video compilation failed: {e}")
            raise
    
    def _add_transition(
        self,
        clip,
        duration: float = 0.5,
        transition_type: str = "fade"
    ):
        """
        Add transition effect to clip
        
        Args:
            clip: Video clip
            duration: Transition duration in seconds
            transition_type: Type of transition (fade, slide, etc)
        
        Returns:
            Clip with transition applied
        """
        try:
            if transition_type == "fade":
                # Fade in at start
                clip = clip.fadein(duration)
            elif transition_type == "slide":
                # Slide transition (simplified)
                pass
            
            return clip
        except Exception as e:
            logger.warning(f"Failed to add transition: {e}")
            return clip
    
    def add_subtitles(
        self,
        video_path: Path,
        subtitles: List[Dict[str, Any]],
        output_path: Path = None
    ) -> Path:
        """
        Add subtitles to video
        
        Args:
            video_path: Path to video file
            subtitles: List of subtitle dictionaries with start, end, text
            output_path: Path to save subtitled video
        
        Returns:
            Path to video with subtitles
        """
        if output_path is None:
            output_path = FINAL_VIDEO_OUTPUT_DIR / f"subtitled_{video_path.name}"
        
        logger.info(f"Adding {len(subtitles)} subtitle entries to video")
        
        try:
            from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
            
            # Load video
            video = VideoFileClip(str(video_path))
            
            # Create text clips for each subtitle
            text_clips = []
            for sub in subtitles:
                txt_clip = TextClip(
                    txt=sub['text'],
                    fontsize=24,
                    color='white',
                    font='Arial',
                    stroke_color='black',
                    stroke_width=2
                )
                txt_clip = txt_clip.set_position(('center', 'bottom'))
                txt_clip = txt_clip.set_duration(sub['end'] - sub['start'])
                txt_clip = txt_clip.set_start(sub['start'])
                text_clips.append(txt_clip)
            
            # Composite with original video
            final = CompositeVideoClip([video] + text_clips)
            
            # Export
            final.write_videofile(
                str(output_path),
                fps=video.fps,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            video.close()
            final.close()
            
            logger.success(f"Subtitles added: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to add subtitles: {e}")
            return video_path
    
    def create_title_card(
        self,
        title: str,
        subtitle: str = "",
        duration: float = 3.0,
        resolution: Tuple[int, int] = VIDEO_RESOLUTION,
        output_path: Path = None
    ) -> Path:
        """
        Create an opening title card
        
        Args:
            title: Main title text
            subtitle: Subtitle text
            duration: Duration in seconds
            resolution: Video resolution
            output_path: Path to save video
        
        Returns:
            Path to title card video
        """
        if output_path is None:
            output_path = FINAL_VIDEO_OUTPUT_DIR / f"title_{title.replace(' ', '_')}.mp4"
        
        logger.info(f"Creating title card: {title}")
        
        try:
            from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
            
            # Create background
            background = ColorClip(size=resolution, color=(10, 10, 30))  # Dark blue
            background = background.set_duration(duration)
            
            # Create title text
            title_clip = TextClip(
                txt=title,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                stroke_color='gold',
                stroke_width=3
            )
            title_clip = title_clip.set_position(('center', 0.4), relative=True)
            title_clip = title_clip.set_duration(duration)
            
            # Create subtitle text if provided
            clips = [background, title_clip]
            if subtitle:
                subtitle_clip = TextClip(
                    txt=subtitle,
                    fontsize=30,
                    color='white',
                    font='Arial'
                )
                subtitle_clip = subtitle_clip.set_position(('center', 0.6), relative=True)
                subtitle_clip = subtitle_clip.set_duration(duration)
                clips.append(subtitle_clip)
            
            # Composite and export
            final = CompositeVideoClip(clips)
            final.write_videofile(
                str(output_path),
                fps=VIDEO_FPS,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            final.close()
            logger.success(f"Title card created: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to create title card: {e}")
            return None
    
    def create_credits_roll(
        self,
        credits_data: Dict[str, List[str]],
        duration: float = 10.0,
        resolution: Tuple[int, int] = VIDEO_RESOLUTION,
        output_path: Path = None
    ) -> Path:
        """
        Create ending credits roll
        
        Args:
            credits_data: Dictionary with credit categories and names
            duration: Duration in seconds
            resolution: Video resolution
            output_path: Path to save video
        
        Returns:
            Path to credits video
        """
        if output_path is None:
            output_path = FINAL_VIDEO_OUTPUT_DIR / "credits.mp4"
        
        logger.info("Creating credits roll")
        
        try:
            from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
            
            # Create background
            background = ColorClip(size=resolution, color=(0, 0, 0))  # Black
            background = background.set_duration(duration)
            
            # Build credits text
            credits_text = "\n\n"
            for category, names in credits_data.items():
                credits_text += f"{category.upper()}\n"
                for name in names:
                    credits_text += f"  {name}\n"
                credits_text += "\n"
            
            # Create credits clip
            credits_clip = TextClip(
                txt=credits_text,
                fontsize=20,
                color='white',
                font='Arial',
                method='caption',
                size=(resolution[0]-100, resolution[1])
            )
            credits_clip = credits_clip.set_position(('center', 'center'))
            credits_clip = credits_clip.set_duration(duration)
            
            # Composite
            final = CompositeVideoClip([background, credits_clip])
            final.write_videofile(
                str(output_path),
                fps=VIDEO_FPS,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            final.close()
            logger.success(f"Credits roll created: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to create credits: {e}")
            return None
