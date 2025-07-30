# Upstream Python SDK

A Python SDK for seamless integration with the Upstream environmental sensor data platform and CKAN data portal.

## Overview

The Upstream Python SDK provides a standardized, production-ready toolkit for environmental researchers and organizations to:

- **Authenticate** with Upstream API and CKAN data portals
- **Manage** environmental monitoring campaigns and stations
- **Upload** sensor data efficiently (with automatic chunking for large datasets)
- **Publish** datasets automatically to CKAN for discoverability
- **Automate** data pipelines for continuous sensor networks

## Key Features

### 🔐 **Unified Authentication**

- Seamless integration with Upstream API and Tapis/CKAN
- Automatic token management and refresh
- Secure credential handling

### 📊 **Complete Data Workflow**

```python
from upstream import UpstreamClient

# Initialize client
client = UpstreamClient(username="researcher", password="password")

# Create campaign and station
from upstream_api_client.models import CampaignsIn, StationCreate
from datetime import datetime, timedelta

campaign_data = CampaignsIn(
    name="Hurricane Monitoring 2024",
    description="Hurricane monitoring campaign",
    contact_name="Dr. Jane Smith",
    contact_email="jane.smith@university.edu",
    allocation="TACC",
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=365)
)
campaign = client.create_campaign(campaign_data)

station_data = StationCreate(
    name="Galveston Pier",
    description="Hurricane monitoring station at Galveston Pier",
    contact_name="Dr. Jane Smith",
    contact_email="jane.smith@university.edu",
    start_date=datetime.now(),
    active=True
)
station = client.create_station(campaign.id, station_data)

# Upload sensor data
result = client.upload_csv_data(
    campaign_id=campaign.id,
    station_id=station.id,
    sensors_file="sensors.csv",
    measurements_file="measurements.csv"
)

# Automatically creates discoverable CKAN dataset
print(f"Data published at: {result.ckan_url}")
```

### 🚀 **Production-Ready Features**

- **Automatic chunking** for large datasets (>50MB)
- **Retry mechanisms** with exponential backoff
- **Comprehensive error handling** with detailed messages
- **Progress tracking** for long-running uploads
- **Extensive logging** for debugging and monitoring

### 🔄 **Automation-Friendly**

Perfect for automated sensor networks:

```python
# Scheduled data upload every 6 hours
def automated_upload():
    # Collect sensor readings and save to CSV files
    sensors_file, measurements_file = collect_sensor_readings()
    client.upload_csv_data(
        campaign_id=CAMPAIGN_ID,
        station_id=STATION_ID,
        sensors_file=sensors_file,
        measurements_file=measurements_file
    )
```

## Installation

```bash
pip install upstream-sdk
```

For development:

```bash
pip install upstream-sdk[dev]
```

## Quick Start

### 1. Basic Setup

```python
from upstream import UpstreamClient

# Initialize with credentials
client = UpstreamClient(
    username="your_username",
    password="your_password",
    base_url="https://upstream-dso.tacc.utexas.edu/dev"
)
```

### 2. Create Campaign

```python
from upstream_api_client.models import CampaignsIn
from datetime import datetime, timedelta

campaign_data = CampaignsIn(
    name="Air Quality Monitoring 2024",
    description="Urban air quality sensor network deployment",
    contact_name="Dr. Jane Smith",
    contact_email="jane.smith@university.edu",
    allocation="TACC",
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=365)
)
campaign = client.create_campaign(campaign_data)
```

### 3. Register Monitoring Station

```python
from upstream_api_client.models import StationCreate
from datetime import datetime

station_data = StationCreate(
    name="Downtown Monitor",
    description="City center air quality station",
    contact_name="Dr. Jane Smith",
    contact_email="jane.smith@university.edu",
    start_date=datetime.now(),
    active=True
)
station = client.create_station(campaign.id, station_data)
```

### 4. Upload Sensor Data

```python
# Upload from CSV files
result = client.upload_csv_data(
    campaign_id=campaign.id,
    station_id=station.id,
    sensors_file="path/to/sensors.csv",
    measurements_file="path/to/measurements.csv"
)

print(f"Uploaded {result.sensors_processed} sensors")
print(f"Added {result.measurements_added} measurements")
```

## Data Format Requirements

### Sensors CSV Format

```csv
alias,variablename,units,postprocess,postprocessscript
temp_01,Air Temperature,°C,,
humidity_01,Relative Humidity,%,,
pm25_01,PM2.5 Concentration,μg/m³,,
```

### Measurements CSV Format

```csv
collectiontime,Lat_deg,Lon_deg,temp_01,humidity_01,pm25_01
2024-01-15T10:30:00Z,30.2672,-97.7431,23.5,65.2,12.8
2024-01-15T10:31:00Z,30.2672,-97.7431,23.7,64.8,13.1
2024-01-15T10:32:00Z,30.2672,-97.7431,23.9,64.5,12.9
```

## Advanced Usage

### Automated Pipeline Example

```python
import schedule
from upstream import UpstreamClient

client = UpstreamClient.from_config("config.yaml")

def hourly_data_upload():
    try:
        # Collect data from sensors
        sensor_data = collect_from_weather_station()

        # Upload to Upstream
        result = client.upload_csv_data(
            campaign_id=CAMPAIGN_ID,
            station_id=STATION_ID,
            sensors_file=sensors_file,
            measurements_file=measurements_file
        )

        logger.info(f"Successfully uploaded {result.sensors_processed} sensors and {result.measurements_added} measurements")

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        # Implement your error handling/alerting

# Schedule uploads every hour
schedule.every().hour.do(hourly_data_upload)
```

### Large Dataset Handling

