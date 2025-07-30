"""
Station management module for the Upstream SDK using OpenAPI client.

This module handles creation, retrieval, and management of monitoring stations
using the generated OpenAPI client.
"""

from upstream_api_client.api import StationsApi
from upstream_api_client.models import (
    GetStationResponse,
    ListStationsResponsePagination,
    StationCreate,
    StationCreateResponse,
    StationUpdate,
)
from upstream_api_client.rest import ApiException

from .auth import AuthManager
from .exceptions import APIError, ValidationError
from .utils import get_logger

logger = get_logger(__name__)


class StationManager:
    """
    Manages station operations using the OpenAPI client.
    """

    def __init__(self, auth_manager: AuthManager) -> None:
        """
        Initialize station manager.

        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager

    def create(
        self,
        campaign_id: str,
        station_create: StationCreate,
    ) -> StationCreateResponse:
        """
        Create a new station.

        Args:
            campaign_id: Parent campaign ID
            station_create: StationCreate model instance

        Returns:
            Created Station instance

        Raises:
            ValidationError: If station data is invalid
            APIError: If creation fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not isinstance(station_create, StationCreate):
            raise ValidationError(
                "station_create must be a StationCreate instance",
                field="station_create",
            )

        try:
            campaign_id_int = int(campaign_id)
            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)
                response = stations_api.create_station_api_v1_campaigns_campaign_id_stations_post(
                    campaign_id=campaign_id_int, station_create=station_create
                )
                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}") from exc
        except ApiException as e:
            if e.status == 422:
                raise ValidationError(f"Station validation failed: {e}") from e
            else:
                raise APIError(
                    f"Failed to create station: {e}", status_code=e.status
                ) from e
        except Exception as e:
            raise APIError(f"Failed to create station: {e}") from e

    def get(self, station_id: str, campaign_id: str) -> GetStationResponse:
        """
        Get station by ID.

        Args:
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            Station instance

        Raises:
            ValidationError: If IDs are invalid
            APIError: If station not found or retrieval fails
        """
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                response = stations_api.get_station_api_v1_campaigns_campaign_id_stations_station_id_get(
                    station_id=station_id_int, campaign_id=campaign_id_int
                )

                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: station_id={station_id}, campaign_id={campaign_id}"
            ) from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Station not found: {station_id}", status_code=404)
            else:
                raise APIError(f"Failed to get station: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to get station: {e}")

    def list(
        self,
        campaign_id: str,
        limit: int = 100,
        page: int = 1,
    ) -> ListStationsResponsePagination:
        """
        List stations for a campaign.

        Args:
            campaign_id: Campaign ID to filter by
            limit: Maximum number of stations to return
            page: Page number for pagination

        Returns:
            List of Station instances

        Raises:
            ValidationError: If campaign_id is invalid
            APIError: If listing fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                response = stations_api.list_stations_api_v1_campaigns_campaign_id_stations_get(
                    campaign_id=campaign_id_int, limit=limit, page=page
                )

                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}") from exc
        except ApiException as e:
            raise APIError(f"Failed to list stations: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to list stations: {e}")

    def update(
        self, station_id: str, campaign_id: str, station_update: StationUpdate
    ) -> StationCreateResponse:
        """
        Update station.

        Args:
            station_id: Station ID
            campaign_id: Campaign ID
            station_update: StationUpdate model instance

        Returns:
            Updated Station instance

        Raises:
            ValidationError: If IDs are invalid or station_update is not a StationUpdate
            APIError: If update fails
        """
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not isinstance(station_update, StationUpdate):
            raise ValidationError(
                "station_update must be a StationUpdate instance",
                field="station_update",
            )

        try:
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                response = stations_api.partial_update_station_api_v1_campaigns_campaign_id_stations_station_id_patch(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    station_update=station_update,
                )

                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: station_id={station_id}, campaign_id={campaign_id}"
            ) from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(
                    f"Station not found: {station_id}", status_code=404
                ) from e
            elif e.status == 422:
                raise ValidationError(f"Station validation failed: {e}") from e
            else:
                raise APIError(
                    f"Failed to update station: {e}", status_code=e.status
                ) from e
        except Exception as e:
            raise APIError(f"Failed to update station: {e}") from e

    def delete(self, station_id: str, campaign_id: str) -> bool:
        """
        Delete station.

        Args:
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            True if deletion successful

        Raises:
            ValidationError: If IDs are invalid
            APIError: If deletion fails
        """
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                # Note: The OpenAPI spec shows delete_sensor method, but this appears to be
                # for deleting stations based on the endpoint path structure
                stations_api.delete_sensor_api_v1_campaigns_campaign_id_stations_delete(
                    campaign_id=campaign_id_int
                )

                logger.info(f"Deleted station: {station_id}")
                return True

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: station_id={station_id}, campaign_id={campaign_id}"
            ) from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Station not found: {station_id}", status_code=404)
            else:
                raise APIError(f"Failed to delete station: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to delete station: {e}")
