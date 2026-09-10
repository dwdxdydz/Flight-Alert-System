# ✈️ Flight Price Alert & Analytics System

## What is this project?

This is a small application that **checks flight prices automatically** and tells you when a flight becomes cheap enough to buy.

Instead of checking the same flight again and again yourself, the application can:

1. Search for flight prices.
2. Save the prices it finds.
3. Compare the price with your target price.
4. Detect useful price drops.
5. Send an email when a good deal is found.
6. Show the collected prices in a dashboard.

Think of it as a **personal flight-price watchdog**.

## Example

Suppose you want to travel from Amsterdam to another city and you want to pay no more than €300.

The application might see:

```text
Monday     €420
Tuesday    €390
Wednesday  €340
Thursday   €285  ← Target reached!
```

The application saves these prices and can send you an email when the €300 target is reached.

## How does it work?

```text
Flight search settings
        ↓
Search flight API
        ↓
Get flight price
        ↓
Save price in MySQL
        ↓
Compare with previous prices
        ↓
Is this a good deal?
        ↓
      Yes
        ↓
Send email alert
        ↓
Show results in dashboard
```

## What can it do?

- Search flights for configured destinations.
- Automatically find airport codes when needed.
- Track airline, travel dates, stops, duration and price.
- Remember old prices using MySQL.
- Show the lowest, average and latest prices.
- Show how much a price is above or below the target.
- Detect significant price drops.
- Detect a new lowest historical price.
- Send email notifications.
- Retry a failed flight-API request instead of immediately giving up.
- Keep application logs so problems are easier to investigate.
- Run safely in `dry-run` mode while testing.
- Run automatically using GitHub Actions.
- Run automated tests before changes are accepted.

## Why use MySQL?

The application does not only need to know **today's price**. It also needs to remember what the price was yesterday, last week, and so on.

MySQL stores this history.

For example:

```text
Date         Route          Price
----------------------------------
01 Sep       AMS → PAR      €420
03 Sep       AMS → PAR      €390
05 Sep       AMS → PAR      €315
08 Sep       AMS → PAR      €285
```

Because the old prices are stored, the application can answer questions such as:

- What is the cheapest price we have seen?
- What is the average price?
- Is the price going down?
- Is today's price a new low?
- How far are we from the target price?

## Dashboard

The project includes a Streamlit dashboard that turns the stored data into easy-to-read charts and numbers.

It can show:

- Current price
- Lowest price
- Average price
- Price history
- Target price vs actual price
- Cheapest destinations
- Airlines and number of stops

Start it with:

```bash
streamlit run dashboard.py
```

## Email alerts

The application can send an email when a useful event happens, such as:

- The price reaches your target.
- The price drops significantly.
- A new historical low is found.

## Setup

Create a Python environment and install the required packages:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add your flight API, email and MySQL details to `.env`.

Example MySQL settings:

```text
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=flight_alert
```

The application creates the required database table when it starts, provided the MySQL account has permission to do so.

## Run the application

Test without sending real alerts:

```bash
python main.py --dry-run
```

Run normally:

```bash
python main.py
```

## Run tests

```bash
pytest -q
```

## Main technologies

- **Python** — application logic
- **Flight API** — gets current flight prices
- **MySQL** — stores price history
- **Streamlit** — creates the dashboard
- **Plotly** — creates interactive charts
- **SMTP** — sends emails
- **GitHub Actions** — runs the monitoring job and tests automatically

## Project structure

```text
main.py                 → Runs the application
flight_search.py        → Searches for flights
data_manager.py        → Reads destination/subscriber data
database.py             → Saves data in MySQL
analytics.py            → Calculates useful statistics
alert_engine.py         → Decides when an alert should be sent
notification_manager.py → Sends email notifications
flight_data.py          → Represents a flight result
dashboard.py            → Displays the analytics dashboard
tests/                  → Automated tests
.github/workflows/      → Automatic scheduled runs and CI
```

## What I learned from this project

This project started as a simple flight-price alert script and was expanded into a complete application.

It demonstrates how a real application can connect several pieces together:

**API → data collection → database → analysis → dashboard → notification → automation**

It is especially useful for demonstrating Python, SQL/MySQL, data analysis, dashboards, APIs and automation skills.

## Future improvements

- Add more dashboard filters.
- Predict future flight prices.
- Detect unusual price changes automatically.
- Deploy the application to the cloud.
- Add a cloud database.
