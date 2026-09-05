#!/usr/bin/env python3
"""
Script Generator - Creates drama scripts for different genres
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from src.utils.logger import setup_logger
from src.utils.constants import load_genre_config, SCRIPT_OUTPUT_DIR

logger = setup_logger()


@dataclass
class Scene:
    """Represents a single scene in the drama"""
    number: int
    title: str
    description: str
    setting: str
    characters: List[str]
    dialogue: List[Dict[str, str]]
    visual_prompts: List[str]
    duration_seconds: int = 30
    mood: str = "neutral"


@dataclass
class DramaScript:
    """Complete drama script with multiple scenes"""
    title: str
    genre: str
    description: str
    language: str
    total_duration: int  # minutes
    scenes: List[Scene]
    voiceover_narration: List[Dict[str, str]]


class ScriptGenerator:
    """
    Generates drama scripts with scenes, dialogue, and visual descriptions
    Supports C-Drama, K-Drama, and US Drama genres
    """
    
    def __init__(self, genre: str = "k-drama"):
        """
        Initialize script generator
        
        Args:
            genre: Drama genre (c-drama, k-drama, us-drama)
        """
        self.genre = genre
        self.genre_config = load_genre_config(genre)
        logger.info(f"ScriptGenerator initialized for {genre}")
    
    def generate_script(
        self,
        title: str,
        description: str,
        num_scenes: int = 5,
        language: str = "english"
    ) -> DramaScript:
        """
        Generate a complete drama script
        
        Args:
            title: Drama title
            description: Plot description
            num_scenes: Number of scenes to generate
            language: Language for dialogue and narration (English for voiceover)
        
        Returns:
            DramaScript object
        """
        logger.info(f"Generating script for '{title}' ({num_scenes} scenes)")
        
        scenes = []
        voiceover_narration = []
        
        # Generate scenes
        for scene_num in range(1, num_scenes + 1):
            scene = self._create_scene(
                scene_num,
                title,
                description,
                num_scenes
            )
            scenes.append(scene)
            
            # Create voiceover narration for this scene
            narration = self._create_voiceover_narration(scene)
            voiceover_narration.append(narration)
        
        script = DramaScript(
            title=title,
            genre=self.genre,
            description=description,
            language=language,
            total_duration=num_scenes * 5,  # ~5 minutes per scene
            scenes=scenes,
            voiceover_narration=voiceover_narration
        )
        
        logger.success(f"Script generated: {title}")
        return script
    
    def _create_scene(
        self,
        scene_num: int,
        title: str,
        description: str,
        total_scenes: int
    ) -> Scene:
        """
        Create an individual scene based on genre
        
        Args:
            scene_num: Scene number in the sequence
            title: Drama title
            description: Plot description
            total_scenes: Total number of scenes
        
        Returns:
            Scene object
        """
        settings = self.genre_config['typical_settings']
        characters = self._get_characters_for_scene(scene_num)
        
        # Determine scene mood based on story progression
        mood = self._determine_scene_mood(scene_num, total_scenes)
        
        # Create scene structure
        scene_setting = settings[scene_num % len(settings)]
        scene_title = f"Scene {scene_num}: {self._generate_scene_title(scene_num, total_scenes)}"
        
        scene = Scene(
            number=scene_num,
            title=scene_title,
            description=self._generate_scene_description(scene_num, total_scenes, description),
            setting=scene_setting,
            characters=characters,
            dialogue=self._generate_dialogue(characters, scene_num),
            visual_prompts=self._generate_visual_prompts(scene_setting, mood),
            duration_seconds=30,
            mood=mood
        )
        
        return scene
    
    def _get_characters_for_scene(self, scene_num: int) -> List[str]:
        """
        Get characters for a specific scene based on genre
        
        Args:
            scene_num: Scene number
        
        Returns:
            List of character names
        """
        archetypes = self.genre_config['character_archetypes']
        # Select 2-3 characters per scene
        num_chars = 2 + (scene_num % 2)
        return [
            archetypes[i % len(archetypes)].replace("-", " ").title()
            for i in range(num_chars)
        ]
    
    def _determine_scene_mood(self, scene_num: int, total_scenes: int) -> str:
        """
        Determine mood based on scene position in story
        
        Args:
            scene_num: Current scene number
            total_scenes: Total number of scenes
        
        Returns:
            Mood string
        """
        progress = scene_num / total_scenes
        
        if progress < 0.3:
            return "mysterious"  # Introduction
        elif progress < 0.6:
            return "intense"  # Conflict building
        elif progress < 0.85:
            return "climactic"  # Peak conflict
        else:
            return "resolving"  # Resolution
    
    def _generate_scene_title(self, scene_num: int, total_scenes: int) -> str:
        """
        Generate title for a scene
        
        Args:
            scene_num: Scene number
            total_scenes: Total scenes
        
        Returns:
            Scene title
        """
        plot_elements = self.genre_config['plot_elements']
        element = plot_elements[scene_num % len(plot_elements)]
        return element.replace("-", " ").title()
    
    def _generate_scene_description(self, scene_num: int, total_scenes: int, plot: str) -> str:
        """
        Generate description for a scene
        
        Args:
            scene_num: Scene number
            total_scenes: Total scenes
            plot: Overall plot description
        
        Returns:
            Scene description
        """
        if scene_num == 1:
            return f"Opening scene: Introduction to the world and main character. {plot}"
        elif scene_num == total_scenes:
            return f"Final scene: Resolution and conclusion of the story."
        else:
            return f"Development scene {scene_num}: Advancing the plot and character relationships."
    
    def _generate_dialogue(
        self,
        characters: List[str],
        scene_num: int
    ) -> List[Dict[str, str]]:
        """
        Generate dialogue for characters in a scene
        
        Args:
            characters: List of character names
            scene_num: Scene number
        
        Returns:
            List of dialogue exchanges
        """
        dialogues = []
        
        # Generate 2-3 dialogue exchanges per scene
        for i in range(2 + (scene_num % 2)):
            character = characters[i % len(characters)]
            emotion = ["hopeful", "concerned", "determined", "conflicted"][i % 4]
            
            dialogue_dict = {
                "character": character,
                "emotion": emotion,
                "text": f"[{emotion.capitalize()} tone] Speaking as {character}...",
                "duration_seconds": 5
            }
            dialogues.append(dialogue_dict)
        
        return dialogues
    
    def _generate_visual_prompts(self, setting: str, mood: str) -> List[str]:
        """
        Generate visual prompts for AI image generation
        
        Args:
            setting: Scene setting
            mood: Scene mood
        
        Returns:
            List of visual prompts
        """
        color_palette = self.genre_config['color_palette']
        
        setting_name = setting.replace("-", " ").title()
        mood_name = mood.replace("-", " ").lower()
        colors = ", ".join(color_palette[:2])
        
        prompts = [
            f"Cinematic {setting_name} scene, {mood_name} atmosphere, colors: {colors}, professional lighting, dramatic composition, 4k resolution",
            f"Close-up character emotion, {mood_name} expression, professional cinematography, warm lighting",
            f"Wide establishing shot of {setting_name}, {mood_name} mood, atmospheric, detailed environment"
        ]
        
        return prompts
    
    def _create_voiceover_narration(self, scene: Scene) -> Dict[str, str]:
        """
        Create voiceover narration for a scene
        
        Args:
            scene: Scene object
        
        Returns:
            Voiceover narration dictionary
        """
        return {
            "scene_number": str(scene.number),
            "narrative_text": f"{scene.description} {' '.join([d['text'] for d in scene.dialogue[:2]])}",
            "emotion_tone": scene.mood,
            "duration_seconds": scene.duration_seconds
        }
    
    def save_script(
        self,
        script: DramaScript,
        format: str = "json"
    ) -> Path:
        """
        Save script to file
        
        Args:
            script: DramaScript object
            format: Output format (json or txt)
        
        Returns:
            Path to saved script file
        """
        filename = f"{script.title.replace(' ', '_')}_{self.genre}.json"
        filepath = SCRIPT_OUTPUT_DIR / filename
        
        # Convert to dictionary for JSON serialization
        script_dict = {
            "title": script.title,
            "genre": script.genre,
            "description": script.description,
            "language": script.language,
            "total_duration_minutes": script.total_duration,
            "num_scenes": len(script.scenes),
            "scenes": [
                {
                    "number": s.number,
                    "title": s.title,
                    "description": s.description,
                    "setting": s.setting,
                    "characters": s.characters,
                    "mood": s.mood,
                    "duration_seconds": s.duration_seconds,
                    "visual_prompts": s.visual_prompts,
                    "dialogue": s.dialogue
                }
                for s in script.scenes
            ],
            "voiceover_narration": script.voiceover_narration
        }
        
        with open(filepath, 'w') as f:
            json.dump(script_dict, f, indent=2)
        
        logger.success(f"Script saved to {filepath}")
        return filepath
