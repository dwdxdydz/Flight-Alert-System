# Flight Price Alert System

An automated flight-price monitoring and analytics application built with Python, MySQL, Streamlit and Plotly. It searches configured routes, stores every observed fare, compares prices with target thresholds, provides historical analytics, and sends email alerts for qualifying deals.

## Architecture

```text
Destination data / subscribers
            ↓
       DataManager
            ↓
       FlightSearch
            ↓
      FlightData model
            ↓
       MySQL history
        ↙         ↘
   Analytics     Alert rule
      ↓              ↓
 Streamlit         Email
      ↓
    Plotly
```

## Features

- Configurable origin, search horizon, and maximum stopovers
- Automatic IATA-code lookup for destinations
- Normalized flight data model with airline and duration
- Historical price persistence in MySQL
- Timestamped route, date, airline, stopover and fare observations
- Dashboard metrics for current, lowest and average prices
- Target-vs-actual price variance
- Historical price trend visualization with Plotly
- Cheapest-destination ranking
- SMTP email notifications
- Environment-based secrets
- `--dry-run` mode for safe alert testing
- Unit tests for flight parsing and analytics
- GitHub Actions CI

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configure the API, SMTP and MySQL values in `.env`. The application can create the configured MySQL database and its `flight_prices` table automatically, provided the MySQL user has permission to create databases.

Required MySQL variables:

```text
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=flight_alert
```

## Collect historical prices

```bash
python main.py --dry-run
python main.py
```

Every successful flight search is persisted before the alert threshold is evaluated. This creates the historical dataset used by the dashboard.

## Dashboard

After collecting observations:

```bash
streamlit run dashboard.py
```

The dashboard provides:

- Current, lowest and average fare
- Target-vs-actual variance
- Interactive historical price trend
- Airline and stopover information in chart tooltips
- Cheapest destinations from the configured origin

## Test

```bash
pytest -q
```

## Environment variables

The main application supports `ORIGIN_AIRPORT` (default `AMS`), `SEARCH_WEEKS` (default `26`), `MAX_STOPOVERS` (default `0`), `SMTP_PORT` (default `587`) and `LOG_LEVEL` (default `INFO`), in addition to the API, SMTP and MySQL credentials.

## Roadmap

- Scheduled execution
- Retry with exponential backoff
- Structured application logging and run metrics
- Smarter alerts for significant price drops and new historical lows
- Additional dashboard filters and business KPIs
