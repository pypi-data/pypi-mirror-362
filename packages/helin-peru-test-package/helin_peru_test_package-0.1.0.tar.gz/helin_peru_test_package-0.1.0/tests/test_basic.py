"""
Basic tests for pypi_test_package core functionality.
"""

import pytest
from pypi_test_package import hello_peru, get_version


def test_hello_peru():
    """Test that hello_peru function returns expected greeting message."""
    result = hello_peru()
    assert isinstance(result, str)
    assert "Hello from Peru" in result
    assert "working correctly" in result


def test_get_version():
    """Test that get_version function returns a valid version string."""
    version = get_version()
    assert isinstance(version, str)
    assert len(version) > 0
    # Check that it follows basic version format (contains dots and numbers)
    assert "." in version
    # Verify it matches the expected version format
    parts = version.split(".")
    assert len(parts) >= 2  # At least major.minor


def test_package_import():
    """Test that the package can be imported successfully."""
    import pypi_test_package
    assert hasattr(pypi_test_package, 'hello_peru')
    assert hasattr(pypi_test_package, 'get_version')
    assert hasattr(pypi_test_package, '__version__')


def test_functions_are_callable():
    """Test that the main functions are callable and return expected types."""
    # Test hello_peru is callable
    assert callable(hello_peru)
    result = hello_peru()
    assert isinstance(result, str)
    
    # Test get_version is callable
    assert callable(get_version)
    version = get_version()
    assert isinstance(version, str)


def test_version_consistency():
    """Test that get_version() returns the same version as __version__."""
    from pypi_test_package import __version__
    assert get_version() == __version__