# Telemetry Harbor Python SDK

<!-- Telemetry Harbor SDK Badges -->

<!-- PyPI -->
![PyPI](https://img.shields.io/pypi/v/telemetry-harbor-sdk.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/telemetry-harbor-sdk.svg)
![Downloads](https://img.shields.io/pypi/dm/telemetry-harbor-sdk.svg)
![License](https://img.shields.io/pypi/l/telemetry-harbor-sdk.svg)
![Wheel](https://img.shields.io/pypi/wheel/telemetry-harbor-sdk.svg)
![Format](https://img.shields.io/pypi/format/telemetry-harbor-sdk.svg)
![Status](https://img.shields.io/pypi/status/telemetry-harbor-sdk.svg)

<!-- GitHub -->
![Build](https://github.com/TelemetryHarbor/harbor-sdk-python/actions/workflows/publish-to-pypi.yml/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/TelemetryHarbor/harbor-sdk-python.svg)
![Issues](https://img.shields.io/github/issues/TelemetryHarbor/harbor-sdk-python.svg)
![Pull Requests](https://img.shields.io/github/issues-pr/TelemetryHarbor/harbor-sdk-python.svg)
![Repo Size](https://img.shields.io/github/repo-size/TelemetryHarbor/harbor-sdk-python.svg)
![Contributors](https://img.shields.io/github/contributors/TelemetryHarbor/harbor-sdk-python.svg)

<!-- Fun / Community -->
![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Stars](https://img.shields.io/github/stars/TelemetryHarbor/harbor-sdk-python.svg?style=social)
![Forks](https://img.shields.io/github/forks/TelemetryHarbor/harbor-sdk-python.svg?style=social)

A modern, production-ready SDK for sending telemetry data to the **Telemetry Harbor** service from any Python application.

This SDK simplifies data sending by handling HTTP communication, JSON serialization, and robust error handling with automatic retries.

For full details and advanced usage, please see our official documentation at [docs.telemetryharbor.com](https://docs.telemetryharbor.com).

***

## Features

* ✅ **Pydantic Models** for strong validation and ease of use.
* 🔁 **Automatic Retries** with exponential backoff for network resilience.
* 📦 **Batch Support** for efficient multi-reading uploads.
* ⚙️ **Simple API** with intuitive methods like `send` and `send_batch`.
* 🌐 **Universal** — works in any Python 3.7+ environment.

***

## Installation

```bash
pip install telemetry-harbor-sdk
````

---

## Quickstart Guide

Here is a basic example of how to use the SDK.

```python
from telemetryharborsdk import HarborClient, GeneralReading

# 1. Initialize the client
client = HarborClient(
    endpoint="https://api.telemetry-harbor.com/v1/ingest/{harbor_id}",
    api_key="your_secret_api_key"
)

# 2. Create a reading
reading = GeneralReading(
    ship_id="MV-Explorer",
    cargo_id="C-1138",
    value=42.5
)

# 3. Send the reading
response = client.send(reading)
print("Successfully sent data!", response)

# --- Or send a batch ---
batch = [
    GeneralReading(ship_id="MV-Explorer", cargo_id="C-1138", value=42.5),
    GeneralReading(ship_id="MV-Explorer", cargo_id="temperature", value=21.7),
]
batch_response = client.send_batch(batch)
print("Successfully sent batch!", batch_response)
```

---

## GPS and Cargo Data Rules

When sending GPS coordinates, send `latitude` and `longitude` as separate readings with:

* The same `ship_id` and `timestamp`.
* Distinct `cargo_id`s `"latitude"` and `"longitude"`.

This allows proper grouping in the backend for time-series queries.

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

> ✅ This enables SQL queries to reconstruct full GPS points by grouping on `ship_id` and `timestamp`.

**Query example (PostgreSQL/TimescaleDB):**

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
ORDER BY time;
```

---

## API Reference

### `HarborClient(endpoint, api_key, max_retries=5, initial_backoff=1.0)`

Create a new client instance.

* `endpoint` (str): Telemetry Harbor ingestion URL.
* `api_key` (str): Your API key.
* `max_retries` (int, optional): Retry attempts on failure (default 5).
* `initial_backoff` (float, optional): Initial backoff in seconds (default 1.0).

### `send(reading: GeneralReading)`

Send a single telemetry reading.

### `send_batch(readings: List[GeneralReading])`

Send multiple readings in a batch.

