"""
Configuration management for ABgrouponline.

This module provides configuration management capabilities including
loading from files, environment variables, and runtime configuration.
"""

import os
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for model-specific settings."""
    default_algorithm: str = "random_forest"
    hyperparameter_tuning: bool = True
    cv_folds: int = 5
    random_state: int = 42
    n_jobs: int = -1

@dataclass
class DataConfig:
    """Configuration for data processing settings."""
    correlation_threshold: float = 0.9
    polynomial_degree: int = 2
    test_size: float = 0.2
    validation_size: float = 0.15
    shuffle: bool = True
    stratify: bool = True

@dataclass
class LoggingConfig:
    """Configuration for logging settings."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_logging: bool = False
    log_dir: str = "logs"
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5

@dataclass
class CacheConfig:
    """Configuration for caching settings."""
    enabled: bool = True
    cache_dir: str = "cache"
    max_size: int = 1073741824  # 1GB
    ttl: int = 3600  # 1 hour

class Config:
    """
    Main configuration class for ABgrouponline.
    
    This class manages all configuration settings for the package,
    including model parameters, data processing settings, and system configuration.
    """
    
    def __init__(self):
        """Initialize configuration with defaults."""
        self.model = ModelConfig()
        self.data = DataConfig()
        self.logging = LoggingConfig()
        self.cache = CacheConfig()
        self._custom_config = {}
        
        # Load configuration from various sources
        self._load_from_environment()
        self._load_from_file()
    
    def _load_from_environment(self):
        """Load configuration from environment variables."""
        # Model configuration
        if "ABGROUP_ALGORITHM" in os.environ:
            self.model.default_algorithm = os.environ["ABGROUP_ALGORITHM"]
        
        if "ABGROUP_CV_FOLDS" in os.environ:
            self.model.cv_folds = int(os.environ["ABGROUP_CV_FOLDS"])
        
        if "ABGROUP_RANDOM_STATE" in os.environ:
            self.model.random_state = int(os.environ["ABGROUP_RANDOM_STATE"])
        
        # Data configuration
        if "ABGROUP_CORRELATION_THRESHOLD" in os.environ:
            self.data.correlation_threshold = float(os.environ["ABGROUP_CORRELATION_THRESHOLD"])
        
        if "ABGROUP_TEST_SIZE" in os.environ:
            self.data.test_size = float(os.environ["ABGROUP_TEST_SIZE"])
        
        # Logging configuration
        if "ABGROUP_LOG_LEVEL" in os.environ:
            self.logging.level = os.environ["ABGROUP_LOG_LEVEL"]
        
        if "ABGROUP_LOG_DIR" in os.environ:
            self.logging.log_dir = os.environ["ABGROUP_LOG_DIR"]
        
        # Cache configuration
        if "ABGROUP_CACHE_ENABLED" in os.environ:
            self.cache.enabled = os.environ["ABGROUP_CACHE_ENABLED"].lower() == "true"
        
        if "ABGROUP_CACHE_DIR" in os.environ:
            self.cache.cache_dir = os.environ["ABGROUP_CACHE_DIR"]
    
    def _load_from_file(self):
        """Load configuration from config files."""
        config_paths = [
            Path.home() / ".abgroup" / "config.yaml",
            Path.home() / ".abgroup" / "config.json",
            Path.cwd() / "abgroup_config.yaml",
            Path.cwd() / "abgroup_config.json",
            Path.cwd() / "config" / "abgroup.yaml",
            Path.cwd() / "config" / "abgroup.json"
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    self._load_config_file(config_path)
                    logger.info(f"Loaded configuration from {config_path}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to load config from {config_path}: {e}")
    
    def _load_config_file(self, config_path: Path):
        """Load configuration from a specific file."""
        with open(config_path, 'r') as f:
            if config_path.suffix == '.yaml' or config_path.suffix == '.yml':
                config_data = yaml.safe_load(f)
            elif config_path.suffix == '.json':
                config_data = json.load(f)
            else:
                raise ValueError(f"Unsupported config file format: {config_path.suffix}")
        
        # Update configuration from file
        if 'model' in config_data:
            for key, value in config_data['model'].items():
                if hasattr(self.model, key):
                    setattr(self.model, key, value)
        
        if 'data' in config_data:
            for key, value in config_data['data'].items():
                if hasattr(self.data, key):
                    setattr(self.data, key, value)
        
        if 'logging' in config_data:
            for key, value in config_data['logging'].items():
                if hasattr(self.logging, key):
                    setattr(self.logging, key, value)
        
        if 'cache' in config_data:
            for key, value in config_data['cache'].items():
                if hasattr(self.cache, key):
                    setattr(self.cache, key, value)
        
        # Store custom configuration
        for key, value in config_data.items():
            if key not in ['model', 'data', 'logging', 'cache']:
                self._custom_config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        
        # Check built-in configurations
        if keys[0] == 'model':
            obj = self.model
        elif keys[0] == 'data':
            obj = self.data
        elif keys[0] == 'logging':
            obj = self.logging
        elif keys[0] == 'cache':
            obj = self.cache
        else:
            # Check custom configuration
            obj = self._custom_config
        
        # Navigate through the keys
        for k in keys if keys[0] in self._custom_config else keys[1:]:
            if hasattr(obj, k):
                obj = getattr(obj, k)
            elif isinstance(obj, dict) and k in obj:
                obj = obj[k]
            else:
                return default
        
        return obj
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        
        # Set built-in configurations
        if keys[0] == 'model' and len(keys) > 1:
            if hasattr(self.model, keys[1]):
                setattr(self.model, keys[1], value)
            else:
                raise ValueError(f"Unknown model config key: {keys[1]}")
        elif keys[0] == 'data' and len(keys) > 1:
            if hasattr(self.data, keys[1]):
                setattr(self.data, keys[1], value)
            else:
                raise ValueError(f"Unknown data config key: {keys[1]}")
        elif keys[0] == 'logging' and len(keys) > 1:
            if hasattr(self.logging, keys[1]):
                setattr(self.logging, keys[1], value)
            else:
                raise ValueError(f"Unknown logging config key: {keys[1]}")
        elif keys[0] == 'cache' and len(keys) > 1:
            if hasattr(self.cache, keys[1]):
                setattr(self.cache, keys[1], value)
            else:
                raise ValueError(f"Unknown cache config key: {keys[1]}")
        else:
            # Set custom configuration
            obj = self._custom_config
            for k in keys[:-1]:
                if k not in obj:
                    obj[k] = {}
                obj = obj[k]
            obj[keys[-1]] = value
    
    def update(self, config_dict: Dict[str, Any]):
        """
        Update configuration with a dictionary.
        
        Args:
            config_dict: Dictionary of configuration updates
        """
        for key, value in config_dict.items():
            self.set(key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Configuration as dictionary
        """
        config_dict = {
            'model': asdict(self.model),
            'data': asdict(self.data),
            'logging': asdict(self.logging),
            'cache': asdict(self.cache)
        }
        config_dict.update(self._custom_config)
        return config_dict
    
    def save(self, filepath: Union[str, Path], format: str = 'yaml'):
        """
        Save configuration to file.
        
        Args:
            filepath: Path to save configuration
            format: File format ('yaml' or 'json')
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        config_dict = self.to_dict()
        
        with open(filepath, 'w') as f:
            if format == 'yaml':
                yaml.dump(config_dict, f, default_flow_style=False)
            elif format == 'json':
                json.dump(config_dict, f, indent=2)
            else:
                raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Configuration saved to {filepath}")
    
    def reset(self):
        """Reset configuration to defaults."""
        self.__init__()
    
    def validate(self) -> bool:
        """
        Validate configuration values.
        
        Returns:
            True if configuration is valid
        """
        try:
            # Validate model configuration
            assert self.model.cv_folds > 0, "cv_folds must be positive"
            assert self.model.random_state >= 0, "random_state must be non-negative"
            
            # Validate data configuration
            assert 0 < self.data.correlation_threshold <= 1, "correlation_threshold must be between 0 and 1"
            assert 0 < self.data.test_size < 1, "test_size must be between 0 and 1"
            assert 0 < self.data.validation_size < 1, "validation_size must be between 0 and 1"
            assert self.data.polynomial_degree >= 1, "polynomial_degree must be >= 1"
            
            # Validate logging configuration
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            assert self.logging.level in valid_levels, f"logging level must be one of {valid_levels}"
            
            # Validate cache configuration
            assert self.cache.max_size > 0, "cache max_size must be positive"
            assert self.cache.ttl > 0, "cache ttl must be positive"
            
            return True
            
        except AssertionError as e:
            logger.error(f"Configuration validation failed: {e}")
            return False

# Global configuration instance
_global_config = Config()

def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Global configuration instance
    """
    return _global_config

def set_config(config: Config):
    """
    Set the global configuration instance.
    
    Args:
        config: Configuration instance to set as global
    """
    global _global_config
    _global_config = config 