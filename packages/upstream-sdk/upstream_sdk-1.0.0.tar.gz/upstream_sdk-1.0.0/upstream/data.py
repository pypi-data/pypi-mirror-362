"""
Data handling and upload functionality for Upstream SDK using OpenAPI client.

This module handles data validation and upload operations using the generated OpenAPI client.
"""

import csv
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from upstream_api_client.api import UploadfileCsvApi
from upstream_api_client.rest import ApiException

from .auth import AuthManager
from .exceptions import UploadError, ValidationError
from .utils import ConfigManager, chunk_file, get_logger, validate_file_size

logger = get_logger(__name__)


class DataValidator:
    """
    Validates data formats for Upstream API.
    """

    REQUIRED_SENSOR_FIELDS = ["alias", "variablename", "units"]
    REQUIRED_MEASUREMENT_FIELDS = ["collectiontime", "Lat_deg", "Lon_deg"]

    def __init__(self, config: ConfigManager) -> None:
        """
        Initialize data validator.

        Args:
            config: Configuration manager instance
        """
        self.config = config

    def validate_sensors_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate sensors data format.

        Args:
            data: List of sensor dictionaries

        Returns:
            Validation result dictionary

        Raises:
            ValidationError: If data format is invalid
        """
        errors = []

        for i, sensor in enumerate(data):
            # Check required fields
            for field in self.REQUIRED_SENSOR_FIELDS:
                if field not in sensor or not sensor[field]:
                    errors.append(f"Row {i+1}: Missing required field '{field}'")

            # Validate alias format
            if "alias" in sensor and not isinstance(sensor["alias"], str):
                errors.append(f"Row {i+1}: 'alias' must be a string")

            # Validate units
            if "units" in sensor and not isinstance(sensor["units"], str):
                errors.append(f"Row {i+1}: 'units' must be a string")

        if errors:
            raise ValidationError(f"Sensor data validation failed: {'; '.join(errors)}")

        return {
            "valid": True,
            "sensor_count": len(data),
            "message": f"Validated {len(data)} sensors",
        }

    def validate_measurements_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate measurements data format.

        Args:
            data: List of measurement dictionaries

        Returns:
            Validation result dictionary

        Raises:
            ValidationError: If data format is invalid
        """
        errors = []

        for i, measurement in enumerate(data):
            # Check required fields
            for field in self.REQUIRED_MEASUREMENT_FIELDS:
                if field not in measurement:
                    errors.append(f"Row {i+1}: Missing required field '{field}'")

            # Validate coordinates
            if "Lat_deg" in measurement:
                try:
                    lat = float(measurement["Lat_deg"])
                    if not (-90 <= lat <= 90):
                        errors.append(f"Row {i+1}: Latitude must be between -90 and 90")
                except (ValueError, TypeError):
                    errors.append(f"Row {i+1}: Invalid latitude value")

            if "Lon_deg" in measurement:
                try:
                    lon = float(measurement["Lon_deg"])
                    if not (-180 <= lon <= 180):
                        errors.append(
                            f"Row {i+1}: Longitude must be between -180 and 180"
                        )
                except (ValueError, TypeError):
                    errors.append(f"Row {i+1}: Invalid longitude value")

            # Validate timestamp format
            if "collectiontime" in measurement:
                timestamp = measurement["collectiontime"]
                if not isinstance(timestamp, str):
                    errors.append(f"Row {i+1}: 'collectiontime' must be a string")

        if errors:
            raise ValidationError(
                f"Measurement data validation failed: {'; '.join(errors)}"
            )

        return {
            "valid": True,
            "measurement_count": len(data),
            "message": f"Validated {len(data)} measurements",
        }

    def validate_csv_file(
        self, file_path: Union[str, Path], file_type: str = "measurements"
    ) -> Dict[str, Any]:
        """
        Validate CSV file format.

        Args:
            file_path: Path to CSV file
            file_type: Type of file ('sensors' or 'measurements')

        Returns:
            Validation result dictionary

        Raises:
            ValidationError: If file is invalid
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise ValidationError(f"File not found: {file_path}")

        if not validate_file_size(file_path, self.config.max_chunk_size_mb):
            raise ValidationError(
                f"File size exceeds maximum limit: {self.config.max_chunk_size_mb}MB"
            )

        try:
            # Read CSV file
            with open(file_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data = list(reader)

            # Validate based on file type
            if file_type == "sensors":
                return self.validate_sensors_data(data)
            elif file_type == "measurements":
                return self.validate_measurements_data(data)
            else:
                raise ValidationError(f"Unknown file type: {file_type}")

        except Exception as e:
            raise ValidationError(f"Failed to validate CSV file: {e}")


class DataUploader:
    """
    Handles data upload operations using the OpenAPI client.
    """

    def __init__(self, auth_manager: AuthManager) -> None:
        """
        Initialize data uploader.

        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager
        self.validator = DataValidator(auth_manager.config)

    def upload_csv_data(
        self,
        campaign_id: str,
        station_id: str,
        sensors_file: Union[str, Path],
        measurements_file: Union[str, Path],
        validate_data: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Upload sensor and measurement data from CSV files using OpenAPI client.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file
            validate_data: Whether to validate data before upload
            **kwargs: Additional upload parameters

        Returns:
            Upload result dictionary

        Raises:
            ValidationError: If data validation fails
            UploadError: If upload fails
        """
        sensors_file = Path(sensors_file)
        measurements_file = Path(measurements_file)

        # Validate files exist
        if not sensors_file.exists():
            raise ValidationError(
                f"Sensors file not found: {sensors_file}", field="sensors_file"
            )
        if not measurements_file.exists():
            raise ValidationError(
                f"Measurements file not found: {measurements_file}",
                field="measurements_file",
            )

        # Validate data format if requested
        if validate_data:
            logger.info("Validating sensor data format...")
            self.validator.validate_csv_file(sensors_file, "sensors")

            logger.info("Validating measurement data format...")
            self.validator.validate_csv_file(measurements_file, "measurements")

        # Upload files using OpenAPI client
        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)

            # Read files as bytes for upload
            with open(sensors_file, "rb") as sf, open(measurements_file, "rb") as mf:
                sensors_data = sf.read()
                measurements_data = mf.read()

            with self.auth_manager.get_api_client() as api_client:
                upload_api = UploadfileCsvApi(api_client)

                response = upload_api.post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    upload_file_sensors=sensors_data,
                    upload_file_measurements=measurements_data,
                )

                logger.info(
                    f"Successfully uploaded data for campaign {campaign_id}, station {station_id}"
                )

                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "station_id": station_id,
                    "sensors_file": str(sensors_file),
                    "measurements_file": str(measurements_file),
                    "response": response,
                    "message": "Data uploaded successfully",
                }

        except ValueError:
            raise ValidationError(
                f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}"
            )
        except ApiException as e:
            if e.status == 422:
                raise ValidationError(f"Data validation failed: {e}")
            else:
                raise UploadError(f"Failed to upload data: {e}")
        except Exception as e:
            logger.error(f"Data upload failed: {e}")
            raise UploadError(f"Failed to upload data: {e}")

    def upload_chunked_csv_data(
        self,
        campaign_id: str,
        station_id: str,
        sensors_file: Union[str, Path],
        measurements_file: Union[str, Path],
        validate_data: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Upload large CSV files in chunks.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file
            validate_data: Whether to validate data before upload
            **kwargs: Additional upload parameters

        Returns:
            Upload result dictionary

        Raises:
            ValidationError: If data validation fails
            UploadError: If upload fails
        """
        sensors_file = Path(sensors_file)
        measurements_file = Path(measurements_file)

        # Validate files exist
        if not sensors_file.exists():
            raise ValidationError(
                f"Sensors file not found: {sensors_file}", field="sensors_file"
            )
        if not measurements_file.exists():
            raise ValidationError(
                f"Measurements file not found: {measurements_file}",
                field="measurements_file",
            )

        # Check if files need chunking
        sensors_needs_chunking = not validate_file_size(
            sensors_file, self.auth_manager.config.max_chunk_size_mb
        )
        measurements_needs_chunking = not validate_file_size(
            measurements_file, self.auth_manager.config.max_chunk_size_mb
        )

        if not sensors_needs_chunking and not measurements_needs_chunking:
            # Files are small enough, use regular upload
            return self.upload_csv_data(
                campaign_id,
                station_id,
                sensors_file,
                measurements_file,
                validate_data,
                **kwargs,
            )

        # Handle chunking for large files
        upload_results = []

        try:
            # Chunk sensors file if needed
            if sensors_needs_chunking:
                logger.info(f"Chunking large sensors file: {sensors_file.name}")
                sensors_chunks = chunk_file(
                    sensors_file,
                    chunk_size=self.auth_manager.config.chunk_size,
                    max_chunk_size_mb=self.auth_manager.config.max_chunk_size_mb,
                )
            else:
                sensors_chunks = [str(sensors_file)]

            # Chunk measurements file if needed
            if measurements_needs_chunking:
                logger.info(
                    f"Chunking large measurements file: {measurements_file.name}"
                )
                measurements_chunks = chunk_file(
                    measurements_file,
                    chunk_size=self.auth_manager.config.chunk_size,
                    max_chunk_size_mb=self.auth_manager.config.max_chunk_size_mb,
                )
            else:
                measurements_chunks = [str(measurements_file)]

            # Upload each combination of chunks
            for i, sensors_chunk in enumerate(sensors_chunks):
                for j, measurements_chunk in enumerate(measurements_chunks):
                    try:
                        result = self.upload_csv_data(
                            campaign_id=campaign_id,
                            station_id=station_id,
                            sensors_file=sensors_chunk,
                            measurements_file=measurements_chunk,
                            validate_data=validate_data
                            and i == 0
                            and j == 0,  # Only validate first chunk
                            **kwargs,
                        )
                        upload_results.append(result)

                    except Exception as e:
                        logger.error(f"Failed to upload chunk {i+1}/{j+1}: {e}")
                        raise UploadError(f"Failed to upload chunk {i+1}/{j+1}: {e}")

            return {
                "success": True,
                "chunks_uploaded": len(upload_results),
                "chunk_results": upload_results,
                "message": f"Successfully uploaded {len(upload_results)} chunks",
            }

        finally:
            # Clean up temporary chunk files
            if sensors_needs_chunking:
                for chunk_file_path in sensors_chunks:
                    if chunk_file_path != str(
                        sensors_file
                    ):  # Don't delete original file
                        try:
                            Path(chunk_file_path).unlink()
                        except Exception as e:
                            logger.warning(
                                f"Failed to delete chunk file {chunk_file_path}: {e}"
                            )

            if measurements_needs_chunking:
                for chunk_file_path in measurements_chunks:
                    if chunk_file_path != str(
                        measurements_file
                    ):  # Don't delete original file
                        try:
                            Path(chunk_file_path).unlink()
                        except Exception as e:
                            logger.warning(
                                f"Failed to delete chunk file {chunk_file_path}: {e}"
                            )

    def prepare_files(
        self,
        campaign_id: int,
        station_id: int,
        sensors_file: Union[str, Path, bytes, Tuple[str, bytes]],
        measurements_file: Union[str, Path, bytes, Tuple[str, bytes]],
        chunk_size: int = 1000,
    ) -> Tuple[Union[bytes, Tuple[str, bytes]], List[Tuple[str, bytes]]]:
        """
        Prepare files for upload with validation and chunking.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: File path, bytes, or tuple (filename, bytes) containing sensor metadata
            measurements_file: File path, bytes, or tuple (filename, bytes) containing measurement data
            chunk_size: Number of measurement lines per chunk (default: 1000)

        Returns:
            Tuple of (prepared_sensors_file, measurements_chunks)

        Raises:
            ValidationError: If files are invalid or cannot be processed
        """
        # Validate files exist and are accessible
        if not sensors_file:
            raise ValidationError("Sensors file is required", field="sensors_file")
        if not measurements_file:
            raise ValidationError(
                "Measurements file is required", field="measurements_file"
            )

        # Prepare sensors file
        upload_file_sensors = self._prepare_file_input(sensors_file, "sensors")

        # Process measurements file in chunks
        measurements_chunks = self._split_measurements_file(
            measurements_file, chunk_size
        )

        return upload_file_sensors, measurements_chunks

    def _prepare_file_input(
        self, file_input: Union[str, Path, bytes, Tuple[str, bytes]], file_type: str
    ) -> Union[bytes, Tuple[str, bytes]]:
        """
        Prepare file input for upload API.

        Args:
            file_input: File path, bytes, or tuple (filename, bytes)
            file_type: Type of file for error messages

        Returns:
            Prepared file input in the format expected by the API

        Raises:
            ValidationError: If file cannot be read or is invalid
        """
        try:
            if isinstance(file_input, (str, Path)):
                # File path - read the file
                file_path = Path(file_input)
                if not file_path.exists():
                    raise ValidationError(
                        f"{file_type.capitalize()} file not found: {file_input}"
                    )

                with open(file_path, "rb") as f:
                    content = f.read()

                # Return as tuple (filename, bytes) for multipart upload
                return (file_path.name, content)

            elif isinstance(file_input, bytes):
                # Raw bytes - return as is
                return file_input

            elif isinstance(file_input, tuple) and len(file_input) == 2:
                # Tuple (filename, bytes) - validate and return
                filename, content = file_input
                if not isinstance(filename, str) or not isinstance(content, bytes):
                    raise ValidationError(
                        f"Invalid {file_type} file tuple format: expected (str, bytes)"
                    )
                return file_input

            else:
                raise ValidationError(
                    f"Invalid {file_type} file format: expected path, bytes, or (filename, bytes) tuple"
                )

        except (OSError, IOError) as e:
            raise ValidationError(f"Failed to read {file_type} file: {e}") from e

    def _split_measurements_file(
        self,
        measurements_file: Union[str, Path, bytes, Tuple[str, bytes]],
        chunk_size: int,
    ) -> List[Tuple[str, bytes]]:
        """
        Split measurements file into chunks for upload.

        Args:
            measurements_file: File path, bytes, or tuple (filename, bytes) containing measurement data
            chunk_size: Number of lines per chunk (excluding header)

        Returns:
            List of tuples (filename, bytes) for each chunk

        Raises:
            ValidationError: If file cannot be read or is invalid
        """
        try:
            # Get the file content
            if isinstance(measurements_file, (str, Path)):
                file_path = Path(measurements_file)
                if not file_path.exists():
                    raise ValidationError(
                        f"Measurements file not found: {measurements_file}"
                    )

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                original_filename = file_path.name

            elif isinstance(measurements_file, bytes):
                lines = measurements_file.decode("utf-8").splitlines(keepends=True)
                original_filename = "measurements.csv"

            elif isinstance(measurements_file, tuple) and len(measurements_file) == 2:
                filename, content = measurements_file
                if not isinstance(filename, str) or not isinstance(content, bytes):
                    raise ValidationError(
                        "Invalid measurements file tuple format: expected (str, bytes)"
                    )
                lines = content.decode("utf-8").splitlines(keepends=True)
                original_filename = filename

            else:
                raise ValidationError(
                    "Invalid measurements file format: expected path, bytes, or (filename, bytes) tuple"
                )

            if not lines:
                raise ValidationError("Measurements file is empty")

            # Ensure we have a header
            header = lines[0]
            data_lines = lines[1:]

            if not data_lines:
                return [("", b"")]

            # Split data lines into chunks
            chunks = []
            for i in range(0, len(data_lines), chunk_size):
                chunk_data_lines = data_lines[i : i + chunk_size]

                # Create chunk content with header + data lines
                chunk_content = header + "".join(chunk_data_lines)
                chunk_bytes = chunk_content.encode("utf-8")

                # Create filename for this chunk
                base_name = Path(original_filename).stem
                extension = Path(original_filename).suffix
                chunk_filename = f"{base_name}_chunk_{i//chunk_size + 1}{extension}"

                chunks.append((chunk_filename, chunk_bytes))

            logger.info(
                f"Split measurements file into {len(chunks)} chunks of {chunk_size} lines each"
            )
            return chunks

        except (OSError, IOError) as e:
            raise ValidationError(f"Failed to read measurements file: {e}") from e
        except UnicodeDecodeError as e:
            raise ValidationError(
                f"Failed to decode measurements file (must be UTF-8): {e}"
            ) from e

    def validate_files(
        self, sensors_file: Union[str, Path], measurements_file: Union[str, Path]
    ) -> Dict[str, Any]:
        """
        Validate CSV files without uploading.

        Args:
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file

        Returns:
            Validation result dictionary

        Raises:
            ValidationError: If validation fails
        """
        sensors_file = Path(sensors_file)
        measurements_file = Path(measurements_file)

        # Validate files exist
        if not sensors_file.exists():
            raise ValidationError(
                f"Sensors file not found: {sensors_file}", field="sensors_file"
            )
        if not measurements_file.exists():
            raise ValidationError(
                f"Measurements file not found: {measurements_file}",
                field="measurements_file",
            )

        # Validate data format
        logger.info("Validating sensor data format...")
        sensors_result = self.validator.validate_csv_file(sensors_file, "sensors")

        logger.info("Validating measurement data format...")
        measurements_result = self.validator.validate_csv_file(
            measurements_file, "measurements"
        )

        return {
            "valid": True,
            "sensors_validation": sensors_result,
            "measurements_validation": measurements_result,
            "message": "All files validated successfully",
        }

    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a CSV file.

        Args:
            file_path: Path to CSV file

        Returns:
            File information dictionary

        Raises:
            ValidationError: If file doesn't exist
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise ValidationError(f"File not found: {file_path}")

        # Get file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)

        # Count rows
        try:
            with open(file_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                row_count = sum(1 for _ in reader) - 1  # Subtract header row
        except Exception as e:
            logger.warning(f"Failed to count rows in {file_path}: {e}")
            row_count = None

        return {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_size_mb": round(file_size_mb, 2),
            "row_count": row_count,
            "needs_chunking": file_size_mb > self.auth_manager.config.max_chunk_size_mb,
            "max_chunk_size_mb": self.auth_manager.config.max_chunk_size_mb,
        }
