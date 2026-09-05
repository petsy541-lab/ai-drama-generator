#!/usr/bin/env python3
"""
AI Drama Generator - Main Entry Point
Creates realistic drama videos with voiceovers and sound effects
"""

import typer
from pathlib import Path
from src.agent.drama_agent import DramaAgent
from src.utils.logger import setup_logger

app = typer.Typer(
    help="AI Drama Generator - Create cinematic dramas with AI",
    rich_markup_mode="rich"
)

logger = setup_logger()


@app.command()
def create(
    genre: str = typer.Option(
        "k-drama",
        "--genre",
        "-g",
        help="Drama genre: [bold]c-drama[/bold], [bold]k-drama[/bold], or [bold]us-drama[/bold]"
    ),
    title: str = typer.Option(
        "Untitled Drama",
        "--title",
        "-t",
        help="Title of the drama"
    ),
    description: str = typer.Option(
        "",
        "--description",
        "-d",
        help="Story description"
    ),
    duration: int = typer.Option(
        3,
        "--duration",
        "-du",
        help="Video duration in minutes"
    ),
    scenes: int = typer.Option(
        5,
        "--scenes",
        "-sc",
        help="Number of scenes to generate"
    ),
    voiceover_style: str = typer.Option(
        "dramatic",
        "--voice-style",
        "-vs",
        help="Voice style: dramatic, emotional, calm, intense"
    ),
    music_style: str = typer.Option(
        "orchestral",
        "--music-style",
        "-ms",
        help="Background music style"
    ),
    emotion_intensity: float = typer.Option(
        0.8,
        "--emotion-intensity",
        "-ei",
        help="Emotion intensity (0.0-1.0)",
        min=0.0,
        max=1.0
    ),
):
    """
    Create a new AI-generated drama video
    
    Example:
    python main.py --genre k-drama --title "Love Story" --duration 5 --scenes 8
    """
    typer.echo(f"\n🎬 [bold cyan]AI Drama Generator[/bold cyan]")
    typer.echo(f"   Creating {genre.upper()} drama...\n")
    
    try:
        # Initialize agent
        agent = DramaAgent(
            genre=genre.lower(),
            language="english",
            emotion_intensity=emotion_intensity,
            music_style=music_style
        )
        
        # Create drama
        logger.info(f"Starting drama creation: {title}")
        video_path = agent.create_drama(
            title=title,
            description=description,
            duration_minutes=duration,
            num_scenes=scenes,
            voiceover_style=voiceover_style
        )
        
        logger.success(f"✅ Drama created successfully: {video_path}")
        typer.echo(f"\n✨ [bold green]Success![/bold green]")
        typer.echo(f"   Video saved to: [bold]{video_path}[/bold]\n")
        
    except Exception as e:
        logger.error(f"Failed to create drama: {str(e)}")
        typer.echo(f"\n❌ [bold red]Error:[/bold red] {str(e)}\n")
        raise typer.Exit(code=1)


@app.command()
def list_genres():
    """
    List available drama genres and their characteristics
    """
    typer.echo("\n🎭 [bold cyan]Available Drama Genres[/bold cyan]\n")
    
    genres = {
        "c-drama": [
            "Ancient/Period pieces",
            "Martial arts and fantasy",
            "Political intrigue",
            "Romance and dynasty stories"
        ],
        "k-drama": [
            "Contemporary romance",
            "Revenge plots",
            "Fantasy/supernatural",
            "Slice-of-life stories"
        ],
        "us-drama": [
            "Crime procedural",
            "Medical drama",
            "Supernatural thriller",
            "Workplace drama"
        ]
    }
    
    for genre, characteristics in genres.items():
        typer.echo(f"📺 [bold]{genre.upper()}[/bold]")
        for char in characteristics:
            typer.echo(f"   • {char}")
        typer.echo()


@app.command()
def voice_options():
    """
    Show available voice and music styles
    """
    typer.echo("\n🎤 [bold cyan]Voice-Over Styles[/bold cyan]\n")
    voices = ["dramatic", "emotional", "calm", "intense", "mysterious", "romantic"]
    for voice in voices:
        typer.echo(f"   • {voice}")
    
    typer.echo("\n🎵 [bold cyan]Music Styles[/bold cyan]\n")
    music = [
        "orchestral",
        "electronic",
        "traditional-chinese",
        "korean-pop",
        "cinematic",
        "ambient"
    ]
    for m in music:
        typer.echo(f"   • {m}")
    typer.echo()


if __name__ == "__main__":
    app()
