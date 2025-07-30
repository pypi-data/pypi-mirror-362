"""
Authentication manager for Upstream SDK using OpenAPI client.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from upstream_api_client import ApiClient, Configuration
from upstream_api_client.api import AuthApi
from upstream_api_client.rest import ApiException

from .exceptions import AuthenticationError, ConfigurationError, NetworkError
from .utils import ConfigManager

logger = logging.getLogger(__name__)


class AuthManager:
    """
    Manages authentication with the Upstream API using OpenAPI client.
    """

    def __init__(self, config: ConfigManager) -> None:
        """
        Initialize authentication manager.

        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.configuration = Configuration(host=config.base_url)
        self.api_client: Optional[ApiClient] = None
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None

        # Validate configuration
        if not config.username or not config.password:
            raise ConfigurationError("Username and password are required")

    def authenticate(self) -> bool:
        """
        Authenticate with the Upstream API.

        Returns:
            True if authentication successful

        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            with ApiClient(self.configuration) as api_client:
                auth_api = AuthApi(api_client)
                # Attempt login
                if self.config.username is None or self.config.password is None:
                    raise AuthenticationError("Username and password are required")

                response = auth_api.login_api_v1_token_post(
                    username=self.config.username,
                    password=self.config.password,
                    grant_type="password",
                )

                # Store token information
                self.access_token = response.access_token
                self.configuration.access_token = response.access_token

                # Calculate expiration time (default to 1 hour if not provided)
                expires_in = getattr(response, "expires_in", 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)

                logger.info("Successfully authenticated with Upstream API")
                return True

        except ApiException as e:
            if e.status == 401:
                raise AuthenticationError("Invalid username or password")
            elif e.status == 422:
                raise AuthenticationError("Authentication request validation failed")
            else:
                raise AuthenticationError(f"Authentication failed: {e}")
        except Exception as e:
            raise NetworkError(f"Authentication request failed: {e}")

    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated with a valid token.

        Returns:
            True if authenticated with valid token
        """
        if not self.access_token or not self.token_expires_at:
            return False

        # Consider token expired if it expires within 5 minutes
        buffer_time = timedelta(minutes=5)
        return datetime.now() < (self.token_expires_at - buffer_time)

    def get_api_client(self) -> ApiClient:
        """
        Get authenticated API client.

        Returns:
            Configured API client with authentication

        Raises:
            AuthenticationError: If not authenticated
        """
        if not self.is_authenticated():
            if not self.authenticate():
                raise AuthenticationError("Failed to authenticate")

        return ApiClient(self.configuration)

    def get_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for direct requests.

        Returns:
            Dictionary of headers including authorization
        """
        if not self.is_authenticated():
            if not self.authenticate():
                raise AuthenticationError("Failed to authenticate")

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def refresh_token(self) -> bool:
        """
        Refresh authentication token.

        Returns:
            True if refresh successful
        """
        # For now, just re-authenticate
        # TODO: Implement proper token refresh if supported by API
        try:
            return self.authenticate()
        except Exception as e:
            logger.warning(f"Token refresh failed: {e}")
            return False

    def logout(self) -> None:
        """
        Logout and clear authentication tokens.
        """
        self.access_token = None
        self.token_expires_at = None
        self.configuration.access_token = None
        logger.info("Successfully logged out")
