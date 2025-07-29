# This setup.py file is kept for backward compatibility only.
# For modern Python packaging, please use pyproject.toml instead.

from setuptools import setup, find_packages

# Minimal setup for backward compatibility
# All configuration is now in pyproject.toml
setup(
    packages=find_packages(where='src'),
    package_dir={'':'src'},
)