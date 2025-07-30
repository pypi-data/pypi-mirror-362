"""
Model loading utilities for ABgrouponline.

This module provides functions to load pre-trained models, manage model
repositories, and handle model versioning.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from .registry import get_global_registry
from .base_model import BaseModel

logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Model loader for managing pre-trained models and model repositories.
    """
    
    def __init__(self, model_dir: Union[str, Path] = None):
        """
        Initialize the model loader.
        
        Args:
            model_dir: Directory containing pre-trained models
        """
        self.model_dir = Path(model_dir) if model_dir else Path.home() / ".abgroup" / "models"
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.registry = get_global_registry()
    
    def load_model(self, 
                   model_name: str, 
                   version: str = "latest",
                   **kwargs) -> BaseModel:
        """
        Load a pre-trained model.
        
        Args:
            model_name: Name of the model to load
            version: Model version to load
            **kwargs: Additional arguments for model initialization
            
        Returns:
            Loaded model instance
        """
        # Check if model is registered
        if model_name in self.registry:
            logger.info(f"Creating new instance of registered model: {model_name}")
            return self.registry.create_model(model_name, **kwargs)
        
        # Try to load from disk
        model_path = self._find_model_path(model_name, version)
        if model_path:
            logger.info(f"Loading model from disk: {model_path}")
            return self._load_from_disk(model_path, **kwargs)
        
        # Try to download from repository
        try:
            logger.info(f"Attempting to download model: {model_name}")
            return self._download_and_load(model_name, version, **kwargs)
        except Exception as e:
            logger.error(f"Failed to download model: {e}")
        
        raise ValueError(f"Model '{model_name}' not found in registry, local storage, or repository")
    
    def _find_model_path(self, model_name: str, version: str) -> Optional[Path]:
        """
        Find the path to a locally stored model.
        
        Args:
            model_name: Name of the model
            version: Model version
            
        Returns:
            Path to model file if found, None otherwise
        """
        model_subdir = self.model_dir / model_name
        if not model_subdir.exists():
            return None
        
        # Look for specific version
        if version != "latest":
            version_path = model_subdir / f"{version}.joblib"
            if version_path.exists():
                return version_path
        
        # Look for latest version
        model_files = list(model_subdir.glob("*.joblib"))
        if model_files:
            # Return the most recently modified file
            latest_file = max(model_files, key=lambda p: p.stat().st_mtime)
            return latest_file
        
        return None
    
    def _load_from_disk(self, model_path: Path, **kwargs) -> BaseModel:
        """
        Load a model from disk.
        
        Args:
            model_path: Path to model file
            **kwargs: Additional arguments
            
        Returns:
            Loaded model instance
        """
        try:
            # Try different loading methods
            if model_path.suffix == '.joblib':
                import joblib
                model = joblib.load(model_path)
            elif model_path.suffix == '.pkl':
                import pickle
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
            else:
                raise ValueError(f"Unsupported model file format: {model_path.suffix}")
            
            if not isinstance(model, BaseModel):
                raise ValueError("Loaded object is not a valid ABgrouponline model")
            
            return model
            
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {e}")
            raise
    
    def _download_and_load(self, model_name: str, version: str, **kwargs) -> BaseModel:
        """
        Download and load a model from remote repository.
        
        Args:
            model_name: Name of the model
            version: Model version
            **kwargs: Additional arguments
            
        Returns:
            Downloaded and loaded model
        """
        # This is a placeholder for future implementation
        # In a real implementation, this would download from Hugging Face Hub,
        # GitHub releases, or custom model repositories
        
        logger.warning("Model downloading not yet implemented")
        raise NotImplementedError("Model downloading from remote repositories not yet implemented")
    
    def list_local_models(self) -> List[Dict[str, Any]]:
        """
        List all locally stored models.
        
        Returns:
            List of model information dictionaries
        """
        models = []
        
        if not self.model_dir.exists():
            return models
        
        for model_subdir in self.model_dir.iterdir():
            if model_subdir.is_dir():
                model_files = list(model_subdir.glob("*.joblib")) + list(model_subdir.glob("*.pkl"))
                
                for model_file in model_files:
                    try:
                        stat = model_file.stat()
                        model_info = {
                            'name': model_subdir.name,
                            'version': model_file.stem,
                            'path': str(model_file),
                            'size_mb': stat.st_size / (1024 * 1024),
                            'modified': stat.st_mtime
                        }
                        models.append(model_info)
                    except Exception as e:
                        logger.warning(f"Error reading model file {model_file}: {e}")
        
        return sorted(models, key=lambda x: x['modified'], reverse=True)
    
    def save_model(self, 
                   model: BaseModel, 
                   model_name: str, 
                   version: str = None,
                   metadata: Dict[str, Any] = None) -> Path:
        """
        Save a model to local storage.
        
        Args:
            model: Model to save
            model_name: Name for the model
            version: Version string (auto-generated if None)
            metadata: Additional metadata to save
            
        Returns:
            Path where model was saved
        """
        if version is None:
            import time
            version = f"v{int(time.time())}"
        
        model_subdir = self.model_dir / model_name
        model_subdir.mkdir(parents=True, exist_ok=True)
        
        model_path = model_subdir / f"{version}.joblib"
        model.save(model_path)
        
        # Save metadata if provided
        if metadata:
            metadata_path = model_subdir / f"{version}_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {model_path}")
        return model_path
    
    def delete_model(self, model_name: str, version: str = None) -> bool:
        """
        Delete a locally stored model.
        
        Args:
            model_name: Name of the model
            version: Version to delete (deletes all if None)
            
        Returns:
            True if deletion was successful
        """
        model_subdir = self.model_dir / model_name
        
        if not model_subdir.exists():
            logger.warning(f"Model directory not found: {model_subdir}")
            return False
        
        try:
            if version:
                # Delete specific version
                model_file = model_subdir / f"{version}.joblib"
                metadata_file = model_subdir / f"{version}_metadata.json"
                
                if model_file.exists():
                    model_file.unlink()
                if metadata_file.exists():
                    metadata_file.unlink()
                
                logger.info(f"Deleted model version {version}")
            else:
                # Delete entire model directory
                import shutil
                shutil.rmtree(model_subdir)
                logger.info(f"Deleted all versions of model {model_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete model: {e}")
            return False

# Global model loader instance
_global_loader = ModelLoader()

def load_model(model_name: str, version: str = "latest", **kwargs) -> BaseModel:
    """
    Load a model using the global model loader.
    
    Args:
        model_name: Name of the model to load
        version: Model version to load
        **kwargs: Additional arguments for model initialization
        
    Returns:
        Loaded model instance
    """
    return _global_loader.load_model(model_name, version, **kwargs)

def list_available_models() -> List[Dict[str, Any]]:
    """
    List all available models (registered + local).
    
    Returns:
        List of available models
    """
    registry = get_global_registry()
    
    # Get registered models
    registered_models = []
    for model_name in registry.list_models():
        info = registry.get_model_info(model_name)
        registered_models.append({
            'name': model_name,
            'type': 'registered',
            'description': info.get('description', ''),
            'category': info.get('category', 'general'),
            'tags': info.get('tags', [])
        })
    
    # Get local models
    local_models = _global_loader.list_local_models()
    for model in local_models:
        model['type'] = 'local'
    
    return registered_models + local_models 