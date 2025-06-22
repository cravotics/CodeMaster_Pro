"""
Configuration Management System

Learning Notes:
- This module demonstrates configuration file handling in Python
- Shows how to manage application settings and API keys securely
- Implements the Singleton pattern for global configuration access
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """
    Configuration manager for the CodeMaster Pro application.
    
    This class handles:
    1. Loading and saving application settings
    2. Managing API keys and credentials
    3. User preference persistence
    4. Default configuration values
    """
    
    _instance = None
    
    def __new__(cls):
        """Implement Singleton pattern for global config access."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration with default values."""
        if hasattr(self, '_initialized'):
            return
            
        self._initialized = True
        self.config_dir = Path.home() / '.codemaster_pro'
        self.config_file = self.config_dir / 'config.json'
        
        # Default configuration values
        self.defaults = {
            'appearance_mode': 'dark',
            'color_theme': 'blue',
            'window_geometry': '1400x900',
            'default_project_path': str(Path.home() / 'CodeMaster_Projects'),
            'auto_save_interval': 300,  # 5 minutes in seconds
            'weather_location': 'New York',
            'preferred_font_family': 'Consolas',
            'font_size': 12,
            'ai_model_preference': 'gpt-3.5-turbo',
            'sql_tutorial_progress': {},
            'recent_projects': [],
            'api_endpoints': {
                'weather': 'https://api.openweathermap.org/data/2.5',
                'fonts': 'https://www.googleapis.com/webfonts/v1',
                'openai': 'https://api.openai.com/v1',
                'anthropic': 'https://api.anthropic.com/v1'
            }
        }
        
        # Load existing configuration
        self.config_data = self.load()
        
        # Create project directory if it doesn't exist
        self.create_project_directory()
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Learning Notes:
        - File I/O operations with error handling
        - JSON parsing and data validation
        - Graceful fallback to defaults
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    
                # Merge with defaults to ensure all keys exist
                merged_config = self.defaults.copy()
                merged_config.update(loaded_config)
                return merged_config
            else:
                return self.defaults.copy()
                
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
            print("Using default configuration...")
            return self.defaults.copy()
    
    def save(self) -> bool:
        """
        Save current configuration to file.
        
        Learning Notes:
        - File creation with proper directory handling
        - JSON serialization
        - Error handling for file operations
        """
        try:
            # Create config directory if it doesn't exist
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # Save configuration
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self.config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config_data[key] = value
    
    def get_api_key(self, service: str) -> Optional[str]:
        """
        Get API key for a service from environment variables.
        
        Learning Notes:
        - Secure API key management using environment variables
        - Service abstraction for different APIs
        - Security best practices
        """
        env_var_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'weather': 'WEATHER_API_KEY',
            'fonts': 'GOOGLE_FONTS_API_KEY'
        }
        
        env_var = env_var_map.get(service)
        if env_var:
            return os.getenv(env_var)
        return None
    
    def update_sql_progress(self, lesson: str, completed: bool) -> None:
        """Update SQL tutorial progress."""
        if 'sql_tutorial_progress' not in self.config_data:
            self.config_data['sql_tutorial_progress'] = {}
        
        self.config_data['sql_tutorial_progress'][lesson] = completed
        self.save()
    
    def add_recent_project(self, project_path: str) -> None:
        """Add project to recent projects list."""
        recent = self.config_data.get('recent_projects', [])
        
        # Remove if already exists to avoid duplicates
        if project_path in recent:
            recent.remove(project_path)
        
        # Add to beginning
        recent.insert(0, project_path)
        
        # Keep only last 10 projects
        self.config_data['recent_projects'] = recent[:10]
        self.save()
    
    def create_project_directory(self) -> None:
        """Create default project directory if it doesn't exist."""
        try:
            project_dir = Path(self.get('default_project_path'))
            project_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Project directory: {project_dir}")
        except Exception as e:
            print(f"⚠️  Could not create project directory: {e}")
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config_data = self.defaults.copy()
        self.save()
        print("🔄 Configuration reset to defaults")
    
    def export_config(self, export_path: str) -> bool:
        """Export configuration to specified path."""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from specified path."""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validate and merge with defaults
            merged_config = self.defaults.copy()
            merged_config.update(imported_config)
            
            self.config_data = merged_config
            self.save()
            return True
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            return False 