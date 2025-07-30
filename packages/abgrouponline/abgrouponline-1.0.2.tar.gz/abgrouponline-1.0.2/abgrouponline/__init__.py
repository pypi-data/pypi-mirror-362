"""
ABgrouponline: State-of-the-Art Machine Learning Model Framework

A comprehensive Python package for loading, managing, and deploying state-of-the-art 
machine learning models based on the latest research publications.

Compatible with Python 3.8+ including Python 3.13.
"""

__version__ = "1.0.2"
__author__ = "ABGroup Research Team"
__email__ = "research@abgrouponline.com"

import sys
import warnings
from typing import Dict, Any, Optional

# Import compatibility utilities
from .utils.compatibility import (
    get_compatibility_manager,
    safe_import,
    check_tensorflow_support,
    warn_if_tensorflow_unavailable
)

# Core imports that should always work
from .core import (
    BaseModel,
    ModelManager,
    ModelRegistry,
    ModelLoader,
    Config
)

# Healthcare models
from .healthcare import DiabetesClassifier

# Utilities
from .utils import setup_logging, get_logger

# Check compatibility on import
_compat_manager = get_compatibility_manager()
_python_version = sys.version_info

# Issue warnings for known compatibility issues
if _python_version >= (3, 13) and not _compat_manager.is_available('tensorflow'):
    warnings.warn(
        f"Running on Python {_python_version.major}.{_python_version.minor}. "
        f"TensorFlow features are not available but all other functionality works normally. "
        f"For full TensorFlow support, use Python 3.8-3.12.",
        UserWarning,
        stacklevel=2
    )


def get_version_info() -> Dict[str, Any]:
    """Get comprehensive version and compatibility information."""
    return {
        'abgrouponline_version': __version__,
        'python_version': f"{_python_version.major}.{_python_version.minor}.{_python_version.micro}",
        'compatibility_report': _compat_manager.get_compatibility_report(),
        'tensorflow_support': check_tensorflow_support(),
    }


def print_version_info():
    """Print version and compatibility information."""
    info = get_version_info()
    
    print(f"ABgrouponline v{info['abgrouponline_version']}")
    print(f"Python {info['python_version']}")
    
    tf_supported, tf_message = info['tensorflow_support']
    print(f"TensorFlow: {'✅' if tf_supported else '❌'} {tf_message}")
    
    report = info['compatibility_report']
    available_count = len(report['available_modules'])
    total_count = available_count + len(report['unavailable_modules'])
    
    print(f"Dependencies: {available_count}/{total_count} available")
    print(f"Status: {report['recommended_action']}")


def load_model(model_name: str, **kwargs):
    """
    Load a model by name.
    
    Args:
        model_name: Name of the model to load
        **kwargs: Additional arguments for model loading
        
    Returns:
        Loaded model instance
    """
    manager = ModelManager()
    return manager.load_model(model_name, **kwargs)


def list_available_models() -> Dict[str, Any]:
    """
    List all available models and their compatibility status.
    
    Returns:
        Dictionary of available models with their status
    """
    models = {
        'diabetes_classifier': {
            'description': 'Advanced diabetes prediction with 12 ML algorithms',
            'requires_tensorflow': False,
            'compatible': True,
            'algorithms': [
                'Random Forest', 'XGBoost', 'LightGBM', 'CatBoost',
                'SVM', 'KNN', 'Naive Bayes', 'Logistic Regression',
                'Decision Tree', 'Extra Trees', 'AdaBoost', 'Neural Network'
            ]
        }
    }
    
    # Add TensorFlow-based models if available
    if _compat_manager.is_available('tensorflow'):
        models['tensorflow_models'] = {
            'description': 'TensorFlow/Keras-based deep learning models',
            'requires_tensorflow': True,
            'compatible': True,
            'note': 'Available with current setup'
        }
    else:
        models['tensorflow_models'] = {
            'description': 'TensorFlow/Keras-based deep learning models',
            'requires_tensorflow': True,
            'compatible': False,
            'note': 'Requires TensorFlow (Python 3.8-3.12)'
        }
    
    return models


# Convenience exports
__all__ = [
    # Version info
    '__version__',
    'get_version_info',
    'print_version_info',
    
    # Core classes
    'BaseModel',
    'ModelManager',
    'ModelRegistry',
    'ModelLoader',
    'Config',
    
    # Healthcare models
    'DiabetesClassifier',
    
    # Utilities
    'setup_logging',
    'get_logger',
    'load_model',
    'list_available_models',
    
    # Compatibility utilities
    'safe_import',
    'check_tensorflow_support',
    'get_compatibility_manager',
] 