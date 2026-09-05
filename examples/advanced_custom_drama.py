#!/usr/bin/env python3
"""
Example: Advanced - Custom Drama with Full Configuration
"""

from src.agent.drama_agent import DramaAgent, DramaConfig
from src.utils.logger import setup_logger

logger = setup_logger()


if __name__ == "__main__":
    # Create agent with custom configuration
    agent = DramaAgent(
        genre="k-drama",
        language="english",
        emotion_intensity=0.95,  # Very high emotion
        music_style="orchestral"
    )
    
    # Create drama with all options
    video = agent.create_drama(
        title="Tears of the Moon",
        description="""A paranormal romance where a human detective falls in love with a ghost 
        who is trying to solve her own murder. Together they uncover secrets that shake 
        the entire city and risk their connection to the living world.""",
        duration_minutes=10,
        num_scenes=10,
        voiceover_style="emotional",  # Very emotional narration
        add_title_card=True,
        add_credits=True
    )
    
    print(f"\n✓ Advanced drama created: {video}")
    print(f"Check the output folder for all generated assets!")
