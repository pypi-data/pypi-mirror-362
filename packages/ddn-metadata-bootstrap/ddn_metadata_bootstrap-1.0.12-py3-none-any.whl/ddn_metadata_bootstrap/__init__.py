# metadata_bootstrap/__init__.py
"""
Metadata Bootstrap - AI-powered schema metadata enhancement.

This package provides tools for automatically generating descriptions and
detecting relationships in YAML/HML schema files using AI.
"""

from .bootstrapper import MetadataBootstrapper
from .config import config

__version__ = "1.0.12"
__author__ = "Kenneth Stott"
__email__ = "ken@hasura.io"

# Make key classes available at package level
__all__ = [
    'MetadataBootstrapper',
    'config'
]

__description__="DDN Metadata Bootstrapper"
