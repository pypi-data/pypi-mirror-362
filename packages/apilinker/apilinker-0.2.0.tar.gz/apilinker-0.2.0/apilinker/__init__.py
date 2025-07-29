"""
ApiLinker: A universal bridge to connect, map, and automate data transfer between any two REST APIs.

This package provides tools for connecting to REST APIs, mapping data fields between them,
scheduling automatic data transfers, and extending functionality through plugins.
"""

__version__ = "0.2.0"

from apilinker.core.connector import ApiConnector
from apilinker.core.mapper import FieldMapper
from apilinker.core.scheduler import Scheduler

# Main class
from .api_linker import ApiLinker

__all__ = ["ApiLinker", "ApiConnector", "FieldMapper", "Scheduler"]
