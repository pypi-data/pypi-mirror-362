# Telemetry Harbor Python SDK

A robust, production-ready Python SDK for interacting with Telemetry Harbor ingestion endpoints.

## Features

-   Flexible, validation-powered data models using Pydantic.
-   Automatic retries with exponential backoff for network reliability.
-   Support for sending single readings or batches.

## Installation

```bash
pip install telemetry-harbor-sdk
```

```python
from harbor_sdk import HarborClient, GeneralReading, GpsReading

client = HarborClient(
    endpoint="[https://api.telemetry-harbor.com/v1/ingest](https://api.telemetry-harbor.com/v1/ingest)",
    api_key="your_secret_api_key"
)

# Send a single reading
gps_reading = GpsReading(ship_id="SS-Voyager", latitude=34.05, longitude=-118.24)
client.send(gps_reading)

# Send a batch of readings
batch = [
    GeneralReading(ship_id="MV-Explorer", cargo_id="C-1138", value=42.5),
    GpsReading(ship_id="MV-Explorer", latitude=40.71, longitude=-74.00)
]
client.send_batch(batch)
```
