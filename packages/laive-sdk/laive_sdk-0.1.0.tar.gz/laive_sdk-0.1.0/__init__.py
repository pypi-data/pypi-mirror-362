"""
Laive Python SDK

A Python client library for the Laive RAG API.
Provides easy access to document upload, vault management, and intelligent querying capabilities.

Example:
    >>> import os
    >>> from laive import LaiveClient
    >>> client = LaiveClient(api_key=os.getenv("LAIVE_API_KEY"))
    >>> results = client.query("What is RAG?", vault_id=123)
    >>> results.prettyprint()
"""

from laive import LaiveClient, QueryResponse, BatchUploadResponse

__version__ = "0.1.0"
__author__ = "Laive"
__email__ = "contact@laive.ai"

__all__ = ["LaiveClient", "QueryResponse", "BatchUploadResponse"] 