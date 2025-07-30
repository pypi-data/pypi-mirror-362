# Telemetry Harbor Python SDK

A robust, production-ready Python SDK for interacting with Telemetry Harbor ingestion endpoints.

## Features

- ✅ Easy-to-use client for sending telemetry data to Harbor.
- 🧠 Flexible, validation-powered data models using [Pydantic](https://docs.pydantic.dev/).
- 🔁 Automatic retries with exponential backoff for network reliability.
- 📦 Support for sending both single readings and batches.

## Installation

```
pip install telemetry-harbor-sdk
```

## Usage

```python
from harbor_sdk import HarborClient, GeneralReading

client = HarborClient(
    endpoint="https://api.telemetry-harbor.com/v1/ingest/{harbor_id}",
    api_key="your_secret_api_key"
)

# Send a single reading
reading = GeneralReading(
    ship_id="MV-Explorer",
    cargo_id="C-1138",
    value=42.5
)
client.send(reading)

# Send a batch of readings
batch = [
    GeneralReading(ship_id="MV-Explorer", cargo_id="C-1138", value=42.5),
    # Add more readings as needed
]
client.send_batch(batch)
```

## GPS and Cargo Data Rules

When sending GPS data:

- `latitude` and `longitude` are sent as **separate readings**, each using a distinct `cargo_id` (e.g., `"latitude"`, `"longitude"`).
- These readings must share the **same `ship_id` and `timestamp`** to be grouped correctly on the backend.
- This allows location data to be joined in time-series queries for mapping or tracking.

**Example batch:**

```json
[
  {
    "ship_id": "MV-Explorer",
    "cargo_id": "latitude",
    "value": 41.123,
    "timestamp": "2025-07-17T10:00:00Z"
  },
  {
    "ship_id": "MV-Explorer",
    "cargo_id": "longitude",
    "value": 29.456,
    "timestamp": "2025-07-17T10:00:00Z"
  }
]
```

> ✅ This structure supports SQL-based reconstruction of full GPS coordinates using `cargo_id` filters and grouping by `ship_id` and `timestamp`.

**Query Example (PostgreSQL/TimescaleDB):**

```sql
SELECT
    time,
    MAX(value) FILTER (WHERE cargo_id = 'latitude') AS latitude,
    MAX(value) FILTER (WHERE cargo_id = 'longitude') AS longitude,
    ship_id
FROM cargo_data
WHERE $__timeFilter(time)
  AND ship_id IN (${ship_id:sqlstring})
  AND cargo_id IN ('latitude', 'longitude')
GROUP BY time, ship_id
HAVING 
    COUNT(DISTINCT CASE WHEN cargo_id = 'latitude' THEN value END) > 0
    AND COUNT(DISTINCT CASE WHEN cargo_id = 'longitude' THEN value END) > 0
ORDER BY time;
```

## 📚 Full Documentation

For full API reference, model structure, and advanced examples, visit:

👉 [**docs.telemetryharbor.com**](https://docs.telemetryharbor.com)
