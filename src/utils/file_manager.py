# File Manager Utilities

import os
from pathlib import Path
from typing import List
import json
import yaml
from src.utils.logger import setup_logger

logger = setup_logger()


class FileManager:
    """
    Manages file operations and output organization
    """
    
    @staticmethod
    def ensure_directory(path: Path) -> Path:
        """
        Ensure directory exists
        
        Args:
            path: Directory path
        
        Returns:
            Path to directory
        """
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def save_json(data: dict, filepath: Path, pretty: bool = True):
        """
        Save dictionary to JSON file
        
        Args:
            data: Dictionary to save
            filepath: Path to save file
            pretty: Whether to format with indentation
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2 if pretty else None)
            logger.info(f"JSON saved: {filepath}")
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")
    
    @staticmethod
    def load_json(filepath: Path) -> dict:
        """
        Load JSON file
        
        Args:
            filepath: Path to JSON file
        
        Returns:
            Loaded dictionary
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
            return {}
    
    @staticmethod
    def get_file_size(filepath: Path) -> str:
        """
        Get human-readable file size
        
        Args:
            filepath: Path to file
        
        Returns:
            File size as string (e.g., "2.5 MB")
        """
        size = filepath.stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
