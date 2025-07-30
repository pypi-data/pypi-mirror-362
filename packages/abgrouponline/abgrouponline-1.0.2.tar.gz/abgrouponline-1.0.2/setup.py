from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Base requirements that work across all Python versions
base_requirements = [
    # Core ML libraries
    "torch>=1.12.0",
    "torchvision>=0.13.0",
    "transformers>=4.20.0",
    "diffusers>=0.20.0",
    "scikit-learn>=1.1.0",
    
    # Data manipulation
    "pandas>=1.4.0",
    "numpy>=1.21.0",
    
    # Visualization
    "matplotlib>=3.5.0",
    "seaborn>=0.11.0",
    "plotly>=5.10.0",
    
    # Utilities
    "requests>=2.28.0",
    "tqdm>=4.64.0",
    "pyyaml>=6.0",
    "huggingface-hub>=0.15.0",
    
    # Gradient boosting
    "xgboost>=1.6.0",
    "lightgbm>=3.3.0",
    "catboost>=1.0.0",
    
    # Imbalanced learning
    "imbalanced-learn>=0.9.0",
    
    # Optional image processing
    "pillow>=9.0.0",
    "opencv-python>=4.5.0",
    
    # Statistical analysis
    "scipy>=1.8.0",
    "statsmodels>=0.13.0",
    
    # Hyperparameter optimization
    "optuna>=3.0.0",
    "hyperopt>=0.2.7",
    
    # Model interpretability
    "shap>=0.40.0",
    "lime>=0.2.0",
]

# Conditional requirements based on Python version
conditional_requirements = []

# TensorFlow is only available for Python < 3.13
python_version = sys.version_info
if python_version < (3, 13):
    conditional_requirements.extend([
        "tensorflow>=2.9.0",
        "keras>=2.9.0",
    ])

# Combine base and conditional requirements
install_requires = base_requirements + conditional_requirements

setup(
    name="abgrouponline",
    version="1.0.2",  # Increment version for the comprehensive fix
    author="ABGroup Research Team",
    author_email="research@abgrouponline.com",
    description="State-of-the-art machine learning models and frameworks for real-world applications - Compatible with all Python versions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abgrouponline/abgrouponline",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",  # Support all Python versions 3.8+
    install_requires=install_requires,
    extras_require={
        "tensorflow": [
            "tensorflow>=2.9.0; python_version<'3.13'",
            "keras>=2.9.0; python_version<'3.13'",
            "tensorflow-addons>=0.17.0; python_version<'3.13'",
        ],
        "full": [
            "tensorflow>=2.9.0; python_version<'3.13'",
            "keras>=2.9.0; python_version<'3.13'",
            "tensorflow-addons>=0.17.0; python_version<'3.13'",
            # Additional ML libraries
            "accelerate>=0.20.0",
            "datasets>=2.12.0",
            "evaluate>=0.4.0",
            "wandb>=0.15.0",
            "joblib>=1.1.0",
            "rich>=12.0.0",
            "albumentations>=1.2.0",
            "timm>=0.9.0",
            "einops>=0.6.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.19.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "abgroup-demo=abgrouponline.examples.diabetes_classifier:main",
            "abgroup-check=abgrouponline.utils.compatibility:check_compatibility",
        ],
    },
    keywords="machine learning, artificial intelligence, diabetes prediction, medical AI, healthcare, research, python compatibility",
    project_urls={
        "Bug Reports": "https://github.com/abgrouponline/abgrouponline/issues",
        "Source": "https://github.com/abgrouponline/abgrouponline",
        "Documentation": "https://abgrouponline.readthedocs.io/",
        "Changelog": "https://github.com/abgrouponline/abgrouponline/releases",
    },
) 