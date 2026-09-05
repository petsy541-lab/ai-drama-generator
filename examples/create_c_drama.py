#!/usr/bin/env python3
"""
Example: Create a C-Drama with Martial Arts Theme
"""

from src.agent.drama_agent import DramaAgent
from src.utils.logger import setup_logger

logger = setup_logger()


if __name__ == "__main__":
    # Create a C-Drama agent
    agent = DramaAgent(
        genre="c-drama",
        language="english",
        emotion_intensity=0.9,
        music_style="traditional-chinese"
    )
    
    # Generate a drama
    video = agent.create_drama(
        title="The Forbidden Palace",
        description="An epic tale of political intrigue and forbidden love in the imperial court during the Qing Dynasty",
        duration_minutes=8,
        num_scenes=8,
        voiceover_style="dramatic",
        add_title_card=True,
        add_credits=True
    )
    
    print(f"\n✓ Drama created: {video}")
