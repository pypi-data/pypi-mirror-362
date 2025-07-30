"""
Configuration class for the core module.
"""

from ..utils.config import Config as BaseConfig, get_config

# Re-export the main Config class
Config = BaseConfig

def get_core_config():
    """Get the global configuration instance."""
    return get_config() 