# Flight Alert System

A small Python service that searches for inexpensive return flights and emails
subscribers when a configured price target is met.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and replace every placeholder with your API and
   SMTP credentials.
4. Configure the `prices` and `users` sheets in your Sheety-compatible endpoint.

The `prices` resource needs `city`, `iataCode`, and `lowestPrice` fields. The
`users` resource needs an `email` field. Missing airport codes are looked up and
written back to the price row automatically.

## Run

Use the subscriber CLI to add a user:

```bash
python Customer.py
```

Run the scheduled alert search manually:

```bash
python main.py
```

Useful optional environment variables are `ORIGIN_AIRPORT` (default `AMS`),
`SEARCH_WEEKS` (default `26`), `MAX_STOPOVERS` (default `0`), and `SMTP_PORT`
(default `587`). The first search is constrained by `MAX_STOPOVERS`; when a
direct-flight search has no result, the service retries with up to two stops.

## Test

```bash
python -m pytest -q
```

## Security

Keep `.env` private. Use an app password for the SMTP account rather than the
account's primary password, and rotate credentials if they are exposed.
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
