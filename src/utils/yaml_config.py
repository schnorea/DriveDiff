"""
YAML Configuration Manager Module
Handles loading, saving, and managing YAML configurations
"""

import os
import yaml
import shutil
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ScanConfiguration:
    """Configuration for scanning operations"""
    scan_paths: List[str]
    exclude_paths: List[str]
    include_patterns: List[str]
    exclude_patterns: List[str]
    logging_level: str
    worker_threads: int
    hash_chunk_size: int
    max_files: int

@dataclass
class ComparisonConfiguration:
    """Configuration for specific comparison type"""
    scan_paths: List[str]
    exclude_paths: List[str]
    include_patterns: List[str]
    exclude_patterns: List[str]

class YamlConfigManager:
    """Manages YAML configuration files"""
    
    def __init__(self, config_file_path: str = None):
        """
        Initialize YAML configuration manager
        
        Args:
            config_file_path: Path to the configuration file
        """
        self.config_file_path = config_file_path or "scan_config.yaml"
        self.default_config_path = "default.yaml"
        
        # Default configuration with separate directory and structure settings
        self.default_config = {
            'logging': {
                'level': 'INFO'
            },
            'directory_comparison': {
                'paths': {
                    'scan': [],
                    'exclude': [
                        '/proc',
                        '/sys',
                        '/dev',
                        '/run',
                        '/tmp',
                        '/var/tmp',
                        '/var/cache'
                    ],
                    'include': [
                        '*.conf',
                        '*.config',
                        '*.cfg',
                        '*.ini',
                        '*.json',
                        '*.yaml',
                        '*.yml',
                        '*.xml',
                        '*.txt',
                        '*.log'
                    ],
                    'exclude_patterns': [
                        '*/tmp/*',
                        '*/temp/*',
                        '*/.git/*',
                        '*/node_modules/*',
                        '*/__pycache__/*',
                        '*.pyc',
                        '*.pyo'
                    ]
                }
            },
            'structure_comparison': {
                'paths': {
                    'scan': [],
                    'exclude': [
                        '/proc',
                        '/sys',
                        '/dev',
                        '/run',
                        '/tmp',
                        '/var/tmp',
                        '/var/cache',
                        '/var/log',
                        '/var/spool'
                    ],
                    'exclude_patterns': [
                        '*/tmp/*',
                        '*/temp/*',
                        '*/.git/*',
                        '*/node_modules/*',
                        '*/__pycache__/*',
                        '*/venv/*',
                        '*/cache/*'
                    ]
                }
            },
            'performance': {
                'worker_threads': 4,
                'hash_chunk_size': 65536,
                'max_files': 0
            }
        }
    
    def load_config(self, file_path: str = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        
        Args:
            file_path: Optional path to config file
            
        Returns:
            Configuration dictionary
        """
        config_path = file_path or self.config_file_path
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config:
                        # Migrate legacy configuration if needed
                        config = self._migrate_legacy_config(config)
                        return self._merge_with_defaults(config)
            
            # If file doesn't exist or is empty, try default.yaml
            if os.path.exists(self.default_config_path):
                with open(self.default_config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config:
                        config = self._migrate_legacy_config(config)
                        return self._merge_with_defaults(config)
            
            # Return default configuration
            return self.default_config.copy()
            
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return self.default_config.copy()
    
    def _migrate_legacy_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migrate legacy configuration format to new dual structure
        
        Args:
            config: Configuration dictionary that may contain legacy format
            
        Returns:
            Migrated configuration dictionary
        """
        # If we have the old 'paths' format but not the new structure, migrate it
        if 'paths' in config and ('directory_comparison' not in config or 'structure_comparison' not in config):
            legacy_paths = config.get('paths', {})
            
            # Don't migrate if paths is empty (modern config)
            if any(legacy_paths.get(key) for key in ['scan', 'exclude', 'include', 'exclude_patterns']):
                print("Migrating legacy configuration to new format...")
                
                # Create directory_comparison from legacy paths
                if 'directory_comparison' not in config:
                    config['directory_comparison'] = {
                        'paths': {
                            'scan': legacy_paths.get('scan', []),
                            'exclude': legacy_paths.get('exclude', []),
                            'include': legacy_paths.get('include', []),
                            'exclude_patterns': legacy_paths.get('exclude_patterns', [])
                        }
                    }
                
                # Create structure_comparison with modified settings
                if 'structure_comparison' not in config:
                    # For structure comparison, exclude include patterns and add more aggressive exclusions
                    config['structure_comparison'] = {
                        'paths': {
                            'scan': legacy_paths.get('scan', []),
                            'exclude': legacy_paths.get('exclude', []) + ['/var/log', '/var/spool'],
                            'exclude_patterns': legacy_paths.get('exclude_patterns', [])
                        }
                    }
                
                # Clear legacy paths to avoid confusion
                config['paths'] = {
                    'scan': [],
                    'exclude': [],
                    'include': [],
                    'exclude_patterns': []
                }
        
        return config
    
    def save_config(self, config: Dict[str, Any], file_path: str = None) -> bool:
        """
        Save configuration to YAML file
        
        Args:
            config: Configuration dictionary to save
            file_path: Optional path to save file
            
        Returns:
            True if successful, False otherwise
        """
        config_path = file_path or self.config_file_path
        
        try:
            # Create backup if file exists
            if os.path.exists(config_path):
                backup_path = f"{config_path}.backup"
                shutil.copy2(config_path, backup_path)
            
            # Save configuration
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, indent=2, sort_keys=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def _merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded config with defaults"""
        merged = self.default_config.copy()
        
        def deep_merge(default: Dict, override: Dict):
            for key, value in override.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    deep_merge(default[key], value)
                else:
                    default[key] = value
        
        deep_merge(merged, config)
        return merged
    
    def get_scan_configuration(self, config: Dict[str, Any] = None) -> ScanConfiguration:
        """
        Get scan configuration object (legacy support - uses directory_comparison)
        
        Args:
            config: Optional config dict, loads from file if None
            
        Returns:
            ScanConfiguration object
        """
        if config is None:
            config = self.load_config()
        
        # Use directory_comparison as default for legacy support
        dir_config = self.get_directory_comparison_config(config)
        performance = config.get('performance', {})
        logging = config.get('logging', {})
        
        return ScanConfiguration(
            scan_paths=dir_config.scan_paths,
            exclude_paths=dir_config.exclude_paths,
            include_patterns=dir_config.include_patterns,
            exclude_patterns=dir_config.exclude_patterns,
            logging_level=logging.get('level', 'INFO'),
            worker_threads=performance.get('worker_threads', 4),
            hash_chunk_size=performance.get('hash_chunk_size', 65536),
            max_files=performance.get('max_files', 0)
        )
    
    def get_directory_comparison_config(self, config: Dict[str, Any] = None) -> ComparisonConfiguration:
        """
        Get directory comparison configuration
        
        Args:
            config: Optional config dict, loads from file if None
            
        Returns:
            ComparisonConfiguration object for directory comparison
        """
        if config is None:
            config = self.load_config()
        
        dir_comparison = config.get('directory_comparison', {})
        paths = dir_comparison.get('paths', {})
        
        return ComparisonConfiguration(
            scan_paths=paths.get('scan', []),
            exclude_paths=paths.get('exclude', []),
            include_patterns=paths.get('include', []),
            exclude_patterns=paths.get('exclude_patterns', [])
        )
    
    def get_structure_comparison_config(self, config: Dict[str, Any] = None) -> ComparisonConfiguration:
        """
        Get structure comparison configuration
        
        Args:
            config: Optional config dict, loads from file if None
            
        Returns:
            ComparisonConfiguration object for structure comparison
        """
        if config is None:
            config = self.load_config()
        
        struct_comparison = config.get('structure_comparison', {})
        paths = struct_comparison.get('paths', {})
        
        return ComparisonConfiguration(
            scan_paths=paths.get('scan', []),
            exclude_paths=paths.get('exclude', []),
            include_patterns=paths.get('include', []),  # May be empty for structure comparison
            exclude_patterns=paths.get('exclude_patterns', [])
        )
    
    def save_directory_comparison_config(self, comparison_config: ComparisonConfiguration, 
                                       config: Dict[str, Any] = None) -> bool:
        """
        Save directory comparison configuration
        
        Args:
            comparison_config: Configuration to save
            config: Optional existing config dict, loads from file if None
            
        Returns:
            True if successful, False otherwise
        """
        if config is None:
            config = self.load_config()
        
        if 'directory_comparison' not in config:
            config['directory_comparison'] = {}
        if 'paths' not in config['directory_comparison']:
            config['directory_comparison']['paths'] = {}
        
        paths = config['directory_comparison']['paths']
        paths['scan'] = comparison_config.scan_paths
        paths['exclude'] = comparison_config.exclude_paths
        paths['include'] = comparison_config.include_patterns
        paths['exclude_patterns'] = comparison_config.exclude_patterns
        
        return self.save_config(config)
    
    def save_structure_comparison_config(self, comparison_config: ComparisonConfiguration, 
                                       config: Dict[str, Any] = None) -> bool:
        """
        Save structure comparison configuration
        
        Args:
            comparison_config: Configuration to save
            config: Optional existing config dict, loads from file if None
            
        Returns:
            True if successful, False otherwise
        """
        if config is None:
            config = self.load_config()
        
        if 'structure_comparison' not in config:
            config['structure_comparison'] = {}
        if 'paths' not in config['structure_comparison']:
            config['structure_comparison']['paths'] = {}
        
        paths = config['structure_comparison']['paths']
        paths['scan'] = comparison_config.scan_paths
        paths['exclude'] = comparison_config.exclude_paths
        paths['include'] = comparison_config.include_patterns
        paths['exclude_patterns'] = comparison_config.exclude_patterns
        
        return self.save_config(config)
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate configuration
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate logging level
        logging_config = config.get('logging', {})
        level = logging_config.get('level', '')
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if level not in valid_levels:
            errors.append(f"Invalid logging level: {level}. Must be one of: {', '.join(valid_levels)}")
        
        # Validate performance settings
        performance = config.get('performance', {})
        
        worker_threads = performance.get('worker_threads', 0)
        if not isinstance(worker_threads, int) or worker_threads < 1 or worker_threads > 32:
            errors.append("Worker threads must be an integer between 1 and 32")
        
        hash_chunk_size = performance.get('hash_chunk_size', 0)
        if not isinstance(hash_chunk_size, int) or hash_chunk_size < 1024:
            errors.append("Hash chunk size must be an integer >= 1024 bytes")
        
        max_files = performance.get('max_files', 0)
        if not isinstance(max_files, int) or max_files < 0:
            errors.append("Max files must be a non-negative integer")
        
        # Validate paths
        paths = config.get('paths', {})
        
        scan_paths = paths.get('scan', [])
        if not isinstance(scan_paths, list):
            errors.append("Scan paths must be a list")
        
        exclude_paths = paths.get('exclude', [])
        if not isinstance(exclude_paths, list):
            errors.append("Exclude paths must be a list")
        
        include_patterns = paths.get('include', [])
        if not isinstance(include_patterns, list):
            errors.append("Include patterns must be a list")
        
        exclude_patterns = paths.get('exclude_patterns', [])
        if not isinstance(exclude_patterns, list):
            errors.append("Exclude patterns must be a list")
        
        return errors
    
    def export_config(self, config: Dict[str, Any], export_path: str) -> bool:
        """
        Export configuration to a specific file
        
        Args:
            config: Configuration to export
            export_path: Path to export file
            
        Returns:
            True if successful, False otherwise
        """
        return self.save_config(config, export_path)
    
    def import_config(self, import_path: str) -> Optional[Dict[str, Any]]:
        """
        Import configuration from a file
        
        Args:
            import_path: Path to import file
            
        Returns:
            Configuration dictionary or None if failed
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
                # Validate imported config
                errors = self.validate_config(config)
                if errors:
                    print(f"Configuration validation errors: {', '.join(errors)}")
                    return None
                
                return config
                
        except Exception as e:
            print(f"Error importing configuration: {e}")
            return None
    
    def _format_yaml_for_display(self, config: Dict[str, Any]) -> str:
        """Format configuration as YAML string for display"""
        try:
            return yaml.dump(config, default_flow_style=False, indent=2, sort_keys=False)
        except Exception as e:
            return f"Error formatting YAML: {e}"
