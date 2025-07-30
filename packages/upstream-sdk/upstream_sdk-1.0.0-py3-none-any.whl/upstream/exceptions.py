"""
Exception classes for the Upstream SDK.

This module defines custom exception classes for different error conditions
that can occur when interacting with the Upstream API and CKAN platform.
"""

import logging
from typing import Any, Dict, Optional

from upstream_api_client import ApiException

logger = logging.getLogger(__name__)


class UpstreamError(Exception):
    """Base exception class for all Upstream SDK errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(UpstreamError):
    """Raised when authentication with the Upstream API fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)


class ValidationError(UpstreamError):
    """Raised when data validation fails."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)
        self.field = field


class UploadError(UpstreamError):
    """Raised when data upload operations fail."""

    def __init__(
        self,
        message: str,
        upload_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)
        self.upload_id = upload_id


class APIError(UpstreamError):
    """Raised when API requests fail."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)
        self.status_code = status_code
        self.response_data = response_data or {}


class NetworkError(UpstreamError):
    """Raised when network operations fail."""

    def __init__(
        self,
        message: str = "Network operation failed",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)


class ConfigurationError(UpstreamError):
    """Raised when SDK configuration is invalid."""

    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)
        self.config_key = config_key


class RateLimitError(UpstreamError):
    """Raised when API rate limits are exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)
        self.retry_after = retry_after


class OpenAPIError(UpstreamError):
    """Raised when OpenAPI client operations fail."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        reason: Optional[str] = None,
        response_headers: Optional[Dict[str, str]] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)
        self.status_code = status_code
        self.reason = reason
        self.response_headers = response_headers or {}


class CKANError(UpstreamError):
    """Raised when CKAN integration operations fail."""

    def __init__(
        self,
        message: str,
        ckan_error_code: Optional[str] = None,
        ckan_error_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details)
        self.ckan_error_code = ckan_error_code
        self.ckan_error_type = ckan_error_type


def handle_openapi_exception(api_exception: ApiException) -> UpstreamError:
    """Convert OpenAPI ApiException to appropriate SDK exception.

    Args:
        api_exception: The ApiException from upstream_api_client

    Returns:
        Appropriate SDK exception
    """
    try:
        status_code = api_exception.status
        reason = api_exception.reason
        headers = getattr(api_exception, "headers", {})

        # Parse response body if available
        response_data = {}
        if hasattr(api_exception, "body") and api_exception.body:
            try:
                import json

                response_data = json.loads(api_exception.body)
            except (json.JSONDecodeError, TypeError):
                response_data = {"raw_body": str(api_exception.body)}

        # Map status codes to specific exceptions
        if status_code == 401:
            return AuthenticationError(
                message="Authentication failed",
                details={
                    "status_code": status_code,
                    "reason": reason,
                    "response_data": response_data,
                },
            )
        elif status_code == 422:
            return ValidationError(
                message=f"Validation error: {reason}",
                details={
                    "status_code": status_code,
                    "reason": reason,
                    "response_data": response_data,
                },
            )
        elif status_code == 429:
            retry_after = None
            if "retry-after" in headers:
                try:
                    retry_after = int(headers["retry-after"])
                except (ValueError, TypeError):
                    pass

            return RateLimitError(
                message="Rate limit exceeded",
                retry_after=retry_after,
                details={
                    "status_code": status_code,
                    "reason": reason,
                    "response_data": response_data,
                },
            )
        elif status_code == 404:
            return APIError(
                message="Resource not found",
                status_code=status_code,
                response_data=response_data,
            )
        elif status_code >= 500:
            return APIError(
                message=f"Server error: {reason}",
                status_code=status_code,
                response_data=response_data,
            )
        else:
            return APIError(
                message=f"API error: {reason}",
                status_code=status_code,
                response_data=response_data,
            )

    except ImportError:
        logger.warning("upstream_api_client not available for exception handling")
        return APIError(f"API error: {api_exception}")
    except Exception as e:
        logger.error(f"Error handling OpenAPI exception: {e}")
        return APIError(f"API error: {api_exception}")


def format_validation_error(validation_error: ValidationError) -> str:
    """Format validation error for user-friendly display.

    Args:
        validation_error: ValidationError instance

    Returns:
        Formatted error message
    """
    message = validation_error.message

    if validation_error.field:
        message = f"Field '{validation_error.field}': {message}"

    if validation_error.details:
        details_str = ", ".join(
            f"{k}: {v}" for k, v in validation_error.details.items()
        )
        message = f"{message} (Details: {details_str})"

    return message


def format_api_error(api_error: APIError) -> str:
    """Format API error for user-friendly display.

    Args:
        api_error: APIError instance

    Returns:
        Formatted error message
    """
    message = api_error.message

    if api_error.status_code:
        message = f"HTTP {api_error.status_code}: {message}"

    if api_error.response_data:
        if isinstance(api_error.response_data, dict):
            if "detail" in api_error.response_data:
                message = f"{message} - {api_error.response_data['detail']}"
            elif "error" in api_error.response_data:
                message = f"{message} - {api_error.response_data['error']}"

    return message
