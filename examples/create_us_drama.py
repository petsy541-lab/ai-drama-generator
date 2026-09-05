#!/usr/bin/env python3
"""
Example: Create a US-Drama with Crime Theme
"""

from src.agent.drama_agent import DramaAgent
from src.utils.logger import setup_logger

logger = setup_logger()


if __name__ == "__main__":
    # Create a US-Drama agent
    agent = DramaAgent(
        genre="us-drama",
        language="english",
        emotion_intensity=0.8,
        music_style="noir-jazz"
    )
    
    # Generate a drama
    video = agent.create_drama(
        title="The Last Detective",
        description="A seasoned detective investigates a mysterious crime that challenges everything she knows about the city",
        duration_minutes=7,
        num_scenes=7,
        voiceover_style="intense",
        add_title_card=True,
        add_credits=True
    )
    
    print(f"\n✓ Drama created: {video}")
