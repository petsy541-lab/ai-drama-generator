#!/usr/bin/env python3
"""
Example: Create a K-Drama with Romance Theme
"""

from src.agent.drama_agent import DramaAgent
from src.utils.logger import setup_logger

logger = setup_logger()


if __name__ == "__main__":
    # Create a K-Drama agent
    agent = DramaAgent(
        genre="k-drama",
        language="english",
        emotion_intensity=0.85,
        music_style="korean-pop"
    )
    
    # Generate a drama
    video = agent.create_drama(
        title="Winter Romance in Seoul",
        description="A heartwarming story of two strangers meeting in a snowy Seoul cafe during winter",
        duration_minutes=5,
        num_scenes=6,
        voiceover_style="romantic",
        add_title_card=True,
        add_credits=True
    )
    
    print(f"\n✓ Drama created: {video}")
