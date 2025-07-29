"""
transFX - A Python package for mathematical transformations and utilities.

This package provides various mathematical transformation functions and utilities.
"""

__version__ = "0.0.4"
__author__ = "weisiren"
__email__ = "cxyvsir04@gmail.com"

# Import main classes and functions
from .math_package import (
    add,
    sum,
    sub,
    mul,
    div
)
from .welcome_package import hello

# Main class for the package
class TransFX:
    """Main TransFX class for mathematical transformations."""
    
    def __init__(self):
        """Initialize TransFX instance."""
        self.version = __version__
    
    def get_version(self):
        """Get the version of transFX."""
        return self.version

# Make main classes available at package level
__all__ = [
    'TransFX',
    '__version__',
    '__author__',
    '__email__',
    'add',
    'sum',
    'sub',
    'mul',
    'div',
    'hello'
]
