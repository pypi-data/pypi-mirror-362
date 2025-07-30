"""
Advanced Diabetes Classifier with Imbalanced Data Handling.

This module implements a state-of-the-art diabetes prediction system based on
recent research on robust predictive frameworks for diabetes classification
using optimized machine learning on imbalanced datasets.

Reference: "Robust predictive framework for diabetes classification using 
optimized machine learning on imbalanced datasets" (2024)
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union, Tuple
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN
from imblearn.ensemble import BalancedBaggingClassifier

from ..core.base_model import SupervisedModel

logger = logging.getLogger(__name__)

class DiabetesClassifier(SupervisedModel):
    """
    Advanced diabetes classifier with comprehensive imbalanced data handling.
    
    This classifier implements state-of-the-art techniques for diabetes prediction
    including multiple machine learning algorithms, advanced resampling methods,
    hyperparameter optimization, and comprehensive evaluation metrics.
    
    Features:
    - Multiple ML algorithms (Random Forest, XGBoost, LightGBM, etc.)
    - Advanced imbalance handling (SMOTE, ADASYN, Borderline-SMOTE, etc.)
    - Automated hyperparameter tuning
    - Comprehensive evaluation metrics
    - Feature engineering and selection
    - Cross-validation support
    """
    
    SUPPORTED_ALGORITHMS = {
        'random_forest': RandomForestClassifier,
        'xgboost': XGBClassifier,
        'lightgbm': LGBMClassifier,
        'catboost': CatBoostClassifier,
        'gradient_boosting': GradientBoostingClassifier,
        'logistic_regression': LogisticRegression,
        'svm': SVC,
        'knn': KNeighborsClassifier,
        'decision_tree': DecisionTreeClassifier,
        'naive_bayes': GaussianNB,
        'neural_network': MLPClassifier,
        'balanced_bagging': BalancedBaggingClassifier
    }
    
    IMBALANCE_METHODS = {
        'smote': SMOTE,
        'adasyn': ADASYN,
        'borderline_smote': BorderlineSMOTE,
        'random_undersampler': RandomUnderSampler,
        'smoteenn': SMOTEENN,
        'none': None
    }
    
    def __init__(self,
                 algorithm: str = 'random_forest',
                 imbalance_method: str = 'smote',
                 hyperparameter_tuning: bool = True,
                 cv_folds: int = 5,
                 correlation_threshold: float = 0.9,
                 polynomial_degree: int = 2,
                 random_state: int = 42,
                 **kwargs):
        """
        Initialize the DiabetesClassifier.
        
        Args:
            algorithm: ML algorithm to use
            imbalance_method: Method for handling class imbalance
            hyperparameter_tuning: Whether to perform hyperparameter tuning
            cv_folds: Number of cross-validation folds
            correlation_threshold: Threshold for removing correlated features
            polynomial_degree: Degree for polynomial feature expansion
            random_state: Random state for reproducibility
            **kwargs: Additional parameters for the chosen algorithm
        """
        super().__init__(model_name=f"DiabetesClassifier_{algorithm}", **kwargs)
        
        if algorithm not in self.SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algorithm}. "
                           f"Supported algorithms: {list(self.SUPPORTED_ALGORITHMS.keys())}")
        
        if imbalance_method not in self.IMBALANCE_METHODS:
            raise ValueError(f"Unsupported imbalance method: {imbalance_method}. "
                           f"Supported methods: {list(self.IMBALANCE_METHODS.keys())}")
        
        self.algorithm = algorithm
        self.imbalance_method = imbalance_method
        self.hyperparameter_tuning = hyperparameter_tuning
        self.cv_folds = cv_folds
        self.correlation_threshold = correlation_threshold
        self.polynomial_degree = polynomial_degree
        self.random_state = random_state
        
        # Initialize components
        self.scaler = StandardScaler()
        self.poly_features = PolynomialFeatures(degree=polynomial_degree, include_bias=False)
        self.resampler = None
        self.classifier = None
        self.best_params_ = None
        self.evaluation_results_ = {}
        self.selected_features_ = None
        
        logger.info(f"Initialized DiabetesClassifier with {algorithm} and {imbalance_method}")
    
    def _setup_resampler(self):
        """Setup the imbalance handling method."""
        if self.imbalance_method == 'none':
            self.resampler = None
        else:
            resampler_class = self.IMBALANCE_METHODS[self.imbalance_method]
            
            # Configure resampler parameters based on type
            if self.imbalance_method in ['smote', 'adasyn', 'borderline_smote']:
                self.resampler = resampler_class(random_state=self.random_state)
            elif self.imbalance_method == 'random_undersampler':
                self.resampler = resampler_class(random_state=self.random_state)
            elif self.imbalance_method == 'smoteenn':
                self.resampler = resampler_class(random_state=self.random_state)
    
    def _setup_classifier(self):
        """Setup the machine learning classifier."""
        classifier_class = self.SUPPORTED_ALGORITHMS[self.algorithm]
        
        # Default parameters for each algorithm
        default_params = {
            'random_forest': {'random_state': self.random_state, 'n_jobs': -1},
            'xgboost': {'random_state': self.random_state, 'eval_metric': 'logloss'},
            'lightgbm': {'random_state': self.random_state, 'verbose': -1},
            'catboost': {'random_state': self.random_state, 'verbose': False},
            'gradient_boosting': {'random_state': self.random_state},
            'logistic_regression': {'random_state': self.random_state, 'max_iter': 1000},
            'svm': {'random_state': self.random_state, 'probability': True},
            'knn': {},
            'decision_tree': {'random_state': self.random_state},
            'naive_bayes': {},
            'neural_network': {'random_state': self.random_state, 'max_iter': 500},
            'balanced_bagging': {'random_state': self.random_state, 'n_jobs': -1}
        }
        
        params = default_params.get(self.algorithm, {})
        params.update(self.model_params)
        
        self.classifier = classifier_class(**params)
    
    def _feature_engineering(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Apply feature engineering including polynomial expansion and correlation filtering.
        
        Args:
            X: Input features
            
        Returns:
            Engineered features
        """
        # Apply polynomial feature expansion
        X_poly = self.poly_features.fit_transform(X)
        
        # Create feature names for polynomial features
        if hasattr(X, 'columns'):
            feature_names = self.poly_features.get_feature_names_out(X.columns)
        else:
            feature_names = self.poly_features.get_feature_names_out()
        
        X_poly_df = pd.DataFrame(X_poly, columns=feature_names, index=X.index)
        
        # Remove highly correlated features
        if self.selected_features_ is None:
            correlation_matrix = X_poly_df.corr().abs()
            upper_triangle = correlation_matrix.where(
                np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
            )
            
            # Find features with correlation greater than threshold
            high_corr_features = [
                column for column in upper_triangle.columns 
                if any(upper_triangle[column] > self.correlation_threshold)
            ]
            
            # Keep features that are not highly correlated
            self.selected_features_ = [
                col for col in X_poly_df.columns 
                if col not in high_corr_features
            ]
            
            logger.info(f"Selected {len(self.selected_features_)} features "
                       f"out of {len(X_poly_df.columns)} after correlation filtering")
        
        return X_poly_df[self.selected_features_]
    
    def _get_hyperparameter_grid(self) -> Dict[str, List]:
        """
        Get hyperparameter grid for the chosen algorithm.
        
        Returns:
            Hyperparameter grid
        """
        grids = {
            'random_forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'xgboost': {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0]
            },
            'lightgbm': {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'num_leaves': [31, 50, 100]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.2]
            },
            'logistic_regression': {
                'C': [0.1, 1.0, 10.0],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear', 'saga']
            },
            'svm': {
                'C': [0.1, 1, 10],
                'kernel': ['rbf', 'linear'],
                'gamma': ['scale', 'auto']
            },
            'knn': {
                'n_neighbors': [3, 5, 7, 9],
                'weights': ['uniform', 'distance'],
                'metric': ['euclidean', 'manhattan']
            }
        }
        
        return grids.get(self.algorithm, {})
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], 
            y: Union[np.ndarray, pd.Series], **kwargs) -> 'DiabetesClassifier':
        """
        Train the diabetes classifier.
        
        Args:
            X: Training features
            y: Training targets
            **kwargs: Additional training parameters
            
        Returns:
            Self for method chaining
        """
        logger.info("Starting diabetes classifier training")
        
        # Convert to DataFrame if needed
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        if not isinstance(y, pd.Series):
            y = pd.Series(y)
        
        # Store original class distribution
        class_counts = y.value_counts()
        logger.info(f"Original class distribution: {class_counts.to_dict()}")
        
        # Feature engineering
        X_engineered = self._feature_engineering(X)
        
        # Scale features
        X_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_engineered),
            columns=X_engineered.columns,
            index=X_engineered.index
        )
        
        # Handle class imbalance
        self._setup_resampler()
        if self.resampler is not None:
            X_resampled, y_resampled = self.resampler.fit_resample(X_scaled, y)
            resampled_counts = pd.Series(y_resampled).value_counts()
            logger.info(f"Resampled class distribution: {resampled_counts.to_dict()}")
        else:
            X_resampled, y_resampled = X_scaled, y
        
        # Setup and train classifier
        self._setup_classifier()
        
        if self.hyperparameter_tuning:
            param_grid = self._get_hyperparameter_grid()
            if param_grid:
                logger.info("Performing hyperparameter tuning")
                grid_search = GridSearchCV(
                    self.classifier,
                    param_grid,
                    cv=self.cv_folds,
                    scoring='f1',
                    n_jobs=-1,
                    verbose=1
                )
                grid_search.fit(X_resampled, y_resampled)
                self.classifier = grid_search.best_estimator_
                self.best_params_ = grid_search.best_params_
                logger.info(f"Best parameters: {self.best_params_}")
        
        # Final training
        self.classifier.fit(X_resampled, y_resampled)
        
        # Update base class attributes
        super().fit(X, y, **kwargs)
        self.is_fitted = True
        
        logger.info("Diabetes classifier training completed")
        return self
    
    def predict(self, X: Union[np.ndarray, pd.DataFrame], **kwargs) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            X: Input features
            **kwargs: Additional prediction parameters
            
        Returns:
            Predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        # Convert to DataFrame if needed
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        # Apply same preprocessing pipeline
        X_engineered = pd.DataFrame(
            self.poly_features.transform(X),
            columns=self.poly_features.get_feature_names_out(X.columns),
            index=X.index
        )[self.selected_features_]
        
        X_scaled = pd.DataFrame(
            self.scaler.transform(X_engineered),
            columns=X_engineered.columns,
            index=X_engineered.index
        )
        
        return self.classifier.predict(X_scaled)
    
    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame], **kwargs) -> np.ndarray:
        """
        Predict class probabilities.
        
        Args:
            X: Input features
            **kwargs: Additional parameters
            
        Returns:
            Class probabilities
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        # Convert to DataFrame if needed
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        # Apply same preprocessing pipeline
        X_engineered = pd.DataFrame(
            self.poly_features.transform(X),
            columns=self.poly_features.get_feature_names_out(X.columns),
            index=X.index
        )[self.selected_features_]
        
        X_scaled = pd.DataFrame(
            self.scaler.transform(X_engineered),
            columns=X_engineered.columns,
            index=X_engineered.index
        )
        
        return self.classifier.predict_proba(X_scaled)
    
    def evaluate(self, X: Union[np.ndarray, pd.DataFrame], 
                 y: Union[np.ndarray, pd.Series]) -> Dict[str, float]:
        """
        Comprehensive evaluation of the model.
        
        Args:
            X: Test features
            y: True targets
            
        Returns:
            Dictionary of evaluation metrics
        """
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)[:, 1]  # Probability of positive class
        
        results = {
            'accuracy': accuracy_score(y, predictions),
            'precision': precision_score(y, predictions),
            'recall': recall_score(y, predictions),
            'f1_score': f1_score(y, predictions),
            'roc_auc': roc_auc_score(y, probabilities),
            'specificity': self._calculate_specificity(y, predictions)
        }
        
        # Store confusion matrix
        cm = confusion_matrix(y, predictions)
        results['confusion_matrix'] = cm.tolist()
        
        # Store detailed classification report
        results['classification_report'] = classification_report(y, predictions, output_dict=True)
        
        self.evaluation_results_ = results
        
        logger.info("Model evaluation completed")
        logger.info(f"Accuracy: {results['accuracy']:.4f}")
        logger.info(f"F1-Score: {results['f1_score']:.4f}")
        logger.info(f"ROC-AUC: {results['roc_auc']:.4f}")
        
        return results
    
    def _calculate_specificity(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate specificity (true negative rate).
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            
        Returns:
            Specificity score
        """
        cm = confusion_matrix(y_true, y_pred)
        tn = cm[0, 0]
        fp = cm[0, 1]
        return tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    def cross_validate(self, X: Union[np.ndarray, pd.DataFrame], 
                      y: Union[np.ndarray, pd.Series],
                      cv: int = None) -> Dict[str, np.ndarray]:
        """
        Perform cross-validation evaluation.
        
        Args:
            X: Features
            y: Targets
            cv: Number of CV folds (uses self.cv_folds if None)
            
        Returns:
            Dictionary of CV scores
        """
        if cv is None:
            cv = self.cv_folds
        
        # Convert to DataFrame if needed
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        # Apply preprocessing
        X_engineered = self._feature_engineering(X)
        X_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_engineered),
            columns=X_engineered.columns,
            index=X_engineered.index
        )
        
        # Setup classifier
        self._setup_classifier()
        
        # Perform cross-validation for multiple metrics
        scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        cv_results = {}
        
        for metric in scoring:
            scores = cross_val_score(
                self.classifier, X_scaled, y, 
                cv=cv, scoring=metric, n_jobs=-1
            )
            cv_results[metric] = scores
            logger.info(f"CV {metric}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
        
        return cv_results
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from the trained model.
        
        Returns:
            DataFrame with feature names and importance scores
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")
        
        if hasattr(self.classifier, 'feature_importances_'):
            importance_scores = self.classifier.feature_importances_
        elif hasattr(self.classifier, 'coef_'):
            importance_scores = np.abs(self.classifier.coef_[0])
        else:
            raise ValueError("Classifier does not support feature importance")
        
        feature_importance_df = pd.DataFrame({
            'feature': self.selected_features_,
            'importance': importance_scores
        }).sort_values('importance', ascending=False)
        
        return feature_importance_df
    
    def summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of the model.
        
        Returns:
            Model summary dictionary
        """
        summary = super().summary()
        summary.update({
            'algorithm': self.algorithm,
            'imbalance_method': self.imbalance_method,
            'hyperparameter_tuning': self.hyperparameter_tuning,
            'cv_folds': self.cv_folds,
            'best_parameters': self.best_params_,
            'selected_features_count': len(self.selected_features_) if self.selected_features_ else 0,
            'evaluation_results': self.evaluation_results_
        })
        return summary 