"""
Compatibility utilities for ABgrouponline package.
Handles graceful imports and version compatibility across different Python versions.
"""

import sys
import warnings
from typing import Dict, List, Optional, Tuple, Any
from importlib import import_module


class CompatibilityManager:
    """Manages compatibility across different Python versions and optional dependencies."""
    
    def __init__(self):
        self.python_version = sys.version_info
        self.available_modules = {}
        self.unavailable_modules = {}
        self._check_all_dependencies()
    
    def _check_all_dependencies(self):
        """Check availability of all optional dependencies."""
        optional_deps = {
            'tensorflow': ['tensorflow', 'tf'],
            'keras': ['keras'],
            'torch': ['torch'],
            'sklearn': ['sklearn', 'scikit-learn'],
            'xgboost': ['xgboost'],
            'lightgbm': ['lightgbm'],
            'catboost': ['catboost'],
            'shap': ['shap'],
            'lime': ['lime'],
            'optuna': ['optuna'],
            'wandb': ['wandb'],
            'transformers': ['transformers'],
            'diffusers': ['diffusers'],
            'huggingface_hub': ['huggingface_hub']
        }
        
        for name, modules in optional_deps.items():
            try:
                # Try to import the first module in the list
                module = import_module(modules[0])
                self.available_modules[name] = {
                    'module': module,
                    'version': getattr(module, '__version__', 'unknown'),
                    'import_names': modules
                }
            except ImportError as e:
                self.unavailable_modules[name] = {
                    'error': str(e),
                    'import_names': modules,
                    'reason': self._get_unavailable_reason(name)
                }
    
    def _get_unavailable_reason(self, module_name: str) -> str:
        """Get the reason why a module is unavailable."""
        if module_name in ['tensorflow', 'keras'] and self.python_version >= (3, 13):
            return f"Not yet compatible with Python {self.python_version.major}.{self.python_version.minor}"
        return "Module not installed"
    
    def is_available(self, module_name: str) -> bool:
        """Check if a module is available."""
        return module_name in self.available_modules
    
    def get_module(self, module_name: str) -> Optional[Any]:
        """Get an imported module if available."""
        if self.is_available(module_name):
            return self.available_modules[module_name]['module']
        return None
    
    def require_module(self, module_name: str, feature_name: str = None):
        """Require a module and raise informative error if not available."""
        if not self.is_available(module_name):
            feature_msg = f" for {feature_name}" if feature_name else ""
            reason = self.unavailable_modules.get(module_name, {}).get('reason', 'Unknown')
            
            if module_name == 'tensorflow' and self.python_version >= (3, 13):
                raise ImportError(
                    f"TensorFlow is required{feature_msg} but is not yet compatible with "
                    f"Python {self.python_version.major}.{self.python_version.minor}. "
                    f"Please use Python 3.8-3.12 or install with: pip install abgrouponline[tensorflow]"
                )
            else:
                raise ImportError(
                    f"{module_name} is required{feature_msg}. "
                    f"Install it with: pip install {module_name}"
                )
    
    def get_compatibility_report(self) -> Dict[str, Any]:
        """Generate a comprehensive compatibility report."""
        return {
            'python_version': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}",
            'python_version_info': self.python_version,
            'available_modules': {
                name: {
                    'version': info['version'],
                    'status': '✅ Available'
                }
                for name, info in self.available_modules.items()
            },
            'unavailable_modules': {
                name: {
                    'reason': info['reason'],
                    'status': '❌ Unavailable'
                }
                for name, info in self.unavailable_modules.items()
            },
            'tensorflow_support': self.python_version < (3, 13),
            'recommended_action': self._get_recommended_action()
        }
    
    def _get_recommended_action(self) -> str:
        """Get recommended action based on current setup."""
        if self.python_version >= (3, 13) and 'tensorflow' in self.unavailable_modules:
            return "Consider using Python 3.8-3.12 for full TensorFlow support, or continue with current setup for PyTorch/scikit-learn models"
        elif len(self.unavailable_modules) > 0:
            missing = list(self.unavailable_modules.keys())
            return f"Install missing packages: pip install {' '.join(missing)}"
        else:
            return "All dependencies available - you're ready to go!"


# Global compatibility manager instance
_compat_manager = None

def get_compatibility_manager() -> CompatibilityManager:
    """Get the global compatibility manager instance."""
    global _compat_manager
    if _compat_manager is None:
        _compat_manager = CompatibilityManager()
    return _compat_manager


def safe_import(module_name: str, feature_name: str = None, optional: bool = True):
    """Safely import a module with graceful fallback."""
    manager = get_compatibility_manager()
    
    if manager.is_available(module_name):
        return manager.get_module(module_name)
    elif not optional:
        manager.require_module(module_name, feature_name)
    else:
        # Return None for optional imports
        return None


def check_tensorflow_support() -> Tuple[bool, str]:
    """Check if TensorFlow is supported in current environment."""
    manager = get_compatibility_manager()
    
    if manager.is_available('tensorflow'):
        version = manager.available_modules['tensorflow']['version']
        return True, f"TensorFlow {version} is available"
    elif manager.python_version >= (3, 13):
        return False, f"TensorFlow not yet supported on Python {manager.python_version.major}.{manager.python_version.minor}"
    else:
        return False, "TensorFlow not installed"


def warn_if_tensorflow_unavailable(feature_name: str):
    """Issue a warning if TensorFlow is unavailable for a feature."""
    supported, message = check_tensorflow_support()
    if not supported:
        warnings.warn(
            f"TensorFlow features for {feature_name} are unavailable: {message}. "
            f"Some functionality may be limited.",
            UserWarning,
            stacklevel=2
        )


def check_compatibility():
    """Command-line tool to check package compatibility."""
    manager = get_compatibility_manager()
    report = manager.get_compatibility_report()
    
    print("🔍 ABgrouponline Compatibility Report")
    print("=" * 50)
    print(f"Python Version: {report['python_version']}")
    print(f"TensorFlow Support: {'✅ Yes' if report['tensorflow_support'] else '❌ No'}")
    print()
    
    print("📦 Available Modules:")
    for name, info in report['available_modules'].items():
        print(f"  {info['status']} {name} ({info['version']})")
    
    if report['unavailable_modules']:
        print("\n❌ Unavailable Modules:")
        for name, info in report['unavailable_modules'].items():
            print(f"  {info['status']} {name} - {info['reason']}")
    
    print(f"\n💡 Recommendation: {report['recommended_action']}")
    
    return report


if __name__ == "__main__":
    check_compatibility() 