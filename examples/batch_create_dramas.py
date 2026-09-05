#!/usr/bin/env python3
"""
Example: Batch Create Multiple Dramas
"""

from src.agent.drama_agent import DramaAgent
from src.utils.logger import setup_logger
from pathlib import Path

logger = setup_logger()


def create_drama_batch():
    """
    Create multiple dramas in batch mode
    """
    
    dramas = [
        {
            "genre": "k-drama",
            "title": "Seoul Nights",
            "description": "A modern love story in the bustling streets of Seoul",
            "scenes": 5,
            "voice_style": "romantic"
        },
        {
            "genre": "c-drama",
            "title": "Dragon's Ascent",
            "description": "A warrior's journey through ancient China seeking redemption",
            "scenes": 6,
            "voice_style": "dramatic"
        },
        {
            "genre": "us-drama",
            "title": "Midnight Justice",
            "description": "A crime thriller that will keep you on edge",
            "scenes": 5,
            "voice_style": "intense"
        }
    ]
    
    output_videos = []
    
    for drama in dramas:
        logger.info(f"\n{'='*60}")
        logger.info(f"Creating: {drama['title']}")
        logger.info(f"{'='*60}")
        
        agent = DramaAgent(
            genre=drama["genre"],
            language="english",
            emotion_intensity=0.8,
            music_style="orchestral"
        )
        
        try:
            video = agent.create_drama(
                title=drama["title"],
                description=drama["description"],
                duration_minutes=5,
                num_scenes=drama["scenes"],
                voiceover_style=drama["voice_style"]
            )
            output_videos.append(video)
            logger.success(f"✓ {drama['title']} created!")
        except Exception as e:
            logger.error(f"✗ Failed to create {drama['title']}: {e}")
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"Batch Creation Complete!")
    logger.info(f"Total dramas created: {len(output_videos)}")
    for video in output_videos:
        logger.info(f"  • {video}")
    logger.info(f"{'='*60}\n")
    
    return output_videos


if __name__ == "__main__":
    videos = create_drama_batch()
