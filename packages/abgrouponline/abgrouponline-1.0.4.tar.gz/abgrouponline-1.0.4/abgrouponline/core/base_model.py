"""
Base model class for all ABgrouponline models.

This module defines the abstract base class that all models in the package
should inherit from, providing a consistent interface and common functionality.
"""

import abc
import json
import pickle
import logging
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path
import joblib
import torch

logger = logging.getLogger(__name__)

class BaseModel(abc.ABC):
    """
    Abstract base class for all models in ABgrouponline.
    
    This class defines the standard interface that all models must implement,
    ensuring consistency across different model types and architectures.
    """
    
    def __init__(self, model_name: str = None, **kwargs):
        """
        Initialize the base model.
        
        Args:
            model_name: Name of the model
            **kwargs: Additional model-specific parameters
        """
        self.model_name = model_name or self.__class__.__name__
        self.model_type = self.__class__.__name__.lower()
        self.is_fitted = False
        self.model_params = kwargs
        self.training_history = {}
        self.metadata = {
            'version': '1.0.0',
            'created_at': pd.Timestamp.now().isoformat(),
            'model_type': self.model_type,
            'framework': self._get_framework()
        }
        self._model = None
        
        logger.info(f"Initialized {self.model_name} model")
    
    @abc.abstractmethod
    def fit(self, X: Union[np.ndarray, pd.DataFrame], 
            y: Union[np.ndarray, pd.Series] = None, **kwargs) -> 'BaseModel':
        """
        Train the model on the provided data.
        
        Args:
            X: Training features
            y: Training targets (for supervised learning)
            **kwargs: Additional training parameters
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abc.abstractmethod
    def predict(self, X: Union[np.ndarray, pd.DataFrame], **kwargs) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            X: Input features
            **kwargs: Additional prediction parameters
            
        Returns:
            Predictions
        """
        pass
    
    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame], **kwargs) -> np.ndarray:
        """
        Predict class probabilities (for classification models).
        
        Args:
            X: Input features
            **kwargs: Additional parameters
            
        Returns:
            Class probabilities
        """
        raise NotImplementedError("This model does not support probability predictions")
    
    def score(self, X: Union[np.ndarray, pd.DataFrame], 
              y: Union[np.ndarray, pd.Series], **kwargs) -> float:
        """
        Evaluate the model performance.
        
        Args:
            X: Test features
            y: True targets
            **kwargs: Additional parameters
            
        Returns:
            Model score
        """
        predictions = self.predict(X, **kwargs)
        return self._calculate_score(y, predictions)
    
    def _calculate_score(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate the default score metric.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Score value
        """
        from sklearn.metrics import accuracy_score, r2_score
        
        # For classification
        if len(np.unique(y_true)) <= 10 and np.issubdtype(y_true.dtype, np.integer):
            return accuracy_score(y_true, y_pred)
        # For regression
        else:
            return r2_score(y_true, y_pred)
    
    def save(self, filepath: Union[str, Path], save_format: str = 'joblib') -> None:
        """
        Save the model to disk.
        
        Args:
            filepath: Path to save the model
            save_format: Format to save in ('joblib', 'pickle', 'torch')
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        if save_format == 'joblib':
            joblib.dump(self, filepath)
        elif save_format == 'pickle':
            with open(filepath, 'wb') as f:
                pickle.dump(self, f)
        elif save_format == 'torch' and hasattr(self, '_model') and hasattr(self._model, 'state_dict'):
            torch.save({
                'model_state_dict': self._model.state_dict(),
                'metadata': self.metadata,
                'model_params': self.model_params
            }, filepath)
        else:
            raise ValueError(f"Unsupported save format: {save_format}")
        
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: Union[str, Path], load_format: str = 'joblib') -> 'BaseModel':
        """
        Load a model from disk.
        
        Args:
            filepath: Path to the saved model
            load_format: Format to load from ('joblib', 'pickle', 'torch')
            
        Returns:
            Loaded model instance
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        if load_format == 'joblib':
            model = joblib.load(filepath)
        elif load_format == 'pickle':
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
        elif load_format == 'torch':
            checkpoint = torch.load(filepath)
            # This would need to be implemented in subclasses
            raise NotImplementedError("PyTorch loading not implemented in base class")
        else:
            raise ValueError(f"Unsupported load format: {load_format}")
        
        logger.info(f"Model loaded from {filepath}")
        return model
    
    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """
        Get model parameters.
        
        Args:
            deep: Whether to return deep copy of parameters
            
        Returns:
            Dictionary of parameters
        """
        if deep:
            import copy
            return copy.deepcopy(self.model_params)
        return self.model_params
    
    def set_params(self, **params) -> 'BaseModel':
        """
        Set model parameters.
        
        Args:
            **params: Parameters to set
            
        Returns:
            Self for method chaining
        """
        self.model_params.update(params)
        return self
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get model metadata.
        
        Returns:
            Metadata dictionary
        """
        return self.metadata.copy()
    
    def update_metadata(self, **metadata) -> None:
        """
        Update model metadata.
        
        Args:
            **metadata: Metadata to update
        """
        self.metadata.update(metadata)
        self.metadata['updated_at'] = pd.Timestamp.now().isoformat()
    
    def _get_framework(self) -> str:
        """
        Detect the underlying ML framework being used.
        
        Returns:
            Framework name
        """
        class_module = self.__class__.__module__
        if 'torch' in class_module or 'pytorch' in class_module:
            return 'pytorch'
        elif 'tensorflow' in class_module or 'keras' in class_module:
            return 'tensorflow'
        elif 'sklearn' in class_module:
            return 'scikit-learn'
        elif 'xgboost' in class_module:
            return 'xgboost'
        elif 'lightgbm' in class_module:
            return 'lightgbm'
        else:
            return 'unknown'
    
    def summary(self) -> Dict[str, Any]:
        """
        Get a summary of the model.
        
        Returns:
            Model summary dictionary
        """
        return {
            'model_name': self.model_name,
            'model_type': self.model_type,
            'is_fitted': self.is_fitted,
            'framework': self.metadata.get('framework', 'unknown'),
            'parameters': len(self.model_params),
            'created_at': self.metadata.get('created_at'),
            'updated_at': self.metadata.get('updated_at')
        }
    
    def __repr__(self) -> str:
        """String representation of the model."""
        return f"{self.__class__.__name__}(name='{self.model_name}', fitted={self.is_fitted})"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        summary = self.summary()
        return f"""
{self.model_name} Model Summary:
- Type: {summary['model_type']}
- Framework: {summary['framework']}
- Fitted: {summary['is_fitted']}
- Parameters: {summary['parameters']}
- Created: {summary['created_at']}
"""

