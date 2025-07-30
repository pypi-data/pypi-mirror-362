"""
Command-line interface for OC Image Segmentation.

This module serves as the main entry point and delegates to the modular CLI implementation.
"""

from .cli import main

# Export main for pyproject.toml entry point
__all__ = ["main"]

if __name__ == "__main__":
    main()
