"""
TestZeus SDK for Python.

This SDK provides a simple interface to interact with TestZeus testing platform.
"""

__version__ = "0.1.0"

from testzeus_sdk.client import TestZeusClient

# Provide a simple alias for the client
Client = TestZeusClient
