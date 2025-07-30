"""
Measurement management module for the Upstream SDK using OpenAPI client.

This module handles creation, retrieval, and management of sensor measurements
using the generated OpenAPI client.
"""

from datetime import datetime
from typing import Any, List, Optional

from upstream_api_client.api import MeasurementsApi
from upstream_api_client.models import (
    AggregatedMeasurement,
    ListMeasurementsResponsePagination,
    MeasurementCreateResponse,
    MeasurementIn,
    MeasurementUpdate,
)
from upstream_api_client.rest import ApiException

from .auth import AuthManager
from .exceptions import APIError, ValidationError
from .utils import get_logger

logger = get_logger(__name__)


class MeasurementManager:
    """
    Manages measurement operations using the OpenAPI client.
    """

    def __init__(self, auth_manager: AuthManager) -> None:
        """
        Initialize measurement manager.

        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager

    def create(
        self,
        campaign_id: str,
        station_id: str,
        sensor_id: str,
        measurement_in: MeasurementIn,
    ) -> MeasurementCreateResponse:
        """
        Create a new measurement.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            measurement_in: MeasurementIn model instance

        Returns:
            Created Measurement instance

        Raises:
            ValidationError: If measurement data is invalid
            APIError: If creation fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not isinstance(measurement_in, MeasurementIn):
            raise ValidationError(
                "measurement_in must be a MeasurementIn instance",
                field="measurement_in",
            )

        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)
            sensor_id_int = int(sensor_id)

            with self.auth_manager.get_api_client() as api_client:
                measurements_api = MeasurementsApi(api_client)
                response = measurements_api.create_measurement_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_post(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    sensor_id=sensor_id_int,
                    measurement_in=measurement_in,
                )
                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}, sensor_id={sensor_id}"
            ) from exc
        except ApiException as e:
            if e.status == 422:
                raise ValidationError(f"Measurement validation failed: {e}") from e
            else:
                raise APIError(
                    f"Failed to create measurement: {e}", status_code=e.status
                ) from e
        except Exception as e:
            raise APIError(f"Failed to create measurement: {e}") from e

    def list(
        self,
        campaign_id: str,
        station_id: str,
        sensor_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_measurement_value: Optional[float] = None,
        max_measurement_value: Optional[float] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        downsample_threshold: Optional[int] = None,
    ) -> ListMeasurementsResponsePagination:
        """
        List measurements for a sensor.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            start_date: Start date for filtering measurements
            end_date: End date for filtering measurements
            min_measurement_value: Minimum measurement value to include
            max_measurement_value: Maximum measurement value to include
            limit: Maximum number of measurements to return
            page: Page number for pagination
            downsample_threshold: Threshold for downsampling

        Returns:
            List of Measurement instances

        Raises:
            ValidationError: If IDs are invalid
            APIError: If listing fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")

        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)
            sensor_id_int = int(sensor_id)

            with self.auth_manager.get_api_client() as api_client:
                measurements_api = MeasurementsApi(api_client)

                response = measurements_api.get_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_get(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    sensor_id=sensor_id_int,
                    start_date=start_date,
                    end_date=end_date,
                    min_measurement_value=min_measurement_value,
                    max_measurement_value=max_measurement_value,
                    limit=limit,
                    page=page,
                    downsample_threshold=downsample_threshold,
                )

                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}, sensor_id={sensor_id}"
            ) from exc
        except ApiException as e:
            raise APIError(f"Failed to list measurements: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to list measurements: {e}")

    def get_with_confidence_intervals(
        self,
        campaign_id: str,
        station_id: str,
        sensor_id: str,
        interval: Optional[str] = None,
        interval_value: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> List[AggregatedMeasurement]:
        """
        Get sensor measurements with confidence intervals for visualization.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            interval: Time interval for aggregation (minute, hour, day)
            interval_value: Multiple of interval (e.g., 15 for 15-minute intervals)
            start_date: Start date for filtering measurements
            end_date: End date for filtering measurements
            min_value: Minimum measurement value to include
            max_value: Maximum measurement value to include

        Returns:
            List of AggregatedMeasurement instances with confidence intervals

        Raises:
            ValidationError: If IDs are invalid
            APIError: If retrieval fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")

        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)
            sensor_id_int = int(sensor_id)

            with self.auth_manager.get_api_client() as api_client:
                measurements_api = MeasurementsApi(api_client)

                response = measurements_api.get_measurements_with_confidence_intervals_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_confidence_intervals_get(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    sensor_id=sensor_id_int,
                    interval=interval,
                    interval_value=interval_value,
                    start_date=start_date,
                    end_date=end_date,
                    min_value=min_value,
                    max_value=max_value,
                )

                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}, sensor_id={sensor_id}"
            ) from exc
        except ApiException as e:
            raise APIError(
                f"Failed to get measurements with confidence intervals: {e}",
                status_code=e.status,
            )
        except Exception as e:
            raise APIError(f"Failed to get measurements with confidence intervals: {e}")

    def update(
        self,
        campaign_id: str,
        station_id: str,
        sensor_id: str,
        measurement_id: str,
        measurement_update: MeasurementUpdate,
    ) -> MeasurementCreateResponse:
        """
        Update a measurement.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            measurement_id: Measurement ID
            measurement_update: MeasurementUpdate model instance

        Returns:
            Updated Measurement instance

        Raises:
            ValidationError: If IDs are invalid or measurement_update is not a MeasurementUpdate
            APIError: If update fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not measurement_id:
            raise ValidationError("Measurement ID is required", field="measurement_id")
        if not isinstance(measurement_update, MeasurementUpdate):
            raise ValidationError(
                "measurement_update must be a MeasurementUpdate instance",
                field="measurement_update",
            )

        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)
            sensor_id_int = int(sensor_id)
            measurement_id_int = int(measurement_id)

            with self.auth_manager.get_api_client() as api_client:
                measurements_api = MeasurementsApi(api_client)

                response = measurements_api.partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_patch(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    sensor_id=sensor_id_int,
                    measurement_id=measurement_id_int,
                    measurement_update=measurement_update,
                )

                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}, sensor_id={sensor_id}, measurement_id={measurement_id}"
            ) from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(
                    f"Measurement not found: {measurement_id}", status_code=404
                ) from e
            elif e.status == 422:
                raise ValidationError(f"Measurement validation failed: {e}") from e
            else:
                raise APIError(
                    f"Failed to update measurement: {e}", status_code=e.status
                ) from e
        except Exception as e:
            raise APIError(f"Failed to update measurement: {e}") from e

    def delete(
        self,
        campaign_id: str,
        station_id: str,
        sensor_id: str,
    ) -> bool:
        """
        Delete all measurements for a sensor.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID

        Returns:
            True if deletion successful

        Raises:
            ValidationError: If IDs are invalid
            APIError: If deletion fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")

        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)
            sensor_id_int = int(sensor_id)

            with self.auth_manager.get_api_client() as api_client:
                measurements_api = MeasurementsApi(api_client)

                measurements_api.delete_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_delete(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    sensor_id=sensor_id_int,
                )

                logger.info(f"Deleted measurements for sensor: {sensor_id}")
                return True

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}, sensor_id={sensor_id}"
            ) from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(
                    f"Measurements not found for sensor: {sensor_id}", status_code=404
                )
            else:
                raise APIError(
                    f"Failed to delete measurements: {e}", status_code=e.status
                )
        except Exception as e:
            raise APIError(f"Failed to delete measurements: {e}")
