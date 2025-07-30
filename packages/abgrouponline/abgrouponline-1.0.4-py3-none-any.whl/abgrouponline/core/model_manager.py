"""
Model manager for ABgrouponline.

This module provides a centralized way to manage multiple models,
handle model lifecycles, and coordinate model operations.
"""

import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import json
import threading
from concurrent.futures import ThreadPoolExecutor

from .base_model import BaseModel
from .model_loader import ModelLoader
from .registry import get_global_registry

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Central manager for handling multiple models and their operations.
    
    This class provides functionality to manage model lifecycles, coordinate
    training operations, handle model serving, and manage resources.
    """
    
    def __init__(self, 
                 model_dir: Union[str, Path] = None,
                 max_workers: int = 4):
        """
        Initialize the model manager.
        
        Args:
            model_dir: Directory for storing models
            max_workers: Maximum number of worker threads
        """
        self.model_loader = ModelLoader(model_dir)
        self.registry = get_global_registry()
        self.max_workers = max_workers
        
        # Active models storage
        self._models: Dict[str, BaseModel] = {}
        self._model_metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        
        # Thread pool for async operations
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        
        logger.info(f"ModelManager initialized with {max_workers} workers")
    
    def create_model(self, 
                     model_type: str, 
                     model_id: str = None,
                     **kwargs) -> str:
        """
        Create a new model instance.
        
        Args:
            model_type: Type of model to create
            model_id: Unique identifier for the model (auto-generated if None)
            **kwargs: Model initialization parameters
            
        Returns:
            Model ID
        """
        if model_id is None:
            import uuid
            model_id = f"{model_type}_{uuid.uuid4().hex[:8]}"
        
        with self._lock:
            if model_id in self._models:
                raise ValueError(f"Model with ID '{model_id}' already exists")
            
            # Create model instance
            model = self.registry.create_model(model_type, **kwargs)
            
            # Store model and metadata
            self._models[model_id] = model
            self._model_metadata[model_id] = {
                'type': model_type,
                'created_at': pd.Timestamp.now().isoformat(),
                'parameters': kwargs,
                'status': 'created'
            }
            
            logger.info(f"Created model '{model_id}' of type '{model_type}'")
            return model_id
    
    def load_model(self, 
                   model_name: str, 
                   model_id: str = None,
                   version: str = "latest",
                   **kwargs) -> str:
        """
        Load a model from storage or registry.
        
        Args:
            model_name: Name of the model to load
            model_id: ID to assign to the loaded model (auto-generated if None)
            version: Model version to load
            **kwargs: Additional loading parameters
            
        Returns:
            Model ID
        """
        if model_id is None:
            import uuid
            model_id = f"{model_name}_{uuid.uuid4().hex[:8]}"
        
        with self._lock:
            if model_id in self._models:
                raise ValueError(f"Model with ID '{model_id}' already exists")
            
            # Load model
            model = self.model_loader.load_model(model_name, version, **kwargs)
            
            # Store model and metadata
            self._models[model_id] = model
            self._model_metadata[model_id] = {
                'name': model_name,
                'version': version,
                'loaded_at': pd.Timestamp.now().isoformat(),
                'status': 'loaded'
            }
            
            logger.info(f"Loaded model '{model_name}' as '{model_id}'")
            return model_id
    
    def get_model(self, model_id: str) -> BaseModel:
        """
        Get a model by its ID.
        
        Args:
            model_id: Model identifier
            
        Returns:
            Model instance
        """
        with self._lock:
            if model_id not in self._models:
                raise ValueError(f"Model '{model_id}' not found")
            return self._models[model_id]
    
    def remove_model(self, model_id: str) -> bool:
        """
        Remove a model from the manager.
        
        Args:
            model_id: Model identifier
            
        Returns:
            True if model was removed successfully
        """
        with self._lock:
            if model_id not in self._models:
                logger.warning(f"Model '{model_id}' not found")
                return False
            
            del self._models[model_id]
            del self._model_metadata[model_id]
            
            logger.info(f"Removed model '{model_id}'")
            return True
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all active models.
        
        Returns:
            List of model information
        """
        with self._lock:
            models_info = []
            for model_id, model in self._models.items():
                metadata = self._model_metadata[model_id].copy()
                metadata.update({
                    'id': model_id,
                    'fitted': model.is_fitted,
                    'model_name': model.model_name,
                    'model_type': model.model_type
                })
                models_info.append(metadata)
            
            return models_info
    
    def train_model(self, 
                    model_id: str, 
                    X, y=None, 
                    async_training: bool = False,
                    **kwargs):
        """
        Train a model.
        
        Args:
            model_id: Model identifier
            X: Training features
            y: Training targets
            async_training: Whether to train asynchronously
            **kwargs: Training parameters
            
        Returns:
            Training result or Future if async
        """
        model = self.get_model(model_id)
        
        def train_fn():
            try:
                with self._lock:
                    self._model_metadata[model_id]['status'] = 'training'
                
                logger.info(f"Starting training for model '{model_id}'")
                result = model.fit(X, y, **kwargs)
                
                with self._lock:
                    self._model_metadata[model_id]['status'] = 'trained'
                    self._model_metadata[model_id]['trained_at'] = pd.Timestamp.now().isoformat()
                
                logger.info(f"Training completed for model '{model_id}'")
                return result
                
            except Exception as e:
                with self._lock:
                    self._model_metadata[model_id]['status'] = 'error'
                    self._model_metadata[model_id]['error'] = str(e)
                
                logger.error(f"Training failed for model '{model_id}': {e}")
                raise
        
        if async_training:
            return self._executor.submit(train_fn)
        else:
            return train_fn()
    
    def predict(self, model_id: str, X, **kwargs):
        """
        Make predictions using a model.
        
        Args:
            model_id: Model identifier
            X: Input features
            **kwargs: Prediction parameters
            
        Returns:
            Predictions
        """
        model = self.get_model(model_id)
        
        if not model.is_fitted:
            raise ValueError(f"Model '{model_id}' is not trained")
        
        return model.predict(X, **kwargs)
    
    def predict_proba(self, model_id: str, X, **kwargs):
        """
        Get prediction probabilities using a model.
        
        Args:
            model_id: Model identifier
            X: Input features
            **kwargs: Prediction parameters
            
        Returns:
            Prediction probabilities
        """
        model = self.get_model(model_id)
        
        if not model.is_fitted:
            raise ValueError(f"Model '{model_id}' is not trained")
        
        return model.predict_proba(X, **kwargs)
    
    def evaluate_model(self, model_id: str, X, y, **kwargs) -> Dict[str, Any]:
        """
        Evaluate a model's performance.
        
        Args:
            model_id: Model identifier
            X: Test features
            y: True targets
            **kwargs: Evaluation parameters
            
        Returns:
            Evaluation results
        """
        model = self.get_model(model_id)
        
        if not model.is_fitted:
            raise ValueError(f"Model '{model_id}' is not trained")
        
        # Use model's built-in evaluation if available
        if hasattr(model, 'evaluate'):
            return model.evaluate(X, y, **kwargs)
        else:
            # Basic evaluation
            score = model.score(X, y, **kwargs)
            return {'score': score}
    
    def save_model(self, 
                   model_id: str, 
                   name: str = None,
                   version: str = None,
                   metadata: Dict[str, Any] = None) -> Path:
        """
        Save a model to storage.
        
        Args:
            model_id: Model identifier
            name: Name to save the model under
            version: Version string
            metadata: Additional metadata
            
        Returns:
            Path where model was saved
        """
        model = self.get_model(model_id)
        
        if name is None:
            name = f"model_{model_id}"
        
        # Combine metadata
        combined_metadata = self._model_metadata[model_id].copy()
        if metadata:
            combined_metadata.update(metadata)
        
        return self.model_loader.save_model(model, name, version, combined_metadata)
    
    def compare_models(self, 
                       model_ids: List[str], 
                       X, y,
                       metrics: List[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Compare performance of multiple models.
        
        Args:
            model_ids: List of model identifiers
            X: Test features
            y: True targets
            metrics: List of metrics to compute
            
        Returns:
            Comparison results
        """
        if metrics is None:
            metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        
        results = {}
        
        for model_id in model_ids:
            try:
                model_results = self.evaluate_model(model_id, X, y)
                results[model_id] = model_results
            except Exception as e:
                logger.error(f"Failed to evaluate model '{model_id}': {e}")
                results[model_id] = {'error': str(e)}
        
        return results
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a model.
        
        Args:
            model_id: Model identifier
            
        Returns:
            Model information
        """
        with self._lock:
            if model_id not in self._models:
                raise ValueError(f"Model '{model_id}' not found")
            
            model = self._models[model_id]
            metadata = self._model_metadata[model_id].copy()
            
            # Add model summary
            model_summary = model.summary()
            metadata.update(model_summary)
            
            return metadata
    
    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up ModelManager resources")
        
        with self._lock:
            # Clear models
            self._models.clear()
            self._model_metadata.clear()
        
        # Shutdown executor
        self._executor.shutdown(wait=True)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
    
    def __len__(self) -> int:
        """Return number of active models."""
        return len(self._models)
    
    def __contains__(self, model_id: str) -> bool:
        """Check if a model exists."""
        return model_id in self._models
    
    def __iter__(self):
        """Iterate over model IDs."""
        return iter(self._models.keys())

# Import pandas for timestamps
import pandas as pd 