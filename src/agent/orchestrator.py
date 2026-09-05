#!/usr/bin/env python3
"""
Orchestrator - Manages workflow and component coordination
"""

import os
from pathlib import Path
from typing import Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger()


class DramaOrchestrator:
    """
    Manages the complete workflow orchestration for drama creation
    """
    
    def __init__(self):
        """
        Initialize orchestrator
        """
        logger.info("DramaOrchestrator initialized")
    
    def validate_environment(self) -> bool:
        """
        Validate that all required dependencies are available
        
        Returns:
            True if all dependencies are available
        """
        logger.info("Validating environment...")
        
        required_packages = [
            'torch',
            'transformers',
            'diffusers',
            'pydub',
            'moviepy',
            'PIL'
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            logger.warning(f"Missing packages: {', '.join(missing)}")
            logger.info(f"Install with: pip install {' '.join(missing)}")
            return False
        
        logger.success("All dependencies available")
        return True
    
    def setup_directories(self) -> bool:
        """
        Create necessary output directories
        
        Returns:
            True if setup successful
        """
        from src.utils.constants import (
            SCRIPT_OUTPUT_DIR,
            SCENE_OUTPUT_DIR,
            VOICEOVER_OUTPUT_DIR,
            SFX_OUTPUT_DIR,
            FINAL_VIDEO_OUTPUT_DIR
        )
        
        dirs = [
            SCRIPT_OUTPUT_DIR,
            SCENE_OUTPUT_DIR,
            VOICEOVER_OUTPUT_DIR,
            SFX_OUTPUT_DIR,
            FINAL_VIDEO_OUTPUT_DIR
        ]
        
        for dir_path in dirs:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Directory ready: {dir_path}")
            except Exception as e:
                logger.error(f"Failed to create directory {dir_path}: {e}")
                return False
        
        logger.success("All directories setup")
        return True
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information for the environment
        
        Returns:
            Dictionary with system info
        """
        import platform
        import torch
        
        info = {
            "os": platform.system(),
            "python_version": platform.python_version(),
            "device": "cuda" if torch.cuda.is_available() else "cpu",
            "torch_version": torch.__version__
        }
        
        if torch.cuda.is_available():
            info["gpu"] = torch.cuda.get_device_name(0)
        
        return info
    
    def print_welcome_banner(self):
        """
        Print welcome banner
        """
        banner = """
        ╔═══════════════════════════════════════════════════════════╗
        ║         🎬  AI DRAMA GENERATOR AGENT  🎬                  ║
        ║                                                           ║
        ║    Create professional drama videos with AI               ║
        ║    • C-Drama (Period, Martial Arts, Political)            ║
        ║    • K-Drama (Romance, Revenge, Fantasy)                  ║
        ║    • US-Drama (Crime, Medical, Supernatural)              ║
        ║                                                           ║
        ║    Features:                                              ║
        ║    ✓ AI Script Generation                                 ║
        ║    ✓ Video Scene Creation (Stable Diffusion)              ║
        ║    ✓ English Voice-Over (Bark TTS)                        ║
        ║    ✓ Sound Effects & Music                                ║
        ║    ✓ Professional Video Editing                           ║
        ║                                                           ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)