```python
# For large files, use chunked upload
result = client.upload_chunked_csv_data(
    campaign_id=campaign.id,
    station_id=station.id,
    sensors_file="sensors.csv",
    measurements_file="large_dataset.csv",  # 500MB file
    chunk_size=10000  # rows per chunk
)
```

### Advanced Upload Options

```python
# For more control over uploads, use the advanced method
result = client.upload_sensor_measurement_files(
    campaign_id=campaign.id,
    station_id=station.id,
    sensors_file="sensors.csv",  # Can be file path, bytes, or (filename, bytes) tuple
    measurements_file="measurements.csv",  # Can be file path, bytes, or (filename, bytes) tuple
    chunk_size=1000  # Process in chunks of 1000 rows
)
```

### Custom Data Processing

```python
# Pre-process data before upload
def custom_pipeline():
    # Your data collection logic
    raw_data = collect_sensor_data()

    # Apply quality control
    cleaned_data = apply_qc_filters(raw_data)

    # Transform to Upstream format
    upstream_data = transform_data(cleaned_data)

    # Upload processed data
    client.upload_csv_data(
        campaign_id=campaign.id,
        station_id=station.id,
        sensors_file="processed_sensors.csv",
        measurements_file="processed_measurements.csv"
    )
```

## Use Cases

### 🌪️ **Disaster Response Networks**

- Hurricane monitoring stations with automated data upload
- Emergency response sensor deployment
- Real-time environmental hazard tracking

### 🌬️ **Environmental Research**

- Long-term air quality monitoring
- Climate change research networks
- Urban environmental health studies

### 🌊 **Water Monitoring**

- Stream gauge networks
- Water quality assessment programs
- Flood monitoring and prediction

### 🏭 **Industrial Monitoring**

- Emissions monitoring compliance
- Environmental impact assessment
- Regulatory reporting automation

## API Reference

### UpstreamClient Methods

#### Campaign Management
- **`create_campaign(campaign_in: CampaignsIn)`** - Create a new monitoring campaign
- **`get_campaign(campaign_id: str)`** - Get campaign by ID
- **`list_campaigns(**kwargs)`** - List all campaigns

#### Station Management
- **`create_station(campaign_id: str, station_create: StationCreate)`** - Create a new monitoring station
- **`get_station(station_id: str, campaign_id: str)`** - Get station by ID
- **`list_stations(campaign_id: str, **kwargs)`** - List stations for a campaign

#### Data Upload
- **`upload_csv_data(campaign_id: str, station_id: str, sensors_file: str, measurements_file: str)`** - Upload CSV files
- **`upload_sensor_measurement_files(campaign_id: str, station_id: str, sensors_file: Union[str, bytes, Tuple], measurements_file: Union[str, bytes, Tuple], chunk_size: int = 1000)`** - Advanced upload with chunking
- **`upload_chunked_csv_data(campaign_id: str, station_id: str, sensors_file: str, measurements_file: str)`** - Chunked upload for large files

#### Utilities
- **`validate_files(sensors_file: str, measurements_file: str)`** - Validate CSV files
- **`get_file_info(file_path: str)`** - Get information about CSV files
- **`authenticate()`** - Test authentication
- **`logout()`** - Logout and invalidate tokens
- **`publish_to_ckan(campaign_id: str, **kwargs)`** - Publish data to CKAN

### Core Classes

- **`UpstreamClient`** - Main SDK interface
- **`CampaignsIn`** - Campaign creation model
- **`StationCreate`** - Station creation model

### Authentication

- **`AuthManager`** - Handle API authentication
- **`TokenManager`** - Manage token lifecycle

### Utilities

- **`DataValidator`** - Validate CSV formats
- **`ChunkManager`** - Handle large file uploads
- **`ErrorHandler`** - Comprehensive error handling

## Configuration

### Environment Variables

```bash
UPSTREAM_USERNAME=your_username
UPSTREAM_PASSWORD=your_password
UPSTREAM_BASE_URL=https://upstream-dso.tacc.utexas.edu/dev
CKAN_URL=https://ckan.tacc.utexas.edu
```

### Configuration File

```yaml
# config.yaml
upstream:
  username: your_username
  password: your_password
  base_url: https://upstream-dso.tacc.utexas.edu/dev

ckan:
  url: https://ckan.tacc.utexas.edu
  auto_publish: true
  default_organization: your-org

upload:
  chunk_size: 10000
  max_file_size_mb: 50
  retry_attempts: 3
  timeout_seconds: 300
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/In-For-Disaster-Analytics/upstream-python-sdk.git
cd upstream-python-sdk
pip install -e .[dev]
pre-commit install
```

### Running Tests

```bash
pytest                          # Run all tests
pytest tests/test_auth.py       # Run specific test file
pytest --cov=upstream           # Run with coverage
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [https://upstream-python-sdk.readthedocs.io](https://upstream-python-sdk.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/In-For-Disaster-Analytics/upstream-python-sdk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/In-For-Disaster-Analytics/upstream-python-sdk/discussions)

## Citation

If you use this SDK in your research, please cite:

```bibtex
@software{upstream_python_sdk,
  title={Upstream Python SDK: Environmental Sensor Data Integration},
  author={In-For-Disaster-Analytics Team},
  year={2024},
  url={https://github.com/In-For-Disaster-Analytics/upstream-python-sdk},
  version={1.0.0}
}
```

## Related Projects

- **[Upstream Platform](https://github.com/In-For-Disaster-Analytics/upstream-docker)** - Main platform repository
- **[Upstream Examples](https://github.com/In-For-Disaster-Analytics/upstream-examples)** - Example workflows and tutorials
- **[CKAN Integration](https://ckan.tacc.utexas.edu)** - Data portal for published datasets

---

**Built for the environmental research community** 🌍
**Enabling automated, reproducible, and discoverable environmental data workflows**
