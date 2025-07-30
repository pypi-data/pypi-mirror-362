from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="abgrouponline",
    version="1.0.1",  # Increment version for the fix
    author="ABGroup Research Team",
    author_email="research@abgrouponline.com",
    description="State-of-the-art machine learning models and frameworks for real-world applications",
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
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8,<3.13",  # Restrict to Python versions with TensorFlow support
    install_requires=[
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
    ],
    extras_require={
        "tensorflow": ["tensorflow>=2.9.0"],  # Make TensorFlow optional
        "full": [
            "tensorflow>=2.9.0",
            "keras>=2.9.0",
            "tensorflow-addons>=0.17.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "abgroup-demo=abgrouponline.examples.diabetes_classifier:main",
        ],
    },
    keywords="machine learning, artificial intelligence, diabetes prediction, medical AI, healthcare, research",
    project_urls={
        "Bug Reports": "https://github.com/abgrouponline/abgrouponline/issues",
        "Source": "https://github.com/abgrouponline/abgrouponline",
        "Documentation": "https://abgrouponline.readthedocs.io/",
    },
) 