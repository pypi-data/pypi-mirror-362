"""
ABgrouponline: State-of-the-Art Machine Learning Model Framework

A comprehensive package for loading, managing, and deploying cutting-edge 
machine learning models based on recent research publications.
"""

__version__ = "1.0.0"
__author__ = "ABgroup Research Team"
__email__ = "research@abgroup.online"

import logging
import warnings
from typing import Dict, Any, Optional, Union, List

# Core imports
from .core import ModelManager, BaseModel, ModelRegistry
from .utils import setup_logging, get_config

# Model categories
from . import healthcare
from . import brain_imaging
from . import language_models
from . import forecasting
from . import preprocessing
from . import evaluation
from . import data

# Key classes and functions
from .core.model_loader import load_model, list_available_models
from .core.registry import register_model

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Model registry instance
_model_registry = ModelRegistry()

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")

def create_model(model_type: str, **kwargs) -> BaseModel:
    """
    Create a model instance of the specified type.
    
    Args:
        model_type: Type of model to create
        **kwargs: Additional arguments for model initialization
        
    Returns:
        Model instance
        
    Example:
        >>> from abgrouponline import create_model
        >>> model = create_model('diabetes_classifier', model_type='random_forest')
    """
    return _model_registry.create_model(model_type, **kwargs)

def get_model_info(model_type: str) -> Dict[str, Any]:
    """
    Get information about a specific model type.
    
    Args:
        model_type: Type of model
        
    Returns:
        Model information dictionary
    """
    return _model_registry.get_model_info(model_type)

def list_models() -> List[str]:
    """
    List all available model types.
    
    Returns:
        List of available model types
    """
    return _model_registry.list_models()

# Version check and compatibility
def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import torch
        import sklearn
        import pandas
        import numpy
        logger.info("All core dependencies are installed")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return False

# Package initialization
logger.info(f"ABgrouponline v{__version__} initialized")
if not check_dependencies():
    logger.warning("Some dependencies are missing. Please install them for full functionality.")

# Export main classes and functions
__all__ = [
    # Core
    'ModelManager',
    'BaseModel',
    'ModelRegistry',
    'load_model',
    'create_model',
    'register_model',
    'list_available_models',
    'get_model_info',
    'list_models',
    
    # Modules
    'healthcare',
    'brain_imaging', 
    'language_models',
    'forecasting',
    'preprocessing',
    'evaluation',
    'data',
    
    # Utilities
    'setup_logging',
    'get_config',
    'check_dependencies',
]

# Model type shortcuts for easier access
HEALTHCARE_MODELS = [
    'diabetes_classifier',
    'translational_medicine',
    'ensemble_healthcare'
]

BRAIN_IMAGING_MODELS = [
    'gm_ldm',
    'brain_autoencoder',
    'functional_connectivity'
]

LANGUAGE_MODELS = [
    'abc_align',
    'constitutional_ai',
    'preference_optimization'
]

FORECASTING_MODELS = [
    'nourish_net',
    'severity_predictor',
    'timeseries_ensemble'
]

NEXT_GEN_MODELS = [
    'recurrent_expansion',
    'multiverse_framework',
    'adaptive_system'
]

# Quick access dictionaries
MODEL_CATEGORIES = {
    'healthcare': HEALTHCARE_MODELS,
    'brain_imaging': BRAIN_IMAGING_MODELS,
    'language_models': LANGUAGE_MODELS,
    'forecasting': FORECASTING_MODELS,
    'next_generation': NEXT_GEN_MODELS
}

def get_models_by_category(category: str) -> List[str]:
    """
    Get all models in a specific category.
    
    Args:
        category: Model category name
        
    Returns:
        List of model names in the category
    """
    return MODEL_CATEGORIES.get(category, [])

# Add to exports
__all__.extend(['MODEL_CATEGORIES', 'get_models_by_category']) 