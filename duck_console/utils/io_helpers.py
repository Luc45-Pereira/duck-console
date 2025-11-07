"""
I/O helper utilities
"""
import re
from pathlib import Path
from typing import Optional, Union


def sanitize_table_name(filename: str) -> str:
    """Convert a filename to a valid SQL table name
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized table name
    """
    # Remove extension
    name = Path(filename).stem
    
    # Replace invalid characters with underscore
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    
    # Ensure it starts with letter
    if not name[0].isalpha():
        name = 'table_' + name
        
    return name.lower()


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure a directory exists, creating it if needed
    
    Args:
        path: Directory path
        
    Returns:
        Path object for the directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path