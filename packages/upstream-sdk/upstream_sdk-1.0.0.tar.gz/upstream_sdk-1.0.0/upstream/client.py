"""
Main client class for the Upstream SDK.

This module provides the primary interface for interacting with the Upstream API
and CKAN data platform using the OpenAPI client.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from upstream_api_client import MeasurementCreateResponse, MeasurementIn
from upstream_api_client.models import CampaignsIn, StationCreate
from upstream_api_client.models.aggregated_measurement import AggregatedMeasurement
from upstream_api_client.models.campaign_create_response import CampaignCreateResponse
from upstream_api_client.models.get_campaign_response import GetCampaignResponse
from upstream_api_client.models.get_station_response import GetStationResponse
from upstream_api_client.models.list_campaigns_response_pagination import (
    ListCampaignsResponsePagination,
)
from upstream_api_client.models.list_measurements_response_pagination import (
    ListMeasurementsResponsePagination,
)
from upstream_api_client.models.list_stations_response_pagination import (
    ListStationsResponsePagination,
)
from upstream_api_client.models.measurement_update import MeasurementUpdate
from upstream_api_client.models.station_create_response import StationCreateResponse

from .auth import AuthManager
from .campaigns import CampaignManager
from .data import DataUploader
from .exceptions import ConfigurationError
from .measurements import MeasurementManager
from .sensors import SensorManager
from .stations import StationManager
from .utils import ConfigManager, get_logger

logger = get_logger(__name__)


class UpstreamClient:
    """Main client class for interacting with the Upstream API."""

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        ckan_url: Optional[str] = None,
        config_file: Optional[Union[str, Path]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Upstream client.

        Args:
            username: Username for authentication
            password: Password for authentication
            base_url: Base URL for the Upstream API
            ckan_url: URL for CKAN integration
            config_file: Path to configuration file
            **kwargs: Additional configuration options

        Raises:
            ConfigurationError: If required configuration is missing
        """
        # Load configuration from file if provided
        if config_file:
            config = ConfigManager.from_file(config_file)
        else:
            config = ConfigManager(
                username=username,
                password=password,
                base_url=base_url,
                ckan_url=ckan_url,
                **kwargs,
            )

        # Initialize authentication manager
        self.auth_manager = AuthManager(config)

        # Initialize component managers
        self.campaigns = CampaignManager(self.auth_manager)
        self.stations = StationManager(self.auth_manager)
        self.sensors = SensorManager(self.auth_manager)
        self.measurements = MeasurementManager(self.auth_manager)
        self.data = DataUploader(self.auth_manager)

        logger.info("Upstream client initialized successfully")

    @classmethod
    def from_config(cls, config_file: Union[str, Path]) -> "UpstreamClient":
        """Create client from configuration file.

        Args:
            config_file: Path to configuration file (JSON or YAML)

        Returns:
            Configured UpstreamClient instance
        """
        return cls(config_file=config_file)

    @classmethod
    def from_environment(cls) -> "UpstreamClient":
        """Create client from environment variables.

        Environment variables:
        - UPSTREAM_USERNAME: Username for authentication
        - UPSTREAM_PASSWORD: Password for authentication
        - UPSTREAM_BASE_URL: Base URL for the Upstream API
        - CKAN_URL: URL for CKAN integration

        Returns:
            Configured UpstreamClient instance
        """
        return cls(
            username=os.environ.get("UPSTREAM_USERNAME"),
            password=os.environ.get("UPSTREAM_PASSWORD"),
            base_url=os.environ.get("UPSTREAM_BASE_URL"),
            ckan_url=os.environ.get("CKAN_URL"),
        )

    def authenticate(self) -> bool:
        """Test authentication with the API.

        Returns:
            True if authentication successful, False otherwise
        """
        return self.auth_manager.authenticate()

    def create_campaign(self, campaign_in: CampaignsIn) -> CampaignCreateResponse:
        """Create a new monitoring campaign.

        Args:
            campaign_in: CampaignsIn model instance

        Returns:
            Created Campaign object
        """
        return self.campaigns.create(campaign_in)

    def get_campaign(self, campaign_id: str) -> GetCampaignResponse:
        """Get campaign by ID.

        Args:
            campaign_id: Campaign ID

        Returns:
            Campaign object
        """
        return self.campaigns.get(campaign_id)

    def list_campaigns(self, **kwargs: Any) -> ListCampaignsResponsePagination:
        """List all campaigns.

        Args:
            **kwargs: Additional filtering parameters

        Returns:
            List of Campaign objects
        """
        return self.campaigns.list(**kwargs)

    def create_station(
        self, campaign_id: str, station_create: StationCreate
    ) -> StationCreateResponse:
        """Create a new monitoring station.

        Args:
            campaign_id: ID of the campaign
            station_create: StationCreate model instance

        Returns:
            Created Station object
        """
        return self.stations.create(campaign_id, station_create)

    def get_station(self, station_id: str, campaign_id: str) -> GetStationResponse:
        """Get station by ID.

        Args:
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            Station object
        """
        return self.stations.get(station_id, campaign_id)

    def list_stations(
        self, campaign_id: str, **kwargs: Any
    ) -> ListStationsResponsePagination:
        """List stations for a campaign.

        Args:
            campaign_id: Campaign ID to filter by
            **kwargs: Additional filtering parameters

        Returns:
            List of Station objects
        """
        return self.stations.list(campaign_id=campaign_id, **kwargs)

    def upload_csv_data(
        self,
        campaign_id: str,
        station_id: str,
        sensors_file: Union[str, Path],
        measurements_file: Union[str, Path],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Upload sensor data from CSV files.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file
            **kwargs: Additional upload parameters

        Returns:
            Upload result dictionary
        """
        return self.data.upload_csv_data(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_file,
            measurements_file=measurements_file,
            **kwargs,
        )

    def upload_sensor_measurement_files(
        self,
        campaign_id: str,
        station_id: str,
        sensors_file: Union[str, Path, bytes, Tuple[str, bytes]],
        measurements_file: Union[str, Path, bytes, Tuple[str, bytes]],
        chunk_size: int = 1000,
    ) -> Dict[str, object]:
        """Upload sensor and measurement CSV files to process and store data in the database.

        This method uses the direct API endpoint for processing sensor and measurement files.
        Measurements are uploaded in chunks to avoid HTTP timeouts with large files.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: File path, bytes, or tuple (filename, bytes) containing sensor metadata
            measurements_file: File path, bytes, or tuple (filename, bytes) containing measurement data
            chunk_size: Number of measurement lines per chunk (default: 1000)

        Returns:
            Response from the upload API containing processing results

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
        return self.sensors.upload_csv_files(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_file,
            measurements_file=measurements_file,
            chunk_size=chunk_size,
        )

    def create_measurement(
        self,
        campaign_id: str,
        station_id: str,
        sensor_id: str,
        measurement_in: MeasurementIn,
    ) -> MeasurementCreateResponse:
        """Create a new measurement.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            measurement_in: MeasurementIn model instance

        Returns:
            Created Measurement instance
        """
        return self.measurements.create(
            campaign_id, station_id, sensor_id, measurement_in
        )

    def list_measurements(
        self, campaign_id: str, station_id: str, sensor_id: str, **kwargs: Any
    ) -> ListMeasurementsResponsePagination:
        """List measurements for a sensor.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            **kwargs: Additional filtering parameters (start_date, end_date, min_measurement_value, etc.)

        Returns:
            List of Measurement instances
        """
        return self.measurements.list(campaign_id, station_id, sensor_id, **kwargs)

    def get_measurements_with_confidence_intervals(
        self, campaign_id: str, station_id: str, sensor_id: str, **kwargs: Any
    ) -> List[AggregatedMeasurement]:
        """Get sensor measurements with confidence intervals for visualization.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            **kwargs: Additional filtering parameters (interval, interval_value, start_date, etc.)

        Returns:
            List of AggregatedMeasurement instances with confidence intervals
        """
        return self.measurements.get_with_confidence_intervals(
            campaign_id, station_id, sensor_id, **kwargs
        )

    def update_measurement(
        self,
        campaign_id: str,
        station_id: str,
        sensor_id: str,
        measurement_id: str,
        measurement_update: MeasurementUpdate,
    ) -> MeasurementCreateResponse:
        """Update a measurement.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            measurement_id: Measurement ID
            measurement_update: MeasurementUpdate model instance

        Returns:
            Updated Measurement instance
        """
        return self.measurements.update(
            campaign_id, station_id, sensor_id, measurement_id, measurement_update
        )

    def delete_measurements(
        self, campaign_id: str, station_id: str, sensor_id: str
    ) -> bool:
        """Delete all measurements for a sensor.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID

        Returns:
            True if deletion successful
        """
        return self.measurements.delete(campaign_id, station_id, sensor_id)

    def upload_chunked_csv_data(
        self,
        campaign_id: str,
        station_id: str,
        sensors_file: Union[str, Path],
        measurements_file: Union[str, Path],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Upload large sensor data from CSV files in chunks.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file
            **kwargs: Additional upload parameters

        Returns:
            Upload result dictionary
        """
        return self.data.upload_chunked_csv_data(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_file,
            measurements_file=measurements_file,
            **kwargs,
        )

    def validate_files(
        self, sensors_file: Union[str, Path], measurements_file: Union[str, Path]
    ) -> Dict[str, Any]:
        """Validate CSV files without uploading.

        Args:
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file

        Returns:
            Validation result dictionary
        """
        return self.data.validate_files(sensors_file, measurements_file)

    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get information about a CSV file.

        Args:
            file_path: Path to CSV file

        Returns:
            File information dictionary
        """
        return self.data.get_file_info(file_path)

    # def publish_to_ckan(self, campaign_id: str, **kwargs: Any) -> Dict[str, Any]:
    #     """Publish campaign data to CKAN.

    #     Args:
    #         campaign_id: Campaign ID
    #         **kwargs: Additional CKAN parameters

    #     Returns:
    #         CKAN publication result

    #     Raises:
    #         ConfigurationError: If CKAN integration not configured
    #     """
    #     if not self.ckan:
    #         raise ConfigurationError("CKAN integration not configured")

    #     return self.ckan.publish_campaign(campaign_id=campaign_id, **kwargs)

    def logout(self) -> None:
        """Logout and invalidate authentication."""
        self.auth_manager.logout()
        logger.info("Client logged out successfully")

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration.

        Returns:
            Configuration dictionary
        """
        return self.auth_manager.config.to_dict()

    def is_authenticated(self) -> bool:
        """Check if currently authenticated.

        Returns:
            True if authenticated with valid token
        """
        return self.auth_manager.is_authenticated()

    def refresh_token(self) -> bool:
        """Refresh authentication token.

        Returns:
            True if refresh successful
        """
        return self.auth_manager.refresh_token()
