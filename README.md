# ✈️ Flight Price Alert & Analytics System

## What is this project?

This application checks flight prices automatically and tells you when a flight becomes cheap enough to consider.

Instead of checking the same routes every day yourself, the application can:

1. Search for flight prices.
2. Save every successful price check.
3. Compare the current price with your target price.
4. Compare today's price with older prices.
5. Detect useful price drops and new historical lows.
6. Send an email when a good deal is found.
7. Show the price history in a dashboard.

Think of it as a **personal flight-price watchdog**.

## Example

Suppose your target price for a route is €300:

```text
Monday     €420
Tuesday    €390
Wednesday  €340
Thursday   €285  ← Target reached!
```

The application saves these observations and can send an email when the price reaches the target.

## How does it work?

```text
Flight settings
      ↓
Flight API
      ↓
Flight information
      ↓
MySQL database
      ↓
Price analysis
      ↓
Is this a good deal?
   ↓           ↓
  Yes          No
   ↓            ↓
Email alert   Finish

      ↓
Streamlit dashboard
```

## Main features

- Searches configured flight routes
- Finds airport **IATA codes** automatically when needed
- Tracks airline, travel dates, stops, duration and price
- Stores historical prices in **MySQL**
- Calculates lowest, average and latest prices
- Compares actual price with the target price
- Detects significant price drops
- Detects new historical lows
- Sends email notifications
- Retries failed API requests using **exponential backoff**
- Keeps application logs for troubleshooting
- Supports `--dry-run` for safe testing
- Runs automatically with **GitHub Actions**
- Includes automated tests

## Why store historical prices?

The interesting part of this project is not just finding today's price. It is remembering previous prices.

For example:

```text
Date       Route       Price
----------------------------
01 Sep     AMS → PAR   €420
03 Sep     AMS → PAR   €390
05 Sep     AMS → PAR   €315
08 Sep     AMS → PAR   €285
```

Because the application has this history, it can answer questions such as:

- What is the cheapest price we have seen?
- What is the average price?
- Is the price falling?
- Is this a new lowest price?
- How far is the current price from the target?

## Dashboard

The project includes a **Streamlit** dashboard that turns the stored data into charts and useful numbers.

It can show:

- Current, lowest and average price
- Target price vs actual price
- Price history
- Cheapest destinations
- Airline information
- Number of stops

Start it with:

```bash
streamlit run dashboard.py
```

## Email alerts

The application can send an email when an important event happens, for example:

- Price reaches the target
- Price drops significantly
- New historical low is found

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add your flight API, email and MySQL details to `.env`.

Example:

```text
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=flight_alert
```

## Run

Test without sending real alerts:

```bash
python main.py --dry-run
```

Run normally:

```bash
python main.py
```

Run the dashboard:

```bash
streamlit run dashboard.py
```

Run tests:

```bash
pytest -q
```

## Project structure

```text
main.py                  → Starts the application
flight_search.py         → Searches for flights
data_manager.py         → Handles destination/subscriber data
database.py              → Stores prices in MySQL
analytics.py             → Calculates statistics
alert_engine.py          → Decides when an alert is useful
notification_manager.py → Sends email alerts
flight_data.py           → Stores flight information
dashboard.py             → Shows the dashboard
tests/                   → Automated tests
.github/workflows/       → Scheduled jobs and CI
```

## Technical terms explained

**API** — A way for one application to communicate with another. Here, the flight API provides flight information and prices.

**IATA code** — The standard short code used for airports, such as `BLR` for Bengaluru and `LHR` for London Heathrow.

**MySQL** — A database system that stores information in tables. This project uses it to remember flight prices.

**SQL** — The language used to search, filter and calculate information inside a database.

**Analytics** — Using stored data to calculate useful information such as averages, lowest prices and trends.

**Streamlit** — A Python framework for quickly building web applications, especially data dashboards.

**Plotly** — A library for creating interactive charts.

**SMTP** — A standard method used by applications to send email.

**Exponential backoff** — If an API request fails, the application waits before trying again. The waiting time becomes longer after repeated failures.

**Logging** — Recording useful information about what the application is doing, especially when something goes wrong.

**GitHub Actions** — A GitHub feature that can automatically run code, tests or scheduled jobs. This project uses it for automation and CI.

**CI (Continuous Integration)** — Automatically checking code changes, usually by running tests, so problems are found early.

## What does this project demonstrate?

This project connects several common parts of software development into one application:

**API → data collection → database → analytics → dashboard → alerts → automation**

It demonstrates practical **Python, SQL/MySQL, APIs, data analysis, dashboards, testing and automation** skills.

## Future improvements

- Predict future flight prices
- Detect unusual price changes
- Add more dashboard filters
- Deploy the application to the cloud
- Use a cloud database
