"""
Model registry for ABgrouponline package.

This module provides a centralized registry for managing different model types,
allowing for dynamic model creation and discovery.
"""

import logging
import inspect
from typing import Dict, Any, List, Type, Callable, Optional
from .base_model import BaseModel

logger = logging.getLogger(__name__)

class ModelRegistry:
    """
    Registry for managing model types and their metadata.
    
    This class provides a centralized way to register, discover, and create
    different model types in the ABgrouponline package.
    """
    
    def __init__(self):
        """Initialize the model registry."""
        self._models: Dict[str, Dict[str, Any]] = {}
        self._initialized = False
        
    def register(self, 
                 name: str, 
                 model_class: Type[BaseModel], 
                 description: str = "",
                 category: str = "general",
                 tags: List[str] = None,
                 **metadata) -> None:
        """
        Register a model class with the registry.
        
        Args:
            name: Unique name for the model
            model_class: Model class to register
            description: Description of the model
            category: Model category (e.g., 'healthcare', 'nlp')
            tags: List of tags for categorization
            **metadata: Additional metadata
        """
        if not inspect.isclass(model_class):
            raise ValueError(f"model_class must be a class, got {type(model_class)}")
        
        if not issubclass(model_class, BaseModel):
            raise ValueError(f"model_class must inherit from BaseModel")
        
        if name in self._models:
            logger.warning(f"Overwriting existing model registration: {name}")
        
        model_info = {
            'class': model_class,
            'description': description,
            'category': category,
            'tags': tags or [],
            'module': model_class.__module__,
            'registered_at': None,
            **metadata
        }
        
        # Add creation time
        import pandas as pd
        model_info['registered_at'] = pd.Timestamp.now().isoformat()
        
        self._models[name] = model_info
        logger.info(f"Registered model: {name} ({model_class.__name__})")
    
    def unregister(self, name: str) -> None:
        """
        Unregister a model from the registry.
        
        Args:
            name: Name of the model to unregister
        """
        if name not in self._models:
            raise ValueError(f"Model '{name}' not found in registry")
        
        del self._models[name]
        logger.info(f"Unregistered model: {name}")
    
    def create_model(self, name: str, **kwargs) -> BaseModel:
        """
        Create an instance of a registered model.
        
        Args:
            name: Name of the model to create
            **kwargs: Arguments to pass to the model constructor
            
        Returns:
            Model instance
        """
        if name not in self._models:
            available = list(self._models.keys())
            raise ValueError(f"Model '{name}' not found. Available models: {available}")
        
        model_class = self._models[name]['class']
        
        try:
            return model_class(**kwargs)
        except Exception as e:
            logger.error(f"Failed to create model '{name}': {e}")
            raise
    
    def get_model_info(self, name: str) -> Dict[str, Any]:
        """
        Get information about a registered model.
        
        Args:
            name: Name of the model
            
        Returns:
            Model information dictionary
        """
        if name not in self._models:
            raise ValueError(f"Model '{name}' not found in registry")
        
        info = self._models[name].copy()
        # Don't return the actual class in the info
        info['class_name'] = info['class'].__name__
        del info['class']
        return info
    
    def list_models(self, category: str = None, tags: List[str] = None) -> List[str]:
        """
        List all registered models, optionally filtered by category or tags.
        
        Args:
            category: Filter by category
            tags: Filter by tags (models must have all specified tags)
            
        Returns:
            List of model names
        """
        models = []
        
        for name, info in self._models.items():
            # Filter by category
            if category and info.get('category') != category:
                continue
            
            # Filter by tags
            if tags and not all(tag in info.get('tags', []) for tag in tags):
                continue
            
            models.append(name)
        
        return sorted(models)
    
    def get_categories(self) -> List[str]:
        """
        Get all available model categories.
        
        Returns:
            List of categories
        """
        categories = set()
        for info in self._models.values():
            categories.add(info.get('category', 'general'))
        return sorted(list(categories))
    
    def get_tags(self) -> List[str]:
        """
        Get all available tags.
        
        Returns:
            List of tags
        """
        tags = set()
        for info in self._models.values():
            tags.update(info.get('tags', []))
        return sorted(list(tags))
    
    def search_models(self, query: str) -> List[str]:
        """
        Search for models by name, description, or tags.
        
        Args:
            query: Search query
            
        Returns:
            List of matching model names
        """
        query = query.lower()
        matches = []
        
        for name, info in self._models.items():
            # Check name
            if query in name.lower():
                matches.append(name)
                continue
            
            # Check description
            if query in info.get('description', '').lower():
                matches.append(name)
                continue
            
            # Check tags
            if any(query in tag.lower() for tag in info.get('tags', [])):
                matches.append(name)
                continue
        
        return sorted(matches)
    
    def get_model_dependencies(self, name: str) -> List[str]:
        """
        Get the dependencies for a model.
        
        Args:
            name: Name of the model
            
        Returns:
            List of dependencies
        """
        if name not in self._models:
            raise ValueError(f"Model '{name}' not found in registry")
        
        info = self._models[name]
        return info.get('dependencies', [])
    
    def validate_model(self, name: str) -> bool:
        """
        Validate that a model can be created successfully.
        
        Args:
            name: Name of the model to validate
            
        Returns:
            True if model can be created, False otherwise
        """
        try:
            model = self.create_model(name)
            return True
        except Exception as e:
            logger.warning(f"Model validation failed for '{name}': {e}")
            return False
    
    def export_registry(self) -> Dict[str, Any]:
        """
        Export the registry as a dictionary.
        
        Returns:
            Registry data
        """
        export_data = {}
        for name, info in self._models.items():
            export_data[name] = {
                'class_name': info['class'].__name__,
                'module': info['module'],
                'description': info.get('description', ''),
                'category': info.get('category', 'general'),
                'tags': info.get('tags', []),
                'registered_at': info.get('registered_at')
            }
        return export_data
    
    def initialize_builtin_models(self) -> None:
        """Initialize built-in models in the registry."""
        if self._initialized:
            return
        
        try:
            # Import and register healthcare models
            self._register_healthcare_models()
            
            # Import and register brain imaging models
            self._register_brain_imaging_models()
            
            # Import and register language models
            self._register_language_models()
            
            # Import and register forecasting models
            self._register_forecasting_models()
            
            self._initialized = True
            logger.info("Built-in models initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize built-in models: {e}")
    
    def _register_healthcare_models(self) -> None:
        """Register healthcare models."""
        try:
            from ..healthcare import DiabetesClassifier, TranslationalMedicine
            
            self.register(
                'diabetes_classifier',
                DiabetesClassifier,
                description="Advanced diabetes prediction with imbalance handling",
                category="healthcare",
                tags=["classification", "healthcare", "imbalanced-data", "ensemble"]
            )
            
            self.register(
                'translational_medicine',
                TranslationalMedicine,
                description="Disease outcome prediction framework",
                category="healthcare",
                tags=["prediction", "healthcare", "translational-medicine"]
            )
            
        except ImportError as e:
            logger.warning(f"Failed to register healthcare models: {e}")
    
    def _register_brain_imaging_models(self) -> None:
        """Register brain imaging models."""
        try:
            from ..brain_imaging import GM_LDM, BrainAutoencoder
            
            self.register(
                'gm_ldm',
                GM_LDM,
                description="Latent diffusion model for brain biomarker identification",
                category="brain_imaging",
                tags=["diffusion", "brain", "biomarker", "generative"]
            )
            
            self.register(
                'brain_autoencoder',
                BrainAutoencoder,
                description="3D autoencoder for brain data",
                category="brain_imaging",
                tags=["autoencoder", "brain", "3d", "dimensionality-reduction"]
            )
            
        except ImportError as e:
            logger.warning(f"Failed to register brain imaging models: {e}")
    
    def _register_language_models(self) -> None:
        """Register language models."""
        try:
            from ..language_models import ABCAlign, ConstitutionalAI
            
            self.register(
                'abc_align',
                ABCAlign,
                description="Safety and accuracy alignment framework for LLMs",
                category="language_models",
                tags=["alignment", "safety", "llm", "nlp"]
            )
            
            self.register(
                'constitutional_ai',
                ConstitutionalAI,
                description="Principle-based model alignment",
                category="language_models",
                tags=["constitutional", "alignment", "principles", "llm"]
            )
            
        except ImportError as e:
            logger.warning(f"Failed to register language models: {e}")
    
    def _register_forecasting_models(self) -> None:
        """Register forecasting models."""
        try:
            from ..forecasting import NourishNet, SeverityPredictor
            
            self.register(
                'nourish_net',
                NourishNet,
                description="Food commodity price forecasting",
                category="forecasting",
                tags=["timeseries", "forecasting", "commodity", "economic"]
            )
            
            self.register(
                'severity_predictor',
                SeverityPredictor,
                description="Early warning system for market disruptions",
                category="forecasting",
                tags=["prediction", "warning", "severity", "classification"]
            )
            
        except ImportError as e:
            logger.warning(f"Failed to register forecasting models: {e}")
    
    def __len__(self) -> int:
        """Return the number of registered models."""
        return len(self._models)
    
    def __contains__(self, name: str) -> bool:
        """Check if a model is registered."""
        return name in self._models
    
    def __iter__(self):
        """Iterate over registered model names."""
        return iter(self._models.keys())


# Global registry instance
_global_registry = ModelRegistry()

def register_model(name: str, 
                   model_class: Type[BaseModel] = None, 
                   **kwargs) -> Callable:
    """
    Decorator for registering models with the global registry.
    
    Args:
        name: Name to register the model under
        model_class: Model class (if not using as decorator)
        **kwargs: Additional metadata
        
    Returns:
        Decorator function or None
        
    Example:
        @register_model('my_model', category='custom')
        class MyModel(BaseModel):
            pass
    """
    def decorator(cls):
        _global_registry.register(name, cls, **kwargs)
        return cls
    
    if model_class is not None:
        # Direct registration
        _global_registry.register(name, model_class, **kwargs)
        return model_class
    else:
        # Decorator usage
        return decorator

def get_global_registry() -> ModelRegistry:
    """
    Get the global model registry instance.
    
    Returns:
        Global registry instance
    """
    return _global_registry 