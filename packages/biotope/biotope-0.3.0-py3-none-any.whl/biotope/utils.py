"""Shared utility functions for biotope commands."""

import subprocess
from pathlib import Path
from typing import Optional


def find_biotope_root() -> Optional[Path]:
    """
    Find the biotope project root directory.
    
    Searches upward from the current working directory to find a directory
    containing a .biotope/ subdirectory.
    
    Returns:
        Path to the biotope project root, or None if not found
    """
    current = Path.cwd()
    while current != current.parent:
        if (current / ".biotope").exists():
            return current
        current = current.parent
    return None


def is_git_repo(directory: Path) -> bool:
    """
    Check if directory is a Git repository.
    
    Args:
        directory: Path to the directory to check
        
    Returns:
        True if the directory is a Git repository, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False 