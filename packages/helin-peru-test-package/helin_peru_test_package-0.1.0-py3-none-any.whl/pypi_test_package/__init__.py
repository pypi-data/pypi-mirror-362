"""
A simple test package for PyPI publishing and Amazon Peru testing.
"""

__version__ = "0.1.0"


def hello_peru() -> str:
    """Return a simple greeting message to verify package functionality."""
    return "Hello from Peru! This package is working correctly."


def get_version() -> str:
    """Return the package version number."""
    return __version__