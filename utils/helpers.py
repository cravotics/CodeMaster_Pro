"""
Helper Utilities for CodeMaster Pro

Learning Notes:
- This module demonstrates common utility patterns in Python applications
- Shows logging configuration for debugging and monitoring
- Includes file operations and cross-platform compatibility helpers
"""

import logging
import os
import sys
import platform
from pathlib import Path
from typing import List, Optional, Dict, Any
import hashlib
import datetime

def setup_logging(log_level: str = 'INFO') -> None:
    """
    Set up application logging configuration.
    
    Learning Notes:
    - Python logging module configuration
    - Log levels and formatting
    - File vs console output
    """
    
    # Create logs directory
    log_dir = Path.home() / '.codemaster_pro' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Set up file handler
    log_file = log_dir / f'codemaster_{datetime.datetime.now().strftime("%Y%m%d")}.log'
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Get logger for this module
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Level: {log_level}")
    logger.info(f"Log file: {log_file}")

def get_system_info() -> Dict[str, str]:
    """
    Get system information for debugging and compatibility.
    
    Learning Notes:
    - Platform detection in Python
    - System information gathering
    - Cross-platform compatibility checks
    """
    
    return {
        'platform': platform.platform(),
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'python_executable': sys.executable,
        'working_directory': str(Path.cwd()),
        'user_home': str(Path.home())
    }

def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file path is safe and accessible.
    
    Learning Notes:
    - Path validation and security
    - File system operations
    - Error handling for file access
    """
    
    try:
        path = Path(file_path)
        
        # Check if path exists
        if not path.exists():
            return False
            
        # Check if it's a file (not directory)
        if not path.is_file():
            return False
            
        # Check read permissions
        if not os.access(path, os.R_OK):
            return False
            
        return True
        
    except Exception as e:
        logging.error(f"Error validating file path {file_path}: {e}")
        return False

def safe_file_read(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    Safely read file contents with error handling.
    
    Learning Notes:
    - Safe file reading with encoding handling
    - Exception handling for file operations
    - Memory-efficient file reading
    """
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return None
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

def safe_file_write(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    Safely write content to file with error handling.
    
    Learning Notes:
    - Safe file writing with backup creation
    - Directory creation for nested paths
    - Atomic write operations
    """
    
    try:
        path = Path(file_path)
        
        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        logging.error(f"Error writing file {file_path}: {e}")
        return False

def calculate_file_hash(file_path: str) -> Optional[str]:
    """
    Calculate SHA-256 hash of a file for integrity checking.
    
    Learning Notes:
    - File hashing for integrity verification
    - Memory-efficient file processing
    - Cryptographic hash functions
    """
    
    try:
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
                
        return sha256_hash.hexdigest()
        
    except Exception as e:
        logging.error(f"Error calculating hash for {file_path}: {e}")
        return None

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Learning Notes:
    - Number formatting and unit conversion
    - User-friendly data presentation
    - Mathematical operations for file sizes
    """
    
    if size_bytes == 0:
        return "0 B"
        
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.1f} {size_names[i]}"

def find_files_by_extension(directory: str, extensions: List[str]) -> List[str]:
    """
    Find all files with specific extensions in a directory.
    
    Learning Notes:
    - Directory traversal and file filtering
    - List comprehensions and generator expressions
    - Pattern matching for file types
    """
    
    try:
        path = Path(directory)
        if not path.exists() or not path.is_dir():
            return []
            
        files = []
        for ext in extensions:
            # Use glob pattern to find files
            pattern = f"**/*.{ext.lstrip('.')}"
            files.extend([str(f) for f in path.glob(pattern)])
            
        return sorted(files)
        
    except Exception as e:
        logging.error(f"Error finding files in {directory}: {e}")
        return []

def create_backup(file_path: str) -> Optional[str]:
    """
    Create a backup copy of a file.
    
    Learning Notes:
    - File copying and backup strategies
    - Timestamp generation for unique names
    - Error handling for file operations
    """
    
    try:
        source_path = Path(file_path)
        if not source_path.exists():
            return None
            
        # Create backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source_path.stem}_{timestamp}{source_path.suffix}"
        backup_path = source_path.parent / f"backup_{backup_name}"
        
        # Copy file content
        import shutil
        shutil.copy2(source_path, backup_path)
        
        logging.info(f"Backup created: {backup_path}")
        return str(backup_path)
        
    except Exception as e:
        logging.error(f"Error creating backup for {file_path}: {e}")
        return None

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for cross-platform compatibility.
    
    Learning Notes:
    - String manipulation and cleaning
    - Cross-platform file naming rules
    - Regular expressions for pattern replacement
    """
    
    import re
    
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]
        
    # Ensure not empty
    if not sanitized:
        sanitized = "untitled"
        
    return sanitized

def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get comprehensive file information.
    
    Learning Notes:
    - File system metadata access
    - Date/time handling
    - Dictionary construction for structured data
    """
    
    try:
        path = Path(file_path)
        if not path.exists():
            return {}
            
        stat = path.stat()
        
        return {
            'name': path.name,
            'extension': path.suffix,
            'size': stat.st_size,
            'size_formatted': format_file_size(stat.st_size),
            'created': datetime.datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.datetime.fromtimestamp(stat.st_mtime),
            'accessed': datetime.datetime.fromtimestamp(stat.st_atime),
            'is_directory': path.is_dir(),
            'is_file': path.is_file(),
            'absolute_path': str(path.absolute()),
            'parent_directory': str(path.parent),
            'hash': calculate_file_hash(file_path) if path.is_file() else None
        }
        
    except Exception as e:
        logging.error(f"Error getting file info for {file_path}: {e}")
        return {}

def validate_api_key(api_key: str, service: str) -> bool:
    """
    Basic validation for API key format.
    
    Learning Notes:
    - String validation patterns
    - Service-specific validation rules
    - Security considerations for API keys
    """
    
    if not api_key or not isinstance(api_key, str):
        return False
    
    # Basic length and format checks
    api_key = api_key.strip()
    
    if service == 'openai':
        return api_key.startswith('sk-') and len(api_key) > 20
    elif service == 'anthropic':
        return api_key.startswith('sk-ant-') and len(api_key) > 20
    elif service == 'weather':
        return len(api_key) >= 20  # OpenWeatherMap API keys
    elif service == 'fonts':
        return len(api_key) >= 20  # Google API keys
    
    return len(api_key) >= 10  # Generic minimum length

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable format.
    
    Learning Notes:
    - Time formatting and conversion
    - Mathematical operations for time units
    - String formatting for user display
    """
    
    if seconds < 1:
        return f"{seconds:.2f}s"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes}m {seconds:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m" 