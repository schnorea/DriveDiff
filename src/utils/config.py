"""
Configuration Manager Module
Handles application settings and configuration
"""

import os
import json
import tempfile
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """Manages application configuration and settings"""
    
    def __init__(self, app_name: str = "SDCardComparison"):
        """
        Initialize configuration manager
        
        Args:
            app_name: Name of the application for config directory
        """
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.config_file = os.path.join(self.config_dir, "settings.json")
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Default settings
        self.default_settings = {
            'window_geometry': '1200x800+100+100',
            'remember_window_pos': True,
            'remember_directories': True,
            'auto_refresh': False,
            'left_path': '',
            'right_path': '',
            'ignore_patterns': [
                '*.tmp', '*.bak', '*.swp', '*~', '.DS_Store', 'Thumbs.db',
                '*.pyc', '*.pyo', '__pycache__', '.git', '.svn', '.hg'
            ],
            'compare_metadata': True,
            'ignore_case': False,
            'follow_symlinks': False,
            'max_file_size': 100,  # MB
            'thread_pool_size': 4,
            'font_family': 'Courier',
            'font_size': 10,
            'color_scheme': 'default',
            'show_line_numbers': False,
            'word_wrap': False,
            'syntax_highlighting': True,
            'last_export_directory': '',
            'last_report_format': 'html',
            'show_identical_files': False,
            'sync_scrolling': True,
            'recent_left_paths': [],
            'recent_right_paths': [],
            'max_recent_paths': 10
        }
    
    def _get_config_directory(self) -> str:
        """Get the configuration directory path"""
        if os.name == 'nt':  # Windows
            config_dir = os.path.join(os.environ.get('APPDATA', ''), self.app_name)
        elif os.name == 'posix':
            if 'darwin' in os.sys.platform.lower():  # macOS
                config_dir = os.path.join(
                    os.path.expanduser('~/Library/Application Support'), 
                    self.app_name
                )
            else:  # Linux and other Unix-like
                config_dir = os.path.join(
                    os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')), 
                    self.app_name.lower()
                )
        else:
            # Fallback to temp directory
            config_dir = os.path.join(tempfile.gettempdir(), self.app_name)
        
        return config_dir
    
    def load_settings(self) -> Dict[str, Any]:
        """
        Load settings from configuration file
        
        Returns:
            Dictionary containing all settings
        """
        settings = self.default_settings.copy()
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    settings.update(saved_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
            # Use defaults if loading fails
        
        return settings
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Save settings to configuration file
        
        Args:
            settings: Dictionary containing settings to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Merge with existing settings
            current_settings = self.load_settings()
            current_settings.update(settings)
            
            # Ensure config directory exists
            os.makedirs(self.config_dir, exist_ok=True)
            
            # Save to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(current_settings, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a specific setting value
        
        Args:
            key: Setting key
            default: Default value if key doesn't exist
            
        Returns:
            Setting value or default
        """
        settings = self.load_settings()
        return settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> bool:
        """
        Set a specific setting value
        
        Args:
            key: Setting key
            value: Setting value
            
        Returns:
            True if successful, False otherwise
        """
        return self.save_settings({key: value})
    
    def reset_settings(self) -> bool:
        """
        Reset all settings to defaults
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            return True
        except Exception as e:
            print(f"Error resetting settings: {e}")
            return False
    
    def add_recent_path(self, path: str, side: str) -> bool:
        """
        Add a path to recent paths list
        
        Args:
            path: Directory path to add
            side: 'left' or 'right'
            
        Returns:
            True if successful, False otherwise
        """
        if side not in ['left', 'right']:
            return False
        
        settings = self.load_settings()
        recent_key = f'recent_{side}_paths'
        recent_paths = settings.get(recent_key, [])
        max_recent = settings.get('max_recent_paths', 10)
        
        # Remove path if it already exists
        if path in recent_paths:
            recent_paths.remove(path)
        
        # Add to beginning of list
        recent_paths.insert(0, path)
        
        # Limit to max_recent_paths
        recent_paths = recent_paths[:max_recent]
        
        return self.save_settings({recent_key: recent_paths})
    
    def get_recent_paths(self, side: str) -> list:
        """
        Get recent paths for a side
        
        Args:
            side: 'left' or 'right'
            
        Returns:
            List of recent paths
        """
        if side not in ['left', 'right']:
            return []
        
        settings = self.load_settings()
        return settings.get(f'recent_{side}_paths', [])
    
    def clear_recent_paths(self, side: Optional[str] = None) -> bool:
        """
        Clear recent paths
        
        Args:
            side: 'left', 'right', or None for both
            
        Returns:
            True if successful, False otherwise
        """
        updates = {}
        
        if side is None or side == 'left':
            updates['recent_left_paths'] = []
        
        if side is None or side == 'right':
            updates['recent_right_paths'] = []
        
        return self.save_settings(updates)
    
    def export_settings(self, file_path: str) -> bool:
        """
        Export settings to a file
        
        Args:
            file_path: Path to export file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            settings = self.load_settings()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, file_path: str, merge: bool = True) -> bool:
        """
        Import settings from a file
        
        Args:
            file_path: Path to import file
            merge: Whether to merge with existing settings or replace
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            if merge:
                current_settings = self.load_settings()
                current_settings.update(imported_settings)
                return self.save_settings(current_settings)
            else:
                return self.save_settings(imported_settings)
                
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
    
    def backup_settings(self, backup_path: Optional[str] = None) -> str:
        """
        Create a backup of current settings
        
        Args:
            backup_path: Optional custom backup path
            
        Returns:
            Path to backup file, or empty string if failed
        """
        try:
            if backup_path is None:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"settings_backup_{timestamp}.json"
                backup_path = os.path.join(self.config_dir, backup_filename)
            
            if self.export_settings(backup_path):
                return backup_path
            else:
                return ""
                
        except Exception as e:
            print(f"Error creating settings backup: {e}")
            return ""
    
    def get_config_info(self) -> Dict[str, Any]:
        """
        Get information about the configuration
        
        Returns:
            Dictionary with configuration information
        """
        return {
            'config_dir': self.config_dir,
            'config_file': self.config_file,
            'config_exists': os.path.exists(self.config_file),
            'config_size': os.path.getsize(self.config_file) if os.path.exists(self.config_file) else 0,
            'default_settings_count': len(self.default_settings),
            'app_name': self.app_name
        }
