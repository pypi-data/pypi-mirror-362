"""
Campaign management module for the Upstream SDK using OpenAPI client.

This module handles creation, retrieval, and management of environmental
monitoring campaigns using the generated OpenAPI client.
"""

from typing import Optional

from upstream_api_client.api import CampaignsApi
from upstream_api_client.models import (
    CampaignCreateResponse,
    CampaignsIn,
    CampaignUpdate,
)
from upstream_api_client.models.get_campaign_response import GetCampaignResponse
from upstream_api_client.models.list_campaigns_response_pagination import (
    ListCampaignsResponsePagination,
)
from upstream_api_client.rest import ApiException

from .auth import AuthManager
from .exceptions import APIError, ValidationError
from .utils import get_logger

logger = get_logger(__name__)


class CampaignManager:
    """Manages campaign operations using the OpenAPI client."""

    auth_manager: AuthManager

    def __init__(self, auth_manager: AuthManager) -> None:
        """Initialize campaign manager.

        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager

    def create(self, campaign_in: CampaignsIn) -> CampaignCreateResponse:
        """
        Create a new campaign.

        Args:
            campaign_in: CampaignsIn model instance

        Returns:
            Created Campaign object

        Raises:
            ValidationError: If campaign_in is not a CampaignsIn
            APIError: If API request fails
        """
        if not isinstance(campaign_in, CampaignsIn):
            raise ValidationError(
                "campaign_in must be a CampaignsIn instance", field="campaign_in"
            )

        try:
            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)
                response: CampaignCreateResponse = (
                    campaigns_api.create_campaign_api_v1_campaigns_post(
                        campaigns_in=campaign_in
                    )
                )
                return response
        except ApiException as e:
            if e.status == 422:
                raise ValidationError(f"Campaign validation failed: {e}")
            else:
                raise APIError(f"Failed to create campaign: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to create campaign: {e}")

    def get(self, campaign_id: str) -> GetCampaignResponse:
        """Get campaign by ID.

        Args:
            campaign_id: Campaign ID

        Returns:
            Campaign object

        Raises:
            APIError: If API request fails or campaign not found
        """
        try:
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)

                response: GetCampaignResponse = (
                    campaigns_api.get_campaign_api_v1_campaigns_campaign_id_get(
                        campaign_id=campaign_id_int
                    )
                )
                return response

        except ValueError:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}")
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Campaign not found: {campaign_id}", status_code=404)
            else:
                raise APIError(f"Failed to get campaign: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to get campaign: {e}")

    def list(
        self, limit: int = 50, page: int = 1, search: Optional[str] = None
    ) -> ListCampaignsResponsePagination:
        """List campaigns with optional filtering.

        Args:
            limit: Maximum number of campaigns to return
            page: Page number for pagination
            search: Search term for campaign names/descriptions

        Returns:
            List of Campaign objects

        Raises:
            APIError: If API request fails
        """
        try:
            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)
                response: ListCampaignsResponsePagination = (
                    campaigns_api.list_campaigns_api_v1_campaigns_get(
                        limit=limit,
                        page=page,
                    )
                )
                logger.info(f"Retrieved {response.total} campaigns")
                return response

        except ApiException as e:
            raise APIError(f"Failed to list campaigns: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to list campaigns: {e}")

    def update(
        self, campaign_id: str, campaign_update: CampaignUpdate
    ) -> CampaignCreateResponse:
        """
        Update an existing campaign.

        Args:
            campaign_id: Campaign ID
            campaign_update: CampaignUpdate model instance

        Returns:
            Updated Campaign object

        Raises:
            ValidationError: If campaign_update is not a CampaignUpdate
            APIError: If API request fails
        """
        if not isinstance(campaign_update, CampaignUpdate):
            raise ValidationError(
                "campaign_update must be a CampaignUpdate instance",
                field="campaign_update",
            )
        try:
            campaign_id_int = int(campaign_id)
            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)
                response: CampaignCreateResponse = (
                    campaigns_api.partial_update_campaign_api_v1_campaigns_campaign_id_patch(
                        campaign_id=campaign_id_int, campaign_update=campaign_update
                    )
                )
                return response
        except ValueError:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}")
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Campaign not found: {campaign_id}", status_code=404)
            elif e.status == 422:
                raise ValidationError(f"Campaign validation failed: {e}")
            else:
                raise APIError(f"Failed to update campaign: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to update campaign: {e}")

    def delete(self, campaign_id: str) -> bool:
        """Delete a campaign.

        Args:
            campaign_id: Campaign ID

        Returns:
            True if successful

        Raises:
            APIError: If API request fails
        """
        try:
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)

                campaigns_api.delete_sensor_api_v1_campaigns_campaign_id_delete(
                    campaign_id=campaign_id_int
                )

                logger.info(f"Deleted campaign: {campaign_id}")
                return True

        except ValueError:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}")
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Campaign not found: {campaign_id}", status_code=404)
            else:
                raise APIError(f"Failed to delete campaign: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to delete campaign: {e}")
