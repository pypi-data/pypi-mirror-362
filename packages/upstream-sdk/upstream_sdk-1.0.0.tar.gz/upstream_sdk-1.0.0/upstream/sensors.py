"""
Sensor management module for the Upstream SDK using OpenAPI client.

This module handles retrieval and management of sensors
using the generated OpenAPI client.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from upstream_api_client.api import SensorsApi, UploadfileCsvApi
from upstream_api_client.models import (
    GetSensorResponse,
    ListSensorsResponsePagination,
    SensorCreateResponse,
    SensorUpdate,
)
from upstream_api_client.rest import ApiException

from .auth import AuthManager
from .data import DataUploader
from .exceptions import APIError, ValidationError
from .utils import get_logger

logger = get_logger(__name__)


class SensorManager:
    """
    Manages sensor operations using the OpenAPI client.
    """

    def __init__(self, auth_manager: AuthManager) -> None:
        """
        Initialize sensor manager.

        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager
        self.data_uploader = DataUploader(auth_manager)

    def get(
        self, sensor_id: str, station_id: str, campaign_id: str
    ) -> GetSensorResponse:
        """
        Get sensor by ID.

        Args:
            sensor_id: Sensor ID
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            Sensor instance

        Raises:
            ValidationError: If IDs are invalid
            APIError: If sensor not found or retrieval fails
        """
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            sensor_id_int = int(sensor_id)
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.get_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_get(
                    sensor_id=sensor_id_int,
                    station_id=station_id_int,
                    campaign_id=campaign_id_int,
                )

                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: sensor_id={sensor_id}, station_id={station_id}, campaign_id={campaign_id}"
            ) from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404)
            else:
                raise APIError(f"Failed to get sensor: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to get sensor: {e}")

    def list(
        self,
        campaign_id: str,
        station_id: str,
        limit: int = 100,
        page: int = 1,
        **kwargs: Any,
    ) -> ListSensorsResponsePagination:
        """
        List sensors for a station.

        Args:
            campaign_id: Campaign ID to filter by
            station_id: Station ID to filter by
            limit: Maximum number of sensors to return
            page: Page number for pagination
            **kwargs: Additional filtering parameters (variable_name, units, alias, etc.)

        Returns:
            List of Sensor instances

        Raises:
            ValidationError: If campaign_id or station_id is invalid
            APIError: If listing fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")

        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.list_sensors_api_v1_campaigns_campaign_id_stations_station_id_sensors_get(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    limit=limit,
                    page=page,
                    **kwargs,
                )

                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}"
            ) from exc
        except ApiException as e:
            raise APIError(f"Failed to list sensors: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to list sensors: {e}")

    def update(
        self,
        sensor_id: str,
        station_id: str,
        campaign_id: str,
        sensor_update: SensorUpdate,
    ) -> SensorCreateResponse:
        """
        Update sensor.

        Args:
            sensor_id: Sensor ID
            station_id: Station ID
            campaign_id: Campaign ID
            sensor_update: SensorUpdate model instance

        Returns:
            Updated Sensor instance

        Raises:
            ValidationError: If IDs are invalid or sensor_update is not a SensorUpdate
            APIError: If update fails
        """
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not isinstance(sensor_update, SensorUpdate):
            raise ValidationError(
                "sensor_update must be a SensorUpdate instance", field="sensor_update"
            )

        try:
            sensor_id_int = int(sensor_id)
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_patch(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    sensor_id=sensor_id_int,
                    sensor_update=sensor_update,
                )

                return response

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: sensor_id={sensor_id}, station_id={station_id}, campaign_id={campaign_id}"
            ) from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404) from e
            elif e.status == 422:
                raise ValidationError(f"Sensor validation failed: {e}") from e
            else:
                raise APIError(
                    f"Failed to update sensor: {e}", status_code=e.status
                ) from e
        except Exception as e:
            raise APIError(f"Failed to update sensor: {e}") from e

    def delete(self, sensor_id: str, station_id: str, campaign_id: str) -> bool:
        """
        Delete sensor.

        Args:
            sensor_id: Sensor ID
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            True if deletion successful

        Raises:
            ValidationError: If IDs are invalid
            APIError: If deletion fails
        """
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            sensor_id_int = int(sensor_id)
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                sensors_api.delete_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_delete(
                    campaign_id=campaign_id_int, station_id=station_id_int
                )

                logger.info(f"Deleted sensor: {sensor_id}")
                return True

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: sensor_id={sensor_id}, station_id={station_id}, campaign_id={campaign_id}"
            ) from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404)
            else:
                raise APIError(f"Failed to delete sensor: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to delete sensor: {e}")

    def upload_csv_files(
        self,
        campaign_id: str,
        station_id: str,
        sensors_file: Union[str, Path, bytes, Tuple[str, bytes]],
        measurements_file: Union[str, Path, bytes, Tuple[str, bytes]],
        chunk_size: int = 1000,
    ) -> Dict[str, object]:
        """
        Upload sensor and measurement CSV files to process and store data in the database.
        Measurements are uploaded in chunks to avoid HTTP timeouts with large files.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: File path, bytes, or tuple (filename, bytes) containing sensor metadata
            measurements_file: File path, bytes, or tuple (filename, bytes) containing measurement data
            chunk_size: Number of measurement lines per chunk (default: 1000)

        Returns:
            Response from the upload API containing processing results

        Raises:
            ValidationError: If IDs are invalid or files are not provided
            APIError: If upload fails

        CSV Format Requirements:

        Sensors CSV (sensors_file):
        - Header: alias,variablename,units,postprocess,postprocessscript
        - alias: Unique identifier for the sensor (used as column header in measurements)
        - variablename: Human-readable description of what the sensor measures
        - units: Measurement units (e.g., °C, %, hPa, m/s)
        - postprocess: Boolean flag indicating if post-processing is required
        - postprocessscript: Name of the post-processing script (if applicable)

        Measurements CSV (measurements_file):
        - Header: collectiontime,Lat_deg,Lon_deg,{sensor_aliases...}
        - collectiontime: Timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
        - Lat_deg: Latitude in decimal degrees
        - Lon_deg: Longitude in decimal degrees
        - Sensor columns: Each sensor alias from sensors.csv becomes a column header
        - Column names must exactly match the sensor aliases
        - Empty values are automatically handled

        File Requirements:
        - Maximum file size: 500 MB per file
        - Encoding: UTF-8
        - Timestamps should be in UTC or include timezone information
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensors_file:
            raise ValidationError("Sensors file is required", field="sensors_file")
        if not measurements_file:
            raise ValidationError(
                "Measurements file is required", field="measurements_file"
            )

        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)

            # Use DataUploader for file preparation and validation
            upload_file_sensors, measurements_chunks = self.data_uploader.prepare_files(
                campaign_id=campaign_id_int,
                station_id=station_id_int,
                sensors_file=sensors_file,
                measurements_file=measurements_file,
                chunk_size=chunk_size,
            )

            all_responses = []

            with self.auth_manager.get_api_client() as api_client:
                upload_api = UploadfileCsvApi(api_client)

                for i, chunk in enumerate(measurements_chunks):
                    logger.info(
                        f"Uploading measurements chunk {i + 1}/{len(measurements_chunks)} ({len(chunk)} lines)"
                    )

                    response = upload_api.post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post(
                        campaign_id=campaign_id_int,
                        station_id=station_id_int,
                        upload_file_sensors=upload_file_sensors,  # Always upload sensors file
                        upload_file_measurements=chunk,
                    )

                    all_responses.append(response)

                logger.info(
                    f"Successfully uploaded {len(measurements_chunks)} measurement chunks for campaign {campaign_id}, station {station_id}"
                )
                return all_responses[-1] if all_responses else {}

        except ValueError as exc:
            raise ValidationError(
                f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}"
            ) from exc
        except ApiException as e:
            if e.status == 422:
                raise ValidationError(f"File validation failed: {e}") from e
            else:
                raise APIError(
                    f"Failed to upload CSV files: {e}", status_code=e.status
                ) from e
        except Exception as e:
            raise APIError(f"Failed to upload CSV files: {e}") from e
