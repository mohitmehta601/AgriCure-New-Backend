"""
System Compatibility Check
==========================

This script checks if your system has all required dependencies
and is ready to run the multi-output stacking system.

Run this before training the model to ensure everything is set up correctly.
"""

import sys
import importlib
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    print("\n" + "="*70)
    print("Python Version Check")
    print("="*70)
    
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python version must be 3.8 or higher")
        print("   Please upgrade Python: https://www.python.org/downloads/")
        return False


def check_package(package_name, import_name=None, optional=False):
    """
    Check if a package is installed.
    
    Args:
        package_name: Display name of the package
        import_name: Actual import name (if different from package_name)
        optional: Whether the package is optional
        
    Returns:
        Boolean indicating if package is available
    """
    if import_name is None:
        import_name = package_name.lower().replace('-', '_')
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        
        status = "✅" if not optional else "✅ (optional)"
        print(f"{status} {package_name:20} version: {version}")
        return True
    except ImportError:
        status = "⚠️" if optional else "❌"
        label = "(optional - system will work without it)" if optional else "(REQUIRED)"
        print(f"{status} {package_name:20} NOT FOUND {label}")
        return not optional


def check_dependencies():
    """Check all required and optional dependencies."""
    print("\n" + "="*70)
    print("Dependency Check")
    print("="*70)
    
    results = {}
    
    # Core dependencies
    print("\n📦 Core Dependencies:")
    results['pandas'] = check_package('pandas')
    results['numpy'] = check_package('numpy')
    results['scikit-learn'] = check_package('scikit-learn', 'sklearn')
    
    # Gradient boosting libraries
    print("\n🚀 Gradient Boosting Libraries:")
    results['xgboost'] = check_package('xgboost')
    results['catboost'] = check_package('catboost')
    results['lightgbm'] = check_package('lightgbm')
    
    # Optional AutoML
    print("\n🤖 AutoML (Optional):")
    results['autogluon'] = check_package('autogluon', optional=True)
    
    # Additional utilities
    print("\n📊 Visualization (Optional):")
    results['matplotlib'] = check_package('matplotlib', optional=True)
    results['seaborn'] = check_package('seaborn', optional=True)
    
    return results


def check_dataset():
    """Check if the dataset file exists."""
    print("\n" + "="*70)
    print("Dataset Check")
    print("="*70)
    
    dataset_path = Path(__file__).parent / "Dataset.csv"
    
    if dataset_path.exists():
        # Get file size
        size_mb = dataset_path.stat().st_size / (1024 * 1024)
        print(f"✅ Dataset found: {dataset_path}")
        print(f"   File size: {size_mb:.2f} MB")
        return True
    else:
        print(f"❌ Dataset NOT FOUND: {dataset_path}")
        print("   Please ensure 'Dataset.csv' is in the same directory as this script.")
        return False


def check_disk_space():
    """Check available disk space."""
    print("\n" + "="*70)
    print("Disk Space Check")
    print("="*70)
    
    try:
        import shutil
        total, used, free = shutil.disk_usage(Path(__file__).parent)
        
        free_gb = free / (1024**3)
        total_gb = total / (1024**3)
        used_percent = (used / total) * 100
        
        print(f"Total Space: {total_gb:.2f} GB")
        print(f"Used: {used_percent:.1f}%")
        print(f"Free: {free_gb:.2f} GB")
        
        if free_gb >= 2:
            print("✅ Sufficient disk space (2+ GB recommended)")
            return True
        else:
            print("⚠️ Low disk space (less than 2 GB free)")
            print("   Consider freeing up space. Training may require 1-2 GB.")
            return False
    except Exception as e:
        print(f"⚠️ Could not check disk space: {e}")
        return True


def provide_installation_guide(missing_packages):
    """Provide installation instructions for missing packages."""
    if not missing_packages:
        return
    
    print("\n" + "="*70)
    print("Installation Guide")
    print("="*70)
    
    print("\nTo install missing required packages, run:")
    print("\n" + "─"*70)
    
    # Separate required from optional
    required = [p for p in missing_packages if p not in ['autogluon', 'matplotlib', 'seaborn']]
    optional = [p for p in missing_packages if p in ['autogluon', 'matplotlib', 'seaborn']]
    
    if required:
        packages = ' '.join(required)
        print(f"pip install {packages}")
    
    if optional:
        print("\n# Optional (for enhanced features):")
        for package in optional:
            print(f"pip install {package}")
    
    print("─"*70)
    
    print("\nOr install all at once:")
    print("pip install -r requirements.txt")


def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("FERTILIZER RECOMMENDATION SYSTEM")
    print("System Compatibility Check")
    print("="*70)
    
    all_checks = []
    
    # Check Python version
    all_checks.append(check_python_version())
    
    # Check dependencies
    dep_results = check_dependencies()
    required_deps = ['pandas', 'numpy', 'scikit-learn', 'xgboost', 'catboost', 'lightgbm']
    missing_packages = [pkg for pkg in required_deps if not dep_results.get(pkg, False)]
    
    if not missing_packages:
        all_checks.append(True)
    else:
        all_checks.append(False)
    
    # Check dataset
    all_checks.append(check_dataset())
    
    # Check disk space
    all_checks.append(check_disk_space())
    
    # Final summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if all(all_checks) and not missing_packages:
        print("\n✅ ✅ ✅ ALL CHECKS PASSED! ✅ ✅ ✅")
        print("\nYour system is ready to train the model!")
        print("\nNext steps:")
        print("1. Run: python multioutput_stacking_fertilizer.py")
        print("2. Wait for training to complete (~10-30 minutes)")
        print("3. Check the results and saved model")
        
        if not dep_results.get('autogluon', False):
            print("\n💡 Tip: Install AutoGluon for better accuracy:")
            print("   pip install autogluon")
    else:
        print("\n⚠️ ISSUES DETECTED")
        print("\nPlease resolve the issues above before training the model.")
        
        if missing_packages:
            provide_installation_guide(missing_packages)
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