class SupervisedModel(BaseModel):
    """
    Base class for supervised learning models.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feature_names_ = None
        self.n_features_ = None
        self.classes_ = None
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], 
            y: Union[np.ndarray, pd.Series], **kwargs) -> 'SupervisedModel':
        """
        Fit supervised model.
        
        Args:
            X: Training features
            y: Training targets
            **kwargs: Additional parameters
            
        Returns:
            Self for method chaining
        """
        # Store feature information
        if hasattr(X, 'columns'):
            self.feature_names_ = list(X.columns)
        self.n_features_ = X.shape[1] if hasattr(X, 'shape') else len(X[0])
        
        # Store class information for classification
        if hasattr(y, 'dtype') and np.issubdtype(y.dtype, np.integer):
            self.classes_ = np.unique(y)
        
        return self

class UnsupervisedModel(BaseModel):
    """
    Base class for unsupervised learning models.
    """
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], 
            y: Union[np.ndarray, pd.Series] = None, **kwargs) -> 'UnsupervisedModel':
        """
        Fit unsupervised model.
        
        Args:
            X: Training data
            y: Ignored (for compatibility)
            **kwargs: Additional parameters
            
        Returns:
            Self for method chaining
        """
        return self
    
    def transform(self, X: Union[np.ndarray, pd.DataFrame], **kwargs) -> np.ndarray:
        """
        Transform data using the fitted model.
        
        Args:
            X: Input data
            **kwargs: Additional parameters
            
        Returns:
            Transformed data
        """
        raise NotImplementedError("Transform method not implemented")
    
    def fit_transform(self, X: Union[np.ndarray, pd.DataFrame], 
                      y: Union[np.ndarray, pd.Series] = None, **kwargs) -> np.ndarray:
        """
        Fit model and transform data in one step.
        
        Args:
            X: Training data
            y: Ignored (for compatibility)
            **kwargs: Additional parameters
            
        Returns:
            Transformed data
        """
        return self.fit(X, y, **kwargs).transform(X, **kwargs) 