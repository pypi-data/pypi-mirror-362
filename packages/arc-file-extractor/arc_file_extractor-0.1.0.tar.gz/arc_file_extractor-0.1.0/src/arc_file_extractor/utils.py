"""Utility functions for Arc File Extractor."""

import shutil
import subprocess
import zipfile
import tarfile
from pathlib import Path
from typing import List, Set
import typer


def check_dependencies() -> List[str]:
    """Check if required external tools are installed.
    
    Returns:
        List of missing dependencies
    """
    required_tools = [
        "unzip", "tar", "gunzip", "bunzip2", "unxz", "7z", "unrar", 
        "zip", "gzip", "bzip2", "xz", "rar"
    ]
    
    missing = []
    for tool in required_tools:
        if not shutil.which(tool):
            missing.append(tool)
    
    return missing


def get_supported_formats() -> dict:
    """Get supported file formats for extraction and compression.
    
    Returns:
        Dictionary with 'extract' and 'compress' keys containing lists of formats
    """
    return {
        "extract": [
            ".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz", 
            ".tar.xz", ".txz", ".gz", ".bz2", ".xz", ".7z", ".rar"
        ],
        "compress": [
            ".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz", 
            ".tar.xz", ".txz", ".7z", ".rar"
        ]
    }


def validate_file_path(file_path: str) -> bool:
    """Validate if a file path exists and is readable.
    
    Args:
        file_path: Path to validate
        
    Returns:
        True if valid, False otherwise
    """
    path = Path(file_path)
    return path.exists() and path.is_file()


def get_file_size(file_path: str) -> str:
    """Get human-readable file size.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Human-readable file size string
    """
    try:
        size = Path(file_path).stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except (OSError, FileNotFoundError):
        return "Unknown"


def get_archive_contents(file_path: str) -> Set[str]:
    """Get the list of files/directories that would be extracted from an archive.
    
    Args:
        file_path: Path to the archive file
        
    Returns:
        Set of file/directory names that would be extracted
    """
    contents = set()
    file_path_lower = file_path.lower()
    
    try:
        if file_path_lower.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                for name in zip_file.namelist():
                    # Get top-level items
                    top_level = name.split('/')[0]
                    if top_level:
                        contents.add(top_level)
        
        elif any(file_path_lower.endswith(ext) for ext in ['.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz', '.tar.xz', '.txz']):
            with tarfile.open(file_path, 'r') as tar_file:
                for member in tar_file.getmembers():
                    # Get top-level items
                    top_level = member.name.split('/')[0]
                    if top_level:
                        contents.add(top_level)
        
        else:
            # For other formats, try to get listing using command line tools
            if file_path_lower.endswith('.7z'):
                try:
                    result = subprocess.run(['7z', 'l', file_path], 
                                          capture_output=True, text=True, check=True)
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('-') and 'Name' not in line:
                            parts = line.split()
                            if len(parts) >= 6:
                                filename = ' '.join(parts[5:])
                                if filename:
                                    top_level = filename.split('/')[0]
                                    contents.add(top_level)
                except subprocess.CalledProcessError:
                    pass
            
            elif file_path_lower.endswith('.rar'):
                try:
                    result = subprocess.run(['unrar', 'l', file_path], 
                                          capture_output=True, text=True, check=True)
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('-') and 'Name' not in line:
                            parts = line.split()
                            if len(parts) >= 5:
                                filename = ' '.join(parts[4:])
                                if filename:
                                    top_level = filename.split('/')[0]
                                    contents.add(top_level)
                except subprocess.CalledProcessError:
                    pass
    
    except Exception:
        # If we can't read the archive, return empty set
        pass
    
    return contents


def check_extraction_conflicts(file_path: str, output_dir: str = None) -> List[str]:
    """Check if extracting an archive would overwrite existing files.
    
    Args:
        file_path: Path to the archive file
        output_dir: Directory where files would be extracted (defaults to current directory)
        
    Returns:
        List of existing files/directories that would be overwritten
    """
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
    
    contents = get_archive_contents(file_path)
    conflicts = []
    
    for item in contents:
        item_path = output_dir / item
        if item_path.exists():
            conflicts.append(str(item_path))
    
    return conflicts


def prompt_overwrite_confirmation(conflicts: List[str]) -> bool:
    """Prompt user to confirm overwriting existing files.
    
    Args:
        conflicts: List of files that would be overwritten
        
    Returns:
        True if user wants to proceed, False otherwise
    """
    if not conflicts:
        return True
    
    print(f"\n[yellow]Warning: The following files/directories already exist:[/yellow]")
    for conflict in conflicts:
        print(f"  • {conflict}")
    
    print(f"\n[yellow]Extracting will overwrite {len(conflicts)} existing item(s).[/yellow]")
    
    return typer.confirm("Do you want to proceed and overwrite these files?")
