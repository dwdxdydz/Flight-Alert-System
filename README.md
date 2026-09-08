# Flight Price Alert System

Automated flight-deal monitoring built with Python. The application reads destinations and subscribers, searches configured flight APIs, compares fares with target prices, and sends email alerts when a deal is found.

## Architecture

```text
Destination data / subscribers
            ↓
       DataManager
            ↓
       FlightSearch
            ↓
     Target-price rule
            ↓
   NotificationManager
            ↓
          Email
```

## Features

- Configurable origin, search horizon, and maximum stopovers
- Automatic IATA-code lookup for destinations
- Normalized flight data model
- Sheety-compatible data persistence layer
- SMTP email notifications
- Environment-based secrets
- `--dry-run` mode for safe testing
- Unit tests for core flight-search behavior

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in the API, data-store, and SMTP values in `.env`.

## Run

```bash
python main.py --dry-run
python main.py
```

## Test

```bash
pytest -q
```

## Production improvements

The application is intentionally provider-agnostic around data storage and notifications. A production deployment can add scheduled execution, retry/backoff, persistent price history, structured metrics, and a dashboard without changing the core alert rule.
