"""
Upstream Python SDK for environmental sensor data platform and CKAN integration.

This package provides a standardized toolkit for environmental researchers and organizations
to interact with the Upstream API and CKAN data portals.
"""

from .auth import AuthManager
from .campaigns import CampaignManager
from .client import UpstreamClient
from .data import DataUploader, DataValidator
from .exceptions import (
    APIError,
    AuthenticationError,
    UploadError,
    UpstreamError,
    ValidationError,
)
from .stations import StationManager

__version__ = "1.0.0"
__author__ = "In-For-Disaster-Analytics Team"
__email__ = "info@tacc.utexas.edu"
__license__ = "MIT"

__all__ = [
    # Core client
    "UpstreamClient",
    # Authentication
    "AuthManager",
    # Campaign management
    "CampaignManager",
    # Station management
    "StationManager",
    # Data handling
    "DataUploader",
    "DataValidator",
    # CKAN integration
    "CKANIntegration",
    # Exceptions
    "UpstreamError",
    "AuthenticationError",
    "ValidationError",
    "UploadError",
    "APIError",
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
