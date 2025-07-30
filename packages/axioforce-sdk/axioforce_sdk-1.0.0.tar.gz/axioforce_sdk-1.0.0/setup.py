#!/usr/bin/env python3
"""
Setup script for Axioforce Python SDK.

This package includes the Axioforce C API library and provides a clean Python interface.
"""

from setuptools import setup, find_packages
import os
import platform
import shutil

# Package information
PACKAGE_NAME = "axioforce-sdk"
VERSION = "1.0.0"
DESCRIPTION = "Python SDK for Axioforce sensor devices"
LONG_DESCRIPTION = """
Axioforce Python SDK

A clean, object-oriented Python wrapper around the Axioforce C API that provides
easy-to-use interfaces for device management and data collection.

Features:
- Simple API for device management and data collection
- Built-in simulator mode for testing
- Automatic resource management with context managers
- Type-safe dataclass structures
- Convenience functions for common use cases
- Full documentation and examples
"""

# Determine the correct library file based on platform
def get_library_files():
    """Get the appropriate library files for the current platform."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        if "64" in machine:
            return ["release/bin/axioforce_c_api.dll"]
        else:
            return ["release/bin/axioforce_c_api.dll"]
    elif system == "darwin":  # macOS
        return ["libaxioforce_c_api.dylib"]
    elif system == "linux":
        return ["release/bin/libaxioforce_c_api.so"]
    else:
        return []

# Get library files
library_files = get_library_files()

# Package data
package_data = {
    "axioforce_sdk": library_files + [
        "README_SDK.md",
        "SDK_MIGRATION_GUIDE.md",
    ]
}

# Data files (non-Python files)
data_files = []

# Copy library files to package directory if they exist
def copy_library_files():
    """Copy library files to the package directory."""
    package_dir = "axioforce_sdk"
    
    # Create package directory if it doesn't exist
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)
    
    # Copy library files
    for lib_file in library_files:
        if os.path.exists(lib_file):
            dest_file = os.path.join(package_dir, os.path.basename(lib_file))
            shutil.copy2(lib_file, dest_file)
            print(f"Copied {lib_file} to {dest_file}")
        else:
            print(f"Warning: Library file {lib_file} not found")

# Copy library files
copy_library_files()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Axioforce Team",
    author_email="support@axioforce.com",
    url="https://github.com/axioforce/axioforce-python-sdk",
    packages=find_packages(),
    package_data=package_data,
    data_files=data_files,
    include_package_data=True,
    install_requires=[
        "typing-extensions>=3.7.4",  # For better type hints support
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="sensor force measurement axioforce hardware interface",
    project_urls={
        "Bug Reports": "https://github.com/axioforce/axioforce-python-sdk/issues",
        "Source": "https://github.com/axioforce/axioforce-python-sdk",
        "Documentation": "https://github.com/axioforce/axioforce-python-sdk/blob/main/README_SDK.md",
    },
    entry_points={
        "console_scripts": [
            "axioforce-csv=axioforce_sdk.cli:csv_output",
            "axioforce-test=axioforce_sdk.cli:test_sdk",
        ],
    },
) 