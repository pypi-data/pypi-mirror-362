"""
SAS Python Utilities Package

This package provides reusable components for working with Azure Cosmos DB and related data access patterns.
"""

import os

source_root = os.path.dirname(os.path.abspath(__file__))
if source_root not in os.sys.path:
    os.sys.path.insert(0, source_root)
