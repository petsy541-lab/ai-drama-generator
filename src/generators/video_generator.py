#!/usr/bin/env python3
"""
Video Generator - Creates AI-generated video scenes using Stable Diffusion
"""

import os
from pathlib import Path
from typing import List, Dict, Any
import json
from src.utils.logger import setup_logger
from src.utils.constants import (
    SCENE_OUTPUT_DIR,
    VIDEO_RESOLUTION,
    VIDEO_FPS
)

logger = setup_logger()


class VideoGenerator:
    """
    Generates video scenes from prompts using AI image generation
    Uses Stable Diffusion or similar free models
    """
    
    def __init__(self, model: str = "stable-diffusion", device: str = "cpu"):
        """
        Initialize video generator
        
        Args:
            model: Model to use for image generation
            device: Device to run on (cpu or cuda)
        """
        self.model = model
        self.device = device
        logger.info(f"VideoGenerator initialized with {model} on {device}")
        self._initialize_model()
    
    def _initialize_model(self):
        """
        Initialize the Stable Diffusion model
        """
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            model_id = "runwayml/stable-diffusion-v1-5"
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float32
            )
            self.pipe.to(self.device)
            logger.success("Stable Diffusion model loaded")
        except ImportError:
            logger.warning("Diffusers not installed. Install with: pip install diffusers torch")
            self.pipe = None
    
    def generate_scene(
        self,
        prompts: List[str],
        scene_number: int = 1,
        num_frames: int = 30,
        style: str = "cinematic"
    ) -> List[Path]:
        """
        Generate multiple frames for a video scene
        
        Args:
            prompts: List of visual prompts for frame generation
            scene_number: Scene identifier
            num_frames: Number of frames to generate
            style: Visual style
        
        Returns:
            List of paths to generated image frames
        """
        logger.info(f"Generating scene {scene_number} with {num_frames} frames")
        
        frame_paths = []
        
        try:
            for frame_num in range(num_frames):
                # Select prompt based on frame position
                prompt = prompts[frame_num % len(prompts)]
                
                # Generate frame
                frame_path = self._generate_frame(
                    prompt=prompt,
                    scene_number=scene_number,
                    frame_number=frame_num,
                    style=style
                )
                
                if frame_path:
                    frame_paths.append(frame_path)
                    
                    # Log progress
                    if (frame_num + 1) % 10 == 0:
                        logger.info(f"Generated {frame_num + 1}/{num_frames} frames")
            
            logger.success(f"Scene {scene_number} generated: {len(frame_paths)} frames")
            return frame_paths
        
        except Exception as e:
            logger.error(f"Failed to generate scene: {e}")
            return frame_paths
    
    def _generate_frame(
        self,
        prompt: str,
        scene_number: int,
        frame_number: int,
        style: str
    ) -> Path:
        """
        Generate a single frame
        
        Args:
            prompt: Visual prompt
            scene_number: Scene ID
            frame_number: Frame ID
            style: Visual style
        
        Returns:
            Path to generated image
        """
        output_path = SCENE_OUTPUT_DIR / f"scene_{scene_number}_frame_{frame_number:04d}.png"
        
        try:
            if self.pipe is None:
                logger.warning("Model not loaded, creating placeholder image")
                self._create_placeholder_image(output_path, prompt)
                return output_path
            
            # Enhanced prompt with style
            full_prompt = f"{prompt}, {style} style, professional, high quality, detailed"
            
            # Generate image
            image = self.pipe(full_prompt).images[0]
            
            # Resize to target resolution
            image = image.resize(VIDEO_RESOLUTION)
            
            # Save frame
            image.save(str(output_path))
            logger.info(f"Frame generated: {output_path}")
            
            return output_path
        
        except Exception as e:
            logger.error(f"Frame generation failed: {e}")
            # Create placeholder on failure
            self._create_placeholder_image(output_path, prompt)
            return output_path
    
    def _create_placeholder_image(self, output_path: Path, prompt: str):
        """
        Create placeholder image for testing
        
        Args:
            output_path: Path to save image
            prompt: Prompt text to display
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            import random
            
            # Create image with random color
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            img = Image.new('RGB', VIDEO_RESOLUTION, color)
            draw = ImageDraw.Draw(img)
            
            # Add text
            text = prompt[:80] + "..." if len(prompt) > 80 else prompt
            draw.text((50, 500), text, fill=(255, 255, 255))
            
            img.save(str(output_path))
            logger.info(f"Placeholder image created: {output_path}")
        except Exception as e:
            logger.error(f"Failed to create placeholder: {e}")
    
    def add_text_overlay(
        self,
        frame_path: Path,
        text: str,
        position: tuple = (50, 50),
        font_size: int = 40,
        output_path: Path = None
    ) -> Path:
        """
        Add text overlay to frame
        
        Args:
            frame_path: Path to frame image
            text: Text to overlay
            position: Text position (x, y)
            font_size: Font size
            output_path: Path to save modified frame
        
        Returns:
            Path to frame with text overlay
        """
        if output_path is None:
            output_path = SCENE_OUTPUT_DIR / f"overlay_{frame_path.name}"
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.open(str(frame_path))
            draw = ImageDraw.Draw(img)
            
            # Try to load a nice font, fallback to default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Add text with shadow effect
            shadow_color = (0, 0, 0)
            text_color = (255, 255, 255)
            
            # Shadow
            draw.text((position[0]+2, position[1]+2), text, fill=shadow_color, font=font)
            # Text
            draw.text(position, text, fill=text_color, font=font)
            
            img.save(str(output_path))
            return output_path
        except Exception as e:
            logger.error(f"Failed to add text overlay: {e}")
            return frame_path
    
    def apply_filter(
        self,
        frame_path: Path,
        filter_type: str = "cinematic",
        output_path: Path = None
    ) -> Path:
        """
        Apply visual filter to frame
        
        Args:
            frame_path: Path to frame image
            filter_type: Type of filter (cinematic, warm, cool, vintage, noir)
            output_path: Path to save filtered frame
        
        Returns:
            Path to filtered frame
        """
        if output_path is None:
            output_path = SCENE_OUTPUT_DIR / f"filtered_{frame_path.name}"
        
        try:
            from PIL import Image, ImageEnhance
            
            img = Image.open(str(frame_path))
            
            if filter_type == "cinematic":
                # Increase contrast and saturation
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.2)
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.1)
            
            elif filter_type == "warm":
                # Increase red/yellow tones
                img = img.convert('RGB')
                pixels = img.load()
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        r, g, b = pixels[i, j]
                        pixels[i, j] = (min(r + 20, 255), g, max(b - 20, 0))
            
            elif filter_type == "cool":
                # Increase blue tones
                img = img.convert('RGB')
                pixels = img.load()
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        r, g, b = pixels[i, j]
                        pixels[i, j] = (max(r - 20, 0), g, min(b + 20, 255))
            
            elif filter_type == "vintage":
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(0.8)
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.1)
            
            elif filter_type == "noir":
                img = img.convert('L')  # Grayscale
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)
            
            img.save(str(output_path))
            return output_path
        except Exception as e:
            logger.error(f"Failed to apply filter: {e}")
            return frame_path
