# ✈️ Flight Price Alert & Analytics System

An automated flight-price monitoring and analytics application built with **Python, MySQL, Streamlit, and Plotly**. It searches configured routes, stores historical fare observations, compares prices with target thresholds, generates analytics, and sends email alerts for qualifying deals.

## Why this project?

The project evolved from a simple flight-price alert script into an end-to-end data application demonstrating **API integration, data collection, relational database design, SQL analytics, dashboarding, automation, testing, and alerting**.

## Architecture

```text
Destination / subscriber data
            ↓
       DataManager
            ↓
       FlightSearch
            ↓
      FlightData model
            ↓
       MySQL history
        ↙         ↘
   Analytics     Alert Engine
      ↓              ↓
 Streamlit         Email
      ↓
    Plotly
```

## Features

- Configurable origin, search horizon, and maximum stopovers
- Automatic IATA airport-code lookup
- Normalized flight data model
- Airline, duration, route, date, stopover, and fare tracking
- Historical price persistence in **MySQL**
- Timestamped price observations
- Lowest, average, and latest price analytics
- Target-vs-actual variance analysis
- Historical price trend visualization with Plotly
- Cheapest-destination ranking
- Price-drop and historical-low alert rules
- SMTP email notifications
- Retry/backoff for API requests
- Application logging
- `--dry-run` mode
- Unit tests and GitHub Actions CI

## Database

Each successful flight search is stored in the `flight_prices` table with the search timestamp, route, travel dates, airline, stops, fare, currency, duration, target price, and booking URL.

The historical dataset makes it possible to analyze price trends instead of evaluating only the current fare.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configure the flight API, SMTP, data-source, and MySQL credentials in `.env`.

Example:

```text
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=flight_alert
```

The application initializes the required historical table when it starts, provided the MySQL user has the necessary permissions.

## Collect flight prices

```bash
python main.py --dry-run
python main.py
```

Every successful search is persisted before alert rules are evaluated.

## Dashboard

After collecting observations:

```bash
streamlit run dashboard.py
```

The dashboard provides current/lowest/average fares, target-vs-actual variance, interactive price trends, airline and stopover information, and cheapest-destination rankings.

## Testing

```bash
pytest -q
```

## Configuration

Important variables include `ORIGIN_AIRPORT` (default `AMS`), `SEARCH_WEEKS` (default `26`), `MAX_STOPOVERS` (default `0`), `LOG_LEVEL` (default `INFO`), `SMTP_PORT` (default `587`), MySQL settings, API credentials, and SMTP credentials.

## Portfolio value

- **Data Analyst:** SQL, historical datasets, KPIs, trends, variance analysis, Plotly
- **Business Analyst:** target-vs-actual analysis, business rules, decision-support dashboard
- **Python/SDE:** API integration, database layer, retries, logging, testing, automation

## Future improvements

- Advanced dashboard filters and KPIs
- Price forecasting
- Route-level anomaly detection
- Containerized deployment
- Cloud database deployment
