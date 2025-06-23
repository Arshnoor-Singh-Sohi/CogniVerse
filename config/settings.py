"""
Application Configuration Module

This module centralizes all configuration settings for CogniVerse.
By keeping configuration separate, we make the app more maintainable
and easier to deploy across different environments.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class ModelConfig:
    """Configuration for different AI models available in the application."""
    name: str
    display_name: str
    description: str
    max_tokens: int
    supports_vision: bool = False
    supports_files: bool = True

@dataclass
class UIConfig:
    """Configuration for user interface elements and styling."""
    theme_colors: Dict[str, str]
    default_theme: str
    available_themes: List[str]
    max_file_size_mb: int
    supported_file_types: List[str]

class AppConfig:
    """
    Main configuration class that holds all application settings.
    
    This class follows the singleton pattern to ensure consistent
    configuration throughout the application lifecycle.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # API Configuration
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Model Configurations
        self.models = {
            "gemini-2.0-flash-exp": ModelConfig(
                name="gemini-2.0-flash-exp",
                display_name="Gemini 2.0 Flash (Experimental)",
                description="Latest experimental model with enhanced reasoning",
                max_tokens=8192,
                supports_vision=True,
                supports_files=True
            ),
            "gemini-1.5-pro": ModelConfig(
                name="gemini-1.5-pro",
                display_name="Gemini 1.5 Pro",
                description="Most capable model for complex tasks",
                max_tokens=2048000,
                supports_vision=True,
                supports_files=True
            ),
            "gemini-1.5-flash": ModelConfig(
                name="gemini-1.5-flash",
                display_name="Gemini 1.5 Flash",
                description="Fast and efficient for everyday tasks",
                max_tokens=1048576,
                supports_vision=True,
                supports_files=True
            )
        }
        
        # UI Configuration
        self.ui = UIConfig(
            theme_colors={
                "dark": {
                    "primary": "#1E88E5",
                    "secondary": "#FFC107",
                    "background": "#0E1117",
                    "surface": "#262730",
                    "text": "#FAFAFA",
                    "accent": "#FF6B6B"
                },
                "light": {
                    "primary": "#1976D2",
                    "secondary": "#FF9800",
                    "background": "#FFFFFF",
                    "surface": "#F5F5F5",
                    "text": "#212121",
                    "accent": "#E91E63"
                }
            },
            default_theme="dark",
            available_themes=["dark", "light"],
            max_file_size_mb=100,
            supported_file_types=[
                "pdf", "txt", "docx", "csv", "json", 
                "png", "jpg", "jpeg", "gif", "bmp"
            ]
        )
        
        # Application Settings
        self.app_name = "CogniVerse"
        self.app_version = "1.0.0"
        self.app_description = "Your Complete AI Conversation Universe"
        
        # Chat Settings
        self.max_conversation_history = 50  # Maximum messages to keep in memory
        self.auto_save_interval = 30  # Seconds between auto-saves
        self.default_temperature = 0.7
        self.max_file_uploads_per_session = 10
        
        # Storage Settings
        self.conversations_dir = "data/conversations"
        self.uploads_dir = "data/uploads"
        self.exports_dir = "data/exports"
        
        # Create necessary directories
        self._create_directories()
        
        self._initialized = True
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.conversations_dir,
            self.uploads_dir,
            self.exports_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """Get configuration for a specific model."""
        return self.models.get(model_name)
    
    def get_available_models(self) -> List[str]:
        """Get list of available model names."""
        return list(self.models.keys())
    
    def get_theme_colors(self, theme: str) -> Dict[str, str]:
        """Get color configuration for a specific theme."""
        return self.ui.theme_colors.get(theme, self.ui.theme_colors[self.ui.default_theme])
    
    def is_file_type_supported(self, file_type: str) -> bool:
        """Check if a file type is supported."""
        return file_type.lower() in self.ui.supported_file_types
    
    def get_max_file_size_bytes(self) -> int:
        """Get maximum file size in bytes."""
        return self.ui.max_file_size_mb * 1024 * 1024
    
    @property
    def debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv("DEBUG", "False").lower() == "true"
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary for serialization."""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "available_models": self.get_available_models(),
            "supported_file_types": self.ui.supported_file_types,
            "max_file_size_mb": self.ui.max_file_size_mb,
            "available_themes": self.ui.available_themes
        }